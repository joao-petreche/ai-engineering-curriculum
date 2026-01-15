"""Generate a full Mês 8 report: Pareto HTML + metrics plots + trade-off CSV.

Usage:
    python scripts/mes8_generate_report.py \
        --frontier_csv runs/frontier.csv \
        --metrics_csv runs/islands_metrics.csv \
        --out_dir reports/mes8

Expected inputs:
- frontier_csv: CSV with columns energy,cost,comfort_gap,(optional)solution_id
- metrics_csv: from build_generation_logger (gen,island,diversity,hypervolume)
"""
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_frontier(frontier_csv: str, out_html: str):
    df = pd.read_csv(frontier_csv)
    fig = px.scatter_3d(
        df,
        x="energy",
        y="cost",
        z="comfort_gap",
        color="solution_id" if "solution_id" in df.columns else None,
        hover_data=df.columns,
        title="Pareto Frontier (Energy vs Cost vs Comfort)",
    )
    Path(out_html).parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(out_html)
    print(f"✅ Saved Pareto frontier to {out_html}")


def plot_metrics(metrics_csv: str, out_html: str):
    df = pd.read_csv(metrics_csv, header=None, names=["gen", "island", "diversity", "hypervolume"])
    fig = go.Figure()
    for island, sub in df.groupby("island"):
        fig.add_trace(
            go.Scatter(x=sub["gen"], y=sub["diversity"], mode="lines", name=f"Island {island} - diversity")
        )
    hv = df.dropna(subset=["hypervolume"])
    if not hv.empty:
        fig.add_trace(
            go.Scatter(x=hv["gen"], y=hv["hypervolume"], mode="lines", name="Hypervolume (2D)", line=dict(dash="dot"))
        )
    fig.update_layout(title="GA/Island Metrics", xaxis_title="Generation", yaxis_title="Value", template="plotly_white")
    Path(out_html).parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(out_html)
    print(f"✅ Saved metrics plot to {out_html}")


def tradeoff_table(frontier_csv: str, out_csv: str):
    df = pd.read_csv(frontier_csv)
    summary = df.describe()[["energy", "cost", "comfort_gap"]]
    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(out_csv)
    print(f"✅ Saved trade-off summary to {out_csv}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frontier_csv", required=True, help="Pareto frontier CSV")
    ap.add_argument("--metrics_csv", required=True, help="Metrics CSV from logger")
    ap.add_argument("--out_dir", default="reports/mes8", help="Output directory")
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    plot_frontier(args.frontier_csv, str(out_dir / "pareto_frontier.html"))
    plot_metrics(args.metrics_csv, str(out_dir / "metrics.html"))
    tradeoff_table(args.frontier_csv, str(out_dir / "tradeoff_summary.csv"))


if __name__ == "__main__":
    main()
