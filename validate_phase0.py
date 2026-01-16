"""
Script de Validação Automática - Fase 0: Infraestrutura
Scientific AI Engineering Training - 12 Meses

Este script valida todos os pré-requisitos antes do aluno iniciar o Mês 1.
Bloqueia progressão se componentes críticos estiverem faltando.

Autor: FAPESP Training Program
Data: MÊS 1 - SEMANA 3
"""

import sys
import subprocess
import platform
import json
from pathlib import Path
from typing import Dict, List, Tuple
import importlib.util

# Cores para output (funciona em Windows 10+ e Linux)
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header():
    """Imprime cabeçalho do script"""
    print(f"\n{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}VALIDAÇÃO AUTOMÁTICA - FASE 0: INFRAESTRUTURA{Colors.END}")
    print(f"{Colors.BOLD}Scientific AI Engineering Training (12 Meses){Colors.END}")
    print(f"{Colors.BOLD}{'='*70}{Colors.END}\n")

def check_python_version() -> Tuple[bool, str]:
    """Valida Python 3.10.x"""
    version = sys.version_info
    is_valid = version.major == 3 and version.minor == 10
    
    message = f"Python {version.major}.{version.minor}.{version.micro}"
    if is_valid:
        return True, f"✅ {message}"
    else:
        return False, f"❌ {message} (Requerido: Python 3.10.x)"

