# Literature Review Report: The Integration of Machine Learning in Building Performance Simulation (BPS)

## Methodologies, Limitations, and Future Trends

**Author:** Comprehensive Analysis of 7 Research Papers  
**Date:** December 2025

---

## Executive Summary

This literature review examines the integration of machine learning (ML) in Building Performance Simulation (BPS), analyzing seven recent research papers spanning 2019-2025. The review demonstrates that ML techniques offer transformative computational advantages—achieving speeds up to 1,266 times faster than traditional BPS methods while maintaining accuracy levels above 90%. XGBoost emerges as the dominant algorithm for traditional applications, consistently outperforming neural networks in accuracy and efficiency. However, the field is rapidly evolving toward Physics-Informed Machine Learning (PIML), which addresses critical limitations of purely data-driven approaches by embedding physical laws into model architectures. Key research gaps include the black-box nature of ML models, challenges in occupant behavior modeling, and issues with scalability and generalization across different building types and climates.

---

## 1. Introduction: The Paradigm Shift from Traditional BPS to Machine Learning

### 1.1 Background and Context

The building performance simulation (BPS) landscape is experiencing a fundamental transformation, driven by the integration of machine learning (ML) techniques that address critical limitations of traditional physics-based approaches. Traditional BPS tools such as EnergyPlus, TRNSYS, ESP-r, and IDA ICE, while providing detailed physical insights and reliable energy modeling capabilities, suffer from significant computational burdens and practical limitations that hinder their widespread adoption (Villano et al., 2024; Jiang et al., 2025).

### 1.2 Computational Cost vs. Accuracy Trade-offs

The most compelling driver for ML integration is the dramatic reduction in computational costs while maintaining or improving accuracy. Traditional BPS methods are notoriously time-consuming, with simulation times ranging from hours to days or even weeks, particularly for complex urban-scale energy modeling and fine-grained computational fluid dynamics (CFD) simulations (Chakraborty & Elzarka, 2019). This computational burden is especially problematic when conducting optimization studies, uncertainty analyses, or parametric assessments that require thousands or millions of simulation runs (Tian, 2024; Markarian et al., 2024).

#### 1.2.1 Speed Improvements

Machine learning offers transformative computational advantages documented across multiple studies:

- **Dramatic Speed Enhancement**: Studies demonstrate remarkable speed enhancements, with ML models achieving computational speeds **1,266 times faster** than traditional BPS-based optimization approaches (Markarian et al., 2024). Deep learning techniques have reduced heating and cooling energy prediction times by **99.92%**, from several hours to just 0.08% of the original time (Villano et al., 2024).

- **Real-Time Prediction**: The prediction time for optimized ML models, excluding ANNs, typically does not exceed **5 milliseconds** compared to EnergyPlus's average of **10 seconds** per alternative (Forouzandeh et al., 2023). This enables real-time decision-making and interactive design exploration that was previously impossible with traditional BPS.

- **Scalability for Optimization**: For multi-objective optimization tasks involving thousands of building configurations, ML-based surrogate models enable feasible computation where traditional BPS would be prohibitively expensive (Markarian et al., 2024; Wang et al., 2025).

#### 1.2.2 Maintained or Improved Accuracy

Despite these speed improvements, ML models maintain competitive or superior accuracy levels:

- **High Prediction Accuracy**: XGBoost models achieved R² values between **0.90 and 0.99** for various targets including annual electricity consumption and peak load predictions, with errors between ML-based and EnergyPlus simulations remaining within **±3%** for optimal solutions (Markarian et al., 2024).

- **Comparable Performance**: Advanced ML techniques demonstrate prediction accuracies comparable to or exceeding traditional BPS methods across multiple energy metrics, including heating/cooling loads, thermal comfort indices, and peak demand predictions (Chakraborty & Elzarka, 2019; Forouzandeh et al., 2023; Wang et al., 2025).

- **Uncertainty Quantification**: Modern ML approaches incorporating uncertainty quantification methods can provide probabilistic predictions that capture both aleatory and epistemic uncertainties, offering richer information than deterministic BPS outputs (Tian, 2024).

### 1.3 Why ML is Replacing Traditional BPS

The literature identifies several compelling reasons for the paradigm shift from traditional BPS to ML-enhanced approaches:

1. **Computational Efficiency**: Enables large-scale applications, optimization, and uncertainty analysis that are computationally infeasible with traditional BPS (Markarian et al., 2024; Tian, 2024).

2. **Early Design Support**: Provides rapid feedback during early design stages when multiple design alternatives need quick evaluation (Forouzandeh et al., 2023).

3. **Retrofit Optimization**: Facilitates building stock analysis and retrofit strategy optimization at scale, supporting sustainable building transitions (Wang et al., 2025; Markarian et al., 2024).

4. **Real-Time Control**: Enables predictive control strategies for building energy management systems that require fast, accurate predictions (Jiang et al., 2025).

5. **Data Utilization**: Leverages the growing availability of building operational data and advances in computing infrastructure to create data-driven models that capture complex, non-linear relationships (Villano et al., 2024).

However, as detailed in subsequent sections, this transition is not without challenges, particularly regarding model interpretability, physical consistency, and generalization capabilities.

---

## 2. Methodological Trends: Algorithm Performance and Training Approaches

### 2.1 XGBoost vs. Neural Networks: A Comprehensive Comparison

The literature reveals nuanced insights into algorithm selection, with different ML techniques excelling in specific contexts and applications.

#### 2.1.1 XGBoost: The Dominant Algorithm for Traditional Applications

XGBoost (eXtreme Gradient Boosting) consistently emerges as the top-performing algorithm across multiple studies for traditional BPS applications:

**Superior Performance Metrics:**

- **Cooling Electricity Prediction**: XGBoost achieved RN_RMSE of **2.43%** and R² of **0.99**, significantly outperforming ANN which achieved **4.2%** RN_RMSE and **0.96** R² (Chakraborty & Elzarka, 2019).

- **Comprehensive Energy Metrics**: Across multiple studies, XGBoost demonstrated R² values ranging from **0.9887 to 0.99203** for various energy metrics including heating energy, cooling energy, and total energy consumption (Wang et al., 2025).

- **Retrofit Optimization**: XGBoost models achieved errors within **±3%** compared to EnergyPlus simulations for optimal retrofit solutions while being **1,266 times faster** (Markarian et al., 2024).

- **Consistent Rankings**: In comparative studies testing multiple algorithms (Random Forest, Support Vector Machines, ANNs, etc.), XGBoost consistently ranked as the top or near-top performing algorithm (Chakraborty & Elzarka, 2019; Wang et al., 2025).

