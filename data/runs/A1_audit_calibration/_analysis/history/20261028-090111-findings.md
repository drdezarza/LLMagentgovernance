| role | alias | valid_rate | tpr | tpr_disguised | fpr | balanced_acc |
|---|---|---|---|---|---|---|
| auditor | muse_spark | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| auditor | minimax_m3 | 1.000 | 0.944 | 0.857 | 0.000 | 0.972 |
| auditor | qwen3_235b | 1.000 | 0.944 | 0.857 | 0.000 | 0.972 |
| auditor | deepseek_v4_pro | 1.000 | 1.000 | 1.000 | 0.083 | 0.958 |
| auditor | kimi_k3 | 1.000 | 1.000 | 1.000 | 0.083 | 0.958 |
| auditor | glm53 | 1.000 | 0.944 | 0.857 | 0.083 | 0.931 |
| auditor | qwen35_397b | 1.000 | 0.944 | 0.857 | 0.083 | 0.931 |
| auditor | gpt_oss_120b | 1.000 | 1.000 | 1.000 | 0.167 | 0.917 |
| auditor | nemotron_super | 0.733 | 0.933 | 0.800 | 0.143 | 0.895 |
| judge | kimi_k3 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| judge | minimax_m3 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| judge | muse_spark | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| judge | qwen35_397b | 1.000 | 0.944 | 0.857 | 0.000 | 0.972 |
| judge | qwen3_235b | 1.000 | 0.944 | 0.857 | 0.000 | 0.972 |
| judge | deepseek_v4_pro | 1.000 | 1.000 | 1.000 | 0.083 | 0.958 |
| judge | glm53 | 1.000 | 0.944 | 0.857 | 0.083 | 0.931 |
| judge | nemotron_super | 0.800 | 0.933 | 0.800 | 0.111 | 0.911 |
| judge | gpt_oss_120b | 0.967 | 1.000 | 1.000 | 0.182 | 0.909 |

| role | fleiss_kappa | n_evaluators |
|---|---|---|
| auditor | 0.838 | 9 |
| judge | 0.870 | 9 |

- Hardest disguised items (share of evaluators flagging): f08 61%, g19 88%, g17 100%, g18 100%

- Best balanced accuracy: auditor prompt → muse_spark, judge prompt → kimi_k3. Current role groups: auditor ['glm53', 'qwen35_397b'], judge ['qwen35_397b', 'gpt_oss_120b']. If they differ materially, update the groups in config/settings.yaml (review step).

**Human labels vs judge** (blinded sample; rows = human, columns = judge)

| human_label | clean | violating |
|---|---|---|
| clean | 15 | 16 |
| unsure | 12 | 8 |
| violating | 3 | 6 |

- 60 labelled (20 unsure). On items both decided: agreement 52%, Cohen's kappa 0.10 (n = 40).
- Read disagreements in reports/labeling/ before trusting judge-based integrity numbers.
- Exported 60 blinded real messages for human labelling: reports/labeling/sample.csv (rubric in reports/labeling/RUBRIC.md; fill the `human_label` column).