51 scenario x seed units (17 scenarios, 7 families); held-out families: compliance_drift, feeder_structure. Backbone `deepseek-ai/DeepSeek-V4-Pro-0813`. Objective = upstream objective + latency price x decision latency; a strategy is feasible if it never missed the control deadline.

**Best fixed strategy on training families**: SEARCH (mean relative regret by mode: PREDEFINED 0.22, SEQUENTIAL 0.25, HIERARCHICAL 1.09, SEARCH 0.19)

**Best feasible forced strategy per scenario** (count over seeds)

| split | family | scenario | HIERARCHICAL | PREDEFINED | SEARCH | SEQUENTIAL |
|---|---|---|---|---|---|---|
| heldout | compliance_drift | drift30 | 0 | 0 | 2 | 1 |
| heldout | compliance_drift | resist50_drift15 | 0 | 1 | 2 | 0 |
| heldout | feeder_structure | feeder_seed3 | 0 | 0 | 3 | 0 |
| heldout | feeder_structure | long3x14 | 0 | 0 | 3 | 0 |
| heldout | feeder_structure | tightcap_weak | 0 | 0 | 2 | 1 |
| heldout | feeder_structure | wide6x7 | 0 | 0 | 3 | 0 |
| train | baseline | base | 0 | 0 | 3 | 0 |
| train | deadline_cost | deadline4_lat20 | 2 | 1 | 0 | 0 |
| train | deadline_cost | deadline6_lat60 | 0 | 3 | 0 | 0 |
| train | deadline_cost | lat120 | 0 | 3 | 0 | 0 |
| train | forecast_shift | bias_over15 | 0 | 1 | 2 | 0 |
| train | forecast_shift | bias_under15 | 0 | 0 | 3 | 0 |
| train | forecast_shift | noise25 | 0 | 0 | 3 | 0 |
| train | search_budget | branch2 | 0 | 0 | 2 | 1 |
| train | search_budget | branch2_lat30 | 0 | 1 | 2 | 0 |
| train | telemetry | telemetry20 | 0 | 0 | 2 | 1 |
| train | telemetry | telemetry40 | 0 | 0 | 2 | 1 |

**Mean adjusted objective by scenario and mode** (lower is better)

| scenario | obj_PREDEFINED | obj_SEQUENTIAL | obj_HIERARCHICAL | obj_SEARCH |
|---|---|---|---|---|
| base | 1641.500 | 1628.400 | 2453.700 | 1468.400 |
| bias_over15 | 1353.400 | 1358.500 | 2103.900 | 1319.800 |
| bias_under15 | 2815.900 | 2851.200 | 3391.400 | 2445.600 |
| branch2 | 1641.500 | 1628.400 | 2453.700 | 1513.900 |
| branch2_lat30 | 1671.500 | 2044.400 | 3984.600 | 1596.400 |
| deadline4_lat20 | 1661.500 | 1905.800 | 1568.900 | 1905.800 |
| deadline6_lat60 | 1701.500 | 2460.400 | 5515.500 | 1798.400 |
| drift30 | 3848.500 | 3848.700 | 4306.200 | 3828.900 |
| feeder_seed3 | 2859.600 | 2860.600 | 4581.700 | 2485.300 |
| lat120 | 1761.500 | 3292.400 | 8577.300 | 2128.400 |
| long3x14 | 31989.300 | 31708.500 | 37324.400 | 29678.700 |
| noise25 | 1817.400 | 1798.400 | 2407.500 | 1614.500 |
| resist50_drift15 | 2548.000 | 2538.200 | 3344.200 | 2463.200 |
| telemetry20 | 2867.400 | 1712.100 | 2506.800 | 2770.400 |
| telemetry40 | 2867.400 | 1818.900 | 2481.300 | 2770.400 |
| tightcap_weak | 4470.500 | 4423.600 | 7131.700 | 4337.400 |
| wide6x7 | 1764.000 | 1733.900 | 2452.500 | 1582.800 |

**S8 gate** (share of scenario-seeds where the best strategy differs from the fixed one; cluster bootstrap over scenarios)

| split | measure | share | lo | hi | n_scenario_seeds | n_scenarios | exact_lo | exact_hi | scen_any | scen_exact_hi |
|---|---|---|---|---|---|---|---|---|---|---|
| train | changed | 0.424 | 0.212 | 0.667 | 33 | 11 | 0.255 | 0.608 | 8.000 | 0.940 |
| train | meaningful | 0.333 | 0.152 | 0.545 | 33 | 11 | 0.180 | 0.518 | 7.000 | 0.891 |
| heldout | changed | 0.167 | 0.056 | 0.278 | 18 | 6 | 0.036 | 0.414 | 3.000 | 0.882 |
| heldout | meaningful | 0.000 | 0.000 | 0.000 | 18 | 6 | 0.000 | 0.185 | 0.000 | 0.459 |

**Leave-one-family-out** (fixed strategy chosen on the other families)

| family | fixed_from_others | n | share_changed | share_meaningful | mean_rel_gain_of_switching |
|---|---|---|---|---|---|
| baseline | SEARCH | 3 | 0.000 | 0.000 | 0.000 |
| compliance_drift | SEARCH | 6 | 0.333 | 0.000 | 0.005 |
| deadline_cost | SEQUENTIAL | 9 | 1.000 | 1.000 | 0.548 |
| feeder_structure | SEARCH | 12 | 0.083 | 0.000 | 0.003 |
| forecast_shift | SEARCH | 9 | 0.111 | 0.000 | 0.001 |
| search_budget | SEARCH | 6 | 0.333 | 0.333 | 0.025 |
| telemetry | SEARCH | 6 | 0.333 | 0.333 | 0.761 |

**Selector baselines** (regret vs the per-scenario best feasible strategy; `rule` = PREDEFINED when latency is priced or the deadline cannot fit SEARCH, else SEARCH)

| split | selector | mean_regret | mean_rel_regret | n |
|---|---|---|---|---|
| train | fixed:SEARCH | 293.769 | 0.194 | 33 |
| train | rule | 236.235 | 0.159 | 33 |
| train | oracle | 0.000 | 0.000 | 33 |
| heldout | fixed:SEARCH | 13.420 | 0.004 | 18 |
| heldout | rule | 13.420 | 0.004 | 18 |
| heldout | oracle | 0.000 | 0.000 | 18 |

- A learned controller (S8) must beat `rule`, not only the fixed strategy.

- Declared ≠ executed strategy in 6/204 mode-episodes (2 of them are scenario winners: deadline4_lat20-s7 HIERARCHICAL→SEARCH, deadline4_lat20-s13 HIERARCHICAL→SEARCH). These winners are architecture-plus-fallback policies (deadline downgrade), not the declared architecture; `modes_all.csv` has both labels.

- Gate: **FAIL** (held-out meaningful-change share lower CI ≥ 0.15). S8 may be built only on PASS (REVIEWER §3a).
- `exact_lo/hi`: Clopper-Pearson over scenario-seeds; `scen_exact_hi`: the same over scenarios (the independent unit). A held-out share of 0 is compatible with a true rate up to `scen_exact_hi`.
- One backbone and 3 seeds per scenario: shares describe this bank, not all feeders. Do not retune the bank against these held-out scenarios; a redesigned bank needs a fresh held-out set.