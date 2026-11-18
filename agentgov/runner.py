"""Daily session orchestration: time-boxed, budget-capped, resumable."""
from __future__ import annotations

import json
import multiprocessing as mp
import os
import time
import traceback
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait
from datetime import datetime
from typing import Any, Dict, List, Optional

from . import config as C
from . import models as M
from .experiments import REGISTRY
from .llm import FatalAPIError, GoClient, HTTPClient, Ledger, ModelUnavailable, RateLimited, RunContext, StopSession, today

DONE, GAVE_UP = "done", "gave_up"
MAX_ATTEMPTS = 5


# --------------------------------------------------------------------------- logging
class Log:
    def __init__(self, session_id):
        C.LOGS.mkdir(parents=True, exist_ok=True)
        self.path = C.LOGS / f"session-{session_id}.log"

    def __call__(self, *msg):
        line = f"[{datetime.now().strftime('%H:%M:%S')}] " + " ".join(str(m) for m in msg)
        print(line, flush=True)
        with open(self.path, "a") as f:
            f.write(line + "\n")


# --------------------------------------------------------------------------- environment
def build_env(mock: bool, log=print, offline_ok: bool = False):
    """Fetch the live catalogue and resolve the roster. Returns (settings, resolved, spec_base)."""
    S = C.settings()
    prov = C.provider(S)
    if mock:
        resolved = M.resolve(S, None)
    elif prov == "opencode_go":
        resolved = _build_env_go(S, log, offline_ok)
    else:
        cred = C.credentials()
        http = HTTPClient(cred["NEBIUS_BASE_URL"], cred["NEBIUS_API_KEY"], timeout=60)
        ids, waited = None, 0
        while ids is None:
            try:
                ids = M.fetch_live(http)
                log(f"catalogue: {len(ids)} live models at {cred['NEBIUS_BASE_URL']}")
            except Exception as e:
                code = getattr(e, "code", None)
                if code in (401, 403):
                    raise FatalAPIError(f"Nebius rejected the API key (HTTP {code}). Edit credentials/nebius.env.")
                # right after the Mac wakes the network is often not up yet: keep trying for up to 15 min
                if code is None and waited < 900 and not offline_ok:
                    log(f"network not ready ({e}); retrying in 30 s")
                    time.sleep(30)
                    waited += 30
                    continue
                if not offline_ok:
                    raise
                ids = (C.read_json(M.LIVE, {}) or {}).get("ids")
                log(f"catalogue fetch failed ({e}); using cached list")
        # 2026-10-20: some models live on a regional endpoint (roster `base_url`, e.g. us-north1). Their catalogues
        # are fetched too; a regional endpoint that fails leaves only its aliases unavailable, never the session.
        extra_bases = sorted({e.get("base_url") for e in (S.get("roster") or {}).values() if e.get("base_url")})
        for b in extra_bases:
            try:
                more = sorted({m.get("id") for m in HTTPClient(b, cred["NEBIUS_API_KEY"], timeout=60).models() if m.get("id")})
                log(f"catalogue: {len(more)} live models at {b}")
                ids = sorted(set(ids or []) | set(more))
            except Exception as e:
                log(f"catalogue fetch failed at {b} ({e}); its aliases stay unavailable this session")
        resolved = M.resolve(S, ids)
        C.write_json(M.RESOLVED, resolved)
    prices = {r["id"]: r["price"] for r in resolved.values() if r.get("id")}
    spec = {"mock": mock, "prices": prices, "default_price": S.get("default_price", [3.0, 15.0]),
            "profiles": C.read_json(M.PROFILES, {}) or {},
            "roster": {a: r["id"] for a, r in resolved.items() if r.get("id")},
            "slow_call_s": float(S["session"].get("slow_call_seconds", 25)),
            "slow_call_s_by_role": {k: float(v) for k, v in (S["session"].get("slow_call_seconds_by_role") or {}).items()},
            "daily_usd": C.budget_caps(S)[0], "monthly_usd": C.budget_caps(S)[1],
            "provider": prov}
    if prov == "opencode_go":
        spec["provider_cfg"] = C.provider_cfg(S)
        spec["base_url"] = C.credentials()["BASE_URL"]
        spec["api_by_model"] = {r["id"]: r.get("api", "chat") for r in resolved.values() if r.get("id")}
        spec["profiles"] = _go_profiles(S, resolved, spec["profiles"])
    return S, resolved, spec


