# Prompt 02 output — Gap matrix: source evidence → candidate question → possible experiment

Saved: 2026-10-22 · Tool: Claude · Labels: VERIFIED / INFERRED / UNKNOWN
Prompt 02 SAVE item: "Gap matrix: source evidence → candidate question → possible experiment."

## Prompt as used
> Analyze my attached literature review **[LiteratureReview_T32_VibhumSharma.pdf]**. Identify central methods, datasets, measured findings, author-reported limitations and unresolved questions. Propose five computationally testable research gaps. For each, cite the specific passage or reference in my review; clearly distinguish a limitation reported in the original paper from your own inference; state the experimental question it suggests and what evidence would test it. Flag any claims needing verification against the original publications. Rank three gaps by research significance, available resources and implementation feasibility. Do not claim novelty without a separate literature search.

Method: the review was read in full; each limitation was then searched for in the 7 original PDFs available in the course project (EvoMDT; Park & Chae; Thiagarajan et al.; X. Wang et al. *iScience*; Zengin Deniz et al.; neuro-oncology VTB; hypofractionation VTB). A limitation is labelled "original" only where that paper's own text states it.

## A. What the review contains

| Element | Extracted from review (section) | Checked in original? |
|---|---|---|
| Methods | Retrospective concordance (% agreement, Cohen's kappa) (3.1); single-pass LLM prompting with a case summary, sometimes with injected guidelines (2.3, 3.1); multi-agent systems with retrieval + consensus (2.3, 3.2); systematic reviews / meta-analysis (3.4) | — |
| Datasets | Institutional case series, "commonly 10–100 cases" (6); EvoMDT: six public QA sets + four real-world sets (3.2) | EvoMDT: MedQA, MedQA-Cancer, MedMCQA-Cancer, MedQuAD, MedQARo, ROND; real-world data "on request" (VERIFIED) |
| Measured findings | WFO 93% (breast, 638 cases); 23–99% across 59 studies; EvoMDT beats Llama-3-70B, Claude-3, Med-PaLM 2 and is 30–40% faster (2.2, 3.2) | EvoMDT MedQA 0.86 vs 0.76 (Llama3-70B) / 0.79 (Claude-3); 30–40% faster (VERIFIED). Park: 86.96% WFO–MTB, 322 gastric patients (VERIFIED; not quoted in review) |
| Author-reported limitations | Retrospective, single-centre, small samples; no outcome link; inconsistent metrics (6) | Park: retrospective single-centre; concordance only; no survival/time/cost data; guidelines differ by country (VERIFIED). EvoMDT: limited scale and geographic diversity; no prospective/outcome study; GI non-HCC, gynaecologic, sarcoma, rare tumours untested (VERIFIED). Thiagarajan: no patient follow-up data (VERIFIED). X. Wang: data bias, uneven generalizability, limited prospective validation (VERIFIED) |
| Unresolved questions | Do AI-assisted boards change outcomes? Do multi-agent gains hold independently? Do results transfer to LMIC settings? Can text-only systems handle multimodal cases? (7, 8) | — |

## B. Gap matrix

| Gap | Review passage (source evidence) | Original paper says vs. my inference | Candidate question | Possible experiment / evidence that would test it |
|---|---|---|---|---|
| **G1. Complexity gap** | Sec. 6 "complexity gap"; Sec. 3.1 Seshachalam "AI paradox" | **Original:** Park — concordance falls with age, performance status, stage IV (VERIFIED). **Inference:** exam vignettes can stand in for case complexity. | Does LLM accuracy on oncology vignettes drop as a pre-defined complexity proxy rises, and does a multi-agent board narrow that drop? | Accuracy + 95% CI per stratum (USMLE Step 1 vs Step 2/3, or model agreement); stratum × method interaction |
| **G2. Answer instability** | Sec. 2.2 "inconsistent recommendations across repeated queries"; Sec. 6 | **Review synthesis only:** its source (Lukac et al.) is missing from the reference list; no available original states it (UNKNOWN). | How often does the same model change its answer to the same oncology case under resampling, paraphrase or option reordering? | Answer-flip rate and Fleiss' kappa over 10 runs/item; accuracy change under option shuffling |
| **G3. Transfer across countries / guidelines** | Sec. 7 fifth gap (LMIC settings) | **Original:** Park — Korean guidelines differ from US-based WFO knowledge (VERIFIED); EvoMDT — limited geographic diversity (VERIFIED). **Inference:** exam source is a usable proxy for practice setting. | Does a model's oncology accuracy differ between US (MedQA) and Indian (MedMCQA) exam items once topic is matched? | Accuracy gap + CI on topic-matched subsets; error categories where guidelines differ |
| **G4. Multi-agent claims lack independent, fair comparison** | Sec. 7 fourth gap; Sec. 3.2 recency; Sec. 6 "new failure surfaces … not yet well characterized" | **Original:** EvoMDT needs external validation (VERIFIED); its backbone is DeepSeek V3/R1 but its MCQ baselines are other single-pass models (VERIFIED). **Inference:** the gain may come from more inference calls or a different backbone, not deliberation; no same-backbone, call-matched baseline found in the text (INFERRED; figures not checked). | With the backbone fixed, does a specialist-role board beat the same model voting over the same number of calls? Do roles matter? Does discussion spread errors? | Paired accuracy (McNemar) board vs self-consistency@9; role ablation; correct→wrong flip counts; tokens per item |
| **G5. Text-only inputs** | Sec. 8 fourth direction; Sec. 2.2 "cannot access imaging or pathology data" | **Original:** EvoMDT — untested on raw unstructured records (VERIFIED). **Inference:** adding image data changes accuracy; no reviewed study tests it. | Does adding an image (or its report) to the text case change a vision-language model's oncology answers? | Text-only vs text+image accuracy on a public multimodal oncology benchmark (access UNKNOWN) |

Considered and dropped: concordance-metric heterogeneity (Sec. 6; Carl 2024, Wu 2026) and the patient-outcome link (Sec. 7). Both need case-level tumor-board decisions or follow-up data with no public source, so they are not computationally testable here.

## C. Ranking (1 = weak, 3 = strong)

| Rank | Gap | Significance | Resources | Feasibility (4 weeks, free T4 GPUs) | Total |
|---|---|---|---|---|---|
| 1 | G4 Multi-agent fair comparison | 3 — tests the review's strongest, least-validated claim | 3 — MedQA (MIT, VERIFIED); open 7B model | 3 — text-only, inference-only | **9** |
| 2 | G1 Complexity gap | 3 — the review's central pattern | 3 — same data | 2 — complexity proxy for exam items is weak | **8** |
| 3 | G2 Answer instability | 2 — known LLM issue, less tumor-board-specific | 3 — same data | 3 — resampling only | **8** |
| — | G3 Country transfer | 2 | 3 — MedMCQA (MIT, VERIFIED) | 2 — exam style confounded with guidelines | 7 |
| — | G5 Multimodal | 3 — fits PhD focus | 1 — dataset access UNKNOWN | 1 — VLM inference on T4 is tight | 5 |

G1 beats G2 on the tie because the review's conclusion rests on it. Provisional choice: G4, with G1 as a secondary analysis inside the same experiment. **No novelty claimed** — whether MDAgents, CoMMa or other medical multi-agent studies already use a same-backbone, call-matched baseline is UNKNOWN (Prompts 03–04).

## D. Claims flagged for verification against originals

| Claim in review | Status | What the original shows / action |
|---|---|---|
| EvoMDT beats Llama-3-70B, Claude-3, Med-PaLM 2 (3.2) | VERIFIED, with caveat | MedQA 0.86 vs 0.76 / 0.79; but on MedQuAD EvoMDT ties Med-PaLM 2 (BERTScore 0.63 vs 0.63) → "matches or outperforms" |
| EvoMDT comparable to human MDTs, 30–40% faster (3.2, Table 1) | VERIFIED | EvoMDT abstract; speed measured on structured dossiers only |
| EvoMDT needs external validation (3.2) | VERIFIED | Authors' limitations section |
| Park & Chae: WFO–MTB concordance in gastric cancer (3.5) | VERIFIED | 86.96%, 322 patients; online 2023, issue 2024, 55:365–372 — add the figure to the review |
| Thiagarajan: national VTB programme in India (2.1) | VERIFIED | Also reports no patient follow-up data |
| EvoMDT used "six public **oncology** QA datasets" (3.2) | NEEDS CORRECTION | EvoMDT calls MedQA "a general medical examination dataset" → "medical and oncology QA datasets" |
| "Wang, D., et al. (2025)", *iScience* | NEEDS CORRECTION | First author is Xiaodong Wang |
| "Lukac et al., 2023" (2.2) | NEEDS CORRECTION | Cited but missing from reference list |
| Concordance "60% to over 90%" (Abstract) vs "~56–87%" (Table 1) vs 23–99% (Wu) | NEEDS CORRECTION | Internally inconsistent; state range with its source |
| WFO 93%, 638 breast cases (Somashekhar 2018) | UNKNOWN | Original not available |
| 23–99% across 59 studies (Wu 2026) | UNKNOWN | Original not available |
| "AI paradox" (Seshachalam 2026) | UNKNOWN | Conference abstract; get full text |
| Carl 2024: no LLM-specific reporting standard | UNKNOWN | Original not available |

Extra source (in project files, not in the review): Zengin Deniz et al. (2026, *Updates in Surgery*) — 47 general-surgery patients; ChatGPT fully concordant 38.3%, at least partly 85.1% (VERIFIED); discordance centred on resectability and staging → supports G1.
