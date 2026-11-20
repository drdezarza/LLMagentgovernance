"""RR_PLAN_v3 N3 (no API calls): household- and subgroup-level curtailment burden (Reviewer 3, point 7).

The saved per-household records (realized.csv: hour, node, requested kW, realized kW) are expanded to all 40 households
of the feeder, including households that never received a request (zero burden). Household attributes (archetype,
lateral, depth) and flexible capacity are regenerated deterministically from the simulator with the same seeds the
episodes used (feeder_seed 1; load seed 100 + scenario seed; population seed = scenario seed). Flexible capacity =
sum over the 24 hours of max(0, true net load) x the household's curtailable share, i.e. the flexible energy available
before any intervention. Hours are 1 h, so kW summed over hours = kWh.

Per cell (one plan x governor x scenario), for requested and realized curtailment:
  * share of households with zero burden; mean, 90th percentile and maximum household kWh;
  * top-10% share (share of the cell total borne by the 4 most burdened households); Gini (checked against the recorded
    curtail_gini for realized curtailment);
  * the same burden as a share of the household's flexible energy: mean, 90th percentile, maximum, and the share of
    households asked for / delivering more than 50% of their flexible energy;
  * subgroup means by archetype, lateral and depth band (1-3, 4-7, 8-10), and the max/min ratio of subgroup means.
Contrasts: each governor - G0, paired by scenario block with plans averaged within block, bootstrap over blocks
(5000, seed 42). Descriptive; no claim in the paper depends on them.

Studies: S7b_C (G0, Gmsg; confirmatory sample) and S7b_mechanism_ablation (G0, Gmsg, Gcap, Ggini, G1r).
Outputs: reports/rr3/N3_household_burden.csv (one row per household x cell), N3_cell_metrics.csv,
         N3_subgroups.csv, N3_contrasts.csv, N3_household_burden.md
Usage:   python tools/rr3_burden.py [AGENTGOV_ROOT]
"""
from __future__ import annotations

import pathlib
import sys

import numpy as np
import pandas as pd

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parents[1])
CODE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE))
from agentgov.upstream import planning_core as P  # noqa: E402

RUNS, OUT = ROOT / "data" / "runs", ROOT / "reports" / "rr3"
STUDIES = {"S7b_C": ["G0", "Gmsg"], "S7b_mechanism_ablation": ["G0", "Gmsg", "Gcap", "Ggini", "G1r"]}
SPEC = P.FeederSpec()
T = P.build_feeder(SPEC, seed=1)
HORIZON = P.EpisodeConfig(seed=0).horizon
_flex_cache: dict[int, dict] = {}


def households(seed: int) -> pd.DataFrame:
    if seed not in _flex_cache:
        load, pv = P.load_profile(T, HORIZON, seed=100 + seed)
        net = load - pv
        pop = P.create_population(T, seed=seed)
        _flex_cache[seed] = pd.DataFrame([{
            "node": n, "archetype": pop[n].archetype, "lateral": int(T.nodes[n]["lateral"]),
            "depth": int(T.nodes[n]["depth"]),
            "flex_kwh": float(sum(P.flexible_kw(T, net[:, t], n) for t in range(HORIZON)))} for n in sorted(pop)])
    return _flex_cache[seed].copy()


def depth_band(d):
    return "1-3" if d <= 3 else ("4-7" if d <= 7 else "8-10")


def top_share(x, k=4):
    x = np.sort(np.asarray(x, float))[::-1]
    s = x.sum()
    return float(x[:k].sum() / s) if s > 0 else np.nan


