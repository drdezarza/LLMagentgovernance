"""Small helpers shared by experiment analyses (no extra dependencies)."""
from __future__ import annotations

import numpy as np
import pandas as pd


def md(df: pd.DataFrame, floatfmt: str = "{:.3f}") -> str:
    """DataFrame -> GitHub markdown table without needing `tabulate`."""
    if df is None or len(df) == 0:
        return "_(empty)_"
    cols = [str(c) for c in df.columns]

    def f(v):
        if isinstance(v, (float, np.floating)):
            return "" if np.isnan(v) else floatfmt.format(v)
        return str(v)
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(f(v) for v in r.values) + " |")
    return "\n".join(lines)


def bootstrap_ci(x, n=5000, seed=42):
    x = np.asarray([v for v in x if v is not None and not np.isnan(v)], float)
    if len(x) == 0:
        return (np.nan, np.nan, np.nan)
    if len(x) == 1:
        return (float(x[0]), float(x[0]), float(x[0]))
    rng = np.random.default_rng(seed)
    b = rng.choice(x, size=(n, len(x)), replace=True).mean(axis=1)
    return float(x.mean()), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))


def paired_diff_ci(a, b, n=5000, seed=42):
    a, b = np.asarray(a, float), np.asarray(b, float)
    return bootstrap_ci(a - b, n=n, seed=seed)


def fmt_ci(t):
    m, lo, hi = t
    return f"{m:+.3f} [{lo:+.3f}, {hi:+.3f}]"
