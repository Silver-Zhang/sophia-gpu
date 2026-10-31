from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
RECORDS = json.loads((ROOT / 'sources/逐节定稿与修订记录.json').read_text())
SRC = {x['line']: x['text'] for x in RECORDS}
TARGET = ROOT / 'exports/博士科研计划书_唯一审查底稿.md'


def body(text):
    return re.split(r'(?m)^### 本节论证功能自检', text)[0].strip()


def replace_once(text, old, new):
    assert text.count(old) == 1, (old[:100], text.count(old))
    return text.replace(old, new, 1)


def setsec(text, number, content, title=None):
    pattern = rf'(?ms)^### {re.escape(number)} ([^\n]+)\n(.*?)(?=^### |\Z)'
    matches = list(re.finditer(pattern, text))
    assert len(matches) == 1, (number, len(matches))
    m = matches[0]
    heading = title or m.group(1)
    return text[:m.start()] + f'### {number} {heading}\n\n{content.strip()}\n\n' + text[m.end():]


def section(text, number):
    return re.search(rf'(?ms)^### {re.escape(number)} [^\n]+\n(.*?)(?=^### |\Z)', text).group(1).strip()


def save(chapters):
    title = '# 面向聚变堆屏蔽快速方案迭代的块结构体素—GPU-MOC协同设计\n\n'
    TARGET.write_text(title + '\n\n'.join(chapters[i].strip() for i in range(1, 12)) + '\n')


C = {1: body(SRC[793]), 2: body(SRC[849].split('## 2 研究问题与目标', 1)[1]),
     3: body(SRC[933]), 4: body(SRC[1021]), 5: body(SRC[1081]),
     6: body(SRC[1148]), 7: body(SRC[1234]), 8: body(SRC[1311]),
     9: body(SRC[1382]), 10: body(SRC[1418]), 11: body(SRC[1458])}
C[2] = '## 第2节 研究问题与目标\n\n' + C[2]
for i in (1, 3, 4):
    C[i] = re.sub(rf'^## {i} ', f'## 第{i}节 ', C[i])

