# Reviewer-response plan v2 (RR_PLAN_v2)

Written 2026-11-16, after the MDPI reviews of submission v14-2 (`paper/submission/comments_reviewers_deCurto.docx`)
and **before any unit of the paid stages below ran**. Hashed in `RR2_FROZEN.json` together with the code that
implements it. Like RR_PLAN_v1 these are **exploratory reviewer-response analyses**: they are not part of
ANALYSIS_PLAN_v1 and they leave every frozen `*_C` stage and every RR_PLAN_v1 stage unchanged. Changing a rule below
after a unit has run needs a new stage id and a dated note at the end of this file.

Disclosure: while designing S7d, the author's assistant looked at the S7b cell means by plan and mechanism (the
objective split into overload, voltage and curtailment terms, and the governor action counts). That inspection
motivated the S7d hypotheses; it is reported in P1. It also looked at the hourly traces (P1e) and found that
SEQUENTIAL's mean advantage over SEARCH in S7b_C comes from one scenario (R3, scenario 3015: SEARCH requested no
curtailment all day because the hour-0 forecast showed no overload, and it never re-plans). S7d itself uses new cells.

## Reviewer comment → work item

| Comment | Work item | API cost |
|---|---|---|
| R1.6 differences between planning methods, with reasons | **P1** decomposition of existing feeder records (S4b, S7b, S7b_C, S7c) | $0 |
| R1.6 (same), controlled test of the mechanism P1 points to | **S7d_search_mechanism** | ~$8–12 |
| R1.3 rationale for the LLMs used; advantages and limitations | **M1** model-evidence table from existing records | $0 |
| R1.3 / R1.4 cost and deployability of the auditor | **A8b_cheap_auditor_live** | ~$5–8 |
| R2.2 tags vs label-only memory unresolved | **S5j2_labelonly_extension** (optional, runs last) | ~$15–20 |

Shared rules: paired bootstrap 5000, seed 42; validity rules of the source study, unchanged; eligible units only;
"resolved" means the 95% CI excludes 0. Results describe these runs, not a population.

## P1 — planner decomposition (no API calls; `tools/rr2_planner_decomposition.py`)

Feeder objective (upstream definition): `objective = overload + voltage + curtailment` with
overload = head_over_kwh, voltage = 4000 × v_violation_total, curtailment = 0.25 × curtailed_kwh. S4b adds
latency price × decision latency.

1. **P1a** components by plan × governance (S7b, S7b_C, S7c at 0% non-response), with process measures: curtailed
   kWh, requests capped by the governor, mean compliance, revisions, directive realisation, message rewrites.
2. **P1b** plan differences under G0, paired by scenario: SEARCH − SEQUENTIAL and SEARCH − HIERARCHICAL, per
   component; per rotation (backbone); count of scenarios each plan wins.
3. **P1c** mechanism effects per plan (S7b): each mechanism − G0, paired by scenario, per component, with the
   governor's action counts.
4. **P1d** S4b: per scenario family × planning mode, objective terms + latency penalty + deadline misses /
   downgrades; winner and margin.
Descriptive only; no verdicts.

## S7d_search_mechanism (paid; feeder; new cells)

**Hypotheses (from P1 inspection, stated before S7d runs).**
- H1: SEARCH's best-of-N grid includes an escalated intensity (1.35 × declared). After the cap of 0.8 on the
  declared intensity, the escalated branch still asks households for up to 1.0 × flexible load, so only SEARCH hits
  the per-household cap (S7b: 214 capped requests per SEARCH episode, 0 for every other plan). H1: removing the
  escalated branch removes most of the cap's cost on SEARCH.
- H2: part of SEARCH's advantage under G0 comes from asking for more curtailment via escalation, not from
  lookahead alone.
- H3: SEARCH plans once with a fixed compliance prior (0.60), while SEQUENTIAL/HIERARCHICAL re-plan on violations with
  the observed compliance. SEQUENTIAL beats SEARCH in 5/15 S7b_C scenarios. H3: giving SEARCH the same feedback
  (re-plan on violation, learned compliance prior) improves it, most where SEQUENTIAL won.

