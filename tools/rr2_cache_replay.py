"""RR_PLAN_v2 amendment 1 (2026-11-17; no API calls): cache-replay audit of feeder cells.

Re-runs recorded feeder cells (S7b, S7b_C, S7c, S7d) with the current code, answering every model call from the
LLM cache only (a call not in the cache stops that cell: "cache incomplete"). Compares the replayed objective with
the recorded one.

Why: until 2026-11-17 the cache used INSERT OR REPLACE. When parallel units sent the same prompt at the same time
(paired cells share prompts until their paths diverge), each got its own sample and the cache kept the LAST one,
not necessarily the one a given unit used. Replaying such a unit from the cache then gives a slightly different
episode. Since 2026-11-17 the first stored answer wins and every unit uses it.

Outputs: reports/rr2/R1_cache_replay.csv and R1_cache_replay.md
Usage:   python tools/rr2_cache_replay.py [AGENTGOV_ROOT] [--cache PATH] [--stages S7b_mechanism_ablation,...]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sqlite3
import sys

import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("root", nargs="?", default=str(pathlib.Path(__file__).resolve().parents[1]))
ap.add_argument("--cache", default=None)
ap.add_argument("--stages", default="S7b_mechanism_ablation,S7b_C,S7c_nonresponse,S7d_search_mechanism")
args = ap.parse_args()
ROOT = pathlib.Path(args.root)
sys.path.insert(0, str(ROOT))
from agentgov import llm as L, planning_ext as PX  # noqa: E402

RUNS = ROOT / "data" / "runs"
OUT = ROOT / "reports" / "rr2"
DB = sqlite3.connect(f"file:{args.cache or ROOT / 'data' / 'cache.nosync' / 'llm_cache.sqlite'}?mode=ro", uri=True)
S0 = pd.read_csv(RUNS / "S0_connectivity" / "_analysis" / "model_profiles.csv")
PROF = {r.model: {"min_max_tokens": int(r.min_max_tokens), "extra_body": json.loads(r.extra_body)} for r in S0.itertuples()}


class Miss(Exception):
    pass


class _Cache:
    def get(self, k):
        r = DB.execute("SELECT text, meta FROM cache WHERE k=?", (k,)).fetchone()
        if r is None:
            raise Miss()
        return r[0], json.loads(r[1] or "{}")

    def put(self, *a):
        raise Miss()


class _Ledger:
    def record(self, **k):
        pass


class _Ctx:
    mock = False
    session_id = experiment = unit = "replay"
    cache, ledger = _Cache(), _Ledger()

    def model_profile(self, m):
        return PROF.get(m, {})

    def price(self, *a):
        return 0.0

    class guard:
        @staticmethod
        def check():
            raise Miss()


def replay(man):
    u, roster = man["unit"], man.get("roster") or {}
    rid = lambda a: roster.get(a, a)
    ctx = _Ctx()
    llm = L.ModelLLM(ctx, rid(u["alias"]), role="planner", temperature=0.2, max_tokens=400)
    msg_on = PX.S7B_GOVS[u["gov"]][0]
    aud = L.ModelLLM(ctx, rid(u["auditor"]), role="auditor", temperature=0.0, max_tokens=300) if msg_on else None
    kw = {}
    esc, fb = bool(u.get("escalation", True)), bool(u.get("feedback", False))
    if not (esc and not fb):
        kw["scenario"] = {"search_escalation": esc, "search_feedback": fb}
    if u.get("nonresponse"):
        kw["scenario"] = {**kw.get("scenario", {}), "nonresponse": u["nonresponse"]}
    out = PX.run_s7b_episode(u["plan"], u["gov"], int(u["seed"]), llm, auditor=aud, **kw)
    return float(out["summary"]["objective"])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for st in args.stages.split(","):
        for d in sorted((RUNS / st).glob("R*-sc*")):
            rf, mf = d / "result.json", d / "manifest.json"
            if not (rf.exists() and mf.exists()):
                continue
            r = json.loads(rf.read_text())
            if r.get("status") != "done":
                continue
            rec = (r.get("summary") or r).get("objective")
            man = json.loads(mf.read_text())
            try:
                rep, status = replay(man), "replayed"
            except Miss:
                rep, status = float("nan"), "cache incomplete"
            except Exception as e:  # noqa
                rep, status = float("nan"), f"error: {type(e).__name__}"
            dev = abs(rep - rec) if rep == rep and rec is not None else float("nan")
            rows.append({"study": st, "cell": d.name, "gov": man["unit"]["gov"], "recorded": rec, "replayed": rep,
                         "abs_dev": dev, "status": status,
                         "exact": bool(dev == dev and dev < 1e-6)})
    D = pd.DataFrame(rows)
    D.to_csv(OUT / "R1_cache_replay.csv", index=False)
    S = D.groupby("study").agg(cells=("cell", "size"), replayed=("status", lambda s: int((s == "replayed").sum())),
                               exact=("exact", "sum"), max_abs_dev=("abs_dev", "max"),
                               median_abs_dev_if_differs=("abs_dev", lambda s: float(s[s > 1e-6].median())
                                                          if (s > 1e-6).any() else 0.0)).reset_index()
    lines = ["# Cache-replay audit of feeder cells (RR_PLAN_v2 amendment 1; no API calls)", "",
             "Each recorded cell re-run with the current code, every model call answered from the LLM cache. "
             "'exact' = replayed objective equals the recorded one to 1e-6. Differences come from the pre-2026-11-17 "
             "cache race (parallel units sending the same prompt; the cache kept the last answer).", "",
             "| " + " | ".join(S.columns) + " |", "|" + "|".join("---" for _ in S.columns) + "|"]
    for r in S.itertuples(index=False):
        lines.append("| " + " | ".join(f"{v:.2f}" if isinstance(v, float) else str(v) for v in r) + " |")
    (OUT / "R1_cache_replay.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
