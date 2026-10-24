---
title: "AI Provenance and Research-Integrity Report — Lab 7"
subtitle: "Does the Virtual Tumor Board Need a Board? (Topic T32)"
author: "Vibhum Sharma · AI Tools for Research · 24 October 2026"
---

# 1. Scope and sources

This report covers Lab 7 from 20 to 24 October 2026. It is built only from records that exist:

| Source | Location |
|---|---|
| Student's own messages (authentic prompt log) | `authentic_prompt_log.md` (this folder) |
| Prompts as applied to each assignment step | `00_prompt_used.md` in each of the 18 prompt folders |
| Code history: 11 commits up to `bd6ba9a` (end of Phase V); 127 files, +6,226 / −146 lines since the first commit | `git_history.txt`; repository `AITR_Lab02_Project` |
| Errors and fixes | Phase III `debugging_log.md` (DBG-01 to DBG-12); Phase V `repository_readiness_check.md` (R1–R4) |
| Decisions | `research_decisions.md`, L-01 to L-47 |
| Verification of literature | `paper/bib_verification.md` |
| Test runs | `test_logs/`, `docs/py311_test_log.txt`, `reproduction_log_fresh_clone.txt` |

**State of the evidence.** No model experiment has been run. There is no GPU and no Hugging Face access in the AI workspace. Every result is therefore PENDING Kaggle runs. Nothing in this report describes a model result, a performance gain or a GPU execution, because none exists.

# 2. How the work was actually divided

This is the most important finding of the audit, so it comes first.

- **AI tool used:** one tool, Claude (Opus 5.5) on claude.ai, with web search, web fetch and a sandboxed Linux workspace (CPU only). No other AI tool was used in Lab 7. If the student used another tool (ChatGPT, Copilot, Elicit…), it must be added here; this report cannot know.
- **What the student did in-session:** supplied the assignment and his own Lab 4 review; set the scope and pace (submit Prompts 1–2 only; then 3–4 with named deliverables; then all phases, phase by phase); asked where the SAVE items were. His messages are short instructions ("Continue."), quoted verbatim in `authentic_prompt_log.md`.
- **What the AI did:** proposed the gap, the research question, the design, the protocol, all code, all tests, the debugging, the literature checks, the paper and this report. It also ran every verification.
- **Consequence:** the "Human decision" column below is honest only if it distinguishes a decision the student made from one he accepted by continuing. Where the student has not yet reviewed a decision, it says **"Accepted by continuing — student review pending"**. Not objecting is not the same as deciding. The sign-off sheet (`human_decision_signoff.md`) lists the decisions the student must check and own before submission. The assignment says "Your reasoning must be yours"; that sheet is where it becomes true.

# 3. Significant AI-assisted activities

