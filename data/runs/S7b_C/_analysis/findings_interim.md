**Confirmatory stage** (pre-registered in reports/prereg/ANALYSIS_PLAN_v1.md; frozen 2026-10-23). Decision rules below were fixed before any unit of this stage ran.

**Instrument validity** (pre-specified): 37/37 cells eligible (judge unresolved ≤ 10%, auditor invalid ≤ 10%); excluded: none.
37 cells over 6 independent scenarios (3 complete); rotations R1: backbone deepseek_v4_pro, auditor minimax_m3, judge glm53; R2: backbone minimax_m3, auditor glm53, judge deepseek_v4_pro; R3: backbone glm53, auditor deepseek_v4_pro, judge minimax_m3.
Integrity = rubric-judged content integrity (factual and non-manipulative; urgency matching a real, stated overload is clean). Messages state the measured overload, the forecast, or a precautionary reason, never '0 kW over'. CIs: bootstrap over scenarios (clusters); n = 3 scenarios per backbone describes these runs only.

**Judge instrument** (A2, rubric prompt vs the AI-assisted human labels, feeder messages; n ≈ 31 decided, not a population accuracy)

| alias | n_decided | agreement | kappa | tpr_vs_human | fpr_vs_human |
|---|---|---|---|---|---|
| deepseek_v4_pro | 31 | 0.903 | 0.739 | 0.667 | 0.000 |
| glm53 | 31 | 1.000 | 1.000 | 1.000 | 0.000 |
| minimax_m3 | 31 | 0.968 | 0.919 | 0.889 | 0.000 |

- Judge unresolved: 0.3% of messages (excluded; bounds in cells.csv). Auditor invalid (fail-closed): 0 audits.
- Messages without a measured overload (forecast/precautionary): 67%; their content integrity 0.96 vs all messages 0.93.

**Objective by plan x governance** (lower is better)

| plan | G0 | Gmsg |
|---|---|---|
| HIERARCHICAL | 2721.8 | 2723.6 |
| SEARCH | 1580.0 | 1532.6 |
| SEQUENTIAL | 1630.5 | 1642.2 |
| natural | 2556.2 | 2546.5 |

**Content integrity by plan x governance**

| plan | G0 | Gmsg |
|---|---|---|
| HIERARCHICAL | 0.943 | 0.957 |
| SEARCH | 0.958 | 0.986 |
| SEQUENTIAL | 0.950 | 0.951 |
| natural | 0.653 | 0.889 |

**Mechanism effects on objective** (vs G0, paired by scenario, 95% cluster CI; non-additivity = G1r − Gmsg − Gcap − Ggini + 2·G0)

| plan | Gmsg-G0 |
|---|---|
| HIERARCHICAL | +1.9 [-15.9, +15.3] |
| SEARCH | -37.2 [-79.7, +0.0] |
| SEQUENTIAL | +11.7 [-4.4, +26.7] |
| all | -1.9 [-16.4, +12.2] |
| natural | -9.7 [-60.1, +18.8] |

**Mechanism effects on content_integrity** (vs G0, paired by scenario, 95% cluster CI; non-additivity = G1r − Gmsg − Gcap − Ggini + 2·G0)

| plan | Gmsg-G0 |
|---|---|
| HIERARCHICAL | +0.014 [+0.000, +0.028] |
| SEARCH | +0.014 [+0.000, +0.042] |
| SEQUENTIAL | +0.001 [-0.017, +0.021] |
| all | +0.037 [-0.002, +0.095] |
| natural | +0.236 [+0.000, +0.625] |

**Mechanism effects on factual_rate** (vs G0, paired by scenario, 95% cluster CI; non-additivity = G1r − Gmsg − Gcap − Ggini + 2·G0)

| plan | Gmsg-G0 |
|---|---|
| HIERARCHICAL | +0.014 [+0.000, +0.028] |
| SEARCH | +0.014 [+0.000, +0.042] |
| SEQUENTIAL | +0.001 [-0.017, +0.021] |
| all | +0.037 [-0.002, +0.095] |
| natural | +0.236 [+0.000, +0.625] |

**Mechanism effects on manipulation_rate** (vs G0, paired by scenario, 95% cluster CI; non-additivity = G1r − Gmsg − Gcap − Ggini + 2·G0)

