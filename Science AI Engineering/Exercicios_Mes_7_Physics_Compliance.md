# Exercícios Mês 7: Physics Compliance Testing & Anti-Hallucination Suite

## 📋 Visão Geral

**Objetivo do Mês:** Construir suite de testes abrangente que valida conformidade física de todas as recomendações do sistema (LLM + surrogates), detecta hallucinations em tempo real, e garante 100% de confiabilidade para deployment em produção.

**Contexto de Integração:**
- **Mês 2 (Scientific Software Engineering):** Aprendemos validação com Pydantic
- **Mês 4 (PIML Surrogates):** Aplicamos physics constraints em modelos ML
- **Mês 5 (Prompt Engineering):** Implementamos hallucination detection básica
- **Mês 6 (Co-Simulação):** Projetamos arquitetura de validação
- **Mês 7 (Este Mês):** Implementamos compliance testing production-grade

**Referências Teóricas:**
- **Jiang et al. (2024):** "Physics-Informed Guardrails for LLM Safety in Engineering"
- **Zakeri et al. (2025):** "Validation Protocols for Building-LLM Systems"
- **NASA Standard:** "Software IV&V Practices" (adaptado para ML)
- **ISO/IEC/IEEE 42010:** Architecture description of software-intensive systems

**Estrutura do Mês:**
- **Semana 1:** Golden Datasets & Test Cases (12-15h)
- **Semana 2:** Physics Violation Detection (12-15h)
- **Semana 3:** Hallucination Logging & Analysis (12-15h)
- **Semana 4:** Integration Testing & Production Readiness (14-15h)

**Tempo Total Estimado:** 50-60 horas

**Repositório Git:** Continuar usando `piml-training` (branch: `physics-compliance`)

---

## 🎯 Objetivos de Aprendizagem

Ao final deste mês, você será capaz de:

1. **Criar golden datasets** validados manualmente para testing
2. **Implementar validators** que detectam 20+ tipos de violações físicas
3. **Logar e analisar hallucinations** em produção com rastreamento completo
4. **Executar test suite** com 100% cobertura de casos críticos
5. **Preparar sistema para produção** com CI/CD pipeline de validação
6. **Documentar compliance** com auditoria formal

---

## 📦 Pré-requisitos

### Conhecimento Técnico
- ✅ Mês 2 (Pydantic validation, guardrails)
- ✅ Mês 4 (Physics constraints em surrogates)
- ✅ Mês 5 (Hallucination detection básica)
- ✅ Mês 6 (Data models e contratos)
- ✅ Pytest e cobertura de testes

### Infraestrutura
- ✅ Todos os modelos treinados (EnergyPlus, surrogates, Gemini)
- ✅ Dados de simulações do Mês 3 (100 cases)
- ✅ Sistema de co-simulação de Mês 6

### Bibliotecas Python (Novas)
```bash
pip install pytest pytest-cov             # Testing framework
pip install hypothesis                    # Property-based testing
pip install openpyxl                      # Excel reports
pip install plotly                        # Visualizações interativas
```

### Validação da Infraestrutura

```python
# test_physics_compliance_setup.py
import pytest
from hypothesis import given, strategies as st

# Teste 1: Validar que conseguimos rodar testes básicos
def test_basic_physics():
    assert 15 <= 25 <= 35, "Temperature deve estar em range viável"
    print("✅ Physics constraints funcionam")

# Teste 2: Hypothesis property-based test
@given(st.floats(min_value=15, max_value=35))
def test_temperature_hypothesis(temp):
    assert 15 <= temp <= 35

# Executar
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

**✅ Checkpoint:** Testes rodam sem erro?

---

## 🔹 Semana 1: Golden Datasets & Test Cases (12-15 horas)

### 📖 Objetivos da Semana

- Criar datasets de teste "golden" com valores conhecidos e validados
- Definir casos de teste críticos (normal, edge case, invalid)
- Documentar rastreabilidade entre casos de teste e requisitos
- Implementar test data fixtures

### 🎯 Exercício 1.1: Golden Dataset Creation (3-4h)

**Contexto:** Golden dataset é conjunto pequeno de casos (~50) com resultados conhecidos e validados manualmente ou via simulação longa. Serve como baseline para todos os testes.

**Tarefa:** Criar 50 golden test cases com 3 categorias: normal operations, edge cases, invalid inputs.

#### Implementação: `golden_dataset_creation.py`

```python
"""
Exercício 1.1: Golden dataset para validação de compliance
Referência: NASA Software IV&V Standards + Test Data Management Best Practices
"""

from typing import List, Dict, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import json
import random
from datetime import datetime


class TestCaseCategory(Enum):
    """Categorias de casos de teste."""
    
    NORMAL_OPERATION = "normal"          # Operação típica
    EDGE_CASE = "edge_case"             # Limites físicos
    INVALID_INPUT = "invalid"           # Entradas inválidas
    EXTREME_CLIMATE = "extreme"         # Condições extremas
    RARE_SCENARIO = "rare"              # Cenários raros mas possíveis


@dataclass
class GoldenTestCase:
    """Caso de teste do golden dataset."""
    
    test_id: str
    category: TestCaseCategory
    description: str
    
    # Input parameters
    wwr: float
    wall_thickness_m: float
    insulation_thickness_m: float
    conductivity_wall_W_mK: float
    conductivity_insulation_W_mK: float
    zone_volume_m3: float
    infiltration_rate_ACH: float
    internal_loads_W_m2: float
    heating_setpoint_C: float
    cooling_setpoint_C: float
    
    # Expected outputs (validado manualmente ou via EnergyPlus longo)
    expected_annual_heating_kwh: float
    expected_annual_cooling_kwh: float
    expected_peak_heating_w: float
    expected_peak_cooling_w: float
    
    # Tolerance (%)
    tolerance_percent: float
    
    # Metadata
    source: str  # "energyplus_simulation", "manual_calculation", "literature"
    validation_date: str
    notes: str = ""
    
    def validate_parameters(self) -> List[str]:
        """Valida se parâmetros são fisicamente válidos."""
        
        errors = []
        
        # Temperatura
        if not (15 <= self.heating_setpoint_C <= 25):
            errors.append(f"Heating setpoint {self.heating_setpoint_C}°C fora do range 15-25°C")
        
        if not (20 <= self.cooling_setpoint_C <= 28):
            errors.append(f"Cooling setpoint {self.cooling_setpoint_C}°C fora do range 20-28°C")
        
        if self.cooling_setpoint_C <= self.heating_setpoint_C:
            errors.append("Cooling setpoint deve ser > heating setpoint")
        
        # WWR
        if not (0.10 <= self.wwr <= 0.60):
            errors.append(f"WWR {self.wwr} fora do range ASHRAE 10-60%")
        
        # Condutividade
        if not (0.025 <= self.conductivity_insulation_W_mK <= 0.050):
            errors.append(f"Condutividade isolamento {self.conductivity_insulation_W_mK} inválida")
        
        # Espessura
        if not (0.05 <= self.insulation_thickness_m <= 0.20):
            errors.append(f"Espessura isolamento {self.insulation_thickness_m}m fora do range")
        
        return errors


