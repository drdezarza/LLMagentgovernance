"""simulate_gcge(deploy_upstream) must reproduce upstream run_gcge exactly."""
import hashlib, json, sys, tempfile, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, pandas as pd
from agentgov.upstream import gcge_core as G
from agentgov import gcge_ext as X
from agentgov.upstream import planning_core as P


class HashLLM:
    """Deterministic, order-independent fake: response is a function of the prompt only."""
    def __init__(self): self.stats = {"calls": 0}
    def generate(self, prompt, system=None, cache_key=None):
        self.stats["calls"] += 1
        h = int(hashlib.sha1(((system or "") + prompt + (cache_key or "")).encode()).hexdigest(), 16)
        r = np.random.default_rng(h % (2**32))
        s = (system or "").upper()
        if "CRITIC" in s:
            return json.dumps({"approve": bool(r.random() < .7), "risk_level": "HIGH", "adjusted_intensity": round(r.random(), 2)})
        if "EVALUATE HOW PERSUASIVE" in s:
            return json.dumps({"shift": round(float(r.uniform(-.3, .3)), 3), "persuaded": bool(r.random() < .5)})
        if "COMPILE" in s:
            return json.dumps({"target_mode": str(r.choice(list(G.VALID_TARGETS))), "theme": "MORAL",
                               "intensity": round(r.random(), 2), "timing": "BURST", "claims": "FACTUAL",
                               "confidence": round(r.random(), 2), "reasoning": "x" * 20})
        return "Cooperate, it helps everyone."


def test_equivalence():
    for mode in ["governed", "naive", "unconstrained"]:
        cfg = G.GCGEConfig(n_agents=20, steps=20, seed=3, governance_mode=mode, label=mode)
        with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
            a, pa, _ = G.run_gcge(cfg, d1, HashLLM(), HashLLM(), verbose=False)
            b, pb, _ = X.simulate_gcge(cfg, d2, HashLLM(), HashLLM())
            pd.testing.assert_frame_equal(a, b)
            pd.testing.assert_frame_equal(pa, pb.drop(columns=["narrative"]))  # narrative = provenance-only extra column
    print("equivalence OK")


class FeederHashLLM:
    """Deterministic fake for the feeder prompts (planner, critic, prosumer, narrative)."""
    def __init__(self): self.stats = {"calls": 0}
    def generate(self, prompt, system=None, cache_key=None):
        self.stats["calls"] += 1
        h = int(hashlib.sha1(((system or "") + prompt).encode()).hexdigest(), 16)
        r = np.random.default_rng(h % (2**32))
        s = (system or "").upper()
        if "BASE SCORE" in s:
            return json.dumps({"shift": {m: round(float(r.uniform(-.3, .3)), 3) for m in P.PLAN_MODES}})
        if "PLAN MODE" in s:
            return json.dumps({"mode": str(r.choice(P.PLAN_MODES)), "target_mode": str(r.choice(P.TARGET_MODES)),
                               "theme": str(r.choice(["MORAL", "FEAR", "URGENCY", "HYBRID"])), "depth": int(r.integers(1, 4)),
                               "branching": int(r.integers(1, 8)), "replan_trigger": str(r.choice(P.REPLAN_TRIG)),
                               "intensity": round(float(r.random()), 2), "confidence": 0.7})
        if "CRITIC" in s:
            return json.dumps({"approve": bool(r.random() < .7), "risk_level": "MEDIUM", "adjusted_intensity": round(r.random(), 2)})
        if "HOW PERSUASIVE" in s:
            return json.dumps({"shift": round(float(r.uniform(-.3, .3)), 3), "persuaded": True})
        if "AUDITOR" in s or "JUDGE" in s:
            return json.dumps({"claims": str(r.choice(["FACTUAL", "MISLEADING"])), "theme": "ECONOMIC",
                               "intensity": 0.5, "manipulative": bool(r.random() < .3)})
        return "Please curtail, the feeder is over its limit. " + str(h % 997)


def test_feeder_equivalence():
    """simulate_episode(governor=None) must reproduce upstream run_episode exactly."""
    from agentgov.upstream import planning_core as P
    from agentgov import planning_ext as PX
    spec = P.FeederSpec()
    cases = [dict(declaration="natural"), dict(declaration="hybrid"),
             dict(declaration="forced", forced_mode="SEARCH"), dict(declaration="forced", forced_mode="HIERARCHICAL"),
             dict(declaration="natural", critic_llm=True, adversarial=True, honesty=0.5)]
    for kw in cases:
        cfg = P.EpisodeConfig(seed=13, **kw)
        a = P.run_episode(cfg, spec, FeederHashLLM())
        b = PX.simulate_episode(cfg, spec, FeederHashLLM())
        assert json.dumps(a["summary"], default=str, sort_keys=True) == json.dumps(b["summary"], default=str, sort_keys=True), kw
        pd.testing.assert_frame_equal(a["timeseries"], b["timeseries"])
        pd.testing.assert_frame_equal(a["realized"], b["realized"].drop(columns=["llm_eval"]))
        pd.testing.assert_frame_equal(a["plan_log"], b["plan_log"])
    # S7 G0 with a forced plan == the S4/E2 forced episode
    for mode in P.PLAN_MODES:
        a = P.run_episode(P.EpisodeConfig(seed=7, declaration="forced", forced_mode=mode, label=f"forced-{mode}"), spec, FeederHashLLM())
        b = PX.run_s7_episode(mode, "G0", 7, FeederHashLLM())
        sa, sb = dict(a["summary"]), dict(b["summary"])
        sa.pop("label"); sb.pop("label")
        assert json.dumps(sa, default=str, sort_keys=True) == json.dumps(sb, default=str, sort_keys=True), mode
    # governed runs execute and respect the constitution
    for gov in ["G1", "G2"]:
        out = PX.run_s7_episode("natural", gov, 42, FeederHashLLM(), auditor=FeederHashLLM())
        assert all(p <= 0.95 + 1e-9 for p in out["plan_log"]["intensity"]), gov
        assert all(m["theme"] not in PX.BANNED_THEMES for m in out["messages"]), gov
    print("feeder equivalence OK")


if __name__ == "__main__":
    test_equivalence()
    test_feeder_equivalence()
