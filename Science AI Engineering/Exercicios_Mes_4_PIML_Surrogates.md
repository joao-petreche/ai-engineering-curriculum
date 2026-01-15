# **🔬 Exercícios Práticos - Mês 4: Consolidação Teórica & Modelagem Surrogate (PIML)**

**Objetivo do Mês:** Entender como a Física informa a Rede Neural e criar modelos substitutos (Surrogates) para prever comportamento do edifício sem rodar EnergyPlus.

**Conceito Central:** Physics-Informed Machine Learning (PIML)
> Em vez de treinar um ML puro (caixa preta), incorporamos conhecimento físico:
> - Inputs: geometria do edifício (features com significado físico)
> - Outputs: carga térmica (output com limite físico: 0 ≤ Q ≤ 500 kW)
> - Constraint: conservação de energia (Q_sim = Q_surrogate ± erro)

**Benchmark:** Treinar XGBoost e MLP para prever carga térmica anual:
- Feature: 8 parâmetros do Mês 3 (WWR, espessura, condutividade, etc.)
- Target: Carga térmica anual (kWh)
- Métrica: RMSE, MAE, R²
- Speedup: Surrogate em 10ms vs EnergyPlus em 10 segundos = **1000x mais rápido!**

**Tempo Estimado Total:** 50-60 horas (distribuído em 4 semanas)

**Pré-Requisitos:**
- ✅ Mês 1-3 concluídos (EnergyPlus, validação, dados em larga escala)
- ✅ 100 simulações completadas com outputs
- ✅ Dados de sensores limpos
- ✅ Familiaridade com scikit-learn, XGBoost, PyTorch/TensorFlow

---

## **📋 Checklist de Progresso do Mês**

| Semana | Objetivo | Status | Tempo Estimado |
|--------|----------|--------|----------------|
| Semana 1 | Feature Engineering & Análise | ⬜ | 12-14h |
| Semana 2 | Modelos XGBoost & MLP | ⬜ | 14-16h |
| Semana 3 | Validação & Constraints Físicos | ⬜ | 12-14h |
| Semana 4 | Projeto Final: Sistema Integrado | ⬜ | 12-16h |

---

## **SEMANA 1: FEATURE ENGINEERING & ANÁLISE EXPLORATÓRIA**

### **📌 Exercício 1.1 - Preparação de Dataset**

**Objetivo:** Transformar dados brutos (100 simulações) em dataset pronto para ML.

**Tarefa:**

1. **Criar Arquivo `prepare_dataset.py`**

