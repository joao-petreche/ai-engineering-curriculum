# **🏗️ Exercícios Práticos - Mês 1: Imersão no EnergyPlus & Automação**

**Objetivo do Mês:** Dominar EnergyPlus via automação Python, saindo da interface gráfica para controle programático completo.

**Estratégia:** "Domain-First" - Entender O QUE estamos simulando antes de aplicar IA.

**Tempo Estimado Total:** 40-50 horas (distribuído em 4 semanas)

**Pré-Requisitos:**
- ✅ Fase 0 concluída (infraestrutura validada)
- ✅ EnergyPlus 24.1.0 instalado e testado
- ✅ Python 3.10.x com bibliotecas (eppy, pandas, matplotlib)
- ✅ GitHub Copilot ativo

---

## **📋 Checklist de Progresso do Mês**

| Semana | Objetivo | Status | Tempo Estimado |
|--------|----------|--------|----------------|
| Semana 1 | Teoria EnergyPlus + Primeiros Scripts | ⬜ | 10-12h |
| Semana 2 | Manipulação de Geometria via Eppy | ⬜ | 10-12h |
| Semana 3 | Parametrização Avançada | ⬜ | 10-12h |
| Semana 4 | Projeto Final: Sistema Automatizado | ⬜ | 10-14h |

---

## **SEMANA 1: TEORIA ENERGYPLUS + PRIMEIROS SCRIPTS**

### **📌 Exercício 1.1 - Leitura Estruturada da Documentação**

**Objetivo:** Construir vocabulário técnico de BPS (Building Performance Simulation).

**Tarefa:**