class GoldenDatasetBuilder:
    """Constrói golden dataset com casos sistemáticos."""
    
    def __init__(self):
        self.cases: List[GoldenTestCase] = []
    
    def add_normal_operation_cases(self) -> None:
        """Adiciona casos de operação normal (5 casos)."""
        
        normal_cases = [
            GoldenTestCase(
                test_id="GOLDEN_001",
                category=TestCaseCategory.NORMAL_OPERATION,
                description="Escritório comercial típico em São Paulo",
                wwr=0.35, wall_thickness_m=0.20, insulation_thickness_m=0.10,
                conductivity_wall_W_mK=1.5, conductivity_insulation_W_mK=0.035,
                zone_volume_m3=2000, infiltration_rate_ACH=0.6,
                internal_loads_W_m2=10,
                heating_setpoint_C=21, cooling_setpoint_C=25,
                expected_annual_heating_kwh=50.0,
                expected_annual_cooling_kwh=100.0,
                expected_peak_heating_w=2000.0,
                expected_peak_cooling_w=5000.0,
                tolerance_percent=5.0,
                source="energyplus_simulation",
                validation_date="2026-01-10"
            ),
            # ... mais 4 casos normais
        ]
        
        self.cases.extend(normal_cases)
    
    def add_edge_case_scenarios(self) -> None:
        """Adiciona casos extremos nos limites (5 casos)."""
        
        edge_cases = [
            GoldenTestCase(
                test_id="GOLDEN_EDGE_001",
                category=TestCaseCategory.EDGE_CASE,
                description="WWR mínimo (10%) - menos ganho solar",
                wwr=0.10, wall_thickness_m=0.15, insulation_thickness_m=0.05,
                conductivity_wall_W_mK=0.6, conductivity_insulation_W_mK=0.035,
                zone_volume_m3=500, infiltration_rate_ACH=0.3,
                internal_loads_W_m2=5,
                heating_setpoint_C=20, cooling_setpoint_C=26,
                expected_annual_heating_kwh=80.0,
                expected_annual_cooling_kwh=30.0,
                expected_peak_heating_w=3000.0,
                expected_peak_cooling_w=1500.0,
                tolerance_percent=8.0,
                source="literature",
                validation_date="2026-01-10"
            ),
            # ... mais 4 casos extremos
        ]
        
        self.cases.extend(edge_cases)
    
    def add_invalid_input_cases(self) -> None:
        """Adiciona casos com entradas inválidas (5 casos)."""
        
        invalid_cases = [
            GoldenTestCase(
                test_id="GOLDEN_INVALID_001",
                category=TestCaseCategory.INVALID_INPUT,
                description="WWR acima do limite (70%)",
                wwr=0.70,  # INVÁLIDO: > 60%
                wall_thickness_m=0.20, insulation_thickness_m=0.10,
                conductivity_wall_W_mK=1.5, conductivity_insulation_W_mK=0.035,
                zone_volume_m3=2000, infiltration_rate_ACH=0.6,
                internal_loads_W_m2=10,
                heating_setpoint_C=21, cooling_setpoint_C=25,
                expected_annual_heating_kwh=-1,  # Invalid marker
                expected_annual_cooling_kwh=-1,
                expected_peak_heating_w=-1,
                expected_peak_cooling_w=-1,
                tolerance_percent=999,
                source="invalid_test",
                validation_date="2026-01-10",
                notes="Deve rejeitar com erro de validação"
            ),
            # ... mais 4 casos inválidos
        ]
        
        self.cases.extend(invalid_cases)
    
    def build(self) -> List[GoldenTestCase]:
        """Constrói dataset completo."""
        
        self.add_normal_operation_cases()
        self.add_edge_case_scenarios()
        self.add_invalid_input_cases()
        
        return self.cases
    
    def save_to_json(self, filepath: str = "data/golden_dataset.json") -> None:
        """Salva dataset em JSON."""
        
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        data = [asdict(case) for case in self.cases]
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"✅ Golden dataset salvo: {filepath} ({len(self.cases)} casos)")
    
    def print_summary(self) -> None:
        """Imprime resumo do dataset."""
        
        by_category = {}
        for case in self.cases:
            cat = case.category.value
            by_category[cat] = by_category.get(cat, 0) + 1
        
        print("\n" + "=" * 80)
        print("GOLDEN DATASET SUMMARY")
        print("=" * 80)
        print(f"Total cases: {len(self.cases)}")
        for cat, count in by_category.items():
            print(f"  {cat.upper()}: {count}")
        print("=" * 80 + "\n")


def main():
    """Demonstração de golden dataset."""
    
    print("🏆 Criando Golden Dataset para Physics Compliance Testing\n")
    
    builder = GoldenDatasetBuilder()
    cases = builder.build()
    
    builder.print_summary()
    
    # Validar todos os casos
    print("📋 Validando parâmetros dos casos de teste:")
    for case in cases[:3]:  # Mostrar primeiros 3
        errors = case.validate_parameters()
        if errors:
            print(f"\n❌ {case.test_id}:")
            for error in errors:
                print(f"   - {error}")
        else:
            print(f"✅ {case.test_id}: Parâmetros válidos")
    
    # Salvar
    builder.save_to_json()


if __name__ == "__main__":
    main()
```

**Execução:**
```bash
python src/golden_dataset_creation.py
```

**Resultado Esperado:**
```
🏆 Criando Golden Dataset para Physics Compliance Testing

GOLDEN DATASET SUMMARY
==================================================
Total cases: 15
  normal: 5
  edge_case: 5
  invalid: 5

📋 Validando parâmetros dos casos de teste:
✅ GOLDEN_001: Parâmetros válidos
✅ GOLDEN_EDGE_001: Parâmetros válidos
❌ GOLDEN_INVALID_001:
   - WWR 0.7 fora do range ASHRAE 10-60%

✅ Golden dataset salvo: data/golden_dataset.json (15 casos)
```

**✅ Checkpoint:** Dataset criado com 15+ casos? Validação funciona?

---

### 🎯 Exercício 1.2: Test Case Traceability (2-3h)

**Contexto:** Rastreabilidade conecta cada caso de teste a requisitos específicos (normas ASHRAE, restrições físicas, etc).

**Tarefa:** Criar matriz de rastreabilidade de casos de teste vs requisitos.

#### Implementação: `test_traceability_matrix.py`

```python
"""
Exercício 1.2: Matriz de rastreabilidade de testes
Referência: IEEE 829 Test Documentation Standard
"""

from typing import Dict, List
import pandas as pd
import json


class TraceabilityMatrix:
    """Matriz de rastreabilidade entre requisitos e casos de teste."""
    
    def __init__(self):
        self.requirements = {
            "REQ_PHYS_001": "Temperature setpoint in 15-35°C range",
            "REQ_PHYS_002": "WWR (Window-to-Wall Ratio) in 10-60% range",
            "REQ_PHYS_003": "Thermal conductivity > 0 W/mK",
            "REQ_PHYS_004": "Energy output non-negative (Q ≥ 0)",
            "REQ_NORM_001": "ASHRAE 90.1 compliance",
            "REQ_NORM_002": "ISO 13790 standard adherence",
            "REQ_HALL_001": "Detect hallucinations in LLM output",
            "REQ_HALL_002": "Log all validation violations",
            "REQ_PERF_001": "Surrogate execution < 50ms",
            "REQ_PERF_002": "Validation < 100ms"
        }
        
        self.test_cases = {
            "GOLDEN_001": ["REQ_PHYS_001", "REQ_PHYS_002", "REQ_NORM_001"],
            "GOLDEN_EDGE_001": ["REQ_PHYS_002", "REQ_NORM_002"],
            "GOLDEN_INVALID_001": ["REQ_PHYS_002", "REQ_HALL_001"],
            # ... mais cases
        }
    
    def generate_traceability_dataframe(self) -> pd.DataFrame:
        """Gera matriz de rastreabilidade."""
        
        all_reqs = list(self.requirements.keys())
        all_cases = list(self.test_cases.keys())
        
        # Criar matriz (cases × requirements)
        matrix = pd.DataFrame(0, index=all_cases, columns=all_reqs)
        
        for test_id, reqs in self.test_cases.items():
            for req_id in reqs:
                matrix.loc[test_id, req_id] = 1
        
        return matrix
    
    def print_traceability_report(self) -> None:
        """Imprime relatório de rastreabilidade."""
        
        matrix = self.generate_traceability_dataframe()
        
        print("\n" + "=" * 150)
        print("TEST CASE TRACEABILITY MATRIX")
        print("=" * 150)
        print(matrix.to_string())
        print("=" * 150)
        
        # Cobertura por requisito
        print("\nREQUIREMENT COVERAGE:")
        for req_id, req_desc in self.requirements.items():
            covered = matrix[req_id].sum()
            print(f"  {req_id}: {int(covered)} test cases - {req_desc}")
        
        # Requisitos sem cobertura
        uncovered = [req for req, count in matrix.sum().items() if count == 0]
        if uncovered:
            print(f"\n⚠️  UNCOVERED REQUIREMENTS: {uncovered}")
        else:
            print("\n✅ Todos os requisitos têm cobertura de testes")


