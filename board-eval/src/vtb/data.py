"""Data loading and the frozen oncology filter for MedQA (USMLE, 5-option test split).

The oncology rule below is FROZEN (protocol v1.0, 2026-10-20). It was fixed before any
model output was generated. (v0.9 keyword-only rule was refined the same day, after
inspecting filter matches only, to drop relative-history, negated and non-oncology-phrase
hits; see research_decisions.md D-04.) Do not edit it after seeing results; if it must change,
log the change in research_decisions.md and bump PROTOCOL_VERSION.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

PROTOCOL_VERSION = "1.0"

# Whole-word / prefix patterns. Case-insensitive. Deliberately conservative:
# benign-only terms (adenoma, polyp, nodule, "mass") are NOT included.
ONCOLOGY_PATTERNS = [
    r"cancers?",
    r"carcinomas?",
    r"adenocarcinomas?",
    r"tumou?rs?",
    r"neoplas(m|ms|tic|ia)",
    r"malignan(t|cy|cies)",
    r"metasta\w*",
    r"oncolog\w*",
    r"lymphomas?",
    r"leuka?emias?",
    r"myelomas?",
    r"sarcomas?",
    r"melanomas?",
    r"mesotheliomas?",
    r"gliomas?",
    r"glioblastomas?",
    r"\w+blastomas?",          # neuro-, retino-, hepato-, medullo-, nephro-blastoma
    r"seminomas?",
    r"teratomas?",
    r"choriocarcinomas?",
    r"chemotherap\w*",
    r"radiotherap\w*",
    r"radiation therapy",
    r"chemoradi\w*",
]
ONCOLOGY_REGEX = re.compile(r"\b(" + "|".join(ONCOLOGY_PATTERNS) + r")\b", re.IGNORECASE)

# Non-oncology phrases that contain an oncology token (removed before matching).
NON_ONCOLOGY_PHRASES = re.compile(
    r"neuroleptic malignant|malignant hyperthermia|malignant hypertension|malignant otitis|"
    r"tumou?r necrosis factor", re.IGNORECASE)

# A stem sentence about a relative's history does not make the patient's case oncological.
FAMILY_CONTEXT = re.compile(
    r"\b(family history|father|mother|brother|sister|uncle|aunt|grandfather|grandmother|"
    r"grandparent|cousin|sibling|son|daughter|wife|husband|relatives?|parents?)\b", re.IGNORECASE)

# Negated mentions ("rule out cancer", "negative for malignancy", "does not reveal a tumor").
NEGATION_BEFORE = re.compile(
    r"(rule out|ruled out|negative for|no evidence of|denies|without|free of|"
    r"not reveal|does not show|no |nor )[^.;]{0,40}$", re.IGNORECASE)

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


def _oncology_hits(text: str, drop_family_sentences: bool) -> list[str]:
    text = NON_ONCOLOGY_PHRASES.sub(" ", text)
    hits: set[str] = set()
    for sent in _SENT_SPLIT.split(text):
        if drop_family_sentences and FAMILY_CONTEXT.search(sent):
            continue
        for m in ONCOLOGY_REGEX.finditer(sent):
            if NEGATION_BEFORE.search(sent[:m.start()]):
                continue
            hits.add(m.group(0).lower())
    return sorted(hits)


@dataclass
class Item:
    item_id: str
    question: str
    options: dict[str, str]
    answer_idx: str
    meta: dict = field(default_factory=dict)

    @property
    def letters(self) -> list[str]:
        return sorted(self.options)


def stable_id(question: str) -> str:
    """Content hash so IDs survive reordering of the source file."""
    return hashlib.sha1(question.strip().encode("utf-8")).hexdigest()[:12]


def load_medqa_jsonl(path: str | Path) -> list[Item]:
    items: list[Item] = []
    seen: set[str] = set()
    with open(path, encoding="utf-8") as f:
        for line_no, line in enumerate(f):
            if not line.strip():
                continue
            r = json.loads(line)
            for key in ("question", "options", "answer_idx"):
                if key not in r:
                    raise ValueError(f"line {line_no}: missing '{key}'")
            if r["answer_idx"] not in r["options"]:
                raise ValueError(f"line {line_no}: answer_idx {r['answer_idx']} not in options")
            iid = stable_id(r["question"])
            if iid in seen:
                raise ValueError(f"line {line_no}: duplicate question (id {iid})")
            seen.add(iid)
            items.append(Item(iid, r["question"], dict(r["options"]), r["answer_idx"],
                              {"meta_info": r.get("meta_info"), "source_line": line_no}))
    return items


def oncology_matches(item: Item) -> dict:
    """Return which oncology terms matched in the stem and in the gold answer text."""
    stem_hits = _oncology_hits(item.question, drop_family_sentences=True)
    gold_hits = _oncology_hits(item.options[item.answer_idx], drop_family_sentences=False)
    return {"stem_hits": stem_hits, "gold_hits": gold_hits}


def is_oncology(item: Item, rule: str = "stem_or_gold") -> bool:
    """rule='stem'          : oncology term in the question stem
       rule='stem_or_gold'  : ... or in the gold answer text (PRIMARY, frozen)
    Distractor options are never used, so an item is not selected just because
    a wrong option names a cancer."""
    m = oncology_matches(item)
    if rule == "stem":
        return bool(m["stem_hits"])
    if rule == "stem_or_gold":
        return bool(m["stem_hits"] or m["gold_hits"])
    raise ValueError(rule)


def write_jsonl(items: list[Item], path: str | Path, extra: dict[str, dict] | None = None) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for it in items:
            rec = {"item_id": it.item_id, "question": it.question, "options": it.options,
                   "answer_idx": it.answer_idx, "meta": it.meta}
            if extra and it.item_id in extra:
                rec.update(extra[it.item_id])
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def load_processed(path: str | Path) -> list[Item]:
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            out.append(Item(r["item_id"], r["question"], r["options"], r["answer_idx"], r.get("meta", {})))
    return out


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()