# P0: consolidate all previously approved replacements before this audit revision.
C[1] = replace_once(C[1], 'Kim等（2026，已在线发表）', 'Kim等（2026，已在线发表，online first）')
C[1] = replace_once(C[1], '本课题的体素指承载材料与输运未知量的确定论MOC网格；蒙卡几何体素化则指用体素近似几何与材料分布，二者用途不同。', '本课题的体素指确定论MOC的空间／材料离散单元，定义见3.1；蒙卡几何体素化不进入本课题实验路线。')
old = '因此，本课题在固定响应精度要求与显存预算下，联合比较体素表示与轨迹生成／缓存、轨迹分组和通量归约策略，检验局部加密能否保住关键输运路径上的精度底线，并缩短方案迭代周期。收益归因须同时考察准备时间、单次扫描时间与迭代次数；新增准备开销、不规则访存和负载不均可能抵消求解时间的节省，本课题不预设局部加密更快。'
new = '因此，本课题在固定响应精度要求与显存预算下，联合比较体素表示与轨迹生成／缓存、轨迹分组和通量归约策略，检验局部加密能否在关键输运路径上满足精度要求的同时缩短方案迭代周期。收益归因须同时考察准备时间、单次扫描时间与迭代次数；新增准备开销、粗细分界面处理开销和块间负载不均可能抵消求解时间的节省，本课题不预设局部加密在所有条件下更快，而是检验其在何种条件下更快、在何处失效。'
C[1] = replace_once(C[1], old, new)
C[2] = replace_once(C[2], '固定各网格配置', '固定两种表示各自的网格配置')
C[2] = replace_once(C[2], '以未参与建模的算例完成适用区间复核，并量化误判率与边界偏差为达成', '以未参与建模的算例检验准则预测的收益方向与失效位置是否与实测一致，统计不一致的比例与边界偏差为达成')
C[5] = replace_once(C[5], 'Baker等（2013）为目标响应驱动的局部细化提供了先例，但不支持块结构GPU-MOC上的加速结论。', 'Baker等（2013）采用目标响应驱动的各向异性网格自适应，提供响应导向的细化先例，但不支持块结构GPU-MOC上的加速结论。')
C[5] = replace_once(C[5], '跨层操作与通信元数据', '跨层数据交换与元数据维护')
C[5] = replace_once(C[5], '沿用第4节最大工作量／平均工作量的口径，分别记录块级与线程束内的不均衡，并结合活跃线程比例和扫描时间判断其影响', '沿用第4节线程束内分段数最大值与均值之比的口径，并另行定义块级不均衡度（块间分段数标准差与均值之比），两者分别记录；结合活跃线程比例和扫描时间判断其影响')
C[6] = replace_once(C[6], '正式比较前冻结响应集合、参考值及容限，各响应按', '本课题将前述“目标响应误差容限”具体化为绝对＋相对组合容限，以避免参考响应接近零时单纯相对误差判据不稳定。正式比较前冻结响应集合、参考值及两项容限，各响应按')
cache = r'部分缓存容量属于本课题的设计选择，并非引用Zhou等（2025）的实现参数；容量上限初设为显存预算的四分之一，即 \(X=0.25M_{\mathrm{budget}}\)，以限制轨迹缓存占用，为通量、材料数据和临时缓冲保留预算。该比例经预实验校准后对两种表示统一冻结；缓存对象按固定轨迹编号顺序选取，不随分组开关改变。若全部轨迹均可装入该容量，则标记为全缓存，不重复作为独立的部分缓存样本。'
C[6] = replace_once(C[6], '部分缓存固定容量和选取规则', '部分缓存容量和选取规则在正式测量前冻结')
C[6] = replace_once(C[6], '显存不可行组合保留为约束记录。', '显存不可行组合保留为约束记录。\n\n' + cache)
C[6] = replace_once(C[6], '[NVIDIA CUDA计时指南](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#timing)', '计时依据为NVIDIA《CUDA C++ Best Practices Guide》（Release 13.4）第9.1节“Timing”，主机计时与异步同步要求参照[§9.1.1 Using CPU Timers](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#using-cpu-timers)，GPU事件计时参照[§9.1.2 Using CUDA GPU Timers](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#using-cuda-gpu-timers)。')
C[6] = replace_once(C[6], '报告配对差中位数、四分位距及2000次配对自助重采样的95%置信区间', '报告配对差中位数、四分位距及配对自助重采样的95%置信区间；重采样采用预设次数（如2000次），在预实验中检查区间端点对重采样次数的敏感性，并在正式比较前冻结')
C[6] = replace_once(C[6], '相对偏差超过本课题预设的1%，即暂停归因，排查遗漏、重叠及插桩扰动，不以未分类残差补齐。', '相对偏差超过预设阈值时，暂停归因并排查遗漏、重叠及插桩扰动。阈值初设为1%，在预实验中依据实测计时噪声与插桩扰动校准，并在正式比较前冻结；不得根据正式比较结果事后放宽，也不得以未分类残差补齐。')
C[6] = replace_once(C[6], '每配置、每场景完成10次独立重复，配对运行顺序随机化。', '每配置、每场景拟以10次独立重复为起点，预实验后依据配对差的实测波动及置信区间宽度要求确定正式测量次数，必要时增加，并在正式比较前冻结；每组配对两侧采用相同重复次数，运行顺序随机化。自助重采样用于估计统计不确定性，不能替代独立重复。')
C[7] = C[7].replace('失效侧', '无时间收益侧').replace('失效区间', '无时间收益区间').replace('失效区', '无时间收益区')
C[7] = setsec(C[7], '7.1', r'对同一算例、同一场景的第 \(j\) 次配对运行，记 \(d_j=T_{\mathrm{局部},j}-T_{\mathrm{均匀},j}\)。\(\Delta T\)按6.6的配对差计算，以下均指配对差中位数，即 \(\Delta T=\operatorname{median}_j(d_j)\)。两种表示均满足精度与显存约束时，\(\Delta T\geq0\)定义为局部加密无时间收益，即均匀细体素不慢于局部加密；是否能够明确判向，仍须按7.3的置信区间与噪声规则判断。另以峰值显存超过预算定义显存不可行，该配置直接退出比较，形成可行域的约束截断，不记为时间收益失效。精度未达标的样本也不进入时间边界估计。', '局部加密无时间收益与显存不可行')
C[7] = replace_once(C[7], '描述量选取参考AMReX的块划分、重建与负载管理经验，以下方向均为待检验假设。[Zhang等，2021，§5.2](https://doi.org/10.1177/10943420211022811)', '本课题类比AMReX的块管理经验选取描述量；该文献提供块划分、网格重建和负载管理的实现参照，不直接支持以下GPU-MOC边界方向假设。[Zhang等，2021，§5.2](https://arxiv.org/pdf/2009.12009#page=4)')
C[7] = replace_once(C[7], '固定评估时段与更新构成时，更新频率增加预期放大单位更新的净时间差：复用更新净省时可能推向适用侧，反之推向无时间收益侧。这些预期须由7.4检验。', r'在单位更新的时间差及更新构成保持不变时，提高更新频率会增加固定评估时段内的更新次数，预期放大更新阶段累计时间差的绝对值。单次更新上的 \(|\Delta T|\) 不会因此自动增大；完整累计周期的收益方向还须计入首次准备成本。上述预期须由7.4检验。')
C[7] = replace_once(C[7], '拟合零水平集给出等时边界，允许多个不相连区间，不跨越离散配置跳变强行插值。', r'拟合零水平集给出等时边界，即在精度与显存均达标的参数空间内，以 \(\Delta T=0\) 为分界，区分适用区与无时间收益区；分界附近保留不确定带，允许多个不相连区间，不跨越离散配置跳变强行插值。')
C[7] = replace_once(C[7], '统计可判向样本中的方向不一致比例、边界位置偏差及可判定覆盖率。', '统计可判向样本中的方向不一致比例、边界位置偏差及可判定覆盖率。可判定覆盖率指全部留出算例中，精度与显存达标、预测与实测时间差区间均不跨零，且通过6.6噪声判据、能够明确核对收益方向的样本比例。')
uncertain = '预测区间跨零或差异未超过计时噪声时，不给出表示—执行组合的选择建议，标记为需补充测量：重复波动主导时增加独立重复次数；边界定位过粗时加密邻近参数采样；留出偏差主导时新增独立留出算例，并保留原有检验结果。补测后仍无法判向，则维持未判定状态。其适用条件为精度与显存约束已满足，但时间收益方向尚不能可靠分辨。'
transfer = '本课题所称“可迁移”，指条件化判定框架可复用：在新条件下，仍可沿用先检查约束、再判断时间收益方向、最后处理不确定性的流程，回答“在何种条件下选择哪种表示—执行组合”。具体参数区间须重新标定并经独立检验，已有数值范围不直接外推。'
C[7] += '\n\n' + uncertain + '\n\n' + transfer
C[8] = replace_once(C[8], 'GPU移植、EXP／OTF比较及其已有加速机制', 'GPU移植、EXP／OTF比较和Zhou等报告的加速机制')
C[8] = replace_once(C[8], 'Baker等（2013）在含探测器的固定源屏蔽计算中，以目标响应驱动各向异性网格自适应，提供响应导向的局部细化先例。', 'Baker等（2013）在含探测器的固定源屏蔽计算中，采用目标响应驱动的各向异性网格自适应，提供响应导向的细化先例。')
C[8] = replace_once(C[8], '并保留不确定带内的补测规则', '并按7.5对不确定带内结果暂不作选择、转入补测')
C[8] = replace_once(C[8], '保留无净收益、显存不可行和未判定结果', '保留无净收益、显存不可行和不确定带结果')
C[9] = setsec(C[9], '9.1', '块结构网格框架已有，状态为**已确认**。\n\n- **MOC求解器本体：待确认。**须核实是否可访问、可修改及其GPU化程度。\n- **求解器接口：待确认。**须核查网格、轨迹、截面与通量接口，以及代码访问条件。\n- **GPU设备：待确认。**型号、显存、使用权限和可用时段尚未提供。\n- **性能分析工具：待确认。**安装情况、版本兼容性和性能计数器访问权限尚未核实。\n- **申请人课程与计算基础：已确认（据本人提供材料）。**已修数学物理方法、辐射屏蔽设计、核反应堆物理等课程，具备Python、C++及Linux、Git开发与版本管理经验。\n- **申请人相关项目经历：已确认（据本人提供材料）。**具有Geant4屏蔽装置、加速器大厅及电子加速器靶结构建模经历，以及基于OpenMC、Serpent参考结果的群常数校准项目经历，涉及敏感性分析、降阶建模和优化；硕士课题围绕石墨吸收群常数自动化修正开展，当前在研，不将预期成果列为已完成。上述经历支撑输运建模、屏蔽评估与计算流程开发，不等同于已有GPU-MOC实现能力。\n- **GPU编程与MOC实现能力：尚不具备，需系统学习。**已有Python、C++编程及粒子输运建模经验，可为学习GPU编程与MOC实现提供一定基础；专项能力须通过后续学习、代码实践与正确性验证建立，具体学习安排尚待确定。')
C[9] = C[9].replace('叶单元', '网格单元')
C[10] = replace_once(C[10], '两条条件化选择准则及检验报告，并记录不确定带处理', '两条选择准则及一条不确定带处理规则，以及相应检验报告')
C[10] = replace_once(C[10], '进入下一阶段的门槛（最终提交门槛）为三个RQ各有对应证据与结论，两条选择准则均有检验结论，不确定带有处理记录；降级情形按9.4修订目标验收，明示原RQ未完成项。', '最终提交门槛：三个RQ各有对应证据与结论，选择准则及不确定带处理均有检验记录；降级情形按9.4修订目标验收，明示原RQ未完成项。')
save(C)

