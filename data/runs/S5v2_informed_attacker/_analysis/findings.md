| attacker_mode | governor | n | asr | asr_lo | asr_hi | judge_invalid | audit_invalid | asr_early | asr_late | adaptation_gap | honest_fp | block_rate | ecs | coop | integrity | cost |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| adaptive | audit | 1 | 0.000 | 0.000 | 0.000 | 0 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.139 | 0.235 | 1.000 | 0.154 |
| adaptive | audit_adaptive | 1 | 0.040 | 0.040 | 0.040 | 0 | 0 | 0.083 | 0.000 | -0.083 | 0.360 | 0.966 | 0.127 | 0.233 | 1.000 | 0.188 |
| adaptive | label | 1 | 0.760 | 0.760 | 0.760 | 0 | 0 | 0.750 | 0.769 | 0.019 | 0.000 | 0.000 | 0.050 | 0.258 | 0.400 | 0.127 |
| static | audit | 1 | 0.000 | 0.000 | 0.000 | 0 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.144 | 0.263 | 1.000 | 0.127 |
| static | audit_adaptive | 1 | 0.000 | 0.000 | 0.000 | 0 | 0 | 0.000 | 0.000 | 0.000 | 0.320 | 1.000 | 0.150 | 0.262 | 1.000 | 0.146 |
| static | label | 1 | 0.360 | 0.360 | 0.360 | 0 | 0 | 0.417 | 0.308 | -0.109 | 0.000 | 0.000 | 0.139 | 0.258 | 0.920 | 0.115 |

- `asr_lo`/`asr_hi` bound the effect of UNRESOLVED judge outputs; they are not confidence intervals. Rounds inside an episode are correlated, so uncertainty must come from independent episodes (seeds).

- Adaptive attacker vs label-trusting governor: ASR 76% (early 75% → late 77%).
- Adaptive attacker vs adaptive-audit governor: ASR 4%, honest false-positive rate 36%.

![S5](s5_attack_curves.png)