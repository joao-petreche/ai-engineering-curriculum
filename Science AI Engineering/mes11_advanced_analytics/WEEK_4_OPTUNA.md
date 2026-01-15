# Mês 11 Week 4: Hyperparameter Optimization & Advanced Analytics

## Overview
**Duration**: 12-15 hours  
**Objective**: Master Optuna framework for hyperparameter tuning and architecture search  
**Deliverable**: Complete Optuna pipeline with pruning, sampling, multi-trial optimization  
**Tech Stack**: Optuna, scikit-learn, Plotly, W&B, PostgreSQL

---

## Exercise 4.1: Optuna Framework Fundamentals

### Learning Objectives
- Define search spaces and objective functions for Optuna
- Run trials and manage study persistence
- Compare samplers and pruners

### Implementation Guide

**Create `optuna_optimizer.py`:**

```python
import optuna
from optuna.pruners import MedianPruner, PatientPruner
from optuna.samplers import TPESampler, RandomSampler, CmaEsSampler
import numpy as np
import pandas as pd
from typing import Dict, List, Callable, Optional
import sqlite3


class OptunaOptimizer:
    """Hyperparameter optimization using Optuna"""
    
    def __init__(self, study_name: str, storage: str = None, 
                 sampler_name: str = 'tpe'):
        """
        Args:
            study_name: Name of the study
            storage: SQLite path for persistence, or None for in-memory
            sampler_name: 'tpe', 'random', 'cmaes'
        """
        self.study_name = study_name
        self.storage = storage
        
        # Select sampler
        if sampler_name == 'tpe':
            sampler = TPESampler(seed=42)
        elif sampler_name == 'random':
            sampler = RandomSampler(seed=42)
        elif sampler_name == 'cmaes':
            sampler = CmaEsSampler(seed=42)
        else:
            sampler = TPESampler(seed=42)
        
        # Create study
        storage_url = f'sqlite:///{storage}' if storage else None
        self.study = optuna.create_study(
            study_name=study_name,
            storage=storage_url,
            sampler=sampler,
            load_if_exists=True,
            direction='minimize'
        )
        
        self.trial_history = []
    
    def optimize_sklearn_model(self, X_train, y_train, X_val, y_val,
                              n_trials: int = 50, timeout: int = None):
        """
        Optimize sklearn model hyperparameters
        """
        def objective(trial):
            # Hyperparameter search space
            params = {
                'max_depth': trial.suggest_int('max_depth', 3, 20),
                'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
                'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 10),
                'n_estimators': trial.suggest_int('n_estimators', 50, 500, step=50),
                'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
                'subsample': trial.suggest_float('subsample', 0.5, 1.0),
            }
            
            # Build and evaluate model
            from sklearn.ensemble import GradientBoostingRegressor
            
            model = GradientBoostingRegressor(**params, random_state=42)
            model.fit(X_train, y_train)
            
            # Validation score
            val_score = np.mean((model.predict(X_val) - y_val) ** 2)
            
            return val_score
        
        self.study.optimize(objective, n_trials=n_trials, timeout=timeout)
        
        return self.study.best_params
    
    def optimize_neural_network(self, X_train, y_train, X_val, y_val,
                               n_trials: int = 50):
        """
        Optimize neural network architecture
        """
        def objective(trial):
            # Architecture search space
            n_layers = trial.suggest_int('n_layers', 2, 4)
            layers = [
                trial.suggest_int(f'n_units_layer{i}', 32, 256, step=32)
                for i in range(n_layers)
            ]
            
            dropout_rate = trial.suggest_float('dropout_rate', 0.0, 0.5, step=0.1)
            learning_rate = trial.suggest_float('learning_rate', 1e-5, 1e-1, log=True)
            batch_size = trial.suggest_categorical('batch_size', [16, 32, 64, 128])
            
            # Build neural network
            import tensorflow as tf
            
            model = tf.keras.Sequential()
            for units in layers:
                model.add(tf.keras.layers.Dense(units, activation='relu'))
                model.add(tf.keras.layers.Dropout(dropout_rate))
            model.add(tf.keras.layers.Dense(1))
            
            optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
            model.compile(optimizer=optimizer, loss='mse')
            
            # Train
            history = model.fit(
                X_train, y_train,
                validation_data=(X_val, y_val),
                epochs=50,
                batch_size=batch_size,
                verbose=0,
                callbacks=[
                    tf.keras.callbacks.EarlyStopping(
                        monitor='val_loss',
                        patience=5,
                        restore_best_weights=True
                    )
                ]
            )
            
            return history.history['val_loss'][-1]
        
        self.study.optimize(objective, n_trials=n_trials)
        
        return self.study.best_params
    
    def get_best_trial(self) -> Dict:
        """Get best trial and its parameters"""
        best_trial = self.study.best_trial
        
        return {
            'trial_number': best_trial.number,
            'value': best_trial.value,
            'params': best_trial.params,
            'state': best_trial.state.name
        }
    
    def get_trials_dataframe(self) -> pd.DataFrame:
        """Convert trials to DataFrame"""
        trials_data = []
        
        for trial in self.study.trials:
            row = {
                'trial_id': trial.number,
                'value': trial.value,
                'state': trial.state.name,
            }
            row.update(trial.params)
            trials_data.append(row)
        
        return pd.DataFrame(trials_data)
    
    def plot_optimization_history(self):
        """Plot optimization progress"""
        import plotly.graph_objects as go
        
        trials_df = self.get_trials_dataframe()
        trials_df['best_value'] = trials_df['value'].cummin()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=trials_df['trial_id'],
            y=trials_df['value'],
            mode='markers',
            name='Trial Value',
            marker=dict(size=8, opacity=0.6)
        ))
        
        fig.add_trace(go.Scatter(
            x=trials_df['trial_id'],
            y=trials_df['best_value'],
            mode='lines',
            name='Best Value',
            line=dict(color='red', width=2)
        ))
        
        fig.update_layout(
            title='Optimization History',
            xaxis_title='Trial Number',
            yaxis_title='Objective Value',
            hovermode='x unified'
        )
        
        return fig
    
    def plot_parallel_coordinates(self):
        """Parallel coordinates plot of trials"""
        import plotly.express as px
        
        trials_df = self.get_trials_dataframe()
        
        # Select numeric columns
        numeric_cols = trials_df.select_dtypes(include=[np.number]).columns.tolist()
        
        fig = px.parallel_coordinates(
            trials_df,
            dimensions=numeric_cols[:10],  # Limit to 10 dimensions
            color='value',
            color_continuous_scale='Viridis'
        )
        
        return fig
    
    def export_to_wandb(self, project: str, entity: str = None):
        """Log optimization results to Weights & Biases"""
        import wandb
        
        wandb.init(project=project, entity=entity)
        
        best = self.get_best_trial()
        wandb.log({
            'best_value': best['value'],
            'best_trial': best['trial_number'],
            'total_trials': len(self.study.trials)
        })
        
        # Log hyperparameter importance
        importance = optuna.importance.get_param_importances(self.study)
        for param, imp in importance.items():
            wandb.log({f'importance_{param}': imp})
        
        wandb.finish()


# Example usage
if __name__ == "__main__":
    from sklearn.datasets import make_regression
    from sklearn.model_selection import train_test_split
    
    # Create dataset
    X, y = make_regression(n_samples=1000, n_features=20, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Optimize
    optimizer = OptunaOptimizer('sklearn_study', storage='optuna_studies.db')
    best_params = optimizer.optimize_sklearn_model(X_train, y_train, X_val, y_val, n_trials=30)
    
    print("Best parameters:", best_params)
    print("\nBest trial:")
    print(optimizer.get_best_trial())
    
    # Visualizations
    fig1 = optimizer.plot_optimization_history()
    fig2 = optimizer.plot_parallel_coordinates()
    
    fig1.show()
    fig2.show()
```