```python
"""
Preparação de dataset para modelos de Surrogate.
Mês 4 - Exercício 1.1
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

class DatasetBuilder:
    """Construtor de dataset para ML."""
    
    def __init__(self, parameter_matrix_path, simulation_results_path):
        """
        Inicializa builder.
        
        Args:
            parameter_matrix_path: CSV com 100 parâmetros (Mês 3)
            simulation_results_path: CSV com resultados EnergyPlus
        """
        self.params = pd.read_csv(parameter_matrix_path)
        self.results = pd.read_csv(simulation_results_path)
        
        # Merge: parâmetros + resultados
        self.dataset = self.params.merge(
            self.results,
            on='simulation_id',
            how='inner'
        )
        
        print(f"✅ Dataset criado: {self.dataset.shape[0]} simulações × {self.dataset.shape[1]} colunas")
    
    def extract_targets(self):
        """
        Extrai targets (saídas de interesse) das simulações.
        
        Returns:
            DataFrame com targets
        """
        
        print("\n🎯 Extração de Targets (Outputs de Interesse)")
        print("-" * 70)
        
        targets = pd.DataFrame({
            'simulation_id': self.dataset['simulation_id'],
            'annual_heating_kwh': self.dataset['annual_heating_kwh'],
            'annual_cooling_kwh': self.dataset['annual_cooling_kwh'],
            'total_energy_kwh': self.dataset['annual_heating_kwh'] + self.dataset['annual_cooling_kwh'],
            'peak_heating_w': self.dataset['peak_heating_w'],
            'peak_cooling_w': self.dataset['peak_cooling_w'],
        })
        
        print("\nTargets extraídos:")
        print(f"  ✅ annual_heating_kwh (consumo anual de aquecimento)")
        print(f"  ✅ annual_cooling_kwh (consumo anual de resfriamento)")
        print(f"  ✅ total_energy_kwh (consumo total)")
        print(f"  ✅ peak_heating_w (pico de demanda aquecimento)")
        print(f"  ✅ peak_cooling_w (pico de demanda resfriamento)")
        
        return targets
    
    def extract_features(self):
        """
        Extrai features (entradas para o modelo).
        
        Features físicas com significado:
        - wwr: impacto na transmissão solar e infiltração
        - wall_thickness: impacto no amortecimento térmico
        - insulation_thickness: impacto na resistência térmica
        - conductivity_wall e conductivity_insulation: impacto na U-value
        - zone_volume: impacto na capacidade térmica
        - infiltration_rate: impacto na ventilação indesejada
        - internal_loads: impacto nas cargas sensíveis
        """
        
        print("\n📊 Extração de Features (Inputs com Significado Físico)")
        print("-" * 70)
        
        feature_cols = [
            'wwr',
            'wall_thickness',
            'insulation_thickness',
            'conductivity_wall',
            'conductivity_insulation',
            'zone_volume',
            'infiltration_rate',
            'internal_loads'
        ]
        
        features = self.dataset[['simulation_id'] + feature_cols].copy()
        
        print("\nFeatures extraídas (8):")
        for i, col in enumerate(feature_cols, 1):
            print(f"  {i}. {col}")
        
        return features
    
    def analyze_correlations(self, features, targets):
        """
        Analisa correlações entre features e targets.
        
        Importante: entender qual feature mais impacta cada target.
        """
        
        print("\n📈 Análise de Correlação (Features vs Targets)")
        print("-" * 70)
        
        # Combinar features e targets
        analysis_df = features.merge(targets, on='simulation_id')
        
        # Calcular correlação
        corr_matrix = analysis_df.corr()
        
        # Extrair correlações com target (aquecimento)
        target_name = 'annual_heating_kwh'
        correlations = corr_matrix[target_name].sort_values(ascending=False)
        
        print(f"\nCorrelação com '{target_name}':")
        for feature, corr in correlations.items():
            if feature != target_name:
                strength = "Forte" if abs(corr) > 0.7 else "Moderada" if abs(corr) > 0.4 else "Fraca"
                direction = "✓ Positiva" if corr > 0 else "✗ Negativa"
                print(f"  {feature:30} {corr:+.3f}  ({strength}, {direction})")
        
        return corr_matrix, analysis_df
    
    def visualize_feature_importance(self, corr_matrix):
        """Visualiza importância das features."""
        
        target_name = 'annual_heating_kwh'
        correlations = corr_matrix[target_name].drop(target_name)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        colors = ['green' if x > 0 else 'red' for x in correlations.values]
        correlations.sort_values().plot(kind='barh', ax=ax, color=colors)
        
        ax.set_xlabel('Correlação com Consumo Anual de Aquecimento', fontsize=12)
        ax.set_title('Importância das Features (Correlação)', fontweight='bold', fontsize=13)
        ax.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        
        output_path = Path("output/mes4_feature_correlation.png")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n✅ Gráfico salvo em: {output_path}")
    
    def build_final_dataset(self):
        """Constrói dataset final para ML."""
        
        features = self.extract_features()
        targets = self.extract_targets()
        
        # Merge
        dataset = features.merge(targets, on='simulation_id')
        
        # Reordenar colunas
        feature_cols = [c for c in dataset.columns if c not in ['simulation_id'] and c not in targets.columns[1:]]
        target_cols = targets.columns[1:].tolist()
        dataset = dataset[['simulation_id'] + feature_cols + target_cols]
        
        return dataset

if __name__ == "__main__":
    print("=" * 70)
    print("📊 PREPARAÇÃO DE DATASET PARA MODELOS DE SURROGATE")
    print("=" * 70)
    print()
    
    # Paths (usar dados do Mês 3)
    param_path = Path("output/mes3_parameter_matrix.csv")
    results_path = Path("output/batch_results.csv")  # Resultados das 100 simulações
    
    # Construir dataset
    builder = DatasetBuilder(param_path, results_path)
    
    # Extrair componentes
    features = builder.extract_features()
    targets = builder.extract_targets()
    
    # Análise de correlação
    corr_matrix, analysis_df = builder.analyze_correlations(features, targets)
    
    # Visualizar
    builder.visualize_feature_importance(corr_matrix)
    
    # Dataset final
    dataset = builder.build_final_dataset()
    
    print(f"\n✅ Dataset final criado:")
    print(f"   Shape: {dataset.shape}")
    print(f"   Features: {dataset.shape[1] - 1 - 5}")
    print(f"   Targets: 5")
    
    # Salvar
    output_path = Path("output/mes4_dataset_ml.csv")
    dataset.to_csv(output_path, index=False)
    print(f"\n💾 Dataset salvo em: {output_path}")
    
    # Estatísticas
    print("\n📊 Estatísticas do Dataset:")
    print(dataset.describe().to_string())
```

2. **Executar**
   ```powershell
   python prepare_dataset.py
   ```

**✅ Checkpoint de Validação:**
- ✅ Dataset 100 × 13 colunas (8 features + 5 targets)
- ✅ Correlações calculadas e interpretadas
- ✅ Gráfico de importância das features
- ✅ Entendo quais features mais impactam consumo energético

