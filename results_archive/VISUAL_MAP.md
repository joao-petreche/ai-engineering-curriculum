# Mapa Visual do Archive

## 🗂️ Estrutura Completa

```
c:\Users\joaop\Downloads\FAPESP\Training_12Meses\
│
├── results_archive/                          [🎯 NOVO - SEUS RESULTADOS AQUI]
│   │
│   ├── 📄 INDEX.md                           Índice completo do sistema
│   ├── 📄 LOCATIONS_MAP.md                   ⭐ Mapa de onde cada arquivo estava
│   ├── 📄 QUICK_REFERENCE.md                 👈 COMECE AQUI - Guia rápido
│   ├── 📄 README.md                          Documentação detalhada
│   ├── 📄 SETUP_COMPLETE.md                  Este resumo
│   ├── 📜 manage_results_archive.ps1         Script PowerShell de gerenciamento
│   │
│   ├── 📁 federated_learning/                [Mes 10 - Aprendizado Federado]
│   │   ├── federated_convergence_20260116_172358.png
│   │   ├── federated_convergence_20260116_172359.png
│   │   ├── federated_convergence_20260116_172400.png
│   │   ├── federated_convergence_20260116_172404.png
│   │   ├── federated_convergence_20260116_172405.png
│   │   ├── federated_convergence_20260116_172406.png
│   │   ├── federated_results_20260116_172401.csv
│   │   ├── federated_results_20260116_172407.csv
│   │   ├── demo_output.txt
│   │   └── hybrid_demo.txt
│   │   [8 arquivos, ~400 KB]
│   │
│   ├── 📁 optimization/                      [Mes 8 - Otimização Avançada]
│   │   │
│   │   ├── 📁 nsga2/                         Resultados NSGA-II
│   │   │   ├── nsga2_convergence_20260116_170241.png
│   │   │   ├── optimization_history_20260116_170241.csv
│   │   │   ├── optimization_metadata_20260116_170241.json
│   │   │   ├── pareto_frontier_20260116_170241.csv     ⭐ Importantíssimo
│   │   │   └── validation_results_20260116_170241.csv
│   │   │   [5 arquivos]
│   │   │
│   │   ├── 📁 constrained/                   Otimização com Restrições
│   │   │   ├── constrained_solutions_20260116_170829.csv
│   │   │   ├── constrained_solutions_20260116_170852.csv
│   │   │   ├── constraints_20260116_170829.json
│   │   │   ├── constraints_20260116_170852.json
│   │   │   ├── constraint_analysis_20260116_170829.json
│   │   │   ├── constraint_analysis_20260116_170852.json
│   │   │   ├── feasibility_analysis_20260116_170829.json
│   │   │   └── feasibility_analysis_20260116_170852.json
│   │   │   [8 arquivos]
│   │   │
│   │   ├── 📁 sensitivity/                   Análise de Sensibilidade
│   │   │   ├── morris_screening_20260116_170533.csv
│   │   │   ├── morris_screening_20260116_170534.png
│   │   │   ├── parameter_ranking_20260116_170533.json
│   │   │   ├── sobol_indices_20260116_170533.csv
│   │   │   └── sobol_indices_20260116_170533.png
│   │   │   [5 arquivos]
│   │   │
│   │   ├── 📁 experiments/                   MLflow Tracking Data
│   │   │   ├── metrics_5aacefae657c4e159c22b5bc8....json
│   │   │   ├── solutions_5aacefae657c4e159c22b5b....csv
│   │   │   ├── metrics_8bc3360f6afc47d3b0b7708....json
│   │   │   ├── solutions_8bc3360f6afc47d3b0b7708....csv
│   │   │   ├── ... [mais 4 pares]
│   │   │   └── mlruns/                       MLflow artifacts
│   │   │       └── 493079306035633638/       Run ID
│   │   │           ├── 5aacefae657c4...
│   │   │           ├── 8bc3360f6afc4...
│   │   │           ├── 93521e0997e9...
│   │   │           ├── a179c1b435b7...
│   │   │           ├── f4a52b4a17f5...
│   │   │           └── fd7563c6e7e3...
│   │   │   [6+ arquivos + MLflow tree]
│   │   │
│   │   [20+ arquivos, ~5 MB]
│   │
│   ├── 📁 piml/                              [Mes 4 - Physics-Informed ML]
│   │   └── surrogate_xgboost.pkl             ⭐ Modelo treinado reutilizável
│   │   [1 arquivo, ~500 KB]
│   │
│   ├── 📁 datasets/                          [Dados de Pesquisa]
│   │   ├── datasets_comparison_table.csv     Tabela comparativa
│   │   ├── tropical_datasets_quick_access.csv ⭐ Acesso rápido
│   │   └── COMPLETION_SUMMARY.txt
│   │   [3 arquivos, ~100 KB]
│   │
│   └── 📁 research_papers/                   [Literatura & Pesquisa]
│       ├── result_Chakraborty_e_Elzarka_2019.pdf
│       ├── result_Forouzandeh_et_al_2023.pdf
│       ├── result_Jiang_et_al_2025.pdf
│       ├── result_Markarian_et_al_2024.pdf
│       ├── result_Tian_2024.pdf
│       ├── result_Villano_et_al_2024.pdf
│       └── result_Wang_et_al_2025.pdf
│       [7 PDFs, ~50 MB]
│
├── Science AI Engineering/
│   ├── mes4_piml/
│   │   └── models/
│   │       └── [VAZIO - modelo está em results_archive/piml/]
│   │
│   ├── mes8_optimization/
│   │   └── results/
│   │       └── [VAZIO - resultados estão em results_archive/optimization/]
│   │
│   └── mes10_federated_learning/
│       └── [VAZIO - outputs estão em results_archive/federated_learning/]
│
├── README.md
├── Scientific_AI_Engineering_Curriculum.md  [Currículo em Inglês]
└── ... [outros arquivos do workspace]
```

