# **🛠️ Exercícios Práticos - Mês 2: Engenharia de Software Científica**

**Objetivo do Mês:** Aplicar rigor de engenharia de software a código científico usando validação de dados e workflows estruturados.

**Estratégia:** "Data-First Validation" - Estruturar dados rigorosamente ANTES de processar no EnergyPlus.

**Conceito Central:** Scripts científicos não devem depender de "strings mágicas" ou valores inválidos. Validação acontece ANTES da simulação.

**Tempo Estimado Total:** 50-60 horas (distribuído em 4 semanas)

**Pré-Requisitos:**
- ✅ Mês 1 concluído (automação EnergyPlus)
- ✅ Conhecimento de orientação a objetos em Python
- ✅ Familiaridade com JSON

---

## **📋 Checklist de Progresso do Mês**

| Semana | Objetivo | Status | Tempo Estimado |
|--------|----------|--------|----------------|
| Semana 1 | Pydantic & Validação de Dados | ⬜ | 12-14h |
| Semana 2 | GuardrailValidator Library (Jiang 2024) | ⬜ | 14-16h |
| Semana 3 | JSON-Python Workflows Modular | ⬜ | 12-14h |
| Semana 4 | Projeto Final: Sistema Integrado | ⬜ | 12-16h |

---

## **SEMANA 1: PYDANTIC & VALIDAÇÃO DE DADOS**

### **📌 Exercício 1.1 - Introdução ao Pydantic**

**Objetivo:** Entender como Pydantic valida dados automaticamente.

**Conceito-Chave:**
Pydantic usa type hints Python para validar dados EM TEMPO DE EXECUÇÃO, não apenas em tempo de compilação.

**Tarefa:**

1. **Instalar Pydantic v2**
   ```powershell
   pip install pydantic==2.5.0
   ```

2. **Criar Arquivo `pydantic_intro.py`**

```python
"""
Introdução ao Pydantic - Validação de Dados.
Mês 2 - Exercício 1.1
"""

from pydantic import BaseModel, Field, ValidationError
from typing import Optional

# ===== MODELO 1: Propriedades de Material Simples =====
class MaterialProperties(BaseModel):
    """
    Propriedades térmicas de um material.
    Pydantic valida automaticamente tipos e valores.
    """
    
    name: str = Field(..., min_length=1, max_length=50, description="Nome do material")
    
    # Valores DEVEM ser números positivos
    thickness: float = Field(..., gt=0, le=10, description="Espessura em metros (0-10m)")
    conductivity: float = Field(..., gt=0, le=2.5, description="Condutividade W/m-K (0-2.5)")
    density: float = Field(..., gt=0, le=3000, description="Densidade kg/m³ (0-3000)")
    specific_heat: float = Field(..., gt=0, le=2000, description="Calor específico J/kg-K (0-2000)")
    
    class Config:
        """Configurações do modelo Pydantic."""
        str_strip_whitespace = True
        json_schema_extra = {
            "example": {
                "name": "Concrete",
                "thickness": 0.20,
                "conductivity": 1.40,
                "density": 2300,
                "specific_heat": 880
            }
        }

# ===== MODELO 2: Zona Térmica =====
class ThermalZone(BaseModel):
    """Definição de uma zona térmica."""
    
    name: str
    volume: float = Field(..., gt=0, description="Volume em m³")
    floor_area: float = Field(..., gt=0, description="Área útil em m²")
    height: float = Field(..., gt=0, le=5, description="Pé direito em metros (max 5m)")

# ===== MODELO 3: Configuração Completa de Simulação =====
class SimulationConfig(BaseModel):
    """Configuração completa de uma simulação."""
    
    project_name: str
    materials: list[MaterialProperties]
    zones: list[ThermalZone]
    wwr: float = Field(default=0.3, ge=0.0, le=0.9, description="Window-to-Wall Ratio")
    heating_setpoint: float = Field(default=20, ge=15, le=25, description="Temperatura de aquecimento °C")
    cooling_setpoint: float = Field(default=26, ge=20, le=30, description="Temperatura de resfriamento °C")

# ===== TESTES =====
def test_valid_material():
    """Teste 1: Criar material com valores válidos."""
    print("📝 Teste 1: Material com valores VÁLIDOS")
    print("-" * 60)
    
    material = MaterialProperties(
        name="Concrete",
        thickness=0.20,
        conductivity=1.40,
        density=2300,
        specific_heat=880
    )
    
    print(f"✅ Material criado com sucesso:")
    print(f"   Nome: {material.name}")
    print(f"   Espessura: {material.thickness} m")
    print(f"   Condutividade: {material.conductivity} W/m-K")
    print()

def test_invalid_thickness():
    """Teste 2: Tentar criar material com espessura negativa (DEVE FALHAR)."""
    print("📝 Teste 2: Material com espessura NEGATIVA (deve falhar)")
    print("-" * 60)
    
    try:
        material = MaterialProperties(
            name="BadMaterial",
            thickness=-0.05,  # ❌ INVÁLIDO: espessura negativa
            conductivity=1.40,
            density=2300,
            specific_heat=880
        )
    except ValidationError as e:
        print(f"❌ Validação falhou (esperado):")
        print(f"   Erro: {e.error_count()} problema(s) encontrado(s)")
        for error in e.errors():
            print(f"   - Campo: {error['loc']}")
            print(f"     Problema: {error['msg']}")
        print()

def test_invalid_conductivity():
    """Teste 3: Tentar criar material com condutividade acima do limite."""
    print("📝 Teste 3: Material com condutividade INVÁLIDA (muito alta)")
    print("-" * 60)
    
    try:
        material = MaterialProperties(
            name="Impossible",
            thickness=0.20,
            conductivity=5.0,  # ❌ INVÁLIDO: max é 2.5
            density=2300,
            specific_heat=880
        )
    except ValidationError as e:
        print(f"❌ Validação falhou (esperado):")
        for error in e.errors():
            print(f"   - {error['msg']}")
        print()

def test_invalid_type():
    """Teste 4: Tentar passar tipo errado (string em vez de float)."""
    print("📝 Teste 4: Tipo de dado ERRADO")
    print("-" * 60)
    
    try:
        material = MaterialProperties(
            name="TypeError",
            thickness="zero ponto vinte",  # ❌ INVÁLIDO: deve ser float
            conductivity=1.40,
            density=2300,
            specific_heat=880
        )
    except ValidationError as e:
        print(f"❌ Validação falhou (esperado):")
        for error in e.errors():
            print(f"   - {error['msg']}")
        print()

def test_complete_config():
    """Teste 5: Criar configuração completa."""
    print("📝 Teste 5: Configuração COMPLETA de Simulação")
    print("-" * 60)
    
    config = SimulationConfig(
        project_name="Mês2_Validação",
        materials=[
            MaterialProperties(
                name="Exterior Wall",
                thickness=0.20,
                conductivity=0.50,
                density=800,
                specific_heat=1000
            ),
            MaterialProperties(
                name="Insulation",
                thickness=0.05,
                conductivity=0.04,
                density=20,
                specific_heat=1500
            )
        ],
        zones=[
            ThermalZone(
                name="Living Room",
                volume=50,
                floor_area=25,
                height=2.8
            ),
            ThermalZone(
                name="Bedroom",
                volume=30,
                floor_area=15,
                height=2.8
            )
        ],
        wwr=0.35,
        heating_setpoint=21,
        cooling_setpoint=26
    )
    
    print(f"✅ Configuração válida criada:")
    print(f"   Projeto: {config.project_name}")
    print(f"   Materiais: {len(config.materials)}")
    print(f"   Zonas: {len(config.zones)}")
    print(f"   WWR: {config.wwr:.1%}")
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("🎓 PYDANTIC - VALIDAÇÃO AUTOMÁTICA DE DADOS")
    print("=" * 60)
    print()
    
    # Executar testes
    test_valid_material()
    test_invalid_thickness()
    test_invalid_conductivity()
    test_invalid_type()
    test_complete_config()
    
    print("=" * 60)
    print("✅ Exercício 1.1 Concluído!")
    print("=" * 60)
```

