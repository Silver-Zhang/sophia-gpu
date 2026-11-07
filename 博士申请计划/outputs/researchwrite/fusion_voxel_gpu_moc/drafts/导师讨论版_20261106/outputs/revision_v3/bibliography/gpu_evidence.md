# GPU输运文献独立证据核查（V2阶段二）

日期：2026-11-06。本轮只写证据与获取记录，不修改正文、旧文档或Git。遵守父目录及V2的AGENTS约束；表2删除的平台列和Zhou行不恢复。硬件和计时条件应并入正文或结果单元格。结构化事实见同目录 `gpu_evidence.json`（顶层 `records`，13项）。

## 应直接采用的结论

1. **加速比必须绑定求解对象、CPU并行度、GPU数量、精度和计时范围。** OpenMOC的近50倍是单GPU相对单Xeon核；Song2026的1015.8倍是组件算例相对单线程CPU；STREAM2026的22.1/40.5倍是MOC/DD求解器相对128核参考；NuDEAL的对照还更换了网格、角度和代码。它们不能组成统一性能排名。
2. **OpenMOC Fig.11为四种GPU分别测试，不是四卡联合。** 已实际查看作者稿p.11图例：GTX480、Quadro4000、TeslaC2070、TeslaK20c。最高曲线来自GTX480。其§3.4.3明确线程负责轨迹—能群，CPU生成轨迹后转CUDA数组，GPU连续扫掠线段；不能把另一篇12核强扩展实验当图11基线。[原文](https://doi.org/10.1016/j.anucene.2013.12.012)
3. **r20原DOI0416正确，不能改成0094。** r20为2019年53(11):2209–2217，出版社全文已取到；0094是2020年54(1):103–111的另一篇性能分析。前者每节点2块K80，即4个GK210逻辑GPU，后者为GTX1080Ti/i9-7900X。两篇设备不可互填。[r20](https://yznkxjs.xml-journal.net/article/doi/10.7538/yzk.2019.youxian.0416)、[2020另一篇](https://yznkxjs.xml-journal.net/article/doi/10.7538/yzk.2019.youxian.0094)
4. **STREAM先行稿设备不能无条件绑定2026期刊倍率。** 2024 KNS全文是8×RTXA5000/2×EPYC7543、64CPU核、OPR八分之一堆芯；2026期刊摘要是128核/四分之一堆芯。2025 KNS又加入GPU-CMFD。正式期刊型号表本轮未取得，JSON中分开记录三个版本。[期刊](https://doi.org/10.1016/j.cpc.2025.109952)、[2024原稿](https://www.kns.org/files/pre_paper/51/24S-051-Siarhei.pdf)、[2025改版](https://www.kns.org/files/pre_paper/53/25S-240-Siarhei.pdf)

## 原有文献的方法与可引用结果

| key | 方法贡献与机制 | 结果及必要条件 | 证据层级/采用范围 |
|---|---|---|---|
| r6 | 轨迹—能群映射，线段顺序依赖保留，CUDA数组与分层存储 | 单GTX480接近50倍/单Xeon核；型号各自一条曲线 | 作者接受稿方法及Fig.11已核；不补未知CPU型号或计时边界 |
| r19 | 轨迹/轨迹—群/轨迹—群—极角三粒度比较，访存与指令模型，异步拷贝，红黑SOR-CMFD | 学位摘要报告1080Ti、单核i9-7900基线和1.6倍优化；全篇未取得 | 只能称摘要证据；三维基准中英文名称冲突，不采用对应6.5h→11min说法 |
| r20 | 空间MPI+CUDA流，将分块拷贝与扫掠重叠；模型拆分MPI、拷贝、负载和迭代代价 | 5节点20逻辑GPU，强效率87%→95%；4异构节点优于20CPU节点 | 出版社全文§2.3—2.4/Fig.3/Table1/§3.2—3.3；原表CPU型号E5-1690v4疑似笔误，原样保留待核 |
| r21 | 对内存、计算、通信建立性能模型；节点/GPU/CU多层负载映射 | 官方摘要1000亿轨迹、16000GPU，强/弱效率70.69%/89.38% | SC23原始摘要可核；ACM全文403，型号、扩展起点、精确线程和归约实现尚无可核证据 |
| r24 | 长轨迹预存，其余OTF；按线段数重排，线程grid-stride遍历轨迹 | 文中缓存80%阈值、交替反序分组为具体实现参数 | arXiv v1方法全文；仅可用于轨迹机制，严格不恢复表2行或速度排名 |
| r25 | 线源降低线段需求、OTF-ART省三维线段、批处理省轨迹/边界状态、GPU-CMFD省迭代 | 单GPU/少群：组件最高1015.8倍、两个SMR274.1/378.9倍相对单线程CPU；显存降98.5% | 正式摘要/引言/结论片段；GPU/CPU型号、精度和倍率计时边界未可核，不猜型号 |
| r26 | 按轴向层调度必要状态与异步搬运，缓解完整角通量上卡压力 | 期刊MOC/DD：8/16卡相对128核为22.1/40.5倍，显存<4.5GB/进程 | 正式摘要与先行全文分层；不可写成整体执行时间同倍加速 |
| r27 | MOC四能群128bit对齐；DGMOC角块顺序；SN自由度线程、依赖槽回收 | TableII：RTX4070Ti SN总26s对Griffin96核53s；TableV：RTX2080Ti DGMOC总412s对480核566s | 作者稿全文方法与TablesII—VI已核；跨代码、异离散，不能当纯硬件竞速；BlueGene/P是作者推测 |

NuDEAL最值得进入正文的贡献不是“单GPU等于多少CPU核”，而是储存与并行度的取舍。DGMOC的角块由32降至2时，缓存7133→2589MB，单扫5.09→5.25s，变化约3%；全64角并行超出显存。DFEM-SN则按下游依赖的存活期回收角通量槽位，并将局部求解细分到自由度线程。这些是可迁移的设计依据，不能把MOC/HFEM、DGMOC和DFEM-SN统一写成GPU-MOC。[NuDEAL](https://doi.org/10.1080/00295639.2026.2652773)

## 建议新增的原始文献

**优先新增3项：new_straum2025、new_denovo_fusion2018、new_zou2022；new_gong2011作为第4项可选历史原始证据。** 元数据均在JSON中，不需要由正文作者补猜。

- **new_straum2025**，Zhang等，Nuclear Engineering and Technology 57(9):103597，DOI [10.1016/j.net.2025.103597](https://doi.org/10.1016/j.net.2025.103597)。作者公开的正式全文可读。非结构四面体SN/群块BiCGSTAB解决外源Kobayashi-like及RPV。GPU为3080Ti/4090，CPU为Ryzen7900X；GPU FP32与CPU FP64且迭代器不同。RPV177575单元优化结果为734/379s；双GPU相同群块条件效率95.4%/93.6%，不是把不同群块最佳结果直接相除。一个块处理群—方向组合，块内按波前同步单元，通量矩输出按地址独占避免写冲突；分群块子群可降低设备间通信。该文应支撑“固定源SN的并行与收敛权衡”，不归入MOC速度排名。[作者公开全文](https://www.researchgate.net/publication/390357834_GPU-based_multi-group_discrete_ordinates_transport_calculations_Parallel_computing_implementation_in_STRAUM)
- **new_denovo_fusion2018**，Royston等，Fusion Science and Technology 74(4):303–314，DOI [10.1080/15361055.2018.1504508](https://doi.org/10.1080/15361055.2018.1504508)。EUROfusion作者稿全文已取。JET固定源SN在Titan每节点K20x+AMD16核；为GPU暴露能量并行而采用跨空间—角度—能量GMRES，即使无上散射GS可一轮收敛。TableIV的100m级别（88,080,384单元）/32群/P3/256角每卦限在2048节点耗时4.6h，是条件明确且文内相容的例子。1b行与结论在角数/P阶存在冲突，勿拼接成精确工况；可选只引用前一工况。本文用实验、MCNP/Shift作响应比较，没有GPU相对CPU的同题速度实验。[作者稿](https://scipub.euro-fusion.org/wp-content/uploads/eurofusion/WPJET3PR1619576_accepted_merged.pdf)
- **new_zou2022**，Zou等，Annals of Nuclear Energy 174:109171，DOI [10.1016/j.anucene.2022.109171](https://doi.org/10.1016/j.anucene.2022.109171)。ALPHA二维MOC瞬态固定源TFSP、隐式时间离散和pin-CMFD；RTX2080Ti明确见正式片段。C5G7-TD验证为GPU-MOC固定源实现的直接先例，但TFSP不等于深屏蔽外源响应，也不是伴随验证。全文未得，本轮不补CPU型号、GPU卡数或速度数。
- **new_gong2011（可选）**，Gong等，Journal of Computational Physics 230(15):6010–6022，DOI [10.1016/j.jcp.2011.04.010](https://doi.org/10.1016/j.jcp.2011.04.010)。单群Sweep3D/SN：1×M2050在不含fixup时整体2.56倍于X5670 chip、8.14倍于Q6600 chip，含fixup时仅1.23倍于X5670。摘要写chip，不能换写单核。用于说明负通量修正与计时范围的重要性；不拿本实验替代多群复杂几何证据。

## 固定源与伴随的证据边界

本轮新增STRAUM和JET Denovo给出真实GPU正向固定源；Zou给出瞬态TFSP。原有GPU-MOC堆芯工作主要验证本征值与功率。GPU伴随性能尚未获得同等强度的原始定量证据，不能把“代码支持forward/adjoint”和“代码有GPU模块”拼成已验证GPU伴随加速。

尤其需要防止将Shift的GPU MC与GPU伴随求解混同。已有[Shift GPU能力原文](https://artefacts-discovery.researcher.life/full_text/DA-2/ed/ed955976c3eb3242bdf3b4a90203eb09/full_text/a88159f48ac900c09eb29e9d6fac3ea8.pdf) §7明确：Denovo确定论步骤、权窗和源偏倚在CPU，MC及权窗处理在GPU。该事实只用于方法边界，不应向正文堆砌无证据的否定句。候选路线可将正向—伴随离散一致性、互易/响应恒等式、权窗生成后的MC响应效率列为研究验证任务。

## 尚待取得的关键证据

- r25正式全文的GPU/CPU型号、精度与逐表计时；现有公开摘要不足以填写型号。
- r26正式全文硬件表及核函数/归约映射；2024/2025先行稿的设备与结果必须独立标记。
- r21正式全文的GPU型号、缩放基线与详细轨迹管理；不从关联预印本或后续应用借值。
- r19学位全文；r20原表CPU型号疑似排字问题；Denovo作者稿1b工况内部冲突。

这些限制保存在证据文件，正文使用已经核实的实质贡献与限定结果。此次不宣称所有条目均已取得全文。

## 补充核验：公开STREAM先行稿独立引用

`new_stream_kns2024` 已独立建立完整元数据（无DOI）：Dzianisau与Lee，GPU Acceleration of 3D MOC Solver in STREAM3D Using OpenACC，KNS Spring Meeting，Jeju，2024-05-09—10。硬件为8×RTX A5000 24GB、2×EPYC7543共64核。C5G7的MOC/总时间分别1368→34s、1704→100s；OPR八分之一堆芯分别61535→3995s、212416→11201s。该先行稿可作为第4项新增、替代可选Gong，独立支撑可核硬件和模块/总时间的区别，不能代替2026正式论文条件。[原始会议全文](https://www.kns.org/files/pre_paper/51/24S-051-Siarhei.pdf)

Denovo角度再次核实：作者稿PDF第12页TableII明确angles/octant，同页100m工况正文及下一页Fig.3题注均写256 angles per octant；TableIII的100m级别实际为88,080,384单元。故256确指每卦限方向数，不能写成总方向数。TableIV位于PDF第16页（刊内第15页）。
