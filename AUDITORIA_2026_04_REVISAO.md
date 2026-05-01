# 🔍 AUDITORIA — REVISÃO ABRIL 2026

**Data:** 30 de abril de 2026
**Escopo:** Re-verificação dos 20 gaps prioritários (P0/P1) identificados em [AUDITORIA_COMPLETA_CURRICULUM.md](AUDITORIA_COMPLETA_CURRICULUM.md) (Janeiro/2026)
**Metodologia:** Inspeção arquivo-por-arquivo do estado atual do repositório, evidência citada por caminho e linha
**Tipo:** Delta audit — complementa (não substitui) a auditoria original

---

## 📊 Sumário Executivo

### Veredicto

O repositório evoluiu significativamente desde a auditoria original. **8 dos 10 gaps P0 (críticos) foram resolvidos** — o que representa o grosso do trabalho técnico identificado em Jan/2026. Porém, três conclusões importantes:

1. **O conteúdo está em ~75–80% de completude**, não os "100%" declarados no [README.md](README.md).
2. **Existe uma camada inteira ausente do escopo da auditoria original: instructor enablement** (material do professor/aplicador).
3. **O repositório NÃO está pronto para onboarding de professores em Jun/Jul 2026** sem o trabalho documentado abaixo.

### Atualização das pontuações

| Métrica | Auditoria Jan/2026 | Re-auditoria Abr/2026 |
|---|---|---|
| Score Geral | 7.2/10 | ~8.0/10 |
| Gaps Críticos (P0) ainda abertos ou parciais | 34 | 6 |
| Gaps Importantes (P1) ainda abertos ou parciais | 40 | 12 |
| Esforço residual (conteúdo) | 257h | ~45h |
| Esforço novo (instructor enablement) | (não auditado) | ~40–80h |

---

## 1. Re-verificação dos 20 gaps prioritários

### Legenda

- ✅ **RESOLVIDO** — implementação completa verificada em arquivo
- ⚠️ **PARCIAL** — implementação existe mas incompleta vs. especificação original
- 🔴 **ABERTO** — não implementado, ou arquivo de saída ausente, ou ainda em estado de stub/pseudocódigo

### Resultado por gap

| # | Gap | Status | Evidência |
|---|---|---|---|
| 1 | [Fase 0] validate_phase0.py automatizado | ✅ | [validate_phase0.py](validate_phase0.py) — 356 linhas, valida Python/EnergyPlus/VS Code/GCP/Copilot, gera JSON report |
| 2 | [Mês 1] run_sim.py / inspect_idf.py completos | ✅ | [Science AI Engineering/scripts/](Science%20AI%20Engineering/scripts/) — 158 + 254 linhas, com main(), error handling |
| 3 | [Mês 2] GuardrailValidator + 15 testes pytest | ⚠️ | [docs/guardrails_spec.md](Science%20AI%20Engineering/docs/guardrails_spec.md) existe; suíte de testes em [tests/](Science%20AI%20Engineering/tests/) tem apenas 3 arquivos (todos do Mês 8) |
| 4 | [Mês 3] generate_dirty_sensor_data.py | ✅ | 161 linhas, gera CSV com outliers/gaps/drift configuráveis |
| 5 | [Mês 4] Dataset 500+ amostras | ✅ | `N_SAMPLES = 500` em [generate_lhs_dataset.py](Science%20AI%20Engineering/mes4_piml/generate_lhs_dataset.py), LHS sobre 12 parâmetros físicos |
| 6 | [Mês 4] PIML completo (sem stubs/TODOs) + K-Fold | ✅ | [train_surrogate.py](Science%20AI%20Engineering/mes4_piml/train_surrogate.py) + validate_physics.py + uncertainty_quantification.py, sem stubs |
| 7 | [Mês 5] VERTEX_AI_SETUP_GUIDE.md | ✅ | [VERTEX_AI_SETUP_GUIDE.md](Science%20AI%20Engineering/mes5_prompt_engineering/VERTEX_AI_SETUP_GUIDE.md) — 400+ linhas, troubleshooting 403/404 incluído |
| 8 | [Mês 5] technical_examples_library.json (50+ exemplos) | 🔴 | Script [generate_few_shot_examples.py](Science%20AI%20Engineering/mes5_prompt_engineering/generate_few_shot_examples.py) existe; **arquivo JSON de saída ausente do repo** |
| 9 | [Mês 6] CoSimulationManager funcional + 3 testes E2E | ⚠️ | [cosimulation_engine.py](Science%20AI%20Engineering/mes6_cosimulation/cosimulation_engine.py) implementado; sem testes E2E |
| 10 | [Mês 7] Golden dataset 50 casos | ✅ | `golden_dataset_50cases_*.csv` referenciado em [expand_golden_dataset.py](Science%20AI%20Engineering/mes6_cosimulation/expand_golden_dataset.py); expansão para 200 casos disponível |
| 11 | [Fase 0] requirements.txt com versões pinadas | 🔴 | [requirements.txt](requirements.txt) usa `>=` em vez de `==` (numpy>=2.1, pandas>=2.2.3, etc.) |
| 12 | [Mês 1] guia_leitura_idd.md (perguntas direcionadas) | ⚠️ | [docs/guia_referencia_completo.md](Science%20AI%20Engineering/docs/guia_referencia_completo.md) é genérico; sem guia específico para o IDD PDF |
| 13 | [Mês 2] Exercício 2.0 "Intro pytest" | ⚠️ | pytest mencionado em [Exercicios_Mes_2_Engenharia_Software.md](Science%20AI%20Engineering/Exercicios_Mes_2_Engenharia_Software.md) (linha 904+); sem seção 2.0 dedicada |
| 14 | [Mês 3] Retry 3x em batch failures | ⚠️ | try/except presente em [generate_lhs_dataset.py](Science%20AI%20Engineering/mes4_piml/generate_lhs_dataset.py); sem loop de retry |
| 15 | [Mês 4] K-Fold k=5 + mean±std | ✅ | `KFold(n_splits=5)` + `cross_val_score()` em train_surrogate.py:197–290 |
| 16 | [Mês 5] Hallucination detection 3-camadas | ⚠️ | Pseudocódigo no Exercicios_Mes_5; só 2 camadas (type + range) implementadas, cross-validation ausente |
| 17 | [Mês 7] PhysicsViolationDetector com 20+ validators | 🔴 | [physics_violation_validator_complete.py](Science%20AI%20Engineering/mes7_physics/physics_violation_validator_complete.py) tem 16 validators; faltam balanço energético, 2ª Lei termodinâmica, conservação de massa |
| 18 | [Mês 10] Stragglers handling (timeout dinâmico, async) | 🔴 | Nenhuma referência a "stragglers", "async aggregation" ou "timeout" em [mes10_federated_learning/](Science%20AI%20Engineering/mes10_federated_learning/) |
| 19 | [Mês 11] Conflict detection (correlation matrix, threshold alerts) | 🔴 | Mencionado em [Exercicios_Mes_11](Science%20AI%20Engineering/Exercicios_Mes_11_Advanced_Analytics.md) como objetivo; sem código |
| 20 | [Mês 12] Operations runbook + workshop 2h | 🔴 | [mes12_capstone/](Science%20AI%20Engineering/mes12_capstone/) tem delivery summaries; sem runbook operacional dedicado nem material de workshop |