3. **Executar e Analisar Erros**
   ```powershell
   python pydantic_intro.py
   ```

**✅ Checkpoint de Validação:**
- ✅ Teste 1: Material válido criado com sucesso
- ✅ Teste 2: Espessura negativa rejeitada
- ✅ Teste 3: Condutividade > 2.5 rejeitada
- ✅ Teste 4: Tipo errado (string) rejeitado
- ✅ Teste 5: Configuração completa validada

**🔑 Aprendizado Principal:**
> "Pydantic valida dados ANTES que possam causar problemas no EnergyPlus"

**⏱️ Tempo Estimado:** 3-4 horas

---

### **📌 Exercício 1.2 - Validação com Constraints Físicas**

**Objetivo:** Implementar validadores customizados para relações físicas complexas.

**Conceito:** Algumas restrições não são simples limites (min/max), mas relações entre múltiplos campos.

**Exemplo:** A densidade vezes o calor específico não pode ultrapassar um limite físico.

**Tarefa:**

1. **Criar Arquivo `validacao_avancada.py`**

```python
"""
Validação Avançada com Constraints Físicos.
Mês 2 - Exercício 1.2
"""

from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import Optional

class AdvancedMaterialProperties(BaseModel):
    """
    Propriedades de material com validação de constraints físicas.
    """
    
    name: str = Field(..., min_length=1, max_length=50)
    thickness: float = Field(..., gt=0, le=10)
    conductivity: float = Field(..., gt=0, le=2.5)
    density: float = Field(..., gt=0, le=3000)
    specific_heat: float = Field(..., gt=0, le=2000)
    
    # ===== VALIDADORES CUSTOMIZADOS =====
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Nome deve conter apenas letras, números e underscore."""
        if not all(c.isalnum() or c == '_' for c in v):
            raise ValueError("Nome deve conter apenas letras, números e underscore")
        return v.strip()
    
    @field_validator('density')
    @classmethod
    def validate_material_density(cls, v, info: ValidationInfo):
        """
        Validador avançado: densidade vs tipo de material.
        
        Exemplo: isolamento (condutividade < 0.1) NÃO pode ter densidade > 100
        """
        conductivity = info.data.get('conductivity')
        
        # Se é isolamento (k < 0.1)
        if conductivity and conductivity < 0.1:
            if v > 100:
                raise ValueError(
                    f"Material isolante com densidade {v} é fisicamente improvável. "
                    f"Isolantes típicos têm ρ < 100 kg/m³"
                )
        
        return v
    
    @field_validator('specific_heat')
    @classmethod
    def validate_energy_capacity(cls, v, info: ValidationInfo):
        """
        Validador: capacidade térmica (ρ × cp) deve ser realista.
        
        Típico: 200 < ρ×cp < 2.5M J/m³K
        """
        density = info.data.get('density', 1000)  # default 1000
        
        energy_capacity = density * v
        
        if energy_capacity < 200:
            raise ValueError(
                f"Capacidade térmica muito baixa ({energy_capacity} J/m³K). "
                f"Recomendação: ρ×cp > 200"
            )
        
        if energy_capacity > 2.5e6:
            raise ValueError(
                f"Capacidade térmica muito alta ({energy_capacity} J/m³K). "
                f"Recomendação: ρ×cp < 2.5M"
            )
        
        return v

# ===== TESTE =====
def test_advanced_validation():
    """Teste de validadores customizados."""
    
    print("📝 Teste: Validadores Customizados")
    print("-" * 60)
    
    # Teste 1: Material realista
    print("\n✅ Teste 1: Material realista (concreto)")
    try:
        concrete = AdvancedMaterialProperties(
            name="Concrete_240mm",
            thickness=0.24,
            conductivity=1.40,
            density=2300,
            specific_heat=880
        )
        print(f"   Capacidade térmica: {concrete.density * concrete.specific_heat:,.0f} J/m³K")
        print("   ✅ Validação passou!")
    except ValueError as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste 2: Isolamento inválido (densidade muito alta)
    print("\n❌ Teste 2: Isolamento com densidade inválida")
    try:
        bad_insulation = AdvancedMaterialProperties(
            name="BadInsulation",
            thickness=0.10,
            conductivity=0.04,  # Isolamento
            density=500,  # ❌ Muito alta para isolante
            specific_heat=1500
        )
    except ValueError as e:
        print(f"   ❌ Erro esperado: {e}")
    
    # Teste 3: Capacidade térmica muito baixa
    print("\n❌ Teste 3: Capacidade térmica muito baixa")
    try:
        low_capacity = AdvancedMaterialProperties(
            name="Foam",
            thickness=0.05,
            conductivity=0.03,
            density=10,  # Muito leve
            specific_heat=1400
        )
    except ValueError as e:
        print(f"   ❌ Erro esperado: {e}")

if __name__ == "__main__":
    test_advanced_validation()
```

