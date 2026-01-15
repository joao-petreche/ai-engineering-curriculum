# Mês 11 Week 1: Custom Metrics & KPIs Framework

## Overview
**Duration**: 12-15 hours  
**Objective**: Build production-grade metrics framework for business KPIs beyond standard loss functions  
**Deliverable**: Multi-objective metrics library with dashboarding and constraint handling  
**Tech Stack**: Python, Pandas, Scikit-learn, W&B, Matplotlib, Pydantic

---

## Exercise 1.1: Business Metrics Framework

### Learning Objectives
- Design metrics for real-world optimization (profit, ROI, sustainability, risk)
- Implement weighted composite scoring functions
- Create reusable metrics library with Pydantic validation

### Implementation Guide

**Create `metrics_framework.py`:**

```python
from dataclasses import dataclass
from typing import Dict, List, Callable
import numpy as np
from pydantic import BaseModel, field_validator
from enum import Enum


class MetricType(str, Enum):
    PROFIT = "profit"
    ROI = "roi"
    SUSTAINABILITY = "sustainability"
    RISK = "risk"
    EFFICIENCY = "efficiency"
    QUALITY = "quality"


@dataclass
class PerformanceResult:
    """Single optimization run result"""
    output: float
    price: float
    compute_cost: float
    energy_consumed: float
    quality_score: float
    time_to_completion: float


class CompositeMetricConfig(BaseModel):
    """Configuration for weighted metrics"""
    weights: Dict[str, float]
    constraints: Dict[str, tuple]  # (min, max)
    
    @field_validator('weights')
    @classmethod
    def weights_sum_to_one(cls, v: Dict[str, float]) -> Dict[str, float]:
        """Weights must sum to 1.0"""
        total = sum(v.values())
        if not (0.99 <= total <= 1.01):
            raise ValueError(f"Weights must sum to 1.0, got {total}")
        return v


class MetricsFramework:
    """Production metrics calculation engine"""
    
    def __init__(self, config: CompositeMetricConfig):
        self.config = config
        self.history = []
    
    @staticmethod
    def profit(results: List[PerformanceResult]) -> float:
        """Calculate total profit = revenue - cost"""
        revenue = sum(r.output * r.price for r in results)
        cost = sum(r.compute_cost for r in results)
        return revenue - cost
    
    @staticmethod
    def roi(profit: float, investment: float) -> float:
        """Return on investment"""
        return profit / investment if investment > 0 else 0.0
    
    @staticmethod
    def efficiency(output: float, energy: float) -> float:
        """Output per unit energy"""
        return output / energy if energy > 0 else 0.0
    
    @staticmethod
    def sustainability_score(energy_consumed: float, baseline_energy: float) -> float:
        """% energy reduction vs baseline (0-1, higher=better)"""
        reduction = (baseline_energy - energy_consumed) / baseline_energy
        return max(0.0, min(1.0, reduction))
    
    @staticmethod
    def quality_metric(quality_scores: List[float]) -> float:
        """Average quality with penalty for variance"""
        mean_quality = np.mean(quality_scores)
        std_quality = np.std(quality_scores)
        # Penalize inconsistency
        return mean_quality - 0.1 * std_quality
    
    @staticmethod
    def risk_score(results: List[PerformanceResult]) -> float:
        """Coefficient of variation in outputs (lower=safer)"""
        outputs = [r.output for r in results]
        mean_output = np.mean(outputs)
        std_output = np.std(outputs)
        cv = std_output / mean_output if mean_output > 0 else 1.0
        # Normalize to [0, 1] with inverse scaling
        return 1.0 / (1.0 + cv)
    
    def composite_score(self, metrics: Dict[str, float]) -> float:
        """Weighted combination of normalized metrics"""
        # Normalize each metric to [0, 1]
        normalized = {}
        for metric_name, value in metrics.items():
            if metric_name in self.config.constraints:
                min_val, max_val = self.config.constraints[metric_name]
                # Clamp and normalize
                normalized[metric_name] = (value - min_val) / (max_val - min_val)
                normalized[metric_name] = max(0.0, min(1.0, normalized[metric_name]))
            else:
                normalized[metric_name] = value
        
        # Weighted sum
        score = sum(
            self.config.weights.get(name, 0.0) * normalized.get(name, 0.0)
            for name in self.config.weights.keys()
        )
        return float(score)
    
    def evaluate_solution(self, results: List[PerformanceResult], 
                         investment: float, baseline_energy: float) -> Dict[str, float]:
        """Complete metrics evaluation for a solution"""
        quality_scores = [r.quality_score for r in results]
        
        metrics = {
            MetricType.PROFIT: self.profit(results),
            MetricType.ROI: self.roi(self.profit(results), investment),
            MetricType.SUSTAINABILITY: self.sustainability_score(
                sum(r.energy_consumed for r in results), 
                baseline_energy
            ),
            MetricType.RISK: self.risk_score(results),
            MetricType.EFFICIENCY: self.efficiency(
                sum(r.output for r in results),
                sum(r.energy_consumed for r in results)
            ),
            MetricType.QUALITY: self.quality_metric(quality_scores),
        }
        
        composite = self.composite_score(metrics)
        
        result_dict = {k.value: v for k, v in metrics.items()}
        result_dict['composite_score'] = composite
        
        self.history.append(result_dict)
        return result_dict
    
    def get_history_dataframe(self):
        """Return metrics history as pandas DataFrame"""
        import pandas as pd
        return pd.DataFrame(self.history)
    
    def correlation_analysis(self) -> Dict[str, float]:
        """Compute pairwise metric correlations"""
        import pandas as pd
        df = self.get_history_dataframe()
        return df.corr().to_dict()


# Example usage
if __name__ == "__main__":
    # Configure metrics
    config = CompositeMetricConfig(
        weights={
            'profit': 0.4,
            'roi': 0.2,
            'sustainability': 0.25,
            'risk': 0.15,
        },
        constraints={
            'profit': (0, 1e6),
            'roi': (0, 1.0),
            'sustainability': (0, 1.0),
            'risk': (0, 1.0),
        }
    )
    
    metrics = MetricsFramework(config)
    
    # Simulate results
    results = [
        PerformanceResult(
            output=1000, price=50, compute_cost=100,
            energy_consumed=500, quality_score=0.92, time_to_completion=2.5
        ),
        PerformanceResult(
            output=950, price=50, compute_cost=95,
            energy_consumed=450, quality_score=0.95, time_to_completion=2.3
        ),
    ]
    
    eval_metrics = metrics.evaluate_solution(results, investment=5000, baseline_energy=1200)
    print("Metrics:", eval_metrics)
    print("Correlation:", metrics.correlation_analysis())
```

