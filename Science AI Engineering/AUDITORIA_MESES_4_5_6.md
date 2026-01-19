# AUDITORIA: MESES 4, 5 e 6 (PIML Surrogates, Prompt Engineering, Co-Simulação)

**Data da Auditoria:** 16 Janeiro 2026  
**Auditor:** GitHub Copilot  
**Contexto:** Aluno completou Meses 1-3 (EnergyPlus, Python, Pydantic, batch simulations)

---

## MÊS 4: PIML Surrogates

### 🔴 GAPS CRÍTICOS

#### 1. **Matemática de Surrogates NÃO Explicada**
- **Gap:** Documento menciona "Physics-Informed ML" mas não explica a matemática:
  - Equação de transferência de calor: Q = U·A·ΔT
  - Como XGBoost aprende correlações físicas (decision trees vs equações)
  - Por que constraints físicos são importantes (Q ≥ 0, conservação de energia)
  - Diferença entre epistemic vs aleatoric uncertainty
- **Impacto:** Aluno pode treinar modelo "caixa preta" sem entender física subjacente
- **Solução:** Adicionar seção "Fundamentos Matemáticos de PIML" em Semana 1 (2-3h):
  ```markdown
  ### Fundamentos de Transferência de Calor e PIML
  
  **Equação Base (Lei de Fourier):**
  Q = -k·A·(dT/dx)
  
  **Features como variáveis físicas:**
  - k (condutividade) → conductivity_wall, conductivity_insulation
  - A (área) → função de WWR (Window-to-Wall Ratio)
  - dT → função de heating_setpoint, cooling_setpoint
  
  **Por que ML aprende física:**
  XGBoost cria splits baseados em thresholds de features. Exemplo:
  - IF insulation_thickness > 0.08m THEN Q ↓ 35%
  - Esta "rule" aproxima Q ∝ 1/R (resistência térmica)
  
  **Constraints Físicos (obrigatórios):**
  1. Q ≥ 0 (energia nunca negativa)
  2. Q_heating + Q_cooling = Q_total (conservação)
  3. 0 < U-value < 5.0 W/m²K (limites físicos de transmitância)
  ```

#### 2. **Dataset de 100 Simulações é INSUFICIENTE para ML Robusto**
- **Gap:** 100 amostras ÷ 80/20 split = 80 train, 20 test → underfitting grave
- **Impacto:** R² esperado (0.85-0.89) é otimista. Real: 0.60-0.75 com 100 amostras
- **Solução:** 
  - **Opção A (Rápida):** Usar Latin Hypercube Sampling (LHS) para 500 simulações (10h com paralelização)
  - **Opção B (Transfer Learning):** Usar dataset pré-treinado (e.g., DOE Commercial Reference Buildings) + fine-tune com 100 locais
  - **Adicionar ao Exercício 1.1:**
  ```python
  from pyDOE2 import lhs
  
  def generate_lhs_samples(n_samples=500, n_features=8):
      """Latin Hypercube Sampling para cobertura espaço paramétrico."""
      lhs_samples = lhs(n_features, samples=n_samples, criterion='maximin')
      # Escalar para ranges físicos
      # ...
  ```

#### 3. **Código XGBoost/MLP INCOMPLETO - Faltam 40% da Implementação**
- **Gap Específico:**
  - `train_xgboost.py` tem stub `load()` sem implementação (linha 900)
  - `mlp_surrogate.py` não existe (apenas mencionado)
  - `physics_constraints.py` tem TODO não resolvido (conservação energia)
  - `benchmark.py` não comparado
- **Impacto:** Aluno não consegue executar pipeline completo
- **Solução:** Fornecer códigos completos:
  ```python
  # physics_constraints.py (COMPLETAR)
  def enforce_energy_conservation(self, Q_heating, Q_cooling, Q_total, tolerance=0.05):
      """Constraint 3: Q_total = Q_heating + Q_cooling ± tolerance."""
      expected_total = Q_heating + Q_cooling
      deviation = abs(Q_total - expected_total) / expected_total
      
      if deviation > tolerance:
          # Ajustar proporcionalmente
          ratio = expected_total / Q_total
          Q_heating *= ratio
          Q_cooling *= ratio
          Q_total = Q_heating + Q_cooling
      
      return Q_heating, Q_cooling, Q_total
  ```

#### 4. **Validação Cruzada NÃO Implementada (K-Fold Stub)**
- **Gap:** Exercício 1.3 tem função `cross_validation_fold()` que apenas printa índices
- **Impacto:** Aluno não saberá se modelo generaliza (overfitting não detectado)
- **Solução:** Implementar K-Fold completo com métricas:
  ```python
  def cross_validation_evaluate(X, y, model_class, n_splits=5):
      kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
      scores = {'rmse': [], 'mae': [], 'r2': []}
      
      for train_idx, val_idx in kf.split(X):
          X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
          y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
          
          model = model_class()
          model.train(X_train, y_train)
          y_pred = model.predict(X_val)
          
          scores['rmse'].append(np.sqrt(mean_squared_error(y_val, y_pred)))
          scores['mae'].append(mean_absolute_error(y_val, y_pred))
          scores['r2'].append(r2_score(y_val, y_pred))
      
      return {k: (np.mean(v), np.std(v)) for k, v in scores.items()}
  ```

---

### 🟡 GAPS IMPORTANTES

#### 5. **Feature Importance Não Interpretada Fisicamente**
- **Gap:** XGBoost retorna importâncias mas não explica correlação com física
- **Solução:** Adicionar interpretação ao Exercício 2.1:
  ```markdown
  **Interpretação Física Esperada:**
  1. insulation_thickness (alta) → Maior isolamento = menor Q (correlação negativa forte)
  2. wwr (alta) → Mais janelas = maior ganho solar + infiltração (positiva)
  3. conductivity_wall (média) → Afeta U-value mas menos que isolamento
  4. infiltration_rate (alta) → Ventilação indesejada impacta carga térmica
  
  Se importâncias NÃO seguem física → revisar features ou dados
  ```

