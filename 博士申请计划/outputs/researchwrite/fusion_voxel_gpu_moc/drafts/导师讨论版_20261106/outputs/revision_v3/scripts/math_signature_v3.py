"""Independent structural projection of MathML and Word OMML.

Retains fractions, scripts, operator limits and accents. Formatting containers
are transparent. This supplements glyph checking rather than replacing it.
"""
from lxml import etree as E
from docx.oxml.ns import qn
import latex2mathml.converter,unicodedata
M='http://schemas.openxmlformats.org/officeDocument/2006/math'
def atoms(s):
 s=unicodedata.normalize('NFKC',s or '').translate(str.maketrans({'ϕ':'φ','−':'-','ˆ':'^','̂':'^','˜':'~','̃':'~','⋅':'·'}))
 return [c for c in s if not c.isspace() and c not in '\u2061\u2062']
def mml(e):
 tag=E.QName(e).localname
 def seq():return sum((mml(c) for c in e),[])
 if tag in ['mi','mo','mn','mtext']:
  a=atoms(e.text)
  return [{'operator':a[0],'sub':[],'sup':[]}] if a in [['∫'],['∑'],['∏']] else a
 if tag=='mspace':return []
 if tag in ['msub','msup','msubsup','munder','mover','munderover']:
  base=mml(e[0]);rest=[mml(c) for c in e[1:]]
  if len(base)==1 and isinstance(base[0],dict) and 'operator' in base[0]:
   sub=rest[0] if tag in ['msub','msubsup','munder','munderover'] else []
   sup=rest[-1] if tag in ['msup','msubsup','mover','munderover'] else []
   return [{'operator':base[0]['operator'],'sub':sub,'sup':sup}]
  if tag in ['mover','munder']:return [{'accent' if tag=='mover' else 'under': [base,rest[0]]}]
  return [{ {'msub':'sub','msup':'sup','msubsup':'subsup'}[tag]:[base]+rest}]
 if tag=='mfrac':return [{'fraction':[mml(e[0]),mml(e[1])]}]
 if tag=='msqrt':return [{'root':seq()}]
 return seq()
def from_latex(s):return mml(E.fromstring(latex2mathml.converter.convert(s).encode()))
def omml(e):
 tag=E.QName(e).localname
 def child(tagname):
  x=e.find(qn('m:'+tagname));return omml(x) if x is not None else []
 def seq():return sum((omml(c) for c in e if E.QName(c).namespace==M and not E.QName(c).localname.endswith('Pr')),[])
 if tag=='t':return atoms(e.text)
 if tag.endswith('Pr'):return []
 if tag=='nary':
  x=e.find(qn('m:naryPr')+'/'+qn('m:chr'));op=x.get(qn('m:val')) if x is not None else '∫'
  return [{'operator':op,'sub':child('sub'),'sup':child('sup')}]+child('e')
 if tag in ['sSub','sSup','sSubSup']:
  args=[child('e')]
  if tag in ['sSub','sSubSup']:args.append(child('sub'))
  if tag in ['sSup','sSubSup']:args.append(child('sup'))
  return [{{'sSub':'sub','sSup':'sup','sSubSup':'subsup'}[tag]:args}]
 if tag=='f':return [{'fraction':[child('num'),child('den')]}]
 if tag=='acc':
  x=e.find(qn('m:accPr')+'/'+qn('m:chr'));a=x.get(qn('m:val')) if x is not None else '^'
  return [{'accent':[child('e'),atoms(a)]}]
 if tag=='d':
  pr=e.find(qn('m:dPr'));left='(';right=')'
  if pr is not None:
   a=pr.find(qn('m:begChr'));b=pr.find(qn('m:endChr'))
   if a is not None:left=a.get(qn('m:val'),'')
   if b is not None:right=b.get(qn('m:val'),'')
  return atoms(left)+seq()+atoms(right)
 if tag=='rad':return [{'root':child('e')}]
 return seq()
