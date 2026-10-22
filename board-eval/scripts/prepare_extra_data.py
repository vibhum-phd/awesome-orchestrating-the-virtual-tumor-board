"""Build the datasets that need Hugging Face access (run on Kaggle/Colab, not required locally).

  medmcqa_dev_onc.jsonl   : MedMCQA dev split, single-answer items, frozen oncology filter v1.0
                            applied to question stem, gold option text AND topic_name
  medqa4_test_all.jsonl   : MedQA USMLE 4-option test (baseline validation against literature)
  medqa_train_pilot.jsonl : 20 MedQA train items for prompt/parse debugging only

Usage:  python scripts/prepare_extra_data.py --out data/processed
Requires: pip install datasets
Every number this script prints is a real count from the downloaded data — paste it into
research_decisions.md.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from vtb.data import Item, ONCOLOGY_REGEX, PROTOCOL_VERSION, _oncology_hits, stable_id, write_jsonl  # noqa: E402

MEDMCQA_HF = "openlifescienceai/medmcqa"          # VERIFY on huggingface.co before running
MEDQA4_HF = "GBaker/MedQA-USMLE-4-options"        # card states CC-BY-4.0 (verified 2026-10-20)


def medmcqa_items(split: str = "validation") -> tuple[list[Item], dict]:
    from datasets import load_dataset
    ds = load_dataset(MEDMCQA_HF, split=split)
    cops = Counter(int(r["cop"]) for r in ds)
    # HF copy is expected 0-based (0..3); the original JSON is 1-based (official dataset.py does cop-1).
    if 4 in cops and 0 not in cops:
        base = 1
    elif 0 in cops and 4 not in cops:
        base = 0
    else:
        raise ValueError(f"cannot infer 'cop' base from distribution {cops}")
    items, skipped_multi = [], 0
    for r in ds:
        if r.get("choice_type") and r["choice_type"] != "single":
            skipped_multi += 1
            continue
        opts = {"A": r["opa"], "B": r["opb"], "C": r["opc"], "D": r["opd"]}
        gold = "ABCD"[int(r["cop"]) - base]
        items.append(Item(stable_id(r["question"] + "||" + "|".join(opts.values())), r["question"], opts, gold,
                          {"subject_name": r.get("subject_name"), "topic_name": r.get("topic_name"),
                           "hf_id": r.get("id")}))
    return items, {"cop_distribution": dict(cops), "cop_base": base, "skipped_multi": skipped_multi}


def medmcqa_is_onc(it: Item) -> bool:
    return bool(_oncology_hits(it.question, True) or _oncology_hits(it.options[it.answer_idx], False)
                or ONCOLOGY_REGEX.search(it.meta.get("topic_name") or ""))


def medqa4_items(split: str) -> list[Item]:
    from datasets import load_dataset
    ds = load_dataset(MEDQA4_HF, split=split)
    out = []
    for r in ds:
        opts = r["options"]
        if isinstance(opts, list):  # some copies store [{"key":..,"value":..}]
            opts = {o["key"]: o["value"] for o in opts}
        out.append(Item(stable_id(r["question"]), r["question"], dict(opts), r["answer_idx"],
                        {"meta_info": r.get("meta_info")}))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/processed")
    args = ap.parse_args()
    out = Path(args.out)
    report = {"protocol_version": PROTOCOL_VERSION}

    mm, info = medmcqa_items("validation")
    # de-duplicate on content id (MedMCQA has some repeated questions)
    seen, dedup = set(), []
    for it in mm:
        if it.item_id not in seen:
            seen.add(it.item_id)
            dedup.append(it)
    onc = [it for it in dedup if medmcqa_is_onc(it)]
    write_jsonl(onc, out / "medmcqa_dev_onc.jsonl")
    report["medmcqa"] = {**info, "n_single_answer": len(mm), "n_after_dedup": len(dedup), "n_onc": len(onc),
                         "onc_subjects": dict(Counter(it.meta["subject_name"] for it in onc).most_common()),
                         "onc_gold_letters": dict(sorted(Counter(it.answer_idx for it in onc).items()))}

    m4 = medqa4_items("test")
    write_jsonl(m4, out / "medqa4_test_all.jsonl")
    report["medqa4_test"] = {"n": len(m4), "options": dict(Counter(len(i.options) for i in m4))}

    tr = medqa4_items("train")
    random.Random(7).shuffle(tr)
    write_jsonl(tr[:20], out / "medqa_train_pilot.jsonl")
    report["pilot_train"] = {"n": 20, "note": "debug only"}

    (out / "extra_manifest.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
