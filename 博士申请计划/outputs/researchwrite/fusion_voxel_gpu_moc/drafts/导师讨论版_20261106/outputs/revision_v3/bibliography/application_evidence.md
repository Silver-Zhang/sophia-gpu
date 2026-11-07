# 工程与基准证据核查

元数据沿用原库并与出版社/官方页面核对；下面按实际阅读层级使用结果。

## r1 ParaStell: parametric modeling and neutronics support for stellarator fusion power plants

ParaStell参数化CAD、DAGMC几何和四面体聚变源，OpenMC中子—光子输运

99组设计，单周期旋转边界；总聚变功率2113 MW，每组3×10^5粒子、30批次

测试设计中的厚型/60%增殖层比例点TBR=1.10，磁体总核热152.0 kW；非局部峰值

启发：用同一组设计同时观察产氚与磁体核热，并对几何更新管理计算数据

证据层级：publisher_fulltext_methods_results；位置：§2.2、§3.2、§4；Fig12。

来源：https://www.frontiersin.org/journals/nuclear-engineering/articles/10.3389/fnuen.2024.1384788/full

## r2 Shielding Design Optimization for the Compact Ignition Tokamak Test Cell Building

以三维MC—二维S_N耦合结果校准一维S_N，再迭代材料与厚度

低钠混凝土、硼含量和厚度选择，同时满足屏蔽和结构约束

相对基准方案造价降低约14%（410万美元）；结果为工程造价

启发：分层模型可以支撑多次设计评价，最终比较采用工程约束满足情况

证据层级：publisher_abstract；位置：Abstract。

来源：https://www.tandfonline.com/doi/abs/10.13182/FST91-A29687

## r3 Automatic generation and validation of an ITER neutronics model from CAD data

McCad将CAD实体转换为MCNP几何，随机体积计算与CAD体积对照

40°扇区及主要部件的几何分区核对

通过体积对照核验转换几何；本轮未取得新的数值误差表

启发：把材料分区核验安排在输运求解之前

证据层级：metadata_and_preexisting_publisher_abstract；位置：已有出版社摘要及Crossref著录；40°模型资料交叉核对。

来源：https://doi.org/10.1016/j.fusengdes.2007.06.038

## r4 OpenMC Interpretation of FNS SINBAD Shielding Benchmark Experiments

OpenMC0.14.1-dev连续能固定源中子/光子输运；钨例使用Denovo/MAVRIC权窗，钒和铍例未用重要性图；IRDFF反应率及ENDF/B-VII.1输运截面

14 MeV D-T源；与测量和MCNP6.2分别比较；作者稿25页含封面

9个TPR测点C/E均值1.0295、标准差0.1956；7个GHR测点均值0.9537、标准差0.1366。±是各测点C/E离散标准差，非蒙卡单次计分误差

启发：按不同响应分别比较C/E、实验不确定度与蒙卡RSD；匹配探测器能量分辨和反应截面

证据层级：author_manuscript_methods_and_results_plus_publisher_HTML；位置：作者稿pp6—7 §III.A、p21 Tables VIII/IX、p22 §IV。

来源：https://library.psfc.mit.edu/catalog/reports/2020/24ja/24ja039/24ja039_full.pdf

## r5 基于SINBAD聚变基准题的cosRMC程序屏蔽计算研究

cosRMC中子—光子耦合；栅元重要性减方差

各穿透深度探测器中子通量谱，与MCNP5及实验比较

cosRMC—MCNP5相对差异处于文中3倍统计相对误差带内；实验谱另行比较

启发：用孔道与体屏蔽配对，分开检验流束与材料衰减

证据层级：official_publisher_abstract_and_PDF_selected_figures；位置：摘要及Figs7—8（050008-6）。

来源：https://www.hjs.sinap.ac.cn/rc-pub/front/front-article/download/56713564/lowqualitypdf/基于SINBAD聚变基准题的cosRMC程序屏蔽计算研究.pdf

## r35 ITER Neutronics Modeling Using Hybrid Monte Carlo/Deterministic and CAD-Based Monte Carlo Methods

CADIS/FW-CADIS配合CAD蒙卡

DAG-MCNP/ADVANTG/Denovo等混合流程

剂量算例MC FOM较模拟直接输运提高约2.1×10^4；全局通量采用FW-CADIS

启发：局部磁体响应与设施外小剂量需要不同响应配置

证据层级：publisher_and_ORNL_abstract；位置：期刊摘要；正式2011,175(1):251—258。2010会议稿不混作完整期刊全文。

来源：https://impact.ornl.gov/en/publications/iter-neutronics-modeling-using-hybrid-monte-carlo-deterministic-a/

## r45 SINBAD — Shielding Integral Benchmark Archive and Database

屏蔽实验基准评估、版本控制与授权分发

SINBAD.v2；NEA-1939包括Volumes1/2；2025-07-02官方发布说明

新发布版包括105项基准；2026技术评审组与持续维护页面已更新

启发：使用具体条目版本、实验定义和不确定度，而非只引用数据库名称

证据层级：official_database_release_and_access_pages；位置：Overview、access；2025新版发布说明。

来源：https://cms.oecd-nea.org/jcms/pl_32139/sinbad-shielding-integral-benchmark-archive-and-database

## r46 Analysis of nuclear response in CFETR toroidal field coils with density reduction VR technique

McCad构建MCNP几何；MAGIC结合逐步密度降低生成权窗，最终恢复实际密度

大/小半径7.2/2.2 m，聚变功率200 MW—1.5 GW

初始偏滤器屏蔽不足，经优化后所评线圈核响应满足所引用ITER设计限值；未公开读到具体峰值表

启发：在最终物理密度上评价线圈响应，用权窗生成过程加速远端统计

证据层级：publisher_abstract_and_introduction；位置：Abstract、Introduction。

来源：https://www.sciencedirect.com/science/article/abs/pii/S0920379619307215

## new_phits2023 Benchmark shielding calculations for fusion and accelerator-driven sub-critical systems

PHITS3.24，JENDL4.0；对FNS和OKTAVIAN给新计算，其余加速器案例综述

铁体直径1 m、厚0.95 m；0.003—10 MeV积分中子产额

Table2六位置C/E为1.39、1.31、1.24、1.21、1.15、1.78；表中误差仅计数统计

启发：把能谱积分和分能区偏差同时保留，区分统计误差与模型/核数据差异

证据层级：publisher_fulltext_selected_methods_results；位置：§2.2.1、§3.1 Table2。

来源：https://www.frontiersin.org/journals/energy-research/articles/10.3389/fenrg.2023.1085264/full

## r29 CUDA C++ Best Practices Guide

官方CUDA内存访问、线程组织和性能分析指南

当前在线指南标示13.5

仅用于实现机制定义，不作为输运性能实验

启发：按真实访问模式与内核计时解释GPU结果

证据层级：official_current_manual；位置：13.5文档首页及优化章节。

来源：https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html
