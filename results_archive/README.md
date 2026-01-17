# Results Archive - Sistema de Organização

Bem-vindo ao arquivo centralizado de resultados do projeto Training 12 Meses. Este sistema oferece uma solução elegante para guardar resultados experimentais mantendo referências aos locais originais.

## 🎯 Objetivo

- ✅ **Centralizar** todos os arquivos de resultados dispersos
- ✅ **Preservar** informações sobre localizações originais
- ✅ **Facilitar** recuperação quando necessário
- ✅ **Manter** workspace organizado sem perder dados
- ✅ **Rastrear** origem e data de cada arquivo

## 📂 Estrutura

```
results_archive/
├── INDEX.md                          # Índice completo do archive
├── LOCATIONS_MAP.md                  # Mapa detalhado de origens
├── QUICK_REFERENCE.md                # Referência rápida (COMECE AQUI!)
├── manage_results_archive.ps1        # Script de gerenciamento
├── README.md                         # Este arquivo
│
├── federated_learning/               # Mes 10 - Federated Learning
│   ├── federated_convergence_*.png
│   ├── federated_results_*.csv
│   ├── demo_output.txt
│   └── hybrid_demo.txt
│
├── optimization/                     # Mes 8 - Advanced Optimization
│   ├── nsga2/                        # Algoritmo NSGA-II
│   │   ├── *convergence*.png
│   │   ├── *history*.csv
│   │   ├── *metadata*.json
│   │   ├── *pareto_frontier*.csv
│   │   └── *validation_results*.csv
│   ├── constrained/                  # Otimização com restrições
│   │   ├── *constraints*.json
│   │   ├── *solutions*.csv
│   │   ├── *constraint_analysis*.json
│   │   └── *feasibility_analysis*.json
│   ├── sensitivity/                  # Análise de sensibilidade
│   │   ├── *morris_screening*.csv/.png
│   │   ├── *sobol_indices*.csv/.png
│   │   └── *parameter_ranking*.json
│   └── experiments/                  # MLflow tracking data
│       ├── metrics_*.json
│       ├── solutions_*.csv
│       └── mlruns/
│
├── piml/                             # Mes 4 - Physics-Informed ML
│   └── surrogate_xgboost.pkl        # Modelo treinado
│
├── datasets/                         # Dados de Pesquisa
│   ├── datasets_comparison_table.csv
│   ├── tropical_datasets_quick_access.csv
│   └── COMPLETION_SUMMARY.txt
│
└── research_papers/                  # Literatura
    └── result_*.pdf                  # 7 papers de revisão
```

## 🚀 Quick Start

### 1. **Ver o que tem no archive**
```powershell
.\manage_results_archive.ps1 -Action list -Category all
```

### 2. **Encontrar um arquivo específico**
Abra `QUICK_REFERENCE.md` para uma tabela "se você quer... procure em..."

### 3. **Consultar origem de um arquivo**
```powershell
# Abra LOCATIONS_MAP.md para ver exatamente onde cada arquivo estava
cat .\LOCATIONS_MAP.md
```

### 4. **Recuperar arquivo para local original**
```powershell
# Copiar (mantém original no archive)
.\manage_results_archive.ps1 -Action restore -Category federated_learning

# Mover (remove do archive)
.\manage_results_archive.ps1 -Action move -Category optimization
```

## � Novo Procedimento: Arquivamento de Resultados

A partir de **17 de Janeiro de 2026**, implementamos um novo procedimento para arquivar resultados experimentais. Este sistema oferece:

### ✨ Características

- **Centralização Automática**: Todos os outputs são arquivados em um único local
- **Rastreamento Completo**: Cada arquivo é mapeado com sua origem original em `LOCATIONS_MAP.md`
- **Limpeza do Workspace**: Após arquivar, os arquivos originais são removidos, mantendo o workspace organizado
- **Recuperação Simples**: Use `manage_results_archive.ps1` para restaurar qualquer arquivo
- **Sem Perda de Dados**: Nada é deletado permanentemente - tudo está documentado e recuperável

### 🔄 Como Funciona

```
1. Experimento executa → gera resultados
   ↓
2. Resultados são COPIADOS para results_archive/
   ↓
3. Origem é registrada em LOCATIONS_MAP.md
   ↓
4. Arquivos ORIGINAIS são DELETADOS do workspace
   ↓
5. Workspace fica limpo, dados estão seguros no archive
```

### 📋 Passo-a-Passo para Arquivar Novos Resultados

**Exemplo: Arquivar resultados do Mes 11 (Advanced Analytics)**

```powershell
# 1. Criar novo subdiretório no archive
mkdir "results_archive\advanced_analytics" -Force

# 2. Copiar arquivos de resultados
Copy-Item "Science AI Engineering\mes11_advanced_analytics\results\*" `
          "results_archive\advanced_analytics\" -Recurse -Force

# 3. Documentar origem em LOCATIONS_MAP.md
# (Adicione uma nova seção com detalhes dos arquivos)

# 4. Deletar originais para limpar workspace
Remove-Item "Science AI Engineering\mes11_advanced_analytics\results\*" -Force -Recurse

