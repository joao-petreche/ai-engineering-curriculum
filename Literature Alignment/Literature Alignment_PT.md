# Alinhamento Bibliográfico: Currículo Scientific AI Engineering

**Projeto Vinculado:** Integração de Machine Learning e Physics-Informed ML na Simulação de Desempenho de Edifícios
**Documento:** Relatório de Fundamentação Científica do Treinamento (Fase 0)
**Data original:** Janeiro 2026
**Última revisão:** Maio 2026 (conteúdo estável; o pacote do manuscrito de revisão de literatura em [Literature Review/](Literature%20Review/) foi atualizado em abril/2026 — sincronização de metadata, remoção de duplicatas, normalização da bibliografia e limpeza de mojibake)

---

## 1. Introdução e Contexto

Este documento detalha a fundamentação científica do currículo de **Scientific AI Engineering**, estruturado como um programa intensivo de 12 meses. O objetivo deste treinamento não é apenas o desenvolvimento de habilidades de programação, mas a capacitação técnica rigorosa para superar as lacunas identificadas na literatura recente (2023-2025) sobre Simulação de Desempenho de Edifícios (BPS) e Inteligência Artificial.

A premissa central, corroborada por **Hong et al. (2025)**, é que a transformação da modelagem energética exige uma nova classe de profissionais capazes de orquestrar fluxos de trabalho híbridos (Física + IA), superando as limitações dos métodos tradicionais.

---

## 2. Fundamentação por Módulos Curriculares

Abaixo, correlacionamos os módulos do treinamento com as referências bibliográficas que justificam sua inclusão e metodologia.

### 2.1. Infraestrutura e Rigor Científico (Mês 0-2)
*O alicerce para reprodutibilidade e escala.*

*   **Escolha do Python & EnergyPlus API:** A transição de interfaces gráficas para scripts Python é mandatória para automação em escala. **Osei-Owusu et al. (2025)** demonstram que fluxos de trabalho modulares JSON-Python são essenciais para viabilizar a automação de milhares de simulações, base para a geração de dados sintéticos (Fase 1 do projeto).
*   **Engenharia de Software (Testes e Tipagem):** A complexidade dos sistemas modernos de IA exige rigor de engenharia. A adoção de *Type Hints* e testes automatizados (pytest) no currículo visa mitigar o risco de "dívida técnica" em projetos científicos de longa duração.

### 2.2. Geração de Dados e Simulação Paramétrica (Mês 3)
*Superando a escassez de dados para treinamento.*

*   **Necessidade de Big Data:** Para treinar modelos robustos, o currículo foca na geração de datasets massivos (>100.000 amostras). **Chakraborty & Elzarka (2019)** estabelecem os protocolos para esta geração, validando o uso de *Surrogate Models* treinados em dados sintéticos como alternativa viável à simulação física lenta.
*   **O "Gap" Tropical:** O foco em validação climática (Mês 3 e 7) responde diretamente a **Wang et al. (2025)** e **Forouzandeh et al. (2023)**, que apontam a carência crítica de estudos validados em climas tropicais/úmidos, onde a dinâmica de calor latente desafia modelos simplificados.

### 2.3. Physics-Informed Machine Learning - PIML (Mês 4 e 7)
*O núcleo da inovação científica do projeto.*