#### 6. **Uncertainty Quantification Muito Simplista**
- **Gap:** `predict_with_uncertainty()` usa ±10% arbitrário sem justificativa
- **Solução:** Usar métodos estatísticos:
  ```python
  # Quantile Regression para intervalos de confiança
  from sklearn.ensemble import GradientBoostingRegressor
  
  model_q05 = GradientBoostingRegressor(loss='quantile', alpha=0.05)
  model_q95 = GradientBoostingRegressor(loss='quantile', alpha=0.95)
  
  y_lower = model_q05.predict(X)
  y_upper = model_q95.predict(X)
  ```

#### 7. **Benchmark vs EnergyPlus NÃO Executado**
- **Gap:** `benchmark.py` mencionado mas não implementado
- **Solução:** Adicionar script funcional:
  ```python
  def benchmark_surrogate_vs_energyplus(surrogate, idf_path, test_params):
      results = []
      for params in test_params:
          # 1. Predição com surrogate (rápido)
          t0 = time.time()
          Q_surrogate = surrogate.predict([params])[0]
          t_surrogate = time.time() - t0
          
          # 2. Simulação com EnergyPlus (lento)
          t0 = time.time()
          Q_energyplus = run_energyplus_with_params(idf_path, params)
          t_energyplus = time.time() - t0
          
          error_pct = abs(Q_surrogate - Q_energyplus) / Q_energyplus * 100
          speedup = t_energyplus / t_surrogate
          
          results.append({
              'Q_surrogate': Q_surrogate,
              'Q_energyplus': Q_energyplus,
              'error_pct': error_pct,
              'speedup': speedup
          })
      
      return pd.DataFrame(results)
  ```

#### 8. **Falta Discussão de Limites do Surrogate**
- **Gap:** Não menciona quando surrogate falha (extrapolação fora de training range)
- **Solução:** Adicionar seção "Limitações" na Semana 4:
  ```markdown
  ### Quando NÃO Usar Surrogate:
  1. **Extrapolação:** Parâmetros fora de training range (e.g., WWR=80% se treinou até 60%)
  2. **Fenômenos não-lineares extremos:** Convecção natural em átrios de 20m altura
  3. **Mudanças de topologia:** Adicionar novo andar (geometria diferente)
  4. **Sistemas não treinados:** PCM (Phase Change Materials), BIPV (Building Integrated PV)
  
  **Estratégia:** Detectar extrapolação → fall back para EnergyPlus
  ```

---

### 🟢 MELHORIAS

#### 9. **Adicionar Visualização Residuais (Diagnóstico)**
```python
def plot_residuals(y_true, y_pred):
    residuals = y_true - y_pred
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1: Residuals vs Predicted
    axes[0].scatter(y_pred, residuals, alpha=0.5)
    axes[0].axhline(0, color='red', linestyle='--')
    axes[0].set_xlabel('Predicted Energy (kWh)')
    axes[0].set_ylabel('Residuals')
    axes[0].set_title('Residual Plot (detectar bias)')
    
    # Plot 2: Q-Q Plot (normalidade)
    from scipy.stats import probplot
    probplot(residuals, dist="norm", plot=axes[1])
    axes[1].set_title('Q-Q Plot (normalidade dos erros)')
    
    plt.tight_layout()
    plt.savefig('output/mes4_residual_analysis.png', dpi=300)
```

#### 10. **Feature Engineering Avançada (Opcional)**
- Adicionar features derivadas:
  ```python
  # U-value efetivo (combina múltiplas features)
  df['u_value_wall'] = 1 / (df['wall_thickness'] / df['conductivity_wall'] + 
                             df['insulation_thickness'] / df['conductivity_insulation'])
  
  # Compacidade (razão área/volume)
  df['compactness'] = df['surface_area'] / df['zone_volume']
  
  # Interaction terms (WWR × orientação)
  df['wwr_south_interaction'] = df['wwr'] * df['wall_area_south']
  ```

---

### ✅ PONTOS FORTES

1. **Estrutura Pedagógica Clara:** Progressão Semana 1→4 bem definida
2. **Checkpoints de Validação:** Cada exercício tem critério de sucesso explícito
3. **Pydantic para Data Models:** Validação automática (continuidade do Mês 2)
4. **Git Workflow:** Commits, branches mencionados em múltiplos pontos
5. **Estimativas de Tempo Realistas:** 50-60h para Mês 4 é apropriado

---

## MÊS 5: Prompt Engineering

### 🔴 GAPS CRÍTICOS

#### 1. **Vertex AI Setup INCOMPLETO - Falta Tutorial de Autenticação**
- **Gap:** Documento assume GCP já configurado mas não ensina:
  - Criar projeto GCP
  - Habilitar Vertex AI API
  - Gerar Service Account Key
  - Configurar IAM permissions
  - Configurar billing alerts
