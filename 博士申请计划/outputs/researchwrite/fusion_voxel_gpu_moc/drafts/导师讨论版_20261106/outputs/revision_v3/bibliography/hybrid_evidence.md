# V2混合减方差证据专项

核验日期：2026-11-06。已读父目录和V2 AGENTS及阶段一结构方案；本次只写证据文件，不改人工修订后的正文或既有Word。表中访问层级是实际证据边界，未取得全文的条目不补造数值或页内评价。

## 主要核验结论

Ibrahim 2014的79.3%→97.8%表示非零计分覆盖；23.3%为非零元素数相对增加。Raffuzzi的全局比较同时给MC-only及包含WW生成的FOM，局部探测器比较才忽略短WW/RR时间。CADIS-Ω的原始迷宫例优于CADIS，但analog的汇总FOM更高。以上三个细节直接影响“重要性更准确是否更高效”的论证。

## 文献身份与证据边界

|key|文献与来源|方法及验证对象|结果定位与启示|访问层级|

|---|---|---|---|---|

|r30|[Automated Variance Reduction of Monte Carlo Shielding Calculations Using the Discrete Ordinates Adjoint Function](https://inl.elsevierpure.com/en/publications/automated-variance-reduction-of-monte-carlo-shielding-calculation/)；1998，Nuclear Science and Engineering|S_N伴随构造CADIS一致源偏倚与权窗；反应堆压力容器空腔剂量学|官方Abstract；成熟方法的增量应落在重要性近似与执行代价|机构出版记录与摘要|

|r31|[FW-CADIS Method for Global and Regional Variance Reduction of Monte Carlo Radiation Transport Calculations](https://web.ornl.gov/~peplowde/p068.pdf)；2014，Nuclear Science and Engineering|先正向预测响应，再按目标构造加权伴随源和一致偏倚；剂量与能谱分布等原文示例|正式版pp40—44，§II.A、II.B、III；Eqs(9)—(12),(20),(23),(25)—(28),TableII；目标定义决定伴随源；平均权目标与程序下限不是同一个量|既有正式全文，本轮重新定位公式|

|r32|[Review of Hybrid Methods for Deep-Penetration Neutron Transport](https://escholarship.org/content/qt91c500xf/qt91c500xf.pdf)；2019，Nuclear Science and Engineering|深穿透混合方法综述；多类方法文献归纳|Abstract及原始论文引用链；用于技术谱系，直接性能引用返回原论文|开放作者稿入口与目录|

|r33|[Novel hybrid Monte Carlo/deterministic technique for shutdown dose rate analyses of fusion energy systems](https://inl.elsevierpure.com/en/publications/novel-hybrid-monte-carlodeterministic-technique-for-shutdown-dose/)；2014，Fusion Engineering and Design|MS-CADIS将最终停堆剂量重要性传回中子阶段；简化停堆剂量示例|官方Abstract；跨步骤响应与单步通量目标不同|机构摘要与出版记录|

|r34|[Local angular adaptivity CADIS hybrid variance reduction method for monte carlo radiation transport calculations](https://www.sciencedirect.com/science/article/pii/S0306454925002026)；2025，Annals of Nuclear Energy|LAA-CADIS局部角度自适应构造重要性；摘要中的强方向性屏蔽测试|Abstract/Highlights；角向适应已有直接先例，新增工作应给出不同误差机制或预算选择|出版社摘要|

|r35|[ITER Neutronics Modeling Using Hybrid Monte Carlo/Deterministic and CAD-Based Monte Carlo Methods](https://impact.ornl.gov/en/publications/iter-neutronics-modeling-using-hybrid-monte-carlo-deterministic-a/)；2011，Nuclear Technology|CADIS/FW-CADIS与CAD蒙卡联合应用；线圈核热、屏蔽外剂量、全域通量|Abstract；作为混合方法工程成熟度证据，本文件避免重复工程结果|官方机构记录/出版社摘要|

|r36|[Assessment of fusion facility dose rate map using mesh adaptivity enhancements of hybrid Monte Carlo/deterministic techniques](https://web.ornl.gov/~5pe/p081.pdf)；2014，Fusion Engineering and Design|材料宏观化、确定论细化、WW空间及能群粗化；ITER瞬发剂量网格|正式版p1878 §3.1；p1879结论；非零覆盖不同于RSD达标；两网格解耦与适应已有明确先例|正式全文，缓存有效PDF和定位文本|

|r37|[基于自动网格划分与权窗平滑的自适应减方差方法](https://html.rhhz.net/hejishu/html/2016/9/2016090502.htm)；2016，核技术|CAD转换、自动网格生成与WW平滑；CLEAR堆顶盖|中文正式全文HTML摘要及方法段；自动网格和平滑已有国内先例|中文期刊全文HTML|

|r38|[NECP-MCX: A hybrid Monte-Carlo-Deterministic particle-transport code for the simulation of deep-penetration problems](https://www.sciencedirect.com/science/article/pii/S0306454920306745)；2021，Annals of Nuclear Energy|NECP-MCX集成NECP-Hydra正/伴随与CADIS/FW-CADIS；Winfrith铁、HBR-2等|Abstract、Introduction、Numerical results公开片段；统一框架已有；2021引言的OpenMC旧状态需用现行文档更新|出版社摘要、引言与分节片段|

|r39|[High-efficiency simulation of VENUS-3 neutron-shielding problem with an automatic and enhanced hybrid Monte-Carlo-Deterministic method](https://www.sciencedirect.com/science/article/pii/S0306454920307350)；2021，Annals of Nuclear Energy|贡献理论指导笛卡儿/嵌套权窗网格粗化；VENUS-3|Abstract；§3公开片段；贡献粗化与嵌套空间组织已有直接先例|出版社摘要与片段|

|r40|[MAVRIC: Monaco with Automated Variance Reduction using Importance Calculations](https://scale-manual.ornl.gov/6.3.1/MAVRIC.html)；2026，ORNL|Denovo正/伴随—CADIS偏倚及WW—Monaco；官方方法与运行流程|SCALE6.3.1 §4.1.2 Eqs(4.1.1)—(4.1.4)及Denovo节；近似重要性可有效；要求源偏倚与WW一致；当前Monaco可MG或CE|固定版本官方手册|

|r41|[OpenMC User Guide: Variance Reduction](https://docs.openmc.org/en/stable/usersguide/variance_reduction.html)；2026，稳定版在线手册，访问日期2026-11-06|MC迭代MAGIC；内置多群RR正向后伴随生成FW-CADIS；官方流程/接口|UserGuide §17.1—17.3；Methods §14.2—14.4；同几何减轻转换负担，MGXS及源区细分仍需配置；WW网格不得再细分源区|当前官方稳定版文档|

|r42|[Application of the Random Ray Method to Variance Reduction in Radiation Shielding Problems](https://www.tandfonline.com/doi/abs/10.1080/00295639.2025.2458958)；2026，Nuclear Science and Engineering|SCONE RR生成前向归一化WW或CADIS/FW-CADIS，与MAGIC比较；2m混凝土整体屏蔽；二维水中源—探测器|作者稿pp11—16 §III/III.A.2 Eq(9),TableI；pp26—29 §III.B TablesVII,VIII；pp30—31结论；提高截面/源阶/散射保真度在这两例未改善VR；整体屏蔽结论不直接外推有显著流束通道|既有完整作者稿，本轮重新读表与公式；出版社正式卷页核对|

|r43|[Automated Hybrid Variance Reduction on Advanced Architectures in the Shift Monte Carlo Code](https://impact.ornl.gov/en/publications/automated-hybrid-variance-reduction-on-advanced-architectures-in-/)；2026，Nuclear Science and Engineering|Shift CPU历史型静态/动态线程和GPU事件型WW输运；Frontier上的两个固定源混合问题|Abstract；正式NSE200(2):444—470，online2025，卷年2026；GPU执行权窗已实现；每GCD吞吐不能当整卡或全前处理加速|ORNL官方出版记录与出版社摘要|

|r44|[FW/CADIS-Ω: An angle-informed hybrid method for deep-penetration radiation transport](https://arxiv.org/abs/1612.00793)；2016，arXiv预印本；相关会议稿PHYSOR 2016|CADIS-Ω以正向角通量加权伴随角通量，生成替代标量重要性；10MeV源、混凝土迷宫、NaI探测器|预印本§4.1 Eq(5),§5/TableI(pp8/13)，§5末p14；方向信息可进入空间—能量标量WW；评价还要看能谱误差均匀性与预计算成本|完整作者稿与arXiv身份页|

|r47|[Development of multilevel mesh adaptivity for global variance reduction in Monte Carlo code cosRMC](https://www.sciencedirect.com/science/article/pii/S0920379624002254)；2024，Fusion Engineering and Design|八叉树材料驱动网格、邻接关系及响应矩阵WW；并行内存优化；CFETR22.5°扇区|Abstract、Introduction、CFETR分节片段；材料自适应+响应矩阵权窗+聚变应用已有先例|出版社摘要、引言及节片段|

|new_magic2011|[Comparison of global variance reduction techniques for Monte Carlo radiation transport simulations of ITER](https://www.sciencedirect.com/science/article/pii/S0920379611000718)；2011，Fusion Engineering and Design|MAGIC以MC已有粒子分布迭代生成权窗/重要性；比较几种全局VR；ITER Alite.004|Abstract；Estimation of GVR Efficiency；Conclusion；为MAGIC提供原始论文证据；方法排序随目标和模型变化|出版社摘要/引言/分节公开片段|

|new_longhistory2013|[Improving computational efficiency of Monte-Carlo simulations with variance reduction](https://arxiv.org/abs/1309.6166)；2013，M&C 2013; author preprint arXiv:1309.6166|遇到大权重偏离时动态调整该历史WW，缓解长历史；简化测试与ITER A-lite|作者稿p9 TableII；p11—12总结；p8—9 FOM/pFOM定义；单机方差效率下降可被并行等待减少抵消；目标需包含执行尾部成本|本轮arXiv原始PDF全文获取并解析|

|new_theta2026|[Developing the THETA transport code with the linear source enhanced random ray method for high-fidelity radiation shielding simulation](https://www.sciencedirect.com/science/article/pii/S0010465526002705)；2026，Computer Physics Communications|THETA采用线性源RR以粗空间区捕捉陡通量梯度；Kobayashi一群固定源、ASPIS铁88等三种屏蔽场景|Abstract；Introduction；§4公开片段；提高空间源阶是局部细网格的替代变量；高精度RR解与更好VR仍需分开检验|出版社摘要/引言/分节片段|

## Raffuzzi的指标及时间口径

FOM=1/(t·平均相对方差)，t以min计。全局评价先对各目标的相对方差取平均，不能用“平均RSD的平方”替代。作者稿§III.A.2 Table I以20次独立运行/权窗生成的均值±一次标准差报告；未计分网格在该FOM中被赋100%标准差，属于本篇特定约定。

全局原型为2MeV源、2m混凝土屏蔽；Intel Xeon Platinum8276单节点56个OpenMP核。ECCO33多群，权窗20cm、RR源区5cm、MC tally10cm。原Table I：

|方法|WW生成 min|MC运行 min|MC-only FOM|含WW时间 FOM|

|---|---|---|---|---|

|Analog|—|99.0±2.9|0.0191±0.00056|—|

|MAGIC|127.9±18.6|108.4±6.8|0.80±0.30|0.37±0.14|

|RR-forward-flux|6.6±0.06|99.5±16.3|0.52±0.31|0.48±0.29|

|RR-FW-CADIS|13.2±0.12|102.4±4.2|1.08±0.14|0.96±0.12|

对照源见[正式出版入口](https://doi.org/10.1080/00295639.2025.2458958)及本地作者稿§III.A.2/Table I（作者稿p16）。此表可以支持“预计算成本会改变排序与收益”的实际比较，仍不等同包含CAD转换、所有MGXS制备和设计人员配置时间的完整工程周期。

局部模型为100cm×100cm水屏蔽，2MeV源与对角探测器，热/快分界0.0625eV；CASMO12，权窗1cm、RR源区0.5cm。Table VII的RR约2min未计入，Table VIII的WW约2—4min未计入。Table VII仅对照analog、CADIS-NJOY与CADIS-MC截面，局部例没有MAGIC对照；全局例才包含MAGIC。其原始数值见JSON quantitative_detail。结论限于无显著流束通道的两类整体屏蔽模型。

## Shift执行证据

[ORNL正式记录](https://impact.ornl.gov/en/publications/automated-hybrid-variance-reduction-on-advanced-architectures-in-/)和摘要确认CPU历史型静态/动态线程、GPU事件型权窗输运三路线。Frontier两例在20节点内小于2min，动态线程扩展较静态最高改善20%；MI250X每个GCD吞吐量为最佳CPU的9—11倍。这些是输运执行层证据；全文未取得，不把它们改写为整卡相对单核速度或包含所有自动减方差前处理的端到端加速。正式著录为NSE 200(2):444—470(2026)，online2025。

## 三项新增文献的用途

new_magic2011提供MAGIC的原始文献；new_longhistory2013解释大权重偏离导致的过度分裂、并行等待及权窗动态调整；new_theta2026为高阶源表示替代过细空间网格提供近期屏蔽证据。三者分别回答“自动基线是什么”“为什么FOM与并行周期会冲突”“预计算精度是否只能靠细化”，无需扩张为三项额外博士任务。

## CADIS公式物理检查

### physical_response

$$L\psi=q,\ L^\dagger\psi^\dagger=d,\ R=\langle d,\psi\rangle=\langle q,\psi^\dagger\rangle$$

连续内积含空间/能量/角度，边界项配对消失；离散需含体积与求积权的转置。 来源：r31 §II.A Eqs(4)—(9)。

### normalized_source_CADIS

$$\int p(x)dx=1,\ C=\int p(x)I(x)dx,\ \widehat p=pI/C,\ w_{birth}=p/\widehat p=C/I$$

将源强Q与概率密度p分开。若q=Qp且I为精确全相空间伴随，则R=QC；近似I时C只作抽样归一化，不等同真实R。 来源：r31 Eqs(10)—(12)，由归一化定义重写。

### weight_windows

$$w_{target}(x)=C/I(x)$$

一致的出生权落在对应权窗附近。target、lower、upper及生存权不同，程序宽度参数与单位归一化由接口规定；固定窗宽常数不应自行发明。 来源：r31 §III Eq(28)后；r40 §4.1.2。

### scalar_vs_angular

$$I(r,E)=\frac1{4\pi}\int\psi^\dagger(r,E,\Omega)d\Omega\quad(\text{isotropic source})$$

一般源方向分布a(Ω|r,E)应采用其加权伴随平均；以角积分标量代替角平均时常数在C与I比值中抵消，但物理R恒等式必须统一角测度。标量WW仍丢失方向区分能力。 来源：r31完整角相空间理论与§III标量实现；r44 §4.1。

### FW_multiresponse

$$d_{FW}=\sum_i\beta_i d_i/\widetilde R_i$$

对应预先指定的无量纲目标Σβ_i R_i/Rtilde_i，β_i为优先级；Rtilde_i来自正向估计且需非零处理。不同能谱/空间/剂量目标应使用相应响应函数，不能把逆标量通量用于所有任务。 来源：r31 §II.B.1/II.B.2 Eqs(20),(23),(25),(26),TableII；多目标线性组合为上述定义的线性推广。

### CADIS_Omega

$$I_\Omega=\frac{\int\psi\psi^\dagger d\Omega}{\int\psi d\Omega}$$

利用前向角通量加权的替代标量重要性；不是直接输出角度权窗，零分母及支持需处理。 来源：r44 §4.1 Eq(5)。

### unbiasedness_vs_efficiency

$$\widehat p>0\text{ where }p>0;\quad w=p/\widehat p$$

近似I本身不自动使MC均值有偏；支持遗漏、错误权重和不守恒截断会改变期望。无偏不保证有限或易估计的方差，更不保证最佳FOM。 来源：r41 Methods §14.4；r31一致偏倚理论，效率判断为方法推论。

## 正文使用建议

第四章主讲伴随驱动的一致偏倚、权窗执行与统计成本；第五章只补工程对象与实际响应，不复述公式。研究问题可围绕贡献路径是否被保留、WW是否可执行、完整达标周期是否缩短展开。细化、粗化、平滑、角向处理和GPU执行各有直接先例；创新应定位于具体误差机制或预算下的可验证选择。

## 未决项与缓存

LAA-CADIS、NECP-MCX逐例性能、cosRMC的53.3%效率计时定义和Shift完整模型设置尚待全文。new_theta2026当前依据出版社摘要和节片段；其量化性能是RR求解相对平源表示的比较，未验证由此生成权窗后的MC效率。原始PDF和全文TXT只保存在被Git忽略的hybrid_sources；retrieval_log.json保留版本来源、哈希和读取状态。