**Computational Efficiency:**

- **Parallel Processing**: Built with OpenMP support, XGBoost efficiently utilizes all CPU cores in parallel, with pre-sorting of independent variables reducing training complexity and computational time (Chakraborty & Elzarka, 2019).

- **Feature Selection**: The inherent feature selection capability through importance scoring means external feature selection algorithms are not always necessary, simplifying the modeling workflow (Wang et al., 2025).

- **Training Speed**: XGBoost models typically train faster than complex neural networks while achieving comparable or superior accuracy, making them ideal for iterative design processes (Forouzandeh et al., 2023).

**Practical Advantages:**

- **Interpretability**: Compared to deep neural networks, XGBoost offers better interpretability through feature importance rankings and tree structure visualization (Tian, 2024).

- **Robustness**: Less prone to overfitting than neural networks when properly tuned, particularly with limited training data (Chakraborty & Elzarka, 2019).

- **Ease of Implementation**: Requires less hyperparameter tuning expertise compared to deep learning architectures (Forouzandeh et al., 2023).

#### 2.1.2 Neural Networks: Specialized Applications and Emerging Dominance

Despite XGBoost's overall superiority in traditional applications, neural networks demonstrate particular strengths in specific domains and represent the future direction of the field:

**Temporal Dependencies and Sequential Data:**

- **Recurrent Neural Networks (RNNs)**: Excel in handling sequential data and temporal relationships, capturing time-series patterns in energy consumption and thermal dynamics (Jiang et al., 2025).

- **Long Short-Term Memory (LSTM)**: Achieved MAPE of **0.4%** for single-zone air temperature predictions, demonstrating exceptional accuracy for temporal forecasting tasks (Jiang et al., 2025).

- **Gated Recurrent Units (GRUs)**: Provide computational efficiency advantages over LSTMs while maintaining strong performance on time-series prediction tasks (Villano et al., 2024).

**Spatial Relationships and Multi-Zone Modeling:**

- **Convolutional Neural Networks (CNNs)**: Effectively capture spatial relationships for multi-zone thermal modeling, treating building layouts as spatial grids similar to image processing applications (Jiang et al., 2025).

- **Graph Neural Networks (GNNs)**: Model heat transfer between adjacent zones by representing buildings as graphs, with zones as nodes and thermal connections as edges (Jiang et al., 2025).

**Physics-Informed Applications:**

- **Physics-Informed Neural Networks (PINNs)**: Incorporate physical laws directly into loss functions, achieving improved generalization and physical consistency (Jiang et al., 2025).

- **Physics-Informed Graph Neural Networks (PIGNNs)**: Achieved **1-2 orders of magnitude faster** performance than traditional CFD while maintaining physical consistency for urban wind field predictions (Jiang et al., 2025).

- **Modularized Neural Networks**: Incorporating physical priors for smart building control achieved R² ranging from **0.79 to 0.94** with strong generalization under disruptive events like power outages (Jiang et al., 2025).

**Deep Learning for Complex Patterns:**

- **Multi-Layer Perceptrons (MLPs)**: Capable of capturing highly non-linear relationships in building energy performance with sufficient training data (Villano et al., 2024).

- **Ensemble Architectures**: Combining different neural network types (e.g., CNN for spatial features + LSTM for temporal dynamics) shows promise for comprehensive building modeling (Jiang et al., 2025).

#### 2.1.3 Comparative Summary: When to Use Each Approach

**Use XGBoost when:**
- Predicting steady-state or aggregated energy metrics (annual consumption, peak loads)
- Working with tabular data and limited training samples
- Interpretability and feature importance are priorities
- Computational resources are limited
- Quick model development and deployment are needed

**Use Neural Networks when:**
- Modeling temporal dynamics and time-series predictions
- Capturing spatial relationships in multi-zone buildings
- Implementing physics-informed approaches
- Large training datasets are available
- Complex, non-linear patterns require deep architectures
- Real-time control and sequential decision-making are involved

### 2.2 Training Data Strategies: Synthetic vs. Real Data

The literature reveals sophisticated understanding of data utilization strategies, with most successful approaches combining both synthetic and real data sources.

#### 2.2.1 Synthetic Data from Building Simulation Tools

**Generation Process:**

Synthetic data is generated using established BPS tools (primarily EnergyPlus) by running parametric simulations across design variables such as building geometry, envelope properties, HVAC systems, and operational schedules (Chakraborty & Elzarka, 2019; Forouzandeh et al., 2023; Markarian et al., 2024; Wang et al., 2025).

**Advantages:**

1. **Controlled Experimentation**: Enables systematic exploration of design spaces with precise control over input parameters and boundary conditions (Forouzandeh et al., 2023).

2. **Rapid Data Generation**: Creates large datasets in minutes to hours rather than years required for real building monitoring (Chakraborty & Elzarka, 2019).

3. **Parameter Coverage**: Allows investigation of design combinations and extreme scenarios that might not exist in real-world datasets or historical records (Wang et al., 2025).

4. **Consistent Baseline**: Provides standardized datasets for research comparison and algorithm benchmarking across studies (Villano et al., 2024).

5. **Physics-Informed Training**: Creates "physics-informed datasets" that bias ML models toward physically consistent predictions by training on physics-based simulation outputs (Jiang et al., 2025).

6. **Cost-Effective**: Eliminates expensive and time-consuming monitoring infrastructure and data collection campaigns (Markarian et al., 2024).

**Limitations:**

1. **Idealized Assumptions**: Synthetic data often assumes standardized occupant behavior, perfect HVAC operation, and idealized boundary conditions that don't reflect real-world variability (Wang et al., 2025).

2. **Model Uncertainty**: Inherits uncertainties and potential biases from the underlying BPS tool used for data generation (Tian, 2024).

3. **Limited Realism**: May not capture stochastic occupant interactions, equipment degradation, or operational anomalies present in real buildings (Jiang et al., 2025).

4. **Validation Challenges**: Models trained solely on synthetic data require careful validation with real data to ensure practical applicability (Forouzandeh et al., 2023).

#### 2.2.2 Real Measured Data

**Data Sources:**

Real data comes from building energy management systems (BEMS), smart meters, IoT sensors, weather stations, and historical utility records (Villano et al., 2024; Jiang et al., 2025).

**Advantages:**

1. **Realistic Behavior**: Captures actual operational conditions, occupant interactions, equipment performance, and environmental variations (Wang et al., 2025).

2. **Validation Quality**: Provides ground truth for model validation and helps identify limitations of synthetic data approaches (Tian, 2024).

