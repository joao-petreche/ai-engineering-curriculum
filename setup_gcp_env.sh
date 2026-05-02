#!/bin/bash

# ==============================================================================
# Configuração de Ambiente: Scientific AI Engineering (GCP/Codespaces)
# Mantido por: Joao Roberto Diego Petreche (v1.2.0)
# ==============================================================================

# Definição dos Projetos
GENAI_PROJECT="gen-lang-client-0464475716"
EPLUS_PROJECT="eplus-colab-cloud"
USER_EMAIL="joao.petreche@gmail.com"

echo "==> [1/7] Validando infraestrutura do Google Cloud..."
if ! command -v gcloud &> /dev/null; then
    curl https://sdk.cloud.google.com | bash -s -- --disable-prompts
    source /home/codespace/google-cloud-sdk/path.bash.inc
else
    echo "    - Google Cloud SDK detectado."
fi

echo "==> [2/7] Instalando componentes necessários (Beta)..."
gcloud components install beta --quiet

echo "==> [3/7] Vinculando Identidade Digital e Projetos..."
gcloud config set account $USER_EMAIL
gcloud config set project $GENAI_PROJECT

echo "==> [4/7] Habilitando APIs críticas em ambos os projetos..."
# Inclui BigQuery para análise de faturamento programática
for PROJ in $GENAI_PROJECT $EPLUS_PROJECT; do
    echo "    - Configurando projeto: $PROJ"
    gcloud services enable cloudbilling.googleapis.com --project=$PROJ
    gcloud services enable aiplatform.googleapis.com --project=$PROJ
    gcloud services enable bigquery.googleapis.com --project=$PROJ
done

echo "==> [5/7] Gerenciando Ambiente Virtual (venv)..."
# Resolve o erro de 'externally-managed-environment'[cite: 1]
if [ ! -d ".venv" ]; then
    echo "    - Criando novo ambiente virtual..."
    python3 -m venv .venv
fi
source .venv/bin/activate
echo "    - Ambiente virtual (.venv) ativo."

echo "==> [6/7] Sincronizando bibliotecas (requirements.txt)..."
# Garante que google-cloud-bigquery e pandas estejam presentes[cite: 7]
pip install --upgrade pip -q
pip install -q -r requirements.txt

echo "==> [7/7] Verificação de Credenciais de Aplicação (ADC)..."
if [ ! -f ~/.config/gcloud/application_default_credentials.json ]; then
    echo "    - REQUERIDO: Execute o comando abaixo para autorizar o acesso aos dados:"
    echo "      gcloud auth application-default login --scopes='https://www.googleapis.com/auth/cloud-platform'"
else
    echo "    - Credenciais ADC prontas para uso."
fi

# --- VERIFICAÇÃO DE FATURAMENTO ---
echo "------------------------------------------------------------"
echo "Relatório Financeiro: Scientific AI Engineering..."
# Executa os scripts dentro do venv[cite: 1, 8]
if python3 check_billing.py && python3 analise_faturamento_real.py; then
    echo "Saúde financeira da infraestrutura validada."
else
    echo "Nota: Se o dataset 'faturamento_v1' for novo, os dados podem levar 24h para aparecer."[cite: 4]
fi
echo "------------------------------------------------------------"

echo -e "\n[OK] Ambiente v1.2.0 pronto. Lembre-se: use 'source .venv/bin/activate' ao iniciar."
