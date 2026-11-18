**Reviewer-response stage v2** (exploratory, built 2026-11-16 after the MDPI reviews of v14-2; not part of ANALYSIS_PLAN_v1). Reading rules fixed before any unit ran: reports/prereg/RR_PLAN_v2.md.

240 cells done (240 eligible: judge resolved ≥ 90% of messages) over 24 scenarios (expected 240 cells / 24 scenarios).

**Cell means** (plan, variant e=escalation f=feedback, governance)

| plan | variant | gov | objective | overload | voltage | curtailment | curtailed_kwh | gov_household_capped | mean_compliance | revisions |
|---|---|---|---|---|---|---|---|---|---|---|
| SEARCH | e0f0 | G0 | 1789.500 | 995.400 | 329.700 | 464.400 | 1857.500 |  | 0.500 | 0.000 |
| SEARCH | e0f0 | Gcap | 1832.600 | 1037.800 | 340.400 | 454.400 | 1817.600 | 0.000 | 0.500 | 0.000 |
| SEARCH | e0f1 | G0 | 1643.200 | 913.400 | 238.500 | 491.300 | 1965.300 |  | 0.500 | 6.600 |
| SEARCH | e0f1 | Gcap | 1673.900 | 950.000 | 243.500 | 480.400 | 1921.600 | 2.600 | 0.500 | 6.900 |
| SEARCH | e1f0 | G0 | 1601.900 | 808.100 | 278.700 | 515.100 | 2060.300 |  | 0.500 | 0.000 |
| SEARCH | e1f0 | Gcap | 1858.400 | 1043.900 | 360.900 | 453.500 | 1814.200 | 203.000 | 0.500 | 0.000 |
| SEARCH | e1f1 | G0 | 1454.000 | 707.700 | 201.200 | 545.200 | 2180.700 |  | 0.500 | 6.500 |
| SEARCH | e1f1 | Gcap | 1718.600 | 959.100 | 280.300 | 479.300 | 1917.100 | 216.500 | 0.500 | 6.700 |
| SEQUENTIAL | e1f0 | G0 | 1614.400 | 891.700 | 226.900 | 495.800 | 1983.000 |  | 0.500 | 6.700 |
| SEQUENTIAL | e1f0 | Gcap | 1658.800 | 936.600 | 238.100 | 484.100 | 1936.500 | 2.400 | 0.500 | 6.700 |

**Paired contrasts** (by scenario; bootstrap 5000, seed 42; objective split into overload, voltage and curtailment terms, R-D4)

