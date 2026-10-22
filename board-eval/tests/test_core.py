import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from vtb.data import Item, is_oncology, oncology_matches  # noqa: E402
from vtb.parse import agreement, extract_answer, majority_vote  # noqa: E402
from vtb.stats import holm, mcnemar_exact, paired_bootstrap_diff  # noqa: E402

L = list("ABCDE")


# ---------------------------------------------------------------- parser
@pytest.mark.parametrize("text,exp", [
    ("blah\nAnswer: C", "C"),
    ("Answer: B\n... on reflection ...\nAnswer: D", "D"),          # last tag wins
    ("The answer is (E).", "E"),
    ("Final answer: **A**", "A"),
    ("answer: c", None),                                            # lowercase letter is not accepted
    ("A is tempting but the answer is B", "B"),
    ("Options A and C are wrong.", None),                          # no tag -> None, not a guess
    ("I think\nB", "B"),                                            # bare letter on last line
    ("Answer: F", None),                                            # not a valid option
    ("", None), (None, None),
    ("\\boxed{D}", "D"),
    ("Answer: A patient with ... so D", None),                      # 'A patient' must not parse as A
    ("Answer: B because of X", None),                               # documented cost of the fix
    ("**Answer: C**", "C"),
    ("Answer: (D).", "D"),
])
def test_extract_answer(text, exp):
    assert extract_answer(text, L) == exp


def test_extract_respects_4_options():
    assert extract_answer("Answer: E", list("ABCD")) is None


def test_majority_vote_ties_and_none():
    assert majority_vote(["B", "A", "A", "B"]) == "B"               # tie -> first seen
    assert majority_vote([None, None]) is None
    assert majority_vote([None, "C", "C", "D"]) == "C"
    assert agreement(["A", "A", "A", "B"]) == 0.75
    assert agreement([None, None]) == 0.0


# ---------------------------------------------------------------- stats
def test_mcnemar_hand_computed():
    a = np.array([1, 1, 1, 1, 1, 0, 0, 1, 1, 0])
    b = np.array([0, 0, 0, 0, 1, 0, 1, 1, 1, 0])
    r = mcnemar_exact(a, b)
    assert (r["a_only_correct"], r["b_only_correct"], r["discordant"]) == (4, 1, 5)
    # exact two-sided binomial, k=4 of n=5: 2*(C(5,4)+C(5,5))/32 = 12/32
    assert r["p_value"] == pytest.approx(0.375)


def test_mcnemar_no_discordance():
    x = np.array([1, 0, 1])
    assert mcnemar_exact(x, x)["p_value"] == 1.0


def test_holm():
    assert holm([0.01, 0.04, 0.03]) == pytest.approx([0.03, 0.06, 0.06])


def test_paired_bootstrap_identical_is_zero():
    x = np.array([1, 0, 1, 1, 0])
    assert paired_bootstrap_diff(x, x, 500, 0) == (0.0, 0.0)


# ---------------------------------------------------------------- oncology filter
def _it(q, gold_text="Aspirin"):
    return Item("x", q, {"A": gold_text, "B": "Other"}, "A")


def test_filter_includes_patient_cancer():
    assert is_oncology(_it("A 60-year-old man with metastatic lung cancer presents with pain."))


def test_filter_excludes_relative_history():
    assert not is_oncology(_it("A 40-year-old man has chest pain. His father died of lung cancer."))


def test_filter_excludes_negated_and_phrases():
    assert not is_oncology(_it("MRI of the brain does not reveal a tumor or abscess."))
    assert not is_oncology(_it("He developed fever and rigidity.", "Neuroleptic malignant syndrome"))
    assert not is_oncology(_it("Which cytokine?", "Tumor necrosis factor-alpha"))


def test_filter_gold_only():
    it = _it("A 25-year-old with painless neck swelling.", "Classical Hodgkin lymphoma")
    assert is_oncology(it) and oncology_matches(it)["gold_hits"] == ["lymphoma"]


def test_distractor_alone_does_not_include():
    it = Item("x", "A 25-year-old with a sore throat.", {"A": "Pharyngitis", "B": "Lymphoma"}, "A")
    assert not is_oncology(it)


# ---------------------------------------------------------------- real processed data
def test_processed_onc_subset_integrity():
    p = ROOT / "data/processed/medqa_test_onc.jsonl"
    if not p.exists():
        pytest.skip("run scripts/prepare_data.py first")
    rows = [json.loads(l) for l in open(p)]
    ids = [r["item_id"] for r in rows]
    assert len(ids) == len(set(ids))
    assert all(r["answer_idx"] in r["options"] for r in rows)
    manifest = json.loads((ROOT / "data/processed/manifest.json").read_text())
    assert manifest["n_onc_primary_stem_or_gold"] == len(rows)


# ---------------------------------------------------------------- end-to-end (mock backend)
def test_end_to_end_mock(tmp_path):
    raw = tmp_path / "raw"
    for m in ["cot", "sc", "board_roles", "board_generic"]:
        subprocess.run([sys.executable, str(ROOT / "scripts/run_experiment.py"), "--dataset", "medqa_onc",
                        "--method", m, "--seed", "0", "--backend", "mock", "--limit", "12", "--chunk", "5",
                        "--out", str(raw)], check=True, capture_output=True)
    # resumability: rerunning must not duplicate records
    subprocess.run([sys.executable, str(ROOT / "scripts/run_experiment.py"), "--dataset", "medqa_onc",
                    "--method", "cot", "--seed", "0", "--backend", "mock", "--limit", "12", "--out", str(raw)],
                   check=True, capture_output=True)
    f = raw / "medqa_onc__cot__mock__seed0.jsonl"
    assert sum(1 for _ in open(f)) == 12
    board = [json.loads(l) for l in open(raw / "medqa_onc__board_roles__mock__seed0.jsonl")]
    assert all(r["calls"] == 9 and len(r["rounds"]) == 2 and len(r["rounds"][0]) == 4 for r in board)
    sc = [json.loads(l) for l in open(raw / "medqa_onc__sc__mock__seed0.jsonl")]
    assert all(len(r["samples"]) == 15 for r in sc)

    out = tmp_path / "res"
    proc = subprocess.run([sys.executable, str(ROOT / "scripts/evaluate.py"), "--raw", str(raw), "--out", str(out),
                           "--data-root", str(ROOT)], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    import pandas as pd
    res = pd.read_csv(out / "results.csv")
    assert {"cot", "sc@9", "board_roles.final", "board_generic.r1_vote"} <= set(res["variant"])
    assert (res["n"] == 12).all()
    assert res.loc[res.variant == "board_roles.final", "calls_per_item"].iloc[0] == 9
    comp = pd.read_csv(out / "comparisons.csv")
    assert (comp["role"] == "PRIMARY").sum() == 1
    assert (out / "figures/frontier__medqa_onc__mock__seed0.png").exists()
