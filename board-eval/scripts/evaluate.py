"""Evaluate raw JSONL runs -> traceable CSVs + figures. Uses ONLY records produced by
run_experiment.py; it never fills in missing values.

  python scripts/evaluate.py --raw results/raw --out results --data-root .

Writes:
  results/integrity_report.json   alignment / coverage / parse checks (read this first)
  results/results.csv             accuracy, 95% CI, parse-fail rate, calls, tokens per variant
  results/comparisons.csv         pre-specified paired tests (exact McNemar, paired bootstrap, Holm)
  results/flips.csv               R1->R2 answer transitions per board method
  results/chair.csv               chair vs final-round majority
  results/stratified.csv          accuracy by round-1 board agreement
  results/figures/*.png|pdf       efficiency frontier, flips, stratified accuracy
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from vtb.data import load_processed  # noqa: E402
from vtb.parse import agreement, majority_vote  # noqa: E402
from vtb.stats import bootstrap_ci, holm, mcnemar_exact, paired_bootstrap_diff  # noqa: E402

import yaml  # noqa: E402

COLORS = {"cot": "#2a78d6", "sc": "#eb6834", "board_roles": "#1baf7a", "board_generic": "#eda100"}
MARKERS = {"cot": "o", "sc": "s", "board_roles": "D", "board_generic": "^"}
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"


def load_raw(raw_dir: Path) -> pd.DataFrame:
    rows = []
    for fp in sorted(raw_dir.glob("*.jsonl")):
        if fp.name == "run_meta.jsonl":
            continue
        for line in open(fp, encoding="utf-8"):
            if line.strip():
                r = json.loads(line)
                r["_file"] = fp.name
                rows.append(r)
    if not rows:
        raise SystemExit(f"no raw records in {raw_dir}")
    return pd.DataFrame(rows)


def integrity(df: pd.DataFrame, cfg: dict, data_root: Path) -> dict:
    rep = {"files": sorted(df["_file"].unique().tolist()), "checks": [], "ok": True}

    def fail(msg):
        rep["checks"].append("FAIL: " + msg)
        rep["ok"] = False

    golds = {}
    for ds in df["dataset"].unique():
        path = data_root / cfg["datasets"][ds]
        golds[ds] = {it.item_id: it.answer_idx for it in load_processed(path)}
    for (ds, m, seed, model), g in df.groupby(["dataset", "method", "seed", "model"]):
        tag = f"{ds}/{m}/seed{seed}/{model}"
        dup = g["item_id"].duplicated().sum()
        if dup:
            fail(f"{tag}: {dup} duplicate item_ids")
        unknown = set(g["item_id"]) - set(golds[ds])
        if unknown:
            fail(f"{tag}: {len(unknown)} item_ids not in dataset file")
        mism = sum(golds[ds].get(i) != gold for i, gold in zip(g["item_id"], g["gold"]))
        if mism:
            fail(f"{tag}: {mism} gold labels disagree with dataset file")
        cov = len(set(g["item_id"]) & set(golds[ds])) / len(golds[ds])
        rep["checks"].append(f"{tag}: n={len(g)} coverage={cov:.3f} parse_fail={g['final'].isna().mean():.3f}")
        if g["protocol_version"].nunique() > 1:
            fail(f"{tag}: mixed protocol versions {g['protocol_version'].unique().tolist()}")
    return rep


def variant_table(df: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """One row per (dataset, model, seed, item, variant) with correctness, calls, tokens."""
    ks = cfg["analysis"]["sc_curve_k"]
    out = []
    for r in df.itertuples(index=False):
        base = {"dataset": r.dataset, "model": r.model, "seed": r.seed, "item_id": r.item_id, "gold": r.gold}
        if r.method == "cot":
            s = r.samples[0]
            out.append({**base, "variant": "cot", "family": "cot", "pred": r.final, "calls": 1,
                        "tokens": s["prompt_tokens"] + s["completion_tokens"]})
        elif r.method == "sc":
            for k in ks:
                sub = r.samples[:k]
                out.append({**base, "variant": f"sc@{k}", "family": "sc",
                            "pred": majority_vote([s["answer"] for s in sub]), "calls": k,
                            "tokens": sum(s["prompt_tokens"] + s["completion_tokens"] for s in sub)})
        else:
            rounds = r.rounds
            n_mem = len(r.roles)
            r1_tok = sum(e["prompt_tokens"] + e["completion_tokens"] for e in rounds[0].values())
            all_rounds_tok = sum(e["prompt_tokens"] + e["completion_tokens"] for rd in rounds for e in rd.values())
            chair_tok = r.chair["prompt_tokens"] + r.chair["completion_tokens"]
            out.append({**base, "variant": f"{r.method}.r1_vote", "family": r.method, "pred": r.r1_vote,
                        "calls": n_mem, "tokens": r1_tok})
            out.append({**base, "variant": f"{r.method}.rlast_vote", "family": r.method, "pred": r.rlast_vote,
                        "calls": n_mem * len(rounds), "tokens": all_rounds_tok})
            out.append({**base, "variant": f"{r.method}.final", "family": r.method, "pred": r.final,
                        "calls": n_mem * len(rounds) + 1, "tokens": all_rounds_tok + chair_tok})
    v = pd.DataFrame(out)
    v["correct"] = (v["pred"] == v["gold"]).astype(int)   # None/NaN pred -> wrong
    v["parse_fail"] = v["pred"].isna().astype(int)
    return v


def summarise(v: pd.DataFrame, cfg: dict, wall: pd.DataFrame) -> pd.DataFrame:
    nb, bs = cfg["analysis"]["bootstrap_resamples"], cfg["analysis"]["bootstrap_seed"]
    rows = []
    for (ds, model, seed, var), g in v.groupby(["dataset", "model", "seed", "variant"]):
        c = g["correct"].to_numpy()
        lo, hi = bootstrap_ci(c, nb, bs)
        rows.append({"dataset": ds, "model": model, "seed": seed, "variant": var, "family": g["family"].iloc[0],
                     "n": len(g), "accuracy": c.mean(), "ci95_lo": lo, "ci95_hi": hi,
                     "parse_fail_rate": g["parse_fail"].mean(), "calls_per_item": g["calls"].mean(),
                     "api_tokens_per_item": g["tokens"].mean()})
    res = pd.DataFrame(rows)
    res = res.merge(wall, how="left", on=["dataset", "model", "seed", "family"])
    return res.sort_values(["dataset", "model", "seed", "family", "calls_per_item"])


def pooled(v: pd.DataFrame, datasets: list[str]) -> pd.DataFrame:
    p = v[v["dataset"].isin(datasets)].copy()
    p["dataset"] = "+".join(datasets)
    return p


def compare(v: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    nb, bs = cfg["analysis"]["bootstrap_resamples"], cfg["analysis"]["bootstrap_seed"]
    pairs = [("board_roles.final", "sc@9", "PRIMARY"),
             ("board_roles.final", "cot", "secondary"),
             ("board_roles.final", "board_generic.final", "secondary"),
             ("board_roles.final", "board_roles.r1_vote", "secondary"),
             ("board_roles.rlast_vote", "board_roles.r1_vote", "secondary")]
    rows = []
    for (ds, model, seed), g in v.groupby(["dataset", "model", "seed"]):
        piv = g.pivot_table(index="item_id", columns="variant", values="correct", aggfunc="first")
        fam_rows = []
        for a, b, role in pairs:
            if a not in piv or b not in piv:
                continue
            both = piv[[a, b]].dropna()
            x, y = both[a].to_numpy(), both[b].to_numpy()
            mc = mcnemar_exact(x, y)
            lo, hi = paired_bootstrap_diff(x, y, nb, bs)
            fam_rows.append({"dataset": ds, "model": model, "seed": seed, "role": role, "a": a, "b": b,
                             "n_paired": len(both), "acc_a": x.mean(), "acc_b": y.mean(),
                             "diff_pp": 100 * (x.mean() - y.mean()), "diff_ci95_lo_pp": 100 * lo,
                             "diff_ci95_hi_pp": 100 * hi, **mc})
        sec = [r for r in fam_rows if r["role"] == "secondary"]
        if sec:
            for r, padj in zip(sec, holm([r["p_value"] for r in sec])):
                r["p_holm"] = padj
        for r in fam_rows:
            r.setdefault("p_holm", r["p_value"])
            thr = cfg["analysis"]["practical_threshold_pp"]
            r["decision"] = ("supported: a > b" if r["p_holm"] < 0.05 and r["diff_pp"] >= thr else
                             "supported: b > a" if r["p_holm"] < 0.05 and r["diff_pp"] <= -thr else
                             "no meaningful difference detected")
        rows += fam_rows
    return pd.DataFrame(rows)


def flips_and_chair(df: pd.DataFrame):
    flips, chair, strat = [], [], defaultdict(list)
    boards = df[df["method"].isin(["board_roles", "board_generic"])]
    for r in boards.itertuples(index=False):
        r1, rl = r.rounds[0], r.rounds[-1]
        for role in r.roles:
            a1, a2 = r1[role]["answer"], rl[role]["answer"]
            t = ("C" if a1 == r.gold else "W") + "->" + ("C" if a2 == r.gold else "W")
            flips.append({"dataset": r.dataset, "model": r.model, "seed": r.seed, "method": r.method,
                          "role": role, "transition": t, "changed": int(a1 != a2)})
        maj = r.rlast_vote
        chair.append({"dataset": r.dataset, "model": r.model, "seed": r.seed, "method": r.method,
                      "chair_vs_majority": "agrees" if r.final == maj else "overrides",
                      "chair_correct": int(r.final == r.gold), "majority_correct": int(maj == r.gold)})
        agr = agreement([r1[role]["answer"] for role in r.roles])
        strat[(r.dataset, r.model, r.seed, r.item_id)].append((r.method, agr))
    f = pd.DataFrame(flips)
    f = (f.groupby(["dataset", "model", "seed", "method", "transition"]).size().rename("count").reset_index()
         if len(f) else f)
    c = pd.DataFrame(chair)
    c = (c.groupby(["dataset", "model", "seed", "method", "chair_vs_majority"])
         .agg(n=("chair_correct", "size"), chair_acc=("chair_correct", "mean"),
              majority_acc=("majority_correct", "mean")).reset_index() if len(c) else c)
    agr_map = {k: dict(vs).get("board_roles") for k, vs in strat.items()}
    return f, c, agr_map


def stratify(v: pd.DataFrame, agr_map: dict) -> pd.DataFrame:
    v = v.copy()
    v["r1_agreement"] = [agr_map.get((d, m, s, i)) for d, m, s, i in
                         zip(v["dataset"], v["model"], v["seed"], v["item_id"])]
    v = v.dropna(subset=["r1_agreement"])
    v["stratum"] = v["r1_agreement"].map(lambda a: "unanimous (4/4)" if a == 1 else
                                         "majority (3/4)" if a >= 0.75 else "split (<=2/4)")
    keep = ["cot", "sc@9", "board_roles.r1_vote", "board_roles.final", "board_generic.final"]
    v = v[v["variant"].isin(keep)]
    return (v.groupby(["dataset", "model", "seed", "stratum", "variant"])
            .agg(n=("correct", "size"), accuracy=("correct", "mean")).reset_index())


def wall_table(df: pd.DataFrame) -> pd.DataFrame:
    w = df.groupby(["dataset", "model", "seed", "method"])["wall_seconds_chunk_share"].mean().reset_index()
    return w.rename(columns={"method": "family", "wall_seconds_chunk_share": "wall_s_per_item_family"})


# ---------------------------------------------------------------- figures

def _style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(INK2)
    ax.tick_params(colors=INK2, labelsize=9)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def _stamp_if_mock(ax, model: str):
    if model == "mock":
        ax.text(0.5, 0.5, "SYNTHETIC — MOCK BACKEND\nnot a result", transform=ax.transAxes, ha="center",
                va="center", fontsize=16, color="#e34948", alpha=0.35, rotation=20, zorder=10)


def fig_frontier(res: pd.DataFrame, out: Path, ds: str, model: str, seed: int):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    r = res[(res.dataset == ds) & (res.model == model) & (res.seed == seed)]
    if r.empty:
        return
    fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=200)
    _style(ax)
    sc = r[r.family == "sc"].sort_values("api_tokens_per_item")
    if len(sc):
        ax.plot(sc.api_tokens_per_item, 100 * sc.accuracy, color=COLORS["sc"], lw=2, marker="s", ms=6, zorder=2)
        for _, p in sc.iterrows():
            ax.annotate(p.variant, (p.api_tokens_per_item, 100 * p.accuracy), textcoords="offset points",
                        xytext=(4, -11), fontsize=7.5, color=INK2)
    for fam in ["cot", "board_roles", "board_generic"]:
        for _, p in r[r.family == fam].iterrows():
            ax.errorbar(p.api_tokens_per_item, 100 * p.accuracy,
                        yerr=[[100 * (p.accuracy - p.ci95_lo)], [100 * (p.ci95_hi - p.accuracy)]],
                        fmt=MARKERS[fam], color=COLORS[fam], ms=7, elinewidth=1, capsize=0,
                        markeredgecolor="white", markeredgewidth=1.5, zorder=3)
            ax.annotate(p.variant.replace("board_", ""), (p.api_tokens_per_item, 100 * p.accuracy),
                        textcoords="offset points", xytext=(5, 4), fontsize=7.5, color=INK)
    ax.set_xscale("log")
    from matplotlib.ticker import FuncFormatter, LogLocator, NullFormatter
    ax.xaxis.set_major_locator(LogLocator(base=10, subs=(1.0, 2.0, 5.0)))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.xaxis.set_minor_formatter(NullFormatter())
    _stamp_if_mock(ax, model)
    ax.set_xlabel("API-equivalent tokens per question (log scale)", color=INK2, fontsize=9)
    ax.set_ylabel("Accuracy (%)", color=INK2, fontsize=9)
    ax.set_title(f"Accuracy vs inference cost — {ds}, {model}, seed {seed}", fontsize=10, color=INK, loc="left")
    from matplotlib.lines import Line2D
    ax.legend(handles=[Line2D([], [], color=COLORS[f], marker=MARKERS[f], lw=2 if f == "sc" else 0, label=lab)
                       for f, lab in [("cot", "CoT (greedy)"), ("sc", "Self-consistency @k"),
                                      ("board_roles", "Tumor board (roles)"),
                                      ("board_generic", "Board (generic agents)")]],
              frameon=False, fontsize=8, loc="lower right")
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(out / f"frontier__{ds}__{model}__seed{seed}.{ext}")
    plt.close(fig)


def fig_flips(flips: pd.DataFrame, out: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    if flips.empty:
        return
    for (ds, model, seed), g in flips.groupby(["dataset", "model", "seed"]):
        fig, ax = plt.subplots(figsize=(6.0, 3.4), dpi=200)
        _style(ax)
        order = ["C->C", "W->C", "C->W", "W->W"]
        meths = [m for m in ["board_roles", "board_generic"] if m in g.method.unique()]
        w = 0.38
        for j, m in enumerate(meths):
            gm = g[g.method == m].set_index("transition")["count"].reindex(order).fillna(0)
            xs = np.arange(len(order)) + (j - (len(meths) - 1) / 2) * (w + 0.02)
            bars = ax.bar(xs, gm.values, width=w, color=COLORS[m], label=m.replace("_", " "))
            for b, val in zip(bars, gm.values):
                ax.annotate(f"{int(val)}", (b.get_x() + b.get_width() / 2, val), textcoords="offset points",
                            xytext=(0, 2), ha="center", fontsize=7.5, color=INK)
        ax.set_xticks(range(len(order)),
                      ["correct→correct", "wrong→correct\n(corrected)", "correct→wrong\n(propagated error)",
                       "wrong→wrong"], fontsize=8)
        _stamp_if_mock(ax, model)
        ax.set_ylabel("Member answers (count)", color=INK2, fontsize=9)
        ax.set_title(f"Round-1 → round-2 answer changes — {ds}, seed {seed}", fontsize=10, color=INK, loc="left")
        ax.legend(frameon=False, fontsize=8)
        fig.tight_layout()
        for ext in ("png", "pdf"):
            fig.savefig(out / f"flips__{ds}__{model}__seed{seed}.{ext}")
        plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=str(ROOT / "results/raw"))
    ap.add_argument("--out", default=str(ROOT / "results"))
    ap.add_argument("--config", default=str(ROOT / "configs/frozen_protocol.yaml"))
    ap.add_argument("--data-root", default=str(ROOT))
    ap.add_argument("--pool", default="medqa_onc,medmcqa_onc", help="datasets pooled for the primary analysis")
    ap.add_argument("--restrict-ids", default=None,
                    help="CSV with item_id,human_label; keep only label==1 (pre-registered sensitivity analysis)")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config))
    out = Path(args.out)
    (out / "figures").mkdir(parents=True, exist_ok=True)

    df = load_raw(Path(args.raw))
    if args.restrict_ids:
        lab = pd.read_csv(args.restrict_ids, dtype={"item_id": str})
        if lab["human_label"].isna().any():
            raise SystemExit("audit sheet has unlabelled rows — finish the human audit first")
        keep = set(lab.loc[lab["human_label"].astype(int) == 1, "item_id"])
        audited = set(lab["item_id"])
        df = df[~df["item_id"].isin(audited) | df["item_id"].isin(keep)]
        print(f"[restrict] kept {len(keep)} of {len(audited)} audited items")
    rep = integrity(df, cfg, Path(args.data_root))
    (out / "integrity_report.json").write_text(json.dumps(rep, indent=2))
    print("\n".join(rep["checks"]))
    if not rep["ok"]:
        raise SystemExit("integrity checks FAILED — fix before interpreting anything")

    v = variant_table(df, cfg)
    pool = [d for d in args.pool.split(",") if d in set(v["dataset"])]
    if len(pool) > 1:
        v = pd.concat([v, pooled(v, pool)], ignore_index=True)
    wall = wall_table(df)
    res = summarise(v, cfg, wall)
    res.to_csv(out / "results.csv", index=False)
    comp = compare(v, cfg)
    comp.to_csv(out / "comparisons.csv", index=False)
    flips, chair, agr = flips_and_chair(df)
    flips.to_csv(out / "flips.csv", index=False)
    chair.to_csv(out / "chair.csv", index=False)
    stratify(v[~v["dataset"].str.contains(r"\+")], agr).to_csv(out / "stratified.csv", index=False)

    for (ds, model, seed), _ in res.groupby(["dataset", "model", "seed"]):
        fig_frontier(res, out / "figures", ds, model, seed)
    fig_flips(flips, out / "figures")
    pd.set_option("display.width", 200)
    print(res[["dataset", "seed", "variant", "n", "accuracy", "ci95_lo", "ci95_hi", "parse_fail_rate",
               "api_tokens_per_item"]].to_string(index=False))
    if len(comp):
        print(comp[["dataset", "seed", "role", "a", "b", "n_paired", "diff_pp", "p_value", "p_holm",
                    "decision"]].to_string(index=False))


if __name__ == "__main__":
    main()
