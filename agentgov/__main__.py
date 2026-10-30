"""Command line: python -m agentgov <command>

  check                 verify credentials, reach Nebius, resolve the model roster
  plan                  show the experiment menu, status, and cost estimates
  run [--hours 3.5]     run one time-boxed session (what the daily schedule calls)
      [--mock]          offline dry run with synthetic responses (no API calls, no cost)
      [--only S2_...]   run only these experiment ids (ignores enabled flags/prerequisites)
  status                progress and spend
  report                rebuild reports/index.html
  analyze <EXP_ID>      re-run the analysis of one experiment
  retry <EXP_ID>        reset failed/given-up units of an experiment so they run again
"""
from __future__ import annotations

import argparse
import sys

from . import config as C
from . import models as M


def main(argv=None):
    ap = argparse.ArgumentParser(prog="agentgov", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["check", "plan", "run", "status", "report", "analyze", "retry"])
    ap.add_argument("exp", nargs="?")
    ap.add_argument("--hours", type=float, default=None)
    ap.add_argument("--mock", action="store_true")
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--workers", type=int)
    ap.add_argument("--stale", action="store_true", help="retry: reset done units whose params fingerprint is outdated")
    a = ap.parse_args(argv)
    C.ensure_dirs()
    S = C.settings()

    if a.cmd == "run":
        from .runner import run_session
        run_session(a.hours or float(S["session"]["hours"]), mock=a.mock, only=a.only, workers=a.workers)
        return

    if a.cmd == "check":
        cred = C.credentials()
        if not C.has_key():
            print(f"✗ No API key. Paste it into {C.CRED_FILE} (line NEBIUS_API_KEY=...)")
            sys.exit(1)
        print(f"✓ key found ({cred['NEBIUS_API_KEY'][:6]}…), endpoint {cred['NEBIUS_BASE_URL']}")
        from .runner import build_env
        try:
            S, resolved, _ = build_env(False)
        except BaseException as e:
            print(f"✗ could not reach Nebius: {e}")
            sys.exit(1)
        print("Roster:")
        for al, r in resolved.items():
            print(f"  {'✓' if r['available'] else '✗'} {al:20s} {r['id'] or '(not in catalogue)'}")
        print(f"Live catalogue saved to {M.LIVE}")
        return

    if a.cmd in ("plan", "status"):
        from .runner import progress
        from .llm import Ledger, today
        resolved = M.resolve(S, None) if a.mock else (C.read_json(M.RESOLVED, None) or M.resolve(S, None))
        prog = progress(S, resolved, a.mock)
        L = Ledger()
        d, m = C.budget_caps(S)
        print(f"Spend: today ${L.spend(today()):.2f} / ${d:.0f} · this month ${L.spend_month():.2f} / ${m:.0f} · all-time ${L.spend():.2f}")
        print(f"{'stage':24s} {'on':3s} {'status':12s} {'units':>9s} {'est $':>8s}  blocked by")
        for k, v in prog.items():
            est = v.get("estimate") or {}
            print(f"{k:24s} {'yes' if v.get('enabled') else 'no':3s} {v['status']:12s} "
                  f"{str(v.get('units_done', 0)) + '/' + str(v.get('units_total', 0)):>9s} {est.get('usd', 0):>8.2f}  "
                  f"{', '.join(v.get('blocked_by', []))}")
        if a.cmd == "plan":
            print("\nEdit config/plan.yaml to enable/disable stages or change their params.")
        return

    if a.cmd == "report":
        from .report import build_report
        build_report(a.mock)
        print(C.REPORTS / ("index_mock.html" if a.mock else "index.html"))
        return

    if a.cmd in ("analyze", "retry"):
        from .runner import make
        entry = next((e for e in C.plan().get("experiments", []) if e["id"] == a.exp), {"id": a.exp})
        resolved = M.resolve(S, None) if a.mock else (C.read_json(M.RESOLVED, None) or M.resolve(S, None))
        exp = make(entry, S, resolved, a.mock)
        if exp is None:
            print("unknown experiment"); sys.exit(1)
        if a.cmd == "analyze":
            from .experiments.base import write_findings
            from .runner import unit_state, DONE, GAVE_UP
            txt = exp.analyze()
            write_findings(exp, txt, interim=not all(unit_state(exp, u) in (DONE, GAVE_UP) for u in exp.units()))
            print(txt)
        else:
            n = 0
            from . import provenance as PV
            ph = PV.params_hash(exp.params)
            for u in exp.units():
                r = exp.unit_status(u["id"])
                stale = a.stale and r.get("status") == "done" and PV.is_stale(exp.params, r.get("fingerprint") or {})
                if r and (r.get("status") not in ("done", None) or stale):
                    r["attempts"] = 0
                    r["status"] = "reset"
                    C.write_json(exp.unit_dir(u["id"]) / "result.json", r)
                    n += 1
            print(f"reset {n} units")


if __name__ == "__main__":
    main()
