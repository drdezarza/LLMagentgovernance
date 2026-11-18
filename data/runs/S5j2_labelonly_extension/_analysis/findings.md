**Reviewer-response stage v2** (exploratory, built 2026-11-16 after the MDPI reviews of v14-2; not part of ANALYSIS_PLAN_v1). Reading rules fixed before any unit ran: reports/prereg/RR_PLAN_v2.md.


**Instrument validity** (S5b rules, unchanged: attacker valid submissions ≥ 80% of rounds, judge unresolved ≤ 10%, auditor invalid ≤ 10%): 72/72 done episodes eligible (expected 72); excluded: none.

**Pooled by governor, seeds 401-416** (bootstrap over episodes)

| governor | episodes | asr_per_round | asr_per_round_lo | asr_per_round_hi | asr_given_submission | asr_given_submission_lo | asr_given_submission_hi | audit_misclassification_rate | audit_misclassification_rate_lo | audit_misclassification_rate_hi | valid_submission_rate | cost_usd |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| audit | 48 | 0.154 | 0.108 | 0.206 | 0.155 | 0.109 | 0.206 | 0.012 | 0.006 | 0.018 | 0.997 | 8.509 |
| audit_memory_struct | 48 | 0.138 | 0.088 | 0.192 | 0.138 | 0.089 | 0.193 | 0.040 | 0.025 | 0.057 | 0.995 | 9.591 |
| audit_quarantine | 48 | 0.088 | 0.055 | 0.125 | 0.089 | 0.056 | 0.127 | 0.048 | 0.029 | 0.068 | 0.993 | 15.736 |

**Paired contrasts** (rotation × seed)

| contrast | reads_as | outcome | scope | n_pairs | delta | lo | hi | batch |
|---|---|---|---|---|---|---|---|---|
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | R1 | 16 | 0.000 | 0.000 | 0.000 | combined 401-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | R2 | 16 | -0.015 | -0.045 | 0.020 | combined 401-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | R3 | 16 | -0.132 | -0.200 | -0.062 | combined 401-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | pooled | 48 | -0.049 | -0.080 | -0.020 | combined 401-416 |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | R1 | 16 | -0.002 | -0.008 | 0.000 | combined 401-416 |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | R2 | 16 | -0.080 | -0.120 | -0.040 | combined 401-416 |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | R3 | 16 | 0.032 | -0.070 | 0.137 | combined 401-416 |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | pooled | 48 | -0.017 | -0.057 | 0.024 | combined 401-416 |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | R1 | 16 | -0.002 | -0.008 | 0.000 | combined 401-416 |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | R2 | 16 | -0.095 | -0.148 | -0.045 | combined 401-416 |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | R3 | 16 | -0.100 | -0.210 | -0.002 | combined 401-416 |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | pooled | 48 | -0.066 | -0.108 | -0.027 | combined 401-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | R1 | 16 | 0.028 | -0.022 | 0.075 | combined 401-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | R2 | 16 | -0.005 | -0.022 | 0.010 | combined 401-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | R3 | 16 | 0.002 | -0.008 | 0.012 | combined 401-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | pooled | 48 | 0.008 | -0.008 | 0.027 | combined 401-416 |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | R1 | 16 | 0.080 | 0.052 | 0.110 | combined 401-416 |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | R2 | 16 | 0.015 | 0.005 | 0.028 | combined 401-416 |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | R3 | 16 | -0.010 | -0.020 | -0.002 | combined 401-416 |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | pooled | 48 | 0.028 | 0.013 | 0.044 | combined 401-416 |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | R1 | 16 | 0.108 | 0.073 | 0.140 | combined 401-416 |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | R2 | 16 | 0.010 | 0.002 | 0.020 | combined 401-416 |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | R3 | 16 | -0.008 | -0.022 | 0.005 | combined 401-416 |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | pooled | 48 | 0.037 | 0.018 | 0.056 | combined 401-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | R1 | 8 | 0.000 | 0.000 | 0.000 | new seeds 409-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | R2 | 8 | -0.045 | -0.080 | -0.010 | new seeds 409-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | R3 | 8 | -0.115 | -0.195 | -0.045 | new seeds 409-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | pooled | 24 | -0.053 | -0.088 | -0.022 | new seeds 409-416 |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | R1 | 8 | 0.000 | 0.000 | 0.000 | new seeds 409-416 |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | R2 | 8 | -0.110 | -0.165 | -0.045 | new seeds 409-416 |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | R3 | 8 | 0.015 | -0.110 | 0.120 | new seeds 409-416 |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | pooled | 24 | -0.032 | -0.082 | 0.017 | new seeds 409-416 |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | R1 | 8 | 0.000 | 0.000 | 0.000 | new seeds 409-416 |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | R2 | 8 | -0.155 | -0.215 | -0.100 | new seeds 409-416 |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | R3 | 8 | -0.100 | -0.260 | 0.035 | new seeds 409-416 |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | pooled | 24 | -0.085 | -0.148 | -0.028 | new seeds 409-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | R1 | 8 | 0.030 | -0.065 | 0.125 | new seeds 409-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | R2 | 8 | -0.015 | -0.040 | 0.010 | new seeds 409-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | R3 | 8 | -0.005 | -0.015 | 0.000 | new seeds 409-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | pooled | 24 | 0.003 | -0.030 | 0.038 | new seeds 409-416 |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | R1 | 8 | 0.075 | 0.030 | 0.120 | new seeds 409-416 |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | R2 | 8 | 0.025 | 0.005 | 0.045 | new seeds 409-416 |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | R3 | 8 | -0.005 | -0.015 | 0.000 | new seeds 409-416 |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | pooled | 24 | 0.032 | 0.012 | 0.055 | new seeds 409-416 |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | R1 | 8 | 0.105 | 0.050 | 0.155 | new seeds 409-416 |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | R2 | 8 | 0.010 | 0.000 | 0.025 | new seeds 409-416 |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | R3 | 8 | -0.010 | -0.030 | 0.000 | new seeds 409-416 |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | pooled | 24 | 0.035 | 0.010 | 0.065 | new seeds 409-416 |
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
- **combined 401-416** R-J1 tags − label-only, ASR: **lower (resolved)** (Δ -0.049 [-0.080, -0.020], n = 48 pairs); R-J2 misclassification: **equivalent within ±0.10** (Δ +0.008 [-0.008, +0.027], n = 48 pairs); R-J3 label-only − plain audit misclassification: Δ +0.028 [+0.013, +0.044], n = 48 pairs.
- **new seeds 409-416** R-J1 tags − label-only, ASR: **lower (resolved)** (Δ -0.053 [-0.088, -0.022], n = 24 pairs); R-J2 misclassification: **equivalent within ±0.10** (Δ +0.003 [-0.030, +0.038], n = 24 pairs); R-J3 label-only − plain audit misclassification: Δ +0.032 [+0.012, +0.055], n = 24 pairs.
- Rotation dependence (combined, tags − label-only ASR): R1 +0.000 [+0.000, +0.000]; R2 -0.015 [-0.045, +0.020]; R3 -0.133 [-0.200, -0.062].

- Consequence (fixed): if the combined R-J1 is not 'lower (resolved)', the paper says tags show no demonstrated blocking advantage over label-only memory; if resolved but a rotation has the opposite sign, it says the advantage is rotation-dependent. No further extension.