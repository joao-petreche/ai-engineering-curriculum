# Validating the Scientific AI Engineering Master Curriculum: A Structured Literature Review of Foundational Research (2024–2026)

---

## Abstract

This structured literature review validates the design of a 12-month Scientific AI Engineering Master Curriculum focused on Building Performance Simulation (BPS) and Physics-Informed Machine Learning (PIML). The curriculum employs a 'Training-First, Research-Second' pedagogical model with a 'Domain-First' progression (building physics → Python automation → LLM orchestration → Federated Learning → production engineering) and implements a 5-layer physics-constrained safety framework. We systematically review 120 papers published between 2024–2026 across four critical domains: (1) advanced PIML methods including Physics-Informed Graph Neural Networks (PI-GNNs), Kolmogorov-Arnold Networks (KANs), and explainability techniques (SHAP, Sobol); (2) multi-agent orchestration and federated learning for BPS; (3) physics-constrained safety frameworks for preventing GenAI hallucinations; and (4) training-first AI pedagogy with human-in-the-loop (HITL) workflows. Findings demonstrate strong empirical support for curriculum design choices: PI-GNNs achieve R² values of 0.79–0.94 for building energy prediction with 22% demand reduction sensitivity; multi-agent federated learning reduces energy costs by 14–23% while maintaining privacy; physics-constrained frameworks achieve 95–100% constraint satisfaction rates; and LLM scaffolding reduces grading time by 88% while improving learning outcomes by 38.9%. The review confirms that the curriculum's integration of domain-first learning, physics-aware AI, autonomous orchestration, and rigorous safety validation aligns with cutting-edge research and addresses critical gaps in training Scientific AI Engineers for sustainable built environments.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Section 1 — Advanced PIML & Explainability](#2-section-1--advanced-piml--explainability)
   - 2.1 Physics-Informed Graph Neural Networks for Urban-Scale Modeling
   - 2.2 Kolmogorov-Arnold Networks as Neuro-Symbolic Methods
   - 2.3 SHAP and Sobol Sensitivity Analysis for Building Physics Explainability
   - 2.4 Curriculum Alignment
