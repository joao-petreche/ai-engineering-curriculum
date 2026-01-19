import numpy as np

from mes8_optimization.metrics import diversity, extract_objectives


def test_diversity_nonzero():
    pop = [
        [0.1, 0.2, 0.3],
        [0.2, 0.2, 0.4],
        [0.3, 0.25, 0.35],
    ]
    d = diversity(pop)
    assert d > 0


def test_extract_objectives():
    class Ind:
        def __init__(self, vals):
            self.fitness = type("fit", (), {"values": vals})

    pop = [Ind((1, 2, 3)), Ind((2, 3, 4))]
    arr = extract_objectives(pop)
    assert arr.shape == (2, 3)
    assert np.allclose(arr[0], [1, 2, 3])
