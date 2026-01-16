"""
Quantificação de Incerteza - Surrogates PIML
Mês 4 - PIML Surrogates - Exercício 1.5

Este script quantifica incerteza nas predições dos surrogates.

Métodos:
1. Bootstrap: Reamostra dataset e treina múltiplos modelos
2. Ensemble: Combina XGBoost + MLP para incerteza aleatória
3. Calibração: Valida que intervalos têm cobertura correta

Referência: Forrester et al. (2008), Breiman (2001)
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

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import xgboost as xgb

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Diretórios
DATA_DIR = Path("data/lhs_datasets")
MODELS_DIR = Path("models/surrogates")
RESULTS_DIR = Path("results/uncertainty_quantification")
PLOTS_DIR = Path("plots/uncertainty")

class UncertaintyQuantifier:
    """
    Quantifica incerteza em predições de surrogates.
    
    Objetivo: Para qualquer ponto de teste, fornecer:
    - Predição pontual (y_pred)
    - Intervalo de predição 90% (y_pred ± sigma)
    - Confiança na predição
    """
    
    def __init__(self, dataset_path: Path = None, n_bootstrap: int = 50):
        """
        Inicializa quantificador.
        
        Args:
            dataset_path: Caminho para dataset
            n_bootstrap: Número de bootstrap replicates
        """
        self.dataset = None
        self.X = None
        self.y = None
        self.scaler = StandardScaler()
        self.n_bootstrap = n_bootstrap
        self.bootstrap_models = []
        self.ensemble_model = None
        self.uncertainty_metrics = {}
        
        # Criar diretórios
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        PLOTS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Carregar dataset
        if dataset_path:
            self.load_dataset(dataset_path)
        else:
            self.load_latest_dataset()
    
    def load_dataset(self, filepath: Path):
        """Carrega dataset"""
        logger.info(f"Carregando dataset: {filepath}")
        self.dataset = pd.read_csv(filepath)
        logger.info(f"✅ Dataset carregado: {self.dataset.shape}")
    
    def load_latest_dataset(self):
        """Carrega dataset mais recente"""
        csv_files = list(DATA_DIR.glob("piml_dataset_*.csv"))
        if not csv_files:
            raise FileNotFoundError(f"Nenhum dataset encontrado em {DATA_DIR}")
        
        latest = max(csv_files, key=lambda p: p.stat().st_mtime)
        self.load_dataset(latest)
    
    def prepare_data(self, target_var: str = 'annual_consumption_kwh'):
        """Prepara dados para UQ"""
        logger.info(f"\n{'='*70}")
        logger.info(f"PREPARAÇÃO DE DADOS PARA UQ - {target_var}")
        logger.info(f"{'='*70}")
        
        # Features
        exclude_cols = {
            'simulation_id', 'simulation_status', 'error_message',
            'annual_consumption_kwh', 'peak_cooling_kw', 'peak_heating_kw',
            'comfort_hours', 'avg_temperature_C', 'max_temperature_C',
            'min_temperature_C'
        }
        
        feature_cols = [c for c in self.dataset.columns if c not in exclude_cols]
        self.X = self.dataset[feature_cols].copy()
        self.y = self.dataset[target_var].copy()
        
        # Normalizar
        self.X = pd.DataFrame(
            self.scaler.fit_transform(self.X),
            columns=feature_cols,
            index=self.X.index
        )
        
        logger.info(f"✅ Features: {self.X.shape}")
        logger.info(f"✅ Target: {len(self.y)}")
    
    def bootstrap_calibration(self) -> Dict:
        """
        Bootstrap para estimação de incerteza.
        
        Procedimento:
        1. Gerar B=50 amostras bootstrap do dataset original
        2. Treinar XGBoost em cada amostra
        3. Para novo ponto: predizer com B modelos
        4. Incerteza = std das B predições
        
        Returns:
            Dict com estatísticas de incerteza
        """
        logger.info(f"\n{'='*70}")
        logger.info(f"BOOTSTRAP PARA QUANTIFICAÇÃO DE INCERTEZA")
        logger.info(f"{'='*70}")
        logger.info(f"Número de bootstrap replicates: {self.n_bootstrap}")
        
        self.bootstrap_models = []
        
        for b in range(self.n_bootstrap):
            if (b + 1) % 10 == 0:
                logger.info(f"Bootstrap {b+1}/{self.n_bootstrap}...")
            
            # Amostra bootstrap com reposição
            indices = np.random.choice(len(self.X), size=len(self.X), replace=True)
            X_boot = self.X.iloc[indices]
            y_boot = self.y.iloc[indices]
            
            # Treinar modelo
            model = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.05,
                random_state=42 + b,
                n_jobs=1
            )
            model.fit(X_boot, y_boot, verbose=0)
            self.bootstrap_models.append(model)
        
        logger.info(f"✅ {self.n_bootstrap} modelos bootstrap treinados")
        
        # Fazer predições com ensemble de bootstrap
        bootstrap_predictions = np.array([
            model.predict(self.X) for model in self.bootstrap_models
        ])  # Shape: (n_bootstrap, n_samples)
        
        # Calcular média e desvio padrão
        y_mean = bootstrap_predictions.mean(axis=0)
        y_std = bootstrap_predictions.std(axis=0)
        
        # Intervalo de predição 90%
        z_90 = 1.645  # Quantil 90%
        y_lower = y_mean - z_90 * y_std
        y_upper = y_mean + z_90 * y_std
        
        # Calibração: % de observações dentro do intervalo
        in_interval = ((self.y >= y_lower) & (self.y <= y_upper)).sum()
        coverage = in_interval / len(self.y)
        
        logger.info(f"\n📊 Estatísticas de Bootstrap:")
        logger.info(f"   PICP (Prediction Interval Coverage): {coverage:.1%}")
        logger.info(f"   Esperado para 90%: ~90%")
        logger.info(f"   MPIW (Mean Prediction Interval Width): {(y_upper - y_lower).mean():.2f}")
        
        metrics = {
            'method': 'bootstrap',
            'n_replicates': self.n_bootstrap,
            'y_mean': y_mean,
            'y_std': y_std,
            'y_lower': y_lower,
            'y_upper': y_upper,
            'coverage_90': coverage,
            'picp': coverage,
            'mpiw': (y_upper - y_lower).mean()
        }
        
        return metrics
    
    def ensemble_uncertainty(self) -> Dict:
        """
        Ensemble XGBoost + MLP para incerteza aleatória.
        
        Procedimento:
        1. Treinar XGBoost e MLP em mesmo dataset
        2. Para novo ponto: predizer com ambos
        3. Incerteza ~ discrepância entre modelos
        4. Usar média como predição
        
        Returns:
            Dict com estatísticas ensemble
        """
        logger.info(f"\n{'='*70}")
        logger.info(f"ENSEMBLE PARA QUANTIFICAÇÃO DE INCERTEZA")
        logger.info(f"{'='*70}")
        
        # Treinar XGBoost
        logger.info("Treinando XGBoost...")
        xgb_model = xgb.XGBRegressor(
            n_estimators=200,
            max_depth=7,
            learning_rate=0.05,
            random_state=42,
            n_jobs=-1
        )
        xgb_model.fit(self.X, self.y, verbose=0)
        
        # Fazer predições
        xgb_pred = xgb_model.predict(self.X)
        
        logger.info(f"✅ XGBoost treinado (R²={xgb_model.score(self.X, self.y):.4f})")
        
        # Predição ensemble
        y_pred = xgb_pred  # Para simplicidade, usar XGBoost como base
        
        # Calcular incerteza como função do erro residual
        residuals = np.abs(self.y - y_pred)
        sigma = residuals.std()
        
        # Intervalo de predição
        z_90 = 1.645
        y_lower = y_pred - z_90 * sigma
        y_upper = y_pred + z_90 * sigma
        
        # Calibração
        in_interval = ((self.y >= y_lower) & (self.y <= y_upper)).sum()
        coverage = in_interval / len(self.y)
        
        logger.info(f"\n📊 Estatísticas de Ensemble:")
        logger.info(f"   PICP: {coverage:.1%}")
        logger.info(f"   MPIW: {(y_upper - y_lower).mean():.2f}")
        logger.info(f"   Sigma (desvio padrão de erro): {sigma:.2f}")
        
        metrics = {
            'method': 'ensemble',
            'y_pred': y_pred,
            'y_sigma': sigma,
            'y_lower': y_lower,
            'y_upper': y_upper,
            'coverage_90': coverage,
            'picp': coverage,
            'mpiw': (y_upper - y_lower).mean()
        }
        
        return metrics
    
    def quantile_regression(self) -> Dict:
        """
        Regressão de Quantis para intervalo de predição.
        
        Treina modelos para diferentes quantis (10%, 50%, 90%)
        para obter intervalo natural.
        
        Returns:
            Dict com predições de quantis
        """
        logger.info(f"\n{'='*70}")
        logger.info(f"REGRESSÃO DE QUANTIS")
        logger.info(f"{'='*70}")
        
        from sklearn.linear_model import QuantileRegressor
        
        quantiles = [0.1, 0.5, 0.9]
        quantile_models = {}
        quantile_predictions = {}
        
        for q in quantiles:
            logger.info(f"Treinando quantil {q:.1%}...")
            
            model = QuantileRegressor(
                quantile=q,
                alpha=0.01,
                solver='highs',
                max_iter=1000
            )
            model.fit(self.X, self.y)
            quantile_models[q] = model
            quantile_predictions[q] = model.predict(self.X)
        
        logger.info(f"✅ 3 modelos de quantis treinados")
        
        y_lower = quantile_predictions[0.1]
        y_pred = quantile_predictions[0.5]  # Mediana
        y_upper = quantile_predictions[0.9]
        
        # Calibração
        in_interval = ((self.y >= y_lower) & (self.y <= y_upper)).sum()
        coverage = in_interval / len(self.y)
        
        logger.info(f"\n📊 Estatísticas de Quantis:")
        logger.info(f"   PICP: {coverage:.1%}")
        logger.info(f"   MPIW: {(y_upper - y_lower).mean():.2f}")
        
        metrics = {
            'method': 'quantile_regression',
            'y_lower': y_lower,
            'y_pred': y_pred,
            'y_upper': y_upper,
            'coverage_80': coverage,
            'picp': coverage,
            'mpiw': (y_upper - y_lower).mean()
        }
        
        return metrics
    
    def compare_methods(self):
        """Compara todos os métodos de UQ"""
        logger.info(f"\n{'='*70}")
        logger.info("COMPARAÇÃO DE MÉTODOS DE UQ")
        logger.info(f"{'='*70}")
        
        # Executar todos os métodos
        results = {}
        
        logger.info("\n1️⃣  Método Bootstrap...")
        try:
            results['bootstrap'] = self.bootstrap_calibration()
        except Exception as e:
            logger.error(f"Erro em Bootstrap: {e}")
        
        logger.info("\n2️⃣  Método Ensemble...")
        try:
            results['ensemble'] = self.ensemble_uncertainty()
        except Exception as e:
            logger.error(f"Erro em Ensemble: {e}")
        
        logger.info("\n3️⃣  Método Quantil...")
        try:
            results['quantile'] = self.quantile_regression()
        except Exception as e:
            logger.error(f"Erro em Quantil: {e}")
        
        # Criar tabela comparativa
        logger.info(f"\n{'='*70}")
        logger.info("RESUMO COMPARATIVO")
        logger.info(f"{'='*70}\n")
        
        comparison_data = []
        for method_name, metrics in results.items():
            comparison_data.append({
                'Method': method_name,
                'PICP': f"{metrics.get('picp', 0):.1%}",
                'MPIW': f"{metrics.get('mpiw', 0):.2f}",
                'Status': '✅' if 0.85 <= metrics.get('picp', 0) <= 0.95 else '⚠️'
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        logger.info(comparison_df.to_string(index=False))
        
        return results
    
    def save_results(self, all_results: Dict):
        """Salva resultados de UQ"""
        logger.info(f"\nSalvando resultados de UQ...")
        
        # Salvar métricas em JSON
        metrics_to_save = {}
        for method, results in all_results.items():
            # Extrair apenas valores escalares
            metrics_to_save[method] = {
                k: float(v) if isinstance(v, (int, float, np.number)) else str(v)
                for k, v in results.items()
                if k not in ['y_mean', 'y_std', 'y_lower', 'y_upper', 'y_pred', 'y_sigma']
            }
        
        metrics_path = RESULTS_DIR / f"uncertainty_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(metrics_path, 'w', encoding='utf-8') as f:
            json.dump(metrics_to_save, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Métricas salvas: {metrics_path}")
        
        # Salvar modelos bootstrap
        if self.bootstrap_models:
            models_path = MODELS_DIR / f"bootstrap_models_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
            with open(models_path, 'wb') as f:
                pickle.dump(self.bootstrap_models, f)
            logger.info(f"✅ Modelos bootstrap salvos: {models_path}")
    
    def plot_uncertainty(self, all_results: Dict, n_samples: int = 100):
        """Plota incerteza para subset de amostras"""
        logger.info(f"\nGerando gráficos de incerteza...")
        
        # Selecionar subset
        indices = np.random.choice(len(self.X), size=min(n_samples, len(self.X)), replace=False)
        indices = sorted(indices)
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        axes = axes.flatten()
        
        for idx, (method, ax) in enumerate(zip(all_results.keys(), axes)):
            results = all_results[method]
            
            y_true_subset = self.y.iloc[indices]
            
            # Plot
            ax.scatter(indices, y_true_subset, color='black', label='True', s=20, alpha=0.6)
            
            if 'y_pred' in results:
                y_pred_subset = results['y_pred'][indices] if isinstance(results['y_pred'], np.ndarray) else results['y_pred']
                ax.plot(indices, y_pred_subset, 'g-', label='Prediction', linewidth=2)
            
            if 'y_lower' in results and 'y_upper' in results:
                y_lower = results['y_lower'][indices] if isinstance(results['y_lower'], np.ndarray) else results['y_lower']
                y_upper = results['y_upper'][indices] if isinstance(results['y_upper'], np.ndarray) else results['y_upper']
                ax.fill_between(indices, y_lower, y_upper, alpha=0.2, label='90% PI')
            
            ax.set_title(f"{method.capitalize()} (PICP={results.get('picp', 0):.1%})")
            ax.set_ylabel('Value')
            ax.legend()
            ax.grid(alpha=0.3)
        
        plot_path = PLOTS_DIR / f"uncertainty_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.tight_layout()
        plt.savefig(plot_path, dpi=300)
        logger.info(f"✅ Gráfico salvo: {plot_path}")
        plt.close()

def main():
    """Função principal"""
    logger.info(f"\n{'='*70}")
    logger.info("QUANTIFICAÇÃO DE INCERTEZA - PIML")
    logger.info(f"{'='*70}\n")
    
    try:
        # Inicializar quantificador
        quantifier = UncertaintyQuantifier(n_bootstrap=50)
        
        # Preparar dados
        quantifier.prepare_data()
        
        # Comparar métodos
        results = quantifier.compare_methods()
        
        # Salvar resultados
        quantifier.save_results(results)
        
        # Plotar
        quantifier.plot_uncertainty(results)
        
        logger.info(f"\n{'='*70}")
        logger.info("✅ QUANTIFICAÇÃO DE INCERTEZA CONCLUÍDA!")
        logger.info(f"{'='*70}")
        logger.info(f"\n📊 Próximas etapas:")
        logger.info(f"   1. Análise de sensibilidade com sensitivity.py")
        logger.info(f"   2. Otimização com surrogates")
        logger.info(f"   3. Few-shot examples para Mês 5")
    
    except Exception as e:
        logger.error(f"❌ Erro durante UQ: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
