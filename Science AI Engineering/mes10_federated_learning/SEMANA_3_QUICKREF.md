# Fase 3 Quick Reference Guide

## Semana 1: Federated Learning Optimization

**File**: `federated_optimizer.py` (530 lines)  
**Purpose**: Distributed optimization across N agents with parameter server aggregation

### Quick Start
```python
from federated_optimizer import FederatedOptimizer, FederatedConfig

config = FederatedConfig(
    num_agents=4,
    population_size=20,
    generations=50,
    topology="ring"  # or "star", "mesh"
)

optimizer = FederatedOptimizer(config)
results = optimizer.run(objective_function=my_function)
print(f"Best loss: {results.best_loss}")
```

### Topologies
- **Star**: Central server, O(N²) communication, synchronous
- **Ring**: Linear chain, O(N) per agent, natural load balancing ⭐ WINNER
- **Mesh**: All-to-all, highest cost, maximum information sharing

### Key Classes
- `FederatedParameterServer`: Aggregates weights from agents
- `FederatedAgent`: Local GA optimizer + synchronization
- `FederatedOptimizer`: Orchestrates entire framework
- `FederatedConfig`: Configuration dataclass

### Metrics
- Convergence loss (best value over generations)
- Communication overhead (ms per generation)
- Agent diversity (population variance)

---

## Semana 2: Adaptive Prompting with LLM

**File**: `adaptive_prompting.py` (846 lines)  
**Purpose**: LLM-guided optimization with phase-aware prompting

### Quick Start
```python
from adaptive_prompting import AdaptiveOptimizer

optimizer = AdaptiveOptimizer(
    objective=my_objective_function,
    parameter_bounds={'param1': (0, 10), 'param2': (5, 15)},
    problem_type="manufacturing",
    use_mock_llm=True  # or False for real OpenAI API
)

results = optimizer.optimize(
    num_rounds=20,
    configs_per_round=3,
    compare_with_random=True
)
```

### Optimization Phases
1. **Exploration** (0-30% progress)
   - Goal: Maximize diversity
   - Strategy: Test extreme values, different regions
   - Prompts: "large search space", "cover different regions"

2. **Refinement** (30-70% progress)
   - Goal: Balance exploitation/exploration
   - Strategy: Build on promising regions
   - Prompts: "refining", "recent improvements"

3. **Exploitation** (70%+ progress)
   - Goal: Fine-tune elite solutions
   - Strategy: Small adjustments to best solutions
   - Prompts: "final tuning", "precision"

4. **Recovery** (stagnation detected)
   - Goal: Escape local optimum
   - Strategy: Radical parameter changes
   - Prompts: "stalled convergence", "escape current region"

### Key Classes
- `PromptManager`: Generates phase-adapted prompts
- `FewShotLearner`: Stores successful prompt-response pairs
- `LLMConfigurator`: Wraps LLM calls (mock or real)
- `ResponseParser`: Extracts configurations from LLM text
- `AdaptiveOptimizer`: Orchestrates full pipeline

### Metrics
- Validity rate: % of configs valid (0-100%)
- Diversity score: Parameter space coverage (0-1)
- Convergence improvement: Loss reduction per round
- LLM call time: Latency tracking

### Few-Shot Learning
```python
# Automatic if improvement > 0.01
optimizer.few_shot_learner.get_examples(phase="exploration", num_examples=2)
# Returns: [FewShotExample, FewShotExample]
```

---

## Integration Strategy (Semana 3)

### Hybrid Architecture
```
HybridOptimizer:
  ├─→ FederatedOptimizer (50% weight)
  │    └─ Genetic algorithms across agents
  ├─→ AdaptiveOptimizer (50% weight)
  │    └─ LLM-guided configuration suggestion
  └─→ Ensemble
       ├─ Blend configurations (weighted)
       ├─ Evaluate + choose best
       └─ Update both components
```

### Expected Improvements
- Better convergence on high-dimensional problems
- Adaptive strategy switching based on progress
- Shared few-shot learning across agents
- Escape from local optima (LLM creativity)

---

## Configuration Examples

### Manufacturing Process Optimization
```python
bounds = {
    'temperature': (140, 160),
    'pressure': (2.0, 3.0),
    'feed_rate': (0.8, 1.5),
    'catalyst_ratio': (0.1, 0.5),
    'dwell_time': (10, 30)
}

optimizer = AdaptiveOptimizer(
    objective=production_cost,
    parameter_bounds=bounds,
    problem_type="manufacturing",
    use_mock_llm=True
)
```

### Financial Portfolio Optimization
```python
bounds = {
    'stock_a': (0, 1),
    'stock_b': (0, 1),
    'stock_c': (0, 1),
    'bond_etf': (0, 1),
    'cash': (0, 1)
}
# Sum = 1 (portfolio constraint)

optimizer = AdaptiveOptimizer(
    objective=portfolio_risk,
    parameter_bounds=bounds,
    problem_type="finance",
    use_mock_llm=False  # Use real LLM for financial insights
)
```

