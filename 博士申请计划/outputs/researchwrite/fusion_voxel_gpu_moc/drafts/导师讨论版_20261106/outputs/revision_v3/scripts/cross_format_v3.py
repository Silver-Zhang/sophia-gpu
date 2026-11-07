"""Paragraph/cell/formula concordance, using actual DOCX XML and PDF glyphs.

No similarity threshold is used to declare a pass. Every expected text block and
all table cells are matched; residuals are localized and fail the final gate.
"""
from pathlib import Path
import json,re,unicodedata,hashlib,difflib,collections
from lxml import etree as ET
from docx import Document
from docx.oxml.ns import qn
import latex2mathml.converter
import pdfplumber
V=Path(__file__).resolve().parents[1]
from safety_v3 import require_v3_root
require_v3_root(V)
M='http://schemas.openxmlformats.org/officeDocument/2006/math'; W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'

def norm(s):
 s=''.join(('⟦SUP:'+unicodedata.normalize('NFKC',c)+'⟧') if c in '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾' else ('⟦SUB:'+unicodedata.normalize('NFKC',c)+'⟧') if c in '₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎' else c for c in s)
 s=unicodedata.normalize('NFKC',s)
 s=s.translate(str.maketrans({'ϕ':'φ','ϑ':'θ','−':'-','‐':'-','‑':'-','ˆ':'^','̂':'^','˜':'~','̃':'~','∣':'|','⋅':'·'}))
 s=re.sub(r'[\s\u2060\u200b\u200c\u200d\ufeff\u2061\u2062]','',s)
 def citation(m):
  parts=[]
  for bit in re.split('[,，]',m.group(1)):
   r=re.fullmatch(r'(\d+)[–—-](\d+)',bit)
   parts+=list(range(int(r[1]),int(r[2])+1)) if r else [int(bit)]
  return '['+','.join(str(n) for n in parts)+']'
 return re.sub(r'\[(\d{1,3}(?:[–—-]\d{1,3})?(?:,\d{1,3}(?:[–—-]\d{1,3})?)*)\]',citation,s)

def latex_text(latex):
 tree=ET.fromstring(latex2mathml.converter.convert(latex).encode())
 def walk(e):
  tag=ET.QName(e).localname
  if tag in ['mi','mo','mn','mtext']:return e.text or ''
  if tag=='mspace':return ''
  if tag=='mover':return walk(e[1])+walk(e[0])
  if tag=='msqrt':return '√'+''.join(walk(c) for c in e)
  return ''.join(walk(c) for c in e)
 return norm(walk(tree))

def math_text(e):
 tag=ET.QName(e).localname
 def children():return ''.join(math_text(c) for c in e if not ET.QName(c).localname.endswith('Pr') and ET.QName(c).namespace==M)
 if tag=='t':return e.text or ''
 if tag.endswith('Pr'):return ''
 if tag=='nary':
  c=e.find(qn('m:naryPr')+'/'+qn('m:chr'));symbol=c.get(qn('m:val')) if c is not None else '∫'
  return norm(symbol)+children()
 if tag=='acc':
  c=e.find(qn('m:accPr')+'/'+qn('m:chr'));symbol=c.get(qn('m:val')) if c is not None else '^'
  return norm(symbol)+children()
 if tag=='d':
  pr=e.find(qn('m:dPr'));left='(';right=')'
  if pr is not None:
   a=pr.find(qn('m:begChr'));b=pr.find(qn('m:endChr'))
   if a is not None:left=a.get(qn('m:val'),'')
   if b is not None:right=b.get(qn('m:val'),'')
  return left+children()+right
 if tag=='rad':return '√'+children()
 return children()

def paragraph_text(p):
 def walk(e):
  if e.tag==qn('m:oMath'):return math_text(e)
  if e.tag==qn('w:t'):return e.text or ''
  if e.tag in [qn('w:tab'),qn('w:br')]:return ' '
  return ''.join(walk(c) for c in e)
 return norm(walk(p))

