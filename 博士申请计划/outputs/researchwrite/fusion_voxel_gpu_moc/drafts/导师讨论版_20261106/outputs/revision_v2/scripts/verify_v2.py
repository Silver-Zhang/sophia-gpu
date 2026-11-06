"""Structural/content gates; visual inspection remains separate and mandatory."""
from pathlib import Path
import re,json,zipfile,hashlib,subprocess,sys
from lxml import etree
from docx import Document
from pypdf import PdfReader
import pdfplumber
V=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(V/'scripts/check_protection_v2.py')],check=True)
P=V/'exports/博士科研计划书_V2.docx';PDF=P.with_suffix('.pdf')
d=Document(P);corpus=json.loads((V/'bibliography/corpus_v2.json').read_text());order=json.loads((V/'bibliography/citation_order_v2.json').read_text())
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','m':'http://schemas.openxmlformats.org/officeDocument/2006/math','wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'}
with zipfile.ZipFile(P) as z:root=etree.fromstring(z.read('word/document.xml'));rels=z.read('word/_rels/document.xml.rels')
text=''.join(root.xpath('//w:t/text()',namespaces=ns))
refs=[''.join(p._p.xpath('.//w:t/text()')) for p in d.paragraphs if p.style.name=='Bibliography']
assert len(refs)==len(corpus)==len(order)==61
bykey={r['key']:r for r in corpus}
def norm(t):return re.sub(r'[^a-z0-9\u4e00-\u9fff]','',t.lower())
ref_errors=[]
for k,n in order.items():
 r=bykey[k];ref=refs[n-1]
 if not norm(r['title']) in norm(ref):ref_errors.append({'key':k,'number':n,'title':r['title'],'reference':ref})
assert not ref_errors,ref_errors
assert len(d.tables)==6 and len(d.inline_shapes)==6
captions=[p.text for p in d.paragraphs if p.style.name in ['Image Caption','Table Caption']]
# Style names come from the engine's canonical English names.
figures=[p for p in d.paragraphs if re.match(r'^图[1-6]\s',p.text)]
tables=[p for p in d.paragraphs if re.match(r'^表[1-6]\s',p.text)]
assert len(figures)==6 and len(tables)==6,(len(figures),len(tables))
assert all(len(t.columns)==4 for t in d.tables)
assert '平台' not in ''.join(c.text for c in d.tables[1].rows[0].cells)
assert 'Zhou' not in ''.join(c.text for row in d.tables[1].rows for c in row.cells)
display_equations=[p for p in d.paragraphs if re.fullmatch(r'\s*（[1-9]）',p.text) and p._p.xpath('.//m:oMath')]
assert len(display_equations)==9
assert not root.xpath('//w:del|//w:ins|//w:commentRangeStart',namespaces=ns) # independent new document, original untouched
assert not any(x in text for x in ['%%','{{FIG','{{TABLE','@new_','@r30'])
reader=PdfReader(PDF);pages=[p.extract_text() or '' for p in reader.pages]
assert all(len(t.strip())>80 for t in pages)
assert not any('\ufffd' in t or '\u25a1' in t for t in pages)
mp=json.loads((V/'qa/toc_page_map.json').read_text());assert len(mp)==25
for h,n in mp.items():assert ''.join(h.split()) in ''.join(pages[n-1].split()),(h,n)
# Border check only flags glyphs beyond page edges, not whitespace/margins.
outside=[]
with pdfplumber.open(PDF) as pdf:
 for i,p in enumerate(pdf.pages,1):
  for c in p.chars:
   if c['x0']<-1 or c['top']<-1 or c['x1']>p.width+1 or c['bottom']>p.height+1:
    outside.append({'page':i,'bbox':[c['x0'],c['top'],c['x1'],c['bottom']],'text':c['text']})
assert not outside,outside
ledger=json.loads((V/'planning/批注处理台账.json').read_text());assert len(ledger)==38
assert sum(r['status']=='已完成' for r in ledger)==36
result={'pages':len(pages),'references':len(refs),'new_references':14,'original_references':47,'figures':6,'editable_tables':6,'native_display_equations':9,'all_native_math_objects':len(root.xpath('//m:oMath',namespaces=ns)),'toc_entries':len(mp),'original_protected_files':54,'comments_addressed':38,'comments_fully_completed':36,'comments_evidence_limited':['164','175'],'bibliography_order_and_titles_match':True,'no_text_outside_pages':True,'external_hyperlinks':rels.count(b'TargetMode="External"'),'docx_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'pdf_sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(),'visual_QA':'see independent page-by-page report; not inferred by this script'}
(V/'qa/结构与内容核验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
