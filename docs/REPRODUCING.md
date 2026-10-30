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
# 604 numbers checked; 0 drifted or missing
```

`paper/numbers.json` lists every number quoted in the manuscript. For each one it records the file, row and column it
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

Reference cost for a full re-run of the article's stages at October 2026 list prices: about $115 (see
`data/ledger/cost_by_stage.csv`). The two largest stages are S5h ($18) and S5d ($15). Reasoning-heavy models can cost
several times their non-reasoning equivalents.

### What a live re-run reproduces

A live re-run reproduces the design, prompts, parsers, validity rules and statistics. It does not reproduce identical
model text: hosted models are sampled (temperatures are recorded in the code) and providers update or retire models.
Expect estimates that agree within their intervals, not to the last digit.

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
``` `ANALYSIS_PLAN_DRAFT.md` is the draft it replaced. The post-freeze follow-ups `S5h` and `S7c` are
exploratory. Their reading rules are written in the stage classes (`agentgov/experiments/followup_exps.py`) and were
fixed before any of their units ran.
