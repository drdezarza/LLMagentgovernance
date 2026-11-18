**Exploratory follow-up** (requested by the co-author, built 2026-10-29 after the freeze; not part of ANALYSIS_PLAN_v1). The reading rules below were fixed before any unit of this stage ran.

**Instrument validity** (S7b rules, unchanged): 360/360 cells eligible (expected 360); excluded: none.
Non-response levels 0%, 20%, 40%: a fixed, nested random subset of households never responds (no curtailment, does not read the message); the operator is not told who. Scenarios, rotations and plans are those of S7b_C (the 0 % cells reproduce S7b_C). CIs: bootstrap over scenarios (clusters), 5000 resamples, seed 42; 15 scenarios.

**Means by non-response level × governance** (pooled over plans and scenarios)

| nonresponse | gov | objective | violation_hours | mean_compliance | curtailed_kwh | content_integrity | manipulation_rate |
|---|---|---|---|---|---|---|---|
| 0.000 | G0 | 2119.578 | 6.917 | 0.530 | 1651.452 | 0.865 | 0.100 |
| 0.000 | Gmsg | 2111.070 | 6.933 | 0.532 | 1655.797 | 0.945 | 0.034 |
| 0.200 | G0 | 2852.931 | 7.583 | 0.357 | 1134.390 | 0.865 | 0.100 |
| 0.200 | Gmsg | 2849.302 | 7.583 | 0.357 | 1133.018 | 0.945 | 0.034 |
| 0.400 | G0 | 3549.671 | 7.733 | 0.230 | 739.202 | 0.865 | 0.100 |
| 0.400 | Gmsg | 3536.987 | 7.733 | 0.232 | 743.649 | 0.945 | 0.034 |

**Objective by plan** (lower is better)

| ('plan', '') | (0.0, 'G0') | (0.0, 'Gmsg') | (0.2, 'G0') | (0.2, 'Gmsg') | (0.4, 'G0') | (0.4, 'Gmsg') |
|---|---|---|---|---|---|---|
| HIERARCHICAL | 2595.500 | 2595.400 | 3257.200 | 3259.600 | 3882.100 | 3882.800 |
| SEARCH | 1725.500 | 1726.900 | 2493.200 | 2500.000 | 3214.000 | 3218.500 |
| SEQUENTIAL | 1614.100 | 1617.600 | 2439.900 | 2441.500 | 3246.100 | 3234.400 |
| natural | 2543.200 | 2504.300 | 3221.400 | 3196.100 | 3856.600 | 3812.300 |

**Effects** (pooled over plans; per-plan rows in nonresponse_effects.csv)

