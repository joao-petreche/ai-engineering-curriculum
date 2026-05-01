# 📅 PROGRAMAÇÃO F2 & F3 — Conclusão do Currículo + Material do Instrutor

**Data de criação:** 2026-05-01
**Autor responsável:** João Petreche
**Documento de origem:** [AUDITORIA_2026_04_REVISAO.md](AUDITORIA_2026_04_REVISAO.md)
**Tipo:** Plano de execução com checkpoints semanais

---

## 🎯 Parâmetros do plano

| Parâmetro | Valor |
|---|---|
| **Marco F2 — Onboarding alunos** | 2026-08-15 |
| **Marco F3 — Material do instrutor pronto** | 2026-12-15 |
| **Disponibilidade Mai–Jun (fim de semestre)** | 3h/semana |
| **Disponibilidade Jul–15-Ago** | 8h/semana |
| **Disponibilidade 16-Ago → 15-Dez** | 4h/semana |

---

## 💰 Orçamento de horas

| Período | Semanas | h/sem | **Disponível** |
|---|---|---|---|
| 2026-05-01 → 2026-06-30 | ~9 | 3h | **~26h** |
| 2026-07-01 → 2026-08-15 | ~6.5 | 8h | **~52h** |
| **F2 total (até onboarding alunos)** | | | **~78h** |
| 2026-08-16 → 2026-12-15 | ~17.5 | 4h | **~70h** |
| **F3 total (até material instrutor pronto)** | | | **~70h** |

---

## 🎓 F2 — Material para alunos

**Objetivo:** repositório "student-ready" até 15-Ago — todos os gaps técnicos da auditoria de 2026-04 fechados, dry-run completo realizado, kit de boas-vindas pronto.

**Carga estimada:** ~64h (contra ~78h disponíveis = ~14h de folga para imprevistos).

### Estratégia de alocação

- **Tarefas curtas e isoladas** (Bloco A + Bloco D) → período 3h/sem
- **Tarefas pesadas com alto contexto** (Bloco B testes, Bloco C tópicos avançados, dry-run) → período 8h/sem

### Fase Maio–Junho (3h/sem, ~26h)

| Sem | Janela | Tarefa | h | ☐ |
|---|---|---|---|---|
| 1 | 05-01 → 05-07 | A11 — Pinar [requirements.txt](requirements.txt) (`>=` → `==`) | 1 | ☐ |
| 1 | 05-01 → 05-07 | A8 — Iniciar `technical_examples_library.json` (50 exemplos físicos) | 2 | ☐ |
| 2 | 05-08 → 05-14 | A8 — Finalizar JSON (validação WWR/U-value) | 1 | ☐ |
| 2 | 05-08 → 05-14 | A14 — Retry 3x em batch failures (try/except + log) | 2 | ☐ |
| 3 | 05-15 → 05-21 | A13 — Exercício 2.0 "Intro pytest" (5 testes simples) | 2 | ☐ |
| 3 | 05-15 → 05-21 | D12 — Iniciar guia direcionado de leitura do IDD PDF | 1 | ☐ |
| 4 | 05-22 → 05-28 | D12 — Finalizar guia IDD (~50 perguntas direcionadas) | 2 | ☐ |
| 4 | 05-22 → 05-28 | B16 — Hallucination 3ª camada (cross-validation) | 1 | ☐ |
| 5 | 05-29 → 06-04 | B16 — Finalizar 3ª camada | 2 | ☐ |
| 5 | 05-29 → 06-04 | B3 — Iniciar suíte pytest GuardrailValidator | 1 | ☐ |
| 6 | 06-05 → 06-11 | B3 — Testes pytest GuardrailValidator (target: 15+ testes) | 3 | ☐ |
| 7 | 06-12 → 06-18 | B17 — Physics validators faltantes (energy balance, 2ª lei, conservação massa) | 3 | ☐ |
| 8 | 06-19 → 06-25 | B17 — Finalizar physics validators + integração ao detector | 3 | ☐ |
| 9 | 06-26 → 06-30 | Buffer / fechamento Bloco B parcial | 2 | ☐ |

**Marco 30/Jun:** Blocos A + D completos · Bloco B ~70% (faltam testes E2E do CoSim) · ~25h investidas.

### Fase Julho–Agosto (8h/sem, ~52h)

