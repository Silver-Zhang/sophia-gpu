# 博士科研计划书 V2（导师讨论稿）

基准提交：`80535d8785e6d8466b00593f58fefc7c98f27cc0`。独立分支：`revision/rp-annotations-20261106`。正式执行依据为用户本轮完整Prompt及其澄清消息；临时V2提示词附件未上传，不作为缺失依赖。

## 阅读与交付

- [可编辑Word](exports/博士科研计划书_V2.docx)
- [PDF，30页](exports/博士科研计划书_V2.pdf)
- [完整Markdown正文](exports/博士科研计划书_V2_完整正文.md)
- [编译用Markdown](exports/manuscript_v2.md)及[排版规范](exports/format.txt)
- [BibTeX，61项](bibliography/references_v2.bib)、[逐项文献核验清单](bibliography/文献核验清单.csv)
- [六图SVG/PNG/PDF及清单](figures/figure_manifest.json)、[六表Markdown/CSV/JSON源](tables/definitions.json)
- [38条批注处理结果](planning/批注处理台账.md)：36条完成，164与175因证据字段不足部分完成，逐项原文、批注及处理见JSON/CSV。
- [章节合并与迁移完成记录](planning/章节合并与内容迁移记录.md)
- [人工删除/插入核对](qa/原人工删除内容核对报告.md)
- [独立数值与证据审查](qa/独立学术审查_数值与证据.md)、[独立论证及批注审查](qa/独立学术审查_论证与批注.md)、[修正闭环](qa/学术审查修正闭环.md)
- [独立逐页排版审查](qa/独立逐页排版审查报告.md)、[机器结构核验](qa/结构与内容核验.json)

## 修订结果与证据范围

六章分别承担需求与总体问题、复杂几何及空间离散、GPU确定论、混合减方差、聚变应用验证、三个候选方向。原2.3—2.5、3.3—3.4、4.3—4.6、5.2、5.3—5.4及第六部分均依批注重组。正文为六个一级、十八个二级标题；无三级及更细章节。原摘要、关键词、旧第六章标题、旧6.1综述、表2平台列及Zhou行没有恢复。

文献库包含原47项及14项新增研究。补充目标导向DG/残差、跨界映射、Balakovo、GPU固定源与瞬态、MAGIC/长历史、随机射线线性源、PHITS材料验证及OpenSn。核验区分全文、作者稿、出版社摘要/节选、官方文档与源码；不能把61条记录核对称为61篇全文精读。OpenSn的2026期刊论文与2026-11-06固定SHA源码分开：当前源码存在可追踪GPU伴随组合路径，本轮没有编译、GPU执行或组合回归通过证据。部分Song、STREAM正式版及ANT-MOC硬件字段仍不足，不用其他版本型号替代。

六幅图为原创物理/算法示意，没有虚构实验数据；源文件保留可编辑文字和形状。六表在Word中为原生可编辑表格。九个展示公式与行内公式为原生OMML。引文、参考文献和目录具有可点击链接；目录页码由渲染后的真实位置回填。

## 原件保护

本目录的`authorization.json`仅登记新V2生成授权。父目录`review_state.json`仍为false。原始批注Word、旧PDF、全部审计档案及原源稿共54个保护文件，哈希均保持不变。136个删除、23个插入、101个格式修订仍在原Word/XML完整保留。V2是新建的讨论稿，未在原件中接受修订、清除批注或覆盖保存。

## 可复现生成

本次环境为macOS、Python 3.12、`md-to-word-docx 3.3.2`、LibreOffice及项目现有字体配置。需要Songti SC、Heiti SC、Times New Roman和STIX Two Math；SVG另用PingFang SC。SVG/PDF转换需Cairo。Python依赖见`requirements.txt`，Word渲染器使用documents技能的`render_docx.py`，可由`DOCX_RENDERER`环境变量指定。PDF与PNG分页受LibreOffice及字体版本影响；重新生成后必须重新做视觉检查。

在本目录运行：

```bash
python scripts/rebuild_v2.py
```

生成链：已核证据→BibTeX→表格源→SVG/PNG/PDF图→显式V2源组装→保护检查→md-to-word→字体/公式/目录修补→PDF与逐页PNG→真实页码回填→完整Markdown→结构核验。不会从旧稿补入任何内容，不会写父目录Word/PDF或自动合并分支。文献下载和官方源码缓存受局部`.gitignore`保护，未收入Git；重建正文与图表不需要网络或这些缓存。

## 需导师确定的事项

1. 三个候选方向中最终博士课题的主线及前两者与耦合应用的工作边界。
2. 可修改求解器、GPU型号/数量/显存、核数据库、FNS输入和工程子结构的获取条件。
3. 首批重点响应、精度要求及实验/工程对照对象。计划书没有预设未经试验的最优网格阈值或收益。