def boot(x):
    x = np.asarray([v for v in x if v == v], float)
    if len(x) == 0:
        return np.nan, np.nan, np.nan
    b = np.random.default_rng(42).choice(x, size=(5000, len(x)), replace=True).mean(axis=1)
    return float(x.mean()), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    hh_rows, cell_rows, sub_rows = [], [], []
    for study, govs in STUDIES.items():
        cells = pd.read_csv(RUNS / study / "_analysis" / "cells.csv")
        if "eligible" in cells:
            cells = cells[cells.eligible.astype(str).str.lower().isin(["true", "1"])]
        cells = cells[cells.gov.isin(govs)]
        for c in cells.itertuples():
            f = RUNS / study / c.id / "realized.csv"
            if not f.exists():
                continue
            try:
                r = pd.read_csv(f)
            except pd.errors.EmptyDataError:      # no request issued in this cell: every household has zero burden
                r = pd.DataFrame(columns=["t", "node", "requested_kw", "realized_kw", "archetype", "depth", "lateral"])
            seed = int(c.seed)
            h = households(seed)
            agg = r.groupby("node")[["requested_kw", "realized_kw"]].sum() if len(r) else \
                pd.DataFrame(columns=["requested_kw", "realized_kw"])
            h = h.merge(agg, left_on="node", right_index=True, how="left").fillna({"requested_kw": 0.0, "realized_kw": 0.0})
            h = h.rename(columns={"requested_kw": "requested_kwh", "realized_kw": "realized_kwh"})
            if len(r):   # attribute check against the saved records
                chk = r.groupby("node")[["archetype", "depth", "lateral"]].first()
                m = h.set_index("node").loc[chk.index]
                assert (m.archetype.values == chk.archetype.values).all() and (m.depth.values == chk.depth.values).all() \
                    and (m.lateral.values == chk.lateral.values).all(), f"attribute mismatch in {c.id}"
            h["depth_band"] = h.depth.map(depth_band)
            for k in ("requested", "realized"):
                h[f"{k}_share_flex"] = h[f"{k}_kwh"] / h.flex_kwh.where(h.flex_kwh > 0)
            meta = {"study": study, "id": c.id, "rot": c.rot, "seed": seed, "plan": c.plan, "gov": c.gov,
                    "block": f"{c.rot}-sc{seed}"}
            hh_rows += [{**meta, **row} for row in h.to_dict("records")]
            row = {**meta, "recorded_curtail_gini": c.curtail_gini}
            for k in ("requested", "realized"):
                x, s = h[f"{k}_kwh"].values, h[f"{k}_share_flex"].values
                row.update({f"{k}_total_kwh": x.sum(), f"{k}_zero_share": float(np.mean(x <= 1e-9)),
                            f"{k}_mean_kwh": x.mean(), f"{k}_p90_kwh": float(np.percentile(x, 90)),
                            f"{k}_max_kwh": x.max(), f"{k}_top10_share": top_share(x), f"{k}_gini": P.gini(x),
                            f"{k}_mean_share_flex": float(np.nanmean(s)), f"{k}_p90_share_flex": float(np.nanpercentile(s, 90)),
                            f"{k}_max_share_flex": float(np.nanmax(s)), f"{k}_over50_flex": float(np.nanmean(s > 0.5))})
                for dim in ("archetype", "lateral", "depth_band"):
                    g = h.groupby(dim)[f"{k}_kwh"].mean()
                    row[f"{k}_{dim}_maxmin_ratio"] = float(g.max() / g.min()) if g.min() > 0 else np.inf
                    for lev, v in g.items():
                        sub_rows.append({**meta, "burden": k, "dimension": dim, "level": str(lev), "mean_kwh": v,
                                         "share_of_total": float(h[h[dim] == lev][f"{k}_kwh"].sum() / x.sum()) if x.sum() else np.nan,
                                         "n_households": int((h[dim] == lev).sum())})
            cell_rows.append(row)
    H, C, S = pd.DataFrame(hh_rows), pd.DataFrame(cell_rows), pd.DataFrame(sub_rows)
    C["gini_matches_record"] = np.isclose(C.realized_gini, C.recorded_curtail_gini, atol=1e-6)
    H.to_csv(OUT / "N3_household_burden.csv", index=False)
    C.to_csv(OUT / "N3_cell_metrics.csv", index=False)
    S.to_csv(OUT / "N3_subgroups.csv", index=False)

    metrics = [m for m in C.columns if m.startswith(("requested_", "realized_")) and not m.endswith("total_kwh")]
    metrics = [m for m in metrics if np.isfinite(C[m].replace([np.inf, -np.inf], np.nan).dropna()).all()]
    con = []
    for study, govs in STUDIES.items():
        d = C[C.study == study]
        for m in metrics + ["realized_total_kwh", "requested_total_kwh"]:
            p = d.replace([np.inf, -np.inf], np.nan).pivot_table(index=["block", "plan"], columns="gov", values=m)
            for g in govs[1:]:
                if g not in p:
                    continue
                blk = (p[g] - p["G0"]).dropna().groupby(level="block").mean()
                est, lo, hi = boot(blk.values)
                con.append({"study": study, "contrast": f"{g} - G0", "metric": m, "n_blocks": len(blk),
                            "g0_mean": float(d[d.gov == "G0"][m].replace([np.inf, -np.inf], np.nan).mean()),
                            "gov_mean": float(d[d.gov == g][m].replace([np.inf, -np.inf], np.nan).mean()),
                            "delta": est, "lo": lo, "hi": hi,
                            "verdict": "higher (resolved)" if lo > 0 else ("lower (resolved)" if hi < 0 else "unresolved")})
    K = pd.DataFrame(con)
    K.to_csv(OUT / "N3_contrasts.csv", index=False)

    # ---- report
    key = ["realized_zero_share", "realized_mean_kwh", "realized_p90_kwh", "realized_max_kwh", "realized_top10_share",
           "realized_gini", "realized_mean_share_flex", "realized_p90_share_flex", "realized_max_share_flex",
           "realized_over50_flex", "requested_zero_share", "requested_p90_kwh", "requested_max_kwh",
           "requested_top10_share", "requested_gini", "requested_max_share_flex", "requested_over50_flex"]
    lines = ["# N3: household- and subgroup-level curtailment burden (RR_PLAN_v3; no API calls)", "",
             f"All 40 households per cell, including households with no request. Recomputed realized Gini matches the "
             f"recorded curtail_gini in {int(C.gini_matches_record.sum())}/{len(C)} cells. Flexible energy = 24 h of "
             "max(0, true net load) × curtailable share, regenerated from the simulator seeds; saved household attributes "
             "match the regenerated ones in every cell. Means over cells; contrasts paired by scenario block, plans averaged, "
             "bootstrap 5000 / seed 42.", ""]
    for study, govs in STUDIES.items():
        d = C[C.study == study]
        t = d.groupby("gov")[key].mean().reindex(govs).T
        lines += [f"**{study}: burden distribution by governor** (cell means)", "",
                  "| metric | " + " | ".join(govs) + " |", "|---" * (len(govs) + 1) + "|"]
        lines += [f"| {m} | " + " | ".join(f"{v:.3f}" for v in t.loc[m].values) + " |" for m in key]
        lines += ["", f"**{study}: governor − G0** (selected metrics)", "", "| contrast | metric | Δ | 95% interval | verdict |",
                  "|---|---|---|---|---|"]
        k = K[(K.study == study) & K.metric.isin(["realized_gini", "realized_max_kwh", "realized_p90_kwh",
                                                     "realized_top10_share", "realized_max_share_flex", "realized_over50_flex",
                                                     "realized_zero_share", "realized_total_kwh", "requested_max_share_flex",
                                                     "realized_archetype_maxmin_ratio", "realized_lateral_maxmin_ratio",
                                                     "realized_depth_band_maxmin_ratio"])]
        lines += [f"| {r.contrast} | {r.metric} | {r.delta:+.3f} | [{r.lo:+.3f}, {r.hi:+.3f}] | {r.verdict} |" for r in k.itertuples()]
        s = S[(S.study == study) & (S.burden == "realized")].groupby(["dimension", "level", "gov"]).mean_kwh.mean().unstack("gov")
        s = s.reindex(columns=govs)
        lines += ["", f"**{study}: mean realized kWh per household by subgroup**", "",
                  "| dimension | level | " + " | ".join(govs) + " |", "|---|---" + "|---" * len(govs) + "|"]
        lines += [f"| {dim} | {lev} | " + " | ".join(f"{v:.2f}" for v in r.values) + " |" for (dim, lev), r in s.iterrows()]
        lines.append("")
    (OUT / "N3_household_burden.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
