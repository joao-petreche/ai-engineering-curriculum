# Mês 10: Federated Learning & Adaptive Prompting

## 📋 Visão Geral
- Objetivo: Implementar otimização multi-agente federada com adaptação dinâmica de prompts LLM.
- Carga estimada: 50-60h.
- Pré-requisitos: Meses 4-9 concluídos; conceitos de federated learning, LLM fine-tuning básicos.
- Stack: Ray Tune, Weights & Biases, LangChain, OpenAI API, PyTorch Lightning (federado).

## 📦 Setup Rápido
```bash
pip install ray[tune] wandb langchain openai torch pytorch-lightning
```

---
## 🔹 Semana 1 — Federated Optimization (12-15h)

### Exercício 1.1 — Ray Cluster Setup (3-4h)
Crie um cluster Ray distribuído (local + remote). Exemplo:
```python
import ray

ray.init(address="auto")  # Connect to existing cluster
# ou
ray.init()  # Local cluster

@ray.remote
def worker_optimize(config):
    """Run optimization on remote worker"""
    return {"loss": evaluate(config)}

# Parallel evaluation
futures = [worker_optimize.remote(config) for config in configs]
results = ray.get(futures)
```
**Checkpoint:** Ray cluster up, workers responding, 4+ workers benchmarked.

### Exercício 1.2 — Federated Parameter Server (3-4h)
Implemente servidor de parâmetros para agregação de atualizações:
```python
class ParameterServer:
    def __init__(self, initial_weights):
        self.weights = initial_weights
    
    def aggregate(self, worker_updates, weights):
        """Federated averaging: w' = sum(w_i) / n"""
        return sum(weights) / len(weights)
    
    def get_weights(self):
        return self.weights
```
**Checkpoint:** Agregação funciona; convergência em 10 iterações.

### Exercício 1.3 — Multi-Agent Optimization (2-3h)
Rode GA/NSGA-II em paralelo com sincronização de população:
```python
def federated_ga(pop_size, num_agents):
    """Each agent runs GA, exchange best solutions"""
    # Each agent: pop_size / num_agents
    # Every N gen: exchange_best_solutions()
    # Converges faster than single agent
```
**Checkpoint:** 3+ agentes, tempo 30-40% melhor que serial.

### Exercício 1.4 — Convergence Analysis (2-3h)
Meça convergência em diferentes topologias (star, ring, mesh).
**Checkpoint:** Plotar convergence curves; mesh 10% mais rápido.

---
## 🔹 Semana 2 — Adaptive LLM Prompting (12-15h)

### Exercício 2.1 — Prompt Engineering Basics (3-4h)
Crie prompt templates que variam por resultado:
```python
base_prompt = """
You are an optimization expert. Given:
- Objective: {objective}
- Current best: {best_value}
- Iteration: {iteration}

Suggest next parameters to try.
"""

def adaptive_prompt(objective, best, iteration, history):
    """Adjust prompt based on progress"""
    if stagnant(history):
        return base_prompt + "\nTry more diverse parameters."
    elif converging(history):
        return base_prompt + "\nFocus on refinement."
    return base_prompt
```
**Checkpoint:** 3 prompt variants, LLM produces valid configs.

### Exercício 2.2 — LLM-Guided Search (3-4h)
Integrate LLM into optimization loop:
```python
def llm_suggest_next_config(history, objective):
    """LLM proposes next parameters based on history"""
    prompt = adaptive_prompt(...)
    response = llm.query(prompt)
    config = parse_llm_response(response)
    return config

# In main loop:
for iteration in range(max_iter):
    # LLM suggests → evaluate → update history
    suggested = llm_suggest_next_config(history, obj)
    loss = evaluate(suggested)
    history.append((suggested, loss))
```
**Checkpoint:** 50 LLM iterations; loss converges 20% faster than random.

### Exercício 2.3 — Few-Shot Learning for Prompting (2-3h)
Fine-tune prompt with examples of good suggestions:
```python
few_shot_prompt = """
Examples of good parameter choices:
1. Objective: maximize_profit
   → Set price_elasticity=0.8, margin=0.4
   
2. Objective: minimize_cost
   → Set batch_size=256, learning_rate=0.001
   
Now, for your objective...
"""
```
**Checkpoint:** LLM consistency improves by 30% with few-shot.

### Exercício 2.4 — Feedback Integration (2-3h)
Feed optimization results back into prompt (online learning):
```python
def learn_from_feedback(feedback, prompt_version):
    """Update prompt based on what worked/failed"""
    if feedback["success"]:
        memorize_pattern(feedback)
    prompt_version += 1
    return improved_prompt
```
**Checkpoint:** Prompt evolves; iteration 10 uses better language than iteration 1.

---
## 🔹 Semana 3 — Real-Time Monitoring & Integration (12-15h)

