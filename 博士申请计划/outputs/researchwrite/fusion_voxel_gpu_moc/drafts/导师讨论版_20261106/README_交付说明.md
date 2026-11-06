# 博士科研计划书导师讨论初稿

日期：2026年11月6日。工作分支：`research/rp-hybrid-literature-draft-20261106`。本版按本目录00—04文件完成六章正式正文，保留全部129个一级至三级标题，其中97个三级小节；保留用户已有研究背景和技术论据，补充文献评述、研究判断、三条候选方向的路线和条件。

## 供导师阅读

- [可编辑Word](outputs/博士研究设想_导师讨论初稿.docx)
- [PDF](outputs/博士研究设想_导师讨论初稿.pdf)
- [完整Markdown正文及编号参考文献](outputs/博士研究设想_完整正文.md)

正文采用宋体风格中文字体Songti SC，标题Heiti SC，西文Times New Roman；A4、页眉页码、可点击目录及参考链接。共37页，其中封面摘要1页、目录1页、六章正文31页、参考文献4页。篇幅根据完整97个三级小节和图表确定，没有为了满足建议页数删节。8个编号公式及行内数学均为原生OMML，共29个数学对象；6张比较表为Word原生可编辑表格。

## 文献与图表

47项文献/官方资料，包括原43项索引及新增CADIS-Ω原始预印本、NEA SINBAD官方说明、CFETR线圈屏蔽研究和cosRMC多层自适应权窗研究。按正文首次出现重新编号，候选身份与最终编号映射见[bibliography/citation_order.json](bibliography/citation_order.json)。

- [BibTeX](bibliography/references.bib)
- [逐条证据与访问层级矩阵](bibliography/evidence_matrix.csv)
- [混合方法原文核验札记](bibliography/hybrid_evidence_notes.md)
- [六图SVG、300 dpi以上PNG、单图PDF及清单](figures/figure_manifest.json)
- [六表Markdown与CSV源](table_sources.md)

6图全部由`build_figures.py`原创生成，无实验数据曲线；SVG保留可编辑文字、形状和连接线。图中中文使用PingFang SC（系统可回退Noto Sans CJK SC）。图表来源及适用条件已写入正文，SVG审查记录见`qa/figure_audits.json`。

证据矩阵区分元数据、摘要、公开节选、作者稿和全文阅读。47项不意味着47篇全文精读；两篇国内博士论文尚未取得全文，部分近期GPU及角度减方差工作只据出版社摘要/节选使用。未取得的硬件细节没有补造。Zhou与CADIS-Ω保留预印本身份；Raffuzzi、Evans按正式2026卷年著录，在线2025信息保存在原始记录。未使用付费盗版来源，也未联系作者。

## 两轮审查

1. [独立学术审查](qa/学术审查报告.md)：核对物理、数值、创新先例、证据和资源条件；修订后无未关闭P0/P1，约8.5/10。
2. [独立形式审查](qa/独立形式审查.md)：对最终PDF全部页面逐页目视，结合OOXML和引用检查。结构自动结果见[package_checks.json](qa/package_checks.json)，最终逐页PNG保存在`qa/render_final/`。

主要修改和用户段落迁移见[修改对照](qa/修改对照.md)。Ibrahim 2014的23.3%已据原文改成“非零计分网格数量相对增加”，与统计达标覆盖和端到端加速区别。原00—04文件及此前`exports/`定稿均未覆盖。

## 复现与继续修改

编辑`sources_ch01.md`至`sources_ch06.md`、`table_sources.md`、`build_figures.py`。导出源为`outputs/manuscript.md`，可读Markdown从同一源与实际Word书目生成；不要只改生成文件而遗漏源。

本次工具链为Python 3.12、md-to-word 3.3.2、python-docx 1.2.0、CairoSVG 2.9.1及Codex随附LibreOffice/Poppler。使用可访问这些依赖的Python运行：

```bash
python rebuild.py
```

`rebuild.py`不进行联网检索，使用已归档元数据；按“图表→正文组装→BibTeX→安装版md-to-word导出→OOXML修复→Word渲染→目录实页回填→结构校验”执行。`DOCX_RENDERER`可指定文档技能的`render_docx.py`。`qa/fonts.conf`适配本机macOS字体与随附LibreOffice，迁移环境应提供对应字体并调整字体目录。修改版式后需要重新检查全部渲染页；目录为已物化的可编辑、可点击目录，页码由重建脚本按实际PDF更新。

`collect_metadata.py`与`refresh_missing.py`用于可选联网更新，原始Crossref响应和人工核对记录已经保存；网络失败不会被当作不存在文献或已获取全文。

## 供导师进一步确认

首先确定三方向中的主方向、主要响应和典型应用问题；确认中子—光子或停堆活化链的范围。随后落实可修改求解器及伴随接口、核数据库和算例授权、GPU型号/显存/时段、性能分析权限与实际培养学制。申请人的GPU编程和MOC实现能力仍需系统学习，硕士课题仍按在研表述。
