**S5e — matched memory replay** (exploratory; rules 2026-10-20). 12 S5d raw-memory episodes, 864 replayed items (rounds with ≥ 1 earlier detection), 5 auditor contexts per item; 10/10 auditor × context cells pass the ≥ 90% valid-label rule.
- Reconstruction check: the raw-context replay reproduces the auditor's original S5d verdict on 100.0% of 864 items (100% of raw-context calls were disk-cache hits).

**Context length delivered** (characters added to the auditor system prompt):

| context | mean_context_chars |
|---|---|
| neutral | 1367.500 |
| none | 0.000 |
| raw | 1367.500 |
| struct | 679.700 |
| struct_pad | 1367.500 |

**Flag rate by context and item group** (`honest_clean` = legitimate proposals the episode's judge calls clean: a flag is a false rejection; `attacker_violating`: a flag is a detection)

| group | neutral | none | raw | struct | struct_pad |
|---|---|---|---|---|---|
| attacker_clean | 0.416 | 0.403 | 0.671 | 0.469 | 0.465 |
| attacker_violating | 0.712 | 0.826 | 0.949 | 0.847 | 0.808 |
| honest_clean | 0.062 | 0.021 | 0.493 | 0.069 | 0.250 |

**By rotation**

| rot | group | neutral | none | raw | struct | struct_pad |
|---|---|---|---|---|---|---|
| R1 | attacker_violating | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| R1 | honest_clean | 0.125 | 0.028 | 0.653 | 0.125 | 0.486 |
| R3 | attacker_violating | 0.400 | 0.638 | 0.894 | 0.681 | 0.600 |
| R3 | honest_clean | 0.000 | 0.014 | 0.333 | 0.014 | 0.014 |

**Paired contrasts** (item-paired, bootstrap over episodes; verdict margin 0.10, pre-specified)

| group | contrast | reads_as | items | episodes | delta | lo | hi | flips_to_flag | flips_to_pass | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| honest_clean | raw - none | total effect of raw memory | 288 | 12 | 0.472 | 0.340 | 0.601 | 136 | 0 | yes |
| honest_clean | struct - none | label-only memory | 288 | 12 | 0.049 | 0.017 | 0.083 | 15 | 1 | no |
| honest_clean | struct_pad - struct | length alone, content held | 288 | 12 | 0.181 | 0.080 | 0.285 | 54 | 2 | ambiguous |
| honest_clean | neutral - none | unrelated context | 288 | 12 | 0.042 | 0.007 | 0.076 | 14 | 2 | no |
| honest_clean | raw - struct_pad | attacker text at matched length (contamination) | 288 | 12 | 0.243 | 0.142 | 0.347 | 85 | 15 | yes |
| attacker_violating | raw - none | total effect of raw memory | 333 | 12 | 0.131 | 0.053 | 0.212 | 42 | 1 | ambiguous |
| attacker_violating | struct - none | label-only memory | 333 | 12 | 0.023 | 0.005 | 0.046 | 9 | 2 | no |
| attacker_violating | struct_pad - struct | length alone, content held | 333 | 12 | -0.039 | -0.068 | -0.013 | 3 | 16 | no |
| attacker_violating | neutral - none | unrelated context | 333 | 12 | -0.118 | -0.187 | -0.054 | 0 | 38 | ambiguous |
| attacker_violating | raw - struct_pad | attacker text at matched length (contamination) | 333 | 12 | 0.147 | 0.064 | 0.234 | 47 | 0 | ambiguous |
| attacker_clean | raw - none | total effect of raw memory | 243 | 12 | 0.259 | 0.171 | 0.348 | 65 | 0 | yes |
| attacker_clean | struct - none | label-only memory | 243 | 12 | 0.068 | 0.042 | 0.095 | 16 | 0 | no |
| attacker_clean | struct_pad - struct | length alone, content held | 243 | 12 | -0.003 | -0.041 | 0.048 | 8 | 9 | no |
| attacker_clean | neutral - none | unrelated context | 243 | 12 | 0.012 | -0.017 | 0.047 | 7 | 4 | no |
| attacker_clean | raw - struct_pad | attacker text at matched length (contamination) | 243 | 12 | 0.193 | 0.075 | 0.312 | 54 | 4 | ambiguous |

- Same candidates, same states and the same detection history in every context: differences are prompt-level context effects, not episode dynamics (those are what S5d measured).
- Truth is the episode's own rotation judge; see A3 and H1 for that judge's error. Label-only padding uses neutral game background, as in S5d's neutral arm.