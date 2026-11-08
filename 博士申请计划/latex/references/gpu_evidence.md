# GPU-MOC证据核查（2026-11-08）

本文件记录可直接核查的证据与尚未取得的信息；“未取得”不等于论文未报告。只对下列已取得的作者稿、会议原文或出版社摘要/章节片段作判断。下载的论文仅在临时目录阅读，未把版权受限PDF提交公开仓库。

## 核心文献证据矩阵

|编号、论文身份|计算对象与方法|算法/数据组织|条件与实测结果|比较基线、证据位置|研究认识与可用性|
|---|---|---|---|---|---|
|13 Boyd W, Shaner S, Li L, Forget B, Smith K. **The OpenMOC method of characteristics neutral particle transport code**. 2014. DOI 10.1016/j.anucene.2013.12.012|二维C5G7七群本征值，平源MOC；另有扩散验证|显式轨迹；能群内层向量化；CUDA轨迹扫描；CMFD|C5G7为142964平源区；第5.3节GPU试验4–128方位角，最大约50倍；CMFD表7：无加速715扫/4655 s，阻尼0.7为21扫/207 s|GPU对单Xeon核，图11；CMFD为同文数值配置，表7；作者稿第7、10–11页|任务并行度与迭代次数均会改变总成本。实际取得MIT作者稿；GPU型号文字在图内，正文不据抽取失败作过细归属。来源https://dspace.mit.edu/server/api/core/bitstreams/c3c8d02f-80f0-4d84-9b8c-dc388917a03b/content |
|24 Song Q, Wang R, Shen Y, Wu Y, Feng K, Guo H, Xiao Y, Gu H. **GPU-accelerated few-group 3D Method of Characteristics for full-core neutron transport in Small Modular Reactors**. 2026. DOI 10.1016/j.pnucene.2025.106109|C5G7组件、扩展三维基准和SMR四群全堆芯，OpenMOC上直接3D MOC|线性源减少所需段；OTF轴向追踪以二维段在线构造三维段；分批限制轨迹和边界通量驻留；GPU CMFD|25 cm组件平源显式基线22129 MB；组合配置组件显存降低98.5%；SMR单GPU可运行|出版社Conclusion及Introduction；显存降低为同文组合优化对原配置。GPU型号、完整收敛阈值/各项消融表未取得，不补写|显存收益涉及源阶次、段数组和边界通量，不能归于单项。取得出版社摘要与章节片段，未取得全文表格。https://www.sciencedirect.com/science/article/pii/S0149197025005074 |
|28 宋佩涛, 张志俭, 梁亮, 等. **基于CPU-GPU异构并行的MOC中子输运计算并行效率优化研究**. 2019. DOI 10.7538/yzk.2019.youxian.0416|二维MOC异构并行|MPI通信掩盖、异步主机设备拷贝|5节点效率87%→95%，由原稿及32号学位论文摘要相互支持；K80数量为V4.2已有，未取得期刊硬件原表进行独立复核|基线为优化前异构算法；学位论文32号摘要第(3)项|通信等待是可解释收益；保留V4.2证据并标明核查边界。期刊页面只能提取框架，学位论文原数据库摘要可读。https://yznkxjs.xml-journal.net/article/doi/10.7538/yzk.2019.youxian.0416 ; https://cnki.istiz.org.cn/kcms/detail/detail.aspx?dbcode=CDFD&dbname=CDFD2024&filename=1023018169.nh |
|29 Li S, Wang Z, Bu L, Wang J, Xin Z, Li S, Wang Y, Feng Y, Shi P, Hu Y, Chi X. **ANT-MOC: Scalable Neutral Particle Transport Using 3D Method of Characteristics on Multi-GPU Systems**. 2023. DOI 10.1145/3581784.3607063|三维全堆芯，中性粒子MOC|存储/计算/通信成本模型；节点/GPU/CU多层负载映射；轨迹管理|约10^11轨迹、16000 GPU；强/弱扩展效率70.69%/89.38%|SC23正式论文档案摘要；未取得全文计时表、群数或效率分母的具体规模|规模数字只按摘要使用；不能重构扩展曲线或比较GPU品牌。https://sc23.supercomputing.org/proceedings/tech_paper/tech_paper_pages/pap300.html |
|30 Dzianisau S, Lee D. **Axially decomposed GPU-enabled three-dimensional method of characteristics/diamond difference solver in neutron transport code STREAM3D-GPU**. 2026. DOI 10.1016/j.cpc.2025.109952|OPR-1000四分之一堆芯，含热工反馈，MOC/DD|轴向数据分解及异步执行|每MPI进程GPU需求从约50 GB降至<4.5 GB；8/16 GPU的MOC/DD求解22.1/40.5倍|128 CPU核参考；出版社摘要。全文抓取403，硬件与详细计时表未取得|只能讨论摘要明确的容量/求解对照；不能与2024会议八分之一堆芯混为相同试验。https://www.sciencedirect.com/science/article/pii/S0010465525004539 |
|35 Dzianisau S, Lee D. **GPU Acceleration of 3D MOC Solver in STREAM3D Using OpenACC**. KNS Spring Meeting, 2024（会议PDF无DOI）|C5G7四分之一：7群、64轴向平面；OPR-1000八分之一：72群、197平面、热工反馈；3 cm轴向网格|按平面传输入/出角通量及CMFD电流，部分数据保留设备；OpenACC卸载MOC|64核（2×EPYC 7543）CPU参考，对同主机+8×RTX A5000；C5G7 MOC 1368→34 s、总1704→100 s；OPR MOC 61535→3995 s、总212416→11201 s|第2页表1、第3页表2；方法第1–2页；作者报告两版本keff一致；未给其差值精度|OPR总时间还受径向MPI分区等待改变影响；不归于扫描单核。原始PDF全部三页已读。https://www.kns.org/files/pre_paper/51/24S-051-Siarhei.pdf |
|31 Kim KM, Im J, Lee HG, Jung YS. **Verification and Performance Assessment of NuDEAL, a GPU-Accelerated Deterministic Transport Framework on Unstructured Meshes**. 2026. DOI 10.1080/00295639.2026.2652773；数据版arXiv:2607.01591v1|C5G7及先进堆本征值；MOC/HFEM、DGMOC、DFEM-SN|预存平面段；方位角顺序扫描；压缩角通量，DoF细粒度并行|3D C5G7 DGMOC：8507520单元=283584×30，RTX2080Ti；角块大小2/4/8/16/32时显存2589/2893/3499/4709/7133 MB；sweep 5.25/5.19/5.10/5.10/5.09 s；MOC 10.50/9.96/9.50/9.30/9.21 s；64角OOM|公开作者稿表5–6；2D DFEM表2：同RTX4070Ti顺序/并发148/26 s。期刊4月23日在线，公开稿7月2日；本次没有逐页核对最终期刊文本|每块角数增加不等于块数增加；多占2.75倍显存仅使sweep快约3.0%。图4严格依据作者稿表6，不能声称已核对期刊最终表号。https://arxiv.org/html/2607.01591v1 |
|33 Wang A, Wang J, Ding Z, Geng X, Shan H, Hu Y, Chen D. **A cyclic-track decomposition method for 3D MOC neutron transport simulation**. 2024. DOI 10.1016/j.nucengdes.2024.113148|轴向挤出几何三维MOC，ANT-MOC|MRT周期轨迹、OTF、组合负载模型，比角度分解细|ORISE 10240→98304 CPU核，效率>40%；节点32核AMD Zen、128 GiB|出版社摘要及Results片段；比较角度分解与循环轨迹分解；完整试验表未取得|规则几何可解析预测负载；一般体素场须重新估计分段/材料访问。https://www.sciencedirect.com/science/article/pii/S0029549324002486 |

## 重要更正与使用范围

1. V4.2把NuDEAL的“angle block size 2/32”解释为“分成2块/32块”，V5改为“每块含2/32个方位角”。全部并发64角OOM明确保留在数据及图注中，不作为零时间绘制。
2. 删除跨论文9–50倍加速范围所支撑的一般性判断。各论文硬件、核数、精度、迭代及问题均不同，保留条件表，以NuDEAL同论文参数扫描替换图4。
3. NuDEAL已取得的是作者原稿，期刊出版信息只用于身份；图表来源明确写arXiv版本。未假定原稿与最终排版一致。
4. 其余V4.2 GPU固定源、伴随与瞬态证据保留；本任务优先深化上表8项，不将保留的旧数字标记为“本轮原文复核通过”。

## 图4数据与许可

`nudeal_table6.csv`保留表6全部6种配置，64角OOM记录为空，不填造值。`plot_nudeal.py`独立绘制2个面板，不复制原图构图或图像；引用原始事实数据及算法结果。arXiv non-exclusive license并不授权转载原论文图片，本次没有转载任何原图。曲线连接离散配置用于阅读，不作插值；不确定度未报告。
