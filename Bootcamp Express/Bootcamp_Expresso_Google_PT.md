# Bootcamp Expresso Google: Preparação para Engenharia de IA Científica

**Autor:** Engenharia de IA Científica (Simulação Termoenergética & Vertex AI)

**Foco:** Nivelamento Técnico e Infraestrutura para Fase 0

**Data:** Janeiro 2026

---

## 1. Visão Geral e Objetivo

Este documento consolida os requisitos de infraestrutura e o plano de nivelamento técnico ("Bootcamp Express") necessário para iniciar o currículo de **Scientific AI Engineering**. O objetivo é garantir que o pesquisador possua o ambiente (hardware/software) e as competências (Python/Cloud) para suportar cargas de trabalho intensivas envolvendo **EnergyPlus** e **Google Cloud Vertex AI**.

A Fase 0 não é apenas burocracia; é um **filtro de engenharia**. A incapacidade de configurar este ambiente indica bloqueios técnicos que impedirão a execução de simulações complexas e *pipelines* de ML no futuro.

---

## 2. Auditoria de Infraestrutura (Hard Constraints)

Abaixo estão os requisitos não-negociáveis. A falha em atender a qualquer um destes itens resultará em incompatibilidade com os scripts de automação e contêineres Docker do curso.

### 2.1 Hardware e Sistema Operacional
*   **Sistema Operacional:** Windows 10 ou 11 (64-bit).
    *   *Nota Técnica:* O currículo utiliza scripts PowerShell (`.ps1`) para orquestração local. Usuários de Linux/Mac assumem a responsabilidade de portar scripts.
*   **Processador (CPU):** Mínimo 4 núcleos físicos. (Recomendado: 8+ núcleos para paralelização de simulações EnergyPlus).
*   **Memória (RAM):**
    *   **Mínimo:** 8 GB (Viável, mas limitante).
    *   **Recomendado:** 16 GB+ (Necessário para rodar VS Code + EnergyPlus + Docker simultaneamente).
*   **Armazenamento:** Mínimo **20 GB** livres (SSD obrigatório para I/O eficiente de datasets).
*   **Permissões:** Acesso de **Administrador** local é mandatório para manipulação de variáveis de ambiente (PATH).

### 2.2 Stack de Software (Versões Estritas)
A reprodutibilidade científica exige controle rigoroso de versões. Não atualize além destas versões sem validação prévia.

*   **Python:** **3.10.x** (Recomendado: 3.10.11).
    *   *Warning:* Versões 3.11/3.12 ainda apresentam instabilidades com certas bibliotecas de *Scientific ML* e *bindings* legados.
*   **EnergyPlus:** **24.1.0**.
    *   *Integração:* Utilizaremos a API Python nativa (`pyenergyplus`) preferencialmente sobre subprocessos CLI.
*   **IDE:** Visual Studio Code (Microsoft).
    *   *Extensões Essenciais:* Python, Jupyter, **GitHub Copilot**, **Google Cloud Code**, Ruff/Black.

### 2.3 Contas e Acessos
Utilizamos um modelo híbrido para maximizar recursos gratuitos (*Free Tier*).

*   **Identidade Institucional (USP/FAPESP):**
    *   Necessário para o **GitHub Student Developer Pack** (Copilot gratuito) e acesso ao **Coursera for USP**.
*   **Identidade Cloud (Google Account Pessoal):**
    *   Use um e-mail `@gmail.com` pessoal para o **Google Cloud Platform (GCP)**.
    *   *Motivo:* Contas institucionais (G-Suite/Workspace) frequentemente possuem políticas de IAM restritivas que bloqueiam a Vertex AI.
    *   **Financeiro:** Necessário cartão de crédito para ativar o *Free Trial* ($300 USD), mas configuraremos *Budget Alerts* para custo zero.

---

## 3. Plano de Nivelamento: O "Bootcamp Express" (Google Stack)

Identificamos lacunas comuns em Python, Git e Terminal. Para saná-las em **1 semana**, utilizaremos recursos oficiais do ecossistema Google e parceiros.

### 3.1 Python para Ciência de Dados (Kaggle)
*Plataforma Google focada em Data Science aplicada.*

*   **Recurso:** [Kaggle Learn](https://www.kaggle.com/learn)
*   **Metodologia:** Micro-cursos práticos (focados em "fazer" e não apenas "assistir").
*   **Cursos Mandatórios:**
    1.  **Python:** Foco em sintaxe, manipulação de listas/dicionários e funções.
    2.  **Pandas:** Cobre diretamente o *Exercício 0.2.E* (ETL de arquivos CSV/JSON).

### 3.2 Controle de Versão e Automação (Coursera/Google)
*Padrão ouro para operações de código.*

*   **Recurso:** Google IT Automation with Python (Coursera).
*   **Acesso:** Via **Coursera for USP** (gratuito para alunos).
*   **Módulo Foco:** "Introduction to Git and GitHub".
    *   Ensina desde `git init` até *Pull Requests*.
    *   Cobre automação básica de terminal (Bash/Linux skills).

### 3.3 Fluência em Terminal e Cloud (Google Cloud Skills Boost)
*Para perder o medo da "tela preta".*

*   **Recurso:** [Google Cloud Skills Boost](https://www.cloudskillsboost.google/)
*   **Labs Recomendados:** "Linux Fundamentals" ou "Cloud Engineering Basics".
*   **Vantagem:** Ambiente *sandbox* real no navegador. Não há risco de danificar sua máquina local.

---

## 4. Cronograma de Execução (1 Semana)

Se você respondeu "NÃO" para qualquer item da auditoria de infraestrutura ou competência, siga este cronograma rigorosamente antes do Mês 1.

| Dias | Foco | Tarefas Críticas | Plataforma |
| :--- | :--- | :--- | :--- |
| **1-2** | **Python Core** | Completar cursos *Python* e *Pandas*. Garantir entendimento de `venv`. | Kaggle Learn |
| **3-4** | **Git & Terminal** | Módulo "Intro to Git/GitHub". Configurar chaves SSH locais. | Coursera (Google) |
| **5** | **Validação** | Executar o **Exercício 0.2.E** (Script de ETL) sem consultar tutoriais básicos. | Local (VS Code) |

---

## 5. Próximos Passos

Após concluir este bootcamp:
1.  Configure seu ambiente local (`venv`, EnergyPlus 24.1.0).
2.  Clone o repositório do currículo.
3.  Execute o script de validação de ambiente (se disponível) ou reporte o status no canal de comunicação.

> **Nota do Engenheiro:** A qualidade da sua infraestrutura na Fase 0 dita o ritmo da sua inovação na Fase 3. Não pule etapas.
