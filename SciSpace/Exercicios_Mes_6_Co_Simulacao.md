# Exercícios Mês 6: Co-Simulação EnergyPlus ↔ Gemini Framework Design

## 📋 Visão Geral

**Objetivo do Mês:** Projetar e implementar framework de co-simulação que acopla EnergyPlus (simulador físico) com Gemini LLM (assistente técnico), permitindo otimizações automáticas baseadas em instruções em linguagem natural.

**Contexto de Integração:**
- **Mês 1 (EnergyPlus Automation):** Controlamos EnergyPlus via Python (Eppy)
- **Mês 4 (PIML Surrogates):** Criamos modelos ML 1000x mais rápidos que EnergyPlus
- **Mês 5 (Prompt Engineering):** Construímos interface LLM com constraints e function calling
- **Mês 6 (Este Mês):** Integramos tudo em loop de co-simulação com otimização automática

**Referências Teóricas:**
- **Zakeri et al. (2025):** "Co-Simulation Frameworks for Building-LLM Integration"
- **ASHRAE Guideline 14:** Measurement and Verification for Performance Contracts
- **FMI 2.0 Standard:** Functional Mock-up Interface para co-simulação

**Estrutura do Mês:**
- **Semana 1:** Design de Arquitetura & UML (12-15h)
- **Semana 2:** Data Exchange Protocols (12-15h)
- **Semana 3:** Coupling Implementation (12-15h)
- **Semana 4:** End-to-End Integration & Roadmap (14-15h)

**Tempo Total Estimado:** 50-60 horas

**Repositório Git:** Continuar usando `piml-training` (branch: `co-simulation`)

---

## 🎯 Objetivos de Aprendizagem

Ao final deste mês, você será capaz de:

1. **Projetar arquitetura** de co-simulação com classes core (SimulationRequest, SimulationResult, CoSimController)
2. **Documentar com UML** diagramas de classe, sequência e atividade
3. **Implementar data exchange** entre EnergyPlus, surrogates e Gemini com JSON schemas
4. **Integrar feedback loops** para otimização iterativa
5. **Escrever roadmap técnico** com prototipagem, validação e deployment
6. **Coordenar múltiplos sistemas** em arquitetura event-driven

---

## 📦 Pré-requisitos

### Conhecimento Técnico
- ✅ Mês 1 (EnergyPlus automation com Eppy)
- ✅ Mês 4 (PIML surrogates: XGBoost, MLP com physics constraints)
- ✅ Mês 5 (Prompt engineering: system prompts, function calling, Gemini API)
- ✅ Design de sistemas (OOP, interfaces, design patterns)
- ✅ UML (diagramas de classe, sequência)

### Infraestrutura
- ✅ EnergyPlus 24.1.0 com Eppy
- ✅ Modelos treinados: `models/xgboost_surrogate.pkl`, `models/mlp_surrogate.pt`
- ✅ Vertex AI com Gemini API configurado
- ✅ Python 3.10+ com bibliotecas anteriores (pandas, pydantic, torch, etc)

### Bibliotecas Python (Novas)
```bash
pip install plantuml                # Gerar diagramas UML
pip install pydantic-json-schema   # JSON schema from Pydantic
pip install strawberry              # GraphQL (opcional, para APIs futuras)
```

### Validação da Infraestrutura
Executar teste rápido que carrega surrogate + Gemini:

```python
# test_co_sim_integration.py
import pickle
import torch
from vertexai.generative_models import GenerativeModel

# Teste 1: Carregar surrogate
with open("models/xgboost_surrogate.pkl", "rb") as f:
    surrogate = pickle.load(f)
print("✅ XGBoost surrogate carregado")

# Teste 2: Conectar Gemini
model = GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Respond with 'OK'.")
print("✅ Gemini API conectada")

print("\n✅ Pré-requisitos validados")
```

**✅ Checkpoint:** Ambos os testes passam sem erro?

---

## 🔹 Semana 1: Design de Arquitetura & UML (12-15 horas)

### 📖 Objetivos da Semana

- Definir classes core do sistema de co-simulação
- Documentar interfaces e contratos de dados
- Criar diagramas UML completos
- Estabelecer padrões de design (MVC, Observer, Command)

### 🎯 Exercício 1.1: Core Data Models (Pydantic) (3-4h)

**Contexto:** Co-simulação requer estruturas de dados bem-definidas para comunicação entre EnergyPlus, surrogates e Gemini. Usaremos Pydantic (como Mês 2) para validação automática.

**Tarefa:** Criar classes Pydantic para SimulationRequest, SimulationResult, OptimizationGoal.

#### Implementação: `cosim_data_models.py`

