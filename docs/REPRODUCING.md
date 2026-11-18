# Reproducing the results

This repository ships the full record of every experiment: each unit's raw outputs, the analysis outputs and a
per-call cost ledger. You can verify the paper, recompute any analysis and exercise the pipeline without an API key.
Re-running experiments live requires a Nebius key and makes new model calls.

## 0. Setup

```bash
git clone https://github.com/drdezarza/LLMagentgovernance.git
cd LLMagentgovernance
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python tests/test_equivalence.py
```

`tests/test_equivalence.py` checks that the governed simulators, with governance hooks switched off, reproduce the
upstream GCGE and feeder simulators exactly. It should print `equivalence OK` and `feeder equivalence OK`.

`make` shortcuts are provided: `make test`, `make verify`, `make analyze`, `make mock`.

## 1. Verify every number in the paper (no API key, seconds)

```bash
python paper/check_numbers.py
# 893 numbers checked; 0 drifted or missing
```

`paper/numbers.json` lists every number checked for the revised manuscript (893 entries, including entries from the
first submission kept for provenance). For each one it records the file, row and column it
comes from in `data/runs/*/_analysis/` or `reports/`, its rounded value, and where the paper uses it. The checker
recomputes each value from the saved file and reports any drift.

## 2. Recompute the analyses from the saved records (no API key)

Each stage's `analyze()` reads only the saved unit records under `data/runs/<STAGE>/` and rewrites `_analysis/`:

```bash
python -m agentgov analyze S5b_C            # one stage
make analyze                                # every stage in config/plan.yaml
git status --short data/runs                # see what changed
```

What to expect:

* Every `findings.md` is reproduced exactly.
* Some CSV cells can differ in the last floating-point digit (for example `…477` vs `…48`), and row order can differ
  in large verdict tables, depending on NumPy/pandas versions. Figures are re-rendered and differ in bytes, not content.
* `analysis_manifest.json` records the time of the analysis and the hash of the analysis code, so it always changes.

Bootstrap intervals use fixed seeds (5000 resamples, seed 42 unless stated), so the intervals are reproducible.

Two analyses also read the call ledger in its SQLite form: the cost/latency table of `A8b_cheap_auditor_live` and
`tools/operating_characteristics.py`. The repository ships the ledger as `data/ledger/calls.csv.gz`; rebuild the
SQLite file once with `python tools/build_ledger_db.py` (or `make ledger-db`). Without it, `analyze A8b_cheap_auditor_live`
still reproduces every verdict but omits the cost table from `findings.md`.

The revision analyses are plain scripts (no API calls):

```bash
python tools/rr_inference_check.py && python tools/rr_frontier.py      # reports/rr/
python tools/rr2_planner_decomposition.py && python tools/rr2_model_evidence.py
python tools/rr2_revision_tables.py                                     # needs data/ledger/calls.csv.gz
make revision-tables                                                    # all of the above
```

They reproduce their CSV and Markdown outputs exactly; figures differ only in embedded metadata.
`tools/rr2_cache_replay.py` is the exception: it replays recorded cells from the original response cache, which is
not distributed (it contains every prompt and response), so its outputs in `reports/rr2/R1_cache_replay.*` are
published as recorded.

## 3. Run the pipeline end to end with a mock model (no API key)

```bash
python -m agentgov run --mock --hours 0.3 --only S7b_C
python -m agentgov run --mock --hours 0.3 --only S5h_live_quarantine
```

Mock mode replaces every model with a deterministic stand-in. It exercises the real simulators, governors, parsers,
validity rules and analyses, and writes to `data/runs_mock/`, never to `data/runs/`. It is the fastest way to check a
change to the code. Mock numbers carry no scientific meaning.

## 4. Re-run experiments live

### Credentials

```bash
cp credentials/nebius.env.example credentials/nebius.env    # then paste your key
# or: export NEBIUS_API_KEY=...   (environment variables take precedence)
python -m agentgov check                                     # key, live catalogue, roster binding
```

`credentials/nebius.env` is git-ignored. Models are referenced by alias. At the start of a session, the live catalogue
is fetched and each alias in `config/settings.yaml → roster` binds to the first candidate model ID that is available.
`python -m agentgov check` shows the binding.

### Running

Completed units are never re-run: the runner skips any unit whose `result.json` says `done`. To re-run a stage from
scratch, move its records aside first:

```bash
mv data/runs/S5h_live_quarantine data/runs/S5h_live_quarantine.published
python -m agentgov plan                                 # status and cost estimates for every stage
python -m agentgov run --only S5h_live_quarantine       # ignores prerequisites for the named stage
python -m agentgov run --hours 6                        # every enabled stage, in plan order, for up to 6 h
```

Useful options: `--hours H` sets the session length (it stops cleanly and resumes the next time); `--workers N` sets
the number of units in parallel (default 4); `--only STAGE [STAGE ...]` runs named stages only.
`python -m agentgov retry STAGE` resets units that ended in error, and `retry STAGE --stale` also resets done units
whose design fingerprint no longer matches the current parameters.

### Budget and safety controls

* **Hard caps** in `config/settings.yaml → budget`: `daily_usd` (default $30) and `monthly_usd` (default $1000). They
  are checked before every call, from token counts and the list prices in the roster. To raise the cap for a single
  day, add it to `config/budget_overrides.yaml`.
* **Slow-model guard**: a model whose median latency exceeds its role limit is skipped for the rest of the session.
* **Disk cache**: every response is cached under `data/cache.nosync/`, so resumed or repeated work is free. The cache
  from the original runs is *not* distributed, so a fresh clone makes fresh calls.

