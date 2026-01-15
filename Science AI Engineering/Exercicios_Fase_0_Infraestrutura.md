# **🛠️ Exercícios Práticos - Fase 0: Infraestrutura e Setup Zero**

**Objetivo:** Validar cada componente da infraestrutura com exercícios práticos antes de iniciar o Mês 1.

**Status Obrigatório:** ✅ Todos os checkpoints devem ser marcados como concluídos antes de avançar para a Fase 1.

**Tempo Estimado:** 8-12 horas (distribuído em 3-4 dias)

---

## **📋 Checklist Geral de Progresso**

| Seção | Status | Tempo Estimado | Prioridade |
|-------|--------|----------------|------------|
| 0.1 Ativação de Benefícios | ⬜ | 2-3h | 🔴 CRÍTICA |
| 0.2 Bancada Digital | ⬜ | 3-4h | 🔴 CRÍTICA |
| 0.3 Engenharia de Software | ⬜ | 2-3h | 🔴 CRÍTICA |
| 0.4 Teste de Proficiência Final | ⬜ | 1-2h | 🔴 CRÍTICA |

---

## **0.1. ATIVAÇÃO DE BENEFÍCIOS (Otimização de Custos)**

### **📌 Exercício 0.1.A - GitHub Education Pack**

**Objetivo:** Ativar GitHub Copilot gratuitamente via conta institucional USP.

**Passo-a-Passo:**

