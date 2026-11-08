# V5.1 图形源与统一字体

所有正文图使用Python/Matplotlib，Microsoft YaHei Regular，9 PDF pt，最终图宽148.2mm。主文统一按0.95倍行宽放置，防止各图缩放后字号不同。

- `figure_style.py`：统一字体和最终输出。默认读取本机Office附带的`msyh.ttc`，其他环境可设置`MICROSOFT_YAHEI_FONT`指向合法安装的微软雅黑。字体文件不随仓库分发。
- `render_legacy.py`＋`legacy_scenes.json`：重建原图1/3/5/6/7。图形路径保留，文字统一重排，可编辑场景JSON。下标数字使用同字体9pt并下移基线，不引入缺字符号或其他字体。
- `mechanisms.py`：DDA/八叉树/BVH、体素/GPU成本关系、实验设计3幅机制图。
- `geometry_sdf.py`：读取`../references/shriwise2017_table1.csv`重绘同研究3种实现的墙钟时间。
- `plot_nudeal.py`：读取`../references/nudeal_table6.csv`重绘角度分块显存/时间。64角OOM保留在数据源。面板审计可通过`NATURE_FIGURE_SCRIPTS`指定nature-figure审计目录。

运行各脚本即可生成`../figures/*.pdf`及本目录的可编辑SVG与PNG预览。字号、字体、碰撞和成稿缩放核查见`../qa/font_revision/`。除5幅旧图重建后的可编辑场景外，所有新增数值图仍以CSV为唯一数据来源。
