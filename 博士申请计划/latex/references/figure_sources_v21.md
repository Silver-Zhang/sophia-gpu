# V2.1 图源及用途（2026-11-10）

| 新图号 | 文件 | 图源、许可及改动 | 用途 |
|---|---|---|---|
| 1 | aries_rs.pdf | ARIES官方CAD图，许可及原件像素见figure_sources_v53.md；文件未变 | 理解屏蔽工程结构，不是本研究结果 |
| 2 | v21_route.pdf | 本轮原创；v21_schematics.py | 需求到MOC/体素/多GPU的路线 |
| 3 | yang_mesh.pdf | Yang等2025原图1(b,d)，CC BY 4.0；沿用拼版、无重采样 | 几何表示比较，非MOC结果 |
| 4 | dda_index.pdf | 既有原创，mechanisms.py；文件未变 | DDA、八叉树与BVH查询对象 |
| 5 | v21_moc.pdf | 本轮原创；v21_schematics.py | 材料数据到源迭代的数值流程 |
| 6 | v21_multi.pdf | 本轮原创；v21_schematics.py | 单节点完整轨迹分解/源场复制基线 |
| 7 | v21_research.pdf | 本轮原创；v21_schematics.py | RQ1/2信息到RQ3及独立验证 |

新图不是实验或性能数据。采用既有figure_style.py，148.2 mm、白底黑线、中文微软雅黑、英文Arial、9 PDF pt；PDF由PGF/XeLaTeX输出；SVG为活文字编辑辅助，已生成在figure_sources下（沿用既有忽略规则）。不分发字体。无多面板定量图，不适用定量面板对齐门槛。四图PDF碰撞检查0 fail/0 warn并人工核对；SVG检查仅有本项目图宽不同于Nature宽度的预期提示。

新引用编号：ARIES设计依据[3]、Yang[8]；旧图源文件内的旧ref13等不是当前编号，当前见citation_map_v21.csv。原CSV和未引用旧图不删除、不当作新交付图。

后续第一章简化：原图2（v21_route.pdf）已移出正文，文件保留供追溯；原图3—7在当前PDF中顺延为图2—6。上表图号为最初重构稿图号。


第二章批注修订：删除旧DDA/八叉树/BVH图（dda_index.pdf，原文件保留），重画v21_moc.pdf。当前图1 ARIES、图2 Yang、图3多群源迭代、图4多GPU、图5研究任务。图3可编辑源为moc_iteration.py；v21_schematics.py调用新源；图宽和字体不变，PDF碰撞审计通过。该图只表示固定真空、预存轨迹及群Jacobi基线，不包含CMFD/群GS的实现分支。