*   **Por que PIML?** Modelos puramente baseados em dados (*black-box*) tendem a violar leis físicas. O currículo ensina explicitamente a implementação de *Physics-Informed Loss Functions*, conforme revisado por **Jiang, Z. X., et al. (2025)**. Esta abordagem penaliza violações termodinâmicas durante o treinamento da rede neural.
*   **Consistência Física:** A implementação de *Constraints* (Mês 7) segue as diretrizes de **Di Natale et al. (2022)**, garantindo que as previsões do modelo respeitem a conservação de energia, fundamental para a aceitação científica dos resultados.
*   **Eficiência de Dados:** O uso de *Physics-Constrained Deep Learning* (**Drgoňa et al., 2021**) é ensinado como método para reduzir a necessidade de dados de treinamento em 30-50%, acelerando a fase experimental.
*   **PI-GCN para Simulação Fluido-Térmica com Alta Eficiência de Dados:** **Peng et al. (2023)** demonstram que uma Rede Convolucional em Grafo Physics-Informed (PI-GCN) prediz com precisão campos de escoamento de fluidos e convecção de calor com apenas 20 amostras de treinamento — benchmark que sustenta diretamente o argumento de eficiência de dados do PIML no Mês 4: arquiteturas physics-informed podem reduzir drasticamente o número de simulações EnergyPlus necessárias para construir surrogates confiáveis.
*   **PI-GNN para Modelagem Térmica Multi-Zona:** **Yang et al. (2024)** demonstram que Redes Neurais em Grafo com Restrições Físicas (PI-GNNs) para dinâmica térmica de edifícios alcançam ganhos de precisão de 17–35% sobre MLPs padrão, ao codificar topologia de zonas e equações de balanço energético diretamente na arquitetura, fornecendo a base empírica para PIML baseado em grafos no Mês 4.
*   **Modelagem de Redes HVAC em Grafo:** **Li et al. (2024)** estendem o PIML em grafo para sistemas centrais de ar condicionado, modelando terminais VAV, AHUs e dutos como nós e arestas derivados de informação de projeto. Essa abordagem é diretamente relevante ao Mês 6 (Co-Simulação), permitindo representação estruturada da topologia HVAC para otimização baseada em surrogates.
*   **Segurança em PIML:** **Drgoňa (2025)** sintetiza avanços recentes em physics-informed machine learning seguro para dinâmica e controle, fornecendo a base metodológica para o framework anti-alucinação do Mês 7 com aplicação de restrições rígidas (vs. apenas penalidades baseadas em loss).

### 2.4. IA Generativa e Agentic AI (Mês 5, 6 e 9)
*A fronteira da automação cognitiva.*

*   **Automação via LLMs:** O treinamento em *Prompt Engineering* e *Fine-Tuning* (Mês 5) prepara a equipe para implementar agentes que traduzem linguagem natural em modelos de simulação. Esta abordagem é pioneira e baseada em **Zhang et al. (2025a)** e **Zhao et al. (2025)**, que demonstram a viabilidade de *Text-to-EnergyPlus*.
*   **Fine-Tuning Eficiente:** O uso de técnicas como LoRA (Low-Rank Adaptation) no currículo é diretamente suportado por **Jiang, G., et al. (2025b)**, que provaram a eficiência deste método para adaptar LLMs a casos complexos de modelagem energética.
*   **RAG (Retrieval-Augmented Generation):** A integração de bases normativas (NBR 15.575) via RAG (Mês 6) segue a tendência de sistemas especialistas assistidos por IA, como o *BIM-GPT* proposto por **Fernandes et al. (2024)**, que alcançou 94% de sucesso em interações com modelos BIM.
*   **LLMs com Restrições Físicas para HVAC:** **Subin et al. (2025)** demonstram que large language models physics-informed conseguem realizar detecção de anomalias em HVAC com geração autônoma de regras, fazendo ponte entre o Mês 5 (métodos de LLM) e o Mês 7 (compliance física) — usam LLMs para derivar e verificar restrições físicas, em vez de produzir previsões livres vulneráveis a violações termodinâmicas.

### 2.5. Otimização e Calibração (Mês 8 e 11)
*Fechando o ciclo entre simulação e realidade.*

*   **Otimização Multi-Objetivo:** O uso de algoritmos genéticos e otimização bayesiana (Optuna) no Mês 8 é validado por **Markarian et al. (2024)**, que reportaram aceleração de 1.266x em otimizações utilizando *surrogates* de ML em comparação com simulação direta.
*   **Incerteza e Calibração:** A ênfase em análise de sensibilidade e incerteza (Mês 11) responde ao alerta de **Tian (2024)** sobre a falha de modelos determinísticos em capturar a variabilidade operacional real.

### 2.6. Aprendizado Federado e Otimização Distribuída (Mês 10)
*Escalando a IA para redes de edifícios multi-site sem centralizar dados.*

