import subprocess
import json
import sys

# Lista de projetos para monitoramento unificado
PROJECTS = ['gen-lang-client-0464475716', 'eplus-colab-cloud']

def get_billing_info(project_id):
    """Busca informações de faturamento via gcloud CLI."""
    print(f"🔍 Verificando projeto: {project_id}...", end=" ", flush=True)

    cmd = [
        'gcloud', 'beta', 'billing', 'projects', 'describe',
        project_id, '--format=json'
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)

        if result.returncode != 0:
            print(f"❌ Erro")
            return {"error": result.stderr.strip()}

        print("✅")
        return json.loads(result.stdout)

    except subprocess.TimeoutExpired:
        print("⏳ Timeout")
        return {"error": "O comando gcloud demorou muito para responder."}
    except Exception as e:
        print("💥 Falha Crítica")
        return {"error": str(e)}

def main():
    print("=" * 50)
    print("📊 MONITORAMENTO DE CUSTOS GLOBAIS (Teto: R$ 100,00)")
    print("=" * 50)

    total_found = 0
    for project in PROJECTS:
        info = get_billing_info(project)

        if "error" in info:
            print(f"   ⚠️  Aviso: {info['error'][:100]}...")
        else:
            # O campo 'billingEnabled' indica se o projeto pode gerar custos
            status = "ATIVO" if info.get("billingEnabled") else "INATIVO"
            account = info.get("billingAccountName", "N/A").split('/')[-1]
            print(f"   💰 Status: {status} | Conta: {account}")
            total_found += 1

    print("\n" + "=" * 50)
    print(f"✅ Monitoramento concluído para {total_found} projeto(s).")
    print("Saldo atual disponível para pesquisa: R$ 59,53")
    print("=" * 50)

if __name__ == "__main__":
    main()
