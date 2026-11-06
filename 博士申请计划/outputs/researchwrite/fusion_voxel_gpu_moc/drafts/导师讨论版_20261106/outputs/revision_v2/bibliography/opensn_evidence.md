# OpenSn GPU—伴随组合独立核查

核查日期：2026-11-06。官方代码快照：`f903a0d71cb8d130dc104f85d9d9ae66fd79146b`，提交时间2026-11-06 05:16:24 UTC，VERSION.txt为1.0.1。仅增证据，不改正文。

**结论：现行代码存在可追踪的GPU与Cartesian伴随组合执行路径；本轮未发现已注册的GPU伴随组合回归，也没有该组合的性能实测。** “有实现路径”属于源码静态核查结论，不能改成“已验证GPU伴随加速”。

## 正式书目信息

Andrs, David; Hardy, Zachary; Hawkins, Daryl; Morel, Jim; Nguyen, Dinh Quoc Dang; Ragusa, Jean C. *OpenSn: A massively parallel, open-source simulation environment for discrete ordinates radiation transport*. Computer Physics Communications, **320** (2026), 110001. DOI：[10.1016/j.cpc.2025.110001](https://doi.org/10.1016/j.cpc.2025.110001)。建议key：`new_opensn2026`。作者顺序、题名、卷、文章号和2026年3月归卷已用Crossref与官方推荐引文核对。DOI含2025，不应因此改书目年为2025。

正式论文的Program Summary仍写GPU加速在开发中。[出版社原始记录](https://www.sciencedirect.com/science/article/pii/S0010465525005028)与2026-11-06现行实现分属不同版本，尚未取得论文发布包对应SHA，不能用后者改写前者的实验贡献。

## 实现路径（固定SHA）

下列不是仅凭两个参数推测兼容：已经逐段追踪转置散射/裂变源到设备扫掠的同一数据流。源迭代的源构造仍在主机，扫掠由GPU完成；不能称全部伴随运算均在GPU。

1. 伴随检查Cartesian、standard角算子和等权反向方向，拒绝时间依赖；未排斥use_gpus。 [modules/linear_boltzmann_solvers/lbs_problem/lbs_problem.cc:1035](https://github.com/Open-Sn/opensn/blob/f903a0d71cb8d130dc104f85d9d9ae66fd79146b/modules/linear_boltzmann_solvers/lbs_problem/lbs_problem.cc#L1035)
2. InitializeMaterials为伴随建立转置截面。 [modules/linear_boltzmann_solvers/lbs_problem/lbs_problem.cc:1177](https://github.com/Open-Sn/opensn/blob/f903a0d71cb8d130dc104f85d9d9ae66fd79146b/modules/linear_boltzmann_solvers/lbs_problem/lbs_problem.cc#L1177)
3. 依问题伴随标志读取GetTransferMatrices/GetProductionMatrix。 [modules/linear_boltzmann_solvers/discrete_ordinates_problem/source_functions/source_function.cc:51](https://github.com/Open-Sn/opensn/blob/f903a0d71cb8d130dc104f85d9d9ae66fd79146b/modules/linear_boltzmann_solvers/discrete_ordinates_problem/source_functions/source_function.cc#L51)
4. CopyPhiAndSrcToDevice将源矩复制到GPU。 [modules/linear_boltzmann_solvers/discrete_ordinates_problem/discrete_ordinates_problem.cu:12](https://github.com/Open-Sn/opensn/blob/f903a0d71cb8d130dc104f85d9d9ae66fd79146b/modules/linear_boltzmann_solvers/discrete_ordinates_problem/discrete_ordinates_problem.cu#L12)
5. use_gpus分派至AAHD/CBCD扫掠块；不按伴随标志回落CPU。 [modules/linear_boltzmann_solvers/discrete_ordinates_problem/sweep/discrete_ordinates_sweep_construction.cc:253](https://github.com/Open-Sn/opensn/blob/f903a0d71cb8d130dc104f85d9d9ae66fd79146b/modules/linear_boltzmann_solvers/discrete_ordinates_problem/sweep/discrete_ordinates_sweep_construction.cc#L253)
6. GPU核参数引用源矩设备指针。 [modules/linear_boltzmann_solvers/discrete_ordinates_problem/sweep_chunks/gpu_kernel/arguments.h:60](https://github.com/Open-Sn/opensn/blob/f903a0d71cb8d130dc104f85d9d9ae66fd79146b/modules/linear_boltzmann_solvers/discrete_ordinates_problem/sweep_chunks/gpu_kernel/arguments.h#L60)
7. AAH GPU扫掠入口调用CopyPhiAndSrcToDevice；CBC对应185行。 [modules/linear_boltzmann_solvers/discrete_ordinates_problem/sweep/scheduler/sweep_scheduler.cu:25](https://github.com/Open-Sn/opensn/blob/f903a0d71cb8d130dc104f85d9d9ae66fd79146b/modules/linear_boltzmann_solvers/discrete_ordinates_problem/sweep/scheduler/sweep_scheduler.cu#L25)
8. 稳态求解后统一执行伴随方向重定向。 [modules/linear_boltzmann_solvers/discrete_ordinates_problem/solvers/steady_state_solver.cc:98](https://github.com/Open-Sn/opensn/blob/f903a0d71cb8d130dc104f85d9d9ae66fd79146b/modules/linear_boltzmann_solvers/discrete_ordinates_problem/solvers/steady_state_solver.cc#L98)

配置检查还要求标准角算子及等权反向方向，并拒绝时间依赖伴随；曲线坐标、CSDA等不可外推。[官方文档§11.7](https://open-sn.github.io/opensn/userguide/discrete_ordinates_problems.html#problem-modes)只是入口说明，结论以上述代码路径为依据。

## 回归测试核查

- 扫描官方快照test目录所有tests.json，42项GPU注册作业中未发现实际启用伴随组合。
- transport_adjoint/tests.json共29项注册测试，没有requires_gpu；测试脚本也没有use_gpus设置。
- `deterministic_sweeps.py`把CASE与USE_GPUS分别传入同一问题构造，因此可配置case="adjoint"与use_gpus=True；但tests.json中伴随项只给case="adjoint"，GPU项只给steady/keigen。脚本具有组合执行入口，不等于组合已经进入回归。
- GPU CPU parity脚本只验证正向。CUDA/HIP工作流使用--gpu；runner明确过滤非requires_gpu用例，故不能将CPU伴随测试计为GPU伴随测试。

- 同一个problem_args可同时令CASE=adjoint及USE_GPUS=True。 [固定定位](https://github.com/Open-Sn/opensn/blob/f903a0d71cb8d130dc104f85d9d9ae66fd79146b/test/python/modules/linear_boltzmann_solvers/transport_steady/deterministic_sweeps.py#L141)
- CPU adjoint单独注册；GPU注册仅steady、fused steady、CBC steady、keigen，没有case=adjoint+GPU。 [固定定位](https://github.com/Open-Sn/opensn/blob/f903a0d71cb8d130dc104f85d9d9ae66fd79146b/test/python/modules/linear_boltzmann_solvers/transport_steady/tests.json#L2514)
- GPU/CPU通量向量一致性脚本未启伴随。 [固定定位](https://github.com/Open-Sn/opensn/blob/f903a0d71cb8d130dc104f85d9d9ae66fd79146b/test/python/modules/linear_boltzmann_solvers/transport_steady/gpu_cpu_parity.py#L25)
- --gpu只选requires_gpu测试，不能认为GPU工作流顺带执行了CPU伴随用例。 [固定定位](https://github.com/Open-Sn/opensn/blob/f903a0d71cb8d130dc104f85d9d9ae66fd79146b/test/src/job_manager.py#L816)
- CUDA工作流调用test/run_tests --gpu；配置存在不等于本轮验证运行通过。 [固定定位](https://github.com/Open-Sn/opensn/blob/f903a0d71cb8d130dc104f85d9d9ae66fd79146b/.github/workflows/regression.yaml#L70)

本轮不编译、不运行GPU，未审读CI运行产物；上述“未发现注册组合测试”严格针对该SHA，不推广至其他分支、未公开测试或未来版本。没有GPU型号、CPU基线或GPU伴随倍率可供正文引用。

## 可采用的文字与验证含义

OpenSn已建立面向非结构多面体网格的SN/DGFEM与离散伴随求解框架。其现行开源实现可追踪到伴随源矩与GPU扫掠相连的执行路径，为正向—伴随共用算子与数据结构提供实现参照；GPU伴随组合的响应一致性和端到端效率仍应独立验证。

建议将正向—伴随响应恒等式、角通量反向映射、CPU/GPU通量与响应一致性，以及源构造/数据传输/扫掠全链路计时作为组合验证。它们是研究路线，不能写成OpenSn已报告的实验结果。

代码快照和获取缓存位于已gitignore的gpu_sources中，交付只含事实、元数据与固定版本定位。
