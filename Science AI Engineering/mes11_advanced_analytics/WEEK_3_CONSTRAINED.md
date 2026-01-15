# Mês 11 Week 3: Constrained Optimization & Advanced Formulations

## Overview
**Duration**: 12-15 hours  
**Objective**: Solve real optimization problems under complex constraints  
**Deliverable**: Constrained optimizer with penalty methods, Lagrange, and SciPy integration  
**Tech Stack**: SciPy, DEAP, Gurobi (optional), Pandas, NetworkX

---

## Exercise 3.1: Penalty Methods & Constraint Handling

### Learning Objectives
- Implement penalty and barrier methods for constraint handling
- Convert constrained to unconstrained optimization
- Validate solution feasibility

### Implementation Guide

**Create `constrained_optimization.py`:**

```python
import numpy as np
from typing import Dict, List, Callable, Tuple, Optional
from scipy.optimize import minimize, differential_evolution
import pandas as pd


class ConstrainedOptimizer:
    """Optimization with penalty methods for constraints"""
    
    def __init__(self, objective_fn: Callable, 
                 constraints: Dict[str, Tuple[float, float]],
                 bounds: Dict[str, Tuple[float, float]]):
        """
        Args:
            objective_fn: Function to minimize
            constraints: {'param_name': (min, max)}
            bounds: {'param_name': (lower, upper)}
        """
        self.objective_fn = objective_fn
        self.constraints = constraints
        self.bounds = bounds
        self.param_names = list(bounds.keys())
        self.penalty_history = []
    
    def evaluate_constraints(self, x_dict: Dict[str, float]) -> Tuple[bool, List[float]]:
        """
        Check constraint violations
        
        Returns:
            is_feasible, list of violations (0 if satisfied)
        """
        violations = []
        
        for param_name, (min_val, max_val) in self.constraints.items():
            value = x_dict.get(param_name)
            if value is None:
                continue
            
            if value < min_val:
                violations.append(min_val - value)
            elif value > max_val:
                violations.append(value - max_val)
            else:
                violations.append(0.0)
        
        is_feasible = all(v == 0.0 for v in violations)
        return is_feasible, violations
    
    def penalty_function(self, x_dict: Dict[str, float], 
                        penalty_weight: float = 1e6) -> float:
        """
        Penalized objective: obj + weight * sum(constraint_violations^2)
        """
        obj_value = self.objective_fn(x_dict)
        _, violations = self.evaluate_constraints(x_dict)
        
        penalty = penalty_weight * sum(v ** 2 for v in violations)
        
        return obj_value + penalty
    
    def barrier_function(self, x_dict: Dict[str, float],
                        barrier_weight: float = 0.1) -> float:
        """
        Barrier method: obj - weight * sum(log(constraint_margin))
        """
        obj_value = self.objective_fn(x_dict)
        
        barrier = 0.0
        for param_name, (min_val, max_val) in self.constraints.items():
            value = x_dict.get(param_name)
            if value is None:
                continue
            
            lower_margin = value - min_val
            upper_margin = max_val - value
            
            if lower_margin > 0 and upper_margin > 0:
                barrier -= barrier_weight * (np.log(lower_margin) + np.log(upper_margin))
            else:
                return float('inf')  # Infeasible
        
        return obj_value + barrier
    
    def optimize_penalty(self, method: str = 'L-BFGS-B', 
                        penalty_weight: float = 1e6) -> Dict[str, float]:
        """
        Optimize using penalty method
        
        Args:
            method: scipy.optimize.minimize method
            penalty_weight: Penalty multiplier
        
        Returns:
            Dictionary of optimized parameters
        """
        # Initial guess
        x0 = np.array([
            (self.bounds[name][0] + self.bounds[name][1]) / 2
            for name in self.param_names
        ])
        
        # Bounds
        bounds = [self.bounds[name] for name in self.param_names]
        
        # Objective with penalty
        def penalized_obj(x):
            x_dict = {name: val for name, val in zip(self.param_names, x)}
            return self.penalty_function(x_dict, penalty_weight)
        
        # Optimize
        result = minimize(penalized_obj, x0, method=method, bounds=bounds)
        
        optimized = {name: val for name, val in zip(self.param_names, result.x)}
        
        return optimized
    
    def optimize_augmented_lagrangian(self, max_iterations: int = 20,
                                     rho: float = 1.0) -> Dict[str, float]:
        """
        Augmented Lagrangian method
        
        Alternately minimizes Lagrangian and updates multipliers
        """
        # Initialize Lagrange multipliers and penalty
        n_constraints = len(self.constraints)
        lambdas = np.zeros(n_constraints)
        rho = rho
        
        best_x = None
        best_obj = float('inf')
        
        for iteration in range(max_iterations):
            # Minimize Lagrangian
            def lagrangian(x):
                x_dict = {name: val for name, val in zip(self.param_names, x)}
                obj = self.objective_fn(x_dict)
                _, violations = self.evaluate_constraints(x_dict)
                
                # Augmented Lagrangian
                lag = obj + sum(
                    lambdas[i] * violations[i] + 0.5 * rho * violations[i] ** 2
                    for i in range(len(violations))
                )
                return lag
            
            # Initial guess
            x0 = np.array([
                (self.bounds[name][0] + self.bounds[name][1]) / 2
                for name in self.param_names
            ])
            bounds = [self.bounds[name] for name in self.param_names]
            
            result = minimize(lagrangian, x0, method='L-BFGS-B', bounds=bounds)
            x = result.x
            x_dict = {name: val for name, val in zip(self.param_names, x)}
            
            # Check feasibility
            is_feasible, violations = self.evaluate_constraints(x_dict)
            obj_value = self.objective_fn(x_dict)
            
            if obj_value < best_obj:
                best_obj = obj_value
                best_x = x.copy()
            
            # Update Lagrange multipliers
            lambdas += rho * np.array(violations)
            
            # Check convergence
            max_violation = max(abs(v) for v in violations)
            if max_violation < 1e-6:
                break
        
        return {name: val for name, val in zip(self.param_names, best_x)}
    
    def optimize_differential_evolution(self, seed: int = 42) -> Dict[str, float]:
        """
        Global optimization with DE
        """
        bounds = [self.bounds[name] for name in self.param_names]
        
        def penalized_obj(x):
            x_dict = {name: val for name, val in zip(self.param_names, x)}
            return self.penalty_function(x_dict, penalty_weight=1e6)
        
        result = differential_evolution(penalized_obj, bounds, seed=seed)
        
        return {name: val for name, val in zip(self.param_names, result.x)}


# Example usage
if __name__ == "__main__":
    def objective(config):
        x, y = config.get('x', 0), config.get('y', 0)
        return (x - 3) ** 2 + (y - 4) ** 2
    
    constraints = {
        'x': (0, 5),      # 0 <= x <= 5
        'y': (1, 6),      # 1 <= y <= 6
    }
    bounds = constraints.copy()
    
    optimizer = ConstrainedOptimizer(objective, constraints, bounds)
    
    # Compare methods
    result_penalty = optimizer.optimize_penalty()
    result_lag = optimizer.optimize_augmented_lagrangian()
    result_de = optimizer.optimize_differential_evolution()
    
    print("Penalty method:", result_penalty)
    print("Augmented Lagrangian:", result_lag)
    print("Differential Evolution:", result_de)
```

