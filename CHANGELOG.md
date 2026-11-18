# Changelog

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