---

## 🎯 Navegação Rápida

### 📍 Estou procurando... ➜ Procure em...

| Você quer | Arquivo | Localização |
|-----------|---------|-------------|
| **Gráfico de Convergência Federada** | `federated_convergence_*.png` | `results_archive/federated_learning/` |
| **Fronteira Pareto (NSGA-II)** | `pareto_frontier_*.csv` | `results_archive/optimization/nsga2/` |
| **Análise de Sensibilidade (Sobol)** | `sobol_indices_*.csv` | `results_archive/optimization/sensitivity/` |
| **Análise de Sensibilidade (Morris)** | `morris_screening_*.csv/.png` | `results_archive/optimization/sensitivity/` |
| **Soluções Otimizadas com Restrições** | `constrained_solutions_*.csv` | `results_archive/optimization/constrained/` |
| **Modelo XGBoost Treinado** | `surrogate_xgboost.pkl` | `results_archive/piml/` |
| **Métricas de Validação** | `validation_results_*.csv` | `results_archive/optimization/nsga2/` |
| **Histórico de Otimização** | `optimization_history_*.csv` | `results_archive/optimization/nsga2/` |
| **Análise de Restrições** | `constraint_analysis_*.json` | `results_archive/optimization/constrained/` |
| **Datasets Disponíveis** | `tropical_datasets_quick_access.csv` | `results_archive/datasets/` |
| **Papers de Pesquisa** | `result_*.pdf` | `results_archive/research_papers/` |
| **Dados MLflow** | `metrics_*.json` | `results_archive/optimization/experiments/` |

---

## 🔄 Fluxo de Recuperação

```
Quer um arquivo de volta no lugar original?

1. Abra LOCATIONS_MAP.md
   ↓
2. Procure o arquivo
   ↓
3. Veja a coluna "Localização Original"
   ↓
4. Execute no PowerShell:
   .\manage_results_archive.ps1 -Action restore -Category [categoria]
   ↓
5. Arquivo está de volta no local original!
```

