## TL;DR

LLMs and agentic systems (2024–2025) are being used to automate EnergyPlus model generation, orchestrate multi-agent simulation workflows, and enable conversational BIM interactions. Reported demonstrations include error-free EnergyPlus model generation and a 94% success rate for Revit query execution.

----

## EnergyPlus automation platforms

This section groups papers that build end-to-end automation around EnergyPlus or translate natural language to EnergyPlus models, demonstrating code generation, API control, and fine-tuning approaches. The table summarizes each paper’s scope, method, engines, main capabilities, and any reported validation.

| Paper and year | Application or use case | Methodology used | Simulation engine(s) controlled or integrated | Key findings or capabilities demonstrated | Reported metrics or validation |
|---|---|---:|---|---|---|
| EPlus-LLM 2024 — Z. Ma, J. Chen et al. [1] | Translate natural-language building descriptions into EnergyPlus models and automate simulation calls | Fine-tuned large language model for direct translation and API-driven automation [1] | EnergyPlus [1] | Fine-tuned LLM can translate NL descriptions to EnergyPlus inputs and invoke simulation APIs to automate workflows [1] | insufficient evidence |
| Text‑To‑EnergyPlus 2024 — K. Zhao et al. [2] | Natural language to EnergyPlus model generation via a knowledge-grounded agentic workflow | Knowledge-grounded agentic workflow and LLM actors for stepwise model synthesis and verification [2] | EnergyPlus [2] | Demonstrates design of an agentic pipeline that breaks down NL requests and assembles EnergyPlus models with knowledge grounding [2] | insufficient evidence |
| Automatic BEM development and debugging 2024 — L. Zhang et al. [3] | Auto-development and automated debugging of building energy models from descriptions | LLM planning and agentic workflow to generate and debug models programmatically [3] | EnergyPlus (targeted) [3] | Presents a generic LLM-planning workflow that generates error‑free EnergyPlus building models and performs debugging steps [3] | Reported generation of error‑free EnergyPlus models in demonstrated cases [3] |

----

## Agentic and multi-agent simulation workflows

This section covers multi-agent or agent-schema efforts where LLM-based agents orchestrate modeling, retrofit analysis, or library sharing for automated BEM tasks. Each paper demonstrates agent decomposition, orchestration, or agent libraries tied to simulation workflows.

| Paper and year | Application or use case | Methodology used | Simulation engine(s) controlled or integrated | Key findings or capabilities demonstrated | Reported metrics or validation |
|---|---|---:|---|---|---|
| Automated BEM for retrofits 2024 — J. Lu et al. [4] | Automated energy modeling for retrofit analysis using role-based agents | GPT‑4 based multi-agent framework built for staged workflow orchestration [4] | OpenStudio SDK with EnergyPlus modeling engine via API access [4] | Agents assigned distinct roles (data extraction, modeling, checking) and use OpenStudio to construct EnergyPlus-compatible simulations [4] | insufficient evidence beyond demonstration; system built on GPT‑4 [4] |
| LLM agent schema and library 2025 — L. Zhang et al. [5] | Standardized schema and reusable LLM agent library for automated building energy analysis | Agent schema design and open-source library to share LLM agents and workflows [5] | insufficient evidence for a single engine (library aims to be general) [5] | Introduces a schema to standardize LLM agent behavior and provides an open GitHub repository for reuse and sharing of agents [5] | insufficient evidence |
| Text‑to‑model agentic pipelines (case studies) 2024 — S. Khadka [featured work] [2] | Scaling data‑driven BEM using prompt engineering and agentic pipelines | Prompt engineering combined with agentic workflow decomposition for model generation [2] | EnergyPlus referenced as target in examples [2] | Shows how agentic LLM workflows can decompose complex modeling tasks into error‑reducing steps using prompts and subagents [2] | insufficient evidence |

----

## BIM integration and conversational interfaces

This section focuses on LLM integration with BIM systems and semantic enrichment approaches that enable querying, updating, or enriching BIM data for simulation preparation. Papers demonstrate API-level integrations, semantic-textual similarity, and ontology-assisted simulation control.

| Paper and year | Application or use case | Methodology used | Simulation engine(s) controlled or integrated | Key findings or capabilities demonstrated | Reported metrics or validation |
|---|---|---:|---|---|---|
| DAVE GPT assistant for BIM 2024 — D. Fernandes et al. [6] | Real-time multimodal interactions for querying and updating Revit BIM models | GPT-driven assistant integrating OpenAI API with Revit API and Python automation [6] | Autodesk Revit via Revit API (BIM environment) [6] | Prototype enables conversational updates/queries in Revit; demonstrated real‑time model management and multimodal (voice/text) commands [6] | 94% success rate for accurately processing and executing single‑function user queries in prototype tests [6] |
| Semantic enrichment for BIM 2024 — K. Forth, A. Borrmann [7] | Enrich missing BIM attributes for energy performance simulations using textual similarity and LLM fine-tuning | Semantic textual similarity and fine‑tuned multilingual LLM to map/extract missing BIM metadata [7] | BIM outputs intended to feed BEM workflows; specific simulation engine not specified [7] | Improves BIM semantic completeness by matching model elements to external databases and enriching missing properties via fine‑tuned LLMs [7] | insufficient evidence |
| Ontology‑assisted GPT multizone airflow 2024 — J. Song, S. Yoon [8] | Use GPT and ontologies to implement multizone airflow simulation workflows | Ontology-guided prompts combined with GPT for BPS task orchestration and simulation setup [8] | Building performance simulation tools for multizone airflow (implementation demonstrated) [8] | Demonstrates integration of ontologies with LLMs to assist multizone airflow simulation setup and assessment [8] | insufficient evidence |

----

## Infrastructure, tooling, and prompt engineering guidance

This section highlights supporting infrastructure (servers, APIs) and methodological guidance on prompts, RAG, and fine‑tuning for robust automated BEM workflows. These works present servers, best‑practice guidance, and tool prototypes for LLM-driven simulation control.

| Paper and year | Application or use case | Methodology used | Simulation engine(s) controlled or integrated | Key findings or capabilities demonstrated | Reported metrics or validation |
|---|---|---:|---|---|---|
| EnergyPlus‑MCP server 2025 — L. Han et al. [9] | Model‑context‑protocol server enabling conversational LLM interactions with EnergyPlus | Server architecture that mediates LLM↔EnergyPlus via structured model/context/protocol interfaces [9] | EnergyPlus via server-mediated API access [9] | Provides an MCP server to standardize LLM interactions with EnergyPlus and streamline conversational workflows for simulation control [9] | insufficient evidence |
| Prompt engineering for ABEM 2025 — G. Jiang et al. [10] | Practical guidelines to improve ABEM using LLMs through prompts and training strategies | Prompt engineering, retrieval-augmented generation (RAG), and fine‑tuning recommendations for ABEM workflows [10] | General ABEM workflows (EnergyPlus examples discussed) [10] | Offers practical prompt design and workflow recommendations to enhance ABEM performance and reduce engineering effort [10] | insufficient evidence |
| User‑friendly AI automation 2025 — M. Elsayed et al. [11] | Rapid automation of EnergyPlus and Radiance modeling using pretrained LLMs | Pretrained LLM translation of NL descriptions to simulation inputs for EnergyPlus and Radiance automation [11] | EnergyPlus and Radiance [11] | Prototype automates energy and daylight modeling tasks from natural language descriptions using pre-trained LLMs [11] | insufficient evidence |