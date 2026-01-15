"""Minimal demo run for NSGA-II with synthetic evaluation.

Usage:
    python -m mes8_optimization.demo_run
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from mes8_optimization.ga_runner import build_nsga2
from mes8_optimization.pareto import pareto_front, choose_reference_point
from mes8_optimization.metrics import extract_objectives, diversity
from mes8_optimization.visualization import plot_pareto_3d
from mes8_optimization.frontier_export import save_frontier_csv


BOUNDS = {
    "wwr": (0.10, 0.60),
    "wall_thickness_m": (0.15, 0.30),
    "insulation_thickness_m": (0.05, 0.20),
    "infiltration_rate_ACH": (0.3, 2.0),
    "heating_setpoint_C": (20, 24),
    "cooling_setpoint_C": (24, 27),
    "shgc": (0.6, 1.2),
    "lambda_insulation": (0.035, 0.045),
    "internal_loads_W_m2": (5, 20),
    "volume_m3": (500, 5000),
}


def evaluate_stub(params):
    """Synthetic multi-objective function for demo only."""
    energy = 60 + 40 * params["wwr"] + 0.5 * params["internal_loads_W_m2"]
    cost = 1800 + 800 * params["insulation_thickness_m"] + 0.2 * params["volume_m3"] / 10
    comfort_gap = max(0, 22 - params["heating_setpoint_C"]) + max(0, params["cooling_setpoint_C"] - 25)
    return energy, cost, comfort_gap


def main():
    metrics = {"diversity": []}

    def hook(gen, pop):
        metrics["diversity"].append(diversity(pop))
        if gen % 10 == 0:
            print(f"Gen {gen}: diversity={metrics['diversity'][-1]:.4f}")

    pop = build_nsga2(evaluate_stub, BOUNDS, pop_size=60, ngen=30, generation_hook=hook)

    objs = extract_objectives(pop)
    front_idx = pareto_front(objs)
    front = objs[front_idx]

    df = pd.DataFrame(front, columns=["energy", "cost", "comfort_gap"])
    df["solution_id"] = range(len(df))
    plot_pareto_3d(df, "pareto_demo.html")
    save_frontier_csv(pop, "runs/frontier_demo.csv")

    ref = choose_reference_point(objs)
    hv = None
    if front.shape[1] == 2:
        from mes8_optimization.pareto import hypervolume_2d

        hv = hypervolume_2d(front, tuple(ref))
    print(f"Pareto size: {len(front)}; ref point: {ref}; hypervolume: {hv}")
    print(f"Diversity history (first 5): {metrics['diversity'][:5]}")


if __name__ == "__main__":
    main()
