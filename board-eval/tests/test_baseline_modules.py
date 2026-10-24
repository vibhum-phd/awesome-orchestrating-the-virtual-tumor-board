"""Module-by-module tests for the baseline pipeline (Prompt 09 cycles 1-5).
All CPU-only; the 'model' is MockBackend, whose outputs are synthetic."""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from vtb.backends import Completion, MockBackend, Request  # noqa: E402
from vtb.data import Item, load_medqa_jsonl, load_processed  # noqa: E402
from vtb.methods import ANSWER_INSTRUCTION, GenConfig, derive_seed, format_question, run_cot, run_sc  # noqa: E402
from vtb.parse import majority_vote  # noqa: E402


# ---------------- cycle 1: data loading and validation
def _write(tmp_path, rows):
    p = tmp_path / "x.jsonl"
    p.write_text("\n".join(json.dumps(r) for r in rows))
    return p


def test_loader_rejects_bad_rows(tmp_path):
    good = {"question": "Q1?", "options": {"A": "a", "B": "b"}, "answer_idx": "A"}
    with pytest.raises(ValueError, match="missing"):
        load_medqa_jsonl(_write(tmp_path, [{"question": "Q", "options": {"A": "a"}}]))
    with pytest.raises(ValueError, match="not in options"):
        load_medqa_jsonl(_write(tmp_path, [{**good, "answer_idx": "C"}]))
    with pytest.raises(ValueError, match="duplicate"):
        load_medqa_jsonl(_write(tmp_path, [good, good]))


def test_loader_shapes_on_real_file():
    p = ROOT / "data/raw/medqa_test.jsonl"
    if not p.exists():
        pytest.skip("raw MedQA not present")
    items = load_medqa_jsonl(p)
    assert len(items) == 1273
    assert all(len(it.options) == 5 and it.answer_idx in it.options and len(it.item_id) == 12 for it in items)


# ---------------- cycle 2: prompt construction
def test_format_question_lists_options_in_order():
    it = Item("x", "Which drug?", {"B": "beta", "A": "alpha"}, "A")
    s = format_question(it)
    assert s.index("A. alpha") < s.index("B. beta") and s.startswith("Question:\nWhich drug?")
    assert "Answer: <letter>" in ANSWER_INSTRUCTION


def test_derive_seed_deterministic_and_tag_specific():
    assert derive_seed(0, "abc", "cot") == derive_seed(0, "abc", "cot")
    assert derive_seed(0, "abc", "cot") != derive_seed(0, "abc", "sc")
    assert derive_seed(0, "abc", "cot") != derive_seed(1, "abc", "cot")


# ---------------- cycle 3: backend interface
def test_mock_backend_shapes():
    be = MockBackend({"What is X?": "B"})
    out = be.generate([Request([{"role": "user", "content": "What is X?"}], n=3, temperature=0.7, seed=1)])
    assert len(out) == 1 and len(out[0]) == 3 and all(isinstance(c, Completion) for c in out[0])


# ---------------- cycle 4: baseline algorithms (CoT, self-consistency)
@pytest.fixture
def items():
    p = ROOT / "data/processed/medqa_test_onc.jsonl"
    if not p.exists():
        pytest.skip("processed data missing")
    return load_processed(p)[:6]


def test_cot_record_shape(items):
    be = MockBackend({it.question: it.answer_idx for it in items})
    recs = run_cot(items, be, GenConfig(), seed=0)
    assert len(recs) == len(items)
    r = recs[0]
    assert set(r) >= {"item_id", "gold", "method", "calls", "final", "samples", "prompt_tokens", "completion_tokens"}
    assert r["calls"] == 1 and len(r["samples"]) == 1 and r["method"] == "cot"


def test_sc_record_shape_and_vote(items):
    be = MockBackend({it.question: it.answer_idx for it in items})
    recs = run_sc(items, be, GenConfig(), seed=0, k_max=15)
    for r in recs:
        assert len(r["samples"]) == 15 and r["calls"] == 15
        assert r["final"] == majority_vote([s["answer"] for s in r["samples"][:9]])  # SC@9 stored as final


def test_cot_is_reproducible(items):
    be = MockBackend({it.question: it.answer_idx for it in items})
    a = [r["final"] for r in run_cot(items, be, GenConfig(), seed=0)]
    b = [r["final"] for r in run_cot(items, be, GenConfig(), seed=0)]
    assert a == b


def test_finish_reason_recorded(items):
    be = MockBackend({it.question: it.answer_idx for it in items})
    cot = run_cot(items, be, GenConfig(), seed=0)
    sc = run_sc(items, be, GenConfig(), seed=0, k_max=3)
    assert all(r["samples"][0]["finish_reason"] == "stop" for r in cot)
    assert all(r["n_truncated"] == 0 and all(s["finish_reason"] == "stop" for s in r["samples"]) for r in sc)
