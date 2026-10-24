"""Cross-file leakage / overlap check for the processed JSONL sets.

Flags question pairs across two files whose word 5-gram Jaccard similarity >= threshold
(exact duplicates score 1.0). Run on Kaggle after building all sets:

  python leakage_checks.py data/processed/medqa_train_pilot.jsonl data/processed/medqa_test_all.jsonl
  python leakage_checks.py data/processed/medmcqa_dev_onc.jsonl  data/processed/medqa_test_onc.jsonl

Exit code 1 if any pair is flagged, so it can gate a notebook cell.
"""
from __future__ import annotations

import json
import re
import sys


def shingles(text: str, k: int = 5) -> set[str]:
    w = re.findall(r"[a-z0-9]+", text.lower())
    return {" ".join(w[i:i + k]) for i in range(max(1, len(w) - k + 1))}


def load(path: str) -> list[dict]:
    return [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]


def overlaps(a_rows, b_rows, thr=0.6, same_file=False):
    b_sh = [(r["item_id"], shingles(r["question"])) for r in b_rows]
    # inverted index on shingles keeps this fast enough for ~10k x 1k items
    index: dict[str, list[int]] = {}
    for j, (_, s) in enumerate(b_sh):
        for g in s:
            index.setdefault(g, []).append(j)
    hits = []
    for r in a_rows:
        sa = shingles(r["question"])
        cand = {j for g in sa for j in index.get(g, [])}
        for j in cand:
            bid, sb = b_sh[j]
            if same_file and bid == r["item_id"]:
                continue
            jac = len(sa & sb) / len(sa | sb)
            if jac >= thr:
                hits.append({"a": r["item_id"], "b": bid, "jaccard_5gram": round(jac, 3)})
    return hits


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    a, b = load(sys.argv[1]), load(sys.argv[2])
    thr = float(sys.argv[3]) if len(sys.argv) > 3 else 0.6
    same = sys.argv[1] == sys.argv[2]
    hits = overlaps(a, b, thr, same)
    print(json.dumps({"file_a": sys.argv[1], "n_a": len(a), "file_b": sys.argv[2], "n_b": len(b),
                      "threshold": thr, "n_flagged_pairs": len(hits), "pairs": hits[:50]}, indent=2))
    sys.exit(1 if hits else 0)
