# 📅 PROGRAMAÇÃO F1 Residual, F2 & F3 — Conclusão do Currículo + Material do Instrutor

**Data de criação:** 2026-05-01  
**Última atualização:** 2026-05-07 (Revisão de timeline — F1 residual mai–dez/2026; F2 jan–ago/2027; F3 set–dez/2027)  
**Autor responsável:** João Petreche  
**Documento de origem:** [AUDITORIA_2026_04_REVISAO.md](AUDITORIA_2026_04_REVISAO.md)  
**Tipo:** Plano de execução com checkpoints semanais

---

## ⚠️ Notas de Atualização (2026-05-07)

**Estado atual:** Semana 1 de maio em andamento (05-07)

**Alterações realizadas:**
- ✅ Removido `simulations/basic_zone/` (exemplo prático de simulação térmica)
- ✅ Removido `curriculum/phase-01-foundation/module-1-1/modulo_1_1_onboarding_simulacao.md` (material de onboarding do Mês 1)
- ✅ Mantido `test_gemini.md` para exploração de GenAI
- ✅ Atualizada documentação base (README, STUDENT_PROFILE, PREREQUISITES, Scientific_AI_Engineering_Curriculum)
- ✅ Criado `CLAUDE.md` para contexto persistente

**Impacto no plano:** Semana 1 pode concentrar-se em **A11 + A8** sem complicações. A timeline original (Semanas 1-16) permanece válida.

---

## 🎯 Parâmetros do plano (Timeline Revisada)

| Parâmetro | Valor |
|---|---|
| **Marco F1 Residual — Conclusão** | 2026-12-31 |
| **Marco F2 — Onboarding alunos** | 2027-08-15 |
| **Marco F3 — Material do instrutor pronto** | 2027-12-15 |
| **Disponibilidade F1 Residual (Mai–Dez 2026)** | 3h/semana |
| **Disponibilidade F2 início (Jan–Mar 2027)** | 3h/semana |
| **Disponibilidade F2 peak (Apr–Aug 2027)** | 8h/semana |
| **Disponibilidade F3 (Set–Dez 2027)** | 4h/semana |

---

## 💰 Orçamento de horas (Revisado)

| Período | Fase | Semanas | h/sem | **Disponível** |
|---|---|---|---|---|
| 2026-05-07 → 2026-12-31 | F1 Residual | ~34 | 3h | **~102h** |
| 2027-01-01 → 2027-03-31 | F2 início | ~13 | 3h | **~39h** |
| 2027-04-01 → 2027-08-15 | F2 peak | ~19 | 8h | **~152h** |
| **F2 total (até onboarding alunos)** | | | | **~191h** |
| 2027-08-16 → 2027-12-15 | F3 | ~17.5 | 4h | **~70h** |
| **F3 total (até material instrutor pronto)** | | | | **~70h** |

---

## 🎓 F1 Residual — Resolução de Inconsistências (Mai–Dez 2026)

**Objetivo:** resolver inconsistências documentais descobertas na revisão de objetivos de maio/2026. Atualizar datas internas, eliminar contradições entre documentos, documentar limitações técnicas conhecidas (Python 3.10, SDK Gemini, etc.).

**Carga estimada:** ~102h (contra ~102h disponíveis).

---

## 🎓 F2 — Material para alunos (Jan–Ago 2027)

**Objetivo:** repositório "student-ready" até 15-Ago/2027 — todos os gaps técnicos da auditoria de 2026-04 fechados, dry-run completo realizado, kit de boas-vindas pronto.

**Carga estimada:** ~191h (contra ~191h disponíveis = margens justas; priorizar Blocos A-D).

### Estratégia de alocação

- **Tarefas curtas e isoladas** (Bloco A + Bloco D) → período 3h/sem
- **Tarefas pesadas com alto contexto** (Bloco B testes, Bloco C tópicos avançados, dry-run) → período 8h/sem

### Fase Janeiro–Março/2027 (3h/sem, ~39h)

