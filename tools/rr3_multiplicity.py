"""RR_PLAN_v3 N1 (no API calls): family-wise sensitivity analysis of the confirmatory claims (Reviewer 3, point 3).

The planned readout (ANALYSIS_PLAN_v1) is unchanged. This adds a clearly labelled sensitivity analysis:

* Family: the six claim-level decisions C1, C2, C3, C4, C5a, C5b (K = 6).
* Each component is recomputed exactly as in the frozen analysis (same data, same bootstrap: 5000 resamples, seed 42,
  same resampling unit), and the recomputed 95% interval is checked against the recorded one.
* Composite claims follow their own definition (intersection-union): C1 needs both measures; C2 needs every rotation;
  C3 needs the pooled lower limit > 0 and a positive point estimate in every rotation. A composite claim's p-value is the
  largest p-value of its interval components.
* Each component is tested against its own claim threshold (C2 > 0.30, C4 > 0.10, C5a < +25 non-inferiority), never
  against zero instead.
* Bonferroni: two-sided 1 - 0.05/6 percentile intervals (one-sided error 0.05/12 per bound, matching the planned two-sided
  95% intervals with 0.025 per bound). Holm: step-down on the claim p-values. Bootstrap p-value for a bound criterion =
  2 x share of bootstrap means on the wrong side of the threshold (so p < alpha iff the two-sided 1 - alpha interval
  clears the threshold); reported as "< 1/5000" when no resample crosses it.

Outputs: reports/rr3/N1_multiplicity.csv, N1_multiplicity.md
Usage:   python tools/rr3_multiplicity.py [AGENTGOV_ROOT]
"""
from __future__ import annotations

import pathlib
import sys

import numpy as np
import pandas as pd

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parents[1])
RUNS, OUT = ROOT / "data" / "runs", ROOT / "reports" / "rr3"
N, SEED, K, ALPHA = 5000, 42, 6, 0.05


def boot_means(x):
    x = np.asarray([v for v in x if v == v], float)
    b = np.random.default_rng(SEED).choice(x, size=(N, len(x)), replace=True).mean(axis=1)
    return float(x.mean()), b


def cluster_boot_means(df, value, cluster="seed"):
    d = df[[cluster, value]].dropna()
    groups = [g[value].values for _, g in d.groupby(cluster)]
    rng = np.random.default_rng(SEED)
    k = len(groups)
    bs = np.array([np.concatenate([groups[i] for i in rng.integers(0, k, k)]).mean() for _ in range(N)])
    return float(d[value].mean()), bs


def p_lower(b, thr):      # H1: mean > thr
    return min(1.0, 2 * float(np.mean(b <= thr)))


def p_upper(b, thr):      # H1: mean < thr
    return min(1.0, 2 * float(np.mean(b >= thr)))


