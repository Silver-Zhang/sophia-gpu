# 聚变应用与原证据复核

核查日期2026-11-08。原论文只暂存系统临时目录，公开提交仅含数值事实和定位，不含原图、全文。

|身份|对象、方法与条件|原始结果与基线|证据位置与来源|技术认识与限制|
|---|---|---|---|---|
|ref1 Ebiwonjumi B, Segantin S, Peterson E. OpenMC Interpretation of FNS SINBAD Shielding Benchmark Experiments. 2025. DOI10.1080/15361055.2024.2323747|FNS W/V/Be，14MeV D-T，OpenMC0.14.1-dev，ENDF/B-VII.1；实验及MCNP6.2对照|9点铍TPR C/E均值1.0295、SD0.1956；7点W/V GHR均值0.9537、SD0.1366；V三点0.9437/0.0143，W四点0.9611/0.1799|实际下载MIT作者稿PDF并提取全文，PDF第21页TableVIII/IX及III.D后段；https://library.psfc.mit.edu/catalog/reports/2020/24ja/24ja039/24ja039_full.pdf|简单未加权平均，SD是测点间C/E离散度，不能解释为MC统计误差或空间误差；作者稿表号与最终期刊版本可能不同|
|ref51 Ibrahim AM, Wilson PPH, Sawan ME, et al. Assessment of fusion facility dose rate map using mesh adaptivity enhancements of hybrid Monte Carlo/deterministic techniques. 2014. DOI10.1016/j.fusengdes.2014.02.046|ITER设施瞬发中子+光子剂量，Denovo/MCNP FW-CADIS；材料宏观化、求解网格细化、权窗粗化三者联合|两次MCNP都为10天，权窗文件约0.21GB；非零计分79.3%→97.8%，多501477元素，数量相对增23.3%；全局平均相对方差MC FOM改善3.4倍；Denovo空间能量元素16.4e6→528.0e6，权窗粗化至16.3e6|实际下载ORNL作者托管原文，PDF第4页/期刊1878页3.1节与图2；https://web.ornl.gov/~5pe/p081.pdf|求解网格/查询网格可以不同；0.21GB是硬盘文件大小，不能直接当GPU驻留显存。3.4倍是三项联合不是单独细化收益；本轮不重绘原曲线|
|ref50 Raffuzzi V, Neame R, Cosgrove P. Application of the Random Ray Method to Variance Reduction in Radiation Shielding Problems. 2026. DOI10.1080/00295639.2025.2458958|SCONE混凝土整体屏蔽；随机射线FW-CADIS，P0-FS；20次独立完整运行|仅MC时间FOM为1.08±0.14，计入WW生成为0.96±0.12 min^-1|出版社PDF搜索索引Table V，P0-FS列，S495页；直接下载403。https://www.tandfonline.com/doi/pdf/10.1080/00295639.2025.2458958|仅这两项得到原表索引支持；±为完整运行间SD。V5.2删除未重新核实的MAGIC数对，不再称其已验证。|
|ref58 Evans TM, Royston KE, Hamilton SP, et al. Automated Hybrid Variance Reduction on Advanced Architectures in the Shift Monte Carlo Code. 2026. DOI10.1080/00295639.2025.2484511|Frontier两固定源屏蔽、Shift CPU历史型静/动态与GPU事件型，CADIS/FW-CADIS|20节点MC阶段<2min；AMD MI250X每GCD吞吐为最佳CPU实现9–11倍；动态线程扩展行为可改善至20%|ORNL作者机构摘要 https://impact.ornl.gov/en/publications/automated-hybrid-variance-reduction-on-advanced-architectures-in-/；未得逐表数据|这是MC事件执行，不是MOC加速，不能加入确定论速度排名|

|ref3 Moreno C, Bader A, Wilson P. ParaStell. 2024. DOI10.3389/fnuen.2024.1384788|ParaStell参数化WISTELL-D包层与屏蔽，DAGMC/OpenMC，11×9=99种几何，2113 MW聚变源功率|研究中的总厚度100%、增殖层比例60%设计点：TBR 1.10、磁体总核热152.0 kW|出版社开放全文第3.2–3.3节 https://www.frontiersin.org/journals/nuclear-engineering/articles/10.3389/fnuen.2024.1384788/full|TBR和热对应指定设计点与功率，不外推为所有99种模型的结果。|
|ref61 Iwamoto Y, Tsuda S, Ogawa T. Benchmark shielding calculations for fusion and accelerator-driven subcritical systems. 2023. DOI10.3389/fenrg.2023.1085264|FNS铁屏蔽，PHITS/JENDL-4.0；0.003–10 MeV积分中子产额|表1深度11/21/31/41/61/96 cm的C/E依次为1.39±0.01、1.31±0.01、1.24±0.01、1.21±0.01、1.15±0.01、1.78±0.02|出版社开放全文Table 1及邻近说明 https://www.frontiersin.org/journals/energy-research/articles/10.3389/fenrg.2023.1085264/full|正文保留六位置范围1.15–1.78，表列不确定度为计数统计；删除此次未复核的铁体尺寸。|

V5.2按用户新增批注重新筛选定量结论。缺少原文支持的数值从正文和表格删除，明细见qa/round2_evidence_decisions.md。文献身份核验和原文数值核验分别记录。数学恒等式与权重归一化继续进行源码保护和人工物理检查。
