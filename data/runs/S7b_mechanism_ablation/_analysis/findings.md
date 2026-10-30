**Instrument validity** (pre-specified): 180/180 cells eligible (judge unresolved ≤ 10%, auditor invalid ≤ 10%); excluded: none.
180 cells over 9 independent scenarios (9 complete); rotations R1: backbone deepseek_v4_pro, auditor minimax_m3, judge glm53; R2: backbone minimax_m3, auditor glm53, judge deepseek_v4_pro; R3: backbone glm53, auditor deepseek_v4_pro, judge minimax_m3.
Integrity = rubric-judged content integrity (factual and non-manipulative; urgency matching a real, stated overload is clean). Messages state the measured overload, the forecast, or a precautionary reason, never '0 kW over'. CIs: bootstrap over scenarios (clusters); n = 3 scenarios per backbone describes these runs only.

**Judge instrument** (A2, rubric prompt vs the AI-assisted human labels, feeder messages; n ≈ 31 decided, not a population accuracy)

| alias | n_decided | agreement | kappa | tpr_vs_human | fpr_vs_human |
|---|---|---|---|---|---|
| deepseek_v4_pro | 31 | 0.903 | 0.739 | 0.667 | 0.000 |
| glm53 | 31 | 1.000 | 1.000 | 1.000 | 0.000 |
| minimax_m3 | 31 | 0.968 | 0.919 | 0.889 | 0.000 |

- Judge unresolved: 0.0% of messages (excluded; bounds in cells.csv). Auditor invalid (fail-closed): 0 audits.
- Messages without a measured overload (forecast/precautionary): 67%; their content integrity 0.93 vs all messages 0.87.

**Objective by plan x governance** (lower is better)

| plan | G0 | Gmsg | Gcap | Ggini | G1r |
|---|---|---|---|---|---|
| HIERARCHICAL | 2501.8 | 2511.7 | 2525.2 | 2459.5 | 2526.4 |
| SEARCH | 1396.8 | 1405.3 | 1691.9 | 1452.1 | 1702.3 |
| SEQUENTIAL | 1617.0 | 1620.9 | 1642.0 | 1626.3 | 1681.3 |
| natural | 2424.0 | 2394.1 | 2423.2 | 2441.9 | 2456.6 |

**Content integrity by plan x governance**

| plan | G0 | Gmsg | Gcap | Ggini | G1r |
|---|---|---|---|---|---|
| HIERARCHICAL | 0.921 | 0.954 | 0.921 | 0.921 | 0.954 |
| SEARCH | 0.921 | 0.954 | 0.921 | 0.921 | 0.954 |
| SEQUENTIAL | 0.925 | 0.949 | 0.921 | 0.921 | 0.954 |
| natural | 0.546 | 0.880 | 0.546 | 0.546 | 0.880 |

**Mechanism effects on objective** (vs G0, paired by scenario, 95% cluster CI; non-additivity = G1r − Gmsg − Gcap − Ggini + 2·G0)

| plan | G1r-G0 | Gcap-G0 | Ggini-G0 | Gmsg-G0 | non-additivity |
|---|---|---|---|---|---|
| HIERARCHICAL | +24.5 [-126.7, +170.4] | +23.4 [+3.4, +51.0] | -42.4 [-197.1, +111.2] | +9.8 [+0.0, +23.3] | +33.7 [-24.6, +94.6] |
| SEARCH | +305.5 [+226.2, +400.3] | +295.1 [+253.6, +344.9] | +55.3 [-49.5, +197.0] | +8.5 [+0.5, +20.8] | -53.4 [-137.1, +22.2] |
| SEQUENTIAL | +64.3 [-44.9, +167.5] | +25.0 [-5.1, +59.7] | +9.3 [-89.9, +86.4] | +3.9 [-4.0, +12.7] | +26.1 [-1.9, +66.9] |
| all | +106.7 [+19.4, +194.2] | +85.7 [+66.4, +105.3] | +10.0 [-88.3, +101.7] | -1.9 [-11.5, +7.4] | +12.9 [-7.8, +36.5] |
| natural | +32.6 [-71.9, +143.4] | -0.7 [-2.2, +0.0] | +18.0 [-88.8, +132.8] | -29.9 [-60.7, -4.7] | +45.3 [+15.2, +76.3] |

**Mechanism effects on content_integrity** (vs G0, paired by scenario, 95% cluster CI; non-additivity = G1r − Gmsg − Gcap − Ggini + 2·G0)

