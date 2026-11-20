# N2: margin and objective-weight sensitivity of the feeder non-inferiority result (RR_PLAN_v3; no API calls)

Recorded outcomes re-scored as overload + w_v × voltage violation + w_c × curtailed kWh (frozen w_v = 4000, w_c = 0.25; recomputing the frozen objective from its terms reproduces it to 9.1e-13). Audit − Baseline, plans averaged within scenario, 15 scenarios, bootstrap 5000 / seed 42. The upper limit is the smallest margin the data support.

**S7b_C (pooled): upper 95% limit of Audit − Baseline** (rows w_v, columns w_c)

| w_v \ w_c | 0.0 | 0.1 | 0.25 | 0.5 | 1.0 |
|---|---|---|---|---|---|
| 1000 | +1.8 | +1.5 | +1.1 | +0.5 | -0.2 |
| 2000 | +0.9 | +0.6 | +0.3 | -0.3 | -0.8 |
| 4000 | -0.6 | -0.8 | -1.1 | -1.7 | -1.8 |
| 8000 | -2.9 | -3.3 | -3.5 | -3.8 | -3.8 |
| 16000 | -7.3 | -7.4 | -7.5 | -7.6 | -7.6 |

- Non-inferior at the frozen 25-unit margin in 25/25 weight pairs; the largest upper limit is +1.8 (w_v 1000, w_c 0.0), 0.1% of the Baseline mean. At the frozen weights the upper limit is -1.1 (-0.05% of the Baseline mean).
- Margins: non-inferior in 25/25 pairs at 10, 25/25 pairs at 15, 25/25 pairs at 25, 25/25 pairs at 50.

Per plan at the frozen weights (S7b_C; descriptive)

| plan | Δ | 95% interval |
|---|---|---|
| HIERARCHICAL | +0.7 | [-6.4, +6.5] |
| SEARCH | -15.6 | [-31.6, -2.8] |
| SEQUENTIAL | +10.3 | [+2.4, +19.1] |
| natural | -36.6 | [-71.7, -8.8] |

**S7c_nonresponse (pooled): upper 95% limit of Audit − Baseline** (rows w_v, columns w_c)

| w_v \ w_c | 0.0 | 0.1 | 0.25 | 0.5 | 1.0 |
|---|---|---|---|---|---|
| 1000 | +2.2 | +1.9 | +1.6 | +1.0 | -0.2 |
| 2000 | +1.5 | +1.2 | +0.9 | +0.3 | -0.8 |
| 4000 | +0.1 | -0.1 | -0.5 | -1.0 | -1.8 |
| 8000 | -2.3 | -2.5 | -2.8 | -3.2 | -3.9 |
| 16000 | -6.7 | -6.8 | -7.0 | -7.6 | -8.0 |

- Non-inferior at the frozen 25-unit margin in 25/25 weight pairs; the largest upper limit is +2.2 (w_v 1000, w_c 0.0), 0.2% of the Baseline mean. At the frozen weights the upper limit is -0.5 (-0.02% of the Baseline mean).
- Margins: non-inferior in 25/25 pairs at 10, 25/25 pairs at 15, 25/25 pairs at 25, 25/25 pairs at 50.

Per plan at the frozen weights (S7c_nonresponse; descriptive)

| plan | Δ | 95% interval |
|---|---|---|
| HIERARCHICAL | -0.0 | [-6.6, +5.3] |
| SEARCH | +1.4 | [-1.4, +4.1] |
| SEQUENTIAL | +3.5 | [-2.6, +9.7] |
| natural | -38.9 | [-73.3, -12.2] |

**Audit − Baseline content integrity by plan** (descriptive)

| study | plan | Δ integrity | 95% interval |
|---|---|---|---|
| S7b_C | all | +0.078 | [+0.042, +0.113] |
| S7b_C | HIERARCHICAL | +0.025 | [+0.006, +0.050] |
| S7b_C | SEARCH | +0.025 | [+0.006, +0.050] |
| S7b_C | SEQUENTIAL | +0.014 | [-0.008, +0.042] |
| S7b_C | natural | +0.247 | [+0.117, +0.383] |
| S7c_nonresponse | all | +0.080 | [+0.044, +0.116] |
| S7c_nonresponse | HIERARCHICAL | +0.025 | [+0.006, +0.050] |
| S7c_nonresponse | SEARCH | +0.025 | [+0.006, +0.050] |
| S7c_nonresponse | SEQUENTIAL | +0.025 | [+0.006, +0.050] |
| S7c_nonresponse | natural | +0.244 | [+0.114, +0.381] |
