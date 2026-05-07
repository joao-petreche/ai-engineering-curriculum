
# 📊 Observabilidade Financeira: Scientific AI Engineering

Este documento descreve a arquitetura e os procedimentos para o monitoramento de custos e créditos promocionais vinculados aos projetos de pesquisa no Google Cloud Platform (GCP).

## 1. Visão Geral da Infraestrutura
A gestão financeira é centralizada na **"Conta com Créditos Dev"** (ID: `018BDF-F25C35-6646B4`), que atende aos seguintes projetos[cite: 3, 6]:
*   **`gen-lang-client-0464475716`**: Focado em Gemini API e IA Generativa[cite: 3].
*   **`eplus-colab-cloud`**: Focado em simulações de eficiência energética (EnergyPlus)[cite: 3].

## 2. Fluxo de Dados de Faturamento
Para evitar surpresas no cartão de crédito e garantir o uso eficiente do saldo disponível (**R$ 59,53**), implementamos um pipeline de dados automatizado[cite: 3, 4]:

1.  **Cloud Billing**: O Google Cloud exporta diariamente os custos detalhados por SKU[cite: 4, 7].
2.  **BigQuery**: Os dados são armazenados no conjunto de dados `faturamento_v1` (Localização: `US`).
3.  **Tabelas de Referência**:
    *   `cloud_pricing_export`: Contém a lista global de preços e taxas de conversão[cite: 7].
    *   `gcp_billing_export_resource_v1_*`: Contém o consumo real por recurso e os créditos aplicados[cite: 4].

## 3. Monitoramento Programático
O controle é realizado via scripts Python executados no ambiente isolado `.venv`[cite: 1]:

*   **`check_billing.py`**: Valida o status das contas e o saldo residual de créditos[cite: 3].
*   **`analise_faturamento_real.py`**: Realiza consultas SQL no BigQuery para calcular o **Custo Líquido** (Gasto Bruto - Créditos).

### Execução do Relatório
```bash
# Ativar o ambiente virtual
source .venv/bin/activate

# Rodar a análise detalhada
python analise_faturamento_real.py
```

## 4. Gestão de Créditos Promocionais
O projeto utiliza um sistema de compensação automática onde o custo fixo (ex: Assinatura Gemini de **R$ 135,71**) é abatido pelos créditos de desenvolvedor[cite: 4].
*   **Custo Bruto**: Valor total dos serviços utilizados.
*   **Créditos**: Descontos promocionais aplicados automaticamente.
*   **Custo Líquido**: Valor real a ser faturado (Meta: **R$ 0,00** enquanto houver saldo)[cite: 4].

## 5. Alertas e Limites
*   **Teto de Alerta**: Configurado para **R$ 100,00**[cite: 3].
*   **Periodicidade**: Recomenda-se a execução do script de análise a cada 24 horas para acompanhar a propagação dos dados do BigQuery[cite: 4].

---

**Mantido por:** Joao Roberto Diego Petreche  
**Versão:** 1.0.0 (Maio/2026)