Tool for every row: Claude (Opus 5.5). "Prompt" = the assignment prompt applied (text in that folder's `00_prompt_used.md`) plus the student's instruction.

| # | Task (prompt) | AI proposal | Human decision | Verification method | Code / result change | Outcome |
|---|---|---|---|---|---|---|
| A1 | Gap selection (P01–02) | Five gaps from the Lab 4 review, ranked; G4 "board vs call-matched single model" chosen | Student chose to stay with his own review (assignment continuity rule); gap choice accepted by continuing — **review pending** | Review text extracted and searched; EvoMDT PDF read for its baselines | Gap matrix; 5 errors found in the student's own review (EvoMDT datasets called "oncology"; wrong first author; reference cited but missing; abstract vs Table 1 range; EvoMDT tie on MedQuAD not stated) | VERIFIED gap grounded in review §6–7 |
| A2 | Submission scope (P01–04) | Full 18-prompt plan | **Student decision:** submit only P01–02, then P03–04 with the deliverables he named | — | Trimmed submission folders | Submitted 22 and 23 Oct |
| A3 | Novelty check (P03–04) | Narrow the claim after finding Kim et al. 2025 (roles and discussion already tested in oncology) | Accepted by continuing — review pending | Kim et al. full PDF text (31 pages) | Claim narrowed to call matching, public data, open 7B model, error flips (L-08) | VERIFIED; but MDAT (Kuerbanjiang 2025) was missed here — see L3 |
| A4 | Data access (P06) | Load MedQA from Hugging Face | — | `curl` → proxy 403 | GitHub copy used; sha256 recorded and re-checked in a fresh clone | VERIFIED hash `cfa75cbc…a734a3` |
| A5 | Oncology filter (P06, P09) | Keyword filter v0.9 → 121 items | Accepted v1.0 by continuing; **human audit of 97 items not done (0/97 labelled)** | AI printed and read the match context of all 121 items | v1.0 → 97 items (DBG-02) | Filter rebuilt before any model run |
| A6 | Power and success criteria (P05) | Exact McNemar power; n = 97 detects only ≈12–15 points; pool MedMCQA | Accepted by continuing — review pending | Exact power checked against simulation | Protocol: pooled primary set, MDE reporting (L-13, L-14) | VERIFIED as computation; MedMCQA n still unknown |
| A7 | Frozen protocol (P07, P16) | v1.0 → v1.1 → v1.2, all before any run | Accepted by continuing — review pending | Change history in the YAML header; tests read the pairs from the YAML | `configs/frozen_protocol.yaml` | Frozen; no run yet, so no results were affected |
| A8 | Baseline code (P08–09) | Data, parser, backends, CoT/SC/board, statistics, runner | Accepted by continuing — student has not yet run it | 46 tests (Python 3.13 and 3.11), mock end-to-end run, fresh clone | 6 modules + 9 scripts | VERIFIED on CPU; GPU path [TEST REQUIRED] |
| A9 | Debugging (P11) | 12 cases from real error messages | — | Each fix has a test or re-run | DBG-01 to DBG-12 (DBG-11 later closed) | 10 fixed, DBG-05 not fixable, DBG-12 needs Kaggle |
| A10 | Kaggle notebooks (P08, P10, P12) | 3 notebooks with STOP cells and gates | **Not run yet** | JSON validity; commands match the README | `notebooks/01–03` | [TEST REQUIRED] |
| A11 | Evaluation (P13) | Protocol-driven `evaluate.py`; pairing and settings audit; mock-output refusal in the paper tables | Accepted by continuing | Tests; mock demo kept in `SYNTHETIC_…` folders with watermarks | DBG-11 fix; token columns | VERIFIED on mock; real CSVs PENDING |
| A12 | Interpretation plan (P14) | Pre-registered decision table for every outcome, including nulls | Accepted by continuing — **interpretation must be the student's once results exist** | — | Outline with slots only | PENDING |
| A13 | Manuscript (P15) | 5-page LaTeX draft; 20 then 23 references | Accepted by continuing — review pending | Every reference opened at source; build log | `paper/` | Metadata VERIFIED for all 23; 2 claims INFERRED |
| A14 | Peer review (P16) | Self-review: 5 major, 8 minor concerns | Revisions applied by the AI; title decision (M5) left to the student | One new literature search, full text read | v0.2; protocol v1.2 | 9 of 13 fixed; **independent human review still needed** |
| A15 | README (P17) | Public README with run-status labels | Accepted by continuing | Run from two fresh clones; secrets/weights scan | 2 README errors fixed (R1, R2) | VERIFIED on CPU |
| A16 | This report (P18) | Built from the logs listed in §1 | Student must check §2 and sign the sign-off sheet | Every claim points to a file | — | — |

# 4. Real AI limitations, manual corrections and purposeful verification

The assignment asks for at least three. There were eleven. "Caught by" is stated honestly: in almost every case the AI caught its own error through a test or a source check that it ran. The student did not catch any of these himself in-session.

| # | What went wrong | Evidence | Caught by | Correction |
|---|---|---|---|---|
| L1 | **AI-written parser was wrong twice.** v1 read "Answer: A patient with…" as option A; v2 rejected the normal answer "Answer: C. Tell the attending…" | DBG-01, DBG-09; `parse_v2_vs_v3.txt` | Unit tests written before the code was used | Parser v3; 5 more test cases |
| L2 | **AI-written oncology filter over-included.** v0.9 counted "His father died of lung cancer", "neuroleptic malignant syndrome", "tumor necrosis factor-α" as oncology | DBG-02; match-context printout | Reading all 121 matches | Filter v1.0 (97 items); human audit still pending |
| L3 | **Literature details typed from memory or missed.** vLLM venue written as "29th" and "ACM" Symposium (source says only "SOSP 2023"); MedAgentsBench first author written as "Tang" (it is Shao), and that error was carried into two later files; EvoMDT year; the closest oncology study (Kuerbanjiang et al. 2025) listed but not analysed in the novelty check | `bib_verification.md` corrections; Prompt 04 addendum | Opening each source while building the `.bib`; the self-review | Corrected in place with dated notes; novelty matrix addendum |
| L4 | **Claims from AI summaries, not from reading.** "MDAgents includes a self-consistency baseline"; the MedAgentsBench findings; the 56.79% Qwen2.5-7B anchor value came from a summariser model reading arXiv 2501.06458 | `bib_verification.md`; `ai_assistance_log.md` #6 | Labelling rule (VERIFIED / INFERRED) | Kept as INFERRED and marked [TO VERIFY] in the paper; **student must read these three tables** |
| L5 | **Code drifted from the specification.** `evaluate.py` still compared the four v1.0 pairs after the protocol named three | DBG-11 | AI audit of code against protocol | Pairs now read from the YAML; test added |
| L6 | **Wrong semantics in an AI-written check.** `env_check.py` reported GitHub unreachable because an HTTP 400 was treated as "no connection" | DBG-08 | Contradiction with a working `git clone` | HTTP errors count as reachable |
| L7 | **Silent data loss risk.** Truncated completions were not recorded at all | DBG-10 | Code review while writing the baseline report | `finish_reason` stored; truncation rate reported per arm |
| L8 | **Documentation that was never run was wrong.** README gave the wrong argument for the sanity script and the wrong expected test count | R1, R2; `reproduction_log_fresh_clone.txt` | Running the README from a fresh clone | Fixed in commit `a398cff` |
| L9 | **Overclaiming in prose.** The paper's AI statement said every citation had been checked against its source; two claims had not | Peer review m1 | Self-review | Reworded |
| L10 | **Portability bug.** A backslash inside an f-string expression fails on Python < 3.12 (Kaggle) | Prompt 15 flag F4 | Compiling and testing under Python 3.11 | Fixed; 46/46 on 3.11 |
| L11 | **Process deviation.** The student's standing preference is to be asked before other tools are used while a paper is being drafted. The AI used web search and web fetch in Prompts 15–16 without asking | `authentic_prompt_log.md` (note at the end) | This audit | Disclosed. The use was read-only; the results are in `bib_verification.md` |

Also recorded: environment limits that the AI could not work around and did not hide. Hugging Face was blocked (DBG-03); the EvoMDT repository needed login (DBG-05, recorded UNKNOWN); there was no GPU. The response was to stop at the GPU boundary, not to simulate results. Mock-backend outputs are watermarked SYNTHETIC, and the paper-table script refuses them (verified: exit 1).

# 5. Which conclusions depend on human reasoning

No scientific conclusion exists yet, because there are no results. What exists are design choices and pre-registered rules. They fall into three groups:

**Made by the student**

- Building on his own Lab 4 review.
- Submission scope and phasing.
- Resource limits: free Kaggle/Colab T4 and his own GTX 1050 Ti (recorded in L-04).

**Proposed by the AI, which the student must now judge** (`human_decision_signoff.md`)

- The gap and the narrowed novelty claim (L-05, L-08).
- Exam MCQs as the proxy for tumor-board decisions.
- The choice of model and datasets.
- The primary comparison, thresholds and Holm family.
- Pooling MedQA with MedMCQA, and the fallback.
- Adding SC@15 (v1.2).
- The interpretation table for each outcome.
- The title (review M5).

**Must be human by construction, and still to be done**

- Labelling the 97 oncology items.
- Reading MDAgents Table 2, the MedAgentsBench table and arXiv 2501.06458 Table 1.
- Accepting or rejecting the baseline (B1–B8) before `results/baseline/VALIDATED` is created.
- Interpreting the real results.
- An independent review of the paper.
- Confirming every literature claim before submission.

# 6. What was learned about vibe coding

1. **Tests, not reading, found the bugs.** Both parser errors looked correct on screen. Writing the edge case first (L1) caught them before any model output depended on them.
2. **Fluent code drifts from its spec.** The evaluator still followed an old protocol after the protocol changed (L5). The fix was to make the code read the spec, not to remember to update it.
3. **A mock backend is useful and dangerous.** It made end-to-end testing possible without a GPU. But random outputs that look like results are an integrity risk. Watermarks plus a hard refusal in the paper-table script were needed.
4. **"Documented" is not "reproducible".** The README was wrong in two places until it was run from a clean clone (L8).
5. **The AI fills gaps from memory.** Venue names, author order and baseline details were confidently wrong or unchecked (L3, L4). The VERIFIED / INFERRED label on every claim was the control that worked.
6. **Gates beat good intentions.** The notebooks stop at STOP cells. Notebook 03 refuses to start without the baseline file. That keeps "run everything and see" from happening.
7. **Speed hides authorship.** The AI produced 6,000+ lines in four days. The student gave scope and pace but has not yet reviewed most of it (§2). The main risk of vibe coding here is not wrong code but a student who cannot defend correct code.

# 7. Remaining risks

| Risk | Status | Mitigation |
|---|---|---|
| vLLM on Kaggle 2×T4 never tested | UNKNOWN | Notebook 01 smoke test; 3B/AWQ fallback via a logged protocol change |
| MedMCQA oncology n unknown; the primary test may be underpowered | UNKNOWN | MDE reported; "exploratory" label if n < ~200 |
| Three INFERRED literature claims | Open | Student reads the tables |
| Oncology filter not human-audited | 0/97 labelled | Audit CSV; sensitivity analysis on audited items |
| Peer review was AI self-review | Open | Supervisor or peer review of v0.2 |
| Benchmark contamination in pre-training | Cannot be removed | Stated as a limitation |
| Compute estimate (7–19 GPU-h) is INFERRED | Open | Replace with the measured smoke-test time |
| GPU dependencies unpinned | Deliberate | Pin from `pip_freeze.txt` after notebook 01 |
| Student ownership of AI-proposed reasoning | Open | Sign-off sheet; student explains each design choice in his own words |
| The `00_prompt_used.md` files show the assignment prompt applied by the AI, not text the student typed | Disclosed here | Verbatim student messages kept in `authentic_prompt_log.md` |

# 8. Integrity statement

Nothing in Lab 7 reports a model result, and no execution log, fix or gain was invented. Every error listed above has a file behind it. Where a decision was the AI's and the student has not yet reviewed it, this report says so.
