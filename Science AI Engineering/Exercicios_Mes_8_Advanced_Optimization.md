# Exercícios Mês 8: Advanced Multi-Objective Optimization (BPS)

## 📋 Visão Geral

- **Objetivo:** Otimizar edifícios com múltiplos objetivos (energia, custo, conforto, CO₂) usando meta-heurísticas, Pareto analysis e integração com co-simulação.
- **Carga estimada:** 50-60 horas
- **Pré-requisitos:** Meses 4-7 (surrogates, Gemini, co-simulação, compliance), NumPy/SciPy, Plotly, DEAP.
- **Stack sugerido:** Python 3.10+, `deap`, `numpy`, `pandas`, `plotly`, `scipy`.

### Resultados esperados ao final do mês
1) Gerar fronteiras de Pareto (≥100 soluções não dominadas) para 3-4 objetivos.
2) GA com constraints físicas operando em ≤ 50 gerações com convergência monitorada.
3) Visualização interativa da fronteira (3D/2D + filtros) exportável a HTML.
4) Análise de trade-offs e recomendação "best compromise" ponderada.
5) Capstone: Otimizar um edifício real/sintético com 3+ objetivos e constraints.

---

## 📦 Setup Rápido

```bash
pip install deap numpy pandas plotly scipy
pip install pytest
```

---

## 🔹 Semana 1 — Fundamentos de Otimização Multiobjetivo (12-15h)

### Exercício 1.1 — Dominância de Pareto & Fronteira (3-4h)
Implementar funções de dominância e extração da fronteira a partir de um conjunto de soluções.

```python
from typing import List, Tuple
import numpy as np

# objs: matriz (n_solucoes x n_objetivos). Minimização em todos os objetivos.
def pareto_front(objs: np.ndarray) -> List[int]:
    n = objs.shape[0]
    dominated = np.zeros(n, dtype=bool)
    for i in range(n):
        if dominated[i]:
            continue
        for j in range(n):
            if i == j or dominated[i]:
                continue
            if np.all(objs[j] <= objs[i]) and np.any(objs[j] < objs[i]):
                dominated[i] = True
    return [i for i, d in enumerate(dominated) if not d]

# Teste rápido
if __name__ == "__main__":
    objs = np.array([
        [10, 2000, 0.2],
        [9, 2200, 0.3],
        [11, 1800, 0.25],
        [8, 2500, 0.35]
    ])
    front_idx = pareto_front(objs)
    print("Fronteira Pareto (índices):", front_idx)  # esperado: [0, 2]
```

**Checkpoint:** fronteira retorna soluções não dominadas e ignora as dominadas.

### Exercício 1.2 — Hypervolume e Métricas (2-3h)
Calcular hypervolume para medir qualidade da fronteira (minimização). Referência: ponto de referência = pior valor observado + margem.

```python
import numpy as np

# hypervolume simples 2D/3D via soma de retângulos (para 2D) ou uso de pacote externo para >3D.
def hypervolume_2d(front: np.ndarray, ref: Tuple[float, float]) -> float:
    # Ordenar por obj1
    front = front[np.argsort(front[:, 0])]
    hv = 0.0
    prev_f1 = ref[0]
    for f1, f2 in front:
        hv += (prev_f1 - f1) * (ref[1] - f2)
        prev_f1 = f1
    return hv

if __name__ == "__main__":
    front = np.array([[8, 2500], [10, 2000]])
    ref = (12, 3000)
    hv = hypervolume_2d(front, ref)
    print("HV:", hv)  # valor > 0
```

**Checkpoint:** métrica aumenta quando fronteira melhora (menores objetivos).

### Exercício 1.3 — Visualização Interativa Pareto (3-4h)
Plot 3D da fronteira com Plotly, exportando para HTML.

```python
import plotly.express as px
import pandas as pd

# df com colunas: energy, cost, comfort_gap

def plot_pareto(df: pd.DataFrame, path: str = "pareto_frontier.html"):
    fig = px.scatter_3d(df, x="energy", y="cost", z="comfort_gap",
                        color="solution_id", hover_data=df.columns)
    fig.update_layout(title="Fronteira de Pareto (Energy/Cost/Comfort)")
    fig.write_html(path)
    print(f"✅ Pareto 3D salvo em {path}")
```