- **Impacto:** Aluno gasta 4-6h debuggando autenticação (erro 403/401)
- **Solução:** Adicionar Seção 0 (Pré-Semana 1):
  ```markdown
  ## Seção 0: Setup Completo de Vertex AI (3-4h)
  
  ### Passo 1: Criar Projeto GCP
  ```bash
  gcloud projects create piml-training-$(date +%Y%m) --name="PIML Training"
  gcloud config set project piml-training-202601
  ```
  
  ### Passo 2: Habilitar APIs
  ```bash
  gcloud services enable aiplatform.googleapis.com
  gcloud services enable cloudbilling.googleapis.com
  ```
  
  ### Passo 3: Criar Service Account
  ```bash
  gcloud iam service-accounts create vertex-ai-user \
      --display-name="Vertex AI User"
  
  gcloud projects add-iam-policy-binding piml-training-202601 \
      --member="serviceAccount:vertex-ai-user@piml-training-202601.iam.gserviceaccount.com" \
      --role="roles/aiplatform.user"
  
  gcloud iam service-accounts keys create vertex-key.json \
      --iam-account=vertex-ai-user@piml-training-202601.iam.gserviceaccount.com
  ```
  
  ### Passo 4: Configurar Python
  ```bash
  export GOOGLE_APPLICATION_CREDENTIALS="vertex-key.json"
  pip install google-cloud-aiplatform
  ```
  
  ### Passo 5: Budget Alert
  ```bash
  gcloud billing budgets create --billing-account=XXXXX \
      --display-name="Vertex AI Budget" \
      --budget-amount=5.00 \
      --threshold-rule=percent=50 \
      --threshold-rule=percent=90
  ```
  ```

#### 2. **Few-Shot Examples SÃO ARTIFICIAIS - Faltam Casos Reais BPS**
- **Gap:** 5 examples no Exercício 1.3 são bem escritos mas:
  - Nunca mostram erros comuns de LLM (e.g., confundir R-value com U-value)
  - Não incluem corner cases (e.g., "Como reduzir energia em 80%?" → resposta deve explicar inviabilidade)
  - Faltam exemplos de cálculos intermediários (e.g., Q = U·A·ΔT com substituição numérica)
- **Impacto:** LLM aprende padrão mas não rigor técnico
- **Solução:** Adicionar 3 examples problemáticos + correção:
  ```python
  # Example 6: Cálculo explícito (ensinar LLM a mostrar work)
  builder.add_example(
      user_input="Calcular U-value de parede com 20cm concreto + 10cm EPS",
      expected_output="""Cálculo passo-a-passo:
  
  CAMADAS:
  1. Concreto: e₁=0.20m, λ₁=1.75 W/mK → R₁ = e₁/λ₁ = 0.20/1.75 = 0.114 m²K/W
  2. EPS: e₂=0.10m, λ₂=0.035 W/mK → R₂ = e₂/λ₂ = 0.10/0.035 = 2.857 m²K/W
  3. Resistências superficiais (ISO 6946): Rsi=0.13, Rse=0.04
  
  RESISTÊNCIA TOTAL:
  R_total = Rsi + R₁ + R₂ + Rse = 0.13 + 0.114 + 2.857 + 0.04 = 3.141 m²K/W
  
  U-VALUE:
  U = 1/R_total = 1/3.141 = 0.318 W/m²K
  
  INTERPRETAÇÃO: Excelente isolamento (U < 0.50). Atende ASHRAE 90.1 Climate Zone 3.""",
      reasoning="Mostra álgebra explícita + unidades em cada passo + interpretação normativa"
  )
  
  # Example 7: Corrigir erro comum (R-value vs U-value)
  builder.add_example(
      user_input="Janela com U-value de 5.0 é boa para São Paulo?",
      expected_output="""❌ NÃO. U-value de 5.0 W/m²K é MUITO ALTO (baixa resistência térmica).
  
  VALORES DE REFERÊNCIA (ASHRAE 90.1):
  - Janela single-pane: U ≈ 5.8 W/m²K (ruim)
  - Janela double-pane: U ≈ 2.8 W/m²K (médio)
  - Janela low-e double: U ≈ 1.8 W/m²K (bom)
  - Janela triple-pane: U ≈ 1.0 W/m²K (excelente)
  
  RECOMENDAÇÃO PARA SÃO PAULO (Climate Zone 3):
  - U ≤ 3.0 W/m²K (mínimo ASHRAE)
  - U ≤ 2.0 W/m²K (recomendado para eficiência)
  
  NOTA: R-value = 1/U-value. R alto = U baixo = melhor isolamento.""",
      reasoning="Corrige misconception comum + contextualiza com benchmark + recomendação geográfica"
  )
  ```

#### 3. **Hallucination Detection TEM FALSOS NEGATIVOS**
- **Gap:** `HallucinationDetector` (Exercício 2.4) verifica bounds mas não detecta:
  - **Unidades inconsistentes:** "condutividade 35" sem "W/mK" → assume 35 W/mK (erro 1000x)
  - **Cálculos errados:** "U=1.5 W/m²K com R=0.5 m²K/W" (deveria ser R=0.667)
  - **Citações fantasma:** "Segundo ASHRAE 90.1-2027" (norma do futuro)
  - **Dados fabricados:** "Estudo de Smith et al. (2025) mostrou 45% redução" (paper inexistente)
- **Solução:** Adicionar validações extras:
  ```python
  def check_unit_consistency(self, response: Dict) -> None:
      """Verifica se unidades estão explícitas."""
      params = response.get("parameters", {})
      units = response.get("units", {})
      
      for param_name, param_value in params.items():
          if param_name not in units:
              self.flags.append(HallucinationFlag(
                  hallucination_type=HallucinationType.UNIT_MISSING,
                  severity=4,
                  field=param_name,
                  detected_value=param_value,
                  expected_range="Must have unit in 'units' dict",
                  explanation="Physical quantity without unit is ambiguous"
              ))
  
  def check_calculation_consistency(self, response: Dict) -> None:
      """Verifica cálculos (se houver R e U)."""
      params = response.get("parameters", {})
      
      if "r_value" in params and "u_value" in params:
          r_val = params["r_value"]
          u_val = params["u_value"]
          expected_u = 1.0 / r_val if r_val > 0 else None
          
          if expected_u and abs(u_val - expected_u) / expected_u > 0.05:
              self.flags.append(HallucinationFlag(
                  hallucination_type=HallucinationType.CALCULATION_ERROR,
                  severity=5,
                  field="u_value",
                  detected_value=f"U={u_val}, R={r_val}",
                  expected_range=f"U should be 1/R = {expected_u:.3f}",
                  explanation="U-value and R-value are mathematically inconsistent"
              ))
  
  def check_citation_plausibility(self, response: Dict) -> None:
      """Detecta citações implausíveis."""
      refs = response.get("normative_references", [])
      current_year = 2026
      
      for ref in refs:
          # Extrair ano (regex simples)
          import re
          year_match = re.search(r'\b(19|20)\d{2}\b', ref)
          if year_match:
              year = int(year_match.group())
              if year > current_year:
                  self.flags.append(HallucinationFlag(
                      hallucination_type=HallucinationType.FABRICATED_CITATION,
                      severity=5,
                      field="normative_references",
                      detected_value=ref,
                      expected_range=f"Year ≤ {current_year}",
                      explanation="Citation from the future (likely fabricated)"
                  ))
  ```

