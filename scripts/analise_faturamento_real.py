from google.cloud import bigquery
import pandas as pd
from google.api_core.exceptions import NotFound

# Configurações extraídas do seu console
PROJECT_ID = "gen-lang-client-0464475716"
DATASET_ID = "faturamento_v1"
# Atualize esta linha com o ID real da sua imagem
TABLE_ID = "gcp_billing_export_resource_v1_018BDF_F25C35_6646B4"

client = bigquery.Client(project=PROJECT_ID)

def consultar_gasto_real():
    query = f"""
    SELECT
      service.description as servico,
      SUM(cost) as custo_bruto,
      SUM((SELECT SUM(amount) FROM UNNEST(credits))) as creditos,
      SUM(cost + (SELECT IFNULL(SUM(amount), 0) FROM UNNEST(credits))) as custo_liquido
    FROM
      `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    WHERE
      _PARTITIONDATE >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
    GROUP BY 1
    ORDER BY custo_liquido DESC
    """
    try:
        df = client.query(query).to_dataframe()
        return df
    except NotFound:
        return None

if __name__ == "__main__":
    print("--- 📊 Relatório de Custos: Scientific AI Engineering ---")

    dados = consultar_gasto_real()

    if dados is None:
        print(f"\n⏳ Aguardando processamento do Google Cloud...")
        print(f"O dataset '{DATASET_ID}' foi criado com sucesso em 01/05/2026.")
        print("A tabela de uso detalhado leva até 24h para aparecer após a ativação[cite: 4].")
    elif dados.empty:
        print("\n✅ Tabela encontrada, mas ainda sem registros para os últimos 30 dias.")
    else:
        print("\n✅ Dados de faturamento recuperados:")
        print(dados.to_string(index=False))
        total_pago = dados['custo_liquido'].sum()
        print(f"\n💰 Total líquido (cobrança real): R$ {total_pago:.2f}")