---

## 📊 Estatísticas por Categoria

```
┌─────────────────────────────────────────────────────────┐
│                    FEDERATED LEARNING                   │
├─────────────────────────────────────────────────────────┤
│ 8 arquivos | 400 KB | PNG: 6 | CSV: 2 | TXT: 0         │
│ Origem: Science AI Engineering/mes10_federated_learning │
│ Uso: Aprendizado Federado, demonstrações              │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                      OPTIMIZATION                       │
├─────────────────────────────────────────────────────────┤
│ 20+ arquivos | 5 MB | JSON: 8 | CSV: 10 | PNG: 3      │
│ Subkategorias: NSGA-II, Constrained, Sensitivity       │
│ Origem: Science AI Engineering/mes8_optimization/      │
│ Uso: Otimização multi-objetivo, análise de params      │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│              PHYSICS-INFORMED ML (PIML)                 │
├─────────────────────────────────────────────────────────┤
│ 1 arquivo | 500 KB | PKL: 1                            │
│ Origem: Science AI Engineering/mes4_piml/models/       │
│ Uso: Modelos surrogate, inferência rápida              │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                      DATASETS                           │
├─────────────────────────────────────────────────────────┤
│ 3 arquivos | 100 KB | CSV: 2 | TXT: 1                  │
│ Origem: External project (archived)                     │
│ Uso: Referência de datasets disponíveis               │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                  RESEARCH PAPERS                        │
├─────────────────────────────────────────────────────────┤
│ 7 arquivos | 50 MB | PDF: 7                            │
│ Origem: External project (archived)                     │
│ Uso: Literatura, revisão sistemática                   │
│ Papers: Chakraborty, Forouzandeh, Jiang, Markarian,   │
│         Tian, Villano, Wang                            │
└─────────────────────────────────────────────────────────┘

TOTAL: 55+ arquivos | 56 MB | Pronto para uso!
```

---

## 🗺️ Mapa de Documentação

```
results_archive/
│
├─ 📘 QUICK_REFERENCE.md
│  └─ Leia primeiro!
│     • Tabela "Procure por"
│     • Exemplos práticos
│     • Statísticas
│
├─ 🗺️ LOCATIONS_MAP.md
│  └─ Rastreie origens
│     • Cada arquivo mapeado
│     • Data de criação
│     • Tipo de arquivo
│
├─ 📗 README.md
│  └─ Guia completo
│     • Exemplos PowerShell
│     • FAQs detalhadas
│     • Integração Git
│
├─ 📕 INDEX.md
│  └─ Índice técnico
│     • Organização detalhada
│     • Política de retenção
│     • Procedimentos avançados
│
├─ ✨ SETUP_COMPLETE.md
│  └─ Resumo de conclusão
│     • O que foi feito
│     • Vantagens
│     • Próximos passos
│
└─ ⚙️ manage_results_archive.ps1
   └─ Automação PowerShell
      • list (listar)
      • copy (copiar)
      • restore (restaurar)
      • move (mover)
      • verify (verificar)
```

---

## ✅ Checklist de Uso

- [ ] Li `QUICK_REFERENCE.md`
- [ ] Consulti `LOCATIONS_MAP.md`
- [ ] Executei `manage_results_archive.ps1 -Action list`
- [ ] Encontrei meus arquivos em `results_archive/`
- [ ] Copiei um arquivo para meu desktop
- [ ] Restaurei um arquivo para local original
- [ ] Verifiquei integridade com `verify`
- [ ] Entendi como adicionar novos resultados

---

**Estrutura criada em**: 17 de Janeiro de 2026  
**Total de arquivos**: 55+  
**Espaço utilizado**: 21.25 MB  
**Status**: ✅ Pronto para uso
