"""Rebuild in an isolated V3 subdirectory; never overwrite final deliverables."""
from pathlib import Path
import shutil,sys,subprocess,os,json,hashlib
V=Path(__file__).resolve().parents[1];T=V/'qa/rebuild_sandbox'
from safety_v3 import require_v3_root
require_v3_root(V)
assert not T.exists(),'Test sandbox exists; inspect before a repeat'
for name in ['sources','bibliography','tables','figures','scripts','planning']:
 shutil.copytree(V/name,T/name,ignore=shutil.ignore_patterns('v3_sources','*_sources','__pycache__','*.pyc'))
(T/'qa').mkdir();(T/'exports').mkdir()
for name in ['fonts.conf','V2_Git交付文件_基准哈希.json']:shutil.copy2(V/'qa'/name,T/'qa'/name)
for name in ['format.txt']:shutil.copy2(V/'exports'/name,T/'exports'/name)
shutil.copy2(V/'authorization.json',T/'authorization.json')
env=os.environ.copy();env['RP_V3_PORTABLE']='1';env['RP_V3_PROJECT_BASE']=str(V.parents[1])
finals=[V/'exports'/f'博士科研计划书_V3{suffix}' for suffix in ['.docx','.pdf','_完整正文.md']]
before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in finals}
r=subprocess.run([sys.executable,str(T/'scripts/rebuild_v3.py'),'--portable'],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(V/'qa/独立重建运行.log').write_text(r.stdout.strip()+'\n')
assert r.returncode==0,r.stdout[-5000:]
after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in finals};assert before==after
compiled=(V/'exports/manuscript_v3.md').read_bytes()==(T/'exports/manuscript_v3.md').read_bytes()
readable=(V/'exports/博士科研计划书_V3_完整正文.md').read_bytes()==(T/'exports/博士科研计划书_V3_完整正文.md').read_bytes()
assert compiled and readable
checks=json.loads((T/'qa/跨格式一致性_核验结果.json').read_text())
mainchecks=json.loads((V/'qa/跨格式一致性_核验结果.json').read_text())
for key in ['PDF_normalized_characters','Word_normalized_characters','table_cells','math_occurrences','references','paragraphs_cells_and_references']:
 assert checks[key]==mainchecks[key],key
report={'passed':True,'sandbox':'qa/rebuild_sandbox/ (ignored)','mode':'portable Git-baseline preservation check; authoring inputs entirely V3','full_pipeline_exit':r.returncode,'compiled_MD_byte_identical':compiled,'readable_MD_byte_identical':readable,'rebuilt_concordance':checks,'final_delivery_hashes_unchanged':before,'binary_timestamp_note':'DOCX/PDF export timestamps or PDF producer metadata may differ; semantic/structural/glyph concordance is revalidated, no false byte-reproducibility claim.'}
(V/'qa/独立重建验证.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Isolated full rebuild passed; final Word/PDF/Markdown bytes untouched.')
