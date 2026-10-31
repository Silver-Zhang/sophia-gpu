# Argument map

## Scientific tension

Regular voxels simplify GPU geometry traversal and data layout but can distort curved interfaces, thin layers and void connectivity. Refinement protects transport paths yet increases storage, ray segments and irregular scheduling. Fast sweeps can be outweighed by source iterations and geometry setup. Need evidence for equal-response-accuracy total cost.

## Central research question

For fusion-relevant 3D fixed-source neutron transport with thin material layers and streaming voids, under what geometric/transport conditions can response-controlled voxel representation and GPU MOC achieve a superior accuracy-memory-time tradeoff to uniform voxels and existing general-geometry transport routes?

## Supporting research questions

1. Geometry: how do interface displacement, volume fraction, chord length/optical depth and void connectivity influence target responses, and what selective refinement/interface handling controls these errors?
2. Solver/architecture: which combination of on-the-fly voxel traversal, track-angle-group batching, accumulation and convergence acceleration minimizes end-to-end time under fixed memory and error budgets?
3. Conditional extension: what forward/adjoint fidelity is sufficient to create effective MC weight windows, and does the complete voxel-GPU-MOC workflow outperform MC-only, MAGIC and random-ray FW-CADIS for selected shielding responses?

## Proposed method and tests

- Start uniform Cartesian, one material per cell, full-3D long characteristics with DDA. Add block-structured local refinement; reserve selective boundary subcell/explicit segment treatment for failure of resolution-only route.
- Separate geometry, spatial source, angular, track-spacing, group, scattering-order, iteration and floating-point effects. Begin multigroup matched-data comparisons, then continuous-energy reference for combined engineering errors.
- Baseline anisotropic scattering extension and void-safe characteristic formula are needed for fusion transfer. Neutron-only primary; coupled neutron-photon transport and angular importance extension are conditional.
- Equal accuracy performance; include geometry/track setup, iterative solve, transfers, peak memory. Optimized multicore CPU and single GPU baselines.
- Tests: analytic absorber/void -> curved multilayer and oblique straight/bent duct -> public fusion benchmark and representative sector. Use exact-geometry MC vs voxel MC to isolate geometry; voxel MC vs MOC to isolate numerical discretization.
- Adjoint operator tested with weighted discrete duality and detector response identity. Weight-window generation must retain support and preserve MC weight conservation. Original geometry stays in final MC where feasible.

## Counterarguments

- High fidelity boundary handling can erase regularity advantages; compare against uniform grid and exact geometry, retain only beneficial local complexity.
- MOC ray effects remain; angular/track convergence and uncollided/collided split assessed conditionally.
- Random rays already remove geometry duplication; added voxel conversion must earn its cost.
- Purely engineering kernel optimization is insufficient novelty: require an error-response relationship and reproducible selection criterion.

## Scope outcome

Review decisions: explicitly account for 3D trajectory quadrature/coverage and weighted conservation; use a void-stable limit; anisotropic multigroup and (n,xn) handling are core physics requirements. Do not claim goal-oriented refinement, OTF tracing or a general importance-fidelity optimum as new. Novelty target is geometry-conversion/path/topology response error linked to GPU total cost. VITAS, NuDEAL and MOCkingbird are literature comparisons unless runnable access is established. Core baselines use controlled implementations and open MC. Both foundation reviews passed (>7.5); methodological review 8.2 and fit/novelty review 8.1. Amendments incorporated before drafting.

Two core methodological contributions plus a conditional hybrid demonstration; no whole-reactor multiphysics, burnup or proprietary full ITER requirement.