# 5. Atualizar INDEX.md com informações da nova categoria
```

### 🎯 Benefícios da Nova Abordagem

| Antes | Depois |
|-------|--------|
| ❌ Resultados espalhados | ✅ Tudo centralizado |
| ❌ Difícil encontrar | ✅ Documentado em QUICK_REFERENCE.md |
| ❌ Workspace bagunçado | ✅ Workspace limpo |
| ❌ Sem rastreabilidade | ✅ Origem mapeada em LOCATIONS_MAP.md |
| ❌ Risco de perda | ✅ Backup automático em archive |

### 📍 Status Atual (17 de Janeiro de 2026)

✅ **Limpeza Inicial Concluída**
- 49 arquivos antigos removidos do workspace
- 58 arquivos preservados no archive
- Todas as origens documentadas
- Veja [CLEANUP_COMPLETE.md](CLEANUP_COMPLETE.md) para detalhes

## �📊 Conteúdo Atual

| Categoria | Quantidade | Tipos | Tamanho |
|-----------|-----------|-------|--------|
| Federated Learning | 8 | PNG, CSV, TXT | ~400 KB |
| Optimization | 22 | JSON, CSV, PNG | ~5 MB |
| PIML | 1 | PKL | ~500 KB |
| Datasets | 9 | CSV, TXT | ~100 KB |
| Research Papers | 10 | PDF | ~50 MB |
| **TOTAL** | **50+** | **Múltiplos** | **~56 MB** |

**Status**: ✅ Todos os arquivos estão no archive (workspace limpo desde 17 de Jan de 2026)

## 🔍 Como Usar

### Arquivo de Índices

| Arquivo | Propósito | Acesso |
|---------|-----------|--------|
| **INDEX.md** | Índice estruturado completo | Detalhes técnicos |
| **LOCATIONS_MAP.md** | Mapa origem → archive | Onde cada arquivo estava |
| **QUICK_REFERENCE.md** | Guia rápido por categoria | Começar aqui! |
| **manage_results_archive.ps1** | Script automático | Operações em massa |

### Cenários de Uso

**📋 Cenário 1: Encontrar resultados de Pareto**
```
1. Abrir QUICK_REFERENCE.md
2. Procurar "Pareto"
3. Ir para: results_archive/optimization/nsga2/
4. Abrir: pareto_frontier_20260116_170241.csv
```

**📋 Cenário 2: Recuperar todos os PLOTs de convergência**
```powershell
# Listar todas as imagens de convergência
Get-ChildItem results_archive -Recurse -Filter "*convergence*.png"

# Copiar para Desktop para visualização rápida
Copy-Item "results_archive\*\*convergence*.png" "$env:USERPROFILE\Desktop" -Recurse
```

**📋 Cenário 3: Arquivar novo resultado (Mes 9 - Production Deployment)**
```powershell
# NOVO PROCEDIMENTO: Arquivar automaticamente após experimento

# 1. Criar diretório no archive
mkdir "results_archive\production_deployment" -Force

# 2. Copiar arquivos (mantém originals)
Copy-Item "Science AI Engineering\mes9_production\results\*" `
          "results_archive\production_deployment\" -Recurse -Force

# 3. Registrar origem em LOCATIONS_MAP.md
# Adicione uma nova seção com formato:
# | arquivo.ext | Science AI Engineering/mes9_production/results/ | CSV | 2026-01-17 |

# 4. Deletar originais para limpar workspace
Remove-Item "Science AI Engineering\mes9_production\results\*" -Force -Recurse

# 5. Atualizar documentação
# - Adicionar seção em INDEX.md
# - Atualizar count em README.md
# - Adicionar em QUICK_REFERENCE.md se necessário
```

**⚠️ IMPORTANTE**: Este é o novo procedimento padrão desde 17 de Janeiro de 2026. Todo resultado deve ser arquivado para manter o workspace organizado!

## 💾 Política de Retenção

### Arquivos NO ARCHIVE (nunca deletar automaticamente):
- Modelos treinados (.pkl, .h5) - podem ser usados em produção
- Data files (CSV) com dados numéricos - rastreabilidade
- Configurações de experimentos (JSON) - reproducibilidade
- Fronteiras Pareto - literatura científica

### Arquivos SEGUROS PARA DELETAR (após arquivar):
- Imagens de monitoramento (PNG) > 60 dias
- Logs de execução (.txt) > 30 dias
- Arquivos temporários (.tmp) > 7 dias

### Nunca deletar:
- Modelos treinados
- Dados de pesquisa
- Histórico de versões
- Papers/literatura

## 🔄 Recuperação e Sincronização

### Manter Backup
```powershell
# Fazer backup do archive
Robocopy "results_archive" "D:\backup\results_archive_$(Get-Date -Format yyyyMMdd)" /E /R:1

# Sincronizar com local remoto (se usando cloud storage)
Robocopy "results_archive" "C:\OneDrive\FAPESP_Backup\results" /MIR
```

### Restaurar Seletivamente
```powershell
# Restaurar apenas Pareto frontiers
Copy-Item "results_archive\optimization\nsga2\pareto_*.csv" `
          "Science AI Engineering\mes8_optimization\results\nsga2\" -Force

