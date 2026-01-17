## Comparative Analysis of Machine Learning Techniques in Building Performance Simulation

### Computational Costs and Time Comparisons
Traditional first-principles-based energy modeling tools, such as DOE-2 and EnergyPlus, are often difficult to use and cost-inefficient, requiring 'tedious expert work' [1]. In contrast, machine learning (ML) techniques have proven to be 'more accurate and quick' for existing buildings with historical time series energy data [1]. Specifically, the Extreme Gradient Boosting (XGBoost) algorithm is highlighted for its speed and efficiency:
- **XGBoost Efficiency**: XGBoost is built with OpenMP support, which enables it to efficiently use all CPU cores in parallel, making it 'extremely fast' during training [2]. It also presorts independent variables at the beginning of the training process, further reducing 'training complexity and computational time' [2].
- **Ensemble Learning Challenges**: Historically, ensemble learning algorithms required 'significantly more computational time and high level of expertise' to combine different base models [1]. However, this research attempts to overcome these limitations using XGBoost [1].

### Accuracy Metrics for ML Algorithms
The performance of the models is evaluated using two primary statistical metrics: Normalized Root Mean Square Error (RN_RMSE) and R² [3]. Lower RN_RMSE values are desirable, while R² values closer to 1 indicate a better fit [3].

#### Performance without Feature Engineering, Selection, and Hyper-parameter Optimization
- **Cooling Electricity**:
  - XGBoost: RN_RMSE of 4.84%, R² of 0.95 [4].
  - ANN: RN_RMSE of 11.72%, R² of 0.68 [4].
  - Degree-day OLS: RN_RMSE of 11.00%, R² of 0.85 [4].
- **Heating Gas**:
  - XGBoost: RN_RMSE of 5.86%, R² of 0.88 [4].
  - ANN: RN_RMSE of 11.04%, R² of 0.57 [4].
  - Degree-day OLS: RN_RMSE of 16.51%, R² of 0.67 [4].

#### Performance with Feature Engineering (without Selection and Hyper-parameter Optimization)
- **Cooling Electricity**:
  - XGBoost: RN_RMSE of 2.95%, R² of 0.98 [5].
  - ANN: RN_RMSE of 6.78%, R² of 0.90 [5].
- **Heating Gas**:
  - XGBoost: RN_RMSE of 3.90%, R² of 0.95 [5].
  - ANN: RN_RMSE of 6.84%, R² of 0.83 [5].

#### Performance with Feature Engineering and Selection (without Hyper-parameter Optimization)
- **Cooling Electricity**:
  - XGBoost: RN_RMSE of 2.98%, R² of 0.98 [6].
  - ANN: RN_RMSE of 4.8%, R² of 0.95 [6].
- **Heating Gas**:
  - XGBoost: RN_RMSE of 4.16%, R² of 0.94 [6].
  - ANN: RN_RMSE of 6.62%, R² of 0.85 [6].

#### Performance with Feature Engineering, Selection, and Hyper-parameter Optimization
- **Cooling Electricity**:
  - XGBoost: RN_RMSE of 2.43%, R² of 0.99 [7].
  - ANN: RN_RMSE of 4.2%, R² of 0.96 [7].
- **Heating Gas**:
  - XGBoost: RN_RMSE of 3.17%, R² of 0.96 [7].
  - ANN: RN_RMSE of 6.16%, R² of 0.87 [7].

#### Performance with Feature Engineering and Hyper-parameter Optimization (without Feature Selection)
- **Cooling Electricity**:
  - XGBoost: RN_RMSE of 2.43%, R² of 0.99 [8].
  - ANN: RN_RMSE of 4.59%, R² of 0.95 [8].
- **Heating Gas**:
  - XGBoost: RN_RMSE of 3.15%, R² of 0.96 [8].
  - ANN: RN_RMSE of 6.80%, R² of 0.84 [8].

### ML Algorithms Tested and Compared
The study tests and compares three machine learning algorithms for predicting cooling electricity and heating gas consumption in a large office building:
- **Extreme Gradient Boosting (XGBoost)**: An ensemble learning algorithm that follows the principle of boosting, combining multiple weak learners (like regression trees) to create a single strong learner [9]. It is noted for its ability to handle feature selection inherently [6].
- **Artificial Neural Networks (ANN)**: Inspired by biological structures, ANNs consist of interconnected neurons arranged in layers (feature, hidden, and response layers) [10].
- **Degree-day-based Ordinary Least Square (OLS) Regression**: A simpler ML algorithm that maps cooling or heating degree-days to energy consumption values [11]. This method does not require feature selection or hyper-parameter tuning [11].

### Training Data Generation
The training data is generated using a synthetic database rather than real measured data. This approach offers several advantages:
- **Synthetic Database**: The study utilized a synthetic database generated from EnergyPlus simulations using a prototype Input Data File (IDF) [12]. This IDF represents a large commercial office building in Chicago, USA [12].
- **Benefits of Synthetic Data**: Synthetic data provides a 'consistent basis for research' and can be generated in 'a matter of minutes', unlike the years required to collect similar data from actual buildings [12]. It also enables data science and ML efforts that might otherwise not proceed due to a lack of access to real data [12].
- **Dataset Details**: The synthetic database contains hourly energy consumption profiles over a four-year period (2012–2015). The hourly data for 2012 is used for training, while data from 2013 to 2015 is used for testing [13].

### Limitations of Black-Box Models and Physical Consistency
The paper acknowledges certain limitations and challenges, particularly concerning ANN and the 'black-box' nature of some models:
- **ANN's 'Black-Box' Nature**: It is difficult to fully understand the real reasons behind ANN's consistently lower accuracy compared to XGBoost, largely due to its 'black-box' nature [14].
- **Data Requirements for ANN**: ANNs typically require a 'large amount of training data' [14]. The study's training set, consisting of one year of hourly data, might be insufficient for ANN to make accurate long-term predictions [14].
- **Hyper-parameter Optimization**: The infinite combinations of hyper-parameter values make total exploration impossible. Data scientists rely on 'greedy techniques' like random search CV. It's possible that the optimal hyper-parameters found might not be the most suitable for an algorithm, though this applies equally to all algorithms compared [14].
- **Physical Consistency**: One possible reason for XGBoost's superior performance is that the 'underlying physics' that the models attempt to capture from the data might be 'especially conducive to the boosting technique' compared to ANN [15].

In summary, this research demonstrates that XGBoost consistently outperforms ANN and degree-day OLS regression in building energy performance simulation, especially when feature engineering, selection, and hyper-parameter optimization steps are included. While ML models offer significant advantages in speed and accuracy over traditional methods, challenges remain in understanding the internal workings of 'black-box' models like ANNs and ensuring optimal performance across various datasets and prediction horizons.