| plan | Gmsg-G0 |
|---|---|
| HIERARCHICAL | -0.014 [-0.028, +0.000] |
| SEARCH | -0.014 [-0.042, +0.000] |
| SEQUENTIAL | +0.006 [-0.021, +0.039] |
| all | -0.025 [-0.069, +0.013] |
| natural | -0.167 [-0.417, +0.000] |

**Mechanism effects on urgency_fear_framing** (vs G0, paired by scenario, 95% cluster CI; non-additivity = G1r − Gmsg − Gcap − Ggini + 2·G0)

| plan | Gmsg-G0 |
|---|---|
| HIERARCHICAL | -0.028 [-0.090, +0.014] |
| SEARCH | -0.014 [-0.042, +0.000] |
| SEQUENTIAL | -0.028 [-0.090, +0.021] |
| all | -0.004 [-0.076, +0.052] |
| natural | +0.167 [-0.042, +0.292] |

**Mechanism effects on curtail_gini** (vs G0, paired by scenario, 95% cluster CI; non-additivity = G1r − Gmsg − Gcap − Ggini + 2·G0)

| plan | Gmsg-G0 |
|---|---|
| HIERARCHICAL | +0.000 [-0.002, +0.002] |
| SEARCH | +0.002 [-0.005, +0.010] |
| SEQUENTIAL | +0.006 [+0.002, +0.009] |
| all | +0.003 [+0.001, +0.005] |
| natural | +0.000 [-0.007, +0.005] |

**Mechanism effects on violation_hours** (vs G0, paired by scenario, 95% cluster CI; non-additivity = G1r − Gmsg − Gcap − Ggini + 2·G0)

| plan | Gmsg-G0 |
|---|---|
| HIERARCHICAL | +0.00 [+0.00, +0.00] |
| SEARCH | +0.00 [+0.00, +0.00] |
| SEQUENTIAL | +0.00 [+0.00, +0.00] |
| all | +0.00 [+0.00, +0.00] |
| natural | +0.00 [+0.00, +0.00] |

- Pooled effects whose CI excludes 0: Gmsg-G0 on curtail_gini +0.00299; Gmsg-G0 on backlash_rate +0.00584.
- Non-additive (pooled, CI excludes 0): none.

**plan x gov interaction** (complete scenarios only)

| outcome | n_blocks | share_plan | share_gov | share_int | share_int_lo | share_int_hi | p_int |
|---|---|---|---|---|---|---|---|
| objective | 3 | 0.819 | 0.000 | 0.000 | 0.000 | 0.001 | 0.999 |
| violation_hours | 3 | 0.333 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 |
| mean_compliance | 3 | 0.865 | 0.000 | 0.011 | 0.001 | 0.087 | 0.735 |
| curtail_gini | 3 | 0.983 | 0.000 | 0.000 | 0.000 | 0.001 | 0.999 |
| content_integrity | 3 | 0.373 | 0.049 | 0.108 | 0.013 | 0.288 | 0.390 |

