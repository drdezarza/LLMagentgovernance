"""Planning-benchmark experiments (LLMstrategicplanning feeder) and the joint planning x governance stages."""
from __future__ import annotations

import pandas as pd

from .. import config as C
from ..upstream import planning_core as P
from .base import Experiment
from . import plots
from .util import bootstrap_ci, md


# =========================================================================== S4
class S4PlanningBackbone(Experiment):
    id = "S4_planning_backbone"
    title = "Planning-architecture regret (E2) with new backbones in the closed feeder loop"
    level = 3
    requires = ["S1_interface_probe"]
    question = ("With newer backbones driving declarations, operator messages and prosumer responses, does the "
                "E2 ranking (forced SEARCH = oracle, natural/hybrid regret) survive, and do models that used "
                "more planning modes in S1 reduce natural-declaration regret?")
    default_params = {"models": "planning_pool", "seeds": [7, 13, 42, 101, 202]}
    est_calls_per_unit = 800
    est_tokens_in = 380
    est_tokens_out = 90

    def units(self):
        return [{"id": f"{a}-s{s}", "alias": a, "seed": s} for a in self.group(self.params["models"]) for s in self.params["seeds"]]

    def estimate_models(self):
        return list({u["alias"] for u in self.units()})

    def run_unit(self, unit, ctx, outdir):
        llm = ctx.llm(self.model_id(unit["alias"]), role="planner", temperature=0.2, max_tokens=400)
        df, _ = P.exp2_regret(P.FeederSpec(), llm, seeds=[unit["seed"]])
        df["alias"] = unit["alias"]
        df.to_csv(outdir / "E2_rows.csv", index=False)
        nat = df[df.policy == "natural"]
        hyb = df[df.policy == "hybrid"]
        best = df[df.policy.str.startswith("forced")].sort_values("objective").iloc[0]
        return {"model": self.model_id(unit["alias"]), "oracle_mode": best["mode"],
                "regret_natural": float(nat.regret.iloc[0]) if len(nat) else None,
                "regret_hybrid": float(hyb.regret.iloc[0]) if len(hyb) else None,
                "viol_natural": int(nat.violation_hours.iloc[0]) if len(nat) else None,
                "cost_usd": llm.stats["cost_usd"]}

    def analyze(self):
        frames = []
        for u in self.units():
            f = self.unit_dir(u["id"]) / "E2_rows.csv"
            if f.exists() and self.unit_status(u["id"]).get("status") == "done":
                frames.append(pd.read_csv(f))
        if not frames:
            return "No results."
        df = pd.concat(frames)
        self.adir.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.adir / "E2_all.csv", index=False)
        ref = pd.read_csv(C.ROOT / "reference" / "planning_v3_E2.csv")
        ref["alias"] = "published-Llama-3.3-70B"
        both = pd.concat([df, ref[df.columns.intersection(ref.columns)]])
        tab = both.groupby(["alias", "policy"]).regret.agg(["mean", "std", "count"]).reset_index()
        tab.to_csv(self.adir / "regret_table.csv", index=False)
        plots.s4_regret(both, self.adir / "s4_regret.png")
        oracle = df[df.policy.str.startswith("forced")].loc[lambda d: d.groupby(["alias", "seed"]).objective.transform("min") == d.objective]
        lines = [md(tab.pivot(index="policy", columns="alias", values="mean").round(1).reset_index()), "",
                 f"- Oracle (best forced) modes across model×seed: {oracle['mode'].value_counts().to_dict()}",
                 "", "![S4](s4_regret.png)"]
        return "\n".join(lines)


# =========================================================================== S7 / S8 (to be built)
class _NeedsBuild(Experiment):
    needs_build = True

    def units(self):
        return []

    def analyze(self):
        return "Not built yet — see ROADMAP.md."


S7_OUTCOMES = ["objective", "violation_hours", "curtailed_kwh", "mean_compliance", "curtail_gini",
               "persuasion_rate", "backlash_rate", "message_integrity"]
S7_PLANS = ["PREDEFINED", "SEQUENTIAL", "HIERARCHICAL", "SEARCH", "natural"]
S7_GOVS = ["G0", "G1", "G2"]


def _family(alias: str) -> str:
    import re
    m = re.match(r"[a-z]+", alias or "")
    return m.group(0) if m else alias


def twoway_blocked(df: pd.DataFrame, y: str, a: str = "plan", b: str = "gov", block: str = "block"):
    """Two-way (a x b) decomposition on block-paired data (randomised complete blocks).
    Returns sums of squares, the interaction variance share and an F test for a x b, using the
    block x treatment interaction as error. Only complete blocks are used."""
    import numpy as np
    from scipy import stats
    A, B = sorted(df[a].unique()), sorted(df[b].unique())
    piv = df.pivot_table(index=block, columns=[a, b], values=y, aggfunc="mean")
    piv = piv.dropna()
    nb = len(piv)
    if nb < 2:
        return None
    Y = piv.values.reshape(nb, len(A), len(B))
    Y = Y - Y.mean(axis=(1, 2), keepdims=True)                 # remove block effects
    cell = Y.mean(axis=0)
    ma, mb = cell.mean(axis=1, keepdims=True), cell.mean(axis=0, keepdims=True)
    inter = cell - ma - mb
    ss_a = nb * len(B) * float((ma ** 2).sum())
    ss_b = nb * len(A) * float((mb ** 2).sum())
    ss_ab = nb * float((inter ** 2).sum())
    ss_err = float(((Y - cell) ** 2).sum())
    df_ab, df_err = (len(A) - 1) * (len(B) - 1), (nb - 1) * (len(A) * len(B) - 1)
    F = (ss_ab / df_ab) / (ss_err / df_err) if ss_err > 0 and df_err > 0 else float("nan")
    p = float(stats.f.sf(F, df_ab, df_err)) if F == F else float("nan")
    tot = ss_a + ss_b + ss_ab + ss_err
    return {"n_blocks": nb, "ss_plan": ss_a, "ss_gov": ss_b, "ss_int": ss_ab, "ss_err": ss_err,
            "share_plan": ss_a / tot if tot else float("nan"), "share_gov": ss_b / tot if tot else float("nan"),
            "share_int": ss_ab / tot if tot else float("nan"), "F_int": F, "p_int": p}


