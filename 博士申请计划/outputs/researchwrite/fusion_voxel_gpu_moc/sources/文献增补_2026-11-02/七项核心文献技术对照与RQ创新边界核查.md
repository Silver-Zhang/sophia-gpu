# 七项核心文献技术对照与RQ创新边界核查（2026-11-02）

> 非定稿资料，不更改RP正文/原13条编号。范围：Liu(2023)、Song(2026)、Dzianisau & Lee(2026)、Buchan(2019)、Zhou(2025)、宋佩涛博士(2021)、汪岸博士(2025)。检索发现必须增补两项先例：Liu(2022)笛卡儿局部网格、Li等(2023) ANT-MOC。审阅口径：**验证证据仅限作者公开的测试条件**，并非第三方独立复现；未取得全文时不把“未报告”写成“作者绝对未做”。

## 证据等级

- A：实际阅读可访问全文及图表（Buchan 2019公开作者稿、Zhou 2025 arXiv PDF）；不是独立重现算例。
- B：出版社可索引正文节选、摘要、实验总结（Song 2026、Dzianisau & Lee 2026）或官方学位数据库长摘要（宋佩涛、汪岸）；未通读完整全文。
- C：出版社/ANS正式摘要（Liu 2023）；缺全文，不能核对附表、误差传播、计时边界。
- 凡言“没有”一律以“在已核查文本中未见证据”解释。

## 1. Liu et al. 2023 [C]

Cong Liu, Junxia Wei, Bin Zhang, Jinhong Li, Zhiqiang Sheng, Shuang Tan, *Goal-Oriented Mesh Adaptivity of Three-Dimensional Neutron Transport Calculation Using Weighted Difference Scheme and Dual-Weighted Residual Error Indicators*, NSE 197(11) 2853–2883, DOI:10.1080/00295639.2023.2169537; 官方摘要 https://wx1.ans.org/pubs/journals/nse/a_54070

- 解决：给定目标量（探测器响应、积分通量或keff）的局部网格自适应与成本降低。方法：多群三维SN加权差分；基于双重加权残差DWR；通过通量重构计算空间残差；提出固定源局部目标与临界非一致裂变源的伴随估计模型；讨论截断通量重构与各向同性伴随近似。硬件：在公开摘要无法核实CPU/线程/设备，不得写成GPU。
- 证据：作者正式摘要报告在相近目标精度下节约>70%的计算工作量和运行时间；因无法核查全文，不能断言对等调参、多次更新、计时是否含整个自适应过程。
- 不支持的扩张：“首次在固定目标响应精度下局部网格比全域细化更快”已经不成立。RQ1可比较GPU-MOC及完成方案迭代周期；RQ2可研究表示与轨迹缓存/分组/归约交互；RQ3可检验有显存截断且需重建时的失效条件。以上是交集外的**研究假设**，不是已证明空白。

## 2. Song et al. 2026 [B]

Qufei Song et al., *GPU-accelerated few-group 3D Method of Characteristics for full-core neutron transport in Small Modular Reactors*, PNE 192, 106109, DOI:10.1016/j.pnucene.2025.106109; https://www.sciencedirect.com/science/article/pii/S0149197025005074

- 解决：3D MOC单GPU超高显存需求。框架OpenMOC GPU移植（CPU/GPU异构）；3D平源显式存储、线性源、在线轴向轨迹追踪(OTF-ART)、轨迹批处理、GPU-CMFD、Track-Group并行；C5G7与NuScale和NETH-HCF175M两种SMR，最后基于MC生成的4群截面，但MC仅作为其截面输入，不表明本RP需要MC实验。
- 证据：单25cm组件显式3D段存储约22,129MB；综合存储优化在单组件降98.5%；初始平源单组件相对单线程CPU最高1015.8x；两类SMR全堆芯相对其CPU基线274.1x/378.9x（不同工况/基线的倍数不可横比）。检验包括正确性、性能及显存。公开节选不足以核对总计时是否纳入场景几何修改—重建—重新择优，以及更多原始数值误差。
- 与RP：GPU轨迹批处理、在线生成、CMFD和显存优化**已经不是原创**。RQ1区别是不同空间表示在共同精度/显存条件下的**联合选择**和完整更新周期；RQ2明确块级界面/轨迹长度分布改变执行策略收益；RQ3明确缓存阈值和更新族的净收益截断。

