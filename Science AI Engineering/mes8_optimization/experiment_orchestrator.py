"""
Experiment Orchestration and Tracking for Building Energy Optimization

This module orchestrates experiments comparing different optimization strategies:
1. NSGA-II (unconstrained multi-objective)
2. Constrained NSGA-II (penalty method)
3. Augmented Lagrangian (AL) refinement

Features:
- MLflow experiment tracking (run, log, compare)
- Structured JSON logging
- Git versioning (commit hash, dirty status)
- Reproducibility (seed tracking, data hashes)
- Automated comparisons (Pareto, feasibility, trade-offs)
- Dashboard visualization (Plotly)
- Comprehensive reporting (Markdown + tables)

Author: Scientific AI Engineering Curriculum
Date: January 2026
Dependencies: mlflow, numpy, pandas, plotly, matplotlib
"""

import json
import logging
import hashlib
import pickle
import subprocess
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

try:
    import mlflow
    from mlflow import log_metric, log_artifact, log_params
except ImportError:
    mlflow = None
    logging.warning("MLflow not installed. Experiment tracking disabled.")


# Configure logging
class ColoredFormatter(logging.Formatter):
    """Colored log formatter for better readability."""
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[92m',     # Green
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',    # Red
        'CRITICAL': '\033[41m'  # Red background
    }
    RESET = '\033[0m'
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        return super().format(record)


# Setup colored logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))
logger.addHandler(handler)


@dataclass
class ExperimentConfig:
    """Configuration for experiment orchestration."""
    experiment_name: str = "building_energy_optimization"
    run_name: str = ""
    strategy: str = "nsga2"  # nsga2, constrained, augmented_lagrangian
    n_solutions: int = 100
    n_generations: int = 30
    random_seed: int = 42
    description: str = ""
    

@dataclass
class ExperimentMetrics:
    """Metrics collected during optimization."""
    # Objectives
    best_consumption: float = 0.0
    best_comfort: float = 0.0
    best_peak: float = 0.0
    mean_consumption: float = 0.0
    
    # Feasibility
    n_feasible: int = 0
    feasibility_percentage: float = 0.0
    
    # Pareto
    pareto_size: int = 0
    hypervolume: float = 0.0
    
    # Computation
    compute_time: float = 0.0
    n_evaluations: int = 0
    
    # Reproducibility
    git_commit: str = ""
    git_dirty: bool = False
    data_hash: str = ""
    timestamp: str = ""


@dataclass
class ComparisonResult:
    """Results from comparing multiple experiments."""
    strategies: List[str] = field(default_factory=list)
    best_objectives: Dict[str, Dict[str, float]] = field(default_factory=dict)
    feasibility_stats: Dict[str, Dict[str, float]] = field(default_factory=dict)
    pareto_stats: Dict[str, Dict[str, float]] = field(default_factory=dict)
    compute_time_stats: Dict[str, float] = field(default_factory=dict)
    winner_strategy: str = ""


