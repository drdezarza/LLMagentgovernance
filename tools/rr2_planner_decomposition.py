"""RR_PLAN_v2 P1 (2026-11-16; no API calls): why the planning methods differ (reviewer comment R1.6).

Decomposes the feeder objective (upstream definition)
    objective = overload + voltage + curtailment
    overload = head_over_kwh, voltage = 4000 x v_violation_total, curtailment = 0.25 x curtailed_kwh
into its terms for every plan x governance cell of S7b, S7b_C and S7c (0% non-response), adds process measures
(curtailed energy, requests capped by the governor, compliance, revisions, message rewrites), and for S4b adds the
latency penalty and deadline misses per scenario family x planning mode. Descriptive only: no verdicts.

Outputs: reports/rr2/P1_*.csv, reports/rr2/P1_findings.md, reports/rr2/P1_components.{png,pdf}

Usage:  python tools/rr2_planner_decomposition.py [AGENTGOV_ROOT]
"""
from __future__ import annotations

import pathlib
import sys

import numpy as np
import pandas as pd

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parents[1])
RUNS = ROOT / "data" / "runs"
OUT = ROOT / "reports" / "rr2"
TERMS = ["overload", "voltage", "curtailment"]
PROC = ["curtailed_kwh", "mean_compliance", "revisions", "directive_realization", "gov_household_capped",
        "gov_policy_capped", "gov_msg_rewrites", "gov_msg_templates"]
PLAN_ORDER = ["SEARCH", "SEQUENTIAL", "HIERARCHICAL", "PREDEFINED", "natural"]
GOV_ORDER = ["G0", "Gmsg", "Gcap", "Ggini", "G1r"]
# validated categorical palette (light): slot order fixed, colour follows the term
COL = {"overload": "#2a78d6", "voltage": "#eb6834", "curtailment": "#1baf7a"}


def boot(x, n=5000, seed=42):
    x = np.asarray([v for v in x if v == v], float)
    if not len(x):
        return np.nan, np.nan, np.nan
    if len(x) == 1:
        return float(x[0]), np.nan, np.nan
    b = np.random.default_rng(seed).choice(x, size=(n, len(x)), replace=True).mean(axis=1)
    return float(x.mean()), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))