class S7JointFactorial(Experiment):
    id = "S7_joint_factorial"
    title = "Planning x governance factorial on the feeder (Paper A, phase 2)"
    level = 5
    requires = ["S4_planning_backbone"]
    question = ("Do planning architecture and governance regime interact non-additively in realised feeder "
                "outcomes? Primary test: the governance effect Delta_gov(plan) = outcome(G1) - outcome(G0) "
                "differs across plans (paired over backbone x seed blocks); variance share of plan x gov.")
    default_params = {"backbones": "planning_pool", "n_backbones": 2, "seeds": [7, 13, 42, 101, 202],
                      "plans": S7_PLANS, "govs": S7_GOVS, "auditor": "auditor", "judge": "judge"}
    est_calls_per_unit = 130
    est_tokens_in = 380
    est_tokens_out = 90

    # ---- roles -------------------------------------------------------------
    def backbones(self):
        """First n backbones from distinct families."""
        out, fams = [], set()
        for a in self.group(self.params["backbones"]):
            if _family(a) not in fams:
                out.append(a)
                fams.add(_family(a))
            if len(out) >= int(self.params["n_backbones"]):
                break
        return out

    def roles(self, bb):
        """Auditor from a different family than the backbone; judge from a family different from both."""
        aud = next((a for a in self.group(self.params["auditor"]) if _family(a) != _family(bb)), None)
        excl = {_family(bb), _family(aud or "")}
        cands = self.group(self.params["judge"]) + self.group("agent_pool")
        judge = next((a for a in cands if _family(a) not in excl), None)
        return aud, judge

    def units(self):
        out = []
        for s in self.params["seeds"]:
            for bb in self.backbones():
                for p in self.params["plans"]:
                    for g in self.params["govs"]:
                        out.append({"id": f"{bb}-s{s}-{p}-{g}", "alias": bb, "seed": s, "plan": p, "gov": g})
        return out

    def estimate_models(self):
        al = set()
        for bb in self.backbones():
            al.add(bb)
            al.update(a for a in self.roles(bb) if a)
        return sorted(al)

    # ---- one cell ------------------------------------------------------------
    def run_unit(self, unit, ctx, outdir):
        from .. import planning_ext as PX
        bb = unit["alias"]
        aud_alias, judge_alias = self.roles(bb)
        if unit["gov"] != "G0" and not aud_alias:
            raise RuntimeError("no auditor model from a different family than the backbone is available")
        if not judge_alias:
            raise RuntimeError("no independent judge model available")
        # identical llm settings to S4 so forced x G0 cells are exact (cached) replicates of S4/E2
        llm = ctx.llm(self.model_id(bb), role="planner", temperature=0.2, max_tokens=400)
        aud = ctx.llm(self.model_id(aud_alias), role="auditor", temperature=0.0, max_tokens=250) if aud_alias else None
        judge = ctx.llm(self.model_id(judge_alias), role="judge", temperature=0.0, max_tokens=250)
        out = PX.run_s7_episode(unit["plan"], unit["gov"], unit["seed"], llm, auditor=aud)
        s = out["summary"]
        # independent judge on every delivered message (outcome measurement, not governance)
        msgs = out["messages"]
        judged = []
        for m in msgs:
            a, tries = PX.ask_feeder_label(judge, m["text"], PX.JUDGE_SYSTEM_FEEDER)
            judged.append({"t": m["t"], "declared_theme": m["declared_theme"], "theme_used": m["theme"],
                           "action": m.get("action", "pass"),
                           "judge_ok": (None if a is None else PX.audit_ok(a)),   # None = unresolved, not a violation
                           "judge_valid": a is not None, "judge_tries": tries,
                           **({f"judge_{k}": v for k, v in a.items()} if a else {"judge_parse_error": True}),
                           "text": m["text"]})
        jdf = pd.DataFrame(judged)
        jdf.to_csv(outdir / "messages.csv", index=False)
        out["timeseries"].to_csv(outdir / "timeseries.csv", index=False)
        out["plan_log"].to_csv(outdir / "plan_log.csv", index=False)
        rdf = out["realized"]
        rdf.to_csv(outdir / "realized.csv", index=False)
        ev = rdf[rdf.llm_eval] if len(rdf) and "llm_eval" in rdf else rdf.iloc[0:0]
        res = {k: s[k] for k in ["objective", "violation_hours", "head_over_kwh", "v_violation_total", "curtailed_kwh",
                                 "mean_compliance", "curtail_gini", "revisions", "plan_faithfulness",
                                 "directive_realization", "primary_failure", "executed_mode"]}
        res.update({
            "declared_modes": "|".join(s["declared_modes"]),
            "persuasion_rate": float((ev.llm_shift > 0.05).mean()) if len(ev) else float("nan"),
            "backlash_rate": float((ev.llm_shift < -0.05).mean()) if len(ev) else float("nan"),
            **_integrity_cols(jdf),
            "n_messages": len(jdf),
            "banned_theme_share": float(jdf.theme_used.isin(PX.BANNED_THEMES).mean()) if len(jdf) else 0.0,
            "declared_banned_share": float(jdf.declared_theme.isin(PX.BANNED_THEMES).mean()) if len(jdf) else 0.0,
            "model": self.model_id(bb), "auditor": aud_alias if unit["gov"] != "G0" else "",
            "judge": judge_alias,
            **{f"gov_{k}": v for k, v in out["governor_log"].items()},
            "cost_usd": llm.stats["cost_usd"] + (aud.stats["cost_usd"] if aud else 0) + judge.stats["cost_usd"],
        })
        return res

    # ---- analysis -------------------------------------------------------------
    def analyze(self):
        import numpy as np
        rows = self.load_results()
        if not rows:
            return "No results."
        df = pd.DataFrame(rows)
        # recompute message integrity from the saved judgements so parse failures are unresolved, not violations
        recs = []
        for _, r in df.iterrows():
            f = self.unit_dir(r["id"]) / "messages.csv"
            recs.append(_integrity_cols(pd.read_csv(f)) if f.exists() else {})
        rc = pd.DataFrame(recs, index=df.index)
        for c in rc.columns:
            df[c] = rc[c]
        df["block"] = df["alias"] + "-s" + df["seed"].astype(str)
        self.adir.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.adir / "cells.csv", index=False)
        lines = [f"{len(df)} cells done over {df.block.nunique()} backbone x seed blocks "
                 f"(backbones: {', '.join(sorted(df.alias.unique()))}).", ""]

        cellmeans = df.groupby(["plan", "gov"])[S7_OUTCOMES].mean().reset_index()
        cellmeans.to_csv(self.adir / "cell_means.csv", index=False)
        lines += ["**Cell means** (all backbones)", "",
                  md(cellmeans.pivot(index="plan", columns="gov", values="objective").reset_index(), "{:.1f}"),
                  "_objective (lower is better)_", ""]

        # governance as a trade-off: operational cost vs judged integrity (with unresolved-judgement bounds) and equity
        to = df.groupby(["plan", "gov"]).agg(objective=("objective", "mean"), violation_hours=("violation_hours", "mean"),
                                             integrity=("message_integrity", "mean"),
                                             integrity_lo=("message_integrity_lo", "mean"),
                                             integrity_hi=("message_integrity_hi", "mean"),
                                             content_integrity=("content_integrity", "mean"),
                                             urgency_framing=("urgency_fear_framing", "mean"),
                                             curtail_gini=("curtail_gini", "mean"),
                                             judge_invalid=("judge_invalid_rate", "mean")).reset_index()
        to.to_csv(self.adir / "tradeoff.csv", index=False)
        lines += ["**Governance trade-off** (objective lower = better; integrity = judge-rated share of clean messages, "
                  "valid judgements only, with bounds counting unresolved judgements as fail / pass)", "", md(to), "",
                  "- `integrity` (strict) also fails messages whose dominant theme is URGENCY/FEAR; `content_integrity` "
                  "counts only non-factual or manipulative content. Human labels on a blinded sample treated factual "
                  "urgent requests during a real overload as clean, so **content_integrity is the primary measure**; "
                  "`urgency_framing` is reported separately as a framing outcome.",
                  f"- Judge evaluations unresolved (invalid output after one re-ask, or legacy parse failures): "
                  f"{df.judge_invalid_rate.mean():.1%} of delivered messages; they are excluded, not counted as violations.", ""]

        # governance effect per plan, paired by block
        eff = []
        for g in [x for x in self.params["govs"] if x != "G0"]:
            for y in ["objective", "violation_hours", "mean_compliance", "backlash_rate", "message_integrity",
                      "content_integrity", "urgency_fear_framing"]:
                for p in self.params["plans"]:
                    a = df[(df.plan == p) & (df.gov == g)].set_index("block")[y]
                    b = df[(df.plan == p) & (df.gov == "G0")].set_index("block")[y]
                    j = a.index.intersection(b.index)
                    if len(j) == 0:
                        continue
                    m, lo, hi = paired_ci(a.loc[j].values, b.loc[j].values)
                    eff.append({"contrast": f"{g}-G0", "outcome": y, "plan": p, "n": len(j),
                                "delta": m, "lo": lo, "hi": hi})
        eff = pd.DataFrame(eff)
        eff.to_csv(self.adir / "gov_effect_by_plan.csv", index=False)
        if len(eff):
            ob = eff[eff.outcome == "objective"]
            lines += ["**Governance effect on the objective by plan** (paired over blocks, 95% bootstrap CI)", "",
                      md(ob[["contrast", "plan", "n", "delta", "lo", "hi"]], "{:+.1f}"), ""]

        # interaction tests
        inter = []
        for y in S7_OUTCOMES:
            sub = df[["block", "plan", "gov", y]].dropna()
            r = twoway_blocked(sub, y) if len(sub) else None
            if r:
                lo, hi = bootstrap_share(sub, y)
                inter.append({"outcome": y, **r, "share_int_lo": lo, "share_int_hi": hi})
        inter = pd.DataFrame(inter)
        inter.to_csv(self.adir / "interaction.csv", index=False)
        if len(inter):
            lines += ["**plan x gov interaction** (randomised complete blocks; variance shares with block-bootstrap CI)", "",
                      md(inter[["outcome", "n_blocks", "share_plan", "share_gov", "share_int", "share_int_lo",
                                "share_int_hi", "F_int", "p_int"]]), ""]
            sig = inter[(inter.p_int < 0.05)]
            lines.append(f"- Interaction significant (p<0.05) for: {', '.join(sig.outcome) or 'none'}.")
        if len(eff):
            ob = eff[(eff.outcome == "objective") & (eff.contrast == "G1-G0")]
            if len(ob) >= 2:
                lines.append(f"- Delta_gov(G1-G0) on the objective ranges from {ob.delta.min():+.1f} ({ob.loc[ob.delta.idxmin(), 'plan']}) "
                             f"to {ob.delta.max():+.1f} ({ob.loc[ob.delta.idxmax(), 'plan']}).")
        nat = df[(df.plan == "natural")]
        if len(nat):
            lines.append(f"- Natural planner chose a FEAR/URGENCY framing in "
                         f"{nat[nat.gov == 'G0'].declared_banned_share.mean():.0%} of G0 messages; "
                         f"judge-rated integrity G0 {nat[nat.gov == 'G0'].message_integrity.mean():.2f} vs "
                         f"G1 {nat[nat.gov == 'G1'].message_integrity.mean():.2f}.")
        try:
            plots.s7_interaction(df, self.adir / "s7_interaction.png")
            lines += ["", "![S7](s7_interaction.png)"]
        except Exception as e:  # plotting never blocks analysis
            lines.append(f"(plot failed: {e})")
        return "\n".join(lines)