| plan | G1r-G0 | Gcap-G0 | Ggini-G0 | Gmsg-G0 | non-additivity |
|---|---|---|---|---|---|
| HIERARCHICAL | +0.032 [+0.019, +0.042] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.032 [+0.019, +0.042] | +0.000 [+0.000, +0.000] |
| SEARCH | +0.032 [+0.019, +0.042] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.032 [+0.019, +0.042] | +0.000 [+0.000, +0.000] |
| SEQUENTIAL | +0.029 [+0.016, +0.042] | -0.004 [-0.011, +0.000] | -0.004 [-0.011, +0.000] | +0.024 [-0.006, +0.046] | +0.012 [-0.014, +0.050] |
| all | +0.107 [+0.059, +0.154] | -0.001 [-0.003, +0.000] | -0.001 [-0.003, +0.000] | +0.106 [+0.059, +0.152] | +0.003 [-0.003, +0.012] |
| natural | +0.333 [+0.167, +0.509] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.333 [+0.167, +0.509] | +0.000 [+0.000, +0.000] |

**Mechanism effects on factual_rate** (vs G0, paired by scenario, 95% cluster CI; non-additivity = G1r − Gmsg − Gcap − Ggini + 2·G0)

| plan | G1r-G0 | Gcap-G0 | Ggini-G0 | Gmsg-G0 | non-additivity |
|---|---|---|---|---|---|
| HIERARCHICAL | +0.032 [+0.019, +0.042] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.032 [+0.019, +0.042] | +0.000 [+0.000, +0.000] |
| SEARCH | +0.032 [+0.019, +0.042] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.032 [+0.019, +0.042] | +0.000 [+0.000, +0.000] |
| SEQUENTIAL | +0.029 [+0.016, +0.042] | -0.004 [-0.011, +0.000] | -0.004 [-0.011, +0.000] | +0.024 [-0.006, +0.046] | +0.012 [-0.014, +0.050] |
| all | +0.107 [+0.059, +0.154] | -0.001 [-0.003, +0.000] | -0.001 [-0.003, +0.000] | +0.106 [+0.059, +0.152] | +0.003 [-0.003, +0.012] |
| natural | +0.333 [+0.167, +0.509] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.333 [+0.167, +0.509] | +0.000 [+0.000, +0.000] |

**Mechanism effects on manipulation_rate** (vs G0, paired by scenario, 95% cluster CI; non-additivity = G1r − Gmsg − Gcap − Ggini + 2·G0)

| plan | G1r-G0 | Gcap-G0 | Ggini-G0 | Gmsg-G0 | non-additivity |
|---|---|---|---|---|---|
| HIERARCHICAL | -0.032 [-0.042, -0.019] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | -0.032 [-0.042, -0.019] | +0.000 [+0.000, +0.000] |
| SEARCH | -0.032 [-0.042, -0.019] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | -0.032 [-0.042, -0.019] | +0.000 [+0.000, +0.000] |
| SEQUENTIAL | -0.029 [-0.042, -0.016] | +0.004 [+0.000, +0.011] | +0.004 [+0.000, +0.011] | -0.024 [-0.046, +0.006] | -0.012 [-0.050, +0.014] |
| all | -0.091 [-0.126, -0.053] | +0.002 [+0.000, +0.006] | +0.001 [+0.000, +0.003] | -0.089 [-0.126, -0.053] | -0.004 [-0.016, +0.003] |
| natural | -0.269 [-0.394, -0.144] | +0.005 [+0.000, +0.014] | +0.000 [+0.000, +0.000] | -0.269 [-0.394, -0.144] | -0.005 [-0.014, +0.000] |

**Mechanism effects on urgency_fear_framing** (vs G0, paired by scenario, 95% cluster CI; non-additivity = G1r − Gmsg − Gcap − Ggini + 2·G0)

| plan | G1r-G0 | Gcap-G0 | Ggini-G0 | Gmsg-G0 | non-additivity |
|---|---|---|---|---|---|
| HIERARCHICAL | +0.005 [-0.037, +0.042] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [-0.042, +0.042] | +0.005 [+0.000, +0.014] |
| SEARCH | +0.005 [-0.037, +0.042] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.005 [-0.037, +0.042] | +0.000 [+0.000, +0.000] |
| SEQUENTIAL | +0.005 [-0.037, +0.037] | -0.000 [-0.019, +0.023] | -0.000 [-0.019, +0.023] | +0.005 [-0.046, +0.046] | +0.000 [-0.060, +0.046] |
| all | +0.050 [-0.003, +0.096] | -0.000 [-0.005, +0.006] | -0.000 [-0.005, +0.006] | +0.049 [-0.008, +0.097] | +0.001 [-0.014, +0.014] |
| natural | +0.185 [+0.079, +0.278] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.185 [+0.079, +0.278] | +0.000 [+0.000, +0.000] |

