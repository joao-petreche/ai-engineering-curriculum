"""
Gerador de Dados de Sensor Sintéticos (Sujos)
Mês 3 - Big Data - Exercício 2.1

Este script gera dados de sensor de temperatura simulados com:
- Dados limpos (padrão sazonal)
- Outliers controlados (5-10%)
- Valores faltantes (2-5%)
- Ruído gaussiano
- Drift gradual

Objetivo: Praticar limpeza e tratamento de time series.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Configurações de geração
SEED = 42
np.random.seed(SEED)

# Parâmetros da série temporal
START_DATE = datetime(2023, 1, 1)
DAYS = 365
TIMESTEP_MINUTES = 15  # 4 amostras por hora
SAMPLES_PER_DAY = 24 * (60 // TIMESTEP_MINUTES)
TOTAL_SAMPLES = DAYS * SAMPLES_PER_DAY

# Parâmetros de temperatura (São Paulo como referência)
TEMP_MEAN_ANNUAL = 20.0  # °C
TEMP_AMPLITUDE_ANNUAL = 5.0  # Variação inverno-verão
TEMP_AMPLITUDE_DAILY = 8.0  # Variação dia-noite
TEMP_NOISE_STD = 0.5  # Ruído gaussiano

# Parâmetros de "sujeira" dos dados
OUTLIER_RATE = 0.07  # 7% outliers
MISSING_RATE = 0.03  # 3% missing
DRIFT_MAGNITUDE = 0.02  # Drift de 2°C ao longo do ano

def generate_clean_temperature_series():
    """
    Gera série temporal limpa de temperatura com padrões realistas.
    
    Returns:
        pd.DataFrame com colunas: timestamp, temperature_clean
    """
    print("📊 Gerando série temporal limpa...")
    
    # Criar timestamps
    timestamps = [START_DATE + timedelta(minutes=i * TIMESTEP_MINUTES) 
                  for i in range(TOTAL_SAMPLES)]
    
    temperatures = []
    
    for i, ts in enumerate(timestamps):
        # Componente anual (sazonal)
        day_of_year = ts.timetuple().tm_yday
        seasonal = TEMP_MEAN_ANNUAL + TEMP_AMPLITUDE_ANNUAL * np.sin(
            2 * np.pi * (day_of_year - 80) / 365  # Pico em março (verão)
        )
        
        # Componente diária
        hour_of_day = ts.hour + ts.minute / 60
        daily = TEMP_AMPLITUDE_DAILY * np.sin(
            2 * np.pi * (hour_of_day - 6) / 24  # Pico às 15h
        )
        
        # Ruído gaussiano
        noise = np.random.normal(0, TEMP_NOISE_STD)
        
        temp = seasonal + daily + noise
        temperatures.append(temp)
    
    df = pd.DataFrame({
        'timestamp': timestamps,
        'temperature_clean': temperatures
    })
    
    print(f"✅ Gerados {len(df)} pontos limpos")
    print(f"   Temperatura média: {df['temperature_clean'].mean():.2f}°C")
    print(f"   Min: {df['temperature_clean'].min():.2f}°C")
    print(f"   Max: {df['temperature_clean'].max():.2f}°C")
    
    return df

def add_outliers(df, rate=OUTLIER_RATE):
    """
    Adiciona outliers realistas aos dados.
    
    Tipos de outliers:
    1. Spike (erro de sensor momentâneo)
    2. Valores físicamente impossíveis (T > 60°C, T < -20°C)
    3. Plateau (sensor travado)
    
    Args:
        df: DataFrame com temperatura limpa
        rate: Taxa de outliers (0-1)
    
    Returns:
        DataFrame com coluna temperature_dirty
    """
    print(f"\n🔴 Adicionando outliers ({rate*100:.1f}% dos dados)...")
    
    df['temperature_dirty'] = df['temperature_clean'].copy()
    n_outliers = int(len(df) * rate)
    outlier_indices = np.random.choice(len(df), n_outliers, replace=False)
    
    outlier_types = []
    
    for idx in outlier_indices:
        outlier_type = np.random.choice(['spike', 'impossible', 'plateau'], 
                                        p=[0.5, 0.3, 0.2])
        outlier_types.append(outlier_type)
        
        if outlier_type == 'spike':
            # Spike temporário (±20°C do valor real)
            spike = np.random.uniform(-20, 20)
            df.loc[idx, 'temperature_dirty'] += spike
        
        elif outlier_type == 'impossible':
            # Valor físicamente impossível
            if np.random.rand() < 0.5:
                df.loc[idx, 'temperature_dirty'] = np.random.uniform(60, 100)  # Muito quente
            else:
                df.loc[idx, 'temperature_dirty'] = np.random.uniform(-30, -15)  # Muito frio
        
        elif outlier_type == 'plateau':
            # Sensor travado (5-10 timesteps consecutivos com mesmo valor)
            plateau_length = np.random.randint(5, 11)
            stuck_value = df.loc[idx, 'temperature_dirty']
            
            for offset in range(plateau_length):
                if idx + offset < len(df):
                    df.loc[idx + offset, 'temperature_dirty'] = stuck_value
    
    print(f"✅ Adicionados {n_outliers} outliers:")
    print(f"   Spikes: {outlier_types.count('spike')}")
    print(f"   Impossíveis: {outlier_types.count('impossible')}")
    print(f"   Plateaus: {outlier_types.count('plateau')}")
    
    return df

def add_missing_values(df, rate=MISSING_RATE):
    """
    Adiciona valores faltantes (NaN) aos dados.
    
    Args:
        df: DataFrame com temperatura suja
        rate: Taxa de missings (0-1)
    
    Returns:
        DataFrame com alguns NaN
    """
    print(f"\n⚪ Adicionando valores faltantes ({rate*100:.1f}% dos dados)...")
    
    n_missing = int(len(df) * rate)
    missing_indices = np.random.choice(len(df), n_missing, replace=False)
    
    df.loc[missing_indices, 'temperature_dirty'] = np.nan
    
    print(f"✅ Adicionados {n_missing} valores NaN")
    
    return df

def add_drift(df, magnitude=DRIFT_MAGNITUDE):
    """
    Adiciona drift gradual (descalibração do sensor ao longo do tempo).
    
    Args:
        df: DataFrame com temperatura suja
        magnitude: Magnitude do drift em °C
    
    Returns:
        DataFrame com drift aplicado
    """
    print(f"\n📉 Adicionando drift gradual ({magnitude}°C ao longo do ano)...")
    
    # Drift linear ao longo do ano
    drift = np.linspace(0, magnitude, len(df))
    
    # Aplicar drift apenas onde não há NaN
    mask = df['temperature_dirty'].notna()
    df.loc[mask, 'temperature_dirty'] += drift[mask]
    
    print(f"✅ Drift aplicado (incremento gradual de {magnitude}°C)")
    
    return df

def generate_metadata(df):
    """
    Gera metadados sobre os dados sujos para validação.
    
    Args:
        df: DataFrame final
    
    Returns:
        dict com estatísticas
    """
    metadata = {
        "generation_date": datetime.now().isoformat(),
        "seed": SEED,
        "total_samples": len(df),
        "time_range": {
            "start": df['timestamp'].min().isoformat(),
            "end": df['timestamp'].max().isoformat(),
            "days": DAYS
        },
        "clean_data": {
            "mean": float(df['temperature_clean'].mean()),
            "std": float(df['temperature_clean'].std()),
            "min": float(df['temperature_clean'].min()),
            "max": float(df['temperature_clean'].max())
        },
        "dirty_data": {
            "mean": float(df['temperature_dirty'].mean()),
            "std": float(df['temperature_dirty'].std()),
            "min": float(df['temperature_dirty'].min()),
            "max": float(df['temperature_dirty'].max()),
            "missing_count": int(df['temperature_dirty'].isna().sum()),
            "missing_rate": float(df['temperature_dirty'].isna().mean())
        },
        "contamination": {
            "outlier_rate": OUTLIER_RATE,
            "missing_rate": MISSING_RATE,
            "drift_magnitude": DRIFT_MAGNITUDE
        }
    }
    
    return metadata

def plot_comparison(df, output_path="output/sensor_data_comparison.png"):
    """
    Plota comparação entre dados limpos e sujos.
    
    Args:
        df: DataFrame com ambas as séries
        output_path: Caminho para salvar gráfico
    """
    print(f"\n📊 Gerando visualização...")
    
    # Selecionar apenas 7 dias para visualização (muitos pontos)
    days_to_plot = 7
    samples_to_plot = days_to_plot * SAMPLES_PER_DAY
    df_plot = df.head(samples_to_plot)
    
    fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
    
    # Plot 1: Dados limpos
    axes[0].plot(df_plot['timestamp'], df_plot['temperature_clean'], 
                 linewidth=1.5, color='#2E86AB', label='Limpo')
    axes[0].set_ylabel('Temperatura (°C)', fontsize=12)
    axes[0].set_title('Dados de Sensor - Série Limpa', fontsize=14, fontweight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Plot 2: Dados sujos
    axes[1].plot(df_plot['timestamp'], df_plot['temperature_dirty'], 
                 linewidth=1.5, color='#A23B72', label='Sujo (outliers + missing + drift)', 
                 alpha=0.7)
    axes[1].plot(df_plot['timestamp'], df_plot['temperature_clean'], 
                 linewidth=0.8, color='#2E86AB', label='Limpo (referência)', 
                 alpha=0.5, linestyle='--')
    axes[1].set_xlabel('Data/Hora', fontsize=12)
    axes[1].set_ylabel('Temperatura (°C)', fontsize=12)
    axes[1].set_title('Dados de Sensor - Série Suja', fontsize=14, fontweight='bold')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✅ Gráfico salvo em: {output_path.absolute()}")
    
    plt.close()

def main():
    """Função principal"""
    print("="*70)
    print("GERADOR DE DADOS DE SENSOR SINTÉTICOS (SUJOS)")
    print("Mês 3 - Big Data - Exercício 2.1")
    print("="*70)
    print()
    
    # Passo 1: Gerar dados limpos
    df = generate_clean_temperature_series()
    
    # Passo 2: Adicionar outliers
    df = add_outliers(df)
    
    # Passo 3: Adicionar valores faltantes
    df = add_missing_values(df)
    
    # Passo 4: Adicionar drift
    df = add_drift(df)
    
    # Passo 5: Gerar metadados
    metadata = generate_metadata(df)
    
    # Passo 6: Salvar arquivos
    output_dir = Path("output/mes3_sensor_data")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Salvar CSV
    csv_path = output_dir / "sensor_data_dirty.csv"
    df.to_csv(csv_path, index=False)
    print(f"\n💾 Dados salvos em: {csv_path.absolute()}")
    print(f"   Tamanho: {csv_path.stat().st_size / 1024:.1f} KB")
    
    # Salvar metadados
    import json
    metadata_path = output_dir / "metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"   Metadados: {metadata_path.absolute()}")
    
    # Passo 7: Plotar comparação
    plot_comparison(df, output_path=output_dir / "comparison.png")
    
    # Resumo final
    print(f"\n{'='*70}")
    print("✅ GERAÇÃO CONCLUÍDA COM SUCESSO!")
    print(f"{'='*70}")
    print(f"\n📊 Resumo:")
    print(f"   Total de amostras: {len(df):,}")
    print(f"   Período: {DAYS} dias ({DAYS/365:.2f} anos)")
    print(f"   Timestep: {TIMESTEP_MINUTES} minutos")
    print(f"   Outliers: {int(len(df) * OUTLIER_RATE):,} ({OUTLIER_RATE*100:.1f}%)")
    print(f"   Missing: {df['temperature_dirty'].isna().sum():,} ({MISSING_RATE*100:.1f}%)")
    print(f"   Drift: {DRIFT_MAGNITUDE}°C ao longo do ano")
    
    print(f"\n💡 Próximos passos:")
    print(f"   1. Abrir {csv_path.name} em Jupyter Notebook")
    print(f"   2. Implementar limpeza de outliers (Savitzky-Golay)")
    print(f"   3. Preencher valores faltantes (interpolação)")
    print(f"   4. Corrigir drift (detrending)")
    print(f"   5. Comparar com série limpa para validar")

if __name__ == "__main__":
    main()
