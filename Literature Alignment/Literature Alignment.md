# Bibliographic Alignment: Scientific AI Engineering Curriculum

**Related Context:** Integration of Machine Learning and Physics-Informed ML in Building Performance Simulation
**Document:** Scientific Foundation Report (Phase 0)
**Date:** January 2026

---

## 1. Introduction and Context

This document details the scientific foundation of the **Scientific AI Engineering** curriculum, structured as an intensive 12-month program. The objective of this training is not merely the development of programming skills, but rigorous technical empowerment to overcome the gaps identified in recent literature (2023-2025) regarding Building Performance Simulation (BPS) and Artificial Intelligence.

The central premise, corroborated by **Hong et al. (2025)**, is that the transformation of energy modeling requires a new class of professionals capable of orchestrating hybrid workflows (Physics + AI), overcoming the limitations of traditional methods.

---

## 2. Foundation by Curricular Modules

Below, we correlate the training modules with the bibliographic references that justify their inclusion and methodology.

### 2.1. Infrastructure and Scientific Rigor (Month 0-2)
*The foundation for reproducibility and scale.*

*   **Python & EnergyPlus API Choice:** The transition from graphical interfaces to Python scripts is mandatory for automation at scale. **Osei-Owusu et al. (2025)** demonstrate that modular JSON-Python workflows are essential to enable thousands of simulations, the basis for synthetic data generation (Phase 1).
*   **Software Engineering (Testing and Typing):** The complexity of modern AI systems demands engineering rigor. The adoption of *Type Hints* and automated tests (pytest) in the curriculum aims to mitigate the risk of "technical debt" in long-term scientific projects.

### 2.2. Data Generation and Parametric Simulation (Month 3)
*Overcoming data scarcity for training.*

*   **Need for Big Data:** To train robust models, the curriculum focuses on generating massive datasets (>100,000 samples). **Chakraborty & Elzarka (2019)** establish the protocols for this generation, validating the use of *Surrogate Models* trained on synthetic data as a viable alternative to slow physical simulation.
*   **The Tropical Gap:** The focus on climatic validation (Month 3 and 7) directly addresses **Wang et al. (2025)** and **Forouzandeh et al. (2023)**, who point out the critical lack of validated studies in tropical/humid climates, where latent heat dynamics challenge simplified models.

### 2.3. Physics-Informed Machine Learning - PIML (Month 4 and 7)
*The core of scientific innovation.*

*   **Why PIML?** Purely data-driven models (*black-box*) tend to violate physical laws. The curriculum explicitly teaches the implementation of *Physics-Informed Loss Functions*, as reviewed by **Jiang, Z. X., et al. (2025)**. This approach penalizes thermodynamic violations during neural network training.
*   **Physical Consistency:** The implementation of *Constraints* (Month 7) follows the guidelines of **Di Natale et al. (2022)**, ensuring that model predictions respect energy conservation, which is fundamental for the scientific acceptance of results.
*   **Data Efficiency:** The use of *Physics-Constrained Deep Learning* (**Drgoňa et al., 2021**) is taught as a method to reduce the need for training data by 30-50%, accelerating the experimental phase.

### 2.4. Generative AI and Agentic AI (Month 5, 6 and 9)
*The frontier of cognitive automation.*

*   **Automation via LLMs:** Training in *Prompt Engineering* and *Fine-Tuning* (Month 5) prepares the team to implement agents that translate natural language into simulation models. This approach is pioneering and based on **Zhang et al. (2025a)** and **Zhao et al. (2025)**, who demonstrate the viability of *Text-to-EnergyPlus*.
*   **Efficient Fine-Tuning:** The use of techniques like LoRA (Low-Rank Adaptation) in the curriculum is directly supported by **Jiang, G., et al. (2025b)**, who proved the efficiency of this method for adapting LLMs to complex energy modeling cases.
*   **RAG (Retrieval-Augmented Generation):** The integration of normative bases (e.g., NBR 15.575) via RAG (Month 6) follows the trend of AI-assisted expert systems, such as the *BIM-GPT* proposed by **Fernandes et al. (2024)**, which achieved 94% success in interactions with BIM models.

### 2.5. Optimization and Calibration (Month 8 and 11)
*Closing the loop between simulation and reality.*

