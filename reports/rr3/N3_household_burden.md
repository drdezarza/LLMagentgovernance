# N3: household- and subgroup-level curtailment burden (RR_PLAN_v3; no API calls)

All 40 households per cell, including households with no request. Recomputed realized Gini matches the recorded curtail_gini in 300/300 cells. Flexible energy = 24 h of max(0, true net load) × curtailable share, regenerated from the simulator seeds; saved household attributes match the regenerated ones in every cell. Means over cells; contrasts paired by scenario block, plans averaged, bootstrap 5000 / seed 42.

**S7b_C: burden distribution by governor** (cell means)

| metric | G0 | Gmsg |
|---|---|---|
| realized_zero_share | 0.138 | 0.138 |
| realized_mean_kwh | 41.294 | 41.416 |
| realized_p90_kwh | 81.466 | 81.790 |
| realized_max_kwh | 113.051 | 113.982 |
| realized_top10_share | 0.244 | 0.244 |
| realized_gini | 0.385 | 0.387 |
| realized_mean_share_flex | 0.132 | 0.133 |
| realized_p90_share_flex | 0.225 | 0.226 |
| realized_max_share_flex | 0.288 | 0.288 |
| realized_over50_flex | 0.000 | 0.000 |
| requested_zero_share | 0.106 | 0.106 |
| requested_p90_kwh | 137.263 | 137.356 |
| requested_max_kwh | 165.805 | 165.660 |
| requested_top10_share | 0.190 | 0.189 |
| requested_gini | 0.291 | 0.291 |
| requested_max_share_flex | 0.369 | 0.369 |
| requested_over50_flex | 0.000 | 0.000 |

**S7b_C: governor − G0** (selected metrics)

| contrast | metric | Δ | 95% interval | verdict |
|---|---|---|---|---|
| Gmsg - G0 | requested_max_share_flex | +0.000 | [-0.000, +0.000] | unresolved |
| Gmsg - G0 | realized_zero_share | +0.000 | [+0.000, +0.000] | unresolved |
| Gmsg - G0 | realized_p90_kwh | +0.323 | [-0.314, +0.913] | unresolved |
| Gmsg - G0 | realized_max_kwh | +0.931 | [-0.005, +2.155] | unresolved |
| Gmsg - G0 | realized_top10_share | +0.001 | [-0.001, +0.002] | unresolved |
| Gmsg - G0 | realized_gini | +0.002 | [+0.000, +0.003] | higher (resolved) |
| Gmsg - G0 | realized_max_share_flex | +0.000 | [-0.001, +0.001] | unresolved |
| Gmsg - G0 | realized_over50_flex | +0.000 | [+0.000, +0.000] | unresolved |
| Gmsg - G0 | realized_archetype_maxmin_ratio | +0.000 | [-0.038, +0.041] | unresolved |
| Gmsg - G0 | realized_lateral_maxmin_ratio | +0.026 | [-0.005, +0.063] | unresolved |
| Gmsg - G0 | realized_depth_band_maxmin_ratio | +0.003 | [-0.005, +0.010] | unresolved |
| Gmsg - G0 | realized_total_kwh | +4.863 | [-2.718, +12.457] | unresolved |

**S7b_C: mean realized kWh per household by subgroup**

| dimension | level | G0 | Gmsg |
|---|---|---|---|
| archetype | conformist | 43.96 | 44.35 |
| archetype | idealist | 48.95 | 49.43 |
| archetype | opportunist | 35.10 | 35.01 |
| archetype | pragmatist | 38.02 | 37.81 |
| archetype | skeptic | 40.15 | 40.26 |
| archetype | strategist | 42.01 | 42.01 |
| depth_band | 1-3 | 38.11 | 38.12 |
| depth_band | 4-7 | 41.51 | 41.60 |
| depth_band | 8-10 | 44.18 | 44.46 |
| lateral | 0 | 39.39 | 39.41 |
| lateral | 1 | 47.36 | 47.93 |
| lateral | 2 | 40.70 | 40.60 |
| lateral | 3 | 37.72 | 37.72 |

**S7b_mechanism_ablation: burden distribution by governor** (cell means)