class ExperimentOrchestrator:
    """
    Orchestrates experiments comparing optimization strategies.
    
    Manages MLflow tracking, logging, comparison, and reporting.
    """
    
    def __init__(
        self,
        output_dir: Path = Path("results/experiments"),
        use_mlflow: bool = True
    ):
        """
        Initialize orchestrator.
        
        Args:
            output_dir: Directory for saving results
            use_mlflow: Whether to use MLflow tracking
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.use_mlflow = use_mlflow and mlflow is not None
        if self.use_mlflow:
            mlflow.set_tracking_uri(str(self.output_dir / "mlruns"))
            logger.info(f"MLflow tracking enabled: {self.output_dir / 'mlruns'}")
        else:
            logger.warning("MLflow tracking disabled")
        
        self.experiments: Dict[str, Dict[str, Any]] = {}
        self.comparison_results: Optional[ComparisonResult] = None
        
        logger.info(f"Experiment orchestrator initialized: {self.output_dir}")
    
    def _get_git_info(self) -> Dict[str, Any]:
        """Get git commit info for reproducibility."""
        try:
            commit = subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'],
                stderr=subprocess.DEVNULL
            ).decode().strip()
            
            dirty = subprocess.check_output(
                ['git', 'status', '--porcelain'],
                stderr=subprocess.DEVNULL
            ).decode().strip() != ""
            
            return {
                'commit': commit,
                'dirty': dirty
            }
        except Exception as e:
            logger.warning(f"Could not get git info: {e}")
            return {'commit': 'unknown', 'dirty': False}
    
    def _hash_data(self, data: Any) -> str:
        """Create hash of data for reproducibility."""
        if isinstance(data, (list, dict)):
            data_str = json.dumps(data, sort_keys=True, default=str)
        else:
            data_str = str(data)
        
        return hashlib.md5(data_str.encode()).hexdigest()[:8]
    
    def start_experiment(
        self,
        config: ExperimentConfig
    ) -> str:
        """
        Start a new experiment run.
        
        Args:
            config: Experiment configuration
            
        Returns:
            Run ID
        """
        run_name = config.run_name or f"{config.strategy}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        logger.info("=" * 80)
        logger.info(f"STARTING EXPERIMENT: {run_name}")
        logger.info("=" * 80)
        logger.info(f"Strategy: {config.strategy}")
        logger.info(f"Solutions: {config.n_solutions}, Generations: {config.n_generations}")
        logger.info(f"Seed: {config.random_seed}")
        
        if self.use_mlflow:
            mlflow.set_experiment(config.experiment_name)
            mlflow.start_run(run_name=run_name)
            
            # Log parameters
            mlflow.log_params({
                'strategy': config.strategy,
                'n_solutions': config.n_solutions,
                'n_generations': config.n_generations,
                'random_seed': config.random_seed
            })
            
            run_id = mlflow.active_run().info.run_id
            logger.info(f"MLflow run started: {run_id}")
        else:
            run_id = hashlib.md5(run_name.encode()).hexdigest()[:8]
        
        self.experiments[run_id] = {
            'config': config,
            'run_name': run_name,
            'start_time': datetime.now(),
            'metrics': None,
            'solutions': None,
            'git_info': self._get_git_info()
        }
        
        return run_id
    
    def log_metrics(
        self,
        run_id: str,
        metrics: ExperimentMetrics
    ) -> None:
        """
        Log experiment metrics.
        
        Args:
            run_id: Run identifier
            metrics: ExperimentMetrics object
        """
        logger.info(f"Logging metrics for run {run_id}")
        
        # Store locally
        self.experiments[run_id]['metrics'] = metrics
        
        # Log to MLflow
        if self.use_mlflow:
            mlflow.log_metrics({
                'best_consumption_kwh': metrics.best_consumption,
                'best_comfort_hours': metrics.best_comfort,
                'best_peak_cooling_kw': metrics.best_peak,
                'mean_consumption_kwh': metrics.mean_consumption,
                'n_feasible': metrics.n_feasible,
                'feasibility_percentage': metrics.feasibility_percentage,
                'pareto_size': metrics.pareto_size,
                'hypervolume': metrics.hypervolume,
                'compute_time_seconds': metrics.compute_time,
                'n_evaluations': metrics.n_evaluations
            })
        
        # Log to JSON
        metrics_json = self.output_dir / f"metrics_{run_id}.json"
        with open(metrics_json, 'w') as f:
            json.dump(asdict(metrics), f, indent=2)
        
        logger.info(f"Metrics saved to {metrics_json}")
        
        # Print summary
        logger.info("-" * 80)
        logger.info("EXPERIMENT SUMMARY")
        logger.info("-" * 80)
        logger.info(f"Best consumption: {metrics.best_consumption:.0f} kWh")
        logger.info(f"Best comfort: {metrics.best_comfort:.0f} h")
        logger.info(f"Best peak: {metrics.best_peak:.1f} kW")
        logger.info(f"Feasible solutions: {metrics.n_feasible} ({metrics.feasibility_percentage:.1f}%)")
        logger.info(f"Pareto size: {metrics.pareto_size}")
        logger.info(f"Compute time: {metrics.compute_time:.2f}s")
        logger.info(f"Evaluations: {metrics.n_evaluations}")
    
    def log_solutions(
        self,
        run_id: str,
        solutions_df: pd.DataFrame
    ) -> None:
        """
        Log solution set to MLflow artifact.
        
        Args:
            run_id: Run identifier
            solutions_df: Solutions DataFrame
        """
        logger.info(f"Logging {len(solutions_df)} solutions")
        
        # Save locally
        solutions_csv = self.output_dir / f"solutions_{run_id}.csv"
        solutions_df.to_csv(solutions_csv, index=False)
        
        self.experiments[run_id]['solutions'] = solutions_df
        
        # Log to MLflow
        if self.use_mlflow:
            mlflow.log_artifact(str(solutions_csv))
        
        logger.info(f"Solutions saved to {solutions_csv}")
    
    def end_experiment(self, run_id: str) -> None:
        """
        End an experiment run.
        
        Args:
            run_id: Run identifier
        """
        experiment = self.experiments.get(run_id)
        if not experiment:
            logger.error(f"Run {run_id} not found")
            return
        
        end_time = datetime.now()
        elapsed = (end_time - experiment['start_time']).total_seconds()
        
        if self.use_mlflow:
            mlflow.log_metric('total_time_seconds', elapsed)
            mlflow.end_run()
        
        logger.info(f"Experiment ended. Total time: {elapsed:.2f}s")
        logger.info("=" * 80)
    
    def compare_runs(
        self,
        run_ids: List[str]
    ) -> ComparisonResult:
        """
        Compare results from multiple runs.
        
        Args:
            run_ids: List of run IDs to compare
            
        Returns:
            ComparisonResult object
        """
        logger.info("=" * 80)
        logger.info("COMPARING EXPERIMENTS")
        logger.info("=" * 80)
        
        if not run_ids:
            logger.error("No runs to compare")
            return ComparisonResult()
        
        result = ComparisonResult(strategies=[])
        
        for run_id in run_ids:
            if run_id not in self.experiments:
                logger.warning(f"Run {run_id} not found")
                continue
            
            exp = self.experiments[run_id]
            config = exp['config']
            metrics = exp['metrics']
            
            if metrics is None:
                logger.warning(f"No metrics for {run_id}")
                continue
            
            strategy = config.strategy
            result.strategies.append(strategy)
            
            # Best objectives
            result.best_objectives[strategy] = {
                'consumption': metrics.best_consumption,
                'comfort': metrics.best_comfort,
                'peak': metrics.best_peak
            }
            
            # Feasibility
            result.feasibility_stats[strategy] = {
                'feasible': metrics.n_feasible,
                'percentage': metrics.feasibility_percentage
            }
            
            # Pareto
            result.pareto_stats[strategy] = {
                'size': metrics.pareto_size,
                'hypervolume': metrics.hypervolume
            }
            
            # Compute time
            result.compute_time_stats[strategy] = metrics.compute_time
        
        # Determine winner (best consumption among feasible solutions)
        best_consumption = float('inf')
        best_strategy = None
        
        for strategy, objs in result.best_objectives.items():
            if objs['consumption'] < best_consumption:
                best_consumption = objs['consumption']
                best_strategy = strategy
        
        result.winner_strategy = best_strategy or "N/A"
        self.comparison_results = result
        
        logger.info(f"Comparison complete: {len(result.strategies)} strategies")
        logger.info(f"Winner: {result.winner_strategy}")
        
        return result
    
    def plot_comparison(self) -> None:
        """Create comparison visualizations."""
        if not self.comparison_results:
            logger.warning("No comparison results to plot")
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        result = self.comparison_results
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Best Consumption Comparison',
                'Feasibility Comparison',
                'Pareto Size Comparison',
                'Compute Time Comparison'
            ),
            specs=[[{'type': 'bar'}, {'type': 'bar'}],
                   [{'type': 'bar'}, {'type': 'bar'}]]
        )
        
        # 1. Consumption
        consumptions = [result.best_objectives[s]['consumption'] for s in result.strategies]
        fig.add_trace(
            go.Bar(x=result.strategies, y=consumptions, name='Consumption', marker_color='steelblue'),
            row=1, col=1
        )
        
        # 2. Feasibility
        feasibilities = [result.feasibility_stats[s]['percentage'] for s in result.strategies]
        fig.add_trace(
            go.Bar(x=result.strategies, y=feasibilities, name='Feasibility %', marker_color='green'),
            row=1, col=2
        )
        
        # 3. Pareto size
        pareto_sizes = [result.pareto_stats[s]['size'] for s in result.strategies]
        fig.add_trace(
            go.Bar(x=result.strategies, y=pareto_sizes, name='Pareto Size', marker_color='coral'),
            row=2, col=1
        )
        
        # 4. Compute time
        times = [result.compute_time_stats[s] for s in result.strategies]
        fig.add_trace(
            go.Bar(x=result.strategies, y=times, name='Time (s)', marker_color='orange'),
            row=2, col=2
        )
        
        fig.update_yaxes(title_text="Consumption (kWh)", row=1, col=1)
        fig.update_yaxes(title_text="Feasibility (%)", row=1, col=2)
        fig.update_yaxes(title_text="Pareto Size", row=2, col=1)
        fig.update_yaxes(title_text="Time (s)", row=2, col=2)
        
        fig.update_layout(
            title_text=f"Optimization Strategy Comparison",
            height=800,
            showlegend=False
        )
        
        output_path = self.output_dir / f"comparison_{timestamp}.html"
        fig.write_html(str(output_path))
        logger.info(f"Saved comparison plot to {output_path}")
    
    def generate_report(self) -> str:
        """
        Generate comprehensive report.
        
        Returns:
            Report content (Markdown)
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        report = f"""# Building Energy Optimization - Experiment Report

**Generated:** {timestamp}
**Experiment Count:** {len(self.experiments)}

## Executive Summary

"""
        
        if self.comparison_results:
            result = self.comparison_results
            report += f"""
**Winner Strategy:** {result.winner_strategy}

Strategies compared:
{', '.join(result.strategies)}

"""
        
        report += "## Detailed Results\n\n"
        
        for run_id, exp in self.experiments.items():
            config = exp['config']
            metrics = exp['metrics']
            
            if metrics is None:
                continue
            
            report += f"### {exp['run_name']}\n\n"
            report += f"**Strategy:** {config.strategy}\n"
            report += f"**Configuration:**\n"
            report += f"- Solutions: {config.n_solutions}\n"
            report += f"- Generations: {config.n_generations}\n"
            report += f"- Random seed: {config.random_seed}\n\n"
            
            report += f"**Results:**\n"
            report += f"- Best consumption: {metrics.best_consumption:.0f} kWh\n"
            report += f"- Best comfort: {metrics.best_comfort:.0f} h\n"
            report += f"- Best peak cooling: {metrics.best_peak:.1f} kW\n"
            report += f"- Feasible solutions: {metrics.n_feasible} ({metrics.feasibility_percentage:.1f}%)\n"
            report += f"- Pareto frontier size: {metrics.pareto_size}\n"
            report += f"- Hypervolume: {metrics.hypervolume:.4f}\n\n"
            
            report += f"**Performance:**\n"
            report += f"- Compute time: {metrics.compute_time:.2f}s\n"
            report += f"- Evaluations: {metrics.n_evaluations}\n"
            report += f"- Evaluations/sec: {metrics.n_evaluations/metrics.compute_time:.0f}\n\n"
            
            report += f"**Reproducibility:**\n"
            report += f"- Git commit: {exp['git_info']['commit']}\n"
            report += f"- Git dirty: {exp['git_info']['dirty']}\n\n"
        
        # Comparison table
        if self.comparison_results:
            report += "## Comparison Table\n\n"
            
            comparison_data = []
            for strategy in self.comparison_results.strategies:
                row = {
                    'Strategy': strategy,
                    'Consumption (kWh)': f"{self.comparison_results.best_objectives[strategy]['consumption']:.0f}",
                    'Feasible (%)': f"{self.comparison_results.feasibility_stats[strategy]['percentage']:.1f}",
                    'Pareto Size': f"{self.comparison_results.pareto_stats[strategy]['size']:.0f}",
                    'Time (s)': f"{self.comparison_results.compute_time_stats[strategy]:.2f}"
                }
                comparison_data.append(row)
            
            comp_df = pd.DataFrame(comparison_data)
            report += comp_df.to_markdown(index=False) + "\n\n"
        
        report += "---\n"
        report += f"*Report generated: {timestamp}*\n"
        
        return report
    
    def save_report(self, report: str) -> Path:
        """
        Save report to file.
        
        Args:
            report: Report content
            
        Returns:
            Path to saved report
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = self.output_dir / f"report_{timestamp}.md"
        
        with open(report_path, 'w') as f:
            f.write(report)
        
        logger.info(f"Saved report to {report_path}")
        
        if self.use_mlflow:
            mlflow.log_artifact(str(report_path))
        
        return report_path


def demo_orchestration():
    """Demonstrate experiment orchestration."""
    logger.info("=" * 80)
    logger.info("EXPERIMENT ORCHESTRATION - DEMO")
    logger.info("=" * 80)
    
    # Initialize orchestrator
    orchestrator = ExperimentOrchestrator(
        output_dir=Path("Science AI Engineering/mes8_optimization/results/experiments")
    )
    
    # Simulate three experiment runs
    strategies = [
        ("nsga2", "NSGA-II Multi-Objective (Unconstrained)"),
        ("constrained", "NSGA-II with Penalty Method"),
        ("augmented_lagrangian", "Augmented Lagrangian")
    ]
    
    run_ids = []
    
    for strategy, description in strategies:
        logger.info(f"\n{'='*80}")
        logger.info(f"Running {description}")
        logger.info(f"{'='*80}")
        
        config = ExperimentConfig(
            strategy=strategy,
            n_solutions=100,
            n_generations=30,
            description=description
        )
        
        run_id = orchestrator.start_experiment(config)
        run_ids.append(run_id)
        
        # Simulate metrics (different for each strategy)
        if strategy == "nsga2":
            metrics = ExperimentMetrics(
                best_consumption=37271.0,
                best_comfort=4934.0,
                best_peak=26.5,
                mean_consumption=52000.0,
                n_feasible=52,
                feasibility_percentage=100.0,
                pareto_size=52,
                hypervolume=7.34,
                compute_time=2.1,
                n_evaluations=3100,
                git_commit="b4ddd3b",
                timestamp=datetime.now().isoformat()
            )
        elif strategy == "constrained":
            metrics = ExperimentMetrics(
                best_consumption=37948.0,
                best_comfort=5280.0,
                best_peak=28.7,
                mean_consumption=55000.0,
                n_feasible=13,
                feasibility_percentage=8.7,
                pareto_size=13,
                hypervolume=6.89,
                compute_time=2.3,
                n_evaluations=3150,
                git_commit="31c4602",
                timestamp=datetime.now().isoformat()
            )
        else:  # augmented_lagrangian
            metrics = ExperimentMetrics(
                best_consumption=38200.0,
                best_comfort=5100.0,
                best_peak=27.2,
                mean_consumption=54000.0,
                n_feasible=28,
                feasibility_percentage=18.7,
                pareto_size=28,
                hypervolume=7.12,
                compute_time=3.5,
                n_evaluations=4200,
                git_commit="31c4602",
                timestamp=datetime.now().isoformat()
            )
        
        # Log metrics
        orchestrator.log_metrics(run_id, metrics)
        
        # Create dummy solutions
        solutions = pd.DataFrame({
            'consumption_kwh': np.random.normal(metrics.best_consumption, 5000, 100),
            'comfort_hours': np.random.normal(metrics.best_comfort, 500, 100),
            'peak_cooling_kw': np.random.normal(metrics.best_peak, 5, 100)
        })
        
        orchestrator.log_solutions(run_id, solutions)
        orchestrator.end_experiment(run_id)
    
    # Compare runs
    logger.info("\n" + "=" * 80)
    comparison = orchestrator.compare_runs(run_ids)
    
    # Generate comparison plot
    orchestrator.plot_comparison()
    
    # Generate report
    report = orchestrator.generate_report()
    report_path = orchestrator.save_report(report)
    
    logger.info("\n" + "=" * 80)
    logger.info("ORCHESTRATION DEMO COMPLETE")
    logger.info("=" * 80)
    logger.info(f"Report saved to: {report_path}")


if __name__ == "__main__":
    demo_orchestration()
