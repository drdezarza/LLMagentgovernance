**Attacker interface by family and output budget** (20 prompts per cell: 10 fixed public states × {no feedback, canned feedback}; S5 attacker system prompt; `effective_max_tokens` = after the model profile's minimum)

| alias | budget | effective_max_tokens | valid_rate | full_rate | empty_rate | median_latency_s | cost_per_valid_usd |
|---|---|---|---|---|---|---|---|
| deepseek_v4_pro | 900 | 900 | 1.000 | 1.000 | 0.000 | 2.557 | 0.002 |
| deepseek_v4_pro | 2000 | 2000 | 0.950 | 0.950 | 0.000 | 2.329 | 0.002 |
| deepseek_v4_pro | 6000 | 6000 | 1.000 | 1.000 | 0.000 | 2.352 | 0.002 |
| deepseek_v4_pro | 12000 | 12000 | 1.000 | 1.000 | 0.000 | 2.474 | 0.002 |
| glm53 | 900 | 900 | 1.000 | 1.000 | 0.000 | 2.649 | 0.002 |
| glm53 | 2000 | 2000 | 1.000 | 1.000 | 0.000 | 2.391 | 0.002 |
| glm53 | 6000 | 6000 | 1.000 | 1.000 | 0.000 | 2.554 | 0.002 |
| glm53 | 12000 | 12000 | 1.000 | 1.000 | 0.000 | 2.037 | 0.002 |
| kimi_k3 | 900 | 900 | 0.900 | 0.900 | 0.000 | 2.970 | 0.011 |
| kimi_k3 | 2000 | 2000 | 1.000 | 1.000 | 0.000 | 3.276 | 0.010 |
| kimi_k3 | 6000 | 6000 | 0.950 | 0.950 | 0.000 | 2.882 | 0.010 |
| kimi_k3 | 12000 | 12000 | 1.000 | 1.000 | 0.000 | 3.013 | 0.010 |
| minimax_m3 | 900 | 2000 | 0.050 | 0.050 | 0.900 | 6.305 | 0.044 |
| minimax_m3 | 2000 | 2000 | 0.050 | 0.050 | 0.800 | 6.467 | 0.041 |
| minimax_m3 | 6000 | 6000 | 0.750 | 0.750 | 0.150 | 15.628 | 0.006 |
| minimax_m3 | 12000 | 12000 | 1.000 | 1.000 | 0.000 | 12.904 | 0.005 |
| qwen35_397b | 900 | 900 | 0.800 | 0.800 | 0.000 | 3.237 | 0.002 |
| qwen35_397b | 2000 | 2000 | 0.950 | 0.950 | 0.000 | 3.195 | 0.002 |
| qwen35_397b | 6000 | 6000 | 0.950 | 0.950 | 0.000 | 3.332 | 0.002 |
| qwen35_397b | 12000 | 12000 | 0.650 | 0.650 | 0.000 | 3.229 | 0.002 |

**Rule (pre-specified):** smallest budget with valid-submission rate ≥ 90% and median latency ≤ 60 s. Chosen: deepseek_v4_pro → 900 (fit, valid 100%); glm53 → 900 (fit, valid 100%); kimi_k3 → 900 (fit, valid 90%); minimax_m3 → 12000 (fit, valid 100%); qwen35_397b → 2000 (fit, valid 95%).
- S5b reads `recommended.json` for the attacker's budget on units that have not run yet.