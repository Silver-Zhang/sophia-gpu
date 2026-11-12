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
# Approved current structure; no historical outline dependency.
expected_sections=['研究背景与研究目标', '复杂几何体素化与 MOC 数值方法研究现状', 'GPU-MOC并行算法研究现状', '聚变屏蔽应用与数值验证依据', '研究内容、技术路线与实施方案']
expected_subsections=['聚变堆中子屏蔽的工程需求与计算挑战', '中子输运数值方法及 MOC 的选择依据', '复杂几何体素化与 GPU 异构并行技术路线', '研究目标与关键科学问题', '复杂几何表示与材料映射方法', '体素化几何与 MOC 特征线离散的耦合', 'MOC 沿程输运求解与多群源迭代', 'MOC 数值误差与空间精度控制方法', '三维MOC计算流程与并行特征', 'CPU-GPU异构并行与任务划分', '特征线存储与GPU显存管理', 'GPU任务调度与负载均衡', '聚变屏蔽基准与实验验证依据', '数值验证与计算效率评价', '聚变屏蔽中的混合减方差方法', '总体研究思路与技术路线', '复杂几何体素化 MOC 特征线追踪与误差控制', '面向复杂体素几何的CPU-GPU协同并行', '体素离散与GPU执行的精度–成本协同优化', '数值验证与聚变屏蔽应用方案', '研究计划与阶段成果', '预期创新与研究可行性']
if re.findall(r'\\section\{([^}]+)\}',s) != expected_sections: errors.append('chapter titles/order differ from approved current structure')
if re.findall(r'\\subsection\{([^}]+)\}',s) != expected_subsections: errors.append('subsection titles/order differ from approved current structure')
if re.search(r'\\subsubsection\{',s): errors.append('unexpected third-level heading')
for idx,chapter in enumerate(re.split(r'\\section\{',s)[1:],1):
    # Chapters 1–2 follow annotations; chapter 3 follows the supplied replacement.
    if idx in (1,2,3):
        if r'\paragraph*{本章小结}' in chapter or '{tab:sum'+str(idx)+'}' in chapter:
            errors.append(f'chapter {idx} summary/table must be removed per annotation')
        continue
    # Chapters 4 and 5 contain the approved validation basis and research plan.
    if idx in (4,5):
        body=chapter.split('\\clearpage',1)[0]
        body=re.sub(r'^[^}]+\}\\label\{[^}]+\}', '', body, count=1)
        if idx==4:
            sections=re.split(r'\\subsection\{[^}]+\}',body)[1:]
            if len(sections)!=3 or any(not x.strip() for x in sections): errors.append('chapter 4 requires three completed subsections')
        else:
            sections=re.split(r'\\subsection\{[^}]+\}',body)[1:]
            if len(sections)!=7 or any(not x.strip() for x in sections): errors.append('chapter 5 requires seven completed subsections')
            for required in ['eq:response_perturbation','eq:independent_residual','eq:joint_selection','fig:research_plan','tab:research_validation','tab:research_schedule']:
                if required not in labels: errors.append('missing research-plan element: '+required)
if s.find(r'\label{eq:transport}') > s.find(r'\subsection{复杂几何体素化与 GPU'):
    errors.append('transport equation must appear in 1.2')
for name in re.findall(r'\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}',s):
    errors += [] if any((root/(name+suffix)).is_file() for suffix in ['', '.pdf', '.png']) else ['missing figure: '+name]
# The current revision numbers references by first appearance; retained uncited entries follow.
if bibs != ['ref'+str(n) for n in range(1,len(bibs)+1)]:
    errors.append('bibliography keys must be sequential and ordered')
# Ignore the macro definition and check actual numeric citation first appearances.
first_seen=[]
for c in re.findall(r'\\upcite\{([^}]+)\}',s):
    if c.startswith('#'): continue
    for token in c.split(','):
        m=re.fullmatch(r'(\d+)\s*(?:--|–|—|-)\s*(\d+)',token.strip())
        seq=range(int(m[1]),int(m[2])+1) if m else [int(token.strip())]
        for n in seq:
            if n not in first_seen: first_seen.append(n)
if first_seen!=list(range(1,len(first_seen)+1)):
    errors.append('numeric citations must follow first appearance')

if args.log:
    log=args.log.read_text(errors='replace')
    errors += [line for line in log.splitlines() if re.search(r'undefined|There were undefined references|Rerun to get cross-references right|Fatal error|^!',line,re.I)]
    warnings += [line for line in log.splitlines() if re.search(r'Overfull|Missing character',line)]
result={'source':str(path),'bibliography_count':len(bibs),'cited_entries':len(used),'equations':len(re.findall(r'\\begin\{equation\}',s)),'figures':len(re.findall(r'\\includegraphics',s)),'tables':len(re.findall(r'\\SummaryTable\{',s))+len(re.findall(r'\\begin\{longtable\}',s)),'errors':errors,'warnings':warnings,'notes':notes}
print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(bool(errors or warnings))
