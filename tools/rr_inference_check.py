"""Reviewer-response analysis R0a (2026-11-01; no API calls): are the key paired contrasts robust to the inference
method? The manuscript uses percentile bootstraps over 12-24 pairs (S5b_C, S5d, S5h) or 15 scenarios (S7b_C); a
reviewer may question their coverage at these sample sizes. For each contrast this script reports, from the SAME
eligible units and pairing as the paper:

  * the paper's percentile bootstrap (5000 resamples, seed 42) - must reproduce the manuscript numbers;
  * a t-interval on the paired differences;
  * an exact sign-flip randomisation test (all 2^n sign patterns when n <= 20, else 200 000 random patterns): the
    p-value for H0 "differences symmetric about 0" - valid at any n under exchangeability of signs within pairs;
  * leave-one-rotation-out (or leave-one-planner-out) estimates: the range shows whether one assignment drives the
    pooled number.

Usage:  python tools/rr_inference_check.py [AGENTGOV_ROOT]   -> reports/rr/inference_check.{csv,md}
"""
from __future__ import annotations

import itertools
import math
import pathlib
import sys

import numpy as np
import pandas as pd

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parents[1])
RUNS = ROOT / "data" / "runs"
OUT = ROOT / "reports" / "rr"


def boot(x, n=5000, seed=42):
    x = np.asarray(x, float)
    rng = np.random.default_rng(seed)
    b = rng.choice(x, size=(n, len(x)), replace=True).mean(axis=1)
    return float(x.mean()), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))


def t_ci(x):
    from scipy import stats
    x = np.asarray(x, float)
    n = len(x)
    se = x.std(ddof=1) / math.sqrt(n) if n > 1 else float("nan")
    q = stats.t.ppf(0.975, n - 1) if n > 1 else float("nan")
    return float(x.mean() - q * se), float(x.mean() + q * se)


def signflip_p(x, max_exact=20, n_rand=200_000, seed=42):
    x = np.asarray(x, float)
    obs = abs(x.mean())
    n = len(x)
    if n <= max_exact:
        signs = np.array(list(itertools.product([-1.0, 1.0], repeat=n)))
    else:
        signs = np.random.default_rng(seed).choice([-1.0, 1.0], size=(n_rand, n))
    stats_ = np.abs((signs * x).mean(axis=1))
    return float((stats_ >= obs - 1e-12).mean()), ("exact" if n <= max_exact else f"{n_rand} random")


def game_pairs(stage, a, b, y):
    v = pd.read_csv(RUNS / stage / "_analysis" / "validity_split.csv")
    s = pd.read_csv(RUNS / stage / "_analysis" / "summary_all.csv")
    el = s[s.eligible.astype(str).str.lower().isin(["true", "1"])][["rot", "seed", "governor", "attacker_mode"]]
    v = v.merge(el, on=["rot", "seed", "governor", "attacker_mode"])
    v = v[v.attacker_mode == "adaptive"]
    p = v.pivot_table(index=["rot", "seed"], columns="governor", values=y)
    d = (p[a] - p[b]).dropna()
    return d.reset_index().rename(columns={0: "d"}).assign(group=lambda q: q.rot)[["group", "d"]]


def rr_pairs(stage, a, b, y, index=("rot", "seed"), col="governor", where=None, group="rot"):
    """Reviewer-response stages (episodes.csv, eligible only): paired differences a - b of `col`, paired on `index`."""
    v = pd.read_csv(RUNS / stage / "_analysis" / "episodes.csv")
    v = v[v.eligible.astype(str).str.lower().isin(["true", "1"])]
    for k, val in (where or {}).items():
        v = v[v[k] == val]
    p = v.pivot_table(index=list(index), columns=col, values=y)
    d = (p[a] - p[b]).dropna().reset_index()
    d = d.rename(columns={0: "d"}) if 0 in d.columns else d.assign(d=(p[a] - p[b]).dropna().values)
    return d.assign(group=d[group])[["group", "d"]]


