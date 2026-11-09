# 图源与许可（2026-11-09）

当前成稿：31页、71文献、13式、7图、5表。开发要求/历史见根目录AGENTS.md；正式文献完整身份见main.tex，旧编号对照见citation_map_v53.csv。

## 图1：ARIES-RS

官方CAD图库：https://aries.pppl.gov/LIB/CAD/FIGURE/ARIES-RS/ 。页面明确允许下载高清图用于打印或文档，不标为CC或公有领域。图为概念设计，不是输运结果；独立CAD图未列个人绘图者/论文图号，按ARIES项目署名。

完整原件等比例并排，仅加a/b：
- Cross-Section：https://aries.pppl.gov/LIB/CAD/FIGURE/ARIES-RS/ars-9610-powercore04.jpg
- Blanket/Shield 3D Sector：https://aries.pppl.gov/LIB/CAD/FIGURE/ARIES-RS/ars-9611-blanket03.jpg

设计依据为[3] Tillack等及ARIES Team，Configuration and engineering design of the ARIES-RS tokamak power plant，Fusion Engineering and Design 38(1–2),87–113,1997，DOI https://doi.org/10.1016/S0920-3796(97)00113-0 。Crossref核对十位个人作者/卷期页，[项目报告目录](https://aries.pppl.gov/LIB/REPORT/ARIES-RS/)另署团队；不臆称CAD图是论文某图。

## 图2：Yang等

©2025 Liang Yang, Jianhui Yang, Jakov Popov, Andrew G. Buchan；[13]，Frontiers in Nuclear Engineering 4:1597165，DOI https://doi.org/10.3389/fnuen.2025.1597165 。出版社全文/PDF及Crossref元数据一致。

原件：https://www.frontiersin.org/files/Articles/1597165/xml-images/fnuen-04-1597165-g001.webp 。采用原图1(b,d)完整分图，裁取并横排，保留原标号/颜色；许可[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)，该图图题及全文未见单独第三方例外。出处、作者、许可与改编方式同时写入正式PDF的FigureSources元数据；图题仅图名及[13]。

左侧为移除圆内单元后的阶梯边界，右侧为贴合边界并保留内外区域的四边形网格。原文输运算例为DG有限元+离散纵标法；原图2为泊松方程解/误差，本计划未采用该图，不将其误差或速度称为MOC结果。

## 高清与完整性

- imshow必须interpolation=none、resample=False；默认插值曾将ARIES降为约280像素，已修复。literature_figures.py断言导出PDF内嵌像素等于输入，防止再次降采样。
- ARIES原2293×1820/2654×1826像素完整保留，成稿822/952 ppi。
- Yang官方原931×1010像素；未取得更高分辨率可用图。保留463×504/463×506分图，0.5行宽排版，成稿318/319 ppi；不插值、锐化、AI补画或冒充矢量。
- 原始资产SHA256：
  - ars-9610-powercore04.jpg：0cc53e58c5abb31908cb8d9e3ccef8f63af1eaafc2d24f2454ad55b0b12e376d
  - ars-9611-blanket03.jpg：982f32923dcfcdb946ee046cc0ce8b518308b17f6d0fa3beb69043631e59ccc1
  - yang_fig1.webp：fe36bce35a4f40fc9dee707f45f0f43d6e083d8c1d3bcf2d4aae5c6366dabc62

## 其他图与限制

DDA/八叉树/BVH、GPU扫描、CADIS/FW-CADIS及联合优化图为独立原创黑白示意；NuDEAL按作者稿表6数据绘制，CSV/脚本保留。Gaston[20]沿用旧文献并补全六位作者，DOI https://doi.org/10.1080/00295450.2021.1871995 ；出版社全文/PDF403，未重新核对图1/10与第三方例外，Crossref的CC BY-NC-ND记录版本不明确，因此不转载或描摹原图，也不另画替代图。CPU扩展结果与GPU性能明确区分。论坛自适应图与现有图重复，未采用。

两幅拼版对齐检查通过；六幅可审计图碰撞通过，Yang纯栅格图人工核对，不能宣称自动文字碰撞检查通过。Claude调用180秒超时，没有独立审核结论。当前编译/引用及版面检查见AGENTS.md，临时QA文件不保留。