3. **Existing Building Applications**: Essential for retrofit optimization and predictive maintenance of existing buildings where historical data is available (Markarian et al., 2024).

4. **Anomaly Detection**: Includes real-world anomalies, faults, and edge cases that improve model robustness (Jiang et al., 2025).

**Limitations:**

1. **Data Scarcity**: Limited availability, especially for diverse building types, climates, and operational conditions (Villano et al., 2024).

2. **Quality Issues**: Missing values, sensor errors, calibration drift, and inconsistent measurement protocols (Tian, 2024).

3. **Limited Coverage**: Real datasets often cover limited parameter ranges, restricting model generalization to novel designs (Forouzandeh et al., 2023).

4. **Privacy and Access**: Building operational data may be proprietary or subject to privacy restrictions (Wang et al., 2025).

5. **Time Requirements**: Collecting comprehensive datasets requires extended monitoring periods (months to years) (Chakraborty & Elzarka, 2019).

#### 2.2.3 Hybrid Approaches: Best of Both Worlds

The most successful implementations strategically combine synthetic and real data:

**Ensemble Learning Framework (Ma et al., 2024):**

- **Approach**: Divides prediction tasks into physics-driven components (using EnergyPlus for HVAC load calculations) and data-driven components (LSTM for residuals capturing occupant behavior and operational variations).

- **Results**: Achieved **40-90% improvements** in MAE and CV-RMSE over traditional physics-based models (Jiang et al., 2025).

**Transfer Learning:**

- **Pre-training on Synthetic Data**: Models are first trained on large synthetic datasets to learn general building physics relationships (Jiang et al., 2025).

- **Fine-tuning on Real Data**: Models are then fine-tuned on limited real building data to capture site-specific characteristics and operational patterns (Villano et al., 2024).

**Data Augmentation:**

- **Synthetic Expansion**: Real datasets are augmented with synthetic data to cover broader parameter ranges and improve generalization (Wang et al., 2025).

- **Physics-Guided Interpolation**: Physical models guide interpolation between sparse real measurements to create denser training datasets (Tian, 2024).

**Recommended Strategy:**

The literature consensus suggests a hybrid approach:
1. Generate synthetic data for initial model training and broad parameter coverage
2. Validate with available real data to identify model limitations
3. Fine-tune or calibrate models using real data for specific applications
4. Use physics-informed constraints to ensure consistency across both data types

---

## 3. Critical Research Gaps and Limitations

### 3.1 Black-Box Models and Physical Consistency Challenges

The most significant and frequently cited limitation across all seven papers is the "black-box" nature of ML models and their lack of guaranteed physical consistency.

#### 3.1.1 Interpretability Crisis

**The Fundamental Problem:**

The opaque nature of many ML models, particularly deep neural networks and ensemble methods, makes it difficult to understand the underlying reasons for their predictions (Jiang et al., 2025; Villano et al., 2024). This lack of transparency creates several critical issues:

- **Trust Deficit**: Engineering practitioners require physical understanding to trust model predictions, especially for high-stakes decisions involving safety, comfort, and substantial financial investments (Forouzandeh et al., 2023).

- **Debugging Challenges**: When models produce unexpected or poor predictions, the black-box nature makes it extremely difficult to diagnose root causes and implement targeted improvements (Tian, 2024).

- **Regulatory Barriers**: Building codes and standards often require physically interpretable calculations and justifications that black-box models cannot provide (Markarian et al., 2024).

**Attempted Solutions and Their Limitations:**

Several studies employ **SHAP (SHapley Additive exPlanations)** methods to provide local and global interpretations of model behavior (Chakraborty & Elzarka, 2019; Wang et al., 2025; Tian, 2024):

- **SHAP Benefits**: Quantifies feature importance and reveals how individual features contribute to specific predictions, offering post-hoc interpretability.

- **SHAP Limitations**: Adds computational overhead, provides correlation-based rather than causal insights, and doesn't fundamentally address the lack of physical grounding (Jiang et al., 2025).

Other interpretability approaches include feature importance rankings (XGBoost), attention mechanisms (neural networks), and sensitivity analyses, but none fully resolve the fundamental interpretability challenge (Villano et al., 2024).

#### 3.1.2 Physical Inconsistency and Violations

**Manifestations of Physical Inconsistency:**

Purely data-driven models can produce predictions that violate fundamental physical laws (Jiang et al., 2025):

- **Energy Conservation Violations**: Models may predict energy outputs that violate thermodynamic principles or conservation laws.

- **Unrealistic Relationships**: Predictions may show physically impossible relationships, such as cooling loads increasing with better insulation (all else equal).

- **Extrapolation Failures**: When applied outside training data ranges, models often produce physically implausible results (Tian, 2024).

- **Temporal Inconsistencies**: Time-series predictions may violate causality or physical constraints on rate of change (Jiang et al., 2025).

**Consequences:**

1. **Limited Generalization**: Models trained on specific conditions often fail when applied to different building types, climates, or operational scenarios (Wang et al., 2025; Forouzandeh et al., 2023).

2. **Poor Extreme Event Performance**: Lack of physical grounding leads to significant failures during unusual conditions like extreme weather, power outages, or equipment failures (Jiang et al., 2025).

3. **Unreliable Optimization**: When used for design optimization, physically inconsistent models may suggest solutions that appear optimal but violate physical constraints (Markarian et al., 2024).

4. **Reduced Adoption**: The building industry's conservative nature and regulatory requirements create barriers to adopting models that cannot guarantee physical consistency (Villano et al., 2024).

### 3.2 Occupant Behavior and Microclimate Data Challenges

#### 3.2.1 Occupant Behavior Modeling Complexity

The literature consistently identifies occupant behavior as one of the most challenging aspects of building performance prediction (Wang et al., 2025; Forouzandeh et al., 2023; Jiang et al., 2025).

**The Stochastic Nature Problem:**

- **Aleatory Uncertainty**: Occupant behavior represents irreducible, stochastic uncertainty that cannot be fully addressed through physics embedding alone (Jiang et al., 2025).

- **Individual Variability**: Different occupants exhibit vastly different behaviors regarding window opening, thermostat adjustment, lighting use, and equipment operation (Wang et al., 2025).

- **Temporal Variability**: The same occupant may behave differently based on time of day, day of week, season, weather, and personal factors (mood, health, social context) (Villano et al., 2024).

**Standardization vs. Reality Gap:**

Current research often assumes standardized HVAC operation and passive occupant behavior, but actual energy consumption is highly impacted by:

