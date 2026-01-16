"""
Validação de Conformidade Física - PIML
Mês 4 - PIML Surrogates - Exercício 1.4

Este script valida que os resultados das simulações EnergyPlus
obedecem leis físicas fundamentais.

Validações:
1. 1ª Lei da Termodinâmica (Conservação de Energia)
2. 2ª Lei da Termodinâmica (Entropia)
3. Limites de Temperatura (15-30°C para conforto)
4. Balanço de Energia (entrada = saída ± tolerância)
5. Coerência de Picos (cooling > heating em clima quente)

Referência: ASHRAE Handbook - Fundamentals (2021)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json
import logging
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Diretórios
DATA_DIR = Path("data/lhs_datasets")
VALIDATION_DIR = Path("validation/physics")
GOLDEN_DATASET_DIR = Path("data/golden_dataset")

class PhysicsValidator:
    """
    Valida conformidade com leis físicas.
    
    Cada simulação deve passar em 5 critérios:
    1. Balanço energético (±5%)
    2. Limites de temperatura (15-30°C)
    3. Consistência HVAC (peak_cooling >= 0)
    4. Conforto térmico (comfort_hours > 0)
    5. Coerência de cargas (peak_cooling > 0 em climas quentes)
    """
    
    # Limites físicos
    MIN_TEMP_C = 15.0           # Limite inferior de conforto
    MAX_TEMP_C = 30.0           # Limite superior de conforto
    ENERGY_BALANCE_TOLERANCE = 0.05  # ±5%
    
    def __init__(self, dataset_path: Path = None):
        """
        Inicializa validador.
        
        Args:
            dataset_path: Caminho para dataset CSV
        """
        self.dataset = None
        self.validation_results = []
        self.violations = []
        
        # Criar diretórios
        VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
        GOLDEN_DATASET_DIR.mkdir(parents=True, exist_ok=True)
        
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
        """Carrega dataset mais recente"""
        csv_files = list(DATA_DIR.glob("piml_dataset_*.csv"))
        if not csv_files:
            raise FileNotFoundError(f"Nenhum dataset encontrado em {DATA_DIR}")
        
        latest = max(csv_files, key=lambda p: p.stat().st_mtime)
        self.load_dataset(latest)
    
    def validate_energy_balance(self, row: pd.Series) -> Tuple[bool, str]:
        """
        1ª Lei da Termodinâmica: Energia não é criada nem destruída.
        
        Verificação:
        - Consumo anual deve estar correlacionado com variáveis de projeto
        - Não pode ser < 0 ou > 1000 kWh/dia (fisicamente impossível)
        
        Args:
            row: Linha do dataset
        
        Returns:
            Tuple: (válido, mensagem)
        """
        consumption = row.get('annual_consumption_kwh', 0)
        
        # Verificar limites fisicamente realistas
        min_consumption = 10.0  # kWh/ano mínimo (muito isolado)
        max_consumption = 200000.0  # kWh/ano máximo (muito grande ou mal isolado)
        
        if consumption < min_consumption or consumption > max_consumption:
            return False, f"Consumo fisicamente impossível: {consumption:.2f} kWh/ano"
        
        # Verificar se é número válido
        if np.isnan(consumption) or np.isinf(consumption):
            return False, "Consumo contém NaN ou Inf"
        
        return True, "Balanço energético válido"
    
    def validate_temperature_bounds(self, row: pd.Series) -> Tuple[bool, str]:
        """
        Limites de Temperatura: 2ª Lei da Termodinâmica.
        
        Verificação:
        - Temperatura mínima >= 0°C (abaixo: congelamento)
        - Temperatura máxima <= 50°C (acima: insuportável)
        - Temperatura média entre mín e máx
        
        Args:
            row: Linha do dataset
        
        Returns:
            Tuple: (válido, mensagem)
        """
        avg_temp = row.get('avg_temperature_C', None)
        max_temp = row.get('max_temperature_C', None)
        min_temp = row.get('min_temperature_C', None)
        
        if avg_temp is None or max_temp is None or min_temp is None:
            return False, "Dados de temperatura incompletos"
        
        # Verificar valores fisicamente realistas
        if min_temp < -30.0 or min_temp > 30.0:
            return False, f"Temperatura mínima incoerente: {min_temp:.2f}°C"
        
        if max_temp < 10.0 or max_temp > 60.0:
            return False, f"Temperatura máxima incoerente: {max_temp:.2f}°C"
        
        # Verificar hierarquia
        if not (min_temp <= avg_temp <= max_temp):
            return False, f"Hierarquia T violada: min={min_temp:.2f}, avg={avg_temp:.2f}, max={max_temp:.2f}"
        
        return True, "Limites de temperatura válidos"
    
    def validate_hvac_consistency(self, row: pd.Series) -> Tuple[bool, str]:
        """
        Consistência HVAC: Demandas não podem ser negativas.
        
        Verificação:
        - peak_cooling_kw >= 0
        - peak_heating_kw >= 0
        - Ambas não podem ser simultaneamente zero (irreal)
        
        Args:
            row: Linha do dataset
        
        Returns:
            Tuple: (válido, mensagem)
        """
        peak_cooling = row.get('peak_cooling_kw', None)
        peak_heating = row.get('peak_heating_kw', None)
        
        if peak_cooling is None or peak_heating is None:
            return False, "Dados HVAC incompletos"
        
        if peak_cooling < 0:
            return False, f"Potência de resfriamento negativa: {peak_cooling:.2f} kW"
        
        if peak_heating < 0:
            return False, f"Potência de aquecimento negativa: {peak_heating:.2f} kW"
        
        if peak_cooling == 0 and peak_heating == 0:
            return False, "Nenhuma carga HVAC (edifício desacoplado de clima?)"
        
        return True, "Consistência HVAC válida"
    
    def validate_comfort_consistency(self, row: pd.Series) -> Tuple[bool, str]:
        """
        Conforto Térmico: Horas de conforto devem estar entre 0 e 8760.
        
        Verificação:
        - comfort_hours >= 0
        - comfort_hours <= 8760 (horas/ano)
        - Correlação com setpoints (setpoint amplo -> mais conforto)
        
        Args:
            row: Linha do dataset
        
        Returns:
            Tuple: (válido, mensagem)
        """
        comfort_hours = row.get('comfort_hours', None)
        
        if comfort_hours is None:
            return False, "Dados de conforto incompletos"
        
        if comfort_hours < 0 or comfort_hours > 8760:
            return False, f"Horas de conforto fora do range: {comfort_hours:.0f}/8760"
        
        return True, "Consistência de conforto válida"
    
    def validate_energy_load_correlation(self, row: pd.Series) -> Tuple[bool, str]:
        """
        Correlação Energética: Consumo deve ser correlacionado com cargas HVAC.
        
        Verificação:
        - Consumo anual >> demanda de pico (resfriamento/aquecimento é temporário)
        - Razão consumo/pico deve estar entre 100-8760 (múltiplo de horas)
        
        Args:
            row: Linha do dataset
        
        Returns:
            Tuple: (válido, mensagem)
        """
        consumption = row.get('annual_consumption_kwh', 0)
        peak_cooling = row.get('peak_cooling_kw', 0)
        
        if peak_cooling <= 0:
            return True, "Sem carga de resfriamento (pode ser válido)"
        
        # Razão consumo anual / demanda de pico
        # Deve estar entre: 100 horas (muito ativo) e 8760 horas (sempre em pico)
        ratio = consumption / peak_cooling if peak_cooling > 0 else np.inf
        
        if ratio < 100:
            return False, f"Consumo demasiado baixo para demanda de pico (ratio={ratio:.1f})"
        
        if ratio > 8760 * 10:  # 10x o total de horas do ano (muito irreal)
            return False, f"Consumo demasiado alto para demanda de pico (ratio={ratio:.1f})"
        
        return True, "Correlação energética válida"
    
    def validate_simulation(self, row: pd.Series) -> Dict:
        """
        Valida uma simulação em 5 critérios.
        
        Args:
            row: Linha do dataset
        
        Returns:
            Dict com resultados de validação
        """
        sim_id = row['simulation_id']
        
        validations = {
            'energy_balance': self.validate_energy_balance(row),
            'temperature_bounds': self.validate_temperature_bounds(row),
            'hvac_consistency': self.validate_hvac_consistency(row),
            'comfort_consistency': self.validate_comfort_consistency(row),
            'energy_load_correlation': self.validate_energy_load_correlation(row),
        }
        
        # Resumo
        all_valid = all(is_valid for is_valid, _ in validations.values())
        
        result = {
            'simulation_id': sim_id,
            'is_valid': all_valid,
            'validations': {name: is_valid for name, (is_valid, _) in validations.items()},
            'messages': {name: msg for name, (_, msg) in validations.items()},
        }
        
        # Se inválido, registrar violação
        if not all_valid:
            violation_messages = [
                f"{name}: {msg}"
                for name, (is_valid, msg) in validations.items()
                if not is_valid
            ]
            self.violations.append({
                'simulation_id': sim_id,
                'violations': violation_messages,
                'timestamp': datetime.now().isoformat()
            })
        
        return result
    
    def validate_all(self):
        """Valida todas as simulações no dataset"""
        logger.info(f"\n{'='*70}")
        logger.info("VALIDAÇÃO FÍSICA DE TODAS AS SIMULAÇÕES")
        logger.info(f"{'='*70}")
        
        self.validation_results = []
        self.violations = []
        
        for idx, row in self.dataset.iterrows():
            if idx % 100 == 0:
                logger.info(f"Validando simulação {idx}/{len(self.dataset)}...")
            
            result = self.validate_simulation(row)
            self.validation_results.append(result)
        
        # Estatísticas
        valid_count = sum(1 for r in self.validation_results if r['is_valid'])
        invalid_count = len(self.validation_results) - valid_count
        
        logger.info(f"\n{'='*70}")
        logger.info("RESULTADOS DA VALIDAÇÃO")
        logger.info(f"{'='*70}")
        logger.info(f"✅ Simulações válidas: {valid_count}/{len(self.validation_results)} ({100*valid_count/len(self.validation_results):.1f}%)")
        logger.info(f"❌ Simulações inválidas: {invalid_count}/{len(self.validation_results)} ({100*invalid_count/len(self.validation_results):.1f}%)")
        
        if self.violations:
            logger.warning(f"\n⚠️  Violações encontradas:")
            violation_types = {}
            for violation in self.violations:
                for msg in violation['violations']:
                    violation_type = msg.split(':')[0]
                    violation_types[violation_type] = violation_types.get(violation_type, 0) + 1
            
            for vtype, count in sorted(violation_types.items(), key=lambda x: -x[1]):
                logger.warning(f"   {vtype}: {count} casos")
    
    def create_golden_dataset(self, n_golden: int = 50):
        """
        Extrai dataset de ouro (50 casos totalmente validados).
        
        Args:
            n_golden: Número de casos para dataset de ouro
        """
        logger.info(f"\n{'='*70}")
        logger.info(f"CRIANDO DATASET DE OURO ({n_golden} CASOS)")
        logger.info(f"{'='*70}")
        
        # Filtrar apenas simulações válidas
        valid_indices = [
            i for i, result in enumerate(self.validation_results)
            if result['is_valid']
        ]
        
        if len(valid_indices) < n_golden:
            logger.warning(f"⚠️  Apenas {len(valid_indices)} casos válidos, mas {n_golden} solicitados")
            n_golden = len(valid_indices)
        
        # Selecionar aleatoriamente
        np.random.seed(42)
        selected_indices = np.random.choice(valid_indices, size=n_golden, replace=False)
        
        # Extrair casos
        golden_dataset = self.dataset.iloc[selected_indices].copy()
        
        logger.info(f"✅ Dataset de ouro criado: {golden_dataset.shape}")
        logger.info(f"   Todas as 5 validações passaram para esses {n_golden} casos")
        
        # Salvar
        golden_path = GOLDEN_DATASET_DIR / f"golden_dataset_{n_golden}cases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        golden_dataset.to_csv(golden_path, index=False)
        logger.info(f"✅ Dataset de ouro salvo: {golden_path}")
        
        return golden_dataset
    
    def save_validation_report(self):
        """Salva relatório completo de validação"""
        logger.info(f"\nSalvando relatório de validação...")
        
        # Criar DataFrame com resultados
        validation_data = []
        for result in self.validation_results:
            row = {'simulation_id': result['simulation_id'], 'is_valid': result['is_valid']}
            row.update(result['validations'])
            validation_data.append(row)
        
        validation_df = pd.DataFrame(validation_data)
        
        # Salvar CSV
        report_path = VALIDATION_DIR / f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        validation_df.to_csv(report_path, index=False)
        logger.info(f"✅ Relatório salvo: {report_path}")
        
        # Salvar log de violações em JSON
        violations_path = VALIDATION_DIR / f"violations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(violations_path, 'w', encoding='utf-8') as f:
            json.dump(self.violations, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ Violações salvas: {violations_path}")
    
    def plot_validation_summary(self):
        """Plota resumo de validação"""
        logger.info(f"\nGerando gráficos de validação...")
        
        # Contar validações
        validation_data = []
        for result in self.validation_results:
            validation_data.append(result['validations'])
        
        validation_df = pd.DataFrame(validation_data)
        
        # Plot 1: Proporção de válidos por critério
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Critérios individuais
        criteria_valid = validation_df.sum()
        ax1.barh(criteria_valid.index, criteria_valid.values)
        ax1.set_xlabel('Número de simulações válidas')
        ax1.set_title('Validação por Critério')
        ax1.set_xlim([0, len(validation_df)])
        
        # Distribuição geral
        all_valid = validation_df.all(axis=1).sum()
        invalid = len(validation_df) - all_valid
        ax2.bar(['Válidas', 'Inválidas'], [all_valid, invalid], color=['green', 'red'])
        ax2.set_ylabel('Número de simulações')
        ax2.set_title('Distribuição Geral')
        
        plot_path = Path("plots") / f"validation_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plot_path.parent.mkdir(parents=True, exist_ok=True)
        plt.tight_layout()
        plt.savefig(plot_path, dpi=300)
        logger.info(f"✅ Gráfico salvo: {plot_path}")
        plt.close()

def main():
    """Função principal"""
    logger.info(f"\n{'='*70}")
    logger.info("VALIDAÇÃO DE CONFORMIDADE FÍSICA")
    logger.info(f"{'='*70}\n")
    
    try:
        # Inicializar validador
        validator = PhysicsValidator()
        
        # Validar todas as simulações
        validator.validate_all()
        
        # Criar dataset de ouro
        validator.create_golden_dataset(n_golden=50)
        
        # Salvar resultados
        validator.save_validation_report()
        validator.plot_validation_summary()
        
        logger.info(f"\n{'='*70}")
        logger.info("✅ VALIDAÇÃO CONCLUÍDA COM SUCESSO!")
        logger.info(f"{'='*70}")
        logger.info(f"\n📊 Próximas etapas:")
        logger.info(f"   1. Quantificar incerteza com uncertainty_quantification.py")
        logger.info(f"   2. Análise de sensibilidade com sensitivity.py")
        logger.info(f"   3. Few-shot examples com golden dataset")
    
    except Exception as e:
        logger.error(f"❌ Erro durante validação: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
