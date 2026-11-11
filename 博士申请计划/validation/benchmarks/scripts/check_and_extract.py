#!/usr/bin/env python3
"""Check pinned public files and export complete neutron measurements, without OpenMC."""
from pathlib import Path
import csv, json, hashlib, zipfile, ast, sys
import h5py
import numpy as np
BASE=Path(__file__).resolve().parent.parent
CASES={
 'fng_w':['rr_nb93','rr_al27','rr_fe56','rr_ni58_np','rr_au197','rr_mn55','rr_zr90'],
 'fng_str':['rr_onaxis1_nb93','rr_onaxis1_al27','rr_onaxis1_ni58','rr_onaxis2_nb93','rr_onaxis2_al27','rr_offaxis_nb93'],
 'oktavian_cu':['nspectrum'],
}
def run():
 out=BASE/'measurements';out.mkdir(exist_ok=True);summary=[]
 with zipfile.ZipFile(BASE/'public_inputs_c47fc57.zip')as z:
  manifest=json.loads(z.read('manifest.json'))
  for r in manifest['files']:
   assert hashlib.sha256(z.read(r['path'])).hexdigest()==r['sha256'],r['path']
  for case,keys in CASES.items():
   data=z.read(f'upstream/results_database/{case}/experiment.h5')
   import io
   with h5py.File(io.BytesIO(data),'r')as f:
    for key in keys:
     table=f[key]['table'][()]
     # Do not drop, fill or interpolate any row in a selected channel.
     assert np.isfinite(table['mean']).all(),(case,key,'missing measurement')
     assert np.isfinite(table['std. dev.']).all(),(case,key,'missing error')
     assert (table['std. dev.']>0).all(),(case,key,'nonpositive error')
     assert (table['mean']>=0).all(),(case,key,'negative measurement')
     if 'energy low [eV]'in table.dtype.names:
      lo=table['energy low [eV]'];hi=table['energy high [eV]']
      assert (hi>lo).all()and (np.diff(lo)>0).all(),(case,key,'energy bins')
     path=out/(case+'__'+key+'.csv')
     with path.open('w',encoding='utf-8',newline='')as g:
      w=csv.writer(g);w.writerow(table.dtype.names)
      for row in table:
       w.writerow([v.decode()if isinstance(v,bytes)else v.item()if isinstance(v,np.generic)else v for v in row])
     summary.append({'case':case,'channel':key,'rows':len(table),'measurement_file':str(path.relative_to(BASE)),'raw_sha256':hashlib.sha256(data).hexdigest()})
  for case,modelpath in [('fng_w','fng_w'),('fng_str','fng_str'),('oktavian_cu','oktavian/oktavian_cu')]:
   ast.parse(z.read(f'upstream/models/{modelpath}/openmc_model.py').decode())
 (BASE/'selected_channels.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'checked_files':len(manifest['files']),'complete_channels':len(summary),'measurement_rows':sum(r['rows']for r in summary),'simulations_run':False},ensure_ascii=False))
if __name__=='__main__':run()
