**A5 — rule-by-rule verification vs joint auditing** (exploratory; rules 2026-10-21). Same auditor models, prompts split by rule, any-violation rejection. 6/6 auditor × procedure cells pass the ≥ 90% complete-label rule.

**Rates against each reference** (`tpr` = share of reference-violating items the auditor would block; `fpr` = share of reference-clean items it would block)

| auditor | reference | n | tpr_joint | fpr_joint | tpr_rules | fpr_rules |
|---|---|---|---|---|---|---|
| deepseek_v4_pro | anchor truth | 22 | 1.000 | 0.125 | 1.000 | 0.125 |
| deepseek_v4_pro | judge glm53 | 902 | 0.961 | 0.174 | 0.974 | 0.242 |
| deepseek_v4_pro | judge kimi_k3 | 112 | 0.927 | 0.070 | 0.909 | 0.105 |
| deepseek_v4_pro | judge minimax_m3 | 902 | 0.868 | 0.044 | 0.903 | 0.080 |
| deepseek_v4_pro | judge muse_spark | 112 | 0.904 | 0.133 | 0.923 | 0.133 |
| deepseek_v4_pro | S5b honest candidates (flag rate) | 68 |  | 0.059 |  | 0.074 |
| minimax_m3 | anchor truth | 22 | 1.000 | 0.000 | 1.000 | 0.000 |
| minimax_m3 | judge deepseek_v4_pro | 900 | 0.993 | 0.342 | 0.977 | 0.312 |
| minimax_m3 | judge glm53 | 900 | 0.994 | 0.397 | 0.996 | 0.342 |
| minimax_m3 | judge kimi_k3 | 112 | 1.000 | 0.193 | 0.945 | 0.158 |
| minimax_m3 | judge muse_spark | 112 | 0.942 | 0.283 | 0.962 | 0.183 |
| minimax_m3 | S5b honest candidates (flag rate) | 68 |  | 0.103 |  | 0.059 |
| glm53 | anchor truth | 22 | 0.929 | 0.000 | 1.000 | 0.000 |
| glm53 | judge deepseek_v4_pro | 895 | 0.939 | 0.122 | 0.938 | 0.158 |
| glm53 | judge kimi_k3 | 112 | 0.818 | 0.018 | 0.891 | 0.035 |
| glm53 | judge minimax_m3 | 895 | 0.867 | 0.032 | 0.884 | 0.032 |
| glm53 | judge muse_spark | 112 | 0.827 | 0.050 | 0.923 | 0.050 |
| glm53 | S5b honest candidates (flag rate) | 68 |  | 0.044 |  | 0.044 |
| deepseek_v4_pro | H1 human (game items) | 52 | 0.968 | 0.000 | 0.968 | 0.095 |
| minimax_m3 | H1 human (game items) | 52 | 1.000 | 0.286 | 1.000 | 0.190 |
| glm53 | H1 human (game items) | 52 | 0.968 | 0.143 | 1.000 | 0.095 |

**Paired differences, rules − joint** (bootstrap over items; margin 0.05, pre-specified)