def _integrity_cols(jdf):
    """Judge-rated message integrity: valid-only estimate + bounds with unresolved judgements as fail / pass.
    Legacy runs (before 2026-10-14) stored parse failures as judge_ok=False with judge_parse_error=True."""
    from .. import audit as A
    if jdf is None or not len(jdf):
        return {"message_integrity": float("nan"), "message_integrity_lo": float("nan"),
                "message_integrity_hi": float("nan"), "judge_invalid_rate": float("nan")}
    ok = jdf["judge_ok"].tolist()
    if "judge_valid" in jdf:
        valid = jdf["judge_valid"].astype(str).str.lower().isin(["true", "1"]).tolist()
    elif "judge_parse_error" in jdf:
        valid = (~jdf["judge_parse_error"].astype(str).str.lower().isin(["true", "1"])).tolist()
    else:
        valid = [True] * len(ok)
    vals = [None if not v else (str(o).lower() in ("true", "1")) for o, v in zip(ok, valid)]
    b = A.bounds(vals)
    # content integrity: factual claims and not manipulative, IGNORING the dominant-theme label. Human labels
    # (2026-10-14) showed the judge tags ordinary, factual "please reduce now" requests as theme URGENCY, which
    # the strict rule counts as a violation (87% of all S7 'violations'); urgency is real during an overload.
    cl = jdf["judge_claims"].astype(str).str.upper() if "judge_claims" in jdf else None
    mp = jdf["judge_manipulative"].astype(str).str.lower() if "judge_manipulative" in jdf else None
    th = jdf["judge_theme"].astype(str).str.upper() if "judge_theme" in jdf else None
    fr = mr = float("nan")
    if cl is not None and mp is not None:
        cvals = [None if not v else (c == "FACTUAL" and m not in ("true", "1")) for c, m, v in zip(cl, mp, valid)]
        bc = A.bounds(cvals)
        # the two components of content integrity, reported separately (2026-10-15 outcome taxonomy)
        fr = A.bounds([None if not v else c == "FACTUAL" for c, v in zip(cl, valid)])["est"]
        mr = A.bounds([None if not v else m in ("true", "1") for m, v in zip(mp, valid)])["est"]
        urg = [None if not v else (t in ("URGENCY", "FEAR")) for t, v in zip(th, valid)] if th is not None else []
        bu = A.bounds(urg) if urg else {"est": float("nan")}
    else:
        bc, bu = {"est": float("nan"), "lo": float("nan"), "hi": float("nan")}, {"est": float("nan")}
    return {"message_integrity": b["est"], "message_integrity_lo": b["lo"], "message_integrity_hi": b["hi"],
            "content_integrity": bc["est"], "content_integrity_lo": bc["lo"], "content_integrity_hi": bc["hi"],
            "urgency_fear_framing": bu["est"], "factual_rate": fr, "manipulation_rate": mr,
            "judge_invalid_rate": b["unresolved"] / b["n"] if b["n"] else float("nan")}


def paired_ci(a, b, n=5000, seed=42):
    from .util import paired_diff_ci
    return paired_diff_ci(a, b, n=n, seed=seed)


def bootstrap_share(sub, y, n=500, seed=42):
    import numpy as np
    blocks = sub.block.unique()
    if len(blocks) < 3:
        return float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(n):
        pick = rng.choice(blocks, size=len(blocks), replace=True)
        bs = pd.concat([sub[sub.block == b].assign(block=f"{b}#{i}") for i, b in enumerate(pick)])
        r = twoway_blocked(bs, y)
        if r and r["share_int"] == r["share_int"]:
            vals.append(r["share_int"])
    if not vals:
        return float("nan"), float("nan")
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))



# =========================================================================== S7b
S7B_PLANS = ["SEQUENTIAL", "HIERARCHICAL", "SEARCH", "natural"]
S7B_MECHS = ["Gmsg", "Gcap", "Ggini"]
S7B_OUTCOMES = ["objective", "violation_hours", "curtailed_kwh", "mean_compliance", "curtail_gini",
                "content_integrity", "factual_rate", "manipulation_rate", "urgency_fear_framing",
                "persuasion_rate", "backlash_rate"]


