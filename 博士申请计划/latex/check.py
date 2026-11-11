#!/usr/bin/env python3
"""Check numeric citations and LaTeX references without requiring TeX packages."""
from pathlib import Path
import argparse,collections,json,re,sys
ap=argparse.ArgumentParser();ap.add_argument('--log',type=Path);ap.add_argument('--source',type=Path);args=ap.parse_args()
root=Path(__file__).resolve().parent;path=args.source or root/'main.tex'; raw=path.read_text();s=re.sub(r'(?m)(?<!\\)%.*$','',raw)
errors=[];warnings=[];notes=[]
bibs=re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',s)
for kind,vals in [('bibitem',bibs),('label',re.findall(r'\\label\{([^}]+)\}',s))]:
    errors += [f'duplicate {kind}: {k}' for k,n in collections.Counter(vals).items() if n>1]
keys=set(bibs);used=set(); labels=set(re.findall(r'\\label\{([^}]+)\}',s))
for citation in re.findall(r'\\upcite\{([^}]+)\}',s):
    if re.fullmatch(r'#\d',citation): continue
    if re.search(r'\d{4}-\d{2}-\d{2}',citation): errors.append('access date misused as citation: '+citation);continue
    for token in re.split(r'[,，]',citation):
        token=token.strip(); m=re.fullmatch(r'(\d+)\s*(?:--|–|—|-)\s*(\d+)',token)
        if m:
            lo,hi=map(int,m.groups())
            if lo>hi: errors.append('reversed citation range: '+token)
            used.update('ref'+str(n) for n in range(lo,hi+1))
        elif token.isdigit(): used.add('ref'+token)
        else: errors.append('invalid numeric citation: '+token)
for citation in re.findall(r'\\(?:cite|citep|citet)\{([^}]+)\}',s): used.update(citation.split(','))
errors += ['missing bibliography entry: '+k for k in sorted(used-keys)]
labels.update(re.findall(r'\\SummaryTable\{[^}]+\}\{([^}]+)\}',s))
refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',s));errors += ['missing label: '+k for k in sorted(refs-labels)]
notes += ['retained uncited bibliography entry: '+k for k in sorted(keys-used)]
# V2.1 retires unrelated V5.3 sources and equations; check the new outline.
outline=(root.parent/'outline/博士科研计划书_重构提纲_V2.1.md').read_text()
expected_sections=re.findall(r'^# 第[一二三四五]章 (.+)$',outline,re.M)
expected_subsections=re.findall(r'^## [1-5]\.\d+ (.+)$',outline,re.M)
# User's second-chapter annotations merge voxel traversal into coupling.
expected_subsections.remove('体素穿越与几何界面求交方法')
# The user replaced chapter 3 verbatim after the original outline was written.
expected_sections[2]='GPU-MOC并行算法研究现状'
third_titles=['三维MOC计算流程与并行特征', 'CPU-GPU异构并行与任务划分', '特征线存储与GPU显存管理', 'GPU任务调度与负载均衡']
expected_subsections=[]
third_inserted=False
for number,title in re.findall(r'^## ([1-5])\.\d+ (.+)$',outline,re.M):
    if title=='体素穿越与几何界面求交方法': continue
    if number=='3':
        if not third_inserted: expected_subsections.extend(third_titles);third_inserted=True
    else: expected_subsections.append(title)
# Approved GPU scope: no device-count commitment in chapter-five headings.
expected_subsections=[title.replace('面向复杂体素几何的 CPU-GPU 多设备协同并行','面向复杂体素几何的CPU-GPU协同并行').replace('体素离散与多 GPU 执行的精度–成本协同优化','体素离散与GPU执行的精度–成本协同优化') for title in expected_subsections]
# Latest annotation moves former 4.1 prose into the chapter introduction.
expected_subsections.remove('聚变屏蔽典型结构与目标响应')
if re.findall(r'\\section\{([^}]+)\}',s) != expected_sections: errors.append('chapter titles/order differ from V2.1')
if re.findall(r'\\subsection\{([^}]+)\}',s) != expected_subsections: errors.append('subsection titles/order differ from V2.1')
if re.search(r'\\subsubsection\{',s): errors.append('unexpected third-level heading')
for idx,chapter in enumerate(re.split(r'\\section\{',s)[1:],1):
    # Chapters 1–2 follow annotations; chapter 3 follows the supplied replacement.
    if idx in (1,2,3):
        if r'\paragraph*{本章小结}' in chapter or '{tab:sum'+str(idx)+'}' in chapter:
            errors.append(f'chapter {idx} summary/table must be removed per annotation')
        continue
    # The user explicitly retains chapter 4–5 headings only.
    if idx in (4,5):
        body=chapter.split('\\clearpage',1)[0]
        body=re.sub(r'^[^}]+\}\\label\{[^}]+\}', '', body, count=1)
        if idx==4:
            sections=re.split(r'\\subsection\{[^}]+\}',body)[1:]
            if len(sections)!=4 or any(not x.strip() for x in sections): errors.append('chapter 4 requires four completed subsections')
        else:
            body=re.sub(r'\\subsection\{[^}]+\}', '', body)
            if body.strip(): errors.append('chapter 5 must contain headings only')
if s.find(r'\label{eq:transport}') > s.find(r'\subsection{复杂几何体素化与 GPU'):
    errors.append('transport equation must appear in 1.2')
for name in re.findall(r'\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}',s):
    errors += [] if any((root/(name+suffix)).is_file() for suffix in ['', '.pdf', '.png']) else ['missing figure: '+name]
# Preserve the user's existing 1–40 numbering plus appended 41–44.
# First-appearance renumbering is a separate editorial change, not a build failure.
if bibs != ['ref'+str(n) for n in range(1,len(bibs)+1)]:
    errors.append('bibliography keys must be sequential and ordered')
if args.log:
    log=args.log.read_text(errors='replace')
    errors += [line for line in log.splitlines() if re.search(r'undefined|There were undefined references|Rerun to get cross-references right|Fatal error|^!',line,re.I)]
    warnings += [line for line in log.splitlines() if re.search(r'Overfull|Missing character',line)]
result={'source':str(path),'bibliography_count':len(bibs),'cited_entries':len(used),'equations':len(re.findall(r'\\begin\{equation\}',s)),'figures':len(re.findall(r'\\includegraphics',s)),'tables':len(re.findall(r'\\SummaryTable\{',s))+len(re.findall(r'\\begin\{longtable\}',s)),'errors':errors,'warnings':warnings,'notes':notes}
print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(bool(errors or warnings))
