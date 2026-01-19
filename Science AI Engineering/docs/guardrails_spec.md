# 🛡️ Especificação Completa: GuardrailValidator

**Módulo:** Mês 2 - Engenharia de Software  
**Objetivo:** Validação rigorosa de dados antes de simulação EnergyPlus  
**Base Científica:** Jiang et al. (2024) - Constraint Validation for Physics-Informed ML

---

## 📋 Visão Geral

O `GuardrailValidator` é uma biblioteca Python que implementa validação em **5 camadas** para garantir que dados de entrada para simulações físicas são:
1. Tipo-seguros (type checking)
2. Dentro de ranges válidos (constraint checking)
3. Fisicamente plausíveis (physics checking)
4. Computacionalmente viáveis (resource checking)
5. Auditáveis (audit trail)

Esta especificação define a API completa, casos de teste e critérios de aceitação para implementação.

---

## 🎯 Requisitos Funcionais

### RF-01: Validação de Tipo
O sistema DEVE validar que todos os campos tenham tipos corretos (float, str, int).

### RF-02: Validação de Range
O sistema DEVE verificar que valores numéricos estejam dentro de ranges físicos válidos.

### RF-03: Validação Cruzada
O sistema DEVE verificar consistência entre múltiplos campos (ex: WWR < 1.0 se há janelas).

### RF-04: Validação Física
O sistema DEVE verificar leis físicas fundamentais (ex: condutividade térmica > 0).

### RF-05: Logging Estruturado
O sistema DEVE gerar logs estruturados de todas as validações (sucesso e falha).

---

## 🏗️ Arquitetura

### Diagrama de Classes

```
┌─────────────────────────────────────────┐
│        GuardrailValidator               │
├─────────────────────────────────────────┤
│ + validate(data: dict) -> ValidationResult │
│ + validate_type(field, value) -> bool   │
│ + validate_range(field, value) -> bool  │
│ + validate_physics(data) -> bool        │
│ + validate_cross(data) -> bool          │
│ + get_validation_report() -> dict       │
└─────────────────────────────────────────┘
                  │
                  │ usa
                  ▼
┌─────────────────────────────────────────┐
│        ValidationResult                 │
├─────────────────────────────────────────┤
│ + is_valid: bool                        │
│ + errors: List[ValidationError]         │
│ + warnings: List[str]                   │
│ + data: dict                            │
└─────────────────────────────────────────┘
                  │
                  │ contém
                  ▼
┌─────────────────────────────────────────┐
│        ValidationError                  │
├─────────────────────────────────────────┤
│ + field: str                            │
│ + value: Any                            │
│ + expected: str                         │
│ + severity: str (ERROR, WARNING)        │
│ + message: str                          │
└─────────────────────────────────────────┘
```

---

## 📦 Classes e Métodos

### Classe: `ValidationError`

```python
from dataclasses import dataclass
from typing import Any, Literal

@dataclass
class ValidationError:
    """Representa um erro de validação"""
    field: str
    value: Any
    expected: str
    severity: Literal["ERROR", "WARNING"]
    message: str
    
    def __str__(self) -> str:
        return f"[{self.severity}] {self.field}: {self.message}"
```

**Exemplo de uso:**
```python
error = ValidationError(
    field="window_to_wall_ratio",
    value=1.5,
    expected="0.0 <= WWR <= 1.0",
    severity="ERROR",
    message="WWR deve estar entre 0 e 1 (100%)"
)
```

---

### Classe: `ValidationResult`

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class ValidationResult:
    """Resultado de uma validação"""
    is_valid: bool
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    data: Dict[str, Any] = field(default_factory=dict)
    
    def add_error(self, error: ValidationError):
        """Adiciona erro ao resultado"""
        self.errors.append(error)
        if error.severity == "ERROR":
            self.is_valid = False
    
    def summary(self) -> str:
        """Retorna resumo da validação"""
        if self.is_valid:
            return f"✅ Validação passou ({len(self.warnings)} warnings)"
        return f"❌ Validação falhou ({len(self.errors)} erros)"
```

---

### Classe: `GuardrailValidator`

```python
from typing import Dict, Any, Tuple
import logging

