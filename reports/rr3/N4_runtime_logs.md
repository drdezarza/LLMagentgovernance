# N4: end-to-end episode runtime from the saved call ledger (RR_PLAN_v3; no API calls)

Ledger: 253046 live-study call records. Calls inside a unit run sequentially (summed latency / wall clock 0.85); four units ran in parallel on a shared provider. Observed wall clock spans the first to the last uncached call (summed over sessions). Because the disk cache served repeated prompts, the uncached-equivalent wall clock adds, for every cache hit, the median uncached latency of the same study, role and model (an estimate). Descriptive, not a controlled benchmark (see A9).

| study | governor | units | cache hits | observed wall p50 (min) | est. uncached wall p50 / p90 (min) | est. s per step | governance s per step | calls/unit | auditor calls/unit | failed attempts /100 | governance share | excl. judge | judge share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S5b_C | audit | 12 | 0.27 | 16.0 | 18.7 / 26.7 | 44.9 | 2.19 | 583 | 81 | 0.33 | 0.08 | 0.11 | 0.25 |
| S5b_C | audit_memory | 12 | 0.22 | 14.0 | 17.8 / 21.0 | 42.6 | 2.15 | 574 | 75 | 0.22 | 0.08 | 0.10 | 0.14 |
| S5b_C | label | 12 | 0.18 | 14.0 | 15.6 / 31.5 | 37.3 | 0.00 | 604 | 0 | 0.34 | 0.00 | 0.00 | 0.23 |
| S5h_live_quarantine | audit | 24 | 0.17 | 13.2 | 15.6 / 22.6 | 37.4 | 2.64 | 551 | 76 | 0.40 | 0.10 | 0.11 | 0.11 |
| S5h_live_quarantine | audit_memory | 24 | 0.19 | 13.3 | 16.5 / 24.3 | 39.5 | 2.47 | 566 | 75 | 0.45 | 0.09 | 0.10 | 0.10 |
| S5h_live_quarantine | audit_quarantine | 24 | 0.17 | 14.0 | 17.4 / 26.5 | 41.7 | 2.48 | 588 | 75 | 0.49 | 0.09 | 0.10 | 0.09 |
| S5i_role_factorial | audit | 36 | 0.31 | 19.1 | 23.0 / 43.4 | 55.2 | 4.09 | 646 | 89 | 0.94 | 0.11 | 0.12 | 0.12 |
| S5i_role_factorial | audit_memory | 36 | 0.27 | 19.7 | 22.5 / 43.9 | 53.9 | 4.56 | 650 | 87 | 1.05 | 0.10 | 0.12 | 0.13 |
| S5j_live_labelonly | audit | 24 | 0.20 | 12.9 | 15.7 / 23.5 | 37.7 | 2.97 | 583 | 80 | 0.27 | 0.10 | 0.11 | 0.10 |
| S5j_live_labelonly | audit_memory_struct | 24 | 0.19 | 13.0 | 15.2 / 22.7 | 36.4 | 2.90 | 578 | 79 | 0.25 | 0.10 | 0.11 | 0.10 |
| S5j_live_labelonly | audit_quarantine | 24 | 0.23 | 14.0 | 18.5 / 23.7 | 44.3 | 3.53 | 626 | 80 | 0.31 | 0.09 | 0.10 | 0.09 |
| S7b_C | G0 | 60 | 0.34 | 2.3 | 3.2 / 5.7 | 8.1 | 0.00 | 149 | 0 | 0.19 | 0.00 | 0.00 | 0.17 |
| S7b_C | Gmsg | 60 | 0.71 | 1.3 | 3.4 / 6.0 | 8.6 | 1.08 | 178 | 28 | 0.08 | 0.17 | 0.20 | 0.15 |
| S7b_mechanism_ablation | G0 | 36 | 0.29 | 2.3 | 3.4 / 5.5 | 8.5 | 0.00 | 143 | 0 | 0.17 | 0.00 | 0.00 | 0.18 |
| S7b_mechanism_ablation | G1r | 36 | 0.73 | 1.0 | 3.7 / 6.6 | 9.3 | 1.04 | 190 | 29 | 0.09 | 0.14 | 0.16 | 0.14 |
| S7b_mechanism_ablation | Gcap | 36 | 0.70 | 0.8 | 3.1 / 5.6 | 7.7 | 0.00 | 143 | 0 | 0.06 | 0.00 | 0.00 | 0.18 |
| S7b_mechanism_ablation | Ggini | 36 | 0.59 | 1.5 | 3.3 / 6.2 | 8.3 | 0.00 | 157 | 0 | 0.16 | 0.00 | 0.00 | 0.16 |
| S7b_mechanism_ablation | Gmsg | 36 | 0.69 | 1.5 | 3.6 / 6.2 | 9.0 | 1.25 | 176 | 29 | 0.06 | 0.16 | 0.19 | 0.15 |
| S7c_nonresponse | G0 | 180 | 0.71 | 0.6 | 3.4 / 5.4 | 8.6 | 0.00 | 128 | 0 | 0.09 | 0.00 | 0.00 | 0.30 |
| S7c_nonresponse | Gmsg | 180 | 0.90 | 0.1 | 3.8 / 6.0 | 9.5 | 0.89 | 160 | 28 | 0.06 | 0.20 | 0.26 | 0.23 |

