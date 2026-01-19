# Quick Reference - Results Archive Navigation

## 📂 Onde encontrar o quê

### Resultados de Federated Learning (Mes 10)
```
results_archive/federated_learning/
├── federated_convergence_*.png         # Gráficos de convergência
├── federated_results_*.csv             # Dados de treinamento
└── Origem: Raiz (/) e Science AI Engineering/mes10_federated_learning/
```
**Usar quando**: Apresentações sobre aprendizado federado, análise de convergência

---

### Resultados de Otimização (Mes 8)
```
results_archive/optimization/
├── nsga2/                              # Algoritmo NSGA-II
│   ├── *convergence*.png               # Gráfico de convergência
│   ├── *history*.csv                   # Histórico de otimização
│   ├── *pareto_frontier*.csv           # Soluções Pareto
│   ├── *metadata*.json                 # Config do experimento
│   └── *validation_results*.csv        # Métricas de validação
│
├── constrained/                        # Otimização com restrições
│   ├── *constraints*.json              # Definições de restrições
│   ├── *solutions*.csv                 # Soluções ótimas
│   ├── *constraint_analysis*.json      # Análise detalhada
│   └── *feasibility_analysis*.json     # Análise de viabilidade
│
└── sensitivity/                        # Análise de sensibilidade
    ├── *morris_screening*.csv/png      # Análise Morris
    ├── *sobol_indices*.csv/png         # Índices de Sobol
    └── *parameter_ranking*.json        # Ranking de parâmetros
```
**Usar quando**: Publicações científicas, otimizações de design, análise de parametrização

---

### Models Treinados (PIML - Mes 4)
```
results_archive/piml/
├── surrogate_xgboost.pkl               # Modelo substituto XGBoost
└── Origem: Science AI Engineering/mes4_piml/models/
```
**Usar quando**: Inferência rápida, comparações de surrogate models

---

### Dados de Pesquisa
```
results_archive/datasets/
├── datasets_comparison_table.csv       # Tabela comparativa de datasets
├── tropical_datasets_quick_access.csv  # Acesso rápido aos datasets
└── COMPLETION_SUMMARY.txt              # Resumo de completude

results_archive/research_papers/
├── result_*.pdf                        # 7 papers de revisão sistemática
└── Temas: Machine Learning, Clima Tropical, Building Performance
```
**Usar quando**: Literatura review, seleção de datasets, pesquisa de metodologias

---

## 🔍 Procurando por um arquivo específico?

| Se você quer... | Procure em... |
|---|---|
| Convergência de federated learning | `federated_learning/federated_convergence_*.png` |
| Fronteira Pareto da otimização | `optimization/nsga2/pareto_frontier_*.csv` |
| Sensibilidade de parâmetros | `optimization/sensitivity/*.csv` |
| Modelos treinados | `piml/surrogate_*.pkl` |
| Datasets disponíveis | `datasets/tropical_datasets_quick_access.csv` |
| Papers de pesquisa | `research_papers/result_*.pdf` |

---

## 📋 Estatísticas do Archive

- **Total de arquivos**: 35+
- **Federated Learning**: 8 arquivos (PNG + CSV)
- **Optimization**: 20+ arquivos (CSV, JSON, PNG)
- **PIML**: 1 modelo treinado
- **Datasets**: 3 arquivos
- **Research Papers**: 7 PDFs

---

## 🔄 Recuperar Arquivo Original

Se precisar mover um arquivo de volta para sua localização original:

1. **Encontre** o arquivo em `results_archive/`
2. **Consulte** `LOCATIONS_MAP.md` para a localização exata
3. **Execute** o comando apropriado:

```powershell
# Exemplo: Mover convergência Pareto para mes8
Move-Item "results_archive\optimization\nsga2\pareto_*.csv" `
          "Science AI Engineering\mes8_optimization\results\nsga2\" -Force
```

---

## 💾 Política de Retenção

| Tipo | Mantém-se em | Quando Arquivar |
|---|---|---|
| Imagens (PNG) | 60 dias | Se documentado em relatório |
| Dados (CSV/JSON) | Indefinido | Nunca (rastreabilidade) |
| Modelos (.pkl) | Indefinido | Nunca (podem ser usados) |
| Logs (.txt) | 30 dias | Se não mais necessário |

---

## 📝 Adicionar Novos Resultados

Para adicionar um novo resultado ao archive:

1. Crie subdiretório em `results_archive/` (ex: `results_archive/novo_mes/`)
2. Copie arquivos: `Copy-Item "caminho_origem\*" "results_archive\novo_mes\" -Recurse`
3. Atualize `LOCATIONS_MAP.md` com detalhes
4. Atualize este arquivo se for categoria frequente

---

**Última atualização**: 17 de janeiro de 2026  
**Mantido por**: Sistema de Archive Automático  
**Contato para consultas**: Verifique `INDEX.md` para mais detalhes