### Exercício 3.1 — Weights & Biases Logging (3-4h)
Log all federated runs to W&B:
```python
import wandb

wandb.init(project="bps-federated", entity="your-team")

# Log metrics
wandb.log({
    "loss": loss,
    "iteration": i,
    "agent_id": agent_id,
    "convergence": compute_convergence()
})

# Log LLM prompts and responses
wandb.log({"llm_prompt": prompt, "llm_response": response})
```
**Checkpoint:** All runs logged; dashboard shows convergence curves.

### Exercício 3.2 — Live Hyperparameter Tracking (3-4h)
Visualize federated agent evolution:
```
WandB Dashboard:
- Line plot: loss over iteration (all agents + aggregate)
- Parallel coords: parameters tried vs. loss
- System metrics: CPU, memory, network traffic per agent
- LLM metrics: prompt length, response time
```
**Checkpoint:** Dashboard auto-updates; compare 3 runs side-by-side.

### Exercício 3.3 — Anomaly Detection (2-3h)
Alert when agent diverges:
```python
def detect_divergence(agent_losses):
    """Alert if one agent's loss >> others"""
    mean = np.mean(agent_losses)
    if max(agent_losses) > mean * 2:
        alert("Agent diverged!")
    return diverged
```
**Checkpoint:** Catch divergence in < 2 iterations.

### Exercício 3.4 — API Integration (2-3h)
Expose federated results via REST API:
```python
@app.get("/federated/status")
def federated_status():
    return {
        "num_agents": ray.nodes(),
        "best_loss": global_best,
        "llm_iterations": iteration_count,
        "convergence": compute_convergence()
    }

@app.post("/federated/get-next-config")
def get_next_config(objective):
    return llm_suggest_next_config(history, objective)
```
**Checkpoint:** API responds in < 2s; 100+ requests/sec.

---
## 🔹 Semana 4 — Edge Co-Simulation & Advanced Features (14-15h)

### Exercício 4.1 — Edge Device Co-Sim (4-5h)
Deploy federated optimizer to edge (edge + cloud):
```python
@ray.remote
def edge_worker_optimize(config, device_simulator):
    """Local computation on edge, send updates to cloud"""
    local_loss = device_simulator.evaluate(config)
    cloud.send_update(local_loss)
    global_weights = cloud.get_weights()
    return global_weights
```
**Checkpoint:** Edge → Cloud sync < 100ms; 10 edge devices coordinated.

### Exercício 4.2 — Privacy-Preserving Aggregation (3-4h)
Aggregate without sharing full data (differential privacy):
```python
def federated_avg_private(local_updates, epsilon=0.1):
    """Add Laplace noise to gradients before averaging"""
    noisy_updates = [add_laplace_noise(u, epsilon) for u in local_updates]
    return average(noisy_updates)
```
**Checkpoint:** Convergence within 5% of non-private; epsilon=0.1 acceptable.

### Exercício 4.3 — Adaptive Agent Scaling (2-3h)
Dynamically add/remove agents based on load:
```python
def adaptive_scaling():
    if convergence_speed < threshold:
        add_agent()  # Scale up
    if cpu_usage < 20%:
        remove_agent()  # Scale down
```
**Checkpoint:** Auto-scale 5 → 10 agents; 40% faster.

### Exercício 4.4 — Benchmark Suite (2-3h)
Comprehensive comparison: federated vs. centralized vs. baselines.
```
Results:
- Centralized GA: 100 iterations to convergence
- Federated (5 agents): 30 iterations (3.3x faster)
- LLM-guided: 25 iterations (4x faster)
- Federated + LLM: 15 iterations (6.7x faster)
```
**Checkpoint:** Table published; 6-7x speedup achieved.

---
## 📋 Checklist de Certificação — Mês 10
- [ ] Ray cluster com 4+ workers, syncronização funciona
- [ ] Parameter server agregando updates corretamente
- [ ] Multi-agent GA converge 30%+ mais rápido
- [ ] LLM prompts adaptativos (3+ variants)
- [ ] LLM-guided search 20%+ mais rápido que random
- [ ] Few-shot prompting melhora consistência 30%+
- [ ] Feedback integration funciona; prompts evoluem
- [ ] W&B logging de todos os runs; dashboard útil
- [ ] Anomaly detection detecta divergência < 2 iter
- [ ] API expõe status e next-config em < 2s
- [ ] Edge co-sim com 10+ devices, sync < 100ms
- [ ] Privacy-preserving agregação (epsilon=0.1) convergência OK
- [ ] Adaptive scaling 5 → 10 agentes, 40% mais rápido
- [ ] Benchmark completo: 6-7x speedup federated + LLM

---
## Recursos
- Ray Tune: distributed hyperparameter tuning
- Weights & Biases: experiment tracking
- LangChain: LLM interface
- OpenAI API: GPT models
- Differential Privacy libraries (diffprivlib, opacus)

---
## Próximos Passos
- Mês 11: Advanced analytics, custom metrics, optimization under constraints
- Antes de M11: validate federated + LLM speedup em real dataset; tune epsilon para privacy.