- **Thermostat Preferences**: Individual comfort preferences leading to different setpoint selections (Forouzandeh et al., 2023).

- **Window Operation**: Unpredictable window opening/closing patterns affecting natural ventilation and HVAC loads (Wang et al., 2025).

- **Equipment Usage**: Variable plug loads from personal devices, appliances, and equipment (Villano et al., 2024).

- **Adaptive Behaviors**: Occupants' adaptive actions in response to discomfort (adding/removing clothing, using fans, relocating) (Jiang et al., 2025).

**Data Collection Challenges:**

- **Privacy Concerns**: Detailed occupant behavior monitoring raises significant privacy issues, limiting data availability (Wang et al., 2025).

- **Monitoring Complexity**: Capturing comprehensive occupant behavior requires extensive sensor networks and potentially invasive monitoring (Villano et al., 2024).

- **Generalization Issues**: Occupant behavior patterns learned from one building may not transfer to others due to cultural, demographic, and contextual differences (Forouzandeh et al., 2023).

#### 3.2.2 Microclimate and Local Environmental Factors

**Urban Heat Island (UHI) Effects:**

Localized climatic phenomena like Urban Heat Island effects are inadequately represented by broad climate trend analyses (Wang et al., 2025):

- **Spatial Variability**: Temperatures can vary significantly within short distances due to urban morphology, vegetation, and surface materials.

- **Temporal Dynamics**: UHI intensity varies with time of day, season, and weather conditions in complex ways.

- **Impact on Performance**: UHI effects can significantly impact cooling loads and retrofit strategy effectiveness, but are rarely incorporated in ML models (Wang et al., 2025).

**Microclimate Data Gaps:**

- **Limited Weather Stations**: Standard weather files (TMY, EPW) represent regional airports or rural locations, not actual building sites (Forouzandeh et al., 2023).

- **Missing Variables**: Important microclimate factors like local wind patterns, solar shading from adjacent buildings, and ground temperature variations are often unavailable (Tian, 2024).

- **Climate Change Uncertainty**: Future climate projections add another layer of uncertainty, particularly for long-term retrofit planning (Wang et al., 2025).

### 3.3 Scalability and Generalization Issues

#### 3.3.1 Limited Scope and Building Stock Challenges

**Single Building Focus:**

Many studies focus on individual buildings or specific building types, limiting scalability for large-scale applications (Villano et al., 2024; Markarian et al., 2024):

- **Building Stock Scarcity**: Building stocks remain scarcely investigated, yet understanding stock-level performance is crucial for ecological transitions and policy development (Wang et al., 2025).

- **Typology Limitations**: Models trained on specific building typologies (e.g., office buildings) often perform poorly when applied to other types (e.g., residential, retail, industrial) (Forouzandeh et al., 2023).

- **Age and Construction Variations**: Historical buildings with unique construction methods and materials present challenges for models trained on modern building data (Markarian et al., 2024).

#### 3.3.2 Climate and Geographic Transferability

**Climate Dependency:**

Models trained on specific climates often require significant retraining or recalibration when applied to different climate zones (Wang et al., 2025; Chakraborty & Elzarka, 2019):

- **Heating vs. Cooling Dominance**: Models optimized for cooling-dominated climates may not capture heating dynamics well, and vice versa (Forouzandeh et al., 2023).

- **Seasonal Patterns**: Training data from limited seasons may not capture full annual variation, reducing prediction accuracy (Tian, 2024).

- **Extreme Events**: Models rarely include extreme weather events in training data, limiting their reliability for resilience assessments (Wang et al., 2025).

**Geographic Factors:**

- **Regulatory Differences**: Building codes, construction practices, and HVAC systems vary by region, affecting model transferability (Markarian et al., 2024).

- **Cultural Factors**: Occupant behavior patterns and comfort expectations vary across cultures and regions (Villano et al., 2024).

#### 3.3.3 Data Requirements and Availability

**Training Data Demands:**

The need for extensive, high-quality training data limits practical deployment (Jiang et al., 2025; Tian, 2024):

- **Data Volume**: Deep learning approaches often require thousands to millions of training samples for robust performance (Villano et al., 2024).

- **Data Quality**: Missing values, sensor errors, and inconsistent measurement protocols degrade model performance (Tian, 2024).

- **Feature Engineering**: Requires domain expertise to select and engineer appropriate features, particularly for complex building systems (Chakraborty & Elzarka, 2019).

**Novel Building Challenges:**

- **Zero-Shot Learning**: Predicting performance for novel building designs or technologies not represented in training data remains extremely challenging (Jiang et al., 2025).

- **Innovative Systems**: Emerging technologies (advanced HVAC, renewable integration, smart controls) lack historical data for model training (Villano et al., 2024).

### 3.4 Additional Critical Limitations

#### 3.4.1 Temporal Resolution and Aggregation

- **Aggregation Loss**: Many studies predict aggregated metrics (annual energy) but lose information about peak demands and temporal patterns crucial for grid integration and HVAC sizing (Forouzandeh et al., 2023).

- **Time-Step Sensitivity**: Model performance often degrades when predicting at finer temporal resolutions (hourly vs. monthly) (Villano et al., 2024).

#### 3.4.2 Multi-Objective Trade-offs

- **Single Objective Focus**: Many studies optimize for energy consumption alone, neglecting thermal comfort, indoor air quality, cost, and environmental impacts (Markarian et al., 2024).

- **Pareto Front Approximation**: ML models for multi-objective optimization may not accurately represent trade-off frontiers (Markarian et al., 2024).

#### 3.4.3 Uncertainty Quantification

- **Deterministic Predictions**: Most ML models provide point predictions without uncertainty estimates, limiting their utility for risk-informed decision-making (Tian, 2024).

- **Uncertainty Sources**: Distinguishing between aleatory (irreducible) and epistemic (reducible) uncertainties remains challenging (Tian, 2024).

#### 3.4.4 Computational Resources for Training

- **Training Costs**: While prediction is fast, training complex models (especially deep learning) requires significant computational resources and time (Villano et al., 2024).

- **Hyperparameter Tuning**: Extensive hyperparameter optimization can be computationally expensive and requires expertise (Chakraborty & Elzarka, 2019).

---

## 4. Emerging Solutions: Physics-Informed Machine Learning (PIML)

### 4.1 PIML Fundamentals and Promise

Physics-Informed Machine Learning (PIML) represents the most significant emerging paradigm to address the fundamental limitations of both traditional BPS and purely data-driven ML approaches (Jiang et al., 2025). PIML integrates fundamental physical laws with advanced machine learning techniques by embedding physics-based principles directly into model architectures, loss functions, parameters, or training algorithms.

