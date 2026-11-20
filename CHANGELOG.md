# Changelog

## 2026-11-20: revised manuscript (v14-7), third review

Material added for the third review of the manuscript. No confirmatory result, frozen plan or unit record of an
earlier stage was changed.

**New stages** (exploratory; reading rules in `reports/prereg/RR_PLAN_v3.md`, written and hashed before each stage ran)

* `A9_runtime_benchmark`: complete governed-message paths with the response cache off, five auditors, concurrency 1, 4
  and 16 (1200 paths).
* `S5l_live_baselines`: joint versus per-rule auditing under the same adaptive attackers, fully crossed with three
  auditors on fresh seeds, plus a local Llama Guard 3 arm (84 episodes).
* `S5m_attack_challenge`: five held-out attack strategies against the standard attack. **Disclosed deviation**: the
  strategies were appended to the plain attacker prompt instead of the informed S5b prompt the plan specifies, which
  left every arm at near-zero attack success. The batch is kept unchanged and is not used or pooled.
* `S5m2_attack_challenge` (Amendment 1, 2026-11-20): the same challenge with the informed prompt and fresh seeds, and a
  fix for a merge that dropped the second-judge contrast from the S5m report (72 episodes).

**New analyses** (no API calls): `reports/rr3/`, produced by `tools/rr3_*.py`: family-wise sensitivity of the six
confirmatory claims (N1), objective-weight and margin sensitivity of the feeder result (N2), household and subgroup
curtailment burden (N3) and episode runtime from the call ledger (N4).

**Code**: `agentgov/experiments/reviewer3_exps.py` and `reviewer3b_exps.py` (new stage classes), registry and
`config/plan.yaml` entries. No existing stage or simulator changed.

**Data and documentation**

* Ledger export updated (795,469 calls; $324 in total). Model catalogue snapshot updated.
* `paper/numbers.json`: 1430 checks against the revised manuscript (537 added); all pass.
* README, `docs/`, `reports/README.md`, `paper/README.md` and `Makefile` (`make revision-tables` now also runs the
  `rr3` tools) describe the new stages and analyses.

## 2026-11-18: revised manuscript (v14-7)

Material for the revision of the manuscript after peer review. No confirmatory result, frozen plan or unit record of
an earlier stage was changed.

**New stages** (exploratory; reading rules written and hashed before each stage ran)

* Round 1, `reports/prereg/RR_PLAN_v1.md`: `A8_auditor_scale` (fixed-text screen of eight lower-cost auditors),
  `S5i_role_factorial` (attacker × auditor factorial with a fixed outside judge), `S5j_live_labelonly` (live
  label-only versus tag memory), `S5k_oracle_feedback` (richer attacker feedback).
* Round 2, `reports/prereg/RR_PLAN_v2.md`: `A8b_cheap_auditor_live` (screened auditors against adaptive attackers),
  `S7d_search_mechanism` (search-planner escalation and feedback ablation), `S5j2_labelonly_extension` (one
  pre-specified extension of S5j).

**New analyses** (no API calls): `reports/rr/` and `reports/rr2/`, produced by `tools/rr_*.py` and `tools/rr2_*.py`:
post hoc inference checks, feeder objective decomposition, model evidence table, cache-replay audit, execution
sensitivity of the feeder contrasts, auditor costs and endpoint provenance.

**Code**

* `agentgov/llm.py`: the response cache now keeps the first stored answer for a prompt and returns it to concurrent
  callers. Before 2026-11-17, simultaneous identical calls could each draw a sample and the cache kept the last one.
  Documented in the dated amendment to `RR_PLAN_v2.md` and in `docs/REPRODUCING.md`.
* `agentgov/planning_ext.py`: scenario switches `search_escalation` and `search_feedback` for S7d; with their defaults
  every episode is identical to before (`tests/test_equivalence.py`).
* `agentgov/config.py`, `llm.py`: optional second provider (OpenCode Go) for the `*_go` replica stages, which are
  disabled and were not run.
* `tools/build_ledger_db.py`: rebuilds the SQLite ledger from `data/ledger/calls.csv.gz`.

**Data and documentation**

* Ledger export updated (636,814 calls; $242 in total). Model catalogue snapshot updated.
* `S7c_nonresponse/_analysis/findings.md`: wording of the 0 % note corrected (the 0 % cells rerun, not reproduce,
  S7b_C).
* `paper/numbers.json`: 893 checks against the revised manuscript; all pass.
* README, `docs/` and `reports/README.md` describe the new stages, the cache behaviour and the endpoint change of the
  `deepseek_v4_flash` alias.

## 2026-10-30: first release

Code, data and reproducibility materials for the submitted manuscript (v14-1).
