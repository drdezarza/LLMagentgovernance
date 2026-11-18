# M1: model evidence (RR_PLAN_v2, descriptive, no API calls)

Every value is read from existing records; empty = not measured for that model. Prices: USD per 1M input/output tokens (roster). A1: 30-item anchor set. A3: fixed bank, auditor vs each other judge (mean). A8: fixed-text screen (judge-referenced sensitivity / false positives, cost per 1000 audits). S5i: plain-audit closed loop, means over eligible episodes (judge Kimi-K3). S3: governance gap in ECS with that population backbone [CI]. Full table with interface columns: `M1_model_evidence.csv`; roles per study: `M1_roles_by_study.csv`.

| alias | tier | price_in_out_usd_per_M | roles | S0_latency_s | A1_auditor_bal_acc | A1_judge_bal_acc | A3_auditor_tpr | A3_auditor_fpr_honest | A3_judge_mean_kappa | A8_sensitivity | A8_false_pos | A8_usd_per_1000_audits | S5i_ASR_as_auditor | S5i_misclass_as_auditor | S5i_ASR_as_attacker | S5i_raw_memory_penalty | S3_ECS_gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek_v4_flash | cheap | 0.3/1.0 | population backbone (S3) | 1.344 |  |  |  |  |  | 0.938 | 0.158 | 0.160 |  |  |  |  | 0.203 [0.195, 0.208] |
| deepseek_v4_pro | frontier | 1.0/4.0 | attacker (S5b/S5h/S5i/S5j/S5k); auditor (S5b/S5h/S5i/S5j/S5k); judge (S5b/S5h/S5j/S5k/S7b/S7c); message auditor (S7b/S7c); planner backbone (S7b/S7c); population backbone (S3) | 0.816 | 0.958 | 0.958 | 0.912 | 0.023 | 0.780 | 0.915 | 0.105 |  | 0.120 | 0.003 | 0.043 | +0.247 [+0.107, +0.400] | 0.209 [0.201, 0.215] |
| gemma3_27b | cheap | 0.1/0.3 | population backbone (S3) | 3.676 |  |  |  |  |  | 0.941 | 0.279 | 0.050 |  |  |  |  | 0.145 [0.134, 0.155] |
| glm53 | frontier | 1.0/4.0 | attacker (S5b/S5h/S5i/S5j/S5k); auditor (S5b/S5h/S5i/S5j/S5k); judge (S5b/S5h/S5j/S5k/S7b/S7c); message auditor (S7b/S7c); planner backbone (S7b/S7c); population backbone (S3) | 0.798 | 0.931 | 0.931 | 0.904 | 0.000 | 0.780 | 0.863 | 0.055 |  | 0.133 | 0.000 | 0.087 | +0.073 [+0.000, +0.187] | 0.208 [0.183, 0.225] |
| glm53_flash | cheap | 0.15/0.5 | population backbone (S3) | 1.212 |  |  |  |  |  | 0.937 | 0.138 | 0.084 |  |  |  |  | 0.208 [0.171, 0.239] |
| gpt_oss_120b | cheap | 0.15/0.6 | population backbone (S3) | 0.799 | 0.917 | 0.909 |  |  |  | 0.922 | 0.333 | 0.229 |  |  |  |  | 0.197 [0.163, 0.224] |
| kimi_k3 | frontier | 3.0/15.0 | judge (S5i); population backbone (S3) | 1.147 | 0.958 | 1.000 |  |  | 0.801 |  |  |  |  |  |  |  | 0.215 [0.206, 0.223] |
| minimax_m3 | mid | 0.3/1.0 | attacker (S5b/S5h/S5i/S5j/S5k); auditor (S5b/S5h/S5i/S5j/S5k); judge (S5b/S5h/S5j/S5k/S7b/S7c); message auditor (S7b/S7c); planner backbone (S7b/S7c); population backbone (S3) | 2.665 | 0.972 | 1.000 | 0.995 | 0.069 | 0.713 | 0.982 | 0.304 |  | 0.003 | 0.010 | 0.127 | +0.760 [+0.713, +0.803] | 0.209 [0.207, 0.213] |
| muse_spark | frontier | 1.25/4.25 | population backbone (S3) | 3.492 | 1.000 | 1.000 |  |  | 0.776 |  |  |  |  |  |  |  | 0.197 [0.182, 0.209] |
| nemotron_super | mid | 0.3/0.9 | population backbone (S3) | 1.408 | 0.895 | 0.911 |  |  |  | 0.862 | 0.059 | 0.285 |  |  |  |  | 0.222 [0.214, 0.226] |
| qwen35_397b | frontier | 0.6/4.0 | population backbone (S3) | 1.309 | 0.931 | 0.972 |  |  |  |  |  |  |  |  |  |  | 0.205 [0.198, 0.216] |
| qwen38_27b | mid | 0.45/3.0 | population backbone (S3) | 0.680 |  |  |  |  |  | 0.932 | 0.125 | 0.363 |  |  |  |  | 0.219 [0.216, 0.221] |
