import numpy as np

from mes8_optimization.pareto import pareto_front, hypervolume_2d
from mes8_optimization.decision import choose_compromise


def test_pareto_front_simple():
    objs = np.array(
        [
            [10, 2000, 0.2],
            [9, 2200, 0.3],
            [11, 1800, 0.25],
            [8, 2500, 0.35],
        ]
    )
    front_idx = pareto_front(objs)
    assert set(front_idx) == {0, 2}


def test_hypervolume_increases():
    ref = (12, 3000)
    front_a = np.array([[10, 2000], [11, 2200]])
    front_b = np.array([[9, 1900], [10, 2000]])
    assert hypervolume_2d(front_b, ref) > hypervolume_2d(front_a, ref)


def test_choose_compromise():
    front = [(10, 2000, 0.2), (9, 2200, 0.3), (11, 1800, 0.25)]
    idx, sol, score = choose_compromise(front, (0.4, 0.4, 0.2))
    assert idx in {0, 2}
    assert len(sol) == 3
    assert score >= 0.0
