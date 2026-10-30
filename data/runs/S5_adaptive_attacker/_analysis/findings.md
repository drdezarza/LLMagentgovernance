| attacker_mode | governor | n | asr | asr_lo | asr_hi | judge_invalid | audit_invalid | asr_early | asr_late | adaptation_gap | honest_fp | block_rate | ecs | coop | integrity | cost |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| adaptive | audit | 3 | 0.000 |  |  |  |  | 0.000 | 0.000 | 0.000 | 0.000 | 0.976 | 0.149 | 0.273 | 1.000 | 0.327 |
| adaptive | audit_adaptive | 3 | 0.000 |  |  |  |  | 0.000 | 0.000 | 0.000 | 0.253 | 1.000 | 0.124 | 0.260 | 0.967 | 0.455 |
| adaptive | label | 3 | 0.000 |  |  |  |  | 0.000 | 0.000 | 0.000 | 0.000 | 0.922 | 0.153 | 0.275 | 1.000 | 0.229 |
| static | audit | 3 | 0.000 |  |  |  |  | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.147 | 0.267 | 1.000 | 0.247 |
| static | audit_adaptive | 3 | 0.000 |  |  |  |  | 0.000 | 0.000 | 0.000 | 0.000 | 0.993 | 0.153 | 0.275 | 1.000 | 0.189 |
| static | label | 3 | 0.000 |  |  |  |  | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.157 | 0.277 | 1.000 | 0.326 |

- `asr_lo`/`asr_hi` bound the effect of UNRESOLVED judge outputs; they are not confidence intervals. Rounds inside an episode are correlated, so uncertainty must come from independent episodes (seeds).

- Adaptive attacker vs label-trusting governor: ASR 0% (early 0% → late 0%).
- Adaptive attacker vs adaptive-audit governor: ASR 0%, honest false-positive rate 25%.

![S5](s5_attack_curves.png)