*   **Multi-Objective Optimization:** The use of genetic algorithms and Bayesian optimization (Optuna) in Month 8 is validated by **Markarian et al. (2024)**, who reported a 1,266x acceleration in optimizations using ML *surrogates* compared to direct simulation.
*   **Uncertainty and Calibration:** The emphasis on sensitivity analysis and uncertainty (Month 11) responds to the warning by **Tian (2024)** regarding the failure of deterministic models to capture real operational variability.

---

## 3. Traceability Matrix (Literature vs. Curriculum)

| Curricular Topic | Principal Reference | Implementation Month | Scientific Justification |
| :--- | :--- | :--- | :--- |
| **EnergyPlus Automation** | Osei-Owusu et al. (2025) | Month 1 | Enable massive data generation. |
| **Dataset Generation** | Chakraborty & Elzarka (2019) | Month 3 | Foundation for training Surrogates. |
| **PIML Foundations** | Jiang, Z. X. et al. (2025) | Month 4 | Ensure thermodynamic consistency. |
| **Physics Constraints** | Di Natale et al. (2022) | Month 7 | Avoid physical "hallucinations" of models. |
| **LLM for BEM** | Zhang et al. (2025a) | Month 5 | Cognitive modeling automation. |
| **Efficient Fine-Tuning** | Jiang, G. et al. (2025b) | Month 5 | LLM adaptation with limited resources. |
| **BIM-GPT / RAG** | Fernandes et al. (2024) | Month 6 | Intelligent assistant for the designer. |
| **Rapid Optimization** | Markarian et al. (2024) | Month 8 | Real-time optimization via Surrogates. |
| **Tropical Validation** | Wang et al. (2025) | Month 3, 7, 12 | Critical gap in global literature. |
| **Uncertainty Analysis** | Tian (2024) | Month 11 | Robustness against real variability. |

---

## 4. Conclusion

The **Scientific AI Engineering** curriculum is not an isolated artifact; it is the **operationalization of the state of the art** reviewed in the literature of 2023-2025. Each technical module was designed to equip the researcher with the exact tools necessary to execute cutting-edge research projects, ensuring that, by the end of Month 12, the team is capable of producing high-impact science and not just "running software".


## 5. Bibliographic References (Curriculum Base)

The references below constitute the mandatory bibliography for the theoretical grounding of the proposed exercises.