### Checkpoint Requirements

- [ ] **Code Implementation**: `metrics_framework.py` with 6+ metric types
- [ ] **Unit Tests**: Test profit, ROI, efficiency calculations with known values
- [ ] **Validation**: Pydantic validation for weights, constraints
- [ ] **Documentation**: Docstrings for each metric explaining business meaning

---

## Exercise 1.2: Multi-Objective Dashboard

### Learning Objectives
- Visualize Pareto trade-offs between business objectives
- Create interactive dashboards with correlation analysis
- Log metrics to W&B for experiment tracking

### Implementation Guide

**Create `dashboard.py`:**

```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from typing import List, Dict
import wandb


class MetricsDashboard:
    """Visualization dashboard for multi-objective optimization"""
    
    def __init__(self, metrics_history: List[Dict], project_name: str = None):
        self.df = pd.DataFrame(metrics_history)
        self.project_name = project_name
        
        if project_name:
            wandb.init(project=project_name, config={"metrics": "dashboard"})
    
    def pareto_2d_plot(self, metric_x: str, metric_y: str, figsize=(10, 7)):
        """Plot 2D Pareto frontier"""
        fig, ax = plt.subplots(figsize=figsize)
        
        # Identify Pareto front (assuming higher is better for both)
        pareto_mask = self._identify_pareto_front(metric_x, metric_y)
        
        # Plot all points
        ax.scatter(self.df[metric_x], self.df[metric_y], alpha=0.3, s=50, label='Non-dominated')
        
        # Highlight Pareto
        pareto_df = self.df[pareto_mask]
        ax.scatter(pareto_df[metric_x], pareto_df[metric_y], 
                  color='red', s=150, marker='*', label='Pareto Front', zorder=5)
        
        ax.set_xlabel(metric_x)
        ax.set_ylabel(metric_y)
        ax.set_title(f'Pareto Trade-off: {metric_x} vs {metric_y}')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        return fig
    
    @staticmethod
    def _identify_pareto_front(df: pd.DataFrame, metric_x: str, metric_y: str) -> np.ndarray:
        """Identify non-dominated solutions"""
        n = len(df)
        is_dominated = np.zeros(n, dtype=bool)
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    if df.iloc[j][metric_x] >= df.iloc[i][metric_x] and \
                       df.iloc[j][metric_y] >= df.iloc[i][metric_y]:
                        if df.iloc[j][metric_x] > df.iloc[i][metric_x] or \
                           df.iloc[j][metric_y] > df.iloc[i][metric_y]:
                            is_dominated[i] = True
                            break
        
        return ~is_dominated
    
    def correlation_heatmap(self, figsize=(10, 8)):
        """Metric correlation matrix"""
        fig, ax = plt.subplots(figsize=figsize)
        
        corr_matrix = self.df.corr()
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                   center=0, ax=ax, cbar_kws={'label': 'Correlation'})
        
        ax.set_title('Metric Correlations')
        return fig
    
    def timeseries_metrics(self, metrics: List[str], figsize=(12, 6)):
        """KPI time-series evolution"""
        fig, axes = plt.subplots(len(metrics), 1, figsize=figsize, sharex=True)
        
        if len(metrics) == 1:
            axes = [axes]
        
        for ax, metric in zip(axes, metrics):
            ax.plot(self.df.index, self.df[metric], marker='o', linewidth=2)
            ax.fill_between(self.df.index, self.df[metric], alpha=0.3)
            ax.set_ylabel(metric)
            ax.grid(True, alpha=0.3)
        
        axes[-1].set_xlabel('Iteration')
        fig.suptitle('KPI Evolution Over Time')
        return fig
    
    def distribution_plots(self, metrics: List[str], figsize=(12, 8)):
        """Distribution analysis for metrics"""
        n_cols = 2
        n_rows = (len(metrics) + n_cols - 1) // n_cols
        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        axes = axes.flatten()
        
        for idx, metric in enumerate(metrics):
            axes[idx].hist(self.df[metric], bins=20, edgecolor='black', alpha=0.7)
            axes[idx].set_title(f'{metric} Distribution')
            axes[idx].set_xlabel(metric)
            axes[idx].set_ylabel('Frequency')
        
        for idx in range(len(metrics), len(axes)):
            fig.delaxes(axes[idx])
        
        return fig
    
    def log_to_wandb(self, metrics: List[str]):
        """Log visualizations to Weights & Biases"""
        if not self.project_name:
            print("W&B not initialized. Call with project_name to enable logging.")
            return
        
        for metric_pair in [('profit', 'roi'), ('sustainability', 'efficiency')]:
            if all(m in self.df.columns for m in metric_pair):
                fig = self.pareto_2d_plot(metric_pair[0], metric_pair[1])
                wandb.log({f"pareto_{metric_pair[0]}_vs_{metric_pair[1]}": wandb.Image(fig)})
                plt.close(fig)
        
        fig = self.correlation_heatmap()
        wandb.log({"correlation_matrix": wandb.Image(fig)})
        plt.close(fig)
        
        fig = self.timeseries_metrics(metrics)
        wandb.log({"timeseries": wandb.Image(fig)})
        plt.close(fig)


# Example usage
if __name__ == "__main__":
    # Simulate metrics history
    metrics_history = [
        {'profit': 50000, 'roi': 0.85, 'sustainability': 0.75, 'risk': 0.8},
        {'profit': 55000, 'roi': 0.90, 'sustainability': 0.80, 'risk': 0.75},
        {'profit': 52000, 'roi': 0.88, 'sustainability': 0.78, 'risk': 0.82},
    ]
    
    dashboard = MetricsDashboard(metrics_history)
    
    # Create and display plots
    fig1 = dashboard.pareto_2d_plot('profit', 'roi')
    fig2 = dashboard.correlation_heatmap()
    fig3 = dashboard.timeseries_metrics(['profit', 'roi', 'sustainability'])
    
    plt.show()
```

