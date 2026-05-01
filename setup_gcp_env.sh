#!/bin/bash

# ==============================================================================
# Configuração de Ambiente: Scientific AI Engineering (GCP/Codespaces)
# Mantido por: Joao Roberto Diego Petreche (v1.1.0)
# ==============================================================================

# Definição dos Projetos
GENAI_PROJECT="gen-lang-client-0464475716"
EPLUS_PROJECT="eplus-colab-cloud"
USER_EMAIL="joao.petreche@gmail.com"

echo "==> [1/6] Validando infraestrutura do Google Cloud..."
if ! command -v gcloud &> /dev/null; then
    curl https://sdk.cloud.google.com | bash -s -- --disable-prompts
    source /home/codespace/google-cloud-sdk/path.bash.inc
else
    echo "    - Google Cloud SDK detectado."
fi

echo "==> [2/6] Instalando componentes necessários (Beta)..."
# Garante que os comandos de faturamento funcionem programaticamente[cite: 3]
gcloud components install beta --quiet

echo "==> [3/6] Vinculando Identidade Digital e Projetos..."
gcloud config set account $USER_EMAIL
# Define o projeto de IA como padrão, mas valida ambos[cite: 3]
gcloud config set project $GENAI_PROJECT

echo "==> [4/6] Habilitando APIs em ambos os projetos..."
for PROJ in $GENAI_PROJECT $EPLUS_PROJECT; do
    echo "    - Configurando projeto: $PROJ"
    gcloud services enable cloudbilling.googleapis.com --project=$PROJ
    gcloud services enable aiplatform.googleapis.com --project=$PROJ
    gcloud services enable storage.googleapis.com --project=$PROJ
done

echo "==> [5/6] Sincronizando bibliotecas do Python..."
python3 -m pip install --upgrade pip -q
python3 -m pip install -q -r requirements.txt

echo "==> [6/6] Verificação de Credenciais de Aplicação (ADC)..."
# Escopo expandido para permitir monitoramento de faturamento e IA[cite: 3]
if [ ! -f ~/.config/gcloud/application_default_credentials.json ]; then
    echo "    - REQUERIDO: Execute o comando abaixo para autorizar o faturamento:"
    echo "      gcloud auth application-default login --scopes='https://www.googleapis.com/auth/cloud-platform'"
else
    echo "    - Credenciais ADC prontas para uso."
fi

# --- VERIFICAÇÃO DE FATURAMENTO ---
echo "------------------------------------------------------------"
echo "Monitorando saúde financeira da infraestrutura híbrida..."
if python3 check_billing.py; then
    echo "Configuração de ambiente concluída para ambos os projetos."
else
    echo "Aviso: Verifique se a 'Cloud Billing API' está ativa nos dois projetos."
fi
echo "------------------------------------------------------------"

echo -e "\n--- Status Atual do Ambiente ---"
echo "Conta: $USER_EMAIL"
echo "Projeto Ativo (Quota): $GENAI_PROJECT"
echo "Projeto de Simulação: $EPLUS_PROJECT"

echo -e "\n[OK] Ambiente v1.1.0 pronto para o currículo de AI Engineering."
