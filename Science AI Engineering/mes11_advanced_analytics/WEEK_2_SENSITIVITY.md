# Mês 11 Week 2: Sensitivity Analysis & Feature Importance

## Overview
**Duration**: 12-15 hours  
**Objective**: Understand parameter sensitivity, feature importance, and interaction effects  
**Deliverable**: Complete sensitivity analysis suite (1D, 2D, SHAP, interaction effects)  
**Tech Stack**: SHAP, scikit-learn, Optuna, Matplotlib, Pandas

---

## Exercise 2.1: Feature Importance with SHAP

### Learning Objectives
- Interpret model decisions using SHAP values
- Identify most influential parameters in optimization
- Create interpretable visualizations of parameter impact

### Implementation Guide

**Create `feature_importance.py`:**

```python
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Callable
import matplotlib.pyplot as plt
import shap


class FeatureImportanceAnalyzer:
    """Feature importance using SHAP and permutation methods"""
    
    def __init__(self, model: Callable, X: np.ndarray, feature_names: List[str]):
        """
        Args:
            model: Callable that takes X array and returns predictions
            X: Feature matrix (n_samples, n_features)
            feature_names: Names of features
        """
        self.model = model
        self.X = X
        self.feature_names = feature_names
        self.n_features = len(feature_names)
        self.shap_values = None
        self.explainer = None
    
    def compute_shap_values(self, method: str = 'kernel'):
        """
        Compute SHAP values
        
        Args:
            method: 'kernel' (model-agnostic), 'tree' (for tree models), 'linear' (for linear)
        """
        if method == 'kernel':
            self.explainer = shap.KernelExplainer(self.model, shap.sample(self.X, 50))
            self.shap_values = self.explainer.shap_values(self.X[:100])  # Sample for speed
        else:
            raise NotImplementedError(f"Method {method} not yet implemented")
        
        return self.shap_values
    
    def summary_plot(self, figsize=(10, 6)):
        """SHAP summary plot (bar chart of mean |SHAP|)"""
        if self.shap_values is None:
            self.compute_shap_values()
        
        fig, ax = plt.subplots(figsize=figsize)
        
        mean_abs_shap = np.abs(self.shap_values).mean(axis=0)
        sorted_idx = np.argsort(mean_abs_shap)[::-1]
        
        sorted_names = [self.feature_names[i] for i in sorted_idx]
        sorted_values = mean_abs_shap[sorted_idx]
        
        ax.barh(sorted_names, sorted_values, color='steelblue')
        ax.set_xlabel('Mean |SHAP value|')
        ax.set_title('Feature Importance (SHAP)')
        ax.grid(True, alpha=0.3, axis='x')
        
        return fig
    
    def dependence_plot(self, feature_idx: int, figsize=(10, 6)):
        """Relationship between feature value and SHAP impact"""
        if self.shap_values is None:
            self.compute_shap_values()
        
        fig, ax = plt.subplots(figsize=figsize)
        
        ax.scatter(self.X[:, feature_idx], self.shap_values[:, feature_idx], alpha=0.6)
        ax.set_xlabel(self.feature_names[feature_idx])
        ax.set_ylabel(f'SHAP value for {self.feature_names[feature_idx]}')
        ax.set_title(f'Dependence Plot: {self.feature_names[feature_idx]}')
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def permutation_importance(self, X_test: np.ndarray, y_test: np.ndarray,
                              n_repeats: int = 10) -> Dict[str, float]:
        """
        Permutation-based feature importance
        
        Args:
            X_test: Test features
            y_test: Test targets
            n_repeats: Number of permutation repeats
        
        Returns:
            Dict mapping feature name to importance score
        """
        baseline_score = np.mean((self.model(X_test) - y_test) ** 2)
        
        importances = {}
        
        for feature_idx in range(self.n_features):
            scores = []
            
            for _ in range(n_repeats):
                X_permuted = X_test.copy()
                np.random.shuffle(X_permuted[:, feature_idx])
                
                permuted_score = np.mean((self.model(X_permuted) - y_test) ** 2)
                scores.append(permuted_score - baseline_score)
            
            importances[self.feature_names[feature_idx]] = np.mean(scores)
        
        return importances
    
    def plot_permutation_importance(self, importances: Dict[str, float], figsize=(10, 6)):
        """Visualize permutation importance"""
        fig, ax = plt.subplots(figsize=figsize)
        
        sorted_items = sorted(importances.items(), key=lambda x: x[1], reverse=True)
        names, values = zip(*sorted_items)
        
        ax.barh(names, values, color='coral')
        ax.set_xlabel('Importance (MSE increase)')
        ax.set_title('Permutation Importance')
        ax.grid(True, alpha=0.3, axis='x')
        
        return fig
    
    def top_k_important_features(self, k: int = 5) -> List[Tuple[str, float]]:
        """Get top k most important features"""
        if self.shap_values is None:
            self.compute_shap_values()
        
        mean_abs_shap = np.abs(self.shap_values).mean(axis=0)
        sorted_idx = np.argsort(mean_abs_shap)[::-1]
        
        top_features = [
            (self.feature_names[idx], mean_abs_shap[idx])
            for idx in sorted_idx[:k]
        ]
        
        return top_features


# Example usage
if __name__ == "__main__":
    # Mock model and data
    np.random.seed(42)
    n_samples = 1000
    
    X = np.random.randn(n_samples, 5)
    feature_names = ['temperature', 'pressure', 'velocity', 'cost', 'efficiency']
    
    # Synthetic relationship: y = 2*temp - pressure + 0.5*velocity
    y = 2 * X[:, 0] - X[:, 1] + 0.5 * X[:, 2] + np.random.randn(n_samples) * 0.1
    
    def mock_model(X):
        return 2 * X[:, 0] - X[:, 1] + 0.5 * X[:, 2]
    
    analyzer = FeatureImportanceAnalyzer(mock_model, X, feature_names)
    
    # SHAP analysis
    shap_values = analyzer.compute_shap_values()
    print("Top 3 important features:", analyzer.top_k_important_features(3))
    
    # Permutation importance
    perms = analyzer.permutation_importance(X, y)
    print("Permutation importance:", perms)
    
    # Plots
    fig1 = analyzer.summary_plot()
    fig2 = analyzer.dependence_plot(0)
    fig3 = analyzer.plot_permutation_importance(perms)
    
    plt.show()
```

