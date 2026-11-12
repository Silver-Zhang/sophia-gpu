# 当前八幅图的图源、许可与数据

对应V4正式稿，文献编号以main.tex为准。

## 图1：ARIES-RS

官方CAD图库：https://aries.pppl.gov/LIB/CAD/FIGURE/ARIES-RS/ 。页面明确允许下载高清图用于打印或文档，不标为CC或公有领域。图为概念设计，不是输运结果；独立CAD图未列个人绘图者/论文图号，按ARIES项目署名。

完整原件等比例并排，仅加a/b：
- Cross-Section：https://aries.pppl.gov/LIB/CAD/FIGURE/ARIES-RS/ars-9610-powercore04.jpg
- Blanket/Shield 3D Sector：https://aries.pppl.gov/LIB/CAD/FIGURE/ARIES-RS/ars-9611-blanket03.jpg

设计依据为[3] Tillack等及ARIES Team，Configuration and engineering design of the ARIES-RS tokamak power plant，Fusion Engineering and Design 38(1–2),87–113,1997，DOI https://doi.org/10.1016/S0920-3796(97)00113-0 。Crossref核对十位个人作者/卷期页，[项目报告目录](https://aries.pppl.gov/LIB/REPORT/ARIES-RS/)另署团队；不臆称CAD图是论文某图。

## 图2：Yang等

©2025 Liang Yang, Jianhui Yang, Jakov Popov, Andrew G. Buchan；[15]，Frontiers in Nuclear Engineering 4:1597165，DOI https://doi.org/10.3389/fnuen.2025.1597165 。出版社全文/PDF及Crossref元数据一致。

原件：https://www.frontiersin.org/files/Articles/1597165/xml-images/fnuen-04-1597165-g001.webp 。采用原图1(b,d)完整分图，裁取并横排，保留原标号/颜色；许可[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)，该图图题及全文未见单独第三方例外。出处、作者、许可与改编方式同时写入正式PDF的FigureSources元数据；图题仅图名及[15]。

左侧为移除圆内单元后的阶梯边界，右侧为贴合边界并保留内外区域的四边形网格。原文输运算例为DG有限元+离散纵标法；原图2为泊松方程解/误差，本计划未采用该图，不将其误差或速度称为MOC结果。

## 高清与完整性

- imshow必须interpolation=none、resample=False；默认插值曾将ARIES降为约280像素，已修复。literature_figures.py断言导出PDF内嵌像素等于输入，防止再次降采样。
- ARIES原2293×1820/2654×1826像素完整保留，成稿822/952 ppi。
- Yang官方原931×1010像素；未取得更高分辨率可用图。保留463×504/463×506分图，0.5行宽排版，成稿318/319 ppi；不插值、锐化、AI补画或冒充矢量。
- 原始资产SHA256：
  - ars-9610-powercore04.jpg：0cc53e58c5abb31908cb8d9e3ccef8f63af1eaafc2d24f2454ad55b0b12e376d
  - ars-9611-blanket03.jpg：982f32923dcfcdb946ee046cc0ce8b518308b17f6d0fa3beb69043631e59ccc1
  - yang_fig1.webp：fe36bce35a4f40fc9dee707f45f0f43d6e083d8c1d3bcf2d4aae5c6366dabc62


## 图3、图4及图8：原创方法示意

图3由`moc_iteration.py`绘制，表示固定真空边界、预存轨迹、群Jacobi的源迭代基线。图4由`render_legacy.py`及`legacy_scenes.json`中的fig3场景生成，表示轨迹扫描、在线生成与缓存和源区通量求和。图8由`research_plan_v21.py`生成，SVG为同名可编辑辅助源，表示第五章的三项拟研究方法及参数反馈。三者均不是实验或计算性能数据。

## 图5：NuDEAL显存与时间

来源为NuDEAL作者稿（arXiv:2607.01591v1）表6，正文参考文献[35]。`nudeal_table6.csv`保存原始数值，`plot_nudeal.py`绘图。每批方位角数2、4、8、16、32对应显存2589、2893、3499、4709、7133 MB，扫描时间5.25、5.19、5.10、5.10、5.09 s，MOC时间10.50、9.96、9.50、9.30、9.21 s。64角度同时驻留超出显存。原表没有报告误差棒。

## 图6与图7：基准几何、实验布置及泄漏谱

完整出处、许可、图号、归一化差异及数据限制见`benchmark_sources.md`。原始图像、参数和数值位于`figure_sources/benchmark_visuals/`，图件由`benchmark_visuals.py`生成。所选公开输入包和测量表位于`validation/benchmarks/`。

## 图件生成约定

原创图采用148.2 mm宽度、白底黑线、中文微软雅黑、英文Arial及9 PDF pt基准字体，不分发字体。图源依赖Matplotlib、PGF/XeLaTeX及本机字体。部分脚本使用`NATURE_FIGURE_QA_SCRIPTS`指定nature-figure的scripts目录。生成的临时检查图和日志不进入仓库。
