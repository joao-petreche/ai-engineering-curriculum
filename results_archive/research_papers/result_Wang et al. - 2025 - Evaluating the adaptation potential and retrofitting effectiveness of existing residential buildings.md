## Machine Learning in Building Retrofits: Applications, Performance, and Future Directions

### Machine Learning Applications in Building Retrofits and Optimization
Machine Learning (ML) models, including XGBoost (XGB) and Random Forest (RF), are applied to enhance the accuracy of predictions related to building energy consumption and thermal comfort (TC) [1]. These models are particularly useful for capturing non-linear relationships and improving predictive performance [1].

*   **Retrofitting Strategy Optimization**: ML algorithms are used to identify and optimize the most impactful retrofitting strategies (RSs) under various climate projections, evaluating the effectiveness of passive design interventions like external shading and nighttime ventilation (NV) [2].
*   **Multi-Objective Optimization**: Beyond traditional energy efficiency metrics such as Energy Use Intensity (EUI), ML research incorporates human-centric TC indices like the Predicted Mean Vote (PMV) to create a holistic retrofitting framework that balances energy performance with occupant well-being [2] [3].
*   **Model Interpretation**: SHapley Additive exPlanations (SHAP) analysis is employed to interpret ML model outputs, identifying and quantifying the effect of key building design variables on energy use and occupant thermal comfort [1]. This method quantifies the marginal contribution of each input feature to a specific model output based on cooperative game theory principles [4].

### Datasets Used in the Studies
The studies utilize a combination of historical meteorological observations and data from IPCC Global Climate Models (GCMs) to construct robust climate baselines and future projections [5].

*   **Historical Data**: Daily meteorological data from the past decade (2007-2021) serve as the baseline reference period, with hourly measured climate data for the Harbin region from 1949 to 2024 obtained from the China Meteorological Administration (CMA) [6] [7]. This dataset undergoes rigorous quality control and institutional validation.
*   **Future Climate Projections**: Data from the Earth System Grid Federation (ESGF) and multiple GCMs developed under the Coupled Model Intercomparison Project Phase 6 (CMIP6) are processed using Climate Data Operators (CDO) toolkit and Statistical Downscaling (SD) techniques to generate high-resolution weather files for building performance simulations [7]. These projections are based on Shared Socioeconomic Pathway (SSP) scenarios (SSP126, SSP245, SSP370, SSP585) [8].
*   **Building Models**: The study uses representative residential proxy models, statistically classified by parameters such as structural typology, building height, construction period, and insulation performance levels [9]. Parametric geometric models are developed to reflect architectural diversity, incorporating variations in orientation, floor height, and Opening Glass Window Ratio (OGWR) [9].

### Performance Metrics and Results for ML Algorithms
ML models are evaluated using multiple statistical metrics to ensure optimal predictive performance [10].

*   **Metrics**: Mean Squared Error (MSE), Root Mean Squared Error (RMSE), and the Coefficient of Determination (R2) are used for evaluation [10].
*   **Best Performing Models**: For Heating Energy Use Intensity (HEUI), XGBoost achieved an R2 of 0.9887 and an RMSE of 3.86164. For Cooling Energy Use Intensity (CEUI), XGBoost had an R2 of 0.9941 and an RMSE of 0.3086. For total EUI, XGBoost showed an R2 of 0.99203 and an RMSE of 2.63915. For Primary Thermal Comfort (PTC), XGBoost achieved an R2 of 0.89903 and an RMSE of 0.00007. For Secondary Thermal Comfort (STC), Random Forest Deep (RF_D) had an R2 of 0.87035 and an RMSE of 0.00023 [11].

### Future Trends and Recommendations
The research highlights a significant shift in energy demand patterns and the need for adaptive strategies.

*   **Shift to Dual-Peak Energy Demand**: The traditional 'winter-dominated energy consumption model' in severe cold regions is shifting towards a 'dual-peak pattern,' where both winter heating and summer cooling demands become equally critical [12].
*   **Increased Cooling Demand**: While winter warming reduces Heating Energy Use Intensity (HEUI), summer heat events significantly elevate Cooling Energy Use Intensity (CEUI), leading to a rapid rise in cooling loads, especially under high-emission scenarios [13].
*   **Holistic Retrofitting Framework**: The study proposes a comprehensive retrofitting framework that integrates high-performance envelope materials, external shading devices, and nighttime ventilation (NV) [14]. It emphasizes moving beyond winter-centric retrofitting to strategies that optimize year-round energy performance and thermal comfort [14].
*   **Key Recommendations**: 
    *   **Insulation**: Prioritize high-performance insulation materials (IM) to enhance airtightness and thermal resistance, especially in extreme cold regions [15]. However, excessive insulation without proper ventilation and shading can lead to summer overheating [16].
    *   **Shading and Glazing**: Optimize Shading Structure Length (SSL) and use low-Solar Heat Gain Coefficient (SHGC) glazing to reduce solar heat gain and mitigate overheating risks [17].
    *   **Ventilation**: Implement dynamically adjustable Opening Glass Window Ratio (OGWR) and smart window systems to improve natural ventilation and cooling efficiency, supporting occupant comfort [17]. Nighttime ventilation is crucial for releasing accumulated heat [18].
    *   **HVAC Systems**: Incorporate HVAC systems with sufficient capacity redundancy to accommodate extreme weather events and selectively relax thermal comfort thresholds in non-core areas to reduce overall EUI [19].

### Specific Case Studies or Real-World Implementations
While the paper discusses a general approach and uses Harbin, China, as a specific severe cold region for its climate projections, it does not detail specific case studies of real-world retrofitting projects or their implementations. Instead, it focuses on simulation-based evaluations and proposes a framework for future application [20].

In summary, the research underscores the growing importance of ML in predicting and optimizing building performance under climate change. It highlights the necessity of integrated, adaptive retrofitting strategies that balance energy efficiency and thermal comfort year-round, moving away from purely winter-focused approaches, particularly in severe cold regions facing increasing summer overheating challenges.