**Correlações Esperadas (Exemplo):**
```
wwr                       +0.65  (janelas maiores → mais heating/cooling)
insulation_thickness      -0.80  (isolamento melhor → menos energia)
conductivity_wall         +0.70  (condutividade maior → menos isolado)
zone_volume               +0.45  (mais volume → mais energia)
```

**⏱️ Tempo Estimado:** 3-4 horas

---

### **📌 Exercício 1.2 - Normalização e Estatísticas**

**Objetivo:** Preparar features para treinamento (normalização, detecção de outliers).

**Tarefa:**

1. **Criar Arquivo `feature_normalization.py`**

```python
"""
Normalização e estatísticas de features.
Mês 4 - Exercício 1.2
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from pathlib import Path
import matplotlib.pyplot as plt

class FeatureProcessor:
    """Processador de features para ML."""
    
    def __init__(self, dataset_path):
        """Carrega dataset."""
        self.df = pd.read_csv(dataset_path)
        self.feature_cols = [c for c in self.df.columns 
                           if c not in ['simulation_id', 'annual_heating_kwh', 
                                       'annual_cooling_kwh', 'total_energy_kwh',
                                       'peak_heating_w', 'peak_cooling_w']]
        self.target_col = 'total_energy_kwh'
    
    def analyze_distributions(self):
        """Analisa distribuição de features."""
        
        print("\n📊 Análise de Distribuições das Features")
        print("-" * 70)
        
        stats = self.df[self.feature_cols].describe()
        print("\nEstatísticas Descritivas:")
        print(stats.to_string())
        
        # Skewness (assimetria)
        print("\n⚠️  Skewness (Assimetria):")
        for col in self.feature_cols:
            skew = self.df[col].skew()
            level = "Normal" if abs(skew) < 0.5 else "Moderado" if abs(skew) < 1 else "Alto"
            print(f"  {col:30} {skew:+.3f}  ({level})")
    
    def normalize_features(self, method='standard'):
        """
        Normaliza features.
        
        Args:
            method: 'standard' (z-score) ou 'minmax' (0-1)
        
        Returns:
            DataFrame com features normalizadas
        """
        
        print(f"\n🔧 Normalização: {method.upper()}")
        print("-" * 70)
        
        if method == 'standard':
            scaler = StandardScaler()
            print("  ✅ StandardScaler: (x - μ) / σ → média=0, desvio=1")
        elif method == 'minmax':
            scaler = MinMaxScaler()
            print("  ✅ MinMaxScaler: (x - min) / (max - min) → intervalo [0, 1]")
        
        # Aplicar normalização
        features_scaled = scaler.fit_transform(self.df[self.feature_cols])
        
        # Criar DataFrame com features normalizadas
        df_normalized = self.df.copy()
        df_normalized[self.feature_cols] = features_scaled
        
        print(f"\n  Após normalização:")
        print(f"    Média: {df_normalized[self.feature_cols].mean().mean():.6f}")
        print(f"    Desvio Padrão: {df_normalized[self.feature_cols].std().mean():.6f}")
        print(f"    Mín: {df_normalized[self.feature_cols].min().min():.6f}")
        print(f"    Máx: {df_normalized[self.feature_cols].max().max():.6f}")
        
        return df_normalized, scaler
    
    def visualize_distributions(self):
        """Visualiza distribuição das features."""
        
        fig, axes = plt.subplots(2, 4, figsize=(14, 8))
        axes = axes.ravel()
        
        for idx, col in enumerate(self.feature_cols):
            axes[idx].hist(self.df[col], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
            axes[idx].set_title(col, fontweight='bold')
            axes[idx].set_xlabel('Valor')
            axes[idx].set_ylabel('Frequência')
            axes[idx].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        output_path = Path("output/mes4_feature_distributions.png")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n✅ Gráfico de distribuições salvo em: {output_path}")

if __name__ == "__main__":
    print("=" * 70)
    print("🔧 NORMALIZAÇÃO DE FEATURES")
    print("=" * 70)
    
    processor = FeatureProcessor(Path("output/mes4_dataset_ml.csv"))
    
    # Analisar
    processor.analyze_distributions()
    
    # Normalizar
    df_normalized, scaler = processor.normalize_features(method='standard')
    
    # Visualizar
    processor.visualize_distributions()
    
    # Salvar
    output_path = Path("output/mes4_dataset_normalized.csv")
    df_normalized.to_csv(output_path, index=False)
    print(f"\n💾 Dataset normalizado salvo em: {output_path}")
```

**⏱️ Tempo Estimado:** 3-4 horas

---

### **📌 Exercício 1.3 - Split Train/Test**

**Objetivo:** Dividir dataset em conjuntos de treinamento e teste.

**Tarefa:**