### Checkpoint Requirements

- [ ] **Pareto Frontier**: 2D visualization with non-dominated solutions highlighted
- [ ] **Correlation Analysis**: Heatmap showing metric relationships
- [ ] **Time-Series**: KPI evolution across optimization iterations
- [ ] **W&B Integration**: Metrics logged to Weights & Biases dashboard
- [ ] **Distribution Analysis**: Histograms for metric distributions

---

## Exercise 1.3: Constraint Handling in Optimization

### Learning Objectives
- Incorporate hard constraints (feasibility boundaries)
- Implement soft constraints (penalty functions)
- Validate solutions against multi-dimensional constraint spaces

### Implementation Guide

**Create `constraint_handler.py`:**

```python
from typing import Dict, List, Callable, Tuple
from dataclasses import dataclass
from enum import Enum
import numpy as np


class ConstraintType(str, Enum):
    HARD = "hard"      # Violating = infeasible
    SOFT = "soft"      # Violating = penalized


@dataclass
class Constraint:
    """Single constraint definition"""
    name: str
    type: ConstraintType
    min_val: float = None
    max_val: float = None
    penalty_weight: float = 1.0  # For soft constraints
    
    def check(self, value: float) -> Tuple[bool, float]:
        """
        Returns (is_feasible, violation)
        - is_feasible: True if constraint satisfied
        - violation: 0 if satisfied, >0 otherwise
        """
        violation = 0.0
        
        if self.min_val is not None and value < self.min_val:
            violation = self.min_val - value
        elif self.max_val is not None and value > self.max_val:
            violation = value - self.max_val
        
        is_feasible = (violation == 0.0)
        return is_feasible, violation


class ConstraintHandler:
    """Multi-constraint validation and penalty application"""
    
    def __init__(self, constraints: List[Constraint]):
        self.constraints = {c.name: c for c in constraints}
        self.constraint_history = []
    
    def validate_solution(self, solution: Dict[str, float]) -> Dict[str, bool]:
        """Check all constraints for a solution"""
        violations = {}
        
        for param_name, constraint in self.constraints.items():
            if param_name in solution:
                is_feasible, _ = constraint.check(solution[param_name])
                violations[param_name] = not is_feasible
        
        return violations
    
    def apply_penalty(self, loss: float, solution: Dict[str, float]) -> float:
        """Apply penalty for constraint violations"""
        penalty = 0.0
        hard_violation = False
        
        for param_name, constraint in self.constraints.items():
            if param_name not in solution:
                continue
            
            is_feasible, violation = constraint.check(solution[param_name])
            
            if not is_feasible:
                if constraint.type == ConstraintType.HARD:
                    # Hard constraint: return infeasible value
                    hard_violation = True
                else:
                    # Soft constraint: add penalty
                    penalty += constraint.penalty_weight * (violation ** 2)
        
        if hard_violation:
            return float('inf')  # Infeasible
        
        return loss + penalty
    
    def get_feasible_region(self) -> Dict[str, Tuple[float, float]]:
        """Return feasible search space"""
        region = {}
        for name, constraint in self.constraints.items():
            min_val = constraint.min_val if constraint.min_val is not None else -np.inf
            max_val = constraint.max_val if constraint.max_val is not None else np.inf
            region[name] = (min_val, max_val)
        return region
    
    def project_to_feasible(self, solution: Dict[str, float]) -> Dict[str, float]:
        """Clamp solution to feasible region"""
        projected = {}
        
        for name, value in solution.items():
            if name in self.constraints:
                constraint = self.constraints[name]
                min_val = constraint.min_val if constraint.min_val is not None else -np.inf
                max_val = constraint.max_val if constraint.max_val is not None else np.inf
                projected[name] = np.clip(value, min_val, max_val)
            else:
                projected[name] = value
        
        return projected
    
    def summary(self) -> str:
        """Print constraint summary"""
        lines = ["Constraint Summary:"]
        for name, constraint in self.constraints.items():
            type_str = constraint.type.value.upper()
            range_str = f"[{constraint.min_val}, {constraint.max_val}]"
            lines.append(f"  {name}: {type_str} {range_str}")
        return "\n".join(lines)


# Example usage
if __name__ == "__main__":
    constraints = [
        Constraint('memory_mb', ConstraintType.HARD, min_val=256, max_val=4096),
        Constraint('latency_ms', ConstraintType.HARD, min_val=10, max_val=2000),
        Constraint('cost_usd', ConstraintType.SOFT, min_val=0, max_val=1000, penalty_weight=0.1),
    ]
    
    handler = ConstraintHandler(constraints)
    print(handler.summary())
    
    # Valid solution
    valid_solution = {'memory_mb': 2048, 'latency_ms': 500, 'cost_usd': 800}
    print("\nValid solution violations:", handler.validate_solution(valid_solution))
    
    # Invalid solution
    invalid_solution = {'memory_mb': 5000, 'latency_ms': 3000, 'cost_usd': 1500}
    print("Invalid solution violations:", handler.validate_solution(invalid_solution))
    
    # Penalty calculation
    loss = 100.0
    penalized_loss = handler.apply_penalty(loss, invalid_solution)
    print(f"Loss: {loss}, Penalized: {penalized_loss}")
```

