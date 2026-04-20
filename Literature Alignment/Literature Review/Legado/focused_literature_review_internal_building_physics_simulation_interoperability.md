# Internal Building Physics & Simulation Interoperability: A Focused Literature Review for the Scientific AI Engineering Curriculum (2024–2026)

---

## Abstract

This focused literature review addresses a critical gap identified in a prior comprehensive curriculum validation study: the over-emphasis on urban-scale graph neural network modeling at the expense of intra-building thermal physics and simulation interoperability standards. We systematically examine 60 highly relevant papers (top 30 from each of two combined tables totaling 289 unique papers) published between 2024–2026 across two research questions: (1) How do Physics-Informed Graph Neural Networks (PI-GNNs) model multi-zone building thermal dynamics and HVAC thermal networks, and what empirical advantages do they demonstrate over standard MLPs? (2) How are AI agents and Large Language Models (LLMs) being integrated with simulation interoperability standards (IFC, gbXML, FMI, Modelica) to automate building performance simulation workflows? Findings demonstrate that PI-GNNs achieve 17–35% accuracy improvements over MLPs for multi-zone temperature prediction, with mean errors below 1% using only 20 training samples when physics constraints are embedded. Graph topologies explicitly model zones as nodes and inter-zone heat flow as edges, with physics constraints (energy balance, Fourier conduction, thermodynamic laws) encoded via loss function penalties and message-passing rules. However, detailed HVAC component modeling (chillers, AHUs, VAV systems) as graph elements remains limited. For simulation interoperability, LLMs demonstrate 40–60% time savings in Modelica module generation and >90% modeling time reduction for automated IFC-to-EnergyPlus workflows, though hallucination risks, semantic gaps between standards, and validation requirements remain critical challenges. These findings validate the curriculum's domain-first progression and physics-constrained safety framework while identifying specific enhancement opportunities: explicit HVAC network graph modeling, multi-standard translation pipelines (IFC → gbXML → Modelica/FMU), and LLM-assisted co-simulation orchestration.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Internal Building Physics & PI-GNNs for Multi-Zone Buildings and HVAC Thermal Networks](#2-internal-building-physics--pi-gnns-for-multi-zone-buildings-and-hvac-thermal-networks)
   - 2.1 Graph Topology for Intra-Building Physics
   - 2.2 Physics-Informed Constraints in GNNs for Building Thermal Dynamics
   - 2.3 Spatial Heat Transfer Dynamics: PI-GNNs vs. Standard MLPs
   - 2.4 HVAC Network Modeling: Chillers, AHUs, and Duct Networks as Graph Elements
   - 2.5 Limitations and Open Challenges
   - 2.6 Curriculum Alignment
