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


PROVIDERS = ("nebius", "opencode_go")
GO_CRED_FILE = ROOT / "credentials" / "opencode_go.env"


def provider(S=None) -> str:
    """Active API provider (settings `provider`, env AGENTGOV_PROVIDER wins). Default nebius.
    Added 2026-11-04 (user request): OpenCode Go as a stand-in while Nebius billing is halted."""
    p = os.environ.get("AGENTGOV_PROVIDER") or ((S or settings()).get("provider") or "nebius")
    p = str(p).strip().lower()
    if p not in PROVIDERS:
        raise ValueError(f"unknown provider {p!r} in settings.yaml (use one of {PROVIDERS})")
    return p


def provider_cfg(S=None) -> Dict[str, Any]:
    """Settings block of the active provider ({} for nebius, whose settings are the top-level roster)."""
    S = S or settings()
    p = provider(S)
    return {} if p == "nebius" else dict(((S.get("providers") or {}).get(p) or {}))


def _read_env(path) -> Dict[str, str]:
    out: Dict[str, str] = {}
    if path.exists():
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def credentials() -> Dict[str, str]:
    """Credentials of the active provider (env vars take precedence).

    Always returns the keys API_KEY and BASE_URL for the active provider, plus PROVIDER. For nebius the historical
    NEBIUS_API_KEY / NEBIUS_BASE_URL keys are kept as well."""
    S = settings()
    p = provider(S)
    if p == "nebius":
        out = _read_env(CRED_FILE)
        for k in ("NEBIUS_API_KEY", "NEBIUS_BASE_URL"):
            if os.environ.get(k):
                out[k] = os.environ[k]
        out.setdefault("NEBIUS_BASE_URL", "https://api.tokenfactory.nebius.com/v1/")
        out["API_KEY"], out["BASE_URL"] = out.get("NEBIUS_API_KEY", ""), out["NEBIUS_BASE_URL"]
    else:
        out = _read_env(GO_CRED_FILE)
        for k in ("OPENCODE_GO_API_KEY", "OPENCODE_GO_BASE_URL"):
            if os.environ.get(k):
                out[k] = os.environ[k]
        out.setdefault("OPENCODE_GO_BASE_URL", provider_cfg(S).get("base_url") or "https://opencode.ai/inference/go/")
        out["API_KEY"], out["BASE_URL"] = out.get("OPENCODE_GO_API_KEY", ""), out["OPENCODE_GO_BASE_URL"]
    out["PROVIDER"] = p
    return out


def cred_file(S=None):
    return CRED_FILE if provider(S) == "nebius" else GO_CRED_FILE


def has_key() -> bool:
    k = credentials().get("API_KEY", "")
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
