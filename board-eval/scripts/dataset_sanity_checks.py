"""Real, model-free sanity checks on the MedQA test file and the oncology subset.
Usage: python dataset_sanity_checks.py <repo_root>
Writes dataset_sanity_checks_output.json next to this script."""
import json, sys, re, statistics as st
from collections import Counter
from pathlib import Path
from itertools import combinations
root = Path(sys.argv[1])
def load(p): return [json.loads(l) for l in open(p, encoding="utf-8")]
allq = load(root / "data/processed/medqa_test_all.jsonl")
onc = load(root / "data/processed/medqa_test_onc.jsonl")
def words(t): return len(t.split())
def summary(rows):
    golds = Counter(r["answer_idx"] for r in rows)
    maj_letter, maj_n = golds.most_common(1)[0]
    longest = sum(max(r["options"], key=lambda k: len(r["options"][k])) == r["answer_idx"] for r in rows)
    shortest = sum(min(r["options"], key=lambda k: len(r["options"][k])) == r["answer_idx"] for r in rows)
    ql = [words(r["question"]) for r in rows]
    return {"n": len(rows), "gold_letters": dict(sorted(golds.items())),
            "majority_letter_baseline_acc": round(maj_n / len(rows), 4), "majority_letter": maj_letter,
            "longest_option_heuristic_acc": round(longest / len(rows), 4),
            "shortest_option_heuristic_acc": round(shortest / len(rows), 4),
            "chance_acc_5_options": 0.2,
            "question_words_median": st.median(ql), "question_words_max": max(ql), "question_words_min": min(ql),
            "meta_info": dict(Counter(r["meta"].get("meta_info") for r in rows))}
def shingles(t, k=5):
    w = re.findall(r"[a-z0-9]+", t.lower()); return {" ".join(w[i:i+k]) for i in range(max(1, len(w)-k+1))}
def near_dups(rows, thr=0.6):
    sh = [shingles(r["question"]) for r in rows]; out = []
    for i, j in combinations(range(len(rows)), 2):
        a, b = sh[i], sh[j]; jac = len(a & b) / len(a | b)
        if jac >= thr: out.append({"a": rows[i]["item_id"], "b": rows[j]["item_id"], "jaccard_5gram": round(jac, 3)})
    return out
res = {"all_test": summary(allq), "oncology_subset": summary(onc),
       "near_duplicates_in_oncology_subset_jaccard_ge_0.6": near_dups(onc)}
Path(__file__).with_name("dataset_sanity_checks_output.json").write_text(json.dumps(res, indent=2))
print(json.dumps(res, indent=2))