### Checkpoint Requirements

- [ ] **Study Creation**: Optuna study created and persisted
- [ ] **Objective Function**: Properly defined with search space
- [ ] **Trials**: 50+ trials completed
- [ ] **Best Params**: Retrieved and validated
- [ ] **Visualizations**: History and parallel coordinates plots working

---

## Exercise 4.2: Pruning & Early Stopping with Optuna

### Learning Objectives
- Implement pruning to stop unpromising trials early
- Use callbacks for trial monitoring
- Reduce optimization time by 30-50%

### Implementation Guide

**Create `optuna_pruning.py`:**

```python
import optuna
from optuna.pruners import MedianPruner, PercentilePruner
from optuna.exceptions import TrialPruned
import numpy as np
from typing import Callable


class PruningOptimizer:
    """Optuna with intelligent pruning strategies"""
    
    def __init__(self, pruner_type: str = 'median', n_startup_trials: int = 10):
        """
        Args:
            pruner_type: 'median', 'percentile', 'patient'
            n_startup_trials: Trials before pruning starts
        """
        if pruner_type == 'median':
            pruner = MedianPruner(n_startup_trials=n_startup_trials)
        elif pruner_type == 'percentile':
            pruner = PercentilePruner(percentile=25, n_startup_trials=n_startup_trials)
        else:
            pruner = MedianPruner(n_startup_trials=n_startup_trials)
        
        self.study = optuna.create_study(pruner=pruner)
        self.pruned_trials = 0
        self.completed_trials = 0
    
    def optimize_with_pruning(self, objective_fn: Callable, n_trials: int = 50):
        """
        Optimize with pruning for early stopping
        
        objective_fn should accept (trial, intermediate_values)
        """
        def objective(trial):
            try:
                return objective_fn(trial)
            except TrialPruned:
                self.pruned_trials += 1
                raise
            finally:
                if trial.should_prune():
                    self.pruned_trials += 1
        
        self.study.optimize(objective, n_trials=n_trials)
        self.completed_trials = len([t for t in self.study.trials 
                                    if t.state.name != 'PRUNED'])
    
    def optimization_efficiency(self) -> Dict:
        """Report pruning statistics"""
        total_trials = len(self.study.trials)
        
        return {
            'total_trials': total_trials,
            'pruned_trials': self.pruned_trials,
            'completed_trials': self.completed_trials,
            'pruning_rate': self.pruned_trials / total_trials if total_trials > 0 else 0,
            'best_value': self.study.best_value
        }


# Example with iterative evaluation
class IterativeOptimizer:
    """Optimizer with iterative evaluation (e.g., epochs)"""
    
    def objective_with_intermediate_values(self, trial, train_fn: Callable,
                                          val_fn: Callable, n_epochs: int = 100):
        """
        Objective function with periodic reporting for pruning
        """
        for epoch in range(n_epochs):
            # Train and validate
            train_loss = train_fn(trial.params)
            val_loss = val_fn(trial.params)
            
            # Report intermediate value (for pruning decision)
            trial.report(val_loss, epoch)
            
            # Check if trial should be pruned
            if trial.should_prune():
                raise optuna.exceptions.TrialPruned()
        
        return val_loss
    
    def optimize_iterative(self, objective_fn: Callable, n_trials: int = 50,
                          n_epochs: int = 100):
        """Run optimization with iterative evaluation"""
        pruner = MedianPruner(n_startup_trials=5)
        study = optuna.create_study(pruner=pruner)
        
        def wrapped_objective(trial):
            return objective_fn(trial, n_epochs)
        
        study.optimize(wrapped_objective, n_trials=n_trials)
        
        return study


# Example usage
if __name__ == "__main__":
    def simple_objective(trial):
        """Objective with pruning support"""
        x = trial.suggest_float('x', -10, 10)
        y = trial.suggest_float('y', -10, 10)
        
        # Simulate iterative computation
        for step in range(100):
            loss = (x - 3) ** 2 + (y - 4) ** 2 + np.random.randn() * 0.01
            
            # Report intermediate value
            trial.report(loss, step)
            
            # Check for pruning
            if trial.should_prune():
                raise optuna.TrialPruned()
        
        return loss
    
    optimizer = PruningOptimizer(pruner_type='median')
    optimizer.optimize_with_pruning(simple_objective, n_trials=50)
    
    stats = optimizer.optimization_efficiency()
    print("Optimization Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
```

