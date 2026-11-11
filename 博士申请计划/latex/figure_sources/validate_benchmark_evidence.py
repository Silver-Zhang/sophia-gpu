"""Audit pinned public benchmark inputs and the selected experimental records."""
from pathlib import Path
import zipfile,json,hashlib,io,re
import numpy as np
import h5py
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'latex/references/benchmark_evidence_audit.json'
REACTIONS={
 'fng_w':{'rr_nb93':'93Nb(n,2n)92mNb','rr_al27':'27Al(n,alpha)24Na','rr_fe56':'56Fe(n,p)56Mn','rr_ni58_np':'58Ni(n,p)58Co','rr_au197':'197Au(n,gamma)198Au','rr_mn55':'55Mn(n,gamma)56Mn','rr_zr90':'90Zr(n,2n)89Zr'},
 'fng_str':{'rr_onaxis1_nb93':'93Nb(n,2n)92mNb','rr_onaxis1_al27':'27Al(n,alpha)24Na','rr_onaxis1_ni58':'58Ni(n,p)58Co','rr_onaxis2_nb93':'93Nb(n,2n)92mNb','rr_onaxis2_al27':'27Al(n,alpha)24Na','rr_offaxis_nb93':'93Nb(n,2n)92mNb'},
 'oktavian_cu':{'nspectrum':'leakage neutron spectrum'}}
with zipfile.ZipFile(ROOT/'validation/benchmarks/public_inputs_c47fc57.zip')as z:
 manifest=json.loads(z.read('manifest.json'))
 assert manifest['commit']=='c47fc573a7e2a9ca11a8958dc67155b1146adf51'
 for row in manifest['files']:assert hashlib.sha256(z.read(row['path'])).hexdigest()==row['sha256']
 report={'repository':manifest['repository'],'commit':manifest['commit'],'checked_files':len(manifest['files']),'channels':[],'sources':{},'simulations_run':False}
 for case,channels in REACTIONS.items():
  name='upstream/results_database/'+case+'/experiment.h5';raw=z.read(name)
  with h5py.File(io.BytesIO(raw),'r')as f:
   for key,reaction in channels.items():
    tab=f[key]['table'][()];mean=tab['mean'];error=tab['std. dev.']
    assert np.isfinite(mean).all()and np.isfinite(error).all()and (mean>0).all()and (error>0).all()
    row={'case':case,'reaction':reaction,'file':name,'table':key,'rows':len(tab),'relative_reported_error_range':[float(min(error/mean)),float(max(error/mean))],'file_sha256':hashlib.sha256(raw).hexdigest()}
    if 'energy low [eV]'in tab.dtype.names:
     lo=tab['energy low [eV]'];hi=tab['energy high [eV]'];assert (hi>lo).all()and (np.diff(lo)>0).all()
     row['energy_bounds_eV']=[float(lo[0]),float(hi[-1])];row['contiguous_bins']=bool(np.all(lo[1:]==hi[:-1]))
    else:row['measurement_labels']=[str(v.decode()if isinstance(v,bytes)else v)for v in tab['Shield depth (cm)']]
    report['channels'].append(row)
 for keV in [230,260]:
  name=f'upstream/src/openmc_fusion_benchmarks/neutron_sources/fng_source/fng_{keV}keV_characteristics.csv'
  source=np.loadtxt(io.BytesIO(z.read(name)),delimiter=',');assert source.shape[0]==38 and np.isfinite(source).all()and (np.diff(source[0])>0).all()
  report['sources'][f'fng_{keV}keV']={'file':name,'angular_bins':36,'energy_columns':int(source.shape[1]),'energy_bounds_eV':[float(source[0,0]),float(source[1,-1])]}
 report['counts']={case:sum(r['rows']for r in report['channels']if r['case']==case)for case in REACTIONS}
 assert report['counts']=={'fng_w':28,'fng_str':76,'oktavian_cu':140}
 model=z.read('upstream/models/oktavian/oktavian_cu/openmc_model.py').decode()
 helpers=z.read('upstream/models/oktavian/oktavian_cu/helpers.py').decode()
 assert 'r=30.5'in model and 'r = 19.95'in helpers
 report['known_issues']=[
  {'case':'oktavian_cu','file':'models/oktavian/oktavian_cu/helpers.py','issue':'helpers.surface uses r=19.95 cm, while nspectrum is a surface-current tally on surf_6 at r=30.5 cm.','treatment':'Do not use this script or its stored OpenMC spectra as an absolute reference without resolving the area normalization. Figure 7 uses the independently published MCNP-4C3/JEFF-3.1 comparison, not these stored OpenMC results.'},
  {'case':'oktavian_cu','issue':'The stored MCNP low-energy underflow interval starts at zero, whereas the experiment table starts at 76399 eV.','treatment':'No row-wise C/E combination or spectrum rebinning between those raw tables was used for the new figure.'},
  {'case':'fng_w','issue':'The model calls the legacy irdff.path/cross_section interface, while the packaged module exposes get_cross_section.','treatment':'Keep the pinned files immutable as provenance. A runnable transport environment requires API adaptation, which is outside this manuscript/figure edit.'},
  {'case':'fng_w and fng_str','issue':'Raw HDF fields are mean and std. dev.; the full error covariance and coverage-factor metadata are not stored. IRDFF cross-section ordinates in the source reader are in barns.','treatment':'Preserve the reported fields and original scripts; no unverified absolute-rate conversion, covariance assumption or one-sigma interpretation is added to the figure or prose.'}]
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'verified_files':report['checked_files'],'counts':report['counts'],'simulations_run':False},ensure_ascii=False))
