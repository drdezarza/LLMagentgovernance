"""Reviewer-response analysis R0b (2026-11-01; no API calls): one-figure summary of the paper's central trade-off.

Every game governor in every closed-loop study (S5b exploratory, S5b_C confirmatory, S5d memory controls, S5h live
quarantine, and - when they exist - S5j/S5k) placed on the same two axes, per 100 scheduled rounds:
  x = judge-clean legitimate proposals lost (auditor misclassification + cap restriction, stacked as one total;
      the split is in the CSV),
  y = attack successes.
Eligible episodes only (each study's own validity rules), adaptive attacker only, 95% bootstrap over episodes
(5000, seed 42). Lower-left is better. Output: reports/rr/frontier.{csv,pdf,png}.

Usage:  python tools/rr_frontier.py [AGENTGOV_ROOT]
"""
from __future__ import annotations

import pathlib
import sys

import numpy as np
import pandas as pd

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parents[1])
RUNS = ROOT / "data" / "runs"
OUT = ROOT / "reports" / "rr"

STUDIES = [("S5b_role_rotation", "S5b (exploratory)", "o"), ("S5b_C", "S5b_C (confirmatory)", "s"),
           ("S5d_memory_variants", "S5d (memory controls)", "^"), ("S5h_live_quarantine", "S5h (live tags)", "D"),
           ("S5j_live_labelonly", "S5j (label-only, RR)", "v"), ("S5i_role_factorial", "S5i (factorial, RR)", "P"),
           ("S5k_oracle_feedback", "S5k white-box (RR)", "X", "oracle")]   # 4th field: attacker_mode (default adaptive)
# fixed categorical order (validated palette, light mode): colour follows the governor, never its rank
GOVS = [("label", "Labels", "#2a78d6"), ("audit", "Plain audit", "#eb6834"), ("audit_memory", "Raw memory", "#1baf7a"),
        ("audit_memory_struct", "Label-only memory", "#eda100"), ("audit_quarantine", "Tag memory", "#e87ba4"),
        ("audit_tighten", "Tightening", "#008300"), ("audit_neutral", "Neutral context", "#6250d6"),
        ("audit_adaptive", "Memory + tightening", "#52514e")]


def boot(x, n=5000, seed=42):
    x = np.asarray([v for v in x if v == v], float)
    if not len(x):
        return np.nan, np.nan, np.nan
    b = np.random.default_rng(seed).choice(x, size=(n, len(x)), replace=True).mean(axis=1)
    return float(x.mean()), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))