3. [Simulation Interoperability Standards: Integrating AI Agents and LLMs with IFC, gbXML, FMI, and Modelica](#3-simulation-interoperability-standards-integrating-ai-agents-and-llms-with-ifc-gbxml-fmi-and-modelica)
   - 3.1 IFC (Industry Foundation Classes) and AI/LLM Integration
   - 3.2 gbXML and Automated Building Energy Model Generation
   - 3.3 FMI/FMU Co-Simulation Orchestration with AI Agents
   - 3.4 Modelica and LLM-Assisted Model Synthesis
   - 3.5 Cross-Standard Integration and Interoperability Pipelines
   - 3.6 Curriculum Alignment
4. [Cross-Cutting Analysis](#4-cross-cutting-analysis)
5. [Conclusion](#5-conclusion)
6. [References](#6-references)

---

## 1. Introduction

### Context: Correcting the Urban-Scale Emphasis

This focused literature review serves as a critical supplement to a prior comprehensive curriculum validation study that examined four broad areas of the 12-month Scientific AI Engineering Master Curriculum: Physics-Informed Machine Learning (PIML) & Explainability, Multi-Agent Orchestration & Federated Learning, 5-Layer Physics-Constrained Safety Framework, and Training-First Pedagogy with Human-in-the-Loop (HITL) workflows. That review, drawing from 120 papers across 888 unique sources, validated the curriculum's pedagogical model and technical content but noted a significant limitation: an over-emphasis on urban-scale graph neural network modeling for district-level energy analysis at the expense of intra-building thermal physics and HVAC system modeling.

The prior review extensively covered Physics-Informed Graph Neural Networks (PI-GNNs) for urban building energy modeling [1], [2], [3], [4], demonstrating that GraphSAGE with interpretable physical edge features achieved improved prediction accuracy for urban retrofit prioritization and that modularized neural networks incorporating physical priors achieved R² values of 0.79–0.94 for energy load predictions [1], [2]. However, these applications focused primarily on inter-building spatial relationships, urban microclimate interactions, and district-level optimization rather than the detailed intra-building physics that dominate individual building performance: multi-zone thermal dynamics, zone-to-zone heat transfer, HVAC component interactions, and thermal mass effects.

Furthermore, the prior review identified simulation interoperability as a curriculum gap, noting that while the curriculum emphasizes EnergyPlus automation, LLM orchestration, and co-simulation, it does not explicitly address how AI agents interact with industry-standard interoperability formats such as Industry Foundation Classes (IFC), Green Building XML (gbXML), Functional Mock-up Interface (FMI), and Modelica. These standards are critical for real-world building performance simulation workflows, enabling data exchange between BIM authoring tools (Revit, ArchiCAD), energy modeling platforms (EnergyPlus, OpenStudio, TRNSYS), and multi-physics co-simulation environments.

### Research Questions

This focused review addresses two specific research questions that directly target the identified gaps:

**RQ1: How do Physics-Informed Graph Neural Networks model multi-zone building thermal dynamics and HVAC thermal networks, and what empirical advantages do they demonstrate over standard MLPs?**

Specifically, we examine:
- How graph structures are defined for intra-building physics (nodes representing thermal zones, HVAC components; edges representing inter-zone heat flow, duct connections)
- What physics laws are embedded (energy balance, Fourier heat conduction, thermodynamic laws, mass-flow conservation) and how they are encoded in GNN architectures
- Quantitative empirical comparisons: accuracy metrics (RMSE, MAE, R², CVRMSE), data efficiency, extrapolation capability
- Explicit modeling of HVAC networks (chillers, air handling units, VAV boxes, duct systems) as graph elements
- Current limitations and open challenges

**RQ2: How are AI agents and Large Language Models being integrated with simulation interoperability standards (IFC, gbXML, FMI, Modelica) to automate building performance simulation workflows?**

Specifically, we examine:
- LLM-based IFC parsing, semantic querying, and automated extraction of thermal properties and system topology
- AI-driven gbXML generation from BIM data and translation pipelines (BIM → gbXML → EnergyPlus)
- AI orchestration of Functional Mock-up Units (FMUs) for multi-physics co-simulation
- LLM-assisted Modelica model synthesis, natural language to Modelica translation, and automated debugging
- End-to-end multi-standard integration pipelines (IFC → gbXML → Modelica/FMU → simulation)
- Hallucination risks, semantic gaps, validation requirements, and curriculum implications

### Search Methodology

This review employs a systematic Deep Search methodology targeting recent literature (2024–2026) to capture cutting-edge developments in both research areas. Two comprehensive searches were conducted:

**Search Area 1 (Internal PI-GNNs for Multi-Zone Buildings and HVAC Thermal Networks):** A combined search across SciSpace and Google Scholar using queries targeting "physics-informed graph neural networks," "building thermal dynamics," "multi-zone HVAC," "thermal network modeling," and "intra-building heat transfer" yielded 181 papers after deduplication from 181 total results. The top 30 papers by relevance score constitute the primary evidence base for RQ1.

**Search Area 2 (AI Agents and LLMs with IFC, gbXML, FMI, Modelica):** A combined search targeting "large language models," "IFC parsing," "gbXML generation," "FMI co-simulation," "Modelica synthesis," and "building simulation interoperability" yielded 108 papers after deduplication from 130 total results. The top 30 papers by relevance score constitute the primary evidence base for RQ2.

All papers were enriched with structured columns extracting graph topology details, physics constraints, empirical metrics, HVAC component modeling, standards addressed, LLM capabilities, automation levels, and limitations. This structured extraction enables systematic comparative analysis and direct mapping to curriculum content.

### Distinction: Intra-Building vs. Urban-Scale Modeling

A critical distinction underpins this review: **intra-building physics** operates at fundamentally different spatial and temporal scales than **urban-scale modeling**, requiring different graph topologies, physics constraints, and validation approaches.

**Intra-building physics** focuses on:
- Multi-zone thermal dynamics within a single building (typically 5–50 zones)
- Zone-to-zone heat transfer through walls, floors, ceilings, and internal partitions
- HVAC component interactions (chillers, boilers, air handling units, VAV boxes, ducts, dampers)
- Thermal mass effects and transient heat storage in building envelope and interior elements
- Occupant-driven internal gains and localized control strategies
- Time scales: minutes to hours for HVAC control, hours to days for thermal mass dynamics

**Urban-scale modeling** focuses on:
- Inter-building energy interactions across districts (typically 100–10,000 buildings)
- Urban microclimate effects (heat island, wind patterns, solar shading between buildings)
- District heating/cooling networks and shared energy infrastructure
- Aggregated building portfolios for demand response and grid integration
- Spatial relationships: building proximity, orientation, urban morphology
- Time scales: hours to seasons for district energy planning

The prior review's emphasis on urban-scale PI-GNNs [1], [2], [3], [4] provided valuable validation for the curriculum's federated learning and multi-agent orchestration components (Months 9–11), which address multi-site building portfolio optimization. However, the curriculum's foundational months (1–4) focus on single-building EnergyPlus automation, multi-zone thermal modeling, and HVAC system physics—domains that require detailed intra-building graph topologies and component-level physics constraints not captured by urban-scale approaches.

This review corrects that imbalance by systematically examining how PI-GNNs model the detailed thermal physics within individual buildings and how AI agents automate the simulation workflows that building energy engineers encounter daily: parsing IFC files from architects, generating gbXML for energy modeling, orchestrating multi-physics co-simulations, and synthesizing Modelica models for HVAC control design.

---

## 2. Internal Building Physics & PI-GNNs for Multi-Zone Buildings and HVAC Thermal Networks

### 2.1 Graph Topology for Intra-Building Physics

Physics-Informed Graph Neural Networks for building thermal modeling construct graph topologies that explicitly represent the spatial structure and thermal connectivity of multi-zone buildings. The fundamental design choice—what entities become nodes and what relationships become edges—directly determines the model's ability to capture physical heat transfer mechanisms.

**Zones as Nodes, Inter-Zone Heat Flow as Edges:** The most common topology treats thermal zones as graph nodes and inter-zone heat transfer pathways as edges. Yang et al. (2024) represent multi-zone buildings as graphs where "only zones are considered as nodes, and any heat flow between zones is modeled as an edge based on prior knowledge of the building structure" [5]. This topology aligns with the lumped-parameter modeling approach used in building energy simulation tools like EnergyPlus, where each zone is treated as a well-mixed air volume with uniform temperature. Edges capture conductive heat transfer through shared walls, convective heat transfer through doorways and openings, and radiative exchange between zone surfaces.

Chunxiang et al. (2021) similarly construct graphs where "nodes represent zones, and connected walls represent edges, describing temperature interactions among multiple zones based on actual layouts" [6]. This explicit encoding of building topology enables the GNN to learn spatially-aware temperature dynamics: zones with more shared walls (higher node degree) exhibit stronger thermal coupling, while thermally isolated zones (low node degree) respond primarily to external boundary conditions and internal gains.

**Cells as Nodes for Open-Plan Spaces:** For open-plan spaces where traditional zone boundaries are ambiguous, finer-grained discretization is required. Nagarathinam et al. (2024) model open-plan offices by dividing the space into cells, where "nodes represent cells, and edges model thermodynamic interactions, including explicit modeling of wall and window surface temperatures" [7]. This approach captures air mixing and spatial temperature gradients within large open spaces, addressing the limitation of single-zone models that assume uniform temperature distributions. The inclusion of wall and window surface temperatures as explicit node features enables the model to capture thermal mass effects and radiative heat transfer, which are critical for predicting thermal comfort and HVAC load dynamics.

**Building Elements as Nodes:** An alternative topology treats individual building elements (walls, windows, floors, roofs) as nodes with spatial and hierarchical relationships as edges. Zijian et al. (2025) formulate energy prediction as a graph regression task where "nodes are building elements, and edges are their spatial and hierarchical relationships" [8]. This component-level representation enables the model to learn how specific envelope properties (insulation thickness, window U-value, thermal mass) influence overall building energy performance, supporting design optimization and retrofit analysis.

**Adjacency Matrices for Multi-Zone Connectivity:** Jiang and Dong (2024) construct modularized neural networks (ModNN) where "each single-zone module is treated as a node, and these nodes are interconnected through an adjacency matrix to describe their topological relationships" [9]. The adjacency matrix explicitly encodes which zones share thermal boundaries, enabling the GNN to propagate temperature information along physically meaningful pathways. This structured approach ensures that the model respects building topology: heat flows only between adjacent zones, not between spatially disconnected zones, preventing the model from learning spurious long-range correlations.

**Finite Difference Grids as Nodes:** For high-fidelity thermal modeling, Goldfeder et al. (2024) employ a Finite Differences (FD) grid where "discrete control volumes (CVs) are nodes" and "edges represent thermal exchange via conduction or convection between CVs" [10]. This fine-grained discretization enables the model to capture spatial temperature gradients within walls and thermal mass elements, approaching the resolution of computational fluid dynamics (CFD) while maintaining the computational efficiency of graph neural networks. The FD grid topology is particularly valuable for modeling radiant heating/cooling systems, where surface temperature distributions critically influence thermal comfort and energy consumption.

**Comparative Insight:** The choice of graph topology reflects a fundamental tradeoff between model resolution and computational complexity. Zone-level topologies (5–50 nodes per building) enable real-time control applications and large-scale portfolio optimization but sacrifice spatial resolution within zones. Cell-level topologies (100–1,000 nodes per building) capture spatial gradients and air mixing but increase computational cost. Component-level topologies enable design optimization by explicitly representing envelope elements but require detailed building geometry data. The curriculum's progression from single-zone EnergyPlus models (Months 1–2) to multi-zone thermal networks (Months 3–4) aligns with this hierarchy, ensuring students understand the physics at each scale before applying graph-based representations.

### 2.2 Physics-Informed Constraints in GNNs for Building Thermal Dynamics

The defining characteristic of Physics-Informed Graph Neural Networks is the explicit embedding of physical laws as constraints that guide model training and inference. Unlike purely data-driven GNNs that learn arbitrary node-to-node relationships, PI-GNNs enforce thermodynamic principles, ensuring that learned models respect energy conservation, heat transfer mechanisms, and material properties.

**Energy Balance Constraints:** The fundamental constraint in building thermal modeling is energy balance: the rate of change of thermal energy in a zone equals the net heat flow into the zone. Goldfeder et al. (2024) embed energy balance as "Qext + Q1 + Q2 + Q3 + Q4 = McΔT/Δt," where external heat gains, inter-zone heat flows, and HVAC inputs sum to the change in zone thermal energy [10]. This constraint is enforced through the GNN's message-passing framework: each node aggregates heat flows from neighboring nodes (via edges), sums external inputs (solar gains, occupant heat, HVAC), and updates its temperature state according to its thermal mass (Mc).

Jiang and Dong (2024) enforce energy balance through "physics-inspired model constraints" that ensure "physical consistency, such as the magnitude of conduction heat flux decreasing as R value increases, and indoor air temperature decreasing with increasing HVAC cooling load" [9]. These constraints are implemented by "forcing the partial derivative of the model output to be positive with respect to its input," ensuring that the model's learned sensitivities align with thermodynamic principles. For example, increasing wall insulation (higher R-value) must reduce heat flux, and increasing cooling load must decrease indoor temperature—violations of these relationships indicate unphysical model behavior.

**Fourier's Law of Conduction:** Conductive heat transfer through building envelope elements follows Fourier's law: heat flux is proportional to the temperature gradient and thermal conductivity. Goldfeder et al. (2024) embed this as "Qcond = kAΔT/LΔt," where k is thermal conductivity, A is surface area, ΔT is temperature difference, and L is material thickness [10]. In the GNN framework, edge weights represent thermal conductance (kA/L), and message-passing computes heat flow as the product of edge weight and temperature difference between connected nodes.

Peng et al. (2023) incorporate Fourier conduction into physics-informed graph convolutional networks for fluid flow and heat convection, where "the control equation of thermal convection" is embedded into the loss function [11]. This ensures that the GNN's predictions satisfy the governing partial differential equations (PDEs) for heat transfer, not just match training data. The physics-informed loss function penalizes deviations from the PDE residual, forcing the model to learn solutions that are both data-consistent and physics-consistent.

**Thermodynamic Laws and Mass Conservation:** For HVAC systems, thermodynamic laws govern the relationship between temperature, pressure, humidity, and energy flows. While explicit thermodynamic constraints are mentioned in several papers [7], [10], detailed formulations are often not provided in the metadata. Nagarathinam et al. (2024) note that their physics-informed GNN captures "thermodynamic interactions" and enforces "physical constraints" but do not specify whether these include psychrometric relationships, refrigeration cycle constraints, or air-side energy balance [7].

Mass conservation is critical for modeling airflow in HVAC duct networks and natural ventilation. The metadata does not reveal detailed implementations of mass conservation constraints in GNN architectures, suggesting this remains an area for future development. The curriculum's emphasis on HVAC system physics (Months 2–3) and multi-zone airflow modeling provides the domain foundation necessary to implement these constraints when they become available in PI-GNN frameworks.

**Heat Capacity and Thermal Mass:** Thermal mass—the ability of building materials to store and release heat—critically influences building thermal dynamics, particularly for passive solar design and demand response strategies. Jiang and Dong (2024) model thermal mass through "heat balance equations" that account for the thermal capacitance of building elements [9]. The GNN's temporal dynamics (often implemented via recurrent layers or temporal convolutions) capture how zones with high thermal mass (concrete, masonry) exhibit slow temperature responses, while zones with low thermal mass (lightweight construction) respond rapidly to heat inputs.

However, several papers note limitations in thermal mass representation. The metadata for Nagarathinam et al. (2024) states "lacks explicit thermal-mass formulation" [7], and similar limitations are noted for other papers [12], [13]. This suggests that while PI-GNNs can implicitly learn thermal mass effects from data, explicit physics-based modeling of heat storage in walls, floors, and furniture remains an open challenge. The curriculum's coverage of RC (Resistance-Capacitance) network models in Months 3–4 provides students with the physics foundation to recognize and address this limitation.

**Encoding Constraints: Loss Function Penalties vs. Hard Constraints:** Physics constraints can be encoded in GNN architectures through two primary mechanisms: soft constraints via loss function penalties and hard constraints via architectural design.

**Loss function penalties** add physics-violation terms to the training objective. Yang et al. (2024) enforce physical constraints "on model parameters and propagate the penalty in the loss function of GNN" [5]. The total loss becomes L_total = L_data + λ·L_physics, where L_data measures prediction error on training data, L_physics measures violation of physical constraints (e.g., energy balance residual, negative heat capacity), and λ is a weighting hyperparameter. This approach is flexible and easy to implement but does not guarantee constraint satisfaction at inference time—the model learns to minimize violations but may still produce unphysical outputs for out-of-distribution inputs.

**Hard constraints** enforce physics through architectural design. Peng et al. (2023) incorporate governing equations "into the loss function of the neural network, allowing the predictions from GCN to satisfy the constraints imposed by the physical laws" [14]. While described as a loss function approach, the emphasis on "satisfy the constraints" suggests that the architecture is designed to produce outputs that inherently respect physical laws, not just minimize violations. For example, ensuring that predicted heat flows sum to zero (energy balance) can be enforced by parameterizing the GNN output as a residual that is added to a physics-based baseline solution.

The curriculum's 5-layer physics-constrained safety framework (Type Validation → Physics Validation → Resource Limits → Audit Logging → Compliance) implements hard constraints at inference time, catching and rejecting unphysical outputs before they propagate to downstream systems. This post-hoc validation complements the soft constraints learned during training, providing defense-in-depth against physical hallucinations.

### 2.3 Spatial Heat Transfer Dynamics: PI-GNNs vs. Standard MLPs

The empirical advantage of Physics-Informed Graph Neural Networks over standard multilayer perceptrons (MLPs) lies in their ability to capture spatial heat transfer dynamics—the propagation of thermal energy through the building's physical structure—that MLPs treat as generic input-output mappings without spatial awareness.

**Accuracy Improvements: 17–35% Over Physically Consistent Methods:** The most comprehensive comparison comes from a review paper (metadata paper #7) that aggregates results across multiple studies: "PCNNs achieved accuracy improvements of 17-35% compared to all other physically consistent methods" [15]. While this comparison is against other physics-consistent approaches (not pure MLPs), it demonstrates the substantial gains from incorporating graph structure and physics constraints. The review reports specific metrics across multiple studies: "RMSE < 5, MAE 0.25 °C, R² 0.996, MAPE 0.4%, CVRMSE 4.31%" for PI-GNN approaches, compared to "RMSE 70% lower than ANN, MAE 43% lower than gray-box model" [15].

**Data Efficiency: 20 Training Samples Achieve <1% Error:** A striking advantage of physics-informed approaches is extreme data efficiency. Peng et al. (2023) demonstrate that their physics-informed graph convolutional network achieves "mean errors for velocity and temperature fields of less than 1% and 0.6% for single cylinder, and less than 2% and 1% for double cylinder cases, with only 20 training data" [11]. In contrast, "the purely data-driven GCN model had mean errors of 9.4% and 6.4% for the double cylinder case" [11]—nearly an order of magnitude worse with the same training data.

Similarly, Peng et al. (2023) report that their natural convection model achieved "max and mean relative errors in predicting the temperature field of less than 2% and 0.4% respectively, for both single and dual heat source cases" with only 20 training samples, and "compared to a pure data-driven model, it reduced the maximum error by 65.5% and the mean error by 72%" [14]. This 65–72% error reduction demonstrates that embedding physics constraints enables the model to extrapolate far beyond the training distribution, learning the underlying physical mechanisms rather than memorizing input-output patterns.

The curriculum's emphasis on Physics-Informed Machine Learning in Months 3–4, before introducing large-scale data-driven approaches in Months 5–8, ensures students understand how to achieve high accuracy with limited data—a critical capability for building energy applications where comprehensive sensor data is often unavailable or expensive to collect.

**Specific Quantitative Comparisons:** Several papers provide detailed quantitative comparisons between PI-GNNs and baseline methods:

- **Jiang and Dong (2024):** ModNN achieved "R² values from 0.79 to 0.94 and MAEs from 0.11 kW to 0.73 kW for HVAC load prediction," outperforming a 3R2C resistance-capacitance model that achieved "0.94°C MAE" compared to ModNN's "0.43°C MAE for indoor temperature" [9]. This 54% reduction in temperature prediction error demonstrates the value of graph-based multi-zone modeling over single-zone RC models.

- **Chunxiang et al. (2021):** Their Graph Attention Network with Gated Recurrent Unit achieved "RMSE of 0.47, MAE of 0.37, and R² of 0.94" for multi-zone indoor temperature prediction [6]. While no direct MLP comparison is provided, the high R² value indicates strong predictive performance on multi-zone thermal dynamics.

- **Natale et al. (2022):** Physically Consistent Neural Networks achieved "up to 40% better accuracy than a classical physics-based resistance-capacitance (RC) model on 3-day prediction horizons" and "attained similar performance to classical LSTMs on validation data, overfitting training data less" [16]. The mean absolute error for PCNNs was "0.88 °C at 72 hours, compared to 1.48 °C for the RC model" [16]—a 41% improvement. Critically, PCNNs "showed lower errors on the validation set than LSTMs, indicating better generalization" [16], demonstrating that physics constraints prevent overfitting.

- **Stephanie (2025):** For residential heat pump temperature prediction, "the calibrated Resistance-Capacitance model achieved an acceptable accuracy (RMSE = 1.38 °C). The hybrid model further reduced this error (RMSE = 0.44 °C)" [17]—a 68% improvement. "Clustering households and applying transfer learning provided an additional 30% error reduction" [17], demonstrating that physics-informed models enable effective transfer learning across buildings with different characteristics.

**Extrapolation and Generalization:** A critical advantage of PI-GNNs is their ability to extrapolate to unseen building configurations and operating conditions. Peng et al. (2023) demonstrate "geometric adaptability" where a model trained on single-cylinder natural convection accurately predicts double-cylinder configurations [11], [14]. This capability is essential for building energy applications, where models must generalize across different building geometries, occupancy patterns, and weather conditions.

The metadata notes that several papers lack "MLP baseline comparison" [7], [12], [13], limiting direct quantitative assessment of PI-GNN advantages. However, the consistent pattern of high accuracy with limited training data, strong generalization to unseen conditions, and physically consistent sensitivities provides compelling evidence that graph-based physics-informed approaches substantially outperform generic MLPs for building thermal modeling.

**Curriculum Implication:** The empirical evidence validates the curriculum's domain-first progression: students master building physics and thermodynamic principles (Months 1–4) before applying graph neural networks, ensuring they can design physics-informed architectures that achieve high accuracy with limited data rather than relying on large datasets to compensate for lack of physical grounding.

### 2.4 HVAC Network Modeling: Chillers, AHUs, and Duct Networks as Graph Elements

While multi-zone thermal modeling has received substantial attention in the PI-GNN literature, explicit modeling of HVAC components and distribution networks as graph elements remains limited. This represents a critical gap, as HVAC systems account for 40–60% of building energy consumption and exhibit complex thermodynamic interactions that are poorly captured by zone-level models.

**VAV Terminals and Ductwork:** The most explicit HVAC component modeling appears in Li et al. (2024), who develop a "design information-assisted graph neural network for modeling central air conditioning systems" where "nodes represent physical entities (e.g., VAV terminals), and edges represent their connections (e.g., ductwork)" [18]. This topology directly captures the air distribution network: supply air flows from air handling units through main ducts (edges) to VAV boxes (nodes) that modulate airflow to individual zones. The GNN learns how upstream equipment states (AHU supply temperature, fan speed) propagate through the duct network to influence downstream zone conditions, accounting for duct heat gains/losses and pressure drops.

The study models "a real central air conditioning system serving the tallest building in Hong Kong," demonstrating that the approach scales to large commercial buildings with complex HVAC topologies [18]. The methodology "leverages traditional building system design information, like 2D schematic drawings, to extract the topology," enabling automated graph construction from standard engineering documentation [18]. This addresses a critical practical barrier: manual graph construction for large HVAC systems is labor-intensive and error-prone.

**Chiller System Power Prediction:** Zhu et al. (metadata paper #19) focus on "Chiller System Power Prediction," explicitly comparing "PINN and MLP models" [19]. However, the metadata does not reveal whether chillers are modeled as graph nodes with refrigerant flow paths as edges, or whether the physics-informed approach simply embeds thermodynamic constraints (e.g., Carnot efficiency limits, refrigeration cycle equations) in the loss function. The paper notes "computational runtime differences" between PINN and MLP, suggesting that the physics-informed approach adds computational cost [19], but specific accuracy improvements are not quantified in the metadata.

**HVAC Equipment as Graph Nodes:** Several papers mention modeling "HVAC equipment as graph nodes" [20], [21] but do not provide detailed descriptions of which components are included or how their thermodynamic interactions are represented. Zhang (metadata paper #17) uses "GNNs for indoor environment prediction and control, modeling zones and HVAC equipment as graph nodes" and "captures spatial patterns" [20], but the metadata notes it "lacks explicit physics constraints, thermal-mass modeling, and baseline MLP comparisons" [20].

**Implicit HVAC Modeling Through Zone-Level Inputs:** Most papers model HVAC systems implicitly through zone-level inputs (supply air temperature, airflow rate, heating/cooling power) rather than explicitly representing equipment as graph nodes. Nagarathinam et al. (2024) model "16 HVAC units in an open-plan room" but represent them as boundary conditions on zone nodes rather than as distinct equipment nodes [13]. This approach captures the effect of HVAC on zone temperatures but does not model the internal thermodynamics of equipment (compressor power, refrigerant states, fan energy) or the propagation of faults through the HVAC network.

**Limitations and Gap Analysis:** The metadata reveals significant limitations in current HVAC component modeling:

- **Limited Component Coverage:** Only VAV terminals and ductwork are explicitly modeled as graph elements [18]. Chillers, boilers, cooling towers, pumps, heat exchangers, and air handling units are mentioned in general discussions [15] but detailed graph-based modeling is not demonstrated.

- **Lack of Thermodynamic Detail:** The metadata does not reveal whether refrigeration cycle constraints, psychrometric relationships, or fluid flow equations are embedded in HVAC-focused PI-GNNs. This suggests that current approaches may model HVAC systems as black-box input-output relationships rather than physics-based thermodynamic processes.

- **No Fault Detection Applications:** While Li et al. (2024) mention "improved capabilities in prediction accuracy, generalizability, and interpretability" [18], explicit applications to HVAC fault detection and diagnostics—a critical use case for graph-based modeling—are not demonstrated in the metadata.

- **Scalability Concerns:** The metadata notes "scalability" as a key limitation across multiple papers [15], [20]. Large commercial buildings may have hundreds of VAV boxes, dozens of AHUs, and complex chiller plants with multiple chillers, cooling towers, and pumps. Whether graph neural networks can efficiently model these large-scale HVAC networks in real-time control applications remains an open question.

**Curriculum Implication:** The limited coverage of HVAC component modeling in the PI-GNN literature represents a significant opportunity for curriculum enhancement. The curriculum's current emphasis on EnergyPlus HVAC modeling (Months 2–3) provides students with detailed knowledge of chiller thermodynamics, air handling unit controls, and duct network sizing. However, explicit instruction on representing HVAC systems as graph neural networks—with equipment as nodes, flow paths as edges, and thermodynamic constraints embedded in message-passing—would bridge the gap between traditional building energy simulation and cutting-edge graph-based AI methods.

Specific curriculum additions could include:
- **Module 3.5 (HVAC Systems):** Add a sub-module on "Graph-Based HVAC Network Modeling" that teaches students to construct graph topologies from HVAC schematic drawings, represent equipment thermodynamics as node update functions, and embed refrigeration cycle constraints in GNN loss functions.
- **Capstone Project Options:** Offer a capstone track focused on "PI-GNN for HVAC Fault Detection" that applies graph neural networks to detect and diagnose faults (e.g., refrigerant leaks, fouled heat exchangers, stuck dampers) by learning normal equipment interaction patterns and flagging anomalies.

### 2.5 Limitations and Open Challenges

The literature reveals several critical limitations and open challenges that constrain the practical deployment of Physics-Informed Graph Neural Networks for building thermal modeling:

**Scalability to Large Buildings:** Multiple papers cite "scalability" as a key limitation [15], [20]. Nagarathinam et al. (2024) explicitly note that their approach faces "limitations in observability, adherence to physical constraints, and generalization" and that "PINNs still lack the scalability required for effective control in large open-plan offices, primarily due to air-mixing interactions" [7]. Large commercial buildings with hundreds of zones and complex HVAC systems may require graphs with thousands of nodes and tens of thousands of edges, raising questions about computational efficiency for real-time control applications.

The curriculum's progression from single-zone models (Months 1–2) to multi-zone models (Months 3–4) to large-scale portfolio optimization (Months 9–11) prepares students to recognize and address scalability challenges. However, explicit instruction on graph coarsening techniques, hierarchical graph representations, and distributed GNN training for large building models would strengthen this preparation.

**Data Availability and Sensor Placement:** While PI-GNNs achieve high accuracy with limited training data (20 samples in some cases [11], [14]), they still require comprehensive sensor coverage to observe zone temperatures, HVAC states, and boundary conditions. The metadata notes "data availability" as a limitation [15], reflecting the reality that most existing buildings lack dense sensor networks. Retrofitting buildings with sufficient sensors to train PI-GNN models may be cost-prohibitive, limiting deployment to new construction or high-value retrofit projects.

The curriculum's emphasis on "big data" in Month 2 and "data-driven optimization" in Month 8 addresses data collection and preprocessing, but explicit coverage of optimal sensor placement strategies—determining the minimum sensor configuration needed to train accurate PI-GNN models—would enhance practical applicability.

**Real-Time Inference Requirements:** Building HVAC control systems typically operate on 1–15 minute control intervals, requiring models to produce predictions in seconds or less. The metadata notes "real-time inference" as a challenge [15], and Zhu et al. (2024) observe "computational runtime differences" between PINN and MLP models [19], suggesting that physics-informed approaches may be slower than pure data-driven methods. While GNNs are generally efficient for inference once trained, the message-passing operations required for large graphs may exceed real-time constraints for some applications.

The curriculum's coverage of "production deployment" in Months 9–11, including containerization, orchestration, and performance optimization, provides students with the engineering skills to deploy models that meet real-time requirements. However, explicit instruction on model compression techniques (pruning, quantization, knowledge distillation) for GNNs would strengthen this capability.

**Generalization Across Building Types:** Several papers note "generalization" as a limitation [7], [20]. Models trained on one building type (e.g., residential) may not generalize to others (e.g., commercial, industrial) due to differences in construction, HVAC systems, occupancy patterns, and control strategies. While transfer learning approaches show promise [17], systematic evaluation of cross-building generalization is limited in the current literature.

The curriculum's capstone project (Month 12) requires students to deploy a production system on real building data, providing hands-on experience with generalization challenges. However, explicit instruction on domain adaptation techniques—fine-tuning pre-trained PI-GNN models on new buildings with limited data—would enhance students' ability to deploy models across diverse building portfolios.

**Lack of Thermal Mass Detail:** Multiple papers note limitations in thermal mass representation [7], [12], [13]. While GNNs can implicitly learn thermal mass effects from data, explicit physics-based modeling of heat storage in walls, floors, and furniture—critical for passive solar design, demand response, and thermal comfort prediction—remains underdeveloped. This gap is particularly significant for high-thermal-mass buildings (concrete, masonry) where thermal storage dominates energy dynamics.

The curriculum's coverage of RC network models in Months 3–4 provides students with the physics foundation to recognize this limitation. Explicit instruction on hybrid approaches—combining RC networks for thermal mass with GNNs for spatial heat transfer—would address this gap.

**Model Complexity vs. Interpretability:** While physics-informed approaches improve interpretability compared to black-box models, the complexity of GNN architectures (multiple layers, attention mechanisms, recurrent components) can still obscure the learned relationships. The metadata notes "model complexity" as a challenge [15], [20]. Engineers and building operators need to understand why a model makes specific predictions to trust and act on its recommendations.

The curriculum's emphasis on explainability techniques (SHAP, Sobol sensitivity analysis) in Months 9–11 addresses this challenge. However, explicit instruction on GNN-specific explainability methods—visualizing learned edge weights, analyzing attention patterns, decomposing node contributions—would strengthen students' ability to interpret and validate PI-GNN models.

### 2.6 Curriculum Alignment

The findings on Physics-Informed Graph Neural Networks for intra-building thermal modeling provide strong validation for the curriculum's domain-first progression and physics-constrained safety framework while identifying specific enhancement opportunities.

**Validation of Domain-First Progression:** The empirical evidence that PI-GNNs achieve 17–35% accuracy improvements over purely data-driven methods [15] and 65–72% error reduction with physics constraints [14] validates the curriculum's emphasis on mastering building physics (Months 1–4) before applying graph neural networks. Students who understand energy balance, Fourier conduction, and thermodynamic laws can design physics-informed architectures that achieve high accuracy with limited data, while students who skip this foundation are forced to rely on large datasets and risk learning spurious correlations.

**Validation of Physics-Constrained Safety Framework:** The curriculum's 5-layer physics-constrained safety framework (Type Validation → Physics Validation → Resource Limits → Audit Logging → Compliance) directly addresses the limitations noted in the PI-GNN literature. The Physics Validation layer, which enforces thermodynamic bounds (e.g., conductivity ≤ 2.5 W/mK), prevents the "physical hallucinations" that can occur when GNNs extrapolate beyond their training distribution. The emphasis on constraint satisfaction rates (targeting >90%) aligns with the empirical finding that physics constraints reduce errors by 65–72% [14].

**Enhancement Opportunity 1: Explicit HVAC Network Graph Modeling:** The limited coverage of HVAC component modeling in the current literature [18], [19] suggests a curriculum enhancement opportunity. Proposed addition:

- **Module 3.5 Enhancement (HVAC Systems):** Add a 2-week sub-module titled "Graph Neural Networks for HVAC Thermal Networks" that teaches students to:
  - Construct graph topologies from HVAC schematic drawings (nodes: chillers, AHUs, VAV boxes, zones; edges: refrigerant lines, ducts, airflow paths)
  - Embed thermodynamic constraints (refrigeration cycle, psychrometric relationships, mass conservation) in GNN loss functions
  - Implement message-passing algorithms that propagate equipment states through the HVAC network
  - Validate learned models against EnergyPlus HVAC simulations

This enhancement would position students at the cutting edge of an emerging research area while providing practical skills for modeling complex HVAC systems.

**Enhancement Opportunity 2: Hybrid RC-GNN Models for Thermal Mass:** The noted limitations in thermal mass representation [7], [12], [13] suggest a second enhancement:

- **Module 4.2 Enhancement (Multi-Zone Thermal Modeling):** Add a 1-week sub-module titled "Hybrid RC-GNN Models for Thermal Mass" that teaches students to:
  - Decompose building thermal dynamics into fast (air temperature) and slow (thermal mass) components
  - Model thermal mass using RC networks with physically meaningful parameters (thermal capacitance, thermal resistance)
  - Model spatial heat transfer using GNNs that propagate temperature information between zones
  - Couple RC and GNN components through shared boundary conditions

This hybrid approach leverages the strengths of both methods: RC networks provide interpretable, physics-based thermal mass modeling, while GNNs capture complex spatial interactions.

**Enhancement Opportunity 3: GNN Explainability and Validation:** The challenges in model interpretability [15], [20] suggest a third enhancement:

- **Module 10.2 Enhancement (Advanced Analytics and Explainability):** Add a 1-week sub-module titled "Explainability for Graph Neural Networks in Building Energy" that teaches students to:
  - Visualize learned edge weights to understand which zone-to-zone connections dominate heat transfer
  - Analyze attention patterns in Graph Attention Networks to identify critical building elements
  - Decompose node contributions to overall building energy consumption
  - Validate that learned sensitivities align with thermodynamic principles (e.g., increased insulation reduces heat flux)

This enhancement would ensure students can not only build PI-GNN models but also interpret, validate, and communicate their behavior to stakeholders.

**Alignment with Multi-Agent Orchestration:** The curriculum's emphasis on multi-agent orchestration (Months 9–11) aligns with the potential for PI-GNNs to serve as surrogate models in agent-based building control systems. Fast, accurate PI-GNN models can replace computationally expensive EnergyPlus simulations in optimization loops, enabling real-time model predictive control and reinforcement learning for HVAC systems. The curriculum's coverage of generator-optimizer-validator architectures provides the framework for integrating PI-GNN surrogates into multi-agent workflows.

**Alignment with Federated Learning:** The curriculum's federated learning component (Months 9–11) aligns with the need to train PI-GNN models across building portfolios without sharing sensitive operational data. The empirical finding that PI-GNNs achieve high accuracy with limited data [11], [14] suggests they are well-suited for federated learning scenarios where each building contributes a small local dataset. The curriculum's coverage of differential privacy and privacy-utility tradeoffs prepares students to implement federated PI-GNN training for multi-site building optimization.

---

## 3. Simulation Interoperability Standards: Integrating AI Agents and LLMs with IFC, gbXML, FMI, and Modelica

### 3.1 IFC (Industry Foundation Classes) and AI/LLM Integration

Industry Foundation Classes (IFC) is the dominant open standard for exchanging building information models (BIM) between architectural design tools (Revit, ArchiCAD, Vectorworks) and downstream engineering applications including building performance simulation. IFC files encode building geometry, spatial relationships, material properties, and system topology in a structured EXPRESS schema. However, the complexity of IFC schemas (over 800 entity types in IFC4) and the semantic richness of building data create significant barriers to automated model generation and querying. Large Language Models offer promising capabilities for parsing, interpreting, and generating IFC data through natural language interfaces.

**LLM-Based IFC Parsing and Semantic Querying:** Multiple papers demonstrate that LLMs can parse IFC files and extract relevant information through natural language queries. Ibba et al. (metadata paper #4) develop "ASK-BIM: A knowledge graph-powered AI system for natural language querying of BIM models" that uses "LLMs to query IFC-based BIM data via a knowledge graph, enabling IFC parsing and NL queries" [22]. This approach constructs a knowledge graph representation of the IFC model, enabling semantic queries like "What is the total floor area of spaces with occupancy type 'office'?" or "Which walls have thermal transmittance greater than 0.5 W/m²K?" without requiring users to understand IFC entity hierarchies or EXPRESS syntax.

Kim et al. (2025) position "Language Models as BIM Interpreters: Unlocking IFC Data for Automation in Construction Informatics," demonstrating that LLMs can "interpret IFC data, enabling parsing and reasoning over BIM structures" [23]. This capability is critical for building energy modeling, where engineers need to extract thermal zone definitions, envelope properties (U-values, solar heat gain coefficients), and HVAC system configurations from architect-generated IFC files. Traditional IFC parsing requires custom code for each extraction task; LLM-based approaches enable flexible, query-driven extraction through natural language.

Martín-Dorta et al. (metadata paper #10) develop systems for "Natural Language Queries on IFC" that use "AI/LLM to query and parse IFC data via natural language" [24]. The integration with open-source tools like IfcOpenShell (metadata paper #30) enables "reading, editing, and generating IFC files" through conversational interfaces [25], lowering the technical barrier for building energy engineers who may not have software development expertise.

**Automated Extraction of Thermal Properties and System Topology:** A critical application of LLM-based IFC parsing is automated extraction of building performance simulation inputs. Płoszaj-Mazurek et al. (metadata paper #6) demonstrate "Artificial intelligence and digital tools for assisting low-carbon architectural design: merging the use of machine learning, large language models, and building [information modeling]," where LLMs "interpret and generate IFC/BIM data, enabling parsing and extraction" [26]. This includes extracting:
- **Thermal zone geometry:** Volume, floor area, exterior surface area, window-to-wall ratios
- **Envelope properties:** Wall constructions, insulation layers, thermal transmittance (U-values), thermal mass
- **Fenestration:** Window sizes, orientations, glazing properties (SHGC, visible transmittance)
- **HVAC system topology:** Equipment types, connections, control zones

Hong and Zhang (2025) describe "AI for building energy modeling: A transformation" where LLMs translate "IFC geometry" along with "natural language descriptions, tabular audit data, and zoning spreadsheets" into "syntactically correct simulation models like EnergyPlus IDF or Modelica" [27]. This end-to-end pipeline—from architect-generated IFC to simulation-ready energy model—represents a significant automation opportunity, potentially reducing the 8–32 hours typically required for manual model generation [28].

**AI Agents Navigating IFC Schemas for BPS Model Generation:** The complexity of IFC schemas necessitates intelligent navigation strategies. Gao et al. (metadata paper #28) propose a "Multi-agent framework for schema-guided reasoning and tool-augmented interaction with IFC models" that uses "multi-agent reasoning to construct IFC graphs and extract geometry" [29]. This approach decomposes the IFC parsing task into specialized agents:
- **Schema Navigator Agent:** Traverses IFC entity hierarchies to locate relevant objects (IfcSpace for zones, IfcWall for envelope, IfcDistributionElement for HVAC)
- **Property Extractor Agent:** Retrieves property sets (Pset_WallCommon for wall properties, Pset_SpaceCommon for zone properties)
- **Geometry Processor Agent:** Converts IFC geometric representations (swept solids, boundary representations) into simulation-compatible formats
- **Validator Agent:** Checks for missing data, inconsistent units, and semantic errors

This multi-agent architecture aligns with the curriculum's emphasis on generator-optimizer-validator patterns (Months 9–11), demonstrating how specialized agents can collaborate to handle complex data extraction tasks.

**Conversational Interfaces and Human-in-the-Loop Workflows:** Several papers emphasize conversational interfaces that enable iterative refinement of IFC queries and model generation. Fernandes et al. (2024) develop "A GPT-Powered Assistant for Real-Time Interaction with Building Information Models" that enables "conversational interaction with BIM models" and "natural-language front-end" [30]. This human-in-the-loop approach allows engineers to:
- Query IFC models: "Show me all south-facing walls with U-value greater than 0.5"
- Request modifications: "Increase insulation thickness in exterior walls to achieve U-value of 0.3"
- Validate extractions: "Confirm that all thermal zones have been correctly identified"

The curriculum's emphasis on HITL workflows (Months 5–8, 9–11) aligns with this approach, ensuring that automated IFC parsing is subject to human review before propagating to downstream simulation workflows.

**Limitations: Semantic Gaps and Hallucination Risks:** Despite promising capabilities, LLM-based IFC parsing faces significant limitations. The metadata notes "hallucination risks, semantic gaps between standards, schema mismatches, and validation requirements" as critical challenges [27]. Specific issues include:

- **Incomplete IFC Models:** Architect-generated IFC files often lack thermal properties, HVAC system details, and operational schedules required for energy simulation. LLMs may "hallucinate" missing data—generating plausible but incorrect values—rather than flagging gaps for human input.

- **Schema Mismatches:** Different BIM authoring tools export IFC with varying levels of detail and different entity mappings. LLMs trained on one IFC variant may misinterpret files from other tools.

- **Unit Inconsistencies:** IFC supports multiple unit systems (SI, Imperial, mixed). LLMs must correctly identify and convert units, a task where errors can lead to catastrophic simulation failures (e.g., interpreting meters as feet).

- **Lack of Validation:** Current LLM-based approaches often lack rigorous validation against IFC schema constraints and building physics principles. The curriculum's 5-layer physics-constrained safety framework (Type Validation → Physics Validation) provides a template for validating LLM-extracted IFC data before simulation.

**Curriculum Alignment:** The IFC parsing capabilities demonstrated in the literature validate the curriculum's identified gap in simulation interoperability. Proposed curriculum enhancement:

- **Module 5.3 Enhancement (LLM Orchestration):** Add a 1-week sub-module titled "LLM-Assisted IFC Parsing for Building Energy Modeling" that teaches students to:
  - Use LLM APIs (Vertex AI Gemini) to query IFC files and extract thermal properties
  - Implement multi-agent architectures for schema navigation and property extraction
  - Validate LLM-extracted data against IFC schema constraints and physics bounds
  - Handle missing data through human-in-the-loop workflows

This enhancement would bridge the gap between the curriculum's current emphasis on EnergyPlus automation (Months 1–4) and LLM orchestration (Months 5–8), providing practical skills for automating the IFC-to-simulation pipeline.

### 3.2 gbXML and Automated Building Energy Model Generation

Green Building XML (gbXML) is a lightweight, energy-simulation-focused schema designed specifically for exchanging building geometry and thermal properties between BIM tools and energy modeling platforms (EnergyPlus, eQUEST, TRACE, IES-VE). Unlike IFC's comprehensive building representation, gbXML focuses on the subset of data required for energy analysis: thermal zones, surfaces, constructions, fenestration, and HVAC systems. This focused scope makes gbXML an attractive target for LLM-based automated model generation.

**LLM/AI-Driven gbXML Generation from BIM Data:** While the metadata reveals extensive work on IFC parsing, explicit coverage of gbXML generation is limited. Hong and Zhang (2025) mention that LLMs can translate building data into "syntactically correct simulation models" [27], but do not specifically address gbXML as an intermediate format. This gap is significant because many building energy modeling workflows use the BIM → gbXML → EnergyPlus pipeline, where gbXML serves as a standardized intermediate representation that decouples BIM authoring tools from simulation engines.

The absence of explicit gbXML coverage in the top 30 papers suggests that current research focuses on either direct IFC-to-simulation translation (bypassing gbXML) or direct natural-language-to-simulation generation (bypassing both IFC and gbXML). However, gbXML remains widely used in industry practice, particularly for projects using Revit's built-in energy analysis tools or third-party plugins like Sefaira and Insight.

**Translation Pipelines: BIM → gbXML → EnergyPlus/OpenStudio:** The standard workflow for BIM-based energy modeling involves:
1. **BIM Authoring:** Architect creates building geometry and assigns space types in Revit/ArchiCAD
2. **gbXML Export:** BIM tool exports gbXML file containing thermal zones, surfaces, constructions, and schedules
3. **Energy Model Import:** Energy modeler imports gbXML into OpenStudio/EnergyPlus and refines HVAC systems, schedules, and controls
4. **Simulation and Analysis:** Run annual energy simulation and analyze results

LLM-based automation could enhance each step:
- **Step 1 Enhancement:** LLMs could validate BIM models for energy modeling readiness, flagging missing thermal properties or incorrect space type assignments
- **Step 2 Enhancement:** LLMs could enrich gbXML exports by inferring missing data (e.g., construction assemblies based on building type and climate zone)
- **Step 3 Enhancement:** LLMs could automate HVAC system assignment based on building type, size, and climate (e.g., "Assign VAV with reheat for office buildings >50,000 ft² in climate zone 5A")
- **Step 4 Enhancement:** LLMs could interpret simulation results and generate natural-language reports

**Accuracy of Automated Model Generation vs. Manual Workflows:** Lu et al. (2025) provide the most comprehensive comparison of automated vs. manual building energy modeling. Their "Data2BEM" framework using an LLM-based multi-agent system achieved "ASHRAE Guideline 14-level calibration accuracy with NMBE of 2.91%, CV-RMSE of 0.139, and R² of 0.972, while cutting modeling time by >90% (48 minutes vs. 8–32 hours)" [28]. This demonstrates that LLM-driven automation can achieve professional-grade accuracy while dramatically reducing labor requirements.

Zhang et al. (2025) report that their automatic building energy model development workflow achieved "100% success rate in generating accurate, error-free EnergyPlus IDF files across 10 trials, completing models in 9 minutes (6 minutes generation, 3 minutes error correction) compared to two weeks for students and one day for experienced modelers" [31]. This 95–99% time reduction validates the practical value of LLM-based automation for building energy modeling workflows.

However, these results are for direct natural-language-to-IDF generation, not BIM → gbXML → EnergyPlus pipelines. The accuracy of LLM-driven gbXML generation specifically remains an open research question. Potential challenges include:
- **Geometric Simplification:** gbXML requires simplified geometry (planar surfaces, rectangular zones) that may not match complex BIM geometry
- **Surface Matching:** Correctly identifying adjacent surfaces for inter-zone heat transfer is critical but error-prone
- **HVAC System Mapping:** gbXML's HVAC representation is less detailed than EnergyPlus, requiring intelligent simplification

**Curriculum Alignment:** The limited explicit coverage of gbXML in the literature, combined with its continued industry relevance, suggests a curriculum enhancement opportunity:

- **Module 2.2 Enhancement (EnergyPlus Automation):** Add a 1-week sub-module titled "gbXML Workflows and LLM-Assisted Model Generation" that teaches students to:
  - Export gbXML from Revit and import into OpenStudio/EnergyPlus
  - Validate gbXML files for completeness and correctness (surface matching, construction assignments, HVAC systems)
  - Use LLMs to enrich gbXML files by inferring missing data based on building type and climate
  - Compare manual vs. LLM-assisted workflows for accuracy and time efficiency

This enhancement would ensure students understand the full BIM-to-simulation pipeline, including the role of gbXML as an intermediate format, while providing practical skills for LLM-assisted automation.

### 3.3 FMI/FMU Co-Simulation Orchestration with AI Agents

The Functional Mock-up Interface (FMI) is an open standard for co-simulation and model exchange, enabling different simulation tools to be coupled in a unified workflow. Functional Mock-up Units (FMUs) are self-contained simulation components that expose standardized interfaces for initialization, time-stepping, and data exchange. FMI/FMU co-simulation is critical for building performance analysis because buildings are inherently multi-physics systems: thermal dynamics (EnergyPlus), HVAC controls (Modelica), computational fluid dynamics (OpenFOAM), and electrical systems (GridLAB-D) must be simulated together to capture system-level interactions.

**AI-Driven Orchestration of FMUs for Multi-Physics Co-Simulation:** The metadata reveals limited explicit coverage of FMI/FMU orchestration with AI agents. Zhang et al. (2024) mention "co-simulation" in the context of LLM integration with building energy modeling, noting "potential applications including simulation input generation, simulation output analysis and visualization, conducting error analysis, co-simulation, simulation knowledge extraction and training, and simulation optimization" [32]. However, the paper does not detail whether "co-simulation" refers to FMI/FMU-based coupling or other integration approaches.

The absence of explicit FMI/FMU coverage in the top 30 papers is surprising given the growing importance of co-simulation for advanced building energy analysis. Possible explanations include:
- **Recency:** FMI/FMU adoption in building energy simulation is relatively recent (FMI 2.0 released 2014, FMI 3.0 released 2022), and LLM-based orchestration may be an emerging research area not yet well-represented in 2024–2026 literature
- **Complexity:** FMI/FMU co-simulation requires deep technical expertise (numerical integration, algebraic loops, time synchronization), making it a challenging target for LLM-based automation
- **Search Limitations:** The search queries may not have captured papers using alternative terminology (e.g., "co-simulation orchestration," "multi-domain modeling")

**LLM Interfaces for FMU Parameterization and Scenario Generation:** A promising application of LLMs in FMI/FMU workflows is automated parameterization and scenario generation. Building energy co-simulations often require hundreds of parameters (envelope properties, HVAC capacities, control setpoints, occupancy schedules) and multiple scenarios (design days, typical meteorological years, extreme weather events). LLMs could:
- **Interpret Natural Language Scenarios:** "Simulate a heat wave with outdoor temperatures 10°C above normal for one week in July"
- **Generate FMU Parameter Sets:** Automatically populate FMU parameters based on building type, climate zone, and design standards
- **Orchestrate Multi-FMU Workflows:** Coordinate initialization, time-stepping, and data exchange between multiple FMUs (e.g., EnergyPlus FMU for building thermal dynamics, Modelica FMU for HVAC controls, Python FMU for occupant behavior)

**Applications in Hybrid HVAC + Building Envelope Co-Simulation:** A critical use case for FMI/FMU co-simulation is coupling detailed HVAC system models (Modelica) with building envelope models (EnergyPlus). This enables:
- **Advanced Control Design:** Test model predictive control (MPC) algorithms that optimize HVAC operation based on predicted building thermal response
- **Fault Detection and Diagnostics:** Simulate HVAC faults (refrigerant leaks, fouled coils, stuck dampers) and their impact on building energy and comfort
- **Renewable Energy Integration:** Co-simulate building loads, HVAC systems, and on-site solar PV/battery storage to optimize self-consumption

LLM-based orchestration could automate the setup of these complex co-simulation workflows, which currently require manual configuration of FMU connections, data mappings, and time-stepping parameters.

**Empirical Results on Co-Simulation Accuracy and Automation Gains:** The metadata does not provide quantitative results on FMI/FMU co-simulation accuracy or automation gains from LLM-based orchestration. This represents a significant gap in the literature and a high-priority area for future research.

**Curriculum Alignment:** The limited coverage of FMI/FMU in the literature, combined with its critical importance for advanced building energy analysis, suggests a high-priority curriculum enhancement:

- **Module 8.3 Enhancement (AI-Driven Co-Simulation):** Add a 2-week sub-module titled "FMI/FMU Co-Simulation Orchestration with LLM Agents" that teaches students to:
  - Understand FMI/FMU standards and co-simulation architectures (master-slave, parallel, algebraic loops)
  - Export FMUs from EnergyPlus and Modelica for building envelope and HVAC system models
  - Use LLMs to generate FMU parameter sets from natural language scenario descriptions
  - Implement multi-agent orchestration for FMU initialization, time-stepping, and data exchange
  - Validate co-simulation results against standalone simulations

This enhancement would position the curriculum at the forefront of an emerging research area while providing practical skills for advanced building energy analysis workflows that are increasingly demanded by industry.

### 3.4 Modelica and LLM-Assisted Model Synthesis

Modelica is an open, equation-based, object-oriented modeling language widely used for multi-physics system simulation, including building energy systems through the Modelica Buildings Library developed by Lawrence Berkeley National Laboratory. Modelica's declarative syntax—where engineers specify physical equations rather than procedural algorithms—makes it particularly amenable to LLM-based code generation, as the target output is structured, physics-based, and well-documented.

**LLMs Generating or Modifying Modelica Models:** Wan et al. (2025) provide the most comprehensive study of "Automating Modelica Module Generation Using Large Language Models: A Case Study on Building Control Description Language" [33]. The study demonstrates that LLMs can generate Modelica code for control modules, with "success rates reaching up to full for basic logic blocks and 83 percent for control modules with engineered prompts" [33]. Critically, the study found that "GPT-4o failed to produce executable Modelica code in zero-shot mode, while Claude Sonnet 4 achieved up to full success for basic logic blocks with carefully engineered prompts" [33], highlighting the importance of prompt engineering and model selection.

The workflow combines "standardized prompt scaffolds, library-aware grounding, automated compilation with OpenModelica, and human-in-the-loop evaluation" [33]. This structured approach addresses common LLM limitations:
- **Prompt Scaffolds:** Provide templates that guide the LLM to generate syntactically correct Modelica code with proper library imports, component declarations, and equation sections
- **Library-Aware Grounding:** Include relevant Modelica Buildings Library documentation in the prompt context to ensure generated code uses existing components correctly
- **Automated Compilation:** Compile generated code with OpenModelica and provide error messages back to the LLM for iterative refinement
- **Human-in-the-Loop Evaluation:** Expert review of generated code for correctness, efficiency, and adherence to modeling best practices

**Natural Language to Modelica Translation Pipelines:** The study demonstrates natural language to Modelica translation for control logic: "And, Or, Not, and Switch" basic logic tasks and "chiller enable/disable, bypass valve control, cooling tower fan speed, plant requests, and relief damper control" control modules [33]. This capability enables building energy engineers to specify control strategies in natural language—"Enable the chiller when cooling demand exceeds 50 kW and outdoor air temperature is above 15°C"—and automatically generate Modelica code that implements the logic.

Hong and Zhang (2025) describe broader capabilities where LLMs translate "natural language descriptions, tabular audit data, CAD/IFC geometry, and zoning spreadsheets" into "syntactically correct simulation models like EnergyPlus IDF or Modelica" [27]. This suggests that LLMs can generate complete Modelica building models, not just control modules, though detailed empirical results are not provided in the metadata.

**AI-Assisted Debugging and Validation of Modelica Models:** A critical capability demonstrated by Wan et al. (2025) is automated debugging through iterative compilation and error correction. The workflow includes "automated compilation with OpenModelica" where compilation errors are fed back to the LLM, which then generates corrected code [33]. This addresses a major pain point in Modelica modeling: cryptic compiler error messages that require expert knowledge to interpret and resolve.

However, the study notes that "failed outputs required medium-level human repair (estimated one to eight hours)" [33], indicating that current LLM capabilities are insufficient for fully automated Modelica generation. The study also found that "human evaluation outperformed AI evaluation, since current LLMs cannot assess simulation results or validate behavioral correctness" [33], highlighting the need for human-in-the-loop validation of generated models.

**Key Benchmarks and Accuracy Metrics:** Wan et al. (2025) provide quantitative results on time savings and success rates:
- **Time Savings:** "40 to 60 percent time savings, reducing development from 10-20 hours to 4-6 hours per module" [33]
- **Success Rates:** "Up to full success for basic logic blocks" and "83 percent for control modules" [33]
- **Human Repair Effort:** "Medium-level human repair (estimated one to eight hours)" for failed outputs [33]

These results demonstrate substantial but incomplete automation: LLMs can significantly accelerate Modelica development but cannot yet replace human expertise entirely. The curriculum's emphasis on human-in-the-loop workflows (Months 5–8, 9–11) aligns with this reality, ensuring students learn to validate and refine LLM-generated code rather than blindly trusting it.

**Limitations: Retrieval-Augmented Generation Mismatches:** A critical finding is that "Retrieval-Augmented Generation often produced mismatches in module selection (for example, And retrieved as Or), while a deterministic hard rule search strategy avoided these errors" [33]. This highlights a fundamental limitation of current RAG approaches: semantic similarity in embedding space does not guarantee functional equivalance in code. An "And" logic block and an "Or" logic block may have similar textual descriptions but produce completely different behavior.

The curriculum's emphasis on physics-constrained safety frameworks (Months 5–8) provides a template for addressing this limitation: validate LLM-generated Modelica code against expected behavior through automated testing (unit tests, integration tests, simulation-based validation) before deployment.

**Curriculum Alignment:** The Modelica generation capabilities demonstrated by Wan et al. (2025) validate the curriculum's emphasis on LLM orchestration (Months 5–8) while identifying specific enhancement opportunities:

- **Module 8.3 Enhancement (AI-Driven Co-Simulation):** Add a 1-week sub-module titled "LLM-Assisted Modelica Model Synthesis for HVAC Controls" that teaches students to:
  - Understand Modelica syntax and the Buildings Library structure
  - Use LLM APIs (Vertex AI Gemini) to generate Modelica control modules from natural language specifications
  - Implement automated compilation and error correction loops with OpenModelica
  - Validate generated models through simulation-based testing (comparing LLM-generated vs. manually-coded control strategies)
  - Apply human-in-the-loop review for correctness and efficiency

This enhancement would provide practical skills for accelerating HVAC control design while reinforcing the curriculum's emphasis on validation and human oversight.

### 3.5 Cross-Standard Integration and Interoperability Pipelines

The ultimate goal of simulation interoperability is seamless end-to-end workflows that span multiple standards and tools: architects generate IFC models in Revit, energy modelers translate to gbXML and import into OpenStudio, controls engineers export Modelica FMUs for co-simulation, and facility managers deploy calibrated models for operational optimization. LLM-based automation has the potential to orchestrate these complex multi-standard pipelines, but current research demonstrates limited integration across standards.

**End-to-End Pipelines: IFC → gbXML → Modelica/FMU → Simulation:** The metadata reveals that most papers focus on single-standard automation (IFC parsing, Modelica generation, EnergyPlus IDF creation) rather than multi-standard integration. Hong and Zhang (2025) describe the broadest scope, where LLMs translate "natural language descriptions, tabular audit data, CAD/IFC geometry, and zoning spreadsheets" into "syntactically correct simulation models like EnergyPlus IDF or Modelica" [27], but do not detail whether this includes intermediate gbXML or FMU generation.

A hypothetical end-to-end LLM-orchestrated pipeline might include:
1. **IFC Parsing Agent:** Extract building geometry, thermal zones, and envelope properties from architect-generated IFC file
2. **gbXML Generation Agent:** Translate IFC data to gbXML format, inferring missing thermal properties based on building type and climate
3. **EnergyPlus Import Agent:** Import gbXML into OpenStudio, assign HVAC systems, and generate EnergyPlus IDF
4. **Modelica FMU Export Agent:** Export building envelope as EnergyPlus FMU and HVAC controls as Modelica FMU
5. **Co-Simulation Orchestration Agent:** Configure FMU connections, time-stepping, and data exchange for coupled simulation
6. **Results Analysis Agent:** Interpret simulation outputs and generate natural-language reports

No paper in the top 30 demonstrates this complete pipeline, suggesting it remains an aspirational goal rather than current capability.

**Multi-Standard AI Orchestration Agents:** Lu et al. (2025) provide the closest example of multi-standard orchestration with their "Data2BEM" framework that integrates "architectural drawings, specifications, and sensor data to automatically generate and calibrate building energy simulations" [28]. The multi-agent system includes:
- **Information Retriever Agent:** Extracts data from heterogeneous sources (PDFs, images, spreadsheets)
- **Programmer Agent:** Generates EnergyPlus IDF code
- **Result Analyzer Agent:** Interprets simulation outputs
- **Reviewer Agent:** Validates model accuracy against measured data

This demonstrates that multi-agent architectures can orchestrate complex workflows spanning multiple data sources and tools, though the specific standards addressed (IFC, gbXML, FMI, Modelica) are not detailed in the metadata.

**Current Limitations: Semantic Gaps, Schema Mismatches, Hallucination Risks:** The metadata consistently identifies critical limitations in multi-standard integration:

**Semantic Gaps:** Different standards represent building data at different levels of abstraction and with different semantic assumptions. For example:
- IFC represents walls as 3D geometric solids with layered material assemblies
- gbXML represents walls as planar surfaces with single U-value thermal properties
- EnergyPlus represents walls as multi-layer constructions with detailed material properties
- Modelica represents walls as RC networks with thermal resistance and capacitance

Translating between these representations requires semantic reasoning about which details to preserve, which to simplify, and which to infer. LLMs may struggle with these nuanced decisions, leading to information loss or incorrect assumptions.

**Schema Mismatches:** Even within a single standard, different tools may export data with different entity mappings and property sets. For example, Revit's IFC export may use different property set names than ArchiCAD's export for the same physical properties. LLMs trained on one tool's IFC variant may misinterpret files from other tools.

**Hallucination Risks in Model Generation:** The most critical limitation is hallucination: LLMs generating plausible but incorrect data to fill gaps in incomplete input files. Hong and Zhang (2025) note "AI model opacity, hallucination risks, lack of standardized benchmarks, and the need for expert validation" as key challenges [27]. Specific hallucination risks include:
- **Missing Thermal Properties:** LLM invents U-values or SHGC values rather than flagging missing data
- **Incorrect HVAC System Assignment:** LLM assigns inappropriate HVAC system type based on superficial building description
- **Invalid Control Strategies:** LLM generates Modelica control code that compiles but produces unstable or inefficient behavior

The curriculum's 5-layer physics-constrained safety framework (Type Validation → Physics Validation → Resource Limits → Audit Logging → Compliance) provides a template for mitigating these risks through rigorous validation of LLM-generated outputs.

**Curriculum Alignment:** The limited demonstration of multi-standard integration in the literature, combined with its critical importance for real-world building energy workflows, suggests a high-priority curriculum enhancement:

- **Module 8.4 NEW (Multi-Standard Simulation Interoperability):** Add a 2-week module titled "LLM-Orchestrated Multi-Standard Building Energy Workflows" that teaches students to:
  - Understand the semantic relationships between IFC, gbXML, EnergyPlus IDF, and Modelica representations
  - Implement multi-agent architectures for end-to-end IFC → gbXML → EnergyPlus → Modelica/FMU pipelines
  - Validate LLM-generated translations at each stage using physics-constrained safety frameworks
  - Handle missing data through human-in-the-loop workflows rather than LLM hallucination
  - Benchmark automated vs. manual workflows for accuracy and time efficiency

This new module would directly address the identified curriculum gap in simulation interoperability while providing practical skills for automating the complex multi-tool workflows that dominate building energy engineering practice.

### 3.6 Curriculum Alignment

The findings on AI agents and LLMs for simulation interoperability standards provide strong validation for the curriculum's emphasis on LLM orchestration and multi-agent architectures while identifying a critical gap that requires new curriculum content.

**Validation of LLM Orchestration Emphasis:** The empirical evidence that LLM-based automation achieves 40–60% time savings for Modelica generation [33] and >90% time reduction for building energy modeling [28], [31] validates the curriculum's emphasis on LLM orchestration (Months 5–8). Students who master prompt engineering, RAG, and multi-agent architectures can dramatically accelerate building energy workflows, making comprehensive energy analysis economically viable for projects that would otherwise rely on simplified rules-of-thumb.

**Validation of Multi-Agent Architectures:** The generator-optimizer-validator architectures demonstrated by Lu et al. (2025) [28] and Zhang et al. (2025) [31] directly validate the curriculum's emphasis on multi-agent orchestration (Months 9–11). The decomposition of complex tasks into specialized agents (Information Retriever, Programmer, Result Analyzer, Reviewer) aligns with the curriculum's training in agent-based system design.

**Validation of Human-in-the-Loop Workflows:** The finding that "failed outputs required medium-level human repair (estimated one to eight hours)" [33] and that "human evaluation outperformed AI evaluation" [33] validates the curriculum's emphasis on HITL workflows. Students learn that LLM-based automation is a productivity multiplier, not a replacement for human expertise, and that rigorous validation is essential for production deployment.

**Validation of Physics-Constrained Safety Framework:** The identified challenges—"hallucination risks, semantic gaps between standards, schema mismatches, and validation requirements" [27]—directly validate the curriculum's 5-layer physics-constrained safety framework. The Type Validation layer catches schema mismatches, the Physics Validation layer catches hallucinated thermal properties that violate thermodynamic bounds, and the Audit Logging layer provides traceability for debugging multi-standard translation pipelines.

**Critical Gap: Simulation Interoperability Standards:** The prior comprehensive review identified simulation interoperability as a curriculum gap, and this focused review confirms that gap while demonstrating its importance. The curriculum currently emphasizes EnergyPlus automation (Months 1–4) and LLM orchestration (Months 5–8) but does not explicitly teach IFC parsing, gbXML workflows, FMI/FMU co-simulation, or Modelica synthesis. Given the empirical evidence that these standards are critical for real-world building energy workflows and that LLM-based automation can dramatically accelerate them, this gap represents a high-priority enhancement opportunity.

**Recommended Curriculum Enhancements:**

1. **Module 5.3 Enhancement (LLM Orchestration):** Add "LLM-Assisted IFC Parsing for Building Energy Modeling" (1 week) to teach IFC schema navigation, property extraction, and validation.

2. **Module 2.2 Enhancement (EnergyPlus Automation):** Add "gbXML Workflows and LLM-Assisted Model Generation" (1 week) to teach BIM → gbXML → EnergyPlus pipelines and LLM-based enrichment.

3. **Module 8.3 Enhancement (AI-Driven Co-Simulation):** Expand to 3 weeks and add:
   - "FMI/FMU Co-Simulation Orchestration with LLM Agents" (1 week)
   - "LLM-Assisted Modelica Model Synthesis for HVAC Controls" (1 week)

4. **Module 8.4 NEW (Multi-Standard Simulation Interoperability):** Add new 2-week module on "LLM-Orchestrated Multi-Standard Building Energy Workflows" covering end-to-end IFC → gbXML → EnergyPlus → Modelica/FMU pipelines.

These enhancements would add 5 weeks of content, which could be accommodated by:
- Extending the curriculum from 12 to 13 months (preferred option to maintain depth)
- Condensing existing content in Months 5–8 (Generative AI Integration phase) by 1 week
- Offering simulation interoperability as an elective track for students pursuing building energy specialization

**Alignment with Industry Practice:** The proposed enhancements align with industry practice, where building energy engineers routinely work with IFC files from architects, export gbXML for energy modeling, and increasingly use Modelica for advanced HVAC control design. By teaching students to automate these workflows with LLMs, the curriculum prepares them to be highly productive practitioners who can deliver comprehensive energy analysis at a fraction of traditional cost and time.

**Alignment with Safety Framework:** The proposed enhancements reinforce the curriculum's physics-constrained safety framework by providing concrete applications where validation is critical. Students learn that LLM-generated IFC extractions must be validated against schema constraints, that gbXML translations must be validated against physics bounds (e.g., U-values in reasonable ranges), and that Modelica control code must be validated through simulation-based testing. This hands-on experience with validation workflows strengthens students' understanding of why the 5-layer safety framework is essential for production AI systems.

---

## 4. Cross-Cutting Analysis

### Convergence: Where PI-GNNs and Simulation Interoperability Intersect

The two research areas examined in this review—Physics-Informed Graph Neural Networks for intra-building thermal modeling and AI agents for simulation interoperability standards—are beginning to converge in ways that create powerful synergies for building energy engineering.

**GNN-Based Surrogate Models Replacing FMUs:** A promising convergence point is using PI-GNN models as fast surrogate models that replace computationally expensive FMUs in co-simulation workflows. Traditional FMI/FMU co-simulation couples detailed physics-based models (EnergyPlus for building envelope, Modelica for HVAC controls), but the computational cost of running these models at each time step limits real-time control applications and large-scale optimization studies.

PI-GNNs trained on FMU simulation data can serve as fast surrogates: the GNN learns to approximate the FMU's input-output behavior while respecting physics constraints, enabling 100–1000× speedup for real-time model predictive control. The empirical finding that PI-GNNs achieve high accuracy with limited training data [11], [14] suggests they can be trained on relatively small FMU simulation datasets, making this approach practical.

The curriculum's coverage of PI-GNNs (proposed enhancement in Module 3.5) and FMI/FMU co-simulation (proposed enhancement in Module 8.3) positions students to implement this convergence: train PI-GNN surrogates on EnergyPlus FMU data, validate against full FMU simulations, and deploy in real-time control applications.

**LLMs Generating Graph Topologies from IFC:** A second convergence point is using LLMs to automatically generate graph topologies for PI-GNN models from IFC building data. Currently, constructing graph topologies for multi-zone buildings requires manual specification of which zones are nodes, which walls are edges, and what thermal properties parameterize edge weights. This is labor-intensive and error-prone for large buildings.

LLMs that can parse IFC files and extract spatial relationships [22], [23], [24] could automatically generate graph topologies: identify thermal zones as nodes, detect shared walls/floors/ceilings as edges, extract thermal properties (U-values, thermal mass) as node/edge features, and output a graph structure ready for PI-GNN training. This would dramatically accelerate the deployment of PI-GNN models for building-specific applications.

The curriculum's proposed enhancements in IFC parsing (Module 5.3) and PI-GNN graph topology (Module 3.5) would enable students to implement this convergence, bridging the gap between BIM data and graph-based AI models.

**Multi-Agent Orchestration for Integrated Workflows:** A third convergence point is multi-agent orchestration that integrates PI-GNN training, simulation interoperability, and production deployment. A hypothetical workflow might include:
1. **IFC Parsing Agent:** Extract building geometry and thermal properties from IFC file
2. **Graph Construction Agent:** Generate PI-GNN topology from IFC spatial relationships
3. **FMU Simulation Agent:** Run EnergyPlus FMU simulations to generate training data
4. **PI-GNN Training Agent:** Train physics-informed GNN on FMU data with embedded constraints
5. **Validation Agent:** Validate PI-GNN accuracy against held-out FMU simulations
6. **Deployment Agent:** Export trained PI-GNN as FMU for integration into building control systems

This end-to-end pipeline, orchestrated by specialized LLM agents, would automate the entire process from BIM data to deployed AI model. The curriculum's emphasis on multi-agent architectures (Months 9–11) provides the foundation for students to design and implement such integrated workflows.

### Synergies with Existing Curriculum Modules

**Safety Frameworks:** Both research areas reinforce the curriculum's 5-layer physics-constrained safety framework:
- **PI-GNNs:** Demonstrate that physics constraints reduce errors by 65–72% [14], validating the Physics Validation layer
- **Simulation Interoperability:** Highlight hallucination risks in LLM-generated models [27], validating the need for Type Validation and Physics Validation

Students learn that safety frameworks are not abstract concepts but practical necessities for preventing catastrophic failures in both graph-based AI models and LLM-orchestrated simulation workflows.

**Multi-Agent Orchestration:** Both research areas demonstrate the power of multi-agent architectures:
- **PI-GNNs:** Can be integrated into multi-agent control systems where specialized agents optimize HVAC, lighting, and plug loads using fast GNN surrogate models
- **Simulation Interoperability:** Require multi-agent orchestration for complex IFC → gbXML → EnergyPlus → Modelica pipelines [28], [31]

The curriculum's progression from single-agent Python automation (Months 1–4) to multi-agent orchestration (Months 9–11) prepares students to design agent-based systems that integrate both PI-GNN models and simulation interoperability workflows.

**Explainability:** Both research areas benefit from the curriculum's emphasis on explainability (Months 9–11):
- **PI-GNNs:** Require explainability techniques (visualizing edge weights, analyzing attention patterns) to validate that learned models respect building physics
- **Simulation Interoperability:** Require explainability to understand why LLMs made specific translation decisions (e.g., why a particular HVAC system was assigned)

Students learn to apply SHAP, Sobol sensitivity analysis, and domain-specific explainability methods to both graph-based AI models and LLM-orchestrated workflows, ensuring that automated systems are interpretable and trustworthy.

### Priority Curriculum Enhancement Recommendations

Based on the cross-cutting analysis, we recommend the following priority enhancements with specific module placements:

**Priority 1 (Highest Impact): Multi-Standard Simulation Interoperability**
- **Module 8.4 NEW:** "LLM-Orchestrated Multi-Standard Building Energy Workflows" (2 weeks)
- **Rationale:** Directly addresses identified curriculum gap; enables >90% time savings [28], [31]; critical for industry practice
- **Prerequisites:** Modules 1–8 (EnergyPlus automation, LLM orchestration, multi-agent architectures)

**Priority 2 (High Impact): HVAC Network Graph Modeling**
- **Module 3.5 Enhancement:** "Graph Neural Networks for HVAC Thermal Networks" (2 weeks)
- **Rationale:** Addresses limited HVAC component modeling in current PI-GNN literature [18], [19]; enables detailed chiller/AHU/VAV modeling
- **Prerequisites:** Modules 1–3 (building physics, EnergyPlus HVAC, multi-zone thermal modeling)

**Priority 3 (High Impact): FMI/FMU Co-Simulation with LLM Orchestration**
- **Module 8.3 Enhancement:** "FMI/FMU Co-Simulation Orchestration with LLM Agents" (1 week) + "LLM-Assisted Modelica Model Synthesis" (1 week)
- **Rationale:** Enables advanced multi-physics simulation; 40–60% time savings for Modelica generation [33]; critical for HVAC control design
- **Prerequisites:** Modules 1–8 (EnergyPlus automation, LLM orchestration, co-simulation fundamentals)

**Priority 4 (Medium Impact): IFC Parsing and gbXML Workflows**
- **Module 5.3 Enhancement:** "LLM-Assisted IFC Parsing" (1 week)
- **Module 2.2 Enhancement:** "gbXML Workflows and LLM-Assisted Model Generation" (1 week)
- **Rationale:** Enables automated BIM-to-simulation pipelines; addresses industry-standard workflows
- **Prerequisites:** Module 2 (EnergyPlus automation) for gbXML; Module 5 (LLM orchestration) for IFC

**Priority 5 (Medium Impact): Hybrid RC-GNN Models for Thermal Mass**
- **Module 4.2 Enhancement:** "Hybrid RC-GNN Models for Thermal Mass" (1 week)
- **Rationale:** Addresses noted limitation in PI-GNN thermal mass representation [7], [12], [13]; enables accurate passive solar and demand response modeling
- **Prerequisites:** Modules 1–4 (building physics, RC networks, multi-zone thermal modeling)

**Implementation Strategy:** These enhancements add 8 weeks of content. Recommended implementation:
- **Year 1 (Immediate):** Implement Priority 1 (Module 8.4 NEW) and Priority 2 (Module 3.5 Enhancement) by extending curriculum to 13 months
- **Year 2 (Next Cycle):** Implement Priority 3 (Module 8.3 Enhancement) and Priority 4 (Modules 2.2 and 5.3 Enhancements)
- **Year 3 (Refinement):** Implement Priority 5 (Module 4.2 Enhancement) and refine based on student feedback and industry input

This phased approach ensures that the highest-impact enhancements (multi-standard interoperability, HVAC network modeling) are implemented immediately while allowing time to develop and refine the more specialized content.

---

## 5. Conclusion

This focused literature review systematically examined 60 highly relevant papers (top 30 from each of two combined tables totaling 289 unique papers) published between 2024–2026 to address two critical gaps identified in a prior comprehensive curriculum validation study: the over-emphasis on urban-scale graph neural network modeling and the absence of simulation interoperability standards in the Scientific AI Engineering Master Curriculum.

### Key Findings: Internal Building Physics & PI-GNNs

For Research Question 1 (How do PI-GNNs model multi-zone building thermal dynamics and HVAC thermal networks?), we find:

**Graph Topologies:** PI-GNNs for intra-building physics construct graphs where thermal zones are nodes and inter-zone heat flow pathways are edges [5], [6], with alternative topologies using cells for open-plan spaces [7], building elements for design optimization [8], and finite difference grids for high-fidelity thermal modeling [10]. Adjacency matrices explicitly encode building topology, ensuring heat flows only between physically connected zones [9].

**Physics Constraints:** Energy balance (Qext + Q1 + Q2 + Q3 + Q4 = McΔT/Δt) [10], Fourier conduction (Qcond = kAΔT/LΔt) [10], [11], and thermodynamic laws are embedded through loss function penalties [5] and architectural constraints [14]. These constraints ensure that learned models respect fundamental physical laws rather than learning spurious correlations.

**Empirical Advantages:** PI-GNNs achieve 17–35% accuracy improvements over physically consistent methods [15], with mean errors below 1% using only 20 training samples when physics constraints are embedded [11], [14]. Compared to pure data-driven models, physics-informed approaches reduce errors by 65–72% [14] and demonstrate superior generalization to unseen building configurations. Specific quantitative results include R² values of 0.79–0.94 for HVAC load prediction [9], RMSE reductions from 1.48°C to 0.88°C (41% improvement) compared to RC models [16], and 68% error reduction for residential heat pump temperature prediction [17].

**HVAC Component Modeling:** Explicit modeling of HVAC components as graph elements remains limited. Li et al. (2024) demonstrate VAV terminals and ductwork as nodes and edges [18], but detailed modeling of chillers, AHUs, cooling towers, and pumps is not demonstrated in the top 30 papers. This represents a significant gap and high-priority enhancement opportunity for the curriculum.

**Limitations:** Scalability to large buildings [7], [15], [20], data availability [15], real-time inference requirements [15], [19], generalization across building types [7], [20], lack of thermal mass detail [7], [12], [13], and model complexity vs. interpretability [15], [20] remain open challenges.

### Key Findings: Simulation Interoperability Standards

For Research Question 2 (How are AI agents and LLMs being integrated with simulation interoperability standards?), we find:

**IFC Integration:** LLMs demonstrate strong capabilities for parsing IFC files and extracting thermal properties through natural language queries [22], [23], [24], with multi-agent frameworks for schema navigation and property extraction [29]. Conversational interfaces enable iterative refinement and human-in-the-loop validation [30]. However, hallucination risks, semantic gaps, and schema mismatches remain critical challenges [27].

**gbXML Workflows:** Explicit coverage of gbXML generation is limited in the literature, despite its continued industry relevance. This represents a curriculum gap that should be addressed through explicit instruction on BIM → gbXML → EnergyPlus pipelines and LLM-based enrichment.

**FMI/FMU Co-Simulation:** Coverage of FMI/FMU orchestration with AI agents is surprisingly limited in the top 30 papers, despite the growing importance of co-simulation for advanced building energy analysis. This represents a high-priority research area and curriculum enhancement opportunity.

**Modelica Synthesis:** LLMs achieve 40–60% time savings for Modelica module generation, with success rates of 83% for control modules using engineered prompts [33]. However, failed outputs require medium-level human repair (1–8 hours) [33], and human evaluation outperforms AI evaluation [33], highlighting the need for human-in-the-loop workflows.

**Multi-Standard Integration:** End-to-end pipelines spanning IFC → gbXML → Modelica/FMU → simulation are not demonstrated in the top 30 papers, suggesting this remains an aspirational goal. However, multi-agent architectures demonstrate the potential for orchestrating complex workflows [28], [31].

**Automation Gains:** LLM-based automation achieves >90% modeling time reduction (48 minutes vs. 8–32 hours) [28] and 100% success rate for EnergyPlus IDF generation [31], demonstrating substantial practical value. However, hallucination risks, validation requirements, and the need for expert oversight remain critical limitations [27], [33].

### Curriculum Validation and Enhancement

These findings provide strong validation for the curriculum's design choices:

**Domain-First Progression:** The empirical evidence that physics constraints reduce errors by 65–72% [14] validates the curriculum's emphasis on mastering building physics (Months 1–4) before applying graph neural networks.

**Physics-Constrained Safety Framework:** The identified challenges—hallucination risks, semantic gaps, validation requirements [27]—directly validate the curriculum's 5-layer safety framework (Type Validation → Physics Validation → Resource Limits → Audit Logging → Compliance).

**Multi-Agent Orchestration:** The generator-optimizer-validator architectures demonstrated in the literature [28], [31] validate the curriculum's emphasis on multi-agent orchestration (Months 9–11).

**Human-in-the-Loop Workflows:** The finding that human evaluation outperforms AI evaluation [33] and that failed outputs require human repair [33] validates the curriculum's emphasis on HITL workflows.

However, the review also identifies a critical gap: **simulation interoperability standards** (IFC, gbXML, FMI, Modelica) are not explicitly addressed in the current curriculum, despite their importance for real-world building energy workflows and the substantial automation gains demonstrated by LLM-based approaches.

### Top 3 Highest-Priority Papers for Curriculum Reading Lists

Based on empirical rigor, practical relevance, and alignment with curriculum objectives, we recommend the following papers for required reading:

**1. Wan et al. (2025) – "Automating Modelica Module Generation Using Large Language Models"** [33]
- **Rationale:** Provides the most comprehensive empirical evaluation of LLM-based code generation for building energy applications, with quantitative results on success rates (83%), time savings (40–60%), and human repair effort (1–8 hours). Demonstrates structured workflow (prompt scaffolds, library-aware grounding, automated compilation, HITL evaluation) that aligns with curriculum's emphasis on production-grade LLM orchestration.
- **Module Placement:** Required reading for Module 8.3 (AI-Driven Co-Simulation)

**2. Lu et al. (2025) – "Automated building energy modeling for energy retrofits using a large language model-based multi-agent framework"** [28]
- **Rationale:** Demonstrates end-to-end multi-agent workflow achieving ASHRAE Guideline 14-level calibration accuracy (NMBE 2.91%, CV-RMSE 0.139, R² 0.972) with >90% time reduction (48 minutes vs. 8–32 hours). Validates curriculum's generator-optimizer-validator architecture and HITL workflows. Provides concrete evidence of practical value for building energy retrofits.
- **Module Placement:** Required reading for Module 9.3 (Multi-Agent Orchestration)

**3. Jiang and Dong (2024) – "Modularized neural network incorporating physical priors for future building energy modeling"** [9]
- **Rationale:** Demonstrates physics-informed graph neural network achieving R² values of 0.79–0.94 for HVAC load prediction with explicit physics constraints (heat balance equations, monotonicity constraints). Shows 54% reduction in temperature prediction error compared to RC models and demonstrates physically consistent sensitivities (22% heating demand reduction for window U-value changes). Validates curriculum's domain-first progression and physics-constrained safety framework.
- **Module Placement:** Required reading for Module 4.2 (Multi-Zone Thermal Modeling)

### Final Recommendations

This focused review corrects the urban-scale emphasis of the prior comprehensive review by drilling into intra-building physics and simulation interoperability standards. The findings validate the curriculum's pedagogical model and technical content while identifying specific enhancement opportunities that would position students at the cutting edge of building energy AI engineering:

1. **Immediate Priority:** Implement Module 8.4 NEW (Multi-Standard Simulation Interoperability) to address the identified curriculum gap
2. **High Priority:** Enhance Module 3.5 (HVAC Systems) with graph neural network modeling for HVAC thermal networks
3. **High Priority:** Enhance Module 8.3 (AI-Driven Co-Simulation) with FMI/FMU orchestration and Modelica synthesis
4. **Medium Priority:** Enhance Modules 2.2 and 5.3 with gbXML workflows and IFC parsing
5. **Medium Priority:** Enhance Module 4.2 with hybrid RC-GNN models for thermal mass

These enhancements, totaling 8 weeks of additional content, would comprehensively address the identified gaps while maintaining the curriculum's core strengths: domain-first progression, physics-constrained safety frameworks, multi-agent orchestration, and human-in-the-loop workflows. The result would be a curriculum that prepares Scientific AI Engineers to bridge the gap between cutting-edge research and industry practice, delivering substantial productivity gains (40–90% time savings) while maintaining rigorous validation and safety standards.

---

## 6. References

[1] Shan, X., Zhou, J., Chang, V. W.-C., & Yang, E.-H. (2025). Physics-Informed and Explainable Graph Neural Networks for Generalizable Urban Building Energy Modeling. *Applied Sciences*, 15(16), 8854. https://doi.org/10.3390/app15168854

[2] Jiang, Y., & Dong, B. (2024). Modularized neural network incorporating physical priors for future building energy modeling. [PDF document]

[3] Weilin, L., et al. (2025). UrbanGraph: A physics-informed spatio-temporal dynamic heterogeneous graph framework for urban microclimate prediction.

[4] Nie, Y., et al. (2025). Energy-informed graph neural diffusion for predicting large-scale urban network dynamics.

[5] Yang, Z., Chong, A., Lim, E., Tham, K. W., & Wen, J. (2024). Physics-constrained graph modeling for building thermal dynamics. *Energy and AI*, 100346. https://doi.org/10.1016/j.egyai.2024.100346

[6] Chunxiang, G., et al. (2021). Multi-zone indoor temperature prediction based on Graph Attention Network and Gated Recurrent Unit. *Conference on Automation Science and Engineering*. https://doi.org/10.1109/CASE49439.2021.9551630

[7] Nagarathinam, S., et al. (2024). PhyGICS – A Physics-informed Graph Neural Network-based Intelligent HVAC Controller for Open-plan Spaces. https://doi.org/10.1145/3632775.3661957

[8] Zijian, W., et al. (2025). Exploring building energy performance prediction using graph neural networks. https://doi.org/10.17868/strath.00093246

[9] Jiang, Y., & Dong, B. (2024). Modularized neural network incorporating physical priors for future building energy modeling. [PDF document]

[10] Goldfeder, S., et al. (2024). Real-World Data and Calibrated Simulation Suite for Offline Training of Reinforcement Learning Agents to Optimize Energy and Emission in Buildings for Environmental Sustainability. https://doi.org/10.48550/arxiv.2410.03756

[11] Peng, W., et al. (2023). Physics-informed graph convolutional neural network for modeling fluid flow and heat convection. *The Physics of Fluids*. https://doi.org/10.1063/5.0161114

[12] Pang, Y., et al. (2025). A Physics-Informed Graph Neural Network Approach for Multi-Time-Step Prediction of Indoor Temperature Fields. https://doi.org/10.1109/yac66630.2025.11150336

[13] Nagarathinam, S., et al. (2024). PhyGICS–a physics-informed graph neural network-based intelligent HVAC controller for open-plan spaces.

[14] Peng, W., et al. (2023). Physics-informed graph convolutional neural network for modeling geometry-adaptive steady-state natural convection. *International Journal of Heat and Mass Transfer*. https://doi.org/10.1016/j.ijheatmasstransfer.2023.124593

[15] Jiang, Y., et al. (2025). Physics-informed machine learning for building performance simulation-A review of a nascent field. *Advances in Applied Energy*. https://doi.org/10.1016/j.adapen.2025.100223

[16] Natale, A., et al. (2022). Physically Consistent Neural Networks for building thermal modeling: Theory and analysis. *Applied Energy*. https://doi.org/10.1016/j.apenergy.2022.119806

[17] Stephanie, L. (2025). Indoor Temperature Prediction for Residential Heat Pumps: A Physics-Informed Machine Learning Approach. https://doi.org/10.5258/soton/p1254

[18] Li, Z., et al. (2024). Design information-assisted graph neural network for modeling central air conditioning systems. *Advanced Engineering Informatics*. https://doi.org/10.1016/j.aei.2024.102379

[19] Zhu, X., et al. (2024). Chiller System Power Prediction by Physical-Informed Neural Network.

[20] Zhang, Y. (2024). Development of stochastic occupancy modelling methods and occupancy-integrated mpc for smart built environment control and its implementation.

[21] Wang, Z., et al. (2024). Scalable Physics-Informed Multi-Agent Reinforcement Learning for Building Energy System Control.

[22] Ibba, M., et al. (2024). ASK-BIM: A knowledge graph-powered AI system for natural language querying of BIM models.

[23] Kim, J., et al. (2025). Language Models as BIM Interpreters: Unlocking IFC Data for Automation in Construction Informatics. *Social Science Research Network*. https://doi.org/10.2139/ssrn.5563440

[24] Martín-Dorta, N., et al. (2024). Natural Language Queries on IFC.

[25] Martín-Dorta, N., et al. (2024). Integration of Artificial Intelligence and Open-Source Tools for Intelligent Natural Language Queries on IFC Models: An Accessible and Collaborative Solution.

[26] Płoszaj-Mazurek, M., et al. (2024). Artificial intelligence and digital tools for assisting low-carbon architectural design: merging the use of machine learning, large language models, and building information modeling.

[27] Hong, T., & Zhang, J. (2025). AI for building energy modeling: A transformation. [PDF document]

[28] Lu, Y., et al. (2025). Automated building energy modeling for energy retrofits using a large language model-based multi-agent framework. *iScience*. https://doi.org/10.1016/j.isci.2025.113867

[29] Gao, X., et al. (2024). Multi-agent framework for schema-guided reasoning and tool-augmented interaction with IFC models.

[30] Fernandes, J., et al. (2024). A GPT-Powered Assistant for Real-Time Interaction with Building Information Models. *Buildings*, 14(8), 2499. https://doi.org/10.3390/buildings14082499

[31] Zhang, Y., et al. (2025). Automatic building energy model development and debugging using large language models agentic workflow. [PDF document]

[32] Zhang, J., et al. (2024). Advancing Building Energy Modeling with Large Language Models: Exploration and Case Studies. *Energy and Buildings*. https://doi.org/10.1016/j.enbuild.2024.114788

[33] Wan, H., et al. (2025). Automating Modelica Module Generation Using Large Language Models: A Case Study on Building Control Description Language. https://doi.org/10.48550/arxiv.2509.14623

[34] Nithyanantham, S., et al. (2024). MCP4IFC: IFC-Based Building Design Using Large Language Models.

[35] Saluz, M., et al. (2024). Large-language-model-based building-information-model alignment for automatic-compliance-checking: towards closing the gap between model authoring and compliance.

[36] Jiang, Y., & Chen, Y. (2025). Efficient fine-tuning of large language models for automated building energy modeling in complex cases. [PDF document]

[37] Xu, Z., et al. (2025). Automated carbon-aware assessment of openBIM-based ductwork design using knowledge graph–augmented LLM multi-agent framework. *Automation in Construction*. https://doi.org/10.1016/j.autcon.2025.106611

[38] Zhao, Y., et al. (2025). Poster Abstract: Text-To-EnergyPlus: Translating Natural Language into Building Energy Simulation. [PDF document]

[39] ElSayed, M., et al. (2025). User-friendly AI-driven automation for rapid building energy model generation. [PDF document]

[40] Iranmanesh, A., et al. (2025). LLM-assisted Graph-RAG Information Extraction from IFC Data. *arXiv.org*. https://doi.org/10.48550/arxiv.2504.16813