#### 4. **Function Calling (Exercício 3.3) NÃO Integra com Surrogates do Mês 4**
- **Gap:** `gemini_function_calling.py` define tool abstrato mas não carrega modelos reais:
  ```python
  # STUB ATUAL (não funcional)
  def predict_energy_tool(wwr, insulation_thickness, ...):
      return {"energy_kwh": 120.0}  # Valor dummy
  ```
- **Impacto:** Aluno não vê integração real ML + LLM
- **Solução:** Integrar com pickle do Mês 4:
  ```python
  import pickle
  from pathlib import Path
  
  # Carregar surrogate treinado no Mês 4
  SURROGATE_PATH = Path("../mes4_piml_surrogates/models/xgboost_model.pkl")
  with open(SURROGATE_PATH, "rb") as f:
      xgb_model = pickle.load(f)
  
  def predict_energy_tool(wwr: float, wall_thickness: float, 
                         insulation_thickness: float, conductivity_wall: float,
                         conductivity_insulation: float, zone_volume: float,
                         infiltration_rate: float, internal_loads: float) -> dict:
      """Tool para Gemini: predizer energia usando surrogate XGBoost."""
      
      # Construir feature vector (ordem do treinamento)
      X = [[wwr, wall_thickness, insulation_thickness, conductivity_wall,
            conductivity_insulation, zone_volume, infiltration_rate, internal_loads]]
      
      # Predição
      Q_total = xgb_model.predict(X)[0]
      
      # Uncertainty (do Mês 4)
      uncertainty_pct = 10.0  # ±10% como definido
      Q_lower = Q_total * 0.9
      Q_upper = Q_total * 1.1
      
      return {
          "predicted_energy_kwh": round(Q_total, 2),
          "uncertainty_range": f"±{uncertainty_pct}%",
          "confidence_interval_95": f"[{Q_lower:.1f}, {Q_upper:.1f}] kWh",
          "model_type": "XGBoost Surrogate (trained on 100 EnergyPlus sims)",
          "execution_time_ms": 10  # Típico para XGBoost
      }
  ```

---

### 🟡 GAPS IMPORTANTES

#### 5. **Template Versionamento (Exercício 1.4) Sem Análise Estatística**
- **Gap:** `PromptVersionManager` registra métricas mas não analisa:
  - Significância estatística (t-test) entre versões
  - Correlação entre constraints_count e accuracy
  - Drift de performance ao longo do tempo
- **Solução:** Adicionar análise estatística:
  ```python
  from scipy.stats import ttest_ind
  
  def statistical_comparison(self, version_a: str, version_b: str) -> dict:
      """Compara duas versões com teste t."""
      metrics_a = [m for m in self.load_performance() if m['version_id'] == version_a]
      metrics_b = [m for m in self.load_performance() if m['version_id'] == version_b]
      
      quality_a = [m['response_quality'] for m in metrics_a]
      quality_b = [m['response_quality'] for m in metrics_b]
      
      t_stat, p_value = ttest_ind(quality_a, quality_b)
      
      return {
          "t_statistic": t_stat,
          "p_value": p_value,
          "significant": p_value < 0.05,
          "interpretation": f"Version {version_b} is {'significantly' if p_value < 0.05 else 'not significantly'} better than {version_a}"
      }
  ```

#### 6. **Cost Tracking (3.4) NÃO Alerta em Tempo Real**
- **Gap:** `CostTracker` calcula custos mas não para execução quando budget ≥ 90%
- **Solução:** Adicionar circuit breaker:
  ```python
  class CostTracker:
      def check_budget_before_call(self) -> bool:
          """Retorna False se budget exceeded."""
          if self.get_remaining_budget() < self.quota.monthly_budget * 0.05:
              print("🛑 BUDGET CRITICAL: Only 5% remaining. Stopping API calls.")
              return False
          return True
  ```

#### 7. **Streaming (3.2) Sem Handling de Conexão Interrompida**
- **Gap:** Código assume stream sempre completa, mas rede pode cair
- **Solução:** Adicionar retry em streaming:
  ```python
  def generate_stream_with_retry(self, prompt: str, max_retries: int = 3):
      for attempt in range(max_retries):
          try:
              for chunk in self.model.generate_content_stream(prompt):
                  yield chunk.text
              break  # Sucesso
          except Exception as e:
              if attempt == max_retries - 1:
                  raise
              print(f"Stream interrupted (attempt {attempt+1}), retrying...")
              time.sleep(2 ** attempt)
  ```

#### 8. **Falta Exemplo de Multi-Turn Conversation**
- **Gap:** Todos os examples são single-turn (user → LLM → done)
- **Solução:** Adicionar Exercício 4.2 com contexto:
  ```python
  class ConversationHistory:
      def __init__(self):
          self.history = []
      
      def add_turn(self, role: str, content: str):
          self.history.append({"role": role, "content": content})
      
      def build_context_prompt(self) -> str:
          """Constrói prompt com histórico."""
          context = "CONVERSATION HISTORY:\n"
          for turn in self.history:
              context += f"{turn['role']}: {turn['content']}\n"
          return context
  
  # Exemplo de uso
  history = ConversationHistory()
  history.add_turn("user", "Como reduzir resfriamento em 20%?")
  history.add_turn("assistant", "Recomendo aumentar isolamento para 10cm...")
  history.add_turn("user", "E se eu só puder usar 8cm?")
  # LLM agora tem contexto de "10cm" mencionado antes
  ```