## 3. Dzianisau & Lee 2026 [B]

Siarhei Dzianisau, Deokjung Lee, *Axially decomposed GPU-enabled three-dimensional method of characteristics/diamond difference solver in neutron transport code STREAM3D-GPU*, CPC 319, 109952, DOI:10.1016/j.cpc.2025.109952; https://www.sciencedirect.com/science/article/pii/S0010465525004539 ; 开发组 https://reactorcore.unist.ac.kr/stream-3d-gpu/

- 解决：高群数3D MOC/DD轴向分解、异步执行及显存规模。注意3D MOC/DD不是与完全直接三维MOC等价的离散方案；GPU OpenACC/OpenMP、MPI域分解，官网报告72群/200轴向平面。
- 证据：OPR-1000四分之一堆芯含热工反馈，对STREAM3D CPU基线比较keff、归一化pin功率、燃料中心温度及平均温度；显存理论约50GB/进程降至<4.5GB，8/16卡相对128CPU核参考分别22.1x/40.5x，并报告成本/能耗估算。不能当作同硬件同线程的GPU加速比，成本/能耗不是第三方实测。
- 与RP：约束下分解执行与数据管理已有成熟方法；新问题是**非均匀块网格几何/材料表示变更**造成的轨迹、缓存、归约交互，及频繁设计修改的端到端成本。其反应堆临界/功率等与固定源屏蔽响应不同，但应用区别单独不足以构成方法创新。

## 4. Buchan et al. 2019 [A]

A.G. Buchan, S. Dargaville, C.C. Pain, *A combined immersed body and adaptive mesh method for simulating neutron transport within complex structures*, ANE, DOI:10.1016/j.anucene.2019.05.044; 开放接受稿 https://qmro.qmul.ac.uk/xmlui/bitstream/123456789/58238/2/Buchan%20A%20combined%20immersed%202019%20Accepted.pdf

- 解决：复杂几何强制贴体有限元网格过大。方法：非贴体整体网格+内部材料结构投影(supermeshing；保守体积映射和有效截面)+基于Hessian与误差度量的各向异性自适应重构；子网格尺度FEM与P1/SN角离散（测试P1,S6,S8）；不涉及GPU-MOC。
- 证据：三类算例包括16cm立方体内高吸收圆柱固定源、2群燃料棒特征值、SUPO复杂结构；比较IBA、IB、GCA、GC四类方法；图7明确拆出了投影、适应与求解时间；吸收圆柱采用初始384个四面体并多轮适应；燃料棒例明确体积不守恒的非贴体几何带来明显keff偏差，IBA给出较好的同网格尺寸精度；图12比较适应过程的时间与网格数。这是**对RP完整开销理念的重要近例**，不能声称自适应建模开销此前无人计量。
- 限制：文中明示更全面V&V留待未来；未提供固定GPU显存约束下在线/缓存/部分缓存的MOC联合最优化或屏蔽方案更新序列。
- 与RP：要明确材料界面体积/长度、薄层和流道响应误差；不能以“少单元”代替“精度可行”。

## 5. Zhou et al. 2025 [A]

Faguo Zhou et al., *Neutron particle transport 3D method of characteristic Multi GPU platform Parallel Computing*, arXiv:2503.17743v1, DOI:10.48550/arXiv.2503.17743; https://arxiv.org/pdf/2503.17743