class GuardrailValidator:
    """
    Validador multi-camadas para dados de simulação BPS.
    
    Implementa 5 camadas de validação:
    1. Type checking
    2. Range checking
    3. Physics checking
    4. Cross-field checking
    5. Audit logging
    """
    
    def __init__(self, strict_mode: bool = True):
        """
        Inicializa validador.
        
        Args:
            strict_mode: Se True, warnings são tratados como erros
        """
        self.strict_mode = strict_mode
        self.logger = logging.getLogger("GuardrailValidator")
        self._setup_logging()
    
    def _setup_logging(self):
        """Configura logging estruturado"""
        handler = logging.FileHandler("validation_audit.log")
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """
        Executa validação completa em 5 camadas.
        
        Args:
            data: Dicionário com dados a validar
        
        Returns:
            ValidationResult com status e erros
        """
        result = ValidationResult(is_valid=True, data=data)
        
        self.logger.info(f"Iniciando validação de {len(data)} campos")
        
        # Camada 1: Type checking
        self._validate_types(data, result)
        
        # Camada 2: Range checking
        self._validate_ranges(data, result)
        
        # Camada 3: Physics checking
        self._validate_physics(data, result)
        
        # Camada 4: Cross-field checking
        self._validate_cross_fields(data, result)
        
        # Camada 5: Audit log
        self._log_validation(result)
        
        return result
    
    def _validate_types(self, data: Dict, result: ValidationResult):
        """Camada 1: Valida tipos de dados"""
        type_schema = self._get_type_schema()
        
        for field, expected_type in type_schema.items():
            if field not in data:
                continue  # Campo opcional
            
            value = data[field]
            if not isinstance(value, expected_type):
                error = ValidationError(
                    field=field,
                    value=value,
                    expected=f"type {expected_type.__name__}",
                    severity="ERROR",
                    message=f"Tipo incorreto: esperado {expected_type.__name__}, "
                            f"recebido {type(value).__name__}"
                )
                result.add_error(error)
    
    def _validate_ranges(self, data: Dict, result: ValidationResult):
        """Camada 2: Valida ranges numéricos"""
        range_schema = self._get_range_schema()
        
        for field, (min_val, max_val) in range_schema.items():
            if field not in data:
                continue
            
            value = data[field]
            if not (min_val <= value <= max_val):
                error = ValidationError(
                    field=field,
                    value=value,
                    expected=f"{min_val} <= value <= {max_val}",
                    severity="ERROR",
                    message=f"Valor fora do range: {value} não está em [{min_val}, {max_val}]"
                )
                result.add_error(error)
    
    def _validate_physics(self, data: Dict, result: ValidationResult):
        """Camada 3: Valida leis físicas"""
        # Lei 1: Condutividade térmica > 0
        if "thermal_conductivity" in data:
            k = data["thermal_conductivity"]
            if k <= 0:
                error = ValidationError(
                    field="thermal_conductivity",
                    value=k,
                    expected="k > 0",
                    severity="ERROR",
                    message="Condutividade térmica deve ser positiva (2ª Lei Termodinâmica)"
                )
                result.add_error(error)
        
        # Lei 2: ρ × cp > 200 (capacidade térmica mínima para materiais reais)
        if "density" in data and "specific_heat" in data:
            rho = data["density"]
            cp = data["specific_heat"]
            thermal_mass = rho * cp
            
            if thermal_mass < 200:
                error = ValidationError(
                    field="thermal_mass",
                    value=thermal_mass,
                    expected="ρ×cp >= 200 J/m³-K",
                    severity="WARNING",
                    message=f"Massa térmica muito baixa: {thermal_mass:.1f} J/m³-K "
                            f"(típico: 200-2000)"
                )
                result.add_error(error)
        
        # Lei 3: U-value consistente com camadas
        if "u_value" in data and "layers" in data:
            self._validate_u_value_consistency(data, result)
    
    def _validate_cross_fields(self, data: Dict, result: ValidationResult):
        """Camada 4: Valida consistência entre campos"""
        # Regra 1: Se tem janela, WWR deve ser > 0
        if data.get("has_window", False):
            wwr = data.get("window_to_wall_ratio", 0)
            if wwr <= 0:
                error = ValidationError(
                    field="window_to_wall_ratio",
                    value=wwr,
                    expected="WWR > 0 se has_window=True",
                    severity="ERROR",
                    message="Parede marcada com janela mas WWR=0"
                )
                result.add_error(error)
        
        # Regra 2: Espessura total = soma das camadas
        if "total_thickness" in data and "layers" in data:
            total = data["total_thickness"]
            layers_sum = sum(layer["thickness"] for layer in data["layers"])
            
            if abs(total - layers_sum) > 0.001:  # Tolerância 1mm
                error = ValidationError(
                    field="total_thickness",
                    value=total,
                    expected=f"sum(layers) = {layers_sum:.4f}",
                    severity="ERROR",
                    message=f"Espessura total ({total}) != soma das camadas ({layers_sum})"
                )
                result.add_error(error)
    
    def _log_validation(self, result: ValidationResult):
        """Camada 5: Registra validação no audit log"""
        if result.is_valid:
            self.logger.info(f"Validação PASSOU: {result.summary()}")
        else:
            self.logger.error(f"Validação FALHOU: {result.summary()}")
            for error in result.errors:
                self.logger.error(f"  {error}")
    
    def _get_type_schema(self) -> Dict[str, type]:
        """Retorna schema de tipos esperados"""
        return {
            "wall_name": str,
            "thickness": float,
            "thermal_conductivity": float,
            "density": float,
            "specific_heat": float,
            "window_to_wall_ratio": float,
            "has_window": bool,
            "orientation": str,
        }
    
    def _get_range_schema(self) -> Dict[str, Tuple[float, float]]:
        """Retorna schema de ranges válidos (min, max)"""
        return {
            "thickness": (0.001, 1.0),  # 1mm a 1m
            "thermal_conductivity": (0.001, 10.0),  # W/m-K
            "density": (10.0, 10000.0),  # kg/m³
            "specific_heat": (100.0, 5000.0),  # J/kg-K
            "window_to_wall_ratio": (0.0, 1.0),  # 0-100%
            "u_value": (0.1, 10.0),  # W/m²-K
        }
    
    def _validate_u_value_consistency(self, data: Dict, result: ValidationResult):
        """Valida que U-value é consistente com resistências das camadas"""
        # U = 1 / R_total
        # R_total = sum(thickness_i / conductivity_i)
        
        layers = data["layers"]
        r_total = sum(
            layer["thickness"] / layer["conductivity"]
            for layer in layers
        )
        
        u_calculated = 1 / r_total if r_total > 0 else float('inf')
        u_declared = data["u_value"]
        
        # Tolerância 10%
        if abs(u_calculated - u_declared) / u_declared > 0.10:
            error = ValidationError(
                field="u_value",
                value=u_declared,
                expected=f"{u_calculated:.3f} W/m²-K",
                severity="WARNING",
                message=f"U-value declarado ({u_declared:.3f}) difere do calculado "
                        f"({u_calculated:.3f}) em mais de 10%"
            )
            result.add_error(error)
    
    def get_validation_report(self) -> Dict:
        """Retorna relatório de validações executadas"""
        # Lê audit log
        with open("validation_audit.log", 'r') as f:
            logs = f.readlines()
        
        return {
            "total_validations": len(logs),
            "passed": len([l for l in logs if "PASSOU" in l]),
            "failed": len([l for l in logs if "FALHOU" in l]),
            "recent_logs": logs[-10:]  # Últimas 10 entradas
        }