old = ROOT / 'exports/博士科研计划书大纲.md'
historical = ROOT / 'exports/大纲_历史版本_已废弃.md'
warning = '本文件含已退出主线的几何误差与耦合目标，不得作为写作依据'
if old.exists():
    assert not historical.exists(), 'Historical destination already exists'
    old.rename(historical)
    historical.write_text(warning + '\n\n' + historical.read_text())
assert historical.exists() and historical.read_text().startswith(warning)

# P1 group 1: joint selection objective; keep calibration and held-out scenarios separate.
C[6] = replace_once(C[6], '参数在调参集选定，测试集冻结；更新时若需重调，其耗时计入方案周期。', '择优标准为：在预先指定的场景或更新序列上，按1.3定义的完整达标周期取最短者；表示参数与执行参数联合择优，不分开择优后再拼接。择优所用场景与正式比较场景分离，正式比较前冻结所选配置；更新时若需重调，其耗时计入方案周期。')
C[6] = replace_once(C[6], '采用表示二水平×轨迹三水平×分组二水平×归约二水平。', '按6.1的择优标准，第一层表示因素的两个水平为对等调参预算内择优并冻结的一对均匀细体素配置与局部加密配置；在该对配置内不再重调网格。采用表示二水平×轨迹三水平×分组二水平×归约二水平的因素组织。')
C[10] = replace_once(C[10], '按6.1确认基线的优化及调参程度', '按6.1的择优标准确认基线的优化及调参程度')
save(C)

