"""Answer extraction. Returns a letter or None (unparseable -> scored as wrong, and counted)."""
from __future__ import annotations

import re

# Highest priority: an explicit "Answer: X" / "final answer is (X)". Last occurrence wins,
# because models often restate the options before concluding.
# The letter must stand alone: followed only by closing marks/punctuation and then
# end-of-line, so "Answer: A patient with..." is NOT read as option A (bug found by
# tests/test_core.py on 2026-10-20). Cost: "Answer: B because..." is also rejected
# (counted as a parse failure, reported per method).
_ANSWER_TAG = re.compile(
    r"(?i:answer)\s*(?i:is)?\s*[:\-]?\s*[\*\(\[]*\s*([A-Z])[\)\]\*]*\s*[.,;:!]?[\)\]\*]*\s*$",
    re.MULTILINE)
_BOXED = re.compile(r"\\boxed\{\s*([A-Z])\s*\}")
_BARE = re.compile(r"^\s*[\*\(\[]*([A-Z])[\)\]\.\*]*\s*$")


def extract_answer(text: str | None, valid: list[str] | str) -> str | None:
    if not text:
        return None
    valid_set = set(valid)
    for pattern in (_ANSWER_TAG, _BOXED):
        hits = [m.group(1) for m in pattern.finditer(text) if m.group(1) in valid_set]
        if hits:
            return hits[-1]
    last_line = text.strip().splitlines()[-1] if text.strip() else ""
    m = _BARE.match(last_line)
    if m and m.group(1) in valid_set:
        return m.group(1)
    return None


def majority_vote(answers: list[str | None]) -> str | None:
    """Plurality over parsed answers; ties broken by which tied letter appeared first
    (deterministic, independent of the gold label). None votes are ignored."""
    counts: dict[str, int] = {}
    order: list[str] = []
    for a in answers:
        if a is None:
            continue
        if a not in counts:
            counts[a] = 0
            order.append(a)
        counts[a] += 1
    if not counts:
        return None
    best = max(counts.values())
    return next(a for a in order if counts[a] == best)


def agreement(answers: list[str | None]) -> float:
    """Share of all votes (including None) held by the plurality answer."""
    if not answers:
        return 0.0
    winner = majority_vote(answers)
    if winner is None:
        return 0.0
    return sum(a == winner for a in answers) / len(answers)