2. **Executar**
   ```powershell
   python validacao_avancada.py
   ```

**✅ Checkpoint de Validação:**
- ✅ Validador de nome: aceita apenas alfanuméricos + underscore
- ✅ Validador de densidade: rejeita isolamento com ρ > 100
- ✅ Validador de capacidade térmica: verifica limites físicos de ρ×cp
- ✅ Mensagens de erro claras e explicam por quê

**Aprendizado:**
> "Validadores customizados garantem que dados não violem leis físicas"

**⏱️ Tempo Estimado:** 3-4 horas

---

### **📌 Exercício 1.3 - JSON Schema Integrado**

**Objetivo:** Gerar documentação automática e validação de JSON.

**Tarefa:**

1. **Criar Arquivo `json_schema.py`**

```python
"""
Geração de JSON Schema a partir de modelos Pydantic.
Mês 2 - Exercício 1.3
"""

from pydantic import BaseModel, Field
import json
from pathlib import Path

class MaterialProperties(BaseModel):
    """Propriedades de material."""
    name: str = Field(..., min_length=1, description="Nome único do material")
    thickness: float = Field(..., gt=0, le=10, description="Espessura em metros")
    conductivity: float = Field(..., gt=0, le=2.5, description="Condutividade W/m-K")
    density: float = Field(..., gt=0, le=3000, description="Densidade kg/m³")
    specific_heat: float = Field(..., gt=0, le=2000, description="Calor específico J/kg-K")

class SimulationSchema(BaseModel):
    """Schema completo de simulação."""
    project_name: str
    materials: list[MaterialProperties]

# ===== GERADOR DE SCHEMA =====
def generate_schema():
    """Gera JSON Schema e salva em arquivo."""
    
    # Gerar schema
    schema = SimulationSchema.model_json_schema()
    
    # Formatar com indentação
    schema_json = json.dumps(schema, indent=2, ensure_ascii=False)
    
    # Salvar em arquivo
    output_path = Path("output/simulation_schema.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(schema_json)
    
    print(f"✅ Schema gerado em: {output_path}")
    print(f"\n📄 Schema JSON:")
    print("-" * 60)
    print(schema_json)
    
    return output_path

# ===== VALIDAÇÃO DE ARQUIVO JSON =====
def validate_json_file(json_path):
    """Valida arquivo JSON contra schema."""
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    try:
        config = SimulationSchema(**data)
        print(f"✅ Arquivo JSON válido!")
        print(f"   Projeto: {config.project_name}")
        print(f"   Materiais: {len(config.materials)}")
        return config
    except ValueError as e:
        print(f"❌ Arquivo JSON inválido!")
        print(f"   Erro: {e}")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("📋 GERADOR DE JSON SCHEMA")
    print("=" * 60)
    print()
    
    # Gerar schema
    generate_schema()
```

2. **Executar**
   ```powershell
   python json_schema.py
   ```

**✅ Checkpoint de Validação:**
- ✅ `simulation_schema.json` gerado automaticamente
- ✅ Schema descreve todos os campos e constraints
- ✅ Você consegue usar schema para validar arquivos JSON externos

**⏱️ Tempo Estimado:** 2-3 horas

---

## **SEMANA 2: GUARDRAILVALIDATOR LIBRARY (JIANG 2024)**

### **📌 Exercício 2.1 - Arquitetura da Biblioteca**

**Objetivo:** Implementar biblioteca `GuardrailValidator` com 3 métodos principais (conforme Jiang 2024).

**Teoria - Jiang et al. 2024:**
> "Large Language Models for Building Energy Applications"
> 
> Guardrails são camadas de validação que impedem que LLMs (ou qualquer código) viole constraints físicos.

**Tarefa:**

1. **Criar Estrutura de Diretórios**
   ```
   mes2_guardrails/
   ├── src/
   │   ├── __init__.py
   │   └── guardrails.py
   ├── tests/
   │   ├── __init__.py
   │   └── test_guardrails.py
   ├── examples/
   │   └── exemplo_uso.py
   └── README.md
   ```

