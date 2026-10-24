"""Simulated power of a two-sided exact McNemar test (alpha=0.05) for paired 0/1 outcomes.
Assumptions (stated, not measured): baseline accuracy p_b; method accuracy p_b + d;
fraction of items where the two methods disagree = disc (must be >= |d|)."""
import numpy as np
from scipy.stats import binomtest
rng = np.random.default_rng(20261024)
def power(n, d, disc, sims=4000):
    # discordant cells: a_only = (disc + d)/2, b_only = (disc - d)/2
    pa, pb = (disc + d) / 2, (disc - d) / 2
    hits = 0
    for _ in range(sims):
        cells = rng.multinomial(n, [pa, pb, 1 - pa - pb])
        k, m = cells[0], cells[0] + cells[1]
        if m and binomtest(k, m, 0.5).pvalue < 0.05:
            hits += 1
    return hits / sims
print("n,disc,d_pp,power")
for n in (97, 200, 400, 1273):
    for disc in (0.15, 0.25):
        for d in (0.02, 0.05, 0.08, 0.10, 0.15):
            if d <= disc:
                print(f"{n},{disc},{int(d*100)},{power(n, d, disc):.2f}")
