"""RR_PLAN_v3 N4 (no API calls): end-to-end episode runtime from the saved call ledger (Reviewer 3, point 9).

Descriptive, from records collected during the experiments (not a controlled workload benchmark; the controlled
benchmark is A9_runtime_benchmark). The ledger records every model call with its completion time (ts), latency,
status, role and whether it was a cache hit. Episodes ran sequentially inside a unit, with four units in parallel.

Per unit (episode or feeder cell) of the live studies:
  * calls (total, uncached, cache hits), failed attempts (any non-ok status: network error, HTTP 5xx/529, empty
    answer), and failed attempts per 100 calls;
  * observed wall clock = start of the first to end of the last uncached call, summed over sessions (a resumed unit is
    not timed across the gap). The disk cache served repeated prompts (15-88 % of calls, by study), so an
    uncached-equivalent wall clock is estimated by adding, for each cache hit, the median uncached latency of the same
    study x role x model (calls inside a unit are sequential, so latencies add);
  * summed call latency by role, and the governance share = auditor-role latency / all latency (in the feeder
    studies the message rewriter runs on the planner model and is counted under planner, so the share is a lower
    bound there); the research judge and the simulated recipients are reported separately because a deployment
    would not run them.
From the cell records: message-governance actions in the feeder (audits, rewrites, template fallbacks, invalid
audits per message) and fail-closed audit decisions in the game (audit_invalid_share).

Outputs: reports/rr3/N4_runtime_units.csv, N4_runtime_summary.csv, N4_fallbacks.csv, N4_runtime_logs.md
Usage:   python tools/rr3_runtime_logs.py [AGENTGOV_ROOT] [LEDGER_CSV_GZ]
"""
from __future__ import annotations

import pathlib
import sys

import numpy as np
import pandas as pd

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parents[1])
LEDGER = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "data" / "ledger" / "calls.csv.gz"
RUNS, OUT = ROOT / "data" / "runs", ROOT / "reports" / "rr3"
GAME = ["S5b_C", "S5h_live_quarantine", "S5i_role_factorial", "S5j_live_labelonly"]
FEEDER = ["S7b_C", "S7b_mechanism_ablation", "S7c_nonresponse"]


