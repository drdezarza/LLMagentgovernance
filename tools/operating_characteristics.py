#!/usr/bin/env python3
"""Operating-characteristics table (ROADMAP 2026-10-15 late, "Practical applications", item 1). Stdlib only.

Reads the finished analyses of S5b / S5d (attack side) and S7b (operational side) plus data/ledger.sqlite and writes
reports/operating_characteristics.md and .csv. Read-only on data/. Built 2026-10-18 (daily review); exploratory.

Per configuration (eligible episodes only, adaptive attacker):
  * attacks that succeeded per 100 rounds (asr_per_round x 100) and the range over rotations;
  * attacks prevented per 100 rounds vs the label governor (S5b, paired by rotation x seed) and vs plain audit;
  * legitimate (clean honest) texts lost per 100: auditor misclassification vs restriction cost (tightened cap), kept apart;
  * deployment cost of the governor itself: auditor calls per round, auditor $ per 100 rounds (billed, and the
    uncached-equivalent), median / p90 auditor latency per call. Judge and simulator calls are measurement, not
    deployment, and are excluded. Only ledger rows of the session that produced the unit's final result are counted
    (retries of model_unavailable attempts are excluded).
S7b: per mechanism, message/content integrity, auditor calls and $ per 100 messages, and the objective delta vs G0 by
planning mode (from mechanism_effects.csv; the S7b objective is lower-is-better, so a positive delta is an operational cost).
"""
import argparse, csv, json, os, random, sqlite3, statistics as st, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, "data", "runs")