### Machine Learning Hyperparameter Tuning
```python
bounds = {
    'learning_rate': (0.0001, 0.1),
    'batch_size': (8, 256),
    'dropout': (0.0, 0.5),
    'hidden_units': (32, 512),
    'num_layers': (1, 5)
}

optimizer = AdaptiveOptimizer(
    objective=model_validation_loss,
    parameter_bounds=bounds,
    problem_type="hyperparameter_tuning",
    use_mock_llm=True
)
```

---

## Performance Benchmarks

### Federated Learning (Semana 1)
- Ring topology: **0.1133 loss** (Winner)
- Star topology: 0.1393 loss
- Mesh topology: 0.1581 loss
- Communication: 2.48-3.01 ms/generation

### Adaptive Prompting (Semana 2)
- 20 rounds × 3 configs/round = 60 evaluations
- Parsing: 100% validity rate
- Diversity: 0.1756 avg score
- LLM calls: 0.0-0.02s (mock mode)

### Combined (Estimated for Semana 3)
- Convergence: 30-40% faster than pure GA
- Stability: Lower variance in intermediate results
- Scalability: O(N) communication with N agents

---

## Troubleshooting

### Federated Learning
**Q: Agents not converging?**  
A: Check topology selection. Ring is usually better than star for diversity.

**Q: High communication cost?**  
A: Use star topology or reduce synchronization frequency.

**Q: Population diversity too low?**  
A: Increase mutation rate or use mesh topology for information diversity.

### Adaptive Prompting
**Q: LLM returning invalid configs?**  
A: Use mock mode for testing. Validity should be ~100%. If <80%, add error handling.

**Q: Recovery phase triggered too early?**  
A: Adjust stagnation_threshold (default=10 rounds). Increase to 15 for longer exploration.

**Q: Few-shot learning not improving?**  
A: Improvement threshold is 0.01. If convergence is slow, examples won't be collected. Try harder optimization problem.

**Q: Real LLM API errors?**  
A: Ensure OPENAI_API_KEY is set. Mock mode activates automatically on failure.

---

## Code Organization

```
mes10_federated_learning/
├── README.md
├── WEEK_1_FEDERATED_OPTIMIZATION.md (curriculum reference)
├── WEEK_2_ADAPTIVE_PROMPTING.md (curriculum reference)
├── WEEK_3_REALTIME_INTEGRATION.md (in progress)
├── WEEK_4_ADVANCED_FEDERATED.md (in progress)
│
├── federated_optimizer.py
│   ├── FederatedParameterServer
│   ├── FederatedAgent
│   ├── FederatedOptimizer
│   └── Config/Metrics dataclasses
│
├── adaptive_prompting.py
│   ├── PromptManager (4 templates)
│   ├── FewShotLearner
│   ├── LLMConfigurator
│   ├── ResponseParser
│   └── AdaptiveOptimizer
│
├── SEMANA_1_FASE3_DELIVERY_SUMMARY.md
├── SEMANA_2_FASE3_DELIVERY_SUMMARY.md
└── SEMANA_3_QUICKREF.md (this file)
```

---

## Common Patterns

### Using Phase Information
```python
optimizer = AdaptiveOptimizer(...)
results = optimizer.optimize(num_rounds=20)

# Check what phases were used
phase_sequence = [m.phase for m in results['metrics_log']]
print(f"Phases used: {phase_sequence}")
# Output: ['exploration', 'exploration', 'refinement', 'exploitation', ...]
```

### Custom Objective Function
```python
def my_objective(config):
    """Minimize this function."""
    x1 = config.get('param1', 0)
    x2 = config.get('param2', 0)
    x3 = config.get('param3', 0)
    
    # Rastrigin-like function
    loss = sum((10 * np.sin(p / 50) + (p - 150)**2 / 1000) 
               for p in [x1, x2, x3])
    return loss

optimizer = AdaptiveOptimizer(
    objective=my_objective,
    parameter_bounds={
        'param1': (100, 200),
        'param2': (100, 200),
        'param3': (100, 200)
    }
)
```

### Accessing Results
```python
results = optimizer.optimize(...)

best_loss = results['best_loss_llm']
best_config = results['best_config_llm']
convergence = results['convergence_history_llm']
metrics = results['metrics_log']  # Per-round metrics

# Comparison
improvement_pct = results['improvement_percent']
print(f"LLM {improvement_pct:+.1f}% vs random baseline")
```

---

## Next Steps

1. **Semana 3**: Integrate federated + adaptive (hybrid)
2. **Semana 4**: Real-time deployment, multi-agent few-shot
3. **Capstone**: Full optimization system for production

Happy optimizing! 🚀