def _build_env_go(S, log, offline_ok):
    """OpenCode Go catalogue + roster (2026-11-04). Same network-wait and auth rules as the Nebius path."""
    cred = C.credentials()
    http = GoClient(cred["BASE_URL"], cred["API_KEY"], timeout=60, cfg=C.provider_cfg(S))
    ids, waited = None, 0
    while ids is None:
        try:
            ids = M.fetch_live(http)
            log(f"catalogue: {len(ids)} live models at OpenCode Go {cred['BASE_URL']}")
        except Exception as e:
            code = getattr(e, "code", None)
            if code in (401, 403):
                raise FatalAPIError(f"OpenCode Go rejected the API key (HTTP {code}). Edit credentials/opencode_go.env.")
            if code is None and waited < 900 and not offline_ok:
                log(f"network not ready ({e}); retrying in 30 s")
                time.sleep(30)
                waited += 30
                continue
            if not offline_ok:
                raise
            ids = None
            log(f"catalogue fetch failed ({e}); assuming every mapped Go model is live")
            break
    resolved = M.resolve(S, ids)
    C.write_json(M.RESOLVED, resolved)
    return resolved


def _go_profiles(S, resolved, profiles):
    """Interface profiles for Go ids, inherited from the Nebius profile of the same alias (min_max_tokens, usable),
    with the Go roster's own extra_body when given (reasoning switches differ by provider). Recorded in manifests."""
    out = dict(profiles or {})
    roster = S.get("roster") or {}
    for alias, r in resolved.items():
        if not r.get("id") or r.get("provider") != "opencode_go":
            continue
        src_id = r.get("inherit_profile") or next((c for c in (roster.get(alias) or {}).get("candidates") or []
                                                   if c in out), None)
        base = dict(out.get(src_id) or {})
        prof = {"usable": base.get("usable", True), "min_max_tokens": int(base.get("min_max_tokens", 0) or 0),
                "extra_body": (r["extra_body"] if r.get("extra_body") is not None else (base.get("extra_body") or {})),
                "inherited_from": src_id, "provider": "opencode_go"}
        out[r["id"]] = prof
    return out


