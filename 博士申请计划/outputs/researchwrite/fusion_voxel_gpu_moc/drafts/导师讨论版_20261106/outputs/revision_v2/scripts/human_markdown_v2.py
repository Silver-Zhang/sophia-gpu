"""Human-readable Markdown with the actual Word citation order and bibliography."""
from pathlib import Path
import json,re
from docx import Document
V=Path(__file__).resolve().parents[1]
s=(V/'exports/manuscript_v2.md').read_text();order=json.loads((V/'bibliography/citation_order_v2.json').read_text())
s=re.sub(r'^---\n.*?\n---\n','',s,flags=re.S)
s=re.sub(r'^\{\{<.*?>\}\}\s*','',s,flags=re.M)
s=re.sub(r'^%% 文档标题 ', '# ',s,flags=re.M)
s=re.sub(r'^%%\s+\S+\s*','',s,flags=re.M)
def cite(m):return '['+','.join(str(order[k]) for k in re.findall(r'@([A-Za-z][A-Za-z0-9_]*)',m.group()))+']'
s=re.sub(r'\[@[A-Za-z][A-Za-z0-9_]*(?:;\s*@[A-Za-z][A-Za-z0-9_]*)*\]',cite,s)
eqs={k:i+1 for i,k in enumerate(re.findall(r'\{#(eq-[A-Za-z]+)\}',s))}
s=re.sub(r'@(eq-[A-Za-z]+)',lambda m:'式（%d）'%eqs[m.group(1)],s)
s=re.sub(r'\s*\{#(eq-[A-Za-z]+)\}',lambda m:'　（%d）'%eqs[m.group(1)],s)
refs=[''.join(p._p.xpath('.//w:t/text()')).replace('\u2060','') for p in Document(V/'exports/博士科研计划书_V2.docx').paragraphs if p.style.name=='Bibliography']
assert len(refs)==len(order),(len(refs),len(order))
(V/'bibliography/正式参考文献表.md').write_text('\n\n'.join(refs)+'\n')
s=s.rstrip()+'\n\n'+'\n\n'.join(refs)+'\n'
assert not re.search(r'@(?:r\d+|new_)',s)
(V/'exports/博士科研计划书_V2_完整正文.md').write_text(s)
print('Readable Markdown and',len(refs),'actual Word bibliography entries exported.')