2. **Implementar `src/guardrails.py`**

```python
"""
GuardrailValidator Library - Jiang 2024.
Validação de dados em 3 camadas: Tipo, Constraint, Intervalo.
"""

from dataclasses import dataclass
from typing import Any, Callable, Optional, Union
from enum import Enum

class ConstraintType(Enum):
    """Tipos de constraints suportadas."""
    RANGE = "range"           # min <= valor <= max
    POSITIVE = "positive"      # valor > 0
    NON_NEGATIVE = "non_negative"  # valor >= 0
    CUSTOM = "custom"         # função customizada
    PHYSICAL = "physical"     # constraint físico (ex: ρ × cp)

@dataclass
class ValidationResult:
    """Resultado de uma validação."""
    is_valid: bool
    message: str
    value: Optional[Any] = None
    constraint_violated: Optional[str] = None

class GuardrailValidator:
    """
    Validador de guardrails em 3 camadas.
    
    Camada 1: Type Validation (verificação de tipo)
    Camada 2: Constraint Validation (verificação de domínio)
    Camada 3: Range Validation (verificação de limites min/max)
    """
    
    def __init__(self, name: str):
        """
        Inicializa validador.
        
        Args:
            name: Nome do validador (para logging)
        """
        self.name = name
        self.constraints = {}
        self.validation_log = []
    
    # ===== MÉTODO 1: VALIDAÇÃO DE TIPO =====
    def validate_type(self, value: Any, expected_type: type) -> ValidationResult:
        """
        Camada 1: Verifica se valor tem o tipo correto.
        
        Args:
            value: Valor a validar
            expected_type: Tipo esperado (int, float, str, bool)
        
        Returns:
            ValidationResult com resultado da validação
        
        Exemplos:
            >>> validator = GuardrailValidator("test")
            >>> result = validator.validate_type(5.0, float)
            >>> result.is_valid
            True
            
            >>> result = validator.validate_type("5.0", float)
            >>> result.is_valid
            False
            >>> print(result.message)
            TypeError: Expected <class 'float'>, got <class 'str'>
        """
        
        if type(value) == expected_type:
            result = ValidationResult(
                is_valid=True,
                message=f"✅ Tipo correto: {expected_type.__name__}",
                value=value
            )
        else:
            result = ValidationResult(
                is_valid=False,
                message=f"❌ TypeError: Esperado {expected_type.__name__}, "
                        f"recebido {type(value).__name__}",
                value=value,
                constraint_violated="TYPE_MISMATCH"
            )
        
        self.validation_log.append(result)
        return result
    
    # ===== MÉTODO 2: VALIDAÇÃO DE CONSTRAINT =====
    def validate_constraint(
        self,
        field_name: str,
        value: Any,
        constraint_type: ConstraintType = ConstraintType.RANGE,
        min_val: Optional[float] = None,
        max_val: Optional[float] = None,
        custom_validator: Optional[Callable] = None
    ) -> ValidationResult:
        """
        Camada 2: Verifica se valor satisfaz constraint de domínio.
        
        Args:
            field_name: Nome do campo (para mensagens)
            value: Valor a validar
            constraint_type: Tipo de constraint (RANGE, POSITIVE, CUSTOM, etc)
            min_val: Valor mínimo (para RANGE)
            max_val: Valor máximo (para RANGE)
            custom_validator: Função para validação customizada
        
        Returns:
            ValidationResult
        
        Exemplos:
            >>> validator = GuardrailValidator("bps")
            
            >>> # Constraint RANGE: 0 < espessura <= 10
            >>> result = validator.validate_constraint(
            ...     "espessura", 0.20, 
            ...     ConstraintType.RANGE,
            ...     min_val=0, max_val=10
            ... )
            >>> result.is_valid
            True
            
            >>> # Violação: espessura = -5
            >>> result = validator.validate_constraint(
            ...     "espessura", -5,
            ...     ConstraintType.RANGE,
            ...     min_val=0, max_val=10
            ... )
            >>> result.is_valid
            False
            >>> print(result.message)
            ❌ ConstraintError: espessura=-5 viola constraint RANGE [0, 10]
        """
        
        is_valid = True
        message = ""
        violated = None
        
        if constraint_type == ConstraintType.RANGE:
            if min_val is not None and value < min_val:
                is_valid = False
                violated = f"MIN_BOUND ({min_val})"
                message = (f"❌ ConstraintError: {field_name}={value} "
                          f"viola constraint RANGE [{min_val}, {max_val}] "
                          f"(valor < mínimo)")
            elif max_val is not None and value > max_val:
                is_valid = False
                violated = f"MAX_BOUND ({max_val})"
                message = (f"❌ ConstraintError: {field_name}={value} "
                          f"viola constraint RANGE [{min_val}, {max_val}] "
                          f"(valor > máximo)")
            else:
                message = f"✅ Constraint RANGE satisfeito: {min_val} ≤ {value} ≤ {max_val}"
        
        elif constraint_type == ConstraintType.POSITIVE:
            if value <= 0:
                is_valid = False
                violated = "POSITIVE"
                message = f"❌ ConstraintError: {field_name}={value} não é positivo"
            else:
                message = f"✅ Constraint POSITIVE satisfeito: {value} > 0"
        
        elif constraint_type == ConstraintType.NON_NEGATIVE:
            if value < 0:
                is_valid = False
                violated = "NON_NEGATIVE"
                message = f"❌ ConstraintError: {field_name}={value} é negativo"
            else:
                message = f"✅ Constraint NON_NEGATIVE satisfeito: {value} ≥ 0"
        
        elif constraint_type == ConstraintType.CUSTOM:
            if custom_validator is None:
                is_valid = False
                message = "❌ CUSTOM validator fornecido é None"
            else:
                try:
                    is_valid = custom_validator(value)
                    if is_valid:
                        message = f"✅ Custom validator passou para {field_name}={value}"
                    else:
                        violated = "CUSTOM"
                        message = f"❌ Custom validator falhou para {field_name}={value}"
                except Exception as e:
                    is_valid = False
                    violated = "CUSTOM_EXCEPTION"
                    message = f"❌ Custom validator levantou exceção: {e}"
        
        result = ValidationResult(
            is_valid=is_valid,
            message=message,
            value=value,
            constraint_violated=violated
        )
        
        self.validation_log.append(result)
        return result
    
    # ===== MÉTODO 3: VALIDAÇÃO DE INTERVALO =====
    def validate_range(
        self,
        field_name: str,
        value: Any,
        min_val: float,
        max_val: float,
        inclusive_min: bool = True,
        inclusive_max: bool = True
    ) -> ValidationResult:
        """
        Camada 3: Verifica se valor está dentro de intervalo específico.
        
        Alias mais amigável para validate_constraint com RANGE.
        
        Args:
            field_name: Nome do campo
            value: Valor a validar
            min_val: Limite inferior
            max_val: Limite superior
            inclusive_min: Se True, min_val é incluído (≤). Se False, excluído (<).
            inclusive_max: Se True, max_val é incluído (≤). Se False, excluído (<).
        
        Returns:
            ValidationResult
        
        Exemplos:
            >>> validator = GuardrailValidator("ranges")
            >>> result = validator.validate_range("temperatura", 22, 15, 30)
            >>> result.is_valid
            True
            
            >>> result = validator.validate_range("temperatura", 35, 15, 30)
            >>> result.is_valid
            False
        """
        
        # Determinar se está no intervalo
        if inclusive_min:
            min_ok = value >= min_val
        else:
            min_ok = value > min_val
        
        if inclusive_max:
            max_ok = value <= max_val
        else:
            max_ok = value < max_val
        
        is_valid = min_ok and max_ok
        
        if is_valid:
            bounds = f"[{min_val}, {max_val}]" if inclusive_min and inclusive_max else \
                     f"({min_val}, {max_val}]" if not inclusive_min else \
                     f"[{min_val}, {max_val})" if not inclusive_max else \
                     f"({min_val}, {max_val})"
            message = f"✅ Intervalo satisfeito: {value} ∈ {bounds}"
        else:
            message = (f"❌ RangeError: {field_name}={value} "
                      f"fora do intervalo [{min_val}, {max_val}]")
        
        result = ValidationResult(
            is_valid=is_valid,
            message=message,
            value=value,
            constraint_violated="RANGE" if not is_valid else None
        )
        
        self.validation_log.append(result)
        return result
    
    # ===== MÉTODOS AUXILIARES =====
    def get_validation_log(self) -> list[ValidationResult]:
        """Retorna log de todas as validações realizadas."""
        return self.validation_log
    
    def clear_log(self):
        """Limpa log de validações."""
        self.validation_log = []
    
    def print_report(self):
        """Imprime relatório de validações."""
        print(f"\n📋 Relatório de Validações - {self.name}")
        print("=" * 70)
        
        total = len(self.validation_log)
        passed = sum(1 for r in self.validation_log if r.is_valid)
        failed = total - passed
        
        print(f"Total: {total} validações")
        print(f"✅ Passou: {passed} ({passed/total*100:.1f}%)")
        print(f"❌ Falhou: {failed} ({failed/total*100:.1f}%)")
        print()
        
        for idx, result in enumerate(self.validation_log, 1):
            print(f"{idx}. {result.message}")

if __name__ == "__main__":
    print("=" * 70)
    print("🛡️  GUARDRAILVALIDATOR LIBRARY - DEMONSTRAÇÃO")
    print("=" * 70)
    print()
    
    # Criar validador
    validator = GuardrailValidator("bps_materials")
    
    # Teste 1: Validação de tipo
    print("📝 TESTE 1: Validação de Tipo")
    print("-" * 70)
    result = validator.validate_type(0.20, float)
    print(result.message)
    result = validator.validate_type("0.20", float)
    print(result.message)
    
    # Teste 2: Validação de constraint
    print("\n📝 TESTE 2: Validação de Constraint")
    print("-" * 70)
    result = validator.validate_constraint(
        "espessura", 0.20,
        ConstraintType.RANGE,
        min_val=0, max_val=10
    )
    print(result.message)
    
    result = validator.validate_constraint(
        "espessura", -5,
        ConstraintType.RANGE,
        min_val=0, max_val=10
    )
    print(result.message)
    
    # Teste 3: Validação de intervalo
    print("\n📝 TESTE 3: Validação de Intervalo")
    print("-" * 70)
    result = validator.validate_range("condutividade", 1.40, 0, 2.5)
    print(result.message)
    
    result = validator.validate_range("condutividade", 3.0, 0, 2.5)
    print(result.message)
    
    # Relatório final
    validator.print_report()
```

