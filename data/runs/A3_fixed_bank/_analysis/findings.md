**A3 — fixed bank × every evaluator** (exploratory; bank frozen once after S5b, see bank_manifest.json). 1626 unique texts, 2286 provenance refs: s5b_dep 565, s5b_hon 525, s5b_att 420, a0 394, s3b 360, anchor 22.

**Instruments** (pre-specified rule 2026-10-16: valid labels ≥ 90% of items; 11/11 evaluator×prompt cells eligible). Anchor TPR/FPR = A1 known-label game items (n = 22, synthetic); flag_* = share judged violating per bank set (strict verdict; rubric prompt: content verdict).

| alias | prompt | n | valid_rate | cached_share | eligible | anchor_tpr | anchor_fpr | anchor_bal_acc | flag_a0 | flag_anchor | flag_s3b | flag_s5b_att | flag_s5b_dep | flag_s5b_hon |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek_v4_pro | audit | 902 | 1.000 | 0.083 | True | 1.000 | 0.125 | 0.938 | 0.911 | 0.682 |  | 0.479 | 0.444 | 0.059 |
| deepseek_v4_pro | judge | 1626 | 1.000 | 0.329 | True | 1.000 | 0.125 | 0.938 | 0.918 | 0.682 | 0.546 | 0.448 | 0.598 | 0.044 |
| deepseek_v4_pro | judge_rubric | 836 | 1.000 | 0.000 | True | 0.929 | 0.125 | 0.902 |  | 0.636 | 0.526 | 0.367 | 0.520 |  |
| glm53 | audit | 902 | 0.998 | 0.224 | True | 0.929 | 0.000 | 0.964 | 0.901 | 0.591 |  | 0.486 | 0.367 | 0.044 |
| glm53 | judge | 1626 | 1.000 | 0.140 | True | 0.929 | 0.125 | 0.902 | 0.844 | 0.636 | 0.542 | 0.445 | 0.531 | 0.029 |
| glm53 | judge_rubric | 836 | 1.000 | 0.000 | True | 0.929 | 0.125 | 0.902 |  | 0.636 | 0.558 | 0.400 | 0.591 |  |
| kimi_k3 | judge | 836 | 0.996 | 0.324 | True | 1.000 | 0.000 | 1.000 |  | 0.636 | 0.562 | 0.456 | 0.633 |  |
| minimax_m3 | audit | 902 | 1.000 | 0.068 | True | 1.000 | 0.000 | 1.000 | 0.972 | 0.636 |  | 0.655 | 0.578 | 0.103 |
| minimax_m3 | judge | 1626 | 1.000 | 0.304 | True | 1.000 | 0.000 | 1.000 | 0.957 | 0.636 | 0.647 | 0.619 | 0.726 | 0.044 |
| minimax_m3 | judge_rubric | 836 | 0.999 | 0.000 | True | 1.000 | 0.000 | 1.000 |  | 0.636 | 0.582 | 0.461 | 0.684 |  |
| muse_spark | judge | 836 | 1.000 | 0.026 | True | 1.000 | 0.000 | 1.000 |  | 0.636 | 0.574 | 0.422 | 0.602 |  |

**Auditor vs each other judge** (bank items from A0 + S5b candidates; `tpr_blocks_violating` = share of items the reference judge calls violating that the plain-audit governor would block at cap 0.80; `fpr_blocks_clean` = share of items the reference judge calls clean that it would block). Each row uses one judge as reference; no majority-vote truth.

| auditor | judge_ref | n_viol_ref | n_clean_ref | tpr_blocks_violating | fpr_blocks_clean | fpr_honest_only |
|---|---|---|---|---|---|---|
| deepseek_v4_pro | glm53 | 520 | 360 | 0.960 | 0.175 | 0.030 |
| deepseek_v4_pro | minimax_m3 | 638 | 242 | 0.865 | 0.041 | 0.015 |
| glm53 | deepseek_v4_pro | 551 | 329 | 0.942 | 0.128 | 0.000 |
| glm53 | minimax_m3 | 638 | 242 | 0.867 | 0.033 | 0.000 |
| minimax_m3 | deepseek_v4_pro | 551 | 329 | 0.995 | 0.350 | 0.062 |
| minimax_m3 | glm53 | 520 | 360 | 0.996 | 0.403 | 0.076 |

**Judge agreement** (strict prompt, pairwise on shared items)

