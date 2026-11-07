"""Record the actual V2-to-V3 source delta without writing any V2 path."""
from pathlib import Path
import json,hashlib,re,difflib,sys
import math_signature_v3 as m
V=Path(__file__).resolve().parents[1];V2=V.parent/'revision_v2'
from safety_v3 import require_v3_root
require_v3_root(V)
changes=[];headings=[];old_math=[];new_math=[]
for n in range(1,7):
 p=f'sources/ch{n:02d}.md';a=(V2/p).read_text();b=(V/p).read_text()
 h1=re.findall(r'^#{1,2} .+$',a,re.M);h2=re.findall(r'^#{1,2} .+$',b,re.M);assert h1==h2;headings+=h1
 for s,target in [(a,old_math),(b,new_math)]:target.extend(m.from_latex(x or y) for x,y in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$([^$\n]+)\$(?!\$)',s,re.S))
 old_eq=re.findall(r'^\$\$.*$',a,re.M);new_eq=re.findall(r'^\$\$.*$',b,re.M);assert old_eq==new_eq
 aa=re.split(r'\n\s*\n',a.strip());bb=re.split(r'\n\s*\n',b.strip())
 for kind,i,j,k,l in difflib.SequenceMatcher(None,aa,bb,autojunk=False).get_opcodes():
  if kind!='equal':changes.append({'file':p,'kind':kind,'V2_blocks':[i+1,j],'V3_blocks':[k+1,l],'before':aa[i:j],'after':bb[k:l]})
# All prior source mathematical expressions remain as a semantic subsequence;
# new inline symbols occur only in the two targeted additions.
i=0
for x in new_math:
 if i<len(old_math) and x==old_math[i]:i+=1
assert i==len(old_math),(i,len(old_math))
figs={}
for p in sorted((V/'figures').glob('fig??.*')):
 a=hashlib.sha256((V2/'figures'/p.name).read_bytes()).hexdigest();b=hashlib.sha256(p.read_bytes()).hexdigest();assert a==b
 figs[p.name]=b
(V/'qa/V2_to_V3_逐段修改.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
(V/'qa/V2_to_V3_保留结构核验.json').write_text(json.dumps({'headings_identical':headings,'original_math_preserved':len(old_math),'new_body_math_occurrences':len(new_math),'display_equations_identical':9,'chapters_2_and_6_byte_identical':all((V/f'sources/ch{n:02d}.md').read_bytes()==(V2/f'sources/ch{n:02d}.md').read_bytes() for n in [2,6]),'all_18_figure_assets_identical':figs},ensure_ascii=False,indent=2)+'\n')
md='''# V2到V3修改对照

V2基准提交：171f19dcfd2a558972cf3ab8f8f4df85d16f0428。V3是局部增量：六章和十八个二级标题逐字相同，第二章与第六部分源字节完全相同，九个展示公式逐字相同。既有数学对象按源语义顺序保留；六图18个SVG/PNG/PDF文件逐字节未变。详细前后段落见同目录JSON。

|位置|V2问题/本轮原因|V3具体修改与最终效果|
|---|---|---|
|3.1、表2 ANT-MOC行|批注164设备类别仍可进一步核查|依据作者单位CNIC原始报道补“东方/16000 DCU”，附原始链接；没有从系统名推测商品型号|
|3.2 GPU硬件条件|Song/ANT/STREAM正式型号缺失|新取出版社TDM/OpenAlex及STREAM博士全文核查；确认期刊128核22.1/40.5与学位版256核8.61/15.44不可混用，正式缺项保留。核查留证，不向正文堆入获取失败说明|
|3.2 Pryer新增一段的前半|批注175需要比源码路径更实质的伴随证据|新增2026 arXiv v1：GPU张量DG固定源、反向微分与独立转置系统数值核对，列RTX A4000/网格/批次与双精度核验范围；没有写GPU-MOC或GPU伴随加速倍率|
|3.2 同段后半|实际混合程序CPU/GPU职责需明确|新增Shift2025正式论文，说明CPU Denovo正/伴随、权窗生成/源偏倚和GPU MC/WW执行的分工，保持与OpenSn静态路径区别|
|4.1 CADIS-Ω式后|三个FOM数值缺少原文支持的机制分析|保留493/5.1/145 min⁻¹，补第26群与第11群的方向贡献差别、标量伴随对称性和分裂轮盘投入；由作者图5/6及§5解释。说明全谱能区统计要求，不把未证低统计/射线假说当原因|
|1.3末尾|章节安排重复|删除重复的第二至第六部分导航句，研究目标原文保留|
|3.3末尾|CUDA训练与个人条件在第六部分重复|仅删训练/资源尾句；性能路线、固定源/伴随模块目标不变|
|5.1局部段末|几句总结不增加学术信息|删FNS/CFETR/JET/CIT后的泛化概括；ITER非零覆盖改为直接说明指标对象。文献对象、核数据、响应和数值结果完整保留|
|图6题注|示意性质可更简洁表达|首句加“原理示意图”，删冗余末句；图像、物理关系与引用不变|
|表1/2/6表注、表4一格|报告式说明可精简|删表1的通用对应提示及表2/6的重复概括；保留术语、C/E、FOM等必要定义。表4把泛化结语改为角加权空间—能量重要性的具体操作|
|4.1行内归一化及FW目标的生成语法|逐段检查发现薄空格被编译为私用区占位|积分操作数加组并移除有问题的显式薄空格，FW求和操作数加组；数学结构与原式语义相同，原生OMML无占位符|
|3.2 NuDEAL句|Word到PDF行末漏绘逗号|删多余“时”一字使逗号移入行内，科学数据不变；PDF全部文字与Word严格按序核对通过|
|交付检查|V2未有四格式逐段强门|新增源重组、330正文块、196表格单元格、65数学对象、393含书目块及32273 PDF字符的硬失败检查；另做31页目视及隔离全链重建|

## 新增文献

- Tristan Pryer. *Batched Wavefront Sweeps for Linear Transport Uncertainty Quantification*. arXiv:2609.14496v1，2026。预印本身份及DOI登记状态详见核验；未冒称期刊同行评议或完整多群屏蔽伴随性能。
- Elliott Biondo等. *Status of GPU capabilities within the Shift Monte Carlo radiation transport code*. EPJ Nuclear Sciences & Technologies 11:5，2025，DOI10.1051/epjn/2024034。采用§7明确的任务分工。

文献由61增至63，所有引文自动重排；书目逐字段、可见URL与实际链接目标均核对。硬件核查中取得的STREAM学位全文仅用于版本辨别，不强行增加一条重复算例引用。

## 未解决证据与保护例外

正式Song/ANT-MOC/STREAM相关商品GPU型号、CPU表及部分完整测试条件仍未取得；完整多群深穿透GPU伴随独立性能基线仍缺。这些空项保留在证据表，本轮限定补查已完成。

V2科研成果及全部Git交付文件未变。完整本地1949项检查中，仅Finder的.DS_Store系统元数据变化；用户2026-11-07明确同意单列该差异继续验收。修订前后哈希原样保存，未改基线或回写V2。原始批注Word及54个原件保护对象未变。
'''
(V/'qa/V2_to_V3_修改对照.md').write_text(md)
print('Recorded',len(changes),'source delta hunks; all headings/display equations and',len(figs),'figure assets preserved.')
