**S5e_memory_replay — matched memory replay** (exploratory; rules 2026-10-20). 18 S5d raw-memory episodes, 1284 replayed items (rounds with ≥ 1 earlier detection), 5 auditor contexts per item; 15/15 auditor × context cells pass the ≥ 90% valid-label rule.
- Reconstruction check: the raw-context replay reproduces the auditor's original S5d verdict on 100.0% of 1284 items (100% of raw-context calls were disk-cache hits).

**Context length delivered** (characters added to the auditor system prompt):

| context | mean_context_chars |
|---|---|
| neutral | 1354.000 |
| none | 0.000 |
| raw | 1354.000 |
| struct | 676.100 |
| struct_pad | 1354.000 |

**Flag rate by context and item group** (`honest_clean` = legitimate proposals the episode's judge calls clean: a flag is a false rejection; `attacker_violating`: a flag is a detection)

| group | neutral | none | raw | struct | struct_pad |
|---|---|---|---|---|---|
| attacker_clean | 0.275 | 0.281 | 0.711 | 0.356 | 0.348 |
| attacker_violating | 0.693 | 0.800 | 0.939 | 0.829 | 0.800 |
| honest_clean | 0.044 | 0.014 | 0.394 | 0.046 | 0.167 |

**By rotation**

| rot | group | neutral | none | raw | struct | struct_pad |
|---|---|---|---|---|---|---|
| R1 | attacker_violating | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| R1 | honest_clean | 0.125 | 0.028 | 0.653 | 0.125 | 0.486 |
| R2 | attacker_violating | 0.548 | 0.595 | 0.857 | 0.690 | 0.738 |
| R2 | honest_clean | 0.007 | 0.000 | 0.194 | 0.000 | 0.000 |
| R3 | attacker_violating | 0.400 | 0.638 | 0.894 | 0.681 | 0.600 |
| R3 | honest_clean | 0.000 | 0.014 | 0.333 | 0.014 | 0.014 |

**Paired contrasts** (item-paired, bootstrap over episodes; verdict margin 0.10, pre-specified)

| group | contrast | reads_as | items | episodes | delta | lo | hi | flips_to_flag | flips_to_pass | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| honest_clean | raw - none | total effect of raw memory | 432 | 18 | 0.380 | 0.252 | 0.512 | 164 | 0 | yes |
| honest_clean | struct - none | label-only memory | 432 | 18 | 0.032 | 0.009 | 0.058 | 15 | 1 | no |
| honest_clean | struct_pad - struct | length alone, content held | 432 | 18 | 0.120 | 0.042 | 0.206 | 54 | 2 | ambiguous |
| honest_clean | neutral - none | unrelated context | 432 | 18 | 0.030 | 0.007 | 0.056 | 15 | 2 | no |
| honest_clean | raw - struct_pad | attacker text at matched length (contamination) | 432 | 18 | 0.227 | 0.130 | 0.329 | 113 | 15 | yes |
| attacker_violating | raw - none | total effect of raw memory | 375 | 18 | 0.180 | 0.110 | 0.257 | 54 | 2 | yes |
| attacker_violating | struct - none | label-only memory | 375 | 18 | 0.052 | 0.021 | 0.089 | 15 | 4 | no |
| attacker_violating | struct_pad - struct | length alone, content held | 375 | 18 | -0.015 | -0.043 | 0.018 | 6 | 17 | no |
| attacker_violating | neutral - none | unrelated context | 375 | 18 | -0.079 | -0.144 | -0.005 | 2 | 42 | ambiguous |
| attacker_violating | raw - struct_pad | attacker text at matched length (contamination) | 375 | 18 | 0.144 | 0.079 | 0.212 | 54 | 2 | ambiguous |
| attacker_clean | raw - none | total effect of raw memory | 477 | 18 | 0.372 | 0.273 | 0.465 | 208 | 3 | yes |
| attacker_clean | struct - none | label-only memory | 477 | 18 | 0.074 | 0.054 | 0.093 | 40 | 4 | no |
| attacker_clean | struct_pad - struct | length alone, content held | 477 | 18 | -0.006 | -0.035 | 0.029 | 24 | 28 | no |
| attacker_clean | neutral - none | unrelated context | 477 | 18 | 0.000 | -0.024 | 0.027 | 14 | 17 | no |
| attacker_clean | raw - struct_pad | attacker text at matched length (contamination) | 477 | 18 | 0.304 | 0.189 | 0.413 | 183 | 10 | yes |

- Same candidates, same states and the same detection history in every context: differences are prompt-level context effects, not episode dynamics (those are what S5d measured).
- Truth is the episode's own rotation judge; see A3 and H1 for that judge's error. Label-only padding uses neutral game background, as in S5d's neutral arm.
- `delta` is the mean of per-episode paired differences (each episode weighted equally, the bootstrap unit); the pooled flag rates above weight items, so the two differ where episodes contribute unequal numbers of items (attacker groups). (Reporting note added 2026-10-21 review; no estimate changed.)