| contrast | outcome | n_pairs | delta | lo | hi |
|---|---|---|---|---|---|
| cap cost SEARCH e1f0 (Gcap − G0) | objective | 24 | 256.490 | 220.920 | 289.060 |
| cap cost SEARCH e1f0 (Gcap − G0) | overload | 24 | 235.830 | 204.780 | 264.590 |
| cap cost SEARCH e1f0 (Gcap − G0) | voltage | 24 | 82.180 | 64.430 | 99.880 |
| cap cost SEARCH e1f0 (Gcap − G0) | curtailment | 24 | -61.530 | -69.280 | -53.090 |
| cap cost SEARCH e0f0 (Gcap − G0) | objective | 24 | 43.130 | 16.970 | 71.660 |
| cap cost SEARCH e0f0 (Gcap − G0) | overload | 24 | 42.360 | 23.710 | 61.820 |
| cap cost SEARCH e0f0 (Gcap − G0) | voltage | 24 | 10.760 | -3.740 | 27.190 |
| cap cost SEARCH e0f0 (Gcap − G0) | curtailment | 24 | -9.990 | -14.840 | -5.120 |
| cap cost SEARCH e1f1 (Gcap − G0) | objective | 24 | 264.610 | 229.000 | 301.170 |
| cap cost SEARCH e1f1 (Gcap − G0) | overload | 24 | 251.380 | 233.380 | 269.850 |
| cap cost SEARCH e1f1 (Gcap − G0) | voltage | 24 | 79.120 | 55.030 | 104.450 |
| cap cost SEARCH e1f1 (Gcap − G0) | curtailment | 24 | -65.890 | -70.530 | -60.990 |
| cap cost SEARCH e0f1 (Gcap − G0) | objective | 24 | 30.710 | -2.260 | 62.150 |
| cap cost SEARCH e0f1 (Gcap − G0) | overload | 24 | 36.670 | 15.350 | 58.090 |
| cap cost SEARCH e0f1 (Gcap − G0) | voltage | 24 | 4.980 | -16.370 | 26.340 |
| cap cost SEARCH e0f1 (Gcap − G0) | curtailment | 24 | -10.940 | -16.220 | -5.590 |
| cap cost SEQUENTIAL (Gcap − G0) | objective | 24 | 44.400 | 25.690 | 65.080 |
| D1 = cap cost(e0f0) − cap cost(e1f0) | objective | 24 | -213.360 | -252.200 | -174.640 |
| D1 = cap cost(e0f0) − cap cost(e1f0) | overload | 24 | -193.470 | -226.160 | -159.850 |
| D1 = cap cost(e0f0) − cap cost(e1f0) | voltage | 24 | -71.430 | -92.510 | -51.040 |
| D1 = cap cost(e0f0) − cap cost(e1f0) | curtailment | 24 | 51.540 | 42.470 | 60.580 |
| SEARCH e0f0 − SEARCH e1f0 (what escalation buys, G0) | objective | 24 | 187.630 | 136.620 | 238.410 |
| SEARCH e0f0 − SEARCH e1f0 (what escalation buys, G0) | overload | 24 | 187.330 | 145.340 | 230.860 |
| SEARCH e0f0 − SEARCH e1f0 (what escalation buys, G0) | voltage | 24 | 50.980 | 21.760 | 78.490 |
| SEARCH e0f0 − SEARCH e1f0 (what escalation buys, G0) | curtailment | 24 | -50.680 | -63.860 | -38.540 |
| SEARCH e0f0 − SEQUENTIAL (lookahead without escalation, G0) | objective | 24 | 175.110 | 15.360 | 460.100 |
| SEARCH e0f0 − SEQUENTIAL (lookahead without escalation, G0) | overload | 24 | 103.700 | 14.940 | 251.700 |
| SEARCH e0f0 − SEQUENTIAL (lookahead without escalation, G0) | voltage | 24 | 102.790 | 7.100 | 277.350 |
| SEARCH e0f0 − SEQUENTIAL (lookahead without escalation, G0) | curtailment | 24 | -31.380 | -69.130 | -7.320 |
| SEARCH e1f0 − SEQUENTIAL (as in S7b/S7b_C, G0) | objective | 24 | -12.510 | -197.950 | 295.990 |
| SEARCH e1f0 − SEQUENTIAL (as in S7b/S7b_C, G0) | overload | 24 | -83.630 | -195.570 | 88.890 |
| SEARCH e1f0 − SEQUENTIAL (as in S7b/S7b_C, G0) | voltage | 24 | 51.810 | -54.420 | 234.430 |
| SEARCH e1f0 − SEQUENTIAL (as in S7b/S7b_C, G0) | curtailment | 24 | 19.310 | -25.040 | 49.920 |
| SEARCH e1f1 − SEARCH e1f0 (feedback, G0) | objective | 24 | -147.840 | -460.040 | 26.430 |
| SEARCH e1f1 − SEARCH e1f0 (feedback, G0) | overload | 24 | -100.420 | -271.360 | 1.490 |
| SEARCH e1f1 − SEARCH e1f0 (feedback, G0) | voltage | 24 | -77.520 | -262.550 | 22.520 |
| SEARCH e1f1 − SEARCH e1f0 (feedback, G0) | curtailment | 24 | 30.100 | 2.350 | 74.220 |
| SEARCH e1f1 − SEARCH e1f0 (feedback, G0) in the 5 scenarios SEQUENTIAL won | objective | 5 | -758.150 | -2170.990 | -30.270 |
| SEARCH e1f1 − SEARCH e1f0 (feedback, G0) in the 5 scenarios SEQUENTIAL won | overload | 5 | -438.950 | -1176.240 | -40.160 |
| SEARCH e1f1 − SEARCH e1f0 (feedback, G0) in the 5 scenarios SEQUENTIAL won | voltage | 5 | -430.780 | -1289.330 | -0.430 |
| SEARCH e1f1 − SEARCH e1f0 (feedback, G0) in the 5 scenarios SEQUENTIAL won | curtailment | 5 | 111.580 | 9.750 | 295.530 |
| SEARCH e1f1 − SEQUENTIAL (G0) in the 5 scenarios SEQUENTIAL won | objective | 5 | -28.480 | -177.750 | 66.160 |
| SEARCH e1f1 − SEQUENTIAL (G0) in the 5 scenarios SEQUENTIAL won | overload | 5 | -66.550 | -163.230 | 15.070 |
| SEARCH e1f1 − SEQUENTIAL (G0) in the 5 scenarios SEQUENTIAL won | voltage | 5 | 21.890 | -60.050 | 93.550 |
| SEARCH e1f1 − SEQUENTIAL (G0) in the 5 scenarios SEQUENTIAL won | curtailment | 5 | 16.180 | -6.970 | 42.490 |
| SEARCH e1f1 − SEARCH e1f0 (feedback, G0) without R3-sc3015 | objective | 23 | 1.390 | -28.350 | 33.450 |
| SEARCH e1f1 − SEARCH e1f0 (feedback, G0) without R3-sc3015 | overload | 23 | -21.690 | -51.480 | 9.260 |
| SEARCH e1f1 − SEARCH e1f0 (feedback, G0) without R3-sc3015 | voltage | 23 | 12.470 | 1.070 | 25.530 |
| SEARCH e1f1 − SEARCH e1f0 (feedback, G0) without R3-sc3015 | curtailment | 23 | 10.600 | 0.050 | 22.630 |
| SEARCH e1f1 − SEARCH e1f0 (feedback, G0) in the 4 scenarios SEQUENTIAL won, without R3-sc3015 | objective | 4 | -52.640 | -87.070 | -18.220 |
| SEARCH e1f1 − SEARCH e1f0 (feedback, G0) in the 4 scenarios SEQUENTIAL won, without R3-sc3015 | overload | 4 | -70.850 | -119.220 | -22.480 |
| SEARCH e1f1 − SEARCH e1f0 (feedback, G0) in the 4 scenarios SEQUENTIAL won, without R3-sc3015 | voltage | 4 | -1.630 | -3.360 | -0.040 |
| SEARCH e1f1 − SEARCH e1f0 (feedback, G0) in the 4 scenarios SEQUENTIAL won, without R3-sc3015 | curtailment | 4 | 19.840 | 5.250 | 34.420 |