### Checkpoint Requirements

- [ ] **Penalty Method**: Implementation working with various weights
- [ ] **Barrier Method**: Logarithmic barriers applied correctly
- [ ] **Augmented Lagrangian**: Multipliers updated iteratively
- [ ] **Multiple Solvers**: Penalty, Lagrangian, and DE all functional
- [ ] **Feasibility Checking**: Solutions validated against constraints

---

## Exercise 3.2: Multi-Objective Constrained Optimization

### Learning Objectives
- Optimize multiple objectives simultaneously with constraints
- Explore Pareto front under feasibility boundaries
- Balance competing objectives

### Implementation Guide

**Create `multiobjective_constrained.py`:**

```python
import numpy as np
import pandas as pd
from typing import Dict, List, Callable, Tuple
from deap import base, creator, tools, algorithms
import matplotlib.pyplot as plt


class MultiObjectiveConstrainedOptimizer:
    """Multi-objective optimization with hard and soft constraints"""
    
    def __init__(self, objectives: Dict[str, Callable],
                 constraints: Dict[str, Tuple[float, float]],
                 bounds: Dict[str, Tuple[float, float]],
                 weights: Dict[str, float] = None):
        """
        Args:
            objectives: {'objective_name': function}
            constraints: {'param': (min, max)}
            bounds: {'param': (lower, upper)}
            weights: {'objective_name': weight} for Pareto feasibility
        """
        self.objectives = objectives
        self.constraints = constraints
        self.bounds = bounds
        self.param_names = list(bounds.keys())
        self.weights = weights or {name: 1.0 for name in objectives.keys()}
        
        # DEAP setup
        creator.create("FitnessMulti", base.Fitness, weights=tuple(
            -1.0 if self.weights[name] > 0 else 1.0
            for name in objectives.keys()
        ))
        creator.create("Individual", list, fitness=creator.FitnessMulti)
        
        self.toolbox = base.Toolbox()
        self._setup_toolbox()
        
        self.logbook = None
        self.hof = None
    
    def _setup_toolbox(self):
        """Configure DEAP genetic operators"""
        # Attribute generators
        for param_name in self.param_names:
            lower, upper = self.bounds[param_name]
            self.toolbox.register(
                f"attr_{param_name}",
                np.random.uniform,
                lower, upper
            )
        
        # Individual and population
        attrs = [getattr(self.toolbox, f"attr_{name}") for name in self.param_names]
        self.toolbox.register(
            "individual",
            tools.initCycle,
            creator.Individual,
            attrs,
            n=1
        )
        self.toolbox.register(
            "population",
            tools.initRepeat,
            list,
            self.toolbox.individual
        )
        
        # Genetic operators
        self.toolbox.register("evaluate", self._evaluate)
        self.toolbox.register("mate", tools.cxBlend, alpha=0.5)
        self.toolbox.register("mutate", self._mutate)
        self.toolbox.register("select", tools.selNSGA2)
    
    def _evaluate(self, individual: creator.Individual) -> Tuple[float, ...]:
        """Evaluate all objectives"""
        config = {name: val for name, val in zip(self.param_names, individual)}
        
        # Check feasibility
        is_feasible, violations = self._check_constraints(config)
        
        # If infeasible, return penalized values
        if not is_feasible:
            penalty = 1e9 * sum(v ** 2 for v in violations)
            return tuple(penalty for _ in self.objectives)
        
        # Evaluate objectives
        return tuple(self.objectives[name](config) for name in self.objectives.keys())
    
    def _check_constraints(self, config: Dict[str, float]) -> Tuple[bool, List[float]]:
        """Check constraint satisfaction"""
        violations = []
        
        for param_name, (min_val, max_val) in self.constraints.items():
            value = config.get(param_name)
            if value is None:
                continue
            
            if value < min_val:
                violations.append(min_val - value)
            elif value > max_val:
                violations.append(value - max_val)
            else:
                violations.append(0.0)
        
        is_feasible = all(v == 0.0 for v in violations)
        return is_feasible, violations
    
    def _mutate(self, individual):
        """Custom mutation respecting bounds"""
        for i, param_name in enumerate(self.param_names):
            if np.random.random() < 0.2:
                lower, upper = self.bounds[param_name]
                individual[i] = np.random.uniform(lower, upper)
        
        return individual,
    
    def optimize(self, pop_size: int = 50, generations: int = 50,
                seed: int = 42) -> List[creator.Individual]:
        """
        Run NSGA-II optimization
        
        Returns:
            Pareto-optimal solutions
        """
        np.random.seed(seed)
        
        population = self.toolbox.population(n=pop_size)
        self.hof = tools.ParetoFront()
        self.hof.update(population)
        
        # Statistics
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean, axis=0)
        stats.register("std", np.std, axis=0)
        
        # Run algorithm
        population, self.logbook = algorithms.eaMulti(
            population, self.toolbox,
            cxpb=0.7, mutpb=0.3,
            ngen=generations,
            stats=stats,
            verbose=False
        )
        
        self.hof.update(population)
        return self.hof
    
    def get_pareto_dataframe(self) -> pd.DataFrame:
        """Get Pareto front as DataFrame"""
        if self.hof is None:
            return None
        
        rows = []
        for ind in self.hof:
            row = {name: val for name, val in zip(self.param_names, ind)}
            for obj_name, fitness_val in zip(self.objectives.keys(), ind.fitness.values):
                row[obj_name] = fitness_val
            rows.append(row)
        
        return pd.DataFrame(rows)
    
    def plot_pareto_front(self, obj1: str, obj2: str, figsize=(10, 8)):
        """Plot 2D Pareto front"""
        if self.hof is None:
            return None
        
        fig, ax = plt.subplots(figsize=figsize)
        
        values = [ind.fitness.values for ind in self.hof]
        obj_names = list(self.objectives.keys())
        idx1 = obj_names.index(obj1)
        idx2 = obj_names.index(obj2)
        
        obj1_vals = [v[idx1] for v in values]
        obj2_vals = [v[idx2] for v in values]
        
        ax.scatter(obj1_vals, obj2_vals, s=100, alpha=0.6)
        ax.set_xlabel(obj1)
        ax.set_ylabel(obj2)
        ax.set_title(f'Pareto Front: {obj1} vs {obj2}')
        ax.grid(True, alpha=0.3)
        
        return fig


# Example usage
if __name__ == "__main__":
    objectives = {
        'cost': lambda c: c.get('x', 0) ** 2,
        'quality': lambda c: (c.get('y', 0) - 10) ** 2,
    }
    
    constraints = {
        'x': (0, 10),
        'y': (0, 20),
    }
    
    bounds = constraints.copy()
    
    optimizer = MultiObjectiveConstrainedOptimizer(objectives, constraints, bounds)
    pareto_front = optimizer.optimize(pop_size=30, generations=30)
    
    df = optimizer.get_pareto_dataframe()
    print(df)
    
    fig = optimizer.plot_pareto_front('cost', 'quality')
    plt.show()
```