### Checkpoint Requirements

- [ ] **Constraint Definition**: Hard and soft constraint types implemented
- [ ] **Validation**: Solutions checked against all constraints
- [ ] **Penalty Function**: Violations converted to penalties
- [ ] **Feasible Region**: Search space bounded correctly
- [ ] **Projection**: Out-of-bounds solutions projected to feasible region

---

## Exercise 1.4: Robustness Analysis

### Learning Objectives
- Measure solution stability under perturbations
- Identify robust vs. fragile solutions
- Create robustness rankings and metrics

### Implementation Guide

**Create `robustness_analysis.py`:**

```python
import numpy as np
from typing import Dict, List, Callable, Tuple
from dataclasses import dataclass
import matplotlib.pyplot as plt


@dataclass
class RobustnessMetrics:
    """Container for robustness analysis results"""
    mean_performance: float
    std_performance: float
    min_performance: float
    max_performance: float
    cv_coefficient: float  # std/mean
    robustness_score: float  # 1 / (1 + CV)
    
    def __str__(self):
        return (
            f"Robustness Analysis:\n"
            f"  Mean Performance: {self.mean_performance:.4f}\n"
            f"  Std Dev: {self.std_performance:.4f}\n"
            f"  Range: [{self.min_performance:.4f}, {self.max_performance:.4f}]\n"
            f"  CV: {self.cv_coefficient:.4f}\n"
            f"  Robustness Score: {self.robustness_score:.4f}"
        )


class RobustnessAnalyzer:
    """Measure solution robustness under perturbations"""
    
    def __init__(self, evaluation_fn: Callable, perturbation_std: float = 0.05):
        """
        Args:
            evaluation_fn: Function that takes solution dict and returns scalar score
            perturbation_std: Standard deviation of Gaussian perturbation
        """
        self.eval_fn = evaluation_fn
        self.perturbation_std = perturbation_std
        self.test_history = []
    
    def add_gaussian_noise(self, solution: Dict[str, float]) -> Dict[str, float]:
        """Add Gaussian noise to solution"""
        noisy = {}
        for key, value in solution.items():
            noise = np.random.normal(0, self.perturbation_std * abs(value))
            noisy[key] = value + noise
        return noisy
    
    def robustness_test(self, solution: Dict[str, float], 
                       num_perturbs: int = 100) -> RobustnessMetrics:
        """Test solution robustness with multiple perturbations"""
        scores = []
        
        for _ in range(num_perturbs):
            perturbed = self.add_gaussian_noise(solution)
            try:
                score = self.eval_fn(perturbed)
                scores.append(score)
            except Exception as e:
                # Invalid perturbation (e.g., violated constraints)
                scores.append(np.nan)
        
        # Remove NaN values
        valid_scores = np.array([s for s in scores if not np.isnan(s)])
        
        if len(valid_scores) == 0:
            raise ValueError("All perturbations resulted in invalid solutions")
        
        metrics = RobustnessMetrics(
            mean_performance=float(np.mean(valid_scores)),
            std_performance=float(np.std(valid_scores)),
            min_performance=float(np.min(valid_scores)),
            max_performance=float(np.max(valid_scores)),
            cv_coefficient=float(np.std(valid_scores) / np.mean(valid_scores)),
            robustness_score=1.0 / (1.0 + np.std(valid_scores) / np.mean(valid_scores))
        )
        
        self.test_history.append({
            'solution': solution.copy(),
            'metrics': metrics,
            'scores': valid_scores.tolist()
        })
        
        return metrics
    
    def compare_robustness(self, solutions: Dict[str, Dict[str, float]], 
                          num_perturbs: int = 100) -> Dict[str, RobustnessMetrics]:
        """Compare robustness across multiple solutions"""
        results = {}
        
        for sol_name, solution in solutions.items():
            results[sol_name] = self.robustness_test(solution, num_perturbs)
        
        return results
    
    def robustness_ranking(self, solutions: Dict[str, Dict[str, float]], 
                          num_perturbs: int = 100) -> List[Tuple[str, float]]:
        """Rank solutions by robustness score"""
        results = self.compare_robustness(solutions, num_perturbs)
        
        ranking = sorted(
            [(name, metrics.robustness_score) for name, metrics in results.items()],
            key=lambda x: x[1],
            reverse=True  # Higher = more robust
        )
        
        return ranking
    
    def plot_robustness_comparison(self, solution_names: List[str]):
        """Visualize robustness test results"""
        if not self.test_history:
            print("No robustness tests performed yet")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Plot 1: Box plot of scores
        scores_data = [test['scores'] for test in self.test_history[-len(solution_names):]]
        axes[0, 0].boxplot(scores_data, labels=solution_names)
        axes[0, 0].set_title('Performance Distribution')
        axes[0, 0].set_ylabel('Score')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Robustness scores
        robustness_scores = [test['metrics'].robustness_score for test in self.test_history[-len(solution_names):]]
        axes[0, 1].bar(solution_names, robustness_scores, color='green', alpha=0.7)
        axes[0, 1].set_title('Robustness Scores')
        axes[0, 1].set_ylabel('Score')
        axes[0, 1].set_ylim([0, 1])
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        # Plot 3: CV comparison
        cvs = [test['metrics'].cv_coefficient for test in self.test_history[-len(solution_names):]]
        axes[1, 0].bar(solution_names, cvs, color='orange', alpha=0.7)
        axes[1, 0].set_title('Coefficient of Variation')
        axes[1, 0].set_ylabel('CV')
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # Plot 4: Range visualization
        for idx, test in enumerate(self.test_history[-len(solution_names):]):
            metrics = test['metrics']
            axes[1, 1].errorbar(
                idx, metrics.mean_performance,
                yerr=metrics.std_performance,
                marker='o', markersize=8, capsize=5
            )
        axes[1, 1].set_xticks(range(len(solution_names)))
        axes[1, 1].set_xticklabels(solution_names)
        axes[1, 1].set_title('Mean ± Std Dev')
        axes[1, 1].set_ylabel('Score')
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        fig.tight_layout()
        return fig


# Example usage
if __name__ == "__main__":
    # Mock evaluation function
    def mock_objective(solution):
        # Simulated objective: closer to [10, 20] is better
        dist = (solution['x'] - 10) ** 2 + (solution['y'] - 20) ** 2
        return 1.0 / (1.0 + dist)
    
    analyzer = RobustnessAnalyzer(mock_objective, perturbation_std=0.1)
    
    # Test solutions
    solutions = {
        'optimal': {'x': 10.0, 'y': 20.0},
        'near_optimal': {'x': 10.5, 'y': 20.3},
        'suboptimal': {'x': 5.0, 'y': 15.0},
    }
    
    # Rank by robustness
    ranking = analyzer.robustness_ranking(solutions, num_perturbs=200)
    print("Robustness Ranking:")
    for rank, (name, score) in enumerate(ranking, 1):
        print(f"  {rank}. {name}: {score:.4f}")
    
    # Visualize
    fig = analyzer.plot_robustness_comparison(list(solutions.keys()))
    plt.show()
```

