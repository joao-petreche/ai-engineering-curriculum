import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# 1. Configurações Físicas (Parâmetros do Módulo 1.1)
# Baseado na equação: Q = U * A * (Text - Tint)
U_VALUE = 2.5       # W/m²K (Transmitância térmica simplificada)
AREA = 20.0         # m² (Área de troca térmica)
INTERNAL_GAINS = 100 # W (Cargas fixas: pessoas/equipamentos)
THERMAL_CAP = 500000 # J/K (Capacidade térmica da zona)

# 2. Geração de Clima Sintético (24 horas)
times = [datetime(2026, 5, 19, h) for h in range(24)]
temp_ext = 15 + 10 * np.sin(np.linspace(0, 2 * np.pi, 24) - np.pi/2) # Ciclo dia/noite

# 3. Loop de Simulação (Passo de tempo: 1 hora)
temp_int = [20.0] # Temperatura inicial interna
q_flux = []

for i in range(len(times)-1):
    delta_t = temp_ext[i] - temp_int[i]
    q_gain = (U_VALUE * AREA * delta_t) + INTERNAL_GAINS

    # Evolução da temperatura: dT = (Q / C) * dt
    new_temp = temp_int[i] + (q_gain / THERMAL_CAP) * 3600
    temp_int.append(new_temp)
    q_flux.append(q_gain)

q_flux.append(q_flux[-1]) # Ajuste de dimensão

# 4. Organização dos Dados (Pandas)
df = pd.DataFrame({
    'timestamp': times,
    'temp_ext': temp_ext,
    'temp_int': temp_int,
    'heat_flux_w': q_flux
})

# 5. Exportação e Visualização
df.to_csv('thermal_results.csv', index=False)
print("✅ Simulação concluída. Resultados salvos em 'thermal_results.csv'.")

plt.figure(figsize=(10, 5))
plt.plot(df['timestamp'], df['temp_ext'], label='Temp. Externa (°C)', linestyle='--')
plt.plot(df['timestamp'], df['temp_int'], label='Temp. Interna (°C)', linewidth=2)
plt.title('Simulação Térmica Básica - Módulo 1.1 (Poli-USP)')
plt.ylabel('Temperatura (°C)')
plt.legend()
plt.grid(True)
plt.savefig('thermal_plot.png')
plt.show()
