"""Assemble one export source; preserve the confirmed 129 headings verbatim."""
from pathlib import Path
import re,json,hashlib,csv
B=Path(__file__).resolve().parent
(B/'outputs').mkdir(exist_ok=True);(B/'tables').mkdir(exist_ok=True);(B/'qa').mkdir(exist_ok=True)
body='\n\n'.join((B/f'sources_ch{i:02d}.md').read_text().strip() for i in range(1,7))
table_parts=re.split(r'(\{\{TABLE\d+\}\})',(B/'table_sources.md').read_text())
tables={table_parts[i]:table_parts[i+1].strip() for i in range(1,len(table_parts),2)}
for marker,content in tables.items():
 body=body.replace(marker,content)
 n=int(re.search(r'\d+',marker).group())
 (B/f'tables/table{n:02d}.md').write_text(content+'\n')
 rows=[[s.strip() for s in line.strip('|').split('|')] for line in content.splitlines() if line.startswith('|')]
 with (B/f'tables/table{n:02d}.csv').open('w',newline='',encoding='utf-8-sig') as f:csv.writer(f,lineterminator="\n").writerows(rows[:1]+rows[2:])
captions={
1:('聚变屏蔽方案评价与设计更新闭环','自绘示意，依据ParaStell、CIT及CAD模型核验流程归纳；虚线为设计反馈。','[@r1; @r2; @r3]'),
2:('几何表示、空间离散与目标成本的作用关系','自绘概念图，区分材料模型、确定论网格、重要性场和权窗网格；箭头表示作用关系，不表示已验证的因果大小。','[@r8; @r9; @r12; @r36]'),
3:('GPU-MOC轨迹策略、扫描和归约流程','自绘示意，虚线表示源迭代；性能瓶颈由实际实现测量确定。','[@r20; @r21; @r24; @r25; @r26]'),
4:('CADIS与FW-CADIS的双路线及一致偏倚','自绘原理图，两条路线按各自重要性场生成一致源偏倚和权窗；FW-CADIS先求正向响应，再构造加权伴随源。','[@r30; @r31; @r40; @r41]'),
5:('重要性预计算、权窗与蒙卡运行的计时边界','自绘成本图；分项不重复计时，正向项在不需要时为零；图中没有假设性能数值。','[@r36; @r39; @r42]'),
6:('三个候选方向的独立起点与选择关系','自绘综合图，可共享算例和接口，方向三不依赖新GPU-MOC实现；导师据学术问题和资源选定主方向。','[@r15; @r21; @r36; @r39; @r42; @r47]')}
for n,(title,note,refs) in captions.items():
 fig=f'![{title}示意](../figures/fig{n:02d}.png){{width=15.7cm}}\n\n%% 图片题注 图{n} {title}\n\n%% 表注 {note}{refs}'
 marker=f'{{{{FIG{n:02d}}}}}'
 if marker in body:body=body.replace(marker,fig)
 elif n==4:body=body.replace('### 4.1.4 ',fig+'\n\n### 4.1.4 ',1)
 elif n==5:body=body.replace('### 4.2.5 ',fig+'\n\n### 4.2.5 ',1)
 else:raise ValueError(n)
# Tables3/4 are inserted immediately after the corresponding literature discussion.
for n,anchor in [(3,'### 4.1.6 '),(4,'## 4.2 ')]:
 marker=f'{{{{TABLE{n:02d}}}}}'
 if marker not in body:
  body=body.replace(anchor,tables[marker]+'\n\n'+anchor,1)
assert not re.search(r'\{\{(?:FIG|TABLE)',body)
expected=[]
for l in (B/'00_确认大纲与现有正文材料.md').read_text().split('## 用户已写正文')[0].splitlines():
 if re.match(r'^## 第一章|^## 第[二三四五六]章|^#### \d|^##### \d',l):expected.append(l.lstrip('#').strip())
actual=[l.lstrip('#').strip() for l in body.splitlines() if re.match(r'^#{1,3} ',l)]
assert expected==actual,(len(expected),len(actual))
keys=list(dict.fromkeys(re.findall(r'@r(\d+)',body)))
assert set(keys)==set(str(i) for i in range(1,48)),keys
front='''---
bibliography: ../bibliography/references.bib
csl: chinese-gb7714-2015-numeric.csl
link-citations: true
---

%% 文档标题 面向聚变堆屏蔽的高效中子输运与确定论—蒙特卡罗耦合减方差方法研究设想

%% 普通 博士科研计划书　导师讨论初稿　2026年11月6日

%% 摘要标题 摘要

%% 摘要 聚变屏蔽计算同时面临复杂几何、高能源深穿透和反复设计更新的要求。本文从空间离散、GPU确定论输运和自动减方差三方面梳理国内外研究，重点比较目标导向自适应、三维MOC轨迹管理、CADIS/FW-CADIS及其角度与网格改进。已有研究表明，求解场的数值精度、重要性场的采样效用与完整计算成本需要分别评价。基于此，提出复杂几何与重要性导向空间离散、GPU正向—伴随输运、面向聚变屏蔽的自动耦合减方差三个候选方向，分别论证其直接先例、研究问题、初步路线和实施条件。拟通过分层验证、受控误差试验及等响应可靠性下的全过程计时，识别可形成独立学术增量的问题，并由导师结合应用与软件基础确定主方向。

%% 关键词 关键词：聚变屏蔽；中子输运；特征线法；GPU；伴随重要性；自动减方差

{{< pagebreak >}}

{{< toc 2 >}}

{{< pagebreak >}}

'''
body=body.replace('S_N', '$S_N$')
source=front+body+'\n\n# 参考文献\n'
source=re.sub(r'[ \t]*(@eq-[A-Za-z]+)[ \t]*',r' \1 ',source)
(B/'outputs/manuscript.md').write_text(source)
(B/'bibliography/citation_order.json').write_text(json.dumps({f'r{k}':i+1 for i,k in enumerate(keys)},ensure_ascii=False,indent=2))
counts={'headings':len(actual),'chapters':6,'level2':sum(l.startswith('## ') for l in body.splitlines()),'level3':sum(l.startswith('### ') for l in body.splitlines()),'references':len(keys),'figures':6,'tables':6,'display_equations':len(re.findall(r'^\$\$',body,re.M)),'Chinese_characters':len(re.findall(r'[\u4e00-\u9fff]',body))}
(B/'qa/structure_check.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2))
(B/'qa/original_input_hashes.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(B.glob('0[0-4]*.md'))},ensure_ascii=False,indent=2))
print(counts)