**Checkpoint:** HTML abre com rotação e hover exibindo parâmetros.

### Exercício 1.4 — Objetivos para BPS (2-3h)
Definir função de avaliação multiobjetivo (minimizar):
- `f1`: kWh/m².ano (energia)
- `f2`: CAPEX $/m² (custo)
- `f3`: comfort_gap (|PMV_target - PMV_real|)
- `f4`: CO2_kg_m² (opcional)

Especificar assinatura:
```python
def evaluate_solution(params: dict) -> Tuple[float, float, float]:
    # usa surrogate (M4) ou co-sim (M6)
    # retorna (f1_energy, f2_capex, f3_comfort_gap)
    ...
```

**Checkpoint:** função retorna tuple coerente para integração no GA.

---

## 🔹 Semana 2 — Genetic Algorithms para BPS (12-15h)

### Exercício 2.1 — GA Base (DEAP) (4-5h)
Crie cromossomo com 10 parâmetros BPS; avalie multiobjetivo. Use `mes8_optimization.ga_runner.build_nsga2`.

```python
import random
import numpy as np
from deap import base, creator, tools

# Objetivos: minimizar todos
creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMulti)

def init_individual():
    # [wwr, wall_thk, insulation, infiltration, setpoint_heat, setpoint_cool, ...]
    return creator.Individual([
        random.uniform(0.10, 0.60),
        random.uniform(0.15, 0.30),
        random.uniform(0.05, 0.20),
        random.uniform(0.3, 2.0),
        random.uniform(20, 24),
        random.uniform(24, 27),
        random.uniform(0.6, 1.2),  # SHGC
        random.uniform(0.035, 0.045),
        random.uniform(5, 20),
        random.uniform(500, 5000)
    ])

def eval_individual(ind):
    params = {
        "wwr": ind[0],
        "wall_thickness_m": ind[1],
        "insulation_thickness_m": ind[2],
        "infiltration_rate_ACH": ind[3],
        "heating_setpoint_C": ind[4],
        "cooling_setpoint_C": ind[5],
        "shgc": ind[6],
        "lambda_insulation": ind[7],
        "internal_loads_W_m2": ind[8],
        "volume_m3": ind[9]
    }
    # Chame surrogate ou co-sim; aqui stub
    energy = 80 + 20 * (ind[0])  # exemplo
    cost = 2000 + 500 * ind[2]
    comfort_gap = max(0, 22 - ind[4]) + max(0, ind[5] - 25)
    return energy, cost, comfort_gap

from mes8_optimization.ga_runner import build_nsga2
from mes8_optimization.metrics import extract_objectives, diversity
from mes8_optimization.pareto import pareto_front

BOUNDS = {
    "wwr": (0.10, 0.60),
    "wall_thickness_m": (0.15, 0.30),
    "insulation_thickness_m": (0.05, 0.20),
    "infiltration_rate_ACH": (0.3, 2.0),
    "heating_setpoint_C": (20, 24),
    "cooling_setpoint_C": (24, 27),
    "shgc": (0.6, 1.2),
    "lambda_insulation": (0.035, 0.045),
    "internal_loads_W_m2": (5, 20),
    "volume_m3": (500, 5000),
}


def eval_individual(ind):
    params = {
        k: ind[i] for i, k in enumerate(BOUNDS.keys())
    }
    # surrogate/co-sim aqui; stub simples:
    energy = 80 + 20 * params["wwr"]
    cost = 2000 + 500 * params["insulation_thickness_m"]
    comfort_gap = max(0, 22 - params["heating_setpoint_C"]) + max(0, params["cooling_setpoint_C"] - 25)
    return energy, cost, comfort_gap


def demo_run():
    hist_div = []

    def hook(gen, pop):
        hist_div.append(diversity(pop))
        if gen % 10 == 0:
            print(f"Gen {gen}: diversity={hist_div[-1]:.4f}")

    pop = build_nsga2(eval_individual, BOUNDS, pop_size=60, ngen=30, generation_hook=hook)
    objs = extract_objectives(pop)
    front = objs[pareto_front(objs)]
    print("Fronteira tamanho:", len(front))


if __name__ == "__main__":
    demo_run()
```