3. **Implementar Testes `tests/test_guardrails.py`**

```python
"""
Testes unitários para GuardrailValidator.
Mês 2 - Exercício 2.1
"""

import pytest
from pathlib import Path
import sys

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from guardrails import GuardrailValidator, ConstraintType, ValidationResult

class TestGuardrailValidator:
    """Testes da classe GuardrailValidator."""
    
    @pytest.fixture
    def validator(self):
        """Fixture: cria validador para cada teste."""
        return GuardrailValidator("test_validator")
    
    # ===== TESTES: validate_type =====
    def test_validate_type_float_success(self, validator):
        """Teste: validar tipo float com sucesso."""
        result = validator.validate_type(5.0, float)
        assert result.is_valid == True
        assert result.value == 5.0
    
    def test_validate_type_float_fail(self, validator):
        """Teste: rejeitar string como float."""
        result = validator.validate_type("5.0", float)
        assert result.is_valid == False
        assert result.constraint_violated == "TYPE_MISMATCH"
    
    def test_validate_type_int_success(self, validator):
        """Teste: validar tipo int."""
        result = validator.validate_type(5, int)
        assert result.is_valid == True
    
    # ===== TESTES: validate_constraint =====
    def test_validate_constraint_range_success(self, validator):
        """Teste: valor dentro do range."""
        result = validator.validate_constraint(
            "thickness", 0.20,
            ConstraintType.RANGE,
            min_val=0, max_val=10
        )
        assert result.is_valid == True
    
    def test_validate_constraint_range_below_min(self, validator):
        """Teste: valor abaixo do mínimo."""
        result = validator.validate_constraint(
            "thickness", -5,
            ConstraintType.RANGE,
            min_val=0, max_val=10
        )
        assert result.is_valid == False
        assert "MIN_BOUND" in result.constraint_violated
    
    def test_validate_constraint_range_above_max(self, validator):
        """Teste: valor acima do máximo."""
        result = validator.validate_constraint(
            "conductivity", 3.0,
            ConstraintType.RANGE,
            min_val=0, max_val=2.5
        )
        assert result.is_valid == False
        assert "MAX_BOUND" in result.constraint_violated
    
    def test_validate_constraint_positive_success(self, validator):
        """Teste: validar positivo com sucesso."""
        result = validator.validate_constraint(
            "density", 2300,
            ConstraintType.POSITIVE
        )
        assert result.is_valid == True
    
    def test_validate_constraint_positive_fail(self, validator):
        """Teste: rejeitar valor não-positivo."""
        result = validator.validate_constraint(
            "density", -100,
            ConstraintType.POSITIVE
        )
        assert result.is_valid == False
    
    # ===== TESTES: validate_range =====
    def test_validate_range_success(self, validator):
        """Teste: valor dentro do intervalo."""
        result = validator.validate_range("temp", 22, 15, 30)
        assert result.is_valid == True
    
    def test_validate_range_fail_above(self, validator):
        """Teste: valor acima do intervalo."""
        result = validator.validate_range("temp", 35, 15, 30)
        assert result.is_valid == False
    
    def test_validate_range_fail_below(self, validator):
        """Teste: valor abaixo do intervalo."""
        result = validator.validate_range("temp", 10, 15, 30)
        assert result.is_valid == False
    
    # ===== TESTES: Logging =====
    def test_validation_log(self, validator):
        """Teste: log de validações."""
        validator.validate_type(5.0, float)
        validator.validate_type("5.0", float)
        
        log = validator.get_validation_log()
        assert len(log) == 2
        assert log[0].is_valid == True
        assert log[1].is_valid == False

# ===== EXECUTAR TESTES =====
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
```