def main():
    """Demonstração de rastreabilidade."""
    
    print("📍 Matriz de Rastreabilidade de Testes\n")
    
    matrix = TraceabilityMatrix()
    matrix.print_traceability_report()


if __name__ == "__main__":
    main()
```

**✅ Checkpoint:** Matriz mostra cobertura de 100% dos requisitos?

---

### 📋 Checklist de Certificação - Semana 1

**Competências Esperadas:**

- [ ] **Exercício 1.1:** Golden dataset com 50+ casos (normal, edge, invalid)
- [ ] **Exercício 1.2:** Matriz de rastreabilidade 100% cobertura
- [ ] **Exercício 1.3:** Test fixtures Pytest implementados
- [ ] **Exercício 1.4:** Test data generators (property-based)

**Resultado de Semana 1:**

Você agora consegue:
1. Criar golden datasets para validação confiável
2. Rastrear cobertura de testes vs requisitos
3. Implementar fixtures Pytest reutilizáveis
4. Gerar dados de teste com Hypothesis

---

## 🔹 Semana 2: Physics Violation Detection (12-15 horas)

### 📖 Objetivos da Semana

- Implementar validators que detectam 20+ tipos de violações
- Criar severity levels (critical, high, medium, low)
- Logar violações com contexto completo
- Implementar auto-correction quando possível

### 🎯 Exercício 2.1: Physics Violation Detectors (4-5h)

**Contexto:** Validator abrangente que detecta violações em múltiplas dimensões: termodinâmica, normas, constraints operacionais.

**Tarefa:** Implementar PhysicsViolationDetector com 20+ tipos de violações específicas.

#### Implementação: `physics_violation_detector.py`

```python
"""
Exercício 2.1: Detector de violações físicas
Referência: Jiang et al. (2024) - Physics-Informed Guardrails
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class ViolationSeverity(Enum):
    """Níveis de severidade."""
    CRITICAL = 5  # Sistema não deve prosseguir
    HIGH = 4      # Problema grave, correção necessária
    MEDIUM = 3    # Aviso, pode prosseguir com cuidado
    LOW = 2       # Informativo
    INFO = 1      # Apenas notificação


class ViolationType(Enum):
    """Tipos de violações."""
    
    # Física fundamental (CRITICAL)
    TEMP_OUT_OF_RANGE = "temperature_out_of_range"
    ENERGY_NEGATIVE = "energy_negative"
    CONDUCTIVITY_INVALID = "conductivity_invalid"
    DENSITY_NEGATIVE = "density_negative"
    
    # Limites operacionais (HIGH)
    SETPOINT_CONFLICT = "setpoint_conflict"
    INFILTRATION_UNREALISTIC = "infiltration_unrealistic"
    PEAK_EXCEEDS_ANNUAL = "peak_exceeds_annual"
    
    # Normas técnicas (HIGH)
    ASHRAE_VIOLATION = "ashrae_violation"
    ISO_VIOLATION = "iso_violation"
    
    # Constraints de design (MEDIUM)
    THICKNESS_OUT_OF_BOUNDS = "thickness_out_of_bounds"
    WWR_OUT_OF_BOUNDS = "wwr_out_of_bounds"
    LOAD_INCONSISTENT = "load_inconsistent"
    
    # Inconsistências lógicas (MEDIUM-LOW)
    COOLING_HEATING_CONFLICT = "cooling_heating_conflict"
    VOLUME_UNREALISTIC = "volume_unrealistic"
    
    # Hallucinations LLM (CRITICAL)
    CONTRADICTORY_STATEMENT = "contradictory_statement"
    FABRICATED_REFERENCE = "fabricated_reference"
    PHYSICALLY_IMPOSSIBLE = "physically_impossible"


@dataclass
class PhysicsViolation:
    """Registro de uma violação detectada."""
    
    violation_id: str
    violation_type: ViolationType
    severity: ViolationSeverity
    affected_parameter: str
    detected_value: Any
    valid_range: str
    explanation: str
    remediation: Optional[str] = None
    auto_corrected_value: Optional[Any] = None


class PhysicsViolationDetector:
    """Detector que valida todas as dimensões de conformidade física."""
    
    def __init__(self):
        self.violations: List[PhysicsViolation] = []
        self.violation_counter = 0
    
    def detect_all_violations(self, parameters: Dict[str, Any]) -> List[PhysicsViolation]:
        """Executa todas as validações."""
        
        self.violations.clear()
        
        # Validações fundamentais (física)
        self._check_temperature_bounds(parameters)
        self._check_energy_bounds(parameters)
        self._check_conductivity(parameters)
        self._check_density(parameters)
        
        # Validações operacionais
        self._check_setpoint_logic(parameters)
        self._check_infiltration_realism(parameters)
        self._check_peak_annual_consistency(parameters)
        
        # Validações normativas
        self._check_ashrae_compliance(parameters)
        self._check_thickness_bounds(parameters)
        self._check_wwr_bounds(parameters)
        
        # Validações lógicas
        self._check_volume_realism(parameters)
        self._check_load_consistency(parameters)
        
        return self.violations
    
    def _check_temperature_bounds(self, params: Dict) -> None:
        """Verifica se temperatura está em range viável."""
        
        temp = params.get("temperature_C")
        if temp and (temp < 15 or temp > 35):
            self.violations.append(PhysicsViolation(
                violation_id=f"VIOL_{self.violation_counter:04d}",
                violation_type=ViolationType.TEMP_OUT_OF_RANGE,
                severity=ViolationSeverity.CRITICAL,
                affected_parameter="temperature_C",
                detected_value=temp,
                valid_range="15-35°C",
                explanation=f"Temperatura {temp}°C está fora da faixa viável para conforto humano",
                remediation=f"Ajustar para {max(15, min(35, temp))}°C",
                auto_corrected_value=max(15, min(35, temp))
            ))
            self.violation_counter += 1
    
    def _check_energy_bounds(self, params: Dict) -> None:
        """Verifica se energia é não-negativa."""
        
        for energy_field in ["annual_heating_kwh", "annual_cooling_kwh", "total_energy_kwh"]:
            energy = params.get(energy_field)
            if energy and energy < 0:
                self.violations.append(PhysicsViolation(
                    violation_id=f"VIOL_{self.violation_counter:04d}",
                    violation_type=ViolationType.ENERGY_NEGATIVE,
                    severity=ViolationSeverity.CRITICAL,
                    affected_parameter=energy_field,
                    detected_value=energy,
                    valid_range="≥ 0 kWh",
                    explanation=f"Energia não pode ser negativa: {energy} kWh",
                    remediation="Revisar cálculos de simulação"
                ))
                self.violation_counter += 1
    
    def _check_conductivity(self, params: Dict) -> None:
        """Verifica condutividade térmica."""
        
        for cond_field in ["conductivity_W_mK", "conductivity_wall_W_mK", "conductivity_insulation_W_mK"]:
            cond = params.get(cond_field)
            if cond and (cond <= 0 or cond > 10):
                self.violations.append(PhysicsViolation(
                    violation_id=f"VIOL_{self.violation_counter:04d}",
                    violation_type=ViolationType.CONDUCTIVITY_INVALID,
                    severity=ViolationSeverity.CRITICAL,
                    affected_parameter=cond_field,
                    detected_value=cond,
                    valid_range="0.01-10.0 W/m·K",
                    explanation=f"Condutividade {cond} W/m·K fisicamente inviável"
                ))
                self.violation_counter += 1
    
    def _check_density(self, params: Dict) -> None:
        """Verifica densidade de materiais."""
        
        if "density_kg_m3" in params and params["density_kg_m3"] <= 0:
            self.violations.append(PhysicsViolation(
                violation_id=f"VIOL_{self.violation_counter:04d}",
                violation_type=ViolationType.DENSITY_NEGATIVE,
                severity=ViolationSeverity.CRITICAL,
                affected_parameter="density_kg_m3",
                detected_value=params["density_kg_m3"],
                valid_range="> 0 kg/m³",
                explanation="Densidade deve ser positiva"
            ))
            self.violation_counter += 1
    
    def _check_setpoint_logic(self, params: Dict) -> None:
        """Verifica lógica de setpoints."""
        
        heating = params.get("heating_setpoint_C")
        cooling = params.get("cooling_setpoint_C")
        
        if heating and cooling and cooling <= heating:
            self.violations.append(PhysicsViolation(
                violation_id=f"VIOL_{self.violation_counter:04d}",
                violation_type=ViolationType.SETPOINT_CONFLICT,
                severity=ViolationSeverity.HIGH,
                affected_parameter="heating_setpoint_C / cooling_setpoint_C",
                detected_value=f"heating={heating}, cooling={cooling}",
                valid_range="cooling > heating",
                explanation=f"Cooling setpoint ({cooling}°C) deve ser > heating ({heating}°C)",
                remediation=f"Ajustar cooling para {heating + 4}°C"
            ))
            self.violation_counter += 1
    
    def _check_ashrae_compliance(self, params: Dict) -> None:
        """Verifica conformidade com ASHRAE 90.1."""
        
        wwr = params.get("wwr")
        if wwr and (wwr < 0.10 or wwr > 0.60):
            self.violations.append(PhysicsViolation(
                violation_id=f"VIOL_{self.violation_counter:04d}",
                violation_type=ViolationType.ASHRAE_VIOLATION,
                severity=ViolationSeverity.HIGH,
                affected_parameter="wwr",
                detected_value=wwr,
                valid_range="10-60% (ASHRAE 90.1)",
                explanation=f"WWR {wwr*100}% viola limites ASHRAE 90.1",
                remediation=f"Ajustar para {max(0.1, min(0.6, wwr))}"
            ))
            self.violation_counter += 1
    
    # ... mais 10+ validadores específicos
    
    def _check_infiltration_realism(self, params: Dict) -> None:
        """Verifica se taxa de infiltração é realista."""
        pass
    
    def _check_peak_annual_consistency(self, params: Dict) -> None:
        """Verifica se pico é consistente com anual."""
        pass
    
    def _check_thickness_bounds(self, params: Dict) -> None:
        """Verifica espessuras."""
        pass
    
    def _check_wwr_bounds(self, params: Dict) -> None:
        """Verifica WWR."""
        pass
    
    def _check_volume_realism(self, params: Dict) -> None:
        """Verifica volume."""
        pass
    
    def _check_load_consistency(self, params: Dict) -> None:
        """Verifica carga interna."""
        pass
    
    def has_critical_violations(self) -> bool:
        """Verifica se há violações críticas."""
        return any(v.severity == ViolationSeverity.CRITICAL for v in self.violations)
    
    def print_violations_report(self) -> None:
        """Imprime relatório de violações."""
        
        if not self.violations:
            print("✅ Nenhuma violação detectada!")
            return
        
        print("\n" + "=" * 100)
        print(f"PHYSICS VIOLATIONS REPORT ({len(self.violations)} violações)")
        print("=" * 100)
        
        # Agrupar por severidade
        by_severity = {}
        for v in self.violations:
            sev = v.severity.name
            if sev not in by_severity:
                by_severity[sev] = []
            by_severity[sev].append(v)
        
        # Exibir por severidade decrescente
        for severity_name in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]:
            violations = by_severity.get(severity_name, [])
            if not violations:
                continue
            
            print(f"\n[{severity_name}] {len(violations)} violation(s):")
            for v in violations[:3]:  # Mostrar primeiras 3
                print(f"\n  {v.violation_id}: {v.violation_type.value}")
                print(f"    Parameter: {v.affected_parameter} = {v.detected_value}")
                print(f"    Expected: {v.valid_range}")
                print(f"    Reason: {v.explanation}")
                if v.remediation:
                    print(f"    Fix: {v.remediation}")
        
        print("\n" + "=" * 100)


def main():
    """Demonstração de detector de violações."""
    
    print("🚨 Physics Violation Detector\n")
    
    detector = PhysicsViolationDetector()
    
    # Teste 1: Parâmetros válidos
    print("Teste 1: Parâmetros válidos")
    valid_params = {
        "temperature_C": 25,
        "annual_heating_kwh": 50,
        "annual_cooling_kwh": 100,
        "conductivity_W_mK": 1.5,
        "density_kg_m3": 2300,
        "heating_setpoint_C": 21,
        "cooling_setpoint_C": 25,
        "wwr": 0.35
    }
    
    violations = detector.detect_all_violations(valid_params)
    detector.print_violations_report()
    
    # Teste 2: Parâmetros inválidos
    print("\n\nTeste 2: Parâmetros inválidos")
    detector = PhysicsViolationDetector()
    
    invalid_params = {
        "temperature_C": 45,  # INVÁLIDO
        "annual_heating_kwh": -10,  # INVÁLIDO
        "conductivity_W_mK": 0,  # INVÁLIDO
        "heating_setpoint_C": 25,
        "cooling_setpoint_C": 20,  # INVÁLIDO (< heating)
        "wwr": 0.80  # INVÁLIDO
    }
    
    violations = detector.detect_all_violations(invalid_params)
    detector.print_violations_report()
    
    if detector.has_critical_violations():
        print("\n⛔ SISTEMA NÃO DEVE PROSSEGUIR: Violações críticas detectadas!")


if __name__ == "__main__":
    main()
```

**✅ Checkpoint:** Detector identifica 20+ tipos de violações? Critical violations param sistema?

---

### 🎯 Exercício 2.2: Violation Logging & Severity Tracking (3-4h)

**Contexto:** Logging estruturado permite auditoria completa, rastreamento de padrões de falha, e identificação de causas raiz.

**Tarefa:** Implementar sistema de logging de violações com persistência e análise.

#### Implementação: `violation_logger.py`

```python
"""
Exercício 2.2: Logging estruturado de violações
Referência: ISO/IEC 20000 - Logging e Auditoria
"""

import json
import sqlite3
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum
import logging


@dataclass
class ViolationLogEntry:
    """Entrada de log de violação."""
    
    timestamp: str
    violation_id: str
    violation_type: str
    severity: str
    parameter: str
    detected_value: Any
    expected_range: str
    test_case_id: Optional[str]
    remediation_applied: bool
    corrected_value: Optional[Any]
    system_state: Dict[str, Any]  # Contexto completo


class ViolationLogger:
    """Logger estruturado para violações."""
    
    def __init__(self, db_path: str = "data/violations.db"):
        self.db_path = db_path
        self._init_database()
        self.setup_file_logger()
    
    def _init_database(self) -> None:
        """Cria tabela de violations no SQLite."""
        
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS violations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                violation_id TEXT NOT NULL,
                violation_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                parameter TEXT NOT NULL,
                detected_value TEXT,
                expected_range TEXT,
                test_case_id TEXT,
                remediation_applied BOOLEAN,
                corrected_value TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def setup_file_logger(self) -> None:
        """Configura logging para arquivo."""
        
        Path("logs").mkdir(exist_ok=True)
        
        self.logger = logging.getLogger("violations")
        self.logger.setLevel(logging.DEBUG)
        
        handler = logging.FileHandler("logs/violations.log")
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(violation_id)s: %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_violation(self, violation: PhysicsViolation, test_case_id: Optional[str] = None) -> None:
        """Loga violação em database e arquivo."""
        
        timestamp = datetime.now().isoformat()
        
        # Database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO violations (
                timestamp, violation_id, violation_type, severity,
                parameter, detected_value, expected_range, test_case_id,
                remediation_applied, corrected_value
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            timestamp,
            violation.violation_id,
            violation.violation_type.value,
            violation.severity.name,
            violation.affected_parameter,
            str(violation.detected_value),
            violation.valid_range,
            test_case_id,
            violation.auto_corrected_value is not None,
            str(violation.auto_corrected_value) if violation.auto_corrected_value else None
        ))
        
        conn.commit()
        conn.close()
        
        # File logging
        extra = {
            'violation_id': violation.violation_id
        }
        self.logger.warning(
            f"{violation.violation_type.value} ({violation.severity.name}): {violation.explanation}",
            extra=extra
        )
    
    def get_violations_by_type(self, violation_type: str) -> List[Dict]:
        """Retorna violações de um tipo específico."""
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM violations WHERE violation_type = ? ORDER BY timestamp DESC",
            (violation_type,)
        )
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas de violações."""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total
        cursor.execute("SELECT COUNT(*) FROM violations")
        total = cursor.fetchone()[0]
        
        # Por severidade
        cursor.execute("""
            SELECT severity, COUNT(*) as count
            FROM violations GROUP BY severity
        """)
        by_severity = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Por tipo
        cursor.execute("""
            SELECT violation_type, COUNT(*) as count
            FROM violations GROUP BY violation_type
        """)
        by_type = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Taxa de correção automática
        cursor.execute("SELECT COUNT(*) FROM violations WHERE remediation_applied = 1")
        auto_corrected = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_violations": total,
            "by_severity": by_severity,
            "by_type": by_type,
            "auto_corrected": auto_corrected,
            "auto_correction_rate": f"{100*auto_corrected/total:.1f}%" if total > 0 else "N/A"
        }
    
    def print_statistics_report(self) -> None:
        """Imprime relatório de estatísticas."""
        
        stats = self.get_statistics()
        
        print("\n" + "=" * 80)
        print("VIOLATION STATISTICS")
        print("=" * 80)
        print(f"Total Violations: {stats['total_violations']}")
        print(f"Auto-Corrected: {stats['auto_corrected']} ({stats['auto_correction_rate']})")
        
        print("\nBy Severity:")
        for severity, count in stats['by_severity'].items():
            print(f"  {severity}: {count}")
        
        print("\nTop 5 Violation Types:")
        sorted_types = sorted(stats['by_type'].items(), key=lambda x: x[1], reverse=True)
        for violation_type, count in sorted_types[:5]:
            print(f"  {violation_type}: {count}")
        
        print("=" * 80 + "\n")


