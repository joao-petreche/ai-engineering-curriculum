from __future__ import annotations

import random
from typing import Callable, Dict, List, Sequence, Tuple

import numpy as np
from deap import base, creator, tools

from .constraints import apply_constraints
from .metrics import diversity, extract_objectives

EvaluateFn = Callable[[Dict[str, float]], Tuple[float, float, float]]


class GARunner:
    """NSGA-II runner with constraint penalties and basic metrics."""

    def __init__(
        self,
        evaluate_fn: EvaluateFn,
        bounds: Dict[str, Tuple[float, float]],
        pop_size: int = 60,
        ngen: int = 40,
        cxpb: float = 0.7,
        mutpb: float = 0.2,
    ) -> None:
        self.evaluate_fn = evaluate_fn
        self.bounds = bounds
        self.pop_size = pop_size
        self.ngen = ngen
        self.cxpb = cxpb
        self.mutpb = mutpb
        self.toolbox = base.Toolbox()
        self._init_deap()

    def _init_deap(self) -> None:
        # Avoid duplicate class creation if imported multiple times
        if not hasattr(creator, "FitnessMulti"):
            creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0, -1.0))
        if not hasattr(creator, "Individual"):
            creator.create("Individual", list, fitness=creator.FitnessMulti)

        self.toolbox.register("individual", self._init_individual)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("evaluate", self._eval_individual)
        self.toolbox.register(
            "mate", tools.cxSimulatedBinaryBounded, low=0.0, up=1.0, eta=20.0
        )
        self.toolbox.register(
            "mutate", tools.mutPolynomialBounded, low=0.0, up=1.0, eta=20.0, indpb=0.2
        )
        self.toolbox.register("select", tools.selNSGA2)

    def _init_individual(self) -> creator.Individual:
        genes = []
        for low, high in self.bounds.values():
            genes.append(random.uniform(low, high))
        return creator.Individual(genes)

    def _decode(self, ind: Sequence[float]) -> Dict[str, float]:
        return {k: ind[i] for i, k in enumerate(self.bounds.keys())}

    def _eval_individual(self, ind: Sequence[float]) -> Tuple[float, float, float]:
        params = self._decode(ind)
        penalty, corrected = apply_constraints(params)
        f1, f2, f3 = self.evaluate_fn(corrected)
        return f1 + penalty, f2 + penalty, f3 + penalty

    def run(self, generation_hook=None) -> List[creator.Individual]:
        pop = self.toolbox.population(n=self.pop_size)
        for ind in pop:
            ind.fitness.values = self.toolbox.evaluate(ind)

        for gen in range(self.ngen):
            offspring = tools.selTournamentDCD(pop, len(pop))
            offspring = [self.toolbox.clone(ind) for ind in offspring]

            for i in range(0, len(offspring), 2):
                if random.random() < self.cxpb:
                    self.toolbox.mate(offspring[i], offspring[i + 1])
                    del offspring[i].fitness.values, offspring[i + 1].fitness.values

            for i in range(len(offspring)):
                if random.random() < self.mutpb:
                    self.toolbox.mutate(offspring[i])
                    del offspring[i].fitness.values

            invalid = [ind for ind in offspring if not ind.fitness.valid]
            for ind in invalid:
                ind.fitness.values = self.toolbox.evaluate(ind)

            pop = self.toolbox.select(pop + offspring, self.pop_size)

            if generation_hook is not None:
                generation_hook(gen, pop)

        return pop


def build_nsga2(
    evaluate_fn: EvaluateFn,
    bounds: Dict[str, Tuple[float, float]],
    pop_size: int = 60,
    ngen: int = 40,
    cxpb: float = 0.7,
    mutpb: float = 0.2,
    generation_hook=None,
) -> List[creator.Individual]:
    runner = GARunner(evaluate_fn, bounds, pop_size, ngen, cxpb, mutpb)
    return runner.run(generation_hook=generation_hook)