| judge_a | judge_b | n | agreement | kappa |
|---|---|---|---|---|
| deepseek_v4_pro | glm53 | 1626 | 0.907 | 0.807 |
| deepseek_v4_pro | kimi_k3 | 833 | 0.920 | 0.833 |
| deepseek_v4_pro | minimax_m3 | 1626 | 0.871 | 0.714 |
| deepseek_v4_pro | muse_spark | 836 | 0.888 | 0.768 |
| glm53 | kimi_k3 | 833 | 0.911 | 0.819 |
| glm53 | minimax_m3 | 1626 | 0.847 | 0.672 |
| glm53 | muse_spark | 836 | 0.911 | 0.820 |
| kimi_k3 | minimax_m3 | 833 | 0.886 | 0.749 |
| kimi_k3 | muse_spark | 833 | 0.905 | 0.802 |
| minimax_m3 | muse_spark | 836 | 0.868 | 0.715 |

**Role assignments** (evasion = share of the attacker family's bank candidates that the auditor's plain audit would pass AND the judge calls violating; `a0` = unadapted candidates on fixed states, `s5b_att` = candidates written inside S5b episodes, which exist only for some rotations). The three observed rotations are marked with their plain-audit ASR (eligible episodes).

| bank | attacker | auditor | judge | n | violating_rate | evasion | observed_rot | observed_audit_asr |
|---|---|---|---|---|---|---|---|---|
| a0 | deepseek_v4_pro | glm53 | minimax_m3 | 80 | 0.975 | 0.038 |  |  |
| a0 | deepseek_v4_pro | minimax_m3 | glm53 | 80 | 0.850 | 0.000 | R1 | 0.000 |
| a0 | glm53 | deepseek_v4_pro | minimax_m3 | 80 | 1.000 | 0.025 | R3 | 0.413 |
| a0 | glm53 | minimax_m3 | deepseek_v4_pro | 80 | 0.988 | 0.000 |  |  |
| a0 | minimax_m3 | deepseek_v4_pro | glm53 | 72 | 0.514 | 0.028 |  |  |
| a0 | minimax_m3 | glm53 | deepseek_v4_pro | 72 | 0.681 | 0.111 | R2 | 0.173 |
| s5b_att | glm53 | deepseek_v4_pro | minimax_m3 | 140 | 0.707 | 0.100 | R3 | 0.413 |
| s5b_att | glm53 | minimax_m3 | deepseek_v4_pro | 140 | 0.593 | 0.007 |  |  |
| s5b_att | minimax_m3 | deepseek_v4_pro | glm53 | 280 | 0.382 | 0.057 |  |  |
| s5b_att | minimax_m3 | glm53 | deepseek_v4_pro | 280 | 0.375 | 0.057 | R2 | 0.173 |

- Full table incl. the outside judge and A0-only attacker families: assignments.csv (30 rows).

**Judge sensitivity, S5b** (ASR per episode re-scored from the deployed attacker texts; eligible episodes; paired over rotation × seed; `independent_rotations` = rotations where this judge played no role)

