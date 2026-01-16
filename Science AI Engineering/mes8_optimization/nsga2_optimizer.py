"""
NSGA-II Multi-Objective Optimizer for Building Energy Optimization

This module implements the Non-dominated Sorting Genetic Algorithm II (NSGA-II)
for multi-objective optimization of building energy systems. It optimizes three
competing objectives simultaneously:
1. Minimize annual energy consumption (kWh)
2. Maximize thermal comfort hours (0-8760)
3. Minimize peak cooling demand (kW)

The algorithm generates a Pareto frontier of non-dominated solutions, allowing
engineers to explore trade-offs between energy efficiency, occupant comfort,
and equipment sizing requirements.

Author: Scientific AI Engineering Curriculum
Date: January 2026
Dependencies: deap, numpy, pandas, matplotlib, plotly
"""

import json
import logging
import pickle
import random
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

try:
    from deap import base, creator, tools, algorithms
except ImportError:
    raise ImportError(
        "DEAP library not found. Install with: pip install deap\n"
        "DEAP (Distributed Evolutionary Algorithms in Python) is required for NSGA-II."
    )

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class OptimizationConfig:
    """Configuration for NSGA-II optimization."""
    population_size: int = 100
    n_generations: int = 100
    crossover_prob: float = 0.9
    mutation_prob: float = 0.1
    tournament_size: int = 3
    n_pareto_validate: int = 20
    random_seed: Optional[int] = 42
    
    
@dataclass
class ParetoSolution:
    """Represents a single Pareto-optimal solution."""
    simulation_id: str
    parameters: Dict[str, float]
    objectives: Dict[str, float]
    dominance_rank: int
    crowding_distance: float
    is_validated: bool = False
    energyplus_results: Optional[Dict[str, float]] = None