### Checkpoint Requirements

- [ ] **Perturbation System**: Gaussian noise generation and application
- [ ] **Metrics Calculation**: Mean, std, CV, robustness score computed correctly
- [ ] **Ranking System**: Solutions ranked by robustness score
- [ ] **Visualization**: Box plots, bar charts showing stability comparisons
- [ ] **100+ Perturbations**: Each solution tested with sufficient sample size

---

## Summary & Certification

### Week 1 Deliverables

| Exercise | Component | Status |
|----------|-----------|--------|
| 1.1 | Metrics Framework | Complete metrics library with 6+ types |
| 1.2 | Dashboard | Pareto, correlation, time-series visualizations |
| 1.3 | Constraints | Hard/soft constraint handling, penalty functions |
| 1.4 | Robustness | Perturbation analysis, stability ranking |

### Validation Checklist

- [ ] All 4 exercises completed with checkpoints verified
- [ ] 50+ unit tests passing (metrics, constraints, robustness)
- [ ] Metrics framework validated with known business scenarios
- [ ] Dashboard displays at least 6 different metrics views
- [ ] Constraint violations properly detected and handled
- [ ] Robustness ranking matches intuitive solution quality

### Next Steps

✅ **Week 1 Complete**: Move to [Week 2: Sensitivity Analysis](WEEK_2_SENSITIVITY.md)