# P1 group 2: two experiment layers, pre-registered before formal measurement.
layers = '消融实验分两层。第一层（RQ2）固定6.1择优得到的一对配置，只交叉执行策略，用于归因。第二层（RQ3）使用预先登记的多组网格配置，覆盖不同块尺寸、加密比例和界面密度；每组内部执行同一套预先登记的执行策略消融规则子集，用于刻画边界关系。两层配置集均在正式测量前登记冻结，不得用留出数据追加配置或重新择优。'
C[6] = setsec(C[6], '6.3', section(C[6], '6.3') + '\n\n' + layers)
C[7] = setsec(C[7], '7.2', '边界数据来自6.3第二层预先登记的多组配置。' + section(C[7], '7.2'))
C[10] = replace_once(C[10], '按6.3开展四因素交叉消融', '按6.3开展两层消融')
save(C)

# P1 group 3: paired estimands, aggregation order, and the conservative measured-only policy.
C[6] = replace_once(C[6], '再以该差在两种表示间的差值刻画交互作用。', '再以该差在两种表示间的差值刻画交互作用。统计顺序为：先在每次配对重复内构造单因素差与交互差，再对差值序列汇总中位数并重采样；不得先汇总各因素中位数再相减。')
C[7] = setsec(C[7], '7.1', r'''场景配对差是在同一场景、同一重复内，局部加密与均匀细体素按1.3定义的完整周期之差，即 \(d_{s,j}=T_{\mathrm{局部},s,j}-T_{\mathrm{均匀},s,j}\)，场景统计量为 \(\Delta T_s=\operatorname{median}_j(d_{s,j})\)。序列累计配对差是在固定更新序列上，两种表示各自累计完整周期之差；先在每次重复内汇总首次计算及全部更新周期，再作两种表示之差，最后对差值序列取中位数，记为 \(\Delta T_{\mathrm{seq}}\)，不得将各场景中位数直接相加。以下统称ΔT时，图表须注明使用场景统计量还是序列统计量。

两种表示均满足精度与显存约束时，ΔT≥0定义为局部加密无时间收益，即均匀细体素不慢于局部加密；是否能够明确判向，仍按6.6与7.3的区间及噪声判据判断。ΔT=0为等时边界，是以连续时间差刻画的收益边界。另以峰值显存超过预算定义显存不可行，该配置直接退出比较，形成可行域的约束截断，不记为时间收益失效。精度未达标的样本也不进入时间边界估计。''')
C[7] = C[7].replace('单次更新上的 \\(|\\Delta T|\\) 不会因此自动增大', '单次更新上的 \\(|\\Delta T_s|\\) 不会因此自动增大')
C[7] = setsec(C[7], '7.3', r'''基于6.3第二层数据建立含交互项的ΔT模型。实测统计区间来自6.6的配对差置信区间，用于已实测配置点上的方向判定：通过噪声判据后，区间完全位于零以下者列为适用区间，完全位于零以上者列为无时间收益区间；区间跨零或差异未超过计时噪声者列为不确定带。

模型预测区间包含模型误差项，用于估计待测区域的边界位置及指导后续测量选点，不直接触发表示—执行组合选择。本课题采用保守方案：两条选择准则只在完成独立检验的实测覆盖范围内生效，不将预测符号直接外推为选择结论。预测区间在7.4留出检验中检查覆盖；若据此校准模型或修订区间，须用新的独立留出算例复检。

拟合零水平集估计等时边界，即在精度与显存均达标的参数空间内，以ΔT=0为分界区分适用区与无时间收益区，分界附近保留不确定带；允许多个不相连区间，不跨越离散配置跳变强行插值。沿预定参数路径，边界偏差定义为预测零点到留出实测过零区间的距离，按参数范围归一化，同时报告区间宽度。实测判向不确定性、模型预测不确定性及留出偏差分别记录；没有实测支持的区域保留为待测范围，不给出组合选择结论。''')
C[7] = setsec(C[7], '7.5', r'''拟形成两条待检验的选择准则。在精度与显存达标、实测区间完全位于ΔT<0且通过6.6噪声判据时，选择局部加密及对应的轨迹、分组、归约组合；其适用条件为留出检验通过，且输入与更新场景处于实测覆盖的验证范围。在相同约束下，实测区间完全位于ΔT>0且通过噪声判据时，选择均匀细体素及对应执行组合；其适用条件为该组合通过独立检验，且输入与更新场景处于实测覆盖的验证范围。

另设一条不确定带处理规则：实测区间跨零或差异未超过计时噪声时，不给出组合选择建议，标记为需补充测量；重复波动主导时增加独立重复次数，边界定位过粗时加密邻近参数采样，留出偏差主导时新增独立留出算例，并保留原有检验结果。未实测区域仅用预测区间指导选点，完成实测及检验前不作组合选择；补测后仍无法判向，则维持未判定状态。其适用条件为精度与显存约束已满足，但时间收益方向尚不能可靠分辨或尚缺实测支持。

已有块结构网格框架为几何与网格规模变化提供构造基础，二者及基准GPU容量内的显存预算变化拟列入验证范围，具体设备使用条件仍须确认。能群数迁移需要匹配的多群截面库，跨GPU架构迁移需要额外设备；这些资源尚未确认，暂列讨论边界。

本课题所称“可迁移”，指条件化判定框架可复用：在新条件下，仍可沿用先检查约束、再判断时间收益方向、最后处理不确定性的流程，回答“在何种条件下选择哪种表示—执行组合”。具体参数区间须重新标定并经独立检验，已有数值范围不直接外推。''')
save(C)

