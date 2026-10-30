"""Paths, settings, plan and credentials for the AGENT-GOV pipeline."""
from __future__ import annotations

import json
import os
import pathlib
from typing import Any, Dict

import yaml

ROOT = pathlib.Path(os.environ.get("AGENTGOV_ROOT", pathlib.Path(__file__).resolve().parents[1]))

CONFIG_DIR = ROOT / "config"
CRED_FILE = ROOT / "credentials" / "nebius.env"
DATA = ROOT / "data"
RUNS = DATA / "runs"
CATALOG_DIR = DATA / "catalog"
CACHE_DIR = DATA / "cache.nosync"          # ".nosync" keeps iCloud from syncing it
LEDGER_DB = DATA / "ledger.sqlite"
STATE_DIR = ROOT / "state"
JOURNAL = ROOT / "journal"
REPORTS = ROOT / "reports"
LOGS = ROOT / "logs"


def ensure_dirs() -> None:
    for p in (DATA, RUNS, CATALOG_DIR, CACHE_DIR, STATE_DIR, JOURNAL, REPORTS, LOGS):
        p.mkdir(parents=True, exist_ok=True)


def load_yaml(name: str) -> Dict[str, Any]:
    with open(CONFIG_DIR / name) as f:
        return yaml.safe_load(f) or {}


def settings() -> Dict[str, Any]:
    return load_yaml("settings.yaml")


def plan() -> Dict[str, Any]:
    return load_yaml("plan.yaml")


def budget_caps(S=None, day=None):
    """(daily_usd, monthly_usd). A per-day override in config/budget_overrides.yaml replaces the daily cap."""
    from datetime import datetime
    S = S or settings()
    b = S.get("budget", {}) or {}
    day = day or datetime.now().strftime("%Y-%m-%d")
    daily = float(b.get("daily_usd", 30))
    monthly = float(b.get("monthly_usd", b.get("total_usd", 1000)))
    f = CONFIG_DIR / "budget_overrides.yaml"
    if f.exists():
        ov = (load_yaml("budget_overrides.yaml") or {}).get("days") or {}
        if str(day) in {str(k) for k in ov}:
            daily = float({str(k): v for k, v in ov.items()}[str(day)])
    return daily, monthly


def credentials() -> Dict[str, str]:
    """Read KEY=VALUE lines from credentials/nebius.env (env vars take precedence)."""
    out: Dict[str, str] = {}
    if CRED_FILE.exists():
        for line in CRED_FILE.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip().strip('"').strip("'")
    for k in ("NEBIUS_API_KEY", "NEBIUS_BASE_URL"):
        if os.environ.get(k):
            out[k] = os.environ[k]
    out.setdefault("NEBIUS_BASE_URL", "https://api.tokenfactory.nebius.com/v1/")
    return out


def has_key() -> bool:
    k = credentials().get("NEBIUS_API_KEY", "")
    return bool(k) and not k.startswith("PASTE")


def read_json(path, default=None):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return default


def write_json(path, obj) -> None:
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=2, default=str)
    os.replace(tmp, path)
