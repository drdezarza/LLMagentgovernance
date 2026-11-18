**Reviewer-response stage v2** (exploratory, built 2026-11-16 after the MDPI reviews of v14-2; not part of ANALYSIS_PLAN_v1). Reading rules fixed before any unit ran: reports/prereg/RR_PLAN_v2.md.


**Instrument validity** (S5b rules, unchanged: attacker valid submissions ≥ 80% of rounds, judge unresolved ≤ 10%, auditor invalid ≤ 10%): 39/39 done episodes eligible (expected 72); excluded: none.

**Pooled by governor, seeds 401-416** (bootstrap over episodes)

| governor | episodes | asr_per_round | asr_per_round_lo | asr_per_round_hi | asr_given_submission | asr_given_submission_lo | asr_given_submission_hi | audit_misclassification_rate | audit_misclassification_rate_lo | audit_misclassification_rate_hi | valid_submission_rate | cost_usd |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| audit | 38 | 0.133 | 0.084 | 0.187 | 0.133 | 0.085 | 0.188 | 0.007 | 0.002 | 0.014 | 0.996 | 6.950 |
| audit_memory_struct | 38 | 0.129 | 0.074 | 0.191 | 0.130 | 0.074 | 0.191 | 0.041 | 0.024 | 0.062 | 0.994 | 7.788 |
| audit_quarantine | 35 | 0.091 | 0.051 | 0.134 | 0.092 | 0.052 | 0.135 | 0.039 | 0.023 | 0.058 | 0.993 | 11.655 |

**Paired contrasts** (rotation × seed)

