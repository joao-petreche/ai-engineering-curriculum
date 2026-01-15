# Mês 11: Advanced Analytics & Custom Metrics

## 📋 Visão Geral
- Objetivo: Implementar métricas customizadas, análise de sensibilidade, e otimização sob restrições.
- Carga estimada: 50-60h.
- Pré-requisitos: Mês 10 concluído; técnicas de análise de sensibilidade.
- Stack: Shap, Optuna, scipy.optimize, custom metric library.

---
## 🔹 Semana 1 — Custom Metrics & KPIs (12-15h)

### Exercício 1.1 — Business Metrics Framework (3-4h)
Defina métricas além de loss (profit, ROI, customer satisfaction):
```python
class Metrics:
    def profit(self, results):
        revenue = sum(r['output'] * r['price'] for r in results)
        cost = sum(r['compute_cost'] for r in results)
        return revenue - cost
    
    def roi(self, profit, investment):
        return profit / investment if investment > 0 else 0
    
    def composite_score(self, profit, sustainability, risk):
        """Weighted combination"""
        w = {'profit': 0.5, 'sustainability': 0.3, 'risk': 0.2}
        return w['profit'] * profit + w['sustainability'] * sustainability - w['risk'] * risk
```
**Checkpoint:** 5+ métricas implementadas; correlation analysis.

### Exercício 1.2 — Multi-Objective Dashboard (3-4h)
Visualize trade-offs:
- Pareto frontier dos objetivos
- Heatmap de correlações entre métricas
- Time-series de KPIs ao longo de iterações
**Checkpoint:** Dashboard W&B com 10+ métricas; interativo.

### Exercício 1.3 — Constraint Handling (2-3h)
Incorpore restrições em otimização:
```python
def evaluate_with_constraints(config):
    loss = objective_function(config)
    
    # Constraints
    if config['memory'] > 4096:
        return float('inf')  # Invalid
    if config['latency'] > 2000:
        return float('inf')
    
    return loss  # Valid
```
**Checkpoint:** Respeita restrições; encontra Pareto fronts válidas.

### Exercício 1.4 — Robustness Analysis (2-3h)
Teste soluções contra perturbações:
```python
def robustness_test(solution, num_perturbs=100):
    """Add noise to solution, measure stability"""
    scores = []
    for _ in range(num_perturbs):
        perturbed = add_noise(solution, std=0.05)
        scores.append(evaluate(perturbed))
    return mean(scores), std(scores)
```
**Checkpoint:** Ranking das soluções por robustez; plot distributions.

---
## 🔹 Semana 2 — Sensitivity Analysis (12-15h)

### Exercício 2.1 — Feature Importance (Shap) (3-4h)
Explique qual parâmetro mais influencia o resultado:
```python
import shap

explainer = shap.TreeExplainer(trained_model)
shap_values = explainer.shap_values(X)
shap.summary_plot(shap_values, X)
```
**Checkpoint:** Feature importance plot; top 3 parâmetros identificados.

### Exercício 2.2 — One-Way Sensitivity (3-4h)
Varie um parâmetro por vez:
```python
def sensitivity_1d(base_config, param_name, range_vals):
    """Vary param_name, keep others fixed"""
    results = []
    for val in range_vals:
        config = base_config.copy()
        config[param_name] = val
        results.append(evaluate(config))
    return results
```
**Checkpoint:** Plot sensibilidade para 5 parâmetros.

### Exercício 2.3 — Interaction Effects (2-3h)
Dois parâmetros variam juntos:
```python
def sensitivity_2d(base, param1, param2, range1, range2):
    """Heatmap of interaction"""
    results = np.zeros((len(range1), len(range2)))
    for i, v1 in enumerate(range1):
        for j, v2 in enumerate(range2):
            config = base.copy()
            config[param1] = v1
            config[param2] = v2
            results[i, j] = evaluate(config)
    return results
```
**Checkpoint:** Heatmap interactions; identify synergies.

### Exercício 2.4 — Global Sensitivity (Sobol) (2-3h)
Variance-based: quanto cada parâmetro explica da variância total?
```python
from SALib.sample import saltelli
from SALib.analyze import sobol

# Generate samples via Sobol
samples = saltelli.sample(problem, 1000, calc_second_order=True)
results = [evaluate(s) for s in samples]

# Analyze
Si = sobol.analyze(problem, results, calc_second_order=True)
```
**Checkpoint:** Sobol indices para todos parâmetros; S1 + S2 plots.

---
## 🔹 Semana 3 — Constrained Optimization (12-15h)

### Exercício 3.1 — Constraint Types (3-4h)
Implementar restrições comuns:
```python
class Constraints:
    def budget(self, config, max_budget=10000):
        cost = compute_cost(config)
        return cost <= max_budget
    
    def latency(self, config, max_latency_ms=500):
        return estimate_latency(config) <= max_latency_ms
    
    def resource_limit(self, config, max_memory_gb=4):
        return config['memory_gb'] <= max_memory_gb
    
    def feasible(self, config):
        return all([
            self.budget(config),
            self.latency(config),
            self.resource_limit(config)
        ])
```
**Checkpoint:** 5+ constraint types; validation funciona.