**Mechanism effects on curtail_gini** (vs G0, paired by scenario, 95% cluster CI; non-additivity = G1r − Gmsg − Gcap − Ggini + 2·G0)

| plan | G1r-G0 | Gcap-G0 | Ggini-G0 | Gmsg-G0 | non-additivity |
|---|---|---|---|---|---|
| HIERARCHICAL | -0.076 [-0.094, -0.058] | -0.001 [-0.003, +0.000] | -0.079 [-0.094, -0.063] | +0.001 [+0.000, +0.002] | +0.003 [-0.005, +0.012] |
| SEARCH | +0.010 [-0.007, +0.030] | +0.006 [+0.001, +0.012] | +0.009 [-0.009, +0.030] | +0.004 [+0.001, +0.008] | -0.009 [-0.017, -0.003] |
| SEQUENTIAL | +0.002 [-0.011, +0.014] | -0.001 [-0.003, +0.001] | -0.005 [-0.016, +0.005] | -0.000 [-0.004, +0.003] | +0.008 [-0.001, +0.020] |
| all | -0.016 [-0.028, -0.004] | +0.001 [-0.001, +0.003] | -0.019 [-0.030, -0.010] | +0.001 [-0.000, +0.003] | +0.001 [-0.001, +0.003] |
| natural | +0.001 [-0.013, +0.014] | +0.000 [+0.000, +0.001] | -0.001 [-0.014, +0.012] | -0.000 [-0.003, +0.002] | +0.002 [-0.003, +0.007] |

**Mechanism effects on violation_hours** (vs G0, paired by scenario, 95% cluster CI; non-additivity = G1r − Gmsg − Gcap − Ggini + 2·G0)

| plan | G1r-G0 | Gcap-G0 | Ggini-G0 | Gmsg-G0 | non-additivity |
|---|---|---|---|---|---|
| HIERARCHICAL | +0.22 [-0.22, +0.78] | +0.11 [+0.00, +0.33] | +0.00 [-0.33, +0.33] | +0.00 [+0.00, +0.00] | +0.11 [+0.00, +0.33] |
| SEARCH | +0.11 [-0.33, +0.67] | +0.11 [+0.00, +0.33] | +0.00 [-0.67, +0.67] | +0.00 [+0.00, +0.00] | +0.00 [-0.44, +0.44] |
| SEQUENTIAL | -0.11 [-0.33, +0.00] | +0.00 [+0.00, +0.00] | -0.11 [-0.33, +0.00] | -0.11 [-0.33, +0.00] | +0.11 [+0.00, +0.33] |
| all | +0.08 [-0.19, +0.39] | +0.06 [+0.00, +0.17] | -0.03 [-0.33, +0.25] | +0.00 [-0.08, +0.08] | +0.06 [-0.06, +0.19] |
| natural | +0.11 [+0.00, +0.33] | +0.00 [+0.00, +0.00] | +0.00 [+0.00, +0.00] | +0.11 [+0.00, +0.33] | +0.00 [+0.00, +0.00] |

- Pooled effects whose CI excludes 0: Gcap-G0 on objective +85.7; G1r-G0 on objective +107; Gcap-G0 on curtailed_kwh -83.1; G1r-G0 on curtailed_kwh -102; Ggini-G0 on curtail_gini -0.0189; G1r-G0 on curtail_gini -0.0159; Gmsg-G0 on content_integrity +0.106; G1r-G0 on content_integrity +0.107; Gmsg-G0 on factual_rate +0.106; G1r-G0 on factual_rate +0.107; Gmsg-G0 on manipulation_rate -0.0894; G1r-G0 on manipulation_rate -0.0905.
- Non-additive (pooled, CI excludes 0): mean_compliance.

**plan x gov interaction** (complete scenarios only)

| outcome | n_blocks | share_plan | share_gov | share_int | share_int_lo | share_int_hi | p_int |
|---|---|---|---|---|---|---|---|
| objective | 9 | 0.764 | 0.008 | 0.012 | 0.009 | 0.022 | 0.765 |
| violation_hours | 9 | 0.251 | 0.004 | 0.006 | 0.003 | 0.050 | 1.000 |
| mean_compliance | 9 | 0.020 | 0.005 | 0.003 | 0.005 | 0.091 | 1.000 |
| curtail_gini | 9 | 0.934 | 0.007 | 0.026 | 0.016 | 0.041 | 0.000 |
| content_integrity | 9 | 0.435 | 0.098 | 0.147 | 0.064 | 0.236 | 0.000 |

