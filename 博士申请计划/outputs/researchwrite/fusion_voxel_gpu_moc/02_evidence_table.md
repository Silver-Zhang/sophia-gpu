# Evidence table

| Claim | Evidence | Strength | Use | Boundary |
|---|---|---|---|---|
| Fusion CAD and deep-shielding transport require careful geometry and validation | Valentine et al. UKAEA fusion benchmark paper | evidence-backed | background/validation | benchmark availability still needs checking |
| Full 3D GPU MOC is established | Zhang Zhizhu 2013; Boyd 2014; Zhou 2025 preprint | evidence-backed | review | no generic GPU novelty |
| Fully 3D unstructured characteristics exist | Gaston 2021 MOCkingbird | evidence-backed | comparator | geometry alone does not distinguish thesis |
| Structured geometry may simplify index/traversal and coalesced GPU access | Amanatides/Woo 1987 + algorithm reasoning | plausible-inference | hypothesis | performance and conversion error require testing |
| Thin gaps/layers and oblique streaming channels may be sensitive to voxel errors | transport optical-depth reasoning + fusion CAD benchmarks | hypothesis | RQ1 | demonstrate response sensitivity, not assume all features matter equally |
| Block-adaptive refinement may improve accuracy-cost tradeoff | prior mesh-adaptive fusion FW-CADIS study + proposed geometry design | hypothesis | RQ1/RQ2 | AMR itself is not novel; divergence can erase benefits |
| Advisor alignment lies in transport discretization, geometric flexibility, acceleration/parallelism and V&V | official SJTU page; VITAS; Yin parallel VNM | evidence-backed | fit | exact code reuse remains conditional |
| Random-ray FW-CADIS is an essential modern comparator | OpenMC official docs; Raffuzzi 2025/2026 | evidence-backed | RQ3 | hybrid coupling itself not new |
| Importance accuracy and total variance reduction cost may have a useful optimum at coarser fidelity | CADIS theory and proposed experiments | hypothesis | extension | quantify with end-to-end FOM and nonzero support |
| Angular-informed CADIS already exists | Munk et al. arXiv:1612.00793 | evidence-backed | review/risk | angular weighting cannot be sole novelty |
| Response-driven adaptation itself is established | Baker 2013, 10.1016/j.anucene.2012.11.029; Wang 2022, 10.3390/en15228335 | evidence-backed | novelty boundary | contribution must target geometry conversion/path error plus GPU cost |
| Advisor has direct unstructured/multiscale transport studies | Sun 2024 CMwA; Sun 2024 PRE; Xiao/Zhang KNS2023 | evidence-backed | fit and methods | neither authorizes code access nor proves fusion GPU capability |
| More faithful importance is not always better, and streaming remains an issue in RR study | Raffuzzi accepted manuscript pp.29–31 | evidence-backed within two tested bulk-shielding cases | extension motivation | narrow hypothesis to geometric/streaming error and total cost, not general first fidelity study |