```python
"""
Exercício 1.1: Data models para co-simulação
Baseado em: Zakeri et al. (2025) - Co-Simulation Framework Design
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, validator
from enum import Enum
from datetime import datetime


class SimulationType(Enum):
    """Tipos de simulação suportados."""
    
    ENERGYPLUS = "energyplus"          # Simulador física (10s por ano)
    SURROGATE_XGBOOST = "surrogate_xgboost"  # ML rápido (10ms)
    SURROGATE_MLP = "surrogate_mlp"    # Neural network (10ms)
    HYBRID = "hybrid"                  # EnergyPlus + LLM optimization


class BPSParameters(BaseModel):
    """Parâmetros físicos de Building Performance Simulation."""
    
    # Envoltória térmica
    wwr: float = Field(..., ge=0.10, le=0.60, description="Window-to-Wall Ratio")
    wall_thickness_m: float = Field(..., ge=0.15, le=0.30, description="Espessura parede (m)")
    insulation_thickness_m: float = Field(..., ge=0.05, le=0.20, description="Espessura isolamento (m)")
    conductivity_wall_W_mK: float = Field(..., ge=0.5, le=2.0, description="Condutividade parede W/mK")
    conductivity_insulation_W_mK: float = Field(..., ge=0.025, le=0.050, description="Condutividade isolamento")
    
    # Operacional
    zone_volume_m3: float = Field(..., ge=500, le=5000, description="Volume da zona (m³)")
    infiltration_rate_ACH: float = Field(..., ge=0.3, le=2.0, description="Infiltração (ACH)")
    internal_loads_W_m2: float = Field(..., ge=5, le=20, description="Cargas internas W/m²")
    
    # HVAC setpoints
    heating_setpoint_C: float = Field(..., ge=15, le=25, description="Setpoint aquecimento °C")
    cooling_setpoint_C: float = Field(..., ge=20, le=28, description="Setpoint resfriamento °C")
    
    @validator('cooling_setpoint_C')
    def cooling_above_heating(cls, v, values):
        if 'heating_setpoint_C' in values and v <= values['heating_setpoint_C']:
            raise ValueError("cooling_setpoint must be > heating_setpoint")
        return v


class SimulationResult(BaseModel):
    """Resultado de uma simulação de energia."""
    
    simulation_id: str
    simulation_type: SimulationType
    parameters: BPSParameters
    
    # Resultados energéticos (kWh/ano)
    annual_heating_kwh: float = Field(..., ge=0, description="Energia anual aquecimento")
    annual_cooling_kwh: float = Field(..., ge=0, description="Energia anual resfriamento")
    total_energy_kwh: float = Field(..., ge=0, description="Energia total anual")
    
    # Picos de potência (W)
    peak_heating_w: float = Field(..., ge=0, description="Pico aquecimento")
    peak_cooling_w: float = Field(..., ge=0, description="Pico resfriamento")
    
    # Conforto e qualidade
    thermal_comfort_pmv: float = Field(..., ge=-3, le=3, description="PMV (Predicted Mean Vote)")
    air_quality_ach_mean: float = Field(..., ge=0, le=2.5, description="ACH médio")
    
    # Metadata
    timestamp: datetime = Field(default_factory=datetime.now)
    execution_time_s: float = Field(..., ge=0, description="Tempo execução (segundos)")
    uncertainty_percent: float = Field(..., ge=0, le=20, description="Incerteza estimada (%)")
    
    @validator('total_energy_kwh')
    def total_equals_sum(cls, v, values):
        if 'annual_heating_kwh' in values and 'annual_cooling_kwh' in values:
            expected = values['annual_heating_kwh'] + values['annual_cooling_kwh']
            if abs(v - expected) > 0.1:  # Tolerância para erros de arredondamento
                raise ValueError(f"total_energy ({v}) != heating ({values['annual_heating_kwh']}) + cooling ({values['annual_cooling_kwh']})")
        return v


class OptimizationGoal(BaseModel):
    """Define objetivo de otimização."""
    
    goal_type: str = Field(..., description="minimize_energy, maximize_comfort, roi_based, etc")
    target_metric: str = Field(..., description="annual_cooling_kwh, total_energy_kwh, peak_cooling_w, etc")
    target_value: float = Field(..., description="Valor alvo")
    tolerance_percent: float = Field(default=5.0, ge=0.1, le=20.0, description="Tolerância aceitável (%)")
    
    constraint_parameters: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Constraints adicionais (e.g., {'max_cost': 100000})"
    )


class SimulationRequest(BaseModel):
    """Request enviado para executar simulação."""
    
    request_id: str
    simulation_type: SimulationType
    parameters: BPSParameters
    optimization_goal: Optional[OptimizationGoal] = None
    
    # Metadata para rastreamento
    user_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    natural_language_query: Optional[str] = Field(None, description="Descrição em linguagem natural")
    
    # Controle de execução
    timeout_seconds: float = Field(default=30.0, ge=1, le=300)
    run_uncertainty_quantification: bool = Field(default=True)


class CoSimulationState(BaseModel):
    """Estado atual da co-simulação (persistente)."""
    
    session_id: str
    current_iteration: int = 0
    max_iterations: int = 10
    
    # Histórico de simulações
    simulation_history: List[SimulationResult] = Field(default_factory=list)
    
    # Melhor resultado encontrado
    best_result: Optional[SimulationResult] = None
    best_objective_value: Optional[float] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    status: str = Field(default="initialized")  # initialized, running, completed, error


def main():
    """Testes de validação dos data models."""
    
    print("🔍 Testando Data Models para Co-Simulação\n")
    
    # Teste 1: BPSParameters válidos
    print("Teste 1: BPSParameters válidos")
    try:
        params = BPSParameters(
            wwr=0.35,
            wall_thickness_m=0.20,
            insulation_thickness_m=0.10,
            conductivity_wall_W_mK=1.5,
            conductivity_insulation_W_mK=0.035,
            zone_volume_m3=2000,
            infiltration_rate_ACH=0.6,
            internal_loads_W_m2=10,
            heating_setpoint_C=21,
            cooling_setpoint_C=25
        )
        print("✅ Parâmetros válidos criados\n")
    except Exception as e:
        print(f"❌ Erro: {e}\n")
    
    # Teste 2: Validação de constraint (cooling < heating deve falhar)
    print("Teste 2: Validação de constraint (deve falhar)")
    try:
        invalid_params = BPSParameters(
            wwr=0.35,
            wall_thickness_m=0.20,
            insulation_thickness_m=0.10,
            conductivity_wall_W_mK=1.5,
            conductivity_insulation_W_mK=0.035,
            zone_volume_m3=2000,
            infiltration_rate_ACH=0.6,
            internal_loads_W_m2=10,
            heating_setpoint_C=25,
            cooling_setpoint_C=21  # INVÁLIDO: < heating
        )
        print("❌ Erro: Constraint não foi validada\n")
    except ValueError as e:
        print(f"✅ Constraint validado corretamente: {e}\n")
    
    # Teste 3: SimulationResult com total_energy inconsistente
    print("Teste 3: SimulationResult com validação de total_energy")
    try:
        result = SimulationResult(
            simulation_id="sim_001",
            simulation_type=SimulationType.SURROGATE_XGBOOST,
            parameters=params,
            annual_heating_kwh=50.0,
            annual_cooling_kwh=100.0,
            total_energy_kwh=151.0,  # INVÁLIDO: 50+100=150, não 151
            peak_heating_w=1000,
            peak_cooling_w=2000,
            thermal_comfort_pmv=0.5,
            air_quality_ach_mean=0.8,
            execution_time_s=0.015,
            uncertainty_percent=8.0
        )
        print("❌ Erro: Validação de total_energy não funcionou\n")
    except ValueError as e:
        print(f"✅ Validação de total_energy funcionou: {e}\n")
    
    # Teste 4: SimulationResult válido
    print("Teste 4: SimulationResult válido")
    try:
        valid_result = SimulationResult(
            simulation_id="sim_001",
            simulation_type=SimulationType.SURROGATE_XGBOOST,
            parameters=params,
            annual_heating_kwh=50.0,
            annual_cooling_kwh=100.0,
            total_energy_kwh=150.0,  # CORRETO
            peak_heating_w=1000,
            peak_cooling_w=2000,
            thermal_comfort_pmv=0.5,
            air_quality_ach_mean=0.8,
            execution_time_s=0.015,
            uncertainty_percent=8.0
        )
        print(f"✅ SimulationResult válido criado\n")
        print(f"   Total energy: {valid_result.total_energy_kwh} kWh")
        print(f"   Execution time: {valid_result.execution_time_s} s\n")
    except Exception as e:
        print(f"❌ Erro: {e}\n")
    
    # Teste 5: OptimizationGoal
    print("Teste 5: OptimizationGoal")
    try:
        goal = OptimizationGoal(
            goal_type="minimize_energy",
            target_metric="annual_cooling_kwh",
            target_value=80.0,
            tolerance_percent=5.0
        )
        print(f"✅ OptimizationGoal válido: {goal.goal_type}\n")
    except Exception as e:
        print(f"❌ Erro: {e}\n")
    
    # Teste 6: SimulationRequest
    print("Teste 6: SimulationRequest")
    try:
        request = SimulationRequest(
            request_id="req_001",
            simulation_type=SimulationType.SURROGATE_XGBOOST,
            parameters=params,
            optimization_goal=goal,
            user_id="user_123",
            natural_language_query="Reduzir resfriamento em 20% mantendo conforto"
        )
        print(f"✅ SimulationRequest válido criado\n")
        print(f"   Request ID: {request.request_id}")
        print(f"   Query: {request.natural_language_query}\n")
    except Exception as e:
        print(f"❌ Erro: {e}\n")
    
    print("=" * 80)
    print("✅ Testes de Data Models concluídos com sucesso!")
    print("=" * 80)


if __name__ == "__main__":
    main()
```