def check_pip() -> Tuple[bool, str]:
    """Valida pip instalado"""
    try:
        result = subprocess.run(
            ["pip", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.split()[1]
            return True, f"✅ pip {version}"
        return False, "❌ pip não encontrado"
    except Exception as e:
        return False, f"❌ Erro ao verificar pip: {str(e)}"

def check_python_package(package_name: str, import_name: str = None) -> Tuple[bool, str]:
    """Valida se pacote Python está instalado"""
    if import_name is None:
        import_name = package_name
    
    spec = importlib.util.find_spec(import_name)
    if spec is not None:
        try:
            module = importlib.import_module(import_name)
            version = getattr(module, '__version__', 'unknown')
            return True, f"✅ {package_name} {version}"
        except:
            return True, f"✅ {package_name} (versão não detectada)"
    return False, f"❌ {package_name} não instalado"

def check_energyplus() -> Tuple[bool, str]:
    """Valida EnergyPlus 24.1.0 instalado"""
    # Caminhos comuns de instalação
    possible_paths = [
        Path("C:/EnergyPlusV24-1-0"),
        Path("C:/Program Files/EnergyPlus-24-1-0"),
        Path.home() / "EnergyPlus-24-1-0"
    ]
    
    for path in possible_paths:
        if path.exists():
            exe = path / "energyplus.exe"
            if exe.exists():
                return True, f"✅ EnergyPlus 24.1.0 encontrado em {path}"
    
    return False, "❌ EnergyPlus 24.1.0 não encontrado (instalar em C:/EnergyPlusV24-1-0)"

def check_vscode_extension(extension_id: str, extension_name: str) -> Tuple[bool, str]:
    """Valida extensão VS Code instalada"""
    try:
        result = subprocess.run(
            ["code", "--list-extensions"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            extensions = result.stdout.lower().split('\n')
            if extension_id.lower() in extensions:
                return True, f"✅ {extension_name}"
            return False, f"❌ {extension_name} não instalada"
        return False, f"⚠️  VS Code não encontrado ou comando 'code' não disponível"
    except Exception as e:
        return False, f"⚠️  Erro ao verificar extensão: {str(e)}"

def check_git() -> Tuple[bool, str]:
    """Valida Git instalado"""
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip().split()[-1]
            return True, f"✅ Git {version}"
        return False, "❌ Git não encontrado"
    except Exception as e:
        return False, f"❌ Erro ao verificar Git: {str(e)}"

def check_git_config() -> Tuple[bool, str]:
    """Valida configuração Git (user.name e user.email)"""
    try:
        name_result = subprocess.run(
            ["git", "config", "user.name"],
            capture_output=True,
            text=True,
            timeout=5
        )
        email_result = subprocess.run(
            ["git", "config", "user.email"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if name_result.returncode == 0 and email_result.returncode == 0:
            name = name_result.stdout.strip()
            email = email_result.stdout.strip()
            if name and email:
                return True, f"✅ Git configurado ({name}, {email})"
        
        return False, "❌ Git não configurado (executar: git config --global user.name/email)"
    except Exception as e:
        return False, f"❌ Erro ao verificar config Git: {str(e)}"

def check_gcp_auth() -> Tuple[bool, str]:
    """Valida autenticação Google Cloud"""
    try:
        # Verifica gcloud instalado
        result = subprocess.run(
            ["gcloud", "version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            return False, "⚠️  gcloud CLI não instalado (opcional para Mês 3+)"
        
        # Verifica autenticação
        auth_result = subprocess.run(
            ["gcloud", "auth", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if "ACTIVE" in auth_result.stdout:
            return True, "✅ GCP autenticado"
        return False, "⚠️  GCP não autenticado (executar: gcloud auth login)"
    
    except FileNotFoundError:
        return False, "⚠️  gcloud CLI não instalado (opcional para Mês 3+)"
    except Exception as e:
        return False, f"⚠️  Erro ao verificar GCP: {str(e)}"

def check_github_copilot() -> Tuple[bool, str]:
    """Valida GitHub Copilot ativo (verifica arquivo de configuração)"""
    # VS Code config path
    if platform.system() == "Windows":
        config_path = Path.home() / "AppData/Roaming/Code/User/settings.json"
    else:
        config_path = Path.home() / ".config/Code/User/settings.json"
    
    if not config_path.exists():
        return False, "⚠️  VS Code settings.json não encontrado"
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
            
        # Verifica se Copilot está habilitado
        copilot_enabled = settings.get("github.copilot.enable", {})
        
        if copilot_enabled or "github.copilot" in str(settings):
            return True, "✅ GitHub Copilot configurado"
        
        return False, "⚠️  GitHub Copilot não detectado nas configurações"
    
    except Exception as e:
        return False, f"⚠️  Erro ao verificar Copilot: {str(e)}"

def run_validation() -> Dict[str, List[Tuple[bool, str]]]:
    """Executa todas as validações e retorna resultados"""
    results = {
        "CRÍTICO": [],
        "IMPORTANTE": [],
        "OPCIONAL": []
    }
    
    # === VALIDAÇÕES CRÍTICAS ===
    print(f"\n{Colors.BOLD}[1/3] VERIFICAÇÕES CRÍTICAS (Bloqueiam Progresso){Colors.END}")
    print("-" * 70)
    
    critical_checks = [
        ("Python 3.10.x", check_python_version()),
        ("pip", check_pip()),
        ("EnergyPlus 24.1.0", check_energyplus()),
        ("Git", check_git()),
        ("Git Config", check_git_config()),
    ]
    
    for name, (status, msg) in critical_checks:
        print(f"{msg}")
        results["CRÍTICO"].append((status, msg))
    
    # === BIBLIOTECAS PYTHON ===
    print(f"\n{Colors.BOLD}[2/3] BIBLIOTECAS PYTHON ESSENCIAIS{Colors.END}")
    print("-" * 70)
    
    packages = [
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("matplotlib", "matplotlib"),
        ("eppy", "eppy"),
        ("pydantic", "pydantic"),
        ("pytest", "pytest"),
    ]
    
    for pkg_name, import_name in packages:
        status, msg = check_python_package(pkg_name, import_name)
        print(f"{msg}")
        results["CRÍTICO"].append((status, msg))
    
    # === VALIDAÇÕES OPCIONAIS ===
    print(f"\n{Colors.BOLD}[3/3] FERRAMENTAS OPCIONAIS (Úteis mas não bloqueantes){Colors.END}")
    print("-" * 70)
    
    optional_checks = [
        ("VS Code Python", check_vscode_extension("ms-python.python", "Python Extension")),
        ("VS Code Pylance", check_vscode_extension("ms-python.vscode-pylance", "Pylance")),
        ("GitHub Copilot", check_github_copilot()),
        ("Google Cloud CLI", check_gcp_auth()),
    ]
    
    for name, (status, msg) in optional_checks:
        print(f"{msg}")
        results["OPCIONAL"].append((status, msg))
    
    return results

def print_summary(results: Dict[str, List[Tuple[bool, str]]]) -> bool:
    """Imprime resumo e retorna se validação passou"""
    print(f"\n{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}RESUMO DA VALIDAÇÃO{Colors.END}")
    print(f"{Colors.BOLD}{'='*70}{Colors.END}\n")
    
    critical_failed = sum(1 for status, _ in results["CRÍTICO"] if not status)
    critical_total = len(results["CRÍTICO"])
    
    important_failed = sum(1 for status, _ in results["IMPORTANTE"] if not status)
    important_total = len(results["IMPORTANTE"])
    
    optional_failed = sum(1 for status, _ in results["OPCIONAL"] if not status)
    optional_total = len(results["OPCIONAL"])
    
    print(f"Críticas:    {critical_total - critical_failed}/{critical_total} ✅")
    print(f"Importantes: {important_total - important_failed}/{important_total} ✅")
    print(f"Opcionais:   {optional_total - optional_failed}/{optional_total} ✅")
    
    # Determina status final
    if critical_failed == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ VALIDAÇÃO PASSOU!{Colors.END}")
        print(f"{Colors.GREEN}Você está pronto para iniciar o Mês 1.{Colors.END}\n")
        
        if optional_failed > 0:
            print(f"{Colors.YELLOW}⚠️  Algumas ferramentas opcionais estão faltando.{Colors.END}")
            print(f"{Colors.YELLOW}   Elas não são bloqueantes mas facilitam o aprendizado.{Colors.END}\n")
        
        return True
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ VALIDAÇÃO FALHOU!{Colors.END}")
        print(f"{Colors.RED}{critical_failed} verificação(ões) crítica(s) falharam.{Colors.END}")
        print(f"{Colors.RED}Corrija os problemas antes de prosseguir para o Mês 1.{Colors.END}\n")
        
        print(f"{Colors.BOLD}AÇÕES RECOMENDADAS:{Colors.END}\n")
        
        for status, msg in results["CRÍTICO"]:
            if not status:
                item = msg.split("❌")[1].strip() if "❌" in msg else msg
                if "Python 3.10" in item:
                    print(f"  • Instalar Python 3.10.x de python.org")
                elif "pip" in item:
                    print(f"  • Reinstalar Python com pip incluído")
                elif "EnergyPlus" in item:
                    print(f"  • Baixar EnergyPlus 24.1.0 de energyplus.net")
                elif "Git" in item and "config" not in item.lower():
                    print(f"  • Instalar Git de git-scm.com")
                elif "Git" in item and "config" in item.lower():
                    print(f"  • Executar: git config --global user.name 'Seu Nome'")
                    print(f"  • Executar: git config --global user.email 'seu@email.com'")
                elif "pandas" in item or "numpy" in item or "matplotlib" in item:
                    print(f"  • Executar: pip install pandas numpy matplotlib eppy pydantic pytest")
        
        print()
        return False

def main():
    """Função principal"""
    print_header()
    
    print(f"{Colors.BOLD}Este script valida sua infraestrutura da Fase 0.{Colors.END}")
    print(f"Verifique cada item abaixo cuidadosamente.\n")
    
    results = run_validation()
    passed = print_summary(results)
    
    # Salva resultados em arquivo JSON
    output_file = Path("validation_results.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "passed": passed,
            "timestamp": subprocess.run(["date"], capture_output=True, text=True).stdout.strip(),
            "results": {
                category: [(status, msg) for status, msg in checks]
                for category, checks in results.items()
            }
        }, f, indent=2, ensure_ascii=False)
    
    print(f"Resultados salvos em: {output_file.absolute()}\n")
    
    # Exit code
    sys.exit(0 if passed else 1)

if __name__ == "__main__":
    main()