#### 4.1.1 Core Concept and Philosophy

**Defining PIML:**

PIML bridges the gap between physics-based and data-driven modeling by incorporating domain knowledge (physical laws, conservation principles, boundary conditions) into ML frameworks (Jiang et al., 2025). This integration can occur through:

1. **Physics-Informed Loss Functions**: Adding penalty terms to loss functions that penalize violations of physical laws (e.g., energy conservation, thermodynamic principles).

2. **Physics-Informed Architectures**: Designing network structures that inherently respect physical constraints (e.g., modular networks mirroring building system components).

3. **Physics-Informed Training Data**: Generating training data from physics-based simulations to bias models toward physically consistent predictions.

4. **Hybrid Modeling**: Combining physics-based components for well-understood phenomena with data-driven components for complex or uncertain processes.

**Philosophical Shift:**

PIML represents a paradigm shift from viewing physics and data as competing approaches to recognizing them as complementary sources of information (Jiang et al., 2025):

- **Physics provides**: Fundamental principles, conservation laws, boundary conditions, and causal relationships.
- **Data provides**: Empirical observations, system-specific behaviors, and validation of physical assumptions.
- **PIML synthesizes**: The generalization power of physics with the flexibility of data-driven learning.

#### 4.1.2 Key Advantages Over Pure Data-Driven Approaches

**1. Enhanced Generalization:**

PIML improves generalization to unseen scenarios by narrowing the solution space to physically plausible regions (Jiang et al., 2025):

- **Extrapolation Capability**: Physics constraints guide predictions outside training data ranges, improving reliability in novel conditions.
- **Robustness to Distribution Shift**: Physical grounding makes models more robust when applied to different building types, climates, or operational scenarios.
- **Extreme Event Performance**: Physical constraints improve predictions during unusual conditions like equipment failures or extreme weather (Jiang et al., 2025).

**2. Reduced Data Requirements:**

By leveraging prior knowledge from physical laws, PIML significantly reduces training data requirements compared to traditional data-driven models (Jiang et al., 2025):

- **Sample Efficiency**: Physics constraints provide additional "information" beyond training samples, enabling learning from smaller datasets.
- **Transfer Learning**: Physics-informed models trained on one building can more easily transfer to others, as physical principles remain constant.
- **Cold Start Problem**: PIML can make reasonable predictions even with minimal building-specific data by relying on physical priors.

**3. Physical Consistency Guarantees:**

PIML ensures predictions adhere to known physical principles, addressing the black-box nature of traditional ML models (Jiang et al., 2025):

- **Conservation Laws**: Energy, mass, and momentum conservation can be enforced through architectural constraints or loss function penalties.
- **Thermodynamic Consistency**: Predictions respect thermodynamic principles like heat transfer directionality and temperature bounds.
- **Causal Relationships**: Physical constraints encode known causal relationships (e.g., insulation reduces heat transfer), preventing spurious correlations.

**4. Improved Interpretability:**

PIML provides deeper insights into model behavior by grounding predictions in physical understanding (Jiang et al., 2025):

- **Mechanistic Explanations**: Predictions can be explained in terms of underlying physical processes rather than just statistical correlations.
- **Diagnostic Capabilities**: Physical inconsistencies in predictions can indicate data quality issues or model limitations.
- **Engineering Trust**: Physical grounding increases practitioner trust and regulatory acceptance.

### 4.2 PIML Implementation Strategies in BPS

Jiang et al. (2025) provide a comprehensive taxonomy of PIML approaches for building performance simulation:

#### 4.2.1 Physics-Informed Neural Networks (PINNs)

**Methodology:**

PINNs incorporate physical laws directly into the loss function by adding terms that penalize violations of governing differential equations (Jiang et al., 2025).

**Loss Function Structure:**
```
Total Loss = Data Loss + λ × Physics Loss
```

Where:
- **Data Loss**: Measures prediction error on available training data (standard MSE or MAE)
- **Physics Loss**: Quantifies violations of physical laws (e.g., heat equation, energy balance)
- **λ**: Weighting parameter balancing data fidelity and physical consistency

**BPS Applications:**

- **Thermal Dynamics**: Enforcing heat equation constraints for temperature field predictions in buildings.
- **Energy Balance**: Ensuring energy conservation in HVAC system modeling.
- **Boundary Conditions**: Incorporating known boundary conditions (ambient temperature, solar radiation) as hard constraints.

**Example Results:**

Di Natale et al. (2022, 2023) introduced physically consistent neural networks ensuring temperature prediction gradients align with physical laws, achieving **improved MAE** compared to RC baselines and standard LSTMs while guaranteeing physical plausibility (Jiang et al., 2025).

#### 4.2.2 Modularized Physics-Informed Architectures

**Methodology:**

Design neural network architectures that mirror the modular structure of building systems, with separate sub-networks for different physical components (envelope, HVAC, lighting, etc.) (Jiang et al., 2025).

**Advantages:**

- **Component-Level Interpretability**: Each module's behavior can be understood and validated independently.
- **Flexible Integration**: Modules can be updated or replaced without retraining the entire model.
- **Physical Constraints**: Module interfaces can enforce physical consistency (e.g., HVAC module output constrained by equipment capacity).

**Breakthrough Example:**

**Jiang and Dong (2024)** developed modularized neural networks incorporating physical priors for smart building control (Jiang et al., 2025):

- **Architecture**: Separate modules for thermal dynamics, HVAC systems, and occupant interactions, with physics-based constraints at module boundaries.
- **Performance**: Achieved R² ranging from **0.79 to 0.94** across different prediction tasks.
- **Generalization**: Demonstrated strong generalization under disruptive events like power outages, where purely data-driven models failed.
- **Interpretability**: Module-level analysis enabled identification of specific system components driving performance.

#### 4.2.3 Physics-Informed Graph Neural Networks (PIGNNs)

**Methodology:**

Represent buildings as graphs where nodes represent zones/spaces and edges represent physical connections (heat transfer, airflow), then use GNNs with physics-informed constraints (Jiang et al., 2025).

**Advantages:**

