# Results Files - Original Locations Map

## Federated Learning (Mes 10)

| Arquivo | Localização Original | Tipo | Tamanho | Data | Recuperável em | Status |
|---------|-------------------|------|--------|------|----------------|--------|
| federated_convergence_20260116_172358.png | Root (/) | PNG Image | ~45 KB | 2026-01-16 17:23:58 | Sempre | Não arquivado |
| federated_convergence_20260116_172359.png | Root (/) | PNG Image | ~45 KB | 2026-01-16 17:23:59 | Sempre | Não arquivado |
| federated_convergence_20260116_172400.png | Root (/) | PNG Image | ~45 KB | 2026-01-16 17:24:00 | Sempre | Não arquivado |
| federated_convergence_20260116_172404.png | Root (/) | PNG Image | ~45 KB | 2026-01-16 17:24:04 | Sempre | Não arquivado |
| federated_convergence_20260116_172405.png | Root (/) | PNG Image | ~45 KB | 2026-01-16 17:24:05 | Sempre | Não arquivado |
| federated_convergence_20260116_172406.png | Root (/) | PNG Image | ~45 KB | 2026-01-16 17:24:06 | Sempre | Não arquivado |
| federated_results_20260116_172401.csv | Root (/) | CSV Data | ~20 KB | 2026-01-16 17:24:01 | Sempre | Não arquivado |
| federated_results_20260116_172407.csv | Root (/) | CSV Data | ~20 KB | 2026-01-16 17:24:07 | Sempre | Não arquivado |
| demo_output.txt | Science AI Engineering/mes10_federated_learning/ | Text | ~5 KB | 2026-01-16 | Sempre | Não arquivado |
| hybrid_demo.txt | Science AI Engineering/mes10_federated_learning/ | Text | ~5 KB | 2026-01-16 | Sempre | Não arquivado |

## Optimization (Mes 8)

### NSGA-II Results
| Arquivo | Localização Original | Tipo | Data | Recuperável em |
|---------|-------------------|------|------|----------------|
| nsga2_convergence_20260116_170241.png | Science AI Engineering/mes8_optimization/results/nsga2/ | PNG | 2026-01-16 17:02:41 | Sempre |
| optimization_history_20260116_170241.csv | Science AI Engineering/mes8_optimization/results/nsga2/ | CSV | 2026-01-16 17:02:41 | Sempre |
| optimization_metadata_20260116_170241.json | Science AI Engineering/mes8_optimization/results/nsga2/ | JSON | 2026-01-16 17:02:41 | Sempre |
| pareto_frontier_20260116_170241.csv | Science AI Engineering/mes8_optimization/results/nsga2/ | CSV | 2026-01-16 17:02:41 | Sempre |
| validation_results_20260116_170241.csv | Science AI Engineering/mes8_optimization/results/nsga2/ | CSV | 2026-01-16 17:02:41 | Sempre |

### Constrained Optimization
| Arquivo | Localização Original | Tipo | Data |
|---------|-------------------|------|------|
| constrained_solutions_20260116_170829.csv | Science AI Engineering/mes8_optimization/results/constrained/ | CSV | 2026-01-16 17:08:29 |
| constrained_solutions_20260116_170852.csv | Science AI Engineering/mes8_optimization/results/constrained/ | CSV | 2026-01-16 17:08:52 |
| constraints_20260116_170829.json | Science AI Engineering/mes8_optimization/results/constrained/ | JSON | 2026-01-16 17:08:29 |
| constraints_20260116_170852.json | Science AI Engineering/mes8_optimization/results/constrained/ | JSON | 2026-01-16 17:08:52 |
| constraint_analysis_20260116_170829.json | Science AI Engineering/mes8_optimization/results/constrained/ | JSON | 2026-01-16 17:08:29 |
| constraint_analysis_20260116_170852.json | Science AI Engineering/mes8_optimization/results/constrained/ | JSON | 2026-01-16 17:08:52 |
| feasibility_analysis_20260116_170829.json | Science AI Engineering/mes8_optimization/results/constrained/ | JSON | 2026-01-16 17:08:29 |
| feasibility_analysis_20260116_170852.json | Science AI Engineering/mes8_optimization/results/constrained/ | JSON | 2026-01-16 17:08:52 |