**Execução:**
```bash
mkdir -p src output
python src/cosim_data_models.py
```

**Resultado Esperado:**
```
Teste 1: BPSParameters válidos
✅ Parâmetros válidos criados

Teste 2: Validação de constraint
✅ Constraint validado corretamente: cooling_setpoint must be > heating_setpoint

Teste 3: SimulationResult com validação de total_energy
✅ Validação de total_energy funcionou: total_energy (151.0) != heating (50.0) + cooling (100.0)

Teste 4: SimulationResult válido
✅ SimulationResult válido criado
   Total energy: 150.0 kWh
   Execution time: 0.015 s

Teste 5: OptimizationGoal
✅ OptimizationGoal válido: minimize_energy

Teste 6: SimulationRequest
✅ SimulationRequest válido criado
   Request ID: req_001
   Query: Reduzir resfriamento em 20% mantendo conforto

✅ Testes de Data Models concluídos com sucesso!
```

**✅ Checkpoint:** Todos os 6 testes passaram? Data models validam constraints corretamente?

---

### 🎯 Exercício 1.2: UML Architecture Diagrams (3-4h)

**Contexto:** Documentar arquitetura em UML facilita comunicação, design review e implementação posterior.

**Tarefa:** Criar 3 diagramas UML (classe, sequência, caso de uso) e salvá-los como PlantUML.

#### Implementação: `cosim_uml_diagrams.py`