def load(stage, mode="adaptive"):
    a = RUNS / stage / "_analysis"
    if (a / "episodes.csv").exists():                      # reviewer-response stages (eligible only)
        v = pd.read_csv(a / "episodes.csv")
        v = v[v.eligible.astype(str).str.lower().isin(["true", "1"])]
    elif (a / "validity_split.csv").exists() and (a / "summary_all.csv").exists():
        v = pd.read_csv(a / "validity_split.csv")
        s = pd.read_csv(a / "summary_all.csv")
        el = s[s.eligible.astype(str).str.lower().isin(["true", "1"])][["rot", "seed", "governor", "attacker_mode"]]
        v = v.merge(el, on=["rot", "seed", "governor", "attacker_mode"])
    else:
        return pd.DataFrame()
    return v[v.attacker_mode == mode]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for stage, label, mk, *mode in STUDIES:
        v = load(stage, *mode)
        if not len(v):
            continue
        v = v.assign(lost=v.audit_misclassification_rate + v.policy_cap_rejection_rate)
        for g, gl, col in GOVS:
            d = v[v.governor == g]
            if not len(d):
                continue
            a, al, ah = boot(100 * d.asr_per_round)
            l, ll, lh = boot(100 * d.lost)
            m = boot(100 * d.audit_misclassification_rate)[0]
            c = boot(100 * d.policy_cap_rejection_rate)[0]
            rows.append({"study": label, "stage": stage, "governor": gl, "episodes": len(d), "attacks_per100": a,
                         "attacks_lo": al, "attacks_hi": ah, "lost_per100": l, "lost_lo": ll, "lost_hi": lh,
                         "misclass_per100": m, "cap_loss_per100": c, "valid_submission": float(d.valid_submission_rate.mean())})
    R = pd.DataFrame(rows)
    R.to_csv(OUT / "frontier.csv", index=False)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ink, ink2, grid = "#0b0b0b", "#52514e", "#e4e3df"
    plt.rcParams.update({"font.size": 9, "axes.edgecolor": ink2, "axes.labelcolor": ink, "xtick.color": ink2,
                         "ytick.color": ink2, "font.family": "DejaVu Sans"})
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.set_facecolor("#fcfcfb")
    fig.patch.set_facecolor("#fcfcfb")
    ax.grid(True, color=grid, linewidth=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    colour = {gl: c for _, gl, c in GOVS}
    marker = {st[1]: st[2] for st in STUDIES}
    for r in R.itertuples():
        c = colour[r.governor]
        ax.errorbar(r.lost_per100, r.attacks_per100,
                    xerr=[[r.lost_per100 - r.lost_lo], [r.lost_hi - r.lost_per100]],
                    yerr=[[r.attacks_per100 - r.attacks_lo], [r.attacks_hi - r.attacks_per100]],
                    fmt="none", ecolor=c, elinewidth=1.0, alpha=0.55, capsize=0)
        ax.scatter(r.lost_per100, r.attacks_per100, s=46, marker=marker[r.study], color=c,
                   edgecolor="#fcfcfb", linewidth=1.2, zorder=3)
    # selective direct labels: one per governor, at its confirmatory point if present, else its first point
    for gl in R.governor.unique():
        d = R[R.governor == gl]
        r = d[d.stage == "S5b_C"].iloc[0] if (d.stage == "S5b_C").any() else d.iloc[0]
        off = {"Plain audit": (-8, -14), "Label-only memory": (10, 10), "Tag memory": (10, -4),
               "Neutral context": (8, 6), "Raw memory": (-8, -14), "Tightening": (8, 6)}.get(gl, (6, 5))
        ax.annotate(gl, (r.lost_per100, r.attacks_per100), xytext=off, textcoords="offset points", fontsize=8,
                    color=ink, ha="right" if off[0] < 0 else "left",
                    arrowprops=dict(arrowstyle="-", color=ink2, lw=0.5) if abs(off[0]) + abs(off[1]) > 14 else None)
    ax.set_xlabel("Legitimate (judge-clean) proposals lost per 100 rounds\n(auditor misclassification + cap restriction)")
    ax.set_ylabel("Attack successes per 100 rounds")
    ax.set_xlim(left=-2)
    ax.set_ylim(bottom=-2)
    # legends: colour = governor, shape = study (identity never colour-alone)
    from matplotlib.lines import Line2D
    h1 = [Line2D([], [], marker="o", ls="", color=colour[g], label=g) for g in R.governor.unique()]
    h2 = [Line2D([], [], marker=marker[s], ls="", color=ink2, label=s) for s in R.study.unique()]
    l1 = ax.legend(handles=h1, title="Governor", loc="upper right", frameon=False, fontsize=7.5, title_fontsize=8)
    ax.add_artist(l1)
    ax.legend(handles=h2, title="Study", loc="upper center", bbox_to_anchor=(0.45, 1.0), frameon=False, fontsize=7.5, title_fontsize=8)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.text(0.01, 0.01, "Lower-left is better. Bars: 95% bootstrap over episodes. Adaptive attacker (S5k: white-box), eligible episodes only.",
             fontsize=7, color=ink2)
    fig.savefig(OUT / "frontier.pdf")
    fig.savefig(OUT / "frontier.png", dpi=200)
    print(R.round(1).to_string(index=False))


if __name__ == "__main__":
    main()
