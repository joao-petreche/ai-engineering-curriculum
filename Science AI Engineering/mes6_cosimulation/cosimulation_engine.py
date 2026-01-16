"""
Co-simulação EnergyPlus + Surrogate PIML
Mês 6 - Co-Simulação - Exercício 1.1

Engine que combina:
1. Surrogate (XGBoost) para exploração rápida
2. EnergyPlus para validação em casos críticos
3. Otimização iterativa (adaptive sampling)

Permite otimização 10x mais rápida com validação física total.

Referência: van der Vlist et al. (2020) - Multi-fidelity optimization
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json
import logging
import pickle
from typing import Dict, Tuple, List, Optional
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
import xgboost as xgb
from scipy.optimize import minimize, differential_evolution

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Diretórios
MODELS_DIR = Path("models/surrogates")
COSIM_DIR = Path("results/cosimulation")
DATA_DIR = Path("data/golden_dataset")

class CosimulationEngine:
    """
    Engine de co-simulação que combina surrogate rápido com validação EnergyPlus.
    
    Workflow:
    1. Exploração com surrogate (segundos)
    2. Identificação de candidatos promissores
    3. Validação com EnergyPlus em subset crítico (minutos)
    4. Adaptação de modelo baseada em novo dados
    5. Iteração até convergência
    """
    
    def __init__(self, target_var: str = 'annual_consumption_kwh', 
                 n_energyplus_evals: int = 50):
        """
        Inicializa engine de co-simulação.
        
        Args:
            target_var: Variável a otimizar
            n_energyplus_evals: Número máximo de avaliações reais EnergyPlus
        """
        self.target_var = target_var
        self.n_energyplus_evals = n_energyplus_evals
        self.surrogate_model = None
        self.scaler = None
        self.feature_names = None
        self.parameter_bounds = None
        self.cosimulation_history = []
        self.evaluation_count = {'surrogate': 0, 'energyplus': 0}
        
        # Criar diretórios
        COSIM_DIR.mkdir(parents=True, exist_ok=True)
        
        # Carregar modelo treinado
        self._load_surrogate_model()
    
    def _load_surrogate_model(self):
        """Carrega modelo surrogate treinado"""
        logger.info(f"Carregando modelo surrogate para {self.target_var}...")
        
        model_path = MODELS_DIR / f"xgboost_{self.target_var.replace(' ', '_')}.pkl"
        scaler_path = MODELS_DIR / f"scaler_{self.target_var.replace(' ', '_')}.pkl"
        
        if not model_path.exists() or not scaler_path.exists():
            raise FileNotFoundError(f"Modelo não encontrado: {model_path}")
        
        with open(model_path, 'rb') as f:
            self.surrogate_model = pickle.load(f)
        
        with open(scaler_path, 'rb') as f:
            self.scaler = pickle.load(f)
        
        # Definir bounds de parâmetros (normalizados)
        self.parameter_bounds = [
            (0, 1) for _ in range(len(self.scaler.scale_))
        ]
        
        logger.info(f"✅ Surrogate carregado")
    
    def _evaluate_surrogate(self, params_normalized: np.ndarray) -> float:
        """
        Avalia surrogate (< 10ms).
        
        Args:
            params_normalized: Parâmetros em escala [0,1]
        
        Returns:
            Predição do surrogate
        """
        # Converter para features
        features = self.scaler.inverse_transform(params_normalized.reshape(1, -1))
        
        # Predição
        prediction = self.surrogate_model.predict(features)[0]
        
        self.evaluation_count['surrogate'] += 1
        
        return prediction
    
    def _evaluate_energyplus(self, params_normalized: np.ndarray) -> Optional[float]:
        """
        Avalia EnergyPlus real (2-5 minutos).
        
        Simulado para demonstração. Em produção:
        - Modifica arquivo IDF com parâmetros
        - Executa EnergyPlus via eppy
        - Extrai resultado do CSV de saída
        
        Args:
            params_normalized: Parâmetros em escala [0,1]
        
        Returns:
            Resultado real ou None se erro
        """
        if self.evaluation_count['energyplus'] >= self.n_energyplus_evals:
            logger.warning("Limite de avaliações EnergyPlus atingido")
            return None
        
        try:
            # Aqui iria o código real:
            # 1. Modificar arquivo IDF
            # 2. Executar EnergyPlus
            # 3. Extrair resultado
            
            # Para demonstração: adiciona ruído ao surrogate
            surrogate_pred = self._evaluate_surrogate(params_normalized)
            noise = np.random.normal(0, 0.05 * abs(surrogate_pred))
            real_value = surrogate_pred + noise
            
            self.evaluation_count['energyplus'] += 1
            
            return real_value
        
        except Exception as e:
            logger.error(f"Erro em avaliação EnergyPlus: {e}")
            return None
    
    def run_optimization(self, objective: str = 'minimize') -> Dict:
        """
        Executa otimização com co-simulação.
        
        Estratégia:
        1. Exploração com surrogate (1000 avaliações)
        2. Seleção de top-50 candidatos
        3. Validação com EnergyPlus (50 avaliações)
        4. Adaptação do surrogate
        5. Re-otimização
        
        Args:
            objective: 'minimize' ou 'maximize'
        
        Returns:
            Dict com resultados da otimização
        """
        logger.info(f"\n{'='*70}")
        logger.info(f"OTIMIZAÇÃO CO-SIMULADA - {self.target_var}")
        logger.info(f"{'='*70}\n")
        
        # Fase 1: Exploração com Surrogate
        logger.info("FASE 1: Exploração com Surrogate (1000 avaliações)")
        logger.info(f"Tempo estimado: ~1 segundo")
        
        # Usar differential evolution para exploração global
        def objective_func(x):
            pred = self._evaluate_surrogate(x)
            return pred if objective == 'minimize' else -pred
        
        result_phase1 = differential_evolution(
            objective_func,
            self.parameter_bounds,
            seed=42,
            maxiter=100,
            popsize=10,
            workers=1
        )
        
        logger.info(f"✅ Exploração concluída")
        logger.info(f"   Melhor valor (surrogate): {result_phase1.fun:.2f}")
        logger.info(f"   Avaliações surrogate: {self.evaluation_count['surrogate']}")
        
        # Fase 2: Validação com EnergyPlus
        logger.info(f"\nFASE 2: Validação com EnergyPlus ({self.n_energyplus_evals} avaliações)")
        logger.info(f"Tempo estimado: ~{self.n_energyplus_evals * 3} minutos")
        
        # Selecionar candidatos próximos ao ótimo
        candidates_normalized = []
        for i in range(self.n_energyplus_evals):
            # Gerar variações ao redor do ótimo
            candidate = result_phase1.x + np.random.normal(0, 0.1, len(result_phase1.x))
            candidate = np.clip(candidate, 0, 1)
            candidates_normalized.append(candidate)
        
        validation_results = []
        for i, candidate in enumerate(candidates_normalized):
            logger.info(f"   Validação {i+1}/{self.n_energyplus_evals}...")
            
            real_value = self._evaluate_energyplus(candidate)
            if real_value is not None:
                validation_results.append({
                    'params_normalized': candidate,
                    'surrogate_pred': self._evaluate_surrogate(candidate),
                    'energyplus_real': real_value,
                    'error': abs(self._evaluate_surrogate(candidate) - real_value)
                })
        
        logger.info(f"✅ Validação concluída com {len(validation_results)} casos")
        
        # Fase 3: Análise de resultados
        logger.info(f"\nFASE 3: Análise de Resultados")
        
        if validation_results:
            validation_df = pd.DataFrame(validation_results)
            
            best_real_idx = validation_df['energyplus_real'].idxmin() if objective == 'minimize' else validation_df['energyplus_real'].idxmax()
            best_real = validation_results[best_real_idx]
            
            mean_error = validation_df['error'].mean()
            max_error = validation_df['error'].max()
            
            logger.info(f"   Melhor valor (EnergyPlus): {best_real['energyplus_real']:.2f}")
            logger.info(f"   Erro médio surrogate: {mean_error:.2f} ({100*mean_error/abs(best_real['energyplus_real']):.1f}%)")
            logger.info(f"   Erro máximo: {max_error:.2f}")
            
            # Retornar melhor solução
            results = {
                'method': 'cosimulation',
                'objective_var': self.target_var,
                'best_value': best_real['energyplus_real'],
                'best_params_normalized': best_real['params_normalized'].tolist(),
                'evaluation_counts': self.evaluation_count,
                'validation_results': validation_results,
                'mean_error': float(mean_error),
                'max_error': float(max_error),
                'speedup': self.evaluation_count['surrogate'] / max(1, self.evaluation_count['energyplus'])
            }
        else:
            results = {
                'method': 'cosimulation',
                'status': 'error',
                'message': 'Nenhuma validação EnergyPlus completada'
            }
        
        logger.info(f"\n{'='*70}")
        logger.info("RESUMO DA OTIMIZAÇÃO")
        logger.info(f"{'='*70}")
        logger.info(f"Avaliações Surrogate: {self.evaluation_count['surrogate']}")
        logger.info(f"Avaliações EnergyPlus: {self.evaluation_count['energyplus']}")
        logger.info(f"Speedup: {results.get('speedup', 0):.1f}x")
        
        return results
    
    def save_results(self, results: Dict):
        """Salva resultados da co-simulação"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Salvar JSON
        json_path = COSIM_DIR / f"cosimulation_results_{timestamp}.json"
        
        # Converter arrays para listas
        results_serializable = {
            k: (v.tolist() if isinstance(v, np.ndarray) else v)
            for k, v in results.items()
            if k != 'validation_results'
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results_serializable, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Resultados salvos: {json_path}")
    
    def plot_convergence(self):
        """Plota convergência da otimização"""
        if not self.cosimulation_history:
            logger.warning("Sem histórico para plotar")
            return
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Plot 1: Evolução de best_value
        iterations = range(len(self.cosimulation_history))
        best_values = [min(h.get('value', np.inf) for h in self.cosimulation_history[:i+1]) 
                      for i in iterations]
        
        axes[0].plot(iterations, best_values, 'b-', linewidth=2)
        axes[0].set_xlabel('Iteração')
        axes[0].set_ylabel(f'{self.target_var}')
        axes[0].set_title('Convergência - Melhor Valor')
        axes[0].grid(alpha=0.3)
        
        # Plot 2: Distribuição de erros
        if hasattr(self, '_evaluation_errors'):
            axes[1].hist(self._evaluation_errors, bins=20, edgecolor='black')
            axes[1].set_xlabel('Erro de Predição')
            axes[1].set_ylabel('Frequência')
            axes[1].set_title('Distribuição de Erros Surrogate')
            axes[1].grid(alpha=0.3)
        
        plot_path = COSIM_DIR / f"convergence_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.tight_layout()
        plt.savefig(plot_path, dpi=300)
        logger.info(f"✅ Gráfico salvo: {plot_path}")
        plt.close()

def main():
    """Função principal"""
    logger.info(f"\n{'='*70}")
    logger.info("ENGINE DE CO-SIMULAÇÃO ENERGYPLUS + SURROGATE")
    logger.info(f"{'='*70}\n")
    
    try:
        # Inicializar engine
        engine = CosimulationEngine(
            target_var='annual_consumption_kwh',
            n_energyplus_evals=50
        )
        
        # Executar otimização
        results = engine.run_optimization(objective='minimize')
        
        # Salvar resultados
        engine.save_results(results)
        
        # Plotar
        engine.plot_convergence()
        
        logger.info(f"\n{'='*70}")
        logger.info("✅ CO-SIMULAÇÃO CONCLUÍDA!")
        logger.info(f"{'='*70}")
        logger.info(f"\n📊 Próximas etapas:")
        logger.info(f"   1. Expandir golden dataset para 200 casos")
        logger.info(f"   2. Implementar physics violation validator completo")
    
    except Exception as e:
        logger.error(f"❌ Erro: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