**Design.** Backbone/judge rotations and scenario seeds of S7b (seeds 1–3) and S7b_C (seeds 11–15): 3 rotations
× 8 scenarios = 24 independent scenarios. Cells:
- SEARCH × escalation {on, off} × feedback {off, on} × governance {G0, Gcap} (192 cells);
- SEQUENTIAL reference × {G0, Gcap} (48 cells; G0 cells reproduce S7b/S7b_C).
`escalation off` = the SEARCH grid uses only the declared intensity. `feedback on` = SEARCH re-plans on a cap violation
with the observed compliance prior, exactly like SEQUENTIAL. With both at default the episode is bit-identical to S7b
(equivalence test). Messages: S7b honest-status rule; judge as in S7b (content integrity reported, not tested).

**Reading rules** (paired by scenario, n = 24 unless cells are missing):
- **R-D0 reproduction:** default SEARCH and SEQUENTIAL cells must reproduce the S7b / S7b_C objective of the same
  (rotation, scenario, governance) cell to 1e-6. Report the count and the largest deviation.
- **R-D1 (H1):** cap cost C = Gcap − G0 (objective) for SEARCH, with escalation on and off (feedback off).
  D1 = C(off) − C(on). **"Escalation explains the cap cost"** if D1 is resolved negative and the escalation-off
  SEARCH has no capped household requests; also report the share explained, 1 − C(off)/C(on). Otherwise
  "not explained".
- **R-D2 (H2):** under G0, feedback off: SEARCH(off) − SEARCH(on) (what escalation buys) and SEARCH(off) −
  SEQUENTIAL (does lookahead without escalation still beat SEQUENTIAL?). Each: resolved higher / lower / unresolved.
- **R-D3 (H3):** under G0, escalation on: SEARCH(feedback on) − SEARCH(feedback off), in all 24 scenarios and
  in the 5 S7b_C scenarios where SEQUENTIAL beat SEARCH (list fixed now: the S7b_C G0 scenarios where SEQUENTIAL
  had the lower objective; computed by the analysis from S7b_C cells, which exist before S7d runs:
  R1-sc1011, R1-sc1014, R2-sc2015, R3-sc3014, R3-sc3015). Same labels. Because R3-sc3015 was seen before S7d
  (disclosure above), R-D3 is also reported without it (all 23 and the remaining 4); a conclusion that holds only
  with R3-sc3015 is reported as "driven by one scenario".