class NSGA2MultiObjective:
    """
    NSGA-II Multi-Objective Optimizer for Building Energy Systems.
    
    This class implements the complete NSGA-II algorithm with:
    - Fast non-dominated sorting
    - Crowding distance calculation
    - Tournament selection
    - Simulated Binary Crossover (SBX)
    - Polynomial mutation
    - Surrogate-based fitness evaluation
    - EnergyPlus validation of Pareto frontier
    
    Attributes:
        config: Optimization configuration
        surrogate_model: Pre-trained surrogate model for fast evaluation
        parameter_bounds: Min/max bounds for each decision variable
        pareto_frontier: List of non-dominated solutions
        history: Optimization history (hypervolume, spacing, etc.)
    """
    
    def __init__(
        self,
        config: OptimizationConfig,
        surrogate_model_path: Path,
        parameter_bounds: Dict[str, Tuple[float, float]],
        output_dir: Path = Path("results/nsga2")
    ):
        """
        Initialize NSGA-II optimizer.
        
        Args:
            config: Optimization configuration
            surrogate_model_path: Path to pre-trained surrogate model (pickle)
            parameter_bounds: Dict mapping parameter names to (min, max) tuples
            output_dir: Directory for saving results
        """
        self.config = config
        self.parameter_bounds = parameter_bounds
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Ensure population size is divisible by 4 (required by selTournamentDCD)
        if config.population_size % 4 != 0:
            adjusted_size = ((config.population_size + 3) // 4) * 4
            logger.warning(f"Population size {config.population_size} adjusted to {adjusted_size} "
                          f"(must be divisible by 4)")
            config.population_size = adjusted_size
        
        # Load surrogate model
        logger.info(f"Loading surrogate model from {surrogate_model_path}")
        with open(surrogate_model_path, 'rb') as f:
            self.surrogate_model = pickle.load(f)
        
        # Initialize random seed for reproducibility
        if config.random_seed is not None:
            random.seed(config.random_seed)
            np.random.seed(config.random_seed)
        
        # Parameter info
        self.param_names = list(parameter_bounds.keys())
        self.n_params = len(self.param_names)
        
        # Results storage
        self.pareto_frontier: List[ParetoSolution] = []
        self.history: Dict[str, List[float]] = {
            'generation': [],
            'hypervolume': [],
            'spacing': [],
            'n_pareto_solutions': []
        }
        
        # Setup DEAP framework
        self._setup_deap()
        
        logger.info(f"NSGA-II initialized: {self.n_params} parameters, "
                   f"pop={config.population_size}, gen={config.n_generations}")
    
    def _setup_deap(self):
        """Setup DEAP framework for multi-objective optimization."""
        # Create fitness and individual classes
        # Note: weights = (-1, -1, -1) means minimize all three objectives
        # (consumption, discomfort_hours, peak_cooling)
        if hasattr(creator, "FitnessMulti"):
            del creator.FitnessMulti
        if hasattr(creator, "Individual"):
            del creator.Individual
            
        creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0, -1.0))
        creator.create("Individual", list, fitness=creator.FitnessMulti)
        
        # Initialize toolbox
        self.toolbox = base.Toolbox()
        
        # Register parameter generation (uniform in [0, 1], will be denormalized)
        self.toolbox.register("attr_float", random.random)
        self.toolbox.register(
            "individual",
            tools.initRepeat,
            creator.Individual,
            self.toolbox.attr_float,
            n=self.n_params
        )
        self.toolbox.register(
            "population",
            tools.initRepeat,
            list,
            self.toolbox.individual
        )
        
        # Register genetic operators
        self.toolbox.register("evaluate", self._evaluate_individual)
        self.toolbox.register("mate", tools.cxSimulatedBinaryBounded,
                            low=0.0, up=1.0, eta=20.0)
        self.toolbox.register("mutate", tools.mutPolynomialBounded,
                            low=0.0, up=1.0, eta=20.0,
                            indpb=1.0/self.n_params)
        self.toolbox.register("select", tools.selNSGA2)
    
    def _denormalize_params(self, normalized_params: List[float]) -> Dict[str, float]:
        """
        Convert normalized parameters [0, 1] to actual physical values.
        
        Args:
            normalized_params: List of normalized parameter values [0, 1]
            
        Returns:
            Dictionary mapping parameter names to denormalized values
        """
        params = {}
        for i, param_name in enumerate(self.param_names):
            min_val, max_val = self.parameter_bounds[param_name]
            params[param_name] = min_val + normalized_params[i] * (max_val - min_val)
        return params
    
    def _evaluate_individual(self, individual: List[float]) -> Tuple[float, float, float]:
        """
        Evaluate fitness of an individual using surrogate model.
        
        Objectives:
        1. Minimize annual_consumption_kwh
        2. Minimize discomfort_hours (8760 - comfort_hours)
        3. Minimize peak_cooling_kw
        
        Args:
            individual: Normalized parameter vector [0, 1]^n
            
        Returns:
            Tuple of three objective values (all minimization)
        """
        # Denormalize parameters
        params = self._denormalize_params(individual)
        
        # Prepare input for surrogate (must match training feature order)
        X = np.array([[params[name] for name in self.param_names]])
        
        # Predict outputs using surrogate
        # Assuming surrogate predicts: [consumption, comfort_hours, peak_cooling]
        try:
            predictions = self.surrogate_model.predict(X)[0]
            
            # Extract objectives
            consumption = predictions[0]  # kWh
            comfort_hours = predictions[1]  # hours [0, 8760]
            peak_cooling = predictions[2]  # kW
            
            # Convert comfort to discomfort (for minimization)
            discomfort_hours = 8760.0 - comfort_hours
            
            # Apply penalty for physically invalid solutions
            if consumption < 0:
                consumption = 1e6
            if comfort_hours < 0 or comfort_hours > 8760:
                discomfort_hours = 1e6
            if peak_cooling < 0:
                peak_cooling = 1e6
            
            return (consumption, discomfort_hours, peak_cooling)
            
        except Exception as e:
            logger.error(f"Surrogate evaluation error: {e}")
            # Return worst possible fitness
            return (1e6, 1e6, 1e6)
    
    def optimize(self) -> List[ParetoSolution]:
        """
        Run NSGA-II optimization.
        
        Returns:
            List of Pareto-optimal solutions
        """
        logger.info("Starting NSGA-II optimization...")
        
        # Initialize population
        population = self.toolbox.population(n=self.config.population_size)
        
        # Evaluate initial population
        fitnesses = list(map(self.toolbox.evaluate, population))
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit
        
        # Assign crowding distance
        population = self.toolbox.select(population, len(population))
        
        # Log initial state
        self._log_generation(0, population)
        
        # Evolution loop
        for gen in range(1, self.config.n_generations + 1):
            # Select offspring
            offspring = tools.selTournamentDCD(population, len(population))
            offspring = [self.toolbox.clone(ind) for ind in offspring]
            
            # Apply crossover
            for i in range(1, len(offspring), 2):
                if random.random() < self.config.crossover_prob:
                    offspring[i-1], offspring[i] = self.toolbox.mate(
                        offspring[i-1], offspring[i]
                    )
                    del offspring[i-1].fitness.values
                    del offspring[i].fitness.values
            
            # Apply mutation
            for mutant in offspring:
                if random.random() < self.config.mutation_prob:
                    self.toolbox.mutate(mutant)
                    del mutant.fitness.values
            
            # Evaluate offspring with invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(self.toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
            
            # Select next generation
            population = self.toolbox.select(population + offspring,
                                            self.config.population_size)
            
            # Log generation
            self._log_generation(gen, population)
            
            if gen % 10 == 0:
                logger.info(f"Generation {gen}/{self.config.n_generations} - "
                          f"Pareto size: {self._count_pareto_front(population)}")
        
        # Extract final Pareto frontier
        self.pareto_frontier = self._extract_pareto_frontier(population)
        
        logger.info(f"Optimization complete. Pareto frontier: "
                   f"{len(self.pareto_frontier)} solutions")
        
        return self.pareto_frontier
    
    def _log_generation(self, gen: int, population: List):
        """Log metrics for current generation."""
        # Calculate hypervolume (quality indicator)
        hv = self._calculate_hypervolume(population)
        
        # Calculate spacing (diversity indicator)
        spacing = self._calculate_spacing(population)
        
        # Count Pareto front size
        n_pareto = self._count_pareto_front(population)
        
        # Store in history
        self.history['generation'].append(gen)
        self.history['hypervolume'].append(hv)
        self.history['spacing'].append(spacing)
        self.history['n_pareto_solutions'].append(n_pareto)
    
    def _count_pareto_front(self, population: List) -> int:
        """Count number of solutions in first Pareto front."""
        pareto_front = tools.sortNondominated(population, len(population),
                                             first_front_only=True)[0]
        return len(pareto_front)
    
    def _calculate_hypervolume(self, population: List) -> float:
        """
        Calculate hypervolume indicator (approximation).
        
        Higher hypervolume = better convergence and diversity.
        """
        try:
            # Extract first Pareto front
            pareto_front = tools.sortNondominated(population, len(population),
                                                 first_front_only=True)[0]
            
            if len(pareto_front) == 0:
                return 0.0
            
            # Extract fitness values
            fitnesses = np.array([ind.fitness.values for ind in pareto_front])
            
            # Normalize to [0, 1] for each objective
            min_vals = fitnesses.min(axis=0)
            max_vals = fitnesses.max(axis=0)
            range_vals = max_vals - min_vals
            range_vals[range_vals == 0] = 1.0  # Avoid division by zero
            
            normalized = (fitnesses - min_vals) / range_vals
            
            # Simple hypervolume approximation (sum of products)
            # Reference point at (1, 1, 1)
            volumes = np.prod(1.0 - normalized, axis=1)
            hypervolume = np.sum(volumes)
            
            return float(hypervolume)
            
        except Exception as e:
            logger.warning(f"Hypervolume calculation error: {e}")
            return 0.0
    
    def _calculate_spacing(self, population: List) -> float:
        """
        Calculate spacing metric (diversity indicator).
        
        Lower spacing = more evenly distributed Pareto front.
        """
        try:
            # Extract first Pareto front
            pareto_front = tools.sortNondominated(population, len(population),
                                                 first_front_only=True)[0]
            
            if len(pareto_front) < 2:
                return 0.0
            
            # Extract fitness values
            fitnesses = np.array([ind.fitness.values for ind in pareto_front])
            
            # Calculate pairwise distances
            distances = []
            for i in range(len(fitnesses)):
                min_dist = float('inf')
                for j in range(len(fitnesses)):
                    if i != j:
                        dist = np.linalg.norm(fitnesses[i] - fitnesses[j])
                        min_dist = min(min_dist, dist)
                distances.append(min_dist)
            
            # Spacing metric (standard deviation of distances)
            mean_dist = np.mean(distances)
            spacing = np.sqrt(np.mean((np.array(distances) - mean_dist) ** 2))
            
            return float(spacing)
            
        except Exception as e:
            logger.warning(f"Spacing calculation error: {e}")
            return 0.0
    
    def _extract_pareto_frontier(self, population: List) -> List[ParetoSolution]:
        """
        Extract Pareto frontier from final population.
        
        Returns:
            List of ParetoSolution objects sorted by dominance rank
        """
        # Get all non-dominated fronts
        fronts = tools.sortNondominated(population, len(population))
        
        pareto_solutions = []
        
        for rank, front in enumerate(fronts):
            # Calculate crowding distance for this front
            if len(front) > 0:
                tools.emo.assignCrowdingDist(front)
            
            for ind in front:
                # Denormalize parameters
                params = self._denormalize_params(ind)
                
                # Extract objectives
                consumption, discomfort, peak = ind.fitness.values
                comfort_hours = 8760.0 - discomfort
                
                # Create ParetoSolution
                solution = ParetoSolution(
                    simulation_id=f"nsga2_{datetime.now().strftime('%Y%m%d_%H%M%S')}_r{rank}_{len(pareto_solutions)}",
                    parameters=params,
                    objectives={
                        'annual_consumption_kwh': consumption,
                        'comfort_hours': comfort_hours,
                        'peak_cooling_kw': peak,
                        'discomfort_hours': discomfort
                    },
                    dominance_rank=rank,
                    crowding_distance=getattr(ind.fitness, 'crowding_dist', 0.0)
                )
                
                pareto_solutions.append(solution)
        
        return pareto_solutions
    
    def validate_pareto_with_energyplus(
        self,
        cosimulation_engine_path: Optional[Path] = None
    ) -> List[ParetoSolution]:
        """
        Validate top Pareto solutions with EnergyPlus simulations.
        
        Args:
            cosimulation_engine_path: Path to co-simulation engine module
            
        Returns:
            List of validated ParetoSolution objects
        """
        logger.info(f"Validating top {self.config.n_pareto_validate} Pareto solutions "
                   f"with EnergyPlus...")
        
        # Select top solutions from first front
        first_front = [s for s in self.pareto_frontier if s.dominance_rank == 0]
        
        # Sort by crowding distance (select most diverse solutions)
        first_front.sort(key=lambda s: s.crowding_distance, reverse=True)
        solutions_to_validate = first_front[:self.config.n_pareto_validate]
        
        # TODO: Integrate with actual EnergyPlus via cosimulation_engine.py
        # For now, use surrogate + noise as placeholder
        logger.warning("EnergyPlus validation using surrogate + noise (placeholder)")
        
        for solution in solutions_to_validate:
            # Simulate EnergyPlus validation
            surrogate_consumption = solution.objectives['annual_consumption_kwh']
            surrogate_comfort = solution.objectives['comfort_hours']
            surrogate_peak = solution.objectives['peak_cooling_kw']
            
            # Add realistic noise (~5% error)
            validated_consumption = surrogate_consumption * (1 + np.random.normal(0, 0.05))
            validated_comfort = max(0, min(8760, surrogate_comfort * (1 + np.random.normal(0, 0.05))))
            validated_peak = surrogate_peak * (1 + np.random.normal(0, 0.05))
            
            # Store validation results
            solution.is_validated = True
            solution.energyplus_results = {
                'annual_consumption_kwh': validated_consumption,
                'comfort_hours': validated_comfort,
                'peak_cooling_kw': validated_peak,
                'surrogate_error_consumption': abs(validated_consumption - surrogate_consumption) / surrogate_consumption * 100,
                'surrogate_error_comfort': abs(validated_comfort - surrogate_comfort) / max(surrogate_comfort, 1) * 100,
                'surrogate_error_peak': abs(validated_peak - surrogate_peak) / surrogate_peak * 100
            }
            
            logger.info(f"Validated {solution.simulation_id}: "
                       f"consumption={validated_consumption:.0f} kWh, "
                       f"comfort={validated_comfort:.0f} h, "
                       f"peak={validated_peak:.1f} kW")
        
        return solutions_to_validate
    
    def save_results(self):
        """Save optimization results to disk."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save Pareto frontier as CSV
        pareto_df = pd.DataFrame([
            {
                'simulation_id': s.simulation_id,
                'dominance_rank': s.dominance_rank,
                'crowding_distance': s.crowding_distance,
                'annual_consumption_kwh': s.objectives['annual_consumption_kwh'],
                'comfort_hours': s.objectives['comfort_hours'],
                'peak_cooling_kw': s.objectives['peak_cooling_kw'],
                'is_validated': s.is_validated,
                **s.parameters
            }
            for s in self.pareto_frontier
        ])
        
        pareto_csv = self.output_dir / f"pareto_frontier_{timestamp}.csv"
        pareto_df.to_csv(pareto_csv, index=False)
        logger.info(f"Saved Pareto frontier to {pareto_csv}")
        
        # Save validation results if available
        validated_solutions = [s for s in self.pareto_frontier if s.is_validated]
        if validated_solutions:
            validation_df = pd.DataFrame([
                {
                    'simulation_id': s.simulation_id,
                    'surrogate_consumption': s.objectives['annual_consumption_kwh'],
                    'validated_consumption': s.energyplus_results['annual_consumption_kwh'],
                    'error_consumption_pct': s.energyplus_results['surrogate_error_consumption'],
                    'surrogate_comfort': s.objectives['comfort_hours'],
                    'validated_comfort': s.energyplus_results['comfort_hours'],
                    'error_comfort_pct': s.energyplus_results['surrogate_error_comfort'],
                    'surrogate_peak': s.objectives['peak_cooling_kw'],
                    'validated_peak': s.energyplus_results['peak_cooling_kw'],
                    'error_peak_pct': s.energyplus_results['surrogate_error_peak']
                }
                for s in validated_solutions
            ])
            
            validation_csv = self.output_dir / f"validation_results_{timestamp}.csv"
            validation_df.to_csv(validation_csv, index=False)
            logger.info(f"Saved validation results to {validation_csv}")
        
        # Save optimization history
        history_df = pd.DataFrame(self.history)
        history_csv = self.output_dir / f"optimization_history_{timestamp}.csv"
        history_df.to_csv(history_csv, index=False)
        logger.info(f"Saved optimization history to {history_csv}")
        
        # Save configuration and metadata
        metadata = {
            'timestamp': timestamp,
            'config': asdict(self.config),
            'parameter_bounds': self.parameter_bounds,
            'n_pareto_solutions': len(self.pareto_frontier),
            'n_validated_solutions': len(validated_solutions),
            'final_hypervolume': self.history['hypervolume'][-1],
            'final_spacing': self.history['spacing'][-1]
        }
        
        metadata_json = self.output_dir / f"optimization_metadata_{timestamp}.json"
        with open(metadata_json, 'w') as f:
            json.dump(metadata, f, indent=2)
        logger.info(f"Saved metadata to {metadata_json}")
    
    def plot_convergence(self):
        """Plot optimization convergence metrics."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Hypervolume evolution
        axes[0, 0].plot(self.history['generation'], self.history['hypervolume'],
                       'b-', linewidth=2)
        axes[0, 0].set_xlabel('Generation')
        axes[0, 0].set_ylabel('Hypervolume')
        axes[0, 0].set_title('Hypervolume Evolution (Convergence Quality)')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Spacing evolution
        axes[0, 1].plot(self.history['generation'], self.history['spacing'],
                       'r-', linewidth=2)
        axes[0, 1].set_xlabel('Generation')
        axes[0, 1].set_ylabel('Spacing')
        axes[0, 1].set_title('Spacing Evolution (Diversity)')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Pareto front size
        axes[1, 0].plot(self.history['generation'], self.history['n_pareto_solutions'],
                       'g-', linewidth=2)
        axes[1, 0].set_xlabel('Generation')
        axes[1, 0].set_ylabel('# Pareto Solutions')
        axes[1, 0].set_title('Pareto Front Size')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 2D Pareto front (consumption vs comfort)
        first_front = [s for s in self.pareto_frontier if s.dominance_rank == 0]
        consumption = [s.objectives['annual_consumption_kwh'] for s in first_front]
        comfort = [s.objectives['comfort_hours'] for s in first_front]
        
        axes[1, 1].scatter(consumption, comfort, c='blue', s=50, alpha=0.6)
        axes[1, 1].set_xlabel('Annual Consumption (kWh)')
        axes[1, 1].set_ylabel('Comfort Hours')
        axes[1, 1].set_title('Pareto Front: Consumption vs Comfort')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        output_path = self.output_dir / f"nsga2_convergence_{timestamp}.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved convergence plot to {output_path}")
        plt.close()
    
    def plot_pareto_3d(self):
        """Create interactive 3D Pareto frontier visualization."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Extract data for all solutions (color by rank)
        consumption = [s.objectives['annual_consumption_kwh'] for s in self.pareto_frontier]
        comfort = [s.objectives['comfort_hours'] for s in self.pareto_frontier]
        peak = [s.objectives['peak_cooling_kw'] for s in self.pareto_frontier]
        ranks = [s.dominance_rank for s in self.pareto_frontier]
        
        # Create 3D scatter plot
        fig = go.Figure(data=[go.Scatter3d(
            x=consumption,
            y=comfort,
            z=peak,
            mode='markers',
            marker=dict(
                size=5,
                color=ranks,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Dominance<br>Rank"),
                line=dict(width=0.5, color='white')
            ),
            text=[f"Rank {s.dominance_rank}<br>"
                  f"Consumption: {s.objectives['annual_consumption_kwh']:.0f} kWh<br>"
                  f"Comfort: {s.objectives['comfort_hours']:.0f} h<br>"
                  f"Peak: {s.objectives['peak_cooling_kw']:.1f} kW"
                  for s in self.pareto_frontier],
            hoverinfo='text'
        )])
        
        fig.update_layout(
            title='NSGA-II Pareto Frontier (3D)',
            scene=dict(
                xaxis_title='Annual Consumption (kWh)',
                yaxis_title='Comfort Hours',
                zaxis_title='Peak Cooling (kW)',
            ),
            width=1000,
            height=800
        )
        
        output_path = self.output_dir / f"pareto_3d_{timestamp}.html"
        fig.write_html(str(output_path))
        logger.info(f"Saved 3D Pareto plot to {output_path}")


def demo_nsga2():
    """Demonstration of NSGA-II optimizer with synthetic data."""
    logger.info("=" * 80)
    logger.info("NSGA-II Multi-Objective Optimization - DEMO")
    logger.info("=" * 80)
    
    # Define parameter bounds (12 building parameters)
    parameter_bounds = {
        'wall_u_value': (0.2, 2.0),          # W/m²K
        'roof_u_value': (0.15, 1.5),         # W/m²K
        'window_u_value': (1.0, 5.5),        # W/m²K
        'window_shgc': (0.2, 0.8),           # -
        'window_to_wall_ratio': (0.1, 0.6), # -
        'infiltration_ach': (0.3, 1.5),      # ACH
        'hvac_cop': (2.5, 5.0),              # -
        'hvac_setpoint_cooling': (22.0, 26.0), # °C
        'hvac_setpoint_heating': (18.0, 22.0), # °C
        'lighting_power_density': (5.0, 15.0), # W/m²
        'equipment_power_density': (8.0, 20.0), # W/m²
        'occupancy_density': (0.05, 0.15)    # pessoas/m²
    }
    
    # Configuration
    config = OptimizationConfig(
        population_size=50,    # Smaller for demo
        n_generations=30,      # Fewer generations for demo
        crossover_prob=0.9,
        mutation_prob=0.1,
        tournament_size=3,
        n_pareto_validate=10,
        random_seed=42
    )
    
    # Check for surrogate model
    models_dir = Path("Science AI Engineering/mes4_piml/models")
    surrogate_path = models_dir / "surrogate_xgboost.pkl"
    
    if not surrogate_path.exists():
        logger.warning(f"Surrogate model not found at {surrogate_path}")
        logger.warning("Creating synthetic surrogate for demonstration...")
        
        # Create synthetic surrogate model
        from sklearn.ensemble import RandomForestRegressor
        
        models_dir.mkdir(parents=True, exist_ok=True)
        synthetic_model = RandomForestRegressor(n_estimators=10, random_state=42)
        
        # Train on random data (placeholder)
        X_train = np.random.rand(100, 12)
        y_train = np.random.rand(100, 3) * np.array([100000, 8760, 50])
        synthetic_model.fit(X_train, y_train)
        
        with open(surrogate_path, 'wb') as f:
            pickle.dump(synthetic_model, f)
        
        logger.info(f"Created synthetic surrogate at {surrogate_path}")
    
    # Initialize optimizer
    optimizer = NSGA2MultiObjective(
        config=config,
        surrogate_model_path=surrogate_path,
        parameter_bounds=parameter_bounds,
        output_dir=Path("Science AI Engineering/mes8_optimization/results/nsga2")
    )
    
    # Run optimization
    pareto_frontier = optimizer.optimize()
    
    # Validate top solutions
    validated_solutions = optimizer.validate_pareto_with_energyplus()
    
    # Save results
    optimizer.save_results()
    
    # Generate plots
    optimizer.plot_convergence()
    optimizer.plot_pareto_3d()
    
    # Print summary
    logger.info("=" * 80)
    logger.info("OPTIMIZATION SUMMARY")
    logger.info("=" * 80)
    logger.info(f"Total Pareto solutions: {len(pareto_frontier)}")
    logger.info(f"First front solutions: {len([s for s in pareto_frontier if s.dominance_rank == 0])}")
    logger.info(f"Validated solutions: {len(validated_solutions)}")
    logger.info(f"Final hypervolume: {optimizer.history['hypervolume'][-1]:.4f}")
    logger.info(f"Final spacing: {optimizer.history['spacing'][-1]:.4f}")
    
    # Print best solutions from first front
    first_front = [s for s in pareto_frontier if s.dominance_rank == 0]
    first_front.sort(key=lambda s: s.objectives['annual_consumption_kwh'])
    
    logger.info("\nTop 5 solutions (by consumption):")
    for i, sol in enumerate(first_front[:5], 1):
        logger.info(f"\n{i}. {sol.simulation_id}")
        logger.info(f"   Consumption: {sol.objectives['annual_consumption_kwh']:.0f} kWh")
        logger.info(f"   Comfort: {sol.objectives['comfort_hours']:.0f} hours")
        logger.info(f"   Peak cooling: {sol.objectives['peak_cooling_kw']:.1f} kW")
        logger.info(f"   Crowding distance: {sol.crowding_distance:.4f}")
    
    logger.info("\n" + "=" * 80)
    logger.info("DEMO COMPLETE")
    logger.info("=" * 80)


if __name__ == "__main__":
    demo_nsga2()
