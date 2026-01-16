"""
Global Sensitivity Analysis for Building Energy Optimization

This module implements variance-based (Sobol) and screening (Morris) methods
for global sensitivity analysis. It identifies which input parameters have
the greatest influence on outputs (consumption, comfort, peak cooling).

Two complementary approaches:
1. Sobol Indices (variance-based): First-order (S1) and total-order (ST) effects
   - Computationally expensive (~10k surrogate evals)
   - Provides interaction information
   - Better for high-dimensional problems

2. Morris Screening (one-at-a-time): Mean (μ) and standard deviation (σ) of EE
   - Lower computational cost (~200-500 evals)
   - Quick parameter ranking
   - Good for screening before detailed analysis

Applications:
- Identify top 5-6 most influential parameters
- Reduce dimensionality for future optimizations
- Understand parameter interactions
- Support engineering decision-making

Author: Scientific AI Engineering Curriculum
Date: January 2026
Dependencies: numpy, pandas, matplotlib, plotly, scikit-learn
References:
  - Sobol, I.M. (2001). Global sensitivity indices for nonlinear mathematical models
  - Morris, M.D. (1991). Factorial sampling plans for preliminary computational experiments
  - SALib: Sensitivity Analysis Library (Python implementation)
"""

import json
import logging
import pickle
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class SobolIndices:
    """Store Sobol sensitivity indices for a single output."""
    output_name: str
    S1: Dict[str, float]        # First-order effects
    ST: Dict[str, float]        # Total-order effects
    S1_conf: Dict[str, float]   # Confidence intervals (S1)
    ST_conf: Dict[str, float]   # Confidence intervals (ST)
    n_samples: int              # Number of samples used


@dataclass
class MorrisMetrics:
    """Store Morris screening metrics for a single output."""
    output_name: str
    mu: Dict[str, float]        # Mean of elementary effects
    sigma: Dict[str, float]     # Std of elementary effects
    mu_star: Dict[str, float]   # Mean of absolute elementary effects
    n_trajectories: int         # Number of trajectories


