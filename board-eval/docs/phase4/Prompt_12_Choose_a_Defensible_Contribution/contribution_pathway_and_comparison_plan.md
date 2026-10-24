# Prompt 12 output — Contribution pathway and executable comparison plan

Saved: 2026-10-24 · Labels: VERIFIED / INFERRED / UNKNOWN
Prompt 12 SAVE item: "Chosen contribution pathway and executable comparison plan."

**Precondition not yet met.** The prompt assumes "my baseline has been validated, and its actual results are [RESULTS]". It has **not** been validated on a real model yet (Prompt 10 Part B is PENDING). The choice below is therefore **provisional**: it is re-confirmed or changed once the baseline numbers exist (§5). The comparison notebook enforces this: it will not start without the baseline sign-off file.

## 1. Inputs
- **Baseline:** greedy CoT + self-consistency on Qwen2.5-7B-Instruct (code validated by audit and tests; real results PENDING).
- **Research question:** RQ1–RQ3 (Prompt 05).
- **Literature evidence:** EvoMDT (single-pass baselines on other backbones, VERIFIED); Kim et al. 2025 (roles help in discussion, not voting; LLM judge; unequal calls, VERIFIED); MDAgents CoT-SC baseline (INFERRED); Wang et al. 2024 and Smit et al. 2023 (sampling competitive, abstracts VERIFIED).

## 2. Three pathways compared (at the level of this code base)

| | A. Reproduce under a new condition | B. Controlled comparative study | C. Targeted modification |
|---|---|---|---|
| Scientific question | Do Kim et al.'s Group-Chat gains hold on public MCQs with an open model? | At equal calls and the same model, does a specialist board beat SC@9; do roles and discussion matter? | Does running round 2 **only when round-1 members disagree** keep board accuracy at fewer calls? |
| Expected code changes | Re-implement AG2 Group Chat (8-turn moderated debate, recruiter); their code is unlicensed, so rewrite from the paper | **None** to the methods: `run_cot`, `run_sc`, `run_board` (roles / generic) already exist and are tested | One isolated change in `run_board`: skip round 2 when round-1 is unanimous; everything else untouched |
| Compute burden | High: Group Chat is about 8 turns × 5 agents + manager + summariser per item | ≈ 34 calls/item for all four arms (INFERRED until the smoke test) | Fewer board calls on unanimous items; depends on the unanimity rate (UNKNOWN) |
| Advantages | Closest to the published system | Directly answers the gap; every arm shares one backbone and budget; ablations come free from stored rounds | Practical efficiency result; tests one change |
| Failure risks | Our re-implementation may differ from theirs, so a mismatch is hard to interpret | Underpowered on MedQA-onc alone (detectable effect ≈ 12–15 pp) | Benefit could be just "fewer calls", which needs its own call-matched control; adds a new arm and more analyses |
| Evidence needed | Their exact prompts and turn logic (not public under a licence) | Paired accuracy, McNemar + MDE, flip rates, tokens | Accuracy-vs-calls curve against the unmodified board |
| Verdict | Not chosen | **Recommended** | Possible later extension; **not** pre-registered, so not run now |

**Recommendation: B.** It is the only pathway whose code already exists and passes its tests, whose comparisons are fully call-matched, and whose ablations (roles, discussion, chair) come out of the same runs without new compute. It is also the pathway the gap asks for. **No novelty beyond this is claimed:** B extends Kim et al. 2025 and MDAgents to a call-matched, public, open-model setting (Prompt 04).

## 3. Fair test plan (protocol v1.1)

| Comparison | Role | Why it answers the question |
|---|---|---|
| Specialist board (final, 9 calls) vs SC@9 | PRIMARY | Same model, same calls: isolates "board" from "more inference" |
| Specialist vs generic board | Secondary (Holm) — **role ablation** | Same pipeline and calls; only the system role changes |
| Round-2 vote vs round-1 vote | Secondary (Holm) — **discussion ablation** | Same members; only the discussion round differs |
| Specialist board vs CoT | Secondary (Holm) | The comparison earlier papers made; shows how much a 1-call baseline flatters the board |
| Board final vs round-1 vote; generic board vs SC@9 | Exploratory | Chair contribution; whether any board structure beats sampling |

**Failure analyses (deep analysis):** C→W / W→C member flips with cluster CIs; chair override vs final-round majority; accuracy by round-1 agreement stratum; parse failures and truncation per arm; seed variation.
**Controls held constant:** model, weights, answer instruction, sampling settings, max tokens, parser, items, seeds.
**Power:** primary set pooled (MedQA-onc + MedMCQA-onc); every null reported with its exact MDE (Prompt 13).

## 4. Executable comparison plan
`notebooks/03_main_grid_kaggle.ipynb` (in this folder):
1. **Gates:** baseline sign-off file exists; leakage-gate outputs show 0 flagged pairs.
2. Primary set, seed 0, all four arms → the runs the primary analysis needs.
3. Full MedQA, seed 0, all four arms (cut first if quota runs short).
4. Primary set, seeds 1–2 (cut second).
5. `evaluate.py` (integrity first) → zip of `results/`.

Calls per item: CoT 1, SC 15 (scored at k = 1, 3, 5, 9, 15), specialist board 9, generic board 9 = 34. Commit hash written to `results/COMMIT_USED.txt`.

## 5. If the real baseline numbers change the picture
| Baseline finding (Prompt 10 Part B) | Effect on this choice |
|---|---|
| CoT ≤ 27.8% on MedQA-onc | B is not informative with this model → switch backbone (logged protocol change) before any comparison |
| Parse failures or truncation > limits | Fix on train items for all arms, then proceed with B |
| SC@k flat from k = 1 to 15 | B still valid; note that sampling gives no gain, so a board gain would come from structure |
| Measured cost ≫ estimate | Keep B; cut runs in the notebook's order |

## 6. If a modification (pathway C) is chosen later
Change only `run_board`'s round-2 trigger behind a new method name (e.g. `board_roles_adaptive`). Leave `run_board`, `run_sc`, `run_cot` and the parser byte-for-byte unchanged (verify with `git diff`). Add one new comparison to a **new** protocol version before running it. Compare against the unmodified board and against SC at the same mean number of calls.

## 7. Decision-log entries (Prompt 12)

| ID | Date | Decision | Reason | Evidence | Next action |
|---|---|---|---|---|---|
| L-34 | 2026-10-24 | Provisionally choose pathway B; re-confirm after baseline Part B | Code exists and is tested; fully call-matched; ablations at no extra compute | §2 | Re-confirm after `baseline_outputs.zip` |
| L-35 | 2026-10-24 | Pathway C (adaptive discussion) not run in this study | Not pre-registered; would need its own call-matched control | §2 | Mention as future work |
| L-36 | 2026-10-24 | Notebook 03 refuses to start without the baseline sign-off and leakage gate | Prompt 10: validate before comparing | Notebook gate cell | — |