| Sem | Janela | Tarefa | h | ☐ |
|---|---|---|---|---|
| 10 | 07-01 → 07-07 | B9 — Testes E2E CoSimulationManager (3 casos: surrogate-only, EnergyPlus-only, hybrid loop) | 6 | ☐ |
| 10 | 07-01 → 07-07 | Revisão final Bloco B + integração com testes existentes | 2 | ☐ |
| 11 | 07-08 → 07-14 | C18 — Stragglers/timeout no FedAvg (timeout dinâmico, async aggregation) | 6 | ☐ |
| 11 | 07-08 → 07-14 | Planning detalhado C19 + C20 | 2 | ☐ |
| 12 | 07-15 → 07-21 | C19 — Conflict detection: correlation matrix + threshold alerts (Mês 11) | 4 | ☐ |
| 12 | 07-15 → 07-21 | C20 — Operations runbook (Mês 12, sem workshop) | 4 | ☐ |
| 13 | 07-22 → 07-28 | C20 — Finalizar runbook | 1 | ☐ |
| 13 | 07-22 → 07-28 | Dry-run como aluno: validate_phase0 → Mês 1 (anotar tempo, bugs, fricções) | 7 | ☐ |
| 14 | 07-29 → 08-04 | Dry-run continuação: Meses 2–6 | 8 | ☐ |
| 15 | 08-05 → 08-11 | Dry-run continuação: Meses 7–12 + correção de bugs encontrados | 8 | ☐ |
| 16 | 08-12 → 08-15 | Kit boas-vindas alunos (welcome message, primeiro-dia checklist, canal de suporte) + atualização final do README | 4 | ☐ |

**Marco 15/Ago:** ☐ Repo "student-ready" — todos os gaps técnicos fechados, dry-run feito, kit pronto. F2 concluída.

### Escopo F2 — explícito

**Dentro do escopo:**
- Blocos A + B + C + D dos 18 itens residuais da auditoria
- Dry-run end-to-end como aluno (~22h)
- Kit de boas-vindas alunos
- Atualização final do README para refletir estado pós-F2

**Fora do escopo (dívida técnica conhecida):**
- ❌ Cobertura de testes pytest para Meses 1–7, 9–12 (apenas Meses 4 e 8 terão testes)
- ❌ Workshop 2h hands-on do Mês 12 (migra para F3 como parte do material do instrutor)
- ❌ Pré-popular `/data/` com datasets-âncora (mantém geração sob demanda; documentar tempo esperado nos exercícios)

---

## 👨‍🏫 F3 — Material do instrutor

**Objetivo:** camada de instructor enablement completa até 15-Dez, permitindo onboarding de professores logo em seguida.

**Carga estimada:** ~62h (versão balanceada entre lean 40h e completo 80h) contra ~70h disponíveis = ~8h de folga.

### Estratégia

Construir em ondas mensais, cada onda entregando algo utilizável. Validar com 1 professor-piloto em outubro/novembro.

### Plano mês-a-mês (4h/sem)

#### 🗓️ Setembro/2026 (08-16 → 09-15, ~17h)

**Foco:** Guia do instrutor + cronograma de aplicação.

| Tarefa | h | ☐ |
|---|---|---|
| Guia do instrutor — Fase 0 + Bootcamp Express (objetivos pedagógicos, armadilhas, tempo aferido) | 4 | ☐ |
| Guia do instrutor — Meses 1–4 (1.5h por mês: 6h) | 6 | ☐ |
| Guia do instrutor — Meses 5–9 (1h por mês: 5h) | 5 | ☐ |
| Cronograma de aplicação (modos presencial 12 meses vs. assíncrono; carga semanal sugerida) | 2 | ☐ |

**Marco 15/Set:** ☐ Guia do instrutor cobrindo Fase 0 → Mês 9 + cronograma pronto.

#### 🗓️ Outubro/2026 (09-16 → 10-15, ~17h)

**Foco:** Gabaritos + FAQ docente + finalizar guia do instrutor.

| Tarefa | h | ☐ |
|---|---|---|
| Guia do instrutor — Meses 10–12 (incluindo workshop do Mês 12 que migrou de F2) | 4 | ☐ |
| Gabaritos — referência cruzada exercício ↔ código-solução existente (Meses 0–6) | 5 | ☐ |
| Gabaritos — soluções escritas para exercícios sem código existente (Meses 7–12) | 4 | ☐ |
| FAQ docente — 20+ perguntas com respostas estruturadas | 4 | ☐ |

**Marco 15/Out:** ☐ Guia completo · Gabaritos cobrindo 12 meses · FAQ pronto. **Convidar 1 professor-piloto** para revisar.

#### 🗓️ Novembro/2026 (10-16 → 11-15, ~17h)

**Foco:** Slides + iteração com feedback do professor-piloto.

