# Prompt 01 output — Review scope

Saved: 2026-10-22 · Tool: Claude · Labels: VERIFIED / INFERRED / UNKNOWN
Prompt 01 SAVE item: "Workspace and decision log; review scope."
- Workspace → this repository (structure per assignment §9; first commit 2026-10-20)
- Decision log → `research_decisions.md` (Phase I entries L-01 to L-05)
- Review scope → this file

## Prompt as used
> I am a postgraduate student converting my completed literature review into an implementation-based research paper. My topic is **Orchestrating the Virtual Tumor Board: AI- and multi-agent-assisted oncology decision support**. Act as a critical research mentor and technical pair programmer. Guide me in stages: evidence-based gap identification, literature-to-experiment mapping, feasibility, research questions, verified baseline, coding, experimental evaluation, manuscript and reproducibility. Mark statements as VERIFIED, INFERRED or UNKNOWN, and explicitly request source files or outputs when evidence is missing. Never invent papers, datasets, repository links, code execution, experiments or metrics. Help me create a portable research_decisions.md log containing decisions, reasons, source/evidence and next actions. Start by asking me to attach my existing review and summarize its scope without assuming unseen content.

Review supplied: `LiteratureReview_T32_VibhumSharma.pdf` (Lab 4, 17 pages, 6,459 words extracted).

## Scope summary
The review is a narrative synthesis of 24 papers (2011–2026) on AI support for tumor boards, with no data or experiments of its own. Everything below is VERIFIED against the extracted review text only, not against the underlying papers.

| Aspect | What the review covers |
|---|---|
| Question | How AI has been used and evaluated as decision support for multidisciplinary and virtual tumor boards |
| Corpus | 24 papers found with Semantic Scholar, ResearchRabbit, Litmaps and Elicit; seeds from Labs 1–3 |
| Three technology generations | Rule-based CDSS (Watson for Oncology, 2018–2021) → single-pass LLMs (2023–2026) → multi-agent systems (2025–2026) |
| Five themes | AI–MDT concordance; multi-agent architectures; VTB implementation; systematic reviews / meta-analyses; cancer-type and task-specific studies |
| Headline claims | Concordance "typically 60% to over 90%" (Abstract); 23–99% across 59 studies (Wu et al. 2026); EvoMDT "comparable to human MDTs", 30–40% faster (Liu et al. 2026) |
| Central pattern | The "complexity gap": AI does well on guideline-clear cases, worse on rare / multimodal / genomically complex ones |
| Stated gaps (Sec. 7) | Few prospective or blinded studies; no patient-outcome links; no reporting standard; thin independent validation of multi-agent systems; LMIC settings missing; cost and governance unstudied |

## What the review does not cover
- No benchmark datasets, code or released models are analysed; only EvoMDT's public QA benchmarks are mentioned.
- Imaging, pathology and genomic inputs come up only as a limitation, not as a theme.
- No AI study from a low- or middle-income setting; India appears only via the non-AI National Cancer Grid VTB.

## Housekeeping problems found while summarising (VERIFIED)
- Doğan et al. (2025), Konzmann et al. (2026) and D. Wang et al. (2025, *iScience*) are in the reference list but never cited in the text.
- Lukac et al. (2023) is cited in Sec. 2.2 but missing from the reference list.
- "Wang et al. (2025)" in Sec. 3.2 is ambiguous: two Wang 2025 papers are listed.
- Internal cross-references ("Section 9", "6.4", "5.2") do not match the review's 1–9 numbering (decision L-03).
