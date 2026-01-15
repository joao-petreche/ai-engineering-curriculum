from __future__ import annotations

from pathlib import Path
from typing import Sequence
import pandas as pd

from .metrics import extract_objectives
from .pareto import pareto_front


def save_frontier_csv(pop: Sequence, out_csv: str) -> None:
    """Extract Pareto frontier from a DEAP population and save to CSV.

    Columns: energy,cost,comfort_gap,solution_id
    """
    objs = extract_objectives(pop)
    front_idx = pareto_front(objs)
    front = objs[front_idx]
    df = pd.DataFrame(front, columns=["energy", "cost", "comfort_gap"])
    df["solution_id"] = range(len(df))
    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)
    print(f"✅ Saved frontier CSV to {out_csv} ({len(df)} solutions)")