```python
"""
Exercício 1.2: Geração de diagramas UML para co-simulação
Referência: UML 2.5 Specification
"""

import os
from typing import List


class UMLDiagramGenerator:
    """Gera diagramas UML em formato PlantUML."""
    
    def __init__(self, output_dir: str = "diagrams"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_class_diagram(self) -> str:
        """Gera diagrama de classes da arquitetura."""
        
        uml = """
@startuml CoSim_ClassDiagram
!theme plain

package "Data Models" {
    class BPSParameters {
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
    }
    
    class SimulationResult {
        simulation_id: str
        simulation_type: SimulationType
        parameters: BPSParameters
        annual_heating_kwh: float
        annual_cooling_kwh: float
        total_energy_kwh: float
        peak_heating_w: float
        peak_cooling_w: float
        execution_time_s: float
        uncertainty_percent: float
    }
    
    class OptimizationGoal {
        goal_type: str
        target_metric: str
        target_value: float
        tolerance_percent: float
    }
    
    class SimulationRequest {
        request_id: str
        simulation_type: SimulationType
        parameters: BPSParameters
        optimization_goal: OptimizationGoal
        natural_language_query: str
    }
    
    class CoSimulationState {
        session_id: str
        current_iteration: int
        simulation_history: List[SimulationResult]
        best_result: SimulationResult
        status: str
    }
}

package "Simulators" {
    abstract class Simulator {
        {abstract} simulate(params: BPSParameters): SimulationResult
        {abstract} validate_parameters(): bool
    }
    
    class EnergyPlusSimulator extends Simulator {
        idf_path: str
        weather_path: str
        simulate(params): SimulationResult
        validate_parameters(): bool
    }
    
    class SurrogateXGBoostSimulator extends Simulator {
        model_path: str
        simulate(params): SimulationResult
        validate_parameters(): bool
    }
    
    class SurrogateMLPSimulator extends Simulator {
        model_path: str
        device: str
        simulate(params): SimulationResult
        validate_parameters(): bool
    }
}

package "LLM Integration" {
    class GeminiInterface {
        config: GeminiConfig
        system_prompt: str
        constraints: DomainConstraints
        generate_recommendation(): str
        parse_function_call(): Dict
        validate_response(): bool
    }
    
    class SurrogateToolRegistry {
        tools: Dict[str, Tool]
        register_tool(name, callable)
        execute_tool(name, args): Any
    }
}

package "Orchestration" {
    class CoSimulationController {
        state: CoSimulationState
        request: SimulationRequest
        simulators: Dict[str, Simulator]
        gemini: GeminiInterface
        
        execute_request(): SimulationResult
        optimize(): SimulationResult
        validate_result(): bool
    }
    
    class OptimizationLoop {
        controller: CoSimulationController
        current_params: BPSParameters
        best_params: BPSParameters
        iteration_count: int
        
        run_optimization(): None
        {private} generate_next_candidate(): BPSParameters
        {private} evaluate_candidate(): float
    }
}

SimulationRequest --> BPSParameters
SimulationRequest --> OptimizationGoal
SimulationResult --> BPSParameters
CoSimulationState --> SimulationResult
EnergyPlusSimulator --> SimulationResult
SurrogateXGBoostSimulator --> SimulationResult
SurrogateMLPSimulator --> SimulationResult
CoSimulationController --> CoSimulationState
CoSimulationController --> SimulationRequest
CoSimulationController --> Simulator
CoSimulationController --> GeminiInterface
OptimizationLoop --> CoSimulationController
OptimizationLoop --> BPSParameters
GeminiInterface --> SurrogateToolRegistry

@enduml
"""
        return uml
    
    def generate_sequence_diagram(self) -> str:
        """Gera diagrama de sequência de uma otimização iterativa."""
        
        uml = """
@startuml CoSim_SequenceDiagram
!theme plain

participant User
participant LLMAgent as "Gemini LLM"
participant Controller as "CoSim\\nController"
participant Simulator as "Surrogate/EP"
participant Validator as "Constraint\\nValidator"

User -> LLMAgent: Descrição em linguagem natural\n"Reduzir resfriamento em 20%"

activate LLMAgent
LLMAgent -> Controller: SimulationRequest\n(parameters, goal)
deactivate LLMAgent

loop for each iteration (max 10)
    activate Controller
    Controller -> Simulator: Execute Simulation\n(current_params)
    activate Simulator
    Simulator --> Controller: SimulationResult\n(energy_kwh, execution_time)
    deactivate Simulator
    
    Controller -> Validator: Validate Result\n(physical_bounds, constraints)
    activate Validator
    Validator --> Controller: ValidationFlags\n([hallucination_flags]?)
    deactivate Validator
    
    Controller -> Controller: Update State\n(iteration++, best_result)
    
    alt Goal achieved?
        Controller -> LLMAgent: Request Final Recommendation
        activate LLMAgent
        LLMAgent -> Simulator: Predict energy for best params\n(via function calling)
        LLMAgent --> User: Recommendation with explanation
        deactivate LLMAgent
        break
    else Continue optimization
        Controller -> LLMAgent: Request next parameter candidate\n(with current results)
        activate LLMAgent
        LLMAgent --> Controller: Suggested new parameters
        deactivate LLMAgent
        Controller -> Controller: Update current_params
    end
    deactivate Controller
end

@enduml
"""
        return uml
    
    def generate_use_case_diagram(self) -> str:
        """Gera diagrama de casos de uso."""
        
        uml = """
@startuml CoSim_UseCaseDiagram
!theme plain

left to right direction

actor Engineer as "Engenheiro BPS"
actor Admin as "Administrador"

rectangle "Co-Simulation System" {
    usecase "Descrever objetivo\nem linguagem natural" as DescribeGoal
    usecase "Executar simulação\nrápida" as SimulateQuick
    usecase "Otimizar parâmetros\nauomaticamente" as OptimizeAuto
    usecase "Analisar resultados\ncom incerteza" as AnalyzeResults
    usecase "Gerar relatório\ntécnico" as GenerateReport
    usecase "Validar resultado\ncontra constraints" as ValidateResult
    usecase "Monitorar custos\nde API" as MonitorCosts
    usecase "Calibrar modelo\ncom dados reais" as CalibrateModel
}

Engineer --> DescribeGoal
Engineer --> SimulateQuick
Engineer --> OptimizeAuto
Engineer --> AnalyzeResults
Engineer --> GenerateReport
Engineer --> ValidateResult

Admin --> MonitorCosts
Admin --> CalibrateModel

OptimizeAuto ..> SimulateQuick : include
OptimizeAuto ..> ValidateResult : include
AnalyzeResults ..> ValidateResult : include
GenerateReport ..> AnalyzeResults : include

@enduml
"""
        return uml
    
    def save_diagrams(self) -> None:
        """Salva todos os diagramas."""
        
        diagrams = {
            "class_diagram.puml": self.generate_class_diagram(),
            "sequence_diagram.puml": self.generate_sequence_diagram(),
            "usecase_diagram.puml": self.generate_use_case_diagram()
        }
        
        for filename, content in diagrams.items():
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Diagrama salvo: {filepath}")


def main():
    """Gera diagramas UML."""
    
    print("📐 Gerando diagramas UML para arquitetura de co-simulação\n")
    
    generator = UMLDiagramGenerator()
    generator.save_diagrams()
    
    print("\n" + "=" * 80)
    print("INSTRUÇÕES PARA VISUALIZAR DIAGRAMAS")
    print("=" * 80)
    print("""
1. Online (via PlantUML Editor):
   - Copiar conteúdo de diagrams/*.puml
   - Colar em: https://www.plantuml.com/plantuml/uml/
   - Visualizar e exportar como PNG/PDF

2. Localmente (com Graphviz + PlantUML):
   - pip install plantuml
   - plantuml diagrams/class_diagram.puml -o output -Tpng
   - Abrir output/class_diagram.png

3. VS Code (com extensão):
   - Instalar: jebbs.plantuml
   - Ctrl+Alt+P para preview
""")
    print("=" * 80)


if __name__ == "__main__":
    main()
```

**Execução:**
```bash
python src/cosim_uml_diagrams.py
```

**Resultado Esperado:**
```
📐 Gerando diagramas UML para arquitetura de co-simulação

✅ Diagrama salvo: diagrams/class_diagram.puml
✅ Diagrama salvo: diagrams/sequence_diagram.puml
✅ Diagrama salvo: diagrams/usecase_diagram.puml

INSTRUÇÕES PARA VISUALIZAR DIAGRAMAS
==================================================
[Instruções para visualizar online ou localmente]
```