### Sensitivity Analysis (Morris & Sobol)
| Arquivo | Localização Original | Tipo | Data |
|---------|-------------------|------|------|
| morris_screening_20260116_170533.csv | Science AI Engineering/mes8_optimization/results/sensitivity/ | CSV | 2026-01-16 17:05:33 |
| morris_screening_20260116_170534.png | Science AI Engineering/mes8_optimization/results/sensitivity/ | PNG | 2026-01-16 17:05:34 |
| parameter_ranking_20260116_170533.json | Science AI Engineering/mes8_optimization/results/sensitivity/ | JSON | 2026-01-16 17:05:33 |
| sobol_indices_20260116_170533.csv | Science AI Engineering/mes8_optimization/results/sensitivity/ | CSV | 2026-01-16 17:05:33 |
| sobol_indices_20260116_170533.png | Science AI Engineering/mes8_optimization/results/sensitivity/ | PNG | 2026-01-16 17:05:33 |

### Experiments (MLflow Tracking)
| Tipo | Localização Original | Descrição |
|------|-------------------|----------|
| Metrics JSON | Science AI Engineering/mes8_optimization/results/experiments/ | 6 experiment runs (IDs: 5aacefae, 8bc3360f, 93521e09, a179c1b4, f4a52b4a, fd7563c6) |
| Solutions CSV | Science AI Engineering/mes8_optimization/results/experiments/ | Corresponding solution files for each run |
| MLflow Artifacts | Science AI Engineering/mes8_optimization/results/experiments/mlruns/ | Complete MLflow tracking data |

## Physics-Informed ML (Mes 4)

| Arquivo | Localização Original | Tipo | Tamanho | Data |
|---------|-------------------|------|--------|------|
| surrogate_xgboost.pkl | Science AI Engineering/mes4_piml/models/ | Python Pickle | ~500 KB | 2026-01-16 |


### Arquivos NÃO DELETADOS (atualmente no workspace):
- Mantidos em posição original para facilitar recuperação
- Referência cruzada disponível em `results_archive/`
- Pode ser movido para arquivo quando não mais necessário

### Arquivos SEGUROS PARA ARQUIVAR:
Qualquer arquivo datado de mais de 30 dias pode ser arquivado se:
1. Seu resultado foi documentado em relatórios ou markdowns
2. Backup existe em `results_archive/`
3. Caminho original é registrado em LOCATIONS_MAP.md

### Arquivos A PRESERVAR:
- Modelos treinados (.pkl, .h5) - usados em produção ou referência
- JSONs de configuração de experimentos - rastreabilidade
- CSVs de Pareto frontiers - dados de pesquisa
- PNGs de visualizações - documentação de projeto

## Recovery Commands

### Mover todos os resultados de Federated Learning
```powershell
$src = "C:\Users\joaop\Downloads\FAPESP\Training_12Meses\results_archive\federated_learning"
$dst = "C:\Users\joaop\Downloads\FAPESP\Training_12Meses\Science AI Engineering\mes10_federated_learning"
Move-Item "$src\*" $dst -Force
```

### Copiar (sem deletar) para arquivo
```powershell
$src = "C:\Users\joaop\Downloads\FAPESP\Training_12Meses"
$dst = "C:\Users\joaop\Downloads\FAPESP\Training_12Meses\results_archive"

# Federated Learning
Copy-Item "$src\federated_*.png" "$dst\federated_learning" -Force
Copy-Item "$src\federated_*.csv" "$dst\federated_learning" -Force

# Outras categorias conforme necessário
```

## Status Atual (17 de Janeiro de 2026)

✅ **Arquivos mapeados**: 35+ arquivos
✅ **Estrutura preparada**: `results_archive/` criado
✅ **Índices criados**: INDEX.md e LOCATIONS_MAP.md
⏳ **Próximo passo**: Mover/copiar arquivos para subdiretórios conforme necessário

## Notas

1. Todos os timestamps estão em formato 24h (YYYYMMDDhhmmss)
2. "Sempre" em "Recuperável em" significa que o arquivo nunca será deletado automaticamente
3. Para adicionar novos resultados, atualize apenas este arquivo
4. Estrutura modular permite fácil expansão para novos meses/projetos