def plan_entries(only: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    out = []
    for e in (C.plan().get("experiments") or []):
        if only and e["id"] not in only:
            continue
        if not only and not e.get("enabled", False):
            continue
        out.append(e)
    return out


def make(entry, S, resolved, mock):
    cls = REGISTRY.get(entry["id"])
    return cls(entry.get("params") or {}, S, resolved, mock) if cls else None


def unit_state(exp, u):
    r = exp.unit_status(u["id"])
    st = r.get("status")
    if st == DONE:
        return DONE
    if st in ("error", "model_unavailable") and r.get("attempts", 0) >= MAX_ATTEMPTS:
        return GAVE_UP
    return "pending"


def _eligible_str(exp) -> str:
    """'eligible/done (excluded: reasons)' from the last analysis' validity.json, '-' when the stage has no rules."""
    v = C.read_json(exp.adir / "validity.json", None)
    if not v:
        return "-"
    rs = v.get("exclusion_reasons") or {}
    tail = (" (" + ", ".join(f"{k}: {n}" for k, n in list(rs.items())[:3]) + ")") if rs else ""
    if "units_done" not in v and "cells" in v:      # evaluator-level rules (A3): eligible cells, not units
        return f"{v.get('cells_eligible', 0)}/{v.get('cells', 0)} cells{tail}"
    return f"{v.get('units_eligible', 0)}/{v.get('units_done', 0)}{tail}"


def progress(S, resolved, mock) -> Dict[str, Any]:
    prog = {}
    done_ids = set()
    for e in C.plan().get("experiments") or []:
        exp = make(e, S, resolved, mock)
        if exp is None:
            prog[e["id"]] = {"status": "unknown_experiment"}
            continue
        if getattr(exp, "needs_build", False):
            prog[e["id"]] = {"status": "needs_build", "title": exp.title, "enabled": e.get("enabled", False)}
            continue
        units = exp.units()
        states = [unit_state(exp, u) for u in units]
        n_done, n_gu = states.count(DONE), states.count(GAVE_UP)
        from . import provenance as PV
        ph = PV.params_hash(exp.params)
        n_stale = 0
        code_versions = set()
        for u, st in zip(units, states):
            if st == DONE:
                fpr = exp.unit_status(u["id"]).get("fingerprint") or {}
                n_stale += int(PV.is_stale(exp.params, fpr))
                if fpr.get("code"):
                    code_versions.add(fpr["code"])
        complete = bool(units) and n_done + n_gu == len(units)
        if complete:
            done_ids.add(e["id"])
        prog[e["id"]] = {"status": "complete" if complete else ("empty" if not units else "pending"),
                         "title": exp.title, "level": exp.level, "enabled": e.get("enabled", False),
                         "units_done": n_done, "units_gave_up": n_gu, "units_total": len(units), "units_stale": n_stale,
                         "code_versions": sorted(code_versions),
                         "requires": exp.requires, "analysed": (exp.adir / "findings.md").exists(),
                         "eligible": _eligible_str(exp),
                         "estimate": exp.estimate() if units else {}}
    for k, v in prog.items():
        v["blocked_by"] = [r for r in v.get("requires", []) if r not in done_ids]
    return prog


# --------------------------------------------------------------------------- worker
def _run_unit(exp_id, params, S, resolved, mock, unit, spec):
    from . import config as C2  # noqa: F401  (spawned process)
    exp = REGISTRY[exp_id](params, S, resolved, mock)
    outdir = exp.unit_dir(unit["id"])
    outdir.mkdir(parents=True, exist_ok=True)
    prev = exp.unit_status(unit["id"])
    from . import provenance as PV
    rec = {"unit": unit, "attempts": prev.get("attempts", 0) + 1, "session": spec["session_id"],
           "started": datetime.now().isoformat(timespec="seconds"), "fingerprint": PV.fingerprint(exp)}
    try:
        C.write_json(outdir / "manifest.json", PV.manifest(exp, unit, spec))
    except Exception as e:  # provenance must never block a run
        rec["manifest_error"] = str(e)
    t0 = time.time()
    try:
        ctx = RunContext({**spec, "experiment": exp_id, "unit": unit["id"]})
        rec["summary"] = exp.run_unit(unit, ctx, outdir)
        rec["status"] = DONE
    except StopSession as e:
        rec["status"], rec["error"] = "stopped", str(e)
        rec["attempts"] -= 1                      # interruptions don't count as failures
    except FatalAPIError as e:
        rec["status"], rec["error"] = "fatal", str(e)
        rec["attempts"] -= 1
    except RateLimited as e:
        rec["status"], rec["error"] = "rate_limited", str(e)
        rec["attempts"] -= 1                      # provider usage window, not a failure of the unit
    except ModelUnavailable as e:
        rec["status"], rec["error"] = "model_unavailable", str(e)
    except Exception as e:
        rec["status"], rec["error"] = "error", f"{type(e).__name__}: {e}"
        rec["traceback"] = traceback.format_exc()[-4000:]
    rec["duration_s"] = round(time.time() - t0, 1)
    rec["finished"] = datetime.now().isoformat(timespec="seconds")
    C.write_json(outdir / "result.json", rec)
    return rec["status"], rec.get("error", "")


# --------------------------------------------------------------------------- session
def run_session(hours: float, mock: bool = False, only: Optional[List[str]] = None, workers: Optional[int] = None):
    C.ensure_dirs()
    S0 = C.settings()
    session_id = datetime.now().strftime("%Y%m%d-%H%M") + ("-mock" if mock else "")
    log = Log(session_id)
    lock = C.STATE_DIR / "session.lock"
    if lock.exists():
        info = C.read_json(lock, {}) or {}
        alive = True
        try:                                   # 2026-11-02 fix: a lock left by a session killed in a reboot/crash
            os.kill(int(info.get("pid", 0)), 0)  # blocked relaunches for up to 4 h; a dead pid means a stale lock
        except (ProcessLookupError, ValueError, TypeError):
            alive = False
        except PermissionError:
            alive = True
        if alive and time.time() - info.get("started", 0) < info.get("hours", 4) * 3600 + 1800:
            log(f"another session is running (since {info.get('started_h')}); exiting")
            return
        if not alive:
            log(f"stale session lock from {info.get('started_h')} (pid {info.get('pid')} not running); continuing")
    C.write_json(lock, {"pid": os.getpid(), "started": time.time(), "hours": hours,
                        "started_h": datetime.now().isoformat(timespec="minutes"), "session": session_id})
    start = time.time()
    sess = {"session": session_id, "mock": mock, "hours": hours, "start": datetime.now().isoformat(timespec="minutes"),
            "units": [], "completed_experiments": [], "stop_reason": "", "notes": []}
    try:
        if not mock and not C.has_key():
            sess["stop_reason"] = f"no API key: fill in {C.cred_file().relative_to(C.ROOT)}"
            log(sess["stop_reason"])
            return
        reserve = float(S0["session"].get("reserve_minutes", 10)) * 60
        S, resolved, spec = build_env(mock, log, offline_ok=False)
        spec.update({"session_id": session_id, "deadline": start + hours * 3600 - reserve})
        workers = workers or int(S["session"].get("workers", 4))
        ledger = Ledger()
        log(f"session {session_id}: {hours} h, {workers} workers, mock={mock}; spent today "
            f"${ledger.spend(today()):.2f} / ${spec['daily_usd']:.0f}, this month ${ledger.spend_month():.2f} / ${spec['monthly_usd']:.0f}")
        avail = [a for a, r in resolved.items() if r["available"]]
        log(f"roster available: {', '.join(avail) or 'none'}")
        stop = None
        for pass_no in range(3):
            n_before = len(sess["units"])
            for entry in plan_entries(only):
                if stop:
                    break
                exp = make(entry, S, resolved, mock)
                if exp is None:
                    log(f"unknown experiment id {entry['id']} in plan.yaml (skipped)")
                    continue
                if getattr(exp, "needs_build", False):
                    log(f"{exp.id}: not built yet (see ROADMAP.md)")
                    continue
                # 2026-11-04: stages are pinned to the provider their design was frozen on (default nebius), so a
                # provider switch never mixes serving stacks inside a stage and never re-analyses other stages
                if not mock and getattr(exp, "provider", "nebius") != spec.get("provider", "nebius"):
                    if pass_no == 0:
                        log(f"{exp.id}: pinned to provider {getattr(exp, 'provider', 'nebius')}; skipped under "
                            f"{spec.get('provider')}")
                    continue
                prog = progress(S, resolved, mock)
                blocked = [r for r in exp.requires if prog.get(r, {}).get("status") != "complete"]
                if blocked and not entry.get("ignore_requires") and not only:
                    log(f"{exp.id}: waiting for {', '.join(blocked)}")
                    continue
                # profiles may have been written by S0 earlier in this session
                spec["profiles"] = C.read_json(M.PROFILES, {}) or {}
                units = exp.units()
                if any(unit_state(exp, u) != DONE for u in units):
                    exp.prepare(None)          # may reset units by a pre-specified rule (S5b after A0), so before `pending`
                pending = [u for u in units if unit_state(exp, u) == "pending"]
                log(f"{exp.id}: {len(units) - len(pending)}/{len(units)} units done, {len(pending)} to run")
                if pending:
                    stop = _dispatch(exp, entry, S, resolved, mock, pending, spec, workers, log, sess)
                units_left = [u for u in exp.units() if unit_state(exp, u) == "pending"]
                ran_now = any(u["experiment"] == exp.id for u in sess["units"][n_before:])
                if units and not units_left and exp.id in sess["completed_experiments"] and not ran_now:
                    continue               # already analysed earlier this session (retry pass); nothing new to analyse
                if units and not units_left:
                    try:
                        from .experiments.base import write_findings
                        findings = exp.analyze()
                        write_findings(exp, findings)
                        if exp.id not in sess["completed_experiments"]:
                            sess["completed_experiments"].append(exp.id)
                        log(f"{exp.id}: complete and analysed")
                    except Exception as e:
                        log(f"{exp.id}: analysis failed: {e}")
                        sess["notes"].append(f"analysis of {exp.id} failed: {e}\n{traceback.format_exc()[-1500:]}")
                elif units_left and any(unit_state(exp, u) == DONE for u in units):
                    # partial analysis so the journal shows interim numbers (also when the session stopped on time:
                    # the reserve minutes cover it; S5b had no interim report on 2026-10-15 because of this)
                    try:
                        from .experiments.base import write_findings
                        write_findings(exp, exp.analyze(), interim=True)
                    except Exception:
                        pass
            # units that failed on a (possibly transient) model outage get another try later this session
            retry = [u for u in sess["units"][n_before:] if u["status"] in ("model_unavailable", "error")]
            wait_s = 600
            if stop or not retry or pass_no == 2 or spec["deadline"] - time.time() < wait_s + 900:
                break
            log(f"{len(retry)} units failed (model outage or error); retrying them in {wait_s // 60} min")
            time.sleep(wait_s)
        if not stop:
            sess["stop_reason"] = sess["stop_reason"] or "queue finished for today (nothing runnable left)"
        else:
            sess["stop_reason"] = stop
    except FatalAPIError as e:
        sess["stop_reason"] = f"fatal: {e}"
        log(sess["stop_reason"])
    except KeyboardInterrupt:
        sess["stop_reason"] = "interrupted by user"
    except Exception as e:
        sess["stop_reason"] = f"crashed: {type(e).__name__}: {e}"
        sess["notes"].append(traceback.format_exc()[-3000:])
        log(sess["stop_reason"])
    finally:
        sess["end"] = datetime.now().isoformat(timespec="minutes")
        sess["minutes"] = round((time.time() - start) / 60, 1)
        try:
            from .report import finalize_session
            finalize_session(sess, mock, log)
        finally:
            try:
                lock.unlink()
            except FileNotFoundError:
                pass


def _alias_of_model(model_id, resolved):
    """Roster alias bound to a raw model id (or the alias itself), else None."""
    for a, ent in (resolved or {}).items():
        if a == model_id or (ent or {}).get("id") == model_id:
            return a
    return None


def _unit_aliases(u):
    """All string values of a unit dict (one level of lists/dicts), to find every model alias it uses."""
    out = set()
    for v in u.values():
        if isinstance(v, str):
            out.add(v)
        elif isinstance(v, (list, tuple)):
            out.update(x for x in v if isinstance(x, str))
        elif isinstance(v, dict):
            out.update(x for x in v.values() if isinstance(x, str))
    return out


def _dispatch(exp, entry, S, resolved, mock, pending, spec, workers, log, sess):
    """Run pending units with a process pool; returns a stop reason or None."""
    ctxmp = mp.get_context("spawn")
    stop = None
    # round-robin across models so one slow model never occupies every worker
    by_alias = {}
    for u in pending:
        by_alias.setdefault(u.get("alias", ""), []).append(u)
    queue = []
    while any(by_alias.values()):
        for k in list(by_alias):
            if by_alias[k]:
                queue.append(by_alias[k].pop(0))
    slow = set()
    inflight = {}
    min_left = float(S["session"].get("min_minutes_to_start_unit", 3)) * 60
    with ProcessPoolExecutor(max_workers=workers, mp_context=ctxmp) as pool:
        while queue or inflight:
            while queue and len(inflight) < workers and not stop:
                if spec["deadline"] - time.time() < min_left:
                    stop = "session time is up"
                    break
                u = queue.pop(0)
                f = pool.submit(_run_unit, exp.id, entry.get("params") or {}, S, resolved, mock, u, spec)
                inflight[f] = u
            if not inflight:
                break
            done, _ = wait(list(inflight), return_when=FIRST_COMPLETED)
            for f in done:
                u = inflight.pop(f)
                try:
                    status, err = f.result()
                except Exception as e:
                    status, err = "error", f"worker crashed: {e}"
                sess["units"].append({"experiment": exp.id, "unit": u["id"], "status": status, "error": err})
                log(f"  {exp.id}/{u['id']}: {status}{(' - ' + err[:160]) if err else ''}")
                if status == "stopped" and not stop:
                    stop = err or "stopped"
                if status == "model_unavailable" and "too slow" in err and u.get("alias"):
                    slow.add(u["alias"])
                    n0 = len(queue)
                    queue[:] = [q for q in queue if q.get("alias") != u["alias"]]
                    log(f"  {u['alias']} is too slow right now; its {n0 - len(queue)} queued units wait for the next session")
                # 2026-11-03 review: the slow model may hold a fixed role (e.g. S5i's judge kimi_k3) that is not the
                # unit's 'alias'; hold back every queued unit that names that model in any field.
                if status == "model_unavailable" and "too slow" in err:
                    slow_alias = _alias_of_model(err.split(" too slow", 1)[0].strip(), resolved)
                    if slow_alias:
                        n0 = len(queue)
                        queue[:] = [q for q in queue if slow_alias not in _unit_aliases(q)]
                        if n0 - len(queue):
                            log(f"  {slow_alias} (any role) is too slow right now; {n0 - len(queue)} more queued units "
                                f"wait for the next session")
                if status == "rate_limited":
                    rl_alias = _alias_of_model(err.split(" rate-limited", 1)[0].strip(), resolved)
                    if rl_alias:
                        n0 = len(queue)
                        queue[:] = [q for q in queue if rl_alias not in _unit_aliases(q)]
                        log(f"  {rl_alias} usage window exhausted; {n0 - len(queue)} queued units wait")
                if status == "fatal":
                    stop = f"fatal: {err}"
            if stop:
                queue.clear()
    return stop