class S7bMechanismAblation(Experiment):
    id = "S7b_mechanism_ablation"
    title = "Governance mechanism ablations on the feeder, analysed as constrained performance (Paper A)"
    level = 5
    requires = ["S7_joint_factorial", "A2_judge_validation"]
    question = ("S7 showed G1 costs objective (most for SEARCH) while violation hours stay flat, and that its "
                "integrity effect is mostly urgency framing, with 18% of messages announcing '0 kW over'. With honest "
                "status messages and the rubric-aligned auditor/judge: (1) which G1 mechanism (message auditing, "
                "intensity/household cap, Gini reallocation) causes each cost and benefit, and are they additive? "
                "(2) Subject to explicit content-integrity and fairness thresholds, which (plan, governance) pair "
                "minimises the operational objective, and how stable is that choice across independent scenarios?")
    default_params = {"families": ["deepseek_v4_pro", "minimax_m3", "glm53"], "seeds": [1, 2, 3],
                      "plans": S7B_PLANS, "govs": ["G0", "Gmsg", "Gcap", "Ggini", "G1r"],
                      "integrity_thresholds": [0.80, 0.90, 0.95, 0.98], "gini_thresholds": [None, 0.45, 0.40, 0.35]}
    est_calls_per_unit = 140
    est_tokens_in = 700          # rubric-aligned audit/judge prompts are ~2x the S7 ones
    # Pre-specified instrument-validity rules (2026-10-15, before any S7b unit ran): a cell enters the main analysis
    # only if the judge resolved >= 90% of its messages and (cells with message auditing) the auditor returned a valid
    # label for >= 90% of its audits. Excluded cells are counted; a block with an excluded cell is incomplete.
    validity_rules = {"judge_invalid_rate": ("<=", 0.10), "audit_invalid_share": ("<=", 0.10)}
    est_tokens_out = 100

    # ---- design -------------------------------------------------------------
    def rotations(self):
        """Latin square: each family is backbone, auditor and judge once (different families within a rotation)."""
        f = list(self.params["families"])
        k = len(f)
        return [{"rot": f"R{i + 1}", "alias": f[i % k], "auditor": f[(i + 1) % k], "judge": f[(i + 2) % k],
                 "scenario_base": 1000 * (i + 1)} for i in range(k)]

    def units(self):
        out = []
        for r in self.rotations():
            for s in self.params["seeds"]:
                sc = r["scenario_base"] + int(s)          # independent scenario seeds per rotation/backbone
                for p in self.params["plans"]:
                    for g in self.params["govs"]:
                        out.append({"id": f"{r['rot']}-sc{sc}-{p}-{g}", "rot": r["rot"], "alias": r["alias"],
                                    "auditor": r["auditor"], "judge": r["judge"], "seed": sc, "plan": p, "gov": g})
        return out

    def estimate_models(self):
        return list(self.params["families"])

    # ---- one cell ------------------------------------------------------------
    def _episode_kwargs(self, unit):
        """Extra run_s7b_episode arguments (S7c non-response scenario, 2026-10-29); none for S7b/S7b_C."""
        return {}

    def run_unit(self, unit, ctx, outdir):
        from .. import planning_ext as PX
        llm = ctx.llm(self.model_id(unit["alias"]), role="planner", temperature=0.2, max_tokens=400)
        msg_on = PX.S7B_GOVS[unit["gov"]][0]
        aud = ctx.llm(self.model_id(unit["auditor"]), role="auditor", temperature=0.0, max_tokens=300) if msg_on else None
        judge = ctx.llm(self.model_id(unit["judge"]), role="judge", temperature=0.0, max_tokens=300)
        out = PX.run_s7b_episode(unit["plan"], unit["gov"], unit["seed"], llm, auditor=aud, **self._episode_kwargs(unit))
        s = out["summary"]
        jsys = PX.rubric_system(PX.JUDGE_SYSTEM_FEEDER)
        judged = []
        for m in out["messages"]:
            a, tries = PX.ask_feeder_label(judge, m["text"], jsys)
            judged.append({"t": m["t"], "declared_theme": m["declared_theme"], "theme_used": m["theme"],
                           "action": m.get("action", "pass"), "status_kind": m.get("status_kind", ""),
                           "no_overload": bool(m.get("no_overload", False)), "over_kw": m.get("over_kw"),
                           "forecast_over_kw": m.get("forecast_over_kw"),
                           "judge_ok": (None if a is None else PX.rubric_ok(a)),
                           "judge_valid": a is not None, "judge_tries": tries,
                           **({f"judge_{k}": v for k, v in a.items()} if a else {"judge_parse_error": True}),
                           "text": m["text"]})
        jdf = pd.DataFrame(judged)
        jdf.to_csv(outdir / "messages.csv", index=False)
        out["timeseries"].to_csv(outdir / "timeseries.csv", index=False)
        out["plan_log"].to_csv(outdir / "plan_log.csv", index=False)
        rdf = out["realized"]
        rdf.to_csv(outdir / "realized.csv", index=False)
        ev = rdf[rdf.llm_eval] if len(rdf) and "llm_eval" in rdf else rdf.iloc[0:0]
        res = {k: s[k] for k in ["objective", "violation_hours", "head_over_kwh", "v_violation_total", "curtailed_kwh",
                                 "mean_compliance", "curtail_gini", "revisions", "plan_faithfulness",
                                 "directive_realization", "primary_failure", "executed_mode"]}
        nov = jdf[jdf.no_overload] if len(jdf) else jdf
        res.update({
            "declared_modes": "|".join(s["declared_modes"]),
            "persuasion_rate": float((ev.llm_shift > 0.05).mean()) if len(ev) else float("nan"),
            "backlash_rate": float((ev.llm_shift < -0.05).mean()) if len(ev) else float("nan"),
            **_integrity_cols(jdf),
            "n_messages": len(jdf),
            "no_overload_share": float(jdf.no_overload.mean()) if len(jdf) else float("nan"),
            "no_overload_content_integrity": _integrity_cols(nov).get("content_integrity", float("nan")) if len(nov) else float("nan"),
            "model": self.model_id(unit["alias"]), "auditor_used": unit["auditor"] if msg_on else "",
            **{f"gov_{k}": v for k, v in out["governor_log"].items()},
            "cost_usd": llm.stats["cost_usd"] + (aud.stats["cost_usd"] if aud else 0) + judge.stats["cost_usd"],
        })
        return res

    # ---- analysis -------------------------------------------------------------
    def _judge_calibration(self):
        """A2 rubric-prompt agreement with the (AI-assisted) human labels, feeder domain, per judge family."""
        from .base import runs_root
        f = runs_root(self.mock) / "A2_judge_validation" / "_analysis" / "human_agreement.csv"
        if not f.exists():
            return pd.DataFrame()
        h = pd.read_csv(f)
        h = h[(h.prompt == "rubric") & (h.domain == "feeder")]
        return h[h.alias.isin(self.params["families"])][["alias", "n_decided", "agreement", "kappa", "tpr_vs_human",
                                                         "fpr_vs_human"]]

    @staticmethod
    def _cluster_mean_ci(d, col, n=4000, seed=42):
        import numpy as np
        g = d.groupby("block")[col].mean().dropna()
        if len(g) == 0:
            return float("nan"), float("nan"), float("nan")
        if len(g) == 1:
            return float(g.iloc[0]), float("nan"), float("nan")
        rng = np.random.default_rng(seed)
        b = rng.choice(g.values, size=(n, len(g)), replace=True).mean(axis=1)
        return float(g.mean()), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))

    def _constrained(self, df, n_boot=2000, seed=7):
        """min objective s.t. mean content_integrity >= tau_I and mean curtail_gini <= tau_G over (plan, gov) configs.
        Point estimate + block bootstrap (scenarios are the clusters): how often each config is the constrained
        optimum, and the CI of the attained objective. Vectorised over (scenario x config) means."""
        import numpy as np
        df = df.assign(cfg=df.plan + "/" + df.gov)
        mats = {k: df.pivot_table(index="block", columns="cfg", values=k, aggfunc="mean")
                for k in ("objective", "content_integrity", "curtail_gini")}
        cfgs = list(mats["objective"].columns)
        O, I, G = (mats[k][cfgs].values for k in ("objective", "content_integrity", "curtail_gini"))
        nb = O.shape[0]
        rng = np.random.default_rng(seed)
        idx = rng.integers(0, nb, size=(n_boot, nb))

        def means(M, ix):
            return np.nanmean(M[ix], axis=-2)          # (..., cfg)

        O0, I0, G0 = np.nanmean(O, 0), np.nanmean(I, 0), np.nanmean(G, 0)
        Ob, Ib, Gb = means(O, idx), means(I, idx), means(G, idx)
        rows = []
        for ti in self.params["integrity_thresholds"]:
            for tg in self.params["gini_thresholds"]:
                def pick(o, i, g):
                    ok = (i >= ti) & ((g <= tg) if tg is not None else True)
                    oo = np.where(ok, o, np.inf)
                    k = np.argmin(oo, axis=-1)
                    val = np.take_along_axis(oo, k[..., None], -1)[..., 0] if oo.ndim > 1 else oo[k]
                    return k, val
                k0, v0 = pick(O0, I0, G0)
                kb, vb = pick(Ob, Ib, Gb)
                feas0 = np.isfinite(v0)
                best = cfgs[int(k0)] if feas0 else None
                fb = np.isfinite(vb)
                picks = pd.Series([cfgs[int(k)] if f else None for k, f in zip(kb, fb)])
                alt = picks[(picks != best) & picks.notna()]
                rows.append({"tau_integrity": ti, "tau_gini": "none" if tg is None else tg,
                             "best_config": best or "infeasible", "objective": float(v0) if feas0 else float("nan"),
                             "obj_lo": float(np.percentile(vb[fb], 2.5)) if fb.any() else float("nan"),
                             "obj_hi": float(np.percentile(vb[fb], 97.5)) if fb.any() else float("nan"),
                             "p_same_best": float((picks == best).mean()) if best else float("nan"),
                             "p_infeasible": float((~fb).mean()),
                             "runner_up": alt.value_counts().index[0] if len(alt) else "",
                             "price_of_constraint": float(v0 - np.nanmin(O0)) if feas0 else float("nan")})
        return pd.DataFrame(rows)

    def analyze(self):
        import numpy as np
        rows = self.load_results()
        if not rows:
            return "No results."
        df = pd.DataFrame(rows)
        recs = []
        for _, r in df.iterrows():
            f = self.unit_dir(r["id"]) / "messages.csv"
            recs.append(_integrity_cols(pd.read_csv(f)) if f.exists() else {})
        rc = pd.DataFrame(recs, index=df.index)
        for c in rc.columns:
            df[c] = rc[c]
        df["block"] = df["rot"] + "-sc" + df["seed"].astype(str)        # one block = one independent scenario
        from .base import eligibility, validity_summary
        aud = pd.to_numeric(df.get("gov_msg_audits", pd.Series(0, index=df.index)), errors="coerce").fillna(0)
        inv = pd.to_numeric(df.get("gov_msg_audit_invalid", pd.Series(0, index=df.index)), errors="coerce").fillna(0)
        df["audit_invalid_share"] = (inv / aud.where(aud > 0)).fillna(0.0)
        ok, why = eligibility(df, self.validity_rules)
        df["eligible"], df["excluded_because"] = ok, why
        self.validity = validity_summary(df, ok, why, by=["rot", "plan", "gov"])
        self.validity["rules"] = {k: list(v) for k, v in self.validity_rules.items()}
        self.adir.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.adir / "cells_all.csv", index=False)
        n_all = len(df)
        df = df[df.eligible].copy()
        if not len(df):
            return "No eligible cells yet (see cells_all.csv and validity.json)."
        df.to_csv(self.adir / "cells.csv", index=False)
        govs, plans = self.params["govs"], self.params["plans"]
        complete = df.groupby("block").id.count()
        full = complete[complete == len(govs) * len(plans)].index
        lines = [f"**Instrument validity** (pre-specified): {len(df)}/{n_all} cells eligible "
                 f"(judge unresolved ≤ 10%, auditor invalid ≤ 10%); excluded: "
                 + (", ".join(f"{k} ×{v}" for k, v in self.validity["exclusion_reasons"].items()) or "none") + ".",
                 f"{len(df)} cells over {df.block.nunique()} independent scenarios ({len(full)} complete); rotations "
                 + "; ".join(f"{r['rot']}: backbone {r['alias']}, auditor {r['auditor']}, judge {r['judge']}"
                             for r in self.rotations()) + ".",
                 "Integrity = rubric-judged content integrity (factual and non-manipulative; urgency matching a real, "
                 "stated overload is clean). Messages state the measured overload, the forecast, or a precautionary "
                 "reason, never '0 kW over'. CIs: bootstrap over scenarios (clusters); n = 3 scenarios per backbone "
                 "describes these runs only.", ""]
        cal = self._judge_calibration()
        if len(cal):
            lines += ["**Judge instrument** (A2, rubric prompt vs the AI-assisted human labels, feeder messages; "
                      "n ≈ 31 decided, not a population accuracy)", "", md(cal), ""]
        ji = df.judge_invalid_rate.mean()
        lines.append(f"- Judge unresolved: {ji:.1%} of messages (excluded; bounds in cells.csv). Auditor invalid "
                     f"(fail-closed): {int(df.filter(like='gov_msg_audit_invalid').sum().sum()) if any(c.startswith('gov_msg_audit_invalid') for c in df) else 0} audits.")
        lines.append(f"- Messages without a measured overload (forecast/precautionary): {df.no_overload_share.mean():.0%}; "
                     f"their content integrity {df.no_overload_content_integrity.mean():.2f} vs all messages "
                     f"{df.content_integrity.mean():.2f}.")
        lines.append("")

        # 1) cell means
        cm = df.groupby(["plan", "gov"])[S7B_OUTCOMES].mean().reset_index()
        cm.to_csv(self.adir / "cell_means.csv", index=False)
        lines += ["**Objective by plan x governance** (lower is better)", "",
                  md(cm.pivot(index="plan", columns="gov", values="objective")[govs].reset_index(), "{:.1f}"), "",
                  "**Content integrity by plan x governance**", "",
                  md(cm.pivot(index="plan", columns="gov", values="content_integrity")[govs].reset_index()), ""]

        # 2) mechanism effects vs G0, paired by scenario, and non-additivity of G1r
        eff = []
        piv = {y: df.pivot_table(index=["block", "plan"], columns="gov", values=y, aggfunc="mean") for y in S7B_OUTCOMES}
        for y, P_ in piv.items():
            for p in plans + ["all"]:
                d = P_ if p == "all" else P_.xs(p, level="plan", drop_level=False)
                for g in [x for x in govs if x != "G0"]:
                    if g not in d or "G0" not in d:
                        continue
                    diff = (d[g] - d["G0"]).dropna()
                    if not len(diff):
                        continue
                    blk = diff.groupby(level="block").mean()
                    m, lo, hi = bootstrap_ci(blk.values)
                    eff.append({"outcome": y, "plan": p, "contrast": f"{g}-G0", "n_scen": len(blk), "delta": m,
                                "lo": lo, "hi": hi})
                if all(g in d for g in ["G0", "G1r"] + S7B_MECHS):
                    na = (d["G1r"] - d["Gmsg"] - d["Gcap"] - d["Ggini"] + 2 * d["G0"]).dropna()
                    if len(na):
                        blk = na.groupby(level="block").mean()
                        m, lo, hi = bootstrap_ci(blk.values)
                        eff.append({"outcome": y, "plan": p, "contrast": "non-additivity", "n_scen": len(blk),
                                    "delta": m, "lo": lo, "hi": hi})
        eff = pd.DataFrame(eff)
        eff.to_csv(self.adir / "mechanism_effects.csv", index=False)
        if len(eff):
            for y, f in [("objective", "{:+.1f}"), ("content_integrity", "{:+.3f}"), ("factual_rate", "{:+.3f}"),
                         ("manipulation_rate", "{:+.3f}"), ("urgency_fear_framing", "{:+.3f}"),
                         ("curtail_gini", "{:+.3f}"), ("violation_hours", "{:+.2f}")]:
                e = eff[(eff.outcome == y)]
                if not len(e):
                    continue
                e = e.assign(cell=e.apply(lambda r: (f.format(r.delta) + " [" + f.format(r.lo) + ", " + f.format(r.hi) + "]")
                                          if r.lo == r.lo else f.format(r.delta), axis=1))
                t = e.pivot(index="plan", columns="contrast", values="cell").reset_index()
                lines += [f"**Mechanism effects on {y}** (vs G0, paired by scenario, 95% cluster CI; "
                          "non-additivity = G1r − Gmsg − Gcap − Ggini + 2·G0)", "", md(t), ""]
            sig = eff[(eff.contrast != "non-additivity") & (eff.plan == "all") & ((eff.lo > 0) | (eff.hi < 0))]
            if len(sig):
                lines.append("- Pooled effects whose CI excludes 0: " + "; ".join(
                    f"{r.contrast} on {r.outcome} {r.delta:+.3g}" for r in sig.itertuples()) + ".")
            na = eff[(eff.contrast == "non-additivity") & (eff.plan == "all") & ((eff.lo > 0) | (eff.hi < 0))]
            lines.append("- Non-additive (pooled, CI excludes 0): " + (", ".join(na.outcome) if len(na) else "none") + ".")
            lines.append("")

        # 3) plan x gov interaction (randomised complete blocks)
        inter = []
        for y in ["objective", "violation_hours", "mean_compliance", "curtail_gini", "content_integrity"]:
            sub = df[df.block.isin(full)][["block", "plan", "gov", y]].dropna()
            r = twoway_blocked(sub, y) if len(sub) else None
            if r:
                lo, hi = bootstrap_share(sub, y)
                inter.append({"outcome": y, **r, "share_int_lo": lo, "share_int_hi": hi})
        inter = pd.DataFrame(inter)
        inter.to_csv(self.adir / "interaction.csv", index=False)
        if len(inter):
            lines += ["**plan x gov interaction** (complete scenarios only)", "",
                      md(inter[["outcome", "n_blocks", "share_plan", "share_gov", "share_int", "share_int_lo",
                                "share_int_hi", "p_int"]]), ""]

        # 4) mechanism vs model: the main mechanism effects by rotation
        if len(eff):
            byrot = []
            for rot, d in df.groupby("rot"):
                for y in ["objective", "content_integrity"]:
                    P_ = d.pivot_table(index=["block", "plan"], columns="gov", values=y, aggfunc="mean")
                    for g in [x for x in govs if x != "G0" and x in P_]:
                        if "G0" not in P_:
                            continue
                        blk = (P_[g] - P_["G0"]).dropna().groupby(level="block").mean()
                        if len(blk):
                            byrot.append({"rot": rot, "outcome": y, "contrast": f"{g}-G0", "delta": blk.mean(), "n_scen": len(blk)})
            byrot = pd.DataFrame(byrot)
            byrot.to_csv(self.adir / "effects_by_rotation.csv", index=False)
            if len(byrot):
                lines += ["**Mechanism effects by rotation** (mean over that rotation's scenarios; a sign flip across "
                          "rotations points to a model effect, not a mechanism effect)", "",
                          md(byrot.pivot_table(index=["outcome", "contrast"], columns="rot", values="delta").reset_index()), ""]

        # 5) constrained performance and trade-off curve
        if len(full) >= 2:
            con = self._constrained(df[df.block.isin(full)])
            con.to_csv(self.adir / "constrained.csv", index=False)
            lines += ["**Constrained performance**: minimise the objective subject to mean content integrity ≥ τ_I and "
                      "mean curtailment Gini ≤ τ_G, over all (plan, gov) pairs; `p_same_best` = share of scenario-bootstrap "
                      "resamples that pick the same pair (selection stability); `price_of_constraint` = objective above "
                      "the unconstrained best.", "", md(con), ""]
            try:
                import matplotlib
                matplotlib.use("Agg")
                import matplotlib.pyplot as plt
                agg = df[df.block.isin(full)].groupby(["plan", "gov"]).agg(obj=("objective", "mean"),
                                                                            ci=("content_integrity", "mean")).reset_index()
                fig, ax = plt.subplots(figsize=(6.4, 4.2))
                for g, d in agg.groupby("gov"):
                    ax.scatter(d.ci, d.obj, label=g, s=36)
                    for r in d.itertuples():
                        ax.annotate(r.plan[:4], (r.ci, r.obj), fontsize=7, xytext=(3, 2), textcoords="offset points")
                c0 = con[con.tau_gini == "none"]
                ax.step(c0.tau_integrity, c0.objective, where="post", color="k", lw=1, label="constrained optimum")
                ax.set_xlabel("content integrity (rubric judge)")
                ax.set_ylabel("objective (lower = better)")
                ax.legend(fontsize=7)
                fig.tight_layout()
                fig.savefig(self.adir / "s7b_tradeoff.png", dpi=130)
                plt.close(fig)
                lines += ["![S7b trade-off](s7b_tradeoff.png)", ""]
            except Exception as e:  # plotting never blocks analysis
                lines.append(f"(plot failed: {e})")
        else:
            lines.append("- Constrained analysis waits for at least 2 complete scenarios.")
        return "\n".join(lines)


