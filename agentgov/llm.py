"""Nebius Token Factory client with disk cache, usage ledger, budget and deadline guards.

All model access in the pipeline goes through `ModelLLM.generate(prompt, system, cache_key)`,
which is call-compatible with the `NebiusLLM` classes in both original notebooks, so the
upstream simulators run unchanged.

* Every live call is written to data/ledger.sqlite (tokens, cost, latency, experiment, unit).
* Every response is cached in data/cache.nosync/llm_cache.sqlite keyed on
  (model, temperature, max_tokens, extra params, system, prompt, cache_key, salt), so an
  interrupted session resumes for free and paired conditions share common random numbers.
* Reasoning traces (<think>...</think>) are stripped before the text reaches upstream parsers.
* `Guard` stops a session cleanly when the deadline or a budget cap is reached.
"""
from __future__ import annotations

import hashlib
import json
import random
import re
import sqlite3
import ssl
import time
import urllib.error
import urllib.request
from datetime import datetime
from typing import Any, Dict, List, Optional

from . import config as C


class StopSession(BaseException):
    """Deadline or budget reached. BaseException so upstream `except Exception` never swallows it."""


class FatalAPIError(BaseException):
    """Authentication / account problem: no point continuing the session."""


class ModelUnavailable(Exception):
    """A specific model keeps failing (404, persistent 5xx); the unit is skipped."""


_THINK = re.compile(r"<(think|thinking|reasoning)>.*?</\1>", re.S | re.I)
_OPEN = re.compile(r"^.*?</(think|thinking|reasoning)>", re.S | re.I)


def strip_reasoning(text: str) -> str:
    t = _THINK.sub(" ", text or "")
    if re.search(r"</(think|thinking|reasoning)>", t, re.I):
        t = _OPEN.sub(" ", t)
    return t.strip()


def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


# --------------------------------------------------------------------------- storage
def _connect(path) -> sqlite3.Connection:
    con = sqlite3.connect(str(path), timeout=60)
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA synchronous=NORMAL")
    return con


class Ledger:
    def __init__(self, path=None):
        self.path = path or C.LEDGER_DB
        con = _connect(self.path)
        con.execute("""CREATE TABLE IF NOT EXISTS calls(
            ts REAL, day TEXT, session TEXT, experiment TEXT, unit TEXT, role TEXT,
            model TEXT, prompt_tokens INTEGER, completion_tokens INTEGER,
            reasoning_tokens INTEGER, cost_usd REAL, latency_s REAL, cached INTEGER,
            mock INTEGER, status TEXT, finish_reason TEXT)""")
        con.execute("CREATE INDEX IF NOT EXISTS calls_day ON calls(day)")
        cols = {r[1] for r in con.execute("PRAGMA table_info(calls)")}
        if "cost_equiv_usd" not in cols:     # logical cost: what the call would cost uncached (token x price)
            con.execute("ALTER TABLE calls ADD COLUMN cost_equiv_usd REAL")
        con.commit(); con.close()

    def record(self, **row):
        con = _connect(self.path)
        cols = ",".join(row)
        con.execute(f"INSERT INTO calls({cols}) VALUES ({','.join('?' * len(row))})", list(row.values()))
        con.commit(); con.close()

    def spend(self, day: Optional[str] = None) -> float:
        con = _connect(self.path)
        if day:
            r = con.execute("SELECT COALESCE(SUM(cost_usd),0) FROM calls WHERE day=? AND mock=0", (day,)).fetchone()
        else:
            r = con.execute("SELECT COALESCE(SUM(cost_usd),0) FROM calls WHERE mock=0").fetchone()
        con.close()
        return float(r[0])

    def spend_month(self, month: Optional[str] = None) -> float:
        month = month or datetime.now().strftime("%Y-%m")
        con = _connect(self.path)
        r = con.execute("SELECT COALESCE(SUM(cost_usd),0) FROM calls WHERE day LIKE ? AND mock=0", (month + "%",)).fetchone()
        con.close()
        return float(r[0])

    def summary(self, where: str = "1=1", params=()) -> List[Dict[str, Any]]:
        con = _connect(self.path)
        cur = con.execute(f"""SELECT model, COUNT(*), SUM(cached), SUM(prompt_tokens), SUM(completion_tokens),
                              ROUND(SUM(cost_usd),4), ROUND(AVG(CASE WHEN cached=0 THEN latency_s END),2),
                              SUM(CASE WHEN status!='ok' THEN 1 ELSE 0 END), ROUND(SUM(COALESCE(cost_equiv_usd, cost_usd)),4)
                              FROM calls WHERE {where} GROUP BY model ORDER BY 6 DESC""", params)
        keys = ["model", "calls", "cached", "prompt_tokens", "completion_tokens", "cost_usd", "mean_latency_s", "errors",
                "cost_equiv_usd"]
        out = [dict(zip(keys, r)) for r in cur.fetchall()]
        con.close()
        return out


