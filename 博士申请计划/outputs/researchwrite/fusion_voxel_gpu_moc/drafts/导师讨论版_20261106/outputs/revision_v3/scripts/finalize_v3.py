"""Deterministic layout repairs after the installed md-to-word pipeline.

The pipeline supplies all document content, native OMML, styles and citations.
This patch supplies runtime-resolvable CJK fonts, repeating headers, URL links
and a materialized, clickable contents page for renderer portability.
"""
from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt,Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.constants import RELATIONSHIP_TYPE as RT
import re,json,sys
B=Path(__file__).resolve().parents[1];P=B/'exports/博士科研计划书_V3.docx'
from safety_v3 import require_v3_root
require_v3_root(B)
assert json.loads((B/'authorization.json').read_text())['approved'] is True
d=Document(P)
def patch_fonts(el):
 for f in el.iter(qn('w:rFonts')):
  east=f.get(qn('w:eastAsia'),'')
  if east in ['宋体','Songti SC']:f.set(qn('w:eastAsia'),'Songti SC')
  elif east in ['黑体','Heiti SC']:f.set(qn('w:eastAsia'),'Heiti SC')
  for k in list(f.attrib):
   if k.endswith('Theme'):del f.attrib[k]
for part in [d.styles.element,d.element,*[s.header._element for s in d.sections],*[s.footer._element for s in d.sections]]:patch_fonts(part)
# Missing CJK fallback in direct table/caption runs follows the paragraph font.
for st in d.styles:
 if st.type==1:
  rp=st.element.get_or_add_rPr();rf=rp.find(qn('w:rFonts'))
  if rf is None:rf=OxmlElement('w:rFonts');rp.append(rf)
  rf.set(qn('w:eastAsia'),'Heiti SC' if st.name in ['Title','Heading 1','Heading 2','Heading 3','TOC Heading','Abstract Title','References Title'] else 'Songti SC')
for t in d.tables:
 pr=t.rows[0]._tr.get_or_add_trPr()
 if pr.find(qn('w:tblHeader')) is None:pr.append(OxmlElement('w:tblHeader'))
for p in d.paragraphs:
 if p.style.name=='Bibliography':
  text=''.join(p._p.xpath('.//w:t/text()'))
  # One DOI URL is sufficient; remove its repeated plain identifier.
  text=re.sub(r'\s+DOI:(10\.[^\s]+)\.$','',text) if 'https://doi.org/' in text else text
  text=re.sub(r'^(\[\d+\])',r'\1 ',text)
  order=json.loads((B/'bibliography/citation_order_v3.json').read_text())
  number=int(re.match(r'\[(\d+)\]',text).group(1));key=next(k for k,v in order.items() if v==number)
  suffix={'r24':'（arXiv预印本）','r44':'（arXiv预印本；相关会议稿PHYSOR 2016）','r29':'（在线指南13.5）','r40':'（SCALE 6.3.1手册）','r27':'（在线发表，2026-04-23）','new_longhistory2013':'（M&C 2013作者预印本）','new_stream_kns2024':'（KNS Spring Meeting，2024-05-09—10）'}.get(key,'')
  text+=suffix
  starts=list(p._p.xpath('./w:bookmarkStart'));ends=list(p._p.xpath('./w:bookmarkEnd'))
  for el in list(p._p):
   if el.tag!=qn('w:pPr'):p._p.remove(el)
  for el in starts:p._p.append(el)
  pos=0
  for m in re.finditer(r'https?://[^\s（）]+',text):
   before=text[pos:m.start()];p.add_run(before)
   target=m.group().rstrip('.。');tail=m.group()[len(target):]
   h=OxmlElement('w:hyperlink');h.set(qn('r:id'),p.part.relate_to(target,RT.HYPERLINK,is_external=True))
   r=OxmlElement('w:r');pr=OxmlElement('w:rPr');rf=OxmlElement('w:rFonts');rf.set(qn('w:ascii'),'Times New Roman');rf.set(qn('w:hAnsi'),'Times New Roman');rf.set(qn('w:eastAsia'),'Songti SC');pr.append(rf);r.append(pr)
   tx=OxmlElement('w:t');tx.text=target;r.append(tx);h.append(r);p._p.append(h)
   p.add_run(tail);pos=m.end()
  p.add_run(text[pos:])
  for el in ends:p._p.append(el)
  p.paragraph_format.keep_together=True;p.paragraph_format.widow_control=True
  p.paragraph_format.alignment=WD_ALIGN_PARAGRAPH.LEFT
 if p.style.name in ['References Title'] or p.text=='参考文献':p.paragraph_format.page_break_before=True
 # All equations retain native editable OMML and receive a proper math face.
 for el in p._p.xpath('.//m:oMath'):
  for mr in el.iter(qn('m:r')):
   wp=mr.find(qn('w:rPr'))
   if wp is None:wp=OxmlElement('w:rPr');mr.insert(0,wp)
   rf=wp.find(qn('w:rFonts'))
   if rf is None:rf=OxmlElement('w:rFonts');wp.append(rf)
   rf.set(qn('w:ascii'),'STIX Two Math');rf.set(qn('w:hAnsi'),'STIX Two Math')