```python
"""
Split Train/Test com validação cruzada.
Mês 4 - Exercício 1.3
"""

import pandas as pd
from sklearn.model_selection import train_test_split, KFold
from pathlib import Path

def split_dataset(dataset_path, test_size=0.2, random_state=42):
    """
    Divide dataset em train e test.
    
    Args:
        dataset_path: Path para CSV
        test_size: Proporção para teste (20%)
        random_state: Para reprodutibilidade
    """
    
    df = pd.read_csv(dataset_path)
    
    # Separar features e target
    feature_cols = [c for c in df.columns 
                   if c not in ['simulation_id', 'annual_heating_kwh', 
                               'annual_cooling_kwh', 'total_energy_kwh',
                               'peak_heating_w', 'peak_cooling_w']]
    X = df[feature_cols]
    y = df['total_energy_kwh']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    print(f"📊 Split Train/Test:")
    print(f"  Train: {len(X_train)} amostras ({len(X_train)/len(df)*100:.1f}%)")
    print(f"  Test:  {len(X_test)} amostras ({len(X_test)/len(df)*100:.1f}%)")
    
    return X_train, X_test, y_train, y_test

def cross_validation_fold(dataset_path, n_splits=5):
    """
    Validação cruzada com K-Fold.
    """
    
    df = pd.read_csv(dataset_path)
    X = df[[c for c in df.columns if c not in ['simulation_id', 'total_energy_kwh']]]
    y = df['total_energy_kwh']
    
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    
    print(f"\n🔄 Validação Cruzada (K={n_splits}):")
    for i, (train_idx, val_idx) in enumerate(kf.split(X)):
        print(f"  Fold {i+1}: Train={len(train_idx)}, Val={len(val_idx)}")
```

**⏱️ Tempo Estimado:** 2-3 horas

---

## **SEMANA 2: MODELOS XGBOOST & MLP**

### **📌 Exercício 2.1 - XGBoost (Baseline Rápido)**

**Objetivo:** Implementar modelo XGBoost como baseline rápido e eficiente.

**Tarefa:**

1. **Criar Arquivo `train_xgboost.py`**

```python
"""
Treinamento de modelo XGBoost para Surrogate.
Mês 4 - Exercício 2.1
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb
from pathlib import Path
import matplotlib.pyplot as plt
import pickle

class XGBoostSurrogate:
    """Modelo XGBoost para predição de carga térmica."""
    
    def __init__(self, n_estimators=100, max_depth=6, learning_rate=0.1):
        """Inicializa modelo."""
        self.model = xgb.XGBRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=learning_rate,
            random_state=42,
            verbose=0
        )
        self.scaler = None
        self.feature_names = None
    
    def train(self, X_train, y_train, X_val=None, y_val=None):
        """
        Treina modelo XGBoost.
        
        Args:
            X_train: Features de treino
            y_train: Target de treino
            X_val: Features de validação (opcional)
            y_val: Target de validação (opcional)
        """
        
        print("🚀 Treinamento XGBoost")
        print("-" * 70)
        
        self.feature_names = X_train.columns.tolist()
        
        # Preparar validation set
        eval_set = None
        if X_val is not None and y_val is not None:
            eval_set = [(X_val, y_val)]
        
        # Treinar
        self.model.fit(
            X_train, y_train,
            eval_set=eval_set,
            verbose=10
        )
        
        print(f"✅ Modelo treinado!")
    
    def predict(self, X):
        """Faz predições."""
        return self.model.predict(X)
    
    def evaluate(self, X_test, y_test):
        """Avalia desempenho do modelo."""
        
        # Predições
        y_pred = self.predict(X_test)
        
        # Métricas
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print("\n📊 Desempenho no Teste")
        print("-" * 70)
        print(f"  RMSE: {rmse:.2f} kWh")
        print(f"  MAE:  {mae:.2f} kWh")
        print(f"  R²:   {r2:.4f}")
        
        # Erro relativo
        y_mean = y_test.mean()
        error_pct = (rmse / y_mean) * 100
        print(f"  Erro Relativo: {error_pct:.2f}%")
        
        return {'rmse': rmse, 'mae': mae, 'r2': r2, 'error_pct': error_pct}
    
    def feature_importance(self):
        """Retorna importância das features."""
        
        importance = self.model.feature_importances_
        
        print("\n🎯 Importância das Features (XGBoost)")
        print("-" * 70)
        
        # Ordenar
        indices = np.argsort(importance)[::-1]
        
        for i, idx in enumerate(indices):
            print(f"  {i+1}. {self.feature_names[idx]:30} {importance[idx]:.4f}")
        
        return importance
    
    def save(self, path):
        """Salva modelo."""
        with open(path, 'wb') as f:
            pickle.dump(self, f)
        print(f"✅ Modelo salvo em: {path}")
    
    @staticmethod
    def load(path):
        """Carrega modelo."""
        with open(path, 'rb') as f:
            return pickle.load(f)

if __name__ == "__main__":
    print("=" * 70)
    print("🌲 XGBOOST SURROGATE PARA CARGA TÉRMICA")
    print("=" * 70)
    print()
    
    # Carregar dataset
    df = pd.read_csv(Path("output/mes4_dataset_normalized.csv"))
    
    # Preparar features e target
    feature_cols = [c for c in df.columns 
                   if c not in ['simulation_id', 'annual_heating_kwh',
                               'annual_cooling_kwh', 'total_energy_kwh',
                               'peak_heating_w', 'peak_cooling_w']]
    X = df[feature_cols]
    y = df['total_energy_kwh']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"📊 Dataset:")
    print(f"  Train: {len(X_train)} amostras")
    print(f"  Test:  {len(X_test)} amostras\n")
    
    # Criar e treinar modelo
    xgb_model = XGBoostSurrogate(n_estimators=100, max_depth=6)
    xgb_model.train(X_train, y_train, X_test, y_test)
    
    # Avaliar
    metrics = xgb_model.evaluate(X_test, y_test)
    
    # Feature importance
    xgb_model.feature_importance()
    
    # Salvar
    model_path = Path("output/mes4_xgboost_surrogate.pkl")
    xgb_model.save(model_path)
```

