# 博士科研计划书历史归档

本目录按版本和时间顺序保存此前的研究计划书正文、PDF、图源、参考数据及相关项目说明。归档文件用于追溯和参考；当前重构依据为 `../outline/博士科研计划书_重构提纲_V2.1.md`，后续正式正文以 `博士申请计划/latex/` 为工作区。

| 顺序 | 归档版本 | 来源提交 | 内容与定位 |
|---|---|---|---|
| V4.2 | [versions/01-V4.2](./versions/01-V4.2/) | [`9069499`](https://github.com/Silver-Zhang/sophia-gpu/commit/90694990d1717da06eafc59f4cc25081a74f9cb5) | 较早的 LaTeX 基线；保留当时的正文、图文件、项目说明和 LJC 参考资料。 |
  - 归档文件数：12；源树：`e950190f125388608ea70ca65f13f1af0313033b`。
| V5.2 | [versions/02-V5.2](./versions/02-V5.2/) | [`2be6e3a`](https://github.com/Silver-Zhang/sophia-gpu/commit/2be6e3a72e062e53941b43bb25a154c1fd6e7f4c) | V5.2 交付版本；保留 PDF、LaTeX、图源、图文件和文献依据。 |
  - 归档文件数：27；源树：`2caf53c275356b35d161f09b78d014816be50d99`。
| V5.3-depth | [versions/03-V5.3-depth-consolidation-2026-11-08](./versions/03-V5.3-depth-consolidation-2026-11-08/) | [`e368285`](https://github.com/Silver-Zhang/sophia-gpu/commit/e36828524536c6c0b1edf1882abeb8d4cc1d9e95) | V5.3 五章整合与精度—成本论证深化版本。 |
  - 归档文件数：23；源树：`2dcc1ee71e2ec115cdb4759b41a3dabe4819e21f`。
| V5.3-final | [versions/04-V5.3-final-2026-11-09](./versions/04-V5.3-final-2026-11-09/) | [`c3cc6e0`](https://github.com/Silver-Zhang/sophia-gpu/commit/c3cc6e0c4048080892c00f4e9c14594066041a55) | main 当前正式 V5.3 基线，含正式 PDF、LaTeX、图源、参考数据和许可记录。 |
  - 归档文件数：29；源树：`7fd205cdbd0f1ff7dde4ae8f20adcd7bdfb5d1d6`。
| V5.3-annotations | [versions/05-V5.3-annotations-2026-11-09](./versions/05-V5.3-annotations-2026-11-09/) | [`f2c3dff`](https://github.com/Silver-Zhang/sophia-gpu/commit/f2c3dff6b760a6630198a0dac6c833af58e3a705) | 原开放 PR #3 的独有批注修订快照；保留其 PDF、LaTeX、图源、批注修改记录及项目说明。 |
  - 归档文件数：24；源树：`3d6a1a7d123a8e4ae48f03a364079b8d2e800ace`。

## 归档说明

- 归档通过复用原 Git blob 保存文件内容，PDF、图片和 DOCX 等二进制文件不经过文本转换。
- `05-V5.3-annotations-2026-11-09` 对应原 PR #3 的 head commit `f2c3dff6b760a6630198a0dac6c833af58e3a705`，其中包括独有的批注修订正文和 `批注修改记录_20261109.md`。
- Git 历史仍保留各版本提交关系；本目录提供按版本浏览的文件快照。
- 当前 V2.1 提纲不复制到历史版本目录，作为 develop 当前工作的唯一结构依据。
- 归档不代表其中所有文献、数值或方法表述已经重新核验；后续重写时应按当前提纲重新审查来源和适用性。

## Pull Request 历史

- PR #1（V5.2）、PR #2（V5.3 五章整合）和 PR #4（V5.3 图表及封面修订）已经合并，其内容由相应版本快照及 Git 历史保留。
- PR #3（V5.3 批注修订）尚未合并；其独有快照已归档，之后关闭该 PR，不将其旧正文并入新的重构正文。
