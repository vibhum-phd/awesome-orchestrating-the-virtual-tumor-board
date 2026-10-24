"""Build the processed evaluation sets from the MedQA (USMLE, 5-option) test split.

Usage:
    python scripts/prepare_data.py --src data/raw/medqa_test.jsonl --out data/processed

Outputs:
    data/processed/medqa_test_all.jsonl       all 1273 items (secondary set)
    data/processed/medqa_test_onc.jsonl       frozen oncology subset (primary set)
    data/processed/onc_filter_audit.csv       every item, matched terms, inclusion flag
    data/processed/manifest.json              counts, sha256 of source + outputs, rule version
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from vtb.data import (PROTOCOL_VERSION, ONCOLOGY_PATTERNS, is_oncology, load_medqa_jsonl,  # noqa: E402
                      oncology_matches, sha256_file, write_jsonl)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", default="data/processed")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    items = load_medqa_jsonl(args.src)
    onc = [it for it in items if is_oncology(it, "stem_or_gold")]
    onc_stem = [it for it in items if is_oncology(it, "stem")]

    write_jsonl(items, out / "medqa_test_all.jsonl")
    write_jsonl(onc, out / "medqa_test_onc.jsonl")

    with open(out / "onc_filter_audit.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "source_line", "meta_info", "included", "stem_hits", "gold_hits", "gold_text", "stem_first_200"])
        for it in items:
            m = oncology_matches(it)
            w.writerow([it.item_id, it.meta["source_line"], it.meta["meta_info"], int(is_oncology(it)),
                        ";".join(m["stem_hits"]), ";".join(m["gold_hits"]),
                        it.options[it.answer_idx], it.question[:200].replace("\n", " ")])

    manifest = {
        "protocol_version": PROTOCOL_VERSION,
        "source_file": str(args.src),
        "source_sha256": sha256_file(args.src),
        "n_all": len(items),
        "n_onc_primary_stem_or_gold": len(onc),
        "n_onc_stem_only": len(onc_stem),
        "options_per_item": dict(Counter(len(it.options) for it in items)),
        "gold_letter_distribution_all": dict(sorted(Counter(it.answer_idx for it in items).items())),
        "gold_letter_distribution_onc": dict(sorted(Counter(it.answer_idx for it in onc).items())),
        "meta_info_onc": dict(Counter(it.meta["meta_info"] for it in onc)),
        "oncology_patterns": ONCOLOGY_PATTERNS,
        "outputs": {p.name: sha256_file(p) for p in [out / "medqa_test_all.jsonl", out / "medqa_test_onc.jsonl"]},
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps({k: v for k, v in manifest.items() if k not in ("oncology_patterns", "outputs")}, indent=2))


if __name__ == "__main__":
    main()