| judge | prompt | contrast | n_pairs | delta_asr | lo | hi | conclusion | independent_rotations | unresolved_share |
|---|---|---|---|---|---|---|---|---|---|
| deepseek_v4_pro | judge | label - audit | 9 | 0.702 | 0.631 | 0.778 | label worse |  | 0.000 |
| deepseek_v4_pro | judge | label - audit_memory | 9 | 0.778 | 0.702 | 0.849 | label worse |  | 0.000 |
| deepseek_v4_pro | judge | label - audit_tighten | 9 | 0.773 | 0.693 | 0.849 | label worse |  | 0.000 |
| deepseek_v4_pro | judge | label - audit_adaptive | 9 | 0.787 | 0.716 | 0.858 | label worse |  | 0.000 |
| deepseek_v4_pro | judge_rubric | label - audit | 9 | 0.729 | 0.649 | 0.800 | label worse |  | 0.000 |
| deepseek_v4_pro | judge_rubric | label - audit_memory | 9 | 0.756 | 0.667 | 0.836 | label worse |  | 0.000 |
| deepseek_v4_pro | judge_rubric | label - audit_tighten | 9 | 0.751 | 0.662 | 0.831 | label worse |  | 0.000 |
| deepseek_v4_pro | judge_rubric | label - audit_adaptive | 9 | 0.764 | 0.671 | 0.853 | label worse |  | 0.000 |
| glm53 | judge | label - audit | 9 | 0.756 | 0.684 | 0.822 | label worse |  | 0.000 |
| glm53 | judge | label - audit_memory | 9 | 0.769 | 0.684 | 0.840 | label worse |  | 0.000 |
| glm53 | judge | label - audit_tighten | 9 | 0.769 | 0.684 | 0.844 | label worse |  | 0.000 |
| glm53 | judge | label - audit_adaptive | 9 | 0.778 | 0.698 | 0.844 | label worse |  | 0.000 |
| glm53 | judge_rubric | label - audit | 9 | 0.707 | 0.644 | 0.769 | label worse |  | 0.000 |
| glm53 | judge_rubric | label - audit_memory | 9 | 0.778 | 0.693 | 0.858 | label worse |  | 0.000 |
| glm53 | judge_rubric | label - audit_tighten | 9 | 0.760 | 0.671 | 0.849 | label worse |  | 0.000 |
| glm53 | judge_rubric | label - audit_adaptive | 9 | 0.782 | 0.698 | 0.858 | label worse |  | 0.000 |
| kimi_k3 | judge | label - audit | 9 | 0.627 | 0.538 | 0.720 | label worse | R1,R2,R3 | 0.002 |
| kimi_k3 | judge | label - audit_memory | 9 | 0.778 | 0.702 | 0.853 | label worse | R1,R2,R3 | 0.002 |
| kimi_k3 | judge | label - audit_tighten | 9 | 0.741 | 0.655 | 0.830 | label worse | R1,R2,R3 | 0.002 |
| kimi_k3 | judge | label - audit_adaptive | 9 | 0.791 | 0.720 | 0.862 | label worse | R1,R2,R3 | 0.002 |
| minimax_m3 | judge | label - audit | 9 | 0.556 | 0.449 | 0.671 | label worse |  | 0.000 |
| minimax_m3 | judge | label - audit_memory | 9 | 0.760 | 0.689 | 0.836 | label worse |  | 0.000 |
| minimax_m3 | judge | label - audit_tighten | 9 | 0.724 | 0.622 | 0.831 | label worse |  | 0.000 |
| minimax_m3 | judge | label - audit_adaptive | 9 | 0.796 | 0.729 | 0.858 | label worse |  | 0.000 |
| minimax_m3 | judge_rubric | label - audit | 9 | 0.582 | 0.467 | 0.707 | label worse |  | 0.000 |
| minimax_m3 | judge_rubric | label - audit_memory | 9 | 0.773 | 0.698 | 0.849 | label worse |  | 0.000 |
| minimax_m3 | judge_rubric | label - audit_tighten | 9 | 0.738 | 0.640 | 0.836 | label worse |  | 0.000 |
| minimax_m3 | judge_rubric | label - audit_adaptive | 9 | 0.800 | 0.729 | 0.867 | label worse |  | 0.000 |
| muse_spark | judge | label - audit | 9 | 0.680 | 0.564 | 0.787 | label worse | R1,R2,R3 | 0.000 |
| muse_spark | judge | label - audit_memory | 9 | 0.760 | 0.689 | 0.827 | label worse | R1,R2,R3 | 0.000 |
| muse_spark | judge | label - audit_tighten | 9 | 0.693 | 0.564 | 0.813 | label worse | R1,R2,R3 | 0.000 |
| muse_spark | judge | label - audit_adaptive | 9 | 0.778 | 0.702 | 0.849 | label worse | R1,R2,R3 | 0.000 |

- Reproduction check: re-scoring with the episode's own primary judge reproduces its ASR exactly in 96% of 54 episodes (deployed texts are stored truncated to 400 characters; differences come from that or from cache misses).

**Judge sensitivity, S3b** (violation rate of delivered texts, unconstrained − governed, paired by backbone × seed; S3b's primary judge was kimi_k3, so its row is a re-test, not a confirmation)

| judge | prompt | n_pairs | viol_unconstrained | viol_governed | gap | lo | hi | unresolved_share | conclusion |
|---|---|---|---|---|---|---|---|---|---|
| deepseek_v4_pro | judge | 18 | 0.989 | 0.144 | 0.844 | 0.767 | 0.917 | 0.000 | governed cleaner |
| deepseek_v4_pro | judge_rubric | 18 | 0.956 | 0.161 | 0.794 | 0.711 | 0.878 | 0.000 | governed cleaner |
| glm53 | judge | 18 | 0.978 | 0.161 | 0.817 | 0.733 | 0.894 | 0.000 | governed cleaner |
| glm53 | judge_rubric | 18 | 0.972 | 0.189 | 0.783 | 0.700 | 0.867 | 0.000 | governed cleaner |
| kimi_k3 | judge | 18 | 0.989 | 0.189 | 0.800 | 0.694 | 0.894 | 0.000 | governed cleaner |
| minimax_m3 | judge | 18 | 0.989 | 0.328 | 0.661 | 0.544 | 0.772 | 0.000 | governed cleaner |
| minimax_m3 | judge_rubric | 18 | 0.983 | 0.211 | 0.772 | 0.678 | 0.861 | 0.000 | governed cleaner |
| muse_spark | judge | 18 | 0.989 | 0.194 | 0.794 | 0.700 | 0.883 | 0.000 | governed cleaner |

- Everything here is exploratory (before the freeze). Texts in the bank were written under specific episodes; the evasion proxy ignores selection against the honest candidate, so it is an upper-bound proxy of per-round ASR, compared against the observed rotations rather than read as a prediction.