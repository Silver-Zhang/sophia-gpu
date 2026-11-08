# 新增图形源

后端为Python/Matplotlib（保存偏好），位图仅用于预览，正文使用矢量PDF。

- `mechanisms.py`：生成`dda_index`、`voxel_gpu_cost`、`research_design`；原创教学几何/研究设计，不含仿造实验数据。中文字体为macOS Heiti，安装环境与主文档一致。
- `geometry_sdf.py`：读取`../references/shriwise2017_table1.csv`，独立重绘同一MC算例三种实现的墙钟时间。
- `plot_nudeal.py`：读取`../references/nudeal_table6.csv`，独立重绘同一3D C5G7/RTX2080Ti的角块大小扫描；64角OOM记录在CSV，不能当作零时间。

在任意目录运行相应脚本，输出路径按脚本自身位置解析。`plot_nudeal.py`的严格面板审计使用nature-figure技能`audit_panel_alignment.py`；可通过`NATURE_FIGURE_SCRIPTS`指定审计脚本目录。其余绘制依赖`matplotlib`。最终审计记录见`../qa/`，未提交版权受限原图或论文PDF。

原V4.2的图1/3/5/6/7继续使用基准文件，其旧源未出现在本仓库，不声称新增了这些图的可编辑源。旧图2/4不再入正文。