| Sem | Janela | Tarefa | h | ☐ |
|---|---|---|---|---|
| 1 | 01-03 → 01-09 | A11 — Pinar [requirements.txt](requirements.txt) (`>=` → `==`) + SDK Gemini atualização | 2 | ☐ |
| 1 | 01-03 → 01-09 | A8 — Iniciar `technical_examples_library.json` (50 exemplos físicos) | 2 | ☐ |
| 2 | 01-10 → 01-16 | A8 — Finalizar JSON (validação WWR/U-value) | 1 | ☐ |
| 2 | 01-10 → 01-16 | A14 — Retry 3x em batch failures (try/except + log) | 2 | ☐ |
| 3 | 01-17 → 01-23 | A13 — Exercício 2.0 "Intro pytest" (5 testes simples) | 2 | ☐ |
| 3 | 01-17 → 01-23 | D12 — Iniciar guia direcionado de leitura do IDD PDF | 1 | ☐ |
| 4 | 01-24 → 01-30 | D12 — Finalizar guia IDD (~50 perguntas direcionadas) | 2 | ☐ |
| 4 | 01-24 → 01-30 | B16 — Hallucination 3ª camada (cross-validation) | 1 | ☐ |
| 5 | 01-31 → 02-06 | B16 — Finalizar 3ª camada | 2 | ☐ |
| 5 | 01-31 → 02-06 | B3 — Iniciar suíte pytest GuardrailValidator | 1 | ☐ |
| 6 | 02-07 → 02-13 | B3 — Testes pytest GuardrailValidator (target: 15+ testes) | 3 | ☐ |
| 7 | 02-14 → 02-20 | B17 — Physics validators faltantes (energy balance, 2ª lei, conservação massa) | 3 | ☐ |
| 8 | 02-21 → 02-27 | B17 — Finalizar physics validators + integração ao detector | 3 | ☐ |
| 9 | 02-28 → 03-06 | B3 (continuação) — Integração suíte pytest com testes existentes | 2 | ☐ |
| 10 | 03-07 → 03-13 | Revisão Bloco A + D + B início (checkpoint) | 2 | ☐ |
| 11 | 03-14 → 03-20 | Buffer / ajustes finais Blocos A–D | 2 | ☐ |
| 12 | 03-21 → 03-31 | PyTorch adição a requirements.txt + LangChain pinagem + validação | 2 | ☐ |

**Marco 31/Mar/2027:** Blocos A + D completos · Bloco B ~70% (faltam testes E2E do CoSim) · ~39h investidas.

### Fase Abril–Agosto/2027 (8h/sem, ~152h)

| Sem | Janela | Tarefa | h | ☐ |
|---|---|---|---|---|
| 13 | 04-04 → 04-10 | B9 — Testes E2E CoSimulationManager (3 casos: surrogate-only, EnergyPlus-only, hybrid loop) | 8 | ☐ |
| 14 | 04-11 → 04-17 | B9 (continuação) — Finalizar e integrar testes E2E | 6 | ☐ |
| 14 | 04-11 → 04-17 | Revisão final Bloco B + validação com código existente | 2 | ☐ |
| 15 | 04-18 → 04-24 | C18 — Stragglers/timeout no FedAvg (timeout dinâmico, async aggregation) | 8 | ☐ |
| 16 | 04-25 → 05-01 | C19 — Conflict detection: correlation matrix + threshold alerts (Mês 11) | 8 | ☐ |
| 17 | 05-02 → 05-08 | C19 (continuação) + C20 — Operations runbook (Mês 12) | 8 | ☐ |
| 18 | 05-09 → 05-15 | C20 — Finalizar runbook + documentação operacional | 8 | ☐ |
| 19 | 05-16 → 05-22 | Dry-run como aluno: validate_phase0 → Mês 2 (anotar tempo, bugs, fricções) | 8 | ☐ |
| 20 | 05-23 → 05-29 | Dry-run continuação: Meses 3–6 | 8 | ☐ |
| 21 | 05-30 → 06-05 | Dry-run continuação: Meses 7–9 | 8 | ☐ |
| 22 | 06-06 → 06-12 | Dry-run continuação: Meses 10–12 + correção de bugs encontrados | 8 | ☐ |
| 23 | 06-13 → 06-19 | Correções pós-dry-run (bugs críticos, fricções documentadas) | 8 | ☐ |
| 24 | 06-20 → 06-26 | Kit boas-vindas alunos (welcome message, primeiro-dia checklist, canal de suporte) | 8 | ☐ |
| 25 | 06-27 → 07-03 | Atualização final do README pós-F2 + consolidação de pendências | 8 | ☐ |
| 26 | 07-04 → 07-10 | Buffer — resolução de issues não-críticas encontradas no dry-run | 8 | ☐ |
| 27 | 07-11 → 07-17 | Validação final: todos os exercícios do Mês 0 ao Mês 12 executáveis | 8 | ☐ |
| 28 | 07-18 → 07-24 | Preparação do repositório final student-ready: tags, release notes, documentação | 8 | ☐ |
| 29 | 07-25 → 07-31 | Buffer final / checkpoint pré-08-15 | 8 | ☐ |
| 30 | 08-01 → 08-15 | Polimento final + validação com checklist F2 | 8 | ☐ |

**Marco 15/Ago/2027:** ☐ Repo "student-ready" — todos os gaps técnicos fechados, dry-run feito, kit pronto. F2 concluída.

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

**Trilhas paralelas (independentes, não bloqueiam F2/F3):**
- 📄 **Literature Alignment + Literature Review** ([Literature Alignment.md](Literature%20Alignment/Literature%20Alignment.md) e [Literature Review/](Literature%20Alignment/Literature%20Review/)) — alinhamento bibliográfico e manuscrito acadêmico revisando 888 papers. Refresheado em abril/2026 (metadata, duplicatas, bibliografia) e maio/2026 (mojibake fix em `manuscript.md`). **Não cabe atualização nesta programação F2/F3** — se houver mudança substantiva, fica em commits separados.
- 📊 **CURRICULUM_FAPESP_ALIGNMENT_REPORT.md** — alinhamento com projeto FAPESP (98/100). Escopo é prontidão para pesquisa, não para uso por instrutores. Mantido intocado.

