# Mês 11: Advanced Analytics & Custom Metrics — Complete Implementation

## 🎯 Overview

**Mês 11** transforms optimization theory into production-grade systems with:
- Business-aligned metrics frameworks
- Deep sensitivity and interaction analysis
- Constrained optimization under real-world limitations
- Advanced hyperparameter tuning with Optuna

**Duration**: 50-60 hours  
**Certification Path**: 12 exercises across 4 weeks  
**Tech Stack**: Python, Optuna, SHAP, scikit-learn, Plotly, W&B, PostgreSQL

---

## 📚 Complete Curriculum Structure

### Week 1: Custom Metrics & KPIs (12-15 hours)

Build production metrics framework aligned with business objectives.

#### Exercise 1.1: Business Metrics Framework
- **Deliverable**: `metrics_framework.py` with 6+ metric types
- **Code**: Pydantic-validated composite metrics
- **Concepts**:
  - Profit = revenue - cost
  - ROI = profit / investment
  - Sustainability = energy reduction vs baseline
  - Risk = stability of outputs (low CV = low risk)
  - Quality = mean quality - inconsistency penalty
  - Efficiency = output per energy unit
- **Checkpoint**: 5+ metrics implemented, correlation analysis

#### Exercise 1.2: Multi-Objective Dashboard
- **Deliverable**: Interactive dashboard with W&B integration
- **Visualizations**:
  - Pareto frontier (2D trade-off plots)
  - Correlation heatmap (metric relationships)
  - Time-series KPIs (evolution across iterations)
  - Distribution analysis (performance variability)
- **Checkpoint**: 6+ visualization types, W&B logging

#### Exercise 1.3: Constraint Handling
- **Deliverable**: `constraint_handler.py` with hard/soft constraints
- **Features**:
  - Hard constraints (infeasibility → reject)
  - Soft constraints (violation → penalty)
  - Feasible region definition
  - Solution projection to feasible space
- **Checkpoint**: Constraints validated, penalties applied correctly

#### Exercise 1.4: Robustness Analysis
- **Deliverable**: Perturbation-based stability evaluation
- **Methods**:
  - Add Gaussian noise to solution
  - Evaluate 100+ perturbed versions
  - Rank by robustness score (1 / (1 + CV))
  - Identify fragile vs. stable solutions
- **Checkpoint**: 100+ perturbations per solution, ranking verified

**Week 1 Outcome**: Complete metrics library usable across optimization projects

---

### Week 2: Sensitivity Analysis & Feature Importance (12-15 hours)

Understand what parameters matter and how they interact.

#### Exercise 2.1: Feature Importance (SHAP)
- **Deliverable**: `feature_importance.py` with SHAP analysis
- **Methods**:
  - Compute SHAP values (model-agnostic)
  - Summary plot: mean |SHAP| for each feature
  - Dependence plots: relationship between input and impact
  - Permutation importance: MSE increase from shuffling
- **Checkpoint**: SHAP computed, top 3 features identified

#### Exercise 2.2: One-Way Sensitivity (1D Analysis)
- **Deliverable**: `sensitivity_1d.py` with parameter sweeps
- **Outputs**:
  - Sensitivity curves (non-linearity visible)
  - Tornado diagram (sensitivity magnitude ranking)
  - Elasticity analysis (% output change per % input change)
  - Identify parameter ranges of interest
- **Checkpoint**: 5+ parameters with 20+ points each, elasticity computed

#### Exercise 2.3: Interaction Effects (2D Analysis)
- **Deliverable**: `sensitivity_2d.py` with 2D parameter space
- **Visualizations**:
  - Heatmaps: color-coded interaction surfaces
  - Contour plots: level curves of constant objective
  - Quantify interaction strength (0-1 scale)
  - Find optimal regions (top 20% of parameter space)
- **Checkpoint**: 20×20 grids, interaction strength computed

**Week 2 Outcome**: Understanding of parameter importance and interactions for problem-specific tuning

---

### Week 3: Constrained Optimization (12-15 hours)

Solve real optimization problems with complex constraint systems.

#### Exercise 3.1: Penalty & Barrier Methods
- **Deliverable**: `constrained_optimization.py` with multiple solvers
- **Techniques**:
  - Penalty method: obj + weight × violations²
  - Barrier method: obj - weight × log(margins)
  - Augmented Lagrangian: iterative multiplier updates
  - Differential Evolution: global optimization
- **Checkpoint**: All 3 methods functional, feasible solutions found

