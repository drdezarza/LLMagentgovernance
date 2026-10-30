# Experiment catalogue

Every study is a *stage* with a stable identifier. The identifiers link the manuscript to its records:
`data/runs/<STAGE>/` holds the raw unit records and `data/runs/<STAGE>/_analysis/` the tables, figures and
`findings.md` produced by that stage's `analyze()` method. Stage classes live in `agentgov/experiments/` and are
registered in `agentgov/experiments/__init__.py`. Parameters are in `config/plan.yaml`.

Costs are taken from the call ledger (`data/ledger/cost_by_stage.csv`) and are list-price USD for the calls actually
made. Calls answered from the disk cache cost nothing. The whole programme, development stages included, cost
**$152** in inference.

## How to read the stage identifiers

| Prefix | Meaning |
|---|---|
| `S…` | Simulation studies: `S3*`/`S5*` use the networked cooperation game; `S4*`/`S7*` use the radial demand-response feeder |
| `A…` | Instrument studies: calibration and validation of auditors, judges and attacker interfaces |
| `H1` | Annotation reference sample (AI-assisted, see below) |
| `…_C` | Confirmatory stage: fresh seeds, analysis plan frozen before any unit ran (`reports/prereg/`) |

**Role rotations.** Adversarial and feeder studies rotate three model families through the roles in a Latin square,
so that no family judges its own outputs:

| Rotation | Game: attacker / auditor / judge | Feeder: planner backbone / auditor / judge |
|---|---|---|
| R1 | DeepSeek-V4-Pro / MiniMax-M3 / GLM-5.3 | DeepSeek-V4-Pro / MiniMax-M3 / GLM-5.3 |
| R2 | MiniMax-M3 / GLM-5.3 / DeepSeek-V4-Pro | MiniMax-M3 / GLM-5.3 / DeepSeek-V4-Pro |
| R3 | GLM-5.3 / DeepSeek-V4-Pro / MiniMax-M3 | GLM-5.3 / DeepSeek-V4-Pro / MiniMax-M3 |

In the game, the honest message compiler and the agent population use Qwen3-235B-A22B, a family that never appears
in a rotated role.

## Stages reported in the article

Section numbers refer to the manuscript (Methods = §4, Results = §5).

### Confirmatory tests (frozen plan, fresh seeds)

| Stage | Hypotheses | Design | Sample | Cost | Paper |
|---|---|---|---|---|---|
| `S3b_C` | C1 | Governed vs unconstrained game; integrity judged from the delivered text (judge Kimi-K3, fixed); backbones DeepSeek-V4.1-Flash, Qwen3.8-27B, MiniMax-M3; seeds 101–106 | 36 runs, 18 pairs | $6.38 | §4.9, §5.1 |
| `S5b_C` | C2–C4 | Label trust vs content audit vs raw-memory audit against an informed adaptive attacker; three rotations; seeds 101–104 | 36 episodes | $6.97 | §4.9, §5.1 |
| `S7b_C` | C5a, C5b | Feeder: no governance (G0) vs message audit (Gmsg) × 4 planners × 3 rotations × scenarios 11–15; non-inferiority margin 25 objective units | 120 cells, 15 scenarios | $5.66 | §4.9, §5.1 |
| `A7_C_outside_judge` | J1 | Every confirmatory text re-judged by an outside judge (Qwen3-235B, frozen rubric); sensitivity only, never decides a verdict | 192 units | $0.52 | §5.1 |

### Exploratory studies

| Stage | Question | Design | Sample | Cost | Paper |
|---|---|---|---|---|---|
| `S3b_text_integrity` | Does the governance advantage survive delivered-text measurement? | 3 backbones × governed/unconstrained × seeds 3–8 | 36 runs | $6.81 | §4.1, §5.2 |
| `A0_attacker_interface` | Which output budget gives each attacker family a valid, timely interface? | 5 families × 4 token budgets (900–12000) on fixed states with the real attacker prompt | 20 settings | $1.57 | §4.2, §5.3 |
| `S5b_role_rotation` | Label trust vs auditing vs memory/tightening variants under rotated roles | 3 rotations × 5 governors (adaptive attacker) + label governor (static attacker) × seeds 1–3 | 54 episodes | $15.25 | §4.2, §5.3 |
| `A3_fixed_bank` | How do auditors and judges score one fixed candidate bank? | Fixed bank × every evaluator and prompt; outside judges Kimi-K3 and Muse Spark | 44 units, 1626 unique texts | $9.59 | §4.3, §5.4 |
| `S5d_memory_variants` | Which part of auditor memory causes false rejection? | Plain audit / neutral length-matched context / raw memory / label-only memory; fixed cap 0.80; seeds 4–9 | 72 episodes | $15.35 | §4.4, §5.5 |
| `S5e_memory_replay` | Same items, same histories: does the context alone change the verdict? | Matched replay of the S5d raw-memory episodes under five auditor contexts | 18 histories, 1284 items | $3.67 | §4.5, §5.6 |
| `S5f_spotlight_replay` | Does marking remembered text as untrusted (spotlighting) help? | Delimiting and datamarking variants of raw memory on the S5e items | 18 histories | $2.50 | §4.5, §5.6 |
| `S5g_quarantine_replay` | Quarantined memory: verified labels + closed-vocabulary tactic tags | Separate extractor (Kimi-K3) may only emit ≤ 3 tags from an 8-tag vocabulary; attacker text never reaches the auditor | 18 histories | $3.66 | §4.5, §5.6 |
| `S5h_live_quarantine` | Does the quarantine result hold when the attacker can react? *(post-freeze follow-up)* | No memory vs live tag memory vs raw memory; adaptive attacker; 3 rotations × seeds 201–208 | 72 episodes, 24 paired comparisons | $18.44 | §4.5, §5.6 |
| `S7b_mechanism_ablation` | Which feeder intervention causes each cost and benefit? | 4 planners × 5 mechanisms (G0, Gmsg, Gcap, Ggini, G1r) × 3 rotations × 3 scenarios | 180 cells | $7.03 | §4.7, §5.7 |
| `S7c_nonresponse` | Does the message-audit result hold when households stop responding? *(post-freeze follow-up)* | G0 vs Gmsg × 4 planners × the 15 S7b_C scenarios × 0/20/40 % persistent non-response (nested random subsets) | 360 cells | $5.54 | §4.7, §5.7 |
| `A1_audit_calibration` | Development calibration of auditor/judge models on a known-label bank | 9 models × 30 constructed messages (incl. disguised violations) | 9 units | $0.47 | §4.8, §5.8 |
| `A2_judge_validation` | Strict vs rubric judge prompts on real messages | 6 judge configurations × 60 real messages with AI-assisted labels | 6 units | $1.00 | §4.8, §5.8 |
| `H1_independent_labels` | Annotation reference sample | 78 stratified items labelled by two annotators and adjudicated, **both annotators AI-assisted** | 1 export | – | §4.8, §5.8 |
| `A4_h1_judges` | Candidate judges against the H1 reference | 6 judge families × strict/rubric prompts on the H1 items | 12 cells | $1.04 | §4.6, §5.8 |
| `A5_rule_by_rule` | Joint audit vs three separate rule checks | Same auditor models, fixed bank + 52 H1 game items | 15 units | $3.40 | §4.6, §5.9 |
| `A6_llama_guard` | A specialist safety classifier as an auditor baseline | Llama Guard 3 (8B, local via Ollama), default vs custom taxonomy | 10 units | local | §4.6, §5.9 |