*   **Aprendizado Federado Heurístico para Residências:** **Toderean et al. (2025)** aplicam aprendizado federado com ajuste adaptativo de hiperparâmetros para predição de energia residencial em nós heterogêneos (*Scientific Reports*), demonstrando que estratégias de agregação heurística alcançam acurácia comparável ao treinamento centralizado preservando a privacidade dos dados — preenchendo o caso federado específico para edifícios que o Mês 10 não possuía.
*   **DRL Federado Acelerado para HVAC:** **Xia et al. (2025)** apresentam um framework de deep reinforcement learning (DRL) federado acelerado para controle HVAC multi-zona em edifícios comerciais (*IEEE Transactions on Smart Grid*), demonstrando que agentes federados alcançam economias de energia próximas ao ótimo sem compartilhar dados operacionais brutos. Complementa o Mês 10 com um caso concreto de DRL distribuído alinhado ao cenário de otimização multi-site do projeto capstone.

---

## 3. Matriz de Rastreabilidade (Literatura vs. Currículo)

| Tópico Curricular | Referência Principal | Mês de Implementação | Justificativa Científica |
| :--- | :--- | :--- | :--- |
| **Automação EnergyPlus** | Osei-Owusu et al. (2025) | Mês 1 | Viabilizar geração de dados massiva. |
| **Geração de Datasets** | Chakraborty & Elzarka (2019) | Mês 3 | Base para treinamento de Surrogates. |
| **PIML Foundations** | Jiang, Z. X. et al. (2025) | Mês 4 | Garantir consistência termodinâmica. |
| **Physics Constraints** | Di Natale et al. (2022) | Mês 7 | Evitar "alucinações" físicas dos modelos. |
| **LLM para BEM** | Zhang et al. (2025a) | Mês 5 | Automação cognitiva de modelagem. |
| **Efficient Fine-Tuning** | Jiang, G. et al. (2025b) | Mês 5 | Adaptação de LLMs com recursos limitados. |
| **BIM-GPT / RAG** | Fernandes et al. (2024) | Mês 6 | Assistência inteligente ao projetista. |
| **Otimização Rápida** | Markarian et al. (2024) | Mês 8 | Otimização em tempo real via Surrogates. |
| **Validação Tropical** | Wang et al. (2025) | Mês 3, 7, 12 | Lacuna crítica na literatura global. |
| **Análise de Incerteza** | Tian (2024) | Mês 11 | Robustez contra variabilidade real. |
| **Eficiência de Dados PI-GCN** | Peng et al. (2023) | Mês 4 | Benchmark PIML com 20 amostras para surrogates. |
| **Aprendizado Federado (Edifícios)** | Toderean et al. (2025) | Mês 10 | Gerenciamento federado de energia em edificações. |
| **DRL Federado para HVAC** | Xia et al. (2025) | Mês 10 | RL distribuído para controle HVAC multi-site. |

---

## 4. Conclusão

O currículo **Scientific AI Engineering** não é um artefato isolado; é a **operacionalização do estado da arte** revisado na literatura de 2023-2025. Cada módulo técnico foi desenhado para equipar o pesquisador com as ferramentas exatas necessárias para executar projetos de pesquisa de ponta, garantindo que, ao final do Mês 12, a equipe esteja apta a produzir ciência de alto impacto e não apenas "rodar software".


## 5. Referências Bibliográficas (Base do Currículo)

As referências abaixo constituem a bibliografia obrigatória para o embasamento teórico dos exercícios propostos.

