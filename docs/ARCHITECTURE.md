# Architecture

## Pipeline

```
python -m agentgov run [--hours H] [--workers N] [--only STAGE ...] [--mock]
  1. fetch the live model catalogue and bind roster aliases to model IDs      agentgov/models.py
  2. walk config/plan.yaml top to bottom; a stage runs when it is enabled and
     its prerequisites (class attribute `requires`) are complete               agentgov/runner.py
  3. a stage is a list of independent units; pending units run in parallel
     (process pool), each writing data/runs/<STAGE>/<UNIT>/result.json         agentgov/experiments/*
  4. every model call goes through one client: disk cache, ledger, budget
     caps, deadline and slow-model guards                                      agentgov/llm.py
  5. complete stages are analysed automatically (tables, figures, findings)
  6. a session journal, a NEXT.md hand-off and an HTML report are written      agentgov/report.py
```

Sessions are time-boxed and resumable: a unit is either done or not, so an interrupted session simply continues the next
time it runs. Paired conditions share cached calls, so resumed or repeated work costs nothing.

## Code map

| Path | Role |
|---|---|
| `agentgov/__main__.py` | Command line: `check`, `plan`, `status`, `run`, `analyze`, `retry`, `report` |
| `agentgov/runner.py` | Session loop, prerequisites, dispatch, interim and final analysis |
| `agentgov/llm.py` | Nebius client, cache, ledger, budget and deadline guard, reasoning-trace stripping |
| `agentgov/models.py` | Catalogue discovery, roster resolution, model groups |
| `agentgov/audit.py` | Strict parsing of auditor and judge labels; fail-closed vs unresolved semantics; bounds |
| `agentgov/mock.py` | Deterministic offline responder for `--mock` |
| `agentgov/provenance.py` | Code, parameter, design and configuration fingerprints; unit manifests |
| `agentgov/upstream/` | Simulators extracted from the predecessor projects (do not edit; regenerate with `tools/extract_upstream.py`) |
| `agentgov/gcge_ext.py` | Cooperation game with a pluggable deployment step: honest compiler, attacker, auditor, governors, judge |
| `agentgov/planning_ext.py` | Feeder with governance hooks (policy, allocation, message), honest-status message rule, non-response |
| `agentgov/experiments/base.py` | `Experiment` interface, validity rules, findings and manifest writer |
| `agentgov/experiments/*.py` | One class per stage (see `docs/EXPERIMENTS.md`) |
| `tests/test_equivalence.py` | With hooks off, both simulators reproduce the upstream code exactly |
| `tools/operating_characteristics.py` | Operating-characteristics tables in `reports/` |

## The two environments

**Networked cooperation game** (from GCGE). Agents on a scale-free network play a repeated cooperation game. Every
two steps, a message compiler broadcasts a policy: target mode, theme, intensity, timing and a *claims* label, plus a
natural-language narrative. A constitution caps intensity (0.80) and forbids fear appeals and non-factual claims. In
the adversarial stages, an attacker LLM submits two candidates per round, trying to get a rule-violating narrative
selected while declaring compliant labels. The governor selects among the honest candidate and the attacker's
candidates.

**Radial demand-response feeder** (from LLMstrategicplanning). Four laterals of ten households, a 1100 kW head import
limit, voltage limits 0.95–1.05 pu, and 24 hourly intervals. A planner (programmed SEQUENTIAL, HIERARCHICAL or SEARCH
executors, or *natural*, where the LLM declares its own plan) issues curtailment requests with an operator message.
Households respond through a game-theoretic willingness model with a bounded LLM persuasion shift. Under the
honest-status rule, messages state the measured overload, a labelled forecast, or a precautionary reason, and never
claim an overload that was not observed.

## Governors

**Game** (`gcge_ext.AttackDeployer`, `followup_exps.QuarantineDeployer`):

| Governor | Behaviour |
|---|---|
| `label` | Trusts the declared labels |
| `audit` | An auditor LLM labels every candidate's text; the audited labels replace the declared ones before selection |
| `audit_memory` | `audit` plus raw memory: the last six caught messages (declared vs audited labels and a 160-character excerpt) in the auditor prompt |
| `audit_memory_struct` | Label-only memory: the same detections without attacker-written text |
| `audit_neutral` | Neutral game-background context, length-matched to raw memory and present exactly when raw memory would be |
| `audit_quarantine` | Label-only records plus at most three tactic tags per detection, from a closed eight-tag vocabulary, assigned by a separate quarantined extractor; free text never passes the parser |
| `audit_tighten`, `audit_adaptive` | The cap tightens by 0.05 per detection (floor 0.60); adaptive combines tightening and memory |

