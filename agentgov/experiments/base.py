"""Experiment interface. An experiment is a set of independent, resumable *units*.

A unit is the smallest piece of work that is either complete or not (e.g. one simulation run,
one model's probe battery). Units write into data/runs/<EXP>/<unit-id>/ and finish by writing
result.json with status "done". The runner skips done units, so a session interrupted by the
deadline or budget simply continues the next day (and repeated LLM calls hit the disk cache).
"""
from __future__ import annotations

import json
import pathlib
from typing import Any, Dict, List

from .. import config as C
from .. import models as M


def runs_root(mock: bool) -> pathlib.Path:
    return C.DATA / ("runs_mock" if mock else "runs")


class Experiment:
    id = "X"
    title = ""
    level = 0
    question = ""
    requires: List[str] = []
    default_params: Dict[str, Any] = {}
    # rough planning numbers (per unit) for `agentgov plan` cost estimates
    est_calls_per_unit = 100
    est_tokens_in = 400
    est_tokens_out = 120

    def __init_subclass__(cls, **kw):
        """Wrap every subclass' units() so that DONE units of models that have since left the live catalogue stay
        part of the stage (fix 2026-10-29: Qwen3.5-397B was delisted at Nebius and the 09:00 re-analysis silently
        dropped its finished units from S0/S1/S3/S4/A0/A1). Units of unavailable models that are not done are still
        left out, so nothing is ever dispatched to a delisted model."""
        super().__init_subclass__(**kw)
        f = cls.__dict__.get("units")
        if f is None or getattr(f, "_keeps_done", False):
            return

        def units(self, _f=f):
            now = _f(self)
            if getattr(self, "_in_units_full", False):
                return now
            gone = {a: r for a, r in (self.resolved or {}).items() if not r.get("available")}
            if not gone:
                return now
            full_res = dict(self.resolved)
            for a, r in gone.items():
                cands = ((self.settings.get("roster") or {}).get(a) or {}).get("candidates") or []
                full_res[a] = {**r, "id": r.get("id") or (cands[0] if cands else a), "available": True}
            saved = self.resolved
            self.resolved, self._in_units_full = full_res, True
            try:
                full = _f(self)
            except Exception:
                full = []
            finally:
                self.resolved, self._in_units_full = saved, False
            have = {u["id"] for u in now}
            extra = [u for u in full if u["id"] not in have and self.unit_status(u["id"]).get("status") == "done"]
            if not extra:
                return now
            keep = have | {u["id"] for u in extra}
            ordered = [u for u in full if u["id"] in keep]      # original design order (tables, bootstrap draws)
            seen = {u["id"] for u in ordered}
            return ordered + [u for u in now if u["id"] not in seen]

        units._keeps_done = True
        units.__doc__ = f.__doc__
        cls.units = units

    def __init__(self, params: Dict[str, Any], settings: Dict[str, Any], resolved: Dict[str, Any], mock: bool):
        self.params = {**self.default_params, **(params or {})}
        self.settings, self.resolved, self.mock = settings, resolved, mock
        self.dir = runs_root(mock) / self.id
        self.adir = self.dir / "_analysis"

    # helpers ---------------------------------------------------------------
    def group(self, g) -> List[str]:
        return M.group(self.settings, self.resolved, g)

    def model_id(self, alias: str) -> str:
        r = self.resolved.get(alias)
        return r["id"] if r and r.get("id") else alias

    def unit_dir(self, uid: str) -> pathlib.Path:
        return self.dir / uid

    def unit_status(self, uid: str) -> Dict[str, Any]:
        return C.read_json(self.unit_dir(uid) / "result.json", {}) or {}

    def load_results(self) -> List[Dict[str, Any]]:
        out = []
        for u in self.units():
            r = self.unit_status(u["id"])
            if r.get("status") == "done":
                out.append({**u, **r.get("summary", {})})
        return out

    # interface ---------------------------------------------------------------
    def prepare(self, ctx) -> None:
        """Main-process hook before units are dispatched (may use ctx.http)."""

    def units(self) -> List[Dict[str, Any]]:
        raise NotImplementedError

    def run_unit(self, unit: Dict[str, Any], ctx, outdir: pathlib.Path) -> Dict[str, Any]:
        """Do the work; return a flat summary dict (stored in result.json)."""
        raise NotImplementedError

    def analyze(self) -> str:
        """Aggregate done units into _analysis/; return markdown findings."""
        return ""

    def estimate(self) -> Dict[str, float]:
        n = len(self.units())
        calls = n * self.est_calls_per_unit
        aliases = self.estimate_models()
        price = [0.5, 1.5]
        if aliases:
            ps = [self.resolved.get(a, {}).get("price") or self.settings.get("default_price", [3, 15]) for a in aliases]
            price = [sum(p[0] for p in ps) / len(ps), sum(p[1] for p in ps) / len(ps)]
        usd = calls * (self.est_tokens_in * price[0] + self.est_tokens_out * price[1]) / 1e6
        return {"units": n, "calls": calls, "usd": round(usd, 2)}

    def estimate_models(self) -> List[str]:
        return []