| contrast | reads_as | outcome | scope | n_pairs | delta | lo | hi | batch |
|---|---|---|---|---|---|---|---|---|
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | R1 | 12 | 0.000 | 0.000 | 0.000 | combined 401-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | R2 | 12 | 0.003 | -0.027 | 0.040 | combined 401-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | R3 | 11 | -0.142 | -0.229 | -0.051 | combined 401-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | pooled | 35 | -0.043 | -0.083 | -0.008 | combined 401-416 |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | R1 | 13 | -0.003 | -0.009 | 0.000 | combined 401-416 |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | R2 | 13 | -0.074 | -0.117 | -0.031 | combined 401-416 |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | R3 | 12 | 0.073 | -0.047 | 0.193 | combined 401-416 |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | pooled | 38 | -0.003 | -0.047 | 0.044 | combined 401-416 |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | R1 | 12 | -0.003 | -0.010 | 0.000 | combined 401-416 |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | R2 | 12 | -0.060 | -0.103 | -0.013 | combined 401-416 |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | R3 | 11 | -0.062 | -0.189 | 0.047 | combined 401-416 |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | pooled | 35 | -0.041 | -0.085 | -0.001 | combined 401-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | R1 | 12 | -0.007 | -0.053 | 0.033 | combined 401-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | R2 | 12 | -0.007 | -0.023 | 0.010 | combined 401-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | R3 | 11 | 0.007 | -0.007 | 0.022 | combined 401-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | pooled | 35 | -0.002 | -0.021 | 0.013 | combined 401-416 |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | R1 | 13 | 0.095 | 0.068 | 0.123 | combined 401-416 |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | R2 | 13 | 0.012 | 0.003 | 0.022 | combined 401-416 |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | R3 | 12 | -0.010 | -0.020 | 0.000 | combined 401-416 |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | pooled | 38 | 0.034 | 0.017 | 0.052 | combined 401-416 |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | R1 | 12 | 0.087 | 0.050 | 0.123 | combined 401-416 |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | R2 | 12 | 0.007 | 0.000 | 0.017 | combined 401-416 |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | R3 | 11 | -0.004 | -0.018 | 0.011 | combined 401-416 |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | pooled | 35 | 0.031 | 0.013 | 0.050 | combined 401-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | R1 | 4 | 0.000 | 0.000 | 0.000 | new seeds 409-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | R2 | 4 | -0.020 | -0.060 | 0.020 | new seeds 409-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | R3 | 3 | -0.120 | -0.240 | -0.040 | new seeds 409-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | asr_per_round | pooled | 11 | -0.040 | -0.087 | -0.004 | new seeds 409-416 |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | R1 | 5 | 0.000 | 0.000 | 0.000 | new seeds 409-416 |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | R2 | 5 | -0.112 | -0.192 | -0.032 | new seeds 409-416 |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | R3 | 4 | 0.120 | 0.040 | 0.200 | new seeds 409-416 |
| audit_memory_struct - audit | label-only memory vs no memory | asr_per_round | pooled | 14 | -0.006 | -0.069 | 0.057 | new seeds 409-416 |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | R1 | 4 | 0.000 | 0.000 | 0.000 | new seeds 409-416 |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | R2 | 4 | -0.110 | -0.170 | -0.060 | new seeds 409-416 |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | R3 | 3 | 0.040 | -0.160 | 0.160 | new seeds 409-416 |
| audit_quarantine - audit | tag memory vs no memory | asr_per_round | pooled | 11 | -0.029 | -0.091 | 0.033 | new seeds 409-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | R1 | 4 | -0.070 | -0.160 | 0.020 | new seeds 409-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | R2 | 4 | -0.030 | -0.040 | -0.010 | new seeds 409-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | R3 | 3 | 0.000 | 0.000 | 0.000 | new seeds 409-416 |
| audit_quarantine - audit_memory_struct | tags vs label-only (incremental value of tags) | audit_misclassification_rate | pooled | 11 | -0.036 | -0.076 | -0.004 | new seeds 409-416 |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | R1 | 5 | 0.112 | 0.072 | 0.152 | new seeds 409-416 |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | R2 | 5 | 0.024 | 0.008 | 0.040 | new seeds 409-416 |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | R3 | 4 | 0.000 | 0.000 | 0.000 | new seeds 409-416 |
| audit_memory_struct - audit | label-only memory vs no memory | audit_misclassification_rate | pooled | 14 | 0.049 | 0.020 | 0.080 | new seeds 409-416 |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | R1 | 4 | 0.040 | -0.010 | 0.080 | new seeds 409-416 |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | R2 | 4 | 0.000 | 0.000 | 0.000 | new seeds 409-416 |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | R3 | 3 | 0.000 | 0.000 | 0.000 | new seeds 409-416 |
| audit_quarantine - audit | tag memory vs no memory | audit_misclassification_rate | pooled | 11 | 0.015 | -0.004 | 0.036 | new seeds 409-416 |
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
- **combined 401-416** R-J1 tags − label-only, ASR: **lower (resolved)** (Δ -0.043 [-0.083, -0.008], n = 35 pairs); R-J2 misclassification: **equivalent within ±0.10** (Δ -0.002 [-0.021, +0.013], n = 35 pairs); R-J3 label-only − plain audit misclassification: Δ +0.034 [+0.017, +0.052], n = 38 pairs.
- **new seeds 409-416** R-J1 tags − label-only, ASR: **lower (resolved)** (Δ -0.040 [-0.087, -0.004], n = 11 pairs); R-J2 misclassification: **equivalent within ±0.10** (Δ -0.036 [-0.076, -0.004], n = 11 pairs); R-J3 label-only − plain audit misclassification: Δ +0.049 [+0.020, +0.080], n = 14 pairs.
- Rotation dependence (combined, tags − label-only ASR): R1 +0.000 [+0.000, +0.000]; R2 +0.003 [-0.027, +0.040]; R3 -0.142 [-0.229, -0.051].

- Consequence (fixed): if the combined R-J1 is not 'lower (resolved)', the paper says tags show no demonstrated blocking advantage over label-only memory; if resolved but a rotation has the opposite sign, it says the advantage is rotation-dependent. No further extension.