### Totalização

- ✅ **Resolvidos:** 8 (1, 2, 4, 5, 6, 7, 10, 15)
- ⚠️ **Parciais:** 6 (3, 9, 12, 13, 14, 16)
- 🔴 **Abertos:** 6 (8, 11, 17, 18, 19, 20)

---

## 2. Pendências técnicas residuais (~45h)

### Bloco A — Quick wins (alta relevância, baixo custo) — ~8h

| # | Pendência | Estimativa |
|---|---|---|
| 11 | Pinar versões em [requirements.txt](requirements.txt) (`>=` → `==`) | 1h |
| 8 | Gerar e commitar `technical_examples_library.json` (50 exemplos com WWR/U-value físicos) | 3h |
| 14 | Adicionar retry 3x no loop de batch (try/except + log) | 2h |
| 13 | Criar Exercício 2.0 "Intro pytest" como seção dedicada | 2h |

### Bloco B — Robustez técnica (importante, médio custo) — ~19h

| # | Pendência | Estimativa |
|---|---|---|
| 3 | Implementar suíte de 15+ testes pytest do GuardrailValidator | 4h |
| 9 | Adicionar 3 testes E2E do CoSimulationManager (loop EnergyPlus ↔ Surrogate) | 6h |
| 16 | Completar 3ª camada (cross-validation) do hallucination detector | 3h |
| 17 | Implementar 4–5 validators físicos faltantes (energy balance, 2ª lei, conservação massa) | 6h |

### Bloco C — Tópicos avançados Meses 10–12 — ~15h

| # | Pendência | Estimativa |
|---|---|---|
| 18 | Stragglers/timeout no FedAvg (timeout dinâmico, async aggregation) | 6h |
| 19 | Conflict detection com correlation matrix + threshold alerts | 4h |
| 20 | Operations runbook (workshop pode ficar para depois ou junto com instructor enablement) | 5h |

### Bloco D — Documentação fina — ~3h

| # | Pendência | Estimativa |
|---|---|---|
| 12 | Guia direcionado de leitura do IDD PDF (50 perguntas por seção) | 3h |

---

## 3. Lacuna nova: Instructor Enablement (~40–80h)

A auditoria original (Jan/2026) avaliou prontidão para **alunos**. O onboarding de **professores/aplicadores** previsto para Jun/Jul 2026 demanda uma camada de material que **não existe hoje** no repositório:

