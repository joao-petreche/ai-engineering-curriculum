## Machine Learning in Building Retrofits and Optimization

Machine learning (ML) algorithms are increasingly being adopted in building performance simulation (BPS) to enhance energy prediction capabilities and reduce computational costs. This integration also extends to optimization methods for building design and retrofit strategies, though ML-based BPS surrogates are less frequently employed for this purpose [1].

### Specific Applications of ML
-   **Surrogate Models for Building Performance Simulation (BPS)**: ML algorithms serve as surrogates for BPS models, significantly reducing computational costs while maintaining energy predictive capabilities [1]. These models are trained on data generated from BPS tools like EnergyPlus to accelerate simulations [2].
-   **Retrofit Optimization**: ML-based BPS surrogates are coupled with multi-objective optimization to inform holistic design and operation retrofits at low computational costs [1]. This approach can identify energy-saving measures and improve occupant thermal comfort much faster than traditional BPS-based optimization [1].
-   **Prediction of Building Loads**: Tree-based models, such as gradient-boosted regression trees, have been developed to predict annual heating and cooling loads with high accuracy and low training times [2]. More granular surrogate models, including feedforward neural networks, have also been trained to estimate hourly heating and cooling demands using building features and weather data [2].
-   **Urban-Scale Energy Performance**: Surrogate models trained on large datasets (e.g., one million buildings) are used to predict urban-scale energy performance for retrofit applications [2].
-   **Uncertainty Analysis**: While not explicitly detailed in the provided text for ML, traditional BPS tools are often used for uncertainty analysis in building energy assessment.

### Datasets Used in Studies
-   **Archetypal Office Building in Ottawa, Canada**: The primary case study involves an archetypal office building in Ottawa, Canada, developed using EnergyPlus and adhering to National Energy Code of Canada for Buildings (NECB) guidelines [1] [3].
-   **Parametric Variation**: A dataset was generated through parametric variation of the BPS model, including eleven inputs (X1-X11) and three outputs (Y1-Y3): annual electricity consumption, peak electric load, and Predictive Mean Vote at Standard Effective Temperature (PMVSET) [3] [4].
-   **Sampling Method**: Latin Hypercube Sampling (LHS) was used to generate 500 samples for EnergyPlus simulations, resulting in 8760 data points per run and a total of 4,380,000 data points [4].
-   **Data Sources**: Input parameters were determined from various databases, including internal publications by the National Research Council Canada (NRC), the Building Envelope Thermal Bridging (BETB) guide, fenestration databases (National Fenestration Rating Council), and other research papers on Canadian office building stock [4].

### Performance Metrics and Results for ML Algorithms
-   **Predictive Accuracy**: The developed models achieved competitive predictive accuracies, with adjusted R² values ranging from 0.90 to 0.99 [1].
-   **Specific Model Performance** [5]:
    -   **Annual Electric Load**: Predicted using Linear Regression (LR) with an adjusted R² of 0.90 and a Coefficient of Variation of Root Mean Square Error (CV(RMSE)) of 0.02. Training and testing time was 0.05 seconds.
    -   **Peak Load**: Predicted using Extreme Gradient Boosting (XGB) with an adjusted R² of 0.91 and a CV(RMSE) of 0.03. Training and testing time was 0.09 seconds.
    -   **Hourly PMVSET**: Predicted using Multi-layer Perceptron (MLP) with an adjusted R² of 0.99 and a CV(RMSE) of 0.08. Training and testing time was 470 seconds.
-   **Computational Efficiency**: The ML-based surrogate modeling and optimization approach was 1266 times faster than a traditional BPS-based optimization approach, reducing simulation time from approximately 38 days to 35 minutes for a yearly EnergyPlus simulation of the archetype building [1] [6].
-   **Retrofit Improvements**: Optimal solutions achieved improvements of 14% for peak load, 10% for annual load, and 34% for occupant thermal comfort (PMVSET) compared to base case values [7].

### Future Trends and Recommendations
-   **Expanded Input Database**: Future research should expand the input database to include building material and construction information from local manufacturers and suppliers [8].
-   **Additional Metrics**: Incorporate additional metrics such as natural gas consumption, CO2 emissions, and monetary costs into future studies [8].
-   **Modular and Scalable Approach**: The proposed methodology is a modular and scalable approach that can be further developed and integrated into practitioners' workflows [8].
-   **Further Investigation of HVAC Efficiency**: Parameters related to HVAC component efficiency (e.g., Heating Efficiency - X10) showed high variability, warranting further investigation in future work [6].

### Case Studies or Real-World Implementations
-   **Archetypal Office Building in Ottawa, ON, Canada**: The core of this study is the application and validation of the proposed methodology on an archetypal office building in Ottawa, Canada [1] [9]. The building model was developed using EnergyPlus and validated against a similar building's annual energy use intensity, showing less than 5% variance [3].
-   **Australian Office Buildings**: Bell (2023) surveyed Australian office building stock and developed retrofit strategies using BPS tools, showing 13-45% energy reduction [1]. Daly, Cooper, and Ma (2018) also studied BPS usage for assessing low-performing office buildings in Australia [1].
-   **Cold Regions**: Yang and Liu (2018) investigated the integration of BPS and BIM tools for optimizing office retrofits in colder regions [1].

In summary, the research highlights the significant potential of coupling ML-based surrogate models with multi-objective optimization to achieve rapid and accurate assessments of building retrofits, offering substantial improvements in computational efficiency and performance outcomes for energy and comfort metrics. This approach provides a robust framework for informing building retrofits at low computational costs, particularly for complex scenarios like net-zero energy retrofits [1].