---

### 🟢 MELHORIAS

#### 9. **Adicionar Prompt Debugging Tool**
```python
def debug_prompt_quality(prompt: str, response: str) -> dict:
    """Analisa qualidade de prompt/response."""
    
    analysis = {
        "prompt_length": len(prompt),
        "prompt_has_role": "ROLE:" in prompt,
        "prompt_has_constraints": "CONSTRAINT" in prompt,
        "prompt_has_examples": "EXAMPLE" in prompt or "Example" in prompt,
        
        "response_length": len(response),
        "response_has_numbers": bool(re.search(r'\d+', response)),
        "response_has_units": bool(re.search(r'W/m.?K|m²K/W|°C|kWh', response)),
        "response_has_citations": bool(re.search(r'ASHRAE|ISO|NBR', response)),
        "response_has_calculation": bool(re.search(r'=|→|\+|\-|\×', response))
    }
    
    # Scoring
    score = sum([
        analysis['prompt_has_role'],
        analysis['prompt_has_constraints'],
        analysis['prompt_has_examples'],
        analysis['response_has_numbers'],
        analysis['response_has_units'],
        analysis['response_has_citations'],
        analysis['response_has_calculation']
    ])
    
    analysis['quality_score'] = f"{score}/7"
    
    return analysis
```

#### 10. **Adicionar Token Counter para Otimização de Custo**
```python
import tiktoken

def count_tokens(text: str, model: str = "gpt-4") -> int:
    """Conta tokens (aproximação para Gemini)."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def optimize_prompt_tokens(prompt: str, max_tokens: int = 1000) -> str:
    """Reduz prompt se > max_tokens."""
    current_tokens = count_tokens(prompt)
    
    if current_tokens <= max_tokens:
        return prompt
    
    # Estratégias de redução
    # 1. Remover examples redundantes
    # 2. Abreviar constraints
    # 3. Usar bullet points em vez de parágrafos
    
    return prompt  # TODO: implementar compressão inteligente
```

---

### ✅ PONTOS FORTES

1. **Few-Shot Learning Bem Estruturado:** 5 examples progressivos de qualidade crescente
2. **Domain Constraints Abrangentes:** 16+ constraints em 5 categorias (physical, normative, operational, economic, technical)
3. **Hallucination Detection Robusto:** 5 tipos de violations detectadas
4. **Cost Tracking Detalhado:** Monitoramento de input/output tokens, predição mensal
5. **Streaming Implementado:** TTFT e TPS medidos corretamente

---

## MÊS 6: Co-Simulação

### 🔴 GAPS CRÍTICOS

#### 1. **Framework É APENAS DESIGN - ZERO IMPLEMENTAÇÃO REAL**
- **Gap Crítico:** TODO o mês é sobre:
  - "Design de arquitetura"
  - "Documentar interfaces"
  - "Criar diagramas UML"
  - "Especificar contratos"
  
  **MAS:** Nenhuma linha de código que realmente acopla EnergyPlus ↔ Gemini
- **Impacto:** Aluno passa 50-60h desenhando arquitetura mas não executa nada funcional
- **Solução:** **REESCREVER COMPLETAMENTE O MÊS 6** para:
  - **Semana 1:** Implementar adaptadores (EnergyPlus → Python, Surrogate → Python)
  - **Semana 2:** Criar `CoSimController` funcional (loop de otimização)
  - **Semana 3:** Integrar Gemini para geração de candidatos (function calling real)
  - **Semana 4:** End-to-end workflow: "Reduzir energia 20%" → parâmetros → otimização → relatório

#### 2. **UML Diagrams SÃO INÚTEIS para Implementação**
- **Gap:** PlantUML gera imagens bonitas mas não:
  - Gera código Python
  - Valida se arquitetura é implementável
  - Detecta acoplamentos indevidos (e.g., Gemini não deveria chamar EnergyPlus diretamente)
- **Impacto:** 8-10h desenhando diagramas que serão ignorados na implementação real
- **Solução:** Substituir UML por:
  - **Typed Python Interfaces (Protocol):**
  ```python
  from typing import Protocol, runtime_checkable
  
  @runtime_checkable
  class Simulator(Protocol):
      """Interface que TODOS os simuladores devem implementar."""
      
      def simulate(self, params: BPSParameters) -> SimulationResult:
          ...
      
      def validate_parameters(self, params: BPSParameters) -> bool:
          ...
  
  # Agora mypy pode verificar se classes implementam corretamente
  ```

#### 3. **Data Exchange Protocols SEM Implementação de Serialização**
- **Gap:** Exercício 2.1 gera JSON schemas mas não mostra:
  - Como EnergyPlus (que usa IDF/CSV) se comunica via JSON
  - Como surrogates (pickle/torch) são serializados
  - Como Gemini recebe/envia dados (API format)
