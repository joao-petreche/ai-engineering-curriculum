"""
Script básico de automação EnergyPlus usando Eppy.
Mês 1 - Exercício 1.3

Este script permite executar simulações EnergyPlus via Python,
sem necessidade de abrir a interface gráfica.
"""

from pathlib import Path
from eppy.modeleditor import IDF
import pandas as pd
import sys

# Configurações do EnergyPlus
ENERGYPLUS_DIR = Path("C:/EnergyPlusV24-1-0")
IDD_FILE = ENERGYPLUS_DIR / "Energy+.idd"

def initialize_idd():
    """Inicializa arquivo IDD do EnergyPlus"""
    if not IDD_FILE.exists():
        print(f"❌ Arquivo IDD não encontrado: {IDD_FILE}")
        print(f"   Verifique se EnergyPlus está instalado em: {ENERGYPLUS_DIR}")
        sys.exit(1)
    
    IDF.setiddname(str(IDD_FILE))
    print(f"✅ IDD carregado: {IDD_FILE.name}")

def run_simulation(idf_path, weather_path, output_dir):
    """
    Executa simulação EnergyPlus via Eppy.
    
    Args:
        idf_path: Caminho para arquivo .idf
        weather_path: Caminho para arquivo .epw
        output_dir: Diretório de saída
    
    Returns:
        Path: Caminho para arquivo CSV de saída
    """
    
    print(f"\n🔄 Iniciando simulação...")
    print(f"📄 Arquivo IDF: {idf_path}")
    print(f"🌦️  Weather: {weather_path}")
    
    # Validar arquivos de entrada
    idf_path = Path(idf_path)
    weather_path = Path(weather_path)
    
    if not idf_path.exists():
        print(f"❌ Arquivo IDF não encontrado: {idf_path}")
        sys.exit(1)
    
    if not weather_path.exists():
        print(f"❌ Arquivo weather não encontrado: {weather_path}")
        sys.exit(1)
    
    # Criar diretório de saída
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Carregar arquivo IDF
        print("📂 Carregando arquivo IDF...")
        idf = IDF(str(idf_path), str(weather_path))
        
        # Executar simulação
        print("⚙️  Executando simulação (pode levar 30s-2min)...")
        idf.run(output_directory=str(output_dir))
        
        print(f"✅ Simulação concluída!")
        print(f"📁 Outputs em: {output_dir.absolute()}")
        
        # Verificar arquivo de saída
        csv_output = output_dir / "eplusout.csv"
        if csv_output.exists():
            file_size = csv_output.stat().st_size / 1024  # KB
            print(f"✅ CSV gerado: {csv_output.name} ({file_size:.1f} KB)")
        else:
            print(f"❌ CSV não encontrado!")
            print(f"   Verifique arquivo de erros: {output_dir / 'eplusout.err'}")
            return None
        
        return csv_output
    
    except Exception as e:
        print(f"❌ Erro durante simulação: {e}")
        return None

def preview_results(csv_path, n_rows=5):
    """
    Mostra preview dos resultados da simulação.
    
    Args:
        csv_path: Caminho para CSV de saída
        n_rows: Número de linhas para exibir
    """
    if csv_path is None or not csv_path.exists():
        print("⚠️  Não foi possível carregar resultados")
        return
    
    try:
        print(f"\n📊 Preview dos resultados ({n_rows} primeiras linhas):")
        print("-" * 80)
        
        df = pd.read_csv(csv_path)
        print(f"\nDimensões: {df.shape[0]} linhas × {df.shape[1]} colunas")
        print(f"\nColunas disponíveis:")
        for i, col in enumerate(df.columns[:10], 1):  # Mostra até 10 colunas
            print(f"  {i}. {col}")
        
        if len(df.columns) > 10:
            print(f"  ... e mais {len(df.columns) - 10} colunas")
        
        print(f"\n{df.head(n_rows).to_string()}")
        
    except Exception as e:
        print(f"❌ Erro ao ler CSV: {e}")

def main():
    """Função principal"""
    print("="*80)
    print("AUTOMAÇÃO ENERGYPLUS - MÊS 1, EXERCÍCIO 1.3")
    print("="*80)
    
    # Inicializar IDD
    initialize_idd()
    
    # Caminhos padrão
    idf_file = ENERGYPLUS_DIR / "ExampleFiles/1ZoneUncontrolled.idf"
    weather_file = ENERGYPLUS_DIR / "WeatherData/USA_CO_Golden-NREL.724666_TMY3.epw"
    output_directory = Path("output/mes1_ex1_3")
    
    # Verificar se arquivos existem
    print(f"\n📋 Verificando arquivos de entrada...")
    print(f"   IDF: {'✅' if idf_file.exists() else '❌'} {idf_file.name}")
    print(f"   Weather: {'✅' if weather_file.exists() else '❌'} {weather_file.name}")
    
    # Executar simulação
    output_csv = run_simulation(idf_file, weather_file, output_directory)
    
    # Mostrar preview dos resultados
    if output_csv:
        preview_results(output_csv, n_rows=10)
        
        print(f"\n{'='*80}")
        print("✅ SIMULAÇÃO CONCLUÍDA COM SUCESSO!")
        print(f"{'='*80}")
        print(f"\n📁 Arquivos de saída em: {output_directory.absolute()}")
        print(f"\n💡 Próximo passo: Analisar resultados no Jupyter Notebook")
    else:
        print(f"\n{'='*80}")
        print("❌ SIMULAÇÃO FALHOU")
        print(f"{'='*80}")
        sys.exit(1)

if __name__ == "__main__":
    main()