### Checkpoint Requirements

- [ ] **SHAP Computation**: Values computed and validated for sample dataset
- [ ] **Summary Plot**: Bar chart showing mean |SHAP| for all features
- [ ] **Dependence Plots**: Relationship visualizations for top 3 features
- [ ] **Permutation Importance**: Calculated and ranked correctly
- [ ] **Top Features**: Identified and validated with domain knowledge

---

## Exercise 2.2: One-Way Sensitivity Analysis

### Learning Objectives
- Vary single parameters to understand individual impact
- Create sensitivity curves and identify non-linearities
- Determine parameter ranges of interest

### Implementation Guide

**Create `sensitivity_1d.py`:**

```python
import numpy as np
import pandas as pd
from typing import Dict, List, Callable, Tuple
import matplotlib.pyplot as plt


class SensitivityAnalyzer1D:
    """One-dimensional sensitivity analysis"""
    
    def __init__(self, objective_fn: Callable, base_config: Dict[str, float]):
        """
        Args:
            objective_fn: Function(config) -> scalar
            base_config: Baseline parameter configuration
        """
        self.objective_fn = objective_fn
        self.base_config = base_config.copy()
        self.sensitivity_data = {}
    
    def analyze_parameter(self, param_name: str, param_range: np.ndarray,
                         label: str = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Vary single parameter, measure output
        
        Args:
            param_name: Parameter to vary
            param_range: Array of values to test
            label: Display label for parameter
        
        Returns:
            Tuple of (param_values, objective_values)
        """
        results = []
        
        for value in param_range:
            config = self.base_config.copy()
            config[param_name] = value
            
            try:
                obj_value = self.objective_fn(config)
                results.append(obj_value)
            except Exception as e:
                results.append(np.nan)
        
        results = np.array(results)
        self.sensitivity_data[param_name] = {
            'range': param_range,
            'results': results,
            'label': label or param_name
        }
        
        return param_range, results
    
    def tornado_diagram(self, figsize=(12, 8)):
        """Tornado chart showing parameter sensitivity magnitude"""
        if not self.sensitivity_data:
            print("No sensitivity data. Run analyze_parameter first.")
            return None
        
        fig, ax = plt.subplots(figsize=figsize)
        
        sensitivities = []
        param_names = []
        
        for param_name, data in self.sensitivity_data.items():
            # Range of outputs
            valid_results = data['results'][~np.isnan(data['results'])]
            
            if len(valid_results) > 0:
                sensitivity = np.nanmax(valid_results) - np.nanmin(valid_results)
                sensitivities.append(sensitivity)
                param_names.append(data['label'])
        
        # Sort by magnitude
        sorted_idx = np.argsort(sensitivities)[::-1]
        sorted_names = [param_names[i] for i in sorted_idx]
        sorted_sens = [sensitivities[i] for i in sorted_idx]
        
        ax.barh(sorted_names, sorted_sens, color='steelblue')
        ax.set_xlabel('Output Range (Max - Min)')
        ax.set_title('Tornado Diagram: Parameter Sensitivity')
        ax.grid(True, alpha=0.3, axis='x')
        
        return fig
    
    def sensitivity_curves(self, figsize=(15, 10)):
        """Plot sensitivity curve for each parameter"""
        if not self.sensitivity_data:
            return None
        
        n_params = len(self.sensitivity_data)
        n_cols = 3
        n_rows = (n_params + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        axes = axes.flatten()
        
        for idx, (param_name, data) in enumerate(self.sensitivity_data.items()):
            ax = axes[idx]
            
            # Plot with error handling for NaN
            valid_mask = ~np.isnan(data['results'])
            valid_range = data['range'][valid_mask]
            valid_results = data['results'][valid_mask]
            
            ax.plot(valid_range, valid_results, marker='o', linewidth=2, markersize=4)
            ax.fill_between(valid_range, valid_results, alpha=0.3)
            
            ax.set_xlabel(data['label'])
            ax.set_ylabel('Objective Value')
            ax.set_title(f'Sensitivity: {data["label"]}')
            ax.grid(True, alpha=0.3)
        
        # Hide unused subplots
        for idx in range(n_params, len(axes)):
            fig.delaxes(axes[idx])
        
        fig.suptitle('One-Way Sensitivity Analysis', fontsize=14)
        fig.tight_layout()
        
        return fig
    
    def elasticity_analysis(self) -> Dict[str, float]:
        """
        Compute elasticity for each parameter
        Elasticity = (% change in output) / (% change in input)
        """
        elasticities = {}
        baseline_output = self.objective_fn(self.base_config)
        
        for param_name, data in self.sensitivity_data.items():
            if param_name not in self.base_config:
                continue
            
            baseline_input = self.base_config[param_name]
            
            valid_mask = ~np.isnan(data['results'])
            valid_range = data['range'][valid_mask]
            valid_results = data['results'][valid_mask]
            
            if len(valid_results) < 2:
                continue
            
            # Compute elasticity at baseline (if available)
            closest_idx = np.argmin(np.abs(valid_range - baseline_input))
            output_at_baseline = valid_results[closest_idx]
            
            if closest_idx > 0:
                # Use central difference if possible
                dx = valid_range[closest_idx] - valid_range[closest_idx - 1]
                dy = valid_results[closest_idx] - valid_results[closest_idx - 1]
            elif closest_idx < len(valid_range) - 1:
                dx = valid_range[closest_idx + 1] - valid_range[closest_idx]
                dy = valid_results[closest_idx + 1] - valid_results[closest_idx]
            else:
                continue
            
            if baseline_input != 0 and dy != 0:
                elasticity = (dy / output_at_baseline) / (dx / baseline_input)
                elasticities[param_name] = elasticity
        
        return elasticities
    
    def get_sensitivity_dataframe(self) -> pd.DataFrame:
        """Return all sensitivity analysis as DataFrame"""
        df = None
        
        for param_name, data in self.sensitivity_data.items():
            col_name = data['label']
            param_df = pd.DataFrame({
                col_name: data['range'],
                f'{col_name}_output': data['results']
            })
            
            if df is None:
                df = param_df
            else:
                df[col_name] = data['range']
                df[f'{col_name}_output'] = data['results']
        
        return df


# Example usage
if __name__ == "__main__":
    def objective(config):
        """Mock objective function"""
        return (config['x'] - 5) ** 2 + 2 * (config['y'] - 10) ** 2 + 0.5 * config['z']
    
    base_config = {'x': 5.0, 'y': 10.0, 'z': 0.0}
    analyzer = SensitivityAnalyzer1D(objective, base_config)
    
    # Analyze parameters
    analyzer.analyze_parameter('x', np.linspace(0, 10, 20), label='Parameter X')
    analyzer.analyze_parameter('y', np.linspace(5, 15, 20), label='Parameter Y')
    analyzer.analyze_parameter('z', np.linspace(-5, 5, 20), label='Parameter Z')
    
    # Results
    print("Elasticity analysis:")
    print(analyzer.elasticity_analysis())
    
    # Visualizations
    fig1 = analyzer.tornado_diagram()
    fig2 = analyzer.sensitivity_curves()
    
    plt.show()
```

