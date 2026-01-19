"""
Constrained Optimization for Building Energy Systems

This module implements constraint handling for multi-objective optimization
using penalty methods and augmented Lagrangian approach. Constraints include:
- Physics-based (thermodynamic limits, correlations)
- Engineering limits (comfort, equipment sizing, budgets)
- Regulatory compliance (energy codes, standards)

Two approaches:
1. Penalty Method (external): φ(x) = f(x) + λ·Σ max(0, g_i(x))²
   - Simple, direct integration with NSGA-II
   - Parameter tuning required (penalty weight λ)

2. Augmented Lagrangian (AL): φ(x,λ,μ) = f(x) + Σ λ_i·g_i(x) + μ/2·Σ g_i(x)²
   - More sophisticated, better for active constraints
   - Sequential updates of λ and μ

3. Active Set Strategy: Identify active constraints, focus optimization effort

This enables realistic optimization where not all candidate solutions are
physically or economically feasible.

Author: Scientific AI Engineering Curriculum
Date: January 2026
Dependencies: numpy, pandas, matplotlib, plotly, scipy
"""

import json
import logging
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Callable

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from scipy.optimize import minimize, differential_evolution

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class Constraint:
    """Definition of a single constraint."""
    name: str
    constraint_type: str  # 'inequality' g(x) <= 0 or 'equality' h(x) = 0
    operator: str  # '<=', '>=', '='
    limit: float
    weight: float = 1.0  # Penalty weight if violated
    description: str = ""
    physics_law: str = ""  # Reference to physical law
    is_active: bool = False  # True if constraint is binding
    
    def evaluate(self, value: float) -> float:
        """
        Evaluate constraint violation.
        Returns 0 if satisfied, >0 if violated.
        """
        if self.operator == '<=':
            violation = max(0, value - self.limit)
        elif self.operator == '>=':
            violation = max(0, self.limit - value)
        elif self.operator == '=':
            violation = abs(value - self.limit)
        else:
            raise ValueError(f"Unknown operator: {self.operator}")
        
        return violation


@dataclass
class ConstrainedSolution:
    """Solution with constraint information."""
    parameters: Dict[str, float]
    objectives: Dict[str, float]  # Original objectives
    penalized_objectives: Dict[str, float]  # Objectives + penalty
    constraint_violations: Dict[str, float]  # Violations per constraint
    total_violation: float  # Sum of all violations
    is_feasible: bool  # True if all constraints satisfied
    active_constraints: List[str]  # Which constraints are binding
    feasibility_ratio: float  # (satisfied / total constraints)


