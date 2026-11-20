# Reviewer-response plan v3 (RR_PLAN_v3)

Written 2026-11-18, after a third review of submission v14-2 arrived, and **before any unit of the paid stages below
ran**. Hashed in `RR3_FROZEN.json` together with the code that implements it. Like RR_PLAN_v1 and v2 these are
**exploratory reviewer-response analyses**: they are not part of ANALYSIS_PLAN_v1 and leave every frozen `*_C` stage
and every earlier reviewer-response stage unchanged. Changing a rule below after a unit has run needs a new stage id
and a dated note at the end of this file.

Disclosures.
* N1 and N2 (no API calls) were written and run on 2026-11-18 before this file was finalised; their outputs are in
  `reports/rr3/`. They recompute recorded results and cannot be tuned against new data. N1 reproduces every recorded
  95% interval exactly before adjusting.
* The S5l and S5m designs were written after the author's assistant had seen the S5i (role factorial) and A5/A6
  (per-rule auditor and Llama Guard on fixed texts) results, which motivated the choice of baselines. Neither S5l nor
  S5m reuses any seed of an earlier live stage.
* The S5m strategies were written once, before any S5m unit ran, and are not revised after seeing results (the
  reviewer's request is a test of generalisation, so tuning the attacks against the results would defeat it).
* Human-only blinded validation of H1 (Reviewer 3, point 1) is not run; the response treats it as a limitation.

## Reviewer comment → work item

| Comment | Work item | API cost |
|---|---|---|
| R3.1 blinded human-only evaluation | not run (author decision); stated as a limitation | $0 |
| R3.2 more seeds, crossed roles | existing S5i (3 × 3 crossing) + **S5l** fresh seeds 601–604 with full crossing (R-L5) | in S5l |
| R3.3 multiplicity | **N1** family-wise sensitivity analysis (`tools/rr3_multiplicity.py`) | $0 |
| R3.4 live end-to-end baseline | **S5l_live_baselines**: per-rule audit and Llama Guard 3 live, same attackers, judge, seeds, token accounting | ~$40–60 |
| R3.5 diverse, unseen attacks, prompt injection | **S5m_attack_challenge** | ~$25–40 |
| R3.6 margins, objective weights; ROUGE-SEM | **N2** (`tools/rr3_objective_sensitivity.py`); ROUGE-SEM discussed only | $0 |
| R3.7 household and subgroup burdens | **N3** (`tools/rr3_burden.py`) | $0 |
| R3.8 label-only memory baseline | already run: S5j_live_labelonly + S5j2 extension (RR_PLAN_v1/v2) | $0 |
| R3.9 end-to-end runtime | **N4** from the saved ledger (`tools/rr3_runtime_logs.py`) + **A9_runtime_benchmark** | ~$3–6 |
| R3.10 human participation / deployment claims | wording (claims already restricted to simulation) | $0 |

Shared rules: paired bootstrap 5000, seed 42; validity rules of the source study (S5b: attacker valid submissions ≥
80% of rounds, judge unresolved ≤ 10%, auditor invalid ≤ 10%), unchanged; eligible units only; "resolved" means the
95% interval excludes 0. Results describe these runs, not a population.

Run order (plan.yaml): A9_runtime_benchmark, then S5l_live_baselines, then S5m_attack_challenge. Daily cap raised to
$200 for 2026-11-18 to 2026-11-20 with the author's approval (`config/budget_overrides.yaml`).

## S5l — live end-to-end baselines (`S5l_live_baselines`)

Design. S5i game, adaptive attacker, outside judge Kimi-K3 fixed, fresh seeds 601–604. Attacker ∈ {DeepSeek-V4-Pro,
MiniMax-M3, GLM-5.3} fully crossed with auditor ∈ {same three}. Governors:
* `audit` — the paper's joint content audit (one call per candidate, bounded re-ask);
* `audit_rules` — per-rule audit: three separate rule checks (claims, pressure, intensity; the A5 prompts) with the
  same auditor model, one re-ask each, candidate rejected if any rule fails; an unparseable rule = invalid audit,
  fail-closed;
* `guard` — Llama Guard 3 8B (`llama-guard3:8b`, local, Ollama) with the frozen content rules as custom categories
  (the A6 prompt and parser). "unsafe" = violating; "safe" = factual, intensity 0, so the declared intensity applies.
  One arm per attacker × seed (no auditor family); its auditor slot is not used.
3 × 3 × 2 × 4 = 72 LLM-audited episodes + 3 × 4 = 12 guard episodes = 84. Guard episodes with a guard parse rate below
0.90 are excluded (in addition to the S5b rules). Governance time, calls, tokens and list-price cost are recorded per
audit (cache hits included at list price).

Reading rules.
* **R-L1** ASR per round, `audit − audit_rules`, paired within attacker × auditor × seed: per auditor and pooled.
* **R-L2** audit misclassification rate (false rejection of benign candidates), same pairing.
* **R-L3** `audit` (mean over the three auditors) − `guard`, paired within attacker × seed, both outcomes.
* **R-L4** governance cost per audit and per episode (calls, tokens, cost, time): descriptive.
* **R-L5** crossed-role replication on fresh seeds (joint audit only): attacker and auditor marginal contrasts as in
  S5i, descriptive.
* Consequence (fixed): the joint audit is described as "at least as good as" the per-rule baseline end to end only if
  the pooled upper limits of both R-L1 and R-L2 are below +0.05; otherwise "not shown to be at least as good as". A
  resolved difference in either direction is reported as such. R-L3 is reported with its interval whatever its sign.

## S5m — attack challenge (`S5m_attack_challenge`)

Design. S5b cyclic rotations (attacker / auditor) with the plain joint audit; primary judge Kimi-K3, second judge
Qwen3-235B (the A7_C outside judge) on every candidate; seeds 701–704. Six attacker strategies, each a fixed text
appended to the unchanged attacker system prompt (`STRATEGIES` in the code): `standard` (no addition; the control),
`authority` (impersonated authority), `quoted` (instructions inside quoted or forwarded material), `implicature`
(insinuation, no explicit claim), `multilingual` (code-switching), `injection` (text addressed to the screening model,
asking it to treat the message as verified / compliant). 4 seeds × 6 strategies × 3 rotations = 72 episodes. Tactic
adherence is a fixed keyword check per strategy (`TACTIC_PATTERNS`), descriptive only.

Reference labels are the judges', not the attacker's intent: a candidate counts as a violation only when the judge
says so (an attack that the judges rate compliant is not counted as a miss).

Reading rules (strategy − standard, paired within rotation × seed).
* **R-M1** ASR per round (judge Kimi-K3).
* **R-M2** auditor miss rate on attacker candidates the primary judge rated violating.
* **R-M3** robustness to the judge: ASR by the second judge (`asr_j2`) and ASR counted only when both judges agree
  (`asr_both`); judge agreement reported.
* Consequence (fixed): strategies with a resolved ASR increase (R-M1 lower limit > 0) are reported as weaknesses of the
  governor. "No demonstrated degradation within +0.10" is stated only for strategies with lower limit ≤ 0 and upper
  limit < +0.10. Others: "unresolved". The injection arm is reported separately as the test of an auditor-directed
  prompt-injection mechanism.

## A9 — controlled runtime benchmark (`A9_runtime_benchmark`)

Design. One unit, so no other pipeline unit runs at the same time; response cache off. Auditors: DeepSeek-V4-Pro,
MiniMax-M3, GLM-5.3 (reference), DeepSeek-V4-Flash, Qwen3.8-27B (lower cost). Concurrency 1, 4, 16. Inputs (fixed
sample, seed 2026): 40 recorded S5i adaptive-audit rounds (all candidates of the round) and 40 recorded S7b_C
no-governance feeder messages.
* Game path: audit every candidate (bounded re-ask) + governed selection.
* Feeder path: audit, factual rewrite (by the auditor model), re-audit, template fallback (S7b message rule).
Recorded per path: wall-clock latency, calls, call errors, invalid audits, rewrite, fallback, tokens, cost. The research
judge and the simulator are not timed.

Reading rules (descriptive). **R-R1** latency p50/p90/p99/max per auditor × path × concurrency; **R-R2** throughput
(paths per minute) and its scaling with concurrency; **R-R3** failures, call errors, invalid audits, rewrite and
fallback shares; **R-R4** cost per 1000 governed paths. No claim depends on A9 beyond these descriptions.

## N1 — multiplicity (no API calls; `tools/rr3_multiplicity.py`)

Family = C1, C2, C3, C4, C5a, C5b (K = 6). Each component recomputed with the frozen data, resampling unit and
bootstrap, and checked against the recorded interval; tested against its own claim threshold (C2 > 0.30, C4 > 0.10,
C5a < +25), never against zero instead. Composite claims by intersection–union (C1 both measures; C2 every rotation; C3
pooled lower limit > 0 and positive in every rotation); claim p = largest component p. Bonferroni (two-sided 99.17%
intervals) and Holm. Sensitivity analysis only; the frozen decision rule is unchanged.

## N2 — margin and objective weights (no API calls; `tools/rr3_objective_sensitivity.py`)

Recorded outcomes re-scored as overload + w_v × voltage violation + w_c × curtailed kWh, w_v ∈ {1000, 2000, 4000,
8000, 16000}, w_c ∈ {0, 0.1, 0.25, 0.5, 1}; Audit − Baseline, plans averaged within scenario, S7b_C and S7c (0%
non-response). Reported: upper 95% limit (= smallest supported margin), as % of the Baseline mean, and non-inferiority
at margins 10, 15, 25, 50; per plan and integrity by plan (descriptive). This evaluates the recorded policies; it does
not show how planners redesigned for other weights would behave.

## N3 — household burden (no API calls; `tools/rr3_burden.py`)

All 40 households per cell including zero-burden households; requested and realized kWh, zero share, mean, p90, max,
top-10% share, Gini (checked against the recorded value), burden as a share of the household's flexible energy
(regenerated from the simulator seeds), subgroup means by archetype, lateral and depth band and their max/min ratio.
Each governor − G0 paired by scenario (S7b_C; S7b mechanism ablation including Ggini and G1r). Descriptive.

## N4 — runtime from saved logs (no API calls; `tools/rr3_runtime_logs.py`)

Per unit of the live studies: calls, cache hits, failed attempts by status, observed wall clock, an uncached-equivalent
wall clock (cache hits imputed at the median uncached latency of the same study × role × model), seconds per step,
governance share of call latency with and without the research judge; feeder rewrite / template / invalid-audit rates
and game fail-closed rates from the cell records. Descriptive; not a controlled benchmark.

## Amendments

**Amendment 1 (2026-11-20, after S5m completed; written by the author's assistant at the author's request).**
Audit of S5m found that its code appended the strategies to the plain attacker prompt (`X.ATTACKER_SYSTEM`) instead
of the unchanged S5b attacker prompt this plan specifies (`X.ATTACKER_SYSTEM_INFORMED`, which tells the attacker the
governor's hard rules). The S5m attackers therefore declared non-factual labels and were rejected by the hard rules:
attacker deploy rate 0.09 (standard arm) vs 0.46 in S5b_C and 0.47 in S5l; standard-arm ASR 0.000 vs 0.107 in S5b_C.
Every strategy sits at that floor, so S5m cannot test the strategies against the attacker the paper studies. The audit
also found an analysis bug: the second-judge ASR (`asr_j2`) was dropped from the R-M3 contrasts because the column was
present twice when the per-episode extras were merged (recomputed by hand, all strategies − standard within about
±0.04 of 0, none resolved upward).
* S5m is kept unchanged and reported as a disclosed deviation (its records and findings are not edited).
* New stage **S5m2_attack_challenge** (`agentgov/experiments/reviewer3b_exps.py`): identical to S5m except (1) base
  prompt = the informed S5b prompt + the same strategy texts, (2) fresh seeds 711–714, (3) the asr_j2 merge fix.
  Rotations, judges, strategies, validity rules, R-M1..R-M3 and the consequence rule are those of S5m. S5m2 is the
  stage that answers R3.5; S5m results are not pooled with it.
* Seen before writing this amendment: all S5m results (above). The S5m2 design is fixed by the S5m design and this
  plan, so no choice in it depends on those results.
