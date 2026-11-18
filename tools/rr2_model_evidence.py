"""RR_PLAN_v2 M1 (2026-11-16; no API calls): model evidence table for reviewer comment R1.3
(rationale for the LLMs used; advantages and limitations).

One row per model alias that played a role in the paper's studies. Every value is read from existing records:
  roles     : role columns of the study records (S3 population backbone; S4b/S7b/S7b_C/S7c planner backbone;
              S5b/S5b_C/S5h/S5i/S5j/S5k attacker, auditor, judge; S7b auditor/judge)
  price     : config/settings.yaml roster (USD per 1M input / output tokens) and tier
  interface : S0 (usable, thinking setting, latency), S1 (parse rates, intensity, plan modes)
  quality   : A1 (anchor-set balanced accuracy as auditor/judge), A3 (auditor vs judge, judge kappa),
              A8 (fixed-text sensitivity / false positives / cost per 1000 audits / latency)
  closed loop: S5i (mean ASR per round and misclassification by auditor and by attacker; raw-memory penalty)
  population: S3 (governance gap in ECS with that backbone, CI)
Descriptive; empty cells mean "not measured". Outputs: reports/rr2/M1_model_evidence.{csv,md}

Usage:  python tools/rr2_model_evidence.py [AGENTGOV_ROOT]
"""
from __future__ import annotations

import json
import pathlib
import sys

import pandas as pd
import yaml

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parents[1])
RUNS = ROOT / "data" / "runs"
OUT = ROOT / "reports" / "rr2"


def rd(stage, name):
    f = RUNS / stage / "_analysis" / name
    return pd.read_csv(f) if f.exists() else pd.DataFrame()