# P1 group 4: standalone selection/pilot cost; scenario attribution is not additive duplication.
C[1] = replace_once(C[1], '纳入几何与材料更新、模型检查、数据准备及传输、全部输运迭代和响应提取', '纳入几何与材料更新、模型检查、必要的表示—执行选择与预运行、数据准备及传输、全部输运迭代和响应提取')
C[6] = replace_once(C[6], '准备阶段截止首轮扫描前', '准备阶段截止首轮正式扫描前')
pilot = '另设“表示—执行选择与预运行”独立计时项，包括为当前方案服务的配置择优、特征提取、收敛预估计等计算，计入完整周期，与正式扫描划界，不重复计入准备或扫描。费用按实际发生次数记录；离线调参成本另报，评价含该投入的累计周期时只计一次，不向每次更新重复挂账。'
C[6] = setsec(C[6], '6.4', section(C[6], '6.4') + '\n\n' + pilot)
C[6] = replace_once(C[6], '首次计算从无方案缓存状态开始，计入初始化、建网与建缓存；可复用更新限定为网格和轨迹保持有效的源项修改，仍计输入处理、有效性检查与数据刷新；重建更新采用几何或网格变更，计入失效判定、受影响数据重建和传输。', '首次计算从无方案缓存状态开始，计入初始化、建网与建缓存，选择与预运行由初始化环节触发；可复用更新限定为网格和轨迹保持有效的源项修改，仍计输入处理、有效性检查与数据刷新，选择与预运行由有效性检查环节触发；重建更新采用几何或网格变更，计入失效判定、受影响数据重建和传输，选择与预运行由失效判定环节触发。上述场景归属仅标明费用来源，耗时统一进入6.4的独立计时项，并从相应父项中扣除，不再重复相加。')
C[6] = replace_once(C[6], '依据去重后的准备、逐轮扫描、其他迭代工作、输出及显式记录的等待重构总时间', '依据去重后的表示—执行选择与预运行、准备、逐轮扫描、其他迭代工作、输出及显式记录的等待重构总时间')
save(C)