**Checkpoint:** GA roda 30 gerações, produz fronteira ≥ 20 soluções não dominadas.

### Exercício 2.2 — Constraints & Reparos (3-4h)
Adicionar penalidades e reparadores para violações físicas (usar regras do Mês 7).

Pseudo:
```python
def apply_constraints(ind):
    penalties = 0
    if ind[0] > 0.60: penalties += 50  # WWR
    if ind[4] >= ind[5]: penalties += 100  # heating >= cooling
    # ... outras
    return penalties

def eval_individual(ind):
    base = simulate_or_surrogate(ind)
    penalty = apply_constraints(ind)
    return base_energy + penalty, base_cost + penalty, base_comfort + penalty
```

**Checkpoint:** soluções inválidas sobem no ranking (penalidade) ou são reparadas (clamp).

### Exercício 2.3 — Convergência & Diversidade (2-3h)
Registrar métricas por geração: melhor, mediana, diversidade (variância dos genes). Plotar curvas.

```python
from mes8_optimization.hooks import build_generation_logger

# Hook para salvar diversidade (e hypervolume 2D se ref_point for fornecido)
hook = build_generation_logger(out_csv="runs/ga_metrics.csv", ref_point=None, every=1)
```

**Checkpoint:** curva de diversidade não colapsa cedo; convergência estabiliza < 10 gerações do final.

### Exercício 2.4 — Ilha (Island Model) (2-3h)
Executar 4 populações em paralelo com migração a cada `k` gerações. Comparar qualidade e tempo.

Use helper: `mes8_optimization.island_runner.run_islands`.

```python
from mes8_optimization.island_runner import run_islands, aggregate_frontier
from mes8_optimization.hooks import build_generation_logger

pops, metrics = run_islands(
    eval_individual,
    BOUNDS,
    n_islands=4,
    pop_size=24,
    ngen=30,
    migrate_every=5,
    migrants=2,
    generation_hook=build_generation_logger("runs/islands_metrics.csv", ref_point=None, every=2),
)
front = aggregate_frontier(pops)
print("Fronteira combinada:", front.shape[0])
```

**Checkpoint:** modelo de ilhas encontra fronteira com melhor hipervolume em tempo similar.

---

## 🔹 Semana 3 — Trade-offs & Decisão (12-15h)

### Exercício 3.1 — Análise de Sensibilidade (3-4h)
Variação univariada ±10% em 10 parâmetros; medir impacto em objetivos; gerar ranking (tornado plot).

```python
import pandas as pd

def tornado(df_baseline: pd.DataFrame, param: str, evaluate_fn, delta=0.1):
    base = evaluate_fn(df_baseline.iloc[0].to_dict())
    up = df_baseline.copy(); up[param] *= (1 + delta)
    down = df_baseline.copy(); down[param] *= (1 - delta)
    return {
        "param": param,
        "delta": delta,
        "impact_up": evaluate_fn(up.iloc[0].to_dict())[0] - base[0],
        "impact_down": evaluate_fn(down.iloc[0].to_dict())[0] - base[0]
    }
```

**Checkpoint:** ranking identifica top-3 parâmetros críticos (maior impacto em energia/custo).

### Exercício 3.2 — Cenários (3-4h)
Rodar GA para 5 cenários (A energia, B custo, C balanceado, D CO₂, E conforto) ajustando pesos ou restrições. Comparar fronteiras.

**Checkpoint:** tabela comparativa de soluções por cenário; deltas de objetivos.

### Exercício 3.3 — Seleção por Preferências (2-3h)
Filtrar fronteira por pesos do usuário (0-1) e escolher solução com menor distância ponderada.

```python
def choose_compromise(front: List[Tuple], weights: Tuple[float, float, float]):
    w = np.array(weights)
    objs = np.array(front)
    norm = (objs - objs.min(axis=0)) / (objs.ptp(axis=0) + 1e-9)
    scores = (norm * w).sum(axis=1)
    idx = scores.argmin()
    return idx, objs[idx], scores[idx]
```

