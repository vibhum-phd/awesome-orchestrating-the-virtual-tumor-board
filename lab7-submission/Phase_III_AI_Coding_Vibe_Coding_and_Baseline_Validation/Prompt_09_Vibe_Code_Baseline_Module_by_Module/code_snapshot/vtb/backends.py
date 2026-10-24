"""LLM backends with one interface: generate(list[Request]) -> list[list[Completion]].

- VLLMBackend : real runs (Kaggle T4 / Colab GPU). Requires `vllm`.
- HFBackend   : slow fallback using `transformers` (debugging / tiny models).
- MockBackend : deterministic fake model for unit tests ONLY. Its outputs are synthetic
                and must never be reported as results.
"""
from __future__ import annotations

import hashlib
import random
import re
from dataclasses import dataclass


@dataclass
class Request:
    messages: list[dict]
    n: int = 1
    temperature: float = 0.0
    top_p: float = 1.0
    max_tokens: int = 512
    seed: int = 0


@dataclass
class Completion:
    text: str
    prompt_tokens: int
    completion_tokens: int


class Backend:
    name = "base"

    def generate(self, requests: list[Request]) -> list[list[Completion]]:
        raise NotImplementedError

    def info(self) -> dict:
        return {"backend": self.name}


class VLLMBackend(Backend):
    name = "vllm"

    def __init__(self, model: str, dtype: str = "half", max_model_len: int = 6144,
                 tensor_parallel_size: int = 1, gpu_memory_utilization: float = 0.90,
                 quantization: str | None = None):
        from vllm import LLM  # imported lazily so tests run without vllm
        self.model = model
        kwargs = dict(model=model, dtype=dtype, max_model_len=max_model_len,
                      tensor_parallel_size=tensor_parallel_size,
                      gpu_memory_utilization=gpu_memory_utilization, seed=0)
        if quantization:
            kwargs["quantization"] = quantization
        self.llm = LLM(**kwargs)
        self.tok = self.llm.get_tokenizer()
        self._kwargs = kwargs

    def generate(self, requests):
        from vllm import SamplingParams
        prompts = [self.tok.apply_chat_template(r.messages, tokenize=False, add_generation_prompt=True)
                   for r in requests]
        params = [SamplingParams(n=r.n, temperature=r.temperature, top_p=r.top_p,
                                 max_tokens=r.max_tokens, seed=r.seed) for r in requests]
        outs = self.llm.generate(prompts, params, use_tqdm=False)
        result = []
        for o in outs:
            pt = len(o.prompt_token_ids)
            result.append([Completion(c.text, pt, len(c.token_ids)) for c in o.outputs])
        return result

    def info(self):
        import vllm
        return {"backend": self.name, "model": self.model, "vllm_version": vllm.__version__,
                **{k: v for k, v in self._kwargs.items() if k != "model"}}


class HFBackend(Backend):
    name = "hf"

    def __init__(self, model: str, dtype: str = "float16", device: str = "cuda"):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.torch = torch
        self.model_name = model
        self.tok = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForCausalLM.from_pretrained(model, torch_dtype=getattr(torch, dtype)).to(device)
        self.device = device

    def generate(self, requests):
        result = []
        for r in requests:
            prompt = self.tok.apply_chat_template(r.messages, tokenize=False, add_generation_prompt=True)
            enc = self.tok(prompt, return_tensors="pt").to(self.device)
            self.torch.manual_seed(r.seed)
            sample = r.temperature > 0
            out = self.model.generate(**enc, max_new_tokens=r.max_tokens, do_sample=sample,
                                      temperature=r.temperature if sample else None,
                                      top_p=r.top_p if sample else None,
                                      num_return_sequences=r.n, pad_token_id=self.tok.eos_token_id)
            pt = enc["input_ids"].shape[1]
            comps = []
            for seq in out:
                gen = seq[pt:]
                comps.append(Completion(self.tok.decode(gen, skip_special_tokens=True), pt, int(len(gen))))
            result.append(comps)
        return result

    def info(self):
        import transformers
        return {"backend": self.name, "model": self.model_name, "transformers_version": transformers.__version__}


class MockBackend(Backend):
    """Fake model for testing plumbing. Answers correctly with prob `p_correct`
    (needs `oracle`: question text -> gold letter). In discussion rounds it adopts the
    majority answer shown with prob `p_conform`, so flip-analysis code has something
    to count. SYNTHETIC — never report its numbers."""
    name = "mock"

    def __init__(self, oracle: dict[str, str], letters: str = "ABCDE",
                 p_correct: float = 0.6, p_conform: float = 0.5):
        self.oracle, self.letters = oracle, letters
        self.p_correct, self.p_conform = p_correct, p_conform

    def _gold_for(self, text: str) -> str | None:
        for q, g in self.oracle.items():
            if q[:80] in text:
                return g
        return None

    def generate(self, requests):
        result = []
        for r in requests:
            text = "\n".join(m["content"] for m in r.messages)
            gold = self._gold_for(text)
            shown = re.findall(r"Answer: ([A-E])", text)
            comps = []
            for i in range(r.n):
                h = hashlib.sha256(f"{r.seed}|{i}|{text}".encode()).hexdigest()
                rng = random.Random(int(h[:12], 16))
                if r.temperature == 0:
                    rng = random.Random(int(hashlib.sha256(text.encode()).hexdigest()[:12], 16))
                if shown and rng.random() < self.p_conform:
                    ans = max(set(shown), key=shown.count)
                elif gold and rng.random() < self.p_correct:
                    ans = gold
                else:
                    ans = rng.choice(self.letters)
                body = f"Mock reasoning {h[:6]}.\nAnswer: {ans}" if rng.random() > 0.03 else "I am not sure."
                comps.append(Completion(body, len(text) // 4, len(body) // 4))
            result.append(comps)
        return result
