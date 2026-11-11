"""Recover the original figure inputs. Usage: python extract_benchmark_sources.py SOURCE_DIR
SOURCE_DIR contains the three PDFs listed in benchmark_visuals/sources.json.
"""
from pathlib import Path
import fitz,csv,json,hashlib,zipfile,sys
SOURCE_DIR=Path(sys.argv[1])
dest=Path(__file__).resolve().parent/'benchmark_visuals';dest.mkdir(exist_ok=True)
# Native Figure 3 image, unchanged pixels; CMYK->RGB for inclusion, no resampling.
d=fitz.open(str(SOURCE_DIR/'fngstr.pdf'));im=d[5].get_images(full=True)[1];assert im[0]==749
pix=fitz.Pixmap(d,749);pix=fitz.Pixmap(fitz.csRGB,pix);pix.save(dest/'fng_streaming_fig3.png');assert(pix.width,pix.height)==(1016,903)
# Recover numeric observations from the vector plot, not a screenshot or an interpolated raster.
p=fitz.open(str(SOURCE_DIR/'jeff_appendix2.pdf'))[29];ds=p.get_drawings()
x0=75.26605224609375;x1=164.16009521484375;y10=63.77838134765625;y1=102.69366455078125
E=lambda x:.1*10**((x-x0)/(x1-x0))
V=lambda y:10**((y1-y)/(y1-y10))
exp=[]
for i in range(11,265,2):
 r=ds[i]['rect'];x=(r.x0+r.x1)/2;y=(r.y0+r.y1)/2
 assert y>90
 # Match each vertical errorbar in the same spectrum panel.
 bars=[]
 for j in [9,10]:
  for item in ds[j]['items']:
   if item[0]!='l':continue
   a,b=item[1:]
   if abs(a.x-b.x)<.002 and abs(a.x-x)<.06 and min(a.y,b.y)<=y<=max(a.y,b.y)and min(a.y,b.y)>90:bars.append((min(a.y,b.y),max(a.y,b.y)))
 assert len(bars)==1,(i,x,y,bars)
 yl,yh=bars[0];exp.append([E(x),V(y),V(yh),V(yl)])
exp.sort();assert len(exp)==127
calc=[]
for item in ds[267]['items'][1:]:
 a,b=item[1:]
 if abs(a.y-b.y)<.002 and b.x>a.x and a.y<190:calc.append([E(a.x),E(b.x),V(a.y)])
assert len(calc)>120
# The original C/E plot uses plus-cross symbols composed of four vector paths.
ce=[];cx0=308.4527282714844;cx1=398.74749755859375;cy0=200.89056396484375;cy2=63.77838134765625
for i in range(548,1050,4):
 r=ds[i]['rect'];x=(r.x0+r.x1)/2;y=(r.y0+r.y1)/2
 if r.y0>220:break
 if y<90:continue # legend glyph, not a datum
 assert r.width<.002
 bars=[]
 for j in [546,547]:
  for item in ds[j]['items']:
   if item[0]!='l':continue
   a,b=item[1:]
   if abs(a.x-b.x)<.002 and abs(a.x-x)<.06 and min(a.y,b.y)<=y<=max(a.y,b.y):bars.append((min(a.y,b.y),max(a.y,b.y)))
 assert len(bars)==1,(i,x,y,bars)
 lo,hi=bars[0];ce.append([.1*10**((x-cx0)/(cx1-cx0)),2*(cy0-y)/(cy0-cy2),2*(cy0-hi)/(cy0-cy2),2*(cy0-lo)/(cy0-cy2)])
ce.sort()
benchmark_error=[]
for j in [278,279]:
 for item in ds[j]['items']:
  if item[0]!='l':continue
  a,b=item[1:]
  if abs(a.x-b.x)<.002 and min(a.y,b.y)<132.334<max(a.y,b.y):
   benchmark_error.append([.1*10**((a.x-cx0)/(cx1-cx0)),2*(cy0-max(a.y,b.y))/(cy0-cy2),2*(cy0-min(a.y,b.y))/(cy0-cy2)])
