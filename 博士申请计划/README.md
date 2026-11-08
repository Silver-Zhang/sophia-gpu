# 博士申请计划 V5.1（用户批注修订）

《面向聚变堆复杂几何的体素化特征线中子输运与GPU并行加速方法研究》

正文唯一来源为[latex/main.tex](latex/main.tex)，使用XeLaTeX；不维护Word或Markdown正文副本。

|交付|路径|
|---|---|
|最终PDF|[exports/博士科研计划书_V5.pdf](exports/博士科研计划书_V5.pdf)|
|编译与完整性检查|[latex/build.sh](latex/build.sh)、[latex/qa/check_integrity.py](latex/qa/check_integrity.py)|
|图与可编辑源|`latex/figures/`、`latex/figure_sources/`|
|69项证据与核查边界|[latex/references/evidence_matrix.csv](latex/references/evidence_matrix.csv)、专项矩阵|
|审阅、编译、逐页检查|[latex/qa/final_review.md](latex/qa/final_review.md)|
|修改历史|[V4.2_to_V5_修改对照.md](V4.2_to_V5_修改对照.md)|
|研究与实验约定|[V5_核心研究问题与实验方案.md](V5_核心研究问题与实验方案.md)|

本轮依据PDF的27条高亮完成全文检查，10幅图统一为微软雅黑9pt。意见处置见[latex/qa/user_annotation_disposition_20261108.md](latex/qa/user_annotation_disposition_20261108.md)。

六章依次为动机、复杂几何与MOC现状、GPU-MOC现状、RQ1–RQ3研究方案、聚变屏蔽验证与减方差应用、博士工作安排。含69项文献、13个公式、10幅图和7张表；原67项文献与9个公式保留。旧图2/4文件仅供基准保护，不再用于正文。

在`latex/`执行`bash build.sh`：隔离旧PDF与中间文件，预检引用后真实运行三遍XeLaTeX，检查返回码及最终日志，再生成本地`main.pdf`并更新交付PDF。源与PDF的SHA256见`qa/build/build_manifest.json`。

需要Python3、XeLaTeX与ctex，以及Songti SC、Heiti SC、Times New Roman和Helvetica字体。绘图用Python/Matplotlib；新增重绘数据为原文表格事实，不含受限原图。核验脚本与图形QA记录均随分支保存。

V4.2正式基准为`90694990d1717da06eafc59f4cc25081a74f9cb5`；V5仅在`revision/rp-v5-voxel-gpu`分支修订，PR供人工审阅，不自动合并。
