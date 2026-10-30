"""Session journal, NEXT.md hand-off and the HTML report."""
from __future__ import annotations

import html
import json
import re
from collections import Counter
from datetime import datetime

from . import config as C
from . import models as M
from .experiments.base import runs_root
from .llm import Ledger, today


def _progress(mock):
    from .runner import build_env, progress
    S = C.settings()
    resolved = (M.resolve(S, None) if mock else (C.read_json(M.RESOLVED, None) or M.resolve(S, None)))
    return progress(S, resolved, mock), resolved


def finalize_session(sess, mock, log=print):
    C.ensure_dirs()
    with open(C.STATE_DIR / "sessions.jsonl", "a") as f:
        f.write(json.dumps(sess, default=str) + "\n")
    prog, resolved = _progress(mock)
    C.write_json(C.STATE_DIR / ("progress_mock.json" if mock else "progress.json"), prog)
    ledger = Ledger()
    spend_rows = ledger.summary("session=?", (sess["session"],))
    write_journal(sess, prog, spend_rows, ledger, mock)
    write_next(prog, ledger, mock)
    build_report(mock)
    log(f"journal, NEXT.md and report updated ({sess['stop_reason']})")


def write_journal(sess, prog, spend_rows, ledger, mock):
    day = datetime.now().strftime("%Y-%m-%d")
    path = C.JOURNAL / f"{day}{'-mock' if mock else ''}.md"
    c = Counter(u["status"] for u in sess["units"])
    lines = [f"\n## Session {sess['session']} ({sess['start']} → {sess.get('end')}, {sess.get('minutes')} min)", "",
             f"- Stop reason: {sess['stop_reason']}",
             f"- Units: " + (", ".join(f"{v} {k}" for k, v in c.items()) or "none"),
             f"- Spend this session: ${sum(r['cost_usd'] or 0 for r in spend_rows):.2f} · today "
             f"${ledger.spend(today()):.2f} · month ${ledger.spend_month():.2f} · all-time ${ledger.spend():.2f}"]
    if spend_rows:
        lines += ["", "| model | calls | cached | in tok | out tok | $ | mean latency s | errors |", "|---|---|---|---|---|---|---|---|"]
        lines += [f"| {r['model']} | {r['calls']} | {r['cached'] or 0} | {r['prompt_tokens']} | {r['completion_tokens']} | "
                  f"{r['cost_usd']} | {r['mean_latency_s']} | {r['errors']} |" for r in spend_rows]
    errs = [u for u in sess["units"] if u["status"] not in ("done", "stopped")]
    if errs:
        lines += ["", "Problems:"] + [f"- {u['experiment']}/{u['unit']}: {u['status']} — {u['error'][:200]}" for u in errs[:15]]
    # full findings only for stages that ran units this session; stages that were complete already are re-analysed
    # but only listed (the journal of 2026-10-21 reprinted all 20 complete stages twice: 2229 lines)
    ran = {u["experiment"] for u in sess["units"]}
    reanalysed = []
    for eid in dict.fromkeys(sess["completed_experiments"]):
        if eid not in ran:
            reanalysed.append(eid)
            continue
        f = runs_root(mock) / eid / "_analysis" / "findings.md"
        if f.exists():
            lines += ["", f"### {eid} completed", "", f.read_text().replace("](", f"](../data/{'runs_mock' if mock else 'runs'}/{eid}/_analysis/")]
    if reanalysed:
        lines += ["", "Re-analysed, no new units this session (findings in data/runs/<id>/_analysis/findings.md): "
                  + ", ".join(reanalysed)]
    lines += ["", "Queue: " + " · ".join(f"{k} {v.get('units_done', 0)}/{v.get('units_total', 0)} ({v['status']})"
                                     for k, v in prog.items() if v.get("enabled"))]
    for n in sess.get("notes", []):
        lines += ["", "```", n, "```"]
    new = not path.exists()
    with open(path, "a") as f:
        if new:
            f.write(f"# Journal {day}\n")
        f.write("\n".join(lines) + "\n")


