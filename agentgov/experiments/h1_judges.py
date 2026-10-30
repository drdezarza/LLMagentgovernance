"""A4 — candidate judges against the independent human reference (built 2026-10-21 in chat, user request).

H1 gave a two-annotator reference (2026-10-23: both annotators used MiniMax-M3 assistance, per the user; see
reports/labeling_v2/PROVENANCE_CORRECTION.json) on 78 blinded messages (S3b / S5b / S7b, hard and ordinary strata, inclusion
probabilities recorded), but it could only score the verdicts already stored with each item (the primary judge of
that item's stage). A4 has every candidate judge family label the same 78 texts with the two A2 prompts (strict
production rule and frozen rubric), so each judge, including families new to the programme (muse_spark), gets an
error estimate against independent human labels, not only against other models.

Units: judge alias x prompt. Items: reports/labeling_v2/items.csv (text only, as the pipeline's judges see it; the
annotators' context column is not shown, as in A2). Domain: S7b items use the feeder judge prompt, others the game
judge prompt. Reference: H1 reference.csv (adjudicated; unsure and judge-invalid = unresolved, never forced).
Role overlap: a judge family that wrote, audited or judged an item in its source stage is flagged and a sensitivity
excluding those items is reported (S5b/S7b rotations use deepseek / minimax / glm in every rotation; S3b items were
written by their backbone and judged by kimi_k3). Validity rule (pre-specified 2026-10-21): a judge x prompt cell counts
only with >= 90% valid labels. Exploratory.
"""
from __future__ import annotations

import pandas as pd

from .. import audit as A
from .. import config as C
from .base import Experiment
from .util import bootstrap_ci, md

FAMILY = {"deepseek": "deepseek", "minimax": "minimax", "glm": "glm", "kimi": "kimi", "qwen": "qwen", "muse": "muse",
          "gpt": "gpt_oss", "nemotron": "nemotron", "gemma": "gemma", "hermes": "hermes", "llama": "llama"}


def family(alias: str) -> str:
    a = str(alias).lower()
    for k, v in FAMILY.items():
        if a.startswith(k):
            return v
    return a


def _b(x):
    return None if x is None or x != x or str(x).strip() == "" else str(x).strip().lower() in ("true", "1", "1.0")


