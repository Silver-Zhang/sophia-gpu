# V2第二章 几何材料表示与空间离散证据

核验日期：2026-11-06。范围：原r6—r18共13项，以及4篇补充原始文献。只生成V2证据文件，没有修改原文、批注、删改状态或任何成品。`geometry_evidence.json`逐项保存作者、题名、DOI、正式卷年、方法、对象、算例、数字及其定位、可用认识、访问层级和未解决项。以下为交给正文重构者的证据组织建议，不是正式章节草稿。

## 本轮实际访问

- 成功下载并验证2份完整PDF：Chen的arXiv作者稿9页、AMReX作者版19页，实际读了方法及相关结果节。两者正式引用分别沿用2014和2021期刊条目。
- OpenMOC重新查MIT官方元数据，并补读已有合法接受稿的§5、§6；本轮下载端点返回429，不把它计为新增全文下载。
- Baker、Buchan、Yang、Liu各篇及Wilson主要取得出版社摘要、引言或索引全文的关键节选；JSON逐条区分。Buchan的QMRO标称PDF返回JavaScript访问页，Liu工程验证OA直链和Gaston的PDF返回403，已记录失败而未当作PDF。
- `geometry_sources/`保存本地缓存和提取文本，`.gitignore`忽略全文及网页，只保留获取日志和忽略规则，供本地追溯而不直接提交版权全文。

## 原有证据的深化

| Key | 核实的具体方法与位置 | 对V2论证的作用 |
|---|---|---|
| r6 OpenMOC | MIT接受稿§5.1二维C5G7、§5.2 LRA、§6明确为二维输运代码 | 定位MOC/CSG及框架基础，避免用2014工作暗指一般三维几何能力 |
| r7 Gaston | 出版社索引全文§IV含首次保存/完全在线两种分段；§IV.E跨域整轨迹传播 | 几何适应性、分段存储、扫描依赖共同决定成本 |
| r8 Chen | 作者稿§3 MCAM建模/求交，§4.1 Table1、§4.3 Table4，PDF p3—7 | CAD接口解决几何访问；DD针对平通量空间近似；简单与复杂模型分别验证 |
| r9 Yang | 出版社Highlights、引言、§3验证对象、结论 | BREP→CSG和体积加权混合材料属于建模层；NUREG/CR-6115是工程对象 |
| r10 Baker | 出版社§2离散、§3目标度量、§4算例类别节选 | 球谐＋子网格尺度空间FEM、残差构造及正/伴随各向异性度量是具体贡献 |
| r11 Goffin | 出版社摘要与方法结构 | keff目标导向与固定源探测器目标的伴随/误差定义需要区分 |
| r12 Buchan | 出版社引言与§3/§5结构节选 | supermeshing守恒投影材料体积到独立背景FEM，使几何/解分辨率解耦 |
| r13 Liu2020 | ANS正式摘要 | 多层八叉树非匹配笛卡儿表示；引出跨粗细界面的角通量传递问题 |
| r14 Liu2022 | 出版社Highlights、Abstract、Numerical results/Conclusions节选 | 金字塔数据结构、扫描优化、空间矩比指标；主要追求全局空间精度 |
| r15 Liu2023 | ANS与出版社详细摘要 | 加权差分通量重构残差、DWR及近似伴随模型；目标量为探测器/积分通量/keff |
| r16 Wilson2026 | 出版社索引全文关键方法、§8.1.1、Table2、Fig3/4 | h(p)-IGA的参考解/粗空间投影及部分一致DSA，把误差控制与求解成本联系起来 |
| r17 AMReX | 作者PDF p4 §5.1/5.2、p7 §7、p13—14 §9 | BoxArray/DistributionMapping、用户标记/重网格、SFC/knapsack和EB；是基础设施而非现成输运粗细界面算法 |
| r18 任等综述 | 官方中英文摘要及正式卷期 | 说明平衡细分与重建成本，作为外围组织参考，非核输运新增算法的原始证据 |

