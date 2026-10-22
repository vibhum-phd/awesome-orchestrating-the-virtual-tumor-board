# Does the virtual tumor board need a board? A call-matched evaluation of multi-agent LLM deliberation on oncology exam questions

**Status:** Gate G1 complete (research brief, frozen protocol, tested code). No model results yet.

## Research question
Does a 4-specialist LLM tumor board (medical, surgical and radiation oncologist, pathologist; 2 rounds + chair = 9 calls) answer oncology vignettes more accurately than one model sampled 9 times with majority vote (self-consistency), on the same open-weight backbone? Ablations: generic agents instead of specialty roles; voting instead of discussion + chair. See `research_brief_G1.md`.

## Repository
```
configs/frozen_protocol.yaml      frozen settings (v1.0)
src/vtb/                          data, parser, backends, methods, stats
scripts/prepare_data.py           MedQA test -> all + oncology subset + audit files   [VERIFIED locally]
scripts/prepare_extra_data.py     MedMCQA-dev oncology, MedQA 4-option, pilot items  [TEST REQUIRED: needs HF]
scripts/run_experiment.py         one (dataset, method, seed) cell -> results/raw/*.jsonl (resumable)
scripts/evaluate.py               integrity checks, results.csv, comparisons.csv, figures
notebooks/01_env_sanity_smoke_kaggle.ipynb   day-one notebook for Kaggle
tests/test_core.py                29 tests incl. mock end-to-end                      [VERIFIED locally]
data/                             see data/README.md
research_decisions.md · baseline_validation.md · ai_assistance_log.md
```

## Reproduce
```bash
pip install -r requirements.txt                        # analysis + tests (CPU)
python -m pytest -q tests                              # VERIFIED: 29 passed (Python 3.13, CPU)
python scripts/prepare_data.py --src data/raw/medqa_test.jsonl --out data/processed   # VERIFIED
pip install -r requirements-gpu.txt                    # [TEST REQUIRED] Kaggle 2xT4
python scripts/prepare_extra_data.py --out data/processed                             # [TEST REQUIRED]
# main grid (per configs/frozen_protocol.yaml)                                        # [TEST REQUIRED]
for ds in medqa_onc medmcqa_onc; do for s in 0 1 2; do for m in cot sc board_roles board_generic; do
  python scripts/run_experiment.py --dataset $ds --method $m --seed $s --backend vllm; done; done; done
for m in cot sc board_roles board_generic; do
  python scripts/run_experiment.py --dataset medqa_all --method $m --seed 0 --backend vllm; done
python scripts/evaluate.py --raw results/raw --out results                            # [TEST REQUIRED on real runs]
python scripts/evaluate.py --raw results/raw --out results/sensitivity_audited \
    --restrict-ids data/processed/onc_subset_human_audit.csv                          # after human audit
```
Plumbing check without a GPU (synthetic outputs — never report): add `--backend mock`.

## Compute
Kaggle free tier, 2× NVIDIA T4. Estimated 7–19 GPU-hours for the full grid (INFERRED; replace with the measured value from the smoke test).

## Limitations (known in advance)
Exam MCQs are a proxy for tumor-board decisions; no RAG, images or real patient data; small oncology subset; keyword-defined oncology scope; possible pre-training contamination of public benchmarks; one backbone family.

## Data and licences
MedQA (Jin et al. 2021) — MIT; MedMCQA (Pal et al. 2022) — MIT; MedQA 4-option HF copy — CC-BY-4.0 (dataset card). Code: MIT (see LICENSE). Raw data is not committed; `data/README.md` explains how to get it.

## Citation
[TO ADD once the paper exists]
