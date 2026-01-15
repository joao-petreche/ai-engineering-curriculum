from __future__ import annotations

import csv
from pathlib import Path
from typing import Callable, Dict, Optional, Tuple

import numpy as np

from .metrics import diversity, extract_objectives
from .pareto import pareto_front, hypervolume_2d


def build_generation_logger(
    out_csv: str = "runs/ga_metrics.csv",
    ref_point: Optional[Tuple[float, float]] = None,
    every: int = 1,
) -> Callable[[int, list, int], None]:
    """Create a hook to log diversity and optional hypervolume per generation.

    Notes:
        - Hypervolume computed only when 2 objectives are present and ref_point provided.
        - CSV columns: gen,island,diversity,hypervolume
    """

    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)

    def hook(gen: int, pop, island: int = 0):
        if gen % every != 0:
            return
        objs = extract_objectives(pop)
        div = diversity(pop)
        hv = None
        if ref_point is not None and objs.shape[1] == 2:
            front = objs[pareto_front(objs)]
            hv = hypervolume_2d(front, ref_point)
        with open(out_csv, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([gen, island, div, hv])

    return hook
