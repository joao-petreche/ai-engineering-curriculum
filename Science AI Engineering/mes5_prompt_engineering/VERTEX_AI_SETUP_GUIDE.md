# 🚀 VERTEX AI SETUP GUIDE - Integração de IA com GCP

## Objetivo
Guia completo para configurar Google Cloud Vertex AI e integrar com surrogates PIML.

**Tempo estimado**: 2-4 horas (com este guia)

---

## PARTE 1: PREPARAÇÃO - Google Cloud Console

### 1.1 Criar Projeto no GCP

1. Acesse [Google Cloud Console](https://console.cloud.google.com)
2. Clique em **Selecionar projeto** (topo esquerdo)
3. Clique em **NOVO PROJETO**
4. Preencha:
   - **Nome do projeto**: `ai-engineering-piml`
   - **ID do projeto**: `ai-engineering-piml-XXXXX` (será gerado)
   - **Organização**: Deixe em branco
5. Clique em **CRIAR**
6. Aguarde 1-2 minutos pela criação

✅ **Verificação**: O projeto aparecerá na lista de projetos.

### 1.2 Habilitar Faturamento

1. No console, abra o menu ☰ (canto superior esquerdo)
2. Vá para **Faturamento**
3. Clique em **CRIAR CONTA DE FATURAMENTO**
4. Preencha dados de cobrança (pode usar cartão de teste)
5. Configure orçamento:
   - **Limite mensal**: USD 10.00 (gratuito para primeiros USD 300)

⚠️ **Importante**: O GCP oferece USD 300 crédito por 90 dias. Você não será cobrado após este crédito sem autorização.

✅ **Verificação**: Status mostrará "Ativa" em verde.

### 1.3 Conectar Faturamento ao Projeto

1. Vá para **Gerenciamento de recursos** → **Projetos**
2. Selecione `ai-engineering-piml-XXXXX`
3. Abra o menu ⋮ (lado direito) → **Editar projeto**
4. Clique em **ALTERAR CONTA DE FATURAMENTO**
5. Selecione a conta criada em 1.2
6. Clique em **CONFIRMAR**

✅ **Verificação**: O projeto mostrará uma conta de faturamento ativa.

### 1.4 Habilitar APIs Necessárias

1. No console, abra **APIs e Serviços** → **Biblioteca**
2. Procure por cada API abaixo e clique em **ATIVAR**:

```
✅ Vertex AI API
✅ Cloud Resource Manager API
✅ Service Usage API
✅ Cloud Build API
✅ Cloud Run API
✅ BigQuery API
✅ Compute Engine API
```

**Tempo esperado**: 1-2 minutos por API (execute em paralelo)

✅ **Verificação**: Cada API mostrará um botão **"Gerenciar"** (não "Ativar")

---

## PARTE 2: AUTENTICAÇÃO - Service Account

### 2.1 Criar Service Account

1. Vá para **APIs e Serviços** → **Credenciais**
2. Clique em **+ CRIAR CREDENCIAIS** (topo)
3. Selecione **Conta de Serviço**
4. Preencha:
   - **Nome da conta**: `vertex-ai-service`
   - **ID da conta**: `vertex-ai-service` (gerado automaticamente)
   - **Descrição**: "Service account para PIML + Vertex AI"
5. Clique em **CRIAR E CONTINUAR**
6. Na próxima tela, **NÃO adicione papéis aqui** (faremos depois)
7. Clique em **CONTINUAR** → **PRONTO**

✅ **Verificação**: A conta aparecerá em "Contas de Serviço".

### 2.2 Criar Chave JSON

1. Clique na conta criada (`vertex-ai-service@...`)
2. Abra a aba **CHAVES**
3. Clique em **ADICIONAR CHAVE** → **Criar nova chave**
4. Selecione **JSON**
5. Clique em **CRIAR**
6. O arquivo `vertex-ai-service-XXXXX.json` será baixado automaticamente

⚠️ **SEGURANÇA**: Este arquivo contém credenciais. **NÃO faça commit no Git!**

✅ **Verificação**: Verifique que o arquivo contém:
```json
{
  "type": "service_account",
  "project_id": "ai-engineering-piml-XXXXX",
  "private_key": "-----BEGIN PRIVATE KEY-----...",
  "client_email": "vertex-ai-service@..."
}
```

### 2.3 Adicionar Papéis à Service Account

1. Abra **IAM e Administrador** → **IAM**
2. Clique em **EDITAR ACESSO** (lado direito)
3. Clique em **ADICIONAR VINCULAÇÃO DE PAPÉIS**
4. Selecione a service account criada
5. Adicione estes papéis:

```
✅ Vertex AI Service Agent
✅ Vertex AI User
✅ Service Account User
✅ Editor (temporário, para testes)
```

6. Clique em **SALVAR**

✅ **Verificação**: A service account mostrará os papéis atribuídos.

---

## PARTE 3: CONFIGURAÇÃO LOCAL - Python

### 3.1 Instalar Bibliotecas Necessárias

```powershell
# No seu ambiente Python
pip install google-cloud-aiplatform==1.35.0
pip install google-cloud-storage==2.10.0
pip install google-cloud-bigquery==3.12.0
pip install google-generativeai==0.3.0  # Para Generative AI
pip install python-dotenv==1.0.0
```

### 3.2 Configurar Variáveis de Ambiente

**Opção A: Via `.env` (recomendado para desenvolvimento)**

1. Coloque o arquivo `vertex-ai-service-XXXXX.json` em uma pasta segura:
   ```
   C:/Users/[seu_usuario]/.gcp/vertex-ai-service.json
   ```

2. Crie arquivo `.env` no raiz do projeto:
   ```
   GOOGLE_APPLICATION_CREDENTIALS=C:/Users/joaop/.gcp/vertex-ai-service.json
   GCP_PROJECT_ID=ai-engineering-piml-XXXXX
   GCP_REGION=us-central1
   ```

3. Carregue no Python:
   ```python
   from dotenv import load_dotenv
   import os
   
   load_dotenv()
   project_id = os.getenv("GCP_PROJECT_ID")
   credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
   ```

**Opção B: Via Variável de Ambiente Global (Windows)**

```powershell
# PowerShell (como Administrador)
[Environment]::SetEnvironmentVariable(
    "GOOGLE_APPLICATION_CREDENTIALS",
    "C:/Users/joaop/.gcp/vertex-ai-service.json",
    [EnvironmentVariableTarget]::User
)

# Reinicie o PowerShell para ativar
```

### 3.3 Teste de Autenticação

Crie script `test_vertex_connection.py`:

```python
#!/usr/bin/env python
"""
Teste de Conexão ao Vertex AI
"""

import os
from google.cloud import aiplatform
from dotenv import load_dotenv

def test_vertex_connection():
    # Carregar variáveis
    load_dotenv()
    project_id = os.getenv("GCP_PROJECT_ID")
    region = os.getenv("GCP_REGION", "us-central1")
    
    if not project_id:
        raise ValueError("GCP_PROJECT_ID não definido em .env")
    
    print(f"🔍 Testando conexão ao Vertex AI...")
    print(f"   Projeto: {project_id}")
    print(f"   Região: {region}")
    
    try:
        # Inicializar Vertex AI
        aiplatform.init(
            project=project_id,
            location=region
        )
        
        print("✅ Autenticação bem-sucedida!")
        print(f"✅ Credenciais carregadas de: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}")
        
        # Listar modelos
        models = aiplatform.Model.list(
            filter="display_name:*",
            order_by="create_time desc"
        )
        
        print(f"\n📋 Modelos no Vertex AI:")
        if len(models) == 0:
            print("   (Nenhum modelo encontrado - é normal na primeira execução)")
        else:
            for model in models[:5]:
                print(f"   - {model.display_name}")
        
        return True
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    success = test_vertex_connection()
    exit(0 if success else 1)
```

Execute:
```powershell
python test_vertex_connection.py
```

**Saída esperada**:
```
🔍 Testando conexão ao Vertex AI...
   Projeto: ai-engineering-piml-XXXXX
   Região: us-central1
✅ Autenticação bem-sucedida!
✅ Credenciais carregadas de: C:/Users/joaop/.gcp/vertex-ai-service.json

📋 Modelos no Vertex AI:
   (Nenhum modelo encontrado - é normal na primeira execução)
```

---

## PARTE 4: INTEGRAÇÃO COM SURROGATES

### 4.1 Upload de Dataset para BigQuery

```python
from google.cloud import bigquery
import pandas as pd

def upload_dataset_to_bigquery(csv_path, project_id):
    """
    Upload dataset PIML para BigQuery
    """
    client = bigquery.Client(project=project_id)
    
    # Ler CSV
    df = pd.read_csv(csv_path)
    
    # Configurar destino
    dataset_id = "piml_datasets"
    table_id = "simulations_500samples"
    table_full_id = f"{project_id}.{dataset_id}.{table_id}"
    
    # Criar dataset se não existe
    dataset = bigquery.Dataset(f"{project_id}.{dataset_id}")
    dataset.location = "US"
    try:
        dataset = client.create_dataset(dataset, exists_ok=True)
        print(f"✅ Dataset criado: {dataset_id}")
    except Exception as e:
        print(f"⚠️  Dataset já existe: {e}")
    
    # Fazer upload
    job_config = bigquery.LoadJobConfig(
        autodetect=True,  # Detectar tipos automaticamente
        write_disposition="WRITE_TRUNCATE",  # Sobrescrever
    )
    
    load_job = client.load_table_from_dataframe(
        df, table_full_id, job_config=job_config
    )
    
    load_job.result()  # Aguardar conclusão
    
    print(f"✅ Dataset carregado: {len(df)} linhas em {table_full_id}")
    
    # Verificar
    table = client.get_table(table_full_id)
    print(f"   Esquema: {len(table.schema)} colunas")
    
    return table_full_id

# Usar
if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    project_id = os.getenv("GCP_PROJECT_ID")
    
    csv_path = "data/lhs_datasets/piml_dataset_500samples_XXXXX.csv"
    table_id = upload_dataset_to_bigquery(csv_path, project_id)
```

### 4.2 Usar Vertex AI Generative AI para Análise

```python
from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel

def analyze_dataset_with_vertex_ai(project_id, dataset_summary):
    """
    Use Vertex AI para análise de dataset
    """
    # Inicializar
    vertexai.init(project=project_id, location="us-central1")
    
    # Usar modelo Gemini
    model = GenerativeModel(
        "gemini-pro",  # Modelo de texto padrão
        system_instruction="Você é um especialista em ML e otimização. Analise estatísticas de dataset PIML."
    )
    
    prompt = f"""
    Analise este dataset PIML de 500 simulações e forneça:
    1. Variáveis mais importantes para consumo de energia
    2. Colinearidades principais
    3. Recomendações de hiperparâmetros para surrogate
    
    Estatísticas:
    {dataset_summary}
    """
    
    response = model.generate_content(prompt)
    
    print("📊 Análise do Vertex AI:")
    print(response.text)
    
    return response.text

# Usar
if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    import pandas as pd
    
    load_dotenv()
    project_id = os.getenv("GCP_PROJECT_ID")
    
    # Carregar estatísticas do dataset
    df = pd.read_csv("data/lhs_datasets/piml_dataset_500samples_XXXXX.csv")
    summary = df.describe().to_string()
    
    analyze_dataset_with_vertex_ai(project_id, summary)
```

---

## PARTE 5: TROUBLESHOOTING

### ❌ Erro: "403 Permission Denied"

**Causa**: Service account não tem permissões suficientes

**Solução**:
1. Vá para **IAM e Administrador** → **IAM**
2. Clique em **EDITAR ACESSO**
3. Encontre sua service account
4. Clique em **ADICIONAR PAPÉIS**
5. Adicione: **Vertex AI User**, **Vertex AI Service Agent**, **Editor**
6. Aguarde 2-3 minutos pela propagação

### ❌ Erro: "Module 'google' has no attribute 'cloud'"

**Causa**: Biblioteca não instalada corretamente

**Solução**:
```powershell
pip uninstall google-cloud-aiplatform -y
pip install google-cloud-aiplatform==1.35.0 --upgrade
```

### ❌ Erro: "GOOGLE_APPLICATION_CREDENTIALS not set"

**Causa**: Variável de ambiente não definida

**Solução**:
```python
# Em seu código Python, antes de qualquer import GCP
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\path\to\vertex-ai-service.json'

# OU use .env
from dotenv import load_dotenv
load_dotenv()
```

### ❌ Erro: "The operation timed out"

**Causa**: Timeout em BigQuery ou Vertex AI

**Solução**:
```python
# Aumentar timeout
from google.cloud import bigquery

client = bigquery.Client(project=project_id)
job_config = bigquery.QueryJobConfig(
    timeout=300  # 5 minutos
)
```

### ⚠️ Aviso: "Charges may be incurred"

**Causa**: Normal - você está usando serviços do GCP

**Solução**:
- Implemente limites de uso:
```python
# BigQuery: Limitar bytes escaneados
job_config = bigquery.QueryJobConfig(
    maximum_bytes_billed=10_000_000  # ~0.05 USD
)
```

---

## PARTE 6: PRÓXIMOS PASSOS

### Mês 5: Integração Completa

1. **Few-shot Prompting**
   - Usar 50 exemplos do golden dataset
   - Instruir Vertex AI com casos técnicos reais

2. **Chain-of-Thought**
   - Dividir problemas em etapas
   - Ex: "Calcule U-value → Simule → Otimize"

3. **Fine-tuning**
   - Treinar modelo customizado com seus dados
   - Melhor performance em domínio específico

4. **Deployment**
   - Deploy de surrogates como API
   - Usar Cloud Run para servir predições

### Recursos Úteis

- [Documentação Vertex AI](https://cloud.google.com/vertex-ai/docs)
- [Guia de Autenticação](https://cloud.google.com/docs/authentication/getting-started)
- [BigQuery Cookbook](https://cloud.google.com/bigquery/docs/recipes)
- [Generative AI API](https://cloud.google.com/vertex-ai/docs/generative-ai/start/quickstarts)

---

## REFERÊNCIA RÁPIDA

**Comandos Úteis**:

```powershell
# Listar projetos
gcloud projects list

# Definir projeto ativo
gcloud config set project ai-engineering-piml-XXXXX

# Ver credenciais ativas
gcloud auth list

# Re-autenticar
gcloud auth login
```

**Arquivo `.env` Exemplo**:
```
GOOGLE_APPLICATION_CREDENTIALS=C:/Users/joaop/.gcp/vertex-ai-service.json
GCP_PROJECT_ID=ai-engineering-piml-XXXXX
GCP_REGION=us-central1
VERTEX_AI_ENDPOINT=us-central1-aiplatform.googleapis.com
```

---

**Status**: ✅ Guia Completo
**Última Atualização**: 2025-01-XX
**Duração Estimada**: 2-4 horas (primeira execução)