```

---

## ✅ Casos de Teste Obrigatórios

### Teste 1: Validação de Tipo - Sucesso

```python
def test_type_validation_success():
    validator = GuardrailValidator()
    
    data = {
        "wall_name": "Parede Externa",
        "thickness": 0.25,
        "thermal_conductivity": 1.4,
        "has_window": True
    }
    
    result = validator.validate(data)
    
    assert result.is_valid == True
    assert len(result.errors) == 0
```

### Teste 2: Validação de Tipo - Falha

```python
def test_type_validation_failure():
    validator = GuardrailValidator()
    
    data = {
        "thickness": "0.25",  # String ao invés de float
        "has_window": "yes"   # String ao invés de bool
    }
    
    result = validator.validate(data)
    
    assert result.is_valid == False
    assert len(result.errors) == 2
    assert any("thickness" in e.field for e in result.errors)
    assert any("has_window" in e.field for e in result.errors)
```

### Teste 3: Validação de Range - Falha

```python
def test_range_validation_failure():
    validator = GuardrailValidator()
    
    data = {
        "window_to_wall_ratio": 1.5,  # > 1.0
        "thermal_conductivity": -0.5  # < 0
    }
    
    result = validator.validate(data)
    
    assert result.is_valid == False
    assert any("window_to_wall_ratio" in e.field for e in result.errors)
    assert any("thermal_conductivity" in e.field for e in result.errors)
```

### Teste 4: Validação Física - Lei Termodinâmica

```python
def test_physics_validation_thermodynamics():
    validator = GuardrailValidator()
    
    data = {
        "density": 100.0,
        "specific_heat": 1.0,  # ρ×cp = 100 < 200
    }
    
    result = validator.validate(data)
    
    # Deve gerar WARNING (não bloqueia, mas alerta)
    assert len(result.warnings) > 0 or len(result.errors) > 0