原始入口：[OpenMOC MIT](https://dspace.mit.edu/entities/publication/c6e8edd6-071b-43ef-adc8-ed39dcb55ae7)、[Chen作者稿](https://arxiv.org/abs/1306.5077)、[Yang](https://www.sciencedirect.com/science/article/abs/pii/S0029549324000943)、[Baker](https://www.sciencedirect.com/science/article/abs/pii/S0306454912004744)、[Buchan](https://www.sciencedirect.com/science/article/abs/pii/S030645491930297X)、[Liu2022](https://www.sciencedirect.com/science/article/abs/pii/S0306454922003231)、[Liu2023](https://wx1.ans.org/pubs/journals/nse/a_54070)、[Wilson](https://www.sciencedirect.com/science/article/pii/S0045782526001453)、[AMReX正式刊](https://journals.sagepub.com/doi/full/10.1177/10943420211022811)。其余逐项入口见JSON。

## 两组百分数的准确口径

Liu2022的60%—80%出自出版社摘要与Highlights，比较对象为均匀细化，条件为强非均匀算例达到相同精度；Numerical results节选说明覆盖单群固定源和多群临界问题，均匀参考由ARES获得。当前公开材料不足以逐例分配60%或80%，也没有完整硬件/计时表。本轮可确认的是“原文算例的相同精度成本节省”，不将其转为GPU加速、整个耦合流程或所有屏蔽响应的收益。[出版社](https://www.sciencedirect.com/science/article/abs/pii/S0306454922003231)

Liu2023的“超过70%”出自官方详细摘要末句，指其考察目标在获得与均匀细网格可比精度时，计算工作量与运行时间的节省。具体目标、伴随近似和残差重构是方法的一部分；不应只保留数字而省略其离散条件。正式版为NSE 197(11):2853—2883，online和正式卷期日期分别记录。[ANS官方](https://wx1.ans.org/pubs/journals/nse/a_54070)

## 四篇必要新增原始文献

1. **new_wang_ragusa2011**：Yaqi Wang、Jean C. Ragusa，JCP 230(3):763—788，DOI [10.1016/j.jcp.2010.10.018](https://doi.org/10.1016/j.jcp.2010.10.018)。比较标准与目标导向DG-S_N自适应，以角矩而非逐方向信息配置二维非结构三角网格。必要性在于补出“远端小值区绝对误差小而相对误差可能大”的方法动机，并提供两网格估计/跳跃指标的比较基础。[INL原始机构记录](https://inl.elsevierpure.com/en/publications/standard-and-goal-oriented-adaptive-mesh-refinement-applied-to-ra/)
2. **new_lathouwers2011**：Danny Lathouwers，ANE 38(6):1373—1381，DOI [10.1016/j.anucene.2011.01.038](https://doi.org/10.1016/j.anucene.2011.01.038)。二维DG-S_N的DWR将完整角度依赖纳入误差估计，结合目标误差界和LEPP细化。必要性在于给出目标指标与目标容限停止条件的衔接，而非把伴随通量本身当作误差。[出版社方法节选](https://www.sciencedirect.com/science/article/abs/pii/S0306454911000594)
3. **new_liu_mapping2021**：Cong Liu、Bin Zhang、Yixue Chen，ANE 152:108033，DOI [10.1016/j.anucene.2020.108033](https://doi.org/10.1016/j.anucene.2020.108033)。以形状/平衡因子在非负线性、非线性映射之间预测校正选择，服务零阶格式的跨非匹配界面传递。必要性在于把“局部加密的界面误差”落实为已有专门研究，形成网格组织—界面重构—目标误差的技术链。[出版社原条目摘要所在作者页](https://www.sciencedirect.com/author/58366099200/bin-zhang)
4. **new_liu_balakovo2023**：Cong Liu、Bin Zhang、Junxia Wei、Shuang Tan，NET 55(2):756—768，DOI [10.1016/j.net.2022.10.017](https://doi.org/10.1016/j.net.2022.10.017)。Balakovo-3堆外剂量基准结合多层八叉树、S2加速和棒级源投影。摘要给出9.5百万→1.9百万网格、对传统S_N/实验分别约4%/10% RMS、较均匀细网格节省约70%成本。必要性是补充已有层级表示在真实工程响应上的验证，同时显示源投影也是精度链的一环。[OA出版社入口](https://www.sciencedirect.com/science/article/pii/S1738573322004983)

四篇新增均为原始研究。第一、二篇主要基于官方摘要、引言和方法节选；第三篇为出版社原始文章摘要；第四篇为OA摘要和方法/源投影公开片段。没有将其中任何一篇标为已完整取得并精读全文。

## 适合第二章的五段论证建议

第一段宜围绕“设计几何如何变成输运材料序列”组织2.1：CSG/CAD求交保留显式界面，体积加权映射和浸没体投影则把多材料实体转为背景网格上的有效材料。Chen、Yang、Buchan分别代表几何访问、材料均匀化和几何—解网格解耦，比较其处理对象比并列列举CAD/体素名称更有解释力。图中可区分实体边界、材料单元、源区和轨迹段，并以同一斜界面展示它们的对应关系。

第二段宜把MOC放在这种表示之后说明：沿轨迹积分所见的是有序材料段及源近似，规则块和非结构单元改变求交、覆盖和分段。OpenMOC的二维验证与Gaston的一般三维追踪体现不同几何假设；这能自然引出几何自由度与段存储/跨域传播之间的代价，而不需要反复宣称某表示“更快”。关键判断应由相同目标精度下的完整准备和求解成本支持。

第三段宜将自适应文献拆成三项不同进展：Liu2020主要解决多层几何/数据组织；Liu2021专门处理非匹配角通量映射；Liu2022用空间矩比改善全局场精度。跨界重构与光学厚度决定粗化后局部误差是否可控，源投影又影响工程响应。Balakovo验证可作为此链的落点：同时报告网格、源、数值参考及实验比较，避免只用未知量减少推断可靠性。

第四段宜以任务定义解释目标导向：Wang/Ragusa和Lathouwers表明深屏蔽远端的相对误差需求难由全局绝对误差直接满足；Baker的各向异性度量、Liu2023的重构残差/近似伴随与Wilson的h(p)参考解分别解决指标、可计算性和误差控制成本。这里的核心是“局部残差对指定目标的贡献”，并应说明目标改变后伴随及指标也会改变。60%—80%和>70%只在各自基线条件下使用。

第五段可收束到2.3的可研究机制：以薄层、斜界面和孔道为受控几何，先测材料体积、弦长/光学路径、跨界通量传递和目标响应的关联，再比较何种局部配置值得其建立与更新成本。AMReX负责层级块和数据分布，MOC覆盖/界面递推与伴随权重由输运算法核验。把几何误差和离散误差分离后，再在第四章考察重要性场/权窗任务，第二章只解释空间表示与目标误差的因果关系，减少跨章重复。

## 后续证据边界

优先补取Buchan、Liu2022/2023及Wilson完整数值表，可以进一步明确每个算例、容限及计时范围；当前信息足以形成具体方法评述，但不支持新增逐图比较或统一性能排名。V2人工删除内容是否保留属于主代理的批注/删改台账判断；本证据文件不会自动要求恢复旧段落、表格列或题注。