def write_findings(exp: "Experiment", text: str, interim: bool = False) -> None:
    """Write findings(.md|_interim.md) and an analysis manifest; archive the previous findings if they change.
    Publication audit (2026-10-15): every table can be traced to the contributing unit ids, their code versions,
    the exclusions applied (exp.validity, set by analyze) and the analysis code/rubric versions."""
    import datetime
    import hashlib
    from .. import provenance as PV
    exp.adir.mkdir(parents=True, exist_ok=True)
    name = "findings_interim.md" if interim else "findings.md"
    p = exp.adir / name
    if p.exists():
        old = p.read_text()
        if old != text:
            h = exp.adir / "history"
            h.mkdir(exist_ok=True)
            stamp = datetime.datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y%m%d-%H%M%S")
            (h / f"{stamp}-{name}").write_text(old)
    p.write_text(text)
    done, codes = [], {}
    for u in exp.units():
        r = exp.unit_status(u["id"])
        if r.get("status") == "done":
            done.append(u["id"])
            c = (r.get("fingerprint") or {}).get("code", "unknown")
            codes[c] = codes.get(c, 0) + 1
    try:
        from .calibration import RUBRIC
        rubric = hashlib.sha1(RUBRIC.encode()).hexdigest()[:12]
    except Exception:
        rubric = ""
    val = getattr(exp, "validity", None) or {}
    man = {"stage": exp.id, "written": datetime.datetime.now().isoformat(timespec="seconds"), "interim": interim,
           "analysis_code": PV.code_hash(), "rubric_sha1": rubric, "params": exp.params,
           "design": PV.design_hash(exp.params), "units_expected": len(exp.units()), "units_done": len(done),
           "unit_code_versions": codes, "validity": val, "contributing_units": done}
    dump(exp.adir / ("analysis_manifest_interim.json" if interim else "analysis_manifest.json"), man)
    if val:
        dump(exp.adir / "validity.json", val)


def eligibility(df, rules):
    """Pre-specified instrument-validity rules -> (eligible mask, reasons per row).
    rules: {column: (op, threshold)} with op in {'>=', '<='}; a missing/NaN value fails the rule
    (unknown validity is not validity)."""
    import numpy as np
    import pandas as pd
    ok = pd.Series(True, index=df.index)
    why = pd.Series("", index=df.index)
    for col, (op, thr) in rules.items():
        v = pd.to_numeric(df[col], errors="coerce") if col in df else pd.Series(np.nan, index=df.index)
        good = (v >= thr) if op == ">=" else (v <= thr)
        good = good & v.notna()
        why = why.where(good, why + f"{col}{'<' if op == '>=' else '>'}{thr};")
        ok &= good
    return ok, why


def validity_summary(df, ok, why, by=None):
    out = {"rules_version": "2026-10-15", "units_done": int(len(df)), "units_eligible": int(ok.sum()),
           "units_excluded": int((~ok).sum()),
           "exclusion_reasons": {k: int(v) for k, v in why[~ok].str.split(";").explode().loc[lambda s: s != ""].value_counts().items()}}
    if by:
        g = pd_groupby_counts(df, ok, by)
        out["by_group"] = g
    return out


def pd_groupby_counts(df, ok, by):
    d = df.assign(_ok=ok.values)
    return {"|".join(map(str, k if isinstance(k, tuple) else (k,))): {"done": int(len(x)), "eligible": int(x._ok.sum())}
            for k, x in d.groupby(by)}


def dump(path, obj):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2, default=str)