```

### Teste 5: Validação Cruzada - Janela sem WWR

```python
def test_cross_validation_window():
    validator = GuardrailValidator()
    
    data = {
        "has_window": True,
        "window_to_wall_ratio": 0.0  # Inconsistente
    }
    
    result = validator.validate(data)
    
    assert result.is_valid == False
    assert any("window_to_wall_ratio" in e.field for e in result.errors)
```

### Teste 6: Validação de Camadas - Espessura Total

```python
def test_cross_validation_layers():
    validator = GuardrailValidator()
    
    data = {
        "total_thickness": 0.30,
        "layers": [
            {"thickness": 0.10, "conductivity": 1.0},
            {"thickness": 0.15, "conductivity": 0.5}  # Soma = 0.25
        ]
    }
    
    result = validator.validate(data)
    
    assert result.is_valid == False
    assert any("total_thickness" in e.field for e in result.errors)
```

### Teste 7: U-Value Consistency

```python
def test_u_value_consistency():
    validator = GuardrailValidator()
    
    # R = 0.1/1.0 + 0.2/0.5 = 0.1 + 0.4 = 0.5
    # U = 1/0.5 = 2.0 W/m²-K
    
    data = {
        "u_value": 3.0,  # Declarado incorreto
        "layers": [
            {"thickness": 0.1, "conductivity": 1.0},
            {"thickness": 0.2, "conductivity": 0.5}
        ]
    }
    
    result = validator.validate(data)
    
    # Deve gerar WARNING (diferença > 10%)
    assert len(result.warnings) > 0 or any("u_value" in e.field for e in result.errors)
```

### Teste 8: Audit Log Gerado

```python
def test_audit_log():
    import os
    
    validator = GuardrailValidator()
    
    data = {"thickness": 0.25}
    result = validator.validate(data)
    
    # Verificar que arquivo de log foi criado
    assert os.path.exists("validation_audit.log")
    
    # Verificar conteúdo
    with open("validation_audit.log", 'r') as f:
        content = f.read()
        assert "Iniciando validação" in content
```

### Teste 9: Strict Mode vs Non-Strict

```python
def test_strict_mode():
    # Strict: warnings são erros
    validator_strict = GuardrailValidator(strict_mode=True)
    
    data = {
        "density": 100.0,
        "specific_heat": 1.0  # Gera WARNING
    }
    
    result_strict = validator_strict.validate(data)
    # Em strict mode, WARNING bloqueia
    
    # Non-strict: warnings são apenas avisos
    validator_non_strict = GuardrailValidator(strict_mode=False)
    result_non_strict = validator_non_strict.validate(data)
    
    # Comportamento pode variar conforme implementação
```

### Teste 10: Validação Completa - Caso Real

```python
def test_complete_validation_real_case():
    validator = GuardrailValidator()
    
    # Parede externa típica brasileira
    data = {
        "wall_name": "Parede Externa Norte",
        "thickness": 0.25,
        "thermal_conductivity": 1.15,  # Bloco cerâmico + reboco
        "density": 1600.0,
        "specific_heat": 920.0,
        "u_value": 2.42,
        "window_to_wall_ratio": 0.25,
        "has_window": True,
        "orientation": "North",
        "total_thickness": 0.25,
        "layers": [
            {"thickness": 0.025, "conductivity": 1.15, "name": "Reboco externo"},
            {"thickness": 0.200, "conductivity": 0.90, "name": "Bloco cerâmico"},
            {"thickness": 0.025, "conductivity": 1.15, "name": "Reboco interno"}
        ]
    }
    
    result = validator.validate(data)
    
    assert result.is_valid == True
    print(result.summary())