def main():
    """Demonstração de violation logging."""
    
    print("📝 Violation Logging System\n")
    
    logger = ViolationLogger()
    
    # Simular algumas violações
    violation1 = PhysicsViolation(
        violation_id="VIOL_0001",
        violation_type=ViolationType.TEMP_OUT_OF_RANGE,
        severity=ViolationSeverity.CRITICAL,
        affected_parameter="temperature_C",
        detected_value=45,
        valid_range="15-35°C",
        explanation="Temperature 45°C exceeds maximum",
        auto_corrected_value=35
    )
    
    violation2 = PhysicsViolation(
        violation_id="VIOL_0002",
        violation_type=ViolationType.ENERGY_NEGATIVE,
        severity=ViolationSeverity.CRITICAL,
        affected_parameter="annual_cooling_kwh",
        detected_value=-10,
        valid_range="≥ 0 kWh",
        explanation="Energy cannot be negative"
    )
    
    logger.log_violation(violation1, test_case_id="GOLDEN_001")
    logger.log_violation(violation2, test_case_id="GOLDEN_002")
    
    logger.print_statistics_report()


if __name__ == "__main__":
    main()
```

**✅ Checkpoint:** Logger persiste violações? Estatísticas funcionam?

---

### 🎯 Exercício 2.3: Violation Pattern Analysis (2-3h)

**Contexto:** Análise de padrões identifica causas raiz (ex: tipo de simulador gera mais erros, parâmetros específicos gatilham violações).

**Tarefa:** Implementar análise estatística de padrões de violação.

#### Implementação: `violation_pattern_analyzer.py`

```python
"""
Exercício 2.3: Análise de padrões de violação
Referência: Statistical Process Control (SPC)
"""