| auditor | reference | rate | n | rules_minus_joint | lo | hi | verdict |
|---|---|---|---|---|---|---|---|
| deepseek_v4_pro | anchor truth | tpr | 14 | 0.000 | 0.000 | 0.000 | within margin |
| deepseek_v4_pro | anchor truth | fpr | 8 | 0.000 | 0.000 | 0.000 | within margin |
| deepseek_v4_pro | judge glm53 | tpr | 534 | 0.013 | -0.002 | 0.028 | within margin |
| deepseek_v4_pro | judge glm53 | fpr | 368 | 0.068 | 0.035 | 0.103 | ambiguous |
| deepseek_v4_pro | judge kimi_k3 | tpr | 55 | -0.018 | -0.091 | 0.036 | ambiguous |
| deepseek_v4_pro | judge kimi_k3 | fpr | 57 | 0.035 | 0.000 | 0.088 | ambiguous |
| deepseek_v4_pro | judge minimax_m3 | tpr | 652 | 0.035 | 0.015 | 0.055 | ambiguous |
| deepseek_v4_pro | judge minimax_m3 | fpr | 250 | 0.036 | 0.004 | 0.068 | ambiguous |
| deepseek_v4_pro | judge muse_spark | tpr | 52 | 0.019 | 0.000 | 0.058 | ambiguous |
| deepseek_v4_pro | judge muse_spark | fpr | 60 | 0.000 | -0.067 | 0.067 | ambiguous |
| minimax_m3 | anchor truth | tpr | 14 | 0.000 | 0.000 | 0.000 | within margin |
| minimax_m3 | anchor truth | fpr | 8 | 0.000 | 0.000 | 0.000 | within margin |
| minimax_m3 | judge deepseek_v4_pro | tpr | 564 | -0.016 | -0.028 | -0.005 | within margin |
| minimax_m3 | judge deepseek_v4_pro | fpr | 336 | -0.030 | -0.074 | 0.012 | ambiguous |
| minimax_m3 | judge glm53 | tpr | 532 | 0.002 | -0.004 | 0.009 | within margin |
| minimax_m3 | judge glm53 | fpr | 368 | -0.054 | -0.098 | -0.011 | ambiguous |
| minimax_m3 | judge kimi_k3 | tpr | 55 | -0.055 | -0.127 | 0.000 | ambiguous |
| minimax_m3 | judge kimi_k3 | fpr | 57 | -0.035 | -0.140 | 0.070 | ambiguous |
| minimax_m3 | judge muse_spark | tpr | 52 | 0.019 | 0.000 | 0.058 | ambiguous |
| minimax_m3 | judge muse_spark | fpr | 60 | -0.100 | -0.217 | 0.017 | ambiguous |
| glm53 | anchor truth | tpr | 14 | 0.071 | 0.000 | 0.214 | ambiguous |
| glm53 | anchor truth | fpr | 8 | 0.000 | 0.000 | 0.000 | within margin |
| glm53 | judge deepseek_v4_pro | tpr | 560 | -0.002 | -0.020 | 0.016 | within margin |
| glm53 | judge deepseek_v4_pro | fpr | 335 | 0.036 | 0.006 | 0.069 | ambiguous |
| glm53 | judge kimi_k3 | tpr | 55 | 0.073 | 0.000 | 0.164 | ambiguous |
| glm53 | judge kimi_k3 | fpr | 57 | 0.018 | 0.000 | 0.053 | ambiguous |
| glm53 | judge minimax_m3 | tpr | 645 | 0.017 | -0.003 | 0.039 | within margin |
| glm53 | judge minimax_m3 | fpr | 250 | 0.000 | -0.020 | 0.020 | within margin |
| glm53 | judge muse_spark | tpr | 52 | 0.096 | 0.019 | 0.174 | ambiguous |
| glm53 | judge muse_spark | fpr | 60 | 0.000 | -0.050 | 0.050 | ambiguous |

**Which rule triggers rule-by-rule rejections** (share of rejections where each rule fired; rules can co-fire)

| alias | rule_claims | rule_pressure | rule_intensity |
|---|---|---|---|
| deepseek_v4_pro | 0.977 | 0.768 | 0.750 |
| glm53 | 0.946 | 0.806 | 0.589 |
| minimax_m3 | 0.897 | 0.841 | 0.425 |

**Calls and latency per decision** (latency = sum over the item's calls, including disk-cache hits for the joint A3 calls; the joint bank verdicts were made in A3 and carry no latency here)

| alias | procedure | calls_per_item | median_latency_s |
|---|---|---|---|
| deepseek_v4_pro | joint | 1.000 | 0.730 |
| deepseek_v4_pro | rules | 3.000 | 1.990 |
| glm53 | joint | 1.020 | 0.870 |
| glm53 | rules | 3.050 | 2.800 |
| minimax_m3 | joint | 1.000 | 1.490 |
| minimax_m3 | rules | 3.020 | 2.960 |

**A5 spend by auditor** (rules calls, plus joint calls on H1 items)

| auditor | cost_usd |
|---|---|
| deepseek_v4_pro | 1.245 |
| glm53 | 1.205 |
| minimax_m3 | 0.948 |

- References are other families' judges (never a majority), the 22 synthetic anchors and the H1 human labels (game items only). Read differences as procedural effects at a fixed model.