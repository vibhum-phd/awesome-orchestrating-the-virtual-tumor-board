# Data

| File | Source | How it is produced | Committed? |
|---|---|---|---|
| `raw/medqa_test.jsonl` | MedQA USMLE 5-option test (Jin et al. 2021, MIT), copy in github.com/gersteinlab/MedAgents `datasets/MedQA/test.jsonl` | `git clone` (notebook cell 4); sha256 must equal `cfa75cbcc53c29b023752b0a395ff49d8202121041392735ae44771a5ec734a3` | no |
| `processed/medqa_test_all.jsonl` | above | `scripts/prepare_data.py` | yes |
| `processed/medqa_test_onc.jsonl` | above, filter v1.0 | `scripts/prepare_data.py` → 97 items | yes |
| `processed/onc_filter_audit.csv` | above | every item with matched terms and inclusion flag | yes |
| `processed/onc_subset_human_audit.csv` | above | **fill `human_label`**: 1 = oncology reasoning is central to the question, 0 = incidental | yes |
| `processed/manifest.json` | above | counts + hashes | yes |
| `processed/medmcqa_dev_onc.jsonl` | MedMCQA dev (Pal et al. 2022, MIT), HF `openlifescienceai/medmcqa` | `scripts/prepare_extra_data.py` (Kaggle) | after build |
| `processed/medqa4_test_all.jsonl` | HF `GBaker/MedQA-USMLE-4-options` (CC-BY-4.0) | `scripts/prepare_extra_data.py` | after build |
| `processed/medqa_train_pilot.jsonl` | MedQA train, 20 random items (seed 7) | pilot/debug only, never reported | after build |

No patient data is used. All items are published exam-style questions.
Leakage: zero-shot evaluation, so there is no training split to leak; prompts are debugged only on train items.