benchmark_error.sort()
with (dest/'jeff_cu_benchmark_uncertainty.csv').open('w',newline='')as f:
 w=csv.writer(f);w.writerow(['energy_MeV','lower_CE','upper_CE']);w.writerows(benchmark_error)
for name,heads,rows in [('jeff_cu_experiment.csv',['energy_MeV','spectrum','lower','upper'],exp),('jeff_cu_mcnp.csv',['energy_low_MeV','energy_high_MeV','spectrum'],calc),('jeff_cu_ce.csv',['energy_MeV','CE','lower','upper'],ce)]:
 with (dest/name).open('w',newline='')as f:w=csv.writer(f);w.writerow(heads);w.writerows(rows)
facts={'Kobayashi':{'domain_octant_cm':[60,100,60],'source_box_cm':[[0,10],[0,10],[0,10]],'void_boxes_cm':[[[0,10],[10,60],[0,10]],[[10,40],[50,60],[0,10]],[[30,40],[50,60],[10,40]],[[30,40],[60,100],[30,40]]],'Sigma_t_source_shield_cm-1':.1,'Sigma_t_void_cm-1':1e-4,'source_density_n_cm-3_s-1':1},'FNG_W':{'shield_depth_cm':49,'source_distance_cm':5.3,'central_measurement_layer_height_cm':7,'approx_foil_depth_groups_cm':[5,15,25,35],'exact_depth_groups_cm':[[4.94,14.94,24.94,34.94],[5.04,15.04,25.04,35.04],[5.09,15.09,25.09,35.09],[5.1,15.1,25.1,35.1]]}}
(dest/'geometry_parameters.json').write_text(json.dumps(facts,indent=2)+'\n')
manifest={'sources':[{'id':'kobayashi_oecd','url':'https://www.oecd-nea.org/upload/docs/application/pdf/2020-01/nsc-doc2000-4.pdf','sha256':hashlib.sha256((SOURCE_DIR/'kobayashi_oecd.pdf').read_bytes()).hexdigest(),'use':'Original geometry based on factual dimensions in figures 5–8 and table 1; no original artwork reproduced.'},{'id':'fng_streaming','url':'https://dspace.mit.edu/bitstreams/c44a5194-a199-4294-93c7-7b41645b9387/download','doi':'10.1080/15361055.2024.2400762','sha256':hashlib.sha256((SOURCE_DIR/'fngstr.pdf').read_bytes()).hexdigest(),'use':'Figure 3 native 1016x903 image; CC BY 4.0, copyright the authors, no scientific edits.'},{'id':'jeff_cu','url':'https://www.oecd-nea.org/upload/docs/application/pdf/2020-08/jefreport-21_appendix2.pdf','sha256':hashlib.sha256((SOURCE_DIR/'jeff_appendix2.pdf').read_bytes()).hexdigest(),'figure':'3.7','page_pdf':30,'page_report':'13-52','use':'Numeric coordinates extracted from vector marks and error bars; original graph artwork not reproduced. 127 spectrum observations, '+str(len(calc))+' calculated energy intervals, '+str(len(ce))+' C/E marks within the published axes. Distinct from the c47fc57 140-bin table.'}],'figure_contract':{'A':'Idealized dog-leg transport geometry versus realistic layered FNG streaming geometry. Schematic/image mixed plate, no quantitative shared axes.','B':'Thickness and foil depth in FNG-W versus energy-resolved Cu leakage response. Mixed geometry and spectrum/C/E, all numerical uncertainties retained from the source plot.'}}
(dest/'sources.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('Extracted',len(exp),'spectrum observations,',len(calc),'MCNP intervals,',len(ce),'C/E marks; native FNG image',pix.width,pix.height)
