"""Run one (dataset, method, seed) cell of the frozen protocol and append JSONL records.

Resumable: items already present in the output file are skipped.

Example (Kaggle, 2x T4):
  python scripts/run_experiment.py --config configs/frozen_protocol.yaml \
      --dataset medqa_onc --method board_roles --seed 0 --backend vllm
Example (unit-test plumbing, CPU, synthetic outputs only):
  python scripts/run_experiment.py --config configs/frozen_protocol.yaml \
      --dataset medqa_onc --method cot --seed 0 --backend mock --out results/mock
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import platform
import sys
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from vtb.backends import HFBackend, MockBackend, VLLMBackend  # noqa: E402
from vtb.data import load_processed  # noqa: E402
from vtb.methods import METHODS, GenConfig  # noqa: E402


def build_backend(kind: str, cfg: dict, items):
    m = cfg["model"]
    if kind == "vllm":
        return VLLMBackend(m["name"], dtype=m.get("dtype", "half"), max_model_len=m.get("max_model_len", 6144),
                           tensor_parallel_size=m.get("tensor_parallel_size", 1),
                           gpu_memory_utilization=m.get("gpu_memory_utilization", 0.9),
                           quantization=m.get("quantization"))
    if kind == "hf":
        return HFBackend(m["name"])
    if kind == "mock":
        return MockBackend({it.question: it.answer_idx for it in items})
    raise ValueError(kind)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(ROOT / "configs/frozen_protocol.yaml"))
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--method", required=True, choices=list(METHODS))
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--backend", default="vllm", choices=["vllm", "hf", "mock"])
    ap.add_argument("--model", default=None, help="override model name from config")
    ap.add_argument("--limit", type=int, default=None, help="first N items only (pilot)")
    ap.add_argument("--chunk", type=int, default=32, help="items per batch; progress saved after each")
    ap.add_argument("--out", default=str(ROOT / "results/raw"))
    args = ap.parse_args()

    cfg = yaml.safe_load(open(args.config))
    if args.model:
        cfg["model"]["name"] = args.model
    ds_path = ROOT / cfg["datasets"][args.dataset]
    items = load_processed(ds_path)
    if args.limit:
        items = items[: args.limit]

    model_tag = cfg["model"]["name"].split("/")[-1] if args.backend != "mock" else "mock"
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{args.dataset}__{args.method}__{model_tag}__seed{args.seed}.jsonl"
    done = set()
    if out_file.exists():
        done = {json.loads(l)["item_id"] for l in open(out_file) if l.strip()}
    todo = [it for it in items if it.item_id not in done]
    print(f"[run] {out_file.name}: {len(done)} done, {len(todo)} to go", flush=True)

    backend = build_backend(args.backend, cfg, items)
    g = cfg["generation"]
    gen = GenConfig(temperature=g["temperature"], top_p=g["top_p"], max_tokens=g["max_tokens"],
                    chair_max_tokens=g["chair_max_tokens"])
    fn = METHODS[args.method]

    t_start = time.time()
    with open(out_file, "a", encoding="utf-8") as f:
        for i in range(0, len(todo), args.chunk):
            chunk = todo[i: i + args.chunk]
            t0 = time.time()
            recs = fn(chunk, backend, gen, args.seed)
            dt_chunk = time.time() - t0
            for r in recs:
                r.update({"dataset": args.dataset, "seed": args.seed, "model": model_tag,
                          "protocol_version": cfg["protocol_version"],
                          "wall_seconds_chunk_share": dt_chunk / len(chunk)})
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
            f.flush()
            print(f"[run] {i + len(chunk)}/{len(todo)} items, chunk {dt_chunk:.1f}s", flush=True)

    meta = {"out_file": out_file.name, "argv": sys.argv, "finished_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "items_run_this_call": len(todo), "wall_seconds": time.time() - t_start,
            "python": platform.python_version(), "platform": platform.platform(),
            "backend": backend.info(), "generation": g}
    try:
        import torch
        meta["gpu"] = [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())]
    except Exception:  # torch absent in CPU test env
        meta["gpu"] = []
    with open(out_dir / "run_meta.jsonl", "a") as f:
        f.write(json.dumps(meta) + "\n")


if __name__ == "__main__":
    main()
