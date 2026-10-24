# Research decisions log — Phase II (Prompts 06–07)

Continues L-01 to L-15 (Phase I). Labels: VERIFIED / INFERRED / UNKNOWN.

| ID | Prompt | Date | Decision | Reason | Evidence | Next action |
|---|---|---|---|---|---|---|
| L-16 | 06 | 2026-10-24 | Floor for "above chance" = 27.8% (majority letter), not 20% | Gold letter B over-represented in the oncology subset | `dataset_sanity_checks_output.json` (VERIFIED) | Update go/no-go and protocol |
| L-17 | 06 | 2026-10-24 | Record SC deviations (15 samples, top-p 0.95) from Wang et al. 2023 | Compute; SC@9 is a call-matched control, not a maximised SC | Wang et al. 2023 PDF (VERIFIED) | Report in Methods |
| L-18 | 06 | 2026-10-24 | Report results by source (MedQA, MedMCQA) as well as pooled | Item types differ (vignettes vs short recall) | MedMCQA README; MedQA lengths (VERIFIED) | Protocol tables |
| L-19 | 06 | 2026-10-24 | Gate runs on `leakage_checks.py` passing | Train/test and cross-dataset overlap UNKNOWN | Self-test (VERIFIED) | Kaggle notebook cell |
| L-20 | 07 | 2026-10-24 | Protocol v1.0 → v1.1 (pooling rule, MDE reporting, 27.8% floor, by-source tables, leakage gate, 3-comparison secondary family) | Prompt 05–06 decisions; no model output existed yet | Git history of `configs/frozen_protocol.yaml` | Freeze v1.1 |
| L-21 | 07 | 2026-10-24 | `evaluate.py` must match v1.1 before any real evaluation | Code still holds the v1.0 comparison list | Code read (VERIFIED) | Fix in Prompt 13 |