- 解决：在OpenMOC基础上OTF轨迹生成的GPU移植、显式轨迹预存替代、按分段数负载平衡；GPU示例含GTX1080Ti/2080Ti/3060/4090和AMD MI60；其4.3使用512x512分组和交替反转排序；这不是RP应照搬的固定参数。
- 证据：C5G7-3D扩展多轨迹数量下与OpenMOC OTF结果k-eff与迭代次数一致（表2、§5.1），这是CPU/GPU移植数值一致性证据，不等于屏蔽固定源目标响应验证；Fig6、§5.2展示约30–100倍CPU/GPU比较；Fig7 EXPLICIT相对于OTF按图/文字约1.5–10倍部分规模收益与更高显存占用；Fig8分段数分组后扫描耗时改善约8–10%。摘要却称300–400倍，未与正文Fig6口径一致，不能采作确定加速承诺。
- 缺口：在全文所示测试范围未见块结构局部加密的表示二水平×GPU执行联合实验；未系统计方案更新、缓存重建及严格的独立几何留出。另需注意它与Li et al. SC23 ANT-MOC存在部分作者重合，技术关系待核查。
- RQ2最直接比较：不以轨迹分组/OTF本身为原创；着眼于局部加密造成的段数不均和界面成本如何使既有策略产生不同净效益。

## 6. 宋佩涛博士论文（2021）[B]

宋佩涛,《MOC全堆芯中子输运CPU/GPU异构并行算法研究》，哈尔滨工程大学，核科学与技术，博士学位年份2021；官方长摘要 https://cnki.istiz.org.cn/kcms/detail/detail.aspx?dbcode=CDFD&dbname=CDFD2024&filename=1023018169.nh

- 解决：异构MOC的GPU映射、性能解析、跨节点扩展与CPU/GPU协同。二维特征线×能群×极角三种并行策略；GPU性能分析包含浮点、访存、缓存；MPI空间域分解、异步通信覆盖；CPU/GPU性能预测与负载分配；三维采用MOC-EX轴向菱形差分及GPU-CMFD，软件ALPHA。不能将二维或MOC-EX计算笼统称完全直接3D-MOC。
- 论文摘要可核指标：二维核函数优化1.6x；单1080Ti相对i9-7900单核>100x；5节点并行效率87%→95%；CPU/GPU协同>11%增益；GPU三维MOC-EX约40x、CMFD约15x、整体约34x(6.5h→11min)；10异构节点强扩展约85%。这些是作者报告的受控数值，但未获全文核查基线细节、统计不确定度。
- 与RP：性能归因模型与异构协同并非新颖；RP需获得块网格—策略交互的解释模型和完整设计修改周期。并非一定需要多GPU或CPU/GPU协同，也不能以它为毕业门槛。

## 7. 汪岸博士论文（2025）[B]

汪岸,《三维中子输运特征线计算方法及大规模并行实现》，北京科技大学，计算机科学与技术，博士学位年份2025；官方长摘要 https://cnki.istiz.org.cn/kcms/detail/detail.aspx?dbcode=CDFD&dbname=CDFD2026&filename=1025098988.nh

- 解决：通用CSG几何形式化、阵列柱面厚边界相交与几何错误检测；直接三维MOC循环轨迹分解；轨迹长度分布规律、负载估计和组合优化分配；完整ANT-MOC程序；国际基准/敏感性/浮点验证与超算扩展。
- 证据：官方摘要披露可处理10^11量级轨迹，CEFR堆芯算例从4096核到98304核范围，弱扩展约95%、强扩展约53%；这些是论文内的实验，不等于屏蔽场景的GPU效果，也不可凭“核数”推定为GPU设备。
- 与RP：数学化负载预测和组合优化已存在；如果RP要称其方法贡献是“负载分析”，必须与针对空间加密改变的成本机制、显存和完整时间选择的新增假设精确对照。

## 额外必引先例（补原文献体系的漏洞）

