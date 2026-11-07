# V3批注175限定补查 GPU固定源与离散伴随

核查日期：2026-11-07。仅写V3证据；V2源文件、书目和QA均只读。已查既有STRAUM、Denovo、ALPHA及OpenSn固定SHA证据，本次保留两项有直接信息增量的原始研究，不扩张整章。

## 可进入3.2的新增事实

**Pryer的2026预印本提供了GPU可微扫掠与离散伴随动作的数值检验。** 作者把相同依赖图上的定源DG通道组织为GPU张量扫掠，并在材料阴影问题中求响应的反向导数，以独立装配的块转置系统核查。与已有OpenSn源码组合路径相比，这里增加了论文中的数值核验；证据对象仍是固定符号分支上的扫掠与响应导数。它没有给出完整多群深穿透GPU伴随相对CPU的速度基线。[固定arXiv v1](https://arxiv.org/html/2609.14496v1)

**Shift的2025状态论文明确给出了另一类CPU/GPU分工。** 其§7说明Denovo正向—伴随、权窗生成及源偏倚由CPU处理，MC及权窗执行在GPU。它是混合流程的实现依据，应与GPU直接求伴随区分。[正式论文](https://doi.org/10.1051/epjn/2024034)

## 新文献与精确核验位置

### new_pryer_wavefront2026

Tristan Pryer. *Batched Wavefront Sweeps for Linear Transport Uncertainty Quantification*. arXiv:2609.14496v1，2026-09-13提交，31页。身份页给出10.48550/arXiv.2609.14496，同时标注DOI注册待完成；著录采用固定v1入口并明确预印本。[身份页](https://arxiv.org/abs/2609.14496v1)

- **硬件与软件（PDFp16，§5）：** Dell Precision5820，Intel Core i9-10900X，64GiB RAM，NVIDIA RTX A4000；Python3.14.4、PyTorch2.11、CUDA runtime12.8。
- **伴随试验（PDFp21—23，§5.3）：** 二维吸收体位置、宽度和强度的不确定性；Q1、128×128网格、4096个前向样本，其中2048个样本用于响应导数，反向微批宽128。
- **独立一致性核验（PDFp23末）：** 在双精度8×8、12×12、16×16、24×24和32×32网格上，对探测器电流、目标区平均通量及吸收响应，用独立装配正向/转置块系统核查。原文仅报告最大误差处于双精度舍入量级，没有逐网格误差数字；不补造绝对阈值。
- **可核的前向性能数字（PDFp17，Table1）：** Q1、256×256、64样本共16777216个DG未知量；L2平均误差9.257×10^-7，探测器电流平均绝对误差3.819×10^-10，扫掠中位时间0.500s；不包含局部矩阵构造和求逆。这不是伴随耗时。
- **存储与批次对照（PDFpp26—27，Table6）：** 同一GPU、1536样本、七群16方向、102×102 Q0网格、固定1000次幂迭代；微批64与1536的时间为10520s和2016s，峰值分配约525MB和12590MB。约5.22倍是GPU内执行布局比较，不是相对CPU或GPU伴随加速。

§4的正向/反向对应关系限于固定face-sign分支。文末数据声明称复现实验代码将在论文接收后存入Zenodo，本轮未见已给定归档URL，亦未运行作者程序。独立双精度小网格核验没有逐项另列设备和伴随计时，应据其报告的验证层级写作。

### new_shift_gpu_status2025

Elliott Biondo, Gregory Davidson, Thomas Evans, Steven Hamilton, Seth Johnson, Tara Pandya, Katherine Royston, José Salcedo-Pérez. *Status of GPU capabilities within the Shift Monte Carlo radiation transport code*. EPJ Nuclear Sciences & Technologies，11:5，2025-01-31，DOI10.1051/epjn/2024034。

§2说明事件型GPU与历史型CPU执行；§7及Fig6/Table1讨论NuScale SMR堆外固定源问题及混合分工。论文摘要的Summit每节点约28倍固定源吞吐提升属于MC输运，不能用于Denovo正/伴随或整体权窗准备。这里主要采用明确的CPU预计算/GPU生产分工，不另加未核的型号。

出版社全文搜索索引可读，§7另与公开PDF句段交叉检查；直接出版社请求失败。本地769字节HTML为拒绝页面，已在获取记录中注明，不能当作下载全文。此事实限于该论文所述版本，不推断后来软件始终未改变。

## 建议加入3.2的文字

> GPU伴随实现也开始采用可微扫掠。Pryer近期预印本将固定源DG扫掠组织为GPU张量程序，通过反向自动微分计算材料阴影响应的导数，并用独立装配的转置系统核对离散伴随作用，为正向执行结构与伴随一致性的共同设计提供参照。混合生产流程还可采用不同分工：Shift在CPU上完成Denovo正向—伴随求解及权窗生成，在GPU上执行MC和权窗控制。

正文可只采用第一项，第二项作为一句实现分工或留在证据说明；无需把性能数字全部塞入段落。

## 175的证据层级与可声称范围

|层级|本轮判断|
|---|---|
|已测GPU正向固定源|既有STRAUM等，维持V2记录|
|已有伴随接口|成熟Denovo及OpenSn伴随，维持各自版本证据|
|源码可组合GPU与伴随|OpenSn固定SHA可追踪路径，不等于已执行组合回归|
|数值核验的离散伴随作用|新增Pryer GPU张量扫掠/反向导数核验|
|完整多群深穿透GPU伴随性能|本轮未取得足够证据，保持空项|

不能写成“成熟GPU-MOC伴随求解器已验证”“GPU伴随达到28倍”或“Pryer已经用于CADIS/FW-CADIS聚变屏蔽”。Pryer的GPU批处理性能与伴随一致性试验应分别陈述。

## 收敛的检索记录

已查询GPU+adjoint+neutron transport、GPU-accelerated adjoint discrete ordinates、CUDA adjoint neutron、GPU adjoint flux characteristics等组合。定位到的Sandman2020确有GPU反向MC试验，但对象是简单非相互作用冷中子束/导管，未纳入多群散射屏蔽伴随主线；声子BTE、扩散模型和神经算子也不用于补足该证据空项。新增两项后停止泛搜。

原始PDF、提取文本和拒绝HTML只在v3_sources本地缓存并由.gitignore排除；JSON records数组提供完整结构字段及获取日志。未修改正文。
