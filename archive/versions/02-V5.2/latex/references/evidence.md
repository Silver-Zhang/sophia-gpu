# 文献依据（按需查编号）

核查日期：2026-11-08。参考文献完整身份见 main.tex。下列记录限于实际取得的原文、作者稿、摘要或片段，不能视为69篇均已全文核验。V5.2已删除缺少原表支持的定量陈述；被删除的数据不可据历史记录恢复。未记录的硬件、条件和误差不得补写。

## 几何与空间离散

|7 Chen，CAD-MOC，2014，DOI10.1088/1674-1137/38/5/058201|SuperMC中CAD建模和射线求交，二维MOC与菱形差分|V5.2删除未经原表支持的−0.0106%、0.33%偏差，不作数值证据|出版社 https://doi.org/10.1088/1674-1137/38/5/058201 |

|9 Buchan A G, Dargaville S, Pain C C. A combined immersed body and adaptive mesh method for simulating neutron transport within complex structures. 2019. DOI 10.1016/j.anucene.2019.05.044|固定源与本征值；背景有限元网格、独立内部实体|浸没体保守投影与自适应有限元；与不自适应IBM及贴体FEM比较|出版社数值例段明确三类例题；取到方法与结论，无逐表时间数字，故不新增成本倍数|出版社Numerical Examples/Conclusions https://www.sciencedirect.com/science/article/abs/pii/S030645491930297X ；QMUL作者稿链接返回HTML，未得到完整PDF|几何细节与解网格分离，可用于材料投影对照；不等同体素MOC|

|14 Gaston D R, Forget B, Smith K S, et al. Method of Characteristics for 3D, Full-Core Neutron Transport on Unstructured Mesh. 2021. DOI 10.1080/00295450.2021.1871995|三维全堆芯、中子MOC非结构网格|MOCkingbird长特征线、跨域传递，轨迹复用与在线生成选择|约14亿单元、12000处理器；不是GPU速度结果。能群、时间与段数未从可获段落核定|出版社PDF搜索索引摘要页931 https://www.tandfonline.com/doi/pdf/10.1080/00295450.2021.1871995 直接访问403；full版本方法段可被检索|表明通用三维追踪的可扩展性；存储与通信需分别计量|

|18 Baker C M J, Buchan A G, Pain C C, et al. Goal based mesh adaptivity for fixed source radiation transport calculations. 2013. DOI 10.1016/j.anucene.2012.11.029|有探测器的固定源屏蔽；球谐与子网格尺度有限元|子网格校正生成残差；以包络正伴随误差度量的最小椭球组合各向异性指标|出版社摘要与Introduction明确响应精度改善及所需元素减少，未取得逐图数据，不新增倍数|https://www.sciencedirect.com/science/article/abs/pii/S0306454912004744 摘要及Introduction|MOC需依据自身离散重建残差，不能直接挪用有限元公式|

|20 Liu C, Wei J, Li J, et al. Multilevel mesh adaptivity for discrete ordinates transport calculation with spatial-moment-ratio indicators. 2022. DOI 10.1016/j.anucene.2022.109288|三维笛卡儿S_N；单群固定源、多群临界|含指针/数组的金字塔数据结构，优化扫描；空间矩比指标与归一化梯度比较|强非均匀问题相同精度较均匀细化省60%—80%计算成本；误差定义为体积加权L2；未见逐案例硬件和时间数据|出版社Highlights、Abstract、Numerical results段 https://www.sciencedirect.com/science/article/abs/pii/S0306454922003231|局部单元数和扫描组织共同决定收益；非MOC性能保证|

