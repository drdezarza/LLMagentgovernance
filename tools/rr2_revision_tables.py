"""Derived tables for the revised manuscript (second revision round; no API calls).

Regenerates, from records in this repository, the small tables the revised manuscript quotes in addition to the stage
analyses and the other rr2 tools:

  reports/rr2/execution_sensitivity.csv   Audit - Baseline feeder objective by plan: frozen confirmatory cells (S7b_C)
                                          and their re-execution at 0 % non-response (S7c); scenario bootstrap
  reports/rr2/cache_replay_counts.csv     per-study summary of reports/rr2/R1_cache_replay.csv
  reports/rr2/message_interventions.csv   message rewrites / template fallbacks per episode under Audit (S7b_C),
                                          natural declarations vs the three structured planners
  reports/rr2/auditor_cost_calls_plain.csv  per-call auditor records (ledger) behind the cost comparison
  reports/rr2/auditor_costs_plain.csv     USD per 1000 completed auditor calls (cache hits at token-based list
                                          price) and median latency of uncached calls: lower-cost candidates (A8b)
                                          vs the plain-audit reference auditors (S5i episodes without memory)
  reports/rr2/endpoint_call_provenance.json  which endpoint identifiers each stage actually called

Bootstrap: 5000 percentile resamples, seed 42, over the 15 scenarios.
Usage:  python tools/rr2_revision_tables.py [REPO_ROOT]        (needs numpy and pandas)
"""
from __future__ import annotations

import json
import pathlib
import sys

import numpy as np
import pandas as pd

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parents[1])
RUNS, OUT = ROOT / "data" / "runs", ROOT / "reports" / "rr2"


def _eligible(d):
    return d[d.eligible.astype(str).str.lower().isin(["true", "1"])]


def _ci(x):
    x = np.asarray(x, float)
    b = np.random.default_rng(42).choice(x, size=(5000, len(x)), replace=True).mean(axis=1)
    return float(x.mean()), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))


def execution_sensitivity():
    rows = []
    for stage in ["S7b_C", "S7c_nonresponse"]:
        d = _eligible(pd.read_csv(RUNS / stage / "_analysis" / "cells.csv"))
        if stage == "S7c_nonresponse":
            d = d[d.nonresponse.eq(0)]
        for plan, z in [("all", d)] + list(d.groupby("plan")):
            q = z.pivot_table(index=["rot", "seed", "plan"], columns="gov", values="objective")
            x = (q.Gmsg - q.G0).groupby(["rot", "seed"]).mean()      # plans averaged within scenario
            m, lo, hi = _ci(x)
            rows.append(dict(study=stage, plan=plan, n_pairs=len(x), delta=m, lo=lo, hi=hi))
    pd.DataFrame(rows).to_csv(OUT / "execution_sensitivity.csv", index=False)


def cache_replay_counts():
    r = pd.read_csv(OUT / "R1_cache_replay.csv")
    rows = [dict(study=s, cells=len(d), replayed=int(d.replayed.notna().sum()),
                 exact=int(d.exact.astype(str).str.lower().eq("true").sum()), max_abs_dev=float(d.abs_dev.max()))
            for s, d in r.groupby("study")]
    pd.DataFrame(rows).to_csv(OUT / "cache_replay_counts.csv", index=False)


def message_interventions():
    d = _eligible(pd.read_csv(RUNS / "S7b_C" / "_analysis" / "cells.csv"))
    d = d[d.gov.eq("Gmsg")]
    rows = []
    for name, z in [("natural", d[d.plan.eq("natural")]), ("structured", d[~d.plan.eq("natural")])]:
        rows.append(dict(group=name, episodes=len(z), rewrites=float(z.gov_msg_rewrites.mean()),
                         templates=float(z.gov_msg_templates.mean())))
    pd.DataFrame(rows).to_csv(OUT / "message_interventions.csv", index=False)


def ledger():
    return pd.read_csv(ROOT / "data" / "ledger" / "calls.csv.gz", low_memory=False)


def auditor_costs(L):
    a = L[(L.role == "auditor") & (L.status == "ok")]
    cand = a[a.experiment.eq("A8b_cheap_auditor_live")]
    ref = a[a.experiment.eq("S5i_role_factorial") & a.unit.str.contains("-audit-s")]   # plain audit, no memory
    calls = pd.concat([cand, ref])
    calls = calls.assign(usd=calls.cost_equiv_usd.fillna(calls.cost_usd))
    calls[["experiment", "unit", "model", "cached", "latency_s", "usd", "day"]].to_csv(
        OUT / "auditor_cost_calls_plain.csv", index=False)
    rows = []
    for (src, model), z in [(("A8b", m), z) for m, z in cand.groupby("model")] + \
                           [(("S5i plain audit", m), z) for m, z in ref.groupby("model")]:
        z = calls.loc[z.index]
        rows.append(dict(model=model, source=src, calls=len(z), usd_per_1000_calls=1000 * float(z.usd.mean()),
                         median_latency_s=float(z[z.cached == 0].latency_s.median()),
                         first_day=z.day.min(), last_day=z.day.max()))
    pd.DataFrame(rows).to_csv(OUT / "auditor_costs_plain.csv", index=False)


def endpoint_provenance(L):
    sel = L[(L.experiment.isin(["A8_auditor_scale", "S5i_role_factorial", "A8b_cheap_auditor_live"]) & L.role.eq("auditor"))
            | L.experiment.eq("S3b_text_integrity")]
    g = sel.groupby(["experiment", "role", "model", "status"]).agg(first_day=("day", "min"), last_day=("day", "max"),
                                                                   calls=("day", "size")).reset_index()
    groups = [dict(stage=r.experiment, role=r.role, model=r.model, status=r.status, first_day=r.first_day,
                   last_day=r.last_day, calls=int(r.calls)) for r in g.itertuples()]
    out = {"source": "data/ledger/calls.csv.gz", "weights_identity": "not documented",
           "cost_query_filter": "role='auditor' AND status='ok'", "groups": groups}
    (OUT / "endpoint_call_provenance.json").write_text(json.dumps(out, indent=2) + "\n")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    execution_sensitivity()
    cache_replay_counts()
    message_interventions()
    L = ledger()
    auditor_costs(L)
    endpoint_provenance(L)
    print(f"revision tables written to {OUT}")