Reference cost for a full re-run of the article's stages at October–November 2026 list prices: about $205 (see
`data/ledger/cost_by_stage.csv`), of which about $90 for the revision follow-ups. The largest stages are S5i ($27),
S5j and S5j2 ($18 each) and S5h ($18). Reasoning-heavy models can cost
several times their non-reasoning equivalents.

### What a live re-run reproduces

A live re-run reproduces the design, prompts, parsers, validity rules and statistics. It does not reproduce identical
model text: hosted models are sampled (temperatures are recorded in the code) and providers update or retire models.
Expect estimates that agree within their intervals, not to the last digit. Endpoint identifiers can also change under
an alias: `deepseek_v4_flash` resolved to `DeepSeek-V4.1-Flash` up to 2 November 2026 and to
`DeepSeek-V4.1-Flash-1017` by 16 November (`reports/rr2/endpoint_call_provenance.json`).

### Cache race in runs before 2026-11-17

Paired conditions are meant to share one sampled answer per identical prompt (common random numbers). Until
2026-11-17 the cache stored answers with `INSERT OR REPLACE`: when parallel workers sent the same prompt at the same
moment, each received its own sample and the cache kept the last one written, not necessarily the one a given unit
used. Recorded results are valid observations of their executions, but paired contrasts carry some extra response
variation and a cache replay of an affected unit can follow a different path. Since that date `Cache.put` keeps the
first stored answer and returns it to every caller (`agentgov/llm.py`); `S5j2_labelonly_extension` is the first stage
run entirely under the fix. The replay audit (`reports/rr2/R1_cache_replay.md`, `cache_replay_counts.csv`) reproduces
162/180 S7b cells, 100/120 S7b_C cells, 329/360 S7c cells and 175/240 S7d cells exactly; the dated amendment in
`reports/prereg/RR_PLAN_v2.md` gives the details. The manuscript reports the resulting execution sensitivity of the
planner-specific feeder contrasts (`reports/rr2/execution_sensitivity.csv`).

Model availability changes over time. If a roster model has left the catalogue, its finished units remain part of the
saved records and analyses, but no new units are dispatched to it. Update the roster's `candidates` to bind the alias
to a successor model, and report the change.

### Scheduled sessions (optional, macOS)

The original study ran as daily time-boxed sessions on a Mac: `scripts/run_session.sh` keeps the machine awake and
writes `logs/`, and `scripts/install_daily.sh 09:00` registers a launchd job (`scripts/uninstall_daily.sh` removes it).
On other systems, use cron or simply run `python -m agentgov run --hours H`.

## 5. Regenerating the upstream simulators (optional)

`agentgov/upstream/gcge_core.py` and `agentgov/upstream/planning_core.py` were extracted automatically from the notebooks
of the predecessor projects. To regenerate and compare them:

```bash
mkdir -p vendor
git clone https://github.com/drdezarza/gcge.git vendor/gcge
git clone https://github.com/drdezarza/LLMstrategicplanning.git vendor/LLMstrategicplanning
python tools/extract_upstream.py vendor
git diff agentgov/upstream
```

## 6. Pre-registration

`reports/prereg/ANALYSIS_PLAN_v1.md` is the analysis plan for the confirmatory stages (`S3b_C`, `S5b_C`, `S7b_C`,
`A7_C_outside_judge`). `reports/prereg/FROZEN.json` records the plan's SHA-256, the SHA-256 of the confirmatory
code and the freeze date (2026-10-23), all set before any confirmatory unit ran. One dated amendment (2026-10-24)
fixed an implementation bug in the J1 outside-judge re-scoring, with no design or rule change; it is logged in the same
file with the amended hashes. The plan and confirmatory code in this repository match those amended hashes:

```bash
sha256sum reports/prereg/ANALYSIS_PLAN_v1.md agentgov/experiments/confirmatory_exps.py
# a59fed5f…e1c515e  reports/prereg/ANALYSIS_PLAN_v1.md
# 6ffd6403…172a69  agentgov/experiments/confirmatory_exps.py
```

`ANALYSIS_PLAN_DRAFT.md` is the draft it replaced. The post-freeze follow-ups `S5h` and `S7c` are
exploratory. Their reading rules are written in the stage classes (`agentgov/experiments/followup_exps.py`) and were
fixed before any of their units ran.

The revision follow-ups have their own frozen reading rules:

* `RR_PLAN_v1.md` + `RR_FROZEN.json` (2026-11-01): A8, S5j, S5i, S5k. The plan and `reviewer_exps.py` match the frozen
  hashes. The two descriptive tools listed in the record (`tools/rr_inference_check.py`, `tools/rr_frontier.py`) were
  extended on 2026-11-06 (additional contrasts, an eligibility filter for revision episodes, a legend change), so
  their current hashes differ from the record; they summarise results and do not implement any stage's reading rules.
* `RR_PLAN_v2.md` + `RR2_FROZEN.json` (2026-11-16): A8b, S7d, S5j2 and the no-API analyses P1 and M1. The stage code,
  the feeder hooks, the equivalence test and both analysis tools match the frozen hashes. One amendment (2026-11-17,
  with a 07:30 addendum) documents the cache race above; its recorded hashes match the current plan, `agentgov/llm.py`
  and `tools/rr2_cache_replay.py`. The plan discloses that S7b cell means and one hourly trace were inspected before
  S7d was designed.

```bash
python - <<'EOF'
import hashlib, json
h = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
d = json.load(open('reports/prereg/RR2_FROZEN.json'))
print(h(d['code_file']) == d['code_sha256'], h(d['plan_file']) == d['amendments'][-1]['addendum']['plan_sha256_after'])
EOF
# True True
```