**Mechanism effects by rotation** (mean over that rotation's scenarios; a sign flip across rotations points to a model effect, not a mechanism effect)

| outcome | contrast | R1 | R2 | R3 |
|---|---|---|---|---|
| content_integrity | Gmsg-G0 | 0.031 | 0.000 | 0.080 |
| objective | Gmsg-G0 | -2.536 | 17.033 | -20.152 |

**Constrained performance**: minimise the objective subject to mean content integrity ≥ τ_I and mean curtailment Gini ≤ τ_G, over all (plan, gov) pairs; `p_same_best` = share of scenario-bootstrap resamples that pick the same pair (selection stability); `price_of_constraint` = objective above the unconstrained best.

| tau_integrity | tau_gini | best_config | objective | obj_lo | obj_hi | p_same_best | p_infeasible | runner_up | price_of_constraint |
|---|---|---|---|---|---|---|---|---|---|
| 0.800 | none | SEARCH/Gmsg | 1532.582 | 1035.901 | 2023.916 | 0.966 | 0.000 | SEQUENTIAL/G0 | 0.000 |
| 0.800 | 0.450 | SEARCH/Gmsg | 1532.582 | 1035.901 | 2023.916 | 0.966 | 0.000 | SEQUENTIAL/G0 | 0.000 |
| 0.800 | 0.400 | SEARCH/Gmsg | 1532.582 | 1035.901 | 2023.916 | 0.966 | 0.000 | SEQUENTIAL/G0 | 0.000 |
| 0.800 | 0.350 | SEARCH/Gmsg | 1532.582 | 1035.901 | 2023.916 | 0.937 | 0.000 | SEQUENTIAL/G0 | 0.000 |
| 0.900 | none | SEARCH/Gmsg | 1532.582 | 1035.901 | 2023.916 | 0.966 | 0.000 | SEQUENTIAL/G0 | 0.000 |
| 0.900 | 0.450 | SEARCH/Gmsg | 1532.582 | 1035.901 | 2023.916 | 0.966 | 0.000 | SEQUENTIAL/G0 | 0.000 |
| 0.900 | 0.400 | SEARCH/Gmsg | 1532.582 | 1035.901 | 2023.916 | 0.966 | 0.000 | SEQUENTIAL/G0 | 0.000 |
| 0.900 | 0.350 | SEARCH/Gmsg | 1532.582 | 1035.901 | 2023.916 | 0.937 | 0.000 | SEQUENTIAL/G0 | 0.000 |
| 0.950 | none | SEARCH/Gmsg | 1532.582 | 1035.901 | 2023.916 | 0.966 | 0.000 | SEQUENTIAL/G0 | 0.000 |
| 0.950 | 0.450 | SEARCH/Gmsg | 1532.582 | 1035.901 | 2023.916 | 0.966 | 0.000 | SEQUENTIAL/G0 | 0.000 |
| 0.950 | 0.400 | SEARCH/Gmsg | 1532.582 | 1035.901 | 2023.916 | 0.966 | 0.000 | SEQUENTIAL/G0 | 0.000 |
| 0.950 | 0.350 | SEARCH/Gmsg | 1532.582 | 1035.901 | 2023.916 | 0.937 | 0.000 | SEQUENTIAL/G0 | 0.000 |
| 0.980 | none | SEARCH/Gmsg | 1532.582 | 1362.421 | 2023.916 | 0.703 | 0.263 | SEQUENTIAL/G0 | 0.000 |
| 0.980 | 0.450 | SEARCH/Gmsg | 1532.582 | 1362.421 | 2023.916 | 0.703 | 0.263 | SEQUENTIAL/G0 | 0.000 |
| 0.980 | 0.400 | SEARCH/Gmsg | 1532.582 | 1362.421 | 2023.916 | 0.703 | 0.263 | SEQUENTIAL/G0 | 0.000 |
| 0.980 | 0.350 | SEARCH/Gmsg | 1532.582 | 1362.421 | 2023.916 | 0.674 | 0.263 | SEQUENTIAL/G0 | 0.000 |

![S7b trade-off](s7b_tradeoff.png)


---

## C5 read-out (frozen rules: pooled over the 4 plans, scenario = cluster, 95% percentile bootstrap, 5000 resamples, seed 42; Δ_obj = 25 objective units)

| hypothesis | plan | outcome | n_scen | delta | lo | hi | verdict |
|---|---|---|---|---|---|---|---|
| C5a | SEQUENTIAL | objective | 6 | 11.691 | -4.377 | 26.685 | per-plan (descriptive) |
| C5a | HIERARCHICAL | objective | 6 | 1.866 | -15.935 | 15.256 | per-plan (descriptive) |
| C5a | SEARCH | objective | 3 | -37.162 | -79.674 | 0.000 | per-plan (descriptive) |
| C5a | natural | objective | 3 | -9.715 | -60.074 | 18.825 | per-plan (descriptive) |
| C5a | all | objective | 6 | -1.885 | -16.402 | 12.152 | supported |
| C5b | SEQUENTIAL | content_integrity | 6 | 0.001 | -0.017 | 0.021 | per-plan (descriptive) |
| C5b | HIERARCHICAL | content_integrity | 6 | 0.014 | 0.000 | 0.028 | per-plan (descriptive) |
| C5b | SEARCH | content_integrity | 3 | 0.014 | 0.000 | 0.042 | per-plan (descriptive) |
| C5b | natural | content_integrity | 3 | 0.236 | 0.000 | 0.625 | per-plan (descriptive) |
| C5b | all | content_integrity | 6 | 0.037 | -0.002 | 0.095 | not supported |

- C5a is a non-inferiority claim: 'not shown' is NOT evidence of a cost, and a CI containing 0 is never read as 'no cost'. Per-plan rows are descriptive (the natural planner had SD ≈ 45 in S7b).
- Expected scenarios: 15; a verdict is final only when every cell is done and eligible.