|21 Liu C, Wei J, Zhang B, et al. Goal-Oriented Mesh Adaptivity of Three-Dimensional Neutron Transport Calculation Using Weighted Difference Scheme and Dual-Weighted Residual Error Indicators. 2023. DOI 10.1080/00295639.2023.2169537|三维多群固定源及临界S_N，探测器/积分通量/乘法因子|加权差分重构残差，区域伴随模型与不一致裂变源模型|相近目标高精度下省超过70%工作量及运行时间；未取得逐表硬件/群数/精确秒数|ANS出版摘要 https://wx1.ans.org/pubs/journals/nse/a_54070 ；T&F原始摘要 https://www.tandfonline.com/doi/abs/10.1080/00295639.2023.2169537|目标指标可减少无效加密，但MOC几何与源区误差须分开|

|22 Liu C, Zhang B, Wei J, Tan S. Verification of multilevel octree grid algorithm of S_N transport calculation with the Balakovo-3 VVER-1000 neutron dosimetry benchmark. 2023. DOI 10.1016/j.net.2022.10.017|Balakovo-3 VVER1000固定源剂量、三维笛卡儿S_N|MLTG、简化S2合成加速、六角组件逐棒源投影|950万→190万单元；相对传统S_N/实验RMS约4%/10%；较均匀细网格省约70%成本|出版社Abstract https://www.sciencedirect.com/science/article/pii/S1738573322004983 搜索索引可读，直接访问403。逐表原始数据暂缺|局部网格证据充分；计算和实验差异的指标、基线不同，不混为离散误差|

|64 Shriwise P C, Davis A, Jacobson L J, Wilson P P H. Particle tracking acceleration via signed distance fields in direct-accelerated geometry Monte Carlo. 2017. DOI 10.1016/j.net.2017.08.008|5MeV中心点源，10cm半径密度1g/cm³氢球，1亿历史MC|SDF按物理事件间飞行区间预筛选下一边界求交，需要时仍调用DAGMC|Table1完整三行：MCNP5 wall2.75min，DAG-MCNP5 25.13min，DAG-MCNP5+SDF 7.30min；CPU time2.75/25.04/7.15min，原表time ratio1/9.13/2.65，preconditioner utilization0.97|出版社作者版本 https://www.sciencedirect.com/science/article/am/pii/S1738573317303145 搜索索引直接展示Table1。OSTI原文 https://www.osti.gov/servlets/purl/1425791 可检索但下载超时|可核查的同研究重绘数据；这是MC查询成本证据，不能证明MOC加速|

|66 Porhemmat M H, Mahzoon M, Salehi A A, Hadad K, Hosseinipour K. Improved memory management for solving neutron transport via a novel Modular Ray Tracing (MRT) approach embedded in parallel method of characteristic (MOC) framework. 2021. DOI 10.1016/j.pnucene.2020.103590|二维MOC、C5G7、正向与伴随|模块化追踪减少存储和改善cache，比较三种角向求积|LC S20的正/伴随keff与参考差7e-6/9e-6；16 CPU线程speedup6.18。摘要未提供存储百分比，不造数字|出版社Abstract和Modular Ray Tracing段 https://www.sciencedirect.com/science/article/abs/pii/S0149197020303371|重复单元的模块复用不能假定适合任意聚变几何；需测复用率|

|68 Amanatides J, Woo A. A Fast Voxel Traversal Algorithm for Ray Tracing. 1987. DOI10.2312/egtp.19871000|规则三维网格射线遍历，非中子算例|沿x/y/z到下一网格面的参数比较，推进最小者|基本邻格推进两次浮点比较、一次加法；不包括初始化、材质查询和物理扫描。不可当作中子GPU实测|作者原文 https://www.cse.yorku.ca/~amana/research/grid.pdf 搜索摘要可读，直接下载超时；Eurographics数字库目录核身份|输入射线/网格，输出有序单元及区间；用于体素MOC材料段生成|

|69 Laine S, Karras T. Efficient Sparse Voxel Octrees. 2010. DOI10.1145/1730804.1730814|稀疏表面体素GPU图形学|紧凑层级结构、子节点掩码/相对寻址、轮廓辅助查询|核查实际技术，不将图形学ray casts吞吐引入中子性能结论|NVIDIA作者机构原始主页、论文及技术报告 https://research.nvidia.com/publication/2010-02_efficient-sparse-voxel-octrees 及 https://research.nvidia.com/sites/default/files/pubs/2010-02_Efficient-Sparse-Voxel/laine2010tr1_paper.pdf|可借鉴叶单元定位与局部存储；不能直接用首表面终止和稀疏表面代替体输运|

