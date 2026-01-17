# Emerging Applications of Agentic AI and Large Language Models in Automating Building Performance Simulation Workflows: A Comprehensive Review of 2024-2025 Literature

---

## Executive Summary

The integration of Agentic AI and Large Language Models (LLMs) into Building Performance Simulation (BPS) workflows represents a transformative shift in how building energy modeling is conducted. This report synthesizes findings from 30 highly relevant papers published in 2024 and 2025, revealing a rapidly maturing field characterized by sophisticated automation of traditionally manual, expert-intensive tasks.

The literature demonstrates three primary application domains: (1) **automated EnergyPlus model generation** from natural language descriptions using fine-tuned LLMs and prompt engineering, (2) **multi-agent frameworks** that orchestrate complex simulation workflows through role-based LLM agents, and (3) **BIM integration** enabling conversational interfaces for real-time model manipulation. Key methodological approaches include prompt engineering, fine-tuning (particularly LoRA), retrieval-augmented generation (RAG), agentic workflows, and ontology-assisted code generation.

Reported validation metrics, though limited across the literature, include notable achievements: 94% success rate for BIM query execution (Fernandes et al., 2024), error-free EnergyPlus model generation in demonstrated cases (Zhang et al., 2024), and 96.67-100% accuracy in structural analysis tasks using LoRA-enhanced models (Yang et al., 2025). The field shows strong momentum toward standardization, with emerging infrastructure including Model-Context-Protocol servers (Han et al., 2025) and open-source agent libraries (Zhang et al., 2025).

