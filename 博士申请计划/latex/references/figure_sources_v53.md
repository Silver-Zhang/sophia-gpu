# V5.3文献图件来源与本轮修改（2026-11-09）

基准：origin/main e368285；分支：revision/rp-v5.3-literature-figures。五章结构、研究主线、13个公式及原69项文献身份保留。上一轮批注PR #3尚未合并，本轮按要求从main开始，只沿用黑白原创图和表格字号要求，不整体引入其正文重写。

## 采用图件

|成稿图/位置|原始资料与处理|许可/引用|
|---|---|---|
|图1，1.1工程需求|ARIES官方CAD图Cross-Section与Blanket/Shield 3D Sector，完整图片等比例并排，仅添加a/b标签。不是本文输运结果。|官方页面明确允许下载高清图用于打印或文档；不标为CC或公有领域。图题署名ARIES项目。设计论文新[3]。|
|图2，2.1材料界面|Yang等2025原文图1(b,d)，选取完整分图并横排，保留原(b)/(d)标号与颜色，替换原fig1。左图移除圆内单元、保留阶梯边界；右图边界节点移动后保留内外四边形区域。|作者©2025 Yang, Yang, Popov and Buchan，CC BY 4.0；图题注明原图号与排列改编。图1图题/全文未见单独第三方署名或许可例外。新[13]。|
|图3，2.2穿越方法|保留DDA/八叉树/BVH原创比较图，黑白。2.1补一处二维截面与局部细化说明。|未采用论坛图片；与已有图重复，不增加图片或论坛文献。理论沿用[14–18]等已有研究。|
|图4，3.1并行扫描|沿用现有GPU扫描、缓存与通量求和原创图，改为黑白。Gaston仅在邻近正文说明CPU跨分区扫描。|按用户追加要求，不转载Gaston图，也不新增替代示意图。Gaston原[18]现[20]沿用，不新增条目。|

## 可追溯来源

- ARIES项目CAD图库及明确文档使用说明：[官方入口](https://aries.pppl.gov/LIB/CAD/FIGURE/ARIES-RS/)。CGI下载跳转失效，静态高清原件仍可访问：
  - https://aries.pppl.gov/LIB/CAD/FIGURE/ARIES-RS/ars-9610-powercore04.jpg
  - https://aries.pppl.gov/LIB/CAD/FIGURE/ARIES-RS/ars-9611-blanket03.jpg
  - 官方未为这两幅独立CAD图列单独绘图者或论文图号，按项目与资源名称署名，不臆定它们是设计论文的某图。
- 新[3] M. S. Tillack, S. Malang, L. Waganer, X. R. Wang, D. K. Sze, L. El-Guebaly, C. P. C. Wong, J. A. Crowell, T. K. Mau, L. Bromberg, and the ARIES Team. *Configuration and engineering design of the ARIES-RS tokamak power plant*. Fusion Engineering and Design, 1997, 38(1–2):87–113. [DOI](https://doi.org/10.1016/S0920-3796(97)00113-0)。Crossref核对十位个人作者及期刊卷期页；[项目正式报告目录](https://aries.pppl.gov/LIB/REPORT/ARIES-RS/)另署ARIES Team。该论文提供设计背景，图片直接来自上述CAD图库，未从出版社论文截取图件。
- 新[13] Liang Yang, Jianhui Yang, Jakov Popov, Andrew G. Buchan. *Hybrid solvers for reactor modelling: matrix-based and matrix-free approaches on voxel-dominated meshes*. Frontiers in Nuclear Engineering, 2025, 4:1597165. [正式全文](https://www.frontiersin.org/journals/nuclear-engineering/articles/10.3389/fnuen.2025.1597165/full)、[DOI](https://doi.org/10.3389/fnuen.2025.1597165)、[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。出版社全文、PDF与Crossref的作者/题名/年份/卷/文章号一致。原图1源文件：https://www.frontiersin.org/files/Articles/1597165/xml-images/fnuen-04-1597165-g001.webp 。保留原生931×1010像素，不用放大插值冒充高清；裁取b/d各约463×504像素，按约71 mm宽排版，约165 ppi；网格与原标号须按成稿目视核对。
- 沿用[20] Derek R. Gaston, Benoit Forget, Kord S. Smith, Logan H. Harbour, Gavin K. Ridley, Guillaume G. Giudicelli. *Method of Characteristics for 3D, Full-Core Neutron Transport on Unstructured Mesh*. Nuclear Technology, 2021, 207(7):931–953. [DOI](https://doi.org/10.1080/00295450.2021.1871995)。Crossref与出版社可检索摘要元数据一致，补全六位作者。出版社全文/PDF直连403，无法重新核对用户建议的图1/图10具体画面及第三方例外；不转载。Crossref列CC BY-NC-ND 4.0（content-version unspecified），不足以确认所需原图与公开仓库用途的许可范围；不称已获得转载授权。正文保留已检索到的非结构MOC与约14亿单元/12000 CPU处理器结果，简述沿程递推与跨分区角通量依赖；不提交原图或替代图。
- Mathematica StackExchange讨论未采用，故不转载、不要求其CC内容进入仓库；局部细化已由原图3和既有自适应网格文献说明。

## 论证与边界

ARIES图对应曲面、多层材料、集管和可拆卸扇区的几何定位问题。Yang图说明保持规则单元与局部贴合边界的区别；原文输运算例为DG有限元+离散纵标法，图2为泊松方程解/误差，本轮未转载图2，也未挪用其误差和加速数字为MOC证据。Gaston研究提供CPU分布式MOC比较对象，MPI通信与GPU线程分配明确区分。

新增2项文献，总数71；按首次引用全局重排正文、图题、表格和bibitem。citation_map_v53.csv增加v53_literature列，仍保留V5.2→V5.3旧对照。原69项身份保留；除Gaston作者补全及编号外原条目不改。图件总数6→7，表格仍5张；表头/表内与表题10.5 pt，原创图黑字黑线白底，原始文献图保留原配色和字体。

## 原始资产校验

- ars-9610-powercore04.jpg: SHA256 0cc53e58c5abb31908cb8d9e3ccef8f63af1eaafc2d24f2454ad55b0b12e376d
- ars-9611-blanket03.jpg: SHA256 982f32923dcfcdb946ee046cc0ce8b518308b17f6d0fa3beb69043631e59ccc1
- yang_fig1.webp: SHA256 fe36bce35a4f40fc9dee707f45f0f43d6e083d8c1d3bcf2d4aae5c6366dabc62

## 完成检查

三遍XeLaTeX成功；71项引用、71项参考文献、13式、7图、5表，check.py无错误/警告，首次引用顺序与交叉引用通过。13式源码逐字保留；原69条文献中68条除编号外逐字保留，Gaston补全六位作者。正式PDF32页，与main基准相同；全部页面已渲染检查，重点复核印刷页1、4、5、10的图文及邻页。新增原图无额外留白页。表题/表内基准字号实测10.5 pt。四幅保留原创图只含黑白矢量颜色。

新拼版的两幅图面板对齐检查通过；新图源静态检查0失败，2提示为未生成TIFF及从共享配置读取宽度，符合本项目仅交付PDF/可编辑Python源的要求，实际宽148.2 mm。六幅含文本的图碰撞检查通过；Yang纯栅格原图无法用PDF文本碰撞审计器检查，已逐分图目视检查网格、原标号和成稿清晰度，不称自动检查通过。

按要求实际调用Claude CLI只读审阅，180秒超时，未取得完成审阅的意见；本轮未通过Claude独立审核。未把失败或不可访问原文记为已核验。临时渲染、审查日志与诊断图不提交。