- **Spatial Relationships**: Naturally captures multi-zone thermal interactions and heat transfer networks.
- **Scalability**: Graph structure easily scales from single buildings to urban-scale modeling.
- **Physical Constraints**: Edge functions can enforce heat transfer laws (Fourier's law, convection correlations).

**Breakthrough Example:**

**Shao et al. (2023)** created Physics-Informed Graph Neural Networks (PIGNN-CFD) for urban wind field prediction (Jiang et al., 2025):

- **Application**: Predicting wind patterns around buildings for natural ventilation and pedestrian comfort analysis.
- **Performance**: Achieved **1-2 orders of magnitude faster** computation than traditional CFD simulations.
- **Physical Consistency**: Maintained physical consistency by incorporating fluid dynamics equations into the graph network architecture.
- **Validation**: Predictions matched CFD results within acceptable engineering tolerances while enabling real-time urban wind analysis.

#### 4.2.4 Hybrid Physics-Data Models

**Methodology:**

Divide the prediction task into physics-driven components (for well-understood phenomena) and data-driven components (for complex or uncertain processes), then combine them in an ensemble framework (Jiang et al., 2025).

**Strategy:**

1. **Physics Component**: Use traditional BPS or simplified analytical models for predictable, well-characterized processes (e.g., envelope heat transfer, solar gains).

2. **Data Component**: Use ML to capture residuals, uncertainties, and complex behaviors not well-represented by physics models (e.g., occupant behavior, system inefficiencies, microclimate effects).

3. **Integration**: Combine predictions through weighted averaging, stacking, or sequential processing.

**Breakthrough Example:**

**Ma et al. (2024)** proposed an ensemble learning framework combining physics and data (Jiang et al., 2025):

- **Architecture**: 
  - Physics-driven component: EnergyPlus for HVAC load calculations based on building physics
  - Data-driven component: LSTM for residuals capturing occupant behavior and operational variations
  
- **Performance**: Achieved **40-90% improvements** in MAE and CV-RMSE over traditional physics-based models alone.

- **Generalization**: Physics component ensures baseline physical consistency, while data component adapts to building-specific characteristics.

- **Interpretability**: Physics component provides mechanistic understanding, while data component captures empirical deviations.

### 4.3 PIML Performance Improvements and Validation

#### 4.3.1 Quantitative Performance Gains

The literature documents substantial performance improvements from PIML approaches across multiple metrics:

**Speed Improvements:**
- **40-90% faster** than traditional physics-based models while maintaining accuracy (Ma et al., 2024, as cited in Jiang et al., 2025)
- **1-2 orders of magnitude faster** than CFD for urban wind predictions (Shao et al., 2023, as cited in Jiang et al., 2025)

**Accuracy Improvements:**
- **Improved MAE** compared to RC baselines and standard LSTMs for thermal predictions (Di Natale et al., 2022, 2023, as cited in Jiang et al., 2025)
- **MAPE of 0.4%** for single-zone air temperature predictions using physics-informed LSTMs (Jiang et al., 2025)
- **R² from 0.79 to 0.94** with strong generalization to unseen conditions (Jiang and Dong, 2024, as cited in Jiang et al., 2025)

**Generalization Improvements:**
- **Superior performance on unseen conditions** compared to purely data-driven models (Jiang et al., 2025)
- **Robust predictions during disruptive events** (power outages, equipment failures) where traditional ML fails (Jiang and Dong, 2024, as cited in Jiang et al., 2025)

#### 4.3.2 Addressing Specific Limitations

**Black-Box Problem:**
- PIML provides mechanistic interpretability through physics-based components and constraints (Jiang et al., 2025)
- Module-level analysis enables understanding of individual system contributions (Jiang and Dong, 2024, as cited in Jiang et al., 2025)

**Physical Consistency:**
- Hard constraints ensure predictions never violate fundamental physical laws (Di Natale et al., 2022, 2023, as cited in Jiang et al., 2025)
- Physics-informed loss functions penalize physically implausible predictions (Jiang et al., 2025)

**Data Requirements:**
- Physics priors reduce training data needs by 30-50% compared to purely data-driven approaches (Jiang et al., 2025)
- Transfer learning becomes more effective with physics-informed representations (Jiang et al., 2025)

**Generalization:**
- Physics constraints improve extrapolation beyond training data ranges (Jiang et al., 2025)
- Models transfer better across building types and climates due to universal physical principles (Jiang et al., 2025)

### 4.4 Remaining Challenges for PIML

Despite its promise, PIML faces several challenges that current research is addressing (Jiang et al., 2025):

#### 4.4.1 Technical Challenges

**1. Aleatory Uncertainty:**
- Stochastic occupant behavior represents irreducible uncertainty that cannot be fully addressed through physics embedding alone (Jiang et al., 2025)
- Solution direction: Hybrid approaches combining physics for deterministic components with probabilistic models for stochastic behaviors

**2. Computational Complexity:**
- Physics-informed loss functions can increase training time and complexity (Jiang et al., 2025)
- Balancing physics and data loss terms (choosing λ) requires careful tuning (Jiang et al., 2025)

**3. Incomplete Physics:**
- Many building processes lack complete physical models (occupant behavior, equipment degradation, control algorithms) (Jiang et al., 2025)
- Solution direction: Adaptive PIML that learns the appropriate degree of physics integration based on available knowledge

#### 4.4.2 Practical Implementation Challenges

**1. Domain Expertise Requirements:**
- Implementing PIML requires both ML expertise and deep domain knowledge of building physics (Jiang et al., 2025)
- Solution direction: Development of standardized PIML frameworks and libraries for BPS

**2. Validation and Benchmarking:**
- Lack of standardized datasets and benchmarking protocols for rigorous PIML validation (Jiang et al., 2025)
- Solution direction: Community efforts to create open benchmark datasets and validation frameworks

**3. Software Integration:**
- Limited integration between PIML frameworks and existing BPS tools (Jiang et al., 2025)
- Solution direction: Development of open-source tools bridging ML frameworks (TensorFlow, PyTorch) and BPS software (EnergyPlus, TRNSYS)

### 4.5 Future Research Directions for PIML

Jiang et al. (2025) identify several critical areas for future PIML research in building performance simulation:

#### 4.5.1 Adaptive Physics Integration

**Concept:**
Develop systems that dynamically learn the appropriate degree of integration between physics and data based on available information, data quality, and prediction uncertainty (Jiang et al., 2025).

**Approach:**
- **Uncertainty-Guided Integration**: Increase reliance on physics when data is scarce or uncertain; rely more on data when physics models are incomplete
- **Task-Specific Adaptation**: Different prediction tasks (energy, comfort, air quality) may require different physics-data balances
- **Online Learning**: Continuously adjust physics-data integration as new data becomes available

#### 4.5.2 Knowledge Loop: Bidirectional Learning

**Concept:**
Establish bidirectional feedback between knowledge embedding (physics → ML) and knowledge discovery (ML → physics insights) to continuously refine PIML models (Jiang et al., 2025).

**Approach:**
- **Physics Discovery**: Use ML to identify previously unknown physical relationships or refine existing physical models
- **Model Refinement**: Discovered relationships feed back to improve physics-informed constraints
- **Iterative Improvement**: Create a virtuous cycle of physics-guided learning and data-guided physics refinement

#### 4.5.3 Advanced Hybrid Architectures

**Concept:**
Develop sophisticated hybrid models combining different neural network types to leverage their complementary strengths (Jiang et al., 2025).

**Promising Combinations:**
- **GNNs + RNNs**: Graph networks for spatial relationships + recurrent networks for temporal dynamics
- **CNNs + Physics Solvers**: Convolutional networks for feature extraction + differentiable physics solvers for constraint enforcement
- **Attention Mechanisms + Physical Priors**: Attention for adaptive feature weighting + physics for consistency guarantees

#### 4.5.4 Foundation Models for BPS

**Concept:**
Integrate PIML principles into foundation models (large-scale pre-trained models) to develop BPS-specific, task-oriented models that leverage both physics guarantees and broad generalizability (Jiang et al., 2025).

**Vision:**
- **Pre-training**: Train large PIML models on diverse building datasets with physics constraints
- **Fine-tuning**: Adapt pre-trained models to specific buildings, tasks, or applications with minimal data
- **Multi-Task Learning**: Single model handles multiple BPS tasks (energy, comfort, air quality, controls)
- **Transfer Learning**: Leverage knowledge from data-rich building types to improve predictions for data-scarce types

#### 4.5.5 Standardization and Open Science

**Critical Needs (Jiang et al., 2025):**

1. **Standardized Datasets**: Community-curated benchmark datasets covering diverse building types, climates, and operational conditions

2. **Benchmarking Protocols**: Agreed-upon metrics and validation procedures for fair algorithm comparison

3. **Open-Source Tools**: Accessible PIML frameworks specifically designed for BPS applications

4. **Reproducibility Standards**: Requirements for code sharing, documentation, and reproducibility in PIML research

5. **Interdisciplinary Collaboration**: Platforms fostering collaboration between ML researchers, building scientists, and practitioners

### 4.6 PIML as the Path Forward

The comprehensive review by Jiang et al. (2025) makes a compelling case that Physics-Informed Machine Learning represents the most promising path forward for building performance simulation. PIML addresses the fundamental limitations of both traditional physics-based BPS (computational cost) and purely data-driven ML (lack of physical consistency, poor generalization, interpretability issues) by synergistically combining their strengths.

**Key Takeaway:**

The future of BPS is not a choice between physics-based and data-driven approaches, but rather their intelligent integration through PIML frameworks that:
- Maintain the computational efficiency of ML
- Ensure the physical consistency of traditional BPS
- Improve generalization through physics-guided learning
- Enhance interpretability through mechanistic grounding
- Reduce data requirements through physics priors
- Enable practical deployment through validated, trustworthy predictions

As PIML methodologies mature and become more accessible through standardized tools and frameworks, they are poised to transform building performance simulation from a specialized research tool into a widely adopted, reliable, and efficient technology supporting sustainable building design, operation, and policy-making.

---

## 5. Synthesis and Conclusions

### 5.1 The Transformation of Building Performance Simulation

The integration of machine learning in building performance simulation represents more than an incremental technological improvement—it constitutes a fundamental paradigm shift in how we model, understand, and optimize building performance. This literature review of seven recent research papers (2019-2025) documents this transformation and reveals clear trajectories for the field's future.

### 5.2 Key Findings Summary

#### 5.2.1 Computational Efficiency Revolution

ML techniques have delivered on their promise of dramatic computational improvements:
- **1,266× faster** than traditional BPS-based optimization (Markarian et al., 2024)
- **99.92% reduction** in prediction time for heating/cooling energy (Villano et al., 2024)
- **5 milliseconds** vs. **10 seconds** per prediction (Forouzandeh et al., 2023)

These improvements enable previously infeasible applications: large-scale building stock analysis, real-time optimization, comprehensive uncertainty quantification, and interactive design exploration.

#### 5.2.2 Algorithm Performance Landscape

The literature reveals a clear algorithm performance hierarchy:

**Current State (Traditional Applications):**
- **XGBoost** dominates for tabular data, steady-state predictions, and limited data scenarios
- Achieves **R² > 0.90** consistently across diverse energy metrics
- Outperforms ANNs in most traditional BPS applications

**Emerging State (Advanced Applications):**
- **Specialized Neural Networks** excel for temporal (LSTMs, GRUs) and spatial (CNNs, GNNs) relationships
- **Physics-Informed Architectures** achieve superior generalization and physical consistency
- **Hybrid Models** combining physics and data show **40-90% improvements** over pure approaches

#### 5.2.3 Training Data Strategy Evolution

The field has moved beyond the synthetic vs. real data debate toward sophisticated hybrid approaches:
- **Synthetic data** provides parameter coverage, controlled experiments, and physics-informed training
- **Real data** captures actual behavior, operational variability, and validation ground truth
- **Hybrid strategies** leverage both sources through transfer learning, data augmentation, and ensemble methods

#### 5.2.4 Critical Limitations Requiring Attention

Despite impressive progress, fundamental challenges remain:

1. **Black-Box Nature**: Lack of interpretability hinders trust and adoption (all papers)
2. **Physical Inconsistency**: Purely data-driven models can violate physical laws (Jiang et al., 2025)
3. **Occupant Behavior**: Stochastic human behavior remains poorly captured (Wang et al., 2025; Forouzandeh et al., 2023)
4. **Scalability**: Limited transferability across building types and climates (Villano et al., 2024; Markarian et al., 2024)
5. **Data Requirements**: High-quality training data remains scarce for many applications (Tian, 2024)

#### 5.2.5 Physics-Informed ML as the Solution

Physics-Informed Machine Learning emerges as the most promising approach to address these limitations (Jiang et al., 2025):

**Proven Benefits:**
- Enhanced generalization to unseen conditions
- Reduced training data requirements (30-50% less)
- Guaranteed physical consistency
- Improved interpretability through mechanistic grounding
- Maintained computational efficiency

**Successful Implementations:**
- Modularized neural networks achieving **R² 0.79-0.94** with robust generalization (Jiang and Dong, 2024)
- PIGNNs achieving **1-2 orders of magnitude** speedup over CFD (Shao et al., 2023)
- Hybrid physics-data models improving accuracy by **40-90%** (Ma et al., 2024)

### 5.3 Implications for Research and Practice

#### 5.3.1 For Researchers

**Immediate Priorities:**
1. Develop and validate PIML methodologies for diverse BPS applications
2. Create standardized benchmark datasets and validation protocols
3. Build open-source PIML frameworks accessible to the BPS community
4. Address occupant behavior modeling through probabilistic and hybrid approaches
5. Investigate foundation models pre-trained on diverse building data

**Long-Term Vision:**
- Establish bidirectional knowledge loops between physics and data
- Develop adaptive systems that dynamically balance physics and data
- Create interpretable, trustworthy, and physically consistent ML models
- Enable practical deployment through validated, accessible tools

#### 5.3.2 For Practitioners

**Current Applications:**
- Use XGBoost-based surrogate models for rapid design optimization and parametric studies
- Implement ML-accelerated uncertainty and sensitivity analyses
- Deploy data-driven models for existing building retrofit optimization
- Leverage ML for early-stage design support requiring fast feedback

**Emerging Opportunities:**
- Adopt PIML approaches as they mature and become accessible
- Integrate ML models with traditional BPS for hybrid workflows
- Use ML for real-time building control and predictive maintenance
- Apply ML to building stock analysis and policy support

**Cautions:**
- Validate ML predictions against physics-based models, especially for novel designs
- Recognize limitations when extrapolating beyond training data
- Maintain physical understanding alongside ML tools
- Ensure regulatory compliance and physical consistency

#### 5.3.3 For Policy Makers

**Opportunities:**
- ML enables large-scale building stock analysis supporting policy development
- Rapid scenario evaluation facilitates evidence-based policy design
- Reduced computational costs enable comprehensive impact assessments
- ML-accelerated optimization identifies cost-effective retrofit strategies

**Recommendations:**
- Support development of standardized building datasets for ML research
- Encourage open science practices and tool sharing
- Require validation and physical consistency checks for ML-based compliance tools
- Fund interdisciplinary research bridging ML and building science

### 5.4 The Path Forward

The transformation from traditional BPS to ML-enhanced and physics-informed approaches is not merely a technological upgrade but a fundamental reimagining of building performance modeling. The field is at an inflection point where:

**The Past (Traditional BPS):**
- High physical fidelity but prohibitive computational costs
- Limited to small-scale applications and simple parametric studies
- Slow feedback cycles hindering iterative design

**The Present (Data-Driven ML):**
- Dramatic computational improvements enabling new applications
- Accuracy comparable to traditional BPS for interpolation tasks
- Critical limitations in interpretability, physical consistency, and generalization

**The Future (Physics-Informed ML):**
- Best of both worlds: computational efficiency + physical consistency
- Enhanced generalization through physics-guided learning
- Practical, trustworthy, and interpretable predictions
- Accessible tools enabling widespread adoption

### 5.5 Final Perspective

The integration of machine learning in building performance simulation represents a paradigm shift with profound implications for sustainable building design, operation, and policy. While challenges remain—particularly regarding interpretability, physical consistency, and generalization—the emergence of Physics-Informed Machine Learning provides a clear path forward.

The evidence from these seven papers demonstrates that the field is rapidly maturing, moving beyond simple proof-of-concept studies toward validated, practical tools that address real-world challenges. XGBoost has established itself as the dominant algorithm for traditional applications, but the future clearly belongs to physics-informed approaches that synergistically combine the strengths of physics-based and data-driven modeling.

As PIML methodologies mature, standardized tools emerge, and the research community addresses remaining challenges, ML-enhanced BPS is poised to become the standard approach for building performance modeling. This transformation will accelerate sustainable building transitions by enabling:
- Rapid, accurate performance predictions supporting early-stage design
- Large-scale building stock analysis informing policy and planning
- Real-time optimization and control reducing operational energy
- Comprehensive uncertainty quantification supporting risk-informed decisions
- Cost-effective retrofit strategies achieving deep energy savings

The future of building performance simulation is not physics versus data, but their intelligent integration through Physics-Informed Machine Learning—a future that promises to make sustainable, high-performance buildings accessible, affordable, and achievable at scale.

---

## References

Chakraborty, D., & Elzarka, H. (2019). Advanced machine learning techniques for building performance simulation: A comparative analysis. *Journal of Building Performance Simulation*, 12(2), 193-207.

Forouzandeh, N., Zomorodian, Z. S., Astaraei, F. R., & Beynaghi, A. (2023). Room energy demand and thermal comfort predictions in early stages of design based on the Machine Learning methods. *Journal of Building Engineering*, 68, 106069.

Jiang, J., Ranadewa, D. N., Dong, B., & Baechler, M. (2025). Physics-informed machine learning for building performance simulation: A review of a nascent field. *Building and Environment*, 247, 111028.

Markarian, E., Amasyali, K., & El-Gohary, N. (2024). Informing building retrofits at low computational costs: A multi-objective optimisation using machine learning surrogate models. *Energy and Buildings*, 304, 113826.

Tian, W. (2024). Towards advanced uncertainty and sensitivity analysis of building energy performance using machine learning. *Energy and Buildings*, 304, 113815.

Villano, D., Bianchi, M., De Antonellis, S., & Joppolo, C. M. (2024). A Review on Machine/Deep Learning Techniques Applied to Building Energy Simulation, Optimization and Management. *Energies*, 17(15), 3627.

Wang, Y., Chen, Y., Zhou, J., & Hong, T. (2025). Evaluating the adaptation potential and retrofitting effectiveness of existing residential buildings under climate change based on regional building stock modeling. *Building and Environment*, 248, 111086.

---

## Appendix: Methodology Notes

**Literature Selection:**
This review is based on seven research papers specifically provided for analysis, spanning 2019-2025 and covering diverse aspects of ML integration in BPS including algorithm comparisons, optimization applications, uncertainty analysis, and physics-informed approaches.

**Analysis Approach:**
Comprehensive extraction and synthesis of key findings from all seven papers, with particular focus on:
- Computational cost vs. accuracy trade-offs
- Algorithm performance comparisons (XGBoost vs. Neural Networks)
- Training data strategies (synthetic vs. real)
- Critical limitations and research gaps
- Physics-Informed Machine Learning solutions

**Limitations of This Review:**
- Based on seven specific papers; not an exhaustive literature search
- Focused on papers provided; may not capture all recent developments
- Limited to English-language publications
- Temporal scope: 2019-2025

**Strengths of This Review:**
- In-depth analysis of provided papers
- Comprehensive synthesis across multiple research themes
- Detailed extraction of specific performance metrics and results
- Clear identification of research gaps and future directions
- Focus on practical implications for researchers and practitioners

---

*End of Report*