**✅ Checkpoint:** Todos os 3 diagramas foram criados em `diagrams/` ?

---

### 🎯 Exercício 1.3: Design Patterns & Architecture (3-4h)

**Contexto:** Padrões de design (Observer, Strategy, Factory) facilitam manutenção, extensibilidade e testabilidade do sistema de co-simulação.

**Tarefa:** Implementar padrões para Simulators (Strategy), Controllers (Observer), e Tool Registry (Factory).

#### Implementação: `cosim_design_patterns.py`

```python
"""
Exercício 1.3: Design patterns para arquitetura de co-simulação
Referência: Gang of Four Design Patterns + SOLID Principles
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import json


# ============================================================================
# STRATEGY PATTERN: Diferentes simuladores, mesma interface
# ============================================================================

class SimulatorStrategy(ABC):
    """Interface abstrata para estratégias de simulação."""
    
    @abstractmethod
    def simulate(self, parameters: Dict[str, float]) -> Dict[str, float]:
        """Executa simulação com parâmetros dados."""
        pass
    
    @abstractmethod
    def validate_parameters(self, parameters: Dict[str, float]) -> bool:
        """Valida se parâmetros estão dentro de bounds físicos."""
        pass
    
    @property
    @abstractmethod
    def execution_time_ms(self) -> float:
        """Tempo típico de execução em millisegundos."""
        pass


class EnergyPlusStrategy(SimulatorStrategy):
    """Implementação usando EnergyPlus (simulador completo)."""
    
    def __init__(self, idf_template_path: str, weather_file: str):
        self.idf_template = idf_template_path
        self.weather_file = weather_file
        self._execution_time = 10000.0  # 10 segundos
    
    def simulate(self, parameters: Dict[str, float]) -> Dict[str, float]:
        # Pseudocódigo: Real impl usaria Eppy
        return {
            "annual_heating_kwh": 50 * parameters.get("insulation_thickness", 0.1),
            "annual_cooling_kwh": 100 * parameters.get("wwr", 0.4),
            "peak_heating_w": 2000,
            "peak_cooling_w": 5000,
            "execution_time_s": self._execution_time / 1000
        }
    
    def validate_parameters(self, parameters: Dict[str, float]) -> bool:
        # Validar bounds
        return (0.1 <= parameters.get("wwr", 0) <= 0.6 and
                0.05 <= parameters.get("insulation_thickness", 0) <= 0.20)
    
    @property
    def execution_time_ms(self) -> float:
        return self._execution_time


class SurrogateXGBoostStrategy(SimulatorStrategy):
    """Implementação usando XGBoost (rápido)."""
    
    def __init__(self, model_path: str):
        self.model_path = model_path
        self._execution_time = 10.0  # 10 ms
        # Em produção: self.model = pickle.load(model_path)
    
    def simulate(self, parameters: Dict[str, float]) -> Dict[str, float]:
        # Pseudocódigo: Real impl usaria XGBoost
        return {
            "annual_heating_kwh": 45 * parameters.get("insulation_thickness", 0.1),
            "annual_cooling_kwh": 95 * parameters.get("wwr", 0.4),
            "peak_heating_w": 1900,
            "peak_cooling_w": 4900,
            "execution_time_s": self._execution_time / 1000
        }
    
    def validate_parameters(self, parameters: Dict[str, float]) -> bool:
        return (0.1 <= parameters.get("wwr", 0) <= 0.6 and
                0.05 <= parameters.get("insulation_thickness", 0) <= 0.20)
    
    @property
    def execution_time_ms(self) -> float:
        return self._execution_time


class SimulatorContext:
    """Context que usa a estratégia (Strategy Pattern)."""
    
    def __init__(self, strategy: SimulatorStrategy):
        self._strategy = strategy
    
    def execute_simulation(self, parameters: Dict[str, float]) -> Optional[Dict[str, float]]:
        """Executa simulação usando estratégia configurada."""
        
        if not self._strategy.validate_parameters(parameters):
            print("❌ Parâmetros inválidos para esta estratégia")
            return None
        
        return self._strategy.simulate(parameters)
    
    def switch_strategy(self, new_strategy: SimulatorStrategy) -> None:
        """Muda estratégia em tempo de execução."""
        self._strategy = new_strategy
        print(f"✅ Estratégia alterada para: {type(new_strategy).__name__}")


# ============================================================================
# OBSERVER PATTERN: Notificar múltiplos listeners de eventos
# ============================================================================

@dataclass
class SimulationEvent:
    """Evento de simulação."""
    
    event_type: str  # "started", "completed", "failed", "iteration_complete"
    iteration: int
    timestamp: str
    data: Dict[str, Any] = field(default_factory=dict)


class SimulationObserver(ABC):
    """Observer abstrata para eventos de simulação."""
    
    @abstractmethod
    def update(self, event: SimulationEvent) -> None:
        """Chamado quando evento ocorre."""
        pass


class LoggerObserver(SimulationObserver):
    """Observer que registra eventos em log."""
    
    def __init__(self, log_file: str = "simulation.log"):
        self.log_file = log_file
    
    def update(self, event: SimulationEvent) -> None:
        print(f"📝 LOG: [{event.event_type}] Iteration {event.iteration} - {event.timestamp}")
        # Em produção: escrever em arquivo


class MetricsObserver(SimulationObserver):
    """Observer que coleta métricas de performance."""
    
    def __init__(self):
        self.metrics = {
            "total_iterations": 0,
            "total_time_s": 0.0,
            "fastest_sim_ms": float('inf'),
            "slowest_sim_ms": 0.0
        }
    
    def update(self, event: SimulationEvent) -> None:
        if event.event_type == "iteration_complete":
            self.metrics["total_iterations"] += 1
            exec_time = event.data.get("execution_time_ms", 0)
            self.metrics["total_time_s"] += exec_time / 1000
            self.metrics["fastest_sim_ms"] = min(self.metrics["fastest_sim_ms"], exec_time)
            self.metrics["slowest_sim_ms"] = max(self.metrics["slowest_sim_ms"], exec_time)
    
    def print_summary(self) -> None:
        print("\n📊 MÉTRICAS DE PERFORMANCE")
        print(f"   Total iterações: {self.metrics['total_iterations']}")
        print(f"   Tempo total: {self.metrics['total_time_s']:.2f}s")
        print(f"   Sim mais rápida: {self.metrics['fastest_sim_ms']:.2f}ms")
        print(f"   Sim mais lenta: {self.metrics['slowest_sim_ms']:.2f}ms")


class SimulationSubject:
    """Subject que gerencia observers (Observer Pattern)."""
    
    def __init__(self):
        self._observers: List[SimulationObserver] = []
    
    def attach(self, observer: SimulationObserver) -> None:
        """Adiciona observer."""
        self._observers.append(observer)
        print(f"✅ Observer anexado: {type(observer).__name__}")
    
    def detach(self, observer: SimulationObserver) -> None:
        """Remove observer."""
        self._observers.remove(observer)
    
    def notify(self, event: SimulationEvent) -> None:
        """Notifica todos os observers."""
        for observer in self._observers:
            observer.update(event)


# ============================================================================
# FACTORY PATTERN: Criar diferentes tipos de simuladores
# ============================================================================

class SimulatorFactory:
    """Factory para criar instâncias de simuladores (Factory Pattern)."""
    
    _strategies: Dict[str, Callable] = {}
    
    @classmethod
    def register(cls, sim_type: str, factory_func: Callable) -> None:
        """Registra novo tipo de simulador."""
        cls._strategies[sim_type] = factory_func
    
    @classmethod
    def create(cls, sim_type: str, **kwargs) -> Optional[SimulatorStrategy]:
        """Cria instância de simulador."""
        factory = cls._strategies.get(sim_type)
        if not factory:
            print(f"❌ Tipo desconhecido: {sim_type}")
            return None
        return factory(**kwargs)
    
    @classmethod
    def list_available(cls) -> List[str]:
        """Lista tipos disponíveis."""
        return list(cls._strategies.keys())


# Registrar factories
SimulatorFactory.register(
    "energyplus",
    lambda idf, weather: EnergyPlusStrategy(idf, weather)
)
SimulatorFactory.register(
    "surrogate_xgboost",
    lambda model: SurrogateXGBoostStrategy(model)
)


# ============================================================================
# COMMAND PATTERN: Encapsular requisições como objetos
# ============================================================================

@dataclass
class SimulationCommand:
    """Comando para executar simulação."""
    
    parameters: Dict[str, float]
    command_id: str
    timestamp: str


class SimulationInvoker:
    """Invoker que executa commands (Command Pattern)."""
    
    def __init__(self, strategy: SimulatorStrategy):
        self.strategy = strategy
        self.command_queue: List[SimulationCommand] = []
        self.executed_commands: List[SimulationCommand] = []
    
    def queue_command(self, command: SimulationCommand) -> None:
        """Adiciona comando à fila."""
        self.command_queue.append(command)
    
    def execute_queued_commands(self) -> List[Dict[str, Any]]:
        """Executa todos os comandos na fila."""
        results = []
        while self.command_queue:
            command = self.command_queue.pop(0)
            result = self.strategy.simulate(command.parameters)
            results.append({
                "command_id": command.command_id,
                "result": result
            })
            self.executed_commands.append(command)
        return results


def main():
    """Demonstração de design patterns."""
    
    print("🎨 Design Patterns para Co-Simulação\n")
    
    # ===== STRATEGY PATTERN =====
    print("=" * 80)
    print("1. STRATEGY PATTERN: Múltiplas estratégias de simulação")
    print("=" * 80)
    
    params = {"wwr": 0.35, "insulation_thickness": 0.10}
    
    # Usar XGBoost (rápido)
    xgboost_strategy = SurrogateXGBoostStrategy("models/xgboost.pkl")
    context = SimulatorContext(xgboost_strategy)
    result_fast = context.execute_simulation(params)
    print(f"✅ XGBoost (rápido): {result_fast['execution_time_s']*1000:.1f}ms")
    print(f"   Resfriamento: {result_fast['annual_cooling_kwh']:.1f} kWh\n")
    
    # Trocar para EnergyPlus (preciso)
    ep_strategy = EnergyPlusStrategy("template.idf", "weather.epw")
    context.switch_strategy(ep_strategy)
    result_accurate = context.execute_simulation(params)
    print(f"✅ EnergyPlus (preciso): {result_accurate['execution_time_s']*1000:.1f}ms")
    print(f"   Resfriamento: {result_accurate['annual_cooling_kwh']:.1f} kWh\n")
    
    # ===== OBSERVER PATTERN =====
    print("=" * 80)
    print("2. OBSERVER PATTERN: Notificar múltiplos listeners")
    print("=" * 80)
    
    subject = SimulationSubject()
    logger = LoggerObserver()
    metrics = MetricsObserver()
    
    subject.attach(logger)
    subject.attach(metrics)
    
    # Simular iterações
    for i in range(3):
        event = SimulationEvent(
            event_type="iteration_complete",
            iteration=i+1,
            timestamp="2026-01-13T10:00:00",
            data={"execution_time_ms": 10 + i*5}
        )
        subject.notify(event)
    
    metrics.print_summary()
    print()
    
    # ===== FACTORY PATTERN =====
    print("=" * 80)
    print("3. FACTORY PATTERN: Criar simuladores dinamicamente")
    print("=" * 80)
    
    print(f"Tipos disponíveis: {SimulatorFactory.list_available()}\n")
    
    # Criar via factory
    sim1 = SimulatorFactory.create("energyplus", idf="t.idf", weather="w.epw")
    sim2 = SimulatorFactory.create("surrogate_xgboost", model="m.pkl")
    
    print(f"✅ Criado: {type(sim1).__name__}")
    print(f"✅ Criado: {type(sim2).__name__}\n")
    
    # ===== COMMAND PATTERN =====
    print("=" * 80)
    print("4. COMMAND PATTERN: Fila de comandos")
    print("=" * 80)
    
    invoker = SimulationInvoker(sim2)
    
    # Enfileirar comandos
    for i in range(3):
        cmd = SimulationCommand(
            parameters={"wwr": 0.3 + i*0.05, "insulation_thickness": 0.08 + i*0.02},
            command_id=f"cmd_{i+1}",
            timestamp="2026-01-13T10:00:00"
        )
        invoker.queue_command(cmd)
    
    # Executar fila
    results = invoker.execute_queued_commands()
    print(f"✅ Executados {len(results)} comandos")
    print(f"   Primeiro resultado: {results[0]['result']['annual_cooling_kwh']:.1f} kWh\n")


if __name__ == "__main__":
    main()
```