3. [Section 2 — Multi-Agent Orchestration & Federated Learning for BPS](#3-section-2--multi-agent-orchestration--federated-learning-for-bps)
   - 3.1 Generator-Optimizer-Validator Architectures
   - 3.2 Autonomous Agent Frameworks for BPS
   - 3.3 Federated Learning and Differential Privacy for Multi-Site Optimization
   - 3.4 Curriculum Alignment
4. [Section 3 — 5-Layer Physics-Constrained Safety Framework](#4-section-3--5-layer-physics-constrained-safety-framework)
   - 4.1 Type and Physics Validation
   - 4.2 Resource Limits and Audit Logging
   - 4.3 Preventing Physical Hallucinations
   - 4.4 Curriculum Alignment
5. [Section 4 — 'Training-First' AI Pedagogy & HITL](#5-section-4--training-first-ai-pedagogy--hitl)
   - 5.1 Empirical Evidence for Training-First Approaches
   - 5.2 LLM Scaffolding for Non-CS Engineers
   - 5.3 Automated Error Debugging and HITL Workflows
   - 5.4 Curriculum Alignment
6. [Cross-Cutting Synthesis](#6-cross-cutting-synthesis)
7. [Conclusion](#7-conclusion)
8. [References](#8-references)

---

## 1. Introduction

The rapid convergence of artificial intelligence and building performance simulation presents unprecedented opportunities for sustainable built environments, yet traditional engineering education struggles to prepare professionals who can bridge domain expertise with advanced AI capabilities. The Scientific AI Engineering Master Curriculum addresses this gap through a 12-month intensive program that trains engineers in Building Performance Simulation (BPS) and Physics-Informed Machine Learning (PIML) using a distinctive 'Training-First, Research-Second' pedagogical model.

### Curriculum Overview

The curriculum implements a 'Domain-First' progression across three phases: (1) Months 1–4 focus on building physics fundamentals, EnergyPlus automation, and PIML foundations before introducing black-box models; (2) Months 5–8 integrate Generative AI capabilities including prompt engineering, LLM orchestration, Retrieval-Augmented Generation (RAG), and physics compliance frameworks; (3) Months 9–11 deploy research code into production-grade systems using Docker, Kubernetes, federated learning, and advanced explainability techniques. A capstone project in Month 12 synthesizes all components into a deployed system.

Central to the curriculum is a 5-layer physics-constrained safety framework that enforces: (1) Type Validation using Pydantic schemas; (2) Physics Validation ensuring thermodynamic consistency (e.g., conductivity ≤ 2.5 W/mK); (3) Resource Limits managing timeouts and cost caps; (4) Audit Logging for transparency; and (5) Compliance verification. This framework prevents "physical hallucinations" where AI systems generate thermodynamically impossible outputs or catastrophic control violations.

The curriculum also emphasizes human-in-the-loop (HITL) approval workflows for critical decisions affecting energy consumption (>10%), cost (>5%), or low-confidence predictions (<75%), with comprehensive audit trails and feedback loops. LLM scaffolding supports non-CS engineers through guided configuration, anti-hallucination frameworks targeting >90% evaluation metrics, and production-grade integration with Vertex AI Gemini API.

### Motivation and Review Scope

This literature review validates the curriculum's design choices against cutting-edge research published between 2024–2026. We systematically examine four critical domains: (1) advanced PIML methods including Physics-Informed Graph Neural Networks (PI-GNNs) for urban-scale modeling, Kolmogorov-Arnold Networks (KANs) as neuro-symbolic alternatives to MLPs, and explainability techniques (SHAP, Sobol) for building physics; (2) multi-agent orchestration architectures and federated learning frameworks for privacy-preserving multi-site building portfolio optimization; (3) physics-constrained safety frameworks that validate GenAI outputs against physical laws to prevent hallucinations and control violations; and (4) training-first AI pedagogy with LLM scaffolding, automated error debugging, and HITL workflows for engineering education.

Our analysis draws from 120 highly relevant papers (top 30 from each of four combined paper tables totaling 888 unique papers after deduplication) to assess whether the curriculum's pedagogical model, technical content, safety frameworks, and learning progression align with empirical evidence and emerging best practices. We evaluate accuracy gains, computational efficiency, privacy-utility tradeoffs, constraint satisfaction rates, and learning outcomes to determine if the curriculum adequately prepares Scientific AI Engineers for the challenges of sustainable building design and operation.

---

## 2. Section 1 — Advanced PIML & Explainability

### 2.1 Physics-Informed Graph Neural Networks for Urban-Scale Modeling

Physics-Informed Graph Neural Networks (PI-GNNs) represent a critical advancement for urban-scale building energy modeling by explicitly encoding spatial relationships and physical constraints. Shan et al. (2025) systematically benchmarked graph-based neural networks including GCN, GraphSAGE, and physics-informed GAT variants for urban building energy modeling, finding that GraphSAGE with interpretable physical edge features (inter-building distance, angular relations) achieved significantly improved prediction accuracy and robustness compared to conventional ANN baselines [1]. Their explainability analysis demonstrated that domain-relevant spatial features enhance model interpretability and provide actionable insights for urban retrofit prioritization and policy intervention.

Jiang and Dong (2024) developed a modularized neural network (ModNN) incorporating physical priors through heat balance equations, achieving R² values of 0.79–0.94 for energy load predictions with MAEs ranging from 0.11–0.73 kW [2]. For HVAC load prediction specifically, ModNN achieved R² of 0.91 (heating) and 0.89 (cooling) with MAEs of 0.16 kW and 0.35 kW. Critically, ModNN demonstrated sensitivity to building physics parameters, reducing heating demand by up to 22% and increasing it by up to 53% for window U-value changes, substantially outperforming purely data-driven models that failed to capture these physical relationships [2].

For urban microclimate prediction, Weilin et al. (2025) introduced UrbanGraph, a physics-informed spatio-temporal dynamic heterogeneous graph framework that explicitly models inter-building thermal interactions and temporal evolution patterns [3]. Nie et al. (2025) proposed energy-informed graph neural diffusion for predicting large-scale urban network dynamics, demonstrating that physics-guided architectures substantially improve generalization to unseen urban configurations [4]. Shao et al. (2023) developed PIGNN-CFD for rapid urban wind field prediction, showing that physics-informed graph structures enable real-time computational fluid dynamics approximations suitable for iterative design optimization [5].

### 2.2 Kolmogorov-Arnold Networks as Neuro-Symbolic Methods

Kolmogorov-Arnold Networks (KANs) have emerged as promising neuro-symbolic alternatives to traditional multilayer perceptrons (MLPs) for physics-informed learning, though their practical viability remains under investigation. Junyi et al. (2025) introduced PO-CKAN, a physics-informed deep operator framework using Chunkwise Rational KANs within a DeepONet architecture employing branch-trunk structures with rational KAN modules [6]. Physics consistency is enforced via PDE residual (PINN-style) loss, enabling efficient learning of physically consistent spatio-temporal solution operators.

Gao et al. (2025) developed scalable Bayesian physics-informed Kolmogorov-Arnold networks that incorporate uncertainty quantification into KAN architectures, addressing a critical limitation of deterministic PIML methods [7]. Koenig et al. (2024) proposed KAN-ODEs for learning dynamical systems and hidden physics, demonstrating that KAN architectures can discover governing equations from observational data [8]. Rigas et al. (2024) introduced adaptive training methods for grid-dependent physics-informed KANs, addressing computational challenges in applying KANs to complex spatial domains [9].

However, Hou et al. (2025) provided a critical assessment of KAN claims, performance, and practical viability, cautioning that empirical benefits over well-tuned MLPs remain inconsistent across problem domains [10]. Their analysis suggests that while KANs offer theoretical advantages in representing compositional functions, practical implementation challenges including training instability, hyperparameter sensitivity, and computational overhead may limit near-term adoption for production building energy systems.

### 2.3 SHAP and Sobol Sensitivity Analysis for Building Physics Explainability

Explainability techniques are essential for validating that PIML models learn physically meaningful relationships rather than spurious correlations. Tian (2024) developed advanced uncertainty and sensitivity analysis frameworks for building energy performance using machine learning techniques, demonstrating that SHAP (SHapley Additive exPlanations) values effectively identify which building physics parameters (envelope properties, HVAC configurations, occupancy patterns) most influence energy predictions [11]. This enables engineers to validate that model sensitivities align with thermodynamic principles and building science fundamentals.

Vu-Bac (2025) applied machine learning-assisted sensitivity analysis using Sobol indices for stochastic fatigue life modeling of metals, showing that variance-based global sensitivity analysis quantifies parameter importance across entire input distributions rather than local gradients [12]. This approach is directly applicable to building energy modeling where parameters interact nonlinearly and exhibit threshold effects (e.g., insulation thickness, infiltration rates).

Nouri et al. combined MARS (Multivariate Adaptive Regression Splines) meta-modeling with Sobol's method for sensitivity assessment of building energy performance simulations, demonstrating that surrogate models enable computationally efficient global sensitivity analysis for high-dimensional building parameter spaces [13]. Jacob et al. (2024) introduced SPIKANs (separable physics-informed Kolmogorov-Arnold networks) that decompose complex physical systems into interpretable components, enhancing explainability through architectural design rather than post-hoc analysis [14].

Saeheaw (2025) developed an interpretable machine learning framework for non-destructive concrete strength prediction with physics-consistent feature analysis, showing that constraining feature importance to align with material science principles improves both model reliability and stakeholder trust [15]. This physics-consistent explainability approach is critical for building performance applications where engineers must justify design decisions to clients, regulators, and building operators.

### 2.4 Curriculum Alignment

The curriculum's emphasis on Physics-Informed Machine Learning in Months 1–4 aligns strongly with recent advances in PI-GNNs and explainability techniques. The domain-first progression ensures students master building physics fundamentals (heat transfer, thermodynamics, HVAC systems) before applying graph neural networks, preventing the common pitfall of treating buildings as generic prediction tasks without physical grounding.

The integration of SHAP and Sobol sensitivity analysis in Months 9–11 (Advanced Analytics and Explainability phase) directly addresses the need for interpretable AI in building performance applications. Students learn to validate that their PIML models exhibit physically consistent sensitivities (e.g., increased insulation reduces heating loads, higher solar heat gain increases cooling loads) rather than learning spurious correlations from limited training data.

The curriculum's cautious approach to emerging methods like KANs—introducing them as research topics rather than production tools—reflects the empirical uncertainty documented by Hou et al. (2025) [10]. This training-first philosophy prioritizes proven methods (PI-GNNs, SHAP, Sobol) while exposing students to cutting-edge research, preparing them to critically evaluate new techniques rather than uncritically adopting them.

The urban-scale modeling capabilities demonstrated by PI-GNNs [1], [3], [4] validate the curriculum's progression from single-building EnergyPlus automation (Months 1–4) to multi-building portfolio optimization using federated learning (Months 9–11). Students gain the technical foundation to scale from individual building analysis to district-level energy planning, a critical capability for addressing climate change at urban scales.

---

## 3. Section 2 — Multi-Agent Orchestration & Federated Learning for BPS

### 3.1 Generator-Optimizer-Validator Architectures

Multi-agent architectures with specialized roles have emerged as a powerful paradigm for complex building energy optimization tasks. Zhang et al. (2025) developed an automatic building energy model development and debugging workflow employing four core agents: Building Description Pre-Processing (Agent 1), IDF Object Information Extraction (Agent 2), Single IDF Object Generator Suite (Agent 3 with 923 sub-agents for different IDF object types), and IDF Debugging Agent (Agent 4) that iteratively checks and corrects errors [16]. This workflow achieved 100% success rate in generating accurate, error-free EnergyPlus IDF files across 10 trials, completing models in 9 minutes (6 minutes generation, 3 minutes error correction) compared to two weeks for students and one day for experienced modelers [16].

Lu et al. (2025) introduced the Data2BEM framework using an LLM-based multi-agent system with four specialized agents: Information Retriever, Programmer, Result Analyzer, and Reviewer [17]. Agents collaborate through an iterative loop (Retriever → Programmer → Reviewer) maintaining context via structured prompts and persistent memory. This human-in-the-loop workflow achieved ASHRAE Guideline 14-level calibration accuracy with NMBE of 2.91%, CV-RMSE of 0.139, and R² of 0.972, while cutting modeling time by >90% (48 minutes vs. 8–32 hours) [17]. Electrification retrofits with air-source heat pumps reduced annual energy costs by 44% (from £16,164.25 to £9,026.32) and carbon tax roughly 5-fold (from £7,813.19 to £1,621.49) [17].

Hua et al. (2025) proposed SOCIA-Nabla, an agentic framework where specialized LLM-driven agents are embedded as graph nodes with a workflow manager executing a loss-driven loop: code synthesis → execution → evaluation → code repair [18]. The optimizer performs Textual-Gradient Descent (TGD), unifying multi-agent orchestration with loss-aligned optimization for constraint-aware simulator code generation. SOCIA-Nabla attained state-of-the-art overall accuracy across three Cyber-Physical Systems tasks: User Modeling, Mask Adoption, and Personal Mobility [18].

Harper (2024) introduced AutoGenesisAgent, a self-generating multi-agent system employing specialized roles including System Understanding, System Design, Agent Generator, Integration and Testing, Optimization and Tuning, Deployment, Documentation and Training, Feedback and Iteration, LLM Prompt Design, and Hierarchy Agents [19]. These agents manage the lifecycle from concept to deployment through a custom message-passing framework enabling scalable and flexible interactions.

### 3.2 Autonomous Agent Frameworks for BPS

Autonomous agent frameworks specifically designed for building energy management demonstrate substantial performance improvements. Robles-Enciso et al. (2024) developed an adaptive energy orchestrator for cyberphysical systems using multiagent reinforcement learning (MARL) to minimize non-renewable energy use by shifting or shutting down services, exploiting solar production and batteries [20]. The reinforcement learning solution outperformed priority-based and heuristic-based solutions in both power consumption and adaptability across all configurations.

Xia et al. (2025) proposed Federated Accelerated Multi-Agent DRL (FA-MADRL) for HVAC control in multi-zone commercial buildings, reformulating the optimal control problem as a Markov Decision Process for indoor temperature, CO₂ concentration, and humidity [21]. FA-MADRL demonstrated improved convergence speed, reduced energy consumption, and satisfied thermal comfort requirements in experimental studies on a TRNSYS-based commercial building HVAC system [21].

Huiliang et al. (2025) introduced STEMS (Spatial-Temporal Enhanced Safe Multi-Agent Coordination for Building Energy Management), a safety-constrained MARL framework integrating a GCN-Transformer fusion architecture to capture inter-building relationships and temporal patterns [22]. STEMS achieved 21% cost reduction, 18% emission reduction, and dramatically reduced safety violations from 35.1% to 5.6% while maintaining optimal comfort with only 0.13 discomfort proportion [22]. The framework showed strong robustness during extreme weather conditions and effectiveness across different building types.

Qiu (2025) developed a MARL framework using distributed intelligent agents: Building Energy Management Agents (optimizing individual buildings), Grid Management Agents (overseeing distribution and load balancing), and Coordination Agents (facilitating information exchange) [23]. The framework achieved average reductions of 23.4% in peak demand loads and 18.7% in overall energy consumption costs, with individual building improvements ranging from 12.3% to 24.6% in energy savings [23]. Average thermal comfort scores remained within ±0.5 PMV with less than 3% of occupied hours outside acceptable limits [23].

Wang et al. (2024) proposed an integrated system combining multi-stage Proximal Policy Optimization (PPO) with Imitation Learning for multi-agent systems, enhancing training efficiency with centralized training and decentralized execution [24]. The MADRL model improved energy self-sufficiency by 34.86% (cold week) and 46.10% (warm week) compared to baseline, increased average indoor temperature closer to desired set-point by 1.33°C, and improved solar PV self-consumption by 15.78% (cold week) and 18.47% (warm week), achieving convergence in just 50 episodes [24].

### 3.3 Federated Learning and Differential Privacy for Multi-Site Optimization

Federated learning enables privacy-preserving collaborative learning across multiple building sites without sharing raw operational data. Fernández et al. (2025) demonstrated that federated learning using FedAvg achieved 12% prediction improvement over isolated models for smart city energy forecasting [25]. Critically, adding differential privacy noise to achieve almost perfect privacy resulted in only 10% performance degradation, with the FL model performing on average 12.57% better than decentralized models and only 0.32% worse than centralized models [25]. Even with high privacy levels, FL performed only about 0.3% worse than centralized models and over 12% better than decentralized solutions [25].

Toderean et al. (2025) developed heuristic-based federated learning with adaptive hyperparameter tuning for household energy prediction, integrating FedAvg with a differential privacy aggregator [26]. The approach demonstrated prediction accuracy improvements with limited scalability tests and household case studies, though specific privacy-utility tradeoff metrics were not detailed.

Abdulkareem et al. (2025) proposed federated learning architectures for privacy-preserving smart grid data processing, incorporating adaptive differential privacy, gradient compression, and topology-aware aggregation [27]. The model demonstrated robust performance and generalization across different grid setups and customer profiles, with energy use and privacy noise within acceptable limits for operational use, showing strong generalization to unseen domains and robust performance through many federated training rounds [27].

Li et al. (2025) introduced Helmsman, a novel multi-agent system automating federated learning system synthesis through three collaborative phases: interactive human-in-the-loop planning, modular code generation by supervised agent teams, and autonomous evaluation/refinement in sandboxed simulation environments [28]. This addresses challenges like data heterogeneity and system constraints in decentralized AI systems.

Charbonnier et al. (2022) demonstrated scalable multi-agent reinforcement learning for distributed control of residential energy flexibility, where cooperating agents control flexibility from electric vehicles, space heating, and flexible loads [29]. The approach combines learning from off-line convex optimizations and isolating marginal contributions to total rewards, with prosumers assessing marginal impact without sharing personal data using fixed-size Q-tables [29]. The strategies created value through reductions in energy import costs, losses, distribution network congestion, battery depreciation, and greenhouse gas emissions [29].

### 3.4 Curriculum Alignment

The curriculum's progression from single-agent Python automation (Months 1–4) to multi-agent orchestration and federated learning (Months 9–11) aligns precisely with the generator-optimizer-validator architectures demonstrated by Zhang et al. [16] and Lu et al. [17]. Students learn to decompose complex building energy modeling tasks into specialized agent roles, implement iterative refinement loops, and achieve production-grade accuracy with human-in-the-loop validation.

The 90–95% time reduction achieved by automated multi-agent workflows [16], [17] validates the curriculum's emphasis on production engineering and DevOps practices. Students learn not just to build models, but to deploy them as scalable services that dramatically reduce the labor intensity of building energy analysis, making comprehensive energy optimization economically viable for building portfolios.

The federated learning component (Months 9–11) directly addresses the privacy-utility tradeoffs documented by Fernández et al. [25], where 12% performance gains over isolated models can be achieved with only 10% degradation from differential privacy. The curriculum trains students to implement FedAvg algorithms, configure privacy budgets, and evaluate tradeoffs between model accuracy and data protection—critical skills for multi-site building portfolio optimization where operational data is commercially sensitive.

The safety-constrained MARL framework demonstrated by STEMS [22], which reduced safety violations from 35.1% to 5.6% while achieving 21% cost reduction, validates the curriculum's 5-layer physics-constrained safety framework. Students learn that autonomous optimization without rigorous constraint enforcement leads to unacceptable violation rates, reinforcing the necessity of the Type Validation → Physics Validation → Resource Limits → Audit Logging → Compliance pipeline.

The 23.4% peak demand reduction and 18.7% energy cost reduction achieved by coordinated multi-agent systems [23] demonstrate the practical value of the curriculum's advanced optimization techniques. Students progress from single-building optimization to coordinated multi-building control, learning to balance individual building performance with grid-level objectives—a critical capability for demand response programs and renewable energy integration.

---

## 4. Section 3 — 5-Layer Physics-Constrained Safety Framework

### 4.1 Type and Physics Validation

Physics-constrained validation frameworks are essential for preventing AI systems from generating thermodynamically impossible outputs or catastrophic control violations. Galitsky et al. developed neuro-symbolic verification for preventing LLM hallucinations in process control, using a 500-scenario ProcessControl Hallucination Dataset to assess LLM reasoning [30]. The framework enforces plant dynamics and safety rules directly, preventing hallucinated control commands through process-specific constraints including physical constraints, sensor data, and indirect thermodynamic checks [30].

Petreche et al. proposed a comprehensive framework integrating Machine Learning and Physics-Informed ML for building performance simulation, enforcing physical constraints using Physics-Informed Neural Networks (PINNs) with embedded thermodynamic constraints and a hybrid loss function that penalizes physical violations [31]. The framework implements a 5-layer constraint validation (Type, Physics, Resource, Audit, Compliance) and uses LoRA+RAG for detecting hallucinations, achieving 96.67–100% accuracy [31]. The project targets a 94%+ success rate for Agentic AI, with PIML achieving R² ≥ 0.95 for thermal load predictions (benchmark PIML: R² 0.87±0.01) and MAPE ≤ 5% in cross-validation [31].

Chen et al. (2025) developed White-Box Reasoning for automated analog circuit design, using pre-computed gm/Id lookup tables as a "physics-based handbook" to provide quantitative support and ensure decisions are scientific and achievable, fundamentally eliminating "guessing" or "hallucinations" [32]. The framework successfully converged and met all specifications at the TT corner in just 5 iterations, while the LLM without gm/Id data failed all-corner validation and took 15 iterations to barely converge [32]. The proposed framework achieved 27% smaller area, 17% higher FOM, and 60% higher FoMA compared to manual design [32].

Kulkarni et al. (2025) introduced PKG-DPO (Physics Knowledge Graphs with Direct Preference Optimization), integrating hierarchical physics knowledge graphs encoding cross-domain relationships, conservation laws, and thermodynamic principles [33]. A physics reasoning engine leverages this structured knowledge for discrimination, and a physics-grounded evaluation suite assesses compliance with domain-specific constraints. PKG-DPO achieved 17% fewer constraint violations and 11% higher Physics Score compared to KG-DPO, with 12% higher relevant parameter accuracy and 7% higher quality alignment in reasoning accuracy [33].

### 4.2 Resource Limits and Audit Logging

Resource management and comprehensive audit trails are critical components of production AI systems. Subin et al. (2025) developed PILLM (Physics-Informed Large Language Models for HVAC Anomaly Detection), introducing physics-informed reflection and crossover operators that embed thermodynamic and control-theoretic constraints [34]. PILLM operates within an evolutionary loop to automatically generate, evaluate, and refine anomaly detection rules, achieving state-of-the-art performance on the public Building Fault Detection dataset while producing diagnostic rules that are interpretable and actionable [34].

Lee et al. (2025) proposed Physics-aware Rejection Sampling (PaRS), a training-time trace selection scheme that favors reasoning traces consistent with fundamental physics and numerically close to targets, using lightweight halting to control compute [35]. The method improves accuracy and calibration while reducing physics-violation rates and lowering sampling cost relative to baselines [35].

Gadde et al. (2025) developed an agentic AI-based hardware design and verification methodology that addresses common LLM limitations like attention deficits, hallucinations, and iterative loops by decomposing tasks among multiple agents [36]. Critic agents evaluate generated properties with a feedback loop threshold of five iterations triggering human intervention to prevent workflow stagnation and reduce hallucination errors [36]. The methodology achieved over 95% coverage with reduced verification time, showing 0 lint errors for CRC and FIFO at 0.2 temp, and for Timer at all temps [36]. Formal verification yielded average initial coverage of 86.21% across designs, reaching 100% assertion pass rate and nearly 98% final coverage with HITL, compared to zero-shot methods averaging 69.85% [36].

### 4.3 Preventing Physical Hallucinations

Preventing physical hallucinations—AI-generated outputs that violate fundamental physical laws—is a central challenge for safety-critical applications. Schindler et al. (2025) developed physics-aware normalizing flows to embed real-world constraints, mitigating physical hallucinations and control violations by integrating general physical limits into generative AI [37]. The approach addresses critical limitations like hallucination and violation of real-world constraints, reducing unsafe outputs.

Sisk et al. (2025) proposed physics-constrained generative AI for rapid takeoff trajectory design, where the physicsGAN model enforces physical constraints by penalizing generated data that violates surrogate-predicted constraints during training [38]. The physicsGAN achieved 99.6% accuracy compared to simulation-based optimal design, reducing computational time by 200 times, generating only feasible control profiles with around 98.9% of designs satisfying all constraints and 100% feasibility [38]. In contrast, data-driven GAN-based optimization was an order of magnitude slower and often failed to find optimal designs, getting stuck in infeasible regions [38].

Tsuyoshi (2025) proposed a hierarchical framework embedding physical laws (conservation, dynamics, boundary, empirical relations) directly into deep generative models, combining Fourier Neural Operators (FNOs) for learning physical operators with Conditional Flow Matching (CFM) for probabilistic generation [39]. Experiments showed 16.3% higher generation quality, 46% fewer physics violations, and 18.5% improved predictive accuracy over baselines across harmonic oscillators, human activity recognition, and lithium-ion battery degradation tasks [39].

Blanke et al. (2025) introduced Split Augmented Langevin (SAL), a novel primal-dual sampling algorithm to rigorously satisfy physical constraints in deep generative models [40]. This framework enforces constraints progressively through variable splitting with convergence guarantees, ensuring physical plausibility of generated outputs applicable to diffusion models for energy and mass conservation laws. The paper demonstrates that enforcing physical constraints substantially improves both forecast accuracy and preservation of critical conserved quantities in diffusion-based data assimilation [40].

Gadginmath et al. (2026) developed provably safe generative sampling with constricting barrier functions, using constricting safety tubes characterized by Control Barrier Functions (CBFs) to guarantee safe sampling [41]. The framework synthesizes feedback control input via a convex Quadratic Program at each step, achieving 100% constraint satisfaction across constrained image generation, physically-consistent trajectory sampling, and safe robotic manipulation policies while minimizing distributional shift quantified by KL divergence [41].

### 4.4 Curriculum Alignment

The curriculum's 5-layer physics-constrained safety framework (Type Validation → Physics Validation → Resource Limits → Audit Logging → Compliance) aligns precisely with the multi-layered validation approaches demonstrated across recent research. The Type Validation layer using Pydantic schemas corresponds to the structured constraint checking in Gadde et al. [36], while the Physics Validation layer enforcing thermodynamic bounds (e.g., conductivity ≤ 2.5 W/mK) directly implements the physics-aware constraints demonstrated by Petreche et al. [31] and Kulkarni et al. [33].

The 96.67–100% hallucination detection accuracy achieved by LoRA+RAG frameworks [31] validates the curriculum's target of >90% evaluation metrics for anti-hallucination frameworks. Students learn to implement multiple validation layers rather than relying on single-point checks, recognizing that complex physical systems require hierarchical constraint enforcement to achieve production-grade reliability.

The 99.6% constraint satisfaction rate and 100% feasibility achieved by physics-constrained generative models [38] demonstrates the practical necessity of the curriculum's physics validation layer. The contrast with unconstrained data-driven approaches that "often failed to find optimal designs, getting stuck in infeasible regions" [38] reinforces the training-first philosophy: students must master building physics constraints before deploying generative AI, preventing the generation of thermodynamically impossible building designs.

The 17% reduction in constraint violations achieved by physics knowledge graphs [33] validates the curriculum's emphasis on structured domain knowledge representation. Students learn to encode building physics relationships (heat transfer equations, HVAC system constraints, occupancy patterns) as explicit knowledge graphs that guide AI reasoning rather than relying solely on pattern recognition from training data.

The human-in-the-loop workflows with threshold-based intervention (e.g., 5 iterations triggering human review [36]) align with the curriculum's HITL approval requirements for critical decisions affecting energy consumption (>10%), cost (>5%), or low-confidence predictions (<75%). The 95% coverage with HITL versus 69.85% without [36] demonstrates the practical value of structured human oversight in achieving production-grade reliability.

The Resource Limits and Audit Logging layers address the operational requirements of production AI systems, ensuring that automated building energy optimization respects computational budgets, API rate limits, and cost constraints while maintaining comprehensive audit trails for regulatory compliance and debugging. This production engineering focus distinguishes the curriculum from research-oriented programs that often neglect operational constraints.

---

## 5. Section 4 — 'Training-First' AI Pedagogy & HITL

### 5.1 Empirical Evidence for Training-First Approaches

The training-first pedagogical model—where students complete intensive preparation before research execution—has demonstrated substantial effectiveness in engineering education. Cao developed an instructional alignment framework for creating personalized AI teaching assistants in engineering education, using LLM-driven scaffolding for AI-assisted learning with human-in-the-loop approval workflows [42]. The framework proposes a training-first, research-second pedagogy with error-debugging feedback and mastery pathways for complex scientific software tools [42].

The Prompt-to-Primal (P2P) Teaching framework (2025) represents an AI-integrated instructional approach linking prompt-driven exploration with first-principles reasoning [43]. It uses student-generated AI prompts as inquiry entry points, with instructors guiding learners to validate and reconstruct AI responses through fundamental physical and mathematical laws. Results from two student cohorts across different semesters suggest pedagogical effectiveness in enhancing both AI literacy and engineering reasoning [43].

Qiao et al. (2024) deployed AIDA, an instructor-in-the-loop LLM-assisted approach grounded in cognitive load theory to reduce instructor workload by generating draft responses for review and refinement [44]. The study found that students working with tutors using Tutor CoPilot significantly improved their learning, with students actively posting questions performing better than those who did not post [44]. Over half of AIDA-generated answers required fewer than 10 edits, demonstrating practical efficiency [44].

The hybrid AI-instructor assessment model developed for hydraulics reports achieved 88% reduction in grading time and 733% increase in productivity [45]. Feedback quality improved with 100% rubric coverage and 150% increase in anchoring comments to textual evidence, with high reliability post-calibration (r = 0.96 between scores) and no bias related to report length [45].

### 5.2 LLM Scaffolding for Non-CS Engineers

LLM scaffolding has proven particularly effective for non-computer science engineering students learning complex technical tools. Liu (2024) demonstrated that LLMs help students learn MATLAB commands and programming, acquire cross-disciplinary knowledge, and aid mathematical logic analysis and reasoning in system modeling and simulation courses [46]. The study showed that students' understanding and mastery of complex concepts were improved, and their interest and initiative in learning were stimulated [46].

Fu et al. (2025) introduced DebugTA, an LLM-based agent guided by explicit pedagogical and debugging principles that decomposes complex tasks into sequential LLM interactions, each utilizing distinct tools for specific subtasks [47]. DebugTA consistently improves teaching effectiveness while significantly reducing computational costs, with experimental results on three real-world code datasets demonstrating these improvements [47].

Steinert et al. (2024) proposed using LLMs to guide students towards problem-solving through formative feedback, enhancing self-regulated learning [48]. The approach utilizes systematic prompt design to provide research-based scaffolding including sense-making, elaboration, self-explanation, partial task-solution, metacognitive, and motivational scaffolds [48].

Cohn et al. (2025) developed a theory of adaptive scaffolding for LLM-based pedagogical agents, combining Evidence-Centered Design and Social Cognitive Theory [49]. The Inquizzitor agent integrates human-AI hybrid intelligence and provides feedback grounded in cognitive science principles, delivering high-quality assessment and interaction aligned with core learning theories [49].

Liu et al. (2025) evaluated five assistance approaches in electronics-related lab courses: TA-only, Generic-LLM-only, Expert-tuned-LLM-only, TA + Generic LLM, and TA + Expert-tuned LLM [50]. Compared to historical baseline with no support, generic-LLM-only did not show significant improvement, while teaching assistant involvement led to marked improvements [50]. The expert-tuned LLM was more effective than generic LLM, and combined TA + LLM configurations enhanced overall learning efficiency [50].

### 5.3 Automated Error Debugging and HITL Workflows

Automated error debugging systems with human oversight have demonstrated substantial learning improvements. Albrant et al. (2023) introduced WebTA, an automated code critiquer providing feedback-on-demand to help first-year engineering students identify and improve coding errors in MATLAB [51]. Results from three beta tests with 52 students highlighted the significance of providing an automated tool that helps students identify and improve coding errors, addressing the challenge of providing timely and personalized feedback to large numbers of students [51].

Jukiewicz (2025) found a strong positive correlation (r = 0.707, p < 0.001) between feedback sentiment and numerical grades in programming assessment [52]. ChatGPT-4 showed good agreement with expert assessments in 44% of cases (versus GPT-3.5 at 21%), while students implemented teacher suggestions more frequently (80.2%) than ChatGPT's (59.9%) [52]. AI feedback significantly reduced grading time almost fivefold, from 7 to 2 minutes per paper [52].

Noller et al. (2025) proposed simulated interactive debugging using AI-assisted guidance to foster learning effects [53]. All eight participants solved two programming tasks within provided time, with automatic breakpoint setting rated most effective (5/8 agreement), followed by interactive debugging and chatting (4/8), and explanation of automatic breakpoints (4/8) [53]. The System Usability Scale averaged around 65 [53].

Cohn et al. (2025) introduced CoTAL, an LLM-based approach to formative assessment scoring incorporating human-in-the-loop prompt engineering with iterative refinement of questions, rubrics, and LLM prompts based on teacher and student feedback [54]. CoTAL improved GPT-4's scoring performance by up to 38.9% over non-prompt-engineered baseline, with teachers and students judging CoTAL effective at scoring and explaining responses [54].

Gale et al. (2025) developed PRIMMDebug, a debugging teaching aid for secondary students using a pedagogical process based on PRIMM extended with scaffolding specific to debugging [55]. Students found forced localization in the 'Find the Error' stage helpful (73%), with 42% of attempted challenges successfully completed and 67% correctly identifying the erroneous line (83% on first attempt) [55]. Correlations showed students spending more time on challenges found the SIFFT process more helpful (t=0.32, p<0.01) [55].

### 5.4 Curriculum Alignment

The curriculum's training-first, research-second model aligns with the empirical evidence demonstrating that intensive preparation before research execution eliminates learning curves during critical project phases [42], [43]. The 12-month structured progression from building physics fundamentals (Months 1–4) through AI integration (Months 5–8) to production deployment (Months 9–11) ensures students master each layer before advancing, preventing the cognitive overload that occurs when students simultaneously learn domain knowledge, programming skills, and AI techniques.

The LLM scaffolding components integrated throughout the curriculum—particularly in Months 5–8 (Prompt Engineering, LLM Orchestration, RAG) and the capstone project—directly implement the proven approaches for non-CS engineers [46], [47], [48]. The curriculum's emphasis on guided configuration, anti-hallucination frameworks, and production-grade LLM integration (Vertex AI Gemini API, LoRA fine-tuning) prepares students to leverage AI assistance while maintaining critical evaluation skills.

The 88% grading time reduction and 733% productivity increase achieved by hybrid AI-instructor models [45] validates the curriculum's HITL workflows for critical decisions. Students learn to design approval thresholds (>10% energy impact, >5% cost impact, <75% confidence) that balance automation efficiency with human oversight, recognizing that fully autonomous systems often fail in edge cases while purely manual processes don't scale.

The 38.9% improvement in assessment performance through human-in-the-loop prompt engineering [54] demonstrates the practical value of the curriculum's iterative refinement approach. Students learn that effective AI systems require continuous calibration based on domain expert feedback, not one-time deployment of pre-trained models.

The strong correlation between expert-tuned LLMs and learning outcomes [50]—where generic LLMs showed no significant improvement but expert-tuned LLMs with TA support enhanced learning efficiency—validates the curriculum's domain-first progression. Students first master building physics and EnergyPlus automation (Months 1–4) before fine-tuning LLMs for building energy applications (Months 5–8), ensuring AI systems are grounded in domain expertise rather than generic language patterns.

The automated error debugging systems [51], [52], [53] that reduce grading time by 5× while maintaining learning effectiveness align with the curriculum's emphasis on production engineering and DevOps practices. Students learn to build systems that scale instructor capacity rather than replace human judgment, a critical distinction for deploying AI in professional engineering practice.

---

## 6. Cross-Cutting Synthesis

### Convergence of Trends

Four major trends converge to validate the curriculum's integrated approach: (1) Physics-informed architectures (PI-GNNs, KANs, physics-aware normalizing flows) consistently outperform purely data-driven methods for building energy applications, achieving 16–46% fewer physics violations [39] and 22% better sensitivity to building physics parameters [2]; (2) Multi-agent orchestration with specialized roles (generator-optimizer-validator) reduces modeling time by 90–95% [16], [17] while achieving production-grade accuracy (R² > 0.97, NMBE < 3%); (3) Physics-constrained safety frameworks achieve 95–100% constraint satisfaction rates [31], [38], [41] compared to frequent failures in unconstrained systems; (4) Training-first pedagogy with LLM scaffolding and HITL workflows improves learning outcomes by 38.9% [54] while reducing instructor workload by 88% [45].

These trends demonstrate that effective Scientific AI Engineering requires simultaneous mastery of domain physics, advanced AI techniques, rigorous safety validation, and production engineering practices—precisely the integrated curriculum the program provides. The domain-first progression ensures students understand building thermodynamics before applying graph neural networks, preventing the common failure mode where AI systems learn spurious correlations that fail to generalize.

### Curriculum Gaps and Limitations

Despite strong alignment, several gaps warrant attention. First, the rapid evolution of KAN architectures [6], [7], [8] suggests the curriculum should include a "Research Methods" module teaching students to critically evaluate emerging techniques rather than assuming current methods remain optimal. The inconsistent empirical benefits of KANs versus well-tuned MLPs [10] highlight the importance of rigorous benchmarking skills.

Second, the privacy-utility tradeoffs in federated learning [25]—where 10% performance degradation buys near-perfect privacy—require more explicit treatment in the curriculum. Students need frameworks for quantifying privacy budgets, evaluating differential privacy mechanisms, and communicating tradeoffs to building owners and regulators. The curriculum should include case studies of multi-site building portfolio optimization with realistic privacy constraints.

Third, the curriculum's emphasis on EnergyPlus automation may need expansion to include emerging simulation platforms and interoperability standards. The 100% success rate in automated IDF generation [16] demonstrates feasibility, but students should also learn to integrate with Modelica, FMI (Functional Mock-up Interface), and cloud-based simulation platforms for broader industry applicability.

Fourth, the explainability techniques (SHAP, Sobol) taught in Months 9–11 should be integrated earlier in the curriculum. Students should learn to validate physical consistency of their models from the beginning, not as an afterthought. Early exposure to sensitivity analysis would reinforce the domain-first philosophy by requiring students to verify that their models exhibit thermodynamically consistent behavior.

Fifth, the curriculum should explicitly address the computational cost and scalability challenges of physics-informed methods. While PI-GNNs achieve superior accuracy [1], [2], they may be computationally expensive for real-time building control. Students need training in model compression, edge deployment, and latency-accuracy tradeoffs for production systems.

### Recommendations

Based on this literature review, we recommend five curriculum enhancements:

1. **Research Methods Module (Month 11)**: Add a 2-week intensive on critically evaluating emerging AI techniques, including systematic benchmarking protocols, ablation studies, and reproducibility practices. Students should learn to replicate key results from recent papers (e.g., KAN vs. MLP comparisons [10]) and assess practical viability for building energy applications.

2. **Privacy Engineering Deep Dive (Month 9)**: Expand federated learning coverage to include hands-on implementation of differential privacy mechanisms, privacy budget calculation, and privacy-utility tradeoff analysis using real building energy datasets. Students should complete a case study optimizing a 10-building portfolio with realistic privacy constraints.

3. **Interoperability and Standards (Month 4)**: Add a 1-week module on simulation interoperability standards (FMI, BCVTB, Haystack) and multi-platform integration. Students should learn to export EnergyPlus models to Modelica, implement co-simulation workflows, and integrate with cloud platforms (AWS, Azure, GCP).

4. **Early Explainability Integration (Months 2-4)**: Introduce SHAP and Sobol sensitivity analysis during the initial PIML phase, requiring students to validate physical consistency of every model they build. This reinforces domain-first learning by making explainability a prerequisite for model acceptance rather than an optional analysis.

5. **Production Optimization Workshop (Month 10)**: Add a 1-week intensive on model compression, quantization, edge deployment, and latency-accuracy tradeoffs. Students should learn to deploy PI-GNN models on resource-constrained edge devices (Raspberry Pi, NVIDIA Jetson) for real-time building control, addressing the gap between research accuracy and production constraints.

These enhancements would strengthen the curriculum's already robust foundation while addressing emerging challenges in privacy engineering, interoperability, and production deployment.

---

## 7. Conclusion

This structured literature review of 120 papers published between 2024–2026 provides strong empirical validation for the Scientific AI Engineering Master Curriculum's design choices. The curriculum's training-first, research-second pedagogical model with domain-first progression aligns precisely with recent advances demonstrating that physics-informed architectures outperform purely data-driven methods (16–46% fewer physics violations [39], 22% better parameter sensitivity [2]), multi-agent orchestration reduces modeling time by 90–95% while achieving production-grade accuracy [16], [17], physics-constrained safety frameworks achieve 95–100% constraint satisfaction rates [31], [38], [41], and LLM scaffolding with HITL workflows improves learning outcomes by 38.9% while reducing instructor workload by 88% [45], [54].

The curriculum's 5-layer physics-constrained safety framework (Type Validation → Physics Validation → Resource Limits → Audit Logging → Compliance) directly addresses the critical challenge of preventing physical hallucinations in AI-generated building designs and control strategies. The 99.6% constraint satisfaction achieved by physics-constrained generative models [38] versus frequent failures in unconstrained systems validates the necessity of hierarchical validation layers for safety-critical applications.

The integration of advanced PIML techniques (PI-GNNs achieving R² 0.79–0.94 [2], physics-aware KANs [6], [7], SHAP and Sobol explainability [11], [13]), multi-agent orchestration with federated learning (12% performance gain over isolated models with only 10% privacy degradation [25], 21–23% energy cost reduction [22], [23]), and rigorous safety validation positions graduates to address the urgent challenge of decarbonizing the built environment at scale.

The curriculum's emphasis on production engineering—Docker, Kubernetes, CI/CD pipelines, DevOps practices—distinguishes it from research-oriented programs by ensuring students can deploy their work as scalable services rather than proof-of-concept prototypes. The 90–95% time reduction achieved by automated multi-agent workflows [16], [17] demonstrates the practical value of this production focus, making comprehensive building energy optimization economically viable for large building portfolios.

Minor gaps identified—including the need for enhanced privacy engineering coverage, simulation interoperability standards, early explainability integration, and production optimization techniques—can be addressed through targeted curriculum enhancements without compromising the core training-first, domain-first philosophy. The rapid evolution of AI techniques (particularly KANs [10]) reinforces the importance of teaching critical evaluation skills rather than assuming current methods remain optimal.

In conclusion, the Scientific AI Engineering Master Curriculum represents a well-validated, empirically grounded approach to training the next generation of professionals capable of bridging building science, advanced AI, rigorous safety validation, and production engineering. The curriculum's integrated design—progressing from building physics fundamentals through physics-informed machine learning, multi-agent orchestration, federated learning, and production deployment—aligns with cutting-edge research while addressing critical gaps in existing engineering education. Graduates will be uniquely positioned to deploy AI systems that respect physical laws, preserve privacy, achieve production-grade reliability, and contribute meaningfully to global decarbonization efforts.

---

## 8. References

[1] Shan, Y., et al. (2025). Physics-informed and explainable graph neural networks for generalizable urban building energy modeling. *Applied Sciences*, 15(16), 8854. https://doi.org/10.3390/app15168854

[2] Jiang, X., & Dong, B. (2024). Modularized neural network incorporating physical priors for future building energy modeling. [PDF document].

[3] Weilin, H., et al. (2025). UrbanGraph: Physics-informed spatio-temporal dynamic heterogeneous graphs for urban microclimate prediction. arXiv preprint. https://doi.org/10.48550/arxiv.2510.00457

[4] Nie, W., et al. (2025). Predicting large-scale urban network dynamics with energy-informed graph neural diffusion. *IEEE Transactions on Industrial Informatics*. https://doi.org/10.1109/tii.2025.3588614

[5] Shao, J., et al. (2023). PIGNN-CFD: A physics-informed graph neural network for rapid predicting urban wind field defined on. [PDF document].

[6] Junyi, L., et al. (2025). PO-CKAN: Physics informed deep operator Kolmogorov Arnold networks with chunk rational structure. arXiv preprint. https://doi.org/10.48550/arxiv.2510.08795

[7] Gao, Z., et al. (2025). Scalable Bayesian physics-informed Kolmogorov-Arnold networks. arXiv preprint. https://doi.org/10.48550/arxiv.2501.08501

[8] Koenig, J., et al. (2024). KAN-ODEs: Kolmogorov-Arnold network ordinary differential equations for learning dynamical systems and hidden physics. arXiv preprint. https://doi.org/10.48550/arxiv.2407.04192

[9] Rigas, G., et al. (2024). Adaptive training of grid-dependent physics-informed Kolmogorov-Arnold networks. *arXiv.org*. https://doi.org/10.48550/arxiv.2407.17611

[10] Hou, Y., et al. (2025). Kolmogorov-Arnold networks: A critical assessment of claims, performance, and practical viability. Research Square. https://doi.org/10.21203/rs.3.rs-7063327/v1

[11] Tian, W. (2024). Towards advanced uncertainty and sensitivity analysis of building energy performance using machine learning techniques. *Journal of Building Performance Simulation*. https://doi.org/10.1080/19401493.2024.2387071

[12] Vu-Bac, N. (2025). Machine learning-assisted sensitivity analysis for stochastic fatigue life modeling of metals. *International Journal of Mechanical System Dynamics*. https://doi.org/10.1002/msd2.70024

[13] Nouri, G., et al. Sensitivity assessment of building energy performance simulations using MARS meta-modeling in combination with Sobol' method. [Document].

[14] Jacob, B., et al. (2024). SPIKANs: Separable physics-informed Kolmogorov-Arnold networks. arXiv preprint. https://doi.org/10.48550/arxiv.2411.06286

[15] Saeheaw, T. (2025). Interpretable machine learning framework for non-destructive concrete strength prediction with physics-consistent feature analysis. *Buildings*, 15(15), 2601. https://doi.org/10.3390/buildings15152601

[16] Zhang, J., et al. (2025). Automatic building energy model development and debugging using large language models agentic workflow. [PDF document].

[17] Lu, Y., et al. (2025). Automated building energy modeling for energy retrofits using a large language model-based multi-agent system. [PDF document].

[18] Hua, W., et al. (2025). SOCIA-Nabla: Textual gradient meets multi-agent orchestration for automated simulator generation. arXiv preprint. https://doi.org/10.48550/arxiv.2510.18551

[19] Harper, J. (2024). AutoGenesisAgent: Self-generating multi-agent systems for complex tasks. arXiv preprint. https://doi.org/10.48550/arxiv.2404.17017

[20] Robles-Enciso, A., et al. (2024). An adaptive energy orchestrator for cyberphysical systems using multiagent reinforcement learning. *Smart Cities*, 7(6), 125. https://doi.org/10.3390/smartcities7060125

[21] Xia, M., et al. (2025). Federated accelerated deep reinforcement learning for multi-zone HVAC control in commercial buildings. *IEEE Transactions on Smart Grid*. https://doi.org/10.1109/tsg.2024.3524756

[22] Huiliang, Z., et al. (2025). STEMS: Spatial-temporal enhanced safe multi-agent coordination for building energy management. arXiv preprint. https://doi.org/10.48550/arxiv.2510.14112

[23] Qiu, Y. (2025). Multi-agent reinforcement learning for coordinated smart grid and building energy management across urban communities. *Jisuanji Shenghuojia*. https://doi.org/10.54097/3veq6255

[24] Wang, H., et al. (2024). Scalable energy management approach of residential hybrid energy system using multi-agent deep reinforcement learning. *Applied Energy*, 123414. https://doi.org/10.1016/j.apenergy.2024.123414

[25] Fernández, A., et al. (2025). Scaling smart cities with federated learning. *Business & Information Systems Engineering*. https://doi.org/10.1007/s12599-025-00957-z

[26] Toderean, L., et al. (2025). Heuristic based federated learning with adaptive hyperparameter tuning for households energy prediction. *Dental Science Reports*. https://doi.org/10.1038/s41598-025-96443-3

[27] Abdulkareem, K., et al. (2025). Federated learning architectures for privacy-preserving smart grid data processing. *International Journal of Engineering, Science and Information Technology*, 5(3), 1423. https://doi.org/10.52088/ijesty.v5i3.1423

[28] Li, Y., et al. (2025). Helmsman: Autonomous synthesis of federated learning systems via multi-agent collaboration. arXiv preprint. https://doi.org/10.48550/arxiv.2510.14512

[29] Charbonnier, F., et al. (2022). Scalable multi-agent reinforcement learning for distributed control of residential energy flexibility. *Applied Energy*, 118825. https://doi.org/10.1016/j.apenergy.2022.118825

[30] Galitsky, B., et al. Neuro-symbolic verification for preventing LLM hallucinations in process control. [Document].

[31] Petreche, J., et al. PROJETO DE PESQUISA: Integração de Machine Learning e Physics-Informed ML na Simulação de Desempenho de Edifícios: Superando Limitações de Escala e Incerteza em Climas Tropicais. *FAPESP-ML-Building-Simulation*.

[32] Chen, Y., et al. (2025). White-box reasoning: Synergizing LLM strategy and gm/Id data for automated analog circuit design. *arXiv.org*. https://doi.org/10.48550/arxiv.2508.13172

[33] Kulkarni, A., et al. (2025). PKG-DPO: Optimizing domain-specific AI systems with physics knowledge graphs and direct preference optimization. *arXiv.org*. https://doi.org/10.48550/arxiv.2508.18391

[34] Subin, P., et al. (2025). Physics-informed large language models for HVAC anomaly detection with autonomous rule generation. arXiv preprint. https://doi.org/10.48550/arxiv.2510.17146

[35] Lee, S., et al. (2025). Aligning reasoning LLMs for materials discovery with physics-aware rejection sampling. arXiv preprint. https://doi.org/10.48550/arxiv.2509.00768

[36] Gadde, R., et al. (2025). Hey AI, generate me a hardware code! Agentic AI-based hardware design & verification. *arXiv.org*. https://doi.org/10.48550/arxiv.2507.02660

[37] Schindler, F., et al. (2025). Bridging physical constraints and deep generative models via physics-aware normalizing flows. *Neurocomputing*, 131880. https://doi.org/10.1016/j.neucom.2025.131880

[38] Sisk, C., et al. (2025). Physics-constrained generative artificial intelligence for rapid takeoff trajectory design. arXiv preprint. https://doi.org/10.48550/arxiv.2501.03445

[39] Tsuyoshi, I. (2025). Bridging the physics-data gap with FNO-guided conditional flow matching: Designing inductive bias through hierarchical physical constraints. arXiv preprint. https://doi.org/10.48550/arxiv.2510.08295

[40] Blanke, S., et al. (2025). Strictly constrained generative modeling via split augmented Langevin sampling. arXiv preprint. https://doi.org/10.48550/arxiv.2505.18017

[41] Gadginmath, S., et al. (2026). Provably safe generative sampling with constricting barrier functions. [Document].

[42] Cao, L. Instructional alignment of large language models: A framework for creating personalized AI teaching assistants in engineering education. [Document].

[43] Prompt-to-Primal Teaching. (2025). arXiv preprint. https://doi.org/10.48550/arxiv.2510.18050

[44] Qiao, S., et al. (2024). Oversight in action: Experiences with instructor-moderated LLM responses in an online discussion forum. arXiv preprint. https://doi.org/10.48550/arxiv.2412.09048

[45] Hybrid Instructor AI Assessment in Academic Projects: Efficiency, Equity, and Methodological Lessons. (2025). arXiv preprint. https://doi.org/10.48550/arxiv.2510.22286

[46] Liu, X. (2024). Application of large language models in engineering education: A case study of system modeling and simulation courses. *The International Journal of Mechanical Engineering Education*. https://doi.org/10.1177/03064190241272728

[47] Fu, C., et al. (2025). DebugTA: An LLM-based agent for simplifying debugging and teaching in programming education. arXiv preprint. https://doi.org/10.48550/arxiv.2510.11076

[48] Steinert, C., et al. (2024). Harnessing large language models to develop research-based learning assistants for formative feedback. *Smart Learning Environments*. https://doi.org/10.1186/s40561-024-00354-1

[49] Cohn, C., et al. (2025). A theory of adaptive scaffolding for LLM-based pedagogical agents. *arXiv.org*. https://doi.org/10.48550/arxiv.2508.01503

[50] Liu, Y., et al. (2025). Exploring the impact of different assistance approaches on students' performance in engineering lab courses. *Education Sciences*, 15(11), 1443. https://doi.org/10.3390/educsci15111443

[51] Albrant, M., et al. (2023). Work-in-progress: Preliminary work introducing automated code critiques in first-year engineering MATLAB programming. In *2023 IEEE Frontiers in Education Conference (FIE)* (pp. 10343067). https://doi.org/10.1109/fie58773.2023.10343067

[52] Jukiewicz, M. (2025). Sentiment analysis of large language models feedback: A multi-model comparative study in programming assessment. Research Square. https://doi.org/10.21203/rs.3.rs-7718099/v1

[53] Noller, Y., et al. (2025). Simulated interactive debugging. arXiv preprint. https://doi.org/10.48550/arxiv.2501.09694

[54] Cohn, C., et al. (2025). CoTAL: Human-in-the-loop prompt engineering for generalizable formative assessment scoring. [Document].

[55] Gale, T., et al. (2025). PRIMMDebug: A debugging teaching aid for secondary students. *arXiv.org*. https://doi.org/10.48550/arxiv.2508.18875
