"""Figures for experiment analyses (matplotlib, Agg backend)."""
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

PAL = ["#2a6f97", "#c8553d", "#588157", "#8d6cab", "#e0a458", "#4d908e", "#9c6644", "#6c757d"]
GOV = {"governed": "#2E7D32", "naive": "#F57F17", "unconstrained": "#C62828"}
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.alpha": 0.25, "figure.dpi": 130})


def _save(fig, path):
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def s1_panels(df, path):
    df = df.sort_values("alias")
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.2))
    x = np.arange(len(df))
    ax[0].bar(x - 0.2, df.policy_nonfactual_rate, 0.4, label="non-factual claims", color=PAL[1])
    ax[0].bar(x + 0.2, df.policy_fear_rate, 0.4, label="FEAR theme", color=PAL[4])
    ax[0].set_title("Voluntary manipulative policies\n(permissive schema)")
    ax[0].legend(fontsize=8)
    ax[1].bar(x, df.plan_mode_entropy.fillna(0), color=PAL[0])
    ax[1].set_title("Planning-mode entropy (0 = collapse)")
    ax[1].set_ylim(0, 1)
    ax[2].bar(x, df.manip_discrimination.fillna(0), color=PAL[2])
    ax[2].axhline(0, color="k", lw=0.8)
    ax[2].set_title("Manipulation discrimination\n(factual − manipulative shift)")
    for a in ax:
        a.set_xticks(x)
        a.set_xticklabels(df.alias, rotation=45, ha="right", fontsize=8)
    _save(fig, path)


def s2_compare(cmp, path):
    mets = cmp.metric.unique().tolist()
    conds = cmp.condition.unique().tolist()
    fig, ax = plt.subplots(1, len(mets), figsize=(3.2 * len(mets), 3.6))
    for a, m in zip(np.atleast_1d(ax), mets):
        sub = cmp[cmp.metric == m]
        x = np.arange(len(conds))
        for off, col, lab, lo, hi, c in [(-0.18, "ours", "this pipeline", "ours_lo", "ours_hi", PAL[0]),
                                         (0.18, "published", "published v4", "pub_lo", "pub_hi", "#999999")]:
            s = sub.set_index("condition").loc[conds]
            a.bar(x + off, s[col], 0.34, color=c, label=lab,
                  yerr=[s[col] - s[lo], s[hi] - s[col]], capsize=3)
        a.set_xticks(x)
        a.set_xticklabels(conds, rotation=30, fontsize=8)
        a.set_title(m.replace("_final", ""))
    np.atleast_1d(ax)[0].legend(fontsize=8)
    _save(fig, path)


def s3_gaps(g, path):
    g = g.sort_values("ecs_gap")
    fig, ax = plt.subplots(figsize=(7, 0.45 * len(g) + 1.5))
    y = np.arange(len(g))
    ax.errorbar(g.ecs_gap, y, xerr=[g.ecs_gap - g.ecs_gap_lo, g.ecs_gap_hi - g.ecs_gap], fmt="o", color=PAL[0], capsize=3)
    ax.axvline(0, color="k", lw=0.8)
    ax.set_yticks(y)
    ax.set_yticklabels(g.alias)
    ax.set_xlabel("ECS gap, governed − unconstrained (95% bootstrap CI over seeds)")
    _save(fig, path)


def s4_regret(df, path):
    pol = sorted(df.policy.unique())
    al = sorted(df.alias.unique())
    fig, ax = plt.subplots(figsize=(1.6 * len(pol) + 3, 4))
    w = 0.8 / max(len(al), 1)
    for k, a in enumerate(al):
        m = df[df.alias == a].groupby("policy").regret.mean().reindex(pol)
        ax.bar(np.arange(len(pol)) + k * w - 0.4 + w / 2, m.values, w, label=a, color=PAL[k % len(PAL)])
    ax.set_xticks(np.arange(len(pol)))
    ax.set_xticklabels(pol, rotation=30, ha="right")
    ax.set_ylabel("mean regret vs per-seed oracle")
    ax.legend(fontsize=7)
    _save(fig, path)


def s5_curves(cv, path):
    fig, ax = plt.subplots(1, 2, figsize=(12, 4), sharey=True)
    for a, am in zip(ax, ["static", "adaptive"]):
        sub = cv[cv.attacker_mode == am]
        for k, gv in enumerate(sorted(sub.governor.unique())):
            ss = sub[sub.governor == gv].copy()
            ss["succ"] = ss.attack_success.map({True: 1.0, False: 0.0, "True": 1.0, "False": 0.0})
            s = ss.groupby("k").succ.mean()     # unresolved judge rounds excluded
            s = s.rolling(5, min_periods=1).mean()
            a.plot(s.index, s.values, label=gv, color=PAL[k], lw=2)
        a.set_title(f"{am} attacker")
        a.set_xlabel("deployment round")
    ax[0].set_ylabel("attack success (5-round rolling mean)")
    ax[0].legend()
    _save(fig, path)


def s6_frontier(agg, path):
    fig, ax = plt.subplots(figsize=(6, 4.2))
    ycol = "ecs_abs_err" if "ecs_abs_err" in agg else "ecs"
    for k, r in agg.reset_index(drop=True).iterrows():
        ax.scatter(r["strong_frac"], r[ycol], s=60, color=PAL[k % len(PAL)])
        ax.annotate(r["policy"], (r["strong_frac"], r[ycol]), xytext=(5, 4), textcoords="offset points")
    ax.set_xlabel("fraction of agent calls sent to the strong model")
    ax.set_ylabel("|ECS − ECS(always strong)|" if ycol == "ecs_abs_err" else "ECS")
    _save(fig, path)


def s7_interaction(df, path):
    """Interaction plots: outcome by plan, one line per governance regime, one panel per outcome."""
    outs = [("objective", "objective (lower better)"), ("violation_hours", "violation hours"),
            ("mean_compliance", "mean compliance"), ("backlash_rate", "prosumer backlash rate")]
    plans = [p for p in ["PREDEFINED", "SEQUENTIAL", "HIERARCHICAL", "SEARCH", "natural"] if p in set(df.plan)]
    col = {"G0": "#C62828", "G1": "#2E7D32", "G2": "#2a6f97"}
    fig, ax = plt.subplots(1, len(outs), figsize=(4.2 * len(outs), 3.8))
    x = np.arange(len(plans))
    for a, (y, lab) in zip(ax, outs):
        for g in sorted(df.gov.unique()):
            sub = df[df.gov == g].groupby("plan")[y]
            m = sub.mean().reindex(plans)
            se = (sub.std() / np.sqrt(sub.count())).reindex(plans)
            a.errorbar(x, m.values, yerr=1.96 * se.values, label=g, color=col.get(g, "k"), marker="o", capsize=3, lw=1.6)
        a.set_xticks(x)
        a.set_xticklabels(plans, rotation=30, ha="right", fontsize=8)
        a.set_title(lab)
    ax[0].legend(fontsize=8)
    _save(fig, path)
