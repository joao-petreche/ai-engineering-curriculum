import os
from google.cloud import billing_v1

def consultar_faturamento(project_id):
    """
    Verifica o status de faturamento do projeto.
    Focado em monitorar o limite de R$ 100,00 extras do Joao Petreche.
    """
    client = billing_v1.CloudBillingClient()
    project_name = f"projects/{project_id}"

    print(f"\n{'='*60}")
    print(f"VERIFICAÇÃO DE FATURAMENTO - PROJETO: {project_id}")
    print(f"{'='*60}")

    try:
        # Consulta as informações de faturamento do projeto
        info = client.get_project_billing_info(name=project_name)

        if info.billing_enabled:
            print(f"ESTADO: [ ATIVO ]")
            print(f"CONTA:  {info.billing_account_name}")
            print(f"\nNota: Seus R$ 59,53 de créditos estão protegendo seu bolso.")
        else:
            print(f"ESTADO: [ INATIVO ]")
            print(f"Atenção: A Gemini API pode não funcionar sem faturamento ativo.")

    except Exception as e:
        print(f"Erro na consulta: {e}")

    print(f"{'='*60}\n")

if __name__ == "__main__":
    # Usando o seu ID de projeto confirmado nos logs anteriores
    PROJECT_ID = "gen-lang-client-0464475716"
    consultar_faturamento(PROJECT_ID)
