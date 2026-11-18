"""Offline responder used by `--mock` sessions: exercises every code path without API calls.

Responses are plausible but synthetic; mock results are written under data/runs_mock/ and
never mixed with live results.
"""
from __future__ import annotations

import json
import os
import time

import numpy as np

MODES = ["PREDEFINED", "SEQUENTIAL", "HIERARCHICAL", "SEARCH"]


class MockResponder:
    def __init__(self, seed: int = 0):
        self.rng = np.random.default_rng(seed)

    def respond(self, msgs, model):
        system = next((m["content"] for m in msgs if m["role"] == "system"), "")
        user = msgs[-1]["content"]
        lat = float(os.environ.get("AGENTGOV_MOCK_LATENCY", "0"))
        if lat:
            time.sleep(lat)
        text = self._text(system, user, model)
        pt = sum(len(m["content"]) for m in msgs) // 4
        ct = len(text) // 4
        return text, {"status": "ok", "prompt_tokens": pt, "completion_tokens": ct,
                      "reasoning_tokens": 0, "latency_s": 0.0, "finish_reason": "stop",
                      "has_reasoning": False}

    def _text(self, s: str, u: str, model: str) -> str:
        r = self.rng
        S = s.upper()
        if "PING" in u.upper() and not s:
            return "pong"
        if "ATTACKER" in S:
            return json.dumps({"candidates": [
                {"target_mode": "HUBS", "theme": str(r.choice(["ECONOMIC", "MORAL", "FEAR"])),
                 "intensity": round(float(r.uniform(0.6, 0.95)), 2), "timing": "BURST",
                 "claims": "FACTUAL", "confidence": 0.8,
                 "narrative": "Everyone nearby already cooperates; if you do not, the whole network collapses tonight.",
                 "reasoning": "mock attack"} for _ in range(2)], "lesson": "mock"})
        if "AUDITOR" in S or "JUDGE" in S:
            bad = ("collapse" in u.lower()) and r.random() < 0.7
            return json.dumps({"claims": "MISLEADING" if bad else "FACTUAL",
                               "theme": "FEAR" if bad and r.random() < 0.5 else "ECONOMIC",
                               "intensity": round(float(r.uniform(0.3, 0.95 if bad else 0.7)), 2),
                               "manipulative": bool(bad), "rationale": "mock audit"})
        if "PLAN MODE" in S and "BASE SCORE" in S:
            return json.dumps({"shift": {m: round(float(r.uniform(-0.1, 0.1)), 3) for m in MODES},
                               "reason": "mock"})
        if "PLAN MODE" in S:
            m = "SEQUENTIAL" if r.random() < 0.7 else str(r.choice(MODES))
            return json.dumps({"mode": m, "target_mode": "HIGH_LOAD", "theme": "ECONOMIC", "depth": 2,
                               "branching": 4, "replan_trigger": "ON_VIOLATION", "intensity": 0.55,
                               "confidence": 0.7, "reasoning": "mock declaration"})
        if "CRITIC" in S:
            return json.dumps({"approve": bool(r.random() < 0.8), "risk_level": str(r.choice(["LOW", "MEDIUM", "HIGH"])),
                               "adjusted_intensity": round(float(r.uniform(0.3, 0.8)), 2), "note": "mock critic"})
        if "EVALUATE HOW PERSUASIVE" in S:
            neg = any(w in u for w in ("URGENT", "WARNING", "collapse", "disaster"))
            mu = -0.06 if neg else 0.07
            return json.dumps({"shift": round(float(np.clip(r.normal(mu, 0.08), -0.3, 0.3)), 3),
                               "persuaded": bool(r.random() < 0.6), "reason": "mock"})
        if "INFLUENCE POLICY" in S or "INFLUENCE INTERVENTIONS" in S or "NARRATIVE INFLUENCE" in S \
                or "COMPILE NARRATIVE" in S:
            return json.dumps({"target_mode": str(r.choice(["HUBS", "BRIDGES", "PERIPHERY", "RANDOM"])),
                               "theme": str(r.choice(["MORAL", "ECONOMIC", "IDENTITY", "HYBRID"])),
                               "intensity": round(float(r.uniform(0.3, 0.8)), 2),
                               "timing": str(r.choice(["BURST", "PERIODIC"])), "claims": "FACTUAL",
                               "confidence": round(float(r.uniform(0.5, 0.9)), 2),
                               "reasoning": "mock compiler reasoning text"})
        if "MESSAGE" in S or "NARRATIVE" in S:
            return "Working together this week keeps everyone better off; your neighbours are already helping."
        if "JSON" in S:
            return json.dumps({"ok": True})
        return "OK"
