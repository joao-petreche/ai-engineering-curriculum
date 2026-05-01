#!/bin/bash

# ==============================================================================
# Configuração de Ambiente: Scientific AI Engineering (GCP/Codespaces)
# Mantido por: Joao Roberto Diego Petreche
# ==============================================================================

PROJECT_ID="gen-lang-client-0464475716"
USER_EMAIL="joao.petreche@gmail.com"

echo "==> [1/4] Validando infraestrutura do Google Cloud..."
if ! command -v gcloud &> /dev/null; then
    curl https://sdk.cloud.google.com | bash -s -- --disable-prompts
    source /home/codespace/google-cloud-sdk/path.bash.inc
else
    echo "    - Google Cloud SDK detectado."
fi

echo "==> [2/4] Vinculando Identidade Digital e Projeto..."
gcloud config set project $PROJECT_ID
gcloud config set account $USER_EMAIL

echo "==> [3/4] Sincronizando bibliotecas do Python..."
# Atualiza o pip e instala dependências sem carregar lixo de texto
python3 -m pip install --upgrade pip -q
python3 -m pip install -q -r requirements.txt

echo "==> [4/4] Verificação de Credenciais de Aplicação (ADC)..."
if [ ! -f ~/.config/gcloud/application_default_credentials.json ]; then
    echo "    - ALERTA: Execute 'gcloud auth application-default login'"
else
    echo "    - Credenciais ADC prontas para uso."
fi

echo -e "\n--- Status Atual do Ambiente ---"
gcloud config list core/project
gcloud config list core/account

echo -e "\n[OK] Ambiente pronto para o currículo de AI Engineering."