| outcome | nonresponse | plan | contrast | n_scen | delta | lo | hi |
|---|---|---|---|---|---|---|---|
| objective | 0.000 | all | Gmsg-G0 | 15 | -8.509 | -17.811 | -0.470 |
| objective | 0.200 | all | Gmsg-G0 | 15 | -3.629 | -12.758 | 5.848 |
| objective | 0.200 | all | (Gmsg-G0) at 20% minus at 0% | 15 | 4.880 | -0.754 | 10.562 |
| objective | 0.400 | all | Gmsg-G0 | 15 | -12.684 | -22.271 | -5.017 |
| objective | 0.400 | all | (Gmsg-G0) at 40% minus at 0% | 15 | -4.175 | -13.503 | 4.088 |
| objective | 0.200 | all | G0: 20% minus 0% (manipulation check) | 15 | 733.353 | 657.067 | 801.409 |
| objective | 0.400 | all | G0: 40% minus 0% (manipulation check) | 15 | 1430.092 | 1322.873 | 1526.018 |
| objective | 0.200 | all | Gmsg: 20% minus 0% (manipulation check) | 15 | 738.233 | 663.436 | 805.028 |
| objective | 0.400 | all | Gmsg: 40% minus 0% (manipulation check) | 15 | 1425.917 | 1317.476 | 1521.975 |
| violation_hours | 0.000 | all | Gmsg-G0 | 15 | 0.017 | 0.000 | 0.050 |
| violation_hours | 0.200 | all | Gmsg-G0 | 15 | 0.000 | 0.000 | 0.000 |
| violation_hours | 0.200 | all | (Gmsg-G0) at 20% minus at 0% | 15 | -0.017 | -0.050 | 0.000 |
| violation_hours | 0.400 | all | Gmsg-G0 | 15 | 0.000 | 0.000 | 0.000 |
| violation_hours | 0.400 | all | (Gmsg-G0) at 40% minus at 0% | 15 | -0.017 | -0.050 | 0.000 |
| violation_hours | 0.200 | all | G0: 20% minus 0% (manipulation check) | 15 | 0.667 | 0.400 | 0.967 |
| violation_hours | 0.400 | all | G0: 40% minus 0% (manipulation check) | 15 | 0.817 | 0.567 | 1.083 |
| violation_hours | 0.200 | all | Gmsg: 20% minus 0% (manipulation check) | 15 | 0.650 | 0.383 | 0.950 |
| violation_hours | 0.400 | all | Gmsg: 40% minus 0% (manipulation check) | 15 | 0.800 | 0.550 | 1.067 |
| mean_compliance | 0.000 | all | Gmsg-G0 | 15 | 0.002 | -0.001 | 0.006 |
| mean_compliance | 0.200 | all | Gmsg-G0 | 15 | -0.000 | -0.004 | 0.003 |
| mean_compliance | 0.200 | all | (Gmsg-G0) at 20% minus at 0% | 15 | -0.002 | -0.005 | -0.000 |
| mean_compliance | 0.400 | all | Gmsg-G0 | 15 | 0.002 | 0.000 | 0.004 |
| mean_compliance | 0.400 | all | (Gmsg-G0) at 40% minus at 0% | 15 | -0.000 | -0.002 | 0.002 |
| mean_compliance | 0.200 | all | G0: 20% minus 0% (manipulation check) | 15 | -0.172 | -0.187 | -0.156 |
| mean_compliance | 0.400 | all | G0: 40% minus 0% (manipulation check) | 15 | -0.299 | -0.320 | -0.278 |
| mean_compliance | 0.200 | all | Gmsg: 20% minus 0% (manipulation check) | 15 | -0.175 | -0.189 | -0.159 |
| mean_compliance | 0.400 | all | Gmsg: 40% minus 0% (manipulation check) | 15 | -0.299 | -0.320 | -0.279 |
| curtailed_kwh | 0.000 | all | Gmsg-G0 | 15 | 4.345 | -2.492 | 11.473 |
| curtailed_kwh | 0.200 | all | Gmsg-G0 | 15 | -1.372 | -9.361 | 4.809 |
| curtailed_kwh | 0.200 | all | (Gmsg-G0) at 20% minus at 0% | 15 | -5.717 | -9.779 | -1.905 |
| curtailed_kwh | 0.400 | all | Gmsg-G0 | 15 | 4.447 | 0.210 | 9.189 |
| curtailed_kwh | 0.400 | all | (Gmsg-G0) at 40% minus at 0% | 15 | 0.102 | -5.646 | 6.302 |
| curtailed_kwh | 0.200 | all | G0: 20% minus 0% (manipulation check) | 15 | -517.062 | -570.792 | -453.789 |
| curtailed_kwh | 0.400 | all | G0: 40% minus 0% (manipulation check) | 15 | -912.250 | -988.602 | -824.864 |
| curtailed_kwh | 0.200 | all | Gmsg: 20% minus 0% (manipulation check) | 15 | -522.779 | -576.171 | -459.104 |
| curtailed_kwh | 0.400 | all | Gmsg: 40% minus 0% (manipulation check) | 15 | -912.148 | -989.576 | -824.449 |
| content_integrity | 0.000 | all | Gmsg-G0 | 15 | 0.080 | 0.044 | 0.116 |
| content_integrity | 0.200 | all | Gmsg-G0 | 15 | 0.080 | 0.044 | 0.116 |
| content_integrity | 0.200 | all | (Gmsg-G0) at 20% minus at 0% | 15 | 0.000 | 0.000 | 0.000 |
| content_integrity | 0.400 | all | Gmsg-G0 | 15 | 0.080 | 0.044 | 0.116 |
| content_integrity | 0.400 | all | (Gmsg-G0) at 40% minus at 0% | 15 | 0.000 | 0.000 | 0.000 |
| content_integrity | 0.200 | all | G0: 20% minus 0% (manipulation check) | 15 | 0.000 | 0.000 | 0.000 |
| content_integrity | 0.400 | all | G0: 40% minus 0% (manipulation check) | 15 | 0.000 | 0.000 | 0.000 |
| content_integrity | 0.200 | all | Gmsg: 20% minus 0% (manipulation check) | 15 | 0.000 | 0.000 | 0.000 |
| content_integrity | 0.400 | all | Gmsg: 40% minus 0% (manipulation check) | 15 | 0.000 | 0.000 | 0.000 |
| manipulation_rate | 0.000 | all | Gmsg-G0 | 15 | -0.067 | -0.097 | -0.036 |
| manipulation_rate | 0.200 | all | Gmsg-G0 | 15 | -0.067 | -0.097 | -0.036 |
| manipulation_rate | 0.200 | all | (Gmsg-G0) at 20% minus at 0% | 15 | 0.000 | 0.000 | 0.000 |
| manipulation_rate | 0.400 | all | Gmsg-G0 | 15 | -0.067 | -0.097 | -0.036 |
| manipulation_rate | 0.400 | all | (Gmsg-G0) at 40% minus at 0% | 15 | 0.000 | 0.000 | 0.000 |
| manipulation_rate | 0.200 | all | G0: 20% minus 0% (manipulation check) | 15 | 0.000 | 0.000 | 0.000 |
| manipulation_rate | 0.400 | all | G0: 40% minus 0% (manipulation check) | 15 | 0.000 | 0.000 | 0.000 |
| manipulation_rate | 0.200 | all | Gmsg: 20% minus 0% (manipulation check) | 15 | 0.000 | 0.000 | 0.000 |
| manipulation_rate | 0.400 | all | Gmsg: 40% minus 0% (manipulation check) | 15 | 0.000 | 0.000 | 0.000 |

**Reading** (fixed 2026-10-29, before any unit: the advantage holds at a level if Gmsg − G0 on the objective has 95% upper bound < Δ = 25 AND content integrity has lower bound > 0, as C5a/C5b; 'not shown' is not evidence of a cost; the 'minus at 0 %' rows say whether the effect changes)

| nonresponse | objective_delta | objective_hi | C5a-type (hi < Δ) | integrity_delta | integrity_lo | C5b-type (lo > 0) | advantage_holds | n_scen |
|---|---|---|---|---|---|---|---|---|
| 0.000 | -8.509 | -0.470 | non-inferior | 0.080 | 0.044 | higher | True | 15 |
| 0.200 | -3.629 | 5.848 | non-inferior | 0.080 | 0.044 | higher | True | 15 |
| 0.400 | -12.684 | -5.017 | non-inferior | 0.080 | 0.044 | higher | True | 15 |

- The manipulation-check rows must show that non-response worsens G0 (objective/violation hours up, compliance down); otherwise the levels did not make coordination less favourable.
- Exploratory; per-plan rows are descriptive (SEQUENTIAL and the natural planner were the plans with the largest audit cost/benefit in S7b/S7b_C).