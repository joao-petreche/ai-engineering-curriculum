from __future__ import annotations

import copy
import random
from typing import Callable, Dict, List, Tuple

from deap import tools

from .ga_runner import GARunner
from .metrics import extract_objectives, diversity
from .pareto import pareto_front

EvaluateFn = Callable[[Dict[str, float]], Tuple[float, float, float]]


def migrate(pop_a, pop_b, k: int = 2):
    """Exchange top-k individuals between two populations (in place)."""
    best_a = tools.selBest(pop_a, k)
    best_b = tools.selBest(pop_b, k)
    pop_a[-k:] = [copy.deepcopy(ind) for ind in best_b]
    pop_b[-k:] = [copy.deepcopy(ind) for ind in best_a]


def run_islands(
    evaluate_fn: EvaluateFn,
    bounds: Dict[str, Tuple[float, float]],
    n_islands: int = 4,
    pop_size: int = 40,
    ngen: int = 40,
    migrate_every: int = 5,
    migrants: int = 2,
    generation_hook=None,
):
    """Run multiple GA islands with periodic migration.

    Returns
    -------
    populations: List of final populations (per island)
    metrics: dict with diversity history per island
    """
    islands: List[GARunner] = [
        GARunner(evaluate_fn, bounds, pop_size=pop_size, ngen=ngen) for _ in range(n_islands)
    ]
    pops = [runner.toolbox.population(n=pop_size) for runner in islands]

    # initial evaluation
    for pop, runner in zip(pops, islands):
        for ind in pop:
            ind.fitness.values = runner.toolbox.evaluate(ind)

    diversity_history = [[] for _ in range(n_islands)]

    for gen in range(ngen):
        for idx, runner in enumerate(islands):
            offspring = tools.selTournamentDCD(pops[idx], len(pops[idx]))
            offspring = [runner.toolbox.clone(ind) for ind in offspring]

            # Variation
            for i in range(0, len(offspring), 2):
                if random.random() < runner.cxpb:
                    runner.toolbox.mate(offspring[i], offspring[i + 1])
                    del offspring[i].fitness.values, offspring[i + 1].fitness.values
            for i in range(len(offspring)):
                if random.random() < runner.mutpb:
                    runner.toolbox.mutate(offspring[i])
                    del offspring[i].fitness.values

            invalid = [ind for ind in offspring if not ind.fitness.valid]
            for ind in invalid:
                ind.fitness.values = runner.toolbox.evaluate(ind)

            pops[idx] = runner.toolbox.select(pops[idx] + offspring, pop_size)
            diversity_history[idx].append(diversity(pops[idx]))

            if generation_hook is not None:
                generation_hook(gen, pops[idx], idx)

        # Migration step
        if (gen + 1) % migrate_every == 0:
            for i in range(n_islands):
                j = (i + 1) % n_islands
                migrate(pops[i], pops[j], k=migrants)

    metrics = {"diversity": diversity_history}
    return pops, metrics


def aggregate_frontier(pops):
    """Combine populations and return the merged Pareto frontier objectives array."""
    merged = []
    for pop in pops:
        merged.extend(pop)
    objs = extract_objectives(merged)
    front = pareto_front(objs)
    return objs[front]