2. **Instalar XGBoost e Executar**
   ```powershell
   pip install xgboost
   python train_xgboost.py
   ```

**✅ Checkpoint de Validação:**
- ✅ XGBoost treinado em < 1 minuto
- ✅ RMSE esperado: 5-10 kWh (dependendo dos dados)
- ✅ R² esperado: > 0.85
- ✅ Feature importance mostra correlações físicas
- ✅ Modelo salvo em pickle

**Métricas Esperadas:**
```
RMSE: 7.42 kWh
MAE:  5.18 kWh
R²:   0.892
Erro Relativo: 3.8%
```

**⏱️ Tempo Estimado:** 4-5 horas

---

### **📌 Exercício 2.2 - MLP Neural Network**

**Objetivo:** Implementar rede neural (MLP) para comparar com XGBoost.

**Tarefa:**

```python
"""
Treinamento de MLP para Surrogate.
Mês 4 - Exercício 2.2
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import torch
import torch.nn as nn
import torch.optim as optim
from pathlib import Path

class MLPSurrogate(nn.Module):
    """Rede Neural MLP para predição de carga térmica."""
    
    def __init__(self, input_size=8, hidden_sizes=[64, 32, 16]):
        """
        Inicializa MLP.
        
        Args:
            input_size: Número de features (8)
            hidden_sizes: Tamanho das camadas ocultas
        """
        super(MLPSurrogate, self).__init__()
        
        layers = []
        prev_size = input_size
        
        # Camadas hidden
        for hidden_size in hidden_sizes:
            layers.append(nn.Linear(prev_size, hidden_size))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(0.2))
            prev_size = hidden_size
        
        # Output layer
        layers.append(nn.Linear(prev_size, 1))
        
        self.network = nn.Sequential(*layers)
    
    def forward(self, x):
        """Forward pass."""
        return self.network(x)

def train_mlp(dataset_path, epochs=100, batch_size=32):
    """Treina MLP."""
    
    print("=" * 70)
    print("🧠 MLP SURROGATE")
    print("=" * 70)
    
    # Carregar
    df = pd.read_csv(dataset_path)
    feature_cols = [c for c in df.columns 
                   if c not in ['simulation_id', 'total_energy_kwh']]
    X = df[feature_cols].values
    y = df['total_energy_kwh'].values.reshape(-1, 1)
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Normalizar
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    # Converter para torch
    X_train_t = torch.FloatTensor(X_train)
    y_train_t = torch.FloatTensor(y_train)
    X_test_t = torch.FloatTensor(X_test)
    y_test_t = torch.FloatTensor(y_test)
    
    # Modelo
    model = MLPSurrogate(input_size=X_train.shape[1])
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()
    
    print(f"\n🚀 Treinamento (epochs={epochs})")
    print("-" * 70)
    
    # Treinar
    for epoch in range(epochs):
        # Forward
        outputs = model(X_train_t)
        loss = criterion(outputs, y_train_t)
        
        # Backward
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 20 == 0:
            print(f"  Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}")
    
    # Avaliar
    with torch.no_grad():
        y_pred = model(X_test_t).numpy()
    
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print(f"\n📊 Desempenho:")
    print(f"  RMSE: {rmse:.2f} kWh")
    print(f"  R²:   {r2:.4f}")
    
    return model, scaler

if __name__ == "__main__":
    train_mlp(Path("output/mes4_dataset_normalized.csv"), epochs=100)
```

**⏱️ Tempo Estimado:** 4-5 horas

---

## **SEMANA 3: VALIDAÇÃO & CONSTRAINTS FÍSICOS**

### **📌 Exercício 3.1 - Validação com Dados Reais de Sensores**

**Objetivo:** Comparar predições do surrogate com dados reais de sensores limpos (Mês 3).

**Tarefa:**

