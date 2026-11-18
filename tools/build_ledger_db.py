"""Rebuild data/ledger.sqlite from the published call ledger data/ledger/calls.csv.gz (stdlib only; no API calls).

The pipeline writes every model call to data/ledger.sqlite during a session. The repository publishes the same table
as data/ledger/calls.csv.gz (all non-mock calls; no prompt or response text). A few analyses read the SQLite form:
the A8b cost/latency table in `python -m agentgov analyze A8b_cheap_auditor_live` and tools/operating_characteristics.py.
Run this once before re-running those analyses.

Usage:  python tools/build_ledger_db.py [--force]
"""
import csv
import gzip
import pathlib
import sqlite3
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC, DB = ROOT / "data" / "ledger" / "calls.csv.gz", ROOT / "data" / "ledger.sqlite"
INT = {"prompt_tokens", "completion_tokens", "reasoning_tokens", "cached", "mock"}
REAL = {"ts", "cost_usd", "latency_s", "cost_equiv_usd"}


def conv(col, v):
    if v == "":
        return None
    if col in INT:
        return int(float(v))
    if col in REAL:
        return float(v)
    return v


def main():
    if DB.exists() and "--force" not in sys.argv:
        sys.exit(f"{DB} exists (a session ledger?); pass --force to replace it")
    if DB.exists():
        DB.unlink()
    with gzip.open(SRC, "rt", newline="") as f:
        r = csv.reader(f)
        cols = next(r)
        types = {c: ("REAL" if c in REAL else "INTEGER" if c in INT else "TEXT") for c in cols}
        con = sqlite3.connect(DB)
        con.execute(f"CREATE TABLE calls ({', '.join(f'{c} {types[c]}' for c in cols)})")
        q = f"INSERT INTO calls VALUES ({','.join('?' * len(cols))})"
        n = 0
        batch = []
        for row in r:
            batch.append([conv(c, v) for c, v in zip(cols, row)])
            if len(batch) == 10000:
                con.executemany(q, batch); n += len(batch); batch = []
        con.executemany(q, batch); n += len(batch)
        con.execute("CREATE INDEX calls_exp_role ON calls (experiment, role)")
        con.commit()
        con.close()
    print(f"{n} calls written to {DB}")


if __name__ == "__main__":
    main()