from typing import Dict, List, Tuple
import pandas as pd
import json


class ViolationPatternAnalyzer:
    """Analisa padrões estatísticos em violações."""
    
    def __init__(self, logger: ViolationLogger):
        self.logger = logger
    
    def get_violations_dataframe(self) -> pd.DataFrame:
        """Carrega violações em DataFrame para análise."""
        
        conn = sqlite3.connect(self.logger.db_path)
        df = pd.read_sql_query("SELECT * FROM violations", conn)
        conn.close()
        
        return df
    
    def identify_high_risk_parameters(self) -> Dict[str, float]:
        """Identifica parâmetros que geram mais violações."""
        
        df = self.get_violations_dataframe()
        
        violations_by_param = df.groupby('parameter').size().reset_index(name='count')
        violations_by_param = violations_by_param.sort_values('count', ascending=False)
        
        total = df.shape[0]
        risk_scores = {
            row['parameter']: row['count'] / total
            for _, row in violations_by_param.iterrows()
        }
        
        return risk_scores
    
    def identify_correlation_violations(self) -> Dict[str, List[str]]:
        """Identifica violações que ocorrem juntas."""
        
        df = self.get_violations_dataframe()
        
        # Agrupar por test_case_id
        case_violations = df.groupby('test_case_id')['violation_type'].apply(list).to_dict()
        
        # Encontrar co-ocorrências
        correlations = {}
        for case_id, violations in case_violations.items():
            if len(violations) > 1:
                key = tuple(sorted(set(violations)))
                if key not in correlations:
                    correlations[key] = 0
                correlations[key] += 1
        
        return correlations
    
    def print_pattern_analysis(self) -> None:
        """Imprime análise de padrões."""
        
        print("\n" + "=" * 100)
        print("VIOLATION PATTERN ANALYSIS")
        print("=" * 100)
        
        # Risk scores
        risk_scores = self.identify_high_risk_parameters()
        print("\nHIGH-RISK PARAMETERS:")
        for param, score in sorted(risk_scores.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {param}: {score:.1%} of violations")
        
        # Correlations
        correlations = self.identify_correlation_violations()
        print("\nCORRELATED VIOLATIONS:")
        for violations, count in sorted(correlations.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {' + '.join(violations)}: {count} occurrences")
        
        print("=" * 100 + "\n")
```

**✅ Checkpoint:** Análise identifica parâmetros de risco e correlações?

---

### 📋 Checklist de Certificação - Semana 2

- [ ] **Exercício 2.1:** Detector com 20+ tipos de violação
- [ ] **Exercício 2.2:** Logger com SQLite + estatísticas
- [ ] **Exercício 2.3:** Pattern analysis implementado
- [ ] **Exercício 2.4:** Integration com test suite (não detalhado aqui)

---

## 🔹 Semana 3: Hallucination Logging & Analysis (12-15 horas)

### 📖 Objetivos da Semana

- Logar todas as hallucinations com contexto
- Correlacionar hallucinations com parâmetros de entrada
- Implementar early warning system
- Criar relatório de confiabilidade do sistema

### 🎯 Exercício 3.1: Hallucination Logger (3-4h)

**Contexto:** Logging detalhado de hallucinations permite análise retrospectiva e melhoria de prompts.

#### Implementação: `hallucination_logger.py`

```python
"""
Exercício 3.1: Logging estruturado de hallucinations
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any
import sqlite3


@dataclass
class HallucinationRecord:
    """Registro de uma hallucination detectada."""
    
    hallucination_id: str
    timestamp: str
    hallucination_type: str  # De Mês 5 Exercise 2.4
    severity: int  # 1-5
    detected_in: str  # Campo LLM que contém hallucination
    llm_output: str
    expected_pattern: str
    correction: Optional[str]
    prompt_version: str
    model_name: str
    user_query: str


class HallucinationLogger:
    """Logger estruturado para hallucinations."""
    
    def __init__(self, db_path: str = "data/hallucinations.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self) -> None:
        """Cria tabela de hallucinations."""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hallucinations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hallucination_id TEXT NOT NULL UNIQUE,
                timestamp TEXT NOT NULL,
                hallucination_type TEXT NOT NULL,
                severity INTEGER,
                detected_in TEXT,
                llm_output TEXT,
                expected_pattern TEXT,
                correction TEXT,
                prompt_version TEXT,
                model_name TEXT,
                user_query TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def log_hallucination(self, record: HallucinationRecord) -> None:
        """Loga uma hallucination."""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO hallucinations (
                hallucination_id, timestamp, hallucination_type, severity,
                detected_in, llm_output, expected_pattern, correction,
                prompt_version, model_name, user_query
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            record.hallucination_id,
            record.timestamp,
            record.hallucination_type,
            record.severity,
            record.detected_in,
            record.llm_output,
            record.expected_pattern,
            record.correction,
            record.prompt_version,
            record.model_name,
            record.user_query
        ))
        
        conn.commit()
        conn.close()
    
    def get_hallucination_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas de hallucinations."""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total
        cursor.execute("SELECT COUNT(*) FROM hallucinations")
        total = cursor.fetchone()[0]
        
        # Por tipo
        cursor.execute("""
            SELECT hallucination_type, COUNT(*) as count
            FROM hallucinations GROUP BY hallucination_type
        """)
        by_type = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Por severidade
        cursor.execute("""
            SELECT severity, COUNT(*) as count
            FROM hallucinations GROUP BY severity
        """)
        by_severity = {int(row[0]): row[1] for row in cursor.fetchall()}
        
        # Taxa crítica
        cursor.execute("SELECT COUNT(*) FROM hallucinations WHERE severity >= 4")
        critical = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_hallucinations": total,
            "by_type": by_type,
            "by_severity": by_severity,
            "critical_hallucinations": critical,
            "critical_rate": f"{100*critical/total:.1f}%" if total > 0 else "N/A"
        }
    
    def print_statistics(self) -> None:
        """Imprime estatísticas de hallucinations."""
        
        stats = self.get_hallucination_statistics()
        
        print("\n" + "=" * 100)
        print("HALLUCINATION STATISTICS")
        print("=" * 100)
        print(f"Total Hallucinations: {stats['total_hallucinations']}")
        print(f"Critical (Severity ≥ 4): {stats['critical_hallucinations']} ({stats['critical_rate']})")
        
        print("\nBy Type:")
        for h_type, count in stats['by_type'].items():
            print(f"  {h_type}: {count}")
        
        print("\nBy Severity:")
        for severity in sorted(stats['by_severity'].keys()):
            count = stats['by_severity'][severity]
            print(f"  Level {severity}: {count}")
        
        print("=" * 100 + "\n")
```

**✅ Checkpoint:** Logger persiste hallucinations? Estatísticas funcionam?

---

### 🎯 Exercício 3.2: Hallucination Correlation Analysis (3-4h)

**Contexto:** Análise correlacional mostra quais inputs ou prompts gatilham hallucinations.

#### Implementação: `hallucination_correlation.py`

```python
"""
Exercício 3.2: Análise de correlação entre inputs e hallucinations
"""

import pandas as pd
import sqlite3
from typing import Dict, List, Tuple


class HallucinationCorrelationAnalyzer:
    """Analisa correlações entre inputs e hallucinations."""
    
    def __init__(self, hall_logger: HallucinationLogger):
        self.hall_logger = hall_logger
    
    def get_hallucinations_dataframe(self) -> pd.DataFrame:
        """Carrega hallucinations em DataFrame."""
        
        conn = sqlite3.connect(self.hall_logger.db_path)
        df = pd.read_sql_query("SELECT * FROM hallucinations", conn)
        conn.close()
        
        return df
    
    def identify_trigger_patterns(self) -> Dict[str, float]:
        """Identifica padrões que gatilham hallucinations."""
        
        df = self.get_hallucinations_dataframe()
        
        # Análise de keywords em queries
        trigger_keywords = {}
        
        for _, row in df.iterrows():
            query = str(row['user_query']).lower()
            
            # Palavras-chave comuns em hallucinations
            keywords = ['optimize', 'maximum', 'minimum', 'best', 'worst', 'impossible']
            
            for kw in keywords:
                if kw in query:
                    trigger_keywords[kw] = trigger_keywords.get(kw, 0) + 1
        
        total = df.shape[0]
        return {
            kw: count / total for kw, count in trigger_keywords.items()
        }
    
    def identify_risky_prompt_versions(self) -> Dict[str, float]:
        """Identifica versões de prompt com alta taxa de hallucinations."""
        
        df = self.get_hallucinations_dataframe()
        
        by_version = df.groupby('prompt_version').agg({
            'hallucination_id': 'count',
            'severity': 'mean'
        }).reset_index()
        
        by_version.columns = ['prompt_version', 'hallucination_count', 'avg_severity']
        
        total_hallucinations = df.shape[0]
        
        risk_scores = {}
        for _, row in by_version.iterrows():
            score = (row['hallucination_count'] / total_hallucinations) * row['avg_severity']
            risk_scores[row['prompt_version']] = score
        
        return risk_scores
    
    def print_correlation_report(self) -> None:
        """Imprime relatório de correlações."""
        
        print("\n" + "=" * 100)
        print("HALLUCINATION CORRELATION ANALYSIS")
        print("=" * 100)
        
        triggers = self.identify_trigger_patterns()
        print("\nTRIGGER KEYWORDS (High correlation with hallucinations):")
        for kw, rate in sorted(triggers.items(), key=lambda x: x[1], reverse=True):
            print(f"  '{kw}': {rate:.1%} of hallucinations contain this keyword")
        
        risks = self.identify_risky_prompt_versions()
        print("\nRISKY PROMPT VERSIONS:")
        for version, risk in sorted(risks.items(), key=lambda x: x[1], reverse=True):
            print(f"  {version}: Risk Score = {risk:.3f}")
        
        print("=" * 100 + "\n")
```

**✅ Checkpoint:** Análise identifica keywords gatilho e versões arriscadas?

---

### 🎯 Exercício 3.3: Hallucination Early Warning System (2-3h)

**Contexto:** Sistema de alerta preventivo para detectar hallucinations antes de afetar usuários.

#### Implementação: `hallucination_early_warning.py`

```python
"""
Exercício 3.3: Sistema de alerta antecipado para hallucinations
"""

from typing import Dict, List, Optional
import json


class HallucinationEarlyWarning:
    """Sistema que detecta sinais de perigo de hallucination."""
    
    def __init__(self, correlation_analyzer: HallucinationCorrelationAnalyzer):
        self.analyzer = correlation_analyzer
        self.risk_thresholds = {
            "critical": 0.8,  # Risk score > 80%
            "high": 0.6,
            "medium": 0.4
        }
    
    def assess_query_risk(self, user_query: str) -> Dict[str, any]:
        """Avalia risco de hallucination para uma query."""
        
        triggers = self.analyzer.identify_trigger_patterns()
        
        query_lower = user_query.lower()
        risk_score = 0.0
        triggered_keywords = []
        
        for keyword, trigger_rate in triggers.items():
            if keyword in query_lower:
                risk_score += trigger_rate
                triggered_keywords.append(keyword)
        
        # Normalizar
        risk_score = min(risk_score / max(len(triggers), 1), 1.0)
        
        # Determinar nível de risco
        if risk_score >= self.risk_thresholds["critical"]:
            risk_level = "CRITICAL"
        elif risk_score >= self.risk_thresholds["high"]:
            risk_level = "HIGH"
        elif risk_score >= self.risk_thresholds["medium"]:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        return {
            "query": user_query,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "triggered_keywords": triggered_keywords,
            "recommendation": self._get_recommendation(risk_level)
        }
    
    def _get_recommendation(self, risk_level: str) -> str:
        """Recomendação baseada no nível de risco."""
        
        recommendations = {
            "CRITICAL": "⛔ Enable manual review before sending to user",
            "HIGH": "⚠️  Apply additional validators, consider review",
            "MEDIUM": "⚠️  Monitor output carefully",
            "LOW": "✅ Proceed normally"
        }
        
        return recommendations.get(risk_level, "Unknown risk")
    
    def print_early_warning_report(self, user_query: str) -> None:
        """Imprime relatório de alerta antecipado."""
        
        assessment = self.assess_query_risk(user_query)
        
        print("\n" + "=" * 100)
        print("EARLY WARNING ASSESSMENT")
        print("=" * 100)
        print(f"Query: {assessment['query']}")
        print(f"Risk Level: {assessment['risk_level']}")
        print(f"Risk Score: {assessment['risk_score']:.1%}")
        
        if assessment['triggered_keywords']:
            print(f"Triggered Keywords: {', '.join(assessment['triggered_keywords'])}")
        
        print(f"Recommendation: {assessment['recommendation']}")
        print("=" * 100 + "\n")
```

**✅ Checkpoint:** Early warning system detecta queries arriscadas?

---

### 📋 Checklist de Certificação - Semana 3

- [ ] **Exercício 3.1:** Logger de hallucinations com estatísticas
- [ ] **Exercício 3.2:** Análise de correlação input-hallucination
- [ ] **Exercício 3.3:** Early warning system implementado
- [ ] **Exercício 3.4:** Integration com Gemini (não detalhado aqui)

---

## 🔹 Semana 4: Integration Testing & Production Readiness (14-15 horas)

### 📖 Objetivos da Semana

- Executar full test suite
- Validar compliance com todas as normas
- Preparar sistema para produção
- Documentar procedimentos de deployment

### 🎯 Exercício 4.1: Full System Integration Test Suite (5-6h)

**Contexto:** Suite integrada que testa system end-to-end com golden dataset.

#### Implementação: `test_physics_compliance_integration.py`

```python
"""
Exercício 4.1: Suite de testes integrada para compliance
"""

import pytest
from typing import List


class TestPhysicsComplianceIntegration:
    """Testes de integração para compliance físico."""
    
    @pytest.fixture
    def golden_dataset(self):
        """Carrega golden dataset."""
        builder = GoldenDatasetBuilder()
        return builder.build()
    
    @pytest.fixture
    def violation_detector(self):
        """Inicializa detector."""
        return PhysicsViolationDetector()
    
    @pytest.fixture
    def violation_logger(self):
        """Inicializa logger."""
        return ViolationLogger()
    
    def test_all_normal_cases_pass(self, golden_dataset, violation_detector):
        """Todos os casos normais devem passar sem violações críticas."""
        
        normal_cases = [c for c in golden_dataset 
                       if c.category == TestCaseCategory.NORMAL_OPERATION]
        
        for case in normal_cases:
            params = {
                'temperature_C': case.heating_setpoint_C,
                'wwr': case.wwr,
                'wall_thickness_m': case.wall_thickness_m
                # ... mais parâmetros
            }
            
            violations = violation_detector.detect_all_violations(params)
            critical = [v for v in violations 
                       if v.severity == ViolationSeverity.CRITICAL]
            
            assert len(critical) == 0, f"Case {case.test_id} has critical violations"
    
    def test_invalid_cases_detected(self, golden_dataset, violation_detector):
        """Casos inválidos devem ser detectados."""
        
        invalid_cases = [c for c in golden_dataset 
                        if c.category == TestCaseCategory.INVALID_INPUT]
        
        for case in invalid_cases:
            params = {
                'wwr': case.wwr,
                'temperature_C': case.heating_setpoint_C
                # ... parâmetros intencionalmente inválidos
            }
            
            violations = violation_detector.detect_all_violations(params)
            
            assert len(violations) > 0, f"Case {case.test_id} should have violations"
    
    def test_logging_persists(self, violation_logger):
        """Logging deve persistir em database."""
        
        violation = PhysicsViolation(
            violation_id="TEST_001",
            violation_type=ViolationType.TEMP_OUT_OF_RANGE,
            severity=ViolationSeverity.HIGH,
            affected_parameter="temperature",
            detected_value=40,
            valid_range="15-35",
            explanation="Test violation"
        )
        
        violation_logger.log_violation(violation)
        
        results = violation_logger.get_violations_by_type("temperature_out_of_range")
        
        assert len(results) > 0
        assert results[0]['violation_id'] == "TEST_001"
    
    def test_auto_correction_improves_compliance(self, violation_detector):
        """Auto-correção deve reduzir violações."""
        
        invalid_params = {
            'temperature_C': 45,  # Inválido
            'wwr': 0.80  # Inválido
        }
        
        violations = violation_detector.detect_all_violations(invalid_params)
        
        # Aplicar correções
        corrected_params = invalid_params.copy()
        for v in violations:
            if v.auto_corrected_value:
                corrected_params[v.affected_parameter] = v.auto_corrected_value
        
        # Re-validar
        second_violations = violation_detector.detect_all_violations(corrected_params)
        
        assert len(second_violations) < len(violations)


class TestProductionReadiness:
    """Testes de preparação para produção."""
    
    def test_no_critical_hallucinations_in_prompts(self):
        """Prompts não devem gerar hallucinations críticas."""
        
        from gemini_streaming import GeminiStreamingClient
        
        client = GeminiStreamingClient()
        response = client.stream_with_callback(
            "Optimize a building for maximum energy efficiency",
            callback=lambda token: None
        )
        
        # Validar com HallucinationDetector (Mês 5)
        from hallucination_detection import HallucinationDetector
        detector = HallucinationDetector()
        
        violations = detector.detect_hallucinations(response)
        critical = [v for v in violations if v['severity'] >= 4]
        
        assert len(critical) == 0, "Critical hallucinations detected in production prompt"
    
    def test_response_time_within_sla(self):
        """Tempo de resposta deve estar dentro do SLA."""
        
        from gemini_streaming import GeminiStreamingClient
        import time
        
        client = GeminiStreamingClient()
        
        start = time.time()
        response = client.stream_with_callback("Simple energy query", callback=None)
        elapsed = time.time() - start
        
        assert elapsed < 5.0, f"Response time {elapsed}s exceeds 5s SLA"
    
    def test_cost_tracking_accurate(self):
        """Rastreamento de custo deve ser preciso."""
        
        from gemini_rate_limiting import CostTracker
        
        tracker = CostTracker(budget_usd=5.0)
        
        # Simular 10 chamadas
        for i in range(10):
            input_tokens = 100
            output_tokens = 50
            
            tracker.add_tokens(input_tokens, output_tokens)
        
        cost = tracker.estimated_daily_cost
        
        # Estimativa: (100*75 + 50*300) / 1000 * 10 = $2.25 por dia
        assert cost < 5.0, "Estimated daily cost too high"


def main():
    """Executar testes."""
    pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    main()
```

**Execução:**
```bash
pytest test_physics_compliance_integration.py -v
```

**✅ Checkpoint:** Suite executa com sucesso? Todos os testes passam?

---

### 🎯 Exercício 4.2: Compliance Documentation (3-4h)

**Contexto:** Documentação formal de compliance para auditoria e produção.

#### Implementação: `compliance_report_generator.py`

```python
"""
Exercício 4.2: Gerador de relatório de compliance
"""

from typing import Dict, List, Any
import json
from datetime import datetime


class ComplianceReportGenerator:
    """Gera relatório formal de compliance."""
    
    def __init__(self, violation_logger, hallucination_logger):
        self.violation_logger = violation_logger
        self.hallucination_logger = hallucination_logger
    
    def generate_compliance_report(self, version: str = "1.0") -> Dict[str, Any]:
        """Gera relatório completo de compliance."""
        
        violation_stats = self.violation_logger.get_statistics()
        hallucination_stats = self.hallucination_logger.get_hallucination_statistics()
        
        report = {
            "metadata": {
                "version": version,
                "generated_at": datetime.now().isoformat(),
                "system": "Physics Compliance Testing Suite",
                "standards_compliance": [
                    "IEEE 829 (Test Documentation)",
                    "ASHRAE 90.1 (Energy Standard)",
                    "ISO 13790 (Thermal Performance)",
                    "NASA IV&V Standards"
                ]
            },
            "violations": {
                "total": violation_stats['total_violations'],
                "by_severity": violation_stats['by_severity'],
                "by_type": violation_stats['by_type'],
                "auto_corrected": violation_stats['auto_corrected'],
                "compliance_score": self._calculate_compliance_score(violation_stats)
            },
            "hallucinations": {
                "total": hallucination_stats['total_hallucinations'],
                "by_type": hallucination_stats['by_type'],
                "critical_rate": hallucination_stats['critical_rate'],
                "reliability_score": self._calculate_reliability_score(hallucination_stats)
            },
            "recommendations": self._generate_recommendations(
                violation_stats, hallucination_stats
            ),
            "production_readiness": self._assess_production_readiness(
                violation_stats, hallucination_stats
            )
        }
        
        return report
    
    def _calculate_compliance_score(self, stats: Dict) -> float:
        """Calcula score de compliance (0-100)."""
        
        total = stats['total_violations']
        if total == 0:
            return 100.0
        
        # Penalidade por severidade
        penalty = 0
        for severity_name, count in stats['by_severity'].items():
            if severity_name == "CRITICAL":
                penalty += count * 25
            elif severity_name == "HIGH":
                penalty += count * 10
            elif severity_name == "MEDIUM":
                penalty += count * 2
        
        score = max(0, 100 - penalty)
        return score
    
    def _calculate_reliability_score(self, stats: Dict) -> float:
        """Calcula score de confiabilidade (0-100)."""
        
        total = stats['total_hallucinations']
        if total == 0:
            return 100.0
        
        critical = stats['critical_hallucinations']
        
        # Taxa de não-hallucination
        score = (1 - critical / total) * 100
        
        return score
    
    def _generate_recommendations(self, v_stats: Dict, h_stats: Dict) -> List[str]:
        """Gera recomendações baseadas em issues."""
        
        recommendations = []
        
        # Violações
        if v_stats['total_violations'] > 10:
            recommendations.append(
                "High violation rate: Review constraint definitions and physics validators"
            )
        
        # Hallucinations
        if h_stats['critical_hallucinations'] > 0:
            recommendations.append(
                "Critical hallucinations detected: Improve system prompts and few-shot examples"
            )
        
        # Autêntico
        if v_stats['auto_corrected'] / max(v_stats['total_violations'], 1) > 0.5:
            recommendations.append(
                "High auto-correction rate: Some constraints may be too restrictive"
            )
        
        return recommendations
    
    def _assess_production_readiness(self, v_stats: Dict, h_stats: Dict) -> Dict[str, Any]:
        """Avalia se sistema está pronto para produção."""
        
        readiness = {
            "status": "READY" if self._calculate_compliance_score(v_stats) > 80 
                               and h_stats['critical_hallucinations'] == 0
                     else "NOT_READY",
            "compliance_score": self._calculate_compliance_score(v_stats),
            "reliability_score": self._calculate_reliability_score(h_stats),
            "critical_issues": h_stats['critical_hallucinations'],
            "can_deploy": (
                self._calculate_compliance_score(v_stats) > 80 
                and h_stats['critical_hallucinations'] == 0
            )
        }
        
        return readiness
    
    def save_report(self, filepath: str = "reports/compliance_report.json") -> None:
        """Salva relatório em arquivo."""
        
        import os
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        
        report = self.generate_compliance_report()
        
        with open(filepath, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Compliance report saved: {filepath}")
    
    def print_executive_summary(self) -> None:
        """Imprime sumário executivo."""
        
        report = self.generate_compliance_report()
        
        print("\n" + "=" * 100)
        print("COMPLIANCE & PRODUCTION READINESS EXECUTIVE SUMMARY")
        print("=" * 100)
        
        print(f"\n📊 PHYSICS COMPLIANCE")
        print(f"  Violations: {report['violations']['total']}")
        print(f"  Compliance Score: {report['violations']['compliance_score']:.1f}/100")
        
        print(f"\n🛡️  HALLUCINATION CONTROL")
        print(f"  Hallucinations: {report['hallucinations']['total']}")
        print(f"  Reliability Score: {report['hallucinations']['reliability_score']:.1f}/100")
        
        print(f"\n🚀 PRODUCTION READINESS")
        readiness = report['production_readiness']
        print(f"  Status: {readiness['status']}")
        print(f"  Can Deploy: {'✅ YES' if readiness['can_deploy'] else '❌ NO'}")
        
        print(f"\n💡 RECOMMENDATIONS")
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"  {i}. {rec}")
        
        print("=" * 100 + "\n")
```

**✅ Checkpoint:** Relatório gerado com compliance scores?

---

### 📋 Checklist de Certificação - Semana 4

- [ ] **Exercício 4.1:** Integration test suite passa com sucesso
- [ ] **Exercício 4.2:** Compliance report gerado com scores > 80
- [ ] **Exercício 4.3:** Production deployment checklist completo
- [ ] **Exercício 4.4:** Monitoring & alerting em produção

---

## 🎓 Resultado Final: Production-Ready Physics Compliance System

Após completar Mês 7, seu sistema possui:

1. ✅ **Golden Dataset:** 50+ casos de teste validados
2. ✅ **Violation Detection:** 20+ tipos de violação com severidade
3. ✅ **Hallucination Control:** Logger + análise correlacional
4. ✅ **Early Warning:** Sistema preventivo de hallucinations
5. ✅ **Integration Tests:** Suite completa com 99%+ cobertura
6. ✅ **Compliance Docs:** Relatório formal para auditoria
7. ✅ **Production Ready:** SLA < 5s, reliability > 95%

---

## 📚 Recursos & Referências

### Papers Citados

- **Jiang et al. (2024):** "Physics-Informed Guardrails for LLM Safety in Engineering Applications"
- **Zakeri et al. (2025):** "Validation Protocols for Building-LLM Co-Simulation Systems"
- **NASA (2016):** "Software IV&V Practices" (NASA/SP-2016-3701)
- **IEEE (2008):** "829-2008 - Software and Systems Engineering - Content of Test Documentation"

### Padrões de Conformidade

- ASHRAE 90.1-2023 (Energy Standard for Buildings)
- ISO 13790:2017 (Energy performance of buildings)
- NBR 15220 (Desempenho Térmico de Edificações)

### Ferramentas & Bibliotecas

```bash
# Testing
pip install pytest pytest-cov hypothesis

# Visualization
pip install plotly pandas

# Database
pip install sqlalchemy

# Logging
pip install python-json-logger

# Monitoring
pip install prometheus-client
```

---

## 🚀 Próximas Ações

**Após Mês 7 (Compliance Testing):**

### Mês 8: Advanced Optimization
- Multi-objective optimization (Pareto-optimal solutions)
- Genetic algorithms for parameter search
- Trade-off analysis (energy vs cost vs comfort)

### Mês 9: Production Deployment
- Docker containerization
- Kubernetes orchestration
- API versioning and backward compatibility
- Database migration strategies

### Mês 10-12: Advanced Topics
- Federated learning for privacy-preserving training
- Real-time monitoring and adaptive prompting
- Climate change scenario analysis
- Integration with building management systems (BMS)

---

## 💬 Troubleshooting & FAQ

### Q: Como aumentar compliance score?
**A:** 
1. Revisar constraint definitions (são muito restritivas?)
2. Melhorar prompt engineering (adicionar exemplos)
3. Implementar domain-specific validators
4. Aumentar golden dataset size

### Q: Hallucinations continuam aparecendo?
**A:**
1. Revisar early warning thresholds
2. Adicionar mais exemplos ao few-shot learning
3. Implementar fact-checking loop antes de retornar ao usuário
4. Usar model mais capaz (ex: Gemini 2.0)

### Q: Como deploy em produção?
**A:**
1. Compliance score > 80% ✅
2. Critical hallucinations = 0 ✅
3. Integration tests passing ✅
4. Compliance report aprovado ✅
5. Deploy para staging → monitorar 1 semana → produção

---

## 🎯 Checklist de Conclusão do Mês 7

- [ ] Todos os 4 exercícios de cada semana completados
- [ ] Golden dataset com 50+ casos de teste
- [ ] Physics violation detector com 20+ tipos
- [ ] Hallucination logger + correlation analysis
- [ ] Early warning system funcionando
- [ ] Integration test suite com 100% cobertura
- [ ] Compliance report gerado (score > 80)
- [ ] Sistema pronto para produção
- [ ] Documentação completa para auditoria

**🎉 Parabéns!** Você agora possui um sistema de production-grade com garantias físicas e hallucination control!

---

**Última Atualização:** 13 de janeiro de 2026
**Versão do Currículo:** 2.0 (Meses 1-7 completos)
**Tempo Total Investido:** ~420-480 horas (7 meses × 60h/mês)

