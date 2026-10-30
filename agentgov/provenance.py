"""Run provenance: what exactly produced a unit's result.

Every unit writes manifest.json next to result.json, and result.json carries a fingerprint
{params, code, config}. A unit already 'done' under different experiment params is reported as STALE
(state/NEXT.md, `agentgov status`) instead of silently counting as current: re-run it with
`python -m agentgov retry <STAGE> --stale` or give the changed design a new stage id.
"""
from __future__ import annotations

import hashlib
import json
import platform
import sys
from functools import lru_cache
from typing import Any, Dict

from . import config as C


def _h(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]


@lru_cache(maxsize=1)
def code_hash() -> str:
    h = hashlib.sha256()
    for p in sorted((C.ROOT / "agentgov").rglob("*.py")):
        h.update(str(p.relative_to(C.ROOT)).encode())
        h.update(p.read_bytes())
    return h.hexdigest()[:16]


def params_hash(params: Dict[str, Any]) -> str:
    return _h(params)


def config_hash() -> str:
    try:
        return _h([C.settings(), C.plan()])
    except Exception:
        return ""


def _versions():
    out = {"python": sys.version.split()[0], "platform": platform.platform()}
    for m in ("numpy", "pandas", "networkx", "scipy", "matplotlib"):
        try:
            out[m] = __import__(m).__version__
        except Exception:
            pass
    return out


def fingerprint(exp) -> Dict[str, str]:
    return {"params": params_hash(exp.params), "design": design_hash(exp.params), "code": code_hash(),
            "config": config_hash()}


def manifest(exp, unit, spec) -> Dict[str, Any]:
    roster = spec.get("roster", {})
    return {
        "experiment": exp.id, "unit": unit, "params": exp.params, "fingerprint": fingerprint(exp),
        "session": spec.get("session_id"), "mock": spec.get("mock"),
        "roster": roster,                                   # alias -> resolved live model id at session start
        "model_profiles": {m: spec.get("profiles", {}).get(m) for m in set(roster.values())
                           if m in spec.get("profiles", {})},
        "prices_usd_per_1M": spec.get("prices", {}),
        "budget": {"daily": spec.get("daily_usd"), "monthly": spec.get("monthly_usd")},
        "versions": _versions(),
    }


# Keys that only enumerate units (raising them ADDS units; it does not change the design of existing ones).
UNIT_LIST_KEYS = ("seeds", "train_seeds", "heldout_seeds")
# Lists of aliases where each alias is its own unit and no other unit depends on the list (A1/A2 `models`, A3
# `outside_judges`). Appending to them adds units; they stay in the design hash so a reorder or removal is still stale.
APPENDABLE_MODEL_KEYS = ("models", "outside_judges")


def design_hash(params: Dict[str, Any]) -> str:
    return _h({k: v for k, v in params.items() if k not in UNIT_LIST_KEYS})


def is_stale(params: Dict[str, Any], fp: Dict[str, Any]) -> bool:
    """A done unit is stale when its design differs from the current params. Units stamped before `design` existed
    are matched against the current params with each seed list truncated to a prefix (seeds were appended)."""
    if not fp:
        return False
    if fp.get("design"):
        if fp["design"] == design_hash(params):
            return False
        # 2026-10-21: appending a model / outside judge to a stage only ADDS units (one unit per alias); a done unit is
        # not stale if its design equals the current one with such a list truncated to a prefix.
        app = {k: list(params[k]) for k in APPENDABLE_MODEL_KEYS if isinstance(params.get(k), (list, tuple))}
        if app:
            import itertools
            for ks in itertools.product(*[range(1, len(v) + 1) for v in app.values()]):
                trial = dict(params)
                for (k, v), n in zip(app.items(), ks):
                    trial[k] = v[:n]
                if design_hash(trial) == fp["design"]:
                    return False
        return True
    old = fp.get("params")
    if not old or old == params_hash(params):
        return False
    lists = {k: list(params[k]) for k in UNIT_LIST_KEYS + APPENDABLE_MODEL_KEYS if isinstance(params.get(k), (list, tuple))}
    if not lists:
        return True
    import itertools
    for ks in itertools.product(*[range(1, len(v) + 1) for v in lists.values()]):
        trial = dict(params)
        for (k, v), n in zip(lists.items(), ks):
            trial[k] = v[:n]
        if params_hash(trial) == old:
            return False
    return True
