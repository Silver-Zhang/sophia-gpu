# 基准67条参考文献元数据核验

核查日期：2026-11-08。52条取得Crossref身份元数据，8条基准无DOI，7条Crossref未注册或未能匹配。原始响应字段及DOI请求地址保存在JSON/CSV。

方法：使用系统curl验证TLS访问Crossref公开元数据；Python urllib最初因本机CA配置失败，切换系统信任库后重跑。未关闭证书验证。

Crossref成功返回的52条题名经逐项人工浏览与原条目相符；完整作者数组、卷期页码、online/print日期均保留，未据DOI字符串推断出版年。部分期刊旧文的online日期是数字化再上线年份。没有原文全文的条目不能据本表认定数值结果已核查。

|条目|DOI|核验结果|Crossref题名|
|---|---|---|---|
|ref1|10.1080/15361055.2024.2323747|身份元数据已获取|OpenMC Interpretation of FNS SINBAD Shielding Benchmark Experiments|
|ref2|10.1016/j.fusengdes.2019.111243|身份元数据已获取|Analysis of nuclear response in CFETR toroidal field coils with density reduction VR technique|
|ref3|10.3389/fnuen.2024.1384788|身份元数据已获取|ParaStell: parametric modeling and neutronics support for stellarator fusion power plants|
|ref4|10.13182/NSE98-2|身份元数据已获取|Automated Variance Reduction of Monte Carlo Shielding Calculations Using the Discrete Ordinates Adjoint Function|
|ref5|10.13182/NSE12-33|身份元数据已获取|FW-CADIS Method for Global and Regional Variance Reduction of Monte Carlo Radiation Transport Calculations|
|ref6|10.1016/j.fusengdes.2007.06.038|身份元数据已获取|Automatic generation and validation of an ITER neutronics model from CAD data|
|ref7|10.1088/1674-1137/38/5/058201|身份元数据已获取|Preliminary study on CAD-based method of characteristics for neutron transport calculation|
|ref8|10.1016/j.nucengdes.2024.112994|身份元数据已获取|Research on approaches to automatic modeling of discrete ordinate programs based on CAD model|
|ref9|10.1016/j.anucene.2019.05.044|身份元数据已获取|A combined immersed body and adaptive mesh method for simulating neutron transport within complex structures|
|ref10|10.1080/00295639.2020.1780842|身份元数据已获取|Nonmatching Discontinuous Cartesian Grid Algorithm Based on the Multilevel Octree Architecture for Discrete Ordinates Transport Calculation|
|ref11|10.1177/10943420211022811|身份元数据已获取|AMReX: Block-structured adaptive mesh refinement for multiphysics applications|
|ref12|10.3724/SP.J.1089.2024-00765|身份元数据已获取|A Survey of GPU-Based Parallel Adaptive Cartesian Grid Modeling Methods and Simulation Applications|
|ref13|10.1016/j.anucene.2013.12.012|身份元数据已获取|The OpenMOC method of characteristics neutral particle transport code|
|ref14|10.1080/00295450.2021.1871995|身份元数据已获取|Method of Characteristics for 3D, Full-Core Neutron Transport on Unstructured Mesh|
|ref15|10.1016/j.anucene.2020.108033|身份元数据已获取|Solution-dependent predictor-corrector flux mapping algorithm for discrete ordinates calculation on multilevel discontinuous grids|
|ref16|10.1016/j.jcp.2010.10.018|身份元数据已获取|Standard and goal-oriented adaptive mesh refinement applied to radiation transport on 2D unstructured triangular meshes|
|ref17|10.1016/j.anucene.2011.01.038|身份元数据已获取|Goal-oriented spatial adaptivity for the SN equations on unstructured triangular meshes|
|ref18|10.1016/j.anucene.2012.11.029|身份元数据已获取|Goal based mesh adaptivity for fixed source radiation transport calculations|
|ref19|10.1016/j.jcp.2012.12.035|身份元数据已获取|Minimising the error in eigenvalue calculations involving the Boltzmann transport equation using goal-based adaptivity on unstructured meshes|
|ref20|10.1016/j.anucene.2022.109288|身份元数据已获取|Multilevel mesh adaptivity for discrete ordinates transport calculation with spatial-moment-ratio indicators|
|ref21|10.1080/00295639.2023.2169537|身份元数据已获取|Goal-Oriented Mesh Adaptivity of Three-Dimensional Neutron Transport Calculation Using Weighted Difference Scheme and Dual-Weighted Residual Error Indicators|
|ref22|10.1016/j.net.2022.10.017|身份元数据已获取|Verification of multilevel octree grid algorithm of S  transport calculation with the Balakovo-3 VVER-1000 neutron dosimetry benchmark|
|ref23|10.1016/j.cma.2026.118872|身份元数据已获取|Adaptive mesh h(p)-refinement of a discontinuous Bubnov-Galerkin isogeometric analysis spatial discretisation of the first-order form of the neutron transport equation with goal-based error measures and diffusion acceleration|
|ref24|10.1016/j.pnucene.2025.106109|身份元数据已获取|GPU-accelerated few-group 3D Method of Characteristics for full-core neutron transport in Small Modular Reactors|
|ref25|10.48550/arXiv.2503.17743|Crossref返回404，需对应注册机构/官网核验||
|ref26|—|基准未列DOI||
|ref27|—|基准未列DOI||
|ref28|10.7538/yzk.2019.youxian.0416|Crossref返回404，需对应注册机构/官网核验||
|ref29|10.1145/3581784.3607063|身份元数据已获取|ANT-MOC: Scalable Neutral Particle Transport Using 3D Method of Characteristics on Multi-GPU Systems|
|ref30|10.1016/j.cpc.2025.109952|身份元数据已获取|Axially decomposed GPU-enabled three-dimensional method of characteristics/diamond difference solver in neutron transport code STREAM3D-GPU|
|ref31|10.1080/00295639.2026.2652773|身份元数据已获取|Verification and Performance Assessment of NuDEAL, a GPU-Accelerated Deterministic Transport Framework on Unstructured Meshes|
|ref32|—|基准未列DOI||
|ref33|10.1016/j.nucengdes.2024.113148|身份元数据已获取|A cyclic-track decomposition method for 3D MOC neutron transport simulation|
|ref34|—|基准未列DOI||
|ref35|—|基准未列DOI||
|ref36|10.1016/j.net.2025.103597|身份元数据已获取|GPU-based multi-group discrete ordinates transport calculations: Parallel computing implementation in STRAUM|
|ref37|10.1016/j.jcp.2011.04.010|身份元数据已获取|GPU accelerated simulations of 3D deterministic particle transport using discrete ordinates method|
|ref38|10.1016/j.anucene.2022.109171|身份元数据已获取|Development and verification of a GPU-based MOC transient solver|
|ref39|10.1080/15361055.2018.1504508|身份元数据已获取|Application of the Denovo Discrete Ordinates Radiation Transport Code to Large-Scale Fusion Neutronics|
|ref40|10.1016/j.cpc.2025.110001|身份元数据已获取|OpenSn: A massively parallel, open-source simulation environment for discrete ordinates radiation transport|
|ref41|10.48550/arXiv.2609.14496|Crossref返回404，需对应注册机构/官网核验||
|ref42|10.1051/epjn/2024034|身份元数据已获取|Status of GPU capabilities within the Shift Monte Carlo radiation transport code|
|ref43|—|基准未列DOI||
|ref44|10.1080/00295639.2019.1586273|身份元数据已获取|Review of Hybrid Methods for Deep-Penetration Neutron Transport|
|ref45|10.48550/arXiv.1612.00793|Crossref返回404，需对应注册机构/官网核验||
|ref46|10.1016/j.anucene.2025.111385|身份元数据已获取|Local angular adaptivity CADIS hybrid variance reduction method for monte carlo radiation transport calculations|
|ref47|10.1016/j.fusengdes.2014.03.014|身份元数据已获取|Novel hybrid Monte Carlo/deterministic technique for shutdown dose rate analyses of fusion energy systems|
|ref48|10.1016/j.fusengdes.2011.01.059|身份元数据已获取|Comparison of global variance reduction techniques for Monte Carlo radiation transport simulations of ITER|
|ref49|—|基准未列DOI||
|ref50|10.1080/00295639.2025.2458958|身份元数据已获取|Application of the Random Ray Method to Variance Reduction in Radiation Shielding Problems|
|ref51|10.1016/j.fusengdes.2014.02.046|身份元数据已获取|Assessment of fusion facility dose rate map using mesh adaptivity enhancements of hybrid Monte Carlo/deterministic techniques|
|ref52|10.11889/j.0253-3219.2016.hjs.39.090502|Crossref返回404，需对应注册机构/官网核验||
|ref53|10.1016/j.anucene.2020.107978|身份元数据已获取|NECP-MCX: A hybrid Monte-Carlo-Deterministic particle-transport code for the simulation of deep-penetration problems|
|ref54|10.1016/j.anucene.2020.108039|身份元数据已获取|High-efficiency simulation of VENUS-3 neutron-shielding problem with an automatic and enhanced hybrid Monte-Carlo-Deterministic method|
|ref55|10.1016/j.fusengdes.2024.114372|身份元数据已获取|Development of multilevel mesh adaptivity for global variance reduction in Monte Carlo code cosRMC|
|ref56|10.1016/j.cpc.2026.110288|身份元数据已获取|Developing the THETA transport code with the linear source enhanced random ray method for high-fidelity radiation shielding simulation|
|ref57|10.48550/arXiv.1309.6166|Crossref返回404，需对应注册机构/官网核验||
|ref58|10.1080/00295639.2025.2484511|身份元数据已获取|Automated Hybrid Variance Reduction on Advanced Architectures in the Shift Monte Carlo Code|
|ref59|—|基准未列DOI||
|ref60|10.11889/j.0253-3219.2024.hjs.47.050008|Crossref返回404，需对应注册机构/官网核验||
|ref61|10.3389/fenrg.2023.1085264|身份元数据已获取|Benchmark shielding calculations for fusion and accelerator-driven sub-critical systems|
|ref62|10.13182/NT175-251|身份元数据已获取|ITER Neutronics Modeling Using Hybrid Monte Carlo/Deterministic and CAD-Based Monte Carlo Methods|
|ref63|10.13182/FST91-A29687|身份元数据已获取|Shielding Design Optimization for the Compact Ignition Tokamak Test Cell Building|
|ref64|10.1016/j.net.2017.08.008|身份元数据已获取|Particle tracking acceleration via signed distance fields in direct-accelerated geometry Monte Carlo|
|ref65|10.1109/MCSE.2022.3154656|身份元数据已获取|Hardware-Accelerated Ray Tracing of CAD-Based Geometry for Monte Carlo Radiation Transport|
|ref66|10.1016/j.pnucene.2020.103590|身份元数据已获取|Improved memory management for solving neutron transport via a novel Modular Ray Tracing (MRT) approach embedded in parallel method of characteristic (MOC) framework|
|ref67|10.2172/1210162|身份元数据已获取|ADVANTG—An Automated Variance Reduction Parameter Generator (Rev. 1)|