### Checkpoint Requirements

- [ ] **Parameter Sweep**: All 5+ parameters analyzed with 20+ points each
- [ ] **Tornado Diagram**: Sensitivity magnitude correctly ranked
- [ ] **Sensitivity Curves**: Non-linearities visible in plots
- [ ] **Elasticity**: Computed for at least 3 parameters
- [ ] **DataFrame Export**: Results saved to CSV for reporting

---

## Exercise 2.3: Interaction Effects (2D Sensitivity)

### Learning Objectives
- Identify parameter synergies and conflicts
- Quantify interaction magnitudes
- Create heatmaps showing 2D parameter spaces

### Implementation Guide

**Create `sensitivity_2d.py`:**

```python
import numpy as np
import pandas as pd
from typing import Dict, Callable, Tuple
import matplotlib.pyplot as plt
from scipy.interpolate import griddata


class SensitivityAnalyzer2D:
    """Two-dimensional sensitivity and interaction analysis"""
    
    def __init__(self, objective_fn: Callable, base_config: Dict[str, float]):
        self.objective_fn = objective_fn
        self.base_config = base_config.copy()
        self.interaction_data = {}
    
    def analyze_interaction(self, param1: str, param1_range: np.ndarray,
                           param2: str, param2_range: np.ndarray,
                           label1: str = None, label2: str = None) -> np.ndarray:
        """
        Analyze interaction between two parameters
        
        Args:
            param1, param2: Parameter names
            param1_range, param2_range: Value ranges to test
            label1, label2: Display labels
        
        Returns:
            2D array of objective values
        """
        label1 = label1 or param1
        label2 = label2 or param2
        
        results = np.zeros((len(param2_range), len(param1_range)))
        
        for i, val2 in enumerate(param2_range):
            for j, val1 in enumerate(param1_range):
                config = self.base_config.copy()
                config[param1] = val1
                config[param2] = val2
                
                try:
                    results[i, j] = self.objective_fn(config)
                except:
                    results[i, j] = np.nan
        
        self.interaction_data[f'{param1}_vs_{param2}'] = {
            'param1': param1,
            'param2': param2,
            'label1': label1,
            'label2': label2,
            'range1': param1_range,
            'range2': param2_range,
            'results': results
        }
        
        return results
    
    def interaction_heatmap(self, param1: str, param2: str, figsize=(10, 8)):
        """Heatmap of 2D interaction"""
        key = f'{param1}_vs_{param2}'
        
        if key not in self.interaction_data:
            print(f"No interaction data for {key}")
            return None
        
        data = self.interaction_data[key]
        
        fig, ax = plt.subplots(figsize=figsize)
        
        im = ax.contourf(data['range1'], data['range2'], data['results'], 
                         levels=20, cmap='RdYlBu_r')
        
        ax.set_xlabel(data['label1'])
        ax.set_ylabel(data['label2'])
        ax.set_title(f'Interaction: {data["label1"]} vs {data["label2"]}')
        
        cbar = fig.colorbar(im, ax=ax)
        cbar.set_label('Objective Value')
        
        return fig
    
    def interaction_contour(self, param1: str, param2: str, figsize=(10, 8)):
        """Contour plot of interaction"""
        key = f'{param1}_vs_{param2}'
        
        if key not in self.interaction_data:
            return None
        
        data = self.interaction_data[key]
        
        fig, ax = plt.subplots(figsize=figsize)
        
        contours = ax.contour(data['range1'], data['range2'], data['results'],
                             levels=10, colors='black', linewidths=0.5)
        ax.clabel(contours, inline=True, fontsize=8)
        
        contourf = ax.contourf(data['range1'], data['range2'], data['results'],
                              levels=20, cmap='viridis')
        
        ax.set_xlabel(data['label1'])
        ax.set_ylabel(data['label2'])
        ax.set_title(f'Contour Plot: {data["label1"]} vs {data["label2"]}')
        
        cbar = fig.colorbar(contourf, ax=ax)
        cbar.set_label('Objective Value')
        
        return fig
    
    def quantify_interaction(self, param1: str, param2: str) -> float:
        """
        Quantify interaction strength using ANOVA decomposition
        Higher = stronger interaction
        """
        key = f'{param1}_vs_{param2}'
        
        if key not in self.interaction_data:
            return 0.0
        
        data = self.interaction_data[key]
        results = data['results']
        
        # Total variance
        total_mean = np.nanmean(results)
        total_var = np.nansum((results - total_mean) ** 2)
        
        # Main effect 1
        main1_effects = np.nanmean(results, axis=0)
        main1_var = np.sum((main1_effects - total_mean) ** 2) * len(data['range2'])
        
        # Main effect 2
        main2_effects = np.nanmean(results, axis=1)
        main2_var = np.sum((main2_effects - total_mean) ** 2) * len(data['range1'])
        
        # Interaction = Total - Main1 - Main2
        interaction_var = total_var - main1_var - main2_var
        
        # Interaction strength (0-1)
        interaction_strength = interaction_var / max(total_var, 1e-10)
        
        return max(0.0, interaction_strength)
    
    def find_optimal_region(self, param1: str, param2: str, 
                           percentile: float = 90) -> Dict:
        """Find region of parameter space with best performance"""
        key = f'{param1}_vs_{param2}'
        
        if key not in self.interaction_data:
            return {}
        
        data = self.interaction_data[key]
        threshold = np.nanpercentile(data['results'], 100 - percentile)
        
        optimal_mask = data['results'] <= threshold
        
        return {
            'param1_range': (
                np.min(data['range1'][np.any(optimal_mask, axis=0)]),
                np.max(data['range1'][np.any(optimal_mask, axis=0)])
            ),
            'param2_range': (
                np.min(data['range2'][np.any(optimal_mask, axis=1)]),
                np.max(data['range2'][np.any(optimal_mask, axis=1)])
            ),
            'threshold': threshold
        }


# Example usage
if __name__ == "__main__":
    def objective(config):
        """Mock objective with interactions"""
        x, y = config.get('x', 0), config.get('y', 0)
        # Add interaction term: x*y
        return (x - 3) ** 2 + (y - 4) ** 2 + 0.5 * x * y
    
    base_config = {'x': 3.0, 'y': 4.0}
    analyzer = SensitivityAnalyzer2D(objective, base_config)
    
    # Analyze interaction
    analyzer.analyze_interaction('x', np.linspace(0, 6, 20),
                                 'y', np.linspace(0, 8, 20),
                                 'Parameter X', 'Parameter Y')
    
    # Quantify
    interaction_strength = analyzer.quantify_interaction('x', 'y')
    print(f"Interaction strength: {interaction_strength:.4f}")
    
    # Find optimal region
    optimal = analyzer.find_optimal_region('x', 'y', percentile=80)
    print(f"Optimal region:\n{optimal}")
    
    # Visualize
    fig1 = analyzer.interaction_heatmap('x', 'y')
    fig2 = analyzer.interaction_contour('x', 'y')
    
    plt.show()
```

### Checkpoint Requirements

- [ ] **2D Parameter Sweeps**: 20×20 grid of evaluations for 2+ parameter pairs
- [ ] **Heatmaps**: Color-coded surface showing interaction patterns
- [ ] **Contour Maps**: Level curves identifying optimal regions
- [ ] **Interaction Quantification**: Strength score computed (0-1)
- [ ] **Optimal Regions**: Identified with threshold percentiles

---

## Summary & Certification

### Week 2 Deliverables

| Exercise | Component | Status |
|----------|-----------|--------|
| 2.1 | SHAP Analysis | Feature importance with summary plots |
| 2.2 | 1D Sensitivity | Tornado diagram, sensitivity curves, elasticity |
| 2.3 | 2D Interaction | Heatmaps, contours, quantified interactions |

### Validation Checklist

- [ ] All 3 exercises completed
- [ ] SHAP values computed for sample model
- [ ] Tornado diagram shows realistic parameter ranking
- [ ] Sensitivity curves reveal non-linearities
- [ ] Interaction heatmaps show clear patterns
- [ ] 100+ total evaluations across all analyses

### Next Steps

✅ **Week 2 Complete**: Move to [Week 3: Constrained Optimization](WEEK_3_CONSTRAINED.md)
