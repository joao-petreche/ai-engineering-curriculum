#!/bin/bash

# ==============================================================================
# Configuração de Ambiente: Scientific AI Engineering (GCP/Codespaces)
# Mantido por: Joao Roberto Diego Petreche
# ==============================================================================

PROJECT_ID="gen-lang-client-0464475716"
USER_EMAIL="joao.petreche@gmail.com"

echo "==> [1/5] Validando infraestrutura do Google Cloud..."
if ! command -v gcloud &> /dev/null; then
    curl https://sdk.cloud.google.com | bash -s -- --disable-prompts
    source /home/codespace/google-cloud-sdk/path.bash.inc
else
    echo "    - Google Cloud SDK detectado."
fi

echo "==> [2/5] Vinculando Identidade Digital e Projeto..."
gcloud config set project $PROJECT_ID
gcloud config set account $USER_EMAIL

echo "==> [3/5] Habilitando APIs do Google Cloud..."
echo "    - Habilitando Cloud Billing API..."
gcloud services enable cloudbilling.googleapis.com --project=$PROJECT_ID
echo "    - Habilitando Vertex AI API..."
gcloud services enable aiplatform.googleapis.com --project=$PROJECT_ID
echo "    - Habilitando Cloud Storage API..."
gcloud services enable storage.googleapis.com --project=$PROJECT_ID

echo "==> [4/5] Sincronizando bibliotecas do Python..."
# Atualiza o pip e instala dependências sem carregar lixo de texto
python3 -m pip install --upgrade pip -q
python3 -m pip install -q -r requirements.txt

echo "==> [5/5] Verificação de Credenciais de Aplicação (ADC)..."
if [ ! -f ~/.config/gcloud/application_default_credentials.json ]; then
    echo "    - ALERTA: Execute 'gcloud auth application-default login'"
else
    echo "    - Credenciais ADC prontas para uso."
fi

# --- VERIFICAÇÃO DE FATURAMENTO ---
echo "------------------------------------------------------------"
echo "Monitorando saúde financeira do projeto..."
if python3 check_billing.py; then
    echo "Configuração de ambiente concluída com sucesso."
else
    echo "Aviso: Não foi possível validar o faturamento. Verifique as APIs."
fi
echo "------------------------------------------------------------"

echo -e "\n--- Status Atual do Ambiente ---"
gcloud config list core/project
gcloud config list core/account

echo -e "\n[OK] Ambiente pronto para o currículo de AI Engineering."