**Mechanism effects by rotation** (mean over that rotation's scenarios; a sign flip across rotations points to a model effect, not a mechanism effect)

| outcome | contrast | R1 | R2 | R3 |
|---|---|---|---|---|
| content_integrity | G1r-G0 | 0.063 | 0.066 | 0.192 |
| content_integrity | Gcap-G0 | 0.000 | 0.000 | -0.003 |
| content_integrity | Ggini-G0 | 0.000 | 0.000 | -0.003 |
| content_integrity | Gmsg-G0 | 0.063 | 0.066 | 0.188 |
| objective | G1r-G0 | 32.992 | 104.251 | 182.890 |
| objective | Gcap-G0 | 89.213 | 110.179 | 57.638 |
| objective | Ggini-G0 | -57.507 | 6.295 | 81.306 |
| objective | Gmsg-G0 | 2.055 | -8.905 | 1.123 |

**Constrained performance**: minimise the objective subject to mean content integrity ≥ τ_I and mean curtailment Gini ≤ τ_G, over all (plan, gov) pairs; `p_same_best` = share of scenario-bootstrap resamples that pick the same pair (selection stability); `price_of_constraint` = objective above the unconstrained best.

| tau_integrity | tau_gini | best_config | objective | obj_lo | obj_hi | p_same_best | p_infeasible | runner_up | price_of_constraint |
|---|---|---|---|---|---|---|---|---|---|
| 0.800 | none | SEARCH/G0 | 1396.838 | 1250.807 | 1554.308 | 0.755 | 0.000 | SEARCH/Ggini | 0.000 |
| 0.800 | 0.450 | SEARCH/G0 | 1396.838 | 1250.807 | 1554.308 | 0.755 | 0.000 | SEARCH/Ggini | 0.000 |
| 0.800 | 0.400 | SEARCH/G0 | 1396.838 | 1250.807 | 1554.308 | 0.755 | 0.000 | SEARCH/Ggini | 0.000 |
| 0.800 | 0.350 | SEARCH/G0 | 1396.838 | 1250.338 | 1556.573 | 0.751 | 0.003 | SEARCH/Ggini | 0.000 |
| 0.900 | none | SEARCH/G0 | 1396.838 | 1254.933 | 1556.406 | 0.580 | 0.011 | SEARCH/Ggini | 0.000 |
| 0.900 | 0.450 | SEARCH/G0 | 1396.838 | 1254.933 | 1556.406 | 0.580 | 0.011 | SEARCH/Ggini | 0.000 |
| 0.900 | 0.400 | SEARCH/G0 | 1396.838 | 1254.933 | 1556.406 | 0.580 | 0.011 | SEARCH/Ggini | 0.000 |
| 0.900 | 0.350 | SEARCH/G0 | 1396.838 | 1254.909 | 1556.431 | 0.577 | 0.015 | SEARCH/Ggini | 0.000 |
| 0.950 | none | SEARCH/Gmsg | 1405.339 | 1298.008 | 1597.464 | 0.513 | 0.415 | SEARCH/G0 | 8.501 |
| 0.950 | 0.450 | SEARCH/Gmsg | 1405.339 | 1298.008 | 1597.464 | 0.513 | 0.415 | SEARCH/G0 | 8.501 |
| 0.950 | 0.400 | SEARCH/Gmsg | 1405.339 | 1298.008 | 1597.464 | 0.513 | 0.415 | SEARCH/G0 | 8.501 |
| 0.950 | 0.350 | SEARCH/Gmsg | 1405.339 | 1297.605 | 1605.211 | 0.509 | 0.419 | SEARCH/G0 | 8.501 |
| 0.980 | none | infeasible |  | 1353.241 | 1776.223 |  | 0.818 | SEARCH/Gmsg |  |
| 0.980 | 0.450 | infeasible |  | 1353.241 | 1776.223 |  | 0.818 | SEARCH/Gmsg |  |
| 0.980 | 0.400 | infeasible |  | 1353.241 | 1776.223 |  | 0.818 | SEARCH/Gmsg |  |
| 0.980 | 0.350 | infeasible |  | 1353.241 | 1776.223 |  | 0.818 | SEARCH/Gmsg |  |

![S7b trade-off](s7b_tradeoff.png)