# P1 group 5: separate feasibility and directional coverage.
C[7] = setsec(C[7], '7.4', r'''留出算例按几何族划分，不参与6.1调参与7.2描述量的建模。模型预测仅使用事前可得信息；收敛等事后量若用于预测，须由预运行估计，其耗时归入6.4独立计时项，并按6.5记录触发场景。模型方向与实测方向的比较仅用于独立检验，不绕过7.5的实测覆盖限制。

两种表示均通过精度、收敛与显存约束的样本记为可行样本；预测与实测区间均能通过6.6噪声判据、明确核对方向的可行样本记为可判向样本。分报总体覆盖率（可判向样本／全部留出样本）、可行性覆盖率（可行样本／全部留出样本）、可行域内判向覆盖率（可判向样本／可行样本），并在可判向样本中统计方向预测不一致比例。可行样本数为零时，判向覆盖率记为不适用，不据此判定时间选择准则失效。

准则是否成立依据可行域内判向覆盖率与方向不一致比例，采用正式检验前冻结的验收要求，不以总体覆盖率作为判据；能够定位过零区间的样本还须满足预设边界偏差要求。不满足相应要求时，按原因报告准则在该测试范围内不成立及适用范围收缩。未进入判向的样本分类记录显存不可行、精度未达标、参考不确定度不足以判定、区间跨零及计时噪声不可分辨等原因。没有实测过零区间时，不宣称定位准确。''')
save(C)

# P1 group 6: resource-conditioned fallback, then P2 wording/empty-region clarifications.
C[9] = replace_once(C[9], '须同步修订研究范围。', '须同步修订研究范围。上述退路的前提是MOC求解器可访问、可修改且GPU资源可用；若求解器或设备条件未落实，则属资源阻断而非研究降级，须按资源条件修订目标与进度，不承诺GPU性能成果。')
C[10] = replace_once(C[10], '触发降级时同步修订后续目标与门槛。', '触发降级时同步修订后续目标与门槛；资源条件未落实时，按9.4的资源阻断条款处理，不进入阶段二。')
C[5] = replace_once(C[5], '累计迭代耗时可能下降，其实现取决于单轮耗时下降且收敛行为不恶化；未知量减少不意味着迭代次数减少，必须同时记录每轮耗时与达标所需迭代次数。', '累计迭代耗时可能下降，其实现取决于每轮耗时与迭代次数共同决定的实测总量。收敛不恶化是有利条件，而非准入条件；累计迭代耗时是否下降最终以实测为准，即使迭代次数增加，累计耗时仍可能下降。未知量减少不意味着迭代次数减少，必须同时记录每轮耗时与达标所需迭代次数。')
C[7] = replace_once(C[7], '上述预期须由7.4检验。', '收敛变化按5.2作为成本解释量，不作为准入条件；上述预期须由7.4检验。')
C[3] = replace_once(C[3], '并须检查有效计算单元的覆盖以及轨迹分段有无遗漏或重复。', '并须检查参与输运计算的有效网格单元覆盖完整、无重复计入，以及轨迹分段有无遗漏或重复；层级覆盖方式按代码核实，不推定采用树结构。')
C[9] = replace_once(C[9], '核验网格单元覆盖无缺口、无重复，父子关系与邻接索引一致。', '核验参与输运计算的有效网格单元覆盖完整、无重复计入，检查层级关系与邻接索引一致；层级覆盖方式按代码核实，不推定采用树结构。')
C[9] = replace_once(C[9], '若正确性通过且按6.6确认无时间收益', '收敛变化按5.2处理；若正确性通过且按6.6确认无时间收益')
C[10] = replace_once(C[10], '以及相应检验报告。进入下一阶段', '以及相应检验报告。适用区间、无时间收益区间、不确定带均允许为空；未观测到方向转换时，交付已测范围与未定位边界的说明，不要求必须发现局部加密占优区间。进入下一阶段')