def write_next(prog, ledger, mock):
    S = C.settings()
    lines = [f"# NEXT (auto-generated {datetime.now().strftime('%Y-%m-%d %H:%M')}{' — MOCK' if mock else ''})", "",
             f"Budget: today ${ledger.spend(today()):.2f} / ${C.budget_caps(S)[0]:.0f} · this month ${ledger.spend_month():.2f} / "
             f"${C.budget_caps(S)[1]:.0f}", "", "## Experiment queue", "",
             "| id | enabled | status | units | eligible | blocked by | est. remaining $ |", "|---|---|---|---|---|---|---|"]
    for k, v in prog.items():
        est = v.get("estimate") or {}
        frac_left = 1 - (v.get("units_done", 0) / v["units_total"]) if v.get("units_total") else 0
        lines.append(f"| {k} | {'yes' if v.get('enabled') else 'no'} | {v['status']} | "
                     f"{v.get('units_done', 0)}/{v.get('units_total', 0)} | {v.get('eligible', '-')} | "
                     f"{', '.join(v.get('blocked_by', [])) or '-'} | "
                     f"{(est.get('usd', 0) * frac_left):.2f} |")
    last = {}
    try:
        last = json.loads((C.STATE_DIR / "sessions.jsonl").read_text().strip().splitlines()[-1])
    except Exception:
        pass
    if "daily budget" in str(last.get("stop_reason", "")):
        lines += ["", f"**Daily budget cap reached in session {last.get('session')}** with work left. "
                  "To allow more on a given day, add it to config/budget_overrides.yaml."]
    runnable = [k for k, v in prog.items() if v.get("enabled") and v["status"] == "pending" and not v.get("blocked_by")]
    builds = [k for k, v in prog.items() if v["status"] == "needs_build"]
    lines += ["", "## What happens next", ""]
    lines.append(f"- Next session will run: {', '.join(runnable) if runnable else 'nothing (queue empty — enable more experiments in config/plan.yaml)'}")
    stale = {k: v.get("units_stale") for k, v in prog.items() if v.get("units_stale")}
    if stale:
        lines.append("- **Stale results** (done under different params than plan.yaml now specifies): "
                     + ", ".join(f"{k} ({n})" for k, n in stale.items())
                     + ". Re-run with `python -m agentgov retry <STAGE> --stale` or use a new stage id.")
    mixed = {k: len(v.get("code_versions") or []) for k, v in prog.items() if len(v.get("code_versions") or []) > 1}
    if mixed:
        lines.append("- Mixed code versions inside a stage (units ran under different agentgov code hashes; see each "
                     "unit's manifest.json — not evidence of invalid results, but check the diff touched nothing the "
                     "stage depends on): " + ", ".join(f"{k} ({n} versions)" for k, n in mixed.items()) + ".")
    if builds:
        lines.append(f"- Stages still to be built (spec in ROADMAP.md): {', '.join(builds)}")
    (C.STATE_DIR / ("NEXT_mock.md" if mock else "NEXT.md")).write_text("\n".join(lines) + "\n")


