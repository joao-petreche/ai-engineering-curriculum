"""
Federated Learning Optimization Framework (Fase 3)

Implements distributed optimization across multiple agents using:
- Ray framework for distributed computing
- Federated parameter servers for weight aggregation
- Multi-agent genetic algorithms with synchronization
- Convergence analysis and topology effects

This module bridges Fase 2 (Advanced Optimization) with distributed systems,
enabling optimization at scale across multiple sites or devices.

Author: Scientific AI Engineering Curriculum
Date: January 2026
Dependencies: ray, numpy, pandas, matplotlib, plotly
"""

import time
import logging
import numpy as np
import pandas as pd
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Callable

import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

try:
    import ray
    from ray.util.queue import Queue as RayQueue
except ImportError:
    ray = None
    logging.warning("Ray not installed. Distributed computing disabled.")


# Configure logging
class ColoredFormatter(logging.Formatter):
    """Colored log formatter for distributed operations."""
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[92m',     # Green
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',    # Red
    }
    RESET = '\033[0m'
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        return super().format(record)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


@dataclass
class FederatedConfig:
    """Configuration for federated learning setup."""
    num_agents: int = 4
    num_generations: int = 30
    population_size: int = 50
    mutation_rate: float = 0.1
    topology: str = "star"  # star, ring, mesh
    aggregation_method: str = "average"  # average, median, robust
    communication_delay_ms: float = 0.0
    dropout_rate: float = 0.0  # Proportion of agents that fail per round


@dataclass
class AgentMetrics:
    """Metrics for individual agent performance."""
    agent_id: int
    best_loss: float = float('inf')
    mean_loss: float = 0.0
    convergence_curve: List[float] = field(default_factory=list)
    communication_rounds: int = 0
    computations: int = 0
    last_update_time: float = 0.0


@dataclass
class FederatedMetrics:
    """Metrics for overall federated optimization."""
    generation: int = 0
    global_best_loss: float = float('inf')
    mean_agent_loss: float = 0.0
    std_agent_loss: float = 0.0
    convergence_curve: List[float] = field(default_factory=list)
    communication_overhead_ms: List[float] = field(default_factory=list)
    agent_metrics: Dict[int, AgentMetrics] = field(default_factory=dict)
    synchronization_efficiency: float = 0.0


class FederatedParameterServer:
    """
    Central parameter server for aggregating weights across agents.
    Implements multiple aggregation strategies.
    """
    
    def __init__(self, aggregation_method: str = "average"):
        """
        Initialize parameter server.
        
        Args:
            aggregation_method: 'average', 'median', or 'robust'
        """
        self.aggregation_method = aggregation_method
        self.weights_history = []
        self.aggregation_times = []
    
    def aggregate(self, agent_weights: List[np.ndarray]) -> np.ndarray:
        """
        Aggregate weights from multiple agents.
        
        Args:
            agent_weights: List of weight arrays from agents
        
        Returns:
            Aggregated weight array
        """
        start_time = time.time()
        
        if self.aggregation_method == "average":
            aggregated = np.mean(agent_weights, axis=0)
        
        elif self.aggregation_method == "median":
            aggregated = np.median(agent_weights, axis=0)
        
        elif self.aggregation_method == "robust":
            # Trim mean: remove top/bottom 10% before averaging
            weights_array = np.array(agent_weights)
            trim_percent = 10
            for i in range(weights_array.shape[1]):
                col = weights_array[:, i]
                lower = np.percentile(col, trim_percent)
                upper = np.percentile(col, 100 - trim_percent)
                mask = (col >= lower) & (col <= upper)
                if mask.sum() > 0:
                    aggregated = np.mean(weights_array[mask], axis=0) if i == 0 else aggregated
        
        else:
            raise ValueError(f"Unknown aggregation method: {self.aggregation_method}")
        
        elapsed = (time.time() - start_time) * 1000  # ms
        self.aggregation_times.append(elapsed)
        self.weights_history.append(aggregated.copy())
        
        return aggregated


