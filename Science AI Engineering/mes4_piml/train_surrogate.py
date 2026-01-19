"""
Treinamento de Surrogates PIML - XGBoost e MLP
Mês 4 - PIML Surrogates - Exercício 1.3

Este script treina modelos surrogate que aproximam o comportamento
de simulações EnergyPlus com 1000x maior velocidade.

Surrogates permitem:
- Otimização rápida (milhões de avaliações)
- Quantificação de incerteza
- Análise de sensibilidade eficiente
- Análise de importância de features

Referência: Forrester et al. (2008) - Engineering Design via Surrogate Modelling
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json
import logging
import pickle
from typing import Dict, Tuple, List
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import cross_val_score, KFold, train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import xgboost as xgb
from sklearn.neural_network import MLPRegressor

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Diretórios
DATA_DIR = Path("data/lhs_datasets")
MODELS_DIR = Path("models/surrogates")
RESULTS_DIR = Path("results/surrogate_training")
PLOTS_DIR = Path("plots/surrogates")

class SurrogateTrainer:
    """
    Treina e valida modelos surrogate (XGBoost e MLP).
    """
    
    def __init__(self, dataset_path: Path = None):
        """
        Inicializa o treinador.
        
        Args:
            dataset_path: Caminho para dataset CSV (se None, procura arquivo mais recente)
        """
        self.dataset = None
        self.X = None
        self.y_dict = None  # Múltiplas variáveis de resposta
        self.scaler = StandardScaler()
        self.models = {}
        self.cv_results = {}
        
        # Criar diretórios
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        PLOTS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Carregar dataset
        if dataset_path:
            self.load_dataset(dataset_path)
        else:
            self.load_latest_dataset()
    
    def load_dataset(self, filepath: Path):
        """Carrega dataset do arquivo"""
        logger.info(f"Carregando dataset: {filepath}")
        self.dataset = pd.read_csv(filepath)
        logger.info(f"✅ Dataset carregado: {self.dataset.shape}")
    
    def load_latest_dataset(self):
        """Carrega dataset mais recente da pasta"""
        csv_files = list(DATA_DIR.glob("piml_dataset_*.csv"))
        if not csv_files:
            raise FileNotFoundError(f"Nenhum dataset encontrado em {DATA_DIR}")
        
        latest = max(csv_files, key=lambda p: p.stat().st_mtime)
        self.load_dataset(latest)
    
    def prepare_features(self):
        """
        Prepara features (entrada) e targets (saída).
        
        Entrada: Parâmetros de projeto (window_to_wall_ratio, etc.)
        Saída: Múltiplas métricas de desempenho
        """
        logger.info(f"\n{'='*70}")
        logger.info("PREPARAÇÃO DE FEATURES E TARGETS")
        logger.info(f"{'='*70}")
        
        # Identificar colunas de parâmetros (entrada)
        # Exluir: simulation_id, colunas de resultado
        exclude_cols = {
            'simulation_id', 
            'simulation_status',
            'annual_consumption_kwh',
            'peak_cooling_kw',
            'peak_heating_kw',
            'comfort_hours',
            'avg_temperature_C',
            'max_temperature_C',
            'min_temperature_C',
            'error_message'
        }
        
        feature_cols = [c for c in self.dataset.columns if c not in exclude_cols]
        self.X = self.dataset[feature_cols].copy()
        
        # Identificar variáveis de resposta (saída)
        response_cols = ['annual_consumption_kwh', 'peak_cooling_kw', 'comfort_hours']
        self.y_dict = {}
        for col in response_cols:
            if col in self.dataset.columns:
                self.y_dict[col] = self.dataset[col].copy()
        
        logger.info(f"✅ Features (entrada): {len(feature_cols)} variáveis")
        for col in feature_cols:
            logger.info(f"   - {col}")
        
        logger.info(f"\n✅ Targets (saída): {len(self.y_dict)} variáveis")
        for col in self.y_dict.keys():
            logger.info(f"   - {col}")
        
        # Normalizar features
        self.X = pd.DataFrame(
            self.scaler.fit_transform(self.X),
            columns=feature_cols,
            index=self.X.index
        )
        
        logger.info(f"\n✅ Features normalizadas (media=0, std=1)")

    def train_xgboost(self, target_var: str = 'annual_consumption_kwh') -> Tuple[xgb.XGBRegressor, Dict]:
        """
        Treina modelo XGBoost com validação cruzada.
        
        Args:
            target_var: Variável de resposta a prever
        
        Returns:
            Tuple: (modelo treinado, resultados de validação cruzada)
        """
        logger.info(f"\n{'='*70}")
        logger.info(f"TREINAMENTO XGBOOST - {target_var}")
        logger.info(f"{'='*70}")
        
        y = self.y_dict[target_var]
        
        # Hiperparâmetros otimizados para PIML
        xgb_params = {
            'n_estimators': [100, 300, 500],
            'max_depth': [5, 7, 9],
            'learning_rate': [0.01, 0.05, 0.1],
            'subsample': [0.7, 0.8, 0.9],
        }
        
        # Grid Search
        base_model = xgb.XGBRegressor(
            random_state=42,
            n_jobs=-1,
            early_stopping_rounds=10
        )
        
        logger.info("Executando GridSearchCV (n_estimators, max_depth, learning_rate, subsample)...")
        
        grid_search = GridSearchCV(
            base_model,
            xgb_params,
            cv=5,
            scoring='r2',
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(self.X, y)
        
        best_model = grid_search.best_estimator_
        
        logger.info(f"\n✅ Melhores hiperparâmetros:")
        for param, value in grid_search.best_params_.items():
            logger.info(f"   {param}: {value}")
        logger.info(f"   Best CV R²: {grid_search.best_score_:.4f}")
        
        # Validação cruzada detalhada
        cv = KFold(n_splits=5, shuffle=True, random_state=42)
        cv_scores_r2 = cross_val_score(best_model, self.X, y, cv=cv, scoring='r2')
        cv_scores_rmse = cross_val_score(best_model, self.X, y, cv=cv, scoring='neg_mean_squared_error')
        cv_scores_rmse = np.sqrt(-cv_scores_rmse)
        
        logger.info(f"\n📊 Resultados da Validação Cruzada (5 folds):")
        logger.info(f"   R² scores: {cv_scores_r2}")
        logger.info(f"   R² média: {cv_scores_r2.mean():.4f} ± {cv_scores_r2.std():.4f}")
        logger.info(f"   RMSE média: {cv_scores_rmse.mean():.4f} ± {cv_scores_rmse.std():.4f}")
        
        # Treinar no dataset completo para modelo final
        best_model.fit(self.X, y)
        
        # Predição no treino (para visualização)
        y_pred = best_model.predict(self.X)
        r2_train = r2_score(y, y_pred)
        rmse_train = np.sqrt(mean_squared_error(y, y_pred))
        mae_train = mean_absolute_error(y, y_pred)
        
        logger.info(f"\n📈 Performance no conjunto completo:")
        logger.info(f"   R² (treino): {r2_train:.4f}")
        logger.info(f"   RMSE: {rmse_train:.4f}")
        logger.info(f"   MAE: {mae_train:.4f}")
        
        results = {
            'model': best_model,
            'cv_r2_mean': cv_scores_r2.mean(),
            'cv_r2_std': cv_scores_r2.std(),
            'cv_rmse_mean': cv_scores_rmse.mean(),
            'cv_rmse_std': cv_scores_rmse.std(),
            'train_r2': r2_train,
            'train_rmse': rmse_train,
            'train_mae': mae_train,
            'best_params': grid_search.best_params_,
            'feature_importance': self._get_feature_importance(best_model),
        }
        
        return best_model, results
    
    def train_mlp(self, target_var: str = 'annual_consumption_kwh') -> Tuple[MLPRegressor, Dict]:
        """
        Treina modelo MLP (Neural Network) com validação cruzada.
        
        Args:
            target_var: Variável de resposta a prever
        
        Returns:
            Tuple: (modelo treinado, resultados de validação cruzada)
        """
        logger.info(f"\n{'='*70}")
        logger.info(f"TREINAMENTO MLP - {target_var}")
        logger.info(f"{'='*70}")
        
        y = self.y_dict[target_var]
        
        # Hiperparâmetros otimizados para PIML
        mlp_params = {
            'hidden_layer_sizes': [(100,), (100, 100), (100, 50)],
            'activation': ['relu', 'tanh'],
            'learning_rate': ['constant', 'adaptive'],
            'alpha': [0.0001, 0.001, 0.01],
        }
        
        # Grid Search
        base_model = MLPRegressor(
            random_state=42,
            max_iter=500,
            early_stopping=True,
            validation_fraction=0.1,
            n_iter_no_change=20
        )
        
        logger.info("Executando GridSearchCV (hidden_layer_sizes, activation, alpha)...")
        
        grid_search = GridSearchCV(
            base_model,
            mlp_params,
            cv=5,
            scoring='r2',
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(self.X, y)
        
        best_model = grid_search.best_estimator_
        
        logger.info(f"\n✅ Melhores hiperparâmetros:")
        for param, value in grid_search.best_params_.items():
            logger.info(f"   {param}: {value}")
        logger.info(f"   Best CV R²: {grid_search.best_score_:.4f}")
        
        # Validação cruzada detalhada
        cv = KFold(n_splits=5, shuffle=True, random_state=42)
        cv_scores_r2 = cross_val_score(best_model, self.X, y, cv=cv, scoring='r2')
        cv_scores_rmse = cross_val_score(best_model, self.X, y, cv=cv, scoring='neg_mean_squared_error')
        cv_scores_rmse = np.sqrt(-cv_scores_rmse)
        
        logger.info(f"\n📊 Resultados da Validação Cruzada (5 folds):")
        logger.info(f"   R² scores: {cv_scores_r2}")
        logger.info(f"   R² média: {cv_scores_r2.mean():.4f} ± {cv_scores_r2.std():.4f}")
        logger.info(f"   RMSE média: {cv_scores_rmse.mean():.4f} ± {cv_scores_rmse.std():.4f}")
        
        # Treinar no dataset completo
        best_model.fit(self.X, y)
        
        # Predição
        y_pred = best_model.predict(self.X)
        r2_train = r2_score(y, y_pred)
        rmse_train = np.sqrt(mean_squared_error(y, y_pred))
        mae_train = mean_absolute_error(y, y_pred)
        
        logger.info(f"\n📈 Performance no conjunto completo:")
        logger.info(f"   R² (treino): {r2_train:.4f}")
        logger.info(f"   RMSE: {rmse_train:.4f}")
        logger.info(f"   MAE: {mae_train:.4f}")
        
        results = {
            'model': best_model,
            'cv_r2_mean': cv_scores_r2.mean(),
            'cv_r2_std': cv_scores_r2.std(),
            'cv_rmse_mean': cv_scores_rmse.mean(),
            'cv_rmse_std': cv_scores_rmse.std(),
            'train_r2': r2_train,
            'train_rmse': rmse_train,
            'train_mae': mae_train,
            'best_params': grid_search.best_params_,
        }
        
        return best_model, results
    
    def _get_feature_importance(self, model) -> Dict[str, float]:
        """Extrai importância de features do modelo XGBoost"""
        feature_importance = model.feature_importances_
        feature_names = self.X.columns.tolist()
        
        importance_dict = {name: float(importance) for name, importance in zip(feature_names, feature_importance)}
        # Normalizar para soma 1
        total = sum(importance_dict.values())
        importance_dict = {k: v/total for k, v in importance_dict.items()}
        
        # Ordenar por importância
        return dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))
    
    def save_models(self):
        """Salva modelos treinados em disco"""
        logger.info(f"\n{'='*70}")
        logger.info("SALVANDO MODELOS")
        logger.info(f"{'='*70}")
        
        for target_var, model_dict in self.models.items():
            # Salvar XGBoost
            xgb_path = MODELS_DIR / f"xgboost_{target_var.replace(' ', '_')}.pkl"
            with open(xgb_path, 'wb') as f:
                pickle.dump(model_dict['xgboost']['model'], f)
            logger.info(f"✅ XGBoost salvo: {xgb_path}")
            
            # Salvar MLP
            mlp_path = MODELS_DIR / f"mlp_{target_var.replace(' ', '_')}.pkl"
            with open(mlp_path, 'wb') as f:
                pickle.dump(model_dict['mlp']['model'], f)
            logger.info(f"✅ MLP salvo: {mlp_path}")
            
            # Salvar scaler
            scaler_path = MODELS_DIR / f"scaler_{target_var.replace(' ', '_')}.pkl"
            with open(scaler_path, 'wb') as f:
                pickle.dump(self.scaler, f)
            logger.info(f"✅ Scaler salvo: {scaler_path}")
    
    def save_cv_results(self):
        """Salva resultados de validação cruzada em CSV"""
        logger.info(f"\nSalvando resultados de validação cruzada...")
        
        cv_data = []
        for target_var, model_dict in self.models.items():
            for model_type in ['xgboost', 'mlp']:
                results = model_dict[model_type]
                cv_data.append({
                    'target_variable': target_var,
                    'model_type': model_type,
                    'cv_r2_mean': results['cv_r2_mean'],
                    'cv_r2_std': results['cv_r2_std'],
                    'cv_rmse_mean': results['cv_rmse_mean'],
                    'cv_rmse_std': results['cv_rmse_std'],
                    'train_r2': results['train_r2'],
                    'train_rmse': results['train_rmse'],
                    'train_mae': results['train_mae'],
                })
        
        cv_df = pd.DataFrame(cv_data)
        cv_path = RESULTS_DIR / f"cross_validation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        cv_df.to_csv(cv_path, index=False)
        logger.info(f"✅ Resultados salvos: {cv_path}")
    
    def plot_feature_importance(self, target_var: str = 'annual_consumption_kwh'):
        """Plota importância de features para XGBoost"""
        if target_var not in self.models or 'xgboost' not in self.models[target_var]:
            logger.warning(f"Modelo XGBoost para {target_var} não encontrado")
            return
        
        importance_dict = self.models[target_var]['xgboost']['feature_importance']
        
        # Pegar top 10 features
        top_features = dict(list(importance_dict.items())[:10])
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(list(top_features.keys()), list(top_features.values()))
        ax.set_xlabel('Feature Importance')
        ax.set_title(f'Top 10 Features - XGBoost ({target_var})')
        ax.invert_yaxis()
        
        plot_path = PLOTS_DIR / f"feature_importance_{target_var}.png"
        plt.tight_layout()
        plt.savefig(plot_path, dpi=300)
        logger.info(f"✅ Gráfico salvo: {plot_path}")
        plt.close()
    
    def train_all_models(self):
        """Treina todos os modelos para todos os targets"""
        logger.info(f"\n{'='*70}")
        logger.info("TREINAMENTO DE TODOS OS MODELOS")
        logger.info(f"{'='*70}\n")
        
        for target_var in self.y_dict.keys():
            logger.info(f"\n{'─'*70}")
            logger.info(f"Treinando para: {target_var}")
            logger.info(f"{'─'*70}")
            
            self.models[target_var] = {}
            
            # Treinar XGBoost
            xgb_model, xgb_results = self.train_xgboost(target_var)
            self.models[target_var]['xgboost'] = xgb_results
            
            # Treinar MLP
            mlp_model, mlp_results = self.train_mlp(target_var)
            self.models[target_var]['mlp'] = mlp_results
        
        # Salvar modelos e resultados
        self.save_models()
        self.save_cv_results()
        
        # Plotar importância de features
        for target_var in self.y_dict.keys():
            self.plot_feature_importance(target_var)

def main():
    """Função principal"""
    logger.info(f"\n{'='*70}")
    logger.info("TREINAMENTO DE SURROGATES PIML")
    logger.info(f"{'='*70}\n")
    
    try:
        # Inicializar treinador
        trainer = SurrogateTrainer()
        
        # Preparar features
        trainer.prepare_features()
        
        # Treinar todos os modelos
        trainer.train_all_models()
        
        logger.info(f"\n{'='*70}")
        logger.info("✅ TREINAMENTO CONCLUÍDO COM SUCESSO!")
        logger.info(f"{'='*70}")
        logger.info(f"\n📊 Próximas etapas:")
        logger.info(f"   1. Validar física com validate_physics.py")
        logger.info(f"   2. Quantificar incerteza com uncertainty_quantification.py")
        logger.info(f"   3. Análise de sensibilidade com sensitivity.py")
    
    except Exception as e:
        logger.error(f"❌ Erro durante treinamento: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