# Restaurar modelos PIML
Copy-Item "results_archive\piml\*.pkl" `
          "Science AI Engineering\mes4_piml\models\" -Force
```

## 🛠️ Script de Gerenciamento

O arquivo `manage_results_archive.ps1` oferece:

```powershell
# Listar arquivos
.\manage_results_archive.ps1 -Action list -Category all
.\manage_results_archive.ps1 -Action list -Category optimization

# Copiar para archive
.\manage_results_archive.ps1 -Action copy -Category federated_learning

# Restaurar do archive
.\manage_results_archive.ps1 -Action restore -Category piml

# Mover (delete do archive após mover)
.\manage_results_archive.ps1 -Action move -Category optimization

# Verificar integridade
.\manage_results_archive.ps1 -Action verify
```

## 📈 Visualizar Resultados

### Gráficos de Convergência
```
results_archive/
├── federated_learning/
│   └── federated_convergence_*.png        # Federated Learning
├── optimization/nsga2/
│   └── nsga2_convergence_*.png            # NSGA-II
└── optimization/sensitivity/
    └── *morris_screening*.png             # Análise Morris
```

### Dados Numéricos
```
results_archive/optimization/nsga2/pareto_frontier_20260116_170241.csv

# Para visualizar:
Import-Csv "pareto_frontier_20260116_170241.csv" | Format-Table
```

## 🔐 Versioning & Git

Recomendações para versionamento:

```bash
# NÃO versionar arquivos grandes
echo "results_archive/research_papers/*.pdf" >> .gitignore
echo "results_archive/*/*.pkl" >> .gitignore
echo "results_archive/**/*.csv" >> .gitignore  # Opcional

# VERSIONAR apenas índices
git add results_archive/INDEX.md
git add results_archive/LOCATIONS_MAP.md
git add results_archive/QUICK_REFERENCE.md
git add results_archive/manage_results_archive.ps1
git add results_archive/README.md
```

## 📞 FAQ

**P: Por que não deletar os arquivos originais?**  
R: Mantemos referências cruzadas e permitem recuperação se houver mudanças de organização.

**P: Quanto espaço o archive usa?**  
R: ~56 MB atualmente. Maior contribuinte: research papers (~50 MB).

**P: Posso mover o archive para outro lugar?**  
R: Sim! Atualize os caminhos em `manage_results_archive.ps1` e `LOCATIONS_MAP.md`.

**P: Como adicionar novos resultados?**  
R: 1) Crie subdiretório, 2) Copie arquivos, 3) Atualize `LOCATIONS_MAP.md`, 4) Atualize `INDEX.md`.

**P: Os arquivos estão sincronizados com Git?**  
R: Não (são grandes). Versione apenas os índices (INDEX.md, LOCATIONS_MAP.md).

## 🎓 Próximos Meses

Ao adicionar resultados dos próximos meses:

```
Mes 11 - Advanced Analytics
└── results_archive/advanced_analytics/
    ├── dashboards/
    ├── statistical_tests/
    └── predictive_models/

Mes 12 - Capstone
└── results_archive/capstone/
    ├── final_models/
    ├── business_metrics/
    └── presentations/
```

---

**Criado**: 17 de Janeiro de 2026  
**Última Atualização**: 17 de Janeiro de 2026  
**Mantido por**: Copilot AI Engineering  
**Próxima Revisão**: Quando adicionar Mes 11 ou 12

---

## 🆕 Novo Procedimento de Arquivo - Resumo Executivo

### O Que Mudou?

A partir de **17 de Janeiro de 2026**, implementamos um procedimento sistemático para arquivar resultados:

1. **Antes**: Resultados espalhados pelo workspace, difíceis de encontrar
2. **Depois**: Tudo centralizado em `results_archive/`, workspace limpo

### Checklist para Próximos Experimentos

```
□ Experimento gera resultados em Science AI Engineering/mes[X]/results/
□ Copiar resultados para results_archive/[categoria]/
□ Registrar origem em LOCATIONS_MAP.md
□ Deletar originais do workspace
□ Atualizar documentação (INDEX, QUICK_REFERENCE)
□ Verificar com: .\manage_results_archive.ps1 -Action verify
```

### Documentação Relacionada

- 📋 [CLEANUP_COMPLETE.md](CLEANUP_COMPLETE.md) - Detalhes da limpeza inicial (49 arquivos removidos)
- 🗺️ [LOCATIONS_MAP.md](LOCATIONS_MAP.md) - Mapa de origem de cada arquivo
- 📘 [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Guia rápido para encontrar arquivos
- 🎯 [START_HERE.md](START_HERE.md) - Ponto de entrada para usuários novos

### Suporte

Se tiver dúvidas sobre o novo procedimento:
1. Leia [CLEANUP_COMPLETE.md](CLEANUP_COMPLETE.md) para entender como funcionou
2. Consulte [README.md](README.md) seção "Novo Procedimento"
3. Execute `.\manage_results_archive.ps1 -Action list` para ver exemplos
