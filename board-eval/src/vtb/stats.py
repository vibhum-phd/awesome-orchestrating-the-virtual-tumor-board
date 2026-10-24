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


def mcnemar_power(n: int, disc: float, d: float, alpha: float = 0.05) -> float:
    """Exact power of the two-sided exact McNemar test (binomial on discordant pairs).
    n paired items; disc = probability an item is discordant; d = accuracy difference (a - b).
    P(a-only) = (disc + d)/2, P(b-only) = (disc - d)/2. Requires |d| <= disc."""
    from scipy.stats import binom
    if disc <= 0 or abs(d) > disc:
        return float("nan")
    q = (disc + d) / (2 * disc)              # P(a-only | discordant)
    power = 0.0
    for m in range(1, n + 1):
        pm = binom.pmf(m, n, disc)
        if pm < 1e-12:
            continue
        ks = np.arange(m + 1)
        cdf = binom.cdf(ks, m, 0.5)
        sf = binom.sf(ks - 1, m, 0.5)
        p_two = np.minimum(1.0, 2 * np.minimum(cdf, sf))
        reject = p_two < alpha
        power += pm * binom.pmf(ks[reject], m, q).sum()
    return float(power)


def mde_80(n: int, disc: float, step_pp: float = 0.5, alpha: float = 0.05) -> float | None:
    """Smallest |difference| (in percentage points) detectable with >= 80% power, given the
    observed discordance. None if not reachable within |d| <= disc."""
    d = step_pp / 100
    while d <= disc + 1e-12:
        if mcnemar_power(n, disc, d, alpha) >= 0.8:
            return round(100 * d, 1)
        d += step_pp / 100
    return None


def cluster_bootstrap_rate(num: np.ndarray, den: np.ndarray, n_boot: int = 10000, seed: int = 0,
                           alpha: float = 0.05):
    """Ratio sum(num)/sum(den) with a percentile CI from resampling clusters (items)."""
    num = np.asarray(num, float)
    den = np.asarray(den, float)
    est = num.sum() / den.sum() if den.sum() else float("nan")
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(num), size=(n_boot, len(num)))
    nn, dd = num[idx].sum(axis=1), den[idx].sum(axis=1)
    ok = dd > 0
    rates = nn[ok] / dd[ok]
    if len(rates) == 0:
        return est, float("nan"), float("nan")
    return float(est), float(np.quantile(rates, alpha / 2)), float(np.quantile(rates, 1 - alpha / 2))