4. **Instalar pytest e Executar Testes**
   ```powershell
   pip install pytest
   pytest tests/test_guardrails.py -v
   ```

**✅ Checkpoint de Validação:**
- ✅ Todos os 3 métodos implementados (validate_type, validate_constraint, validate_range)
- ✅ Todos os testes passam (100% test coverage)
- ✅ Mensagens de erro claras e úteis
- ✅ Documentação com exemplos em cada método

**🔑 Referência:**
> Jiang et al. 2024: "Large Language Models for Building Energy Applications"
> "Guardrails implementam validação em múltiplas camadas para garantir integridade de dados"

**⏱️ Tempo Estimado:** 8-10 horas

---

### **📌 Exercício 2.2 - Integração com Pydantic**

**Objetivo:** Usar GuardrailValidator com modelos Pydantic.

**Tarefa:**

1. **Criar Arquivo `pydantic_integration.py`**

```python
"""
Integração GuardrailValidator + Pydantic.
Mês 2 - Exercício 2.2
"""

from pydantic import BaseModel, Field, field_validator, ValidationInfo
from sys import path as syspath
from pathlib import Path

syspath.insert(0, str(Path(__file__).parent / "src"))
from guardrails import GuardrailValidator, ConstraintType

class MaterialWithGuardrails(BaseModel):
    """Material com validação via Guardrails + Pydantic."""
    
    name: str = Field(..., min_length=1, max_length=50)
    thickness: float = Field(..., gt=0, le=10)
    conductivity: float = Field(..., gt=0, le=2.5)
    density: float = Field(..., gt=0, le=3000)
    specific_heat: float = Field(..., gt=0, le=2000)
    
    @field_validator('thickness')
    @classmethod
    def check_thickness_with_guardrails(cls, v):
        """Usar GuardrailValidator para validação customizada."""
        validator = GuardrailValidator("thickness_check")
        
        # Validar tipo
        type_result = validator.validate_type(v, float)
        if not type_result.is_valid:
            raise ValueError(type_result.message)
        
        # Validar range
        range_result = validator.validate_range("thickness", v, 0.001, 10)
        if not range_result.is_valid:
            raise ValueError(range_result.message)
        
        return v

def test_material_creation():
    """Teste: criar material com validação completa."""
    
    print("📝 Teste: Criação de Material com Guardrails")
    print("-" * 60)
    
    # Sucesso
    try:
        mat = MaterialWithGuardrails(
            name="Concrete",
            thickness=0.20,
            conductivity=1.40,
            density=2300,
            specific_heat=880
        )
        print(f"✅ Material criado: {mat.name}")
    except ValueError as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_material_creation()
```

**⏱️ Tempo Estimado:** 3-4 horas

