"""Mês 8 optimization toolkit: Pareto, GA, constraints, decision support."""

from .pareto import pareto_front, hypervolume_2d, choose_reference_point, normalize_objectives
from .constraints import apply_constraints, clamp_params
from .ga_runner import build_nsga2
from .island_runner import run_islands, aggregate_frontier
from .decision import choose_compromise
from .sensitivity import tornado_impact
from .visualization import plot_pareto_3d
from .metrics import diversity, extract_objectives
from .hooks import build_generation_logger
from .frontier_export import save_frontier_csv

__all__ = [
    "pareto_front",
    "hypervolume_2d",
    "choose_reference_point",
    "normalize_objectives",
    "apply_constraints",
    "clamp_params",
    "build_nsga2",
    "run_islands",
    "aggregate_frontier",
    "choose_compromise",
    "tornado_impact",
    "plot_pareto_3d",
    "diversity",
    "extract_objectives",
    "build_generation_logger",
    "save_frontier_csv",
]
