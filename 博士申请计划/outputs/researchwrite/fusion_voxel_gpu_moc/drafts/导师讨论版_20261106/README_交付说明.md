# 博士科研计划书导师讨论初稿

> 当前状态：用户Word批注修订已完整归档，生成源已按保留文本同步，Word原件未改写。**未经用户明确确认禁止重新生成Word或恢复删除内容。** 现有PDF和原两轮自审仍为首版基线，详见[用户审阅源同步说明](qa/用户审阅源同步说明.md)。下述129标题、37页等数据描述首版交付，不代表当前审阅版的排版与标题数量。

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

## 用户批注修订版本

用户后续保存的Word修改版已核验并原样归档：38条批注，136处删除、23处插入和101处格式修订标记（OOXML元素计数，不等同于独立修改次数）。批注正文、起止锚点、引用及关系完整；修订保留作者、时间和原始内容，未接受或拒绝任何修改，也未执行批注意见。

当前Word的SHA256为`3b6364646e2b0f29e785997afc0b6912685fa50ff60ef049399e9a0f2550582e`。全部批注和删改已先提取、核对并归档至[审阅归档](review_archive/3b6364646e2b/删改与批注核对.md)，随后将修订后保留的文本同步到六章源、前置源和Markdown。另保留15组未跟踪/结构差异及87个源块对照。批注尚待逐条实施。现有PDF、图形资产及原两轮自审记录仍为此前正式初稿，未重建Word。

## 复现与继续修改

现行正文源为`frontmatter.md`和`sources_ch01.md`至`sources_ch06.md`，图表与题注在章节源中显式保留。`table_sources.md`及`tables/`为派生快照。图形绘制代码为`build_figures.py`；原始格式修订仍以归档Word及XML为准。

本次工具链为Python 3.12、md-to-word 3.3.2、python-docx 1.2.0、CairoSVG 2.9.1及Codex随附LibreOffice/Poppler。使用可访问这些依赖的Python运行：

```bash
python assemble_manuscript.py  # 只更新Markdown及表格快照
python verify_review_sync.py   # 核对原件、批注、修订和源投影
```

`rebuild.py`和`finalize_docx.py`当前在任何写入前都会因用户尚未确认而停止；不得绕过`review_guard.py`。原完整导出流程及所需渲染器仍保留，只有用户确认后才可考虑重新导出，届时必须重新检查全部页面，并保证不恢复已删内容。`review_state.json`记录当前未获确认的状态及源文件哈希。源文件如有后续手工编辑，不要直接重跑Word导入覆盖它们。

`collect_metadata.py`与`refresh_missing.py`用于可选联网更新，原始Crossref响应和人工核对记录已经保存；网络失败不会被当作不存在文献或已获取全文。

## 供导师进一步确认

首先确定三方向中的主方向、主要响应和典型应用问题；确认中子—光子或停堆活化链的范围。随后落实可修改求解器及伴随接口、核数据库和算例授权、GPU型号/显存/时段、性能分析权限与实际培养学制。申请人的GPU编程和MOC实现能力仍需系统学习，硕士课题仍按在研表述。
