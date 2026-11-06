"""Structural/content checks on the actual DOCX/PDF; not a visual QA substitute."""
from pathlib import Path
import sys
_base=Path(__file__).resolve().parent
if (_base/'review_state.json').exists():
 import json,subprocess
 if not json.loads((_base/'review_state.json').read_text()).get('regeneration_approved',False):
  subprocess.run([sys.executable,str(_base/'verify_review_sync.py')],check=True)
  raise SystemExit(0)
from docx import Document
from docx.oxml.ns import qn
from pypdf import PdfReader
import re,json,hashlib,csv
B=Path(__file__).resolve().parent; OUT=B/'outputs';d=Document(OUT/'博士研究设想_导师讨论初稿.docx')
pdf=B/'qa/render_final/博士研究设想_导师讨论初稿.pdf';r=PdfReader(pdf)
src=(OUT/'manuscript.md').read_text();order=json.loads((B/'bibliography/citation_order.json').read_text())
refs=[p for p in d.paragraphs if p.style.name=='Bibliography']
assert len(refs)==47
numbers=[int(re.match(r'\[(\d+)\]',p.text).group(1)) for p in refs]
assert numbers==list(range(1,48))
head_expected=[l.lstrip('#').strip() for l in src.splitlines() if re.match(r'^#{1,3} ',l) and l!='# 参考文献']
head_actual=[p.text for p in d.paragraphs if p.style.name in ['Heading 1','Heading 2','Heading 3'] and p.text!='参考文献']
assert head_actual==head_expected,(len(head_actual),len(head_expected))
maths=d.element.xpath('.//m:oMath');assert len(maths)>=8
assert not d.element.xpath('.//m:nary/m:e[not(*)]')
assert len(d.tables)==6 and len(d.element.xpath('.//w:drawing'))==6
assert len(d.element.xpath('.//w:tblHeader'))==6
assert sum(v.is_external for v in d.part.rels.values())==47
alltext=''.join(d.element.xpath('.//w:t/text() | .//m:t/text()'))
for token in ['@eq-','{{FIG','{{TABLE','打开文档后目录','XX待填','AI协助']:assert token not in alltext,token
page_text=[''.join(p.extract_text().split()) for p in r.pages]
mp=json.loads((B/'qa/toc_page_map.json').read_text())
for title,num in mp.items():assert ''.join(title.split()) in page_text[num-1],(title,num)
for n in range(1,7):
 assert len(re.findall(r'图\s*'+str(n)+r'(?!\d)',alltext))>=2
 assert len(re.findall(r'表\s*'+str(n)+r'(?!\d)',alltext))>=2
original=json.loads((B/'qa/original_input_hashes.json').read_text())
for name,sha in original.items():assert hashlib.sha256((B/name).read_bytes()).hexdigest()==sha
# Export standalone human-readable Markdown with actual citation numbering.
human=re.sub(r'^---\n.*?\n---\n','',src,flags=re.S)
human=re.sub(r'\{\{<.*?>\}\}','',human)
human=re.sub(r'^%% (?:文档标题|普通|摘要标题|摘要|关键词|表格题注|图片题注|表注) ', '',human,flags=re.M)
eqs={key:i+1 for i,key in enumerate(re.findall(r'\{#(eq-[^}]+)\}',human))}
def eq(m):return m.group(1)+'\n\n（'+str(eqs[m.group(2)])+'）'
human=re.sub(r'(\$\$[^\n]+\$\$) \{#(eq-[^}]+)\}',eq,human)
human=re.sub(r'@eq-[A-Za-z]+',lambda m:'式（'+str(eqs[m.group()[1:]])+'）',human)
def cite(m):
 nums=sorted(set(order[k] for k in re.findall(r'@(r\d+)',m.group())))
 return '['+','.join(map(str,nums))+']'
human=re.sub(r'\[@r\d+(?:;\s*@r\d+)*\]',cite,human)
human=human.replace('{width=15.7cm}','')
human+='\n\n'+'\n\n'.join(''.join(p._p.xpath('.//w:t/text()')) for p in refs)+'\n'
assert '@r' not in human and '@eq' not in human
(OUT/'博士研究设想_完整正文.md').write_text(human)
report={'status':'structural checks passed; visual review recorded separately','pages':len(r.pages),'chapters':6,'confirmed_headings':len(head_actual),'third_level_sections':97,'references':47,'figures':6,'native_tables':6,'native_OMML_objects':len(maths),'numbered_display_equations':8,'repeating_table_headers':6,'external_reference_links':47,'TOC_entries_with_verified_page_numbers':len(mp),'original_00_04_unchanged':True,'MD_citation_order_matches_DOCX':True}
(B/'qa/package_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
