> **Provenance correction (2026-10-23):** The author stated (chat, 2026-10-23) that both H1 annotators (A1, B1) used MiniMax-M3 assistance. The ai_assistance=no flags in annotator_A.csv / annotator_B.csv are superseded by this statement and are left unchanged (original files). An earlier review (2026-10-20) had recorded the opposite; this correction replaces it. H1 is an AI-assisted reference, not independent human validation; agreement with MiniMax-family evaluators may be inflated by shared assistance.

**A4 — candidate judges vs the H1 reference** (exploratory; rules 2026-10-21). 78 items, reference decided on 72; 12/12 judge × prompt cells pass the ≥ 90% valid-label rule.

**All items and items without role overlap** (`no_overlap` drops items whose source stage used the judge's family as writer, auditor or judge; for deepseek / minimax / glm this leaves only S3b items they did not write)

| alias | prompt | scope | eligible_cell | n | unresolved | agreement | kappa | tpr | fpr | weighted_agreement |
|---|---|---|---|---|---|---|---|---|---|---|
| minimax_m3 | rubric | all | True | 72 | 0 | 0.972 | 0.944 | 0.974 | 0.030 | 0.947 |
| kimi_k3 | rubric | all | True | 72 | 0 | 0.944 | 0.888 | 0.949 | 0.061 | 0.933 |
| deepseek_v4_pro | rubric | all | True | 72 | 0 | 0.931 | 0.862 | 0.872 | 0.000 | 0.892 |
| qwen3_235b | rubric | all | True | 72 | 0 | 0.931 | 0.861 | 0.897 | 0.030 | 0.966 |
| glm53 | rubric | all | True | 72 | 0 | 0.917 | 0.833 | 0.897 | 0.061 | 0.879 |
| muse_spark | rubric | all | True | 72 | 0 | 0.847 | 0.700 | 0.718 | 0.000 | 0.816 |
| deepseek_v4_pro | rubric | no_overlap | True | 18 | 0 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| minimax_m3 | rubric | no_overlap | True | 20 | 0 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| glm53 | rubric | no_overlap | True | 26 | 0 | 0.962 | 0.885 | 1.000 | 0.167 | 0.931 |
| qwen3_235b | rubric | no_overlap | True | 60 | 0 | 0.933 | 0.866 | 0.862 | 0.000 | 0.966 |
| kimi_k3 | rubric | no_overlap | True | 46 | 0 | 0.935 | 0.864 | 0.895 | 0.037 | 0.922 |
| muse_spark | rubric | no_overlap | True | 72 | 0 | 0.847 | 0.700 | 0.718 | 0.000 | 0.816 |
| minimax_m3 | strict | all | True | 72 | 0 | 0.819 | 0.639 | 0.795 | 0.152 | 0.907 |
| kimi_k3 | strict | all | True | 70 | 2 | 0.786 | 0.567 | 0.816 | 0.250 | 0.881 |
| glm53 | strict | all | True | 72 | 0 | 0.778 | 0.550 | 0.821 | 0.273 | 0.872 |
| deepseek_v4_pro | strict | all | True | 72 | 0 | 0.764 | 0.521 | 0.821 | 0.303 | 0.860 |
| qwen3_235b | strict | all | True | 72 | 0 | 0.722 | 0.430 | 0.846 | 0.424 | 0.773 |
| muse_spark | strict | all | True | 72 | 0 | 0.708 | 0.411 | 0.744 | 0.333 | 0.740 |
| deepseek_v4_pro | strict | no_overlap | True | 18 | 0 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| glm53 | strict | no_overlap | True | 26 | 0 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| minimax_m3 | strict | no_overlap | True | 20 | 0 | 0.950 | 0.828 | 1.000 | 0.250 | 0.986 |
| muse_spark | strict | no_overlap | True | 72 | 0 | 0.708 | 0.411 | 0.744 | 0.333 | 0.740 |
| qwen3_235b | strict | no_overlap | True | 60 | 0 | 0.683 | 0.371 | 0.793 | 0.419 | 0.766 |
| kimi_k3 | strict | no_overlap | True | 44 | 2 | 0.682 | 0.342 | 0.611 | 0.269 | 0.857 |

**By source**

| alias | prompt | scope | eligible_cell | n | unresolved | agreement | kappa | tpr | fpr | weighted_agreement |
|---|---|---|---|---|---|---|---|---|---|---|
| deepseek_v4_pro | rubric | S3b | True | 26 | 0 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| deepseek_v4_pro | rubric | S5b | True | 26 | 0 | 0.885 | 0.755 | 0.727 | 0.000 | 0.864 |
| deepseek_v4_pro | rubric | S7b | True | 20 | 0 | 0.900 | 0.783 | 0.750 | 0.000 | 0.907 |
| deepseek_v4_pro | strict | S3b | True | 26 | 0 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| deepseek_v4_pro | strict | S5b | True | 26 | 0 | 0.885 | 0.761 | 0.818 | 0.067 | 0.948 |
| deepseek_v4_pro | strict | S7b | True | 20 | 0 | 0.300 | -0.346 | 0.375 | 0.750 | 0.287 |
| glm53 | rubric | S3b | True | 26 | 0 | 0.962 | 0.885 | 1.000 | 0.167 | 0.931 |
| glm53 | rubric | S5b | True | 26 | 0 | 0.885 | 0.761 | 0.818 | 0.067 | 0.864 |
| glm53 | rubric | S7b | True | 20 | 0 | 0.900 | 0.783 | 0.750 | 0.000 | 0.898 |
| glm53 | strict | S3b | True | 26 | 0 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| glm53 | strict | S5b | True | 26 | 0 | 0.923 | 0.842 | 0.909 | 0.067 | 0.965 |
| glm53 | strict | S7b | True | 20 | 0 | 0.300 | -0.400 | 0.250 | 0.667 | 0.287 |
| kimi_k3 | rubric | S3b | True | 26 | 0 | 0.962 | 0.885 | 1.000 | 0.167 | 0.992 |
| kimi_k3 | rubric | S5b | True | 26 | 0 | 0.885 | 0.761 | 0.818 | 0.067 | 0.906 |
| kimi_k3 | rubric | S7b | True | 20 | 0 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| kimi_k3 | strict | S3b | True | 26 | 0 | 0.962 | 0.885 | 1.000 | 0.167 | 0.992 |
| kimi_k3 | strict | S5b | True | 24 | 2 | 0.958 | 0.915 | 1.000 | 0.071 | 0.980 |
| kimi_k3 | strict | S7b | True | 20 | 0 | 0.350 | -0.383 | 0.125 | 0.500 | 0.343 |
| minimax_m3 | rubric | S3b | True | 26 | 0 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| minimax_m3 | rubric | S5b | True | 26 | 0 | 0.923 | 0.842 | 0.909 | 0.067 | 0.923 |
| minimax_m3 | rubric | S7b | True | 20 | 0 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| minimax_m3 | strict | S3b | True | 26 | 0 | 0.962 | 0.885 | 1.000 | 0.167 | 0.992 |
| minimax_m3 | strict | S5b | True | 26 | 0 | 0.962 | 0.922 | 1.000 | 0.067 | 0.983 |
| minimax_m3 | strict | S7b | True | 20 | 0 | 0.450 | -0.279 | 0.000 | 0.250 | 0.454 |
| muse_spark | rubric | S3b | True | 26 | 0 | 0.962 | 0.898 | 0.950 | 0.000 | 0.992 |
| muse_spark | rubric | S5b | True | 26 | 0 | 0.808 | 0.581 | 0.545 | 0.000 | 0.787 |
| muse_spark | rubric | S7b | True | 20 | 0 | 0.750 | 0.419 | 0.375 | 0.000 | 0.759 |
| muse_spark | strict | S3b | True | 26 | 0 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| muse_spark | strict | S5b | True | 26 | 0 | 0.846 | 0.685 | 0.818 | 0.133 | 0.804 |
| muse_spark | strict | S7b | True | 20 | 0 | 0.150 | -0.735 | 0.000 | 0.750 | 0.148 |
| qwen3_235b | rubric | S3b | True | 26 | 0 | 0.962 | 0.885 | 1.000 | 0.167 | 0.992 |
| qwen3_235b | rubric | S5b | True | 26 | 0 | 0.962 | 0.920 | 0.909 | 0.000 | 0.983 |
| qwen3_235b | rubric | S7b | True | 20 | 0 | 0.850 | 0.667 | 0.625 | 0.000 | 0.861 |
| qwen3_235b | strict | S3b | True | 26 | 0 | 0.962 | 0.885 | 1.000 | 0.167 | 0.992 |
| qwen3_235b | strict | S5b | True | 26 | 0 | 0.769 | 0.527 | 0.727 | 0.200 | 0.811 |
| qwen3_235b | strict | S7b | True | 20 | 0 | 0.350 | -0.182 | 0.625 | 0.833 | 0.352 |

- The H1 sample is enriched for hard cases; `weighted_agreement` uses 1/inclusion probability. n is small per source (≤ 26 decided), so read differences between judges as indicative.