### Exercício 3.2 — Penalty Methods (3-4h)
Transformar constraints em penalty term:
```python
def penalized_objective(config, constraints):
    loss = objective_function(config)
    
    # Add penalties for constraint violations
    if not constraints.budget(config):
        loss += 1000 * (cost - budget) ** 2
    if not constraints.latency(config):
        loss += 500 * (latency - limit) ** 2
    
    return loss
```
**Checkpoint:** Penalti bem-calibrado; solução respeita constraints.

### Exercício 3.3 — Feasible Region Exploration (2-3h)
Mapa de regiões viáveis:
```python
def plot_feasible_region(param1, param2, constraints):
    """2D slice of feasibility"""
    X, Y = np.meshgrid(...)
    Z = np.array([[constraints.feasible({param1: x, param2: y}) 
                   for x in X] for y in Y])
    contourf(X, Y, Z)
```
**Checkpoint:** Plots mostram regiões viáveis; identifica bordas.

### Exercício 3.4 — Multi-Objective Constrained (2-3h)
Pareto frontier respeitando constraints:
```python
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import Problem

class ConstrainedOptimization(Problem):
    def _evaluate(self, x, out, *args, **kwargs):
        f = []
        g = []  # constraints
        for xi in x:
            f.append([objective1(xi), objective2(xi)])
            g.append([max(0, constraint1(xi)), max(0, constraint2(xi))])
        out["F"] = np.array(f)
        out["G"] = np.array(g)
```
**Checkpoint:** NSGA-II com constraints; 50+ soluções viáveis.

---
## 🔹 Semana 4 — Advanced Integration & Performance (14-15h)

### Exercício 4.1 — Optuna Integration (3-4h)
Use Optuna para automated hyperparameter tuning:
```python
import optuna

def objective(trial):
    batch_size = trial.suggest_int('batch_size', 32, 256)
    lr = trial.suggest_float('lr', 1e-5, 1e-1, log=True)
    
    loss = train_model(batch_size, lr)
    
    # Constraints
    trial.report(loss, loss)
    if not constraints.feasible({'batch_size': batch_size, 'lr': lr}):
        raise optuna.TrialPruned()
    
    return loss

study = optuna.create_study(sampler=optuna.samplers.TPESampler())
study.optimize(objective, n_trials=100)
```
**Checkpoint:** Optuna integrado; 100 trials, best loss 20% melhor que baseline.

### Exercício 4.2 — AutoML Pipeline (3-4h)
Automatizar seleção de modelo e configuração:
```
Pipeline:
1. Feature engineering
2. Model selection (RF, XGB, NN, ...)
3. Hyperparameter tuning
4. Ensemble weighting
5. Evaluation
```
**Checkpoint:** AutoML finds best pipeline; documentation clara.

### Exercício 4.3 — Real-Time Experiment Adaptation (2-3h)
Experiment evolui baseado em resultados em tempo real:
```python
def adaptive_experiment():
    for iteration in range(max_iter):
        if convergence_detected():
            narrower_search_space()
        if divergence_detected():
            reset_and_restart()
        results = run_batch(current_config)
        update_search_space(results)
```
**Checkpoint:** Convergência 40% mais rápida que fixed space.

### Exercício 4.4 — Benchmark Comparison (2-3h)
Compare todas as abordagens:
```
Results Summary:
- Centralized GA: 100 iterations
- Federated (5 agents): 30 iterations
- LLM-guided: 25 iterations
- Custom metrics: 22 iterations
- Constrained optimization: 20 iterations
- Optuna AutoML: 15 iterations
- Combined (Federated + LLM + Optuna): 8 iterations
```
**Checkpoint:** 12x speedup vs. baseline; all techniques combined.

---
## 📋 Checklist de Certificação — Mês 11
- [ ] 5+ custom metrics implementadas e correlacionadas
- [ ] Dashboard multi-objetivo com Pareto frontier
- [ ] Constraint handling funciona para 5+ tipos
- [ ] Robustness analysis mostra distribuições estáveis
- [ ] Feature importance (Shap) identifica parâmetros-chave
- [ ] 1D sensitivity plots para 5+ parâmetros
- [ ] 2D interaction heatmaps mostram sinergias
- [ ] Sobol indices computados; S1 + S2 válidos
- [ ] Constraint types (budget, latency, memory, etc)
- [ ] Penalty methods bem-calibrados
- [ ] Feasible region visualization clara
- [ ] Pareto frontier respeitando constraints
- [ ] Optuna integrado; 100 trials OK
- [ ] AutoML pipeline automático
- [ ] Real-time adaptation 40%+ mais rápido
- [ ] Benchmark: 12x speedup vs. baseline

---
## Próximos Passos
- Mês 12: Capstone project, integration, case studies
- Antes de M12: documentar todas as técnicas; validar em real-world dataset.
