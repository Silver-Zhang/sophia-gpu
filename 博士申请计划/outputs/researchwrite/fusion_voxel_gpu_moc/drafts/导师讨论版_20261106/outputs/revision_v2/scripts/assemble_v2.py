"""Assemble only V2-reviewed sources; never read legacy manuscript as content."""
from pathlib import Path
import json,re
V=Path(__file__).resolve().parents[1]
front='''---
bibliography: ../bibliography/references_v2.bib
csl: chinese-gb7714-2015-numeric.csl
link-citations: true
---

%% 文档标题 面向聚变堆屏蔽的高效中子输运与确定论—蒙特卡罗耦合减方差方法研究设想

{{< toc 2 >}}

{{< pagebreak >}}
'''
(V/'sources/frontmatter.md').write_text(front)
body='\n\n'.join((V/f'sources/ch{i:02d}.md').read_text().strip() for i in range(1,7))
brief=json.loads((V/'planning/图形物理与制作约定.json').read_text())
for f in brief:
 n=f['n'];cit='['+'; '.join('@'+k for k in f['sources'])+']'
 # A single academic caption states physical content, provenance cites the concepts.
 content=f'![](../figures/fig{n:02d}.png){{width=15.8cm}}\n\n%% 图片题注 图{n} {f["caption"].rstrip("。")}'+cit+'。'
 assert body.count('{{FIG%02d}}'%n)==1
 body=body.replace('{{FIG%02d}}'%n,content)
for n in range(1,7):
 assert body.count('{{TABLE%02d}}'%n)==1
 body=body.replace('{{TABLE%02d}}'%n,(V/f'tables/table{n:02d}.md').read_text().strip())
assert not re.search(r'\{\{(?:TABLE|FIG)',body)
keys=re.findall(r'@([A-Za-z][A-Za-z0-9_]*)',body)
order={k:i+1 for i,k in enumerate(dict.fromkeys(k for k in keys if not k.startswith('eq')))}
corpus={r['key'] for r in json.loads((V/'bibliography/corpus_v2.json').read_text())}
assert set(order)==corpus,(set(order)-corpus,corpus-set(order))
(V/'bibliography/citation_order_v2.json').write_text(json.dumps(order,ensure_ascii=False,indent=2)+'\n')
(V/'exports/manuscript_v2.md').write_text(front+'\n'+body+'\n\n# 参考文献\n')
print('Assembled',len(order),'cited identities;',len(re.findall(r"^\$\$",body,re.M)),'display equations')
