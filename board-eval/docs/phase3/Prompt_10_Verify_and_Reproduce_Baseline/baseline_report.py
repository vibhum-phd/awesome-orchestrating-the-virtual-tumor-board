"""Baseline validation numbers (Prompt 10) computed ONLY from raw run files.

  python scripts/baseline_report.py --raw results/raw [--rerun results/rerun] --out results/baseline

For every (dataset, model, seed) that has CoT and/or SC runs it reports:
  n, accuracy + 95% bootstrap CI, parse-failure rate, the majority-letter floor of that item set,
  SC accuracy at k = 1,3,5,9,15 and SC@1 - CoT (sampling vs greedy), and, if a rerun directory is
  given, how many CoT answers/texts were identical on rerun (determinism).
It prints numbers only; the human writes the judgement in baseline_validation.md.
Raw files from MockBackend (model == 'mock') are tagged SYNTHETIC in every output row.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from vtb.parse import majority_vote  # noqa: E402
from vtb.stats import bootstrap_ci  # noqa: E402

KS = [1, 3, 5, 9, 15]


def read(path: Path) -> list[dict]:
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def collect(raw: Path) -> dict:
    runs: dict = {}
    for fp in sorted(raw.glob("*.jsonl")):
        if fp.name == "run_meta.jsonl":
            continue
        recs = read(fp)
        if not recs:
            continue
        r0 = recs[0]
        if r0["method"] not in ("cot", "sc"):
            continue
        key = (r0["dataset"], r0["model"], r0["seed"])
        runs.setdefault(key, {})[r0["method"]] = {r["item_id"]: r for r in recs}
    return runs


def acc_block(correct: list[int]) -> dict:
    a = np.array(correct)
    lo, hi = bootstrap_ci(a, 10000, 20261020)
    return {"acc": round(float(a.mean()), 4), "ci95": [round(lo, 4), round(hi, 4)]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=str(ROOT / "results/raw"))
    ap.add_argument("--rerun", default=None)
    ap.add_argument("--out", default=str(ROOT / "results/baseline"))
    args = ap.parse_args()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    runs = collect(Path(args.raw))
    rerun = collect(Path(args.rerun)) if args.rerun else {}
    rows = []
    for (ds, model, seed), arms in sorted(runs.items()):
        row = {"dataset": ds, "model": model, "seed": seed,
               "synthetic": model == "mock"}
        any_arm = next(iter(arms.values()))
        golds = [r["gold"] for r in any_arm.values()]
        letter, cnt = Counter(golds).most_common(1)[0]
        row["n"] = len(golds)
        row["majority_letter_floor"] = {"letter": letter, "acc": round(cnt / len(golds), 4)}
        if "cot" in arms:
            recs = list(arms["cot"].values())
            row["cot"] = {**acc_block([int(r["final"] == r["gold"]) for r in recs]),
                          "parse_fail": round(sum(r["final"] is None for r in recs) / len(recs), 4),
                          "truncated": round(sum(r["samples"][0].get("finish_reason") == "length" for r in recs) / len(recs), 4)}
        if "sc" in arms:
            recs = list(arms["sc"].values())
            row["sc"] = {}
            for k in KS:
                votes = [majority_vote([s["answer"] for s in r["samples"][:k]]) for r in recs]
                row["sc"][f"k{k}"] = acc_block([int(v == r["gold"]) for v, r in zip(votes, recs)])
            row["sc"]["sample_parse_fail"] = round(
                float(np.mean([s["answer"] is None for r in recs for s in r["samples"]])), 4)
            row["sc"]["sample_truncated"] = round(
                float(np.mean([s.get("finish_reason") == "length" for r in recs for s in r["samples"]])), 4)
            if "cot" in row:
                row["sc1_minus_cot"] = round(row["sc"]["k1"]["acc"] - row["cot"]["acc"], 4)
            ks = [row["sc"][f"k{k}"]["acc"] for k in KS]
            row["sc_steps"] = [round(b - a, 4) for a, b in zip(ks, ks[1:])]
        rr = rerun.get((ds, model, seed), {}).get("cot")
        if rr and "cot" in arms:
            common = [i for i in rr if i in arms["cot"]]
            same_ans = sum(rr[i]["final"] == arms["cot"][i]["final"] for i in common)
            same_txt = sum(rr[i]["samples"][0]["text"] == arms["cot"][i]["samples"][0]["text"] for i in common)
            row["determinism_cot"] = {"n": len(common), "same_answer": same_ans, "same_text": same_txt}
        rows.append(row)
    (out_dir / "baseline_report.json").write_text(json.dumps(rows, indent=2))
    lines = ["| dataset | seed | n | floor | CoT acc (CI) | CoT parse fail | CoT truncated | SC@1 | SC@9 | SC@15 | SC@1−CoT | determinism (same/n) | synthetic |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        c = r.get("cot", {})
        s = r.get("sc", {})
        d = r.get("determinism_cot")
        cot_txt = f"{c['acc']:.3f} ({c['ci95'][0]:.3f}–{c['ci95'][1]:.3f})" if c else "—"
        det_txt = f"{d['same_answer']}/{d['n']}" if d else "—"
        lines.append(f"| {r['dataset']} | {r['seed']} | {r['n']} | {r['majority_letter_floor']['acc']:.3f} | {cot_txt} | "
                     f"{c.get('parse_fail', '—')} | {c.get('truncated', '—')} | {s.get('k1', {}).get('acc', '—')} | {s.get('k9', {}).get('acc', '—')} | "
                     f"{s.get('k15', {}).get('acc', '—')} | {r.get('sc1_minus_cot', '—')} | {det_txt} | "
                     f"{'SYNTHETIC' if r['synthetic'] else 'real'} |")
    (out_dir / "baseline_report.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