## GPU计算

|13 Boyd W, Shaner S, Li L, Forget B, Smith K. **The OpenMOC method of characteristics neutral particle transport code**. 2014. DOI 10.1016/j.anucene.2013.12.012|二维C5G7七群本征值，平源MOC；另有扩散验证|显式轨迹；能群内层向量化；CUDA轨迹扫描；CMFD|C5G7为142964平源区；第5.3节GPU试验4–128方位角，最大约50倍；CMFD表7：无加速715扫/4655 s，阻尼0.7为21扫/207 s|GPU对单Xeon核，图11；CMFD为同文数值配置，表7；作者稿第7、10–11页|任务并行度与迭代次数均会改变总成本。实际取得MIT作者稿；GPU型号文字在图内，正文不据抽取失败作过细归属。来源https://dspace.mit.edu/server/api/core/bitstreams/c3c8d02f-80f0-4d84-9b8c-dc388917a03b/content |

|24 Song Q, Wang R, Shen Y, Wu Y, Feng K, Guo H, Xiao Y, Gu H. **GPU-accelerated few-group 3D Method of Characteristics for full-core neutron transport in Small Modular Reactors**. 2026. DOI 10.1016/j.pnucene.2025.106109|C5G7组件、扩展三维基准和SMR四群全堆芯，OpenMOC上直接3D MOC|线性源减少所需段；OTF轴向追踪以二维段在线构造三维段；分批限制轨迹和边界通量驻留；GPU CMFD|25 cm组件平源显式基线22129 MB；组合配置组件显存降低98.5%；SMR单GPU可运行|出版社Conclusion及Introduction；显存降低为同文组合优化对原配置。GPU型号、完整收敛阈值/各项消融表未取得，不补写|显存收益涉及源阶次、段数组和边界通量，不能归于单项。取得出版社摘要与章节片段，未取得全文表格。https://www.sciencedirect.com/science/article/pii/S0149197025005074 |

|28 宋佩涛等，异构MOC，2019，DOI10.7538/yzk.2019.youxian.0416|MPI通信重叠、异步主机设备传输与任务分配|V5.2删除K80数量、节点数和87%→95%效率；只介绍方法|期刊 https://yznkxjs.xml-journal.net/article/doi/10.7538/yzk.2019.youxian.0416；学位论文[32]摘要|

|29 Li S, Wang Z, Bu L, Wang J, Xin Z, Li S, Wang Y, Feng Y, Shi P, Hu Y, Chi X. **ANT-MOC: Scalable Neutral Particle Transport Using 3D Method of Characteristics on Multi-GPU Systems**. 2023. DOI 10.1145/3581784.3607063|三维全堆芯，中性粒子MOC|存储/计算/通信成本模型；节点/GPU/CU多层负载映射；轨迹管理|约10^11轨迹、16000 GPU；强/弱扩展效率70.69%/89.38%|SC23正式论文档案摘要；未取得全文计时表、群数或效率分母的具体规模|规模数字只按摘要使用；不能重构扩展曲线或比较GPU品牌。https://sc23.supercomputing.org/proceedings/tech_paper/tech_paper_pages/pap300.html |

|30 Dzianisau S, Lee D. **Axially decomposed GPU-enabled three-dimensional method of characteristics/diamond difference solver in neutron transport code STREAM3D-GPU**. 2026. DOI 10.1016/j.cpc.2025.109952|OPR-1000四分之一堆芯，含热工反馈，MOC/DD|轴向数据分解及异步执行|每MPI进程GPU需求从约50 GB降至<4.5 GB；8/16 GPU的MOC/DD求解22.1/40.5倍|128 CPU核参考；出版社摘要。全文抓取403，硬件与详细计时表未取得|只能讨论摘要明确的容量/求解对照；不能与2024会议八分之一堆芯混为相同试验。https://www.sciencedirect.com/science/article/pii/S0010465525004539 |

