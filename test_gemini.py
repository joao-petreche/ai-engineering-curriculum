import sys
from google import genai

# 1. Configuração de Ambiente (Baseado no padrão do demo.ipynb e colab_gemini_API.ipynb)
if 'google.colab' in sys.modules:
    from google.colab import auth
    auth.authenticate_user()
    print("--- Ambiente: Google Colab (Autenticado via auth) ---")
else:
    print("--- Ambiente: Codespace/Local (Autenticado via gcloud ADC) ---")

# 2. Inicialização do Cliente para o Projeto gen-lang-client-0464475716
# Usamos vertexai=True para garantir o uso da infraestrutura profissional do GCP
client = genai.Client(
    vertexai=True,
    project='gen-lang-client-0464475716',
    location='us-central1'
)

def list_and_test():
    try:
        # 3. Listagem de Modelos Disponíveis (Seguindo o padrão solicitado)
        print("\nModelos da família 'flash' disponíveis no seu projeto:")
        for m in client.models.list():
            if "flash" in m.name:
                print(f" - {m.name}")

        # 4. Teste de Geração de Conteúdo
        # Usamos o gemini-1.5-flash por ser a versão estável confirmada
        print("\n--- Testando Geração de Conteúdo ---")
        prompt = "Como professor da USP, explique a importância da IA científica na Engenharia Civil."

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )

        print(f"Resposta:\n{response.text}")

    except Exception as e:
        print(f"\nErro durante a execução: {e}")
        print("Dica: Verifique se o 'gcloud auth application-default login' foi concluído.")

if __name__ == "__main__":
    list_and_test()