def feeder_pairs(y):
    c = pd.read_csv(RUNS / "S7b_C" / "_analysis" / "cells.csv")
    c = c[c.eligible.astype(str).str.lower().isin(["true", "1"])]
    p = c.pivot_table(index=["block", "rot", "plan"], columns="gov", values=y)
    d = (p["Gmsg"] - p["G0"]).dropna().reset_index()
    d.columns = ["block", "rot", "plan", "d"]
    return d


ROWS = []


def check(label, source, d, groups=None, unit="pairs"):
    x = d.d.values if hasattr(d, "d") else np.asarray(d)
    m, lo, hi = boot(x)
    tl, th = t_ci(x)
    p, kind = signflip_p(x)
    loo = []
    if groups is not None:
        for g in sorted(set(groups)):
            keep = np.asarray(groups) != g
            if keep.sum():
                loo.append(float(x[keep].mean()))
    ROWS.append({"contrast": label, "source": source, "n": len(x), "unit": unit, "estimate": m, "boot_lo": lo,
                 "boot_hi": hi, "t_lo": tl, "t_hi": th, "signflip_p": p, "signflip": kind,
                 "leave_one_group_out_min": min(loo) if loo else np.nan,
                 "leave_one_group_out_max": max(loo) if loo else np.nan})


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    # primary game contrasts (S5b_C, frozen plan pairing: rotation x seed)
    d = game_pairs("S5b_C", "label", "audit", "asr_per_round")
    check("C3 label - audit, ASR per round", "S5b_C", d, d.group)
    d = game_pairs("S5b_C", "audit_memory", "audit", "audit_misclassification_rate")
    check("C4 raw memory - audit, misclassification", "S5b_C", d, d.group)
    d = game_pairs("S5b_C", "audit_memory", "audit", "asr_per_round")
    check("raw memory - audit, ASR per round (secondary)", "S5b_C", d, d.group)
    # feeder primary (S7b_C): scenario = cluster, plan effects averaged within scenario (frozen plan)
    for y, lab in (("objective", "C5a Audit - Baseline, objective"), ("content_integrity", "C5b Audit - Baseline, content integrity")):
        f = feeder_pairs(y)
        blk = f.groupby(["block", "rot"]).d.mean().reset_index()
        check(lab, "S7b_C", blk, blk.rot, unit="scenarios")
        # leave-one-planner-out on the pooled estimate
        lpo = [float(f[f.plan != p].groupby("block").d.mean().mean()) for p in sorted(f.plan.unique())]
        ROWS[-1]["leave_one_plan_out_min"], ROWS[-1]["leave_one_plan_out_max"] = min(lpo), max(lpo)
    # exploratory memory contrasts
    for stage, a, b, y, lab in [
            ("S5b_role_rotation", "label", "audit", "asr_per_round", "S5b label - audit, ASR"),
            ("S5b_role_rotation", "audit_memory", "audit", "audit_misclassification_rate", "S5b raw memory - audit, misclassification"),
            ("S5d_memory_variants", "audit_memory", "audit", "audit_misclassification_rate", "S5d raw memory - audit, misclassification"),
            ("S5d_memory_variants", "audit_memory_struct", "audit", "audit_misclassification_rate", "S5d label-only - audit, misclassification"),
            ("S5d_memory_variants", "audit_memory", "audit", "asr_per_round", "S5d raw memory - audit, ASR"),
            ("S5d_memory_variants", "audit_neutral", "audit", "asr_per_round", "S5d neutral context - audit, ASR"),
            ("S5h_live_quarantine", "audit_quarantine", "audit_memory", "audit_misclassification_rate", "S5h tags - raw memory, misclassification"),
            ("S5h_live_quarantine", "audit_quarantine", "audit", "audit_misclassification_rate", "S5h tags - audit, misclassification"),
            ("S5h_live_quarantine", "audit_quarantine", "audit_memory", "asr_per_round", "S5h tags - raw memory, ASR"),
            ("S5h_live_quarantine", "audit_quarantine", "audit", "asr_per_round", "S5h tags - audit, ASR")]:
        try:
            d = game_pairs(stage, a, b, y)
        except (FileNotFoundError, KeyError):
            continue
        check(lab, stage, d, d.group)
    # reviewer-response stages (added 2026-11-06 review; same pairing as each stage's analysis, RR_PLAN_v1)
    rr = [
        ("S5j_live_labelonly", "audit_quarantine", "audit_memory_struct", "asr_per_round", {}, ("rot", "seed"), "governor", "rot",
         "R-J1 S5j tags - label-only, ASR"),
        ("S5j_live_labelonly", "audit_quarantine", "audit_memory_struct", "audit_misclassification_rate", {}, ("rot", "seed"), "governor", "rot",
         "R-J2 S5j tags - label-only, misclassification"),
        ("S5j_live_labelonly", "audit_memory_struct", "audit", "audit_misclassification_rate", {}, ("rot", "seed"), "governor", "rot",
         "R-J3 S5j label-only - audit, misclassification"),
        ("S5i_role_factorial", "audit_memory", "audit", "audit_misclassification_rate", {}, ("attacker", "auditor", "seed"), "governor", "auditor",
         "R-I3 S5i raw memory - audit, misclassification (pooled; group = auditor)"),
        ("S5k_oracle_feedback", "oracle", "adaptive", "asr_per_round", {"governor": "audit"}, ("rot", "seed"), "attacker_mode", "rot",
         "R-K1 S5k white-box - selection, ASR (audit)"),
        ("S5k_oracle_feedback", "oracle", "adaptive", "asr_per_round", {"governor": "audit_quarantine"}, ("rot", "seed"), "attacker_mode", "rot",
         "R-K1 S5k white-box - selection, ASR (tag memory)")]
    for au in ("deepseek_v4_pro", "glm53", "minimax_m3"):
        rr.append(("S5i_role_factorial", "audit_memory", "audit", "audit_misclassification_rate", {"auditor": au},
                   ("attacker", "seed"), "governor", "attacker", f"R-I3 S5i raw memory - audit, misclassification ({au} auditor)"))
    for stage, a, b, y, where, idx, col, grp, lab in rr:
        try:
            d = rr_pairs(stage, a, b, y, idx, col, where, grp)
        except (FileNotFoundError, KeyError):
            continue
        check(lab, stage, d, d.group)
    R = pd.DataFrame(ROWS)
    R.to_csv(OUT / "inference_check.csv", index=False)
    show = R.copy()
    for c in ("estimate", "boot_lo", "boot_hi", "t_lo", "t_hi", "leave_one_group_out_min", "leave_one_group_out_max"):
        show[c] = show[c].map(lambda v: f"{v:+.3f}" if v == v else "")
    show["signflip_p"] = R.signflip_p.map(lambda v: f"{v:.4f}" if v >= 0.0001 else "<0.0001")
    cols = ["contrast", "n", "estimate", "boot_lo", "boot_hi", "t_lo", "t_hi", "signflip_p",
            "leave_one_group_out_min", "leave_one_group_out_max"]
    lines = ["# R0a — inference-method robustness of the key paired contrasts", "",
             "Reviewer-response analysis (2026-11-01, no API calls). Same eligible units and pairing as the paper; "
             "`boot_*` must reproduce the manuscript. Sign-flip = randomisation test of the paired differences "
             "(exact when n ≤ 20). Leave-one-group-out = pooled estimate dropping one role assignment (rotation; for S5i: one auditor or attacker).", "",
             "| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in show.iterrows():
        lines.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    if "leave_one_plan_out_min" in R:
        lines += ["", "Leave-one-planner-out (S7b_C): " + "; ".join(
            f"{r.contrast}: {r.leave_one_plan_out_min:+.3f} to {r.leave_one_plan_out_max:+.3f}"
            for r in R.dropna(subset=["leave_one_plan_out_min"]).itertuples())]
    (OUT / "inference_check.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