| Item | Descrição | Estimativa |
|---|---|---|
| **Guia do instrutor** | Objetivos pedagógicos por mês, condução de exercícios, armadilhas comuns observadas | 12–20h |
| **Gabaritos / soluções** | Referência cruzada exercício ↔ código-solução existente; criar onde ausente | 8–16h |
| **Slides de abertura** | 1–2 decks por fase para uso em sala (Fase 0, Fase 1, Fase 2, Fase 3) | 6–12h |
| **Cronograma de aplicação** | Modos presencial 12-meses vs. assíncrono; carga horária semanal sugerida | 2–4h |
| **FAQ docente** | 20+ perguntas que professores farão antes de aplicar | 4–8h |
| **Dry-run roteirizado** | Pelo menos 1 mês-piloto com tempo aferido empiricamente (não só estimado) | 6–12h |
| **Roteiro do onboarding** | A sessão Jun/Jul propriamente dita (agenda, materiais, exercícios, Q&A) | 2–8h |
| **Total** | | **40–80h** |

A faixa larga reflete duas decisões ainda não tomadas: (a) onboarding cobrindo currículo inteiro vs. apenas Fase 0/Bootcamp, e (b) profundidade do gabarito (apenas referência ao código existente vs. solução escrita por exercício).

---

## 4. Red flags estruturais

Itens fora do escopo dos 20 gaps prioritários, observados durante a re-auditoria:

1. **Sem diretório `/data/`** — datasets são gerados sob demanda. Para uso em sala (onde tempo de geração é caro), recomenda-se pré-popular datasets-âncora (ao menos para Mês 1 e Mês 4).
2. **Cobertura de testes esparsa** — apenas 3 arquivos em [Science AI Engineering/tests/](Science%20AI%20Engineering/tests/), todos do Mês 8 (`test_ga_metrics_mes8.py`, `test_islands_mes8.py`, `test_pareto_mes8.py`). Meses 1–7 e 9–12 não têm suíte automatizada.
3. **README.md desatualizado** — declarações de "100% complete" e "production-ready" geram atrito ao usuário externo. **Corrigido nesta entrega** (ver [README.md](README.md) atualizado em 2026-04-30).
4. **CURRICULUM_FAPESP_ALIGNMENT_REPORT.md** mantido intocado — escopo dele (alinhamento com projeto FAPESP) é diferente de "prontidão para uso por instrutores". A pontuação 98/100 segue válida no escopo dela.

---

## 5. Próximos passos — programação F2/F3/F4

A continuação do trabalho está estruturada em quatro fases:

| Fase | Objetivo | Esforço | Marco | Status |
|---|---|---|---|---|
| **F1. Diagnóstico** | Re-auditar e documentar pendências reais | — | 2026-05-01 | ✅ Concluído (este documento) |
| **F2. Revisão técnica + dry-run + kit alunos** | Fechar pendências dos Blocos A–D, repo "student-ready" | ~64h | 2026-08-15 | Pendente |
| **F3. Instructor enablement** | Criar camada de material do professor (guia, gabaritos, slides, FAQ, dry-run, roteiro de onboarding) | ~62h | 2026-12-15 | Pendente |

### Programação detalhada

A programação semana-a-semana de F2 e F3, com tarefas, entregáveis, marcos e checkboxes para acompanhamento, está em:

👉 **[PROGRAMACAO_F2_F3.md](PROGRAMACAO_F2_F3.md)**

Parâmetros consolidados:
- **Onboarding alunos:** 2026-08-15
- **Material do instrutor pronto:** 2026-12-15 (onboarding professores logo após)
- **Disponibilidade:** 3h/sem (Mai–Jun) → 8h/sem (Jul–Ago) → 4h/sem (Ago–Dez)
- **Orçamento total:** ~78h para F2 + ~70h para F3

---

## 📚 Referências

- [AUDITORIA_COMPLETA_CURRICULUM.md](AUDITORIA_COMPLETA_CURRICULUM.md) — Auditoria original (Jan/2026), histórica
- [README.md](README.md) — Documento principal do repositório (atualizado nesta entrega)
- [CURRICULUM_FAPESP_ALIGNMENT_REPORT.md](CURRICULUM_FAPESP_ALIGNMENT_REPORT.md) — Alinhamento com projeto FAPESP (escopo distinto, mantido intocado)
- [Scientific_AI_Engineering_Curriculum.md](Scientific_AI_Engineering_Curriculum.md) — Currículo mestre

---

**Conclusão:** O currículo evoluiu bem desde a auditoria original — a maior parte do trabalho técnico crítico foi concluída. Resta uma quantidade gerenciável de pendências (~45h) para fechar o conteúdo, e uma camada nova de ~40–80h para preparar o material que professores/aplicadores precisarão receber no onboarding de Jun/Jul. **Estado atual: pré-onboarding, não production-ready.**