def elig(d):
    if "eligible" in d:
        return d[d.eligible.astype(str).str.lower().isin(["true", "1"])]
    return d


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    settings = yaml.safe_load((ROOT / "config" / "settings.yaml").read_text())
    roster = settings.get("roster") or {}

    # ---- roles from records
    roles = []
    role_src = {
        "S3_gcge_cross_model": ("summary.csv", {"alias": "population backbone"}),
        "S7b_mechanism_ablation": ("cells.csv", {"alias": "planner backbone", "auditor_used": "message auditor", "judge": "judge"}),
        "S7b_C": ("cells.csv", {"alias": "planner backbone", "auditor_used": "message auditor", "judge": "judge"}),
        "S7c_nonresponse": ("cells.csv", {"alias": "planner backbone", "auditor_used": "message auditor", "judge": "judge"}),
        "S5b_C": ("summary.csv", {"attacker": "attacker", "auditor": "auditor", "judge": "judge"}),
        "S5b_role_rotation": ("summary.csv", {"attacker": "attacker", "auditor": "auditor", "judge": "judge"}),
        "S5h_live_quarantine": ("summary.csv", {"attacker": "attacker", "auditor": "auditor", "judge": "judge"}),
        "S5i_role_factorial": ("episodes.csv", {"attacker": "attacker", "auditor": "auditor", "judge": "judge"}),
        "S5j_live_labelonly": ("episodes.csv", {"attacker": "attacker", "auditor": "auditor", "judge": "judge"}),
        "S5k_oracle_feedback": ("episodes.csv", {"attacker": "attacker", "auditor": "auditor", "judge": "judge"}),
    }
    for st, (fn, cols) in role_src.items():
        d = elig(rd(st, fn))
        for c, role in cols.items():
            if c in d:
                for a, n in d[c].dropna().astype(str).value_counts().items():
                    if a and a.lower() not in ("none", "nan", ""):
                        roles.append({"alias": a, "role": role, "study": st, "n": int(n)})
    R = pd.DataFrame(roles)
    R.to_csv(OUT / "M1_roles_by_study.csv", index=False)
    role_txt = (R.groupby(["alias", "role"]).study.apply(lambda s: "/".join(sorted(set(x.split("_")[0] for x in s))))
                .reset_index().groupby("alias").apply(lambda g: "; ".join(f"{r.role} ({r.study})" for r in g.itertuples()))
                if len(R) else pd.Series(dtype=str))

    aliases = sorted(set(R.alias) if len(R) else set())
    T = pd.DataFrame({"alias": aliases})
    T["roles"] = T.alias.map(role_txt)
    T["model_id"] = T.alias.map(lambda a: (roster.get(a, {}).get("candidates") or roster.get(a, {}).get("ids") or [""])[0]
                                if isinstance(roster.get(a, {}), dict) else "")
    T["tier"] = T.alias.map(lambda a: roster.get(a, {}).get("tier", ""))
    T["price_in_out_usd_per_M"] = T.alias.map(lambda a: "/".join(str(x) for x in roster.get(a, {}).get("price", [])) or "")

    # ---- S0 / S1 interface
    s0 = rd("S0_connectivity", "model_profiles.csv")
    if len(s0):
        s0 = s0.set_index("alias")
        T["S0_usable"] = T.alias.map(s0.usable)
        T["S0_thinking_setting"] = T.alias.map(s0.extra_body).fillna("")
        T["S0_latency_s"] = T.alias.map(s0.latency_s)
    s1 = rd("S1_interface_probe", "summary.csv")
    if len(s1):
        s1 = s1.set_index("alias")
        T["S1_plan_parse"] = T.alias.map(s1.plan_parse_rate)
        T["S1_policy_nonfactual"] = T.alias.map(s1.policy_nonfactual_rate)
        T["S1_top_plan_mode"] = T.alias.map(s1.plan_top_mode)

    # ---- A1 anchor set
    a1 = rd("A1_audit_calibration", "evaluator_scores.csv")
    if len(a1):
        for role in ("auditor", "judge"):
            x = a1[a1.role == role].set_index("alias")
            T[f"A1_{role}_bal_acc"] = T.alias.map(x.balanced_acc)
            T[f"A1_{role}_valid"] = T.alias.map(x.valid_rate)
    # ---- A3 fixed bank
    a3 = rd("A3_fixed_bank", "auditor_vs_judge.csv")
    if len(a3):
        g = a3.groupby("auditor")[["tpr_blocks_violating", "fpr_honest_only"]].mean()
        T["A3_auditor_tpr"] = T.alias.map(g.tpr_blocks_violating)
        T["A3_auditor_fpr_honest"] = T.alias.map(g.fpr_honest_only)
    ja = rd("A3_fixed_bank", "judge_agreement.csv")
    if len(ja):
        k = pd.concat([ja[["judge_a", "kappa"]].rename(columns={"judge_a": "j"}),
                       ja[["judge_b", "kappa"]].rename(columns={"judge_b": "j"})]).groupby("j").kappa.mean()
        T["A3_judge_mean_kappa"] = T.alias.map(k)
    # ---- A8 fixed-text auditor screen
    a8 = rd("A8_auditor_scale", "auditor_scale.csv")
    if len(a8):
        a8 = a8.set_index("auditor")
        for c, n in [("tpr_judges", "A8_sensitivity"), ("fpr_judges", "A8_false_pos"), ("h1_sensitivity", "A8_H1_sensitivity"),
                     ("usd_per_1000_audits", "A8_usd_per_1000_audits"), ("median_latency_s", "A8_median_latency_s"),
                     ("eligible", "A8_eligible")]:
            T[n] = T.alias.map(a8[c])
    # ---- S5i closed loop (plain audit, eligible)
    s5 = elig(rd("S5i_role_factorial", "episodes.csv"))
    if len(s5):
        pa = s5[s5.governor == "audit"]
        T["S5i_ASR_as_auditor"] = T.alias.map(pa.groupby("auditor").asr_per_round.mean())
        T["S5i_misclass_as_auditor"] = T.alias.map(pa.groupby("auditor").audit_misclassification_rate.mean())
        T["S5i_ASR_as_attacker"] = T.alias.map(pa.groupby("attacker").asr_per_round.mean())
        mp = rd("S5i_role_factorial", "memory_penalty_by_auditor.csv")
        if len(mp):
            mp = mp.set_index("auditor")
            T["S5i_raw_memory_penalty"] = T.alias.map(
                mp.apply(lambda r: f"{r.delta:+.3f} [{r.lo:+.3f}, {r.hi:+.3f}]", axis=1))
    # ---- S3 population governance gap
    s3 = rd("S3_gcge_cross_model", "ecs_gap_by_model.csv")
    if len(s3):
        s3 = s3.set_index("alias")
        T["S3_ECS_gap"] = T.alias.map(s3.apply(lambda r: f"{r.ecs_gap:.3f} [{r.ecs_gap_lo:.3f}, {r.ecs_gap_hi:.3f}]", axis=1))
        T["S3_backlash_governed"] = T.alias.map(s3.backlash_gov)
    T.to_csv(OUT / "M1_model_evidence.csv", index=False)

    # ---- markdown: compact view + full csv
    def f(v, nd=3):
        if isinstance(v, float):
            return "" if v != v else f"{v:.{nd}f}"
        return "" if v is None else str(v)
    view = ["alias", "tier", "price_in_out_usd_per_M", "roles", "S0_latency_s", "A1_auditor_bal_acc", "A1_judge_bal_acc",
            "A3_auditor_tpr", "A3_auditor_fpr_honest", "A3_judge_mean_kappa", "A8_sensitivity", "A8_false_pos",
            "A8_usd_per_1000_audits", "S5i_ASR_as_auditor", "S5i_misclass_as_auditor", "S5i_ASR_as_attacker",
            "S5i_raw_memory_penalty", "S3_ECS_gap"]
    view = [c for c in view if c in T]
    lines = ["# M1: model evidence (RR_PLAN_v2, descriptive, no API calls)", "",
             "Every value is read from existing records; empty = not measured for that model. Prices: USD per 1M "
             "input/output tokens (roster). A1: 30-item anchor set. A3: fixed bank, auditor vs each other judge "
             "(mean). A8: fixed-text screen (judge-referenced sensitivity / false positives, cost per 1000 audits). "
             "S5i: plain-audit closed loop, means over eligible episodes (judge Kimi-K3). S3: governance gap in ECS "
             "with that population backbone [CI]. Full table with interface columns: `M1_model_evidence.csv`; "
             "roles per study: `M1_roles_by_study.csv`.", "",
             "| " + " | ".join(view) + " |", "|" + "|".join("---" for _ in view) + "|"]
    for r in T[view].itertuples(index=False):
        lines.append("| " + " | ".join(f(v) for v in r) + " |")
    (OUT / "M1_model_evidence.md").write_text("\n".join(lines) + "\n")
    print(f"M1 written: {len(T)} models -> {OUT / 'M1_model_evidence.md'}")
    return T


if __name__ == "__main__":
    main()
