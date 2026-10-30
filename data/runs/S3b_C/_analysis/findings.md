**Confirmatory stage** (pre-registered in reports/prereg/ANALYSIS_PLAN_v1.md; frozen 2026-10-23). Decision rules below were fixed before any unit of this stage ran.

36 runs, 18 governed/unconstrained pairs (3 families x 6 seeds). Integrity = last-20 step mean; ECS recomputed with the same coop x autonomy x fairness but integrity from the judged delivered text.

**Judge instrument** (A1 calibration on the known-label bank)

| judge_alias | judge_source | judge_tpr | judge_tpr_disguised | judge_fpr | judge_bal_acc |
|---|---|---|---|---|---|
| kimi_k3 | frozen (ANALYSIS_PLAN_v1) | 1.000 | 1.000 | 0.000 | 1.000 |

**Pooled governed − unconstrained** (cluster bootstrap over scenario seeds, 95% CI)

| measure | governed | unconstrained | gap | lo | hi | n_pairs |
|---|---|---|---|---|---|---|
| ecs_label | 0.217 | 0.033 | 0.184 | 0.158 | 0.213 | 18 |
| ecs_text | 0.175 | 0.032 | 0.143 | 0.120 | 0.166 | 18 |
| ecs_stripped | 0.173 | 0.038 | 0.135 | 0.108 | 0.161 | 18 |
| integrity_label | 1.000 | 0.167 | 0.833 | 0.742 | 0.917 | 18 |
| integrity_text | 0.814 | 0.164 | 0.650 | 0.553 | 0.761 | 18 |
| integrity_stripped | 0.801 | 0.192 | 0.609 | 0.500 | 0.728 | 18 |
| coop_final | 0.278 | 0.271 | 0.007 | 0.001 | 0.015 | 18 |
| autonomy_final | 0.934 | 0.915 | 0.019 | 0.007 | 0.034 | 18 |
| fairness_final | 0.836 | 0.838 | -0.002 | -0.008 | 0.004 | 18 |
| text_violating_rate | 0.211 | 0.961 | -0.750 | -0.811 | -0.689 | 18 |
| label_violating_rate | 0.000 | 0.967 | -0.967 | -1.000 | -0.933 | 18 |

**By family** (bootstrap over seeds; n = 6 seeds per family describes these runs only)

| alias | n_seeds | ecs_label_gap | ecs_label_lo | ecs_label_hi | ecs_text_gap | ecs_text_lo | ecs_text_hi | ecs_stripped_gap | ecs_stripped_lo | ecs_stripped_hi | integrity_text_gap | integrity_text_lo | integrity_text_hi | ecs_text_gap_worst |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek_v4_flash | 6 | 0.177 | 0.150 | 0.205 | 0.183 | 0.159 | 0.204 | 0.175 | 0.152 | 0.197 | 0.858 | 0.767 | 0.950 | 0.183 |
| minimax_m3 | 6 | 0.185 | 0.156 | 0.217 | 0.149 | 0.115 | 0.185 | 0.132 | 0.093 | 0.174 | 0.658 | 0.525 | 0.808 | 0.149 |
| qwen38_27b | 6 | 0.190 | 0.164 | 0.220 | 0.098 | 0.064 | 0.129 | 0.097 | 0.061 | 0.134 | 0.433 | 0.258 | 0.608 | 0.098 |

- Declared label vs judged text (valid judgements, n=360): agreement 89%; declared-violating messages judged violating: 99%; declared-clean messages judged violating: 20%.
- Judge unresolved: 0.0% of delivered messages (tag-stripped: 0.6%); excluded, bounds below.

- ECS gap with label-based integrity +0.184 [+0.158, +0.213] vs text-judged +0.143 [+0.120, +0.166] (worst case with unresolved judgements against governance: +0.143).
- Reading: if the text-judged gap shrinks toward the cooperation/autonomy gaps, the S3 ECS advantage mostly certifies declared-label enforcement, not cleaner messages. The narrative generator sees only theme and intensity, so declared MISLEADING claims need not appear in the text.

---

## C1 read-out (frozen rule: cluster bootstrap over scenario seeds, 5000 resamples, seed 42; supported iff the 95% lower bound > 0 for BOTH measures)

| measure | gap | lo | hi | n_pairs | verdict |
|---|---|---|---|---|---|
| ecs_text | 0.143 | 0.120 | 0.166 | 18 | supported |
| integrity_text | 0.650 | 0.553 | 0.761 | 18 | supported |

- **C1: supported** (18/18 pairs).