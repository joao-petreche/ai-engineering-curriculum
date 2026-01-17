## Machine Learning for Building Energy and Thermal Comfort Predictions

### Computational Costs and Time Comparisons
Machine Learning (ML) models offer significant reductions in prediction time compared to traditional building energy simulation tools like EnergyPlus. While EnergyPlus typically takes an average of 10 seconds per alternative, optimized ML models complete predictions much faster. For instance, ANNs models are trained in 6 seconds, but other ML models have prediction times under 5 milliseconds. This represents a meaningful reduction in computational cost [1].

### Accuracy Metrics for Machine Learning Algorithms
Several accuracy metrics are used to evaluate the performance of ML models in predicting energy demand and thermal comfort:
-   **R² (Coefficient of Determination)**: This metric indicates how well the model's predictions align with actual values. A higher R² value (closer to 1.0) signifies greater accuracy and similarity between predicted and actual results [2].
    -   For cooling demand, the highest R² was 0.97 for Extremely Randomized Trees (ERT) [3].
    -   For heating demand, the highest R² was 0.84 for Bagging Regressor (BR) [3].
    -   For annual comfort indices, the best models (BR and ERT) achieved R² values between 0.74 and 0.96 [3].
    -   After optimization, R² values for cooling and heating demands increased to 0.85 and 0.66, respectively. The average R² for annual thermal comfort indices ranged from 0.58 to 0.92 [4].
-   **MAE (Mean Absolute Error)**: This metric is commonly used in Decision Tree (DT) and Random Forest (RF) studies. Lower MAE values indicate higher accuracy [2].
-   **MSE (Mean Squared Error)**: Generally used in domains that minimize least-squares, lower MSE values indicate higher accuracy [2].

### Specific ML Algorithms Tested and Their Performance
This study tested seven different ML models, including three single models and four ensemble models, for predicting annual energy demand and thermal comfort [5].
-   **Single Models**: Artificial Neural Networks (ANN), K-Nearest Neighbor (KNN), and Decision Tree (DT) [6].
-   **Ensemble Models**: Adaboost (AB), Random Forest (RF), Extremely Randomized Trees (ERT), and Bagging Regressor (BR) [6].

Performance results for optimized models (based on R²) include:
-   **Extremely Randomized Trees (ERT)**: Achieved the highest R² of 0.99 for cooling demand and 0.57 for heating demand [4].
-   **Random Forest (RF)**: Achieved an R² of 0.80 for cooling demand and 0.85 for heating demand [4].
-   **Artificial Neural Network (ANN)**: Achieved an R² of 0.94 for cooling demand and 0.63 for heating demand [4].
-   **K-Nearest Neighbor (KNN)**: Achieved an R² of 0.87 for cooling demand and 0.66 for heating demand [4].
-   **Bagging**: Achieved an R² of 0.81 for cooling demand and 0.85 for heating demand [4].
-   **Decision Tree**: Achieved an R² of 0.80 for cooling demand and 0.84 for heating demand [4].
-   **Adaboost**: Achieved an R² of 0.73 for cooling demand and 0.24 for heating demand [4].

### Training Data Generation
For this study, the training data was generated using **synthetic simulation data** [7].
-   **Methodology**: 3024 synthetic samples of a single-zone model with seven input features were simulated using the EnergyPlus engine [5]. This process involved calculating the energy demand for each sample via Honeybee, which uses the EnergyPlus engine, based on Tehran's annual weather file [8].
-   **Testing Data**: An additional 360 unseen samples were used as testing data to report accuracy [5].

### Limitations of Black-Box Models and Physical Consistency
The study highlights several limitations related to the application of ML models, particularly in early design stages:
-   **Lack of Explicit Relation**: Implementing ML can be challenging in the design stage because the relationship between inputs and target variables is not explicit [9].
-   **Training Data Challenge**: Preparing sufficient and accurate training data is a significant challenge [9].
-   **Generalizability**: The study's framework is constrained to definite sets of design parameters with specific ranges. A more inclusive framework would need to consider all possible input parameters and value ranges to increase the generalizability of the models and include more complex design options, such as different glazing systems, shadings, and facades [10].
-   **Single Zone Calculation**: The current study was limited to a single-zone calculation, suggesting that building-level frameworks should be studied for broader applicability [11].
-   **Limited Building Types and Weather Conditions**: Other common building types (e.g., residential, educational) and different weather conditions should be included in the training data for a more robust model [11].

In summary, while ML methods offer significant speed advantages and high accuracy for predicting building energy demand and thermal comfort, their effective implementation requires careful consideration of data generation, model optimization, and addressing limitations related to generalizability and physical consistency.