|35 Dzianisau S, Lee D. **GPU Acceleration of 3D MOC Solver in STREAM3D Using OpenACC**. KNS Spring Meeting, 2024（会议PDF无DOI）|C5G7四分之一：7群、64轴向平面；OPR-1000八分之一：72群、197平面、热工反馈；3 cm轴向网格|按平面传输入/出角通量及CMFD电流，部分数据保留设备；OpenACC卸载MOC|64核（2×EPYC 7543）CPU参考，对同主机+8×RTX A5000；C5G7 MOC 1368→34 s、总1704→100 s；OPR MOC 61535→3995 s、总212416→11201 s|第2页表1、第3页表2；方法第1–2页；作者报告两版本keff一致；未给其差值精度|OPR总时间还受径向MPI分区等待改变影响；不归于扫描单核。原始PDF全部三页已读。https://www.kns.org/files/pre_paper/51/24S-051-Siarhei.pdf |

|31 Kim KM, Im J, Lee HG, Jung YS. **Verification and Performance Assessment of NuDEAL, a GPU-Accelerated Deterministic Transport Framework on Unstructured Meshes**. 2026. DOI 10.1080/00295639.2026.2652773；数据版arXiv:2607.01591v1|C5G7及先进堆本征值；MOC/HFEM、DGMOC、DFEM-SN|预存平面段；方位角顺序扫描；压缩角通量，DoF细粒度并行|3D C5G7 DGMOC：8507520单元=283584×30，RTX2080Ti；角块大小2/4/8/16/32时显存2589/2893/3499/4709/7133 MB；sweep 5.25/5.19/5.10/5.10/5.09 s；MOC 10.50/9.96/9.50/9.30/9.21 s；64角OOM|公开作者稿表5–6；2D DFEM表2：同RTX4070Ti顺序/并发148/26 s。期刊4月23日在线，公开稿7月2日；本次没有逐页核对最终期刊文本|每块角数增加不等于块数增加；多占2.75倍显存仅使sweep快约3.0%。图4严格依据作者稿表6，不能声称已核对期刊最终表号。https://arxiv.org/html/2607.01591v1 |

|33 Wang A, Wang J, Ding Z, Geng X, Shan H, Hu Y, Chen D. **A cyclic-track decomposition method for 3D MOC neutron transport simulation**. 2024. DOI 10.1016/j.nucengdes.2024.113148|轴向挤出几何三维MOC，ANT-MOC|MRT周期轨迹、OTF、组合负载模型，比角度分解细|ORISE 10240→98304 CPU核，效率>40%；节点32核AMD Zen、128 GiB|出版社摘要及Results片段；比较角度分解与循环轨迹分解；完整试验表未取得|规则几何可解析预测负载；一般体素场须重新估计分段/材料访问。https://www.sciencedirect.com/science/article/pii/S0029549324002486 |

## 聚变与减方差

|ref1 Ebiwonjumi B, Segantin S, Peterson E. OpenMC Interpretation of FNS SINBAD Shielding Benchmark Experiments. 2025. DOI10.1080/15361055.2024.2323747|FNS W/V/Be，14MeV D-T，OpenMC0.14.1-dev，ENDF/B-VII.1；实验及MCNP6.2对照|9点铍TPR C/E均值1.0295、SD0.1956；7点W/V GHR均值0.9537、SD0.1366；V三点0.9437/0.0143，W四点0.9611/0.1799|实际下载MIT作者稿PDF并提取全文，PDF第21页TableVIII/IX及III.D后段；https://library.psfc.mit.edu/catalog/reports/2020/24ja/24ja039/24ja039_full.pdf|简单未加权平均，SD是测点间C/E离散度，不能解释为MC统计误差或空间误差；作者稿表号与最终期刊版本可能不同|