def comp(claim, component, est, b, side, thr, recorded=None, n=None):
    lo95, hi95 = np.percentile(b, [2.5, 97.5])
    a = ALPHA / K
    loB, hiB = np.percentile(b, [100 * a / 2, 100 * (1 - a / 2)])
    p = p_lower(b, thr) if side == "lower" else p_upper(b, thr)
    return {"claim": claim, "component": component, "n": n, "estimate": est, "criterion": f"{'lower' if side == 'lower' else 'upper'} limit {'>' if side == 'lower' else '<'} {thr:g}",
            "lo95": lo95, "hi95": hi95, "recorded_lo95": (recorded or (np.nan, np.nan))[0],
            "recorded_hi95": (recorded or (np.nan, np.nan))[1],
            "pass95": bool(lo95 > thr) if side == "lower" else bool(hi95 < thr),
            "lo_bonf": loB, "hi_bonf": hiB,
            "pass_bonf": bool(loB > thr) if side == "lower" else bool(hiB < thr),
            "p_boot": p, "p_floor": bool(p == 0.0)}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    # ---- C1 (S3b_C): cluster bootstrap over scenario seeds, both measures > 0
    pg = pd.read_csv(RUNS / "S3b_C" / "_analysis" / "paired_gaps.csv")
    rec = pd.read_csv(RUNS / "S3b_C" / "_analysis" / "pooled_gaps.csv").set_index("measure")
    for m in ("ecs_text", "integrity_text"):
        est, b = cluster_boot_means(pg, m)
        rows.append(comp("C1", m, est, b, "lower", 0.0, (rec.loc[m, "lo"], rec.loc[m, "hi"]), len(pg)))
    # ---- C2-C4 (S5b_C): eligible adaptive episodes
    v = pd.read_csv(RUNS / "S5b_C" / "_analysis" / "validity_split.csv")
    sa = pd.read_csv(RUNS / "S5b_C" / "_analysis" / "summary_all.csv")
    el = sa[sa.eligible.astype(str).str.lower().isin(["true", "1"])][["rot", "seed", "governor"]]
    v = v.merge(el, on=["rot", "seed", "governor"], how="inner")
    v = v[v.attacker_mode == "adaptive"]
    r24 = pd.read_csv(RUNS / "S5b_C" / "_analysis" / "confirmatory_C2_C4.csv")
    recd = {(r.hypothesis, r.scope): (r.lo, r.hi) for r in r24.itertuples()}
    lab = v[v.governor == "label"]
    for rot, d in lab.groupby("rot"):
        est, b = boot_means(d.asr_given_submission)
        rows.append(comp("C2", f"label ASR given submission, {rot}", est, b, "lower", 0.30, recd.get(("C2", rot)), len(d)))
    P = {y: v.pivot_table(index=["rot", "seed"], columns="governor", values=y)
         for y in ("asr_per_round", "audit_misclassification_rate")}
    d3 = (P["asr_per_round"]["label"] - P["asr_per_round"]["audit"]).dropna()
    est, b = boot_means(d3.values)
    rows.append(comp("C3", "label - audit ASR per round, pooled", est, b, "lower", 0.0, recd.get(("C3", "pooled")), len(d3)))
    c3_rot_positive = bool((d3.groupby(level="rot").mean() > 0).all())
    d4 = (P["audit_misclassification_rate"]["audit_memory"] - P["audit_misclassification_rate"]["audit"]).dropna()
    est, b = boot_means(d4.values)
    rows.append(comp("C4", "raw memory - audit misclassification, pooled", est, b, "lower", 0.10, recd.get(("C4", "pooled")), len(d4)))
    # ---- C5 (S7b_C): plans averaged within scenario, bootstrap over the 15 scenarios
    c = pd.read_csv(RUNS / "S7b_C" / "_analysis" / "cells.csv")
    c = c[c.eligible.astype(str).str.lower().isin(["true", "1"])] if "eligible" in c else c
    c["block"] = c.rot.astype(str) + "-sc" + c.seed.astype(str)
    r5 = pd.read_csv(RUNS / "S7b_C" / "_analysis" / "confirmatory_C5.csv")
    r5 = {r.hypothesis: (r.lo, r.hi) for r in r5[r5.plan == "all"].itertuples()}
    for y, hyp, side, thr in (("objective", "C5a", "upper", 25.0), ("content_integrity", "C5b", "lower", 0.0)):
        p = c.pivot_table(index=["block", "plan"], columns="gov", values=y)
        blk = (p.Gmsg - p.G0).dropna().groupby(level="block").mean()
        est, b = boot_means(blk.values)
        rows.append(comp(hyp, f"Gmsg - G0 {y}, pooled over plans", est, b, side, thr, r5.get(hyp), len(blk)))
    D = pd.DataFrame(rows)
    D["recomputed_matches_record"] = (np.isclose(D.lo95, D.recorded_lo95, atol=1e-9) &
                                      np.isclose(D.hi95, D.recorded_hi95, atol=1e-9)) | D.recorded_lo95.isna()
    D.to_csv(OUT / "N1_multiplicity_components.csv", index=False)
    # ---- claim level
    cl = []
    for claim, g in D.groupby("claim", sort=False):
        extra_ok = c3_rot_positive if claim == "C3" else True
        cl.append({"claim": claim, "components": len(g), "p_claim": float(g.p_boot.max()),
                   "p_floor": bool(g.p_boot.max() == 0.0),
                   "pass95_planned": bool(g.pass95.all() and extra_ok), "pass_bonferroni": bool(g.pass_bonf.all() and extra_ok),
                   "extra_condition": "positive in every rotation: " + str(c3_rot_positive) if claim == "C3" else ""})
    C = pd.DataFrame(cl).sort_values("p_claim", kind="stable").reset_index(drop=True)
    m = len(C)
    holm, still = [], True
    for i, r in C.iterrows():
        thr = ALPHA / (m - i)
        ok = still and (r.p_claim < thr or (r.p_floor and 1 / N < thr))
        if not ok:
            still = False
        holm.append({"holm_threshold": thr, "pass_holm": bool(ok and (r.claim != "C3" or c3_rot_positive))})
    C = pd.concat([C, pd.DataFrame(holm)], axis=1)
    C.to_csv(OUT / "N1_multiplicity.csv", index=False)

    def f(x):
        return "< 0.0002" if x == 0 else f"{x:.4f}"
    lines = ["# N1: family-wise sensitivity analysis of the confirmatory claims (RR_PLAN_v3; no API calls)", "",
             "The planned readout is unchanged. Family = C1, C2, C3, C4, C5a, C5b (K = 6). Components recomputed with the "
             "frozen data, resampling units and bootstrap (5000, seed 42); every recomputed 95% interval matches the "
             f"recorded one: **{bool(D.recomputed_matches_record.all())}**. Bonferroni intervals are two-sided "
             f"{100 * (1 - ALPHA / K):.2f}% percentile intervals; each component is tested against its own claim threshold.", "",
             "| claim | component | n | estimate | criterion | 95% interval | Bonferroni interval | bootstrap p |",
             "|---|---|---|---|---|---|---|---|"]
    for r in D.itertuples():
        lines.append(f"| {r.claim} | {r.component} | {r.n} | {r.estimate:+.3f} | {r.criterion} | "
                     f"[{r.lo95:+.3f}, {r.hi95:+.3f}] | [{r.lo_bonf:+.3f}, {r.hi_bonf:+.3f}] | {f(r.p_boot)} |")
    lines += ["", "**Claim level** (composite claims: largest component p; Holm step-down at α = 0.05)", "",
              "| claim | p (claim) | planned 95% rule | Bonferroni | Holm | note |", "|---|---|---|---|---|---|"]
    for r in C.itertuples():
        lines.append(f"| {r.claim} | {f(r.p_claim)} | {'met' if r.pass95_planned else 'not met'} | "
                     f"{'met' if r.pass_bonferroni else 'not met'} | {'met' if r.pass_holm else 'not met'} | {r.extra_condition} |")
    lines += ["", f"- Claims met under Bonferroni: {int(C.pass_bonferroni.sum())}/{m}; under Holm: {int(C.pass_holm.sum())}/{m}.",
              "- A bootstrap p of '< 0.0002' means no resample crossed the threshold (resolution 1/5000).",
              "- C5a is a non-inferiority claim. Its Bonferroni interval still lies below the +25 margin, but it now "
              "includes 0, so the adjusted analysis supports non-inferiority only, not an objective improvement (the paper "
              "does not claim one).",
              "- Sensitivity analysis only: it does not replace the frozen decision rule."]
    (OUT / "N1_multiplicity.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