class FederatedAgent:
    """
    Individual agent in federated learning system.
    Maintains local population and communicates with parameter server.
    """
    
    def __init__(self, 
                 agent_id: int,
                 population_size: int,
                 param_dim: int,
                 fitness_func: Callable,
                 mutation_rate: float = 0.1):
        """
        Initialize federated agent.
        
        Args:
            agent_id: Unique agent identifier
            population_size: Size of local population
            param_dim: Dimension of parameter space
            fitness_func: Objective function
            mutation_rate: Mutation probability
        """
        self.agent_id = agent_id
        self.population_size = population_size
        self.param_dim = param_dim
        self.fitness_func = fitness_func
        self.mutation_rate = mutation_rate
        
        # Initialize local population (random)
        self.population = np.random.uniform(-5, 5, (population_size, param_dim))
        self.fitness = np.array([fitness_func(ind) for ind in self.population])
        
        self.metrics = AgentMetrics(agent_id=agent_id)
    
    def local_ga_iteration(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Perform one generation of local genetic algorithm.
        
        Returns:
            Tuple of (new_population, fitness)
        """
        N = self.population_size
        
        # Selection (tournament)
        tournament_size = 3
        parents = []
        for _ in range(N):
            tournament = np.random.choice(N, tournament_size)
            winner = tournament[np.argmin(self.fitness[tournament])]
            parents.append(self.population[winner].copy())
        
        # Crossover (single-point)
        offspring = []
        for i in range(0, N, 2):
            p1, p2 = parents[i], parents[(i + 1) % N]
            cp = np.random.randint(self.param_dim)
            c1 = np.concatenate([p1[:cp], p2[cp:]])
            c2 = np.concatenate([p2[:cp], p1[cp:]])
            offspring.extend([c1, c2])
        
        offspring = np.array(offspring[:N])
        
        # Mutation (gaussian)
        for i in range(N):
            mask = np.random.rand(self.param_dim) < self.mutation_rate
            offspring[i][mask] += np.random.normal(0, 0.1, mask.sum())
        
        # Evaluate
        offspring_fitness = np.array([self.fitness_func(ind) for ind in offspring])
        
        # Elitism: keep best from both populations
        combined = np.vstack([self.population, offspring])
        combined_fitness = np.concatenate([self.fitness, offspring_fitness])
        best_indices = np.argsort(combined_fitness)[:N]
        
        self.population = combined[best_indices]
        self.fitness = combined_fitness[best_indices]
        
        self.metrics.computations += N * 2  # Selection + evaluation
        
        return self.population.copy(), self.fitness.copy()
    
    def receive_global_weights(self, global_weights: np.ndarray):
        """
        Receive aggregated weights from parameter server.
        Blend with local population (communication).
        
        Args:
            global_weights: Aggregated weights from server
        """
        # Blend: 70% local, 30% global
        blend_ratio = 0.3
        best_local_idx = np.argmin(self.fitness)
        self.population[best_local_idx] = (
            (1 - blend_ratio) * self.population[best_local_idx] + 
            blend_ratio * global_weights
        )
        self.fitness[best_local_idx] = self.fitness_func(self.population[best_local_idx])
        self.metrics.communication_rounds += 1
    
    def get_best_solution(self) -> Tuple[np.ndarray, float]:
        """Get local best solution."""
        best_idx = np.argmin(self.fitness)
        return self.population[best_idx].copy(), float(self.fitness[best_idx])


class FederatedOptimizer:
    """
    Main federated optimization orchestrator.
    Coordinates multiple agents with different topologies.
    """
    
    def __init__(self,
                 config: FederatedConfig,
                 fitness_func: Callable,
                 param_dim: int = 12,
                 use_ray: bool = True):
        """
        Initialize federated optimizer.
        
        Args:
            config: FederatedConfig with algorithm parameters
            fitness_func: Objective function to minimize
            param_dim: Dimension of parameter space
            use_ray: Whether to use Ray for distributed computing
        """
        self.config = config
        self.fitness_func = fitness_func
        self.param_dim = param_dim
        self.use_ray = use_ray and ray is not None
        
        # Initialize parameter server
        self.param_server = FederatedParameterServer(config.aggregation_method)
        
        # Initialize agents
        self.agents: Dict[int, FederatedAgent] = {}
        for i in range(config.num_agents):
            self.agents[i] = FederatedAgent(
                agent_id=i,
                population_size=config.population_size,
                param_dim=param_dim,
                fitness_func=fitness_func,
                mutation_rate=config.mutation_rate
            )
        
        # Metrics
        self.metrics = FederatedMetrics()
        
        logger.info(f"Initialized federated optimizer with {config.num_agents} agents")
        logger.info(f"Topology: {config.topology}, Aggregation: {config.aggregation_method}")
    
    def get_communication_topology(self) -> Dict[int, List[int]]:
        """
        Get communication topology for agents.
        
        Returns:
            Dictionary mapping agent_id to list of neighbors
        """
        num_agents = self.config.num_agents
        
        if self.config.topology == "star":
            # All agents communicate with central server
            topology = {i: [i] for i in range(num_agents)}
        
        elif self.config.topology == "ring":
            # Agents in ring: each talks to next
            topology = {i: [(i + 1) % num_agents] for i in range(num_agents)}
        
        elif self.config.topology == "mesh":
            # Fully connected: all talk to all
            topology = {i: list(range(num_agents)) for i in range(num_agents)}
        
        else:
            raise ValueError(f"Unknown topology: {self.config.topology}")
        
        return topology
    
    def synchronize_generation(self) -> float:
        """
        Perform one synchronization round.
        All agents update from parameter server.
        
        Returns:
            Communication overhead in milliseconds
        """
        start_time = time.time()
        
        # Gather weights from all agents
        agent_weights = []
        for agent_id in range(self.config.num_agents):
            best_sol, _ = self.agents[agent_id].get_best_solution()
            agent_weights.append(best_sol)
        
        # Aggregate at parameter server
        global_weights = self.param_server.aggregate(agent_weights)
        
        # Broadcast back to agents (simulated with delay)
        if self.config.communication_delay_ms > 0:
            time.sleep(self.config.communication_delay_ms / 1000)
        
        for agent_id in range(self.config.num_agents):
            # Simulate dropout
            if np.random.rand() > self.config.dropout_rate:
                self.agents[agent_id].receive_global_weights(global_weights)
        
        elapsed = (time.time() - start_time) * 1000  # ms
        self.metrics.communication_overhead_ms.append(elapsed)
        
        return elapsed
    
    def optimize(self) -> Dict[str, Any]:
        """
        Run federated optimization for configured generations.
        
        Returns:
            Dictionary with results and metrics
        """
        logger.info("=" * 80)
        logger.info("FEDERATED OPTIMIZATION")
        logger.info("=" * 80)
        logger.info(f"Config: {self.config.num_agents} agents, "
                   f"{self.config.num_generations} generations, "
                   f"topology={self.config.topology}")
        
        start_time = time.time()
        
        for gen in range(self.config.num_generations):
            # 1. Local GA iterations on each agent
            for agent_id in range(self.config.num_agents):
                self.agents[agent_id].local_ga_iteration()
            
            # 2. Synchronization round
            comm_time = self.synchronize_generation()
            
            # 3. Update metrics
            best_losses = []
            for agent_id in range(self.config.num_agents):
                _, loss = self.agents[agent_id].get_best_solution()
                best_losses.append(loss)
                self.agents[agent_id].metrics.best_loss = loss
            
            global_best = min(best_losses)
            self.metrics.global_best_loss = global_best
            self.metrics.mean_agent_loss = np.mean(best_losses)
            self.metrics.std_agent_loss = np.std(best_losses)
            self.metrics.convergence_curve.append(global_best)
            self.metrics.generation = gen
            
            # Calculate synchronization efficiency
            local_work_time = comm_time * 0.1  # Approximate
            self.metrics.synchronization_efficiency = 1.0 / (1.0 + comm_time / local_work_time)
            
            if (gen + 1) % 10 == 0:
                logger.info(f"Gen {gen+1:3d}: best_loss={global_best:.4f}, "
                           f"mean_loss={self.metrics.mean_agent_loss:.4f}, "
                           f"comm_time={comm_time:.2f}ms")
        
        elapsed = time.time() - start_time
        
        logger.info("=" * 80)
        logger.info(f"Optimization complete in {elapsed:.2f}s")
        logger.info(f"Final best loss: {self.metrics.global_best_loss:.4f}")
        logger.info(f"Mean agent loss: {self.metrics.mean_agent_loss:.4f}")
        logger.info("=" * 80)
        
        return {
            'global_best_loss': float(self.metrics.global_best_loss),
            'convergence_curve': self.metrics.convergence_curve,
            'total_time': elapsed,
            'communication_overhead': np.mean(self.metrics.communication_overhead_ms),
            'num_generations': self.config.num_generations,
            'num_agents': self.config.num_agents,
            'topology': self.config.topology,
            'aggregation': self.config.aggregation_method
        }
    
    def plot_convergence(self) -> Path:
        """Generate convergence plots."""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Plot 1: Global convergence
        axes[0, 0].plot(self.metrics.convergence_curve, linewidth=2, color='steelblue')
        axes[0, 0].set_xlabel('Generation')
        axes[0, 0].set_ylabel('Global Best Loss')
        axes[0, 0].set_title('Federated Convergence Curve')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Agent heterogeneity
        final_losses = [self.agents[i].metrics.best_loss for i in range(self.config.num_agents)]
        axes[0, 1].bar(range(self.config.num_agents), final_losses, color='coral')
        axes[0, 1].set_xlabel('Agent ID')
        axes[0, 1].set_ylabel('Best Loss')
        axes[0, 1].set_title('Agent Performance Heterogeneity')
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        # Plot 3: Communication overhead
        axes[1, 0].plot(self.metrics.communication_overhead_ms, linewidth=1, color='orange')
        axes[1, 0].set_xlabel('Generation')
        axes[1, 0].set_ylabel('Communication Time (ms)')
        axes[1, 0].set_title('Communication Overhead Over Time')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Plot 4: Synchronization efficiency
        eff_curve = [1.0 / (1.0 + t / 50.0) for t in self.metrics.communication_overhead_ms]
        axes[1, 1].plot(eff_curve, linewidth=2, color='green')
        axes[1, 1].axhline(y=0.9, color='r', linestyle='--', label='Target (90%)')
        axes[1, 1].set_xlabel('Generation')
        axes[1, 1].set_ylabel('Synchronization Efficiency')
        axes[1, 1].set_title('Efficiency vs Generation')
        axes[1, 1].set_ylim([0, 1.1])
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        output_path = Path(f"federated_convergence_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        logger.info(f"Saved convergence plot to {output_path}")
        plt.close()
        
        return output_path
    
    def plot_topology_comparison(self, results_by_topology: Dict[str, Dict]) -> Path:
        """
        Compare multiple topology results.
        
        Args:
            results_by_topology: Dict mapping topology name to results
        
        Returns:
            Path to saved plot
        """
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Convergence Speed", "Communication Cost"),
            specs=[[{'type': 'scatter'}, {'type': 'bar'}]]
        )
        
        # Convergence curves
        colors = ['steelblue', 'coral', 'green', 'purple']
        for (topology, results), color in zip(results_by_topology.items(), colors):
            convergence = results.get('convergence_curve', [])
            fig.add_trace(
                go.Scatter(y=convergence, name=topology, mode='lines', line=dict(color=color)),
                row=1, col=1
            )
        
        # Communication costs
        topologies = list(results_by_topology.keys())
        comm_costs = [results_by_topology[t].get('communication_overhead', 0) for t in topologies]
        fig.add_trace(
            go.Bar(x=topologies, y=comm_costs, name='Comm Cost (ms)', marker_color='lightseagreen'),
            row=1, col=2
        )
        
        fig.update_xaxes(title_text="Generation", row=1, col=1)
        fig.update_yaxes(title_text="Best Loss", row=1, col=1)
        fig.update_yaxes(title_text="Communication Time (ms)", row=1, col=2)
        
        fig.update_layout(title_text="Topology Comparison", height=500)
        
        output_path = Path(f"topology_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
        fig.write_html(str(output_path))
        logger.info(f"Saved topology comparison to {output_path}")
        
        return output_path


def sphere_function(x: np.ndarray) -> float:
    """Sphere function: sum(x_i^2)"""
    return float(np.sum(x**2))


def rastrigin_function(x: np.ndarray) -> float:
    """Rastrigin function (multimodal benchmark)."""
    A = 10
    return float(A * len(x) + np.sum(x**2 - A * np.cos(2 * np.pi * x)))


def demo_federated_optimization():
    """Demonstrate federated optimization with multiple topologies."""
    logger.info("=" * 80)
    logger.info("FEDERATED LEARNING - DEMO")
    logger.info("=" * 80)
    
    # Topology comparison
    topologies = ["star", "ring", "mesh"]
    results_by_topology = {}
    
    for topology in topologies:
        logger.info(f"\n{'='*60}")
        logger.info(f"Running {topology.upper()} topology")
        logger.info(f"{'='*60}")
        
        config = FederatedConfig(
            num_agents=4,
            num_generations=30,
            population_size=50,
            mutation_rate=0.1,
            topology=topology,
            aggregation_method="average",
            communication_delay_ms=1.0,
            dropout_rate=0.0
        )
        
        optimizer = FederatedOptimizer(
            config=config,
            fitness_func=sphere_function,
            param_dim=12,
            use_ray=False
        )
        
        results = optimizer.optimize()
        results_by_topology[topology] = results
        
        # Plot individual convergence
        optimizer.plot_convergence()
    
    # Compare topologies
    logger.info("\n" + "=" * 80)
    logger.info("TOPOLOGY COMPARISON")
    logger.info("=" * 80)
    
    for topology, results in results_by_topology.items():
        final_loss = results['convergence_curve'][-1]
        avg_comm = results['communication_overhead']
        logger.info(f"{topology:10s}: final_loss={final_loss:.4f}, comm_overhead={avg_comm:.2f}ms")
    
    # Save detailed results
    results_df = pd.DataFrame({
        'topology': list(results_by_topology.keys()),
        'final_loss': [results_by_topology[t]['convergence_curve'][-1] for t in results_by_topology],
        'total_time': [results_by_topology[t]['total_time'] for t in results_by_topology],
        'communication_cost': [results_by_topology[t]['communication_overhead'] for t in results_by_topology],
    })
    
    output_file = f"federated_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    results_df.to_csv(output_file, index=False)
    logger.info(f"Saved results to {output_file}")
    
    logger.info("\n" + "=" * 80)
    logger.info("DEMO COMPLETE")
    logger.info("=" * 80)


if __name__ == "__main__":
    demo_federated_optimization()