- **R-D4:** each contrast decomposed into overload, voltage and curtailment terms (descriptive).
- **Consequence fixed in advance:** the paper states a mechanism ("SEARCH wins by escalating requests, which the
  cap removes" / "SEARCH lacks compliance feedback") only for a resolved rule; otherwise it reports the P1 traces
  as consistent with, not as establishing, the mechanism.

## M1 — model evidence table (no API calls; `tools/rr2_model_evidence.py`)

One row per model family used in the paper's main studies (population, attacker, auditor, judge, planner backbone):
roles played, provider price, interface profile (S0: valid output, thinking setting, latency), measurement
quality as judge/auditor (A1, A3, A8 where present), auditor effect on attack success and misclassification
(S5i), governance gap with that backbone (S3), cost per 1000 audits (A8). Descriptive; missing cells stay empty.

## A8b_cheap_auditor_live (paid; closed loop)

A8 found two cheaper auditors that match frontier sensitivity on fixed texts (DeepSeek-V4-Flash, Qwen3.8-27B) and
said they need a closed-loop check before being recommended.

**Design.** Exactly the S5i cell design with the auditor replaced: attackers {DeepSeek-V4-Pro, MiniMax-M3,
GLM-5.3} × cheap auditor {deepseek_v4_flash, qwen38_27b}, governor plain audit, judge fixed Kimi-K3, seeds 301–304,
population and attacker budgets as S5i (24 episodes). The frontier comparison arm is the existing S5i plain-audit
cells at the same attacker × seed (same seeds, judge and population).

**Reading rules** (S5b validity rules; contrasts paired within attacker × seed, n = 12 per cheap auditor):
- **R-B1:** cheap − frontier ASR per round, frontier = mean of the three S5i auditors in that attacker × seed cell.
  **"Non-inferior"** if the CI upper bound < +0.05; "inferior" if the lower bound > 0; otherwise "unresolved".
- **R-B2:** the same for auditor misclassification of judge-clean honest proposals (margin +0.05).
- **R-B3:** observed cost per 1000 audits and median latency for each auditor in the closed loop.
- Sensitivity: R-B1/R-B2 also against each frontier auditor separately, and without same-family cells
  (DeepSeek-V4-Flash auditing DeepSeek-V4-Pro).
- **Consequence fixed in advance:** a cheap auditor is described as a "closed-loop candidate" only if R-B1 and
  R-B2 are both non-inferior; otherwise the paper keeps the frontier auditors and reports A8 as fixed-text only.

## S5j2_labelonly_extension (paid; optional; runs last)

Same arms, rotations, instruments and rules as S5j (plain audit, label-only memory, quarantined tags), new seeds
409–416 (72 episodes).

**Reading rules.**
- The S5j result on seeds 401–408 remains the pre-specified answer and is reported unchanged.
- **R-J1x/R-J2x/R-J3x:** S5j's R-J1–R-J3 recomputed on seeds 401–416 combined (48 pairs), plus seeds 409–416
  alone, plus per rotation.
- **Consequence fixed in advance:** no further extension whatever the outcome. If R-J1x is not "lower (resolved)",
  the paper says tags show no demonstrated blocking advantage over label-only memory. If it is resolved but a
  rotation shows the opposite sign, the paper says the advantage is rotation-dependent.

## Order and budget

Run order: A8b → S7d → S5j2 (P1 and M1 need no session). Expected ≈ $30–40 in total, under the $30/day and
$1000/month caps: a long session stops at the daily cap and S5j2 resumes the next day unless the author raises
that day's cap in `config/budget_overrides.yaml`.

## Amendments

**1 (2026-11-17, 01:45; A8b finished, S7d at 229/240 units, S5j2 not started).** R-D0 found that 10 of the first 54
default S7d cells did not reproduce S7b / S7b_C to 1e-6 (largest deviation 92 on R3-sc3011 SEARCH G0; most < 1%).
Cause (traced from the hourly records and the cache): until today the LLM cache stored answers with INSERT OR
REPLACE. Paired cells send identical prompts until their paths diverge, and parallel workers sometimes sent the
same prompt at the same moment; each received its own sample and the cache kept the last, which was not always the
one a given cell had used. Re-running such a cell from the cache then follows a slightly different path (in
R2-sc2001-SEARCH-G0 the first difference is one household's reaction at hour 15; planner messages and requests
are identical). It affects replays of earlier runs, not the validity of any recorded run.
Changes, none of which alters a design, metric, exclusion or reading rule:
- Code: `Cache.put` now keeps the first stored answer and the calling unit uses it (`agentgov/llm.py`), so paired
  cells share one answer per prompt from S5j2 on. S7d's last 11 units and A8b ran under the old cache.
- New diagnostic `tools/rr2_cache_replay.py` (no API calls): replays every feeder cell from the cache with the current
  code and reports whether it reproduces the recorded objective. First result on the cache as of 00:35 (before S7d):
  S7b 162/180 exact (max deviation 16.5), S7b_C 100/120 (max 92.4), S7c 329/360 (max 70.2); the rest differ or
  cannot be replayed because the path reaches a prompt that was never cached.
- R-D0 is read together with the replay: an S7d default cell that equals the cache replay of its S7b / S7b_C cell
  reproduces S7b "up to the cache race". The S7d contrasts are unaffected in design (all S7d cells ran in one
  session under identical conditions).
- Addendum (2026-11-17, 07:30, S7d complete): replay on the final cache. S7d 175/240 cells exact; default cells (e1f0)
  96/96. Cells with feedback (e0f1, e1f1) mostly cannot be replayed (31/48 each): with feedback on, sibling cells (e.g.
  G0 and Gcap with escalation off, which are identical) sent the same prompts in parallel under the old cache. In-process
  and cross-process (PYTHONHASHSEED 1-3) runs of the feedback episodes with a deterministic stand-in model are
  identical, so this is the cache race, not non-determinism in the new code. R-D0 as computed: 54/66 default cells equal
  their S7b / S7b_C record; each of the 96 default cells equals its own cache replay, which is the same computation as replaying the S7b / S7b_C record.
