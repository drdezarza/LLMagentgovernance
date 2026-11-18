"""Model catalogue discovery and roster resolution.

settings.yaml lists a roster of aliases, each with candidate model ids in preference order.
At session start the live catalogue (GET /v1/models) is fetched and each alias is bound to the
first candidate that exists. Experiments refer to aliases or to groups of aliases, never to raw
ids, so a renamed or retired endpoint only needs a settings edit.
"""
from __future__ import annotations

import re
import time
from typing import Any, Dict, List

from . import config as C

RESOLVED = C.CATALOG_DIR / "resolved_roster.json"
LIVE = C.CATALOG_DIR / "models_live.json"
PROFILES = C.CATALOG_DIR / "model_profiles.json"


def fetch_live(http) -> List[str]:
    data = http.models()
    ids = sorted({m.get("id") for m in data if m.get("id")})
    C.write_json(LIVE, {"fetched": time.strftime("%Y-%m-%d %H:%M:%S"), "n": len(ids), "ids": ids, "raw": data})
    return ids


GO_PREFIX = "opencode_go/"       # internal ids of OpenCode Go models carry this prefix (ledger, cache, prices)


def resolve(settings: Dict[str, Any], live_ids: List[str] | None) -> Dict[str, Dict[str, Any]]:
    """alias -> {id, price, tier, available}. With live_ids=None (mock/offline) the first candidate wins."""
    if C.provider(settings) == "opencode_go":
        return resolve_go(settings, live_ids)
    out = {}
    lower = {i.lower(): i for i in (live_ids or [])}
    for alias, ent in (settings.get("roster") or {}).items():
        cands = ent.get("candidates") or []
        chosen = None
        if live_ids is None:
            chosen = cands[0] if cands else None
        else:
            for c in cands:
                if c.lower() in lower:
                    chosen = lower[c.lower()]; break
            if not chosen and ent.get("pattern"):
                rx = re.compile(ent["pattern"], re.I)
                hits = [i for i in live_ids if rx.search(i)]
                chosen = hits[0] if hits else None
        out[alias] = {"id": chosen, "available": chosen is not None,
                      "price": ent.get("price", settings.get("default_price", [3.0, 15.0])),
                      "tier": ent.get("tier", ""), "note": ent.get("note", ""),
                      "base_url": ent.get("base_url") or None}
    return out


def resolve_go(settings: Dict[str, Any], live_ids: List[str] | None) -> Dict[str, Dict[str, Any]]:
    """OpenCode Go roster (settings providers.opencode_go.roster: alias -> {id, api, price, extra_body}).

    Aliases of the main roster that Go does not serve are returned as unavailable, so nothing is dispatched to them.
    Resolved ids are prefixed with GO_PREFIX so ledger rows, cache keys and profiles never mix with Nebius ones."""
    go = (settings.get("providers") or {}).get("opencode_go") or {}
    groster = go.get("roster") or {}
    live = {i.lower() for i in (live_ids or [])}
    out = {}
    for alias in list((settings.get("roster") or {}).keys()) + [a for a in groster if a not in (settings.get("roster") or {})]:
        ent = groster.get(alias)
        if not ent or not ent.get("id"):
            out[alias] = {"id": None, "available": False, "price": settings.get("default_price", [3.0, 15.0]),
                          "tier": "", "note": "not served by OpenCode Go", "base_url": None, "provider": "opencode_go"}
            continue
        raw = str(ent["id"])
        ok = live_ids is None or raw.lower() in live
        out[alias] = {"id": GO_PREFIX + raw if ok else None, "available": ok,
                      "price": ent.get("price", settings.get("default_price", [3.0, 15.0])),
                      "tier": ent.get("tier", ""), "note": ent.get("note", ""), "base_url": None,
                      "provider": "opencode_go", "api": ent.get("api", "chat"),
                      "extra_body": ent.get("extra_body"), "inherit_profile": ent.get("inherit_profile")}
    return out


def group(settings: Dict[str, Any], resolved: Dict[str, Dict[str, Any]], name_or_list) -> List[str]:
    """Expand a group name (or explicit list) to the aliases that are available and usable."""
    if isinstance(name_or_list, str):
        aliases = (settings.get("groups") or {}).get(name_or_list, [name_or_list])
    else:
        aliases = list(name_or_list)
    profiles = C.read_json(PROFILES, {}) or {}
    out = []
    for a in aliases:
        r = resolved.get(a)
        if not r or not r["available"]:
            continue
        if profiles.get(r["id"], {}).get("usable") is False:
            continue
        out.append(a)
    return out


def first_available(settings, resolved, aliases) -> str | None:
    g = group(settings, resolved, aliases)
    return g[0] if g else None
