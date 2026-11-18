**Reviewer-response stage v2** (exploratory, built 2026-11-16 after the MDPI reviews of v14-2; not part of ANALYSIS_PLAN_v1). Reading rules fixed before any unit ran: reports/prereg/RR_PLAN_v2.md.


**Instrument validity** (S5b rules, unchanged: attacker valid submissions ≥ 80% of rounds, judge unresolved ≤ 10%, auditor invalid ≤ 10%): 67/67 done episodes eligible (expected 72); excluded: none.

**Pooled by governor, seeds 401-416** (bootstrap over episodes)

| governor | episodes | asr_per_round | asr_per_round_lo | asr_per_round_hi | asr_given_submission | asr_given_submission_lo | asr_given_submission_hi | audit_misclassification_rate | audit_misclassification_rate_lo | audit_misclassification_rate_hi | valid_submission_rate | cost_usd |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| audit | 47 | 0.155 | 0.106 | 0.207 | 0.155 | 0.107 | 0.207 | 0.012 | 0.006 | 0.019 | 0.997 | 8.419 |
| audit_memory_struct | 46 | 0.130 | 0.083 | 0.182 | 0.130 | 0.083 | 0.183 | 0.039 | 0.023 | 0.057 | 0.995 | 9.284 |
| audit_quarantine | 46 | 0.086 | 0.052 | 0.123 | 0.087 | 0.053 | 0.124 | 0.050 | 0.030 | 0.071 | 0.994 | 15.333 |

**Paired contrasts** (rotation × seed)

| contrast | reads_as | outcome | scope | n_pairs | delta | lo | hi | batch |
|---|---|---|---|---|---|---|---|---|
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | R1 | 16 | 0.000 | 0.000 | 0.000 | combined 401-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | R2 | 15 | -0.011 | -0.040 | 0.024 | combined 401-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | R3 | 15 | -0.123 | -0.195 | -0.051 | combined 401-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | pooled | 46 | -0.043 | -0.077 | -0.016 | combined 401-416 |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | R1 | 16 | -0.002 | -0.008 | 0.000 | combined 401-416 |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | R2 | 15 | -0.085 | -0.125 | -0.045 | combined 401-416 |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | R3 | 15 | 0.035 | -0.075 | 0.147 | combined 401-416 |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | pooled | 46 | -0.017 | -0.058 | 0.024 | combined 401-416 |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | R1 | 16 | -0.002 | -0.008 | 0.000 | combined 401-416 |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | R2 | 15 | -0.096 | -0.147 | -0.043 | combined 401-416 |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | R3 | 15 | -0.088 | -0.200 | 0.016 | combined 401-416 |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | pooled | 46 | -0.061 | -0.106 | -0.023 | combined 401-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | R1 | 16 | 0.028 | -0.022 | 0.075 | combined 401-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | R2 | 15 | 0.000 | -0.013 | 0.016 | combined 401-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | R3 | 15 | 0.003 | -0.008 | 0.013 | combined 401-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | pooled | 46 | 0.010 | -0.008 | 0.029 | combined 401-416 |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | R1 | 16 | 0.080 | 0.052 | 0.110 | combined 401-416 |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | R2 | 15 | 0.011 | 0.003 | 0.019 | combined 401-416 |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | R3 | 15 | -0.011 | -0.019 | -0.003 | combined 401-416 |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | pooled | 46 | 0.028 | 0.012 | 0.044 | combined 401-416 |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | R1 | 16 | 0.108 | 0.073 | 0.140 | combined 401-416 |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | R2 | 15 | 0.011 | 0.003 | 0.021 | combined 401-416 |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | R3 | 15 | -0.008 | -0.024 | 0.005 | combined 401-416 |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | pooled | 46 | 0.038 | 0.019 | 0.058 | combined 401-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | R1 | 8 | 0.000 | 0.000 | 0.000 | new seeds 409-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | R2 | 7 | -0.040 | -0.080 | 0.000 | new seeds 409-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | R3 | 7 | -0.091 | -0.166 | -0.023 | new seeds 409-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | pooled | 22 | -0.042 | -0.075 | -0.015 | new seeds 409-416 |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | R1 | 8 | 0.000 | 0.000 | 0.000 | new seeds 409-416 |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | R2 | 7 | -0.126 | -0.183 | -0.057 | new seeds 409-416 |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | R3 | 7 | 0.017 | -0.131 | 0.137 | new seeds 409-416 |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | pooled | 22 | -0.035 | -0.089 | 0.018 | new seeds 409-416 |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | R1 | 8 | 0.000 | 0.000 | 0.000 | new seeds 409-416 |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | R2 | 7 | -0.166 | -0.234 | -0.103 | new seeds 409-416 |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | R3 | 7 | -0.074 | -0.263 | 0.069 | new seeds 409-416 |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | pooled | 22 | -0.076 | -0.144 | -0.020 | new seeds 409-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | R1 | 8 | 0.030 | -0.065 | 0.125 | new seeds 409-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | R2 | 7 | -0.006 | -0.029 | 0.017 | new seeds 409-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | R3 | 7 | -0.006 | -0.017 | 0.000 | new seeds 409-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | pooled | 22 | 0.007 | -0.027 | 0.045 | new seeds 409-416 |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | R1 | 8 | 0.075 | 0.030 | 0.120 | new seeds 409-416 |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | R2 | 7 | 0.017 | 0.006 | 0.034 | new seeds 409-416 |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | R3 | 7 | -0.006 | -0.017 | 0.000 | new seeds 409-416 |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | pooled | 22 | 0.031 | 0.009 | 0.055 | new seeds 409-416 |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | R1 | 8 | 0.105 | 0.050 | 0.155 | new seeds 409-416 |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | R2 | 7 | 0.011 | 0.000 | 0.023 | new seeds 409-416 |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | R3 | 7 | -0.011 | -0.034 | 0.000 | new seeds 409-416 |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | pooled | 22 | 0.038 | 0.011 | 0.071 | new seeds 409-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | R1 | 8 | 0.000 | 0.000 | 0.000 | S5j 401-408 (pre-specified) |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | R2 | 8 | 0.015 | -0.025 | 0.065 | S5j 401-408 (pre-specified) |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | R3 | 8 | -0.150 | -0.265 | -0.025 | S5j 401-408 (pre-specified) |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | pooled | 24 | -0.045 | -0.098 | 0.003 | S5j 401-408 (pre-specified) |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | R1 | 8 | -0.005 | -0.015 | 0.000 | S5j 401-408 (pre-specified) |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | R2 | 8 | -0.050 | -0.090 | -0.010 | S5j 401-408 (pre-specified) |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | R3 | 8 | 0.050 | -0.120 | 0.235 | S5j 401-408 (pre-specified) |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | pooled | 24 | -0.002 | -0.060 | 0.065 | S5j 401-408 (pre-specified) |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | R1 | 8 | -0.005 | -0.015 | 0.000 | S5j 401-408 (pre-specified) |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | R2 | 8 | -0.035 | -0.090 | 0.015 | S5j 401-408 (pre-specified) |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | R3 | 8 | -0.100 | -0.245 | 0.035 | S5j 401-408 (pre-specified) |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | pooled | 24 | -0.047 | -0.105 | 0.002 | S5j 401-408 (pre-specified) |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | R1 | 8 | 0.025 | -0.000 | 0.050 | S5j 401-408 (pre-specified) |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | R2 | 8 | 0.005 | -0.010 | 0.020 | S5j 401-408 (pre-specified) |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | R3 | 8 | 0.010 | -0.010 | 0.025 | S5j 401-408 (pre-specified) |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | pooled | 24 | 0.013 | 0.000 | 0.027 | S5j 401-408 (pre-specified) |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | R1 | 8 | 0.085 | 0.050 | 0.120 | S5j 401-408 (pre-specified) |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | R2 | 8 | 0.005 | 0.000 | 0.015 | S5j 401-408 (pre-specified) |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | R3 | 8 | -0.015 | -0.030 | -0.005 | S5j 401-408 (pre-specified) |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | pooled | 24 | 0.025 | 0.005 | 0.048 | S5j 401-408 (pre-specified) |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | R1 | 8 | 0.110 | 0.070 | 0.150 | S5j 401-408 (pre-specified) |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | R2 | 8 | 0.010 | 0.000 | 0.025 | S5j 401-408 (pre-specified) |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | R3 | 8 | -0.005 | -0.025 | 0.015 | S5j 401-408 (pre-specified) |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | pooled | 24 | 0.038 | 0.013 | 0.067 | S5j 401-408 (pre-specified) |