| metric | G0 | Gmsg | Gcap | Ggini | G1r |
|---|---|---|---|---|---|
| realized_zero_share | 0.107 | 0.108 | 0.108 | 0.018 | 0.020 |
| realized_mean_kwh | 41.916 | 41.837 | 39.839 | 41.560 | 39.359 |
| realized_p90_kwh | 81.334 | 81.464 | 77.135 | 79.460 | 75.624 |
| realized_max_kwh | 118.811 | 118.793 | 114.168 | 115.998 | 111.346 |
| realized_top10_share | 0.245 | 0.246 | 0.245 | 0.239 | 0.241 |
| realized_gini | 0.387 | 0.388 | 0.388 | 0.368 | 0.371 |
| realized_mean_share_flex | 0.135 | 0.135 | 0.128 | 0.135 | 0.128 |
| realized_p90_share_flex | 0.233 | 0.234 | 0.223 | 0.227 | 0.216 |
| realized_max_share_flex | 0.283 | 0.283 | 0.270 | 0.281 | 0.269 |
| realized_over50_flex | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| requested_zero_share | 0.079 | 0.079 | 0.079 | 0.000 | 0.000 |
| requested_p90_kwh | 137.011 | 137.030 | 130.180 | 133.724 | 126.877 |
| requested_max_kwh | 165.200 | 165.227 | 157.260 | 160.522 | 152.787 |
| requested_top10_share | 0.186 | 0.186 | 0.187 | 0.180 | 0.181 |
| requested_gini | 0.287 | 0.287 | 0.288 | 0.266 | 0.267 |
| requested_max_share_flex | 0.368 | 0.368 | 0.350 | 0.359 | 0.341 |
| requested_over50_flex | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

**S7b_mechanism_ablation: governor − G0** (selected metrics)

