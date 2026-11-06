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
B=Path(__file__).resolve().parent;P=B/'outputs/博士研究设想_导师讨论初稿.docx'
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
  order=json.loads((B/'bibliography/citation_order.json').read_text())
  number=int(re.match(r'\[(\d+)\]',text).group(1));key=next(k for k,v in order.items() if v==number)
  suffix={'r24':'（arXiv预印本）','r44':'（arXiv预印本；相关会议稿PHYSOR 2016）','r29':'（Release 13.4，2026-10-12）','r40':'（SCALE 6.3.1手册）','r27':'（在线发表，2026-04-23）'}.get(key,'')
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
d.save(P)
(B/'qa/docx_repairs.json').write_text(json.dumps({'font_mapping':{'宋体':'Songti SC','黑体':'Heiti SC'},'math_face':'STIX Two Math','table_headers':len(d.tables),'clickable_URLs':True,'contents':'materialized editable internal links','heading_entries':len(headings),'reference_entries':47},ensure_ascii=False,indent=2))
print('Patched CJK fonts, table headers, reference links and',len(headings),'contents entries')