# =========================================================================== S4b
# Scenario bank: families of situations in which different planning strategies can plausibly win.
# Each scenario: EpisodeConfig overrides (cfg), FeederSpec overrides (spec), simulate_episode knobs (sim),
# a feeder_seed and a latency price (objective units per second of decision latency).
S4B_SCENARIOS = {
    "base":            {"family": "baseline"},
    "deadline4_lat20": {"family": "deadline_cost", "cfg": {"deadline_s": 4.0}, "lat_cost": 20.0},
    "deadline6_lat60": {"family": "deadline_cost", "cfg": {"deadline_s": 6.0}, "lat_cost": 60.0},
    "lat120":          {"family": "deadline_cost", "lat_cost": 120.0},
    "branch2":         {"family": "search_budget", "sim": {"max_branching": 2}},
    "branch2_lat30":   {"family": "search_budget", "sim": {"max_branching": 2}, "lat_cost": 30.0},
    "noise25":         {"family": "forecast_shift", "cfg": {"state_noise": 0.25}},
    "bias_under15":    {"family": "forecast_shift", "sim": {"forecast_bias": -0.15}},
    "bias_over15":     {"family": "forecast_shift", "sim": {"forecast_bias": 0.15}},
    "telemetry20":     {"family": "telemetry", "cfg": {"tool_fail_p": 0.20}},
    "telemetry40":     {"family": "telemetry", "cfg": {"tool_fail_p": 0.40}},
    # held-out families (never used to choose the best fixed strategy)
    "drift30":         {"family": "compliance_drift", "sim": {"compliance_drift": 0.30}},
    "resist50_drift15": {"family": "compliance_drift", "cfg": {"resistance_mean": 0.50}, "sim": {"compliance_drift": 0.15}},
    "wide6x7":         {"family": "feeder_structure", "spec": {"n_laterals": 6, "nodes_per_lateral": 7}},
    "long3x14":        {"family": "feeder_structure", "spec": {"n_laterals": 3, "nodes_per_lateral": 14}},
    "tightcap_weak":   {"family": "feeder_structure", "spec": {"head_cap_kw": 950.0, "line_r_pu": 0.028}},
    "feeder_seed3":    {"family": "feeder_structure", "feeder_seed": 3},
}
S4B_HELDOUT_FAMILIES = ["compliance_drift", "feeder_structure"]
S4B_MODES = ["PREDEFINED", "SEQUENTIAL", "HIERARCHICAL", "SEARCH"]