def governor_of(study, unit):
    parts = unit.split("-")
    if study in GAME:
        return parts[2] if len(parts) > 3 else "?"
    return parts[3] if len(parts) > 3 else "?"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    d = pd.read_csv(LEDGER, usecols=["ts", "session", "experiment", "unit", "role", "model", "prompt_tokens",
                                      "completion_tokens", "latency_s", "cached", "mock", "status"])
    d = d[d.experiment.isin(GAME + FEEDER) & (d["mock"] == 0)].copy()
    d["ok"] = d.status.eq("ok")
    d["start"] = d.ts - d.latency_s.fillna(0)
    # imputed latency for cache hits: median uncached latency of the same study x role x model (calls within a unit
    # run sequentially: summed call latency / wall clock is 0.93-0.98 in every study)
    # (falls back to the median over all live studies for the role x model when a study has no uncached call of it)
    med = d[(d.cached == 0) & d.ok].groupby(["experiment", "role", "model"]).latency_s.median()
    med2 = d[(d.cached == 0) & d.ok].groupby(["role", "model"]).latency_s.median()
    d["lat_est"] = np.where(d.cached == 1, [med.get((e, r, m), med2.get((r, m), np.nan))
                                            for e, r, m in zip(d.experiment, d.role, d.model)], d.latency_s)
    roles = sorted(d.role.unique())
    rows = []
    for (exp, unit), g in d.groupby(["experiment", "unit"]):
        live = g[(g.cached == 0)]
        okc, hit = g[g.ok & (g.cached == 0)], g[g.ok & (g.cached == 1)]
        wall = sum(float(s.ts.max() - s.start.min()) for _, s in live.groupby("session"))
        est = g[g.ok].groupby("role").lat_est.sum()
        n_ok = int(g.ok.sum())
        r = {"study": exp, "unit": unit, "governor": governor_of(exp, unit), "calls": n_ok,
             "cache_hits": int(hit.shape[0]), "uncached_calls": int(okc.shape[0]),
             "failed_attempts": int((~g.ok).sum()), "cached_share": float(hit.shape[0] / max(1, n_ok)),
             "sessions": int(live.session.nunique()), "wall_observed_s": wall,
             "imputed_cache_hit_latency_s": float(hit.lat_est.sum()),
             "prompt_tokens": int(g[g.ok].prompt_tokens.sum()), "completion_tokens": int(g[g.ok].completion_tokens.sum())}
        r["wall_uncached_est_s"] = wall + r["imputed_cache_hit_latency_s"]
        tot = float(est.sum())
        for role in roles:
            r[f"lat_{role}_s"] = float(est.get(role, 0.0))
            r[f"calls_{role}"] = int((g[g.ok].role == role).sum())
        r["latency_est_total_s"] = tot
        r["failed_per_100_calls"] = 100 * r["failed_attempts"] / max(1, n_ok + r["failed_attempts"])
        r["governance_share"] = r["lat_auditor_s"] / tot if tot else np.nan
        r["judge_share"] = r["lat_judge_s"] / tot if tot else np.nan
        r["governance_share_excl_judge"] = r["lat_auditor_s"] / (tot - r["lat_judge_s"]) if tot - r["lat_judge_s"] > 0 else np.nan
        rows.append(r)
    U = pd.DataFrame(rows)
    steps = {}
    for exp in GAME:
        f = RUNS / exp / "_analysis" / ("episodes_all.csv" if (RUNS / exp / "_analysis" / "episodes_all.csv").exists() else "summary_all.csv")
        if f.exists():
            e = pd.read_csv(f)
            steps.update({(exp, i): r for i, r in zip(e["id"], e["rounds"])} if "rounds" in e else {})
    U["steps"] = [steps.get((s, u), 24 if s in FEEDER else np.nan) for s, u in zip(U.study, U.unit)]
    U["wall_est_per_step_s"] = U.wall_uncached_est_s / U.steps
    U["governance_s_per_step"] = U.lat_auditor_s / U.steps
    U.to_csv(OUT / "N4_runtime_units.csv", index=False)

    def q(x, p):
        x = x.dropna()
        return float(np.percentile(x, p)) if len(x) else np.nan
    S = []
    for (exp, gov), g in U.groupby(["study", "governor"]):
        S.append({"study": exp, "governor": gov, "units": len(g), "cached_share_mean": g.cached_share.mean(),
                  "wall_obs_min_p50": q(g.wall_observed_s, 50) / 60,
                  "wall_est_min_p50": q(g.wall_uncached_est_s, 50) / 60, "wall_est_min_p90": q(g.wall_uncached_est_s, 90) / 60,
                  "wall_est_min_max": g.wall_uncached_est_s.max() / 60,
                  "wall_est_s_per_step_p50": q(g.wall_est_per_step_s, 50), "governance_s_per_step_p50": q(g.governance_s_per_step, 50),
                  "calls_per_unit_mean": g.calls.mean(), "auditor_calls_per_unit_mean": g.calls_auditor.mean(),
                  "failed_per_100_calls": 100 * g.failed_attempts.sum() / max(1, g.calls.sum() + g.failed_attempts.sum()),
                  "governance_share": g.lat_auditor_s.sum() / g.latency_est_total_s.sum(),
                  "governance_share_excl_judge": g.lat_auditor_s.sum() / (g.latency_est_total_s.sum() - g.lat_judge_s.sum()),
                  "judge_share": g.lat_judge_s.sum() / g.latency_est_total_s.sum()})
    S = pd.DataFrame(S)
    S.to_csv(OUT / "N4_runtime_summary.csv", index=False)

    # failure statuses overall
    st = d[~d.ok].groupby(["experiment", "status"]).size().unstack(fill_value=0)

    # fallbacks from cell records
    F = []
    for exp in FEEDER:
        c = pd.read_csv(RUNS / exp / "_analysis" / "cells.csv")
        c = c[c.gov.isin(["Gmsg", "G1r"])]
        if exp == "S7c_nonresponse":
            c = c[pd.to_numeric(c.nonresponse, errors="coerce").fillna(0) == 0] if "nonresponse" in c else c
        for gov, g in c.groupby("gov"):
            a = g.gov_msg_audits.sum()
            F.append({"study": exp, "governor": gov, "cells": len(g), "messages_audited": int(a),
                      "rewrite_rate": g.gov_msg_rewrites.sum() / a if a else np.nan,
                      "template_fallback_rate": g.gov_msg_templates.sum() / a if a else np.nan,
                      "invalid_audit_rate": g.gov_msg_audit_invalid.sum() / a if (a and "gov_msg_audit_invalid" in g) else np.nan,
                      "cells_with_template": int((g.gov_msg_templates > 0).sum())})
    for exp in GAME:
        f = RUNS / exp / "_analysis" / ("episodes_all.csv" if (RUNS / exp / "_analysis" / "episodes_all.csv").exists() else "summary_all.csv")
        if not f.exists():
            continue
        e = pd.read_csv(f)
        e = e[e.governor.astype(str).str.startswith("audit")]
        for gov, g in e.groupby("governor"):
            F.append({"study": exp, "governor": gov, "cells": len(g),
                      "invalid_audit_rate": float(g.audit_invalid_share.mean()) if "audit_invalid_share" in g else np.nan,
                      "max_invalid_audit_rate_episode": float(g.audit_invalid_share.max()) if "audit_invalid_share" in g else np.nan})
    F = pd.DataFrame(F)
    F.to_csv(OUT / "N4_fallbacks.csv", index=False)

    def fmt(v, p=2):
        return "" if v != v else f"{v:.{p}f}"
    lines = ["# N4: end-to-end episode runtime from the saved call ledger (RR_PLAN_v3; no API calls)", "",
             f"Ledger: {len(d)} live-study call records. Calls inside a unit run sequentially (summed latency / wall clock "
             f"{(U.latency_est_total_s - U.imputed_cache_hit_latency_s).sum() / U.wall_observed_s.sum():.2f}); four units ran in parallel on a shared provider. "
             "Observed wall clock spans the first to the last uncached call (summed over sessions). Because the disk cache "
             "served repeated prompts, the uncached-equivalent wall clock adds, for every cache hit, the median uncached "
             "latency of the same study, role and model (an estimate). Descriptive, not a controlled benchmark (see A9).", "",
             "| study | governor | units | cache hits | observed wall p50 (min) | est. uncached wall p50 / p90 (min) | est. s per step | governance s per step | calls/unit | auditor calls/unit | failed attempts /100 | governance share | excl. judge | judge share |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in S.itertuples():
        lines.append(f"| {r.study} | {r.governor} | {r.units} | {fmt(r.cached_share_mean)} | {fmt(r.wall_obs_min_p50, 1)} | "
                     f"{fmt(r.wall_est_min_p50, 1)} / {fmt(r.wall_est_min_p90, 1)} | {fmt(r.wall_est_s_per_step_p50, 1)} | "
                     f"{fmt(r.governance_s_per_step_p50, 2)} | {fmt(r.calls_per_unit_mean, 0)} | {fmt(r.auditor_calls_per_unit_mean, 0)} | "
                     f"{fmt(r.failed_per_100_calls)} | {fmt(r.governance_share)} | {fmt(r.governance_share_excl_judge)} | {fmt(r.judge_share)} |")
    lines += ["", "Steps: game rounds (S5) or feeder hours (S7, 24). Governance share = auditor-role latency / all "
              "call latency, pooled over the units of the row (estimated incl. cache hits); 'excl. judge' removes the research judge, which a deployment would not run. "
              "Feeder rewrites run on the planner model and count under planner, so the feeder governance share is a lower bound.", "",
              "**Failed attempts by status** (all retried by the client; counts)", "",
              "| study | " + " | ".join(st.columns) + " |", "|---" * (len(st.columns) + 1) + "|"]
    lines += [f"| {i} | " + " | ".join(str(int(v)) for v in r.values) + " |" for i, r in st.iterrows()]
    lines += ["", "**Governance fallbacks** (feeder: per audited message; game: fail-closed audit decisions per episode, mean)", "",
              "| study | governor | units | messages audited | rewrite | template fallback | invalid audit |", "|---|---|---|---|---|---|---|"]
    for r in F.itertuples():
        lines.append(f"| {r.study} | {r.governor} | {r.cells} | {'' if r.messages_audited != r.messages_audited else int(r.messages_audited)} | "
                     f"{fmt(getattr(r, 'rewrite_rate'), 3)} | {fmt(getattr(r, 'template_fallback_rate'), 3)} | {fmt(r.invalid_audit_rate, 3)} |")
    (OUT / "N4_runtime_logs.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