**Reading (RR_PLAN_v2)**

- **S5j 401-408 (pre-specified)** R-J1 tags − label-only, ASR: **unresolved** (Δ -0.045 [-0.098, +0.003], n = 24 pairs); R-J2 misclassification: **equivalent within ±0.10** (Δ +0.013 [+0.000, +0.027], n = 24 pairs); R-J3 label-only − plain audit misclassification: Δ +0.025 [+0.005, +0.048], n = 24 pairs.
- **combined 401-416** R-J1 tags − label-only, ASR: **lower (resolved)** (Δ -0.043 [-0.077, -0.016], n = 46 pairs); R-J2 misclassification: **equivalent within ±0.10** (Δ +0.010 [-0.008, +0.029], n = 46 pairs); R-J3 label-only − plain audit misclassification: Δ +0.028 [+0.012, +0.044], n = 46 pairs.
- **new seeds 409-416** R-J1 tags − label-only, ASR: **lower (resolved)** (Δ -0.042 [-0.075, -0.015], n = 22 pairs); R-J2 misclassification: **equivalent within ±0.10** (Δ +0.007 [-0.027, +0.045], n = 22 pairs); R-J3 label-only − plain audit misclassification: Δ +0.031 [+0.009, +0.055], n = 22 pairs.
- Rotation dependence (combined, tags − label-only ASR): R1 +0.000 [+0.000, +0.000]; R2 -0.011 [-0.040, +0.024]; R3 -0.123 [-0.195, -0.051].

- Consequence (fixed): if the combined R-J1 is not 'lower (resolved)', the paper says tags show no demonstrated blocking advantage over label-only memory; if resolved but a rotation has the opposite sign, it says the advantage is rotation-dependent. No further extension.