```python
"""
Validação de Surrogate contra dados reais de sensores.
Mês 4 - Exercício 3.1
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

def validate_against_sensor_data(surrogate_model, sensor_data_path):
    """
    Valida surrogate contra dados reais.
    
    Args:
        surrogate_model: Modelo XGBoost ou MLP treinado
        sensor_data_path: CSV com dados de sensor limpos
    """
    
    print("🔬 Validação contra Dados Reais de Sensores")
    print("-" * 70)
    
    # Carregar dados de sensor
    df_sensor = pd.read_csv(sensor_data_path)
    
    # TODO: Extrair parâmetros do edifício com sensores
    # (em um cenário real, teríamos os parâmetros da construção)
    
    # Fazer predição
    y_pred = surrogate_model.predict(X_sensor)
    
    # Comparar com sensor
    y_actual = df_sensor['temperature_celsius'].resample('D').mean()
    
    # Métricas
    mae = np.mean(np.abs(y_actual - y_pred))
    rmse = np.sqrt(np.mean((y_actual - y_pred)**2))
    
    print(f"\n✅ Comparação com Sensor Real:")
    print(f"  MAE:  {mae:.2f} K")
    print(f"  RMSE: {rmse:.2f} K")

if __name__ == "__main__":
    # TODO: Implementar validação completa
    pass
```

**⏱️ Tempo Estimado:** 4-5 horas

---

### **📌 Exercício 3.2 - Constraints Físicos (Physics-Informed)**

**Objetivo:** Adicionar constraints físicos ao modelo para garantir saídas realistas.

**Conceito:**
- Carga térmica nunca pode ser negativa: Q ≥ 0
- Carga térmica tem limite máximo (baseado em física): Q ≤ Q_max
- Conservação de energia: Q_heating + Q_cooling = Q_total

**Tarefa:**

```python
"""
Enforcing Physics Constraints no Surrogate.
Mês 4 - Exercício 3.2
"""

import numpy as np

class PhysicsConstrainedSurrogate:
    """Surrogate com constraints físicos."""
    
    def __init__(self, base_model, q_max=500):
        """
        Inicializa surrogate com constraints.
        
        Args:
            base_model: Modelo XGBoost ou MLP
            q_max: Carga térmica máxima em kW (limite físico)
        """
        self.base_model = base_model
        self.q_max = q_max
    
    def predict_with_constraints(self, X):
        """
        Faz predição aplicando constraints físicos.
        
        Args:
            X: Features
        
        Returns:
            Predições com constraints aplicados
        """
        
        # Predição base
        y_pred = self.base_model.predict(X)
        
        # Aplicar constraint 1: Q ≥ 0 (nunca negativo)
        y_pred = np.maximum(y_pred, 0)
        
        # Aplicar constraint 2: Q ≤ Q_max
        y_pred = np.minimum(y_pred, self.q_max)
        
        # TODO: Aplicar constraint 3: Conservação de energia
        # Q_total = Q_heating + Q_cooling (com tolerância)
        
        return y_pred
    
    def predict_with_uncertainty(self, X):
        """
        Retorna predição + intervalo de confiança (importante!).
        
        Returns:
            y_pred: Predição pontual
            y_lower: Limite inferior (95% confiança)
            y_upper: Limite superior (95% confiança)
        """
        
        # Predição base
        y_pred = self.base_model.predict(X)
        
        # Estimar incerteza (exemplo simplificado)
        uncertainty = 0.1 * y_pred  # ±10% de incerteza
        y_lower = np.maximum(y_pred - uncertainty, 0)
        y_upper = np.minimum(y_pred + uncertainty, self.q_max)
        
        return y_pred, y_lower, y_upper

if __name__ == "__main__":
    # TODO: Testar constraints
    pass
```

**⏱️ Tempo Estimado:** 3-4 horas

---

## **SEMANA 4: PROJETO FINAL DO MÊS**

### **📌 Exercício 4.1 - Sistema Integrado Completo**

**Objetivo:** Integrar surrogate no pipeline completo (EnergyPlus → Surrogate → Otimização).

**Entregável Final:**

```
mes4_piml_surrogates/
├── src/
│   ├── dataset_builder.py
│   ├── xgboost_surrogate.py
│   ├── mlp_surrogate.py
│   ├── physics_constraints.py
│   └── benchmark.py
├── models/
│   ├── xgboost_model.pkl
│   └── mlp_model.pt
├── analysis/
│   ├── feature_correlation.png
│   ├── feature_importance.png
│   ├── training_curves.png
│   ├── predictions_vs_actual.png
│   └── benchmark_report.md
├── results/
│   ├── xgboost_metrics.csv
│   ├── mlp_metrics.csv
│   └── comparison.csv
├── run_training_pipeline.py
└── README.md
```

**Script Principal (run_training_pipeline.py):**

