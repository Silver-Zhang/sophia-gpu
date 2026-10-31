# 创新性与导师契合度：基础文件独立审查

审查日期：2026-10-18。范围：00_scope、01_research_canon、02_evidence_table、03_argument_map、04_section_contracts；仅审查大纲证据、已有工作边界和导师契合度，不代替求解器技术审查。未联系作者或导师；作者身份均以作者列表核验。

结论：基础论证可进入大纲写作，需落实以下 8 项修改。其中第 1、3、4、5 项直接影响新颖性及导师匹配表述，不宜留到正文润色阶段。未发现必须改题的先验重复，但当前证据也不足以证明所拟组合为首次。

## 8 项可执行修正

1. **增加导师团队 2024 年工作的直接证据，避免将契合度压缩为 VITAS 2022。** Sun 等的 UVNM-SN 已研究非结构异质输运、体积修正及 NDA；同年 upwind-HDG 研究一阶 Boltzmann 方程、多尺度问题及上风扫描。建议在 canon 和导师匹配段建立“几何误差与体积修正—非结构确定论离散—迭代/扫描效率”三条方法连续性。它们支持方法论契合，不支持团队已经具备聚变体素 GPU MOC。来源：[Sun et al., CMwA 170 (2024) 142–160, DOI 10.1016/j.camwa.2024.06.032](https://www.sciencedirect.com/science/article/abs/pii/S0898122124003006)；[Sun et al., PRE 110 (2024) 065301](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.110.065301)。均有 Tengfei Zhang 实际署名。

2. **把 VITAS 的版本限制和团队并行证据写准确。** VITAS 2022 的各向同性/轴向挤出是该文版本描述，不可推断 2026 年平台仍全部受限。KNS 2023 原始会议文献已报告基于 VITAS 的各向异性 HVNM-SN 开发及板状问题验证。Yin 等 2024 是 CPU/MPI 的非均匀介质 HVNM 并行，不是 GPU“异构计算”；heterogeneous 指介质非均匀。可用它支持并行分解、负载与通信分析经验，不能直接迁移性能结论。来源：[VITAS 2022](https://www.sciencedirect.com/science/article/pii/S030645492200370X)；[Xiao and Zhang, KNS Autumn Meeting, 26–27 October 2023](https://www.kns.org/files/int_paper/paper/RPHA-2023_2023_5/RPHA-2023-WeiXiao.pdf)；[Yin et al., NST 35 (2024) 69](https://www.nst.sinap.ac.cn/article/doi/10.1007/s41365-024-01430-4?tab=2)。KNS 文件页眉为 KNS Autumn Meeting，应按页眉记录会议名，不根据网址目录猜会议名称。

3. **细分 NuDEAL 三条路线，禁止把它概括为已解决任意三维几何的 GPU MOC。** 2026 作者全文明确 MOC/HFEM 和 DGMOC 均限于轴向挤出几何，DFEM-SN 才解除该几何限制。拟题应与其分别对比几何表示、角/空间离散、显存需求和评价响应。可以保留真正三维长特征线、聚变固定源与斜向贯穿通道的特定定位；不能据此否认既有任意三维 MOC。来源：[NuDEAL 作者全文，§1、§2.1.2](https://arxiv.org/html/2607.01591v1)，其 [arXiv 元数据](https://arxiv.org/abs/2607.01591)链接 DOI 10.1080/00295639.2026.2652773。出版网页本次不能直接打开，引用时注明阅读对象为作者全文，勿自造卷期页码。

4. **把“响应驱动局部加密”从创新名称改成已有技术背景，并补一个直接先例。** Baker 等 2013 已对固定源屏蔽问题使用伴随和目标响应误差进行空间自适应；Wang 等 2022 已在 ARES 中以目标导向多碰撞源和动态角求积处理管道流束。因此，创新应落到“CAD→体素转换所造成的路径/连通性误差的响应相关判据，以及该判据与 GPU 代价的联合选择”，而不是泛称首次目标驱动加密。具体判据仍应写为待建立、待检验。来源：[Baker et al., ANE 55 (2013) 169–183](https://www.sciencedirect.com/science/article/abs/pii/S0306454912004744)，DOI 10.1016/j.anucene.2012.11.029；[Wang et al., Energies 15 (2022) 8335](https://www.mdpi.com/1996-1073/15/22/8335)。

5. **扩展综述的“不能算创新”清单，覆盖 on-the-fly、负载均衡和体素/权窗分辨率分离。** MOCkingbird 2021 已支持三维非结构 MOC，既可保存轨迹段，也可每次扫描实时追踪；2013 中国 GPU MOC 文献已含多 GPU；Zhou 等 2025 预印本讨论实时轨迹生成、预加载和负载平衡。单独采用这些构件没有新颖性。建议用消融实验检验所选组合为何适合聚变几何，不承诺“300–400 倍”等跨硬件、跨基线性能。来源：[Gaston et al. 2021](https://www.tandfonline.com/doi/pdf/10.1080/00295450.2021.1871995)；[ZhiZhu Zhang, Kan Wang, Qing Li, 2013](https://www.sciencedirect.com/science/article/abs/pii/S0306454913003423)；[Zhou et al., arXiv:2503.17743](https://arxiv.org/abs/2503.17743)。2013 年 Zhang 为 ZhiZhu Zhang，不是导师 Tengfei Zhang。

6. **把 fusion FW-CADIS 的适应网格先例具体化。** ORNL 既有 ITER 工作已经包括 macromaterial、确定论网格细化和权窗网格/能群粗化，后者将权窗存储与确定论分辨率解耦。计划不能把“聚变 + FW-CADIS + 自适应 + 降低显存”本身视为贡献。建议将延伸问题改为：体素 GPU MOC 在何种几何与重要性精度下，连同前处理和权窗生成，降低达到指定统计精度的总成本。来源：[ORNL, Automatic Mesh Adaptivity for Hybrid Monte Carlo/Deterministic Neutronics Modeling of Difficult Shielding Problems](https://www.ornl.gov/content/automatic-mesh-adaptivity-hybrid-monte-carlodeterministic-neutronics-modeling-difficult)。

7. **把 random-ray FW-CADIS 设为实质竞争方案，但不夸大现有论文结论。** Raffuzzi、Neame、Cosgrove 文章已研究 random-ray 生成权窗；仅两类屏蔽问题的结果不能外推所有聚变几何或宣称普遍优于 MAGIC。参考文献可按正式卷期写 2026, 200(sup1): S485–S502，并备注 2025-03-03 在线；不要重复列成两篇。OpenMC 官方文档应支持可运行比较路线，论文支持方法先例，两者不混用为同一版本验证。来源：[剑桥作者接受稿及摘要](https://www.repository.cam.ac.uk/items/b2f47a30-76cc-4ab1-ba68-d1d9f039e6da)；[期刊正式记录](https://www.tandfonline.com/doi/full/10.1080/00295639.2025.2458958)；[OpenMC 方法文档](https://docs.openmc.org/en/stable/methods/variance_reduction.html)。

8. **将“文献比较对象”与“必须复现实验对象”拆开。** MOCkingbird、NuDEAL、VITAS 的代码和许可本次未核实，不能要求它们全部成为博士前两年的可运行基线。最小可行比较包括同一实现的均匀/局部细化体素、CPU/GPU、精确几何 MC/体素 MC；外部确定论程序获得许可与模型一致性后再加入。最终只能对可复现、同精度、同资源实验宣称性能优势。导师官方主页支持先进输运数值算法方向，不能据主页推定代码授权、聚变项目、硬件配额或导师认可。来源：[SJTU 官方主页](https://me.sjtu.edu.cn/teacher_directory1/zhangtengfei)。

## 保守创新表述（建议供大纲采用）

本研究拟面向聚变固定源输运中薄层、曲面界面和斜向空腔通道并存的几何，研究体素化引起的几何与输运路径扰动如何传递至指定工程响应，并建立在给定响应误差与显存约束下选择局部几何分辨率和 GPU 特征线执行策略的方法。潜在贡献在于给出该表示—求解组合的适用条件、成本收益和失效边界，而非把体素、MOC、GPU、自适应或 FW-CADIS 本身作为新方法。若核心方法得到验证，再检验其作为正向/伴随重要性求解器的总成本优势，并与现有 random-ray FW-CADIS 和 MC 权窗迭代比较。

## 分数与状态

| 维度 | 分数/10 | 判据 |
|---|---:|---|
| 研究问题清晰度 | 8.5 | 主问题与 3 个子问题明确，应用响应尚需在大纲锁定 |
| 科学张力 | 8.5 | 几何保真、GPU 规则性和总成本冲突明确 |
| 证据匹配 | 7.5 | 主张克制；需补 2024 导师论文与目标导向自适应先例 |
| 逻辑链 | 8.5 | 核心两项与条件延伸有明确关系 |
| 方法可行性（仅证据层） | 7.5 | 资源和外部代码不预设；待明确最小基线 |
| 创新性 | 7.5 | 方向具体，但不能让“响应驱动加密”承担单独新颖性 |
| 风险边界 | 8.5 | 承认体素化失效与延伸工作可不启动 |
| 语言质量 | 8.5 | foundation 简明，最终中文大纲另审 |

**foundation_score = 8.1/10，建议：修正后进入导师可阅的大纲写作。** 这是证据和论证基础的评分，不是已证明课题新颖性或可取得预期性能的结论。

额外元数据风险：ANL 的 2019 parallel VNM 网页虽列正确题名、作者和 DOI 10.1016/j.pnucene.2019.03.007，但其摘要错配为水泥水化研究；不得使用该摘要作为输运内容依据。应采用出版商记录，并保留错误发现日志。