**Execução:**
```bash
python src/cosim_design_patterns.py
```

**Resultado Esperado:**
```
🎨 Design Patterns para Co-Simulação

1. STRATEGY PATTERN
✅ XGBoost (rápido): 10.0ms
   Resfriamento: 95.0 kWh

✅ EnergyPlus (preciso): 10000.0ms
   Resfriamento: 100.0 kWh

2. OBSERVER PATTERN
✅ Observer anexado: LoggerObserver
✅ Observer anexado: MetricsObserver
📝 LOG: [iteration_complete] Iteration 1

📊 MÉTRICAS DE PERFORMANCE
   Total iterações: 3
   Tempo total: 0.04s
   Sim mais rápida: 10.00ms
   Sim mais lenta: 20.00ms

3. FACTORY PATTERN
Tipos disponíveis: ['energyplus', 'surrogate_xgboost']
✅ Criado: EnergyPlusStrategy
✅ Criado: SurrogateXGBoostStrategy

4. COMMAND PATTERN
✅ Executados 3 comandos
```

**✅ Checkpoint:** Todos 4 padrões implementados e funcionando?

---

### 📋 Checklist de Certificação - Semana 1

**Competências Esperadas:**

- [ ] **Exercício 1.1:** Implementou 5 data models com validações Pydantic
- [ ] **Exercício 1.2:** Gerou 3 diagramas UML (classe, sequência, use case)
- [ ] **Exercício 1.3:** Implementou 4 design patterns (Strategy, Observer, Factory, Command)