class S4bScenarioBank(Experiment):
    id = "S4b_scenario_bank"
    title = "Planning scenario bank: does the best feasible strategy change across situations? (S8 gate)"
    level = 4
    requires = ["S4_planning_backbone"]
    question = ("S4/S7 used one scenario family in which forced SEARCH always won, so a controller had nothing to "
                "learn. Across a bank of scenario families (deadlines with latency cost, limited search budget, "
                "forecast shift, telemetry failures, drifting compliance, other feeder structures), how often does the "
                "best feasible forced strategy differ from the best fixed strategy chosen on training families? "
                "Gate for S8: a meaningful share of HELD-OUT scenarios (families never used for selection).")
    default_params = {"model": "deepseek_v4_pro", "scenarios": list(S4B_SCENARIOS),
                      "heldout_families": S4B_HELDOUT_FAMILIES, "train_seeds": [7, 13, 42],
                      "heldout_seeds": [303, 404, 505], "modes": S4B_MODES,
                      "min_rel_gain": 0.05, "gate_share_lo": 0.15}
    est_calls_per_unit = 4 * 60      # calibrated on S4 actuals (~$0.04 per forced episode with DeepSeek-V4-Pro)
    est_tokens_in = 380
    est_tokens_out = 90

    def _family_of(self, sc):
        return S4B_SCENARIOS[sc]["family"]

    def _seeds(self, sc):
        return self.params["heldout_seeds"] if self._family_of(sc) in self.params["heldout_families"] \
            else self.params["train_seeds"]

    def _model(self):
        from .. import models as M
        return M.first_available(self.settings, self.resolved, self.params["model"]) or self.params["model"]

    def units(self):
        return [{"id": f"{sc}-s{s}", "scenario": sc, "family": self._family_of(sc), "seed": s,
                 "split": "heldout" if self._family_of(sc) in self.params["heldout_families"] else "train"}
                for sc in self.params["scenarios"] if sc in S4B_SCENARIOS for s in self._seeds(sc)]

    def estimate_models(self):
        return [self._model()]

    def run_unit(self, unit, ctx, outdir):
        import dataclasses
        from .. import planning_ext as PX
        sc = S4B_SCENARIOS[unit["scenario"]]
        # identical llm settings to S4 so base-scenario episodes are cached replicates of S4/E2 at shared seeds
        llm = ctx.llm(self.model_id(self._model()), role="planner", temperature=0.2, max_tokens=400)
        spec = dataclasses.replace(P.FeederSpec(), **sc.get("spec", {}))
        lat_cost = float(sc.get("lat_cost", 0.0))
        rows = []
        for mode in self.params["modes"]:
            cfg = dataclasses.replace(PX.episode_config(mode, unit["seed"], label=f"{unit['scenario']}-{mode}"),
                                      **sc.get("cfg", {}))
            out = PX.simulate_episode(cfg, spec, llm, feeder_seed=int(sc.get("feeder_seed", 1)),
                                      scenario=sc.get("sim"))
            s = out["summary"]
            rows.append({"mode": mode, "objective": s["objective"], "latency_s": s["latency_s"],
                         "objective_adj": s["objective"] + lat_cost * s["latency_s"],
                         "violation_hours": s["violation_hours"], "curtailed_kwh": s["curtailed_kwh"],
                         "deadline_misses": s["deadline_misses"], "deadline_downgrades": s["deadline_downgrades"],
                         "tool_failures": s["tool_failures"], "mean_compliance": s["mean_compliance"],
                         "curtail_gini": s["curtail_gini"], "executed_mode": s["executed_mode"]})
        df = pd.DataFrame(rows)
        df["feasible"] = df.deadline_misses == 0
        pool = df[df.feasible] if df.feasible.any() else df
        best = pool.sort_values("objective_adj").iloc[0]
        df["regret"] = df.objective_adj - float(best.objective_adj)
        df.to_csv(outdir / "modes.csv", index=False)
        summ = {"scenario": unit["scenario"], "family": unit["family"], "split": unit["split"],
                "best_mode": best["mode"], "best_obj": float(best.objective_adj), "lat_cost": lat_cost,
                "n_feasible": int(df.feasible.sum()), "model": llm.model, "cost_usd": llm.stats["cost_usd"]}
        for _, r in df.iterrows():
            summ[f"obj_{r['mode']}"] = float(r.objective_adj)
            summ[f"feas_{r['mode']}"] = bool(r.feasible)
        return summ

    def analyze(self):
        import numpy as np
        res = self.load_results()
        if not res:
            return "No results."
        df = pd.DataFrame(res)
        self.adir.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.adir / "summary.csv", index=False)
        modes = [m for m in self.params["modes"] if f"obj_{m}" in df]

        def regret(d, m):
            o = d[f"obj_{m}"].where(d.get(f"feas_{m}", True).astype(bool), np.inf)
            return o - d.best_obj
        tr, ho = df[df.split == "train"], df[df.split == "heldout"]
        # best fixed strategy chosen on TRAINING families only: lowest mean relative regret
        rel = {m: float((regret(tr, m) / tr.best_obj.abs().clip(lower=1.0)).replace(np.inf, 10.0).mean())
               for m in modes} if len(tr) else {}
        fixed = min(rel, key=rel.get) if rel else (df.best_mode.mode().iloc[0])
        out_rows = []
        for split, d in (("train", tr), ("heldout", ho)):
            if not len(d):
                continue
            r_fixed = regret(d, fixed)
            gain = (r_fixed / d.best_obj.abs().clip(lower=1.0)).replace(np.inf, 10.0)
            changed = (d.best_mode != fixed)
            meaningful = changed & (gain >= float(self.params["min_rel_gain"]))
            dd = d.assign(changed=changed.astype(float), meaningful=meaningful.astype(float), rel_gain=gain)
            for col in ("changed", "meaningful"):
                est = self._cluster_share(dd, col)
                out_rows.append({"split": split, "measure": col, "share": est[0], "lo": est[1], "hi": est[2],
                                 "n_scenario_seeds": len(dd), "n_scenarios": dd.scenario.nunique()})
            dd.to_csv(self.adir / f"per_unit_{split}.csv", index=False)
        tab = pd.DataFrame(out_rows)
        # exact (Clopper-Pearson) 95% interval per split, both per scenario-seed and per scenario (the cluster);
        # an all-zero sample gives a bootstrap interval of [0, 0], which does NOT mean the rate is zero
        from scipy import stats as _st

        def _cp(k, n):
            if n == 0:
                return (np.nan, np.nan)
            lo = 0.0 if k == 0 else float(_st.beta.ppf(0.025, k, n - k + 1))
            hi = 1.0 if k == n else float(_st.beta.ppf(0.975, k + 1, n - k))
            return lo, hi
        for i, r in tab.iterrows():
            d = tr if r["split"] == "train" else ho
            k = int(round(r["share"] * r["n_scenario_seeds"]))
            tab.loc[i, "exact_lo"], tab.loc[i, "exact_hi"] = _cp(k, int(r["n_scenario_seeds"]))
            per_sc = pd.read_csv(self.adir / f"per_unit_{r['split']}.csv").groupby("scenario")[r["measure"]].max()
            tab.loc[i, "scen_any"] = int(per_sc.sum())
            tab.loc[i, "scen_exact_hi"] = _cp(int(per_sc.sum()), len(per_sc))[1]
        tab.to_csv(self.adir / "gate.csv", index=False)
        # declared vs executed strategy: a forced mode can be downgraded by the deadline critic, so a 'winner' may be
        # an architecture-plus-fallback policy rather than the architecture itself
        mm = []
        for u in self.units():
            f = self.unit_dir(u["id"]) / "modes.csv"
            if f.exists() and self.unit_status(u["id"]).get("status") == "done":
                m = pd.read_csv(f)
                m["scenario"], m["seed"], m["split"] = u["scenario"], u["seed"], u["split"]
                mm.append(m)
        mismatch_lines, rule_lines = [], []
        if mm:
            M_ = pd.concat(mm, ignore_index=True)
            M_["mismatch"] = M_["mode"] != M_["executed_mode"]
            M_.to_csv(self.adir / "modes_all.csv", index=False)
            win = M_.merge(df[["scenario", "seed", "best_mode"]], on=["scenario", "seed"])
            win = win[win["mode"] == win.best_mode]
            mismatch_lines = [f"- Declared ≠ executed strategy in {int(M_.mismatch.sum())}/{len(M_)} mode-episodes "
                              f"({int(win.mismatch.sum())} of them are scenario winners: "
                              + ", ".join(f"{r.scenario}-s{r.seed} {r['mode']}→{r.executed_mode}" for _, r in win[win.mismatch].iterrows())
                              + "). These winners are architecture-plus-fallback policies (deadline downgrade), not the "
                              "declared architecture; `modes_all.csv` has both labels."]
            # simple, hand-written baseline a learned controller must beat: if decision latency is priced or the
            # deadline cannot fit SEARCH, use PREDEFINED (cheapest latency); otherwise SEARCH
            def rule(sc):
                c = S4B_SCENARIOS[sc]
                tight = float(c.get("cfg", {}).get("deadline_s", 30.0)) < P.MODE_COST_S["SEARCH"] * \
                    max(2, int(c.get("sim", {}).get("max_branching", 4))) / 4.0
                return "PREDEFINED" if (float(c.get("lat_cost", 0.0)) > 0 or tight) else "SEARCH"
            rr = []
            for split, d in (("train", tr), ("heldout", ho)):
                if not len(d):
                    continue
                for name, choose in (("fixed:" + fixed, lambda sc: fixed), ("rule", rule), ("oracle", None)):
                    if choose is None:
                        reg = pd.Series(0.0, index=d.index)
                    else:
                        reg = pd.Series([regret(d.loc[[i]], choose(d.loc[i, "scenario"])).iloc[0] for i in d.index], index=d.index)
                    relg = (reg / d.best_obj.abs().clip(lower=1.0)).replace(np.inf, 10.0)
                    rr.append({"split": split, "selector": name, "mean_regret": float(reg.replace(np.inf, np.nan).mean()),
                               "mean_rel_regret": float(relg.mean()), "n": len(d)})
            rr = pd.DataFrame(rr)
            rr.to_csv(self.adir / "selector_baselines.csv", index=False)
            rule_lines = ["**Selector baselines** (regret vs the per-scenario best feasible strategy; `rule` = PREDEFINED "
                          "when latency is priced or the deadline cannot fit SEARCH, else SEARCH)", "", md(rr.round(3)), "",
                          "- A learned controller (S8) must beat `rule`, not only the fixed strategy."]
        # leave-one-family-out: fixed strategy chosen on all other families, change share in the left-out family
        lofo = []
        for fam, d in df.groupby("family"):
            rest = df[df.family != fam]
            rr = {m: float((regret(rest, m) / rest.best_obj.abs().clip(lower=1.0)).replace(np.inf, 10.0).mean())
                  for m in modes}
            fx = min(rr, key=rr.get)
            g_ = (regret(d, fx) / d.best_obj.abs().clip(lower=1.0)).replace(np.inf, 10.0)
            lofo.append({"family": fam, "fixed_from_others": fx, "n": len(d),
                         "share_changed": float((d.best_mode != fx).mean()),
                         "share_meaningful": float(((d.best_mode != fx) & (g_ >= float(self.params["min_rel_gain"]))).mean()),
                         "mean_rel_gain_of_switching": float(g_.mean())})
        lofo = pd.DataFrame(lofo)
        lofo.to_csv(self.adir / "leave_one_family_out.csv", index=False)
        wins = df.groupby(["split", "family", "scenario"]).best_mode.value_counts().unstack(fill_value=0).reset_index()
        wins.to_csv(self.adir / "best_mode_by_scenario.csv", index=False)
        mean_obj = df.groupby("scenario")[[f"obj_{m}" for m in modes]].mean().round(1).reset_index()
        gate = tab[(tab.split == "heldout") & (tab.measure == "meaningful")]
        passed = bool(len(gate)) and float(gate.lo.iloc[0]) >= float(self.params["gate_share_lo"])
        C.write_json(self.adir / "gate.json", {"passed": passed, "fixed_strategy": fixed,
                                               "criterion": f"held-out share (best != fixed and gain >= "
                                                            f"{self.params['min_rel_gain']:.0%}) lower 95% CI >= "
                                                            f"{self.params['gate_share_lo']}",
                                               "table": out_rows})
        lines = [f"{len(df)} scenario x seed units ({df.scenario.nunique()} scenarios, {df.family.nunique()} families); "
                 f"held-out families: {', '.join(self.params['heldout_families'])}. Backbone `{df.model.iloc[0]}`. "
                 "Objective = upstream objective + latency price x decision latency; a strategy is feasible if it "
                 "never missed the control deadline.", "",
                 f"**Best fixed strategy on training families**: {fixed} (mean relative regret by mode: "
                 + ", ".join(f"{m} {v:.2f}" for m, v in rel.items()) + ")", "",
                 "**Best feasible forced strategy per scenario** (count over seeds)", "", md(wins), "",
                 "**Mean adjusted objective by scenario and mode** (lower is better)", "", md(mean_obj), "",
                 "**S8 gate** (share of scenario-seeds where the best strategy differs from the fixed one; cluster "
                 "bootstrap over scenarios)", "", md(tab.round(3)), "",
                 "**Leave-one-family-out** (fixed strategy chosen on the other families)", "", md(lofo.round(3)), "",
                 ] + rule_lines + [""] + mismatch_lines + ["",
                 f"- Gate: **{'PASS' if passed else 'FAIL'}** ({'held-out meaningful-change share lower CI ≥ ' + str(self.params['gate_share_lo'])})."
                 " S8 may be built only on PASS (REVIEWER §3a).",
                 "- `exact_lo/hi`: Clopper-Pearson over scenario-seeds; `scen_exact_hi`: the same over scenarios (the "
                 "independent unit). A held-out share of 0 is compatible with a true rate up to `scen_exact_hi`.",
                 "- One backbone and 3 seeds per scenario: shares describe this bank, not all feeders. Do not retune the "
                 "bank against these held-out scenarios; a redesigned bank needs a fresh held-out set."]
        return "\n".join(lines)

    @staticmethod
    def _cluster_share(d, col, n=5000, seed=42):
        import numpy as np
        groups = [g[col].values for _, g in d.groupby("scenario")]
        if not groups:
            return (np.nan, np.nan, np.nan)
        rng = np.random.default_rng(seed)
        k = len(groups)
        bs = [np.concatenate([groups[i] for i in rng.integers(0, k, k)]).mean() for _ in range(n)]
        return float(d[col].mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


class S8JointController(_NeedsBuild):
    id = "S8_joint_controller"
    title = "Constrained contextual bandit selecting (plan, governance, model, budget) jointly (Paper A, phase 3)"
    level = 6
    requires = ["S7_joint_factorial", "S6_risk_routing"]
    question = "Does a jointly learned controller beat separately optimised planning and governance selectors?"
