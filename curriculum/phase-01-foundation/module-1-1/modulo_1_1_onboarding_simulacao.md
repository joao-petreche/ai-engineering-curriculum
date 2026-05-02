
## 🎓 Módulo 1.1: Onboarding e Primeira Simulação
**Objetivo:** Configurar o ambiente de laboratório virtual, validar a infraestrutura de nuvem e executar uma simulação térmica básica integrando física e código.

### 1. Preparação do Ambiente (Codespace)
Antes de iniciar, certifique-se de que você está operando dentro do container oficial do curso.
*   **Acesso:** Abra o repositório no GitHub e inicie um Codespace.
*   **Extensões:** Verifique se as extensões recomendadas (Python, Pylance, Gemini Code Assist, EnergyPlus Modelkit) estão ativas no menu lateral[cite: 1].

### 2. Automação de Infraestrutura
O laboratório utiliza um script centralizado para garantir que as variáveis de ambiente e faturamento estejam corretas. No terminal do VS Code, execute:

```bash
./setup_gcp_env.sh
```

**O que o script valida?**
*   **SDK do Google Cloud**: Configura o `PATH` para acesso imediato aos comandos de nuvem.
*   **Memória RAM**: Garante que o ambiente tenha pelo menos **3GB livres** para evitar falhas durante o uso de IAs e simuladores[cite: 3].
*   **FinOps**: Valida o projeto `gen-lang-client-0464475716` e garante que o custo líquido permaneça em **R$ 0,00** através dos créditos promocionais[cite: 3, 4].

### 3. Autenticação e IA
Para que as ferramentas de assistência (Gemini/Claude) funcionem, valide seu acesso:
1.  Execute `python test_gemini.py` para confirmar a conexão com a API de IA Generativa.
2.  Verifique se o chat lateral do **Gemini Code Assist** exibe seu nome de usuário e o projeto correto[cite: 1].

### 4. Executando a Primeira Simulação (BPS)
Nesta fase, utilizaremos o **EnergyPlus** para calcular a carga térmica de uma zona simples.

1.  **Localize os arquivos**: Abra a pasta `simulations/basic_zone/`.
2.  **Analise o modelo**: Use a extensão `energyplus-modelkit` para visualizar o arquivo `.idf` ou `.epJSON`.
3.  **Rode o script de integração**:
    ```bash
    python run_thermal_sim.py
    ```
4.  **Verifique os resultados**: O script deve gerar um arquivo `.csv` e um gráfico de temperatura interna $T_{int}$ versus temperatura externa $T_{ext}$, utilizando a equação fundamental de balanço de calor:

$$Q_{gain} = U \cdot A \cdot (T_{ext} - T_{int}) + Q_{internal}$$

### 5. Checkpoint de Entrega
*   Print do terminal confirmando a execução do `./setup_gcp_env.sh` com custo R$ 0.00[cite: 3].
*   Gráfico de saída da primeira simulação térmica.
*   Um breve parágrafo gerado com auxílio do **Gemini** explicando a diferença entre um simulador puramente físico e um modelo de IA.