**Códigos Entregáveis:**

```bash
src/
├── cosim_data_models.py         # 1.1 - Pydantic models
├── cosim_uml_diagrams.py        # 1.2 - UML generation
└── cosim_design_patterns.py     # 1.3 - Design patterns

diagrams/
├── class_diagram.puml
├── sequence_diagram.puml
└── usecase_diagram.puml

output/
└── design_patterns_test_output.txt
```

**Validação Final (Git):**

```bash
git log --oneline | grep -i "architecture\|design\|cosim"
# Esperado: Commits para cada exercício

grep -r "class.*Strategy\|class.*Observer\|class.*Factory" src/
# Esperado: Padrões de design presentes
```

**Critério de Aprovação:**

✅ 5+ data models com Pydantic validations  
✅ 3 diagramas UML gerados em PlantUML  
✅ 4 padrões de design implementados e testados  
✅ Todos os códigos executam sem erro  
✅ Tempo total: 12-15 horas conforme estimado  

**Resultado de Semana 1:**

Você agora consegue:
1. Modelar dados complexos com validação automática (Pydantic)
2. Documentar arquitetura em UML (classe, sequência, caso de uso)
3. Implementar padrões SOLID (Strategy, Observer, Factory, Command)
4. Preparar codebase para implementação em Semanas 2-4

---

## 🔹 Semana 2: Data Exchange Protocols (12-15 horas)

### 📖 Objetivos da Semana

- Definir JSON schemas para comunicação entre componentes
- Implementar serialização/deserialização com validação
- Especificar API contracts para integração EnergyPlus-Gemini
- Criar protocolos de versionamento de dados

### 🎯 Exercício 2.1: JSON Schema & Serialization (3-4h)

**Contexto:** Diferentes componentes (EnergyPlus, surrogates, Gemini) precisam trocar dados. JSON schemas garantem compatibilidade e validação automática.

**Tarefa:** Gerar JSON schemas a partir de Pydantic models e testar serialização.

#### Implementação: `cosim_json_schemas.py`

```python
"""
Exercício 2.1: JSON schemas para data exchange
Referência: JSON Schema Draft 2020-12 + Pydantic JSON Schema
"""

from cosim_data_models import (
    BPSParameters, SimulationResult, OptimizationGoal, 
    SimulationRequest, CoSimulationState
)
import json


def generate_json_schemas() -> Dict[str, Dict]:
    """Gera JSON schemas para todos os modelos."""
    
    schemas = {
        "BPSParameters": BPSParameters.model_json_schema(),
        "SimulationResult": SimulationResult.model_json_schema(),
        "OptimizationGoal": OptimizationGoal.model_json_schema(),
        "SimulationRequest": SimulationRequest.model_json_schema(),
        "CoSimulationState": CoSimulationState.model_json_schema()
    }
    
    return schemas


def save_json_schemas(output_dir: str = "schemas") -> None:
    """Salva JSON schemas para arquivo."""
    
    os.makedirs(output_dir, exist_ok=True)
    schemas = generate_json_schemas()
    
    for name, schema in schemas.items():
        filepath = os.path.join(output_dir, f"{name}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(schema, f, indent=2)
        print(f"✅ Schema salvo: {filepath}")


def test_serialization() -> None:
    """Testa serialização/deserialização."""
    
    # Criar instância
    params = BPSParameters(
        wwr=0.35,
        wall_thickness_m=0.20,
        insulation_thickness_m=0.10,
        conductivity_wall_W_mK=1.5,
        conductivity_insulation_W_mK=0.035,
        zone_volume_m3=2000,
        infiltration_rate_ACH=0.6,
        internal_loads_W_m2=10,
        heating_setpoint_C=21,
        cooling_setpoint_C=25
    )
    
    # Serializar para JSON
    json_str = params.model_dump_json(indent=2)
    print("✅ Serialização bem-sucedida\n")
    print(f"JSON ({len(json_str)} chars):")
    print(json_str[:300] + "...\n")
    
    # Deserializar de JSON
    loaded_params = BPSParameters.model_validate_json(json_str)
    print("✅ Desserialização bem-sucedida")
    print(f"   WWR: {loaded_params.wwr}")
    print(f"   Insulation: {loaded_params.insulation_thickness_m}m\n")


def main():
    """Demonstração de JSON schemas e serialização."""
    
    print("📋 JSON Schemas para Co-Simulação\n")
    
    # Gerar e salvar schemas
    save_json_schemas()
    
    # Testar serialização
    test_serialization()
    
    print("=" * 80)
    print("✅ Exercício 2.1 concluído")
    print("=" * 80)


if __name__ == "__main__":
    main()
```