### Checkpoint Requirements

- [ ] **NSGA-II Implementation**: Multi-objective with constraint handling
- [ ] **Pareto Front**: 10+ non-dominated solutions found
- [ ] **Constraint Validation**: All final solutions feasible
- [ ] **Convergence**: Fitness improves over generations
- [ ] **Visualization**: 2D Pareto fronts plotted correctly

---

## Exercise 3.3: Real-World Constrained Problem

### Learning Objectives
- Solve realistic manufacturing/supply chain optimization
- Integrate multiple constraint types
- Validate and document solution

### Implementation Guide

**Create `real_world_optimization.py`:**

```python
# Manufacturing Problem: Minimize cost while meeting demand and capacity constraints

import numpy as np
import pandas as pd
from typing import Dict, List
from scipy.optimize import minimize


class ManufacturingOptimizer:
    """
    Optimize production schedules:
    - Minimize: Total cost
    - Subject to:
      - Meet demand at each facility
      - Respect machine capacity
      - Inventory constraints
      - Transportation limits
    """
    
    def __init__(self):
        self.facilities = ['Factory_A', 'Factory_B', 'Factory_C']
        self.products = ['Product_1', 'Product_2', 'Product_3']
        self.periods = 4  # Quarters
        
        # Cost parameters (per unit)
        self.production_cost = {
            'Factory_A': {'Product_1': 100, 'Product_2': 120, 'Product_3': 110},
            'Factory_B': {'Product_1': 105, 'Product_2': 115, 'Product_3': 125},
            'Factory_C': {'Product_1': 110, 'Product_2': 118, 'Product_3': 108},
        }
        
        self.holding_cost = 5  # per unit per period
        self.transport_cost = 2  # per unit
        
        # Demand (units per period)
        self.demand = {
            'Product_1': [1000, 1200, 1100, 1300],
            'Product_2': [800, 900, 950, 1000],
            'Product_3': [600, 700, 750, 800],
        }
        
        # Capacity (units per period)
        self.capacity = {
            'Factory_A': 2000,
            'Factory_B': 2500,
            'Factory_C': 2000,
        }
        
        # Max inventory per facility
        self.max_inventory = 1000
    
    def objective(self, x: np.ndarray) -> float:
        """
        Calculate total cost
        x: flattened array of production quantities
        """
        cost = 0.0
        idx = 0
        
        for facility in self.facilities:
            for product in self.products:
                for period in range(self.periods):
                    production = x[idx]
                    cost += production * self.production_cost[facility][product]
                    cost += production * self.holding_cost  # Holding cost
                    cost += production * self.transport_cost
                    idx += 1
        
        return cost
    
    def constraints_factory_capacity(self, x: np.ndarray) -> List[float]:
        """Capacity constraints: production <= capacity per facility/period"""
        violations = []
        idx = 0
        
        for facility in self.facilities:
            for period in range(self.periods):
                period_production = 0.0
                
                for product in self.products:
                    period_production += x[idx]
                    idx += 1
                
                capacity = self.capacity[facility]
                if period_production > capacity:
                    violations.append(period_production - capacity)
                else:
                    violations.append(0.0)
        
        return violations
    
    def constraints_demand_met(self, x: np.ndarray) -> List[float]:
        """Demand constraints: total production >= demand"""
        violations = []
        idx = 0
        
        for facility in self.facilities:
            for product in self.products:
                product_production = 0.0
                
                for period in range(self.periods):
                    product_production += x[idx]
                    idx += 1
                
                total_demand = sum(self.demand[product])
                if product_production < total_demand:
                    violations.append(total_demand - product_production)
                else:
                    violations.append(0.0)
        
        return violations
    
    def optimize(self) -> Dict:
        """Solve the optimization problem"""
        n_vars = len(self.facilities) * len(self.products) * self.periods
        
        # Bounds: non-negative production
        bounds = [(0, 3000) for _ in range(n_vars)]
        
        # Initial guess
        x0 = np.ones(n_vars) * 100
        
        # Constraints
        constraints = []
        
        # Capacity constraints
        def capacity_constraint(x):
            violations = self.constraints_factory_capacity(x)
            return np.array([-v for v in violations])  # SciPy minimizes, so negate
        
        constraints.append({'type': 'ineq', 'fun': capacity_constraint})
        
        # Demand constraints
        def demand_constraint(x):
            violations = self.constraints_demand_met(x)
            return np.array([v for v in violations])
        
        constraints.append({'type': 'ineq', 'fun': demand_constraint})
        
        # Solve
        result = minimize(
            self.objective,
            x0,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints,
            options={'maxiter': 500}
        )
        
        return {
            'success': result.success,
            'total_cost': result.fun,
            'production': result.x,
            'message': result.message
        }


# Example usage
if __name__ == "__main__":
    optimizer = ManufacturingOptimizer()
    result = optimizer.optimize()
    
    print(f"Optimization success: {result['success']}")
    print(f"Total cost: ${result['total_cost']:,.2f}")
    print(f"Message: {result['message']}")
```

### Checkpoint Requirements

- [ ] **Real-World Problem**: Manufacturing or supply chain setup
- [ ] **Multiple Constraints**: 3+ different constraint types
- [ ] **Solution Found**: Optimizer converges to feasible solution
- [ ] **Validation**: All constraints satisfied in final solution
- [ ] **Cost Reduction**: Solution shows 10%+ improvement over baseline

---

## Summary & Certification

### Week 3 Deliverables

| Exercise | Component | Status |
|----------|-----------|--------|
| 3.1 | Penalty Methods | Penalty, barrier, augmented Lagrangian |
| 3.2 | Multi-Obj Constrained | NSGA-II with constraints, Pareto front |
| 3.3 | Real-World Problem | Manufacturing optimization example |

### Validation Checklist

- [ ] All 3 exercises completed
- [ ] Penalty method converges to feasible solution
- [ ] Augmented Lagrangian multipliers update correctly
- [ ] NSGA-II produces diverse Pareto front
- [ ] Manufacturing problem satisfies all constraints
- [ ] Documentation complete with examples

### Next Steps

✅ **Week 3 Complete**: Move to [Week 4: Advanced Analytics & Optuna](WEEK_4_OPTUNA.md)