**Reading (RR_PLAN_v2)**

- **R-D0** 54/66 default cells reproduce the S7b / S7b_C objective to 1e-6 (largest deviation 92.4).
- **R-D1** cap cost on SEARCH: escalation on +256.490 [+220.916, +289.060], off +43.134 [+16.974, +71.665]; D1 -213.356 [-252.204, -174.637], n = 24; capped household requests with escalation off: 0. **Escalation explains the cap cost** (share explained 83%).
- **R-D2a** SEARCH e0f0 − SEARCH e1f0 (what escalation buys, G0): **higher (resolved)** (+187.625 [+136.622, +238.412], n = 24).
- **R-D2b** SEARCH e0f0 − SEQUENTIAL (lookahead without escalation, G0): **higher (resolved)** (+175.112 [+15.360, +460.096], n = 24).
- **R-D3** SEARCH e1f1 − SEARCH e1f0 (feedback, G0): **unresolved** (-147.843 [-460.037, +26.425], n = 24).
- **R-D3 (subset/sensitivity)** SEARCH e1f1 − SEARCH e1f0 (feedback, G0) in the 5 scenarios SEQUENTIAL won: **lower (resolved)** (-758.153 [-2170.985, -30.265], n = 5).
- **R-D3 (subset/sensitivity)** SEARCH e1f1 − SEQUENTIAL (G0) in the 5 scenarios SEQUENTIAL won: **unresolved** (-28.478 [-177.749, +66.158], n = 5).
- **R-D3 (subset/sensitivity)** SEARCH e1f1 − SEARCH e1f0 (feedback, G0) without R3-sc3015: **unresolved** (+1.390 [-28.354, +33.454], n = 23).
- **R-D3 (subset/sensitivity)** SEARCH e1f1 − SEARCH e1f0 (feedback, G0) in the 4 scenarios SEQUENTIAL won, without R3-sc3015: **lower (resolved)** (-52.642 [-87.066, -18.218], n = 4).

- Consequence (fixed): a mechanism is stated in the paper only for a resolved rule; otherwise the P1 traces are reported as consistent with, not establishing, it.
- 24 scenarios over 3 backbone rotations: these runs only.