### Checkpoint Requirements

- [ ] **Pruning Enabled**: MedianPruner or PercentilePruner active
- [ ] **Early Stopping**: 20%+ of trials pruned (unpromising ones)
- [ ] **Intermediate Reporting**: Values reported every epoch/iteration
- [ ] **Time Saved**: Optimization time reduced by 30%+ vs. no pruning
- [ ] **Statistics**: Pruning efficiency metrics calculated

---

## Exercise 4.3: Multi-Objective with Optuna

### Learning Objectives
- Optimize multiple conflicting objectives simultaneously
- Generate Pareto fronts with Optuna
- Handle trade-offs between objectives

### Implementation Guide

**Create `optuna_multiobjective.py`:**

```python
import optuna
from optuna.samplers import TPESampler
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class MultiObjectiveOptunaOptimizer:
    """Multi-objective optimization with Optuna"""
    
    def __init__(self, directions: list = None):
        """
        Args:
            directions: List of 'minimize' or 'maximize' for each objective
        """
        directions = directions or ['minimize', 'minimize']
        
        sampler = TPESampler(seed=42)
        self.study = optuna.create_study(
            directions=directions,
            sampler=sampler
        )
    
    def optimize(self, objective_fn, n_trials: int = 100):
        """
        Optimize with multiple objectives
        
        objective_fn should return tuple of (obj1, obj2, ...)
        """
        self.study.optimize(objective_fn, n_trials=n_trials)
    
    def get_pareto_front(self) -> pd.DataFrame:
        """Get non-dominated solutions"""
        trials_df = pd.DataFrame([
            {
                'trial_id': t.number,
                'values': t.values,
                'params': t.params
            }
            for t in self.study.best_trials
        ])
        
        return trials_df
    
    def plot_pareto_front_2d(self, obj1_idx: int = 0, obj2_idx: int = 1):
        """Plot 2D Pareto front"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # All trials
        all_values = [t.values for t in self.study.trials]
        all_obj1 = [v[obj1_idx] for v in all_values]
        all_obj2 = [v[obj2_idx] for v in all_values]
        
        ax.scatter(all_obj1, all_obj2, alpha=0.3, s=30, label='All trials')
        
        # Pareto front
        pareto_values = [t.values for t in self.study.best_trials]
        pareto_obj1 = [v[obj1_idx] for v in pareto_values]
        pareto_obj2 = [v[obj2_idx] for v in pareto_values]
        
        ax.scatter(pareto_obj1, pareto_obj2, color='red', s=100, 
                  marker='*', label='Pareto Front', zorder=5)
        
        ax.set_xlabel(f'Objective {obj1_idx + 1}')
        ax.set_ylabel(f'Objective {obj2_idx + 1}')
        ax.set_title('Pareto Front (2D)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        return fig


# Example usage
if __name__ == "__main__":
    def multi_objective(trial):
        """Minimize cost while maximizing quality"""
        x = trial.suggest_float('x', 0, 10)
        y = trial.suggest_float('y', 0, 10)
        
        cost = (x - 3) ** 2 + (y - 4) ** 2
        quality = -(x - 5) ** 2 - (y - 6) ** 2 + 100
        
        return cost, quality
    
    optimizer = MultiObjectiveOptunaOptimizer(
        directions=['minimize', 'maximize']
    )
    optimizer.optimize(multi_objective, n_trials=100)
    
    # Results
    pareto_df = optimizer.get_pareto_front()
    print("Pareto Front Size:", len(pareto_df))
    print(pareto_df)
    
    # Visualization
    fig = optimizer.plot_pareto_front_2d(0, 1)
    plt.show()
```