1. **Leitura Obrigatória do EnergyPlus Input Output Reference**
   - [ ] Acessar [EnergyPlus Documentation](https://energyplus.net/documentation)
   - [ ] Baixar PDF: "Input Output Reference" (versão 24.1)
   - [ ] Ler e fazer anotações das seguintes seções:

**Seções Obrigatórias (2-3 horas de leitura):**

| Seção | Páginas Aprox. | Conceitos-Chave | Tempo |
|-------|----------------|-----------------|-------|
| **Building** | 50-100 | Coordenadas, geometria, norte | 30min |
| **Zone** | 150-200 | Volume térmico, multiplicadores | 30min |
| **BuildingSurface:Detailed** | 300-350 | Vértices, orientação, construção | 45min |
| **Material** | 400-450 | Condutividade, densidade, calor específico | 30min |
| **WindowMaterial** | 500-550 | Transmissão solar, U-value | 30min |

2. **Glossário Técnico**
   - [ ] Criar arquivo `glossario_bps.md` no repositório
   - [ ] Documentar pelo menos 20 termos técnicos com definições próprias

**Template do Glossário:**
```markdown
# Glossário BPS - Scientific AI Engineering

## Termos de Geometria
- **Zone (Zona Térmica)**: Volume de ar com temperatura uniforme...
- **Surface (Superfície)**: Elemento construtivo que delimita uma zona...

## Termos de Materiais
- **Thermal Conductivity (Condutividade Térmica)**: ...
- **U-Value (Coeficiente Global de Transferência de Calor)**: ...

## Termos de Simulação
- **Timestep**: Intervalo de tempo da simulação...
- **Design Day**: Dia típico usado para dimensionamento...
```

**✅ Checkpoint de Validação:**
- ✅ Glossário criado com mínimo de 20 termos
- ✅ Cada termo tem definição em português E termo em inglês
- ✅ Arquivo commitado no GitHub com commit: "Mês 1 - Glossário BPS"

**⏱️ Tempo Estimado:** 3-4 horas

---

### **📌 Exercício 1.2 - Primeira Simulação Manual via Interface**

**Objetivo:** Entender fluxo completo de simulação ANTES de automatizar.

**Tarefa:**

1. **Executar Simulação de Exemplo via EnergyPlus GUI**
   - [ ] Abrir EnergyPlus Launcher (EP-Launch)
   - [ ] Carregar arquivo: `C:\EnergyPlusV24-1-0\ExampleFiles\1ZoneUncontrolled.idf`
   - [ ] Selecionar weather file: `USA_CO_Golden-NREL.724666_TMY3.epw`
   - [ ] Executar simulação (Run)

2. **Análise dos Outputs**
   - [ ] Abrir arquivo `eplusout.csv` em Excel/VS Code
   - [ ] Identificar colunas de interesse:
     - ✅ `Zone Air Temperature`
     - ✅ `Zone Total Heating/Cooling Energy`
     - ✅ Timestamps

3. **Análise Visual no Jupyter Notebook**
   - [ ] Criar notebook `analise_primeira_simulacao.ipynb`

**Código do Notebook:**
```python
# Célula 1: Imports
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Configurar estilo
plt.style.use('seaborn-v0_8-darkgrid')

# Célula 2: Carregar dados
output_file = Path("C:/EnergyPlusV24-1-0/ExampleFiles-Run/eplusout.csv")

# Ler CSV (skiprows=1 para pular header do EnergyPlus)
df = pd.read_csv(output_file)

print(f"✅ Dados carregados: {len(df)} registros")
print(f"📊 Colunas: {df.columns.tolist()}")
df.head(10)

# Célula 3: Filtrar colunas de interesse
# Identificar nome exato das colunas de temperatura
temp_cols = [col for col in df.columns if 'Temperature' in col]
print(f"Colunas de temperatura encontradas: {temp_cols}")

# Selecionar primeira coluna de temperatura da zona
if temp_cols:
    temp_col = temp_cols[0]
    temps = df[temp_col]
    
    print(f"\n📈 Estatísticas de Temperatura:")
    print(f"Média: {temps.mean():.2f} °C")
    print(f"Mínima: {temps.min():.2f} °C")
    print(f"Máxima: {temps.max():.2f} °C")

# Célula 4: Visualização
fig, ax = plt.subplots(figsize=(14, 6))

# Plotar temperatura (primeiras 24 horas = 24*4 timesteps de 15min)
timesteps_dia = 24 * 4  # 96 timesteps (15min cada)
temps_dia = df[temp_col].iloc[:timesteps_dia]

ax.plot(temps_dia.values, linewidth=2, color='#FF6B6B')
ax.set_xlabel('Timestep (15 minutos)', fontsize=12)
ax.set_ylabel('Temperatura da Zona (°C)', fontsize=12)
ax.set_title('Temperatura da Zona - Primeiro Dia de Simulação', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Célula 5: Análise de Padrões
print("\n🔍 Análise de Padrões Térmicos:")
print(f"Amplitude térmica diária: {temps_dia.max() - temps_dia.min():.2f} °C")
print(f"Horário de temperatura máxima: Timestep {temps_dia.idxmax()}")
print(f"Horário de temperatura mínima: Timestep {temps_dia.idxmin()}")
```

**✅ Checkpoint de Validação:**
- ✅ Simulação executada com sucesso (eplusout.csv gerado)
- ✅ Notebook cria gráfico de temperatura das primeiras 24h
- ✅ Você consegue explicar: por que a temperatura varia ao longo do dia?
- ✅ Notebook commitado SEM outputs (Clear All Outputs antes de commit)

**⏱️ Tempo Estimado:** 2-3 horas

---

### **📌 Exercício 1.3 - Primeira Automação com Eppy**

**Objetivo:** Executar simulação via Python (sem abrir interface gráfica).

**Teoria - Biblioteca Eppy:**
- [Documentação Oficial](https://eppy.readthedocs.io/en/latest/)
- Permite ler, modificar e salvar arquivos .idf programaticamente

**Tarefa:**

1. **Instalar Eppy**
   ```powershell
   pip install eppy
   ```

2. **Criar Script `run_sim.py`**

**Código Inicial (Versão Básica):**
```python
"""
Script básico de automação EnergyPlus usando Eppy.
Mês 1 - Exercício 1.3
"""

from pathlib import Path
from eppy.modeleditor import IDF

# Configurações do EnergyPlus
ENERGYPLUS_DIR = Path("C:/EnergyPlusV24-1-0")
IDD_FILE = ENERGYPLUS_DIR / "Energy+.idd"
IDF.setiddname(str(IDD_FILE))

def run_simulation(idf_path, weather_path, output_dir):
    """
    Executa simulação EnergyPlus via Eppy.
    
    Args:
        idf_path: Caminho para arquivo .idf
        weather_path: Caminho para arquivo .epw
        output_dir: Diretório de saída
    """
    
    print(f"🔄 Iniciando simulação...")
    print(f"📄 Arquivo IDF: {idf_path}")
    print(f"🌦️  Weather: {weather_path}")
    
    # Criar diretório de saída
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Carregar arquivo IDF
    idf = IDF(str(idf_path), str(weather_path))
    
    # Executar simulação
    idf.run(output_directory=str(output_dir))
    
    print(f"✅ Simulação concluída!")
    print(f"📁 Outputs em: {output_dir}")
    
    # Verificar arquivo de saída
    csv_output = output_dir / "eplusout.csv"
    if csv_output.exists():
        print(f"✅ CSV gerado: {csv_output}")
    else:
        print(f"❌ CSV não encontrado!")
    
    return csv_output

if __name__ == "__main__":
    # Caminhos
    idf_file = ENERGYPLUS_DIR / "ExampleFiles/1ZoneUncontrolled.idf"
    weather_file = ENERGYPLUS_DIR / "WeatherData/USA_CO_Golden-NREL.724666_TMY3.epw"
    output_directory = Path("output/mes1_ex1_3")
    
    # Executar
    output_csv = run_simulation(idf_file, weather_file, output_directory)
    
    print("\n📊 Primeiras 5 linhas do resultado:")
    import pandas as pd
    df = pd.read_csv(output_csv)
    print(df.head())
```

3. **Executar Script**
   ```powershell
   python run_sim.py
   ```

**✅ Checkpoint de Validação:**
```powershell
# 1. Script executa sem erros
python run_sim.py

# 2. Verificar que arquivo CSV foi gerado
Test-Path "output/mes1_ex1_3/eplusout.csv"
# Resultado esperado: True

# 3. Verificar tamanho do arquivo (deve ser > 100 KB)
(Get-Item "output/mes1_ex1_3/eplusout.csv").Length / 1KB
# Resultado esperado: > 100
```

**Critério de Sucesso:**
- ✅ Script executa simulação SEM abrir interface gráfica
- ✅ CSV gerado em `output/mes1_ex1_3/`
- ✅ Mensagem "✅ Simulação concluída!" aparece no terminal
- ✅ Script commitado no GitHub

**⏱️ Tempo Estimado:** 2-3 horas

---

### **📌 Exercício 1.4 - Configuração do Gemini como Tutor**

**Objetivo:** Usar LLM como assistente para debugging de erros do EnergyPlus.

**Tarefa:**

1. **Configurar Gemini no VS Code**
   - [ ] Instalar extensão "Google Cloud Code" (já feito na Fase 0)
   - [ ] Autenticar com conta @gmail.com
   - [ ] Ativar Gemini Code Assist

2. **Criar Arquivo de Erro Intencional**
   - [ ] Copiar `1ZoneUncontrolled.idf` para `teste_erro.idf`
   - [ ] Modificar linha do material para criar erro proposital

**Exemplo de Erro Proposital:**
```idf
Material,
  Wall Material,           !- Name
  Rough,                   !- Roughness
  -0.05,                   !- Thickness {m} <-- ERRO: valor negativo!
  0.5,                     !- Conductivity {W/m-K}
  800,                     !- Density {kg/m3}
  1000;                    !- Specific Heat {J/kg-K}
```

3. **Executar Simulação e Capturar Erro**
   ```python
   # Adicionar ao run_sim.py
   try:
       idf.run(output_directory=str(output_dir))
   except Exception as e:
       print(f"❌ Erro durante simulação:")
       print(str(e))
       
       # Ler arquivo de erro do EnergyPlus
       err_file = output_dir / "eplusout.err"
       if err_file.exists():
           with open(err_file, 'r') as f:
               error_log = f.read()
               print("\n📋 Log de erro do EnergyPlus:")
               print(error_log[-500:])  # Últimas 500 chars
   ```

4. **Usar Gemini para Diagnosticar**
   - [ ] Copiar mensagem de erro
   - [ ] No VS Code, abrir Gemini Chat (Ctrl+Shift+I ou botão lateral)
   - [ ] Prompt para Gemini:

```
Contexto: Estou executando simulação EnergyPlus e recebi o seguinte erro:

[COLAR ERRO AQUI]

O arquivo IDF tem o seguinte material:
[COLAR TRECHO DO MATERIAL]

Pergunta:
1. Qual é a causa raiz deste erro?
2. Como corrigi-lo?
3. Quais são os limites físicos válidos para espessura de materiais?
```

5. **Documentar Aprendizado**
   - [ ] Criar arquivo `erros_comuns_energyplus.md`
   - [ ] Documentar pelo menos 3 erros comuns e suas soluções

**Template do Documento:**
```markdown
# Erros Comuns EnergyPlus - Diagnóstico e Soluções

## Erro 1: Material com Espessura Negativa

**Mensagem de Erro:**
```
** Severe  ** Material="WALL MATERIAL", Illegal value for thickness=-0.05
** Fatal   ** Errors occurred on processing input file. Preceding condition(s) cause termination.
```

**Causa Raiz:** 
Espessura de material não pode ser negativa (violação de lei física).

**Solução:**
Alterar valor para positivo (ex: 0.05 m) ou remover material se não for usado.

**Limites Físicos:**
- Mínimo: > 0 m (tipicamente ≥ 0.001 m para evitar problemas numéricos)
- Máximo: < 10 m (paredes muito grossas são raras)

**Diagnóstico via Gemini:**
[Colar resposta do Gemini aqui]
```

**✅ Checkpoint de Validação:**
- ✅ Gemini configurado e respondendo no VS Code
- ✅ Arquivo `erros_comuns_energyplus.md` criado com 3+ erros documentados
- ✅ Você consegue usar Gemini para diagnosticar erros do EnergyPlus
- ✅ Documento commitado no GitHub

**⏱️ Tempo Estimado:** 2-3 horas

---

## **SEMANA 2: MANIPULAÇÃO DE GEOMETRIA VIA EPPY**

### **📌 Exercício 2.1 - Leitura e Inspeção de Arquivo IDF**

**Objetivo:** Entender estrutura de arquivo .idf e navegar via Eppy.

**Tarefa:**

1. **Criar Script de Inspeção `inspect_idf.py`**

```python
"""
Script de inspeção de arquivos IDF usando Eppy.
Mês 1 - Exercício 2.1
"""

from pathlib import Path
from eppy.modeleditor import IDF
import json

# Configurações
ENERGYPLUS_DIR = Path("C:/EnergyPlusV24-1-0")
IDD_FILE = ENERGYPLUS_DIR / "Energy+.idd"
IDF.setiddname(str(IDD_FILE))

def inspect_idf(idf_path):
    """
    Inspeciona arquivo IDF e extrai informações estruturais.
    
    Args:
        idf_path: Caminho para arquivo .idf
    """
    
    print(f"🔍 Inspecionando: {idf_path}\n")
    
    # Carregar IDF
    idf = IDF(str(idf_path))
    
    # 1. Listar todos os tipos de objetos
    print("📋 Tipos de Objetos no IDF:")
    print("-" * 50)
    
    object_types = idf.idfobjects.keys()
    for obj_type in sorted(object_types):
        count = len(idf.idfobjects[obj_type])
        if count > 0:
            print(f"  {obj_type}: {count} objeto(s)")
    
    # 2. Inspecionar Building
    print("\n🏢 Informações do Building:")
    print("-" * 50)
    buildings = idf.idfobjects['BUILDING']
    if buildings:
        building = buildings[0]
        print(f"  Nome: {building.Name}")
        print(f"  Norte: {building.North_Axis}°")
        print(f"  Terreno: {building.Terrain}")
    
    # 3. Inspecionar Zones
    print("\n🏠 Zonas Térmicas:")
    print("-" * 50)
    zones = idf.idfobjects['ZONE']
    for zone in zones:
        print(f"  • {zone.Name}")
        print(f"    Multiplicador: {zone.Multiplier}")
        print(f"    Coordenadas: X={zone.X_Origin}, Y={zone.Y_Origin}, Z={zone.Z_Origin}")
    
    # 4. Inspecionar Materiais
    print("\n🧱 Materiais:")
    print("-" * 50)
    materials = idf.idfobjects['MATERIAL']
    for mat in materials:
        print(f"  • {mat.Name}")
        print(f"    Espessura: {mat.Thickness} m")
        print(f"    Condutividade: {mat.Conductivity} W/m-K")
        print(f"    Densidade: {mat.Density} kg/m³")
    
    # 5. Inspecionar Superfícies (BuildingSurface:Detailed)
    print("\n🔲 Superfícies:")
    print("-" * 50)
    surfaces = idf.idfobjects['BUILDINGSURFACE:DETAILED']
    
    surface_types = {}
    for surf in surfaces:
        surf_type = surf.Surface_Type
        surface_types[surf_type] = surface_types.get(surf_type, 0) + 1
    
    for surf_type, count in surface_types.items():
        print(f"  {surf_type}: {count}")
    
    # 6. Exportar estrutura para JSON
    structure = {
        "building": building.Name if buildings else None,
        "zones": [z.Name for z in zones],
        "materials": [m.Name for m in materials],
        "surface_counts": surface_types
    }
    
    output_json = Path("output/idf_structure.json")
    output_json.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(structure, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Estrutura exportada para: {output_json}")

if __name__ == "__main__":
    idf_file = ENERGYPLUS_DIR / "ExampleFiles/1ZoneUncontrolled.idf"
    inspect_idf(idf_file)
```

2. **Executar e Analisar**
   ```powershell
   python inspect_idf.py
   ```

3. **Documentar Estrutura**
   - [ ] Criar arquivo `estrutura_idf.md`
   - [ ] Desenhar diagrama hierárquico da estrutura IDF

**Template do Documento:**
```markdown
# Estrutura de Arquivo IDF - EnergyPlus

## Hierarquia de Objetos

```
IDF File
├── Building (1)
│   ├── Nome
│   ├── Norte (orientação)
│   └── Terreno
├── Zones (N)
│   ├── Nome da zona
│   ├── Coordenadas (X, Y, Z)
│   └── Multiplicador
├── Materials (N)
│   ├── Nome do material
│   ├── Propriedades térmicas
│   └── Propriedades físicas
├── Constructions (N)
│   └── Camadas de materiais
└── BuildingSurface:Detailed (N)
    ├── Tipo (Wall, Floor, Roof, etc.)
    ├── Zona associada
    ├── Construção
    └── Vértices (geometria)
```

## Objetos Inspecionados - 1ZoneUncontrolled.idf

**Building:** 
- Nome: [DOCUMENTAR AQUI]
- Norte: [DOCUMENTAR]

**Zones:** [LISTAR]

**Materials:** [LISTAR COM PROPRIEDADES]

**Superfícies:**
- Paredes: X
- Pisos: Y
- Tetos: Z
- Janelas: W
```

**✅ Checkpoint de Validação:**
- ✅ Script executa e lista todos os objetos do IDF
- ✅ JSON exportado em `output/idf_structure.json`
- ✅ Documento `estrutura_idf.md` criado com hierarquia
- ✅ Você entende a relação: Material → Construction → Surface → Zone

**⏱️ Tempo Estimado:** 3-4 horas

---

### **📌 Exercício 2.2 - Modificação de Window-to-Wall Ratio (WWR)**

**Objetivo:** Alterar geometria de janelas programaticamente (exercício central do Mês 1).

**Conceito - Window-to-Wall Ratio (WWR):**
- **Definição:** Proporção da área de janelas em relação à área de parede
- **Fórmula:** WWR = (Área de Janelas) / (Área de Parede)
- **Exemplo:** WWR = 0.3 significa 30% da parede é vidro

**Tarefa:**

1. **Criar Script `modify_wwr.py`**

```python
"""
Modificação de Window-to-Wall Ratio usando Eppy.
Mês 1 - Exercício 2.2 - DESAFIO PRINCIPAL
"""

from pathlib import Path
from eppy.modeleditor import IDF
import shutil

# Configurações
ENERGYPLUS_DIR = Path("C:/EnergyPlusV24-1-0")
IDD_FILE = ENERGYPLUS_DIR / "Energy+.idd"
IDF.setiddname(str(IDD_FILE))

def calculate_surface_area(surface):
    """
    Calcula área de uma superfície a partir de seus vértices.
    
    Args:
        surface: Objeto BuildingSurface:Detailed do Eppy
        
    Returns:
        float: Área em m²
    """
    # Obter vértices
    vertices = []
    for i in range(1, 100):  # Máximo de vértices
        try:
            x = getattr(surface, f'Vertex_{i}_Xcoordinate')
            y = getattr(surface, f'Vertex_{i}_Ycoordinate')
            z = getattr(surface, f'Vertex_{i}_Zcoordinate')
            
            if x is not None:
                vertices.append((float(x), float(y), float(z)))
            else:
                break
        except AttributeError:
            break
    
    # Cálculo simplificado para retângulos (assumindo 4 vértices)
    if len(vertices) == 4:
        # Distância entre vértice 0 e 1
        width = ((vertices[1][0] - vertices[0][0])**2 + 
                 (vertices[1][1] - vertices[0][1])**2 + 
                 (vertices[1][2] - vertices[0][2])**2)**0.5
        
        # Distância entre vértice 1 e 2
        height = ((vertices[2][0] - vertices[1][0])**2 + 
                  (vertices[2][1] - vertices[1][1])**2 + 
                  (vertices[2][2] - vertices[1][2])**2)**0.5
        
        return width * height
    
    return 0.0

def modify_wwr(idf_path, output_path, target_wwr=0.3):
    """
    Modifica WWR de todas as paredes externas.
    
    Args:
        idf_path: Caminho do IDF original
        output_path: Caminho do IDF modificado
        target_wwr: WWR desejado (0.0 a 0.9)
    """
    
    print(f"🔄 Modificando WWR para {target_wwr:.1%}")
    print(f"📄 Input: {idf_path}")
    print(f"💾 Output: {output_path}\n")
    
    # Carregar IDF
    idf = IDF(str(idf_path))
    
    # Obter todas as paredes externas
    walls = [s for s in idf.idfobjects['BUILDINGSURFACE:DETAILED'] 
             if s.Surface_Type == 'Wall' and s.Outside_Boundary_Condition == 'Outdoors']
    
    print(f"🔲 Paredes externas encontradas: {len(walls)}")
    
    # Processar cada parede
    for idx, wall in enumerate(walls):
        wall_area = calculate_surface_area(wall)
        print(f"\n  Parede {idx+1}: {wall.Name}")
        print(f"    Área: {wall_area:.2f} m²")
        
        # Calcular área de janela necessária
        window_area_target = wall_area * target_wwr
        print(f"    Janela desejada: {window_area_target:.2f} m² ({target_wwr:.1%})")
        
        # Verificar se já existe janela nesta parede
        existing_windows = [w for w in idf.idfobjects['FENESTRATIONSURFACE:DETAILED']
                           if w.Building_Surface_Name == wall.Name]
        
        if existing_windows:
            # Modificar janela existente
            window = existing_windows[0]
            print(f"    ✏️  Modificando janela existente: {window.Name}")
            
            # Recalcular vértices da janela (simplificado para retângulo central)
            # ... (implementar lógica de redimensionamento)
        else:
            # Criar nova janela
            print(f"    ➕ Criando nova janela...")
            # ... (implementar criação de janela)
    
    # Salvar IDF modificado
    idf.saveas(str(output_path))
    print(f"\n✅ IDF modificado salvo em: {output_path}")

if __name__ == "__main__":
    # Caminhos
    original_idf = ENERGYPLUS_DIR / "ExampleFiles/1ZoneUncontrolled.idf"
    modified_idf = Path("output/mes1_ex2_2/1Zone_WWR30.idf")
    modified_idf.parent.mkdir(parents=True, exist_ok=True)
    
    # Modificar WWR para 30%
    modify_wwr(original_idf, modified_idf, target_wwr=0.3)
    
    print("\n📊 Próximo passo: Executar simulação com novo IDF")
```

**⚠️ NOTA:** Este script é um TEMPLATE. A implementação completa do cálculo de vértices de janelas é complexa e será refinada durante o mês.

2. **Executar e Testar**
   ```powershell
   python modify_wwr.py
   ```

**✅ Checkpoint de Validação:**
- ✅ Script identifica paredes externas corretamente
- ✅ Calcula área de cada parede
- ✅ IDF modificado é salvo (mesmo que janelas ainda não sejam criadas perfeitamente)
- ✅ Você entende a lógica: área_janela = área_parede × WWR

**⏱️ Tempo Estimado:** 4-5 horas (exercício mais complexo)

---

## **SEMANA 3: PARAMETRIZAÇÃO AVANÇADA**

### **📌 Exercício 3.1 - Estudo Paramétrico Automatizado**

**Objetivo:** Executar múltiplas simulações variando parâmetros (WWR, espessura de isolamento).

**Tarefa:**

1. **Criar Script `parametric_study.py`**

```python
"""
Estudo paramétrico automatizado.
Mês 1 - Exercício 3.1
"""

from pathlib import Path
from eppy.modeleditor import IDF
import pandas as pd
import matplotlib.pyplot as plt

# Configurações
ENERGYPLUS_DIR = Path("C:/EnergyPlusV24-1-0")
IDD_FILE = ENERGYPLUS_DIR / "Energy+.idd"
IDF.setiddname(str(IDD_FILE))

def run_parametric_study(base_idf, weather_file, param_ranges):
    """
    Executa estudo paramétrico variando WWR.
    
    Args:
        base_idf: IDF base
        weather_file: Arquivo climático
        param_ranges: Dict com parâmetros e valores (ex: {'WWR': [0.1, 0.3, 0.5, 0.7]})
    
    Returns:
        DataFrame com resultados
    """
    
    results = []
    
    # Iterar sobre valores de WWR
    for wwr in param_ranges['WWR']:
        print(f"\n{'='*60}")
        print(f"🔄 Simulando WWR = {wwr:.1%}")
        print(f"{'='*60}")
        
        # Modificar IDF (usar função do exercício 2.2)
        modified_idf_path = Path(f"output/parametric/wwr_{int(wwr*100)}.idf")
        modified_idf_path.parent.mkdir(parents=True, exist_ok=True)
        
        # TODO: Chamar função modify_wwr() aqui
        
        # Executar simulação
        idf = IDF(str(modified_idf_path), str(weather_file))
        output_dir = Path(f"output/parametric/run_wwr_{int(wwr*100)}")
        idf.run(output_directory=str(output_dir))
        
        # Extrair resultados
        csv_path = output_dir / "eplusout.csv"
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            
            # Calcular consumo anual (simplificado)
            # TODO: Identificar colunas corretas de energia
            
            results.append({
                'WWR': wwr,
                'Annual_Heating_kWh': 0,  # TODO: calcular
                'Annual_Cooling_kWh': 0,  # TODO: calcular
                'Total_Energy_kWh': 0     # TODO: calcular
            })
            
            print(f"✅ Simulação concluída")
        else:
            print(f"❌ CSV não gerado")
    
    return pd.DataFrame(results)

if __name__ == "__main__":
    base_idf = ENERGYPLUS_DIR / "ExampleFiles/1ZoneUncontrolled.idf"
    weather = ENERGYPLUS_DIR / "WeatherData/USA_CO_Golden-NREL.724666_TMY3.epw"
    
    # Definir ranges de parâmetros
    params = {
        'WWR': [0.1, 0.2, 0.3, 0.4, 0.5]
    }
    
    # Executar estudo
    results = run_parametric_study(base_idf, weather, params)
    
    # Salvar resultados
    results.to_csv("output/parametric/results.csv", index=False)
    print(f"\n✅ Resultados salvos em output/parametric/results.csv")
    
    # Plotar
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(results['WWR']*100, results['Total_Energy_kWh'], marker='o', linewidth=2)
    ax.set_xlabel('Window-to-Wall Ratio (%)', fontsize=12)
    ax.set_ylabel('Consumo Energético Anual (kWh)', fontsize=12)
    ax.set_title('Impacto do WWR no Consumo Energético', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("output/parametric/wwr_impact.png", dpi=300)
    print(f"✅ Gráfico salvo em output/parametric/wwr_impact.png")
```

**✅ Checkpoint de Validação:**
- ✅ Script executa 5 simulações (WWR = 10%, 20%, 30%, 40%, 50%)
- ✅ CSV com resultados gerado
- ✅ Gráfico mostra relação entre WWR e consumo energético
- ✅ Você entende: por que WWR maior aumenta/diminui consumo?

**⏱️ Tempo Estimado:** 5-6 horas

---

## **SEMANA 4: PROJETO FINAL DO MÊS**

### **📌 Exercício 4.1 - Sistema Automatizado Completo**

**Objetivo:** Criar sistema modular que aceita configurações via JSON e executa simulações.

**Especificações do Entregável:**

**Estrutura de Arquivos:**
```
mes1_projeto_final/
├── config/
│   └── simulation_config.json
├── src/
│   ├── __init__.py
│   ├── idf_modifier.py
│   ├── simulation_runner.py
│   └── results_analyzer.py
├── tests/
│   └── test_idf_modifier.py
├── output/
│   └── (gerado automaticamente)
├── run_simulation.py (script principal)
└── README.md
```

**1. Arquivo de Configuração (config/simulation_config.json):**
```json
{
  "project_name": "Mes1_Final_WWR_Study",
  "base_idf": "C:/EnergyPlusV24-1-0/ExampleFiles/1ZoneUncontrolled.idf",
  "weather_file": "C:/EnergyPlusV24-1-0/WeatherData/USA_CO_Golden-NREL.724666_TMY3.epw",
  "parameters": {
    "wwr_values": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
    "insulation_thickness_m": [0.05, 0.10, 0.15]
  },
  "output_dir": "output/mes1_final",
  "analysis": {
    "metrics": ["annual_heating_kwh", "annual_cooling_kwh", "peak_heating_w", "peak_cooling_w"],
    "generate_plots": true
  }
}
```

**2. Módulo Principal (src/simulation_runner.py):**
```python
"""
Módulo principal de execução de simulações.
"""

from pathlib import Path
from eppy.modeleditor import IDF
import json
import pandas as pd

class SimulationRunner:
    """Classe para gerenciar execução de simulações EnergyPlus."""
    
    def __init__(self, config_path):
        """
        Inicializa runner com arquivo de configuração.
        
        Args:
            config_path: Path para JSON de configuração
        """
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Configurar Eppy
        ep_dir = Path("C:/EnergyPlusV24-1-0")
        idd_file = ep_dir / "Energy+.idd"
        IDF.setiddname(str(idd_file))
        
        self.results = []
    
    def run_all(self):
        """Executa todas as simulações configuradas."""
        
        print(f"🚀 Iniciando projeto: {self.config['project_name']}")
        print(f"📊 Total de simulações: {self._count_simulations()}")
        
        # Iterar sobre parâmetros
        for wwr in self.config['parameters']['wwr_values']:
            for insulation in self.config['parameters']['insulation_thickness_m']:
                self._run_single_simulation(wwr, insulation)
        
        # Salvar resultados
        self._save_results()
        
        # Gerar análises
        if self.config['analysis']['generate_plots']:
            self._generate_plots()
        
        print("\n✅ Todas as simulações concluídas!")
    
    def _count_simulations(self):
        """Conta número total de simulações."""
        wwr_count = len(self.config['parameters']['wwr_values'])
        ins_count = len(self.config['parameters']['insulation_thickness_m'])
        return wwr_count * ins_count
    
    def _run_single_simulation(self, wwr, insulation):
        """Executa uma simulação individual."""
        
        print(f"\n{'='*60}")
        print(f"🔄 WWR={wwr:.1%}, Isolamento={insulation}m")
        print(f"{'='*60}")
        
        # TODO: Implementar lógica completa
        # 1. Modificar IDF (WWR + isolamento)
        # 2. Executar simulação
        # 3. Extrair métricas
        # 4. Armazenar resultados
        
        pass
    
    def _save_results(self):
        """Salva resultados em CSV."""
        df = pd.DataFrame(self.results)
        output_path = Path(self.config['output_dir']) / "results.csv"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"💾 Resultados salvos em: {output_path}")
    
    def _generate_plots(self):
        """Gera gráficos de análise."""
        # TODO: Implementar visualizações
        pass
```

**3. Script Principal (run_simulation.py):**
```python
"""
Script principal do projeto final - Mês 1.
"""

from pathlib import Path
from src.simulation_runner import SimulationRunner

def main():
    """Função principal."""
    
    print("=" * 70)
    print("🎓 MÊS 1 - PROJETO FINAL: Sistema Automatizado EnergyPlus")
    print("=" * 70)
    
    # Carregar configuração
    config_path = Path("config/simulation_config.json")
    
    # Criar runner
    runner = SimulationRunner(config_path)
    
    # Executar todas as simulações
    runner.run_all()
    
    print("\n🎉 Projeto concluído com sucesso!")
    print("📂 Verifique a pasta output/mes1_final/ para resultados")

if __name__ == "__main__":
    main()
```

**✅ Checkpoint de Validação Final:**

| Critério | Status | Peso |
|----------|--------|------|
| Sistema aceita configuração via JSON | ⬜ | 15% |
| Modifica WWR corretamente | ⬜ | 20% |
| Modifica espessura de isolamento | ⬜ | 20% |
| Executa múltiplas simulações automaticamente | ⬜ | 15% |
| Extrai métricas corretas (heating/cooling) | ⬜ | 15% |
| Gera CSV com resultados | ⬜ | 5% |
| Gera gráficos de análise | ⬜ | 10% |

**Critérios de Sucesso (Mínimo 80%):**
- ✅ Sistema executa pelo menos 6 simulações (6 valores de WWR)
- ✅ Resultados são consistentes (consumo aumenta/diminui logicamente)
- ✅ Código está documentado (docstrings em todas as funções)
- ✅ README.md explica como usar o sistema
- ✅ Código commitado no GitHub com estrutura modular

**⏱️ Tempo Estimado:** 10-14 horas

---

## **📚 ENTREGÁVEL FINAL DO MÊS 1**

### **Repositório GitHub deve conter:**

```
piml-training/
├── mes1_imersao_energyplus/
│   ├── config/
│   │   └── simulation_config.json
│   ├── src/
│   │   ├── __init__.py
│   │   ├── idf_modifier.py
│   │   ├── simulation_runner.py
│   │   └── results_analyzer.py
│   ├── output/
│   │   └── (excluído do git via .gitignore)
│   ├── docs/
│   │   ├── glossario_bps.md
│   │   ├── estrutura_idf.md
│   │   └── erros_comuns_energyplus.md
│   ├── run_simulation.py
│   └── README.md
└── notebooks/
    ├── analise_primeira_simulacao.ipynb
    └── analise_resultados_finais.ipynb
```

### **README.md do Projeto Final:**

```markdown
# Mês 1 - Imersão no EnergyPlus & Automação

## Objetivo
Sistema automatizado para execução de estudos paramétricos no EnergyPlus via Python.

## Funcionalidades
- ✅ Modificação de Window-to-Wall Ratio (WWR)
- ✅ Modificação de espessura de isolamento
- ✅ Execução automatizada de múltiplas simulações
- ✅ Extração de métricas energéticas
- ✅ Geração de gráficos de análise

## Como Usar

1. **Configurar simulação:**
   Editar `config/simulation_config.json` com parâmetros desejados.

2. **Executar:**
   ```bash
   python run_simulation.py
   ```

3. **Analisar resultados:**
   Verificar `output/mes1_final/results.csv` e gráficos.

## Estrutura de Código

- `src/idf_modifier.py`: Funções para modificar arquivos IDF
- `src/simulation_runner.py`: Classe principal de execução
- `src/results_analyzer.py`: Análise e visualização de resultados

## Métricas Calculadas

- Consumo anual de aquecimento (kWh)
- Consumo anual de resfriamento (kWh)
- Pico de demanda de aquecimento (W)
- Pico de demanda de resfriamento (W)

## Lições Aprendidas

[Documentar principais aprendizados do mês aqui]

## Próximos Passos (Mês 2)

- Integração com Pydantic para validação de dados
- Implementação de GuardrailValidator
- JSON-Python workflows
```

---

## **✅ CERTIFICAÇÃO DE CONCLUSÃO DO MÊS 1**

**Checklist Final:**

### **Conhecimentos Teóricos**
- [ ] Entendo estrutura de arquivos .idf (Building, Zone, Surface, Material)
- [ ] Sei calcular Window-to-Wall Ratio (WWR)
- [ ] Entendo relação entre WWR e consumo energético
- [ ] Conheço principais erros do EnergyPlus e como diagnosticar

### **Habilidades Práticas**
- [ ] Executo simulações EnergyPlus via Python (sem GUI)
- [ ] Modifico geometria de edifícios via Eppy
- [ ] Crio estudos paramétricos automatizados
- [ ] Extraio e analiso resultados de simulação
- [ ] Uso Gemini/Copilot para debugging

### **Entregáveis**
- [ ] Glossário BPS (20+ termos)
- [ ] Script de inspeção de IDF
- [ ] Sistema automatizado funcional
- [ ] 3+ notebooks de análise
- [ ] Documentação completa no README.md

### **DevOps**
- [ ] Código organizado em módulos
- [ ] Git commits regulares (mínimo 10 commits no mês)
- [ ] .gitignore configurado (output/ excluído)
- [ ] Notebooks commitados SEM outputs

---

## **🎯 Próximo Mês: Engenharia de Software Científica**

Após concluir o Mês 1, você estará pronto para:
- Implementar validação rigorosa de dados com Pydantic
- Criar biblioteca GuardrailValidator
- Trabalhar com JSON-Python workflows
- Aplicar rigor de engenharia de software a código científico

**Próximo arquivo:** `Exercicios_Mes_2_Engenharia_Software.md`

---

**📊 Tempo Total Investido no Mês 1:** 40-50 horas
**🎓 Nível de Dificuldade:** ⭐⭐⭐ (3/5)
**🔧 Complexidade Técnica:** Média-Alta