| contrast | metric | Δ | 95% interval | verdict |
|---|---|---|---|---|
| Gmsg - G0 | requested_max_share_flex | +0.000 | [-0.000, +0.000] | unresolved |
| Gcap - G0 | requested_max_share_flex | -0.018 | [-0.020, -0.017] | lower (resolved) |
| Ggini - G0 | requested_max_share_flex | -0.009 | [-0.012, -0.007] | lower (resolved) |
| G1r - G0 | requested_max_share_flex | -0.027 | [-0.031, -0.024] | lower (resolved) |
| Gmsg - G0 | realized_zero_share | +0.001 | [+0.000, +0.002] | unresolved |
| Gcap - G0 | realized_zero_share | +0.001 | [-0.002, +0.004] | unresolved |
| Ggini - G0 | realized_zero_share | -0.089 | [-0.100, -0.076] | lower (resolved) |
| G1r - G0 | realized_zero_share | -0.087 | [-0.099, -0.075] | lower (resolved) |
| Gmsg - G0 | realized_p90_kwh | +0.130 | [-0.161, +0.494] | unresolved |
| Gcap - G0 | realized_p90_kwh | -4.199 | [-5.334, -3.389] | lower (resolved) |
| Ggini - G0 | realized_p90_kwh | -1.874 | [-4.731, +1.379] | unresolved |
| G1r - G0 | realized_p90_kwh | -5.710 | [-7.773, -3.541] | lower (resolved) |
| Gmsg - G0 | realized_max_kwh | -0.018 | [-0.084, +0.026] | unresolved |
| Gcap - G0 | realized_max_kwh | -4.643 | [-6.150, -3.186] | lower (resolved) |
| Ggini - G0 | realized_max_kwh | -2.813 | [-4.735, -0.772] | lower (resolved) |
| G1r - G0 | realized_max_kwh | -7.464 | [-10.433, -4.619] | lower (resolved) |
| Gmsg - G0 | realized_top10_share | +0.001 | [-0.000, +0.003] | unresolved |
| Gcap - G0 | realized_top10_share | +0.001 | [-0.000, +0.001] | unresolved |
| Ggini - G0 | realized_top10_share | -0.005 | [-0.012, +0.000] | unresolved |
| G1r - G0 | realized_top10_share | -0.004 | [-0.011, +0.003] | unresolved |
| Gmsg - G0 | realized_gini | +0.001 | [-0.000, +0.003] | unresolved |
| Gcap - G0 | realized_gini | +0.001 | [-0.001, +0.003] | unresolved |
| Ggini - G0 | realized_gini | -0.019 | [-0.030, -0.010] | lower (resolved) |
| G1r - G0 | realized_gini | -0.016 | [-0.028, -0.004] | lower (resolved) |
| Gmsg - G0 | realized_max_share_flex | +0.000 | [-0.000, +0.000] | unresolved |
| Gcap - G0 | realized_max_share_flex | -0.013 | [-0.016, -0.011] | lower (resolved) |
| Ggini - G0 | realized_max_share_flex | -0.002 | [-0.008, +0.003] | unresolved |
| G1r - G0 | realized_max_share_flex | -0.014 | [-0.021, -0.009] | lower (resolved) |
| Gmsg - G0 | realized_over50_flex | +0.000 | [+0.000, +0.000] | unresolved |
| Gcap - G0 | realized_over50_flex | +0.000 | [+0.000, +0.000] | unresolved |
| Ggini - G0 | realized_over50_flex | +0.000 | [+0.000, +0.000] | unresolved |
| G1r - G0 | realized_over50_flex | +0.000 | [+0.000, +0.000] | unresolved |
| Gmsg - G0 | realized_archetype_maxmin_ratio | -0.017 | [-0.058, +0.016] | unresolved |
| Gcap - G0 | realized_archetype_maxmin_ratio | -0.090 | [-0.308, +0.028] | unresolved |
| Ggini - G0 | realized_archetype_maxmin_ratio | -1.017 | [-2.269, -0.107] | lower (resolved) |
| G1r - G0 | realized_archetype_maxmin_ratio | -1.023 | [-2.290, -0.095] | lower (resolved) |
| Gmsg - G0 | realized_lateral_maxmin_ratio | +0.005 | [-0.015, +0.024] | unresolved |
| Gcap - G0 | realized_lateral_maxmin_ratio | +0.005 | [-0.020, +0.029] | unresolved |
| Ggini - G0 | realized_lateral_maxmin_ratio | -0.039 | [-0.218, +0.128] | unresolved |
| G1r - G0 | realized_lateral_maxmin_ratio | -0.017 | [-0.177, +0.143] | unresolved |
| Gmsg - G0 | realized_depth_band_maxmin_ratio | -0.002 | [-0.014, +0.010] | unresolved |
| Gcap - G0 | realized_depth_band_maxmin_ratio | -0.002 | [-0.012, +0.005] | unresolved |
| Ggini - G0 | realized_depth_band_maxmin_ratio | -0.020 | [-0.052, +0.011] | unresolved |
| G1r - G0 | realized_depth_band_maxmin_ratio | -0.013 | [-0.054, +0.034] | unresolved |
| Gmsg - G0 | realized_total_kwh | -3.148 | [-8.550, +1.883] | unresolved |
| Gcap - G0 | realized_total_kwh | -83.058 | [-95.786, -71.380] | lower (resolved) |
| Ggini - G0 | realized_total_kwh | -14.236 | [-74.384, +49.985] | unresolved |
| G1r - G0 | realized_total_kwh | -102.255 | [-159.582, -44.535] | lower (resolved) |

**S7b_mechanism_ablation: mean realized kWh per household by subgroup**

| dimension | level | G0 | Gmsg | Gcap | Ggini | G1r |
|---|---|---|---|---|---|---|
| archetype | conformist | 37.42 | 37.31 | 36.01 | 37.13 | 35.84 |
| archetype | idealist | 51.02 | 51.26 | 48.66 | 51.75 | 49.30 |
| archetype | opportunist | 37.86 | 37.41 | 35.68 | 36.73 | 34.42 |
| archetype | pragmatist | 44.53 | 44.51 | 42.30 | 44.70 | 42.16 |
| archetype | skeptic | 35.25 | 35.22 | 33.42 | 33.69 | 31.77 |
| archetype | strategist | 42.75 | 42.57 | 40.50 | 43.01 | 40.28 |
| depth_band | 1-3 | 35.96 | 35.79 | 34.23 | 36.06 | 34.03 |
| depth_band | 4-7 | 44.99 | 44.88 | 42.62 | 44.38 | 42.07 |
| depth_band | 8-10 | 43.77 | 43.83 | 41.74 | 43.30 | 41.08 |
| lateral | 0 | 37.20 | 37.07 | 35.54 | 35.67 | 34.06 |
| lateral | 1 | 47.84 | 47.64 | 45.60 | 48.47 | 45.70 |
| lateral | 2 | 43.77 | 43.74 | 41.42 | 43.33 | 40.92 |
| lateral | 3 | 38.86 | 38.90 | 36.80 | 38.78 | 36.75 |

