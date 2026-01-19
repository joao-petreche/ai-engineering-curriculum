from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple
import numpy as np


def is_dominated(a: np.ndarray, b: np.ndarray) -> bool:
    """Return True if solution a is dominated by b (minimization)."""
    return np.all(b <= a) and np.any(b < a)


def pareto_front(objs: np.ndarray) -> List[int]:
    """Return indices of non-dominated solutions for minimization objectives."""
    n = objs.shape[0]
    dominated = np.zeros(n, dtype=bool)
    for i in range(n):
        if dominated[i]:
            continue
        for j in range(n):
            if i == j or dominated[i]:
                continue
            if is_dominated(objs[i], objs[j]):
                dominated[i] = True
    return [i for i, d in enumerate(dominated) if not d]


def sort_nondominated(objs: np.ndarray) -> List[List[int]]:
    """Fast non-dominated sorting (simplified for small populations)."""
    remaining = set(range(objs.shape[0]))
    fronts: List[List[int]] = []
    while remaining:
        front = pareto_front(objs[list(remaining)])
        mapped_front = [list(remaining)[idx] for idx in front]
        fronts.append(mapped_front)
        for idx in mapped_front:
            remaining.discard(idx)
    return fronts


def hypervolume_2d(front: np.ndarray, ref: Tuple[float, float]) -> float:
    """Simple 2D hypervolume for minimization (assumes front is non-dominated)."""
    front = front[np.argsort(front[:, 0])]
    hv = 0.0
    prev_f1 = ref[0]
    for f1, f2 in front:
        hv += (prev_f1 - f1) * (ref[1] - f2)
        prev_f1 = f1
    return hv


def normalize_objectives(objs: np.ndarray) -> np.ndarray:
    """Normalize objectives to [0,1] for each column."""
    mins = objs.min(axis=0)
    ranges = objs.ptp(axis=0) + 1e-9
    return (objs - mins) / ranges


def choose_reference_point(objs: np.ndarray, margin: float = 0.1) -> np.ndarray:
    """Reference point = worst observed + margin."""
    worst = objs.max(axis=0)
    return worst * (1.0 + margin)