1. **Criação da Conta GitHub Institucional**
   - [ ] Acessar [github.com/education](https://github.com/education)
   - [ ] Clicar em "Sign up for GitHub" usando e-mail @usp.br
   - [ ] Verificar e-mail institucional (checar spam se necessário)

2. **Aplicação para Student/Teacher Benefits**
   - [ ] No painel GitHub, ir em **Settings → Billing and licensing → Education benefits**
   - [ ] Clicar em "Start an application" (Student ou Teacher)
   - [ ] Fazer upload de documento comprobatório:
     - ✅ Carteirinha digital USP (frente/verso)
     - ✅ OU Declaração de matrícula recente
   - [ ] Aguardar aprovação (geralmente 24-48h)

3. **Ativação do GitHub Copilot**
   - [ ] Após aprovação, acessar [github.com/copilot](https://github.com/copilot)
   - [ ] Verificar que o plano está como "Free for Students"
   - [ ] Clicar em "Get access to GitHub Copilot"

**✅ Checkpoint de Validação:**
```bash
# No VS Code, após instalar extensão GitHub Copilot:
# 1. Abrir arquivo .py qualquer
# 2. Digitar comentário: "# função para calcular média de uma lista"
# 3. Pressionar Enter
# 4. O Copilot deve sugerir código automaticamente em cinza
```

**Critério de Sucesso:**
- ✅ Badge "Student Developer Pack" visível no perfil GitHub
- ✅ Copilot funcionando no VS Code (sugestões em cinza)
- ✅ Sem cobranças no GitHub billing

**⏱️ Tempo Estimado:** 30-60 minutos (+ 24-48h para aprovação)

---

### **📌 Exercício 0.1.B - Google Cloud Platform (Conta Pessoal)**

**Objetivo:** Configurar GCP com Free Tier e trava de segurança financeira.

**⚠️ REGRA CRÍTICA:** Use conta @gmail.com pessoal (NÃO @usp.br)

**Passo-a-Passo:**

1. **Criação do Projeto GCP**
   - [ ] Acessar [console.cloud.google.com](https://console.cloud.google.com) com @gmail.com
   - [ ] Clicar em "Select a project" → "New Project"
   - [ ] Nome do projeto: `piml-training-lab`
   - [ ] Organização: "No organization" (conta pessoal)
   - [ ] Clicar em "Create"

2. **Ativação do Billing (Free Tier)**
   - [ ] No menu lateral, ir em **Billing → My billing accounts**
   - [ ] Clicar em "Add billing account"
   - [ ] Inserir dados do cartão de crédito
   - [ ] Aceitar termos do Free Tier ($300 USD de crédito)
   - [ ] Verificar que o projeto `piml-training-lab` está vinculado

3. **Configuração de Budget Alert (Trava de Segurança)**
   - [ ] No menu lateral, ir em **Billing → Budgets & alerts**
   - [ ] Clicar em "Create Budget"
   - [ ] Configurações obrigatórias:
     ```
     Budget name: alerta-mensal-r1
     Projects: piml-training-lab
     Budget type: Specified amount
     Target amount: R$ 1.00 (ou $0.20 USD)
     ```
   - [ ] Thresholds de alerta:
     - ✅ 50% do budget → Email
     - ✅ 100% do budget → Email
     - ⬜ 100% do budget → Stop billing (opcional, não recomendado na fase de testes)
   - [ ] Email de notificação: seu @gmail.com
   - [ ] Clicar em "Finish"

4. **Ativação de APIs Necessárias**
   - [ ] No menu lateral, ir em **APIs & Services → Library**
   - [ ] Pesquisar e ativar (Enable) as seguintes APIs:
     - ✅ **Vertex AI API**
     - ✅ **Cloud Storage API**
     - ✅ **Cloud Build API**
   - [ ] Aguardar mensagem "API enabled" para cada uma

**✅ Checkpoint de Validação:**
```python
# Criar arquivo test_gcp_connection.py e executar:

from google.cloud import aiplatform

# Configurar projeto
PROJECT_ID = "piml-training-lab"
REGION = "us-central1"

aiplatform.init(project=PROJECT_ID, location=REGION)

# Listar modelos disponíveis (não precisa usar, só testar conexão)
try:
    models = aiplatform.Model.list(limit=5)
    print("✅ Conexão GCP estabelecida com sucesso!")
    print(f"📊 Projeto: {PROJECT_ID}")
except Exception as e:
    print(f"❌ Erro de conexão: {e}")
```

**Executar no terminal:**
```bash
pip install google-cloud-aiplatform
python test_gcp_connection.py
```

**Critério de Sucesso:**
- ✅ Projeto `piml-training-lab` visível no console
- ✅ Budget alert configurado e email de confirmação recebido
- ✅ Script Python conecta sem erros
- ✅ Vertex AI API ativada (sem erros 403)

**⏱️ Tempo Estimado:** 45-60 minutos

---

### **📌 Exercício 0.1.C - Coursera for USP**

**Objetivo:** Validar acesso gratuito aos cursos via convênio institucional.

**Passo-a-Passo:**

1. **Acesso via Link Institucional**
   - [ ] Acessar EXCLUSIVAMENTE: [coursera.org/partners/usp](https://www.coursera.org/partners/usp)
   - [ ] Fazer login com e-mail @usp.br (NÃO criar conta nova)
   - [ ] Verificar mensagem "USP - Universidade de São Paulo" no topo

2. **Teste de Matrícula Gratuita**
   - [ ] Pesquisar curso: "Machine Learning on Google Cloud Specialization"
   - [ ] Clicar no curso e verificar botão "Enroll for Free" (ou "Inscrever-se gratuitamente")
   - [ ] Se aparecer preço ($49/mês), você NÃO está logado corretamente
   - [ ] Matricular-se no primeiro curso da especialização

**✅ Checkpoint de Validação:**
- ✅ Consegue se matricular SEM inserir dados de pagamento
- ✅ Dashboard Coursera mostra "USP Partnership" na barra superior
- ✅ Acesso ao primeiro vídeo do curso sem cobranças

**Critério de Sucesso:**
- ✅ Matrícula confirmada em pelo menos 1 curso
- ✅ Sem solicitação de cartão de crédito
- ✅ Acesso ilimitado aos vídeos e materiais

**⏱️ Tempo Estimado:** 15-20 minutos

---

### **📌 Exercício 0.1.D - Google Developer Program**

**Objetivo:** Liberar acesso aos laboratórios práticos do Google Cloud Skills Boost.

**Passo-a-Passo:**

1. **Criação do Perfil de Desenvolvedor**
   - [ ] Acessar [developers.google.com/profile](https://developers.google.com/profile) com @gmail.com
   - [ ] Clicar em "Join" ou "Sign up"
   - [ ] Preencher informações:
     ```
     Name: [Seu nome]
     Country: Brazil
     Focus areas: Cloud, Machine Learning, AI
     Experience level: Intermediate
     ```
   - [ ] Aceitar termos

2. **Vinculação ao Google Cloud Skills Boost**
   - [ ] Acessar [cloudskillsboost.google](https://www.cloudskillsboost.google/)
   - [ ] Fazer login com a MESMA conta @gmail.com
   - [ ] Verificar badge "Google Developer" no perfil

3. **Teste de Laboratório Gratuito**
   - [ ] Pesquisar "Vertex AI Gemini API"
   - [ ] Clicar em um laboratório/quest
   - [ ] Verificar se há créditos gratuitos ou acesso "Plus"

**✅ Checkpoint de Validação:**
- ✅ Perfil Google Developer ativo
- ✅ Acesso ao Cloud Skills Boost confirmado
- ✅ Pelo menos 1 crédito de laboratório disponível

**⏱️ Tempo Estimado:** 15-20 minutos

---

## **0.2. BANCADA DIGITAL (Hardware & Software)**

### **📌 Exercício 0.2.A - Instalação do Python 3.10.x**

**Objetivo:** Instalar versão controlada do Python e validar instalação.

**Passo-a-Passo:**

1. **Download e Instalação**
   - [ ] Acessar [python.org/downloads](https://www.python.org/downloads/)
   - [ ] Baixar versão específica: **Python 3.10.11** (ou 3.10.x mais recente)
   - [ ] Durante instalação:
     - ✅ Marcar "Add Python 3.10 to PATH"
     - ✅ Escolher "Install Now" (instalação padrão)

2. **Validação da Instalação**
   - [ ] Abrir terminal/PowerShell NOVO (fechar e abrir novamente)
   - [ ] Executar comandos de validação (ver checkpoint abaixo)

**✅ Checkpoint de Validação:**
```powershell
# 1. Verificar versão do Python
python --version
# Resultado esperado: Python 3.10.11 (ou 3.10.x)

# 2. Verificar versão do pip
pip --version
# Resultado esperado: pip 23.x.x from C:\...\Python310\... (python 3.10)

# 3. Criar ambiente virtual de teste
python -m venv test_env

# 4. Ativar ambiente (Windows PowerShell)
.\test_env\Scripts\Activate.ps1

# 5. Verificar que está no ambiente virtual
# (test_env) deve aparecer no prompt

# 6. Desativar e remover
deactivate
Remove-Item -Recurse -Force test_env
```

**Critério de Sucesso:**
- ✅ `python --version` retorna 3.10.x
- ✅ `pip --version` referencia Python 3.10
- ✅ Ambiente virtual criado e ativado sem erros

**⏱️ Tempo Estimado:** 20-30 minutos

---

### **📌 Exercício 0.2.B - Instalação do EnergyPlus 24.1.0**

**Objetivo:** Instalar EnergyPlus e validar execução via linha de comando.

**Passo-a-Passo:**

1. **Download e Instalação**
   - [ ] Acessar [energyplus.net/downloads](https://energyplus.net/downloads)
   - [ ] Baixar versão: **EnergyPlus 24.1.0** (Windows 64-bit)
   - [ ] Executar instalador (Next → Next → Install)
   - [ ] Diretório padrão: `C:\EnergyPlusV24-1-0`

2. **Validação da Instalação**
   - [ ] Verificar que o diretório existe
   - [ ] Executar simulação de teste via terminal

**✅ Checkpoint de Validação:**
```powershell
# 1. Verificar diretório de instalação
Test-Path "C:\EnergyPlusV24-1-0"
# Resultado esperado: True

# 2. Verificar executável
Test-Path "C:\EnergyPlusV24-1-0\energyplus.exe"
# Resultado esperado: True

# 3. Executar simulação de exemplo
cd "C:\EnergyPlusV24-1-0\ExampleFiles"

# 4. Rodar arquivo de exemplo (1ZoneUncontrolled)
& "C:\EnergyPlusV24-1-0\energyplus.exe" -w USA_CO_Golden-NREL.724666_TMY3.epw -d output_test 1ZoneUncontrolled.idf

# 5. Verificar que arquivos de saída foram criados
Test-Path "output_test\eplusout.csv"
# Resultado esperado: True
```

**Critério de Sucesso:**
- ✅ EnergyPlus instalado em `C:\EnergyPlusV24-1-0`
- ✅ Simulação de exemplo executa sem erros
- ✅ Arquivo `eplusout.csv` gerado no diretório output_test

**⏱️ Tempo Estimado:** 30-40 minutos

---

### **📌 Exercício 0.2.C - Configuração do VS Code**

**Objetivo:** Instalar VS Code e extensões obrigatórias + configurar integrações.

**Passo-a-Passo:**

1. **Instalação do VS Code**
   - [ ] Baixar de [code.visualstudio.com](https://code.visualstudio.com/)
   - [ ] Instalar com configurações padrão

2. **Instalação de Extensões Obrigatórias**
   - [ ] Abrir VS Code
   - [ ] Pressionar `Ctrl+Shift+X` (Extensions)
   - [ ] Pesquisar e instalar cada extensão abaixo:

**Extensões Obrigatórias:**

| Extensão | Publisher | Validação |
|----------|-----------|-----------|
| Python | Microsoft | Ícone Python na barra lateral |
| Jupyter | Microsoft | Pode abrir arquivos .ipynb |
| GitHub Copilot | GitHub | Ícone Copilot na barra inferior |
| Google Cloud Code | Google | "Cloud Code" no menu lateral |

3. **Configuração de Logins**
   - [ ] **GitHub Copilot:** Clicar no ícone inferior → "Sign in to GitHub" → Autorizar
   - [ ] **Google Cloud Code:** Clicar em "Cloud Code" → "Sign in" → Usar @gmail.com
   - [ ] **Python Interpreter:** 
     - Pressionar `Ctrl+Shift+P`
     - Digitar "Python: Select Interpreter"
     - Escolher `Python 3.10.11 64-bit`

**✅ Checkpoint de Validação:**
```python
# Criar arquivo test_vscode.py no VS Code:

def calcular_media(valores):
    """Calcula média de uma lista de valores."""
    return sum(valores) / len(valores)

# Testes de validação
numeros = [10, 20, 30, 40, 50]
media = calcular_media(numeros)
print(f"Média: {media}")

# ✅ Verificar se o Copilot sugere código ao digitar comentários
# ✅ Verificar se o linter Python detecta erros (ex: variável não usada)
```

**Executar teste:**
```powershell
python test_vscode.py
# Resultado esperado: Média: 30.0
```

**Critério de Sucesso:**
- ✅ Todas as 4 extensões instaladas e ativas
- ✅ GitHub Copilot fazendo sugestões (texto cinza ao digitar)
- ✅ Python interpreter 3.10.x selecionado (canto inferior direito)
- ✅ Google Cloud Code autenticado com @gmail.com

**⏱️ Tempo Estimado:** 30-40 minutos

---

### **📌 Exercício 0.2.D - Instalação do Kit de Bibliotecas Python**

**Objetivo:** Instalar todas as bibliotecas obrigatórias e validar importações.

**Passo-a-Passo:**

1. **Criação de Ambiente Virtual do Projeto**
   ```powershell
   # Criar diretório do projeto
   mkdir "C:\Users\joaop\Downloads\AI Engineering\piml-training"
   cd "C:\Users\joaop\Downloads\AI Engineering\piml-training"
   
   # Criar ambiente virtual
   python -m venv venv
   
   # Ativar ambiente
   .\venv\Scripts\Activate.ps1
   ```

2. **Instalação de Bibliotecas (Categorias)**
   ```powershell
   # ===== CATEGORIA 1: Dados e ML Clássico =====
   pip install pandas numpy scikit-learn matplotlib jupyter scipy
   
   # ===== CATEGORIA 2: Domínio BPS (Building Performance Simulation) =====
   pip install eppy energyplus-api-helpers
   
   # ===== CATEGORIA 3: IA Generativa e Deep Learning =====
   pip install google-cloud-aiplatform streamlit pydantic
   
   # ===== CATEGORIA 4: Utilitários =====
   pip install pytest black ipykernel
   ```

3. **Validação das Instalações**
   - [ ] Criar script de teste (ver checkpoint abaixo)
   - [ ] Executar e verificar que TODAS as importações funcionam

**✅ Checkpoint de Validação:**
```python
# Criar arquivo test_imports.py:

"""Script de validação de bibliotecas instaladas."""

def test_data_ml():
    """Testa bibliotecas de dados e ML clássico."""
    try:
        import pandas as pd
        import numpy as np
        import sklearn
        import matplotlib.pyplot as plt
        import scipy
        print("✅ Categoria 1 (Dados/ML): OK")
        return True
    except ImportError as e:
        print(f"❌ Categoria 1 falhou: {e}")
        return False

def test_bps():
    """Testa bibliotecas do domínio BPS."""
    try:
        import eppy
        print("✅ Categoria 2 (BPS): OK")
        return True
    except ImportError as e:
        print(f"❌ Categoria 2 falhou: {e}")
        return False

def test_ai():
    """Testa bibliotecas de IA Generativa."""
    try:
        from google.cloud import aiplatform
        import streamlit
        import pydantic
        print("✅ Categoria 3 (IA Generativa): OK")
        return True
    except ImportError as e:
        print(f"❌ Categoria 3 falhou: {e}")
        return False

def test_utils():
    """Testa utilitários."""
    try:
        import pytest
        import black
        print("✅ Categoria 4 (Utilitários): OK")
        return True
    except ImportError as e:
        print(f"❌ Categoria 4 falhou: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testando instalação de bibliotecas...\n")
    
    results = [
        test_data_ml(),
        test_bps(),
        test_ai(),
        test_utils()
    ]
    
    if all(results):
        print("\n🎉 TODAS as bibliotecas foram instaladas corretamente!")
        print("✅ Bancada Digital está pronta para uso.")
    else:
        print("\n⚠️ Algumas bibliotecas falharam. Reinstale individualmente.")
```

**Executar teste:**
```powershell
python test_imports.py
```

**Critério de Sucesso:**
- ✅ Todas as 4 categorias retornam "OK"
- ✅ Nenhum erro de ImportError
- ✅ Mensagem final: "TODAS as bibliotecas foram instaladas corretamente!"

**⏱️ Tempo Estimado:** 20-30 minutos

---

### **📌 Exercício 0.2.E - Teste de Proficiência Python**

**Objetivo:** Validar conhecimento básico de Python necessário para o curso.

**Desafio Prático (SEM consultar tutoriais):**

Criar script `proficiency_test.py` que:
1. Leia arquivo CSV com dados de consumo energético
2. Filtre apenas registros onde consumo > 100 kWh
3. Calcule a média de consumo filtrada
4. Salve resultado em novo arquivo CSV

**Dados de Entrada (criar arquivo `consumo.csv`):**
```csv
data,zona,consumo_kwh
2024-01-01,Norte,85
2024-01-02,Sul,120
2024-01-03,Leste,150
2024-01-04,Oeste,95
2024-01-05,Norte,200
2024-01-06,Sul,110
```

**Template Inicial:**
```python
import pandas as pd

def processar_consumo(arquivo_entrada, arquivo_saida, threshold=100):
    """
    Processa dados de consumo energético.
    
    Args:
        arquivo_entrada: Path para CSV de entrada
        arquivo_saida: Path para CSV de saída
        threshold: Valor mínimo de consumo para filtro
    """
    # TODO: Implementar lógica
    pass

if __name__ == "__main__":
    processar_consumo("consumo.csv", "consumo_filtrado.csv")
    print("✅ Processamento concluído!")
```

**✅ Checkpoint de Validação:**

Resultado esperado em `consumo_filtrado.csv`:
```csv
data,zona,consumo_kwh
2024-01-02,Sul,120
2024-01-03,Leste,150
2024-01-05,Norte,200
2024-01-06,Sul,110
```

Média calculada e impressa: **145.0 kWh**

**Critério de Sucesso:**
- ✅ Código funciona sem erros
- ✅ Arquivo de saída contém apenas registros com consumo > 100
- ✅ Média calculada corretamente (145.0)
- ✅ Implementação feita SEM consultar tutoriais básicos de pandas

**⏱️ Tempo Estimado:** 30-40 minutos

---

## **0.3. ENGENHARIA DE SOFTWARE (DevOps Básico)**

### **📌 Exercício 0.3.A - Configuração do Git & GitHub**

**Objetivo:** Configurar repositório privado com .gitignore adequado para o projeto.

**Passo-a-Passo:**

1. **Instalação do Git**
   - [ ] Baixar de [git-scm.com/downloads](https://git-scm.com/downloads)
   - [ ] Instalar com configurações padrão

2. **Configuração Inicial do Git**
   ```powershell
   # Configurar nome e email
   git config --global user.name "Seu Nome"
   git config --global user.email "seu_email@usp.br"
   
   # Verificar configuração
   git config --list
   ```

3. **Criação do Repositório GitHub**
   - [ ] Acessar [github.com](https://github.com)
   - [ ] Clicar em "New Repository"
   - [ ] Configurações:
     ```
     Name: piml-training
     Description: Scientific AI Engineering & BPS - Training Repository
     Visibility: Private (importante!)
     Initialize: Add README
     ```
   - [ ] Clicar em "Create repository"

4. **Clone e Configuração Local**
   ```powershell
   # Navegar até pasta de trabalho
   cd "C:\Users\joaop\Downloads\AI Engineering"
   
   # Clonar repositório
   git clone https://github.com/SEU_USERNAME/piml-training.git
   cd piml-training
   ```

5. **Criação do .gitignore**
   - [ ] Criar arquivo `.gitignore` na raiz do projeto

**Conteúdo do .gitignore:**
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
*.egg-info/
dist/
build/

# Jupyter Notebooks
.ipynb_checkpoints/
*.ipynb

# EnergyPlus (arquivos pesados)
*.eso
*.sql
*.mtr
*.mtd
*.rdd
*.shd
*.audit
*.bnd
*.eio
*.err
*.mdd
*.mtd
*.rvaudit
*.sci
*.shd
*.dfs

# VS Code
.vscode/

# Credenciais e Configurações Sensíveis
.env
*.key
*.json  # Credenciais GCP
credentials/

# Dados Temporários
*.tmp
*.log
temp/
output/

# Sistema Operacional
.DS_Store
Thumbs.db
```

**✅ Checkpoint de Validação:**
```powershell
# 1. Criar arquivo de teste Python
echo "print('Hello World')" > test.py

# 2. Criar diretório venv de teste
mkdir venv

# 3. Verificar status do git
git status

# Resultado esperado:
# - test.py aparece como untracked
# - venv/ NÃO aparece (ignorado pelo .gitignore)

# 4. Adicionar .gitignore e test.py
git add .gitignore test.py

# 5. Fazer commit
git commit -m "Initial setup: .gitignore and test script"

# 6. Push para GitHub
git push origin main

# 7. Limpar teste
Remove-Item test.py
Remove-Item -Recurse venv
```

**Critério de Sucesso:**
- ✅ Repositório privado `piml-training` criado no GitHub
- ✅ .gitignore configurado (venv/ e __pycache__/ são ignorados)
- ✅ Primeiro commit realizado com sucesso
- ✅ Push para GitHub funciona sem erros

**⏱️ Tempo Estimado:** 30-40 minutos

---

### **📌 Exercício 0.3.B - Code Quality (Black Formatter)**

**Objetivo:** Configurar formatação automática de código no VS Code.

**Passo-a-Passo:**

1. **Instalação da Extensão Black Formatter**
   - [ ] No VS Code, pressionar `Ctrl+Shift+X`
   - [ ] Pesquisar "Black Formatter"
   - [ ] Instalar extensão (Publisher: Microsoft)

2. **Configuração de Format on Save**
   - [ ] Pressionar `Ctrl+,` (Settings)
   - [ ] Pesquisar "format on save"
   - [ ] Marcar checkbox "Editor: Format On Save"
   - [ ] Pesquisar "python formatting provider"
   - [ ] Selecionar "black" no dropdown

3. **Teste de Formatação Automática**
   - [ ] Criar arquivo `test_formatting.py` com código mal formatado (ver checkpoint)
   - [ ] Salvar arquivo (`Ctrl+S`)
   - [ ] Verificar que o código foi reformatado automaticamente

**✅ Checkpoint de Validação:**

**Código Inicial (mal formatado):**
```python
# test_formatting.py
def calcular(x,y,z):
    resultado=x+y*z
    if resultado>100:
        print( "Valor alto" )
    else:
        print("Valor baixo")
    return resultado

dados=[1,2,3,4,5,6,7,8,9,10]
media=sum(dados)/len(dados)
```

**Código Após Salvar (bem formatado pelo Black):**
```python
# test_formatting.py
def calcular(x, y, z):
    resultado = x + y * z
    if resultado > 100:
        print("Valor alto")
    else:
        print("Valor baixo")
    return resultado


dados = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
media = sum(dados) / len(dados)
```

**Critério de Sucesso:**
- ✅ Black Formatter instalado e ativo
- ✅ Format on Save habilitado
- ✅ Código é reformatado automaticamente ao salvar
- ✅ Espaçamento correto (ex: `x + y` ao invés de `x+y`)

**⏱️ Tempo Estimado:** 15-20 minutos

---

### **📌 Exercício 0.3.C - Regra de Ouro: Jupyter Notebooks Limpos**

**Objetivo:** Estabelecer workflow de limpeza de notebooks antes de commits.

**Passo-a-Passo:**

1. **Criação de Notebook de Teste**
   - [ ] No VS Code, criar arquivo `test_notebook.ipynb`
   - [ ] Adicionar células com código e executar (gerar outputs)

2. **Workflow de Limpeza Manual**
   ```python
   # Célula 1
   import numpy as np
   data = np.random.rand(5)
   print(data)
   
   # Célula 2
   mean_value = np.mean(data)
   print(f"Média: {mean_value}")
   ```

3. **Antes de Commit: Clear All Outputs**
   - [ ] No VS Code, com notebook aberto:
     - Clicar nos 3 pontos (`...`) no topo do notebook
     - Selecionar "Clear All Outputs"
   - [ ] Verificar que todas as células estão sem outputs
   - [ ] Salvar arquivo

4. **Adicionar ao Git**
   ```powershell
   git add test_notebook.ipynb
   git commit -m "Add test notebook (outputs cleared)"
   git push
   ```

**✅ Checkpoint de Validação:**

**Arquivo .ipynb NÃO deve conter:**
```json
"outputs": [
  {
    "output_type": "stream",
    "text": ["0.12345..."]
  }
]
```

**Arquivo .ipynb DEVE conter:**
```json
"outputs": []
```

**Critério de Sucesso:**
- ✅ Notebook foi executado localmente (tem outputs)
- ✅ Outputs foram limpos antes do commit
- ✅ Arquivo no GitHub não contém dados de output
- ✅ Tamanho do arquivo .ipynb < 50 KB (sem outputs pesados)

**⏱️ Tempo Estimado:** 15-20 minutos

---

## **0.4. TESTE DE PROFICIÊNCIA FINAL (Integração Completa)**

### **📌 Exercício 0.4.A - Mini-Projeto Integrado**

**Objetivo:** Validar TODA a infraestrutura em um único exercício prático.

**Cenário:**
Você precisa criar um script Python que:
1. Conecta ao GCP para testar autenticação
2. Lê dados de um arquivo CSV simulado
3. Executa simulação básica do EnergyPlus
4. Gera relatório final

**Requisitos Técnicos:**
- ✅ Usar ambiente virtual (`venv`)
- ✅ Código formatado pelo Black
- ✅ Criar Jupyter Notebook com análise visual
- ✅ Commitar no GitHub SEM outputs do notebook
- ✅ Documentar processo no README.md

**Passo-a-Passo:**

1. **Setup do Projeto**
   ```powershell
   # Criar estrutura de diretórios
   mkdir proficiency_test
   cd proficiency_test
   mkdir data output scripts
   
   # Criar ambiente virtual
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   
   # Instalar dependências
   pip install pandas matplotlib google-cloud-aiplatform
   ```

2. **Script 1: Teste GCP (scripts/test_gcp.py)**
   ```python
   """Teste de conexão com Google Cloud Platform."""
   
   from google.cloud import aiplatform
   
   def test_gcp_connection():
       """Valida autenticação com Vertex AI."""
       try:
           PROJECT_ID = "piml-training-lab"
           REGION = "us-central1"
           
           aiplatform.init(project=PROJECT_ID, location=REGION)
           
           print("✅ GCP Authentication: OK")
           print(f"📊 Projeto: {PROJECT_ID}")
           print(f"📍 Região: {REGION}")
           return True
       except Exception as e:
           print(f"❌ GCP Authentication Failed: {e}")
           return False
   
   if __name__ == "__main__":
       test_gcp_connection()
   ```

3. **Script 2: Simulação EnergyPlus (scripts/run_simulation.py)**
   ```python
   """Script básico de execução do EnergyPlus."""
   
   import subprocess
   import os
   from pathlib import Path
   
   def run_energyplus_simulation():
       """Executa simulação de exemplo do EnergyPlus."""
       
       # Caminhos
       ep_dir = Path("C:/EnergyPlusV24-1-0")
       ep_exe = ep_dir / "energyplus.exe"
       example_file = ep_dir / "ExampleFiles/1ZoneUncontrolled.idf"
       weather_file = ep_dir / "WeatherData/USA_CO_Golden-NREL.724666_TMY3.epw"
       output_dir = Path("output")
       
       # Verificações
       if not ep_exe.exists():
           print(f"❌ EnergyPlus não encontrado em {ep_exe}")
           return False
       
       output_dir.mkdir(exist_ok=True)
       
       # Executar simulação
       print("🔄 Iniciando simulação EnergyPlus...")
       
       cmd = [
           str(ep_exe),
           "-w", str(weather_file),
           "-d", str(output_dir),
           str(example_file)
       ]
       
       result = subprocess.run(cmd, capture_output=True, text=True)
       
       if result.returncode == 0:
           print("✅ Simulação concluída com sucesso!")
           print(f"📁 Outputs em: {output_dir}")
           
           # Verificar arquivo de saída
           csv_output = output_dir / "eplusout.csv"
           if csv_output.exists():
               print(f"✅ Arquivo CSV gerado: {csv_output}")
               return True
       else:
           print(f"❌ Simulação falhou: {result.stderr}")
           return False
   
   if __name__ == "__main__":
       run_energyplus_simulation()
   ```

4. **Notebook de Análise (analysis.ipynb)**
   ```python
   # Célula 1: Imports
   import pandas as pd
   import matplotlib.pyplot as plt
   from pathlib import Path
   
   # Célula 2: Carregar dados
   output_file = Path("output/eplusout.csv")
   
   if output_file.exists():
       df = pd.read_csv(output_file)
       print(f"✅ Dados carregados: {len(df)} registros")
       print(df.head())
   else:
       print("❌ Arquivo de output não encontrado!")
   
   # Célula 3: Visualização básica
   # (Análise simples dos dados - ex: consumo por hora)
   
   # Célula 4: Estatísticas
   print("📊 Estatísticas Descritivas:")
   print(df.describe())
   ```

5. **Documentação (README.md)**
   ```markdown
   # Teste de Proficiência - Fase 0
   
   ## Objetivo
   Validar integração completa da infraestrutura.
   
   ## Componentes Testados
   - ✅ Python 3.10.x
   - ✅ Ambiente virtual (venv)
   - ✅ EnergyPlus 24.1.0
   - ✅ Google Cloud Platform (autenticação)
   - ✅ Bibliotecas essenciais (pandas, matplotlib)
   - ✅ Git & GitHub workflow
   
   ## Como Executar
   
   1. Ativar ambiente virtual:
      ```bash
      .\venv\Scripts\Activate.ps1
      ```
   
   2. Testar conexão GCP:
      ```bash
      python scripts/test_gcp.py
      ```
   
   3. Executar simulação EnergyPlus:
      ```bash
      python scripts/run_simulation.py
      ```
   
   4. Abrir notebook de análise:
      ```bash
      jupyter notebook analysis.ipynb
      ```
   
   ## Resultados
   - ✅ Todos os testes passaram
   - ✅ Simulação executada com sucesso
   - ✅ Outputs gerados em `output/`
   ```

6. **Git Workflow**
   ```powershell
   # Adicionar arquivos (SEM outputs do notebook!)
   git add scripts/ data/ README.md analysis.ipynb .gitignore
   
   # Verificar que output/ está ignorado
   git status  # não deve listar output/
   
   # Commit
   git commit -m "Teste de proficiência Fase 0 - Infraestrutura completa"
   
   # Push
   git push origin main
   ```

**✅ Checkpoint de Validação Final:**

| Componente | Status | Evidência |
|------------|--------|-----------|
| Python 3.10.x | ⬜ | `python --version` retorna 3.10.x |
| Ambiente Virtual | ⬜ | `(venv)` no prompt |
| EnergyPlus 24.1.0 | ⬜ | Simulação executada, CSV gerado |
| GCP Autenticação | ⬜ | Script `test_gcp.py` retorna "OK" |
| Bibliotecas | ⬜ | Imports funcionam sem erros |
| Black Formatter | ⬜ | Código formatado automaticamente |
| Git/GitHub | ⬜ | Commits aparecem no repositório remoto |
| Jupyter Notebooks | ⬜ | Notebook limpo (sem outputs) no GitHub |

**Critério de Sucesso (TODOS devem ser ✅):**
- ✅ `test_gcp.py` executa sem erros de autenticação
- ✅ `run_simulation.py` gera arquivo `eplusout.csv`
- ✅ Notebook executa todas as células sem erros
- ✅ Código está formatado (espaçamento correto)
- ✅ Repository no GitHub contém todos os arquivos
- ✅ Notebook no GitHub NÃO contém outputs
- ✅ Diretório `output/` NÃO está no GitHub (ignorado)

**⏱️ Tempo Estimado:** 60-90 minutos

---

## **✅ CERTIFICAÇÃO DE CONCLUSÃO DA FASE 0**

### **Checklist Final de Aprovação**

Antes de iniciar o Mês 1, TODOS os itens abaixo devem estar marcados como ✅:

#### **Benefícios Acadêmicos**
- [ ] GitHub Copilot ativado e funcionando no VS Code
- [ ] GCP Free Tier ativado ($300 USD de crédito)
- [ ] Budget alert configurado (R$ 1,00/mês)
- [ ] Coursera for USP validado (matrícula gratuita confirmada)
- [ ] Google Developer Program ativo

#### **Ambiente de Desenvolvimento**
- [ ] Python 3.10.x instalado e validado
- [ ] EnergyPlus 24.1.0 instalado e testado via CLI
- [ ] VS Code com 4 extensões obrigatórias (Python, Jupyter, Copilot, Cloud Code)
- [ ] Todas as bibliotecas instaladas (pandas, numpy, scikit-learn, eppy, streamlit, etc.)

#### **Engenharia de Software**
- [ ] Repositório privado `piml-training` criado no GitHub
- [ ] .gitignore configurado corretamente
- [ ] Black Formatter instalado e Format on Save ativo
- [ ] Workflow de Jupyter Notebooks estabelecido (clear outputs antes de commit)

#### **Testes de Proficiência**
- [ ] Teste de proficiência Python concluído (processar CSV sem consultar tutoriais)
- [ ] Mini-projeto integrado executado com sucesso
- [ ] Simulação EnergyPlus via Python funcionando
- [ ] Autenticação GCP validada

#### **Documentação**
- [ ] README.md criado no repositório
- [ ] Pelo menos 3 commits no GitHub
- [ ] Todos os scripts documentados com docstrings

---

## **🎯 Próximos Passos**

**Após concluir TODOS os checkpoints acima:**

1. **Fazer commit final:**
   ```powershell
   git add .
   git commit -m "Fase 0 concluída - Infraestrutura validada"
   git push origin main
   ```

2. **Criar issue de conclusão no GitHub:**
   - Título: "Fase 0 - Infraestrutura Validada"
   - Descrição: Listar todos os checkpoints concluídos
   - Label: `milestone`, `setup`

3. **Agendar primeira Weekly Sync:**
   - Preparar apresentação de 5 minutos sobre a infraestrutura
   - Demonstrar: EnergyPlus rodando via Python + Copilot ativo

4. **Iniciar Mês 1:**
   - Ler arquivo: `Exercicios_Mes_1_EnergyPlus.md` (será criado em seguida)
   - Começar leitura do EnergyPlus Input Output Reference

---

## **📚 Recursos Adicionais**

### **Troubleshooting Comum**

**Problema 1: Python não reconhecido no terminal**
```powershell
# Solução: Adicionar ao PATH manualmente
$env:Path += ";C:\Users\joaop\AppData\Local\Programs\Python\Python310"
```

**Problema 2: EnergyPlus não executa**
```powershell
# Verificar permissões de execução
icacls "C:\EnergyPlusV24-1-0\energyplus.exe"
```

**Problema 3: GCP retorna erro 403 (Permission Denied)**
```bash
# Reautenticar no Cloud Code
# No VS Code: Cloud Code → Sign Out → Sign In novamente
```

**Problema 4: Copilot não faz sugestões**
```bash
# Verificar status na barra inferior do VS Code
# Clicar no ícone Copilot → Check Status
# Se "Inactive", fazer logout/login do GitHub
```

### **Links de Referência Rápida**

- [EnergyPlus Documentation](https://energyplus.net/documentation)
- [Pandas Cheat Sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
- [Pydantic Docs](https://docs.pydantic.dev/latest/)
- [Black Code Style](https://black.readthedocs.io/en/stable/)
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)

---

**🎉 Parabéns por concluir a Fase 0!**

Você agora tem uma bancada digital profissional e está pronto para iniciar a jornada de 12 meses em Scientific AI Engineering & BPS.

**Próximo arquivo:** `Exercicios_Fase_1_Fundamentos.md` (a ser criado)