# Cross-reference alignment without changing the agreed RQs or extending scope.
C[2] = C[2].replace('块内归约后累加', 'GPU线程块内归约后累加')
C[2] = replace_once(C[2], '检验准则预测的收益方向与失效位置是否与实测一致，统计不一致的比例与边界偏差为达成', '检验模型预测的收益方向与失效位置是否与实测一致，并核对实测覆盖范围内的两条选择准则及一条不确定带处理规则，统计方向不一致比例、覆盖率与可定位边界的偏差为达成')
C[2] = replace_once(C[2], '在RQ1条件下固定两种表示各自的网格配置，交叉切换', '在RQ1条件下，按6.3第一层固定两种表示各自的网格配置，交叉切换')
C[2] = replace_once(C[2], '固定物理与求解设置，分别改变加密比例', '固定物理与求解设置，按6.3第二层预先登记的配置分别改变加密比例')
C[3] = C[3].replace('块结构框架已有；局部加密尚未实现', '块结构网格框架已有；MOC求解器本体与GPU资源状态见9.1；局部加密尚未实现')
C[5] = replace_once(C[5], 'AMReX的实现需维护跨层数据交换与元数据维护', 'AMReX的实现涉及跨层数据交换与元数据维护')
C[6] = replace_once(C[6], '消融时固定两种表示各自的网格配置及其余参数', '每组消融内部固定两种表示各自的网格配置及其余非目标参数')
C[6] = replace_once(C[6], '嵌套子项不再次相加，跨流重叠按时间轴去重', '嵌套子项不再次相加，CPU／GPU并发及跨流重叠按统一时间轴去重')
C[7] = replace_once(C[7], '预测区间在7.4留出检验中检查覆盖；若据此校准模型或修订区间，须用新的独立留出算例复检。', '预测区间在7.4留出检验中检查覆盖；后续选点限于新一轮预先登记的测量，不得据原留出结果回改本轮冻结配置。若校准模型或修订区间，须保留原检验结果，并用新的独立留出算例复检。')
C[9] = C[9].replace('局部加密需本课题在已有框架上', '局部加密需本课题在已有网格框架上')
C[10] = replace_once(C[10], '按7.3建立ΔT模型，按7.4开展留出检验', '按7.3建立ΔT模型，预测仅用于边界估计与后续选点，按7.4开展留出检验')
save(C)


# User review: three new P1 corrections and P2 consistency fixes.
C[2] = setsec(C[2], '2.1', section(C[2], '2.1') + '最快达标配置在调参场景上确定并冻结，正式比较在独立的测试场景上进行，详见6.1。')
C[2] = replace_once(C[2], '统计方向不一致比例、覆盖率与可定位边界的偏差', '统计方向不一致比例、各类覆盖率与可定位边界的偏差')
C[6] = setsec(C[6], '6.1', section(C[6], '6.1') + '上述固定条件针对每个配对比较点；第二层不同点之间允许按预先登记方案受控改变几何布局、更新序列与显存预算，同一点内两种表示的物理输入、更新序列及预算保持一致。')
C[6] = replace_once(C[6], r'，即 \(X=0.25M_{\mathrm{budget}}\)', '')
C[6] = replace_once(C[6], '消融实验分两层。第一层（RQ2）固定6.1择优得到的一对配置，只交叉执行策略，用于归因。第二层（RQ3）使用预先登记的多组网格配置，覆盖不同块尺寸、加密比例和界面密度；每组内部执行同一套预先登记的执行策略消融规则子集，用于刻画边界关系。两层配置集均在正式测量前登记冻结，不得用留出数据追加配置或重新择优。',
'''消融实验分两层。第一层（RQ2）除表示二水平（即6.1择优冻结的那对配置）外，仅交叉执行策略因素，用于归因。

第二层（RQ3）使用预先登记的多组配置，选取原则为分层抽样而非择优。关键区域占比通过几何族内不同屏蔽布局变化实现；修改范围与更新频率通过6.5的三类场景序列实现，重建比例由序列中需要重建的更新所占比例控制；显存预算通过受控的预算档位实现。配置按块尺寸、加密比例和界面密度分层抽样，依据预实验提示覆盖候选边界附近及两侧，不预设一定观测到收益方向转换。每组内部执行同一套预先登记的执行策略消融规则子集，用于刻画边界关系。配置点数量须与7.3的模型复杂度匹配；两层配置集、采样规则及点数均在正式测量前登记冻结，不得用留出数据追加配置或重新择优。''')
C[6] = setsec(C[6], '6.5', section(C[6], '6.5') + '第二层各序列预先登记修改范围、固定设计评估时段内的更新次数及重建更新比例；序列构成在正式测量前冻结。')
C[6] = setsec(C[6], '6.6', section(C[6], '6.6') + '第一层的交互归因结论限于该对择优配置及第二层实测支持的邻域，不外推为表示—执行的普遍交互规律；可迁移性按7.5的框架可复用界定。')
C[7] = replace_once(C[7], '基于6.3第二层数据建立含交互项的ΔT模型。', '基于6.3第二层数据建立ΔT模型，先拟合主效应；仅当交互项在预实验中可分辨、独立配置点数满足参数估计与剩余自由度要求且设计可辨识时，才纳入相应交互项。第二层配置点数量与候选模型复杂度在正式测量前匹配并登记，重复运行不计作新增独立配置点。配置点数不足时采用可加主效应模型，并在7.4留出检验中报告该简化对边界估计的影响。')
C[7] = replace_once(C[7], '预测与实测区间均能通过6.6噪声判据、明确核对方向的可行样本记为可判向样本', '实测区间通过6.6噪声判据、且预测方向与实测方向可明确核对的可行样本记为可判向样本；预测方向仅在含模型误差的预测区间不跨零时判定，不对预测区间套用实测计时噪声判据')
C[7] = replace_once(C[7], 'https://arxiv.org/pdf/2009.12009#page=4', 'https://doi.org/10.1177/10943420211022811')
C[8] = C[8].replace('达标总时间', '达标方案周期').replace('无净收益', '无时间收益')
C[9] = C[9].replace('未形成净加速', '未形成时间收益').replace('不以出现净加速作为验收前提', '不以出现时间收益作为验收前提').replace('已测无收益范围', '已测无时间收益范围')
save(C)

