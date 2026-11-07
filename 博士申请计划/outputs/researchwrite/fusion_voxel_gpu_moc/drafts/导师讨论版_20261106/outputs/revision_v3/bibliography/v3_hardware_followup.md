# V3：批注164硬件条件增量核查

核查日期：2026-11-07。仅新增本报告、JSON和获取日志，未改 V2、原 `gpu_evidence.json` 或正文。

本轮没有取得三项正式论文缺失的确切 GPU 商品型号和 CPU 型号，仍保留空值。新增可用事实是 ANT-MOC 的作者单位明确将 SC23 成果关联到“东方”超算及 16000 个国产 DCU；另取得 STREAM 作者 2025 博士论文全文，反而更清楚地证明不同版本条件不能互填。

| 文献 | 新增实际获取与定位 | 可确认范围 | 仍缺内容 |
|---|---|---|---|
| Song 2026，DOI 10.1016/j.pnucene.2025.106109 | Crossref VOR TDM链接实取 HTTP200 XML；仅1869字节 coredata，无正文；OpenAlex仅出版社位置，无PDF | 元数据为2026年2月；既有少群/单GPU/单线程CPU比较边界保持 | 正式实验GPU/CPU型号、精度、完整计时范围 |
| ANT-MOC SC23，DOI 10.1145/3581784.3607063 | SC23摘要、CNIC两份官方报道实读；ACM PDF/full HTML均403 | SC23摘要1000亿轨迹、16000设备、70.69%/89.38%；作者单位补足DCU类别及“东方”系统名 | 商用型号、节点CPU、强弱扩展起点与计时表 |
| STREAM3D-GPU 2026，DOI 10.1016/j.cpc.2025.109952 | TDM HTTP200但仅1893字节 coredata；官方出版目录只链DOI；作者博士论文全文另取 | 正式结果仍为128核参考、8/16卡MOC/DD求解22.1/40.5倍；学位论文条件独立记录 | 期刊正式硬件表及确切型号 |

ANT-MOC 的有限补充可直接用作者单位原始报道支撑：2023年7月7日正文第一篇成果段明确“16000个DCU”，文末相关成果[1]为同题SC23论文；12月20日会议报道的 ANT-MOC 段明确“东方”超算及16000个异构加速器，文末[1]再次列同题论文。两处都没有产品型号，不能由系统名推导 MI60/MI50。[CNIC 7月报道](https://cnic.cas.cn/kxyj/kyjz/202307/t20230707_6807109.html)、[CNIC 12月报道](https://cnic.cas.cn/gzdt/202312/t20231220_6924039.html)、[SC23官方摘要](https://sc23.supercomputing.org/proceedings/tech_paper/tech_paper_pages/pap300.html)。

## 新取得的 STREAM 学位论文：用于版本判别

作者实验室现行 Alumni 页面中，Doctoral Degree / Dr. Siarhei Dzianisau / Doctor Thesis 链接到公开 Drive。已下载完整博士论文 *Optimization of a 3D neutron transport code STREAM for highly parallel execution using Graphics Processing Units*（UNIST，2025年8月），不是2026 CPC正式论文。[官方入口](https://reactorcore.unist.ac.kr/reactorcore/alumni.do)、[作者公开PDF](https://drive.google.com/file/d/1hNlsf8ZFzX-zIOAU5rNnEhGHClHhKK9_/view)。

- 印刷第10页 Table1（PDF第25页，已渲染实看）：每GPU节点2×AMD EPYC7543 32核、8×NVIDIA RTX A5000 24GB、2048GB DDR4 ECC。
- 印刷第31页 §4.1.2及Table2（PDF第46页，已渲染实看）：8个CPU节点、共256核；CPU名称写 Gold4262。下一页Fig15题注（PDF第47页，已渲染实看）却写 Gold6242。原文内部矛盾完整保留，不代作者默改。
- 印刷第31—32页：OPR1000四分之一堆芯75组件，30燃耗点；65轴向平面、72中子群、8个CMFD群、48方位角、6极角、0.05cm射线间距。CPU与GPU编译器、CPU剩余工作量不同。
- 印刷第32—34页Fig15/17/18：CPU总1517min、MOC850min；8卡总1406min、MOC99min（列8.61倍）；16卡总751min、MOC55min（列15.44倍）。文中计时配置包含降低燃耗计算精度的版本。模块与总程序计时明确不同。

这些256核、8.61/15.44倍条件与期刊摘要128核、22.1/40.5倍不一致，因此取得学位全文仍不能证明期刊用了同一 A5000/EPYC 硬件。学位论文仅作为证据归档，不要求新增正文和书目，也不把其型号与期刊倍率绑定。

## 获取层级与提交边界

Crossref/OpenAlex响应、出版社TDM响应和原始全文均有本地缓存；全部放在 `v3_sources/` 并由局部 `.gitignore` 排除。仅提交本事实归纳、JSON及 `v3_sources/acquisition_log.md`。TDM根节点虽叫“full-text-retrieval-response”，实际没有正文；OpenAlex的OA标志也不能代替ACM全文成功获取。JSON逐项记录URL、位置、访问层级和未决内容。本轮已按有限时间收敛，不再扩搜。