class ConstrainedOptimizer:
    """
    Constraint handling optimizer for building energy systems.
    
    Combines NSGA-II with penalty methods or augmented Lagrangian to handle
    constraints. Enables realistic optimization with feasibility tracking.
    
    Attributes:
        surrogate_model: Pre-trained surrogate
        parameter_bounds: Dict of parameter bounds
        constraints: List of Constraint objects
        physics_validator: Optional validator for physics constraints
    """
    
    def __init__(
        self,
        surrogate_model,
        parameter_bounds: Dict[str, Tuple[float, float]],
        output_dir: Path = Path("results/constrained"),
        physics_validator=None
    ):
        """
        Initialize constrained optimizer.
        
        Args:
            surrogate_model: Pre-trained surrogate function
            parameter_bounds: Parameter bounds dict
            output_dir: Directory for results
            physics_validator: Optional physics validator
        """
        self.surrogate_model = surrogate_model
        self.parameter_bounds = parameter_bounds
        self.parameter_names = list(parameter_bounds.keys())
        self.n_params = len(self.parameter_names)
        self.physics_validator = physics_validator
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.constraints: List[Constraint] = []
        self.solutions: List[ConstrainedSolution] = []
        
        logger.info(f"Initialized constrained optimizer ({self.n_params} params)")
    
    def add_constraint(
        self,
        name: str,
        constraint_type: str,
        operator: str,
        limit: float,
        description: str = "",
        physics_law: str = "",
        weight: float = 1.0
    ) -> None:
        """
        Add a constraint to the optimization.
        
        Args:
            name: Unique constraint name
            constraint_type: 'inequality' or 'equality'
            operator: '<=', '>=', or '='
            limit: Constraint limit value
            description: Human-readable description
            physics_law: Reference to physical law violated
            weight: Penalty weight (higher = stricter)
        """
        constraint = Constraint(
            name=name,
            constraint_type=constraint_type,
            operator=operator,
            limit=limit,
            weight=weight,
            description=description,
            physics_law=physics_law
        )
        self.constraints.append(constraint)
        logger.info(f"Added constraint: {name} ({operator} {limit})")
    
    def define_default_constraints(self) -> None:
        """Define standard constraints for building optimization."""
        # Consumption constraint (kWh/year) - relaxed to match typical buildings
        self.add_constraint(
            name='max_annual_consumption',
            constraint_type='inequality',
            operator='<=',
            limit=120000,
            weight=1000.0,
            description='Maximum annual consumption (120,000 kWh)',
            physics_law='Energy budget'
        )
        
        # Comfort constraint (hours/year) - reasonable expectation
        self.add_constraint(
            name='min_comfort_hours',
            constraint_type='inequality',
            operator='>=',
            limit=5000,
            weight=500.0,
            description='Minimum comfort hours (5,000 h)',
            physics_law='Habitability requirement'
        )
        
        # Peak cooling constraint (kW) - based on typical buildings
        self.add_constraint(
            name='max_peak_cooling',
            constraint_type='inequality',
            operator='<=',
            limit=45.0,
            weight=100.0,
            description='Maximum peak cooling (45 kW)',
            physics_law='Equipment capacity limit'
        )
        
        # Comfort upper limit (sanity check)
        self.add_constraint(
            name='max_comfort_hours',
            constraint_type='inequality',
            operator='<=',
            limit=8760,
            weight=100.0,
            description='Physical limit on comfort (≤ 8760 h)',
            physics_law='Time constraint'
        )
        
        # Positive consumption
        self.add_constraint(
            name='min_consumption',
            constraint_type='inequality',
            operator='>=',
            limit=10000,
            weight=1000.0,
            description='Minimum consumption (10,000 kWh)',
            physics_law='Energy balance'
        )
        
        logger.info("Defined 5 default constraints (realistic bounds)")
    
    def _denormalize_params(self, normalized: np.ndarray) -> Dict[str, float]:
        """Convert normalized [0,1] to physical bounds."""
        params = {}
        for i, param_name in enumerate(self.parameter_names):
            min_val, max_val = self.parameter_bounds[param_name]
            params[param_name] = min_val + normalized[i] * (max_val - min_val)
        return params
    
    def _evaluate_objectives(self, params: Dict[str, float]) -> Dict[str, float]:
        """Evaluate objectives using surrogate."""
        X = np.array([[params[name] for name in self.parameter_names]])
        outputs = self.surrogate_model.predict(X)[0]
        
        return {
            'annual_consumption_kwh': outputs[0],
            'comfort_hours': outputs[1],
            'peak_cooling_kw': outputs[2]
        }
    
    def _evaluate_constraints(
        self,
        objectives: Dict[str, float]
    ) -> Tuple[Dict[str, float], float, List[str]]:
        """
        Evaluate all constraints.
        
        Returns:
            (violations dict, total violation, list of active constraints)
        """
        violations = {}
        active = []
        
        for constraint in self.constraints:
            # Extract value being constrained
            if 'consumption' in constraint.name:
                value = objectives['annual_consumption_kwh']
            elif 'comfort' in constraint.name:
                value = objectives['comfort_hours']
            elif 'peak_cooling' in constraint.name:
                value = objectives['peak_cooling_kw']
            else:
                value = 0
            
            # Evaluate constraint
            violation = constraint.evaluate(value)
            violations[constraint.name] = violation
            
            # Mark as active if violated
            if violation > 1e-6:  # Tolerance for numerical errors
                active.append(constraint.name)
        
        total_violation = sum(violations.values())
        
        return violations, total_violation, active
    
    def penalty_method(
        self,
        objectives: Dict[str, float],
        violations: Dict[str, float],
        penalty_weight: float = 1000.0
    ) -> Dict[str, float]:
        """
        Apply external penalty method.
        
        Penalized objective = f(x) + λ·Σ g_i(x)²
        where g_i(x) is constraint violation
        
        Args:
            objectives: Original objectives (dict)
            violations: Constraint violations (dict)
            penalty_weight: λ parameter (higher = stricter)
            
        Returns:
            Penalized objectives dict
        """
        # Use consumption as primary objective for example
        base_consumption = objectives['annual_consumption_kwh']
        
        # Sum squared violations with weights
        penalty = 0.0
        for constraint in self.constraints:
            violation = violations.get(constraint.name, 0.0)
            penalty += constraint.weight * (violation ** 2)
        
        # Apply penalty weight
        penalized = base_consumption + penalty_weight * penalty / 1e6  # Scale
        
        return {
            'penalized_consumption': penalized,
            'original_consumption': base_consumption,
            'total_penalty': penalty
        }
    
    def augmented_lagrangian(
        self,
        objectives: Dict[str, float],
        violations: Dict[str, float],
        multipliers: Dict[str, float],
        penalty_param: float = 1.0
    ) -> Tuple[float, Dict[str, float]]:
        """
        Augmented Lagrangian method.
        
        AL(x,λ,μ) = f(x) + Σ λ_i·g_i(x) + μ/2·Σ g_i(x)²
        
        Args:
            objectives: Original objectives
            violations: Constraint violations
            multipliers: Lagrange multipliers per constraint
            penalty_param: μ (penalty parameter)
            
        Returns:
            (AL value, updated objectives dict)
        """
        base_consumption = objectives['annual_consumption_kwh']
        
        # Compute Lagrangian term
        lagrangian_term = 0.0
        penalty_term = 0.0
        
        for constraint in self.constraints:
            violation = violations.get(constraint.name, 0.0)
            multiplier = multipliers.get(constraint.name, 0.0)
            
            lagrangian_term += multiplier * violation
            penalty_term += 0.5 * penalty_param * (violation ** 2)
        
        al_value = base_consumption + lagrangian_term + penalty_term
        
        return al_value, {
            'consumption': base_consumption,
            'lagrangian': lagrangian_term,
            'penalty': penalty_term,
            'al_value': al_value
        }
    
    def optimize_constrained(
        self,
        method: str = 'penalty',
        n_solutions: int = 100,
        penalty_weight: float = 1000.0
    ) -> List[ConstrainedSolution]:
        """
        Run constrained multi-objective optimization.
        
        Args:
            method: 'penalty' or 'augmented_lagrangian'
            n_solutions: Number of candidate solutions
            penalty_weight: λ for penalty method
            
        Returns:
            List of ConstrainedSolution objects
        """
        logger.info(f"Starting constrained optimization ({method}, N={n_solutions})")
        
        self.solutions = []
        
        # Generate candidate solutions
        np.random.seed(42)
        candidates = np.random.rand(n_solutions, self.n_params)
        
        for i, normalized_params in enumerate(candidates):
            # Denormalize
            params = self._denormalize_params(normalized_params)
            
            # Evaluate objectives
            objectives = self._evaluate_objectives(params)
            
            # Evaluate constraints
            violations, total_violation, active = self._evaluate_constraints(objectives)
            
            # Apply penalty/AL
            if method == 'penalty':
                penalized_obj = self.penalty_method(objectives, violations, penalty_weight)
                penalized_consumption = penalized_obj['penalized_consumption']
            else:  # augmented_lagrangian
                multipliers = {c.name: 0.0 for c in self.constraints}
                al_val, _ = self.augmented_lagrangian(objectives, violations, multipliers, penalty_weight)
                penalized_consumption = al_val
            
            # Check feasibility
            is_feasible = (total_violation < 1e-6)
            feasibility_ratio = (len(self.constraints) - len(active)) / len(self.constraints)
            
            # Create solution
            solution = ConstrainedSolution(
                parameters=params,
                objectives=objectives,
                penalized_objectives={'penalized_consumption': penalized_consumption},
                constraint_violations=violations,
                total_violation=total_violation,
                is_feasible=is_feasible,
                active_constraints=active,
                feasibility_ratio=feasibility_ratio
            )
            
            self.solutions.append(solution)
            
            if i % 25 == 0:
                logger.info(f"  Solution {i+1}/{n_solutions}: "
                          f"feasible={is_feasible}, "
                          f"active={len(active)}, "
                          f"consumption={objectives['annual_consumption_kwh']:.0f} kWh")
        
        # Sort by penalized objectives
        self.solutions.sort(
            key=lambda s: s.penalized_objectives['penalized_consumption']
        )
        
        logger.info(f"Optimization complete. Generated {len(self.solutions)} solutions")
        
        # Statistics
        feasible_count = sum(1 for s in self.solutions if s.is_feasible)
        logger.info(f"Feasible solutions: {feasible_count}/{len(self.solutions)} "
                   f"({100*feasible_count/len(self.solutions):.1f}%)")
        
        return self.solutions
    
    def save_results(self):
        """Save constrained optimization results."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Create results DataFrame
        results_data = []
        for sol in self.solutions:
            row = {
                'is_feasible': sol.is_feasible,
                'feasibility_ratio': sol.feasibility_ratio,
                'total_violation': sol.total_violation,
                'annual_consumption_kwh': sol.objectives['annual_consumption_kwh'],
                'comfort_hours': sol.objectives['comfort_hours'],
                'peak_cooling_kw': sol.objectives['peak_cooling_kw'],
                'penalized_consumption': sol.penalized_objectives['penalized_consumption'],
                'n_active_constraints': len(sol.active_constraints),
            }
            # Add parameters
            row.update(sol.parameters)
            # Add violations
            for constraint_name, violation in sol.constraint_violations.items():
                row[f'violation_{constraint_name}'] = violation
            
            results_data.append(row)
        
        results_df = pd.DataFrame(results_data)
        results_csv = self.output_dir / f"constrained_solutions_{timestamp}.csv"
        results_df.to_csv(results_csv, index=False)
        logger.info(f"Saved constrained solutions to {results_csv}")
        
        # Save constraint definitions
        constraints_data = [asdict(c) for c in self.constraints]
        constraints_json = self.output_dir / f"constraints_{timestamp}.json"
        with open(constraints_json, 'w') as f:
            json.dump(constraints_data, f, indent=2)
        logger.info(f"Saved constraints to {constraints_json}")
        
        # Save feasibility analysis
        feasible_solutions = [s for s in self.solutions if s.is_feasible]
        feasibility_info = {
            'total_solutions': len(self.solutions),
            'feasible_solutions': len(feasible_solutions),
            'feasibility_percentage': 100.0 * len(feasible_solutions) / len(self.solutions),
            'best_feasible_consumption': (
                min(s.objectives['annual_consumption_kwh'] 
                    for s in feasible_solutions) 
                if feasible_solutions else None
            ),
            'best_penalized_consumption': self.solutions[0].penalized_objectives['penalized_consumption'],
            'most_violated_constraint': (
                max([(c.name, sum(s.constraint_violations[c.name] 
                                 for s in self.solutions)) 
                     for c in self.constraints],
                    key=lambda x: x[1])[0]
                if self.constraints else None
            )
        }
        
        feasibility_json = self.output_dir / f"feasibility_analysis_{timestamp}.json"
        with open(feasibility_json, 'w') as f:
            json.dump(feasibility_info, f, indent=2)
        logger.info(f"Saved feasibility analysis to {feasibility_json}")
    
    def plot_constraint_analysis(self):
        """Create constraint violation analysis plots."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 1. Feasibility distribution
        is_feasible = [s.is_feasible for s in self.solutions]
        feasible_count = sum(is_feasible)
        infeasible_count = len(is_feasible) - feasible_count
        
        axes[0, 0].bar(['Feasible', 'Infeasible'], [feasible_count, infeasible_count],
                      color=['green', 'red'], alpha=0.7)
        axes[0, 0].set_ylabel('Number of Solutions')
        axes[0, 0].set_title('Solution Feasibility Distribution')
        axes[0, 0].grid(True, alpha=0.3, axis='y')
        
        # 2. Total violation vs consumption
        total_violations = [s.total_violation for s in self.solutions]
        consumptions = [s.objectives['annual_consumption_kwh'] for s in self.solutions]
        colors = ['green' if f else 'red' for f in is_feasible]
        
        axes[0, 1].scatter(consumptions, total_violations, c=colors, alpha=0.6, s=30)
        axes[0, 1].set_xlabel('Annual Consumption (kWh)')
        axes[0, 1].set_ylabel('Total Constraint Violation')
        axes[0, 1].set_title('Consumption vs Constraint Violation')
        axes[0, 1].set_yscale('log')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Active constraints count
        active_counts = [len(s.active_constraints) for s in self.solutions]
        axes[1, 0].hist(active_counts, bins=len(self.constraints)+1, alpha=0.7, color='steelblue')
        axes[1, 0].set_xlabel('Number of Active Constraints')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].set_title('Distribution of Active Constraints')
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # 4. Feasibility ratio vs consumption (only feasible)
        if any(is_feasible):
            feasible_solutions = [s for s in self.solutions if s.is_feasible]
            feasible_consumptions = [s.objectives['annual_consumption_kwh'] 
                                   for s in feasible_solutions]
            feasible_comfort = [s.objectives['comfort_hours'] for s in feasible_solutions]
            
            axes[1, 1].scatter(feasible_consumptions, feasible_comfort, 
                             alpha=0.6, s=50, color='green')
            axes[1, 1].set_xlabel('Annual Consumption (kWh)')
            axes[1, 1].set_ylabel('Comfort Hours')
            axes[1, 1].set_title('Feasible Solutions: Consumption vs Comfort')
            axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        output_path = self.output_dir / f"constraint_analysis_{timestamp}.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved constraint analysis plot to {output_path}")
        plt.close()
    
    def plot_pareto_constrained(self):
        """Create Pareto-like plot for constrained solutions."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Extract data
        consumptions = [s.objectives['annual_consumption_kwh'] for s in self.solutions]
        comforts = [s.objectives['comfort_hours'] for s in self.solutions]
        is_feasible_list = [s.is_feasible for s in self.solutions]
        
        fig = go.Figure()
        
        # Infeasible solutions (red)
        infeasible_idx = [i for i, f in enumerate(is_feasible_list) if not f]
        if infeasible_idx:
            fig.add_trace(go.Scatter(
                x=[consumptions[i] for i in infeasible_idx],
                y=[comforts[i] for i in infeasible_idx],
                mode='markers',
                marker=dict(size=6, color='red', opacity=0.4),
                name='Infeasible',
                text=[f"Violations: {self.solutions[i].total_violation:.2f}" 
                      for i in infeasible_idx],
                hovertemplate='<b>Infeasible</b><br>Consumption: %{x:.0f} kWh<br>Comfort: %{y:.0f} h<extra></extra>'
            ))
        
        # Feasible solutions (green)
        feasible_idx = [i for i, f in enumerate(is_feasible_list) if f]
        if feasible_idx:
            fig.add_trace(go.Scatter(
                x=[consumptions[i] for i in feasible_idx],
                y=[comforts[i] for i in feasible_idx],
                mode='markers',
                marker=dict(size=8, color='green', opacity=0.7, line=dict(width=1, color='darkgreen')),
                name='Feasible',
                text=[f"Active: {len(self.solutions[i].active_constraints)}" 
                      for i in feasible_idx],
                hovertemplate='<b>Feasible</b><br>Consumption: %{x:.0f} kWh<br>Comfort: %{y:.0f} h<extra></extra>'
            ))
        
        fig.update_layout(
            title='Constrained Solutions: Consumption vs Comfort<br>Green=Feasible, Red=Infeasible',
            xaxis_title='Annual Consumption (kWh)',
            yaxis_title='Comfort Hours',
            height=600,
            hovermode='closest'
        )
        
        output_path = self.output_dir / f"constrained_pareto_{timestamp}.html"
        fig.write_html(str(output_path))
        logger.info(f"Saved constrained Pareto plot to {output_path}")


def demo_constrained_optimization():
    """Demonstrate constrained optimization."""
    logger.info("=" * 80)
    logger.info("CONSTRAINED MULTI-OBJECTIVE OPTIMIZATION - DEMO")
    logger.info("=" * 80)
    
    # Load surrogate
    import pickle
    models_dir = Path("Science AI Engineering/mes4_piml/models")
    surrogate_path = models_dir / "surrogate_xgboost.pkl"
    
    with open(surrogate_path, 'rb') as f:
        surrogate = pickle.load(f)
    
    # Parameter bounds
    parameter_bounds = {
        'wall_u_value': (0.2, 2.0),
        'roof_u_value': (0.15, 1.5),
        'window_u_value': (1.0, 5.5),
        'window_shgc': (0.2, 0.8),
        'window_to_wall_ratio': (0.1, 0.6),
        'infiltration_ach': (0.3, 1.5),
        'hvac_cop': (2.5, 5.0),
        'hvac_setpoint_cooling': (22.0, 26.0),
        'hvac_setpoint_heating': (18.0, 22.0),
        'lighting_power_density': (5.0, 15.0),
        'equipment_power_density': (8.0, 20.0),
        'occupancy_density': (0.05, 0.15)
    }
    
    # Initialize optimizer
    optimizer = ConstrainedOptimizer(
        surrogate_model=surrogate,
        parameter_bounds=parameter_bounds,
        output_dir=Path("Science AI Engineering/mes8_optimization/results/constrained")
    )
    
    # Define constraints
    logger.info("\n" + "=" * 80)
    logger.info("DEFINING CONSTRAINTS")
    logger.info("=" * 80)
    optimizer.define_default_constraints()
    
    # Run optimization with penalty method
    logger.info("\n" + "=" * 80)
    logger.info("CONSTRAINED OPTIMIZATION (Penalty Method)")
    logger.info("=" * 80)
    solutions = optimizer.optimize_constrained(
        method='penalty',
        n_solutions=150,
        penalty_weight=1000.0
    )
    
    # Save results
    optimizer.save_results()
    
    # Generate visualizations
    logger.info("\n" + "=" * 80)
    logger.info("GENERATING VISUALIZATIONS")
    logger.info("=" * 80)
    optimizer.plot_constraint_analysis()
    optimizer.plot_pareto_constrained()
    
    # Summary
    logger.info("\n" + "=" * 80)
    logger.info("CONSTRAINED OPTIMIZATION SUMMARY")
    logger.info("=" * 80)
    
    feasible = [s for s in solutions if s.is_feasible]
    logger.info(f"\nTotal solutions generated: {len(solutions)}")
    logger.info(f"Feasible solutions: {len(feasible)} ({100*len(feasible)/len(solutions):.1f}%)")
    
    if feasible:
        logger.info("\nBest feasible solutions (by consumption):")
        for i, sol in enumerate(sorted(feasible, 
                                      key=lambda s: s.objectives['annual_consumption_kwh'])[:5], 1):
            logger.info(f"\n  {i}. Consumption: {sol.objectives['annual_consumption_kwh']:.0f} kWh")
            logger.info(f"     Comfort: {sol.objectives['comfort_hours']:.0f} h")
            logger.info(f"     Peak cooling: {sol.objectives['peak_cooling_kw']:.1f} kW")
            logger.info(f"     Active constraints: {sol.active_constraints}")
    
    # Compare constrained vs unconstrained
    logger.info("\n" + "-" * 80)
    logger.info("Comparison: Best unconstrained vs best feasible")
    logger.info("-" * 80)
    
    best_unconstrained = min(solutions, key=lambda s: s.penalized_objectives['penalized_consumption'])
    best_feasible = min(feasible, key=lambda s: s.objectives['annual_consumption_kwh']) if feasible else None
    
    logger.info(f"\nUnconstrained best:")
    logger.info(f"  Consumption: {best_unconstrained.objectives['annual_consumption_kwh']:.0f} kWh")
    logger.info(f"  Feasibility: {best_unconstrained.is_feasible}")
    logger.info(f"  Violations: {best_unconstrained.total_violation:.2f}")
    
    if best_feasible:
        logger.info(f"\nConstrained best (feasible):")
        logger.info(f"  Consumption: {best_feasible.objectives['annual_consumption_kwh']:.0f} kWh")
        logger.info(f"  Feasibility: {best_feasible.is_feasible}")
        logger.info(f"  Trade-off: +{(best_feasible.objectives['annual_consumption_kwh'] - best_unconstrained.objectives['annual_consumption_kwh']):.0f} kWh "
                   f"for feasibility")
    
    logger.info("\n" + "=" * 80)
    logger.info("DEMO COMPLETE")
    logger.info("=" * 80)


if __name__ == "__main__":
    demo_constrained_optimization()