#### Exercise 3.2: Multi-Objective Constrained Optimization
- **Deliverable**: `multiobjective_constrained.py` with NSGA-II
- **Features**:
  - DEAP-based multi-objective optimization
  - Hard constraint enforcement (infeasible → penalized)
  - Soft constraint penalties
  - Pareto front generation
  - Constraint validation in final solutions
- **Checkpoint**: 10+ Pareto solutions, all feasible

#### Exercise 3.3: Real-World Problem Solving
- **Deliverable**: `real_world_optimization.py` (manufacturing example)
- **Problem**: Minimize production cost while meeting:
  - Demand constraints (per product, per period)
  - Capacity constraints (per facility, per period)
  - Inventory limits
  - Transportation restrictions
- **Checkpoint**: 10%+ cost reduction vs. baseline

**Week 3 Outcome**: Ability to formulate and solve real-world constrained optimization problems

---

### Week 4: Hyperparameter Optimization & Optuna (12-15 hours)

Master advanced hyperparameter tuning with Optuna framework.

#### Exercise 4.1: Optuna Fundamentals
- **Deliverable**: `optuna_optimizer.py` with multi-solver support
- **Features**:
  - Study creation and persistence (SQLite)
  - Multiple samplers: TPE (Tree-structured Parzen Estimator), Random, CMA-ES
  - Objective functions for sklearn and TensorFlow models
  - Trials DataFrame export
  - Optimization history and parallel coordinates plots
- **Checkpoint**: 50+ trials, best parameters extracted

#### Exercise 4.2: Pruning & Early Stopping
- **Deliverable**: `optuna_pruning.py` with intelligent pruning
- **Methods**:
  - MedianPruner: stop if median performance exceeded
  - PercentilePruner: stop if below percentile
  - Intermediate reporting: trial.report() every epoch
  - Pruning efficiency: 20%+ unpromising trials eliminated
- **Checkpoint**: Pruning reduces time by 30%+

#### Exercise 4.3: Multi-Objective with Optuna
- **Deliverable**: `optuna_multiobjective.py` with Pareto generation
- **Features**:
  - Simultaneous optimization of 2+ objectives
  - Automatic Pareto front identification
  - 2D/3D visualization of trade-offs
  - Study.best_trials returns non-dominated solutions
- **Checkpoint**: 10+ Pareto solutions, clear trade-offs visible

#### Exercise 4.4: Full ML Pipeline Optimization
- **Deliverable**: `optuna_ml_pipeline.py` optimizing entire pipeline
- **Parameters**:
  - Preprocessing: scaling method, polynomial degree
  - Feature engineering: engineered features on/off
  - Model selection: RF, GB, Ridge
  - Hyperparameters: n_estimators, depth, learning_rate, etc.
- **Checkpoint**: Test R² > baseline by 15%, cross-validated

**Week 4 Outcome**: Mastery of state-of-the-art hyperparameter optimization framework

---

## 🛠️ Implementation Architecture

### Core Modules Created

```
mes11_advanced_analytics/
├── WEEK_1_CUSTOM_METRICS.md
│   ├── metrics_framework.py         (Pydantic metrics, composite scoring)
│   ├── dashboard.py                 (Pareto plots, correlations, W&B)
│   ├── constraint_handler.py        (Hard/soft constraints, projection)
│   └── robustness_analysis.py       (Perturbation, ranking, visualization)
│
├── WEEK_2_SENSITIVITY.md
│   ├── feature_importance.py        (SHAP, permutation importance)
│   ├── sensitivity_1d.py            (Tornado, curves, elasticity)
│   └── sensitivity_2d.py            (Heatmaps, contours, interaction strength)
│
├── WEEK_3_CONSTRAINED.md
│   ├── constrained_optimization.py  (Penalty, barrier, Lagrangian)
│   ├── multiobjective_constrained.py (NSGA-II + constraints)
│   └── real_world_optimization.py   (Manufacturing problem)
│
├── WEEK_4_OPTUNA.md
│   ├── optuna_optimizer.py          (Study, samplers, visualizations)
│   ├── optuna_pruning.py            (MedianPruner, efficiency stats)
│   ├── optuna_multiobjective.py     (Pareto with Optuna)
│   └── optuna_ml_pipeline.py        (Full pipeline optimization)
│
└── README.md                        (Quick start & overview)
```

### Integration Points

| Component | Uses | Data Flow |
|-----------|------|-----------|
| metrics_framework | objective functions | Custom metrics → optimization objective |
| constraint_handler | penalty/barrier methods | Violations → penalized objective |
| sensitivity_1d | parameter ranges | Parameter importance → search bounds |
| optuna_optimizer | all above | Samples → evaluates → reports |
| robustness_analysis | final solutions | Best solutions → stability ranking |

---