- **Solução:** Implementar adaptadores reais:
  ```python
  class EnergyPlusAdapter:
      """Adapta EnergyPlus IDF para/de JSON."""
      
      def params_to_idf(self, params: BPSParameters, idf_template: str) -> str:
          """Injeta parâmetros em template IDF."""
          idf = eppy.openidf(idf_template)
          
          # Modificar WWR
          for window in idf.idfobjects['FENESTRATIONSURFACE:DETAILED']:
              window.Area *= params.wwr / 0.40  # Base: 40%
          
          # Modificar isolamento
          for material in idf.idfobjects['MATERIAL']:
              if material.Name == 'Insulation':
                  material.Thickness = params.insulation_thickness_m
                  material.Conductivity = params.conductivity_insulation_W_mK
          
          # ... outras modificações
          
          return idf.idfstr()
      
      def idf_results_to_json(self, eso_path: str) -> SimulationResult:
          """Parseia ESO do EnergyPlus para JSON."""
          # Ler ESO (EnergyPlus SQL output)
          conn = sqlite3.connect(f"{eso_path}.sql")
          cursor = conn.cursor()
          
          # Query energia anual
          heating_kwh = cursor.execute(
              "SELECT Value FROM TabularDataWithStrings WHERE ReportName='AnnualBuildingUtilityPerformanceSummary' AND RowName='Heating'"
          ).fetchone()[0]
          
          # ... outras queries
          
          return SimulationResult(
              annual_heating_kwh=heating_kwh,
              # ...
          )
  ```

#### 4. **Optimization Loop NÃO DEFINIDO (Semana 3)**
- **Gap:** Documento diz "implementar feedback loops" mas:
  - Não especifica algoritmo (Grid Search? Bayesian Optimization? Genetic Algorithm?)
  - Não define critério de convergência (erro < 5%? max 10 iterações?)
  - Não mostra como Gemini sugere próximo candidato (prompt engineering para isso?)
- **Solução:** Implementar loop com Bayesian Optimization:
  ```python
  from skopt import gp_minimize
  from skopt.space import Real
  
  class BayesianOptimizationLoop:
      def __init__(self, controller: CoSimulationController, goal: OptimizationGoal):
          self.controller = controller
          self.goal = goal
          
          # Definir espaço de busca
          self.search_space = [
              Real(0.10, 0.60, name='wwr'),
              Real(0.05, 0.20, name='insulation_thickness_m'),
              Real(0.3, 2.0, name='infiltration_rate_ACH'),
              # ... outros parâmetros
          ]
      
      def objective_function(self, x):
          """Função a minimizar (energia)."""
          # Construir parâmetros
          params = BPSParameters(
              wwr=x[0],
              insulation_thickness_m=x[1],
              infiltration_rate_ACH=x[2],
              # ... defaults para outros
          )
          
          # Simular com surrogate (rápido)
          result = self.controller.simulate(params, use_surrogate=True)
          
          # Retornar métrica a minimizar
          if self.goal.target_metric == 'total_energy_kwh':
              return result.total_energy_kwh
      
      def optimize(self, n_iterations: int = 20) -> BPSParameters:
          """Executa otimização."""
          result = gp_minimize(
              func=self.objective_function,
              dimensions=self.search_space,
              n_calls=n_iterations,
              random_state=42
          )
          
          # Construir parâmetros ótimos
          best_params = BPSParameters(
              wwr=result.x[0],
              insulation_thickness_m=result.x[1],
              infiltration_rate_ACH=result.x[2],
              # ...
          )
          
          # Validar com EnergyPlus (1 sim apenas)
          validated_result = self.controller.simulate(best_params, use_surrogate=False)
          
          return best_params, validated_result
  ```

---

### 🟡 GAPS IMPORTANTES

#### 5. **Roadmap (Semana 4) É Muito Vago**
- **Gap:** Diz "Phase 1: Prototipagem, Phase 2: Validação" mas não especifica:
  - Quais features em cada phase
  - KPIs de sucesso (e.g., "95% accuracy vs EnergyPlus")
  - Milestones com datas
- **Solução:** Roadmap detalhado:
  ```markdown
  ## Roadmap Técnico Detalhado
  
  ### Q1 2026: Prototipagem (Jan-Mar)
  **Objetivo:** MVP funcional com surrogate + Gemini
  
  **Milestones:**
  - [Jan 31] M1: Surrogates treinados (R² > 0.85) ✅ (Mês 4)
  - [Feb 15] M2: Gemini integration com function calling ✅ (Mês 5)
  - [Feb 28] M3: CoSimController executa loop básico (10 iterações)
  - [Mar 15] M4: UI conversacional (Streamlit) permite queries em linguagem natural
  
  **KPIs:**
  - Accuracy: Surrogate vs EnergyPlus < 8% error
  - Latency: Query → resultado < 5 segundos
  - Cost: < $2/dia com 50 queries
  
  ### Q2 2026: Validação (Apr-Jun)
  **Objetivo:** Validar com edifícios reais
  
  **Milestones:**
  - [Apr 30] M5: Calibração com dados de 3 edifícios reais (sensores)
  - [May 31] M6: Testes A/B com 10 engenheiros (usability)
  - [Jun 30] M7: Publicação: "LLM-Assisted BPS Optimization" (submetido)
  
  **KPIs:**
  - Calibration: CVRMSE < 15% (ASHRAE Guideline 14)
  - User satisfaction: SUS score > 70
  - Performance: 20% reduction in optimization time vs manual
  ```

#### 6. **Falta Handling de Falhas em Produção**
- **Gap:** Não menciona:
  - O que fazer se EnergyPlus crashar (IDF inválido)
  - O que fazer se Gemini retornar JSON malformado
  - O que fazer se surrogate extrapolar (fora de training range)
