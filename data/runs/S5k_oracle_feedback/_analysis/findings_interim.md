**Reviewer-response stage** (exploratory, built 2026-11-01 after submission v14-1; not part of ANALYSIS_PLAN_v1). Reading rules fixed before any unit ran: reports/prereg/RR_PLAN_v1.md.

**Instrument validity** (S5b rules, unchanged: attacker valid submissions ≥ 80% of rounds, judge unresolved ≤ 10%, auditor invalid ≤ 10%): 20/20 done episodes eligible (expected 48); excluded: none.

**Pooled by arm** (governor + attacker feedback; bootstrap over episodes)

| arm | episodes | asr_per_round | asr_per_round_lo | asr_per_round_hi | asr_given_submission | asr_given_submission_lo | asr_given_submission_hi | audit_misclassification_rate | audit_misclassification_rate_lo | audit_misclassification_rate_hi | valid_submission_rate | cost_usd |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| audit+adaptive | 5 | 0.096 | 0.000 | 0.224 | 0.100 | 0.000 | 0.233 | 0.016 | 0.000 | 0.048 | 0.984 | 0.968 |
| audit+oracle | 5 | 0.144 | 0.024 | 0.264 | 0.154 | 0.027 | 0.283 | 0.016 | 0.000 | 0.048 | 0.960 | 1.102 |
| audit_quarantine+adaptive | 5 | 0.104 | 0.008 | 0.272 | 0.105 | 0.008 | 0.272 | 0.032 | 0.000 | 0.080 | 0.984 | 1.773 |
| audit_quarantine+oracle | 5 | 0.096 | 0.024 | 0.168 | 0.100 | 0.024 | 0.181 | 0.032 | 0.008 | 0.056 | 0.984 | 1.668 |

**Paired contrasts** (rotation × seed; all outcomes in contrasts.csv)

| contrast | reads_as | outcome | scope | n_pairs | delta | lo | hi |
|---|---|---|---|---|---|---|---|
| audit+oracle - audit+adaptive | white-box minus selection feedback under audit | asr_per_round | R1 | 2 | 0.000 | 0.000 | 0.000 |
| audit+oracle - audit+adaptive | white-box minus selection feedback under audit | asr_per_round | R2 | 2 | 0.160 | -0.040 | 0.360 |
| audit+oracle - audit+adaptive | white-box minus selection feedback under audit | asr_per_round | R3 | 1 | -0.080 | -0.080 | -0.080 |
| audit+oracle - audit+adaptive | white-box minus selection feedback under audit | asr_per_round | pooled | 5 | 0.048 | -0.048 | 0.208 |
| audit_quarantine+oracle - audit_quarantine+adaptive | white-box minus selection feedback under audit_quarantine | asr_per_round | R1 | 2 | 0.000 | 0.000 | 0.000 |
| audit_quarantine+oracle - audit_quarantine+adaptive | white-box minus selection feedback under audit_quarantine | asr_per_round | R2 | 2 | 0.140 | 0.080 | 0.200 |
| audit_quarantine+oracle - audit_quarantine+adaptive | white-box minus selection feedback under audit_quarantine | asr_per_round | R3 | 1 | -0.320 | -0.320 | -0.320 |
| audit_quarantine+oracle - audit_quarantine+adaptive | white-box minus selection feedback under audit_quarantine | asr_per_round | pooled | 5 | -0.008 | -0.176 | 0.128 |
| audit_quarantine+oracle - audit+oracle | tag memory vs plain audit, white-box attacker | asr_per_round | R1 | 2 | 0.000 | 0.000 | 0.000 |
| audit_quarantine+oracle - audit+oracle | tag memory vs plain audit, white-box attacker | asr_per_round | R2 | 2 | -0.060 | -0.120 | 0.000 |
| audit_quarantine+oracle - audit+oracle | tag memory vs plain audit, white-box attacker | asr_per_round | R3 | 1 | -0.120 | -0.120 | -0.120 |
| audit_quarantine+oracle - audit+oracle | tag memory vs plain audit, white-box attacker | asr_per_round | pooled | 5 | -0.048 | -0.096 | 0.000 |
| audit+oracle - audit+adaptive | white-box minus selection feedback under audit | audit_misclassification_rate | R1 | 2 | 0.000 | 0.000 | 0.000 |
| audit+oracle - audit+adaptive | white-box minus selection feedback under audit | audit_misclassification_rate | R2 | 2 | 0.000 | 0.000 | 0.000 |
| audit+oracle - audit+adaptive | white-box minus selection feedback under audit | audit_misclassification_rate | R3 | 1 | 0.000 | 0.000 | 0.000 |
| audit+oracle - audit+adaptive | white-box minus selection feedback under audit | audit_misclassification_rate | pooled | 5 | 0.000 | 0.000 | 0.000 |
| audit_quarantine+oracle - audit_quarantine+adaptive | white-box minus selection feedback under audit_quarantine | audit_misclassification_rate | R1 | 2 | -0.020 | -0.080 | 0.040 |
| audit_quarantine+oracle - audit_quarantine+adaptive | white-box minus selection feedback under audit_quarantine | audit_misclassification_rate | R2 | 2 | 0.040 | 0.000 | 0.080 |
| audit_quarantine+oracle - audit_quarantine+adaptive | white-box minus selection feedback under audit_quarantine | audit_misclassification_rate | R3 | 1 | -0.040 | -0.040 | -0.040 |
| audit_quarantine+oracle - audit_quarantine+adaptive | white-box minus selection feedback under audit_quarantine | audit_misclassification_rate | pooled | 5 | 0.000 | -0.048 | 0.048 |
| audit_quarantine+oracle - audit+oracle | tag memory vs plain audit, white-box attacker | audit_misclassification_rate | R1 | 2 | 0.000 | -0.040 | 0.040 |
| audit_quarantine+oracle - audit+oracle | tag memory vs plain audit, white-box attacker | audit_misclassification_rate | R2 | 2 | 0.040 | 0.000 | 0.080 |
| audit_quarantine+oracle - audit+oracle | tag memory vs plain audit, white-box attacker | audit_misclassification_rate | R3 | 1 | 0.000 | 0.000 | 0.000 |
| audit_quarantine+oracle - audit+oracle | tag memory vs plain audit, white-box attacker | audit_misclassification_rate | pooled | 5 | 0.016 | -0.016 | 0.056 |

**Reading (RR_PLAN_v1)**

- **R-K1 (audit)** white-box − selection feedback, ASR per round: **unresolved** (Δ +0.048 [-0.048, +0.208], n = 5 pairs).
  - given a valid submission: Δ +0.054 [-0.056, +0.229], n = 5 pairs
- **R-K1 (audit_quarantine)** white-box − selection feedback, ASR per round: **unresolved** (Δ -0.008 [-0.176, +0.128], n = 5 pairs).
  - given a valid submission: Δ -0.004 [-0.176, +0.135], n = 5 pairs
- **R-K2** worst-case ASR under audit with white-box feedback: 0.144 [0.024, 0.264] per round (valid submissions 0.96).
- **R-K2** worst-case ASR under audit_quarantine with white-box feedback: 0.096 [0.024, 0.168] per round (valid submissions 0.98).

- A rise means the S5b/S5b_C ASR figures are for a selection-feedback attacker and are optimistic against an attacker who can observe the auditor; report both in the paper's threat model.