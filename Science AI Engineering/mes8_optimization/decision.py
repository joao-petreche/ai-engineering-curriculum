from __future__ import annotations

from typing import List, Tuple
import numpy as np


def choose_compromise(front: List[Tuple[float, float, float]], weights: Tuple[float, float, float]):
    """Pick solution with minimum weighted normalized distance (all minimized)."""
    w = np.array(weights, dtype=float)
    w = w / (w.sum() + 1e-9)
    objs = np.array(front, dtype=float)
    norm = (objs - objs.min(axis=0)) / (objs.ptp(axis=0) + 1e-9)
    scores = (norm * w).sum(axis=1)
    idx = int(scores.argmin())
    return idx, objs[idx].tolist(), float(scores[idx])