| Tarefa | h | ☐ |
|---|---|---|
| Slide deck — Fase 0 + Bootcamp Express (abertura, objetivos, ambiente) | 3 | ☐ |
| Slide deck — Fase 1 (Meses 0–4, fundamentos) | 3 | ☐ |
| Slide deck — Fase 2 (Meses 5–9, integração AI) | 3 | ☐ |
| Slide deck — Fase 3 (Meses 10–12, sistemas avançados) | 3 | ☐ |
| Iteração com feedback do professor-piloto (correções no guia/gabaritos/FAQ) | 5 | ☐ |

**Marco 15/Nov:** ☐ 4 decks de slides · Versão validada por professor-piloto.

#### 🗓️ Dezembro/2026 (11-16 → 12-15, ~17h)

**Foco:** Dry-run roteirizado + roteiro do onboarding + polimento.

| Tarefa | h | ☐ |
|---|---|---|
| Dry-run roteirizado — selecionar mês-piloto e cronometrar aplicação real | 8 | ☐ |
| Roteiro do onboarding — agenda da sessão Jun–Jul/2027, materiais, exercícios, Q&A | 5 | ☐ |
| Polimento final, README pós-F3, kit do instrutor consolidado | 2 | ☐ |
| Buffer | 2 | ☐ |

**Marco 15/Dez:** ☐ **Repo "instructor-ready"** — material do instrutor completo, validado, com roteiro de onboarding pronto. F3 concluída.

---

## 🎯 Marcos consolidados

| Data | Marco | Status |
|---|---|---|
| 2026-05-01 | F1 concluído (auditoria + atualização docs) | ✅ |
| 2026-06-30 | Blocos A + D completos, B ~70% | ☐ |
| 2026-08-15 | **F2 concluída — repo student-ready · Onboarding alunos pode acontecer** | ☐ |
| 2026-09-15 | F3 onda 1 — guia do instrutor + cronograma | ☐ |
| 2026-10-15 | F3 onda 2 — gabaritos + FAQ + convite professor-piloto | ☐ |
| 2026-11-15 | F3 onda 3 — slides + iteração com feedback | ☐ |
| 2026-12-15 | **F3 concluída — repo instructor-ready · Onboarding professores pode acontecer** | ☐ |

---

## ⚠️ Riscos e mitigações

| # | Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|---|
| 1 | Dry-run (sem 13–15) revela bugs nos ~80% "completos" e estoura 8h alocadas | Média | Alto | Começar spot-check de Fase 0 + Mês 1 já em junho como dry-run preliminar (cabe nas 3h/sem se priorizado) |
| 2 | Período 3h/sem (Mai–Jun) é vulnerável a fim de semestre acadêmico | Média | Médio | Tarefas alocadas ali são curtas e independentes; atrasar 1 semana não trava dependências. Buffer de ~2h na sem 9 |
| 3 | F3 sem feedback de instrutor real produz material desconectado da realidade docente | Média | Alto | Convidar professor-piloto em meados de outubro (após gabaritos + FAQ); reservar 5h em novembro para iteração |
| 4 | Estimativas otimistas (típico subestimar em 20–30%) | Alta | Médio | Folgas: F2 tem ~14h, F3 tem ~8h. Se uma tarefa estourar, primeiro corte cai sobre slides "extras" (manter 1 deck por fase) e dry-run reduzido |
| 5 | Onboarding alunos em 15-Ago colide com período letivo USP | Baixa | Médio | Verificar calendário acadêmico USP; ajustar para pré ou pós-volta às aulas se necessário |

---

## 📋 Como usar este documento

**Cadência:** abrir nas segundas-feiras para checar tarefas da semana, fechar nas sextas/sábados para marcar checkboxes ☐ → ☑.

**Atualização:** se uma semana atrasar, **não realocar**. Use o buffer (sem 9 e sem 16) ou desça uma tarefa do Bloco C para a dívida técnica conhecida (e atualize a auditoria).

**Re-planning trigger:** se chegar em 30/Jun com **menos de 50% do Bloco B feito**, há atraso real — reabra a programação e converse sobre cortes.

**Encerramento de F2:** marcar todos os checkboxes da seção F2, atualizar README com novo banner ("student-ready"), criar release tag `v1.0-students` no Git.

**Encerramento de F3:** mesma rotina, tag `v1.0-instructors`.

---

## 📚 Referências

- [AUDITORIA_2026_04_REVISAO.md](AUDITORIA_2026_04_REVISAO.md) — fonte das pendências técnicas
- [AUDITORIA_COMPLETA_CURRICULUM.md](AUDITORIA_COMPLETA_CURRICULUM.md) — auditoria histórica (Jan/2026)
- [README.md](README.md) — documento principal (será atualizado nos marcos de F2 e F3)
- [Scientific_AI_Engineering_Curriculum.md](Scientific_AI_Engineering_Curriculum.md) — currículo mestre