**Feeder** (`planning_ext.S7B_GOVS`):

| Mechanism | Message audit | Intensity / per-household cap | Fairness reallocation |
|---|:-:|:-:|:-:|
| `G0` | | | |
| `Gmsg` | ✓ (rubric auditor: pass, one rewrite, or a factual template) | | |
| `Gcap` | | ✓ (intensity ≤ 0.8; request ≤ 0.8 × forecast flexible kW) | |
| `Ggini` | | | ✓ (reallocate when the cumulative-request Gini exceeds 0.45) |
| `G1r` | ✓ | ✓ | ✓ |

## Instruments

* **Auditor**: part of governance. It labels candidate text (claims: factual / exaggerated / misleading; theme;
  intensity; manipulative). An invalid or unparseable output **fails closed**, rejecting the message, and is counted.
* **Judge**: part of measurement. A model from a different family than every agent in the unit rates delivered text
  with the same label schema; the feeder stages use a fixed content rubric (`agentgov/experiments/calibration.py`). An
  unparseable judgement is **unresolved**, never a default verdict; analyses report valid-only estimates with
  bounds.
* **Calibration**: A1 (known-label bank), A2 (real messages, strict vs rubric prompts), H1/A4 (AI-assisted reference),
  A3 (fixed bank × every evaluator), A5/A6 (procedural and specialist baselines).
* **Attacker interface**: A0 picks, by a pre-specified rule, the smallest output budget at which each attacker family
  submits valid candidates in ≥ 90 % of attempts with a median latency ≤ 60 s. Adversarial stages read
  `data/runs/A0_attacker_interface/_analysis/recommended.json`.

## Model roster

Models are referenced by alias (`config/settings.yaml → roster`). Each alias lists candidate model IDs in order of
preference and binds to the first one in the live catalogue. The families used in the article:

| Alias | Model | Used as |
|---|---|---|
| `deepseek_v4_pro` | DeepSeek-V4-Pro | rotated attacker / auditor / judge / feeder planner |
| `minimax_m3` | MiniMax-M3 | rotated attacker / auditor / judge / feeder planner; S3b backbone |
| `glm53` | GLM-5.3 | rotated attacker / auditor / judge / feeder planner |
| `kimi_k3` | Kimi-K3 | S3b judge; quarantined tag extractor; A3/A4 judge |
| `qwen3_235b` | Qwen3-235B-A22B-Instruct-2507 | game compiler and agent population; outside judge (J1) |
| `deepseek_v4_flash`, `qwen38_27b` | DeepSeek-V4.1-Flash, Qwen3.8-27B | S3b backbones |
| `gpt_oss_120b`, `nemotron_super`, `muse_spark`, `qwen35_397b` | gpt-oss-120b, Nemotron-3-Super, Muse Spark, Qwen3.5-397B | calibration and judge comparisons |
| `llama-guard3:8b` (local) | Llama Guard 3 8B via Ollama | A6 specialist baseline |

The exact model IDs bound in the last session are in `data/catalog/resolved_roster.json`. The IDs used by each unit
are in its `manifest.json`.

## Adding a stage

1. Subclass `Experiment` (or an existing stage class) in `agentgov/experiments/`. Implement `units()`, which returns
   dictionaries with a unique `id`, `run_unit(unit, ctx, outdir)`, which returns a flat summary dictionary, and
   `analyze()`, which writes `_analysis/` and returns Markdown. Declare `requires`, `validity_rules` and a
   `rules_version` before running anything.
2. Register the class in `agentgov/experiments/__init__.py` and add an entry to `config/plan.yaml`.
3. Test offline: `python -m agentgov run --mock --hours 0.3 --only <STAGE>` (outputs go to `data/runs_mock/`).
4. Check the estimate with `python -m agentgov plan`, then run live.

A change to a stage's design after units have run should get a new stage ID, or be re-run with `retry --stale`.
Finished units are never silently reused under a different design.
