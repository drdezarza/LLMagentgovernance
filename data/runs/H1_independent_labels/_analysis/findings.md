> **Provenance correction (2026-10-23):** The author stated (chat, 2026-10-23) that both H1 annotators (A1, B1) used MiniMax-M3 assistance. The ai_assistance=no flags in annotator_A.csv / annotator_B.csv are superseded by this statement and are left unchanged (original files). An earlier review (2026-10-20) had recorded the opposite; this correction replaces it. H1 is an AI-assisted reference, not independent human validation; agreement with MiniMax-family evaluators may be inflated by shared assistance.

78 items (items flagged AI-assisted in the CSVs, excluded: 0). **Inter-annotator agreement (three categories, 78 items): 77%, Cohen's κ 0.61.** Disagreements: 0 clean vs violating, 18 involving unsure.
- Binary agreement on the 60 items both annotators decided (unsure excluded, so it omits the 18 unsure disagreements): 100%, κ 1.00. Do not quote this figure alone.
- Reference: 72 decided, 0 disputed (need adjudication), 6 unsure.

**Evaluators vs the H1 reference** (`weighted_agreement` uses 1/inclusion probability, i.e. estimates agreement on the source populations rather than on the hard-case-enriched sample)

| evaluator | source | n | agreement | kappa | tpr | fpr | weighted_agreement |
|---|---|---|---|---|---|---|---|
| judge | all | 72 | 0.931 | 0.860 | 0.949 | 0.091 | 0.950 |
| judge | S3b | 26 | 0.962 | 0.885 | 1.000 | 0.167 | 0.992 |
| judge | S5b | 26 | 0.846 | 0.685 | 0.818 | 0.133 | 0.930 |
| judge | S7b | 20 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| auditor | all | 21 | 0.571 | 0.222 | 0.833 | 0.533 | 0.777 |
| auditor | S5b | 21 | 0.571 | 0.222 | 0.833 | 0.533 | 0.777 |
| declared | all | 52 | 0.558 | 0.219 | 0.258 | 0.000 | 0.553 |
| declared | S3b | 26 | 0.538 | 0.235 | 0.400 | 0.000 | 0.904 |
| declared | S5b | 26 | 0.577 | 0.000 | 0.000 | 0.000 | 0.472 |

**Secondary: each human annotator vs the earlier AI-assisted labels** (`annotator_AI.csv`, development material, not part of the reference; three categories)

- A vs AI: 87% (78 items), κ 0.79; B vs AI: 90% (78 items), κ 0.84; A vs B: 77%, κ 0.61.
- Items where A and B agree that also match the AI label: 60/60. Report this next to the human reference (annotators agree more with the AI file than with each other).