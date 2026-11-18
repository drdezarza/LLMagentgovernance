**Confirmatory stage** (pre-registered in reports/prereg/ANALYSIS_PLAN_v1.md; frozen 2026-10-23). Decision rules below were fixed before any unit of this stage ran.

**Outside judge** `qwen3_235b` (frozen rubric prompt; instrument rule ≥ 90% valid labels per source; the outside judge never decides a primary verdict):

| source | units | texts | valid_rate | cost | eligible |
|---|---|---|---|---|---|
| S3b_C | 36 | 360 | 1.000 | 0.048 | True |
| S5b_C | 36 | 2682 | 1.000 | 0.356 | True |
| S7b_C | 120 | 2880 | 1.000 | 0.112 | True |

**J1 judge sensitivity** (`same_conclusion` = the primary conclusion's direction/threshold holds under the outside judge)

| source | contrast | scope | n | est | lo | hi | primary_direction | same_conclusion |
|---|---|---|---|---|---|---|---|---|
| S3b_C | governed − unconstrained: violating rate (outside judge) | all backbones | 18 | -0.733 | -0.772 | -0.689 | negative | True |
| S3b_C | governed − unconstrained: violating rate (outside judge) | excl. qwen backbone (family overlap) | 12 | -0.850 | -0.900 | -0.808 | negative | True |
| S5b_C | label − audit: asr_outside | pooled | 12 | 0.687 | 0.633 | 0.740 | lower bound > 0 | True |
| S5b_C | audit_memory − audit: misclass_outside | pooled | 12 | 0.463 | 0.307 | 0.600 | lower bound > 0.1 | True |
| S7b_C | Gmsg − G0: content integrity (outside judge) | pooled | 15 | 0.086 | 0.051 | 0.121 | lower bound > 0 | True |

- Family overlap: Qwen3-235B is the S5b_C population (honest compiler) family and shares the Qwen family with the qwen38_27b S3b_C backbone; S3b_C is also shown without that backbone.
- Texts: S3b_C full narratives (policy_log.csv); S5b_C candidates.csv (truncated at 700 chars, as in A3); S7b_C full messages.