### Checkpoint Requirements

- [ ] **Multiple Objectives**: 2+ objectives optimized simultaneously
- [ ] **Pareto Front**: 10+ non-dominated solutions identified
- [ ] **Visualization**: 2D plot showing all trials and Pareto frontier
- [ ] **Trade-offs**: Clear visualization of objective trade-offs
- [ ] **Diversity**: Pareto front well-distributed across objective space

---

## Exercise 4.4: Integration with Machine Learning Pipeline

### Learning Objectives
- Optimize complete ML pipeline (preprocessing, model, hyperparameters)
- Handle categorical and continuous parameters
- Validate performance on hold-out test set

### Implementation Guide

**Create `optuna_ml_pipeline.py`:**

```python
import optuna
from optuna.samplers import TPESampler
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score
from typing import Dict, Tuple


class MLPipelineOptimizer:
    """Optimize entire ML pipeline with Optuna"""
    
    def __init__(self, X_train, y_train, X_test, y_test):
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        
        sampler = TPESampler(seed=42)
        self.study = optuna.create_study(sampler=sampler)
    
    def objective(self, trial) -> float:
        """
        Pipeline optimization objective
        """
        # Preprocessing: scaling
        scaling_method = trial.suggest_categorical(
            'scaling', ['none', 'standard', 'minmax']
        )
        
        X_train = self.X_train.copy()
        X_test = self.X_test.copy()
        
        if scaling_method == 'standard':
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)
            X_test = scaler.transform(X_test)
        
        # Preprocessing: feature engineering
        use_poly_features = trial.suggest_categorical('use_poly', [True, False])
        
        if use_poly_features:
            poly_degree = trial.suggest_int('poly_degree', 2, 3)
            poly = PolynomialFeatures(degree=poly_degree)
            X_train = poly.fit_transform(X_train)
            X_test = poly.transform(X_test)
        
        # Model selection
        model_type = trial.suggest_categorical(
            'model',
            ['random_forest', 'gradient_boosting', 'ridge']
        )
        
        if model_type == 'random_forest':
            model = RandomForestRegressor(
                n_estimators=trial.suggest_int('n_estimators', 50, 300, step=50),
                max_depth=trial.suggest_int('max_depth', 5, 20),
                min_samples_split=trial.suggest_int('min_samples_split', 2, 10),
                random_state=42
            )
        
        elif model_type == 'gradient_boosting':
            model = GradientBoostingRegressor(
                n_estimators=trial.suggest_int('n_estimators', 50, 300, step=50),
                learning_rate=trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
                max_depth=trial.suggest_int('max_depth', 3, 10),
                random_state=42
            )
        
        else:  # ridge
            model = Ridge(
                alpha=trial.suggest_float('alpha', 1e-5, 1e2, log=True)
            )
        
        # Cross-validation score
        cv_scores = cross_val_score(
            model, X_train, self.y_train,
            cv=5,
            scoring='neg_mean_squared_error'
        )
        
        return -cv_scores.mean()  # Return MSE (to minimize)
    
    def optimize(self, n_trials: int = 100):
        """Run optimization"""
        self.study.optimize(self.objective, n_trials=n_trials)
    
    def get_best_pipeline_config(self) -> Dict:
        """Get best configuration"""
        return self.study.best_params
    
    def build_and_evaluate_best(self) -> Tuple[float, float]:
        """
        Build best model and evaluate on test set
        
        Returns:
            (train_score, test_score)
        """
        params = self.study.best_params
        
        # Rebuild preprocessing
        X_train = self.X_train.copy()
        X_test = self.X_test.copy()
        
        if params.get('scaling_method') == 'standard':
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)
            X_test = scaler.transform(X_test)
        
        if params.get('use_poly'):
            poly = PolynomialFeatures(degree=params.get('poly_degree', 2))
            X_train = poly.fit_transform(X_train)
            X_test = poly.transform(X_test)
        
        # Rebuild model
        model_type = params['model']
        
        if model_type == 'random_forest':
            model = RandomForestRegressor(
                n_estimators=params['n_estimators'],
                max_depth=params['max_depth'],
                min_samples_split=params['min_samples_split'],
                random_state=42
            )
        
        elif model_type == 'gradient_boosting':
            model = GradientBoostingRegressor(
                n_estimators=params['n_estimators'],
                learning_rate=params['learning_rate'],
                max_depth=params['max_depth'],
                random_state=42
            )
        
        else:
            model = Ridge(alpha=params['alpha'])
        
        # Train and evaluate
        model.fit(X_train, self.y_train)
        
        train_score = model.score(X_train, self.y_train)
        test_score = model.score(X_test, self.y_test)
        
        return train_score, test_score


# Example usage
if __name__ == "__main__":
    from sklearn.datasets import make_regression
    from sklearn.model_selection import train_test_split
    
    # Create dataset
    X, y = make_regression(n_samples=1000, n_features=20, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Optimize
    optimizer = MLPipelineOptimizer(X_train, y_train, X_test, y_test)
    optimizer.optimize(n_trials=50)
    
    # Best configuration
    print("Best configuration:")
    print(optimizer.get_best_pipeline_config())
    
    # Final evaluation
    train_score, test_score = optimizer.build_and_evaluate_best()
    print(f"\nTrain R²: {train_score:.4f}")
    print(f"Test R²: {test_score:.4f}")
```

