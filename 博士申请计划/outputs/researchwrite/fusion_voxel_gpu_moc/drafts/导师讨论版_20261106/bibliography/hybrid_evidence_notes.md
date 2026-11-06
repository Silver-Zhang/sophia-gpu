# 混合减方差文献独立核验札记

核验日期：2026-11-06。核验范围为候选文献30—43及CADIS-Ω原始工作。仅记录本次实际访问层级；官方摘要、作者稿和正式全文分别标记。所有结论均为文献范围内贡献；不推断软件当前可获取性。原00—04未修改。

## 必须修正的证据口径

**Ibrahim 2014的23.3%是非零计分网格数增加，而不是统计精度达标网格数增加。** 正式全文p1878 §3.1写明非零计分占比由79.3%到97.8%（相对增加约23.3%，增加501477个元素）。比较两次均为10天MCNP，权窗文件均约0.21 GB；同节MC FOM提高3.4倍。研究采用材料宏观化、确定论网格细化和权窗粗化三个处理。该结果既不是23.3%端到端加速，也不是按某RSD门槛定义的覆盖提升。建议正文采用“固定10天计算下非零计分覆盖增加”，在统计评价处另行定义本研究自己的达标覆盖。

来源：[正式全文](https://web.ornl.gov/~5pe/p081.pdf)，DOI [10.1016/j.fusengdes.2014.02.046](https://doi.org/10.1016/j.fusengdes.2014.02.046)。全文5页、1875—1879；本次经curl有效下载和pdftotext解析。不要将全文中MC FOM与预计算全流程加速互换。

## 逐项核验

|候选|访问层级|核验结果与可用贡献|证据边界与稳定来源|
|---|---|---|---|
|30 Wagner/Haghighat 1998|机构出版记录+摘要|Nuclear Science and Engineering 128(2):186—208；CADIS将S_N伴随用于一致的源偏倚和权窗，展示反应堆压力容器空腔剂量问题|方法思想可用，不照搬摘要泛化的千倍性能。[INL](https://inl.elsevierpure.com/en/publications/automated-variance-reduction-of-monte-carlo-shielding-calculation/)，[DOI](https://doi.org/10.13182/NSE98-2)|
|31 Wagner/Peplow/Mosher 2014|既有全文+ORNL原文检索|NSE 176:37—57。FW-CADIS为分布、多探测器、能谱设计正向加权伴随源|正文公式须说明目标定义和归一化。适合全局不代表所有目标实际相同RSD。[ORNL](https://web.ornl.gov/~peplowde/p068.pdf)，[DOI](https://doi.org/10.13182/NSE12-33)|
|32 Munk/Slaybaugh 2019|开放作者稿+ANS目录|NSE 193(10):1055—1089；综述CADIS、FW-CADIS及角度相关混合方法|综述归纳不能替代新增算法原始证据。[作者稿](https://escholarship.org/content/qt91c500xf/qt91c500xf.pdf)，[DOI](https://doi.org/10.1080/00295639.2019.1586273)|
|33 Ibrahim等2014 MS-CADIS|INL机构摘要|FED 89(9—10):1933—1938；重要性对应最终停堆剂量，跨中子—活化—衰变光子多步骤|不是单次固定源CADIS变体的简单替代；原索引Peterson-Droogh与机构Josh L. Peterson著录有异，应以元数据进一步核对。[INL](https://inl.elsevierpure.com/en/publications/novel-hybrid-monte-carlodeterministic-technique-for-shutdown-dose/)，[DOI](https://doi.org/10.1016/j.fusengdes.2014.03.014)|
|34 Zhao等2025 LAA-CADIS|出版社摘要|ANE 218:111385；局部角度自适应面向复杂通道、强角度相关屏蔽|仅摘要，本次未读全文，不报告图表或具体硬件加速数。[出版社](https://www.sciencedirect.com/science/article/pii/S0306454925002026)，[DOI](https://doi.org/10.1016/j.anucene.2025.111385)|
|35 Ibrahim等2011 ITER|出版社摘要+ORNL记录|Nuclear Technology 175(1):251—258；计算环向场线圈内侧腿核热、生物屏蔽外瞬发剂量、全装置中子/光子网格通量|2017为出版社平台online迁移记录，不应覆盖正式2011卷年。[ORNL](https://impact.ornl.gov/en/publications/iter-neutronics-modeling-using-hybrid-monte-carlo-deterministic-a/)，[DOI](https://doi.org/10.13182/NT175-251)|
|36 Ibrahim等2014网格|正式全文|材料宏观化、确定论细化、权窗空间/能群粗化，ITER瞬发剂量|23.3%口径见前；已经直接解决自适应FW-CADIS和两类网格解耦。[全文](https://web.ornl.gov/~5pe/p081.pdf)|
|37 郑华庆等2016|中文期刊全文HTML|核技术39(9):090502（全文页1—5）；CAD、自动网格和权窗平滑，CLEAR堆顶盖屏蔽|中文原文可支持具体机制，不把其算例推广到所有聚变孔道。[全文](https://html.rhhz.net/hejishu/html/2016/9/2016090502.htm)，[DOI](https://doi.org/10.11889/j.0253-3219.2016.hjs.39.090502)|
|38 He等2021 NECP-MCX|出版社摘要与引言|ANE 151:107978；集成CADIS/FW-CADIS，正/伴随NECP-Hydra生成源偏倚和权窗|摘要FOM约千倍的比较对象为MCNP WWG，不能称对所有MC千倍；2021引言对OpenMC的旧状态须由当前官方文档更新。[出版社](https://doi.org/10.1016/j.anucene.2020.107978)|
|39 Zheng等2021 VENUS-3|出版社摘要|ANE 153:108039；贡献理论指导笛卡儿及嵌套网格权窗粗化，VENUS-3验证减方差和内存节省|粗化与贡献理论组合已有直接先例。无全文，不补硬件数值。[出版社](https://doi.org/10.1016/j.anucene.2020.108039)|
|40 SCALE MAVRIC|官方6.3.1手册|Denovo正/伴随—CADIS偏倚及权窗—Monaco；强调相空间形状与稳健正通量对权窗更重要|手册版本固定6.3.1；Denovo自身并行不等于该MAVRIC序列所有环节并行。[手册](https://scale-manual.ornl.gov/6.3.1/MAVRIC.html)|
|41 OpenMC|官方稳定版方法/用户手册|内置多群random-ray正向后伴随生成FW-CADIS权窗，可指定局部tally targets，另有MAGIC|当前流程仍需MGXS和RR配置；同几何并未消除空间源区细分和权窗网格要求。[用户手册](https://docs.openmc.org/en/stable/usersguide/variance_reduction.html)，[方法手册](https://docs.openmc.org/en/stable/methods/variance_reduction.html)|
|42 Raffuzzi等|既有作者稿全文+出版社全文HTML|正式NSE 200(S1):S485—S502(2026)，online 2025-03-03；在SCONE的RR中实现CADIS/FW-CADIS；比较两类屏蔽与MAGIC|两个算例均bulk shielding，无显著streaming；提高截面或RR解保真度未改善减方差；独立重复波动较大，WW预处理时间在FOM中被忽略。不能据此普遍宣称粗解最优。[出版社](https://www.tandfonline.com/doi/abs/10.1080/00295639.2025.2458958)，[Cambridge](https://www.repository.cam.ac.uk/items/b2f47a30-76cc-4ab1-ba68-d1d9f039e6da)|
|43 Evans等|出版社摘要+ORNL记录|NSE 200(2):444—470(2026)，online 2025-05-28；Shift CPU静态/动态线程历史型和GPU事件型权窗输运|Frontier两例、20节点小于2min；MI250X每GCD吞吐为最佳CPU的9—11倍，不能说整卡或完整自动前处理9—11倍。[ORNL](https://impact.ornl.gov/en/publications/automated-hybrid-variance-reduction-on-advanced-architectures-in-/)，[DOI](https://doi.org/10.1080/00295639.2025.2484511)|
|新增 Munk等2016 CADIS-Ω|现有作者稿全文+arXiv原始摘要|FW/CADIS-Ω: An angle-informed hybrid method for deep-penetration radiation transport；Denovo/ADVANTG实现，混凝土迷宫|利用正/伴随角信息构造替代标量重要性，并不等同于存储完整角度权窗；单迷宫初步结果不代表通用优势。[arXiv](https://arxiv.org/abs/1612.00793)，[作者PDF](https://munkm.github.io/papers/munk_physor16.pdf)|

## 可用于正文的创新边界

1. A方向应同时区别Baker/Liu的响应导向离散、Ibrahim的确定论网格细化与权窗粗化、Zheng的贡献理论粗化。可检验增量是几何/材料路径误差如何影响权窗有效性，以及预算下的离散选择，而非泛称“重要性指导局部加密”。
2. B方向应明确正向GPU计算不自动给出离散伴随。离散伴随应含空间体积、角权与能群配对的内积，验证离散对偶关系和响应恒等式；仅翻转飞行方向不充分。
3. C方向须包含OpenMC random-ray和MAGIC可运行基线；若比较现成FW-CADIS，应核对接口、MGXS与目标设置。权窗粗化、平滑和“在GPU用权窗”皆已有先例。
4. 重要性误差、MC估计无偏性和统计效率是三件不同的事。维持源偏倚支持集及似然权重可保证估计期望；近似重要性仍可能产生稀有大权重或过度分裂，须核验统计稳定性。
5. 尽量不在正文堆砌各论文加速比。真正比较应记录前处理、MGXS、正/伴随、映射、MC、通信/输出和设计更新的全流程时间，并将MC-only FOM单列。

## 补充直接先例 cosRMC 2024

Zhang Xian、Liu Shichang、Li Shu、Chen Yixue，Development of multilevel mesh adaptivity for global variance reduction in Monte Carlo code cosRMC，Fusion Engineering and Design 202 (2024):114372，[DOI](https://doi.org/10.1016/j.fusengdes.2024.114372)。本次访问层级：出版社摘要、引言及分节公开片段；未取得完整数值表和PDF。其方法将材料驱动八叉树局部划分、邻接关系、响应矩阵权窗以及并行内存配置结合，测试CFETR 22.5°环向扇区。故方向A/C应明确区别“材料驱动局部网格+响应矩阵权窗”的已有路径；潜在增量应定位为几何/材料误差对伴随重要性有效性的影响及全流程预算选择，不能泛称首次自适应聚变权窗。

摘要报告自适应权窗相较均匀权窗的计算效率提升53.3%、统计误差小于10%的网格占93.33%；未核对全文效率定义前不将53.3%改写为端到端加速比。第4章正文仅采用方法贡献，不使用上述数值。[出版社入口](https://www.sciencedirect.com/science/article/pii/S0920379624002254)。

CADIS-Ω原始arXiv记录补充：2016-12-02提交，页面给出的会议关联题名为“An Angle-Informed Hybrid Method for CADIS and FW-CADIS”，PHYSOR 2016 (Sun Valley, Idaho, May 2016)。引用arXiv版时保留其自身题名与10.48550/arXiv.1612.00793，避免混用两版题名。