## 📊 Learning Outcomes

### By End of Week 1
✅ Define custom business metrics aligned with domain  
✅ Create dashboards for multi-objective tracking  
✅ Implement constraint satisfaction checks  
✅ Quantify solution robustness under uncertainty  

### By End of Week 2
✅ Identify most influential parameters (SHAP)  
✅ Understand non-linear parameter impacts (1D)  
✅ Discover parameter synergies (2D interactions)  
✅ Optimize with focus on important parameters  

### By End of Week 3
✅ Formulate constrained optimization problems  
✅ Apply multiple constraint handling techniques  
✅ Generate Pareto fronts under constraints  
✅ Solve real-world production/supply chain problems  

### By End of Week 4
✅ Design effective search spaces for Optuna  
✅ Reduce tuning time via intelligent pruning  
✅ Optimize full ML pipelines end-to-end  
✅ Balance model quality, training time, interpretability  

### Overall Competencies

- 🎯 **Metrics Design**: Create KPIs aligned with business goals
- 📈 **Sensitivity Analysis**: Understand problem structure deeply
- ⚙️ **Constrained Optimization**: Solve real-world problems with limitations
- 🔍 **Hyperparameter Tuning**: Optimize ML systems at scale
- 📊 **Multi-Objective Trade-offs**: Navigate competing objectives
- 🛡️ **Solution Robustness**: Build stable, reliable systems

---

## 🎓 Certification Checklist

### Exercise Completion (12 exercises)

- [ ] **1.1** Metrics Framework — 6+ types, correlation analysis
- [ ] **1.2** Dashboard — 6+ visualization types, W&B logging
- [ ] **1.3** Constraint Handling — Hard/soft enforcement, projection
- [ ] **1.4** Robustness Analysis — 100+ perturbations, ranking
- [ ] **2.1** Feature Importance — SHAP computed, top features identified
- [ ] **2.2** 1D Sensitivity — 5 parameters, 20 points each, elasticity
- [ ] **2.3** 2D Interaction — 20×20 grids, interaction strength, optimal regions
- [ ] **3.1** Penalty Methods — All 3 solvers working, feasible solutions
- [ ] **3.2** Multi-Obj Constrained — NSGA-II, 10+ Pareto solutions
- [ ] **3.3** Real-World Problem — 10%+ cost reduction verified
- [ ] **4.1** Optuna Fundamentals — 50+ trials, best params extracted
- [ ] **4.2** Pruning & Early Stopping — 30%+ time savings with 20%+ pruning rate
- [ ] **4.3** Multi-Objective Optuna — Pareto front with 10+ solutions
- [ ] **4.4** Full Pipeline Optimization — Test R² > baseline + 15%

### Code Quality Standards

- [ ] All code follows PEP 8 style guide
- [ ] Comprehensive docstrings for all functions
- [ ] Type hints on function signatures
- [ ] Unit tests for critical functions
- [ ] 90%+ code coverage (tests)
- [ ] No commented-out code or debug prints

### Documentation Standards

- [ ] Each exercise has clear learning objectives
- [ ] Implementation guide with complete code examples
- [ ] Checkpoint requirements that can be verified
- [ ] Example usage showing realistic scenarios
- [ ] Visualization examples for each output type

### Performance Standards

- [ ] All optimizations complete in < 1 hour
- [ ] Cross-validation prevents overfitting
- [ ] Test performance within 5% of train performance
- [ ] Pareto fronts show clear trade-offs (not clustered)
- [ ] Sensitivity analysis identifies 3+ important parameters

---

## 🚀 Quick Start Guide

### Installation

```bash
# Create virtual environment
python -m venv mes11_env
source mes11_env/bin/activate  # or `mes11_env\Scripts\activate` on Windows

# Install dependencies
pip install optuna shap scikit-learn pandas numpy matplotlib plotly wandb scipy deap tensorflow

# Clone or download mes11 materials
cd mes11_advanced_analytics
```

### Week 1 Execution

```bash
# Start with Exercise 1.1
python metrics_framework.py
# Expected output: Metrics computed, correlation matrix shown

# Progress to 1.2
python dashboard.py
# Expected output: Pareto plots, W&B logged

# Complete 1.3 and 1.4
python constraint_handler.py
python robustness_analysis.py
```

### Week 2 Execution

```bash
# SHAP analysis
python feature_importance.py

# 1D sensitivity
python sensitivity_1d.py

# 2D interactions
python sensitivity_2d.py
```

### Week 3 Execution

```bash
# Constrained optimization methods
python constrained_optimization.py

# Multi-objective under constraints
python multiobjective_constrained.py

# Real-world manufacturing problem
python real_world_optimization.py
```

