"""Assemble explicit reviewed sources only; never restore legacy content.

This source-only command does not generate or modify a Word document. It has no
hard-coded abstract, figure notes, missing headings or table insertion anchors.
"""
from pathlib import Path
import csv, json, re
B=Path(__file__).resolve().parent
front=(B/'frontmatter.md').read_text()
chapters=[(B/f'sources_ch{i:02d}.md').read_text() for i in range(1,7)]
source=front+'\n\n'+'\n\n'.join(chapters)+'\n\n# 参考文献\n'
assert not re.search(r'\{\{(?:FIG|TABLE)',source),'Legacy implicit insertion marker: resolve explicitly in the reviewed sources.'
order=json.loads((B/'bibliography/citation_order.json').read_text())
unknown=set(re.findall(r'@(r\d+)',source))-set(order)
assert not unknown,unknown
(B/'outputs/manuscript.md').write_text(source)
# Tables are derived from their explicit positions in the chapter source.
blocks=re.split(r'\n\s*\n','\n\n'.join(chapters))
table_parts=[];tables=0
for i,block in enumerate(blocks):
    if not block.startswith('|'):continue
    tables+=1
    title=next((b for b in reversed(blocks[:i]) if b.startswith('%% 表格题注 ')),None)
    assert title and re.search(r'表\s*'+str(tables)+r'\b',title),(tables,title)
    note=blocks[i+1] if i+1<len(blocks) and blocks[i+1].startswith('%% 表注 ') else ''
    content='\n\n'.join(s for s in [title,block,note] if s)
    table_parts.append('{{TABLE%02d}}\n%s'%(tables,content))
    (B/f'tables/table{tables:02d}.md').write_text(content+'\n')
    rows=[[v.strip() for v in l.strip().strip('|').split('|')] for l in block.splitlines()]
    assert len({len(r) for r in rows})==1
    with (B/f'tables/table{tables:02d}.csv').open('w',encoding='utf-8-sig',newline='') as f:
        csv.writer(f,lineterminator='\n').writerows(rows[:1]+rows[2:])
assert tables==6
(B/'table_sources.md').write_text('<!-- 派生快照；现行正文中的表格以sources_ch01—06.md为准。 -->\n\n'+'\n\n'.join(table_parts)+'\n')
human=re.sub(r'^---\n.*?\n---\n','',source,flags=re.S)
human=re.sub(r'^\{\{<.*?>\}\}\s*','',human,flags=re.M)
human=re.sub(r'^%%\s+\S+\s*','',human,flags=re.M)
def cite(m):return '['+','.join(str(order[k]) for k in re.findall(r'@(r\d+)',m.group()))+']'
human=re.sub(r'\[@r\d+(?:;\s*@r\d+)*\]',cite,human)
eqs={k:i+1 for i,k in enumerate(re.findall(r'\{#(eq-[a-zA-Z]+)\}',human))}
human=re.sub(r'@(eq-[a-zA-Z]+)',lambda m:'式（%d）'%eqs[m.group(1)],human)
human=human.rstrip()+'\n\n'+(B/'bibliography/review_reference_list.md').read_text()
(B/'outputs/博士研究设想_完整正文.md').write_text(human)
print('Assembled reviewed Markdown and table snapshots. Word and PDF were not modified.')