class Cache:
    def __init__(self, path=None):
        self.path = path or (C.CACHE_DIR / "llm_cache.sqlite")
        con = _connect(self.path)
        con.execute("CREATE TABLE IF NOT EXISTS cache(k TEXT PRIMARY KEY, text TEXT, meta TEXT, ts REAL)")
        con.commit(); con.close()

    def get(self, k):
        con = _connect(self.path)
        r = con.execute("SELECT text, meta FROM cache WHERE k=?", (k,)).fetchone()
        con.close()
        return (r[0], json.loads(r[1] or "{}")) if r else None

    def put(self, k, text, meta):
        con = _connect(self.path)
        con.execute("INSERT OR REPLACE INTO cache VALUES (?,?,?,?)", (k, text, json.dumps(meta), time.time()))
        con.commit(); con.close()


# --------------------------------------------------------------------------- guard
class Guard:
    """Shared stop conditions. Checked before every live call."""

    def __init__(self, deadline: float, daily_usd: float, total_usd: float, ledger: Ledger):
        self.deadline, self.daily_usd, self.total_usd, self.ledger = deadline, daily_usd, total_usd, ledger
        self._last = 0.0
        self._ok = True

    def check(self):
        now = time.time()
        if now >= self.deadline:
            raise StopSession("session time is up")
        if now - self._last > 5:            # budget query at most every 5 s per process
            self._last = now
            if self.ledger.spend(today()) >= self.daily_usd:
                raise StopSession(f"daily budget ${self.daily_usd:.2f} reached")
            if self.ledger.spend_month() >= self.total_usd:
                raise StopSession(f"monthly budget ${self.total_usd:.2f} reached")


# --------------------------------------------------------------------------- http
def _ssl_ctx():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()