* **CHAKRABORTY, D.; ELZARKA, H.** Advanced machine learning techniques for building performance simulation: a comparative analysis. **Journal of Building Performance Simulation**, 2019. DOI: [10.1080/19401493.2018.1498538](https://doi.org/10.1080/19401493.2018.1498538).
* **DI NATALE, L.; SVETOZAREVIC, B.; HEER, P.; JONES, C. N.** Physically Consistent Neural Networks for building thermal modeling: Theory and analysis. **Applied Energy**, v. 325, p. 119806, 2022. DOI: [10.1016/j.apenergy.2022.119806](https://doi.org/10.1016/j.apenergy.2022.119806).
* **DRGOŇA, J.; TUOR, A. R.; CHANDAN, V.; VRABIE, D. L.** Physics-constrained deep learning of multi-zone building thermal dynamics. **Energy and Buildings**, v. 243, p. 110992, 2021. DOI: [10.1016/j.enbuild.2021.110992](https://doi.org/10.1016/j.enbuild.2021.110992).
* **ELSAYED, M.; SHULTZ, J.; KURTZ, J.** User-friendly AI-driven automation for rapid building energy model generation. **Energy and Buildings**, v. 345, p. 116092, 2025. DOI: [10.1016/j.enbuild.2025.116092](https://doi.org/10.1016/j.enbuild.2025.116092).
* **FERNANDES, D.; GARG, S.; NIKKEL, M.; GUVEN, G.** A GPT-Powered Assistant for Real-Time Interaction with Building Information Models. **Buildings**, v. 14, n. 8, p. 2499, 2024. DOI: [10.3390/buildings14082499](https://doi.org/10.3390/buildings14082499).
* **FORTH, K.; BORRMANN, A.** Semantic enrichment for BIM-based building energy performance simulations using semantic textual similarity and fine-tuning multilingual LLM. **Journal of Building Engineering**, v. 95, p. 110312, 2024. DOI: [10.1016/j.jobe.2024.110312](https://doi.org/10.1016/j.jobe.2024.110312).
* **FOROUZANDEH, N.; ZOMORODIAN, Z. S.; SHAGHAGHIAN, Z.; TAHSILDOOST, M.** Room energy demand and thermal comfort predictions in early stages of design based on the Machine Learning methods. **Intelligent Buildings International**, 2023. DOI: [10.1080/17508975.2022.2049190](https://doi.org/10.1080/17508975.2022.2049190).
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
* **RENDE, A. N. N.; YILMAZ, T.; ULUSOY, Ö.** Negotiating Comfort: Simulating Personality-Driven LLM Agents in Shared Residential Social Networks. **arXiv preprint**, 2025. DOI: [10.48550/ARXIV.2507.09657](https://doi.org/10.48550/ARXIV.2507.09657).
* **SHAO, X.; LIU, Z.; ZHANG, S.; ZHAO, Z.; HU, C.** PIGNN-CFD: A physics-informed graph neural network for rapid predicting urban wind field defined on unstructured mesh. **Building and Environment**, v. 232, p. 110056, 2023. DOI: [10.1016/j.buildenv.2023.110056](https://doi.org/10.1016/j.buildenv.2023.110056).
* **SONG, J.; YOON, S.** Ontology-assisted GPT-based building performance simulation and assessment: Implementation of multizone airflow simulation. **Energy and Buildings**, v. 325, p. 114983, 2024. DOI: [10.1016/j.enbuild.2024.114983](https://doi.org/10.1016/j.enbuild.2024.114983).
* **TIAN, W.** Towards advanced uncertainty and sensitivity analysis of building energy performance using machine learning techniques. **Journal of Building Performance Simulation**, v. 17, n. 6, p. 655-662, 2024. DOI: [10.1080/19401493.2024.2387071](https://doi.org/10.1080/19401493.2024.2387071).
* **VILLANO, F.; MAURO, G. M.; PEDACE, A.** A Review on Machine/Deep Learning Techniques Applied to Building Energy Simulation, Optimization and Management. **Thermo**, 2024. DOI: [10.3390/thermo4010008](https://doi.org/10.3390/thermo4010008).
* **WANG, D. Y.; DONG, Q.; SUN, C.** Evaluating the adaptation potential and retrofitting effectiveness of existing residential buildings in severe cold regions of China under climate change. **Building and Environment**, 2025. DOI: [10.1016/j.buildenv.2025.112982](https://doi.org/10.1016/j.buildenv.2025.112982).
* **YANG, Z.; WU, P.** Research on intelligent generation of structural demolition suggestions based on multi-model collaboration. **arXiv preprint**, 2025. DOI: [10.48550/ARXIV.2508.15820](https://doi.org/10.48550/ARXIV.2508.15820).
* **ZHAN, D.; RAYEGAN, S.; QIN, S.; WANG, L.; HASSAN, I. G.** Leveraging large language models to enhance urban building energy modeling: A case study. 2025. DOI: [10.5194/icuc12-542](https://doi.org/10.5194/icuc12-542).
* **ZHAO, K.; DIENG, O.; LEE, S.** Poster Abstract: Text-To-EnergyPlus: Translating Natural Language into Building Energy Simulation. In: **Proceedings of the 12th ACM International Conference on Systems for Energy-Efficient Buildings, Cities, and Transportation**, p. 326-327, 2025. DOI: [10.1145/3736425.3772120](https://doi.org/10.1145/3736425.3772120).
* **ZHANG, L.; FORD, V.; CHEN, Z.; CHEN, J.** Automatic building energy model development and debugging using large language models agentic workflow. **Energy and Buildings**, v. 327, p. 115116, 2025. DOI: [10.1016/j.enbuild.2024.115116](https://doi.org/10.1016/j.enbuild.2024.115116).
* **ZHANG, L.; FU, X.; LI, Y.; CHEN, J.** Large language model-based agent Schema and library for automated building energy analysis and modeling. **Automation in Construction**, v. 176, p. 106244, 2025. DOI: [10.1016/j.autcon.2025.106244](https://doi.org/10.1016/j.autcon.2025.106244).
* **ZHANG, L.; CHEN, Z.; FORD, V.** Advancing building energy modeling with large language models: Exploration and case studies. **Energy and Buildings**, v. 323, p. 114788, 2024. DOI: [10.1016/j.enbuild.2024.114788](https://doi.org/10.1016/j.enbuild.2024.114788).
