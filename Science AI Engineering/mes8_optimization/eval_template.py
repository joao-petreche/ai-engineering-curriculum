from __future__ import annotations

"""Template to plug your surrogate or co-simulation evaluator.

Usage:
    from mes8_optimization.eval_template import make_surrogate_evaluator
    evaluate_fn = make_surrogate_evaluator(my_surrogate_model)
    # my_surrogate_model must expose predict(params_dict) -> dict with keys:
    #   energy_kwh_m2, capex_per_m2, comfort_gap, (optional) co2_kg_m2
    # Example:
    #   model.predict({"wwr": 0.3, "wall_thickness_m": 0.2, ...}) ->
    #       {"energy_kwh_m2": 45.2, "capex_per_m2": 1850, "comfort_gap": 0.12}

    bounds = {...}
    pop = build_nsga2(evaluate_fn, bounds, ...)
"""

from typing import Callable, Dict, Tuple

EvaluateFn = Callable[[Dict[str, float]], Tuple[float, float, float]]


def make_surrogate_evaluator(model, co2_key: str = None) -> EvaluateFn:
    """Wrap a surrogate with the expected signature.

    The model must provide predict(params: dict) -> dict containing at least:
      - "energy_kwh_m2"
      - "capex_per_m2"
      - "comfort_gap"
    Optionally:
      - co2_key (e.g., "co2_kg_m2") if you want a 4th objective (not used here).
    """

    def evaluate(params: Dict[str, float]):
        pred = model.predict(params)
        energy = float(pred["energy_kwh_m2"])
        capex = float(pred["capex_per_m2"])
        comfort_gap = float(pred["comfort_gap"])
        return energy, capex, comfort_gap

    return evaluate


def make_cosim_evaluator(run_simulation: Callable[[Dict[str, float]], Dict[str, float]]) -> EvaluateFn:
    """Wrap a co-simulation callable that returns the same keys as above."""

    def evaluate(params: Dict[str, float]):
        pred = run_simulation(params)
        energy = float(pred["energy_kwh_m2"])
        capex = float(pred.get("capex_per_m2", pred.get("capex", 0.0)))
        comfort_gap = float(pred["comfort_gap"])
        return energy, capex, comfort_gap

    return evaluate
