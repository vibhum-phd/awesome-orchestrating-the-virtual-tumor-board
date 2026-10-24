"""Inference methods compared in this study. All share the same answer instruction and
the same backbone; they differ only in how inference calls are organised.

  cot            : 1 greedy chain-of-thought call                         (baseline B1)
  sc             : k_max sampled CoT calls, plurality vote on first k     (baseline B2, call-matched at k=9)
  board_roles    : virtual tumor board, 4 oncology specialist roles,
                   2 rounds + chair/moderator = 9 calls                   (method under study)
  board_generic  : identical pipeline, 4 identical generic-physician
                   agents (no specialty roles)                            (ablation: are roles doing anything?)

Every method processes a whole batch of items stage by stage so vLLM can batch requests.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .backends import Backend, Request
from .data import Item
from .parse import extract_answer, majority_vote

ANSWER_INSTRUCTION = (
    "Reason through the case step by step, concisely (no more than about 150 words). "
    "Then give your final choice on the last line in exactly this format: Answer: <letter>"
)

GENERIC_SYSTEM = "You are an experienced physician answering a medical examination question."

ROLE_SYSTEMS = {
    "medical_oncologist": "You are a medical oncologist sitting on a multidisciplinary tumor board. "
                          "Bring the perspective of systemic therapy, cancer biology and medical management.",
    "surgical_oncologist": "You are a surgical oncologist sitting on a multidisciplinary tumor board. "
                           "Bring the perspective of surgical anatomy, resectability, operative and perioperative care.",
    "radiation_oncologist": "You are a radiation oncologist sitting on a multidisciplinary tumor board. "
                            "Bring the perspective of radiotherapy, radiobiology, imaging and treatment toxicity.",
    "pathologist": "You are a pathologist sitting on a multidisciplinary tumor board. "
                   "Bring the perspective of histopathology, molecular markers, laboratory findings and pathophysiology.",
}

CHAIR_SYSTEM = ("You chair a multidisciplinary tumor board. You have read each member's assessment. "
                "Weigh the arguments on their merits (not by headcount alone) and decide the single best answer.")


@dataclass
class GenConfig:
    temperature: float = 0.7
    top_p: float = 0.95
    max_tokens: int = 512
    chair_max_tokens: int = 384


def derive_seed(base_seed: int, item_id: str, tag: str) -> int:
    h = hashlib.sha256(f"{base_seed}|{item_id}|{tag}".encode()).hexdigest()
    return int(h[:8], 16)


def format_question(item: Item) -> str:
    opts = "\n".join(f"{k}. {item.options[k]}" for k in item.letters)
    return f"Question:\n{item.question}\n\nOptions:\n{opts}"


def _user(item: Item) -> str:
    return f"{format_question(item)}\n\n{ANSWER_INSTRUCTION}"


def _tok(c) -> dict:
    return {"prompt_tokens": c.prompt_tokens, "completion_tokens": c.completion_tokens,
            "finish_reason": getattr(c, "finish_reason", None)}


def _sum_tokens(entries: list[dict]) -> dict:
    return {"prompt_tokens": sum(e["prompt_tokens"] for e in entries),
            "completion_tokens": sum(e["completion_tokens"] for e in entries),
            "n_truncated": sum(e.get("finish_reason") == "length" for e in entries)}


# ---------------------------------------------------------------- baselines

def run_cot(items: list[Item], backend: Backend, cfg: GenConfig, seed: int) -> list[dict]:
    reqs = [Request([{"role": "system", "content": GENERIC_SYSTEM}, {"role": "user", "content": _user(it)}],
                    n=1, temperature=0.0, top_p=1.0, max_tokens=cfg.max_tokens,
                    seed=derive_seed(seed, it.item_id, "cot")) for it in items]
    outs = backend.generate(reqs)
    recs = []
    for it, comps in zip(items, outs):
        c = comps[0]
        ans = extract_answer(c.text, it.letters)
        recs.append({"item_id": it.item_id, "gold": it.answer_idx, "method": "cot", "calls": 1,
                     "final": ans, "samples": [{"text": c.text, "answer": ans, **_tok(c)}],
                     **_tok(c)})
    return recs


def run_sc(items: list[Item], backend: Backend, cfg: GenConfig, seed: int, k_max: int = 15) -> list[dict]:
    reqs = [Request([{"role": "system", "content": GENERIC_SYSTEM}, {"role": "user", "content": _user(it)}],
                    n=k_max, temperature=cfg.temperature, top_p=cfg.top_p, max_tokens=cfg.max_tokens,
                    seed=derive_seed(seed, it.item_id, "sc")) for it in items]
    outs = backend.generate(reqs)
    recs = []
    for it, comps in zip(items, outs):
        samples = [{"text": c.text, "answer": extract_answer(c.text, it.letters), **_tok(c)} for c in comps]
        # Token accounting is "API-equivalent": each sample is billed its own copy of the prompt,
        # as if issued as k separate calls. vLLM actually shares the prefix, so wall-clock cost
        # of SC is lower than this; we report wall-clock separately so the reader sees both.
        recs.append({"item_id": it.item_id, "gold": it.answer_idx, "method": "sc", "calls": k_max,
                     "k_max": k_max, "final": majority_vote([s["answer"] for s in samples[:9]]),
                     "samples": samples, **_sum_tokens(samples)})
    return recs


# ---------------------------------------------------------------- tumor board

def run_board(items: list[Item], backend: Backend, cfg: GenConfig, seed: int,
              roles: dict[str, str], method_name: str, rounds: int = 2) -> list[dict]:
    role_names = list(roles)
    state = {it.item_id: {"rounds": []} for it in items}

    # Round 1: independent assessments
    r1_reqs, keys = [], []
    for it in items:
        for rn in role_names:
            r1_reqs.append(Request([{"role": "system", "content": roles[rn]},
                                    {"role": "user", "content": _user(it)}],
                                   n=1, temperature=cfg.temperature, top_p=cfg.top_p,
                                   max_tokens=cfg.max_tokens, seed=derive_seed(seed, it.item_id, f"r1|{rn}")))
            keys.append((it, rn))
    outs = backend.generate(r1_reqs)
    for it in items:
        state[it.item_id]["rounds"].append({})
    for (it, rn), comps in zip(keys, outs):
        c = comps[0]
        state[it.item_id]["rounds"][0][rn] = {"text": c.text, "answer": extract_answer(c.text, it.letters), **_tok(c)}

    # Rounds 2..R: each member sees the others' latest assessments and may revise
    for r in range(1, rounds):
        reqs, keys = [], []
        for it in items:
            prev = state[it.item_id]["rounds"][r - 1]
            for rn in role_names:
                others = "\n\n".join(f"[{o.replace('_', ' ').title()}]\n{prev[o]['text'].strip()}"
                                     for o in role_names if o != rn)
                msgs = [{"role": "system", "content": roles[rn]},
                        {"role": "user", "content": _user(it)},
                        {"role": "assistant", "content": prev[rn]["text"]},
                        {"role": "user", "content": "The other board members gave these assessments:\n\n"
                                                    f"{others}\n\nReconsider the case in light of their views. "
                                                    "Keep your answer if you still think it is right, or change it. "
                                                    + ANSWER_INSTRUCTION}]
                reqs.append(Request(msgs, n=1, temperature=cfg.temperature, top_p=cfg.top_p,
                                    max_tokens=cfg.max_tokens, seed=derive_seed(seed, it.item_id, f"r{r+1}|{rn}")))
                keys.append((it, rn))
        outs = backend.generate(reqs)
        for it in items:
            state[it.item_id]["rounds"].append({})
        for (it, rn), comps in zip(keys, outs):
            c = comps[0]
            state[it.item_id]["rounds"][r][rn] = {"text": c.text, "answer": extract_answer(c.text, it.letters), **_tok(c)}

    # Chair decision (greedy)
    reqs = []
    for it in items:
        last = state[it.item_id]["rounds"][-1]
        board = "\n\n".join(f"[{rn.replace('_', ' ').title()}]\n{last[rn]['text'].strip()}" for rn in role_names)
        msgs = [{"role": "system", "content": CHAIR_SYSTEM},
                {"role": "user", "content": f"{format_question(it)}\n\nBoard assessments (final round):\n\n{board}\n\n"
                                            + ANSWER_INSTRUCTION}]
        reqs.append(Request(msgs, n=1, temperature=0.0, top_p=1.0, max_tokens=cfg.chair_max_tokens,
                            seed=derive_seed(seed, it.item_id, "chair")))
    outs = backend.generate(reqs)

    recs = []
    for it, comps in zip(items, outs):
        c = comps[0]
        st = state[it.item_id]
        chair = {"text": c.text, "answer": extract_answer(c.text, it.letters), **_tok(c)}
        entries = [e for rd in st["rounds"] for e in rd.values()] + [chair]
        recs.append({
            "item_id": it.item_id, "gold": it.answer_idx, "method": method_name,
            "calls": len(entries), "roles": role_names,
            "rounds": st["rounds"], "chair": chair,
            "r1_vote": majority_vote([st["rounds"][0][rn]["answer"] for rn in role_names]),
            "rlast_vote": majority_vote([st["rounds"][-1][rn]["answer"] for rn in role_names]),
            "final": chair["answer"],
            **_sum_tokens(entries),
        })
    return recs


def generic_roles(n: int = 4) -> dict[str, str]:
    return {f"physician_{i+1}": GENERIC_SYSTEM for i in range(n)}


METHODS = {
    "cot": lambda items, be, cfg, seed: run_cot(items, be, cfg, seed),
    "sc": lambda items, be, cfg, seed: run_sc(items, be, cfg, seed, k_max=15),
    "board_roles": lambda items, be, cfg, seed: run_board(items, be, cfg, seed, ROLE_SYSTEMS, "board_roles"),
    "board_generic": lambda items, be, cfg, seed: run_board(items, be, cfg, seed, generic_roles(4), "board_generic"),
}
