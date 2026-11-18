# R0a — inference-method robustness of the key paired contrasts

Reviewer-response analysis (2026-11-01, no API calls). Same eligible units and pairing as the paper; `boot_*` must reproduce the manuscript. Sign-flip = randomisation test of the paired differences (exact when n ≤ 20). Leave-one-group-out = pooled estimate dropping one role assignment (rotation; for S5i: one auditor or attacker).

| contrast | n | estimate | boot_lo | boot_hi | t_lo | t_hi | signflip_p | leave_one_group_out_min | leave_one_group_out_max |
|---|---|---|---|---|---|---|---|---|---|
| C3 label - audit, ASR per round | 12 | +0.717 | +0.630 | +0.807 | +0.612 | +0.821 | 0.0005 | +0.615 | +0.780 |
| C4 raw memory - audit, misclassification | 12 | +0.463 | +0.307 | +0.600 | +0.293 | +0.634 | 0.0020 | +0.395 | +0.530 |
| raw memory - audit, ASR per round (secondary) | 12 | -0.073 | -0.137 | -0.013 | -0.145 | -0.002 | 0.0625 | -0.110 | -0.035 |
| C5a Audit - Baseline, objective | 15 | -10.283 | -20.091 | -1.118 | -21.063 | +0.497 | 0.0536 | -17.304 | -1.546 |
| C5b Audit - Baseline, content integrity | 15 | +0.078 | +0.042 | +0.113 | +0.037 | +0.119 | 0.0020 | +0.039 | +0.117 |
| S5b label - audit, ASR | 9 | +0.600 | +0.480 | +0.711 | +0.457 | +0.743 | 0.0039 | +0.547 | +0.700 |
| S5b raw memory - audit, misclassification | 9 | +0.471 | +0.276 | +0.644 | +0.244 | +0.698 | 0.0078 | +0.327 | +0.633 |
| S5d raw memory - audit, misclassification | 18 | +0.360 | +0.238 | +0.484 | +0.225 | +0.495 | 0.0001 | +0.247 | +0.447 |
| S5d label-only - audit, misclassification | 18 | +0.018 | +0.002 | +0.038 | -0.003 | +0.038 | 0.1094 | +0.003 | +0.030 |
| S5d raw memory - audit, ASR | 18 | -0.078 | -0.151 | -0.016 | -0.156 | +0.000 | 0.0630 | -0.130 | +0.010 |
| S5d neutral context - audit, ASR | 18 | +0.096 | +0.029 | +0.173 | +0.015 | +0.176 | 0.0215 | +0.033 | +0.147 |
| S5h tags - raw memory, misclassification | 24 | -0.358 | -0.460 | -0.253 | -0.470 | -0.247 | <0.0001 | -0.483 | -0.228 |
| S5h tags - audit, misclassification | 24 | +0.040 | +0.015 | +0.065 | +0.014 | +0.066 | 0.0069 | +0.003 | +0.065 |
| S5h tags - raw memory, ASR | 24 | +0.052 | +0.020 | +0.088 | +0.014 | +0.089 | 0.0071 | +0.000 | +0.077 |
| S5h tags - audit, ASR | 24 | -0.057 | -0.118 | -0.000 | -0.119 | +0.006 | 0.0820 | -0.085 | -0.038 |
| R-J1 S5j tags - label-only, ASR | 24 | -0.045 | -0.098 | +0.003 | -0.100 | +0.010 | 0.1175 | -0.075 | +0.007 |
| R-J2 S5j tags - label-only, misclassification | 24 | +0.013 | +0.000 | +0.027 | -0.000 | +0.027 | 0.0966 | +0.007 | +0.018 |
| R-J3 S5j label-only - audit, misclassification | 24 | +0.025 | +0.005 | +0.048 | +0.002 | +0.048 | 0.0504 | -0.005 | +0.045 |
| R-I3 S5i raw memory - audit, misclassification (pooled; group = auditor) | 36 | +0.360 | +0.247 | +0.473 | +0.241 | +0.479 | <0.0001 | +0.160 | +0.503 |
| R-K1 S5k white-box - selection, ASR (audit) | 12 | +0.027 | -0.023 | +0.100 | -0.045 | +0.099 | 0.7031 | -0.005 | +0.045 |
| R-K1 S5k white-box - selection, ASR (tag memory) | 12 | +0.010 | -0.063 | +0.070 | -0.067 | +0.087 | 0.8438 | -0.030 | +0.045 |
| R-I3 S5i raw memory - audit, misclassification (deepseek_v4_pro auditor) | 12 | +0.247 | +0.107 | +0.400 | +0.073 | +0.420 | 0.0078 | +0.190 | +0.305 |
| R-I3 S5i raw memory - audit, misclassification (glm53 auditor) | 12 | +0.073 | +0.000 | +0.187 | -0.040 | +0.187 | 0.5000 | +0.040 | +0.110 |
| R-I3 S5i raw memory - audit, misclassification (minimax_m3 auditor) | 12 | +0.760 | +0.713 | +0.803 | +0.708 | +0.812 | 0.0005 | +0.750 | +0.775 |

Leave-one-planner-out (S7b_C): C5a Audit - Baseline, objective: -17.160 to -1.500; C5b Audit - Baseline, content integrity: +0.021 to +0.099