## 卷年与在线发表

- ref1：online 2024-03-25，print 2025-01-02；V4.2卷81(1)与2025一致。
- ref12：online 2025-07-14，print 2026-02-01；V4.2卷38(2)与2026一致。
- ref24、30：DOI含2025，但Crossref print均为2026-02；不应按DOI年份改成2025。
- ref50：online 2025-03-03，print 2026-02-26，卷200(sup1)；Crossref无页码，基准S485–S502需以出版社核对。
- ref58：online 2025-05-28，print 2026-02，卷200(2):444–470；可据此补充正式卷期页码。
- ref31：online 2026-04-23，尚无卷期，页码1–25。

Crossref404条目：ref25/41/45/57为arXiv DOI，应向DataCite/arXiv查验；ref28/52/60为中文期刊DOI，应向出版社或相应DOI注册机构查验。

## DataCite补查

4条arXiv DOI（ref25/41/45/57）均从DataCite取得元数据，题名、作者与年份与基准一致，原始字段保存在`metadata_datacite.json`。因此当前共56条取得DOI注册机构身份元数据；尚有8条原稿未列DOI及3条中文期刊DOI待对应来源核验。ref25与ref41元数据列CC BY 4.0；ref45与ref57为arXiv非排他传播许可，不等价于图表可公开转载许可。

## V5新增两条身份补查

ref68的DataCite元数据确认Amanatides/Woo、1987年、完整题名与DOI；ref69的Crossref元数据确认Laine/Karras、2010年、完整题名及55–63页。新增条目原始字段分别见`metadata_datacite.json`与`metadata_new_geometry.json`。原67项56条身份获取，连同新增2项共58条；此数量不代表全文/数值核查数量。
