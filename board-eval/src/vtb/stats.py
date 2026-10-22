"""Small, dependency-light statistics used by the evaluator."""
from __future__ import annotations

import numpy as np
from scipy.stats import binomtest


def bootstrap_ci(correct: np.ndarray, n_boot: int = 10000, seed: int = 0, alpha: float = 0.05):
    """Percentile CI for a mean of 0/1 outcomes (item-level resampling)."""
    rng = np.random.default_rng(seed)
    n = len(correct)
    idx = rng.integers(0, n, size=(n_boot, n))
    means = correct[idx].mean(axis=1)
    return float(np.quantile(means, alpha / 2)), float(np.quantile(means, 1 - alpha / 2))


def paired_bootstrap_diff(a: np.ndarray, b: np.ndarray, n_boot: int = 10000, seed: int = 0, alpha: float = 0.05):
    """CI for mean(a) - mean(b) with items resampled jointly (keeps the pairing)."""
    assert len(a) == len(b)
    rng = np.random.default_rng(seed)
    n = len(a)
    idx = rng.integers(0, n, size=(n_boot, n))
    d = a[idx].mean(axis=1) - b[idx].mean(axis=1)
    return float(np.quantile(d, alpha / 2)), float(np.quantile(d, 1 - alpha / 2))


def mcnemar_exact(a: np.ndarray, b: np.ndarray) -> dict:
    """Exact two-sided McNemar test on paired 0/1 outcomes.
    b01 = a wrong & b right, b10 = a right & b wrong. Valid for any n (no chi-square approximation)."""
    a = a.astype(bool)
    b = b.astype(bool)
    b10 = int(np.sum(a & ~b))
    b01 = int(np.sum(~a & b))
    n_disc = b10 + b01
    p = 1.0 if n_disc == 0 else float(binomtest(b10, n_disc, 0.5, alternative="two-sided").pvalue)
    return {"a_only_correct": b10, "b_only_correct": b01, "discordant": n_disc, "p_value": p}


def holm(pvals: list[float]) -> list[float]:
    """Holm step-down adjusted p-values (same order as input)."""
    m = len(pvals)
    order = np.argsort(pvals)
    adj = np.empty(m)
    running = 0.0
    for rank, i in enumerate(order):
        val = min(1.0, (m - rank) * pvals[i])
        running = max(running, val)
        adj[i] = running
    return adj.tolist()
