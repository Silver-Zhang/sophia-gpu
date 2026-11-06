"""Rebuild the package offline from committed prose, records and figure code."""
from pathlib import Path
import os,sys,subprocess,re,json,shutil
from docx import Document
from pypdf import PdfReader
B=Path(__file__).resolve().parent;PY=sys.executable
BIN=Path(PY).parent;ENGINE=BIN/'md-to-word'
RENDER=Path(os.environ.get('DOCX_RENDERER',str(Path.home()/'.codex/plugins/cache/openai-primary-runtime/documents/26.1104.11149/skills/documents/render_docx.py')))
def run(script):subprocess.run([PY,str(B/script)],cwd=B,check=True)
run('build_figures.py');run('assemble_manuscript.py');run('build_bibliography.py')
env=os.environ.copy();env['FONTCONFIG_FILE']=str(B/'qa/fonts.conf')
doc=B/'outputs/博士研究设想_导师讨论初稿.docx'
render=B/'qa/render_final'
for attempt in range(3):
 subprocess.run([str(ENGINE),'manuscript.md','-f','format.txt','-o',doc.name,'--json'],cwd=B/'outputs',check=True)
 run('finalize_docx.py')
 subprocess.run([PY,str(RENDER),str(doc),'--output_dir',str(render),'--emit_pdf'],env=env,cwd=B,check=True)
 pages=[''.join(p.extract_text().split()) for p in PdfReader(render/(doc.stem+'.pdf')).pages]
 mp={}
 for p in Document(doc).paragraphs:
  if p.style.name in ['Heading 1','Heading 2','References Title']:
   match=[i+1 for i,t in enumerate(pages) if i>1 and ''.join(p.text.split()) in t]
   if not match:raise ValueError(p.text)
   mp[p.text]=match[0]
 mfile=B/'qa/toc_page_map.json';previous=json.loads(mfile.read_text()) if mfile.exists() else {}
 mfile.write_text(json.dumps(mp,ensure_ascii=False,indent=2))
 if mp==previous:break
else:raise RuntimeError('Contents pagination did not stabilize')
shutil.copy2(render/(doc.stem+'.pdf'),B/'outputs'/(doc.stem+'.pdf'))
run('verify_package.py')
print('Rebuild complete. Inspect all newly rendered pages before delivery.')