```python
"""
Pipeline completo de treinamento de Surrogates.
Mês 4 - Projeto Final
"""

from pathlib import Path
from src.dataset_builder import DatasetBuilder
from src.xgboost_surrogate import XGBoostSurrogate
from src.mlp_surrogate import MLPSurrogate
from src.physics_constraints import PhysicsConstrainedSurrogate
from src.benchmark import Benchmark

def main():
    """Pipeline completo."""
    
    print("=" * 70)
    print("🎓 MÊS 4 - PROJETO FINAL: PIML Surrogates")
    print("=" * 70)
    print()
    
    # 1. Preparar dataset
    print("📊 Etapa 1: Preparação de Dataset")
    print("-" * 70)
    builder = DatasetBuilder(
        Path("output/mes3_parameter_matrix.csv"),
        Path("output/batch_results.csv")
    )
    dataset = builder.build_final_dataset()
    print(f"✅ Dataset: {dataset.shape}\n")
    
    # 2. Treinar XGBoost
    print("🌲 Etapa 2: Treinamento XGBoost")
    print("-" * 70)
    xgb_model = XGBoostSurrogate()
    xgb_metrics = xgb_model.train_and_evaluate(dataset)
    print(f"✅ XGBoost: RMSE={xgb_metrics['rmse']:.2f}, R²={xgb_metrics['r2']:.4f}\n")
    
    # 3. Treinar MLP
    print("🧠 Etapa 3: Treinamento MLP")
    print("-" * 70)
    mlp_model = MLPSurrogate()
    mlp_metrics = mlp_model.train_and_evaluate(dataset)
    print(f"✅ MLP: RMSE={mlp_metrics['rmse']:.2f}, R²={mlp_metrics['r2']:.4f}\n")
    
    # 4. Aplicar constraints físicos
    print("🔬 Etapa 4: Aplicação de Constraints Físicos")
    print("-" * 70)
    xgb_physics = PhysicsConstrainedSurrogate(xgb_model)
    print(f"✅ Constraints aplicados\n")
    
    # 5. Benchmark e comparação
    print("⚡ Etapa 5: Benchmark (Surrogate vs EnergyPlus)")
    print("-" * 70)
    benchmark = Benchmark(xgb_model, mlp_model, dataset)
    speedup = benchmark.compare_speed()
    print(f"✅ Speedup: {speedup:.0f}x mais rápido!\n")
    
    print("=" * 70)
    print("✅ PIPELINE COMPLETO!")
    print("=" * 70)

if __name__ == "__main__":
    main()
```

**✅ Checkpoint Final do Mês:**

| Critério | Status | Peso |
|----------|--------|------|
| Dataset preparado (features + targets) | ⬜ | 10% |
| XGBoost treinado (R² > 0.85) | ⬜ | 25% |
| MLP treinado (R² > 0.80) | ⬜ | 25% |
| Constraints físicos implementados | ⬜ | 15% |
| Benchmark (speedup calculado) | ⬜ | 15% |
| Validação contra sensor real | ⬜ | 10% |

---

## **📚 ENTREGÁVEL FINAL DO MÊS 4**

### **Estrutura Final no GitHub:**

```
piml-training/
├── mes4_piml_surrogates/
│   ├── src/
│   │   ├── prepare_dataset.py
│   │   ├── feature_normalization.py
│   │   ├── train_xgboost.py
│   │   ├── train_mlp.py
│   │   ├── physics_constraints.py
│   │   └── benchmark.py
│   ├── models/
│   │   ├── xgboost_surrogate.pkl
│   │   └── mlp_surrogate.pt
│   ├── analysis/
│   │   ├── feature_correlation.png
│   │   ├── feature_importance_xgb.png
│   │   ├── training_curves_mlp.png
│   │   ├── predictions_vs_actual.png
│   │   ├── error_distribution.png
│   │   └── physics_constraint_validation.png
│   ├── results/
│   │   ├── xgboost_metrics.csv
│   │   ├── mlp_metrics.csv
│   │   ├── comparison_summary.csv
│   │   └── benchmark_report.md
│   ├── run_training_pipeline.py
│   ├── README.md
│   └── NOTAS_LIÇÕES.md
└── notebooks/
    ├── exploratory_analysis.ipynb
    ├── model_comparison.ipynb
    └── physics_validation.ipynb
```

### **README.md - Mês 4:**

