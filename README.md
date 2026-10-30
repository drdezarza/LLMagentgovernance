# LLM Agent Governance

**Code, data and reproducibility materials for _Content-Aware Governance of Multi-Agent LLM Systems_**


[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](#installation)
[![Code license: MIT](https://img.shields.io/badge/code-MIT-green.svg)](LICENSE)
[![Data license: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-lightgrey.svg)](DATA_LICENSE.md)
[![Paper numbers verified](https://img.shields.io/badge/paper%20numbers-604%20verified-brightgreen.svg)](paper/)

---

Multi-agent systems built on large language models (LLMs) increasingly send messages that other agents, or people,
act on. A *governor* can check those messages before delivery. This repository asks when that oversight helps, and
what it costs:

* **Does declared compliance survive inspection of the delivered text?** Agents label their own messages; we test
  whether the governance advantage measured from those labels holds when an LLM judge reads what was actually sent.
* **Can an informed sender evade inspection?** Adaptive LLM attackers try to get rule-violating messages selected while
  declaring compliant labels. We compare label trust, content auditing and auditor memory designs.
* **What does oversight cost?** We measure legitimate messages wrongly rejected, attacks admitted and the operational
  loss on a simulated demand-response feeder (an operator asks households to reduce electricity use to relieve network
  stress), separating message auditing, request-intensity caps and fairness reallocation.

Everything runs against hosted open-weight models (Nebius AI Studio / Token Factory) through a resumable,
budget-capped experiment pipeline. **Every LLM-based evaluation is treated as a measurement instrument**: auditors and
judges are calibrated, invalid outputs are counted rather than imputed, and stage-level validity rules are fixed before
results are seen.

## Key results

All tests below used previously unused simulation seeds and an analysis plan frozen on 2026-10-23
([`reports/prereg/`](reports/prereg/)). Intervals are 95 % percentile-bootstrap confidence intervals (5000 resamples).

| Claim | Outcome (sample) | Estimate [95 % CI] | Pre-specified criterion | Met |
|---|---|---|---|:-:|
| C1 | Text-judged ECS gap, governed − unconstrained (18 pairs) | +0.143 [+0.120, +0.166] | lower limit > 0 | ✓ |
| C1 | Text-judged integrity gap (18 pairs) | +0.650 [+0.553, +0.761] | lower limit > 0 | ✓ |
| C2 | Label-trusting governor: attack success given a valid submission (per rotation) | 0.640 / 0.990 / 0.857 | lower limit > 0.30 in every rotation | ✓ |
| C3 | Attack success per round, label trust − content audit (12 pairs) | +0.717 [+0.630, +0.807] | pooled lower limit > 0, positive in all rotations | ✓ |
| C4 | False rejection of judge-clean messages, raw memory − audit (12 pairs) | +0.463 [+0.307, +0.600] | lower limit > 0.10 | ✓ |
| C5a | Feeder objective, message audit − no governance (15 scenarios) | −10.3 [−20.1, −1.1] | upper limit < +25 (non-inferiority) | ✓ |
| C5b | Feeder content integrity, message audit − no governance (15 scenarios) | +0.078 [+0.042, +0.113] | lower limit > 0 | ✓ |

Exploratory follow-ups (run after the freeze, with reading rules fixed before any unit ran):

* **Quarantined memory under adaptive attack (S5h, 72 episodes).** Storing only verified detection labels plus
  closed-vocabulary tactic tags, never attacker-written text, cuts false rejection relative to raw memory by
  0.358 [0.253, 0.460] per round. It adds 0.040 [0.015, 0.065] relative to no memory, with one role assignment above the
  0.10 margin. Raw memory still blocks more attacks.
* **Household non-response (S7c, 360 cells).** With 20 % or 40 % of households never responding, the message-audit
  objective difference stays within the 25-unit margin (−3.6 [−12.8, +5.8] and −12.7 [−22.3, −5.0]).

The results concern simulated households and a simulated feeder; they do not establish effects on human participants
or field readiness. See the paper for the full interpretation and limitations.

## Repository at a glance

```
agentgov/            experiment pipeline (Python package)
  experiments/       one class per study stage; registry in __init__.py
  upstream/          simulators extracted from the predecessor projects (GCGE game, feeder planning)
  gcge_ext.py        governance hooks, auditors, attackers and judges for the cooperation game
  planning_ext.py    governance hooks, message rules and non-response for the feeder
config/              plan.yaml (stages and parameters), settings.yaml (model roster, budget caps)
data/runs/<STAGE>/   every unit's raw records + _analysis/ (tables, figures, findings.md, validity, manifest)
data/ledger/         per-call token/cost/latency ledger (no prompt or response text)
reports/             frozen analysis plan, annotation samples and rubrics, operating-characteristics tables
paper/               numbers.json: every number quoted in the manuscript, mapped to its source file
docs/                documentation (start with docs/EXPERIMENTS.md)
tests/, tools/       equivalence tests against the upstream simulators; analysis utilities
```

## Installation

```bash
git clone https://github.com/drdezarza/LLMagentgovernance.git
cd LLMagentgovernance
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python tests/test_equivalence.py          # simulators reproduce the upstream code exactly
```

Python 3.9 or later. No API key is needed to inspect data, re-run analyses or run the pipeline in mock mode.

## Reproducing the paper

| Level | What it does | Command | API key | Time |
|---|---|---|:-:|---|
| 1 | Check every number quoted in the manuscript against the saved analysis files | `python paper/check_numbers.py` | no | seconds |
| 2 | Recompute any stage's tables, figures and findings from the saved unit records | `python -m agentgov analyze S5b_C` | no | seconds–minutes |
| 3 | Run the whole pipeline end to end with a deterministic mock LLM | `python -m agentgov run --mock --hours 0.3 --only S7b_C` | no | minutes |
| 4 | Re-run experiments live against the same model families | `python -m agentgov run --only S5h_live_quarantine` | yes | hours |

Re-running every analysis (level 2) reproduces all `findings.md` files exactly. Some CSV values differ only in
the last floating-point digit, depending on library versions. Live re-runs (level 4) make new model calls, so they
reproduce the design and the statistics, not identical text. See [`docs/REPRODUCING.md`](docs/REPRODUCING.md).

## Documentation

| Document | Contents |
|---|---|
| [`docs/EXPERIMENTS.md`](docs/EXPERIMENTS.md) | Every study stage: question, design, sample, models, cost and where it appears in the paper |
| [`docs/REPRODUCING.md`](docs/REPRODUCING.md) | Step-by-step reproduction, live runs, budget controls and expected deviations |
| [`docs/DATA.md`](docs/DATA.md) | Layout and schema of every data file, provenance fingerprints and validity records |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | How the pipeline works, the governors, the instruments, the model roster and how to add a stage |

## Relation to earlier work

This study builds on two earlier projects by the same group. It reuses their simulators unchanged, verified by
`tests/test_equivalence.py`:

* [**GCGE**](https://github.com/drdezarza/gcge): constitutional governance in a networked LLM cooperation game.
* [**LLMstrategicplanning**](https://github.com/drdezarza/LLMstrategicplanning): LLM planning architectures for
  microgrid dispatch and prosumer response.

The new contribution is the evaluation of the communication-governance layer itself: delivered-text measurement,
adaptive attackers, matched memory replay, a decomposition of feeder interventions, and prospectively specified tests.


## License

Code is released under the [MIT License](LICENSE). Data, analysis outputs and annotation materials (`data/`, `reports/`,
`paper/numbers.json`) are released under [CC BY 4.0](DATA_LICENSE.md). The simulators in `agentgov/upstream/` derive from
the predecessor repositories listed above.

## Responsible use

The attacker prompts are experimental LLM senders that try to have rule-violating *persuasive messages* selected in a
simulated game. They contain no exploit code and do not attack grid hardware or real systems. The material is
released to support the evaluation of oversight mechanisms.
