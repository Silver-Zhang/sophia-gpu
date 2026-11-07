"""Compile V3 through md-to-word, then render and resolve static clickable TOC."""
from pathlib import Path
import os,sys,subprocess,json,shutil
from docx import Document
from pypdf import PdfReader
V=Path(__file__).resolve().parents[1];B=V.parents[1];PY=sys.executable
from safety_v3 import require_v3_root
require_v3_root(V)
assert json.loads((V/'authorization.json').read_text())['approved'] is True
ENGINE=Path(PY).parent/'md-to-word'
RENDER=Path(os.environ.get('DOCX_RENDERER',str(Path.home()/'.codex/plugins/cache/openai-primary-runtime/documents/26.1104.11149/skills/documents/render_docx.py')))
for s in ['assemble_v3.py','check_protection_v3.py']:
 subprocess.run([PY,str(V/'scripts'/s)],check=True)
env=os.environ.copy();env['FONTCONFIG_FILE']=str(V/'qa/fonts.conf')
doc=V/'exports/博士科研计划书_V3.docx';render=V/'qa/render_final'
for attempt in range(3):
 r=subprocess.run([str(ENGINE),'manuscript_v3.md','-f','format.txt','-o',doc.name,'--json'],cwd=V/'exports',capture_output=True,text=True)
 (V/f'qa/engine_export_{attempt+1}.log').write_text((r.stdout+'\n'+r.stderr).strip()+'\n')
 if r.returncode:print(r.stdout,r.stderr);r.check_returncode()
 subprocess.run([PY,str(V/'scripts/finalize_v3.py')],check=True)
 # Remove only generated page images so a shorter revision leaves no stale pages.
 if render.exists():
  for old in render.glob('page-*.png'):old.unlink()
 r=subprocess.run([PY,str(RENDER),str(doc),'--output_dir',str(render),'--emit_pdf'],env=env,cwd=V,capture_output=True,text=True)
 (V/f'qa/render_export_{attempt+1}.log').write_text((r.stdout+'\n'+r.stderr).strip()+'\n')
 if r.returncode:print(r.stdout,r.stderr);r.check_returncode()
 pages=[''.join(p.extract_text().split()) for p in PdfReader(render/(doc.stem+'.pdf')).pages]
 mp={}
 for p in Document(doc).paragraphs:
  if p.style.name in ['Heading 1','Heading 2','References Title']:
   match=[i+1 for i,t in enumerate(pages) if i>0 and ''.join(p.text.split()) in t]
   if not match:raise ValueError(p.text)
   mp[p.text]=match[0]
 mfile=V/'qa/toc_page_map.json';previous=json.loads(mfile.read_text()) if mfile.exists() else {}
 mfile.write_text(json.dumps(mp,ensure_ascii=False,indent=2)+'\n')
 print('Render',attempt+1,':',len(pages),'pages;',len(mp),'TOC entries')
 if mp==previous:break
else:raise RuntimeError('Contents pagination did not stabilize')
shutil.copy2(render/(doc.stem+'.pdf'),V/'exports'/(doc.stem+'.pdf'))
print('V3 Word/PDF generated; all pages require visual inspection before delivery.')