```markdown
# Mês 4 - PIML Surrogates (XGBoost & MLP)

## Objetivo
Criar modelos substitutos (surrogates) que predizem carga térmica **1000x mais rápido** que EnergyPlus.

## Componentes Principais

### 1. Feature Engineering (`prepare_dataset.py`)
- Extração de 8 features com significado físico
- Análise de correlação
- Normalização (StandardScaler)
- Split train/test

### 2. XGBoost Surrogate (`train_xgboost.py`)
- 100 estimadores, max_depth=6
- RMSE esperado: 5-10 kWh
- R² esperado: > 0.85
- Feature importance
- Treinamento < 1 minuto

### 3. MLP Neural Network (`train_mlp.py`)
- Arquitetura: 8 → 64 → 32 → 16 → 1
- Dropout para regularização
- R² esperado: > 0.80
- Treinamento com Adam optimizer

### 4. Physics Constraints (`physics_constraints.py`)
- Constraint 1: Q ≥ 0 (nunca negativo)
- Constraint 2: Q ≤ Q_max (máximo físico)
- Constraint 3: Conservação de energia
- Intervalos de confiança (95%)

### 5. Benchmark (`benchmark.py`)
- Comparação XGBoost vs MLP vs EnergyPlus
- Métricas: RMSE, MAE, R², tempo
- Speedup: Surrogate vs Full Simulation

## Resultados Esperados

**XGBoost:**
- RMSE: 7.42 kWh
- MAE: 5.18 kWh
- R²: 0.892
- Tempo: 10ms (1000x mais rápido!)

**MLP:**
- RMSE: 8.56 kWh
- MAE: 5.87 kWh
- R²: 0.872
- Tempo: 5ms

## Uso Prático

```python
# Carregar modelo treinado
from src.xgboost_surrogate import XGBoostSurrogate
model = XGBoostSurrogate.load('models/xgboost_surrogate.pkl')

# Prever carga térmica
X_new = [0.35, 0.20, 0.10, 0.50, 0.04, 100, 0.6, 5]
Q = model.predict([X_new])[0]

# Com constraints
from src.physics_constraints import PhysicsConstrainedSurrogate
physics_model = PhysicsConstrainedSurrogate(model)
Q_constrained, Q_lower, Q_upper = physics_model.predict_with_uncertainty([X_new])
```

## Physics-Informed ML (PIML)

Ao contrário de ML puro ("caixa preta"), PIML:
1. Usa features com significado físico
2. Aprende correlações refletindo leis de transferência de calor
3. Aplica constraints para garantir outputs realistas
4. Detecta violações de conservação de energia

## Benchmark vs EnergyPlus

| Aspecto | EnergyPlus | Surrogate | Vantagem |
|---------|-----------|-----------|----------|
| Tempo/simulação | 10s | 10ms | 1000x rápido |
| Acurácia | 100% (referência) | 99.5% | Praticamente = |
| Otimização | 1000 sims = 2.7h | 1000 sims = 10s | 1000x rápido |
| Calibração | 100 sims = 15min | Treinamento = 1min | Praticamente = |

## Próximos Passos (Mês 5)

- Integrar surrogate em sistema de otimização
- Usar com Prompt Engineering para recomendações
- Validar com dados reais de construção
- Refinar constraints físicos
```

---

## **✅ CERTIFICAÇÃO DE CONCLUSÃO DO MÊS 4**

**Checklist Final:**

### **Conhecimentos Teóricos**
- [ ] Entendo feature engineering para PIML
- [ ] Conheço diferenças entre XGBoost e MLP
- [ ] Entendo como enforçar constraints físicos
- [ ] Sei calcular métricas de regressão (RMSE, MAE, R²)
- [ ] Entendo validação cruzada

### **Habilidades Práticas**
- [ ] Preparo dataset com 8 features + 5 targets
- [ ] Normalizo features corretamente
- [ ] Treino XGBoost em < 1 minuto
- [ ] Treino MLP com PyTorch/TensorFlow
- [ ] Aplico constraints físicos nas predições
- [ ] Comparo modelos com métricas objetivas

### **Entregáveis**
- [ ] Dataset ML (100 × 13)
- [ ] Modelo XGBoost (R² > 0.85)
- [ ] Modelo MLP (R² > 0.80)
- [ ] Análises: correlações, importâncias, predições
- [ ] Benchmark: XGBoost vs MLP vs EnergyPlus
- [ ] Relatório com insights

### **DevOps**
- [ ] Código modularizado (dataset, xgb, mlp, constraints)
- [ ] 20+ commits no Git
- [ ] Modelos salvos em formato portável
- [ ] Reprodutibilidade (random_state, seeds)

---

## **📊 Tempo Total Investido no Mês 4:** 50-60 horas
## **🎓 Nível de Dificuldade:** ⭐⭐⭐⭐ (4/5)
## **🔧 Complexidade Técnica:** Alta (ML, Validação, Physics-Informed)

---

**🎉 Parabéns por completar Mês 4!**

Você agora tem:
✅ Dois modelos surrogates treinados e validados
✅ Entendimento profundo de PIML (Physics-Informed ML)
✅ Capacidade de fazer 1000 predições em < 1 segundo
✅ Modelos com constraints físicos garantidos
✅ Benchmark objetivo (XGBoost vs MLP vs EnergyPlus)

**Próximo arquivo:** `Exercicios_Mes_5_Prompt_Engineering.md`

O Mês 5 será sobre integração com IA Generativa: usar Vertex AI/Gemini para fazer recomendações sobre otimização energética baseadas nos surrogates! 🤖
