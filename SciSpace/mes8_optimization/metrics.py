from __future__ import annotations

from typing import List, Sequence
import numpy as np


def extract_objectives(pop: Sequence) -> np.ndarray:
    """Return array (n, m) of objective values from DEAP individuals."""
    return np.array([ind.fitness.values for ind in pop], dtype=float)


def diversity(pop: Sequence) -> float:
    """Mean per-gene stddev as a simple diversity metric."""
    if len(pop) == 0:
        return 0.0
    arr = np.array(pop, dtype=float)
    return float(np.mean(np.std(arr, axis=0)))


def hypervolume_progress(fronts: List[np.ndarray], ref: np.ndarray) -> List[float]:
    """Compute hypervolume for each front (2D only for simplicity)."""
    from .pareto import hypervolume_2d

    hv = []
    for front in fronts:
        hv.append(hypervolume_2d(front, tuple(ref)))
    return hv
