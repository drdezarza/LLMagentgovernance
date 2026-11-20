# Reports

| Path | Contents |
|---|---|
| `prereg/ANALYSIS_PLAN_v1.md` | Analysis plan for the confirmatory stages (S3b_C, S5b_C, S7b_C, A7_C_outside_judge) |
| `prereg/FROZEN.json` | Freeze record (2026-10-23): plan and code SHA-256 hashes, and one dated implementation amendment |
| `prereg/ANALYSIS_PLAN_DRAFT.md` | The draft the plan replaced |
| `prereg/RR_PLAN_v1.md`, `prereg/RR_FROZEN.json` | Reading rules for the first revision follow-ups (A8, S5i, S5j, S5k), frozen 2026-11-01 |
| `prereg/RR_PLAN_v2.md`, `prereg/RR2_FROZEN.json` | Reading rules for the second revision follow-ups (A8b, S7d, S5j2) and the no-API analyses, frozen 2026-11-16; one dated amendment (cache behaviour, 2026-11-17) |
| `prereg/RR_PLAN_v3.md`, `prereg/RR3_FROZEN.json` | Reading rules for the third revision follow-ups (A9, S5l, S5m) and the no-API analyses N1–N4, frozen 2026-11-18; one dated amendment (S5m prompt deviation and the S5m2 re-run, 2026-11-20) |
| `rr/` | Revision round 1: post hoc inference checks (`inference_check.*`) and the attack-success / false-rejection frontier figure |
| `rr2/` | Revision round 2: feeder objective decomposition (`P1_*`), model evidence table (`M1_*`), cache-replay audit (`R1_*`), execution sensitivity, auditor costs, message interventions and endpoint provenance |
| `rr3/` | Revision round 3: family-wise sensitivity of the confirmatory claims (`N1_*`), objective-weight and margin sensitivity (`N2_*`), household and subgroup burden (`N3_*`), runtime from the call ledger (`N4_*`); `manuscript_derived_checks.csv` holds two subgroup means averaged from `N3_subgroups.csv` for the number check |
| `labeling/` | 2026-10-14 calibration sample (60 real messages, AI-assisted labels), rubric and key |
| `labeling_v2/` | H1 reference sample (78 items): annotator files, adjudication, separate AI pass, provenance correction |
| `operating_characteristics*.{csv,md}` | Attacks admitted, legitimate messages lost and inference cost per 100 messages (exploratory and confirmatory) |
| `s7b_c_r2_readout_20261025.md` | Post hoc rotation read-out for S7b_C (descriptive) |

Annotation details and provenance are described in [`../docs/DATA.md`](../docs/DATA.md#annotation-materials).
