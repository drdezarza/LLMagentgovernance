# Independent labelling (v2) — instructions

Purpose: an **independent** human reference for the article's integrity measures. The 2026-10-14 sample was labelled
with AI assistance; it stays as development/calibration material. This sample must be labelled **without AI tools**.

1. Two annotators label **all** items in `items.csv` independently, each in their own copy of the template
   (`annotator_A.csv`, `annotator_B.csv`). Do not discuss items until both are finished. Do not open `key.csv`.
2. For each item fill:
   - `label`: clean / violating / unsure (rubric in RUBRIC_v2.md; unsure is allowed, never guess)
   - `reason`: one short sentence
   - `evidence_used`: what in the message or `context` decided it (e.g. "claims 91% cooperate; not verifiable")
   - `annotator_id`: an anonymous id (e.g. A1)
   - `ai_assistance`: no / yes (yes = any AI tool was used for that item; those items are excluded from the reference)
3. After both are done, resolve disagreements in `adjudication.csv` (`final_label`, `note`); leave agreed items blank.
The pipeline computes inter-annotator agreement, the adjudicated reference, and evaluator agreement weighted by the
recorded sampling probabilities. Files are never overwritten once any label is present.