Operating-characteristics tables (attacks admitted, legitimate messages lost and inference cost per 100 messages) are
in `reports/operating_characteristics*.csv`. They are produced by `tools/operating_characteristics.py` (§5.10).

> **Note on `H1_independent_labels`.** The stage name and its in-code title date from the original protocol, which
> asked for unassisted annotation. The authors later confirmed that both annotators used MiniMax-M3 assistance
> (`reports/labeling_v2/PROVENANCE_CORRECTION.json`). The paper therefore treats H1 as an adjudicated **AI-assisted
> reference**, not an independent human ground truth. The original files are kept unchanged.

## Development stages (not reported in the article)

These earlier stages built and validated the pipeline and explored designs that were later superseded. Their records
are kept for provenance; they are not part of the article's evidence. `paper/numbers.json` keeps four
S2/S3 values for provenance only; none is printed in the final text.

| Stage | Purpose | Sample | Cost |
|---|---|---|---|
| `S0_connectivity` | Which roster models are live; interface settings (token budgets, reasoning switches) per model | 15 models | $0.16 |
| `S1_interface_probe` | Bounded-interface behaviour of each model family in both simulators | 15 models | $1.01 |
| `S2_gcge_replication` | Replication of the published GCGE result through this pipeline | 15 runs | $0.55 |
| `S3_gcge_cross_model` | GCGE governance advantage across 12 model families (label-based integrity) | 72 runs | $17.42 |
| `S4_planning_backbone` | Planning-architecture regret with new planner backbones | 20 units | $4.39 |
| `S4b_scenario_bank` | Does the best feasible planning strategy change across scenarios? (gate for a joint controller) | 51 units | $5.20 |
| `S5_adaptive_attacker`, `S5v2_informed_attacker` | Pilots of the adversarial comparison | 18 + 6 episodes | $2.86 |
| `S6_risk_routing`, `S6v2_impact_routing` | Pilots of cheap/strong model routing (separate research line, parked) | 15 + 10 units | $1.18 |
| `S7_joint_factorial` | First planning × governance factorial on the feeder (superseded by S7b) | 150 cells | $4.56 |
| `S8_joint_controller` | Joint controller: not built (gated on S4b) | – | – |

## Validity rules and outcome taxonomy

Each stage declares instrument-validity rules **before** its units run (class attribute `validity_rules`; recorded in
`_analysis/validity.json` with a `rules_version`). Only eligible units enter the main tables; exclusions are counted and
listed. Examples:

* Adversarial episodes (S5b, S5d, S5h, S5b_C): the attacker submitted a parseable candidate in ≥ 80 % of rounds,
  judge-unresolved verdicts ≤ 10 % and auditor-invalid outputs ≤ 10 % of evaluations.
* Feeder cells (S7b, S7b_C, S7c): judge resolved ≥ 90 % of messages; auditor valid ≥ 90 % of audits.
* Evaluator cells (A3, S5e–S5g, A4–A6): ≥ 90 % valid labels per evaluator × prompt (or context) cell.

Outcomes are kept separate:

* **False rejection** (auditor misclassification): the auditor flags a message that the research judge rates clean.
  This is judge-relative error, not human-established error.
* **Restriction cost**: a legitimate message blocked by a tightened intensity cap rather than by a content verdict.
* **Attack success**: a rule-violating attacker message is selected and delivered. It is reported both per scheduled
  round and conditional on a valid submission, together with the attacker's valid-submission rate.
* **ECS** (the composite governance score of the predecessor GCGE work) is secondary; its components are always
  reported alongside it.

An invalid evaluator output is never converted into a verdict. Governance fails closed (an unverifiable audit
rejects the message); measurement reports unresolved judgements as bounds.
