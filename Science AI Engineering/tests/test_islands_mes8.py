from mes8_optimization.island_runner import run_islands, aggregate_frontier


def eval_dummy(params):
    return params["wwr"] * 10, params["wall_thickness_m"] * 1000, params["insulation_thickness_m"] * 100


BOUNDS = {
    "wwr": (0.1, 0.6),
    "wall_thickness_m": (0.15, 0.3),
    "insulation_thickness_m": (0.05, 0.2),
}


def test_island_runs():
    pops, metrics = run_islands(
        eval_dummy,
        BOUNDS,
        n_islands=2,
        pop_size=12,
        ngen=6,
        migrate_every=3,
        migrants=1,
        generation_hook=lambda gen, pop, island: None,
    )
    assert len(pops) == 2
    assert all(len(p) == 12 for p in pops)
    assert "diversity" in metrics
    assert len(metrics["diversity"][0]) == 6


def test_aggregate_frontier():
    pops, _ = run_islands(eval_dummy, BOUNDS, n_islands=2, pop_size=8, ngen=4, migrate_every=2, migrants=1)
    front = aggregate_frontier(pops)
    assert front.shape[0] >= 1
