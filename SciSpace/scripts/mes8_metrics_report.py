"""Generate plots and summary from GA/island metrics CSVs.

Usage:
    python scripts/mes8_metrics_report.py --csv runs/ga_metrics.csv --out reports/mes8_metrics.html

The CSV is expected to have columns: gen,island,diversity,hypervolume
(see mes8_optimization.hooks.build_generation_logger).
"""
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go


def load_metrics(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path, header=None, names=["gen", "island", "diversity", "hypervolume"])
    return df


def plot_metrics(df: pd.DataFrame, out_html: str):
    fig = go.Figure()

    for island, sub in df.groupby("island"):
        fig.add_trace(
            go.Scatter(
                x=sub["gen"],
                y=sub["diversity"],
                mode="lines",
                name=f"Island {island} - diversity",
            )
        )
    if df["hypervolume"].notna().any():
        hv = df.dropna(subset=["hypervolume"])
        fig.add_trace(
            go.Scatter(
                x=hv["gen"],
                y=hv["hypervolume"],
                mode="lines",
                name="Hypervolume (2D)",
                line=dict(color="black", dash="dot"),
            )
        )

    fig.update_layout(
        title="GA/Island Metrics",
        xaxis_title="Generation",
        yaxis_title="Metric Value",
        template="plotly_white",
    )

    Path(out_html).parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(out_html)
    print(f"✅ Saved metrics plot to {out_html}")


def summarize(df: pd.DataFrame):
    last = df.groupby("island").tail(1)
    print("\n=== Summary ===")
    print("Islands:", df["island"].nunique())
    print("Generations logged:", df["gen"].max() + 1)
    print("Final diversity per island:")
    print(last[["island", "diversity"]])
    if df["hypervolume"].notna().any():
        hv_last = df.dropna(subset=["hypervolume"]).groupby("island").tail(1)
        print("Final hypervolume per island:")
        print(hv_last[["island", "hypervolume"]])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, help="Path to metrics CSV")
    ap.add_argument("--out", default="reports/mes8_metrics.html", help="Output HTML path")
    args = ap.parse_args()

    df = load_metrics(args.csv)
    plot_metrics(df, args.out)
    summarize(df)


if __name__ == "__main__":
    main()