# --------------------------------------------------------------------------- html report
def _md_to_html(md: str, img_prefix: str) -> str:
    out, in_table, in_list, in_code = [], False, False, False
    for line in md.splitlines():
        if line.startswith("```"):
            out.append("</pre>" if in_code else "<pre>")
            in_code = not in_code
            continue
        if in_code:
            out.append(html.escape(line)); continue
        s = line.strip()
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                continue
            if not in_table:
                out.append("<table>"); in_table = True
                out.append("<tr>" + "".join(f"<th>{_inline(c)}</th>" for c in cells) + "</tr>")
            else:
                out.append("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in cells) + "</tr>")
            continue
        if in_table:
            out.append("</table>"); in_table = False
        m = re.match(r"!\[(.*?)\]\((.*?)\)", s)
        if m:
            out.append(f'<img src="{img_prefix}{m.group(2)}" alt="{html.escape(m.group(1))}">'); continue
        if s.startswith("- "):
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append(f"<li>{_inline(s[2:])}</li>"); continue
        if in_list:
            out.append("</ul>"); in_list = False
        h = re.match(r"(#+) (.*)", s)
        if h:
            n = min(len(h.group(1)) + 1, 6)
            out.append(f"<h{n}>{_inline(h.group(2))}</h{n}>")
        elif s:
            out.append(f"<p>{_inline(s)}</p>")
    if in_table:
        out.append("</table>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def _inline(s):
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s


CSS = """
:root{--bg:#fbfaf7;--fg:#1f2328;--mut:#6a6f76;--line:#e3e0d8;--acc:#2a6f97;--ok:#2E7D32;--warn:#b26a00}
@media (prefers-color-scheme:dark){:root{--bg:#16181b;--fg:#e6e6e6;--mut:#9aa0a6;--line:#2c3036;--acc:#6fb1d8;--ok:#7bc47f;--warn:#e0a458}}
body{background:var(--bg);color:var(--fg);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;max-width:1100px;margin:0 auto;padding:24px 16px}
h1{font-size:26px;margin:0 0 4px}h2{margin-top:36px;border-bottom:1px solid var(--line);padding-bottom:6px}
.mut{color:var(--mut)}table{border-collapse:collapse;margin:10px 0;font-size:13px;display:block;overflow-x:auto}
td,th{border:1px solid var(--line);padding:4px 8px;text-align:left;white-space:nowrap}th{background:rgba(127,127,127,.08)}
img{max-width:100%;border:1px solid var(--line);border-radius:6px;margin:8px 0;background:#fff}
.pill{display:inline-block;padding:1px 8px;border-radius:10px;font-size:12px;border:1px solid var(--line)}
.complete{color:var(--ok)}.pending{color:var(--warn)}code{font-size:12.5px}pre{overflow-x:auto;font-size:12px}
"""


def build_report(mock=False):
    prog, _ = _progress(mock)
    ledger = Ledger()
    S = C.settings()
    rr = runs_root(mock)
    parts = [f"<h1>AGENT-GOV research log{' (mock)' if mock else ''}</h1>",
             f"<p class='mut'>Updated {datetime.now().strftime('%Y-%m-%d %H:%M')} · spend today "
             f"${ledger.spend(today()):.2f} / ${C.budget_caps(S)[0]:.0f} · this month ${ledger.spend_month():.2f} / "
             f"${C.budget_caps(S)[1]:.0f}</p>", "<h2>Queue</h2><table><tr><th>stage</th><th>title</th><th>enabled</th>"
             "<th>status</th><th>units</th><th>blocked by</th></tr>"]
    for k, v in prog.items():
        parts.append(f"<tr><td>{k}</td><td>{html.escape(v.get('title', ''))}</td><td>{'yes' if v.get('enabled') else 'no'}</td>"
                     f"<td><span class='pill {v['status']}'>{v['status']}</span></td>"
                     f"<td>{v.get('units_done', 0)}/{v.get('units_total', 0)}</td><td>{', '.join(v.get('blocked_by', []))}</td></tr>")
    parts.append("</table>")
    from .experiments import REGISTRY
    for k, v in prog.items():
        adir = rr / k / "_analysis"
        f = adir / "findings.md"
        interim = False
        if not f.exists():
            f = adir / "findings_interim.md"
            interim = True
        if not f.exists():
            continue
        cls = REGISTRY.get(k)
        parts.append(f"<h2>{k}: {html.escape(v.get('title', ''))}{' <span class=mut>(interim)</span>' if interim else ''}</h2>")
        if cls is not None and cls.question:
            parts.append(f"<p class='mut'><i>{html.escape(cls.question)}</i></p>")
        rel = f"../data/{'runs_mock' if mock else 'runs'}/{k}/_analysis/"
        parts.append(_md_to_html(f.read_text(), rel))
    rows = ledger.summary("mock=?", (int(mock),))
    if rows:
        parts.append("<h2>Model usage (all sessions)</h2><table><tr>" + "".join(f"<th>{c}</th>" for c in rows[0]) + "</tr>")
        parts += ["<tr>" + "".join(f"<td>{html.escape(str(r[c]))}</td>" for c in r) + "</tr>" for r in rows]
        parts.append("</table>")
    doc = f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>" \
          f"<title>AGENT-GOV log</title><style>{CSS}</style></head><body>{''.join(parts)}</body></html>"
    C.REPORTS.mkdir(parents=True, exist_ok=True)
    (C.REPORTS / ("index_mock.html" if mock else "index.html")).write_text(doc)