- **Solução:** Adicionar error handling robusto:
  ```python
  class CoSimController:
      def simulate_with_fallback(self, params: BPSParameters) -> SimulationResult:
          """Simula com fallback: surrogate → EnergyPlus se falhar."""
          
          # Tentativa 1: Surrogate (rápido)
          try:
              result = self.surrogate_simulator.simulate(params)
              
              # Verificar se extrapolou
              if self.is_extrapolation(params):
                  print("⚠️  Extrapolation detected, falling back to EnergyPlus")
                  raise ExtrapolationError()
              
              return result
          
          except (ExtrapolationError, Exception) as e:
              print(f"⚠️  Surrogate failed: {e}, using EnergyPlus")
              
              # Tentativa 2: EnergyPlus (lento mas confiável)
              try:
                  result = self.energyplus_simulator.simulate(params)
                  return result
              
              except Exception as e2:
                  print(f"❌ EnergyPlus also failed: {e2}")
                  
                  # Fallback final: retornar resultado "safe" com erro máximo
                  return SimulationResult(
                      simulation_id=f"failed_{uuid.uuid4()}",
                      simulation_type=SimulationType.ENERGYPLUS,
                      parameters=params,
                      annual_heating_kwh=np.nan,
                      annual_cooling_kwh=np.nan,
                      total_energy_kwh=np.nan,
                      uncertainty_percent=100.0,  # 100% incerteza = "não sabemos"
                      execution_time_s=0.0,
                      # ...
                  )
  ```

#### 7. **Observer Pattern (Design Patterns) Desnecessariamente Complexo**
- **Gap:** Exercício 1.3 implementa Observer para "eventos de simulação" mas:
  - Para uso local (não distribuído), callbacks simples são suficientes
  - Observer adiciona complexidade sem benefício (over-engineering)
- **Solução:** Simplificar para callbacks:
  ```python
  class CoSimController:
      def __init__(self, on_iteration_complete: Optional[Callable] = None):
          self.on_iteration_complete = on_iteration_complete
      
      def run_optimization(self):
          for i in range(max_iterations):
              result = self.simulate(...)
              
              # Callback simples
              if self.on_iteration_complete:
                  self.on_iteration_complete(iteration=i, result=result)
  
  # Uso
  def print_progress(iteration, result):
      print(f"Iteration {iteration}: Energy = {result.total_energy_kwh} kWh")
  
  controller = CoSimController(on_iteration_complete=print_progress)
  ```

#### 8. **JSON Schema Validation Repetitiva (Exercício 2.1)**
- **Gap:** Gera schemas manualmente mas Pydantic já faz isso
- **Solução:** Usar Pydantic diretamente:
  ```python
  # Em vez de gerar schema separadamente:
  schema = BPSParameters.model_json_schema()
  
  # Usar Pydantic para validação:
  try:
      params = BPSParameters.model_validate_json(json_string)
  except ValidationError as e:
      print(f"Invalid JSON: {e}")
  ```

---

### 🟢 MELHORIAS

#### 9. **Adicionar Diagrama de Deploy (Kubernetes/Docker)**
- Mês 6 menciona "deploy" mas não mostra arquitetura:
```yaml
# docker-compose.yml
version: '3.8'
services:
  cosim-api:
    image: cosim-api:latest
    ports:
      - "8000:8000"
    environment:
      - GOOGLE_APPLICATION_CREDENTIALS=/keys/vertex-key.json
      - ENERGYPLUS_PATH=/usr/local/EnergyPlus-24.1.0
    volumes:
      - ./models:/app/models
      - ./keys:/keys
  
  redis:
    image: redis:7
    ports:
      - "6379:6379"
```

#### 10. **Adicionar Metrics Dashboard (Prometheus + Grafana)**
```python
from prometheus_client import Counter, Histogram, start_http_server

# Métricas
simulation_counter = Counter('cosim_simulations_total', 'Total simulations')
simulation_duration = Histogram('cosim_simulation_duration_seconds', 'Simulation duration')
surrogate_accuracy = Histogram('cosim_surrogate_accuracy_percent', 'Surrogate accuracy')

class CoSimController:
    @simulation_duration.time()
    def simulate(self, params):
        simulation_counter.inc()
        result = ...
        return result

# Exportar métricas HTTP
start_http_server(8001)
```

---

### ✅ PONTOS FORTES

1. **Data Models Pydantic Bem Definidos:** BPSParameters, SimulationResult com validação automática
2. **Enum para Tipos de Simulação:** SimulationType.ENERGYPLUS vs SURROGATE_XGBOOST
3. **Constraints Documentados:** Validações (cooling > heating, total = heating + cooling)
4. **Estrutura Pedagógica:** Progressão clara (Semana 1 design → Semana 4 integration)

---

## PRIORIDADES CONSOLIDADAS (Meses 4-6)

### 🔴 CRÍTICO (Bloqueadores - Resolver AGORA)

| ID | Gap | Mês | Impacto | Tempo Fix | Prioridade |
|----|-----|-----|---------|-----------|-----------|
| C1 | Matemática de PIML não explicada | 4 | Aluno não entende física → ML caixa preta | 4h | 🔴🔴🔴🔴🔴 |
| C2 | Dataset 100 amostras insuficiente | 4 | R² real 0.60-0.75 vs esperado 0.85-0.89 | 12h | 🔴🔴🔴🔴 |
| C3 | Código XGBoost/MLP 40% incompleto | 4 | Pipeline não executa end-to-end | 8h | 🔴🔴🔴🔴🔴 |
| C4 | Validação cruzada stub (não funciona) | 4 | Overfitting não detectado | 3h | 🔴🔴🔴🔴 |
| C5 | Vertex AI setup sem tutorial | 5 | Aluno gasta 6h debuggando auth (403/401) | 5h | 🔴🔴🔴🔴🔴 |
| C6 | Few-shot examples artificiais | 5 | LLM não aprende rigor técnico | 4h | 🔴🔴🔴 |
| C7 | Hallucination detection com falsos negativos | 5 | Unidades/cálculos errados não detectados | 5h | 🔴🔴🔴🔴 |
| C8 | Function calling não integra surrogates | 5 | Gemini não chama modelos reais do Mês 4 | 4h | 🔴🔴🔴🔴 |
| C9 | Mês 6 é APENAS design (zero implementação) | 6 | 50-60h sem código funcional | 40h | 🔴🔴🔴🔴🔴 |
| C10 | Optimization loop não definido | 6 | Não sabe como otimizar (Grid? Bayesian?) | 8h | 🔴🔴🔴🔴 |