class A4H1Judges(Experiment):
    id = "A4_h1_judges"
    title = "Candidate judges vs the independent two-annotator reference (H1 items, strict and rubric prompts)"
    level = 1
    requires = ["H1_independent_labels"]
    question = ("Against independent human labels, how accurate is each candidate judge family, with the strict "
                "production prompt and with the frozen rubric? Is a family new to the programme (muse_spark) fit to "
                "serve as an outside judge in the confirmatory runs?")
    default_params = {"models": ["kimi_k3", "minimax_m3", "deepseek_v4_pro", "glm53", "qwen3_235b", "muse_spark"],
                      "prompts": ["strict", "rubric"], "dir": "labeling_v2", "rotation_families": ["deepseek", "minimax", "glm"]}
    rules_version = "2026-10-21"
    est_calls_per_unit = 82
    est_tokens_in = 700
    est_tokens_out = 90

    def units(self):
        return [{"id": f"{a}-{p}", "alias": a, "prompt": p} for a in self.group(self.params["models"])
                for p in self.params["prompts"]]

    def estimate_models(self):
        return list(self.group(self.params["models"]))

    def _h1(self):
        return C.REPORTS / self.params["dir"]

    def _ref_path(self):
        from .base import runs_root
        return runs_root(self.mock) / "H1_independent_labels" / "_analysis" / "reference.csv"

    def items(self):
        d = self._h1()
        if not (d / "items.csv").exists() or not (d / "key.csv").exists():
            return pd.DataFrame()
        it = pd.read_csv(d / "items.csv").merge(pd.read_csv(d / "key.csv")[["item", "source", "unit"]], on="item")
        it["domain"] = it.source.map(lambda s: "feeder" if str(s).startswith("S7") else "game")
        return it

    def run_unit(self, unit, ctx, outdir):
        from .. import gcge_ext as X
        from .. import planning_ext as PX
        from ..upstream import gcge_core as G
        from .calibration import RUBRIC, RUBRIC_PROMPT_SUFFIX, _content_violating
        items = self.items()
        llm = ctx.llm(self.model_id(unit["alias"]), role="evaluator", temperature=0.0, max_tokens=300)
        base = {"game": (X.JUDGE_SYSTEM, G.VALID_THEMES), "feeder": (PX.JUDGE_SYSTEM_FEEDER, PX.EXT_THEMES)}
        rows = []
        for _, it in items.iterrows():
            system, themes = base[it["domain"]]
            sysp = system if unit["prompt"] == "strict" else system + RUBRIC_PROMPT_SUFFIX + RUBRIC
            lab, tries = A.ask_label(llm, str(it["text"]), sysp, themes)
            if lab is None:
                v = None
            elif unit["prompt"] == "rubric":
                v = _content_violating(lab)
            elif it["domain"] == "game":
                v = bool(X.violating(lab))
            else:
                v = not PX.audit_ok(lab)
            rows.append({"item": it["item"], "domain": it["domain"], "valid": lab is not None, "tries": tries,
                         "verdict_violating": v})
        df = pd.DataFrame(rows, columns=["item", "domain", "valid", "tries", "verdict_violating"])
        df.to_csv(outdir / "verdicts.csv", index=False)
        return {"model": llm.model, "alias": unit["alias"], "prompt": unit["prompt"], "n_items": int(len(df)),
                "valid_rate": float(df.valid.mean()) if len(df) else float("nan"), "cost_usd": llm.stats["cost_usd"]}

    # ---- analysis -----------------------------------------------------------------------------------------------
    def _overlap(self, judge_alias, source, unit_name):
        fam = family(judge_alias)
        if str(source).startswith("S3b"):
            return fam in (family(str(unit_name).split("-")[0]), "kimi")
        return fam in set(self.params["rotation_families"])

    def analyze(self):
        from .calibration import _kappa
        if not self._ref_path().exists():
            return "H1 reference not available yet."
        ref = pd.read_csv(self._ref_path())[["item", "reference", "source", "unit", "inclusion_prob"]]
        frames = []
        for u in self.units():
            f = self.unit_dir(u["id"]) / "verdicts.csv"
            if f.exists() and self.unit_status(u["id"]).get("status") == "done":
                d = pd.read_csv(f)
                d["alias"], d["prompt"] = u["alias"], u["prompt"]
                frames.append(d)
        if not frames:
            return "No results."
        v = pd.concat(frames, ignore_index=True).merge(ref, on="item", how="left")
        v["v"] = v.verdict_violating.map(_b)
        v["overlap"] = [self._overlap(a, s, n) for a, s, n in zip(v.alias, v.source, v.unit)]
        self.adir.mkdir(parents=True, exist_ok=True)
        v.to_csv(self.adir / "all_verdicts.csv", index=False)
        cells = v.groupby(["alias", "prompt"]).valid.mean().reset_index(name="valid_rate")
        cells["eligible"] = cells.valid_rate >= 0.90
        self.validity = {"rules_version": self.rules_version, "rules": {"valid_rate": [">=", 0.9]},
                         "cells": int(len(cells)), "cells_eligible": int(cells.eligible.sum()),
                         "excluded": {f"{r.alias}|{r.prompt}": float(r.valid_rate) for r in cells[~cells.eligible].itertuples()}}
        ok = set(map(tuple, cells[cells.eligible][["alias", "prompt"]].values))
        rows = []
        for (a, p), d in v.groupby(["alias", "prompt"]):
            for scope in ("all", "no_overlap", "S3b", "S5b", "S7b"):
                dd = d if scope == "all" else d[~d.overlap] if scope == "no_overlap" else d[d.source == scope]
                dec = dd[dd.reference.isin(["clean", "violating"]) & dd.v.notna()]
                if not len(dec):
                    continue
                h = dec.reference == "violating"
                j = dec.v.astype(bool)
                w = 1.0 / dec.inclusion_prob.astype(float)
                rows.append({"alias": a, "prompt": p, "scope": scope, "eligible_cell": (a, p) in ok, "n": int(len(dec)),
                             "unresolved": int(len(dd[dd.reference.isin(["clean", "violating"])]) - len(dec)),
                             "agreement": float((h == j).mean()), "kappa": _kappa(h, j),
                             "tpr": float(j[h].mean()) if h.any() else float("nan"),
                             "fpr": float(j[~h].mean()) if (~h).any() else float("nan"),
                             "weighted_agreement": float(((h == j) * w).sum() / w.sum())})
        res = pd.DataFrame(rows)
        res.to_csv(self.adir / "judges_vs_reference.csv", index=False)
        cells.to_csv(self.adir / "instruments.csv", index=False)
        head = res[res.scope.isin(["all", "no_overlap"])].sort_values(["prompt", "scope", "kappa"], ascending=[True, True, False])
        from .calibration import h1_provenance_note
        lines = [h1_provenance_note() + f"**A4 — candidate judges vs the H1 reference** (exploratory; rules {self.rules_version}). "
                 f"{v.item.nunique()} items, reference decided on {int(ref.reference.isin(['clean', 'violating']).sum())}; "
                 f"{int(cells.eligible.sum())}/{len(cells)} judge × prompt cells pass the ≥ 90% valid-label rule"
                 + (f" (excluded: {', '.join(self.validity['excluded'])})" if self.validity["excluded"] else "") + ".", "",
                 "**All items and items without role overlap** (`no_overlap` drops items whose source stage used the "
                 "judge's family as writer, auditor or judge; for deepseek / minimax / glm this leaves only S3b items "
                 "they did not write)", "", md(head.round(3)), "",
                 "**By source**", "", md(res[res.scope.isin(["S3b", "S5b", "S7b"])].round(3)), "",
                 "- The H1 sample is enriched for hard cases; `weighted_agreement` uses 1/inclusion probability. "
                 "n is small per source (≤ 26 decided), so read differences between judges as indicative."]
        return "\n".join(lines)