def render_md(text,order):
 def cite(m):return '['+','.join(str(n) for n in sorted(order[k] for k in re.findall(r'@([A-Za-z][A-Za-z0-9_]*)',m[0])))+']'
 text=re.sub(r'\[@[A-Za-z][A-Za-z0-9_]*(?:;\s*@[A-Za-z][A-Za-z0-9_]*)*\]',cite,text)
 text=re.sub(r'\[([^\]]+)\]\(https?://[^)]+\)',r'\1',text)
 text=re.sub(r'\$([^$]+)\$',lambda m:latex_text(m[1]),text)
 text=text.replace('**','').replace('`','')
 return norm(text)

def md_blocks(source,order,human=False):
 source=re.sub(r'^---\n.*?\n---\n','',source,flags=re.S)
 out=[];table=0;eq=0
 for block in re.split(r'\n\s*\n',source.strip()):
  block=block.strip()
  if not block or block.startswith('{{<'):continue
  if block.startswith('!['):continue # asset identity/dimensions checked separately
  if block.startswith('|'):
   table+=1;rows=[line for line in block.splitlines() if not re.match(r'^\|[\s:|-]+\|$',line)]
   for r,row in enumerate(rows):
    for c,cell in enumerate(row.strip('|').split('|')):
     out.append({'role':'cell','location':f'table{table}.r{r}.c{c}','text':render_md(cell,order)})
   continue
  if block.startswith('$$'):
   eq+=1;latex=re.match(r'^\$\$(.*?)\$\$',block,re.S)[1]
   out.append({'role':'equation','location':f'equation{eq}','text':latex_text(latex)+norm(f'（{eq}）'),'latex':latex})
   continue
  if block.startswith('%% '):
   parts=block.split(' ',2);kind=parts[1];body=parts[2] if len(parts)==3 else ''
   if kind=='文档标题':continue
   role={'图片题注':'figure_caption','表格题注':'table_caption','表注':'table_note'}.get(kind,'paragraph')
  elif block.startswith('#'):
   body=re.sub(r'^#+\s*','',block);role='heading'
   if body=='参考文献':role='references_heading'
   if human and len(out)==0 and '面向聚变堆屏蔽' in body:continue
  else:
   body=block;role='reference' if re.match(r'^\[\d+\]\s',body) else 'paragraph'
   if human and re.match(r'^图\d+\s',body):role='figure_caption'
   if human and re.match(r'^表\d+\s',body):role='table_caption'
  out.append({'role':role,'location':f'block{len(out)+1}','text':render_md(body,order),'level':len(re.match(r'^#+',block)[0]) if role=='heading' else None})
 return out

def word_blocks(path):
 d=Document(path);out=[];table=0
 # Walk direct body order so tables are checked exactly where they occur.
 from docx.text.paragraph import Paragraph
 for el in d.element.body:
  if el.tag==qn('w:tbl'):
   table+=1
   for r,row in enumerate(el.findall(qn('w:tr'))):
    for c,cell in enumerate(row.findall(qn('w:tc'))):
     text=''.join(paragraph_text(p) for p in cell.findall(qn('w:p')))
     out.append({'role':'cell','location':f'table{table}.r{r}.c{c}','text':text})
  elif el.tag==qn('w:p'):
   p=Paragraph(el,d._body);style=p.style.name;text=paragraph_text(el)
   if not text or style in ['Title','Captioned Figure'] or style.lower().startswith('toc'):continue
   if re.fullmatch(r'\([1-9]\)',norm(p.text)) and el.xpath('.//m:oMath'):role='equation'
   elif style=='Bibliography':role='reference'
   elif p.text=='参考文献':role='references_heading'
   elif style.startswith('Heading'):role='heading'
   else:role={'Image Caption':'figure_caption','Table Caption':'table_caption','Table Note':'table_note'}.get(style,'paragraph')
   out.append({'role':role,'location':f'word.block{len(out)+1}','text':text,'level':int(style[-1]) if role=='heading' else None})
 return out

def differences(expected,actual):
 out=[]
 # No diff alignment may skip a missing block: include every insert/delete/replace.
 a=[(b['role'],b.get('level'),b['text']) for b in expected];b=[(b['role'],b.get('level'),b['text']) for b in actual]
 for tag,i,j,k,l in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
  if tag=='equal':continue
  out.append({'kind':tag,'expected_positions':[i,j],'actual_positions':[k,l],'expected':expected[i:j],'actual':actual[k:l]})
 return out

if __name__=='__main__':
 from concordance_v3 import main
 main()