### Checkpoint Requirements

- [ ] **Full Pipeline**: Preprocessing, model, hyperparameters optimized
- [ ] **Multiple Models**: 3+ model types available
- [ ] **Feature Engineering**: Polynomial features optional
- [ ] **Cross-Validation**: Used for robust evaluation
- [ ] **Test Performance**: Best model evaluated on hold-out test set
- [ ] **Reproducibility**: Seed fixed for deterministic results

---

## Summary & Certification

### Week 4 Deliverables

| Exercise | Component | Status |
|----------|-----------|--------|
| 4.1 | Optuna Fundamentals | Study management, trials, samplers |
| 4.2 | Pruning & Callbacks | MedianPruner, early stopping, efficiency |
| 4.3 | Multi-Objective | Pareto front, 2D visualization |
| 4.4 | ML Pipeline | Full pipeline optimization with validation |

### Validation Checklist

- [ ] All 4 exercises completed
- [ ] 100+ trials completed across exercises
- [ ] Best trial identified with clear improvement over baseline
- [ ] Pruning reduces computation by 30%+ (if implemented)
- [ ] Pareto front shows clear trade-offs
- [ ] Final ML pipeline generalizes well (test/train difference < 10%)

---

## Mês 11 Complete! 🎉

### All 4 Weeks Done

