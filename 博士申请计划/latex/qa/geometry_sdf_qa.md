# geometry_sdf 图件核查

目的：同一氢球蒙卡算例中的几何访问开销，SDF预筛选有收益，但未抹平相对解析CSG的开销。

- 数据：ref64 Table1，三种实现全部保留；绘制wall time，CSV同时保留CPU time及作者time ratio，不自行换基线。
- 统计：原表未报告重复计时离散度，未虚构误差棒。
- 输出：单图，Python matplotlib，132mm自然宽度，LaTeX按0.85linewidth放置；不是Nature投稿，因此common journal width warning不适用。
- PDF text检查最低9pt；碰撞检查0 fail/0 warn。单面板，alignment不适用。
- 源预检SVG问题已补充SVG导出后解决。PNG仅是300dpi预览；LaTeX采用矢量PDF，因此TIFF和600dpi默认建议不适用。
- 所有标签无重叠；CSG、CAD、SDF三种实现次序与原表一致；x轴分钟及零起点清楚。时间最高点和SDF点作直接数值标注，其余数值正文与CSV可读。
