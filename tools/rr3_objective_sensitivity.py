"""RR_PLAN_v3 N2 (no API calls): sensitivity of the feeder non-inferiority result to the margin and to the objective
weights (Reviewer 3, point 6).

The recorded feeder outcomes are re-scored; the planners are NOT re-run, so this shows how the recorded policies compare
under other weightings, not how planners redesigned for other weights would behave.

  objective(w_v, w_c) = overload_kWh + w_v x voltage_violation + w_c x curtailed_kWh       (frozen: w_v 4000, w_c 0.25)

For every weight pair: Audit (Gmsg) - Baseline (G0), plans averaged within scenario, bootstrap over the 15 scenarios
(5000, seed 42), for the confirmatory sample (S7b_C) and its re-execution at 0 % non-response (S7c). Reported: the
upper 95% limit (= the smallest non-inferiority margin the data support, in objective units), the same limit as a
percentage of the Baseline mean objective, and whether it lies below the frozen 25-unit margin and alternative margins
(10, 15, 25, 50). Per plan as well (descriptive). Also: Audit - Baseline content integrity per plan (does the audit
raise integrity where the objective moves?).

Outputs: reports/rr3/N2_objective_sensitivity.csv, N2_integrity_by_plan.csv, N2_objective_sensitivity.md
Usage:   python tools/rr3_objective_sensitivity.py [AGENTGOV_ROOT]
"""
from __future__ import annotations

import pathlib
import sys

import numpy as np
import pandas as pd

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parents[1])
RUNS, OUT = ROOT / "data" / "runs", ROOT / "reports" / "rr3"
WV = [1000, 2000, 4000, 8000, 16000]
WC = [0.0, 0.1, 0.25, 0.5, 1.0]
MARGINS = [10, 15, 25, 50]


def boot(x):
    x = np.asarray(x, float)
    b = np.random.default_rng(42).choice(x, size=(5000, len(x)), replace=True).mean(axis=1)
    return float(x.mean()), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))


def load(stage):
    d = pd.read_csv(RUNS / stage / "_analysis" / "cells.csv")
    d = d[d.eligible.astype(str).str.lower().isin(["true", "1"])] if "eligible" in d else d
    if stage == "S7c_nonresponse":
        d = d[pd.to_numeric(d.nonresponse, errors="coerce").fillna(0) == 0]
    d = d.copy()
    d["block"] = d.rot.astype(str) + "-sc" + d.seed.astype(str)
    return d


def contrast(d, y, plan=None):
    z = d if plan is None else d[d.plan == plan]
    p = z.pivot_table(index=["block", "plan"], columns="gov", values=y)
    blk = (p.Gmsg - p.G0).dropna().groupby(level="block").mean()
    base = z[z.gov == "G0"][y].mean()
    return (*boot(blk.values), len(blk), float(base))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows, irows = [], []
    for stage in ("S7b_C", "S7c_nonresponse"):
        d = load(stage)
        rec = d.objective - (d.head_over_kwh + 4000 * d.v_violation_total + 0.25 * d.curtailed_kwh)
        check = float(rec.abs().max())
        for wv in WV:
            for wc in WC:
                d["obj_w"] = d.head_over_kwh + wv * d.v_violation_total + wc * d.curtailed_kwh
                for plan in [None] + sorted(d.plan.unique()):
                    m, lo, hi, n, base = contrast(d, "obj_w", plan)
                    rows.append({"study": stage, "plan": plan or "all", "w_voltage": wv, "w_curtailment": wc,
                                 "frozen_weights": wv == 4000 and wc == 0.25, "delta": m, "lo": lo, "hi": hi, "n": n,
                                 "baseline_mean": base, "hi_pct_of_baseline": 100 * hi / base if base else np.nan,
                                 **{f"noninferior_at_{M}": bool(hi < M) for M in MARGINS},
                                 "max_abs_recompute_error_frozen": check})
        for plan in [None] + sorted(d.plan.unique()):
            m, lo, hi, n, base = contrast(d, "content_integrity", plan)
            irows.append({"study": stage, "plan": plan or "all", "delta_integrity": m, "lo": lo, "hi": hi, "n": n,
                          "baseline_integrity": base})
    R = pd.DataFrame(rows)
    R.to_csv(OUT / "N2_objective_sensitivity.csv", index=False)
    I = pd.DataFrame(irows)
    I.to_csv(OUT / "N2_integrity_by_plan.csv", index=False)
    lines = ["# N2: margin and objective-weight sensitivity of the feeder non-inferiority result (RR_PLAN_v3; no API calls)", "",
             "Recorded outcomes re-scored as overload + w_v × voltage violation + w_c × curtailed kWh (frozen w_v = 4000, "
             f"w_c = 0.25; recomputing the frozen objective from its terms reproduces it to "
             f"{R.max_abs_recompute_error_frozen.max():.1e}). Audit − Baseline, plans averaged within scenario, 15 scenarios, "
             "bootstrap 5000 / seed 42. The upper limit is the smallest margin the data support.", ""]
    for stage in ("S7b_C", "S7c_nonresponse"):
        a = R[(R.study == stage) & (R.plan == "all")]
        t = a.pivot_table(index="w_voltage", columns="w_curtailment", values="hi").round(1)
        lines += [f"**{stage} (pooled): upper 95% limit of Audit − Baseline** (rows w_v, columns w_c)", "",
                  "| w_v \\ w_c | " + " | ".join(str(c) for c in t.columns) + " |", "|---" * (len(t.columns) + 1) + "|"]
        for wv, r in t.iterrows():
            lines.append(f"| {wv} | " + " | ".join(f"{v:+.1f}" for v in r.values) + " |")
        n25 = int(a.noninferior_at_25.sum())
        worst = a.loc[a.hi.idxmax()]
        lines += ["", f"- Non-inferior at the frozen 25-unit margin in {n25}/{len(a)} weight pairs; the largest upper limit is "
                  f"{worst.hi:+.1f} (w_v {int(worst.w_voltage)}, w_c {worst.w_curtailment}), "
                  f"{worst.hi_pct_of_baseline:.1f}% of the Baseline mean. At the frozen weights the upper limit is "
                  f"{a[a.frozen_weights].hi.iloc[0]:+.1f} ({a[a.frozen_weights].hi_pct_of_baseline.iloc[0]:.2f}% of the Baseline mean).",
                  f"- Margins: non-inferior in " + ", ".join(f"{int(a[f'noninferior_at_{M}'].sum())}/{len(a)} pairs at {M}" for M in MARGINS) + ".", ""]
        p = R[(R.study == stage) & (R.plan != "all") & R.frozen_weights][["plan", "delta", "lo", "hi"]]
        lines += [f"Per plan at the frozen weights ({stage}; descriptive)", "", "| plan | Δ | 95% interval |", "|---|---|---|"]
        lines += [f"| {r.plan} | {r.delta:+.1f} | [{r.lo:+.1f}, {r.hi:+.1f}] |" for r in p.itertuples()] + [""]
    lines += ["**Audit − Baseline content integrity by plan** (descriptive)", "", "| study | plan | Δ integrity | 95% interval |",
              "|---|---|---|---|"]
    lines += [f"| {r.study} | {r.plan} | {r.delta_integrity:+.3f} | [{r.lo:+.3f}, {r.hi:+.3f}] |" for r in I.itertuples()]
    (OUT / "N2_objective_sensitivity.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