|ref51 Ibrahim AM, Wilson PPH, Sawan ME, et al. Assessment of fusion facility dose rate map using mesh adaptivity enhancements of hybrid Monte Carlo/deterministic techniques. 2014. DOI10.1016/j.fusengdes.2014.02.046|ITER设施瞬发中子+光子剂量，Denovo/MCNP FW-CADIS；材料宏观化、求解网格细化、权窗粗化三者联合|两次MCNP都为10天，权窗文件约0.21GB；非零计分79.3%→97.8%，多501477元素，数量相对增23.3%；全局平均相对方差MC FOM改善3.4倍；Denovo空间能量元素16.4e6→528.0e6，权窗粗化至16.3e6|实际下载ORNL作者托管原文，PDF第4页/期刊1878页3.1节与图2；https://web.ornl.gov/~5pe/p081.pdf|求解网格/查询网格可以不同；0.21GB是硬盘文件大小，不能直接当GPU驻留显存。3.4倍是三项联合不是单独细化收益；本轮不重绘原曲线|

|ref50 Raffuzzi V, Neame R, Cosgrove P. Application of the Random Ray Method to Variance Reduction in Radiation Shielding Problems. 2026. DOI10.1080/00295639.2025.2458958|SCONE混凝土整体屏蔽；随机射线FW-CADIS，P0-FS；20次独立完整运行|仅MC时间FOM为1.08±0.14，计入WW生成为0.96±0.12 min^-1|出版社PDF搜索索引Table V，P0-FS列，S495页；直接下载403。https://www.tandfonline.com/doi/pdf/10.1080/00295639.2025.2458958|仅这两项得到原表索引支持；±为完整运行间SD。V5.2删除未重新核实的MAGIC数对，不再称其已验证。|

|ref58 Evans TM, Royston KE, Hamilton SP, et al. Automated Hybrid Variance Reduction on Advanced Architectures in the Shift Monte Carlo Code. 2026. DOI10.1080/00295639.2025.2484511|Frontier两固定源屏蔽、Shift CPU历史型静/动态与GPU事件型，CADIS/FW-CADIS|20节点MC阶段<2min；AMD MI250X每GCD吞吐为最佳CPU实现9–11倍；动态线程扩展行为可改善至20%|ORNL作者机构摘要 https://impact.ornl.gov/en/publications/automated-hybrid-variance-reduction-on-advanced-architectures-in-/；未得逐表数据|这是MC事件执行，不是MOC加速，不能加入确定论速度排名|

|ref3 Moreno C, Bader A, Wilson P. ParaStell. 2024. DOI10.3389/fnuen.2024.1384788|ParaStell参数化WISTELL-D包层与屏蔽，DAGMC/OpenMC，11×9=99种几何，2113 MW聚变源功率|研究中的总厚度100%、增殖层比例60%设计点：TBR 1.10、磁体总核热152.0 kW|出版社开放全文第3.2–3.3节 https://www.frontiersin.org/journals/nuclear-engineering/articles/10.3389/fnuen.2024.1384788/full|TBR和热对应指定设计点与功率，不外推为所有99种模型的结果。|

|ref61 Iwamoto Y, Tsuda S, Ogawa T. Benchmark shielding calculations for fusion and accelerator-driven subcritical systems. 2023. DOI10.3389/fenrg.2023.1085264|FNS铁屏蔽，PHITS/JENDL-4.0；0.003–10 MeV积分中子产额|表1深度11/21/31/41/61/96 cm的C/E依次为1.39±0.01、1.31±0.01、1.24±0.01、1.21±0.01、1.15±0.01、1.78±0.02|出版社开放全文Table 1及邻近说明 https://www.frontiersin.org/journals/energy-research/articles/10.3389/fenrg.2023.1085264/full|正文保留六位置范围1.15–1.78，表列不确定度为计数统计；删除此次未复核的铁体尺寸。|