1. Liu et al. 2022, *Multilevel mesh adaptivity for discrete ordinates transport calculation with spatial-moment-ratio indicators*, ANE 176, 109288, DOI:10.1016/j.anucene.2022.109288. 三维笛卡儿多层金字塔+自适应SN扫描和存储，异质算例作者报告60–80%成本节省。原“块结构网格+局部加密”不能当独创。
2. Li et al. 2023, *ANT-MOC: Scalable Neutral Particle Transport Using 3D Method of Characteristics on Multi-GPU Systems*, SC23 https://sc23.supercomputing.org/proceedings/tech_paper/tech_paper_pages/pap300.html . 轨迹管理、显存/计算/通信性能模型、多级负载映射；作者报告16000 GPU/千亿量级轨迹及并行效率。RQ2不能凭“性能模型”本身称新。

## 七项与RQ的可替代性表

| 核心工作 | RQ1完整达标周期+空间/执行联合择优 | RQ2块网格×GPU执行交互机制 | RQ3多层边界、更新族及实测范围准则 |
|---|---|---|---|
| Liu 2023 | 目标精度和节约时间与RQ1部分重合；非GPU-MOC | 未获证据支持 | 未获证据支持 |
| Song 2026 | GPU-MOC与显存优化已覆盖；未见块网格二侧公平联合优化 | 缓存/分组/显存单侧已覆盖 | 未见多场景完整周期与失效范围 |
| Dzianisau 2026 | GPU内存管理已覆盖；MOC/DD而非完全直接3D | 轴向分解异步已覆盖 | 未见更新族完整周期 |
| Buchan 2019 | 自适应+建网/求解时间已部分覆盖 | 非MOC GPU缓存机制 | 部分几何/网格适用性分析，但非GPU完整设计周期 |
| Zhou 2025 | OTF/EXP GPU执行优化已覆盖 | 分段负载排序与权衡已有；块网格交互未见 | 未见严谨边界与独立留出 |
| 宋佩涛2021 | CPU/GPU映射及效率已覆盖 | 性能模型和负载分配已有 | 未见该RP严格设定 |
| 汪岸2025 | 直接三维MOC实现已覆盖 | 循环轨迹分布和负载优化已有 | 未见该RP严格设定 |

**提醒**：本表的“未见”指已读取资料中尚未发现，而非可证明现有文献全无此研究。

## 三个RQ的最低可检验增量（不是现成创新结论）

- RQ1：除公平联合调参外，必须完成块级轨迹穿越、界面/材料映射、体素分段守恒及关键屏蔽响应达标的**可复用算法模块**；报告首次与源更新/重建更新全周期，不能只以局部比全域快视为原创。
- RQ2：提出并验证解释为何网格表示改变会**反转**部分缓存、分组或归约策略收益的分项成本机制；如无反转，就报告条件内稳定协同/无显著交互，仍需真实机制证据。已有的GPU性能指标不能重新命名为理论创新。
- RQ3：固定几何族留出和预登记分层点，给出条件化实测判向覆盖率、方向错误率、跨零不确定带和可行域截断；不以模型预测区间直接触发未测配置的选择。若模型不足只能报告受限范围，不能自称普适预测法。

## 需补充全文才能作出的判断

- Liu 2023的成本是否包括所有伴随、迭代重建与搜索开销、是否有未见的GPU方法；
- Song 2026与Dzianisau 2026是否已有时间变动/重用序列及软件细节被公开节选省略；
- 两篇博士论文是否存在与表示—执行耦合有关的未披露正文实验；
- Zhou 2025摘要300–400x与Fig6 30–100x是否因未说明的不同基线，尚无法消除矛盾。

**同行评审结论**：论文有潜力，但题目不能仅靠“组合两项既有技术”；应构成『可靠的块MOC表示算法 + 对应GPU执行成本机制 + 有效边界内可否证的选择规则』的统一方法学。否则有工程集成价值，却难认独立博士级计算方法创新。
