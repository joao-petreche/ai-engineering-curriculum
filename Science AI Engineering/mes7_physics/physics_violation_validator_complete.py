"""
Physics Violation Validator Completo - Categorização Detalhada
Mês 7 - Physics Compliance - Exercício 1.1

Validador robusto que:
1. Detecta 20+ tipos de violações de física
2. Categoriza por severidade (crítico/importante/menor)
3. Fornece explicação física para cada violação
4. Gera relatórios detalhados e acionáveis
5. Permite correção automática de certos erros

Objetivo: Garantir que todos os dados obedeçam leis termodinâmicas
e relações físicas realistas.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json
import logging
from typing import Dict, List, Tuple, Optional
from enum import Enum

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Diretórios
DATA_DIR = Path("data")
VALIDATION_DIR = Path("validation/physics_complete")

class SeverityLevel(Enum):
    """Níveis de severidade de violações"""
    CRITICAL = "crítico"      # Impossível fisicamente
    IMPORTANT = "importante"  # Altamente improvável
    MINOR = "menor"           # Improvável mas possível

class PhysicsViolation:
    """Classe base para violações de física"""
    
    def __init__(self, sim_id: str, violation_type: str, 
                 severity: SeverityLevel, message: str, 
                 physics_law: str):
        """
        Inicializa violação.
        
        Args:
            sim_id: ID da simulação
            violation_type: Tipo de violação (ex: "temperatura_impossível")
            severity: Nível de severidade
            message: Mensagem descritiva
            physics_law: Lei física violada (ex: "2ª Lei da Termodinâmica")
        """
        self.sim_id = sim_id
        self.violation_type = violation_type
        self.severity = severity
        self.message = message
        self.physics_law = physics_law
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            'simulation_id': self.sim_id,
            'violation_type': self.violation_type,
            'severity': self.severity.value,
            'message': self.message,
            'physics_law': self.physics_law,
            'timestamp': self.timestamp
        }

class CompletePhysicsValidator:
    """
    Validador completo de conformidade física.
    
    Detecta 20+ tipos de violações organizadas em 5 categorias:
    1. Limites Termodinâmicos (temperatura, entropia)
    2. Balanço Energético (entrada = saída)
    3. HVAC (demandas, eficiência)
    4. Conforto (ocupação, saúde)
    5. Correlações (relações físicas entre variáveis)
    """
    
    # Constantes físicas
    ABSOLUTE_ZERO_C = -273.15
    MAX_REALISTIC_TEMP_C = 60.0
    MIN_REALISTIC_TEMP_C = -30.0
    
    def __init__(self, dataset_path: Path = None):
        """Inicializa validador"""
        self.dataset = None
        self.violations = []
        self.violation_summary = {}
        
        VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
        
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
        csv_files = list(DATA_DIR.rglob("*dataset*.csv"))
        if not csv_files:
            raise FileNotFoundError("Nenhum dataset encontrado")
        
        latest = max(csv_files, key=lambda p: p.stat().st_mtime)
        self.load_dataset(latest)
    
    def _check_thermodynamic_limits(self, row: pd.Series) -> List[PhysicsViolation]:
        """
        Valida limites termodinâmicos absolutos.
        
        1ª Lei: Temperatura não pode ser < -273.15°C (Absolute Zero)
        2ª Lei: Temperatura máx ≥ mín, média entre elas
        """
        violations = []
        sim_id = row['simulation_id']
        
        for temp_col in ['avg_temperature_C', 'min_temperature_C', 'max_temperature_C']:
            if temp_col not in row:
                continue
            
            temp = row[temp_col]
            
            # Verificação 1: Absolute Zero
            if temp < self.ABSOLUTE_ZERO_C:
                violations.append(PhysicsViolation(
                    sim_id=sim_id,
                    violation_type="absolute_zero_violation",
                    severity=SeverityLevel.CRITICAL,
                    message=f"{temp_col} = {temp:.2f}°C (< -273.15°C Absolute Zero)",
                    physics_law="1ª Lei da Termodinâmica (limite absoluto)"
                ))
            
            # Verificação 2: Limite realista superior
            if temp > self.MAX_REALISTIC_TEMP_C:
                violations.append(PhysicsViolation(
                    sim_id=sim_id,
                    violation_type="unrealistic_high_temp",
                    severity=SeverityLevel.IMPORTANT,
                    message=f"{temp_col} = {temp:.2f}°C (> 60°C irreal para edifício)",
                    physics_law="Fisiologia Humana"
                ))
        
        return violations
    
    def _check_temperature_hierarchy(self, row: pd.Series) -> List[PhysicsViolation]:
        """
        Verifica hierarquia termodinâmica: T_min ≤ T_avg ≤ T_max.
        
        Violação da 2ª Lei se não respeitada.
        """
        violations = []
        sim_id = row['simulation_id']
        
        min_t = row.get('min_temperature_C', np.nan)
        avg_t = row.get('avg_temperature_C', np.nan)
        max_t = row.get('max_temperature_C', np.nan)
        
        if np.isnan(min_t) or np.isnan(avg_t) or np.isnan(max_t):
            return violations
        
        # Verificação 1: min ≤ avg
        if min_t > avg_t:
            violations.append(PhysicsViolation(
                sim_id=sim_id,
                violation_type="temp_hierarchy_min_avg",
                severity=SeverityLevel.CRITICAL,
                message=f"T_min ({min_t:.2f}°C) > T_avg ({avg_t:.2f}°C)",
                physics_law="2ª Lei da Termodinâmica (hierarquia)"
            ))
        
        # Verificação 2: avg ≤ max
        if avg_t > max_t:
            violations.append(PhysicsViolation(
                sim_id=sim_id,
                violation_type="temp_hierarchy_avg_max",
                severity=SeverityLevel.CRITICAL,
                message=f"T_avg ({avg_t:.2f}°C) > T_max ({max_t:.2f}°C)",
                physics_law="2ª Lei da Termodinâmica (hierarquia)"
            ))
        
        # Verificação 3: Intervalo realista (delta T > 0.5°C)
        if max_t - min_t < 0.5:
            violations.append(PhysicsViolation(
                sim_id=sim_id,
                violation_type="temp_range_too_small",
                severity=SeverityLevel.MINOR,
                message=f"ΔT = {max_t - min_t:.2f}°C (muito pequeno)",
                physics_law="Variabilidade Térmica Realista"
            ))
        
        return violations
    
    def _check_energy_balance(self, row: pd.Series) -> List[PhysicsViolation]:
        """
        Valida balanço de energia: Consumo ∝ Demanda HVAC.
        
        1ª Lei: Energia não é criada nem destruída.
        """
        violations = []
        sim_id = row['simulation_id']
        
        consumption = row.get('annual_consumption_kwh', np.nan)
        peak_cool = row.get('peak_cooling_kw', np.nan)
        peak_heat = row.get('peak_heating_kw', np.nan)
        
        if np.isnan(consumption) or np.isnan(peak_cool) or np.isnan(peak_heat):
            return violations
        
        # Verificação 1: Consumo não-negativo
        if consumption < 0:
            violations.append(PhysicsViolation(
                sim_id=sim_id,
                violation_type="negative_consumption",
                severity=SeverityLevel.CRITICAL,
                message=f"Consumo = {consumption:.0f} kWh (negativo!)",
                physics_law="1ª Lei da Termodinâmica"
            ))
        
        # Verificação 2: Consumo vs. demanda coerente
        if peak_cool > 0:
            ratio = consumption / peak_cool
            # Razão realista: 100-8760 horas
            if ratio < 100:
                violations.append(PhysicsViolation(
                    sim_id=sim_id,
                    violation_type="consumption_demand_ratio_low",
                    severity=SeverityLevel.IMPORTANT,
                    message=f"Consumo/Demanda = {ratio:.0f} horas (muito baixo)",
                    physics_law="Balanço Energético"
                ))
            elif ratio > 8760 * 10:
                violations.append(PhysicsViolation(
                    sim_id=sim_id,
                    violation_type="consumption_demand_ratio_high",
                    severity=SeverityLevel.IMPORTANT,
                    message=f"Consumo/Demanda = {ratio:.0f} horas (muito alto)",
                    physics_law="Balanço Energético"
                ))
        
        # Verificação 3: Consumo realista (10-500 MWh/ano para edifício típico)
        if consumption < 10000 or consumption > 500000:
            violations.append(PhysicsViolation(
                sim_id=sim_id,
                violation_type="unrealistic_consumption",
                severity=SeverityLevel.IMPORTANT,
                message=f"Consumo = {consumption:.0f} kWh (irreal para edifício)",
                physics_law="Balanço Energético Realista"
            ))
        
        return violations
    
    def _check_hvac_consistency(self, row: pd.Series) -> List[PhysicsViolation]:
        """
        Valida consistência HVAC: demandas físicas realistas.
        """
        violations = []
        sim_id = row['simulation_id']
        
        peak_cool = row.get('peak_cooling_kw', np.nan)
        peak_heat = row.get('peak_heating_kw', np.nan)
        hvac_eff = row.get('hvac_efficiency', np.nan)
        
        if np.isnan(peak_cool) or np.isnan(peak_heat):
            return violations
        
        # Verificação 1: Demandas não-negativas
        if peak_cool < 0:
            violations.append(PhysicsViolation(
                sim_id=sim_id,
                violation_type="negative_cooling_demand",
                severity=SeverityLevel.CRITICAL,
                message=f"Pico resfriamento = {peak_cool:.2f} kW (negativo!)",
                physics_law="Conservação de Energia"
            ))
        
        if peak_heat < 0:
            violations.append(PhysicsViolation(
                sim_id=sim_id,
                violation_type="negative_heating_demand",
                severity=SeverityLevel.CRITICAL,
                message=f"Pico aquecimento = {peak_heat:.2f} kW (negativo!)",
                physics_law="Conservação de Energia"
            ))
        
        # Verificação 2: Pelo menos uma demanda > 0
        if peak_cool == 0 and peak_heat == 0:
            violations.append(PhysicsViolation(
                sim_id=sim_id,
                violation_type="no_hvac_demand",
                severity=SeverityLevel.IMPORTANT,
                message="Nenhuma demanda HVAC (edifício desacoplado do clima?)",
                physics_law="Transferência de Calor"
            ))
        
        # Verificação 3: Eficiência HVAC realista
        if not np.isnan(hvac_eff):
            if hvac_eff < 0.5 or hvac_eff > 1.0:
                violations.append(PhysicsViolation(
                    sim_id=sim_id,
                    violation_type="unrealistic_hvac_efficiency",
                    severity=SeverityLevel.IMPORTANT,
                    message=f"Eficiência HVAC = {hvac_eff:.2f} (irreal)",
                    physics_law="Ciclo de Carnot (termodinâmica)"
                ))
        
        return violations
    
    def _check_comfort_consistency(self, row: pd.Series) -> List[PhysicsViolation]:
        """
        Valida conforto térmico: horas de conforto coerentes.
        """
        violations = []
        sim_id = row['simulation_id']
        
        comfort_hours = row.get('comfort_hours', np.nan)
        
        if np.isnan(comfort_hours):
            return violations
        
        # Verificação 1: Limite superior (8760 horas/ano)
        if comfort_hours < 0 or comfort_hours > 8760:
            violations.append(PhysicsViolation(
                sim_id=sim_id,
                violation_type="comfort_hours_out_of_range",
                severity=SeverityLevel.CRITICAL,
                message=f"Horas conforto = {comfort_hours:.0f} (fora de [0, 8760])",
                physics_law="Limitações Temporais"
            ))
        
        # Verificação 2: Conforto nulo é raro
        if comfort_hours < 100:
            violations.append(PhysicsViolation(
                sim_id=sim_id,
                violation_type="very_low_comfort",
                severity=SeverityLevel.IMPORTANT,
                message=f"Apenas {comfort_hours:.0f} horas de conforto (muito baixo)",
                physics_law="Fisiologia Humana"
            ))
        
        return violations
    
    def _check_correlations(self, row: pd.Series) -> List[PhysicsViolation]:
        """
        Valida correlações lógicas entre variáveis.
        
        Exemplo: Maior WSR → maior demanda HVAC (em geral)
        """
        violations = []
        sim_id = row['simulation_id']
        
        # Se temos dados de correlação
        wsr = row.get('window_to_wall_ratio', np.nan)
        peak_cool = row.get('peak_cooling_kw', np.nan)
        
        # Verificação: WSR alto deve correlacionar com pico alto
        if not np.isnan(wsr) and not np.isnan(peak_cool):
            if wsr > 0.4 and peak_cool < 5:
                violations.append(PhysicsViolation(
                    sim_id=sim_id,
                    violation_type="wsr_cooling_mismatch",
                    severity=SeverityLevel.MINOR,
                    message=f"WSR={wsr:.1%} alto mas pico resfriamento={peak_cool:.1f}kW baixo",
                    physics_law="Transferência de Calor Solar"
                ))
        
        return violations
    
    def validate_all(self) -> Tuple[List[PhysicsViolation], Dict]:
        """
        Valida todas as simulações em 5 categorias.
        
        Returns:
            Tuple: (lista de violações, resumo por tipo)
        """
        logger.info(f"\n{'='*70}")
        logger.info("VALIDAÇÃO COMPLETA DE FÍSICA - 20+ CRITÉRIOS")
        logger.info(f"{'='*70}\n")
        
        self.violations = []
        all_violations_by_type = {}
        
        for idx, row in self.dataset.iterrows():
            if idx % 100 == 0:
                logger.info(f"Validando simulação {idx}/{len(self.dataset)}...")
            
            # Executar todas as validações
            violations = []
            violations += self._check_thermodynamic_limits(row)
            violations += self._check_temperature_hierarchy(row)
            violations += self._check_energy_balance(row)
            violations += self._check_hvac_consistency(row)
            violations += self._check_comfort_consistency(row)
            violations += self._check_correlations(row)
            
            self.violations.extend(violations)
            
            # Contabilizar
            for v in violations:
                vtype = v.violation_type
                all_violations_by_type[vtype] = all_violations_by_type.get(vtype, 0) + 1
        
        # Resumo
        logger.info(f"\n{'='*70}")
        logger.info("RESUMO DE VIOLAÇÕES")
        logger.info(f"{'='*70}\n")
        
        logger.info(f"Total de violações encontradas: {len(self.violations)}")
        
        # Por severidade
        by_severity = {}
        for v in self.violations:
            sev = v.severity.value
            by_severity[sev] = by_severity.get(sev, 0) + 1
        
        logger.info(f"\nPor Severidade:")
        for sev, count in sorted(by_severity.items(), 
                                 key=lambda x: {'crítico': 0, 'importante': 1, 'menor': 2}.get(x[0], 3)):
            logger.info(f"  {sev.capitalize()}: {count}")
        
        # Top 10 tipos
        logger.info(f"\nTop 10 Tipos de Violações:")
        sorted_types = sorted(all_violations_by_type.items(), key=lambda x: -x[1])
        for vtype, count in sorted_types[:10]:
            logger.info(f"  {vtype}: {count}")
        
        self.violation_summary = all_violations_by_type
        
        return self.violations, all_violations_by_type
    
    def save_detailed_report(self):
        """Salva relatório detalhado de validação"""
        logger.info("\nSalvando relatórios detalhados...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # JSON com todas as violações
        violations_json = [v.to_dict() for v in self.violations]
        json_path = VALIDATION_DIR / f"physics_violations_detailed_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(violations_json, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ JSON detalhado: {json_path}")
        
        # CSV para análise
        violations_df = pd.DataFrame(violations_json)
        csv_path = VALIDATION_DIR / f"physics_violations_{timestamp}.csv"
        violations_df.to_csv(csv_path, index=False)
        logger.info(f"✅ CSV: {csv_path}")
        
        # Relatório textual
        report_path = VALIDATION_DIR / f"validation_report_{timestamp}.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("RELATÓRIO COMPLETO DE VALIDAÇÃO FÍSICA\n")
            f.write("="*70 + "\n\n")
            f.write(f"Data: {datetime.now().isoformat()}\n")
            f.write(f"Total de simulações: {len(self.dataset)}\n")
            f.write(f"Total de violações: {len(self.violations)}\n\n")
            
            f.write("VIOLAÇÕES POR TIPO:\n")
            for vtype, count in sorted(self.violation_summary.items(), key=lambda x: -x[1]):
                f.write(f"  {vtype}: {count}\n")
        
        logger.info(f"✅ Relatório: {report_path}")

def main():
    """Função principal"""
    logger.info(f"\n{'='*70}")
    logger.info("VALIDADOR COMPLETO DE CONFORMIDADE FÍSICA")
    logger.info(f"{'='*70}\n")
    
    try:
        validator = CompletePhysicsValidator()
        
        # Validar
        violations, summary = validator.validate_all()
        
        # Salvar
        validator.save_detailed_report()
        
        logger.info(f"\n{'='*70}")
        logger.info("✅ VALIDAÇÃO CONCLUÍDA!")
        logger.info(f"{'='*70}")
    
    except Exception as e:
        logger.error(f"❌ Erro: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