class GlobalSensitivityAnalyzer:
    """
    Global Sensitivity Analysis using Sobol and Morris methods.
    
    This class provides variance-based (Sobol) and screening (Morris)
    sensitivity analysis to identify influential parameters in the
    building energy optimization problem.
    
    Attributes:
        surrogate_model: Pre-trained surrogate model
        parameter_bounds: Dict of parameter bounds
        parameter_names: List of parameter names (ordered)
        sobol_results: Dict of SobolIndices objects
        morris_results: Dict of MorrisMetrics objects
    """
    
    def __init__(
        self,
        surrogate_model_path: Path,
        parameter_bounds: Dict[str, Tuple[float, float]],
        output_dir: Path = Path("results/sensitivity")
    ):
        """
        Initialize sensitivity analyzer.
        
        Args:
            surrogate_model_path: Path to pre-trained surrogate
            parameter_bounds: Dict mapping param names to (min, max)
            output_dir: Directory for saving results
        """
        logger.info("Initializing Global Sensitivity Analyzer...")
        
        # Load surrogate model
        with open(surrogate_model_path, 'rb') as f:
            self.surrogate_model = pickle.load(f)
        logger.info(f"Loaded surrogate from {surrogate_model_path}")
        
        # Parameter setup
        self.parameter_bounds = parameter_bounds
        self.parameter_names = list(parameter_bounds.keys())
        self.n_params = len(self.parameter_names)
        
        # Results storage
        self.sobol_results: Dict[str, SobolIndices] = {}
        self.morris_results: Dict[str, MorrisMetrics] = {}
        
        # Output directory
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Analyzer ready: {self.n_params} parameters")
    
    def _denormalize_params(self, normalized: np.ndarray) -> np.ndarray:
        """
        Convert normalized params [0,1] to physical bounds.
        
        Args:
            normalized: Array of shape (N, n_params) with values in [0,1]
            
        Returns:
            Denormalized array with physical values
        """
        denormalized = np.zeros_like(normalized)
        for i, param_name in enumerate(self.parameter_names):
            min_val, max_val = self.parameter_bounds[param_name]
            denormalized[:, i] = min_val + normalized[:, i] * (max_val - min_val)
        return denormalized
    
    def _evaluate_samples(self, X: np.ndarray) -> np.ndarray:
        """
        Evaluate surrogate model on sample set.
        
        Args:
            X: Array of shape (N, n_params) with physical parameter values
            
        Returns:
            Array of shape (N, 3) with [consumption, comfort_hours, peak_cooling]
        """
        try:
            return self.surrogate_model.predict(X)
        except Exception as e:
            logger.error(f"Surrogate evaluation error: {e}")
            return np.zeros((X.shape[0], 3))
    
    def sobol_analysis(
        self,
        n_samples: int = 2048,
        output_indices: List[int] = None
    ) -> Dict[str, SobolIndices]:
        """
        Compute Sobol sensitivity indices using variance-based method.
        
        Uses the Saltelli sampling scheme:
        - Generate two base samples: A (N, d), B (N, d)
        - Create N*(2d+2) evaluations for Sobol
        - Compute S1 and ST indices with confidence intervals
        
        Args:
            n_samples: Base sample size N (total evals ≈ N*(2*d+2))
            output_indices: Indices of outputs to analyze [0,1,2]
                           [0: consumption, 1: comfort, 2: peak]
                           Default: all 3 outputs
            
        Returns:
            Dict mapping output names to SobolIndices
        """
        if output_indices is None:
            output_indices = [0, 1, 2]
        
        output_names = ['annual_consumption_kwh', 'comfort_hours', 'peak_cooling_kw']
        
        logger.info(f"Starting Sobol analysis: N={n_samples}, d={self.n_params}")
        logger.info(f"Total surrogate evaluations: {n_samples * (2 * self.n_params + 2)}")
        
        # Generate base samples in [0,1]
        A = np.random.rand(n_samples, self.n_params)
        B = np.random.rand(n_samples, self.n_params)
        
        # Denormalize to physical bounds
        A_phys = self._denormalize_params(A)
        B_phys = self._denormalize_params(B)
        
        # Evaluate base samples
        fA = self._evaluate_samples(A_phys)  # (n_samples, 3)
        fB = self._evaluate_samples(B_phys)  # (n_samples, 3)
        
        logger.info(f"Evaluated base samples: fA shape {fA.shape}, fB shape {fB.shape}")
        
        # Generate Sobol matrices
        # Create C_i matrices: swap i-th column of A with B
        sobol_samples = []
        sobol_indices = {'AC': [], 'BC': []}  # Store indices for later
        
        for i in range(self.n_params):
            # C_i = A with i-th column from B
            C = A.copy()
            C[:, i] = B[:, i]
            C_phys = self._denormalize_params(C)
            sobol_samples.append(C_phys)
            sobol_indices['AC'].append(i)
            
            # For Saltelli scheme, also compute AB_i (B with A's i-th)
            # This is optional but improves convergence
        
        # Combine all samples: [A, B, C1, C2, ..., Cd]
        X_sobol = np.vstack([A_phys, B_phys] + sobol_samples)
        f_sobol = self._evaluate_samples(X_sobol)
        
        # Split results
        fA = f_sobol[:n_samples]
        fB = f_sobol[n_samples:2*n_samples]
        fC = f_sobol[2*n_samples:]  # Shape: (n_params*n_samples, 3)
        
        logger.info(f"Evaluations complete. Computing indices...")
        
        # Compute Sobol indices for each output
        results = {}
        
        for out_idx, out_name in enumerate(output_names):
            if out_idx not in output_indices:
                continue
            
            f_A = fA[:, out_idx]
            f_B = fB[:, out_idx]
            
            # Total variance
            f_all = np.concatenate([f_A, f_B, fC[:, out_idx]])
            V = np.var(f_all, ddof=1)
            
            if V == 0:
                logger.warning(f"Zero variance for {out_name}, skipping")
                continue
            
            # Compute indices for each parameter
            S1 = {}
            ST = {}
            S1_conf = {}
            ST_conf = {}
            
            for i in range(self.n_params):
                param_name = self.parameter_names[i]
                f_C_i = fC[i*n_samples:(i+1)*n_samples, out_idx]
                
                # First-order index: S1_i = Var_X_i(E_X~i(Y|X_i)) / V
                # Approximation: S1 = (1/N * sum(f_B * (f_C - f_A))) / V
                S1_i = np.mean(f_B * (f_C_i - f_A)) / V
                S1[param_name] = float(max(0, S1_i))  # Clip to [0, 1]
                
                # Confidence interval (bootstrapped)
                S1_samples = []
                for boot in range(100):
                    idx = np.random.choice(n_samples, n_samples, replace=True)
                    S1_boot = np.mean(f_B[idx] * (f_C_i[idx] - f_A[idx])) / V
                    S1_samples.append(S1_boot)
                S1_conf[param_name] = float(np.std(S1_samples))
                
                # Total-order index: ST_i = 1 - Var_X~i(E_X_i(Y|X~i)) / V
                # Approximation: ST = (1/2N * sum((f_A - f_C)^2)) / V
                ST_i = np.mean((f_A - f_C_i) ** 2) / (2 * V)
                ST[param_name] = float(min(1, ST_i))  # Clip to [0, 1]
                
                # Confidence interval (bootstrapped)
                ST_samples = []
                for boot in range(100):
                    idx = np.random.choice(n_samples, n_samples, replace=True)
                    ST_boot = np.mean((f_A[idx] - f_C_i[idx]) ** 2) / (2 * V)
                    ST_samples.append(ST_boot)
                ST_conf[param_name] = float(np.std(ST_samples))
            
            # Store results
            results[out_name] = SobolIndices(
                output_name=out_name,
                S1=S1,
                ST=ST,
                S1_conf=S1_conf,
                ST_conf=ST_conf,
                n_samples=n_samples
            )
            
            logger.info(f"Sobol indices computed for {out_name}")
            logger.info(f"  Top 5 S1: {sorted(S1.items(), key=lambda x: x[1], reverse=True)[:5]}")
            logger.info(f"  Top 5 ST: {sorted(ST.items(), key=lambda x: x[1], reverse=True)[:5]}")
        
        self.sobol_results = results
        return results
    
    def morris_screening(
        self,
        n_trajectories: int = 100,
        n_levels: int = 10,
        output_indices: List[int] = None
    ) -> Dict[str, MorrisMetrics]:
        """
        One-At-a-Time (OAT) Morris screening method.
        
        Generates trajectories through parameter space, computing elementary
        effects (EE) for each parameter along each trajectory. Results in:
        - μ: Mean EE (main effect magnitude)
        - σ: Std of EE (interaction/nonlinearity)
        
        Args:
            n_trajectories: Number of random trajectories
            n_levels: Number of discretization levels (typically 4 or 10)
            output_indices: Indices of outputs [0,1,2] default all
            
        Returns:
            Dict mapping output names to MorrisMetrics
        """
        if output_indices is None:
            output_indices = [0, 1, 2]
        
        output_names = ['annual_consumption_kwh', 'comfort_hours', 'peak_cooling_kw']
        
        logger.info(f"Starting Morris screening: trajectories={n_trajectories}, "
                   f"levels={n_levels}")
        logger.info(f"Total surrogate evaluations: {n_trajectories * (self.n_params + 1)}")
        
        # Grid spacing
        delta = 1 / (n_levels - 1)
        
        # Generate trajectories
        X_morris = []
        trajectory_evals = []
        
        for traj in range(n_trajectories):
            if traj % 20 == 0:
                logger.info(f"  Generating trajectory {traj}/{n_trajectories}")
            
            # Random starting point
            x = np.random.rand(self.n_params)
            traj_samples = [x.copy()]
            
            # Random ordering of parameters
            param_order = np.random.permutation(self.n_params)
            
            for param_idx in param_order:
                # Perturb parameter by ±delta
                x_new = x.copy()
                # Random direction (up or down)
                direction = np.random.choice([-1, 1])
                # Ensure within bounds
                x_new[param_idx] = np.clip(x[param_idx] + direction * delta, 0, 1)
                traj_samples.append(x_new.copy())
                x = x_new
            
            X_morris.extend(traj_samples)
            trajectory_evals.append(len(traj_samples))
        
        X_morris = np.array(X_morris)
        X_morris_phys = self._denormalize_params(X_morris)
        
        logger.info(f"Evaluating {len(X_morris)} samples...")
        f_morris = self._evaluate_samples(X_morris_phys)
        
        # Compute elementary effects for each trajectory
        results = {}
        
        for out_idx, out_name in enumerate(output_names):
            if out_idx not in output_indices:
                continue
            
            logger.info(f"Computing Morris metrics for {out_name}...")
            
            # Store EE for each parameter and trajectory
            EE = {param_name: [] for param_name in self.parameter_names}
            
            idx = 0
            for traj in range(n_trajectories):
                traj_len = trajectory_evals[traj]
                f_traj = f_morris[idx:idx+traj_len, out_idx]
                
                # Elementary effects: |f(x+step) - f(x)| / step
                for step in range(self.n_params):
                    param_name = self.parameter_names[step]
                    ee = abs(f_traj[step+1] - f_traj[step]) / delta
                    EE[param_name].append(ee)
                
                idx += traj_len
            
            # Compute statistics
            mu = {}
            sigma = {}
            mu_star = {}
            
            for param_name in self.parameter_names:
                ee_array = np.array(EE[param_name])
                mu[param_name] = float(np.mean(ee_array))
                sigma[param_name] = float(np.std(ee_array))
                mu_star[param_name] = float(np.mean(np.abs(ee_array)))
            
            # Store results
            results[out_name] = MorrisMetrics(
                output_name=out_name,
                mu=mu,
                sigma=sigma,
                mu_star=mu_star,
                n_trajectories=n_trajectories
            )
            
            logger.info(f"Morris metrics computed for {out_name}")
            logger.info(f"  Top 5 μ*: {sorted(mu_star.items(), key=lambda x: x[1], reverse=True)[:5]}")
        
        self.morris_results = results
        return results
    
    def save_results(self):
        """Save sensitivity analysis results to disk."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save Sobol indices
        if self.sobol_results:
            sobol_data = []
            for out_name, indices in self.sobol_results.items():
                for param_name in self.parameter_names:
                    sobol_data.append({
                        'output': out_name,
                        'parameter': param_name,
                        'S1': indices.S1.get(param_name, 0),
                        'S1_conf': indices.S1_conf.get(param_name, 0),
                        'ST': indices.ST.get(param_name, 0),
                        'ST_conf': indices.ST_conf.get(param_name, 0),
                        'interaction': indices.ST.get(param_name, 0) - indices.S1.get(param_name, 0)
                    })
            
            sobol_df = pd.DataFrame(sobol_data)
            sobol_csv = self.output_dir / f"sobol_indices_{timestamp}.csv"
            sobol_df.to_csv(sobol_csv, index=False)
            logger.info(f"Saved Sobol indices to {sobol_csv}")
        
        # Save Morris metrics
        if self.morris_results:
            morris_data = []
            for out_name, metrics in self.morris_results.items():
                for param_name in self.parameter_names:
                    morris_data.append({
                        'output': out_name,
                        'parameter': param_name,
                        'mu': metrics.mu.get(param_name, 0),
                        'sigma': metrics.sigma.get(param_name, 0),
                        'mu_star': metrics.mu_star.get(param_name, 0)
                    })
            
            morris_df = pd.DataFrame(morris_data)
            morris_csv = self.output_dir / f"morris_screening_{timestamp}.csv"
            morris_df.to_csv(morris_csv, index=False)
            logger.info(f"Saved Morris metrics to {morris_csv}")
        
        # Save parameter ranking (combined Sobol + Morris)
        if self.sobol_results:
            output_name = 'annual_consumption_kwh'
            if output_name in self.sobol_results:
                sobol = self.sobol_results[output_name]
                morris = self.morris_results.get(output_name)
                
                ranking_data = []
                for param_name in self.parameter_names:
                    rank_entry = {
                        'parameter': param_name,
                        'sobol_S1': sobol.S1.get(param_name, 0),
                        'sobol_ST': sobol.ST.get(param_name, 0),
                    }
                    if morris:
                        rank_entry['morris_mu_star'] = morris.mu_star.get(param_name, 0)
                    ranking_data.append(rank_entry)
                
                ranking_df = pd.DataFrame(ranking_data)
                # Sort by Sobol ST (total effect)
                ranking_df = ranking_df.sort_values('sobol_ST', ascending=False)
                
                ranking_csv = self.output_dir / f"parameter_ranking_{timestamp}.csv"
                ranking_df.to_csv(ranking_csv, index=False)
                logger.info(f"Saved parameter ranking to {ranking_csv}")
    
    def plot_sobol_indices(self, output_name: str = 'annual_consumption_kwh'):
        """Create Sobol indices visualization."""
        if output_name not in self.sobol_results:
            logger.warning(f"No Sobol results for {output_name}")
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        sobol = self.sobol_results[output_name]
        
        # Prepare data sorted by ST
        params_sorted = sorted(sobol.ST.items(), key=lambda x: x[1], reverse=True)
        param_names_sorted = [p[0] for p in params_sorted]
        S1_sorted = [sobol.S1[p] for p in param_names_sorted]
        ST_sorted = [sobol.ST[p] for p in param_names_sorted]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # S1 plot
        ax1.barh(param_names_sorted, S1_sorted, color='steelblue', alpha=0.7)
        ax1.set_xlabel('S1 (First-Order Index)')
        ax1.set_title(f'Sobol First-Order Effects\n{output_name}')
        ax1.grid(True, alpha=0.3, axis='x')
        
        # ST plot
        ax2.barh(param_names_sorted, ST_sorted, color='coral', alpha=0.7)
        ax2.set_xlabel('ST (Total-Order Index)')
        ax2.set_title(f'Sobol Total-Order Effects\n{output_name}')
        ax2.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        
        output_path = self.output_dir / f"sobol_indices_{timestamp}.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved Sobol plot to {output_path}")
        plt.close()
    
    def plot_morris_screening(self, output_name: str = 'annual_consumption_kwh'):
        """Create Morris screening visualization (scatter plot)."""
        if output_name not in self.morris_results:
            logger.warning(f"No Morris results for {output_name}")
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        morris = self.morris_results[output_name]
        
        # Prepare data
        mu_array = np.array([morris.mu[p] for p in self.parameter_names])
        sigma_array = np.array([morris.sigma[p] for p in self.parameter_names])
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Scatter plot: mu vs sigma
        colors = ['red' if (mu_array[i] > np.percentile(mu_array, 75) and 
                            sigma_array[i] > np.percentile(sigma_array, 75))
                  else 'blue' for i in range(len(self.parameter_names))]
        
        ax.scatter(mu_array, sigma_array, s=100, c=colors, alpha=0.6, edgecolors='black')
        
        # Add labels
        for i, param in enumerate(self.parameter_names):
            ax.annotate(param, (mu_array[i], sigma_array[i]), 
                       xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        # Reference lines (median)
        ax.axvline(np.median(mu_array), color='gray', linestyle='--', alpha=0.5, label='Median μ')
        ax.axhline(np.median(sigma_array), color='gray', linestyle=':', alpha=0.5, label='Median σ')
        
        ax.set_xlabel('μ (Mean Elementary Effect)', fontsize=11)
        ax.set_ylabel('σ (Std of Elementary Effect)', fontsize=11)
        ax.set_title(f'Morris Screening Analysis\n{output_name}\nRed=High μ AND High σ (important+interactive)',
                    fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        output_path = self.output_dir / f"morris_screening_{timestamp}.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved Morris plot to {output_path}")
        plt.close()
    
    def plot_tornado_diagram(self, output_name: str = 'annual_consumption_kwh'):
        """Create tornado diagram comparing Sobol ST indices."""
        if output_name not in self.sobol_results:
            logger.warning(f"No Sobol results for {output_name}")
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        sobol = self.sobol_results[output_name]
        
        # Sort by ST
        params_sorted = sorted(sobol.ST.items(), key=lambda x: x[1], reverse=True)
        param_names = [p[0] for p in params_sorted]
        ST_values = [sobol.ST[p] for p in param_names]
        
        fig = go.Figure()
        
        # Add horizontal bar for ST
        fig.add_trace(go.Bar(
            y=param_names,
            x=ST_values,
            orientation='h',
            marker=dict(
                color=ST_values,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title='ST Index')
            ),
            text=[f'{v:.3f}' for v in ST_values],
            textposition='auto'
        ))
        
        fig.update_layout(
            title=f'Parameter Sensitivity Tornado Diagram<br>{output_name}',
            xaxis_title='Sobol ST (Total-Order Index)',
            yaxis_title='Parameter',
            height=600,
            showlegend=False
        )
        
        output_path = self.output_dir / f"tornado_diagram_{timestamp}.html"
        fig.write_html(str(output_path))
        logger.info(f"Saved tornado diagram to {output_path}")


def demo_sensitivity():
    """Demonstrate global sensitivity analysis."""
    logger.info("=" * 80)
    logger.info("Global Sensitivity Analysis - DEMO")
    logger.info("=" * 80)
    
    # Parameter bounds (same as NSGA-II)
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
    
    # Load surrogate
    models_dir = Path("Science AI Engineering/mes4_piml/models")
    surrogate_path = models_dir / "surrogate_xgboost.pkl"
    
    # Initialize analyzer
    analyzer = GlobalSensitivityAnalyzer(
        surrogate_model_path=surrogate_path,
        parameter_bounds=parameter_bounds,
        output_dir=Path("Science AI Engineering/mes8_optimization/results/sensitivity")
    )
    
    # Sobol analysis
    logger.info("\n" + "=" * 80)
    logger.info("SOBOL ANALYSIS (Variance-based)")
    logger.info("=" * 80)
    sobol_results = analyzer.sobol_analysis(n_samples=512)
    
    # Morris screening
    logger.info("\n" + "=" * 80)
    logger.info("MORRIS SCREENING (One-at-a-time)")
    logger.info("=" * 80)
    morris_results = analyzer.morris_screening(n_trajectories=50)
    
    # Save results
    analyzer.save_results()
    
    # Generate visualizations
    logger.info("\n" + "=" * 80)
    logger.info("GENERATING VISUALIZATIONS")
    logger.info("=" * 80)
    analyzer.plot_sobol_indices('annual_consumption_kwh')
    analyzer.plot_morris_screening('annual_consumption_kwh')
    analyzer.plot_tornado_diagram('annual_consumption_kwh')
    
    # Summary
    logger.info("\n" + "=" * 80)
    logger.info("SENSITIVITY ANALYSIS SUMMARY")
    logger.info("=" * 80)
    
    sobol = sobol_results.get('annual_consumption_kwh')
    if sobol:
        logger.info("\nSobol Total-Order (ST) - Top 5 Parameters:")
        for i, (param, value) in enumerate(sorted(sobol.ST.items(), 
                                                  key=lambda x: x[1], reverse=True)[:5], 1):
            logger.info(f"  {i}. {param}: {value:.4f}")
    
    morris = morris_results.get('annual_consumption_kwh')
    if morris:
        logger.info("\nMorris μ* (Main Effect) - Top 5 Parameters:")
        for i, (param, value) in enumerate(sorted(morris.mu_star.items(), 
                                                  key=lambda x: x[1], reverse=True)[:5], 1):
            logger.info(f"  {i}. {param}: {value:.4f}")
    
    logger.info("\n" + "=" * 80)
    logger.info("DEMO COMPLETE")
    logger.info("=" * 80)


if __name__ == "__main__":
    demo_sensitivity()
