# S7b_C per-rotation message read-out (2026-10-25 review; exploratory, post hoc, $0)

Question (2026-10-24 review): why is C5b (Gmsg − G0 content integrity) 0.000 in rotation R2?
Source: data/runs/S7b_C/*/messages.csv (primary in-stage judge) and data/runs/A7_C_outside_judge/S7b_C--*/verdicts.csv
(outside judge Qwen3-235B). Script: tools/s7b_c_rotation_readout.py (stdlib). All 120 units, 2,880 messages.
Rotations: R1 backbone DeepSeek-V4-Pro / auditor MiniMax-M3 / judge GLM-5.3; R2 MiniMax-M3 / GLM-5.3 / DeepSeek-V4-Pro;
R3 GLM-5.3 / DeepSeek-V4-Pro / MiniMax-M3.

| rot | planner | G0 non-factual (primary) | Gmsg non-factual (primary) | G0 violating (outside) | Gmsg violating (outside) | Gmsg auditor actions (pass/rewrite/template) |
|---|---|---|---|---|---|---|
| R1 | natural (n=120) | 0.300 | 0.167 | 0.275 | 0.150 | 83/36/1 |
| R1 | structured (n=360) | 0.075 | 0.017 | 0.058 | 0.025 | 336/24/0 |
| R2 | natural (n=120) | 0.000 | 0.000 | 0.067 | 0.042 | 104/14/2 |
| R2 | structured (n=360) | 0.000 | 0.000 | 0.064 | 0.039 | 311/43/6 |
| R3 | natural (n=120) | 0.750 | 0.142 | 0.842 | 0.175 | 29/81/10 |
| R3 | structured (n≈358) | 0.112 | 0.106 | 0.161 | 0.147 | 354/6/0 |

Reading:
- The R2 null is a floor effect, not an auditor failure: the primary judge (DeepSeek-V4-Pro) finds 0/720 non-factual
  G0 messages from the MiniMax-M3 backbone, so there is nothing to remove. GLM-5.3 still rewrote or templated 65/480
  (13.5%) R2 messages that the primary judge rated clean (restriction cost under the outcome taxonomy, not a gain).
- The outside judge sees a low but non-zero R2 base rate (6.4–6.7%) and a small reduction under Gmsg (≈2.5 pp), so part
  of the floor is the primary judge's leniency in R2. Judge and backbone are confounded by the rotation design; these runs
  cannot separate "MiniMax-M3 writes clean messages" from "DeepSeek-V4-Pro judges leniently".
- The C5b gain is driven by backbones that write manipulative free-form messages (R3 GLM-5.3 natural: 0.750 → 0.142;
  R1 natural 0.300 → 0.167). For structured plans the auditor barely acts in R3 (6/360 rewrites) and residual
  non-factual rates stay ≈0.11 — an auditor-sensitivity gap for DeepSeek-V4-Pro as auditor on structured-plan messages.
- No per-message CIs here (clustered by scenario would be needed); descriptive only. Not part of the frozen confirmatory analysis.