# Suppress unused integral/sum limits so Word/LO show no placeholder boxes.
for el in d.element.xpath('.//m:oMath'):
 for mr in el.iter(qn('m:r')):
  wp=mr.find(qn('w:rPr'))
  if wp is None:wp=OxmlElement('w:rPr');mr.insert(0,wp)
  rf=wp.find(qn('w:rFonts'))
  if rf is None:rf=OxmlElement('w:rFonts');wp.append(rf)
  rf.set(qn('w:ascii'),'STIX Two Math');rf.set(qn('w:hAnsi'),'STIX Two Math')
for nary in d.element.xpath('.//m:nary'):
 pr=nary.find(qn('m:naryPr'))
 if pr is None:pr=OxmlElement('m:naryPr');nary.insert(0,pr)
 for tag,flag in [('m:sub','m:subHide'),('m:sup','m:supHide')]:
  el=nary.find(qn(tag))
  if el is None or not ''.join(el.itertext()).strip():
   opt=pr.find(qn(flag))
   if opt is None:opt=OxmlElement(flag);pr.append(opt)
   opt.set(qn('m:val'),'on')
# Keep the document title on two intentional lines without splitting a term.
for p in d.paragraphs:
 if p.style.name=='Title':
  title=p.text
  for el in list(p._p):
   if el.tag!=qn('w:pPr'):p._p.remove(el)
  a,b=title.split('高效中子输运与',1)
  run=p.add_run(a+'高效中子输运与');run.font.size=Pt(18);run.add_break()
  p.add_run(b).font.size=Pt(18)
 if '博士科研计划书　导师讨论初稿' in p.text:
  p.paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.first_line_indent=Pt(0)
# Store heading bookmarks and replace unexpanded TOC field with editable links.
headings=[]
for i,p in enumerate(d.paragraphs):
 if p.style.name in ['Heading 1','Heading 2','References Title']:
  name=f'rp_heading_{len(headings)}';bid=str(2000+len(headings));start=OxmlElement('w:bookmarkStart');start.set(qn('w:id'),bid);start.set(qn('w:name'),name)
  end=OxmlElement('w:bookmarkEnd');end.set(qn('w:id'),bid);p._p.insert(0,start);p._p.append(end)
  headings.append((p.text,p.style.name,name))
page_map_path=B/'qa/toc_page_map.json'; page_map=json.loads(page_map_path.read_text()) if page_map_path.exists() else {}
toc=[]
from docx.text.paragraph import Paragraph
for node in d.element.xpath('.//w:body//w:p'):
 p=Paragraph(node,d._body)
 if p._p.xpath('.//w:instrText[contains(.,"TOC")]') or p._p.xpath('.//w:fldSimple[contains(@w:instr,"TOC")]'):
  toc.append(p)