**Checkpoint:** usuário ajusta pesos e solução muda de forma previsível.

### Exercício 3.4 — AHP (Decision Matrix) (3-4h)
Construir matriz de decisão (soluções × critérios); aplicar AHP para ranking final; checar razão de consistência.

**Checkpoint:** razão de consistência < 0.1; ranking estável a pequenas variações.

---

## 🔹 Semana 4 — Técnicas Avançadas & Capstone (12-15h)

### Exercício 4.1 — Mutação Adaptativa (3-4h)
Alterar `mutpb` e `eta` dinamicamente conforme diversidade diminui; comparar convergência.

**Checkpoint:** mutação adaptativa evita estagnação; hipervolume melhora ≥5%.

### Exercício 4.2 — Surrogate-Assisted GA (3-4h)
Usar surrogate do Mês 4 para avaliar rapidamente; validar amostras com co-sim a cada N gerações; medir trade-off tempo × acurácia.

**Checkpoint:** speedup ≥10× com erro controlado (<5% em energia).

### Exercício 4.3 — Otimização em Tempo Real (2-3h)
Conectar GA ao controller de co-sim (Mês 6) e rodar com stream de dados (BMS). Reinicializar população quando condições mudam.

**Checkpoint:** sistema ajusta setpoints em < 60s após mudança; mantém conforto.

### Exercício 4.4 — Capstone M8 (3-4h)
Otimizar edifício real/sintético com 3-4 objetivos; entregar:
- Fronteira Pareto (HTML interativo)
- Melhor compromisso por pesos do cliente
- Relatório de trade-offs (PDF/Markdown)

**Checkpoint:** ≥50 soluções na fronteira; recomendação validada por constraints físicas.

---

## 📋 Checklist de Certificação — Mês 8

- [ ] NSGA-II/GA gera ≥100 soluções não dominadas
- [ ] Hypervolume calculado e monitorado
- [ ] Constraints físicas aplicadas (sem violações críticas)
- [ ] Diversidade monitorada e controlada
- [ ] 5 cenários otimizados e comparados
- [ ] Visualização interativa (Plotly) entregue
- [ ] Trade-off e decisão por pesos/AHP implementados
- [ ] Surrogate-assisted GA com speedup ≥10×
- [ ] Capstone concluído com relatório e fronteira

---

## 📚 Referências
- Deb, K. (2001). Multi-Objective Optimization Using Evolutionary Algorithms.
- Coello, C. A. C. (2006). Evolutionary Multi-objective Optimization.
- NSGA-II original: Deb et al. (2002).
- Plotly docs (visualização interativa).
- DEAP docs (toolbox, operadores, NSGA-II).

---

## 🚀 Próximos Passos
- Mês 9: Containerização, Kubernetes, CI/CD, observabilidade.
- Integrar GA com pipelines de co-sim e compliance (Mês 7) para testes automáticos antes de aceitar soluções.
- Usar `mes8_optimization.demo_run` como template para o capstone (substituir `eval_individual` pelo surrogate/co-sim real).
- Rodar `pytest -q tests/test_pareto_mes8.py tests/test_ga_metrics_mes8.py tests/test_islands_mes8.py`.
- Executar `python -m mes8_optimization.demo_run` e gerar `pareto_demo.html`; depois substituir o stub de avaliação.
- Gerar gráficos a partir dos CSVs de métricas: `python scripts/mes8_metrics_report.py --csv runs/islands_metrics.csv --out reports/mes8_metrics.html`.
- Conectar surrogate ou co-sim: usar `mes8_optimization.eval_template.make_surrogate_evaluator(model)` ou `make_cosim_evaluator(run_simulation)` e passar como `evaluate_fn` no GA/ilhas.
- Gerar relatório completo (fronteira + métricas + sumário):
    `python scripts/mes8_generate_report.py --frontier_csv runs/frontier.csv --metrics_csv runs/islands_metrics.csv --out_dir reports/mes8`
- Exportar fronteira direto do GA/ilhas para CSV: `from mes8_optimization.frontier_export import save_frontier_csv` e salvar para usar no relatório.