def md(df, fmt="{:.1f}"):
    if df is None or not len(df):
        return "_(empty)_"
    cols = [str(c) for c in df.columns]
    f = lambda v: (fmt.format(v) if isinstance(v, (float, np.floating)) and v == v else ("" if isinstance(v, float) else str(v)))
    return "\n".join(["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
                     + ["| " + " | ".join(f(v) for v in r) + " |" for r in df.itertuples(index=False)])


def load_cells(stage, extra_filter=None):
    f = RUNS / stage / "_analysis" / ("cells.csv" if (RUNS / stage / "_analysis" / "cells.csv").exists() else "cells_all.csv")
    if not f.exists():
        return pd.DataFrame()
    d = pd.read_csv(f)
    if "eligible" in d:
        d = d[d.eligible.astype(str).str.lower().isin(["true", "1"])]
    if extra_filter is not None:
        d = extra_filter(d)
    d = d.copy()
    d["overload"] = d.head_over_kwh
    d["voltage"] = 4000.0 * d.v_violation_total
    d["curtailment"] = 0.25 * d.curtailed_kwh
    d["block"] = d.rot.astype(str) + "-sc" + d.seed.astype(str)
    d["study"] = stage
    return d


def paired(d, a_mask, b_mask, y):
    a = d[a_mask].groupby("block")[y].mean()
    b = d[b_mask].groupby("block")[y].mean()
    x = (a - b).dropna()
    return (*boot(x.values), len(x))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    s7b = load_cells("S7b_mechanism_ablation")
    s7c_ = load_cells("S7b_C")
    s7c0 = load_cells("S7c_nonresponse", lambda d: d[pd.to_numeric(d.get("nonresponse", 0), errors="coerce").fillna(0) == 0])
    allc = pd.concat([d for d in (s7b, s7c_, s7c0) if len(d)], ignore_index=True)
    lines = ["# P1: why the planning methods differ (RR_PLAN_v2, descriptive, no API calls)", "",
             "Objective = overload + voltage + curtailment (overload = energy above the feeder import limit, kWh; "
             "voltage = 4000 × summed voltage-limit violation; curtailment = 0.25 × curtailed kWh). Lower is better. "
             "Eligible cells only (each study's validity rules). CIs: bootstrap over scenarios (5000, seed 42).", ""]

    # ---- P1a components by plan x governance
    keep = [c for c in ["objective"] + TERMS + PROC if c in allc]
    A = allc.groupby(["study", "plan", "gov"])[keep].mean().reset_index()
    A["plan"] = pd.Categorical(A.plan, [p for p in PLAN_ORDER if p in set(A.plan)], ordered=True)
    A["gov"] = pd.Categorical(A.gov, [g for g in GOV_ORDER if g in set(A.gov)], ordered=True)
    A = A.sort_values(["study", "plan", "gov"])
    A.to_csv(OUT / "P1a_components_by_plan_gov.csv", index=False)
    lines += ["## P1a. Objective terms by plan and governance", ""]
    for st, d in A.groupby("study", sort=False):
        cols = ["plan", "gov", "objective", "overload", "voltage", "curtailment", "curtailed_kwh", "mean_compliance",
                "revisions"] + [c for c in ("gov_household_capped", "gov_msg_rewrites") if c in d]
        lines += [f"**{st}**", "", md(d[cols].reset_index(drop=True)), ""]

    # ---- P1b plan differences under G0, paired by scenario
    rows = []
    for st, d in allc[allc.gov == "G0"].groupby("study"):
        plans = set(d.plan)
        for a, b in [("SEARCH", "SEQUENTIAL"), ("SEARCH", "HIERARCHICAL"), ("SEQUENTIAL", "HIERARCHICAL"),
                     ("SEARCH", "natural")]:
            if a in plans and b in plans:
                for y in ["objective"] + TERMS + ["curtailed_kwh"]:
                    m, lo, hi, n = paired(d, d.plan == a, d.plan == b, y)
                    rows.append({"study": st, "contrast": f"{a} − {b}", "outcome": y, "delta": m, "lo": lo, "hi": hi,
                                 "n_scenarios": n})
    B = pd.DataFrame(rows)
    B.to_csv(OUT / "P1b_plan_contrasts_G0.csv", index=False)
    wins = []
    for st, d in allc[allc.gov == "G0"].groupby("study"):
        p = d.pivot_table(index="block", columns="plan", values="objective")
        best = p.idxmin(axis=1).value_counts()
        rot = d.groupby(["rot", "plan"]).objective.mean().unstack()
        wins.append((st, best, rot))
        pd.DataFrame({"wins": best}).to_csv(OUT / f"P1b_wins_{st}.csv")
        rot.to_csv(OUT / f"P1b_objective_by_rotation_{st}.csv")
    lines += ["## P1b. Plan differences without governance (G0), paired by scenario", "",
              md(B[B.outcome.isin(["objective"] + TERMS)].assign(
                  ci=lambda x: x.apply(lambda r: f"[{r.lo:+.1f}, {r.hi:+.1f}]", axis=1))[
                  ["study", "contrast", "outcome", "delta", "ci", "n_scenarios"]]), ""]
    for st, best, rot in wins:
        lines += [f"- {st}: scenarios won under G0: " + ", ".join(f"{k} {v}" for k, v in best.items())
                  + "; mean objective by rotation (backbone):", "", md(rot.reset_index()), ""]

    # ---- P1b2 per-scenario SEARCH - SEQUENTIAL under G0 (robustness of the mean to single scenarios)
    rows, summ = [], []
    for st, d in allc[allc.gov == "G0"].groupby("study"):
        if not {"SEARCH", "SEQUENTIAL"} <= set(d.plan):
            continue
        p = d.pivot_table(index="block", columns="plan", values=["objective"] + TERMS)
        for b in p.index:
            rows.append({"study": st, "scenario": b, **{f"d_{y}": p.loc[b, (y, "SEARCH")] - p.loc[b, (y, "SEQUENTIAL")]
                                                       for y in ["objective"] + TERMS}})
        x = (p[("objective", "SEARCH")] - p[("objective", "SEQUENTIAL")]).dropna()
        worst = x.abs().idxmax()
        m2, lo2, hi2 = boot(x.drop(worst).values)
        summ.append({"study": st, "n": len(x), "mean": x.mean(), "median": x.median(),
                     "largest_abs_scenario": worst, "largest_abs_delta": x[worst],
                     "mean_without_largest": m2, "ci_without_largest": f"[{lo2:+.1f}, {hi2:+.1f}]",
                     "search_better_count": int((x < 0).sum())})
    pd.DataFrame(rows).to_csv(OUT / "P1b2_search_minus_sequential_by_scenario_G0.csv", index=False)
    S2 = pd.DataFrame(summ)
    S2.to_csv(OUT / "P1b2_search_minus_sequential_summary_G0.csv", index=False)
    lines += ["**SEARCH − SEQUENTIAL per scenario under G0** (sensitivity of the mean to the single most extreme scenario; "
              "descriptive, not a pre-specified test)", "", md(S2), ""]

    # ---- P1e hourly traces: overload hours with no request (plan did not respond to an overload it did not forecast)
    rows = []
    for st in ["S7b_mechanism_ablation", "S7b_C"]:
        for cdir in sorted((RUNS / st).glob("R*-sc*")):
            f = cdir / "timeseries.csv"
            if not f.exists() or "-G0" not in cdir.name:
                continue
            t = pd.read_csv(f)
            over = t.head_over_kw > 1e-6
            rows.append({"study": st, "cell": cdir.name, "plan": cdir.name.split("-")[2],
                         "block": "-".join(cdir.name.split("-")[:2]),
                         "overload_hours": int(over.sum()),
                         "overload_hours_no_request": int((over & (t.requested_kw <= 1e-6)).sum()),
                         "first_overload_hour": int(t.t[over].min()) if over.any() else np.nan,
                         "first_request_hour": int(t.t[t.requested_kw > 1e-6].min()) if (t.requested_kw > 1e-6).any() else np.nan})
    E = pd.DataFrame(rows)
    if len(E):
        E.to_csv(OUT / "P1e_unanswered_overload_hours_G0.csv", index=False)
        ES = E.groupby(["study", "plan"]).agg(cells=("cell", "size"), mean_overload_hours=("overload_hours", "mean"),
                                              mean_unanswered=("overload_hours_no_request", "mean"),
                                              cells_never_requesting=("first_request_hour", lambda s: int(s.isna().sum()))
                                              ).reset_index()
        ES.to_csv(OUT / "P1e_unanswered_overload_summary_G0.csv", index=False)
        lines += ["## P1e. Overload hours in which the plan requested nothing (G0, hourly traces)", "",
                  "SEARCH plans once at hour 0 from the forecast with a fixed compliance prior and no re-planning; "
                  "SEQUENTIAL and HIERARCHICAL re-plan after a violation. An overload the hour-0 forecast did not "
                  "show therefore stays unanswered under SEARCH.", "", md(ES), ""]
        never = E[(E.plan == "SEARCH") & E.first_request_hour.isna() & (E.overload_hours > 0)]
        if len(never):
            lines += ["SEARCH cells with overload but no request all day: " + ", ".join(f"{r.study}/{r.cell}"
                                                                                       for r in never.itertuples()), ""]
        # illustrative paired trajectory: the scenario with the largest SEARCH - SEQUENTIAL gap in S7b_C
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            gap = pd.read_csv(OUT / "P1b2_search_minus_sequential_by_scenario_G0.csv")
            gap = gap[gap.study == "S7b_C"].reset_index(drop=True)
            blk = gap.loc[gap.d_objective.idxmax(), "scenario"]
            fig, axs = plt.subplots(1, 2, figsize=(9.5, 3.4), sharey=True)
            for ax, plan in zip(axs, ["SEARCH", "SEQUENTIAL"]):
                t = pd.read_csv(RUNS / "S7b_C" / f"{blk}-{plan}-G0" / "timeseries.csv")
                ax.plot(t.t, t.head_over_kw, color="#2a78d6", lw=2, label="overload (kW above limit)")
                ax.plot(t.t, t.requested_kw, color="#eb6834", lw=2, label="curtailment requested (kW)")
                ax.plot(t.t, t.curtailed_kw, color="#1baf7a", lw=2, label="curtailment delivered (kW)")
                ax.set_title(f"{plan}", fontsize=10, loc="left")
                ax.set_xlabel("hour")
                for s in ("top", "right"):
                    ax.spines[s].set_visible(False)
                ax.yaxis.grid(True, color="#e6e5e0", lw=0.8)
                ax.set_axisbelow(True)
            axs[0].set_ylabel("kW")
            axs[1].legend(frameon=False, fontsize=8, loc="upper left")
            fig.suptitle(f"S7b_C {blk}, no governance: SEARCH plans once from the hour-0 forecast; SEQUENTIAL re-plans "
                         "after the first violation", fontsize=9, x=0.01, ha="left")
            fig.tight_layout()
            fig.savefig(OUT / "P1_trajectory.png", dpi=160)
            fig.savefig(OUT / "P1_trajectory.pdf")
            plt.close(fig)
            lines += [f"![trajectory {blk}](P1_trajectory.png)", ""]
        except Exception as e:
            lines += [f"(trajectory figure skipped: {e})", ""]

    # ---- P1c mechanism effects per plan (S7b), per term
    rows = []
    if len(s7b):
        for p, d in s7b.groupby("plan"):
            for g in [x for x in GOV_ORDER if x != "G0" and x in set(d.gov)]:
                for y in ["objective"] + TERMS + ["curtailed_kwh"] + [c for c in ("gov_household_capped",) if c in d]:
                    if y == "gov_household_capped":
                        v = d[d.gov == g][y]
                        rows.append({"plan": p, "mechanism": g, "outcome": "household requests capped (per episode)",
                                     "delta": float(pd.to_numeric(v, errors="coerce").fillna(0).mean()), "lo": np.nan,
                                     "hi": np.nan, "n_scenarios": int(len(v))})
                        continue
                    m, lo, hi, n = paired(d, d.gov == g, d.gov == "G0", y)
                    rows.append({"plan": p, "mechanism": g, "outcome": y, "delta": m, "lo": lo, "hi": hi, "n_scenarios": n})
    Cm = pd.DataFrame(rows)
    Cm.to_csv(OUT / "P1c_mechanism_effects_by_plan_S7b.csv", index=False)
    if len(Cm):
        piv = Cm[Cm.mechanism.isin(["Gmsg", "Gcap"])].copy()
        piv["v"] = piv.apply(lambda r: f"{r.delta:+.1f}" + (f" [{r.lo:+.1f}, {r.hi:+.1f}]" if r.lo == r.lo else ""), axis=1)
        T = piv.pivot_table(index=["mechanism", "plan"], columns="outcome", values="v", aggfunc="first").reset_index()
        order = ["mechanism", "plan", "objective", "overload", "voltage", "curtailment", "curtailed_kwh",
                 "household requests capped (per episode)"]
        T = T[[c for c in order if c in T]]
        lines += ["## P1c. What each governance mechanism changes, by plan (S7b, mechanism − G0, paired by scenario)", "",
                  md(T), ""]

    # ---- P1d S4b scenario bank
    f4 = RUNS / "S4b_scenario_bank" / "_analysis" / "modes_all.csv"
    if f4.exists():
        m = pd.read_csv(f4)
        m["overload"] = np.nan                                     # S4b stores the total only, plus its drivers
        m["latency_penalty"] = m.objective_adj - m.objective
        m["curtailment"] = 0.25 * m.curtailed_kwh
        m["physics_terms"] = m.objective - m.curtailment           # overload + voltage
        fam = {}
        try:
            sys.path.insert(0, str(ROOT))
            from agentgov.experiments.planning_exps import S4B_SCENARIOS  # noqa
            fam = {k: v.get("family", "") for k, v in S4B_SCENARIOS.items()}
        except Exception:
            pass
        if "family" not in m:
            m["family"] = m.scenario.map(fam)
        D = m.groupby(["split", "family", "scenario", "mode"])[["objective_adj", "physics_terms", "curtailment",
                                                                 "latency_penalty", "latency_s", "deadline_misses",
                                                                 "deadline_downgrades", "violation_hours",
                                                                 "curtailed_kwh"]].mean().reset_index()
        D.to_csv(OUT / "P1d_s4b_terms_by_scenario_mode.csv", index=False)
        W = D.loc[D.groupby("scenario").objective_adj.idxmin(), ["split", "family", "scenario", "mode", "objective_adj"]]
        S = D[D["mode"] == "SEARCH"].set_index("scenario").objective_adj
        W["search_obj"] = W.scenario.map(S)
        W["margin_vs_search"] = W.search_obj - W.objective_adj
        W.to_csv(OUT / "P1d_s4b_winners.csv", index=False)
        FA = D.groupby(["family", "mode"])[["objective_adj", "physics_terms", "curtailment", "latency_penalty",
                                            "deadline_misses"]].mean().reset_index()
        FA.to_csv(OUT / "P1d_s4b_terms_by_family_mode.csv", index=False)
        lines += ["## P1d. Planning scenario bank (S4b): objective terms, latency penalty and deadline misses", "",
                  "physics_terms = overload + voltage (S4b saved them as one total); latency_penalty = latency price × "
                  "decision latency (zero in scenarios without a latency price).", "",
                  "**Winner per scenario** (lowest mean adjusted objective over seeds; margin = SEARCH − winner)", "",
                  md(W.reset_index(drop=True)), "", "**By scenario family and mode**", "", md(FA), ""]

    # ---- figure: S7b objective terms, G0 vs Gcap vs Gmsg, by plan
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        d = A[(A.study == "S7b_mechanism_ablation") & (A.gov.isin(["G0", "Gmsg", "Gcap"]))].copy()
        plans = [p for p in ["SEARCH", "SEQUENTIAL", "HIERARCHICAL", "natural"] if p in set(d.plan)]
        govs = ["G0", "Gmsg", "Gcap"]
        fig, ax = plt.subplots(figsize=(9, 4.2))
        x0, w, gap = 0, 0.26, 0.012
        ticks, labels = [], []
        for i, p in enumerate(plans):
            for j, g in enumerate(govs):
                r = d[(d.plan == p) & (d.gov == g)]
                if not len(r):
                    continue
                xpos = i + (j - 1) * (w + 0.03)
                bottom = 0.0
                for t in TERMS:
                    h = float(r[t].iloc[0])
                    ax.bar(xpos, h - gap * 0, bottom=bottom, width=w, color=COL[t], edgecolor="#fcfcfb", linewidth=1.5,
                           label=t if (i == 0 and j == 0) else None)
                    bottom += h
                ax.text(xpos, bottom + 30, g, ha="center", va="bottom", fontsize=8, color="#55544f")
            ticks.append(i)
            labels.append(p)
        ax.set_xticks(ticks, labels)
        ax.set_ylabel("objective (lower is better)")
        fig.suptitle("S7b: objective terms by planning method under no governance (G0), message audit (Gmsg) "
                     "and intensity cap (Gcap)", fontsize=10, x=0.01, ha="left")
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.yaxis.grid(True, color="#e6e5e0", linewidth=0.8)
        ax.set_axisbelow(True)
        ax.xaxis.grid(False)
        ax.set_ylim(0, float(d[TERMS].sum(axis=1).max()) * 1.12)
        ax.legend(frameon=False, ncol=3, loc="lower left", bbox_to_anchor=(0, 1.0), fontsize=9)
        fig.tight_layout()
        fig.savefig(OUT / "P1_components.png", dpi=160)
        fig.savefig(OUT / "P1_components.pdf")
        plt.close(fig)
        lines += ["![P1](P1_components.png)", ""]
    except Exception as e:  # figure is optional
        lines += [f"(figure skipped: {e})", ""]
    (OUT / "P1_findings.md").write_text("\n".join(lines) + "\n")
    print(f"P1 written to {OUT}")


if __name__ == "__main__":
    main()
