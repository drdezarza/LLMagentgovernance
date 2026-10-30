# Data guide

All data in this repository were produced by the pipeline in `agentgov/`, between 13 and 29 October 2026, using
models served by Nebius AI Studio / Token Factory (plus one local Llama Guard model for A6). Nothing was edited
by hand, except the documented provenance corrections in `reports/labeling_v2/`. The data are released under
CC BY 4.0 (see `DATA_LICENSE.md`).

```
data/
  runs/<STAGE>/<UNIT>/        raw records of one unit (one simulation run, episode, cell or evaluator battery)
  runs/<STAGE>/_analysis/     outputs of the stage's analyze(): CSV tables, PNG figures, findings.md, validity, manifest
  catalog/                    model catalogue snapshot and the alias → model-ID binding used by the last session
  ledger/                     per-call ledger (tokens, cost, latency, cache hits); no prompt or response text
  superseded/                 unit outputs replaced under a pre-specified re-run rule, kept for provenance
reports/
  prereg/                     analysis plan for the confirmatory stages and its freeze record (hashes, amendment)
  labeling/                   2026-10-14 annotation sample (60 real messages, AI-assisted) with rubric and key
  labeling_v2/                H1 annotation sample (78 items): two annotator files, adjudication, AI pass, provenance
  operating_characteristics*  attacks admitted, legitimate messages lost and inference cost per 100 messages
paper/numbers.json            every number in the manuscript → source file, selector, value, tolerance, usage
```

## Units and their files

A *unit* is the smallest piece of work that is either complete or not. Its directory name is its ID, and encodes the
design cell: for example, `R2-adaptive-audit_memory-s103` (rotation, attacker mode, governor, seed) or
`R1-sc1011-SEQUENTIAL-Gmsg-nr20` (rotation, scenario, planner, mechanism, non-response level).

Every unit has:

| File | Contents |
|---|---|
| `result.json` | `unit` (design cell), `status` (`done` / `error` / `model_unavailable` / `reset`), `attempts`, `session`, start/finish times, `duration_s`, `fingerprint` (see below) and `summary`, the flat dictionary of unit-level outcomes used by the analysis |
| `manifest.json` | Experiment ID, unit, full parameter set and provenance written when the unit ran |

Additional files by simulator:

### Cooperation game (`S3b*`, `S5*`, `S2`, `S3`, `S6*`)

| File | Contents |
|---|---|
| `config.json` | Game configuration (agents, network topology, steps, deployment interval, governance mode, seed) |
| `timeseries.csv` | Per step: cooperation rate, ECS and its components (autonomy retention, epistemic integrity, subgroup fairness), payoffs, persuasion and backlash rates |
| `policy_log.csv` | Every deployed message policy: target mode, theme, intensity, timing, declared claims label, source (honest / attacker / fallback), judged labels and the narrative text |
| `agents.csv` | Final state of each agent |
| `rounds.csv` | Adversarial stages, one row per deployment round: deployed source, attack success, honest false positive, number of attacker candidates, detections, intensity cap, auditor-invalid and judge-invalid counters, stored detections (`n_caught`), extra auditor context in characters, judged labels of the deployed text |
| `candidates.csv` | Every candidate in every round (honest and attacker) with declared labels, auditor labels, judge labels, selection and hard-fail flags, and the text (truncated at 700 characters) |
| `states.jsonl` | Public state shown to the compiler and attacker at each deployment round |
| `extractor.csv` | `S5g`/`S5h` only: each distinct caught excerpt (SHA-1 prefix), whether the quarantined extractor returned a parseable tag list, and the tags |
| `judged_messages.csv`, `timeseries_text.csv` | `S3b*` only: judge verdicts on delivered narratives and the time series rescored with text-judged integrity |

### Demand-response feeder (`S7*`, `S4*`)

| File | Contents |
|---|---|
| `timeseries.csv` | Per hour: voltage range and violations, head import and overload, requested and curtailed kW, compliance, executed planning mode |
| `messages.csv` | Every household message: declared and used theme, governor action (`pass`, `rewrite` or `template`), status kind (measured / forecast / precautionary overload), judge labels and validity, and the text |
| `realized.csv` | Every household request: requested and realized kW, compliance, household archetype and position, base willingness, LLM persuasion shift, and in `S7c` whether the household is a non-responder |
| `plan_log.csv` | Planner declarations and revisions |