text = TARGET.read_text()
assert [int(x) for x in re.findall(r'^## 第(\d+)节 ', text, re.M)] == list(range(1, 12))
assert all(len(re.findall(rf'^### {i}\.\d+ ', text, re.M)) == expected for i, expected in [(1,4),(2,4),(3,4),(4,5),(5,6),(6,7),(7,5),(8,3),(9,4),(11,3)])
assert text.count('Wagner') == 1 and 'Wagner' not in '\n'.join(C[i] for i in range(1,11))
assert 'FW-CADIS' not in '\n'.join(C[i] for i in range(1,11))
for banned in ['量化误判率', '保住关键输运路径上的精度底线', '叶单元', '通信元数据', '其已有加速机制', '每配置、每场景完成10次独立重复', '申请人技能：未知']:
    assert banned not in text, banned
assert not old.exists()
assert '\\(' in text and '\\)' in text
assert text.count('\\(') == text.count('\\)')

qa = {'active_draft':str(TARGET.relative_to(ROOT)), 'historical_outline':str(historical.relative_to(ROOT)),
      'source_session':'01a14f3e-ba35-7c23-8887-5535bdfed119',
      'chapters':11, 'self_checks_in_main_text':False,
      'revisions':['P0: recovered and consolidated approved chapter text and all replacement clauses',
                   'P1.1: joint selection objective', 'P1.2: two-layer ablation',
                   'P1.3: paired statistics and measured-only selection rules',
                   'P1.4: standalone selection/pilot cost', 'P1.5: three coverage denominators',
                   'P1.6: resource prerequisite', 'P2: convergence/effective cells/empty regions'],
      'sha256':hashlib.sha256(text.encode()).hexdigest(), 'characters':len(text),
      'checks':'chapter order; section counts; extension confined to chapter 11; removed superseded phrases; balanced inline math; historical warning',
      'resource_status':'grid framework confirmed; MOC body/interfaces/GPU/tools pending; applicant courses/programming/projects supplied by applicant; GPU programming/MOC implementation competence not yet acquired; transferable programming/transport background available; learning schedule pending',
      'new_review_revisions':['P1: descriptor coverage and stratified second-layer sampling', 'P1: identifiable model complexity matched to independent configurations', 'P1: RQ1 independent test scenes', 'P2: terminology/coverage/scope/source consistency'],
      'verified_sources':{'CUDA':'Official Best Practices Guide PDF Release 13.4, 2026-10-12; checked 2026-10-20', 'Zhang2021':'Journal-typeset edition, DOI 10.1177/10943420211022811, section 5.2 Regridding and load balancing; checked 2026-10-20'},
      'chapters_1_to_4_status':'rechecked against merged draft and approved terminology anchors',
      'remaining_pending':'External solver/GPU/tool resources; applicant GPU programming/MOC implementation competence requires learning; specific learning schedule remains unconfirmed',
      'next_action':'user review of four replacement passages; no reference renumbering yet'}
(ROOT/'qa_logs/合并底稿核验记录.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
state_path=ROOT/'state.json'
state=json.loads(state_path.read_text())
state['status']='awaiting_user_review'
state['scope']='merged_research_proposal_chapters_1_to_11'
state['outputs']=[str(TARGET.relative_to(ROOT))]
state['active_review_draft']=str(TARGET.relative_to(ROOT))
state['current_scope']='chapters 1–11, frozen representation–execution co-design problem anchor'
state['current_status']='merged_and_revised_awaiting_user_review'
state['historical_outputs']=[str(historical.relative_to(ROOT)), 'exports/博士科研计划书大纲.docx']
state['next_step']='Review the sole merged draft; do not use the historical outline as a writing source.'
state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2))
print(json.dumps(qa,ensure_ascii=False,indent=2))

# Preserve the approved reference-numbering stage when rebuilding the draft.
import runpy
if (ROOT / 'sources/参考文献核验与编号记录.json').exists():
    runpy.run_path(str(ROOT / 'drafts/number_verified_references.py'), run_name='__main__')