Steps: game rounds (S5) or feeder hours (S7, 24). Governance share = auditor-role latency / all call latency, pooled over the units of the row (estimated incl. cache hits); 'excl. judge' removes the research judge, which a deployment would not run. Feeder rewrites run on the planner model and count under planner, so the feeder governance share is a lower bound.

**Failed attempts by status** (all retried by the client; counts)

| study | empty | http_402 | http_529 | net_error |
|---|---|---|---|---|
| S5b_C | 5 | 0 | 0 | 58 |
| S5h_live_quarantine | 15 | 0 | 16 | 152 |
| S5i_role_factorial | 70 | 8 | 8 | 383 |
| S5j_live_labelonly | 7 | 0 | 12 | 101 |
| S7b_C | 3 | 0 | 0 | 23 |
| S7b_mechanism_ablation | 3 | 0 | 0 | 28 |
| S7c_nonresponse | 0 | 0 | 0 | 37 |

**Governance fallbacks** (feeder: per audited message; game: fail-closed audit decisions per episode, mean)

| study | governor | units | messages audited | rewrite | template fallback | invalid audit |
|---|---|---|---|---|---|---|
| S7b_C | Gmsg | 60 | 1663 | 0.123 | 0.011 | 0.001 |
| S7b_mechanism_ablation | G1r | 36 | 1011 | 0.133 | 0.013 |  |
| S7b_mechanism_ablation | Gmsg | 36 | 1010 | 0.134 | 0.011 |  |
| S7c_nonresponse | Gmsg | 60 | 1662 | 0.122 | 0.011 | 0.001 |
| S5b_C | audit | 12 |  |  |  | 0.001 |
| S5b_C | audit_memory | 12 |  |  |  | 0.000 |
| S5h_live_quarantine | audit | 24 |  |  |  | 0.000 |
| S5h_live_quarantine | audit_memory | 24 |  |  |  | 0.001 |
| S5h_live_quarantine | audit_quarantine | 24 |  |  |  | 0.000 |
| S5i_role_factorial | audit | 36 |  |  |  | 0.000 |
| S5i_role_factorial | audit_memory | 36 |  |  |  | 0.000 |
| S5j_live_labelonly | audit | 24 |  |  |  | 0.001 |
| S5j_live_labelonly | audit_memory_struct | 24 |  |  |  | 0.000 |
| S5j_live_labelonly | audit_quarantine | 24 |  |  |  | 0.000 |
