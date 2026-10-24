"""Environment test (Prompt 08). Prints facts about the machine it runs on; claims nothing.

Usage:  python scripts/env_check.py [--require-gpu] [--json out.json]

Expected output type: a JSON object (also printed) with keys
  python, platform, cpu_count, ram_gb, disk_free_gb, packages{name: version|null},
  cuda{available, torch_cuda, devices[], capabilities[]}, vllm_import, data{medqa_sha256_ok, n_all, n_onc},
  seed_check{numpy_repeatable}, network{huggingface, github}, problems[]
Exit code 0 if no blocking problem, 1 otherwise. A problem is "blocking" only if --require-gpu is
given and no CUDA GPU with compute capability >= 7.0 is visible, or the MedQA hash does not match.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata as md
import json
import os
import platform
import shutil
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_MEDQA_SHA256 = "cfa75cbcc53c29b023752b0a395ff49d8202121041392735ae44771a5ec734a3"
PACKAGES = ["numpy", "pandas", "scipy", "matplotlib", "PyYAML", "pytest", "torch", "transformers",
            "vllm", "datasets", "huggingface-hub"]


def version(pkg: str) -> str | None:
    try:
        return md.version(pkg)
    except md.PackageNotFoundError:
        return None


def ram_gb() -> float | None:
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemTotal"):
                    return round(int(line.split()[1]) / 1024 / 1024, 1)
    except OSError:
        return None
    return None


def reachable(url: str, timeout: int = 8) -> bool:
    """True if the host answered at all. An HTTP error status (e.g. GitHub's 400 to HEAD /)
    still proves the network path works; only connection/TLS/proxy failures count as unreachable.
    (Bug found 2026-10-24: the first version treated HTTP 400 as 'unreachable'.)"""
    import urllib.error
    try:
        urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=timeout)
        return True
    except urllib.error.HTTPError:
        return True
    except Exception:
        return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--require-gpu", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()
    out: dict = {"python": sys.version.split()[0], "platform": platform.platform(),
                 "cpu_count": os.cpu_count(), "ram_gb": ram_gb(),
                 "disk_free_gb": round(shutil.disk_usage(ROOT).free / 1e9, 1),
                 "packages": {p: version(p) for p in PACKAGES}, "problems": []}

    cuda = {"available": False, "torch_cuda": None, "devices": [], "capabilities": []}
    try:
        import torch
        cuda["available"] = torch.cuda.is_available()
        cuda["torch_cuda"] = torch.version.cuda
        for i in range(torch.cuda.device_count()):
            cuda["devices"].append(torch.cuda.get_device_name(i))
            cuda["capabilities"].append(".".join(map(str, torch.cuda.get_device_capability(i))))
    except ImportError:
        out["problems"].append("torch not installed (fine for CPU analysis, required for GPU runs)")
    out["cuda"] = cuda
    if args.require_gpu:
        ok = cuda["available"] and any(float(c) >= 7.0 for c in cuda["capabilities"])
        if not ok:
            out["problems"].append("BLOCKING: no CUDA GPU with compute capability >= 7.0 (vLLM requirement)")

    try:
        import vllm  # noqa: F401
        out["vllm_import"] = "ok"
    except Exception as e:  # ImportError or CUDA init errors
        out["vllm_import"] = f"failed: {type(e).__name__}: {str(e)[:160]}"

    raw = ROOT / "data/raw/medqa_test.jsonl"
    data = {"medqa_raw_present": raw.exists()}
    if raw.exists():
        h = hashlib.sha256(raw.read_bytes()).hexdigest()
        data["medqa_sha256_ok"] = h == EXPECTED_MEDQA_SHA256
        if not data["medqa_sha256_ok"]:
            out["problems"].append(f"BLOCKING: MedQA sha256 mismatch ({h[:12]}…)")
    for name, rel in [("n_all", "data/processed/medqa_test_all.jsonl"), ("n_onc", "data/processed/medqa_test_onc.jsonl")]:
        p = ROOT / rel
        data[name] = sum(1 for _ in open(p)) if p.exists() else None
    out["data"] = data

    import numpy as np
    a = np.random.default_rng(0).random(5)
    b = np.random.default_rng(0).random(5)
    out["seed_check"] = {"numpy_repeatable": bool((a == b).all())}

    out["network"] = {"huggingface": reachable("https://huggingface.co"), "github": reachable("https://github.com")}
    if not out["network"]["huggingface"]:
        out["problems"].append("Hugging Face not reachable: model download and MedMCQA build will fail here")

    text = json.dumps(out, indent=2)
    print(text)
    if args.json:
        Path(args.json).write_text(text)
    return 1 if any(p.startswith("BLOCKING") for p in out["problems"]) else 0


if __name__ == "__main__":
    sys.exit(main())
