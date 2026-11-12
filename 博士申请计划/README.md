# 博士申请计划

- [当前V4 PDF](exports/周璐楠博士科研计划书_V4_定点修订_20261112.pdf)
- [唯一LaTeX正文](latex/main.tex)
- [最新修改记录](outline/V3定点学术修订记录_20261112.md)
- [图源与许可](latex/references/figure_sources.md)
- [基准图件来源与数据限制](latex/references/benchmark_sources.md)

## 构建

在`latex`目录执行`bash build.sh --check`，完成结构、引文、交叉引用和三遍XeLaTeX检查，不覆盖正式PDF。执行`bash build.sh`生成当前V4 PDF。需安装XeLaTeX及正文使用的字体。

`figure_sources`保存当前八幅图的Python、JSON、SVG及原始图像，依赖与字体约定见图源说明。`validation/benchmarks`保存固定版本公开输入包、所选测量表及提取脚本。该输入包是可追溯的研究数据，不是旧稿备份。文献证据中既有核查记录保留其证据层级，较早记录中的编号须按DOI或题名对应当前参考文献。

历史PDF、旧提纲、过程包及未使用图件已按用户要求移除，已提交内容可从Git历史恢复。