The feeder objective (lower is better) is `O = E_over + 4000·V_viol + 0.25·E_curt`: cumulative head-limit overload,
aggregate voltage violation and curtailed energy. It is a benchmark loss, not a calibrated monetary welfare function.

### Evaluator and replay stages (`A*`, `S5e`–`S5g`)

| File | Contents |
|---|---|
| `labels.csv` / `verdicts.csv` | One row per evaluated text: the parsed label fields (claims, theme, intensity, manipulative), validity, number of tries and, where applicable, the reference label |
| `items.csv` | Replay stages: the fixed items (candidate, source episode, history position, judge reference) |
| `attempts.csv` | `A0`: every attacker interface attempt by token budget, with validity, latency and cost |
| `bank.csv`, `items.csv` at stage level | Shared, frozen inputs evaluated by every unit of the stage |

## Analysis outputs (`_analysis/`)

| File | Contents |
|---|---|
| `findings.md` | Human-readable results of the stage, with sample sizes, eligibility, intervals and the pre-specified reading |
| `findings_interim.md` | The last interim analysis while the stage was incomplete (historical) |
| `*.csv` | Every table behind `findings.md`; names are descriptive (for example `confirmatory_C2_C4.csv`, `s5h_contrasts.csv`, `nonresponse_effects.csv`) |
| `*.png` | Figures |
| `validity.json` | Pre-specified validity rules (`rules`, `rules_version`), units done and eligible, exclusion reasons and counts by group |
| `analysis_manifest.json` | When the analysis ran, analysis-code hash, rubric hash, parameters, design hash, expected and done units, the code versions the units ran under, and the list of contributing unit IDs |
| `history/` | Earlier versions of `findings.md` that later analyses replaced (for example after a bug fix), named by timestamp |

## Provenance fingerprints

Each `result.json` carries a `fingerprint`:

* `params`: hash of the full stage parameters;
* `design`: hash of the parameters excluding unit lists such as seeds, so that a design change is detectable while
  added seeds are not (`retry --stale`);
* `code`: hash of the `agentgov` source at the time the unit ran;
* `config`: hash of `config/settings.yaml` and `config/plan.yaml`.

`analysis_manifest.json → unit_code_versions` counts how many units of a stage ran under each code hash. A few
exploratory stages contain units from more than one code version, because bugs that did not affect the stage were fixed
between sessions. Each such case is recorded and was checked.

## Ledger (`data/ledger/`)

`calls.csv.gz` has one row per model call (416,219 calls, mock calls excluded). Columns: `ts` (Unix time),
`day`, `session`, `experiment`, `unit`, `role` (planner, compiler, agent, attacker, auditor, judge, extractor, …),
`model`, `prompt_tokens`, `completion_tokens`, `reasoning_tokens`, `cost_usd` (list price, 0 for cache hits),
`latency_s`, `cached`, `mock`, `status`, `finish_reason`, and `cost_equiv_usd` (what a cache hit would have cost
uncached). `cost_by_stage.csv` aggregates it by stage. Prompts and responses are not included.

## Annotation materials

* `reports/labeling/`: 60 real messages sampled on 2026-10-14 (`sample.csv`), the blinded rubric, the key linking items
  to their source, and the labels (human with AI assistance; see `provenance.json`). These are calibration material.
* `reports/labeling_v2/`: the H1 sample of 78 stratified items (`items.csv`; sampling weights in `key.csv`), the
  rubric (`RUBRIC_v2.md`), the two annotator files (`annotator_A.csv`, `annotator_B.csv`), the adjudication, and one
  separate AI annotation pass (`annotator_AI.csv`). `PROVENANCE_CORRECTION.json` records the authors' statement that
  both annotators used MiniMax-M3 assistance. The original `ai_assistance=no` flags are left unchanged and superseded
  by that record. Annotator identities are pseudonymous (A1, B1).

## Known caveats

* Model text is not deterministic across providers and dates. The saved records are the evidence; live re-runs give
  new realisations.
* `S7c` reruns the `S7b_C` scenarios with fresh model calls. Its 0 % cells are its own baseline and do not reproduce
  the `S7b_C` cells exactly (19 of 120 differ in objective or integrity).
* Qwen3.5-397B temporarily left the provider catalogue on 2026-10-29. Its finished units remain in all analyses
  (`agentgov/experiments/base.py` keeps done units of models that are later unavailable).