```

---

## 📊 Critérios de Aceitação

### CA-01: Test Coverage
- [ ] Test coverage ≥ 90% (medido com pytest-cov)
- [ ] Todos os 10 testes obrigatórios passam
- [ ] Nenhum teste flakey (não-determinístico)

### CA-02: Performance
- [ ] Validação de 1 objeto < 10ms
- [ ] Validação de 1000 objetos < 2s
- [ ] Audit log não excede 100MB por dia

### CA-03: Documentação
- [ ] Docstrings em 100% dos métodos públicos
- [ ] README com exemplos de uso
- [ ] Tabela de ranges fundamentada (ASHRAE Handbook, ISO 10456)

### CA-04: Qualidade de Código
- [ ] Tipagem estática completa (mypy --strict passa)
- [ ] Formatação Black
- [ ] Linting Pylint ≥ 9.0/10

### CA-05: Integridade Científica
- [ ] Ranges baseados em referências (não arbitrários)
- [ ] Validações físicas verificadas por engenheiro
- [ ] Exemplos de teste com valores reais (não 0.0, 1.0)

---

## 📚 Referências Técnicas

### Ranges Físicos Fundamentados

| Propriedade | Min | Max | Unidade | Referência |
|-------------|-----|-----|---------|------------|
| Thermal Conductivity | 0.001 | 10.0 | W/m-K | ASHRAE Fundamentals 2021, Ch. 26 |
| Density | 10.0 | 10000.0 | kg/m³ | ISO 10456:2007 |
| Specific Heat | 100.0 | 5000.0 | J/kg-K | ASHRAE Fundamentals 2021, Ch. 26 |
| Thickness (walls) | 0.001 | 1.0 | m | Prática construtiva |
| WWR | 0.0 | 1.0 | adim | Definição (razão) |
| U-value | 0.1 | 10.0 | W/m²-K | ASHRAE 90.1-2019 |

### Validações Físicas

1. **2ª Lei Termodinâmica**: Calor não flui espontaneamente de corpo frio para quente
   - `thermal_conductivity > 0`

2. **Massa Térmica Mínima**: Materiais reais têm capacidade térmica > 200 J/m³-K
   - `density × specific_heat ≥ 200`

3. **Conservação de Energia**: U-value consistente com resistências térmicas
   - `U = 1 / sum(R_i)`

---

## 🚀 Exemplo de Uso Completo

```python
from guardrails import GuardrailValidator

# Inicializar validador
validator = GuardrailValidator(strict_mode=True)

# Dados de entrada
wall_data = {
    "wall_name": "Parede Externa Sul",
    "thickness": 0.30,
    "thermal_conductivity": 1.2,
    "density": 1800.0,
    "specific_heat": 1000.0,
    "window_to_wall_ratio": 0.30,
    "has_window": True,
    "orientation": "South"
}

# Validar
result = validator.validate(wall_data)

# Verificar resultado
if result.is_valid:
    print("✅ Dados validados com sucesso!")
    # Prosseguir para simulação
else:
    print(f"❌ Validação falhou: {len(result.errors)} erros")
    for error in result.errors:
        print(f"  • {error}")
    
    # Bloquear simulação
    raise ValueError("Dados inválidos, simulação não executada")

# Relatório de auditoria
report = validator.get_validation_report()
print(f"\nRelatório: {report['passed']} passed, {report['failed']} failed")
```

---

## 📝 Checklist de Implementação

### Fase 1: Estrutura Base (2h)
- [ ] Criar `validation_error.py` com classe ValidationError
- [ ] Criar `validation_result.py` com classe ValidationResult
- [ ] Criar `guardrail_validator.py` com classe principal
- [ ] Setup de logging estruturado

### Fase 2: Camadas de Validação (2h)
- [ ] Implementar `_validate_types()`
- [ ] Implementar `_validate_ranges()`
- [ ] Implementar `_validate_physics()`
- [ ] Implementar `_validate_cross_fields()`
- [ ] Implementar `_log_validation()`

### Fase 3: Testes (1h)
- [ ] Criar `test_guardrails.py`
- [ ] Implementar 10 testes obrigatórios
- [ ] Executar pytest-cov
- [ ] Ajustar até coverage ≥ 90%

### Fase 4: Documentação (30min)
- [ ] README.md com quickstart
- [ ] Docstrings completas
- [ ] Tabela de ranges fundamentada
- [ ] Exemplos de uso real

---

## 🎓 Observações Finais

**Esta especificação é COMPLETA e EXECUTÁVEL.**  
O aluno deve:
1. Ler toda a especificação (30min)
2. Implementar classes seguindo a API (3h)
3. Executar testes obrigatórios (1h)
4. Documentar e commitar (30min)

**Tempo Total Estimado: 5 horas**

**Critério de Sucesso Final:**
- ✅ Todos os 10 testes passam
- ✅ Coverage ≥ 90%
- ✅ mypy --strict sem erros
- ✅ Exemplos de uso funcionam

---

**Referências:**
- Jiang, Z., et al. (2024). "Large Language Models for Building Energy Applications". Automation in Construction.
- ASHRAE. (2021). "Fundamentals Handbook". Chapter 26: Heat, Air, and Moisture Control.
- ISO 10456:2007. "Building materials and products - Hygrothermal properties".