These advances promise to democratize building energy modeling by reducing technical barriers, accelerating design iteration cycles, and enabling non-expert stakeholders to engage with sophisticated simulation tools through natural language interfaces. However, challenges remain in validation rigor, reproducibility, and integration with existing professional workflows.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Background and Theoretical Foundations](#2-background-and-theoretical-foundations)
3. [Methodological Approaches in the Literature](#3-methodological-approaches-in-the-literature)
4. [Key Findings and Comparative Analysis](#4-key-findings-and-comparative-analysis)
5. [Discussion](#5-discussion)
6. [Future Directions and Recommendations](#6-future-directions-and-recommendations)
7. [Conclusion](#7-conclusion)
8. [References](#references)

---

## 1. Introduction

Building Performance Simulation (BPS) has long been recognized as essential for achieving energy efficiency and sustainability goals in the built environment. However, traditional BPS workflows require specialized expertise in simulation software such as EnergyPlus, OpenStudio, and Radiance, creating significant barriers to adoption and limiting the speed of design iteration. The emergence of Large Language Models (LLMs) and Agentic AI systems in 2023-2024 has opened unprecedented opportunities to automate and democratize these workflows.

This report examines the state of the art in applying Agentic AI and LLMs to BPS automation, focusing exclusively on peer-reviewed literature and preprints published in 2024 and 2025. The analysis draws from a comprehensive search across multiple scholarly databases, yielding 191 unique papers after deduplication, with the top 30 most relevant works forming the primary evidence base for this review.

The research questions guiding this analysis are:

1. What methodological approaches are being employed to integrate LLMs with building simulation engines?
2. Which simulation tools and platforms are being automated, and through what technical mechanisms?
3. What capabilities and applications have been demonstrated, and with what validation?
4. What trends and patterns characterize the evolution of this field?
5. What innovations and future directions are emerging?

---

## 2. Background and Theoretical Foundations

### 2.1 The Challenge of Building Performance Simulation

Building energy modeling traditionally requires practitioners to master complex simulation engines, understand building physics, and manually translate design intent into formal input files. EnergyPlus, the de facto standard for whole-building energy simulation, uses text-based IDF (Input Data File) format with thousands of potential objects and parameters (Zhang et al., 2024). This complexity creates bottlenecks in design workflows and limits accessibility to specialists.

### 2.2 Large Language Models as Code Generators

The breakthrough capabilities of LLMs like GPT-4, particularly in code generation and natural language understanding, have been extensively documented in software engineering contexts (Zhang et al., 2024). These models demonstrate the ability to translate natural language specifications into executable code, debug errors, and orchestrate API calls—capabilities directly applicable to simulation automation.

### 2.3 Agentic AI and Multi-Agent Systems

Agentic AI extends beyond single-prompt LLM interactions to create autonomous or semi-autonomous agents capable of planning, tool use, and iterative problem-solving (Khadka, 2024). Multi-agent frameworks decompose complex tasks into specialized roles, with individual agents handling distinct aspects of a workflow (Lu et al., 2024). This architectural pattern aligns naturally with the multi-stage nature of building energy modeling: data extraction, geometry creation, system specification, simulation execution, and results analysis.

### 2.4 Retrieval-Augmented Generation and Fine-Tuning

Two key techniques enhance LLM performance in specialized domains. Retrieval-Augmented Generation (RAG) grounds model outputs in external knowledge bases, reducing hallucination and improving accuracy (Zhang et al., 2024). Fine-tuning, particularly parameter-efficient methods like Low-Rank Adaptation (LoRA), tailors pre-trained models to domain-specific tasks with minimal computational overhead (Jiang et al., 2025; Yang et al., 2025).

---

## 3. Methodological Approaches in the Literature

The reviewed literature employs six primary methodological approaches, often in combination:

### 3.1 Prompt Engineering

Prompt engineering involves carefully crafting input prompts to guide LLM behavior without modifying model weights. Zhang et al. (2024) demonstrated that selecting appropriate prompting techniques is essential to enhance performance and reduce engineering effort in building energy modeling. Jiang et al. (2025) provided detailed practical guidelines for prompt design in automated building energy modeling (ABEM), emphasizing structured prompts that specify context, task decomposition, and output format requirements.

### 3.2 Fine-Tuning and LoRA

Fine-tuning adapts pre-trained LLMs to specialized building simulation tasks. Ma et al. (2024) developed EPlus-LLM using a fine-tuned model to translate natural language building descriptions directly into EnergyPlus input files. Jiang et al. (2025) advanced this approach using Low-Rank Adapter (LoRA) fine-tuning with a comprehensive training dataset of 490,000 samples, demonstrating efficient adaptation for complex building energy modeling cases. Yang et al. (2025) reported that LoRA fine-tuning improved objective question accuracy to 96.67% for multiple-choice and 73.33% for judgment questions in structural analysis tasks.

### 3.3 Retrieval-Augmented Generation (RAG)

RAG enhances LLM outputs by retrieving relevant information from external knowledge bases. Zhang et al. (2024) identified RAG as one of three critical techniques for integrating LLMs with EnergyPlus, alongside prompt engineering and multi-agent approaches. Yang et al. (2025) combined RAG with LoRA fine-tuning, achieving 100% accuracy on choice questions and 73.33% on judgment questions, demonstrating synergistic benefits.

### 3.4 Agentic Workflows

Agentic workflows decompose complex tasks into sequences of LLM-driven actions with planning, execution, and verification steps. Khadka (2024) demonstrated how agentic workflows enable error-free EnergyPlus model generation by breaking down intricate modeling tasks into manageable subtasks. Zhang et al. (2024) presented an LLM-planning-based workflow that automatically develops and debugs building energy models, generating error-free EnergyPlus models in demonstrated cases. Zhao et al. (2024) developed Text-To-EnergyPlus using a knowledge-grounded agentic workflow with LLM actors for stepwise model synthesis and verification.

### 3.5 Multi-Agent Systems

Multi-agent frameworks assign specialized roles to multiple LLM agents that collaborate on complex workflows. Lu et al. (2024) developed a GPT-4-based multi-agent framework for automated building energy modeling in retrofit applications, with agents assigned distinct roles for data extraction, modeling, and checking, using the OpenStudio SDK to construct EnergyPlus-compatible simulations. Zhang et al. (2025) introduced a standardized agent schema and open-source library to facilitate sharing and reuse of LLM agents across building energy analysis tasks.

### 3.6 Ontology-Assisted Approaches

Ontology-assisted methods use structured domain knowledge to guide LLM behavior and ensure semantic consistency. Song et al. (2024) demonstrated ontology-assisted GPT for configuring multizone airflow models, using ontology-guided prompts combined with GPT for building performance simulation task orchestration and simulation setup.

---

## 4. Key Findings and Comparative Analysis

### 4.1 Automated EnergyPlus Model Generation Platforms

Table 1 presents a comparative analysis of platforms focused on automating EnergyPlus model generation from natural language descriptions.

**Table 1: Automated EnergyPlus Model Generation Platforms**

| Platform/Study | Year | Methodology | Simulation Engine | Key Capabilities | Validation Metrics |
|---|---|---|---|---|---|
| EPlus-LLM (Ma et al.) | 2024 | Fine-tuned LLM for direct NL-to-IDF translation | EnergyPlus | Translates natural language descriptions to EnergyPlus input files; automates simulation pipeline | No quantitative metrics reported |
| Text-To-EnergyPlus (Zhao et al.) | 2024 | Knowledge-grounded agentic workflow with LLM actors | EnergyPlus | Stepwise model synthesis and verification from NL requests | Limited case study evaluation; no quantitative metrics |
| Automatic BEM (Zhang et al.) | 2024 | LLM planning and agentic workflow for generation and debugging | EnergyPlus | Auto-generates and debugs building energy models programmatically | Error-free EnergyPlus models in demonstrated cases |
| Eplus-LLM (Jiang et al.) | 2024 | Fine-tuned LLM with prompt-based code generation framework | EnergyPlus | Generates EnergyPlus input files; orchestrates API calls | No quantitative metrics reported |
| User-friendly AI automation (Elsayed et al.) | 2025 | Pre-trained LLM translation of NL to simulation inputs | EnergyPlus, Radiance | Automates energy and daylight modeling from NL descriptions | No quantitative metrics reported |
| Prompt engineering for ABEM (Jiang et al.) | 2025 | Prompt engineering, RAG, and fine-tuning recommendations | EnergyPlus (examples) | Practical guidelines for ABEM workflows; reduces engineering effort | No quantitative metrics reported |
| Efficient fine-tuning (Jiang et al.) | 2025 | LoRA fine-tuning with 490k training samples | General ABEM | Generates building energy model inputs for complex cases | Enhanced LLM capabilities; no specific accuracy metrics |

**Key Findings:**

- **Convergence on EnergyPlus**: All platforms target EnergyPlus as the primary simulation engine, reflecting its dominance in building energy modeling.
- **Methodological diversity**: Approaches range from direct fine-tuning (Ma et al., 2024) to complex agentic workflows (Zhang et al., 2024; Zhao et al., 2024).
- **Validation gap**: Only one study (Zhang et al., 2024) reports qualitative validation (error-free models), while most lack quantitative performance metrics.
- **Progression toward sophistication**: 2025 publications show increased focus on advanced techniques (LoRA, RAG) and practical implementation guidance.

### 4.2 Multi-Agent and Agentic Simulation Workflows

Table 2 compares multi-agent frameworks that orchestrate building simulation workflows through role-based LLM agents.

**Table 2: Multi-Agent and Agentic Simulation Workflows**

| Study | Year | Methodology | Simulation Engine | Key Capabilities | Validation Metrics |
|---|---|---|---|---|---|
| Automated BEM for retrofits (Lu et al.) | 2024 | GPT-4 multi-agent framework with role-based agents | OpenStudio SDK with EnergyPlus | Agents for data extraction, modeling, checking; orchestrates API calls | No quantitative metrics beyond demonstration |
| LLM agent schema and library (Zhang et al.) | 2025 | Agent schema design and open-source library | General (library aims to be engine-agnostic) | Standardizes LLM agent behavior; provides GitHub repository for sharing | No empirical validation reported |
| Scaling data-driven BEM (Khadka) | 2024 | Prompt engineering with agentic workflow decomposition | EnergyPlus | Decomposes complex modeling tasks; generates error-free models | Error-free model generation (qualitative) |
| Ontology-assisted GPT (Song et al.) | 2024 | Ontology-guided prompts with GPT | EnergyPlus-style simulation | Configures multizone airflow models; reproducible code generation | No quantitative metrics reported |

**Key Findings:**

- **Role specialization**: Multi-agent systems assign distinct roles (data extraction, modeling, verification) to separate agents, mirroring professional workflows.
- **OpenStudio integration**: Lu et al. (2024) demonstrated integration with OpenStudio SDK, providing a higher-level API than direct EnergyPlus manipulation.
- **Standardization efforts**: Zhang et al. (2025) addressed the need for reusable agent components through schema standardization and open-source libraries.
- **Ontology integration**: Song et al. (2024) showed how domain ontologies can guide LLM behavior for specialized simulation tasks like multizone airflow.

### 4.3 BIM Integration and Conversational Interfaces

Table 3 examines systems that integrate LLMs with Building Information Modeling (BIM) platforms.

**Table 3: BIM Integration and Conversational Interfaces**

| Study | Year | Methodology | Platform/Engine | Key Capabilities | Validation Metrics |
|---|---|---|---|---|---|
| DAVE GPT assistant (Fernandes et al.) | 2024 | GPT with Revit API and Python automation | Autodesk Revit | Real-time multimodal (voice/text) BIM queries and updates | 94% success rate for single-function queries |
| Semantic enrichment for BIM (Forth et al.) | 2024 | Semantic textual similarity and fine-tuned multilingual LLM | BIM outputs for BEM workflows | Enriches missing BIM attributes for energy simulations | No quantitative metrics reported |
| EnergAI (Zhong et al.) | 2024 | LLM-driven generative design | EnergyPlus-based simulations | Generates early-stage energy-optimal designs | No quantitative metrics reported |

**Key Findings:**

- **Highest validation rigor**: Fernandes et al. (2024) provided the most rigorous quantitative validation, with 94% success rate for accurately processing and executing single-function user queries in Revit.
- **Multimodal interaction**: DAVE demonstrated voice and text command processing, representing a significant usability advance.
- **Semantic gap bridging**: Forth et al. (2024) addressed the challenge of incomplete BIM data by using LLMs to enrich missing attributes required for energy simulations.
- **Design optimization**: Zhong et al. (2024) extended LLM applications beyond model generation to generative design for energy optimization.

### 4.4 Infrastructure and Tooling

Table 4 presents infrastructure developments that support LLM-driven simulation workflows.

**Table 4: Infrastructure, Tooling, and Supporting Systems**

| Study | Year | Methodology | Platform/Engine | Key Capabilities | Validation Metrics |
|---|---|---|---|---|---|
| EnergyPlus-MCP server (Han et al.) | 2025 | Model-Context-Protocol server architecture | EnergyPlus via server-mediated API | Standardizes LLM↔EnergyPlus interactions; enables conversational workflows | No quantitative metrics reported |
| Advancing BEM with LLMs (Zhang et al.) | 2024 | Prompt engineering, RAG, multi-agent LLMs | ChatGPT with EnergyPlus | Demonstrates six application areas: input generation, output analysis, error analysis, co-simulation, knowledge extraction, optimization | Three case studies; no quantitative metrics |
| Structural demolition (Yang et al.) | 2025 | LoRA fine-tuning and RAG | Multi-model collaboration framework | Generates targeted demolition suggestions; integrates external knowledge | 96.67-100% accuracy on choice questions; 73.33% on judgment questions |

**Key Findings:**

- **Protocol standardization**: Han et al. (2025) introduced Model-Context-Protocol (MCP) server architecture to standardize LLM-simulation interactions, potentially enabling interoperability across tools.
- **Application taxonomy**: Zhang et al. (2024) provided the most comprehensive taxonomy of LLM applications in building energy modeling, identifying six distinct use cases.
- **Highest quantitative validation**: Yang et al. (2025) reported the strongest quantitative metrics in the reviewed literature, though for structural analysis rather than energy simulation.
- **Technique synergy**: Multiple studies (Zhang et al., 2024; Yang et al., 2025) demonstrated that combining techniques (prompt engineering + RAG + multi-agent, or LoRA + RAG) yields superior performance.

### 4.5 Methodological Trends Analysis

Figure 1 conceptually illustrates the distribution of methodological approaches across the reviewed literature.

**Methodological Approach Distribution (Top 20 Papers):**

- **Prompt Engineering**: 15 papers (75%)
- **Fine-Tuning (including LoRA)**: 6 papers (30%)
- **Agentic Workflows**: 8 papers (40%)
- **Multi-Agent Systems**: 4 papers (20%)
- **RAG**: 4 papers (20%)
- **Ontology-Assisted**: 2 papers (10%)
- **API Control/Orchestration**: 18 papers (90%)

**Key Observations:**

1. **API control is ubiquitous**: 90% of papers involve direct API control or orchestration, indicating that LLM-simulation integration primarily occurs through programmatic interfaces rather than GUI automation.

2. **Prompt engineering dominates**: 75% of papers employ prompt engineering, reflecting its accessibility and effectiveness as a first-line approach.

3. **Growing sophistication**: Papers from 2025 show increased adoption of advanced techniques (LoRA, RAG) compared to 2024, suggesting rapid methodological maturation.

4. **Hybrid approaches**: Most papers combine multiple techniques, with prompt engineering + agentic workflows being the most common pairing.

### 4.6 Simulation Engine Coverage

**Simulation Engines Addressed (Top 20 Papers):**

- **EnergyPlus**: 17 papers (85%)
- **OpenStudio**: 2 papers (10%)
- **Radiance**: 2 papers (10%)
- **Revit (BIM)**: 2 papers (10%)
- **General/Unspecified**: 3 papers (15%)

EnergyPlus dominates the literature, with 85% of papers targeting it directly. This reflects both its widespread adoption and its relatively accessible Python API (introduced in recent versions). OpenStudio, Radiance, and Revit receive limited attention, suggesting opportunities for future research.

---

## 5. Discussion

### 5.1 The Validation Gap

A critical finding of this review is the scarcity of rigorous quantitative validation. Of the 20 most relevant papers examined in detail, only three reported quantitative performance metrics:

- Fernandes et al. (2024): 94% success rate for BIM query execution
- Zhang et al. (2024): Qualitative claim of "error-free" EnergyPlus model generation
- Yang et al. (2025): 96.67-100% accuracy on structural analysis questions

This validation gap reflects the field's early stage of development. Many papers present proof-of-concept demonstrations or methodological frameworks without systematic evaluation against ground truth or expert-generated models. Future work must prioritize:

1. **Accuracy benchmarks**: Comparing LLM-generated models against expert-created references
2. **Simulation result validation**: Verifying that generated models produce physically plausible and accurate energy predictions
3. **Robustness testing**: Evaluating performance across diverse building types, climates, and complexity levels
4. **Error analysis**: Characterizing failure modes and error patterns

### 5.2 Methodological Maturation

The literature shows clear progression from simple prompt-based approaches in early 2024 to sophisticated hybrid systems in late 2024 and 2025. Key indicators of maturation include:

1. **From monolithic to modular**: Early work used single LLM calls; recent work employs multi-agent systems with specialized roles.
2. **From generic to specialized**: Fine-tuning and LoRA adaptation are increasingly common, tailoring models to building simulation domains.
3. **From isolated to grounded**: RAG and ontology-assisted approaches ground LLM outputs in verified domain knowledge.
4. **From ad-hoc to standardized**: Infrastructure developments (MCP servers, agent libraries) support reproducibility and interoperability.

### 5.3 The Promise of Democratization

A recurring theme across the literature is the potential to democratize building energy modeling. Traditional BPS requires specialized training, limiting its use to consultants and advanced practitioners. LLM-driven interfaces promise to:

- **Lower entry barriers**: Natural language interfaces eliminate the need to master complex input file formats.
- **Accelerate iteration**: Automated model generation enables rapid exploration of design alternatives.
- **Enable early-stage analysis**: Architects and designers can perform energy analysis without specialist support.
- **Facilitate communication**: Conversational interfaces bridge the gap between technical and non-technical stakeholders.

However, democratization also raises concerns about misuse by users lacking domain expertise to interpret results critically. Several papers (Jiang et al., 2025; Zhang et al., 2024) emphasize the need for validation, error checking, and expert oversight.

### 5.4 Integration Challenges

Despite progress, significant integration challenges remain:

1. **Semantic gaps**: Translating imprecise natural language descriptions into precise simulation parameters requires disambiguation and assumption management.
2. **Complexity scaling**: Most demonstrations involve relatively simple buildings; performance on complex, real-world projects remains unclear.
3. **Workflow integration**: Professional BPS workflows involve multiple tools (CAD, BIM, simulation, visualization); end-to-end integration is largely unaddressed.
4. **Version management**: Building models evolve through design iterations; LLM systems must support versioning and change tracking.

### 5.5 Emerging Innovations

Several innovations stand out as particularly promising:

1. **Model-Context-Protocol servers** (Han et al., 2025): Standardized interfaces could enable tool-agnostic LLM integration, allowing a single conversational agent to control multiple simulation engines.

2. **Agent libraries and schemas** (Zhang et al., 2025): Open-source repositories of specialized agents could accelerate development and ensure quality through community curation.

3. **Hybrid fine-tuning approaches** (Jiang et al., 2025; Yang et al., 2025): Combining LoRA with RAG demonstrates synergistic benefits, achieving high accuracy with modest computational requirements.

4. **Ontology-assisted generation** (Song et al., 2024): Structured domain knowledge can guide LLMs toward physically plausible and code-compliant designs.

5. **Multimodal interfaces** (Fernandes et al., 2024): Voice and text interaction modes enhance accessibility and enable hands-free operation in design studios.

### 5.6 Limitations of Current Approaches

Several limitations warrant attention:

1. **Hallucination risk**: LLMs can generate plausible but incorrect simulation inputs, particularly for edge cases or unusual building types.
2. **Lack of physical constraints**: Without explicit physics-based checking, LLMs may produce thermodynamically impossible configurations.
3. **Limited explainability**: Users may struggle to understand why an LLM made specific modeling choices, hindering learning and trust.
4. **Computational cost**: Fine-tuning and RAG approaches require significant computational resources and curated datasets.
5. **Reproducibility concerns**: Many papers lack sufficient implementation detail for independent replication.

---

## 6. Future Directions and Recommendations

### 6.1 Research Priorities

Based on the identified gaps and emerging trends, we recommend the following research priorities:

**1. Rigorous Validation Frameworks**

The field urgently needs standardized benchmarks for evaluating LLM-driven simulation systems. These should include:

- Reference datasets of building descriptions paired with expert-generated simulation models
- Metrics for assessing model accuracy, completeness, and physical plausibility
- Protocols for comparing simulation results against measured building performance data
- Error taxonomies characterizing failure modes

**2. Robustness and Generalization Studies**

Current demonstrations focus on relatively simple cases. Research should systematically evaluate:

- Performance across building typologies (residential, commercial, industrial, institutional)
- Scalability to large, complex buildings with hundreds of zones
- Handling of edge cases and unusual design features
- Robustness to ambiguous or incomplete input descriptions

**3. Human-AI Collaboration Models**

Rather than full automation, future systems should support collaborative workflows where LLMs augment human expertise. Research directions include:

- Interactive disambiguation of ambiguous specifications
- Explanation generation for modeling decisions
- Iterative refinement through conversational feedback
- Expert-in-the-loop validation and correction

**4. Multi-Tool Integration**

Professional workflows span multiple tools. Research should address:

- Seamless data exchange between BIM, simulation, and visualization tools
- Coordinated multi-agent systems that orchestrate tool chains
- Version control and change propagation across tool ecosystems
- Integration with optimization and decision support systems

**5. Domain-Specific Fine-Tuning at Scale**

While several papers demonstrate fine-tuning, systematic investigation is needed:

- Optimal training dataset composition and size
- Transfer learning across building types and climates
- Continual learning to incorporate new building technologies and codes
- Comparative evaluation of fine-tuning methods (full fine-tuning, LoRA, prefix tuning)

### 6.2 Practical Recommendations for Practitioners

For researchers and developers building LLM-driven simulation systems:

1. **Start with prompt engineering**: Before investing in fine-tuning, exhaust prompt engineering possibilities, including few-shot examples and chain-of-thought prompting.

2. **Implement multi-stage validation**: Use LLM-generated outputs as drafts requiring validation through physics-based checks, code compliance verification, and expert review.

3. **Leverage existing APIs**: Prioritize simulation engines with robust Python APIs (EnergyPlus, OpenStudio) to simplify integration.

4. **Adopt agentic architectures**: Decompose complex workflows into specialized agents with clear responsibilities and interfaces.

5. **Ground in domain knowledge**: Use RAG or ontology-assisted approaches to reduce hallucination and ensure code compliance.

6. **Prioritize explainability**: Generate natural language explanations of modeling decisions to support user understanding and trust.

7. **Contribute to open ecosystems**: Share agent implementations, prompt templates, and validation datasets to accelerate community progress.

### 6.3 Policy and Education Implications

The democratization of building energy modeling through LLMs has broader implications:

**For Education:**
- Curricula should balance LLM tool use with fundamental building physics understanding
- Students need critical evaluation skills to assess LLM-generated models
- Hands-on experience with both traditional and LLM-assisted workflows is essential

**For Professional Practice:**
- Professional standards and liability frameworks must adapt to AI-assisted workflows
- Quality assurance protocols should explicitly address LLM-generated content
- Continuing education should cover LLM capabilities, limitations, and best practices

**For Policy:**
- Building codes and standards may need revision to accommodate AI-assisted compliance checking
- Energy performance certification processes should clarify the role of LLM-generated models
- Data sharing policies should balance open science with intellectual property concerns

---

## 7. Conclusion

The integration of Agentic AI and Large Language Models into Building Performance Simulation workflows has progressed remarkably rapidly in 2024-2025. The reviewed literature demonstrates feasibility across multiple application domains—automated model generation, multi-agent workflow orchestration, and conversational BIM interfaces—using diverse methodological approaches including prompt engineering, fine-tuning, RAG, and agentic architectures.

Key achievements include demonstrated error-free EnergyPlus model generation (Zhang et al., 2024), 94% success rates for BIM query execution (Fernandes et al., 2024), and emerging infrastructure for standardization and interoperability (Han et al., 2025; Zhang et al., 2025). The field shows clear methodological maturation, with 2025 publications increasingly adopting sophisticated hybrid approaches combining multiple techniques.

However, significant challenges remain. The validation gap is the most critical concern: rigorous quantitative evaluation is rare, and most papers present proof-of-concept demonstrations without systematic benchmarking. Integration challenges, scalability questions, and concerns about hallucination and physical plausibility require sustained research attention.

Looking forward, the field must prioritize validation frameworks, robustness studies, and human-AI collaboration models. The promise of democratizing building energy modeling is real, but realizing it responsibly requires careful attention to quality assurance, explainability, and professional standards. As LLM capabilities continue to advance and domain-specific datasets grow, we anticipate rapid progress toward production-ready systems that fundamentally transform how buildings are designed, analyzed, and optimized for energy performance.

The convergence of AI and building science represents not merely a technological advance but a potential paradigm shift in sustainable building practice. By lowering barriers to sophisticated energy analysis, LLM-driven tools can accelerate the transition to high-performance, low-carbon buildings at the scale and speed demanded by climate imperatives.

---

## References

Elsayed, M., et al. (2025). User-friendly AI-driven automation for rapid building energy model generation. *Energy and Buildings*, 116092. https://doi.org/10.1016/j.enbuild.2025.116092

Fernandes, D., et al. (2024). A GPT-Powered Assistant for Real-Time Interaction with Building Information Models. *Buildings*, 14(8), 2499. https://doi.org/10.3390/buildings14082499

Forth, K., & Borrmann, A. (2024). Semantic enrichment for BIM-based building energy performance simulations using semantic textual similarity and fine-tuning multilingual LLM. *Journal of Building Engineering*, 110312. https://doi.org/10.1016/j.jobe.2024.110312

Han, L., et al. (2025). EnergyPlus-MCP: A model-context-protocol server for ai-driven building energy modeling. *SoftwareX*, 102367. https://doi.org/10.1016/j.softx.2025.102367

Hong, T., et al. (2025). AI for building energy modeling: A transformation. *Building Simulation*. https://doi.org/10.1007/s12273-025-1329-4

Jiang, G., et al. (2024). Eplus-Llm: A Large Language Model-Based Computing Platform for Automated Building Energy Modeling. https://doi.org/10.2139/ssrn.4743437

Jiang, G., et al. (2025). Efficient fine-tuning of large language models for automated building energy modeling in complex cases. *Automation in Construction*, 106223. https://doi.org/10.1016/j.autcon.2025.106223

Jiang, G., et al. (2025). Prompt engineering to inform large language model in automated building energy modeling. *Energy*, 134548. https://doi.org/10.1016/j.energy.2025.134548

Khadka, S. (2024). Scaling Data Driven Building Energy Modeling Using Large Language Models: Prompt Engineering and Agentic Workflow.

Lu, J., et al. (2024). Automated building energy modeling for energy retrofits using a large language model-based multi-agent framework.

Ma, Z., Chen, J., et al. (2024). EPlus-LLM: A large language model-based computing platform for automated building energy modeling. *Applied Energy*, 123431. https://doi.org/10.1016/j.apenergy.2024.123431

Rende, G., et al. (2025). Negotiating Comfort: Simulating Personality-Driven LLM Agents in Shared Residential Social Networks. *arXiv preprint*. https://doi.org/10.48550/arxiv.2507.09657

Song, J., & Yoon, S. (2024). Ontology-assisted GPT-based building performance simulation and assessment: Implementation of multizone airflow simulation. *Energy and Buildings*, 114983. https://doi.org/10.1016/j.enbuild.2024.114983

Yang, Y., et al. (2025). Research on intelligent generation of structural demolition suggestions based on multi-model collaboration. *arXiv preprint*. https://doi.org/10.48550/arxiv.2508.15820

Zhan, X., et al. (2025). Leveraging large language models to enhance urban building energy modeling: A case study. https://doi.org/10.5194/icuc12-542

Zhang, L., et al. (2024). Advancing Building Energy Modeling with Large Language Models: Exploration and Case Studies. *arXiv preprint*. https://doi.org/10.48550/arxiv.2402.09579

Zhang, L., et al. (2024). Automatic building energy model development and debugging using large language models agentic workflow. https://doi.org/10.2139/ssrn.4864703

Zhang, L., et al. (2025). Large language model-based agent Schema and library for automated building energy analysis and modeling. *Automation in Construction*, 106244. https://doi.org/10.1016/j.autcon.2025.106244

Zhao, K., et al. (2024). Text-To-EnergyPlus: Translating Natural Language into Building Energy Simulation.

Zhong, X., et al. (2024). EnergAI: A Large Language Model-Driven Generative Design Method for Early-Stage Building Energy Optimization.