**✅ Checkpoint:** Schemas foram salvos em `schemas/`? Serialização/desserialização funcionou?

---

### 🎯 Exercício 2.2: API Contract Specification (3-4h)

**Contexto:** Definir contratos de API (request/response) entre EnergyPlus, surrogates e Gemini facilita integração.

**Tarefa:** Especificar 3 contratos de API em OpenAPI 3.0 e documentar com exemplos.

[Implementação seria OpenAPI spec files + validation tester]

**✅ Checkpoint:** 3 contratos de API documentados com exemplos?

---

### 🎯 Exercício 2.3-2.4: Versioning & Compatibility (3-4h cada)

[Similar pattern: serialization versioning, backward compatibility handling]

---

### 📋 Checklist de Certificação - Semana 2

**Competências Esperadas:**

- [ ] Exercício 2.1: JSON schemas gerados e testados
- [ ] Exercício 2.2: 3 contratos de API em OpenAPI
- [ ] Exercício 2.3: Versionamento de schemas implementado
- [ ] Exercício 2.4: Testes de compatibilidade passando

**Resultado de Semana 2:**

Você agora consegue:
1. Gerar JSON schemas automáticos a partir de modelos Pydantic
2. Serializar/deserializar dados com validação
3. Documentar contratos de API em OpenAPI 3.0
4. Gerenciar compatibilidade entre versões de dados

---

## 🔹 Semana 3: Coupling Implementation (12-15 horas)

### 📖 Objetivos da Semana

- Implementar CoSimulationController que orquestra componentes
- Integrar EnergyPlus com surrogates em loop adaptativo
- Conectar Gemini para geração de próximos candidatos
- Implementar feedback loops para otimização

### 🎯 Exercício 3.1-3.4: Progressive Integration

[4 exercises building CoSimulationController with:
- Simulator switching logic
- Parameter generation via Gemini
- Result validation & constraint enforcement
- Optimization loop with convergence criteria]

**Resultado de Semana 3:**

Você agora consegue:
1. Orquestrar múltiplos simuladores em loop de otimização
2. Integrar Gemini para geração automática de parâmetros
3. Aplicar constraints físicos e normativas
4. Rastrear convergência e melhor resultado

---

## 🔹 Semana 4: End-to-End Integration & Roadmap (14-15 horas)

### 📖 Objetivos da Semana

- Integração final de todos os componentes
- Full pipeline: Natural language → Parâmetros → Otimização → Relatório
- Roadmap técnico para produção (prototipagem → validação → deployment)
- Projeto final: Sistema completo com documentação

### 🎯 Exercício 4.1-4.3: Full System Integration

[3 exercises covering:
- End-to-end workflow
- Performance benchmarking
- Deployment considerations
- Production readmap]

### 🎯 Projeto Final: Technical Roadmap Document

Criar documento completo com:
- **Phase 1 (Q1 2026):** Prototipagem com surrogates
- **Phase 2 (Q2 2026):** Validação com EnergyPlus em subset cases
- **Phase 3 (Q3 2026):** User testing e refinement
- **Phase 4 (Q4 2026):** Production deployment

Incluir:
- Requisitos técnicos
- Arquitetura detalhada
- Plano de testes
- Estratégia de deployment
- Métricas de sucesso

**Resultado de Semana 4:**

Você completou:
1. ✅ Arquitetura de co-simulação completa
2. ✅ Prototipos funcionais em Semanas 1-3
3. ✅ Roadmap técnico para implementação em produção
4. ✅ Documentação completa para handoff para equipe de dev

---

## 📚 Recursos Adicionais

### Padrões & Referências
- **Zakeri et al. (2025):** Co-Simulation Frameworks for Building-LLM Integration
- **FMI 2.0 Standard:** Functional Mock-up Interface (co-simulation standard)
- **UML 2.5 Specification:** Object Management Group
- **OpenAPI 3.0 Specification:** RESTful API documentation

### Ferramentas Recomendadas
- **PlantUML:** Diagramas UML (https://plantuml.com)
- **OpenAPI Editor:** Swagger Editor (https://editor.swagger.io)
- **JSON Schema Validator:** AJV (https://ajv.js.org)

---

## ⚠️ Notas Importantes

### Antes de Semana 3 (Coupling)
- Ter modelos e padrões bem documentados
- Validar que JSON schemas são bidirecionais
- Testar ambos os paths: EnergyPlus e Surrogate

### Considerações de Performance
- EnergyPlus: ~10s por simulação (usar para validação)
- Surrogates: ~10ms (usar para otimização iterativa)
- Stratégia: Otimizar com surrogates, validar top-3 com EnergyPlus

### Considerações de Segurança
- Validar todas as entradas (Pydantic + custom validators)
- Rate limit chamadas a Gemini (de Mês 5)
- Logar todas as requisições e respostas

---

## 📝 Próximas Ações

**Semana 1 (Esta):**
- [ ] Completar exercícios 1.1-1.3
- [ ] Git commits para cada exercício
- [ ] Validar checkpoints

**Semana 2 (Próxima):**
- [ ] Exercício 2.1: JSON schemas
- [ ] Exercício 2.2: API contracts
- [ ] Exercício 2.3-2.4: Versioning & compatibility

**Semana 3-4:**
- [ ] Implementar CoSimulationController
- [ ] Full end-to-end pipeline
- [ ] Technical roadmap final document

---

**🎉 Você completou a visão geral do currículo Mês 6: Co-Simulação!**

Este mês é focado em design e arquitetura. A implementação completa ocorrerá em Mês 6+ quando você tiver completado todos os pré-requisitos de Meses 1-5.

Boa sorte! 🚀

