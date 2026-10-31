# Research canon

## Verified literature facts

1. Zhang's official SJTU page lists advanced neutron transport algorithms, multiphysics, reduced models/data assimilation, and VITAS. https://me.sjtu.edu.cn/teacher_directory1/zhangtengfei
2. VITAS is a variational nodal framework, not an established voxel MOC code: Zhang et al., 10.1016/j.anucene.2022.109335. The described 2022 version uses isotropic scattering and axial extrusion of supported 2D geometries; do not universalize this version limitation to all later work.
3. Yin et al. report efficient heterogeneous VNM parallel algorithms: 10.1007/s41365-024-01430-4. Details await full accessible text. Related 3D VNM parallel paper: https://www.sciencedirect.com/science/article/abs/pii/S0149197019300642
4. GPU MOC and multi-GPU MOC exist: Zhang Zhizhu, Wang Kan, Li Qing (not Zhang Tengfei), 2013, 10.1016/j.anucene.2013.06.039; Boyd et al., 2014, 10.1016/j.anucene.2013.12.012.
5. Unstructured fully 3D MOC exists: Gaston et al., 2021, 10.1080/00295450.2021.1871995. Full and on-the-fly track storage are established options.
6. NuDEAL's 2026 author manuscript links published DOI 10.1080/00295639.2026.2652773 and compares GPU MOC/HFEM, DGMOC, and DFEM-SN: https://arxiv.org/abs/2607.01591.
7. CADIS/FW-CADIS, fusion applications and adaptive deterministic/weight-window meshes predate this proposal: https://web.ornl.gov/~5pe/p081.pdf
8. OpenMC stable documentation currently describes random-ray forward/adjoint FW-CADIS on shared MC geometry: https://docs.openmc.org/en/stable/methods/variance_reduction.html
9. Random-ray shielding variance reduction is published: Raffuzzi, Neame, Cosgrove, 10.1080/00295639.2025.2458958; online 2025, volume 200 supplement 1 (2026), S485-S502.
10. Fusion-relevant benchmark resources include FNG HCPB, Cu, FNS and CAD/CSG code comparisons: https://scientific-publications.ukaea.uk/papers/benchmarking-of-emergent-radiation-transport-codes-for-fusion-neutronics-applications/

## Review additions

- Sun et al. 2024, 10.1016/j.camwa.2024.06.032, UVNM-SN on unstructured heterogeneous transport with volume correction and NDA, is direct advisor-method evidence. Sun et al. 2024, 10.1103/PhysRevE.110.065301, studies upwind-HDG for multiscale first-order transport and sweep structure. Both have Tengfei Zhang in the author list.
- Xiao and Zhang, KNS Autumn Meeting 2023, https://www.kns.org/files/int_paper/paper/RPHA-2023_2023_5/RPHA-2023-WeiXiao.pdf, develops anisotropic heterogeneous VNM on VITAS and checks a slab problem. 2022 isotropic limitation is not universal.
- Baker et al. 2013, 10.1016/j.anucene.2012.11.029, is prior goal-based fixed-source mesh adaptivity. Wang et al. 2022, 10.3390/en15228335, is a Chinese goal-oriented multi-collision source/streaming study. Response-driven AMR alone is not new.
- NuDEAL MOC/HFEM and DGMOC remain axially extruded; its DFEM-SN handles general geometry. Do not claim the whole framework is unrestricted 3D MOC.
- Yin 2024 concerns heterogeneous MATERIALS and CPU/MPI parallelism, not heterogeneous CPU/GPU hardware.
- Raffuzzi accepted manuscript, conclusions pp.30–31: two bulk-shielding cases, higher-fidelity importance did not improve variance reduction in those tests; prominent streaming paths were not studied. It cannot support universal conclusions or novelty of a generic fidelity-cost optimum.
- Core physical response scope: neutron flux, leakage, reaction rates and specified-region tritium production; (n,xn) production and multigroup anisotropy included where relevant. Total nuclear heating, shutdown dose, activation and multiphysics are not core commitments.
- OpenMC random-ray comparator must be version-pinned with isotropic-source capability checked; compare algorithmic performance under matched approximations, and engineering workflows separately.

## Applicant and experimental facts

- No applicant preliminary calculations, measured data, publications or code have been supplied.
- No GPU allocation, proprietary solver license, CAD model or supervisor agreement has been verified.

## Definitions

- Voxelization: spatial geometry/material representation; it is not itself the transport discretization.
- MOC: integrate the transport equation along characteristics; this proposal prioritizes full-3D long-characteristic fixed-source formulation, distinguishing it from 2D/1D axial-extrusion models and short-characteristic interpolating SN sweeps.
- GPU acceleration: complete time-to-target-accuracy including geometry, tracks, iterations and transfers; not a kernel-only single-core speedup.
- CADIS/FW-CADIS: importance sampling and consistent source/weight-window biasing; not adding deterministic and MC solutions or removing deterministic bias from a replaced geometry.

## Prohibited claims

- First voxel/GPU/MOC/adjoint hybrid method, universal superiority, guaranteed 100x speedup.
- VITAS already supports GPU MOC or fusion FW-CADIS; advisor authored papers in which he appears only as reviewer.
- Volume preservation guarantees optical path/topological or response accuracy.
- Independent GPU updates of all spatial cells without accounting for track dependencies.
- High-accuracy scalar flux guarantees efficient importance maps in streaming regimes.
- MC on the same voxel geometry validates original CAD geometry without a separate geometry comparison.