if toc:
 p=toc[0]
 for el in list(p._p):
  if el.tag!=qn('w:pPr'):p._p.remove(el)
 p.style=d.styles['TOC Heading'];p.add_run('目录')
 prev=p
 for text,style,name in headings:
  el=OxmlElement('w:p');prev._p.addnext(el)
  from docx.text.paragraph import Paragraph
  q=Paragraph(el,p._parent);q.style=d.styles['toc 1' if style in ['Heading 1','References Title'] else 'toc 2']
  pf=q.paragraph_format;pf.line_spacing=Pt(16);pf.space_before=Pt(2 if style in ['Heading 1','References Title'] else 0);pf.space_after=Pt(0);pf.keep_with_next=False;pf.keep_together=True
  pf.tab_stops.add_tab_stop(Cm(15.8),2,1)
  h=OxmlElement('w:hyperlink');h.set(qn('w:anchor'),name);r=OxmlElement('w:r');tx=OxmlElement('w:t');tx.text=text;r.append(tx);h.append(r);q._p.append(h)
  q.add_run('\t'+str(page_map.get(text,'')));
  for run in q.runs:run.font.size=Pt(10.5)
  prev=q
 # Remove cached instruction hints after field, if any, without removing breaks.
 for p in d.paragraphs:
  if '右键' in p.text and '目录' in p.text:p._element.getparent().remove(p._element)
# Chapter boundaries keep the six roles visible; no separate empty cover.
for p in d.paragraphs:
 if p.style.name=='Heading 1':p.paragraph_format.page_break_before=True
# Explicit row protection and readable, top-aligned text in comparison tables.
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
for t in d.tables:
 for row in t.rows:
  pr=row._tr.get_or_add_trPr()
  if pr.find(qn('w:cantSplit')) is None:pr.append(OxmlElement('w:cantSplit'))
  for c in row.cells:
   c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.TOP
   for p in c.paragraphs:
    p.paragraph_format.keep_with_next=False
    p.paragraph_format.line_spacing=1.1
    p.paragraph_format.space_after=Pt(3)
# Set diagram alternative text without exposing authoring notes in the page.
for i,x in enumerate(d.element.xpath('.//wp:docPr'),1):
 x.set('descr',json.loads((B/'planning/图形物理与制作约定.json').read_text())[i-1]['caption'])
# Prevent citation groups from breaking internally or becoming line-initial orphans.
# WORD JOINER changes break opportunities only; source citation keys stay untouched.
for pel in d.element.xpath('.//w:p'):
 ts=pel.xpath('.//w:t');joined=''.join(t.text or '' for t in ts)
 spans=list(re.finditer(r'\[(?:[0-9,–—-])+\]',joined))
 positions={i for m in spans for i in range(m.start(),m.end())}
 starts={m.start() for m in spans if m.start()>0};offset=0
 for t in ts:
  original=t.text or '';parts=[]
  for j,ch in enumerate(original):
   index=offset+j
   if index in starts:parts.append('\u2060')
   parts.append(ch)
   if index in positions:parts.append('\u2060')
  t.text=''.join(parts);offset+=len(original)
for i,t in enumerate(d.tables):
 widths=[3.0,3.5,4.0,5.5] if i<5 else [2.5,4.5,4.5,4.5]
 t.autofit=False
 for col,w in zip(t.columns,widths):col.width=Cm(w)
 for row in t.rows:
  for c,w in zip(row.cells,widths):c.width=Cm(w)
d.save(P)
(B/'qa/docx_repairs.json').write_text(json.dumps({'font_mapping':{'宋体':'Songti SC','黑体':'Heiti SC'},'math_face':'STIX Two Math','table_headers':len(d.tables),'clickable_URLs':True,'contents':'materialized editable internal links','heading_entries':len(headings),'reference_entries':len(json.loads((B/'bibliography/corpus_v3.json').read_text()))},ensure_ascii=False,indent=2))
print('Patched CJK fonts, table headers, reference links and',len(headings),'contents entries')