def rcsv(p):
    with open(p, newline="") as f:
        return list(csv.DictReader(f))


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def pct(xs, q):
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return None
    k = (len(xs) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def f(x, d=2):
    return "" if x is None else f"{x:.{d}f}"


def eligible_ids(stage):
    p = os.path.join(RUNS, stage, "_analysis", "summary_all.csv")
    rows = rcsv(p)
    out = {}
    for r in rows:
        el = str(r.get("eligible", "True")).lower() in ("true", "1")
        if el and r.get("attacker_mode", "adaptive") == "adaptive":
            out[(r["rot"], int(float(r["seed"])), r["governor"])] = r["id"]
    return out


def unit_session(stage, uid):
    try:
        with open(os.path.join(RUNS, stage, uid, "result.json")) as fh:
            return json.load(fh).get("session")
    except Exception:
        return None


def ledger_cost(con, stage, uid, session, role):
    q = ("select count(*), coalesce(sum(cost_usd),0), coalesce(sum(cost_equiv_usd),0) from calls "
         "where experiment=? and unit=? and role=? and mock=0 and status='ok'")
    args = [stage, uid, role]
    if session:
        q += " and session=?"
        args.append(session)
    n, c, ce = con.execute(q, args).fetchone()
    lat = [r[0] for r in con.execute(q.replace("count(*), coalesce(sum(cost_usd),0), coalesce(sum(cost_equiv_usd),0)",
                                               "latency_s") + " and cached=0", args)]
    return n, c, ce, lat


def boot(xs, n=2000, seed=42):
    """95% percentile bootstrap of the mean over episodes (or pairs); stdlib. Added 2026-10-24 for the -C table."""
    xs = [x for x in xs if x is not None]
    if len(xs) < 2:
        return (None, None)
    rng = random.Random(seed)
    ms = sorted(sum(rng.choice(xs) for _ in xs) / len(xs) for _ in range(n))
    return ms[int(0.025 * n)], ms[int(0.975 * n) - 1]


def attack_side(con, stages=("S5b_role_rotation", "S5d_memory_variants")):
    rows = []
    for stage in stages:
        an = os.path.join(RUNS, stage, "_analysis")
        if not os.path.exists(os.path.join(an, "validity_split.csv")):
            continue
        el = eligible_ids(stage)
        ep = {}
        for r in rcsv(os.path.join(an, "validity_split.csv")):
            if r["attacker_mode"] != "adaptive":
                continue
            key = (r["rot"], int(float(r["seed"])), r["governor"])
            if key in el:
                ep[key] = r
        govs = sorted({k[2] for k in ep}, key=lambda g: (g != "label", g != "audit", g))
        for g in govs:
            keys = [k for k in ep if k[2] == g]
            asr = [fnum(ep[k]["asr_per_round"]) for k in keys]
            by_rot = defaultdict(list)
            for k in keys:
                by_rot[k[0]].append(fnum(ep[k]["asr_per_round"]))
            rot_means = [mean(v) for v in by_rot.values()]

            def paired(ref, ci=False):
                d = [fnum(ep[(r, s, ref)]["asr_per_round"]) - fnum(ep[(r, s, g)]["asr_per_round"])
                     for (r, s, _) in keys if (r, s, ref) in ep]
                if ci:
                    return boot(d) if d and ref != g else (None, None)
                return (mean(d), len(d)) if d else (None, 0)

            pv_label, n_label = paired("label")
            pv_audit, n_audit = paired("audit")
            pvl_lo, pvl_hi = paired("label", ci=True)
            asr_lo, asr_hi = boot(asr)
            mis = [fnum(ep[k]["audit_misclassification_rate"]) for k in keys]
            mis_lo, mis_hi = boot(mis)
            n_calls = c_b = c_e = 0.0
            lats, n_rounds = [], 0
            for k in keys:
                uid = el[k]
                n, c, ce, lat = ledger_cost(con, stage, uid, unit_session(stage, uid), "auditor")
                n_calls += n; c_b += c; c_e += ce; lats += lat
                n_rounds += int(float(ep[k]["rounds"]))
            rows.append({
                "stage": stage, "governor": g, "episodes": len(keys), "rounds": n_rounds,
                "attacks_succeeded_per100": 100 * mean(asr),
                "asr_ci_lo_per100": None if asr_lo is None else 100 * asr_lo, "asr_ci_hi_per100": None if asr_hi is None else 100 * asr_hi,
                "prevented_vs_label_ci_lo": None if pvl_lo is None else 100 * pvl_lo,
                "prevented_vs_label_ci_hi": None if pvl_hi is None else 100 * pvl_hi,
                "lost_misclass_ci_lo": None if mis_lo is None else 100 * mis_lo,
                "lost_misclass_ci_hi": None if mis_hi is None else 100 * mis_hi,
                "asr_rot_min_per100": 100 * min(rot_means), "asr_rot_max_per100": 100 * max(rot_means),
                "prevented_vs_label_per100": None if pv_label is None else 100 * pv_label, "n_pairs_label": n_label,
                "prevented_vs_audit_per100": None if (pv_audit is None or g == "audit") else 100 * pv_audit,
                "n_pairs_audit": n_audit,
                "lost_misclass_per100": 100 * mean([fnum(ep[k]["audit_misclassification_rate"]) for k in keys]),
                "lost_restriction_per100": 100 * mean([fnum(ep[k]["policy_cap_rejection_rate"]) for k in keys]),
                "valid_submission": mean([fnum(ep[k]["valid_submission_rate"]) for k in keys]),
                "auditor_calls_per_round": n_calls / n_rounds if n_rounds else None,
                "auditor_usd_per100_rounds": 100 * c_b / n_rounds if n_rounds else None,
                "auditor_usd_equiv_per100_rounds": 100 * c_e / n_rounds if n_rounds else None,
                "auditor_latency_median_s": pct(lats, 0.5), "auditor_latency_p90_s": pct(lats, 0.9),
            })
    return rows


def s7b_side(con, stage="S7b_mechanism_ablation"):
    an = os.path.join(RUNS, stage, "_analysis")
    if not os.path.exists(os.path.join(an, "cells.csv")):
        return [], []
    cells = rcsv(os.path.join(an, "cells.csv"))
    by = defaultdict(list)
    for r in cells:
        by[r["gov"]].append(r)
    out = []
    for g in sorted(by, key=lambda x: (x != "G0", x)):
        rs = by[g]
        msgs = sum(fnum(r["n_messages"]) or 0 for r in rs)
        n_calls = c_b = c_e = 0.0
        lats = []
        for r in rs:
            n, c, ce, lat = ledger_cost(con, stage, r["id"], unit_session(stage, r["id"]), "auditor")
            n_calls += n; c_b += c; c_e += ce; lats += lat
        out.append({"gov": g, "units": len(rs), "messages": int(msgs),
                    "message_integrity": mean([fnum(r["message_integrity"]) for r in rs]),
                    "content_integrity": mean([fnum(r["content_integrity"]) for r in rs]),
                    "auditor_calls_per100_msgs": 100 * n_calls / msgs if msgs else None,
                    "auditor_usd_per100_msgs": 100 * c_b / msgs if msgs else None,
                    "auditor_usd_equiv_per100_msgs": 100 * c_e / msgs if msgs else None,
                    "auditor_latency_median_s": pct(lats, 0.5)})
    eff = [r for r in rcsv(os.path.join(an, "mechanism_effects.csv")) if r["outcome"] == "objective"]
    return out, eff


def main():
    ap = argparse.ArgumentParser(description="operating-characteristics table")
    ap.add_argument("--attack", nargs="*", default=["S5b_role_rotation", "S5d_memory_variants"])
    ap.add_argument("--feeder", default="S7b_mechanism_ablation")
    ap.add_argument("--out", default="operating_characteristics", help="file prefix under reports/")
    ap.add_argument("--confirmatory", action="store_true", help="title/notes for the frozen *_C stages")
    a = ap.parse_args()
    con = sqlite3.connect("file:" + os.path.join(ROOT, "data", "ledger.sqlite") + "?mode=ro", uri=True)
    A = attack_side(con, a.attack)
    B, E = s7b_side(con, a.feeder)
    os.makedirs(os.path.join(ROOT, "reports"), exist_ok=True)
    if A:
        with open(os.path.join(ROOT, "reports", a.out + ".csv"), "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(A[0].keys()))
            w.writeheader(); w.writerows(A)
    if B:
        with open(os.path.join(ROOT, "reports", a.out + "_s7b.csv"), "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(B[0].keys()))
            w.writeheader(); w.writerows(B)
    title = ("# Operating characteristics: CONFIRMATORY runs (" + ", ".join(a.attack + [a.feeder]) + "; frozen plan "
             "ANALYSIS_PLAN_v1, descriptive secondary output)" if a.confirmatory else
             "# Operating characteristics (exploratory, before the analysis-plan freeze)")
    L = [title, "",
         "Generated by `tools/operating_characteristics.py` from `data/runs/*/_analysis` and `data/ledger.sqlite`. "
         "Eligible episodes only; adaptive attacker; per 100 rounds of 25-round episodes (one deployment opportunity "
         "per round). Lost legitimate texts are split into auditor misclassification (classification error) and "
         "restriction cost (clean text over a deliberately tightened cap). Auditor cost is the governor's own "
         "deployment cost; judge calls (measurement) are excluded. `$ equiv` = cost without the response cache. "
         "These runs only (3 rotations, family confounded with role inside a rotation): read with the rotation range.", "",
         ("## A. Attack side (" + ", ".join(a.attack) + "; 95% bootstrap CIs over episodes / pairs in the CSV)" if a.confirmatory
          else "## A. Attack side (S5b seeds 1-3; S5d seeds 4+, fixed cap)"), "",
         "| stage | governor | ep | attacks/100 rounds | range over rotations | prevented vs label | prevented vs plain audit | "
         "lost: misclass /100 | lost: restriction /100 | auditor calls/round | auditor $/100 rounds | $ equiv | "
         "latency median / p90 s |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    def wci(v, lo, hi):
        return f(v, 1) + (f" [{f(lo, 1)}, {f(hi, 1)}]" if a.confirmatory and lo is not None else "")
    for r in A:
        L.append(f"| {r['stage'].split('_')[0]} | {r['governor']} | {r['episodes']} | "
                 f"{wci(r['attacks_succeeded_per100'], r['asr_ci_lo_per100'], r['asr_ci_hi_per100'])} | "
                 f"{f(r['asr_rot_min_per100'],1)}–{f(r['asr_rot_max_per100'],1)} | "
                 f"{wci(r['prevented_vs_label_per100'], r['prevented_vs_label_ci_lo'], r['prevented_vs_label_ci_hi'])} | "
                 f"{f(r['prevented_vs_audit_per100'],1)} | {wci(r['lost_misclass_per100'], r['lost_misclass_ci_lo'], r['lost_misclass_ci_hi'])} | "
                 f"{f(r['lost_restriction_per100'],1)} | "
                 f"{f(r['auditor_calls_per_round'],2)} | {f(r['auditor_usd_per100_rounds'],3)} | {f(r['auditor_usd_equiv_per100_rounds'],3)} | "
                 f"{f(r['auditor_latency_median_s'],1)} / {f(r['auditor_latency_p90_s'],1)} |")
    L += ["", "Prevented = paired mean difference in attack success over rotation × seed (same seeds within a stage; "
          "S5d has no label arm). Positive = fewer successful attacks than the reference. "
          + ("Brackets: 95% percentile bootstrap over episodes (pairs for 'prevented'), 2000 resamples, seed 42; descriptive, "
             "not a confirmatory test (the C-claims are in the stage findings)." if a.confirmatory else
             "No CIs here: the stage findings carry the bootstrap intervals."), ""]
    if B:
        L += [("## B. Operational side (" + a.feeder + "; 4 planning modes)" if a.confirmatory
               else "## B. Operational side (S7b feeder; 4 planning modes × 9 scenarios)"), "",
              "| mechanism | units | messages | message integrity | content integrity | auditor calls/100 msgs | "
              "auditor $/100 msgs | $ equiv | auditor latency median s |", "|---|---|---|---|---|---|---|---|---|"]
        for r in B:
            L.append(f"| {r['gov']} | {r['units']} | {r['messages']} | {f(r['message_integrity'],3)} | "
                     f"{f(r['content_integrity'],3)} | {f(r['auditor_calls_per100_msgs'],1)} | "
                     f"{f(r['auditor_usd_per100_msgs'],3)} | {f(r['auditor_usd_equiv_per100_msgs'],3)} | "
                     f"{f(r['auditor_latency_median_s'],1)} |")
        L += ["", "Objective delta vs G0 by planning mode (lower objective is better, so positive = operational cost; paired over "
              + ("the stage's" if a.confirmatory else "9") + " scenarios; from mechanism_effects.csv):", "",
              "| plan | contrast | delta | 95% CI |", "|---|---|---|---|"]
        for r in E:
            L.append(f"| {r['plan']} | {r['contrast']} | {f(fnum(r['delta']),1)} | [{f(fnum(r['lo']),1)}, {f(fnum(r['hi']),1)}] |")
    with open(os.path.join(ROOT, "reports", a.out + ".md"), "w") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    sys.exit(main())
