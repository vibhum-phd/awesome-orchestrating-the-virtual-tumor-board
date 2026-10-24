"""Answer extraction. Returns a letter or None (unparseable -> scored as wrong, and counted)."""
from __future__ import annotations

import re

# Highest priority: an explicit "Answer: X" / "final answer is (X)". Last occurrence wins,
# because models often restate the options before concluding.
#
# History (see Lab_7 Prompt 11 debugging log):
#  v1 (2026-10-20) accepted any capital after "Answer:" -> "Answer: A patient with..." parsed as A (test caught it).
#  v2 (2026-10-20) required the letter to end the line -> also rejected "Answer: C. Tell the attending..."
#     and "Answer: B because ...", which models commonly write (found in code review, 2026-10-24).
#  v3 (2026-10-24, before any real model output): the letter must not run into another letter
#     ("Answer: Cisplatin" is not C), and ONLY the article-like case "A" + space + lowercase word is
#     rejected ("Answer: A patient..."). Everything else after the letter is allowed.
_ANSWER_TAG = re.compile(r"(?i:answer)\s*(?i:is)?\s*[:\-]?\s*[\*\(\[]*\s*([A-Z])(?![A-Za-z])")
_ARTICLE_A = re.compile(r"\s+[a-z]")
_BOXED = re.compile(r"\\boxed\{\s*([A-Z])\s*\}")
_BARE = re.compile(r"^\s*[\*\(\[]*([A-Z])[\)\]\.\*]*\s*$")


def _tag_hits(text: str, valid_set: set[str]) -> list[str]:
    out = []
    for m in _ANSWER_TAG.finditer(text):
        letter = m.group(1)
        if letter not in valid_set:
            continue
        if letter == "A" and _ARTICLE_A.match(text, m.end()):
            continue  # "Answer: A patient with ..." — the article, not option A
        out.append(letter)
    return out


def extract_answer(text: str | None, valid: list[str] | str) -> str | None:
    if not text:
        return None
    valid_set = set(valid)
    for finder in (lambda t: _tag_hits(t, valid_set),
                   lambda t: [m.group(1) for m in _BOXED.finditer(t) if m.group(1) in valid_set]):
        hits = finder(text)
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