### Week 4 Execution

```bash
# Optuna fundamentals
python optuna_optimizer.py

# Pruning strategies
python optuna_pruning.py

# Multi-objective Pareto
python optuna_multiobjective.py

# Full pipeline optimization
python optuna_ml_pipeline.py
```

---

## 📚 Key Concepts Reference

### Metrics Design
- **Composite Score** = Σ weights_i × normalized_i
- **ROI** = (Revenue - Cost) / Investment
- **Robustness** = 1 / (1 + CV)

### Sensitivity Analysis
- **Elasticity** = (% output change) / (% input change)
- **Tornado Diagram** = Ranked by output range
- **Interaction Strength** = variance from interaction / total variance

### Constrained Optimization
- **Penalty Method**: min obj + λ × Σ violations²
- **Barrier Method**: min obj - ε × Σ log(margins)
- **Augmented Lagrangian**: Iteratively update λ and ρ

### Hyperparameter Tuning
- **TPE** = Bayesian optimization with Parzen estimators
- **Pruning** = Early stopping for unpromising trials
- **Pareto Front** = Non-dominated solutions in multi-objective

---

## 🎯 Real-World Applications

### Manufacturing Optimization
- **Problem**: Minimize production cost while meeting demand
- **Solutions from Mês 11**: Constrained optimization with penalty methods
- **Expected Impact**: 10-15% cost reduction

### Model Training
- **Problem**: Choose preprocessing, model, hyperparameters
- **Solutions from Mês 11**: Full pipeline optimization with Optuna
- **Expected Impact**: 15-20% accuracy improvement

### Business KPI Management
- **Problem**: Balance profit, sustainability, risk
- **Solutions from Mês 11**: Multi-objective with custom metrics
- **Expected Impact**: Better decision-making with trade-off visualization

### Supply Chain Optimization
- **Problem**: Warehouse locations, inventory levels, routes
- **Solutions from Mês 11**: Multi-objective constrained optimization
- **Expected Impact**: 20-25% supply chain cost reduction

---

## 🔗 Connections to Other Months

| From | To | How Used |
|------|----|----|
| **Mês 9** | Mês 11 | Deploy Mês 11 systems to production infrastructure |
| **Mês 10** | Mês 11 | Apply federated metrics across distributed training |
| **Mês 11** | Mês 12 | Use all techniques for capstone optimization project |

---

## 📈 Progress Tracking

**Estimated Time Breakdown**:
- Week 1 (Metrics): 12-15h
- Week 2 (Sensitivity): 12-15h
- Week 3 (Constrained): 12-15h
- Week 4 (Optuna): 12-15h
- **Total**: 50-60h

**Milestone Checkpoints**:
- ✅ After Exercise 1.4: Can build custom metrics dashboard
- ✅ After Exercise 2.3: Can analyze parameter importance and interactions
- ✅ After Exercise 3.3: Can solve real-world optimization problems
- ✅ After Exercise 4.4: Can optimize full ML pipelines with Optuna

---

## 🆘 Common Issues & Solutions

### Issue: SHAP computation slow
**Solution**: Use sample=50 for kernel explainer, increase n_samples in pool

### Issue: Optuna trials not improving
**Solution**: Expand search space, increase n_startup_trials before pruning, check objective function for bugs

### Issue: Constrained solutions infeasible
**Solution**: Increase penalty_weight, use barrier method instead, project to feasible region

### Issue: Pareto front too small (< 5 solutions)
**Solution**: Increase n_trials, use larger population, reduce mutation rates

---

## 📞 Getting Help

1. **Code Errors**: Check docstrings and example usage in each module
2. **Concept Questions**: Review the "Key Concepts Reference" section
3. **Optimization Issues**: Enable verbose logging in Optuna/scipy
4. **Performance**: Profile with `cProfile` to find bottlenecks

---

## 🎉 Graduation Requirements

To earn **Mês 11 Certification**:

1. ✅ Complete all 12 exercises with verified checkpoints
2. ✅ Build 8+ reusable Python modules
3. ✅ Generate 100+ parameter combinations across experiments
4. ✅ Create Pareto fronts with 10+ non-dominated solutions
5. ✅ Show 20%+ improvement over baseline in test scenario
6. ✅ Document all custom metrics and business meanings
7. ✅ Demonstrate proficiency in 4+ optimization techniques

**Upon Completion**: You're ready for **Mês 12: Capstone Project** 🚀

---

**Mês 11 Status**: ✅ **COMPLETE**  
**Total Curriculum Progress**: 11/12 months  
**Next Destination**: Capstone Project (Real-World Application)
