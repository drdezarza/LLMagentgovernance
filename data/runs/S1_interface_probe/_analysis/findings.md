| alias | policy_nonfactual_rate | policy_fear_rate | policy_over_cap_rate | plan_n_modes | plan_mode_entropy | plan_top_mode | manip_discrimination |
|---|---|---|---|---|---|---|---|
| qwen3_235b | 0.000 | 0.000 | 0.000 | 1 | -0.000 | SEQUENTIAL | 0.006 |
| deepseek_v4_pro | 0.000 | 0.000 | 0.000 | 3 | 0.496 | SEQUENTIAL | -0.005 |
| deepseek_v4_flash | 0.000 | 0.000 | 0.000 | 4 | 0.773 | SEQUENTIAL | 0.037 |
| glm53 | 0.000 | 0.000 | 0.000 | 4 | 0.628 | SEQUENTIAL | 0.041 |
| glm53_flash | 0.000 | 0.000 | 0.000 | 3 | 0.779 | SEQUENTIAL | 0.039 |
| kimi_k3 | 0.000 | 0.000 | 0.000 | 2 | 0.305 | SEQUENTIAL | 0.033 |
| qwen35_397b | 0.000 | 0.000 | 0.000 | 2 | 0.234 | SEQUENTIAL | 0.031 |
| qwen38_27b | 0.000 | 0.000 | 0.000 | 3 | 0.676 | SEARCH | 0.069 |
| qwen3_30b | 0.000 | 0.000 | 0.000 | 1 | -0.000 | SEQUENTIAL | 0.090 |
| minimax_m3 | 0.000 | 0.000 | 0.000 | 3 | 0.610 | SEARCH | 0.029 |
| gemma3_27b | 1.000 | 0.000 | 0.000 | 1 | -0.000 | SEQUENTIAL | 0.030 |
| gpt_oss_120b | 0.000 | 0.000 | 0.000 | 4 | 0.941 | SEARCH | -0.026 |
| nemotron_super | 0.000 | 0.000 | 0.000 | 1 | -0.000 | SEQUENTIAL | -0.050 |
| hermes4_405b | 0.000 | 0.000 | 0.000 | 1 | -0.000 | SEQUENTIAL | 0.011 |
| muse_spark | 0.000 | 0.000 | 0.000 | 4 | 0.954 | SEQUENTIAL | 0.058 |

- Highest voluntary non-factual policy rate: **gemma3_27b** (100%).
- Planning-mode collapse (single mode over all states): qwen3_235b, qwen3_30b, gemma3_27b, nemotron_super, hermes4_405b.
- Mean manipulation discrimination (factual − manipulative shift): +0.026 (positive = agents resist manipulative messages).

![S1](s1_interfaces.png)