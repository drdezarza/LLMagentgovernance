#!/usr/bin/env python3
"""Re-check every number in paper/numbers.json against the current data/runs/*/_analysis files.
Usage (from the AGENT-GOV root):  python3 paper/check_numbers.py   (stdlib only; works in the device shell)
Entry kinds:
  csv : {"source": path, "where": {col: value, ...}, "column": col}        -> float compare with tolerance
  md  : {"source": path, "regex": pattern-with-one-group}                  -> first match, float compare
Exit code 1 and a list of drifted/missing entries when anything changed."""
import csv, json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = json.loads((ROOT / "paper" / "numbers.json").read_text())
bad = []
for e in spec["numbers"]:
    src = ROOT / e["source"]
    if not src.exists():
        bad.append((e["id"], "missing source " + e["source"])); continue
    try:
        if e["kind"] == "csv":
            rows = list(csv.DictReader(open(src)))
            hit = [r for r in rows if all(str(r.get(k)) == str(v) for k, v in e.get("where", {}).items())]
            if not hit:
                bad.append((e["id"], "row not found")); continue
            got = float(hit[0][e["column"]])
        else:
            m = re.search(e["regex"], src.read_text())
            if not m:
                bad.append((e["id"], "pattern not found")); continue
            got = float(m.group(1).replace("+", "").replace("−", "-"))
    except Exception as ex:
        bad.append((e["id"], f"error {ex}")); continue
    scale = float(e.get("scale", 1.0))
    if abs(got * scale - float(e["value"])) > float(e.get("tol", 0.0015)):
        bad.append((e["id"], f"text {e['value']} vs current {got * scale:.4f}"))
print(f"{len(spec['numbers'])} numbers checked; {len(bad)} drifted or missing")
for b in bad:
    print(" -", *b)
sys.exit(1 if bad else 0)