| Week | Topic | Hours | Status |
|------|-------|-------|--------|
| 1 | Custom Metrics & KPIs | 12-15 | ✅ Complete |
| 2 | Sensitivity Analysis | 12-15 | ✅ Complete |
| 3 | Constrained Optimization | 12-15 | ✅ Complete |
| 4 | Optuna & Advanced Analytics | 12-15 | ✅ Complete |
| **TOTAL** | **Advanced Analytics** | **50-60** | ✅ **COMPLETE** |

### Certification Requirements

To earn Mês 11 certification:

- [x] Complete all 12 exercises with checkpoints
- [x] Build 5+ reusable libraries (metrics, sensitivity, constraint, pruning, pipeline)
- [x] Generate 100+ parameter combinations
- [x] Achieve Pareto fronts with 10+ solutions
- [x] Document all custom metrics and their business meanings
- [x] Show 20%+ improvement in test performance via optimization

### Key Skills Acquired

✅ Business metrics framework design  
✅ Sensitivity and interaction analysis (SHAP, 1D, 2D)  
✅ Constrained optimization (penalty, Lagrangian, DE)  
✅ Multi-objective optimization under constraints  
✅ Advanced hyperparameter tuning with Optuna  
✅ ML pipeline optimization with cross-validation  
✅ Pareto analysis and trade-off exploration  

### Next Steps

👉 **Proceed to Mês 12: Capstone Project**

In Mês 12, you will:
- Select a real-world optimization problem
- Apply all techniques from Mês 1-11
- Build production-ready optimization system
- Deploy and measure ROI
- Publish results

---

**Mês 11 Status**: ✅ **COMPLETE & CERTIFIED**  
**Total Curriculum Progress**: 11/12 months  
**Total Hours Invested**: 550-660 hours  
**Next Milestone**: Mês 12 Capstone
