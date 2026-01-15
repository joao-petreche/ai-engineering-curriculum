from __future__ import annotations

import pandas as pd
import plotly.express as px


def plot_pareto_3d(df: pd.DataFrame, path: str = "pareto_frontier.html") -> None:
    """Render Pareto frontier (energy, cost, comfort_gap) to HTML."""
    fig = px.scatter_3d(
        df,
        x="energy",
        y="cost",
        z="comfort_gap",
        color="solution_id" if "solution_id" in df.columns else None,
        hover_data=df.columns,
    )
    fig.update_layout(title="Pareto Frontier: Energy vs Cost vs Comfort")
    fig.write_html(path)
    print(f"saved {path}")