---

## **SEMANA 3: JSON-PYTHON WORKFLOWS MODULAR**

### **📌 Exercício 3.1 - Arquitetura de Workflow**

**Objetivo:** Criar sistema modular que vai de JSON → Python → EnergyPlus → CSV.

**Tarefa:**

1. **Criar Arquivo `modular_workflow.py`**

```python
"""
Modular JSON-Python Workflow para BPS.
Mês 2 - Exercício 3.1
"""

from pathlib import Path
from pydantic import BaseModel, Field
import json
from typing import Optional

class WorkflowStep(BaseModel):
    """Etapa de um workflow."""
    
    step_id: int
    step_name: str
    description: Optional[str] = None
    input_file: Optional[Path] = None
    output_file: Optional[Path] = None
    parameters: dict = {}

class ModularWorkflow:
    """
    Workflow modular que executa etapas sequenciais.
    
    Etapas típicas:
    1. Ler JSON de configuração
    2. Validar dados (Pydantic + Guardrails)
    3. Modificar IDF
    4. Executar simulação
    5. Extrair resultados
    6. Salvar CSV
    """
    
    def __init__(self, workflow_config: dict):
        """Inicializa workflow."""
        self.config = workflow_config
        self.steps = []
        self.results = {}
    
    def add_step(self, step: WorkflowStep):
        """Adiciona etapa ao workflow."""
        self.steps.append(step)
    
    def execute(self):
        """Executa workflow completo."""
        print(f"🚀 Executando workflow com {len(self.steps)} etapas")
        print("=" * 70)
        
        for step in self.steps:
            print(f"\n📍 Etapa {step.step_id}: {step.step_name}")
            print(f"   {step.description}")
            
            # TODO: Implementar execução de cada etapa
            self._execute_step(step)
    
    def _execute_step(self, step: WorkflowStep):
        """Executa uma etapa individual."""
        if step.step_name == "validate":
            self._step_validate(step)
        elif step.step_name == "modify_idf":
            self._step_modify_idf(step)
        elif step.step_name == "simulate":
            self._step_simulate(step)
        elif step.step_name == "extract":
            self._step_extract(step)
    
    def _step_validate(self, step):
        """Etapa: validar dados."""
        print(f"   ✅ Validando dados...")
    
    def _step_modify_idf(self, step):
        """Etapa: modificar IDF."""
        print(f"   ✅ Modificando IDF...")
    
    def _step_simulate(self, step):
        """Etapa: executar simulação."""
        print(f"   ✅ Executando simulação...")
    
    def _step_extract(self, step):
        """Etapa: extrair resultados."""
        print(f"   ✅ Extraindo resultados...")

def create_example_workflow():
    """Cria exemplo de workflow."""
    
    config = {
        "project_name": "Mes2_Workflow_Exemplo",
        "base_idf": "exemplo.idf",
        "weather_file": "weather.epw"
    }
    
    workflow = ModularWorkflow(config)
    
    # Adicionar etapas
    workflow.add_step(WorkflowStep(
        step_id=1,
        step_name="validate",
        description="Validar arquivo de entrada"
    ))
    
    workflow.add_step(WorkflowStep(
        step_id=2,
        step_name="modify_idf",
        description="Modificar propriedades do edifício"
    ))
    
    workflow.add_step(WorkflowStep(
        step_id=3,
        step_name="simulate",
        description="Executar simulação EnergyPlus"
    ))
    
    workflow.add_step(WorkflowStep(
        step_id=4,
        step_name="extract",
        description="Extrair métricas dos resultados"
    ))
    
    return workflow

if __name__ == "__main__":
    workflow = create_example_workflow()
    workflow.execute()
```

**⏱️ Tempo Estimado:** 4-5 horas

---

## **SEMANA 4: PROJETO FINAL DO MÊS**

### **📌 Exercício 4.1 - Sistema Integrado Completo**

**Objetivo:** Combinar Pydantic + GuardrailValidator + JSON Workflows em um sistema profissional.

**Entregável Final:**

```
mes2_engenharia_software/
├── src/
│   ├── __init__.py
│   ├── guardrails.py
│   ├── validators.py (Pydantic models)
│   ├── workflow.py
│   └── material_extractor.py
├── config/
│   └── building_config.json
├── tests/
│   ├── test_guardrails.py
│   ├── test_validators.py
│   └── test_integration.py
├── examples/
│   └── exemplo_uso_completo.py
├── run_validation_pipeline.py (script principal)
└── README.md
```

**Script Principal (run_validation_pipeline.py):**

```python
"""
Pipeline completo de validação.
Mês 2 - Projeto Final
"""

from pathlib import Path
import json
from src.validators import SimulationConfig
from src.guardrails import GuardrailValidator, ConstraintType
from src.workflow import ModularWorkflow

def main():
    """Função principal."""
    
    print("=" * 70)
    print("🎓 MÊS 2 - PROJETO FINAL: Sistema de Validação Integrado")
    print("=" * 70)
    print()
    
    # 1. Carregar configuração JSON
    print("📖 Etapa 1: Carregar e validar JSON")
    print("-" * 70)
    
    with open("config/building_config.json", 'r') as f:
        config_dict = json.load(f)
    
    # 2. Validar com Pydantic
    print("\n🔍 Etapa 2: Validar com Pydantic")
    print("-" * 70)
    
    try:
        config = SimulationConfig(**config_dict)
        print(f"✅ Configuração válida!")
        print(f"   Projeto: {config.project_name}")
        print(f"   Materiais: {len(config.materials)}")
        print(f"   Zonas: {len(config.zones)}")
    except ValueError as e:
        print(f"❌ Validação falhou: {e}")
        return
    
    # 3. Validar com GuardrailValidator
    print("\n🛡️  Etapa 3: Validar com GuardrailValidator")
    print("-" * 70)
    
    validator = GuardrailValidator("material_validation")
    
    for material in config.materials:
        # Validar cada propriedade
        validator.validate_type(material.thickness, float)
        validator.validate_constraint(
            material.name,
            material.thickness,
            ConstraintType.RANGE,
            min_val=0.001,
            max_val=10
        )
    
    validator.print_report()
    
    # 4. Executar workflow
    print("\n⚙️  Etapa 4: Executar Workflow Modular")
    print("-" * 70)
    
    workflow_config = {
        "project_name": config.project_name,
        "validated": True
    }
    
    workflow = ModularWorkflow(workflow_config)
    workflow.execute()
    
    print("\n✅ Pipeline de validação concluído com sucesso!")

if __name__ == "__main__":
    main()
```