**Total Tempo para Resolver Críticos:** ~93 horas

---

### 🟡 IMPORTANTE (Dificultadores - Resolver em Q1)

| ID | Gap | Mês | Impacto | Tempo Fix |
|----|-----|-----|---------|-----------|
| I1 | Feature importance não interpretada fisicamente | 4 | Aluno não valida se modelo aprendeu física correta | 2h |
| I2 | Uncertainty quantification simplista (±10% arbitrário) | 4 | Intervalos de confiança não confiáveis | 4h |
| I3 | Benchmark vs EnergyPlus não executado | 4 | Não prova 1000x speedup | 4h |
| I4 | Limites do surrogate não discutidos | 4 | Aluno usa surrogate em extrapolação (erros graves) | 2h |
| I5 | Template versionamento sem análise estatística | 5 | Não sabe se versão B é realmente melhor que A | 3h |
| I6 | Cost tracking sem alerta em tempo real | 5 | Budget pode exceder sem alerta | 2h |
| I7 | Streaming sem retry em conexão interrompida | 5 | Falhas de rede quebram sistema | 2h |
| I8 | Falta exemplo multi-turn conversation | 5 | LLM não usa contexto de turnos anteriores | 3h |
| I9 | Roadmap muito vago (sem KPIs/datas) | 6 | Aluno não sabe o que entregar em cada fase | 4h |
| I10 | Falta error handling em produção | 6 | Crashes não tratados (IDF inválido, JSON malformado) | 5h |

**Total Tempo para Resolver Importantes:** ~31 horas

---

### 🟢 MELHORIAS (Complementos - Opcional)

| ID | Melhoria | Mês | Benefício | Tempo |
|----|----------|-----|-----------|-------|
| M1 | Visualização de residuais (diagnóstico) | 4 | Detectar bias no modelo | 2h |
| M2 | Feature engineering avançada (U-value, compacidade) | 4 | Melhorar R² em 5-10% | 3h |
| M3 | Prompt debugging tool | 5 | Avaliar qualidade de prompt quantitativamente | 2h |
| M4 | Token counter para otimização de custo | 5 | Reduzir custos em 20-30% | 2h |
| M5 | Diagrama de deploy (Docker/K8s) | 6 | Facilitar produção | 3h |
| M6 | Metrics dashboard (Prometheus/Grafana) | 6 | Monitoramento em tempo real | 4h |

**Total Tempo para Melhorias:** ~16 horas

---

## PLANO DE AÇÃO RECOMENDADO

### FASE 1: Fixes Críticos (2 semanas, 93h)
**Objetivo:** Tornar Meses 4, 5 e 6 executáveis e funcionais

**Semana 1 (45h):**
1. **C1 (4h):** Adicionar seção "Fundamentos Matemáticos de PIML" no Mês 4
2. **C3 (8h):** Completar código XGBoost/MLP/constraints
3. **C4 (3h):** Implementar K-Fold funcional
4. **C5 (5h):** Tutorial completo de setup Vertex AI
5. **C6 (4h):** Adicionar 3 few-shot examples problemáticos
6. **C7 (5h):** Expandir hallucination detection (unidades, cálculos, citações)
7. **C8 (4h):** Integrar function calling com surrogates reais
8. **REVISÃO:** Testar todos os exercícios modificados (12h)

**Semana 2 (48h):**
9. **C2 (12h):** Gerar 500 simulações com LHS (Latin Hypercube)
10. **C9 (40h):** Reescrever Mês 6 com implementação real:
    - Semana 1: Adaptadores (EnergyPlus, Surrogate)
    - Semana 2: CoSimController funcional
    - Semana 3: Gemini integration real
    - Semana 4: End-to-end workflow

### FASE 2: Fixes Importantes (1 semana, 31h)
**Objetivo:** Melhorar qualidade e robustez

**Semana 3 (31h):**
1. I1-I4 (Mês 4): Interpretação física, uncertainty, benchmark, limites (12h)
2. I5-I8 (Mês 5): Análise estatística, alerts, retry, multi-turn (10h)
3. I9-I10 (Mês 6): Roadmap detalhado, error handling (9h)

### FASE 3: Melhorias (Opcional, 16h)
**Objetivo:** Extras para produção

M1-M6: Visualizações, features avançadas, debugging, deploy, monitoring

---

## RESUMO EXECUTIVO

### Status Atual (16 Jan 2026)

| Mês | Status | Bloqueadores Críticos | Dias de Atraso Estimado |
|-----|--------|----------------------|-------------------------|
| **Mês 4 (PIML)** | 🟡 60% funcional | 4 gaps críticos | +5 dias |
| **Mês 5 (Prompts)** | 🟡 70% funcional | 4 gaps críticos | +3 dias |
| **Mês 6 (Co-Sim)** | 🔴 10% funcional | 2 gaps críticos | +10 dias |

### Impacto no Aluno
- **Sem fixes:** Aluno completaria meses 4-6 mas com:
  - Modelos ML com accuracy 20-30% abaixo do esperado
  - LLM integration não funcional (auth errors, hallucinations não detectadas)
  - Co-simulação apenas em papel (0 código funcional)
  
- **Com fixes (Fase 1+2):** Aluno terá:
  - ✅ Surrogates com R² > 0.85 (500 amostras)
  - ✅ Gemini integration robusta (auth, hallucination detection, function calling)
  - ✅ Co-simulação executável end-to-end

### Recomendação Final
**🚨 PRIORIDADE MÁXIMA: Executar Fase 1 (93h) antes de aluno iniciar Mês 7**

Razão: Meses 7-12 dependem de:
- Surrogates funcionais (Mês 4)
- LLM integration robusta (Mês 5)
- Framework de co-simulação (Mês 6)

**Deadline crítico:** 30 Janeiro 2026 (2 semanas)

---

**Fim da Auditoria**