---

## 👨‍🏫 F3 — Material do instrutor

**Objetivo:** camada de instructor enablement completa até 15-Dez, permitindo onboarding de professores logo em seguida.

**Carga estimada:** ~62h (versão balanceada entre lean 40h e completo 80h) contra ~70h disponíveis = ~8h de folga.

### Estratégia

Construir em ondas mensais, cada onda entregando algo utilizável. Validar com 1 professor-piloto em outubro/novembro.

### Plano mês-a-mês (4h/sem)

#### 🗓️ Setembro/2027 (08-16 → 09-15, ~17h)

**Foco:** Guia do instrutor + cronograma de aplicação.

| Tarefa | h | ☐ |
|---|---|---|
| Guia do instrutor — Fase 0 + Bootcamp Express (objetivos pedagógicos, armadilhas, tempo aferido) | 4 | ☐ |
| Guia do instrutor — Meses 1–4 (1.5h por mês: 6h) | 6 | ☐ |
| Guia do instrutor — Meses 5–9 (1h por mês: 5h) | 5 | ☐ |
| Cronograma de aplicação (modos presencial 12 meses vs. assíncrono; carga semanal sugerida) | 2 | ☐ |

**Marco 15/Set/2027:** ☐ Guia do instrutor cobrindo Fase 0 → Mês 9 + cronograma pronto.

#### 🗓️ Outubro/2027 (09-16 → 10-15, ~17h)

**Foco:** Gabaritos + FAQ docente + finalizar guia do instrutor.

| Tarefa | h | ☐ |
|---|---|---|
| Guia do instrutor — Meses 10–12 (incluindo workshop do Mês 12 que migrou de F2) | 4 | ☐ |
| Gabaritos — referência cruzada exercício ↔ código-solução existente (Meses 0–6) | 5 | ☐ |
| Gabaritos — soluções escritas para exercícios sem código existente (Meses 7–12) | 4 | ☐ |
| FAQ docente — 20+ perguntas com respostas estruturadas | 4 | ☐ |

**Marco 15/Out/2027:** ☐ Guia completo · Gabaritos cobrindo 12 meses · FAQ pronto. **Convidar 1 professor-piloto** para revisar.

#### 🗓️ Novembro/2027 (10-16 → 11-15, ~17h)

**Foco:** Slides + iteração com feedback do professor-piloto.

| Tarefa | h | ☐ |
|---|---|---|
| Slide deck — Fase 0 + Bootcamp Express (abertura, objetivos, ambiente) | 3 | ☐ |
| Slide deck — Fase 1 (Meses 0–4, fundamentos) | 3 | ☐ |
| Slide deck — Fase 2 (Meses 5–9, integração AI) | 3 | ☐ |
| Slide deck — Fase 3 (Meses 10–12, sistemas avançados) | 3 | ☐ |
| Iteração com feedback do professor-piloto (correções no guia/gabaritos/FAQ) | 5 | ☐ |

**Marco 15/Nov/2027:** ☐ 4 decks de slides · Versão validada por professor-piloto.

#### 🗓️ Dezembro/2027 (11-16 → 12-15, ~17h)

**Foco:** Dry-run roteirizado + roteiro do onboarding + polimento.

| Tarefa | h | ☐ |
|---|---|---|
| Dry-run roteirizado — selecionar mês-piloto e cronometrar aplicação real | 8 | ☐ |
| Roteiro do onboarding — agenda da sessão Jan–Fev/2028, materiais, exercícios, Q&A | 5 | ☐ |
| Polimento final, README pós-F3, kit do instrutor consolidado | 2 | ☐ |
| Buffer | 2 | ☐ |

**Marco 15/Dez/2027:** ☐ **Repo "instructor-ready"** — material do instrutor completo, validado, com roteiro de onboarding pronto. F3 concluída.

---

## 🎯 Marcos consolidados

| Data | Marco | Status |
|---|---|---|
| 2026-05-01 | F1 concluído (auditoria) | ✅ |
| 2026-12-31 | **F1 Residual concluída** — inconsistências resolvidas, limitações técnicas documentadas | ☐ |
| 2027-03-31 | Blocos A + D completos, B ~70% | ☐ |
| 2027-08-15 | **F2 concluída — repo student-ready · Onboarding alunos pode acontecer** | ☐ |
| 2027-09-15 | F3 onda 1 — guia do instrutor + cronograma | ☐ |
| 2027-10-15 | F3 onda 2 — gabaritos + FAQ + convite professor-piloto | ☐ |
| 2027-11-15 | F3 onda 3 — slides + iteração com feedback | ☐ |
| 2027-12-15 | **F3 concluída — repo instructor-ready · Onboarding professores pode acontecer** | ☐ |

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