**✅ Checkpoint Final do Mês:**

| Critério | Status | Peso |
|----------|--------|------|
| Pydantic models implementados | ⬜ | 15% |
| GuardrailValidator com 3 métodos | ⬜ | 25% |
| 100% test coverage em guardrails | ⬜ | 20% |
| JSON-Python workflow funcionando | ⬜ | 20% |
| Sistema integrado testado | ⬜ | 20% |

---

## **📚 ENTREGÁVEL FINAL DO MÊS 2**

### **Estrutura Final no GitHub:**

```
piml-training/
├── mes2_engenharia_software/
│   ├── src/
│   │   ├── guardrails.py (500+ linhas)
│   │   ├── validators.py (Pydantic models)
│   │   ├── workflow.py
│   │   └── material_extractor.py
│   ├── tests/
│   │   ├── test_guardrails.py (15+ testes)
│   │   ├── test_validators.py
│   │   └── test_integration.py
│   ├── config/
│   │   └── building_config.json
│   ├── examples/
│   │   └── exemplo_uso_completo.py
│   ├── run_validation_pipeline.py
│   ├── README.md
│   └── NOTAS_LIÇÕES.md
└── notebooks/
    ├── analise_pydantic.ipynb
    └── validacao_guardrails.ipynb
```

### **README.md - Mês 2:**

```markdown
# Mês 2 - Engenharia de Software Científica

## Objetivo
Aplicar rigor de engenharia de software a código científico usando validação multi-camada.

## Componentes Principais

### 1. Pydantic Models (`validators.py`)
- Validação automática de tipos
- Constraints customizados
- JSON schema generation

### 2. GuardrailValidator Library (`guardrails.py`) - JIANG 2024
- 3 métodos de validação: Type, Constraint, Range
- Logging estruturado
- 100% test coverage

### 3. JSON-Python Workflows (`workflow.py`)
- Etapas sequenciais modulares
- Validação em cada etapa
- Integração com EnergyPlus

## Como Usar

```python
from src.guardrails import GuardrailValidator, ConstraintType

# Criar validador
validator = GuardrailValidator("bps_materials")

# Validar tipo
result = validator.validate_type(0.20, float)

# Validar constraint
result = validator.validate_constraint(
    "espessura", 0.20,
    ConstraintType.RANGE,
    min_val=0, max_val=10
)

# Validar intervalo
result = validator.validate_range("temperatura", 22, 15, 30)

# Ver relatório
validator.print_report()
```

## Testes

```bash
pytest tests/ -v --cov=src --cov-report=html
```

## Referências

- Jiang et al. 2024: "Large Language Models for Building Energy Applications"
- [Pydantic Docs](https://docs.pydantic.dev/)

## Lições Aprendidas

[Documentar principais insights]

## Próximos Passos (Mês 3)

- Escalar para 1.000 simulações (Latin Hypercube Sampling)
- Integrar dados reais de sensores
- Limpeza de time series
```

---

## **✅ CERTIFICAÇÃO DE CONCLUSÃO DO MÊS 2**

**Checklist Final:**

### **Conhecimentos Teóricos**
- [ ] Entendo validação em múltiplas camadas (Type, Constraint, Range)
- [ ] Conheço Pydantic e field_validator
- [ ] Entendo guardrails (Jiang 2024)
- [ ] Sei projetar JSON schemas para dados científicos

### **Habilidades Práticas**
- [ ] Implemento modelos Pydantic com constraints customizados
- [ ] Crio GuardrailValidator reutilizável
- [ ] Escrevo testes unitários (pytest)
- [ ] Integro validação em workflows
- [ ] Gero JSON schemas automaticamente

### **Entregáveis**
- [ ] GuardrailValidator com 3 métodos (500+ linhas)
- [ ] 15+ testes com pytest (100% coverage)
- [ ] 3+ Pydantic models com validators
- [ ] Sistema de workflow modular
- [ ] Documentação completa

### **DevOps**
- [ ] Código organizado em módulos/pacotes
- [ ] 15+ commits no Git
- [ ] README.md com exemplos de uso
- [ ] Testes passando e CI-ready

---

## **📊 Tempo Total Investido no Mês 2:** 50-60 horas
## **🎓 Nível de Dificuldade:** ⭐⭐⭐⭐ (4/5)
## **🔧 Complexidade Técnica:** Alta

---

**🎉 Parabéns por completar Mês 2!**

Você agora tem:
✅ Entendimento profundo de validação de dados
✅ Implementação profissional de guardrails
✅ Experiência com Pydantic e pytest
✅ Arquitetura modular para workflows científicos

**Próximo arquivo:** `Exercicios_Mes_3_Big_Data.md`

Pronto para continuar? O Mês 3 será sobre escalabilidade: de 1 para 1.000 simulações! 🚀