* **CHAKRABORTY, D.; ELZARKA, H.** Advanced machine learning techniques for building performance simulation: a comparative analysis. **Journal of Building Performance Simulation**, 2019. DOI: [10.1080/19401493.2018.1498538](https://doi.org/10.1080/19401493.2018.1498538).
* **DI NATALE, L.; SVETOZAREVIC, B.; HEER, P.; JONES, C. N.** Physically Consistent Neural Networks for building thermal modeling: Theory and analysis. **Applied Energy**, v. 325, p. 119806, 2022. DOI: [10.1016/j.apenergy.2022.119806](https://doi.org/10.1016/j.apenergy.2022.119806).
* **DRGOŇA, J.; TUOR, A. R.; CHANDAN, V.; VRABIE, D. L.** Physics-constrained deep learning of multi-zone building thermal dynamics. **Energy and Buildings**, v. 243, p. 110992, 2021. DOI: [10.1016/j.enbuild.2021.110992](https://doi.org/10.1016/j.enbuild.2021.110992).
* **DRGOŇA, J.** Safe physics-informed machine learning for dynamics and control. **arXiv preprint**, 2025. DOI: [10.48550/ARXIV.2504.12952](https://doi.org/10.48550/ARXIV.2504.12952).
* **ELSAYED, M.; SHULTZ, J.; KURTZ, J.** User-friendly AI-driven automation for rapid building energy model generation. **Energy and Buildings**, v. 345, p. 116092, 2025. DOI: [10.1016/j.enbuild.2025.116092](https://doi.org/10.1016/j.enbuild.2025.116092).
* **FERNANDES, D.; GARG, S.; NIKKEL, M.; GUVEN, G.** A GPT-Powered Assistant for Real-Time Interaction with Building Information Models. **Buildings**, v. 14, n. 8, p. 2499, 2024. DOI: [10.3390/buildings14082499](https://doi.org/10.3390/buildings14082499).
* **FORTH, K.; BORRMANN, A.** Semantic enrichment for BIM-based building energy performance simulations using semantic textual similarity and fine-tuning multilingual LLM. **Journal of Building Engineering**, v. 95, p. 110312, 2024. DOI: [10.1016/j.jobe.2024.110312](https://doi.org/10.1016/j.jobe.2024.110312).
* **FOROUZANDEH, N.; ZOMORODIAN, Z. S.; SHAGHAGHIAN, Z.; TAHSILDOOST, M.** Room energy demand and thermal comfort predictions in early stages of design based on the Machine Learning methods. **Intelligent Buildings International**, 2023. DOI: [10.1080/17508975.2022.2049190](https://doi.org/10.1080/17508975.2022.2049190).
* **LI, A.; ZHANG, J.; XIAO, F.; FAN, C.; YU, Y.; CHEN, Z.** Design Information-Assisted Graph Neural Network for Modeling Central Air Conditioning Systems. **Advanced Engineering Informatics**, 2024. DOI: [10.1016/j.aei.2024.102379](https://doi.org/10.1016/j.aei.2024.102379).
* **LI, H.; XU, Y.; HONG, T.** EnergyPlus-MCP: A model-context-protocol server for ai-driven building energy modeling. **SoftwareX**, v. 32, p. 102367, 2025. DOI: [10.1016/j.softx.2025.102367](https://doi.org/10.1016/j.softx.2025.102367).
* **HONG, T.; ZHANG, L.** AI for building energy modeling: A transformation. **Building Simulation**, v. 18, n. 9, p. 2219-2225, 2025. DOI: [10.1007/s12273-025-1329-4](https://doi.org/10.1007/s12273-025-1329-4).
* **JIANG, G.; CHEN, J.** Efficient fine-tuning of large language models for automated building energy modeling in complex cases. **Automation in Construction**, v. 175, p. 106223, 2025. DOI: [10.1016/j.autcon.2025.106223](https://doi.org/10.1016/j.autcon.2025.106223).
* **JIANG, G.; MA, Z.; ZHANG, L.; CHEN, J.** EPlus-LLM: A large language model-based computing platform for automated building energy modeling. **Applied Energy**, v. 367, p. 123431, 2024. DOI: [10.1016/j.apenergy.2024.123431](https://doi.org/10.1016/j.apenergy.2024.123431).
* **JIANG, G.; MA, Z.; ZHANG, L.; CHEN, J.** Prompt engineering to inform large language model in automated building energy modeling. **Energy**, v. 316, p. 134548, 2025. DOI: [10.1016/j.energy.2025.134548](https://doi.org/10.1016/j.energy.2025.134548).
* **JIANG, Z.; DONG, B.** Modularized neural network incorporating physical priors for future building energy modeling. **Patterns**, v. 5, n. 8, p. 101029, 2024. DOI: [10.1016/j.patter.2024.101029](https://doi.org/10.1016/j.patter.2024.101029).
* **JIANG, Z. X.; WANG, X. Z.; LI, H.; HONG, T. Z.; DONG, B.** Physics-informed machine learning for building performance simulation-A review of a nascent field. **Advances in Applied Energy**, 2025. DOI: [10.1016/j.adapen.2025.100223](https://doi.org/10.1016/j.adapen.2025.100223).
* **KHADKA, S.** Scaling Data Driven Building Energy Modeling Using Large Language Models: Prompt Engineering and Agentic Workflow. **M.S. thesis**, The University of Arizona, 2025.
* **KHADKA, S.; ZHANG, L.** Scaling Data-Driven Building Energy Modelling using Large Language Models. **arXiv preprint**, 2024. DOI: [10.48550/ARXIV.2407.03469](https://doi.org/10.48550/ARXIV.2407.03469).
* **KUBWIMANA, B.; NAJAFI, H.** A Novel Approach for Optimizing Building Energy Models Using Machine Learning Algorithms. **Energies**, v. 16, n. 3, p. 1033, 2023. DOI: [10.3390/en16031033](https://doi.org/10.3390/en16031033).
* **LU, J.; ZHENG, Z.; LANGTRY, M.; JACKSON, M.; ZHAO, Y.; FENG, C.; ZHANG, R.; ZHANG, C.; ZHANG, J.; CHOUDHARY, R.** Automated building energy modeling for energy retrofits using a large language model-based multi-agent framework. **iScience**, v. 28, n. 11, p. 113867, 2025. DOI: [10.1016/j.isci.2025.113867](https://doi.org/10.1016/j.isci.2025.113867).
* **MARKARIAN, E.; QIBLAWI, S.; KRISHNAN, S.; AZAR, E.** Informing building retrofits at low computational costs: a multi-objective optimisation using machine learning surrogates of building performance simulation models. **Journal of Building Performance Simulation**, 2024. DOI: [10.1080/19401493.2024.2384487](https://doi.org/10.1080/19401493.2024.2384487).
* **MICHALAKOPOULOS, V.; PELEKIS, S.; KORMPAKIS, G.; KARAKOLIS, V.; MOUZAKITIS, S.; ASKOUNIS, D.** Data-driven building energy efficiency prediction using physics-informed neural networks. In: **2024 IEEE Conference on Technologies for Sustainability (SusTech)**, p. 84-91, 2024. DOI: [10.1109/SusTech60925.2024.10553513](https://doi.org/10.1109/SusTech60925.2024.10553513).
* **OSEI-OWUSU, J.; BAHADORI-JAHROMI, A.; AMIRKHANI, S.; GODFREY, P.** Automating Building Energy Performance Simulation with EnergyPlus Using Modular JSON–Python Workflows: A Case Study of the Hilton Watford Hotel. **Sustainability**, v. 17, n. 22, p. 10317, 2025. DOI: [10.3390/su172210317](https://doi.org/10.3390/su172210317).
* **PENG, J.-Z.; HUA, Y.; LI, Y.-B.; CHEN, Z.-H.; WU, W.-T.; AUBRY, N.** Physics-Informed Graph Convolutional Neural Network for Modeling Fluid Flow and Heat Convection. **Physics of Fluids**, 2023. DOI: [10.1063/5.0161114](https://doi.org/10.1063/5.0161114).
* **RENDE, A. N. N.; YILMAZ, T.; ULUSOY, Ö.** Negotiating Comfort: Simulating Personality-Driven LLM Agents in Shared Residential Social Networks. **arXiv preprint**, 2025. DOI: [10.48550/ARXIV.2507.09657](https://doi.org/10.48550/ARXIV.2507.09657).
* **SHAO, X.; LIU, Z.; ZHANG, S.; ZHAO, Z.; HU, C.** PIGNN-CFD: A physics-informed graph neural network for rapid predicting urban wind field defined on unstructured mesh. **Building and Environment**, v. 232, p. 110056, 2023. DOI: [10.1016/j.buildenv.2023.110056](https://doi.org/10.1016/j.buildenv.2023.110056).
* **SONG, J.; YOON, S.** Ontology-assisted GPT-based building performance simulation and assessment: Implementation of multizone airflow simulation. **Energy and Buildings**, v. 325, p. 114983, 2024. DOI: [10.1016/j.enbuild.2024.114983](https://doi.org/10.1016/j.enbuild.2024.114983).
* **SUBIN, P.; PARK, J.; KIM, H.** Physics-informed large language models for HVAC anomaly detection with autonomous rule generation. **arXiv preprint**, 2025. DOI: [10.48550/ARXIV.2510.17146](https://doi.org/10.48550/ARXIV.2510.17146).
* **TIAN, W.** Towards advanced uncertainty and sensitivity analysis of building energy performance using machine learning techniques. **Journal of Building Performance Simulation**, v. 17, n. 6, p. 655-662, 2024. DOI: [10.1080/19401493.2024.2387071](https://doi.org/10.1080/19401493.2024.2387071).
* **TODEREAN, L.; DAIAN, M.; CIOARA, T.; ANGHEL, I.; MICHALAKOPOULOS, V.; SARANTINOPOULOS, E.; SARMAS, E.** Heuristic Based Federated Learning With Adaptive Hyperparameter Tuning for Households Energy Prediction. **Scientific Reports**, 2025. DOI: [10.1038/s41598-025-96443-3](https://doi.org/10.1038/s41598-025-96443-3).
* **VILLANO, F.; MAURO, G. M.; PEDACE, A.** A Review on Machine/Deep Learning Techniques Applied to Building Energy Simulation, Optimization and Management. **Thermo**, 2024. DOI: [10.3390/thermo4010008](https://doi.org/10.3390/thermo4010008).
* **WANG, D. Y.; DONG, Q.; SUN, C.** Evaluating the adaptation potential and retrofitting effectiveness of existing residential buildings in severe cold regions of China under climate change. **Building and Environment**, 2025. DOI: [10.1016/j.buildenv.2025.112982](https://doi.org/10.1016/j.buildenv.2025.112982).
* **XIA, Y.; WANG, X.; YIN, X.; BO, W.; WANG, L.; LI, S.; LI, K.** Federated Accelerated Deep Reinforcement Learning for Multi-Zone HVAC Control in Commercial Buildings. **IEEE Transactions on Smart Grid**, 2025. DOI: [10.1109/tsg.2024.3524756](https://doi.org/10.1109/tsg.2024.3524756).
* **YANG, Z.; GAIDHANE, A. D.; DRGOŇA, J.; CHANDAN, V.; HALAPPANAVAR, M. M.; LIU, F.; CAO, Y.** Physics-Constrained Graph Modeling for Building Thermal Dynamics. **Energy and AI**, 2024. DOI: [10.1016/j.egyai.2024.100346](https://doi.org/10.1016/j.egyai.2024.100346).
* **YANG, Z.; WU, P.** Research on intelligent generation of structural demolition suggestions based on multi-model collaboration. **arXiv preprint**, 2025. DOI: [10.48550/ARXIV.2508.15820](https://doi.org/10.48550/ARXIV.2508.15820).
* **ZHAN, D.; RAYEGAN, S.; QIN, S.; WANG, L.; HASSAN, I. G.** Leveraging large language models to enhance urban building energy modeling: A case study. 2025. DOI: [10.5194/icuc12-542](https://doi.org/10.5194/icuc12-542).
* **ZHAO, K.; DIENG, O.; LEE, S.** Poster Abstract: Text-To-EnergyPlus: Translating Natural Language into Building Energy Simulation. In: **Proceedings of the 12th ACM International Conference on Systems for Energy-Efficient Buildings, Cities, and Transportation**, p. 326-327, 2025. DOI: [10.1145/3736425.3772120](https://doi.org/10.1145/3736425.3772120).
* **ZHANG, L.; FORD, V.; CHEN, Z.; CHEN, J.** Automatic building energy model development and debugging using large language models agentic workflow. **Energy and Buildings**, v. 327, p. 115116, 2025. DOI: [10.1016/j.enbuild.2024.115116](https://doi.org/10.1016/j.enbuild.2024.115116).
* **ZHANG, L.; FU, X.; LI, Y.; CHEN, J.** Large language model-based agent Schema and library for automated building energy analysis and modeling. **Automation in Construction**, v. 176, p. 106244, 2025. DOI: [10.1016/j.autcon.2025.106244](https://doi.org/10.1016/j.autcon.2025.106244).
* **ZHANG, L.; CHEN, Z.; FORD, V.** Advancing building energy modeling with large language models: Exploration and case studies. **Energy and Buildings**, v. 323, p. 114788, 2024. DOI: [10.1016/j.enbuild.2024.114788](https://doi.org/10.1016/j.enbuild.2024.114788).