class HTTPClient:
    def __init__(self, base_url: str, api_key: str, timeout: float = 120.0):
        self.base = base_url.rstrip("/") + "/"
        self.key = api_key
        self.timeout = timeout
        self.ctx = _ssl_ctx()

    def _req(self, path, payload=None):
        data = json.dumps(payload).encode() if payload is not None else None
        req = urllib.request.Request(self.base + path, data=data, method="POST" if data else "GET",
                                     headers={"Authorization": f"Bearer {self.key}",
                                              "Content-Type": "application/json",
                                              "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=self.timeout, context=self.ctx) as r:
            return json.loads(r.read().decode())

    def models(self) -> List[Dict[str, Any]]:
        return self._req("models").get("data", [])

    def chat(self, model, messages, temperature, max_tokens, extra=None) -> Dict[str, Any]:
        payload = {"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
        if extra:
            payload.update(extra)
        return self._req("chat/completions", payload)


def http_error_code(e) -> Optional[int]:
    return getattr(e, "code", None)


# --------------------------------------------------------------------------- model wrapper
class ModelLLM:
    """Drop-in for the notebooks' NebiusLLM: .generate(prompt, system=None, cache_key=None) -> str."""

    def __init__(self, ctx: "RunContext", model: str, role: str = "default", temperature: float = 0.25,
                 max_tokens: int = 400, salt: str = "", cache_enabled: bool = True,
                 extra: Optional[Dict[str, Any]] = None, use_profile: bool = True):
        self.ctx, self.model, self.role = ctx, model, role
        self.temperature = temperature
        prof = ctx.model_profile(model) if use_profile else {}
        self.max_tokens = max(max_tokens, int(prof.get("min_max_tokens", 0)))
        self.extra = extra if extra is not None else (prof.get("extra_body") or {})
        self.salt, self.cache_enabled = salt, cache_enabled
        self.consecutive_errors = 0
        self._lat: List[float] = []
        self._stats = {"calls": 0, "cached": 0, "errors": 0, "role": role, "model": model,
                       "prompt_tokens": 0, "completion_tokens": 0, "cost_usd": 0.0,
                       # logical accounting: every call incl. cache hits, at observed token usage x list price
                       "logical_calls": 0, "logical_prompt_tokens": 0, "logical_completion_tokens": 0,
                       "cost_equiv_usd": 0.0}
        self.last_meta: Dict[str, Any] = {}

    # upstream compatibility -------------------------------------------------
    @property
    def stats(self):
        return dict(self._stats)

    @property
    def call_count(self):
        return self._stats["calls"]

    def generate(self, prompt: str, system: Optional[str] = None, cache_key: Optional[str] = None) -> str:
        msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
        return self.chat(msgs, cache_key=cache_key)

    # core -------------------------------------------------------------------
    def _key(self, msgs, cache_key):
        blob = json.dumps([self.model, self.temperature, self.max_tokens, self.extra, msgs,
                           cache_key or "", self.salt], sort_keys=True)
        return hashlib.sha256(blob.encode()).hexdigest()

    def chat(self, msgs, cache_key=None) -> str:
        ctx = self.ctx
        k = self._key(msgs, cache_key)
        if self.cache_enabled:
            hit = ctx.cache.get(k)
            if hit is not None:
                self._stats["cached"] += 1
                self.last_meta = {**hit[1], "cached": True}
                self._logical(hit[1], cached=True)
                return hit[0]
        ctx.guard.check()
        if ctx.mock:
            text, meta = ctx.mock_llm.respond(msgs, self.model)
        else:
            text, meta = self._live(msgs)
        if meta.get("status") == "ok" and self.cache_enabled:
            ctx.cache.put(k, text, meta)
        self.last_meta = meta
        if ctx.mock:
            self._logical(meta, cached=False, record=True)
        return text

    def _logical(self, meta, cached, record=None):
        """Count a logical call. Cache hits are written to the ledger (cached=1, cost 0, cost_equiv from tokens)."""
        pt, ct = int(meta.get("prompt_tokens") or 0), int(meta.get("completion_tokens") or 0)
        eq = self.ctx.price(self.model, pt, ct)
        s = self._stats
        s["logical_calls"] += 1
        s["logical_prompt_tokens"] += pt
        s["logical_completion_tokens"] += ct
        s["cost_equiv_usd"] += eq
        if cached or record:
            self.ctx.ledger.record(ts=time.time(), day=today(), session=self.ctx.session_id,
                                   experiment=self.ctx.experiment, unit=self.ctx.unit, role=self.role,
                                   model=self.model, prompt_tokens=pt, completion_tokens=ct,
                                   reasoning_tokens=int(meta.get("reasoning_tokens") or 0), cost_usd=0.0,
                                   cost_equiv_usd=eq, latency_s=0.0, cached=int(bool(cached)),
                                   mock=int(self.ctx.mock), status="ok", finish_reason="cache" if cached else "mock")

    def _live(self, msgs):
        ctx = self.ctx
        attempts, wait = 6, 2.0
        for a in range(attempts):
            t0 = time.time()
            status, finish = "ok", ""
            try:
                r = ctx.http_for(self.model).chat(self.model, msgs, self.temperature, self.max_tokens, self.extra)
                ch = (r.get("choices") or [{}])[0]
                msg = ch.get("message") or {}
                raw = msg.get("content") or ""
                finish = ch.get("finish_reason") or ""
                usage = r.get("usage") or {}
                pt, ct = int(usage.get("prompt_tokens") or 0), int(usage.get("completion_tokens") or 0)
                rt = int(((usage.get("completion_tokens_details") or {}).get("reasoning_tokens")) or 0)
                text = strip_reasoning(raw)
                if not text:
                    status = "empty"          # typically: reasoning consumed the token budget
                cost = ctx.price(self.model, pt, ct)
                lat = time.time() - t0
                self._account(pt, ct, rt, cost, lat, status, finish)
                if status == "ok":
                    self.consecutive_errors = 0
                self._watch(lat)
                return (text if text else '{"error": "empty completion"}'), {
                    "status": status, "prompt_tokens": pt, "completion_tokens": ct, "reasoning_tokens": rt,
                    "latency_s": round(lat, 3), "finish_reason": finish, "has_reasoning": raw != text}
            except urllib.error.HTTPError as e:
                code = http_error_code(e)
                body = ""
                try:
                    body = e.read().decode()[:300]
                except Exception:
                    pass
                self._account(0, 0, 0, 0.0, time.time() - t0, f"http_{code}", body[:60])
                if code in (401, 402, 403):
                    raise FatalAPIError(f"HTTP {code} from Nebius ({body}). Check the API key / account credit.")
                # Nebius has returned transient 404 "model does not exist" for live models (2026-10-13,
                # Qwen3.5-397B): retry a 404 twice with backoff before giving up on the unit.
                if code in (400, 422) or (code == 404 and a >= 2):
                    raise ModelUnavailable(f"{self.model}: HTTP {code} {body}")
            except (urllib.error.URLError, TimeoutError, ConnectionError, OSError, json.JSONDecodeError) as e:
                self._account(0, 0, 0, 0.0, time.time() - t0, "net_error", str(e)[:60])
                self._watch(time.time() - t0)
            self.consecutive_errors += 1
            if self.consecutive_errors >= 25:
                raise ModelUnavailable(f"{self.model}: 25 consecutive failures")
            ctx.guard.check()
            time.sleep(wait + random.random())
            wait = min(wait * 2, 60)
        return '{"error": "LLM call failed"}', {"status": "failed"}

    def _watch(self, lat):
        """Give up on a model whose live calls are too slow to finish a unit in a session."""
        self._lat.append(lat)
        self._lat = self._lat[-20:]
        # role-specific limit (2026-10-15): a long-output reasoning attacker is not a short-output evaluator
        limit = float((self.ctx.spec.get("slow_call_s_by_role") or {}).get(self.role, self.ctx.spec.get("slow_call_s", 25)))
        if len(self._lat) >= 10:
            med = sorted(self._lat)[len(self._lat) // 2]
            if med > limit:
                raise ModelUnavailable(f"{self.model} too slow: median {med:.0f}s per call over the last "
                                       f"{len(self._lat)} calls (limit {limit:.0f}s)")

    def _account(self, pt, ct, rt, cost, lat, status, finish):
        s = self._stats
        s["calls"] += 1
        s["prompt_tokens"] += pt; s["completion_tokens"] += ct; s["cost_usd"] += cost
        if status == "ok":
            s["logical_calls"] += 1
            s["logical_prompt_tokens"] += pt; s["logical_completion_tokens"] += ct; s["cost_equiv_usd"] += cost
        if status != "ok":
            s["errors"] += 1
        self.ctx.ledger.record(ts=time.time(), day=today(), session=self.ctx.session_id,
                               experiment=self.ctx.experiment, unit=self.ctx.unit, role=self.role,
                               model=self.model, prompt_tokens=pt, completion_tokens=ct,
                               reasoning_tokens=rt, cost_usd=cost, cost_equiv_usd=cost, latency_s=lat, cached=0,
                               mock=int(self.ctx.mock), status=status, finish_reason=finish)


# --------------------------------------------------------------------------- context
class RunContext:
    """Everything a worker needs; rebuilt inside each worker process from a plain dict."""

    def __init__(self, spec: Dict[str, Any]):
        self.spec = spec
        self.session_id = spec["session_id"]
        self.mock = bool(spec.get("mock"))
        self.experiment = spec.get("experiment", "")
        self.unit = spec.get("unit", "")
        self.ledger = Ledger()
        self.cache = Cache(C.CACHE_DIR / ("mock_cache.sqlite" if self.mock else "llm_cache.sqlite"))
        self.guard = Guard(spec["deadline"], spec["daily_usd"], spec.get("monthly_usd", spec.get("total_usd", 1000.0)), self.ledger)
        self.prices = spec.get("prices", {})
        self.default_price = spec.get("default_price", [3.0, 15.0])
        self.profiles = spec.get("profiles", {})
        self.roster = spec.get("roster", {})
        self.http = None
        self._http_by_model: Dict[str, Any] = {}
        if not self.mock:
            cred = C.credentials()
            self.http = HTTPClient(cred["NEBIUS_BASE_URL"], cred["NEBIUS_API_KEY"])
            # models on a regional endpoint (roster `base_url`); same API key
            for ent in (C.settings().get("roster") or {}).values():
                if ent.get("base_url"):
                    cl = HTTPClient(ent["base_url"], cred["NEBIUS_API_KEY"])
                    for mid in ent.get("candidates") or []:
                        self._http_by_model[mid] = cl
        from .mock import MockResponder
        self.mock_llm = MockResponder(seed=hash(self.unit) % 10_000)

    def http_for(self, model):
        return self._http_by_model.get(model, self.http)

    def price(self, model, pt, ct) -> float:
        pin, pout = self.prices.get(model, self.default_price)
        return (pt * pin + ct * pout) / 1e6

    def model_profile(self, model) -> Dict[str, Any]:
        return self.profiles.get(model, {})

    def resolve(self, alias_or_id: str) -> str:
        """Roster alias -> live model id (ids pass through)."""
        r = self.roster.get(alias_or_id)
        return r if isinstance(r, str) and r else alias_or_id

    def llm(self, alias_or_id, role="default", **kw) -> ModelLLM:
        return ModelLLM(self, self.resolve(alias_or_id), role=role, **kw)
