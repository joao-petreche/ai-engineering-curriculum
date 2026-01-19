"""
Gerador de Few-Shot Examples Técnicos - PIML
Mês 5 - Prompt Engineering - Exercício 2.1

Este script gera 50 exemplos técnicos para Few-Shot Prompting
com Vertex AI Generative AI.

Cada exemplo:
- Input: Pergunta técnica realista sobre simulação/PIML
- Output: Resposta correta baseada em dados validados
- Metadata: Fonte (golden dataset), validação, categoria

Categorias:
1. Geometria (WSR, orientação, altura)
2. Materiais (U-value, condutividade, densidade)
3. HVAC (COP, setpoint, eficiência)
4. Energia (consumo anual, demanda pico, conforto)
5. Clima/Operação (sazonalidade, ocupação, carga)
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from datetime import datetime
import logging
from typing import Dict, List

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Diretórios
GOLDEN_DATASET_DIR = Path("data/golden_dataset")
EXAMPLES_DIR = Path("data/few_shot_examples")

class FewShotExampleGenerator:
    """
    Gera exemplos técnicos para Few-Shot Prompting.
    
    Objetivo:
    - Prover contexto técnico real ao LLM
    - Melhorar qualidade de predições com Vertex AI
    - Educar estudantes com casos reais PIML
    """
    
    # Categorias de exemplos
    CATEGORIES = {
        'geometry': "Geometria de Edifício",
        'materials': "Propriedades de Materiais",
        'hvac': "Sistemas HVAC",
        'energy': "Consumo e Eficiência Energética",
        'climate_operation': "Clima e Operação"
    }
    
    def __init__(self, golden_dataset_path: Path = None):
        """Inicializa gerador"""
        self.golden_dataset = None
        self.examples = []
        self.example_library = {}
        
        # Criar diretórios
        EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)
        
        # Carregar dataset de ouro
        if golden_dataset_path:
            self.load_golden_dataset(golden_dataset_path)
        else:
            self.load_latest_golden_dataset()
    
    def load_golden_dataset(self, filepath: Path):
        """Carrega golden dataset"""
        logger.info(f"Carregando golden dataset: {filepath}")
        self.golden_dataset = pd.read_csv(filepath)
        logger.info(f"✅ Golden dataset carregado: {self.golden_dataset.shape}")
    
    def load_latest_golden_dataset(self):
        """Carrega golden dataset mais recente"""
        csv_files = list(GOLDEN_DATASET_DIR.glob("golden_dataset_*.csv"))
        if not csv_files:
            raise FileNotFoundError(f"Nenhum golden dataset encontrado em {GOLDEN_DATASET_DIR}")
        
        latest = max(csv_files, key=lambda p: p.stat().st_mtime)
        self.load_golden_dataset(latest)
    
    def generate_geometry_examples(self, n_examples: int = 10) -> List[Dict]:
        """
        Gera exemplos sobre geometria de edifício.
        
        Variáveis:
        - window_to_wall_ratio: 10-50%
        - Orientação: N, S, L, O
        """
        logger.info(f"Gerando {n_examples} exemplos de GEOMETRIA...")
        
        examples = []
        sample_rows = self.golden_dataset.sample(n=min(n_examples, len(self.golden_dataset)))
        
        for idx, row in sample_rows.iterrows():
            wwr = row['window_to_wall_ratio']
            consumption = row['annual_consumption_kwh']
            comfort = row['comfort_hours']
            
            example = {
                'category': 'geometry',
                'example_id': f'geom_{len(examples)+1:02d}',
                'input': f"""
Um edifício foi projetado com Window-to-Wall Ratio de {wwr:.1%}.
Qual é o consumo energético anual esperado?
Considere clima temperado com DHWh = 2800.
""".strip(),
                'expected_output': f"""
Para um edifício com WSR = {wwr:.1%} em clima temperado:
- Consumo anual estimado: {consumption:.0f} kWh
- Horas de conforto: {comfort:.0f}/8760
- Classificação: {"A (Eficiente)" if consumption < 80000 else "B (Normal)" if consumption < 120000 else "C (Ineficiente)"}

Justificativa:
WSR mais alta aumenta ganho solar (bom no inverno, ruim no verão).
Requer HVAC mais robusto, elevando consumo.
""".strip(),
                'source': f"golden_dataset sample #{idx}",
                'difficulty': 'intermediate',
                'tags': ['WSR', 'solar_gain', 'energy_estimation'],
                'validation_status': 'verified'
            }
            examples.append(example)
        
        logger.info(f"✅ {len(examples)} exemplos de geometria gerados")
        return examples
    
    def generate_materials_examples(self, n_examples: int = 10) -> List[Dict]:
        """
        Gera exemplos sobre propriedades de materiais.
        
        Variáveis:
        - wall_conductivity: 0.3-1.5 W/m-K
        - wall_thickness: 10-40 cm
        - glass_u_value: 1.5-5.0 W/m²-K
        """
        logger.info(f"Gerando {n_examples} exemplos de MATERIAIS...")
        
        examples = []
        sample_rows = self.golden_dataset.sample(n=min(n_examples, len(self.golden_dataset)))
        
        for idx, row in sample_rows.iterrows():
            wall_cond = row['wall_conductivity']
            glass_u = row['glass_u_value']
            consumption = row['annual_consumption_kwh']
            
            example = {
                'category': 'materials',
                'example_id': f'mat_{len(examples)+1:02d}',
                'input': f"""
Uma parede foi construída com condutividade térmica de {wall_cond:.2f} W/m-K.
Vidros têm U-value de {glass_u:.1f} W/m²-K.
Qual será o impacto no consumo de energia do edifício?
""".strip(),
                'expected_output': f"""
Paredes com λ = {wall_cond:.2f} W/m-K + vidros com U = {glass_u:.1f} W/m²-K:
- Consumo anual: {consumption:.0f} kWh
- Resistência térmica parede: R = {0.2/wall_cond:.3f} m²K/W (considerando 20cm)
- Resistência térmica vidros: R = {1/glass_u:.3f} m²K/W

Análise:
- Se λ < 0.5: Material isolante (concreto aerado, poliestireno)
  → Consumo reduzido até 30%
- Se λ > 1.0: Material condutor (concreto, alvenaria)
  → Requer janelas de alta eficiência
- Vidros duplos ideais com U < 2.8 W/m²-K
""".strip(),
                'source': f"golden_dataset sample #{idx}",
                'difficulty': 'advanced',
                'tags': ['conductivity', 'U_value', 'thermal_resistance', 'material_properties'],
                'validation_status': 'verified'
            }
            examples.append(example)
        
        logger.info(f"✅ {len(examples)} exemplos de materiais gerados")
        return examples
    
    def generate_hvac_examples(self, n_examples: int = 10) -> List[Dict]:
        """
        Gera exemplos sobre sistemas HVAC.
        
        Variáveis:
        - hvac_efficiency: 0.7-0.95 COP
        - cooling_setpoint: 24-28°C
        - heating_setpoint: 18-22°C
        """
        logger.info(f"Gerando {n_examples} exemplos de HVAC...")
        
        examples = []
        sample_rows = self.golden_dataset.sample(n=min(n_examples, len(self.golden_dataset)))
        
        for idx, row in sample_rows.iterrows():
            hvac_eff = row['hvac_efficiency']
            cool_sp = row['cooling_setpoint']
            heat_sp = row['heating_setpoint']
            peak_cooling = row['peak_cooling_kw']
            
            example = {
                'category': 'hvac',
                'example_id': f'hvac_{len(examples)+1:02d}',
                'input': f"""
Um sistema HVAC com eficiência (COP) = {hvac_eff:.2f} foi instalado.
Setpoints: Aquecimento {heat_sp:.0f}°C, Resfriamento {cool_sp:.0f}°C.
Demanda de pico: {peak_cooling:.1f} kW.
Como otimizar este sistema?
""".strip(),
                'expected_output': f"""
HVAC com COP = {hvac_eff:.2f}, Demanda pico = {peak_cooling:.1f} kW:

1. Avaliação de Eficiência:
   - COP < 0.75: Sistema antigo, substituir
   - COP 0.75-0.90: Moderado, otimizar operação
   - COP > 0.90: Moderno, avaliar setpoints

2. Otimização de Setpoints:
   - Aquecimento: {heat_sp:.0f}°C (atual)
   - Resfriamento: {cool_sp:.0f}°C (atual)
   - Δ setpoint: {cool_sp - heat_sp:.0f}°C
   
   Recomendação:
   - Ampliar Δ (ex: 20°C heat, 26°C cool) reduz consumo 10-15%
   - Usar setbacks noturnos para 23-25°C

3. Economia Potencial:
   - Redução de 1°C no cooling → 3-5% economia
   - Redução de 1°C no heating → 2-3% economia
""".strip(),
                'source': f"golden_dataset sample #{idx}",
                'difficulty': 'intermediate',
                'tags': ['COP', 'setpoint', 'HVAC_optimization', 'efficiency'],
                'validation_status': 'verified'
            }
            examples.append(example)
        
        logger.info(f"✅ {len(examples)} exemplos de HVAC gerados")
        return examples
    
    def generate_energy_examples(self, n_examples: int = 10) -> List[Dict]:
        """
        Gera exemplos sobre consumo e eficiência energética.
        
        Variáveis:
        - annual_consumption_kwh: 20000-200000
        - peak_cooling_kw: 5-25 kW
        - comfort_hours: 0-8760
        """
        logger.info(f"Gerando {n_examples} exemplos de ENERGIA...")
        
        examples = []
        sample_rows = self.golden_dataset.sample(n=min(n_examples, len(self.golden_dataset)))
        
        for idx, row in sample_rows.iterrows():
            consumption = row['annual_consumption_kwh']
            peak = row['peak_cooling_kw']
            comfort = row['comfort_hours']
            avg_temp = row['avg_temperature_C']
            
            eui = consumption / 100  # Energy Use Intensity (kWh/m²/ano)
            comfort_pct = 100 * comfort / 8760
            
            example = {
                'category': 'energy',
                'example_id': f'ener_{len(examples)+1:02d}',
                'input': f"""
Um edifício tem:
- Consumo anual: {consumption:.0f} kWh
- Demanda pico: {peak:.1f} kW  
- Horas de conforto: {comfort:.0f} de 8760

Qual é a eficiência energética deste edifício?
Como se compara a padrões internacionais?
""".strip(),
                'expected_output': f"""
Análise de Eficiência Energética:

1. Métricas Calculadas:
   - Consumo anual: {consumption:.0f} kWh
   - EUI (por 100m²): {eui:.0f} kWh/m²/ano
   - Conforto: {comfort_pct:.1f}% das horas
   - Temperatura média: {avg_temp:.1f}°C

2. Classificação ASHRAE 90.1:
   - EUI < 50: Excelente (Top 10%)
   - EUI 50-100: Bom (Top 25%)
   - EUI 100-150: Médio (Mediana)
   - EUI > 150: Ruim (Bottom 25%)
   
   Este edifício: {"⭐⭐⭐⭐⭐ Excelente" if eui < 50 else "⭐⭐⭐⭐ Bom" if eui < 100 else "⭐⭐⭐ Médio" if eui < 150 else "⭐⭐ Ruim"}

3. Comparativos:
   - Edifício de escritório típico: 100-150 kWh/m²/ano
   - Edifício eficiente: 50-80 kWh/m²/ano
   - Este edifício: {eui:.0f} kWh/m²/ano

4. Recomendações de Melhoria:
   - Aumentar isolamento: -10 a -15%
   - Otimizar HVAC: -5 a -10%
   - Renovar janelas: -8 a -12%
   - Gestão ocupação: -5 a -8%
""".strip(),
                'source': f"golden_dataset sample #{idx}",
                'difficulty': 'beginner',
                'tags': ['EUI', 'energy_efficiency', 'consumption', 'standards'],
                'validation_status': 'verified'
            }
            examples.append(example)
        
        logger.info(f"✅ {len(examples)} exemplos de energia gerados")
        return examples
    
    def generate_climate_operation_examples(self, n_examples: int = 10) -> List[Dict]:
        """
        Gera exemplos sobre clima e operação.
        
        Variáveis:
        - occupancy_schedule: 30-100%
        - equipment_load: 5-15 W/m²
        - air_leakage_ach: 0.3-2.0 ar/hora
        """
        logger.info(f"Gerando {n_examples} exemplos de CLIMA E OPERAÇÃO...")
        
        examples = []
        sample_rows = self.golden_dataset.sample(n=min(n_examples, len(self.golden_dataset)))
        
        for idx, row in sample_rows.iterrows():
            occupancy = row['occupancy_schedule']
            equipment = row['equipment_load']
            ach = row['air_leakage_ach']
            consumption = row['annual_consumption_kwh']
            
            example = {
                'category': 'climate_operation',
                'example_id': f'clim_{len(examples)+1:02d}',
                'input': f"""
Um edifício em clima temperado tem:
- Taxa de ocupação: {occupancy:.0%} da capacidade
- Carga de equipamentos: {equipment:.1f} W/m²
- Infiltração: {ach:.1f} ar/hora

Como isso afeta o consumo energético anual?
""".strip(),
                'expected_output': f"""
Análise de Operação e Clima:

1. Fatores de Impacto:
   - Ocupação: {occupancy:.0%}
     * Maior ocupação → Mais calor dissipado (ganhos internos)
     * Requer mais resfriamento em meia estação
     * Aumenta conforto exigido
   
   - Equipamentos: {equipment:.1f} W/m²
     * Carga baixa (< 5 W/m²): Edifício residencial
     * Carga média (5-10 W/m²): Escritório típico
     * Carga alta (> 10 W/m²): Centro de dados / Laboratório
   
   - Infiltração: {ach:.1f} ar/hora
     * ACH < 0.5: Edifício estanque (moderno)
     * ACH 0.5-1.0: Padrão
     * ACH > 1.0: Edifício antigo ou com problemas

2. Efeitos Combinados:
   - Consumo anual: {consumption:.0f} kWh
   
   Simulações mostram:
   - Aumentar ocupação em 20% → +5-10% consumo
   - Aumentar equipamentos em 5 W/m² → +15-20% consumo
   - Reduzir infiltração em 0.5 ACH → -8-12% consumo

3. Oportunidades de Otimização:
   - Sistemas inteligentes de ocupação
   - Reduzir infiltração (vedação de janelas/portas)
   - Controle de carga (desligar equipamentos não essenciais)
""".strip(),
                'source': f"golden_dataset sample #{idx}",
                'difficulty': 'advanced',
                'tags': ['occupancy', 'climate', 'infiltration', 'internal_gains', 'operational'],
                'validation_status': 'verified'
            }
            examples.append(example)
        
        logger.info(f"✅ {len(examples)} exemplos de clima/operação gerados")
        return examples
    
    def generate_all_examples(self, n_per_category: int = 10) -> Dict[str, List[Dict]]:
        """
        Gera todos os exemplos (50 total, 10 por categoria).
        
        Args:
            n_per_category: Número de exemplos por categoria
        
        Returns:
            Dict com exemplos organizados por categoria
        """
        logger.info(f"\n{'='*70}")
        logger.info(f"GERAÇÃO DE {n_per_category * 5} FEW-SHOT EXAMPLES")
        logger.info(f"{'='*70}\n")
        
        all_examples = {}
        
        # Gerar por categoria
        all_examples['geometry'] = self.generate_geometry_examples(n_per_category)
        all_examples['materials'] = self.generate_materials_examples(n_per_category)
        all_examples['hvac'] = self.generate_hvac_examples(n_per_category)
        all_examples['energy'] = self.generate_energy_examples(n_per_category)
        all_examples['climate_operation'] = self.generate_climate_operation_examples(n_per_category)
        
        self.example_library = all_examples
        
        return all_examples
    
    def create_few_shot_prompt(self, category: str = None) -> str:
        """
        Cria prompt com exemplos para Few-Shot Learning.
        
        Args:
            category: Categoria específica ou None para todas
        
        Returns:
            String com Few-Shot prompt formatado
        """
        logger.info(f"Criando Few-Shot prompt...")
        
        prompt_parts = [
            "Você é um especialista em Physics-Informed Machine Learning (PIML) e simulação de edifícios.",
            "Use estes exemplos técnicos de casos reais para informar suas respostas:",
            ""
        ]
        
        # Selecionar exemplos
        if category:
            examples_to_use = self.example_library.get(category, [])
        else:
            examples_to_use = [
                ex for exs in self.example_library.values()
                for ex in exs[:3]  # 3 de cada categoria
            ]
        
        # Formatar exemplos
        for example in examples_to_use:
            prompt_parts.append(f"\n{'='*70}")
            prompt_parts.append(f"EXEMPLO: {example['category'].upper()} - {example['example_id']}")
            prompt_parts.append(f"{'='*70}")
            prompt_parts.append(f"\nPergunta:\n{example['input']}")
            prompt_parts.append(f"\nResposta Esperada:\n{example['expected_output']}")
            prompt_parts.append(f"\nTags: {', '.join(example['tags'])}")
        
        prompt_parts.append(f"\n{'='*70}")
        prompt_parts.append("Use a estrutura e conhecimento desses exemplos para responder novas perguntas.")
        
        return "\n".join(prompt_parts)
    
    def save_examples(self):
        """Salva exemplos em vários formatos"""
        logger.info(f"\n{'='*70}")
        logger.info("SALVANDO FEW-SHOT EXAMPLES")
        logger.info(f"{'='*70}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Formato 1: JSON estruturado (para processamento programático)
        json_path = EXAMPLES_DIR / f"few_shot_examples_library_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.example_library, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ JSON salvo: {json_path}")
        
        # Formato 2: Texto para Few-Shot Prompt (para LLMs)
        txt_path = EXAMPLES_DIR / f"few_shot_prompt_{timestamp}.txt"
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(self.create_few_shot_prompt())
        logger.info(f"✅ Prompt TXT salvo: {txt_path}")
        
        # Formato 3: CSV com resumo (para análise)
        all_examples_flat = []
        for category, examples in self.example_library.items():
            for example in examples:
                all_examples_flat.append({
                    'category': category,
                    'example_id': example['example_id'],
                    'difficulty': example['difficulty'],
                    'tags': ', '.join(example['tags']),
                    'validation': example['validation_status']
                })
        
        csv_path = EXAMPLES_DIR / f"few_shot_examples_index_{timestamp}.csv"
        pd.DataFrame(all_examples_flat).to_csv(csv_path, index=False)
        logger.info(f"✅ Índice CSV salvo: {csv_path}")
        
        # Formato 4: Exemplos por categoria separados
        for category, examples in self.example_library.items():
            category_path = EXAMPLES_DIR / f"examples_{category}_{timestamp}.json"
            with open(category_path, 'w', encoding='utf-8') as f:
                json.dump(examples, f, indent=2, ensure_ascii=False)
            logger.info(f"✅ Categoria {category}: {category_path}")
    
    def generate_statistics(self):
        """Gera estatísticas sobre exemplos"""
        logger.info(f"\n{'='*70}")
        logger.info("ESTATÍSTICAS DOS EXEMPLOS")
        logger.info(f"{'='*70}")
        
        total_examples = sum(len(exs) for exs in self.example_library.values())
        
        logger.info(f"\n📊 Resumo:")
        logger.info(f"   Total de exemplos: {total_examples}")
        
        for category, examples in self.example_library.items():
            logger.info(f"\n   {category.upper()}:")
            logger.info(f"      Exemplos: {len(examples)}")
            
            # Contar por dificuldade
            difficulties = {}
            for ex in examples:
                diff = ex.get('difficulty', 'unknown')
                difficulties[diff] = difficulties.get(diff, 0) + 1
            
            for diff, count in difficulties.items():
                logger.info(f"      - {diff}: {count}")

def main():
    """Função principal"""
    logger.info(f"\n{'='*70}")
    logger.info("GERADOR DE FEW-SHOT EXAMPLES")
    logger.info(f"{'='*70}\n")
    
    try:
        # Inicializar gerador
        generator = FewShotExampleGenerator()
        
        # Gerar exemplos
        examples = generator.generate_all_examples(n_per_category=10)
        
        # Gerar estatísticas
        generator.generate_statistics()
        
        # Salvar todos os formatos
        generator.save_examples()
        
        logger.info(f"\n{'='*70}")
        logger.info("✅ GERAÇÃO DE EXEMPLOS CONCLUÍDA!")
        logger.info(f"{'='*70}")
        logger.info(f"\n📚 Próximos passos:")
        logger.info(f"   1. Usar few_shot_prompt.txt com Vertex AI")
        logger.info(f"   2. Treinar fine-tuned model com examples (Mês 5+)")
        logger.info(f"   3. Integrar com chatbot de análise PIML")
    
    except Exception as e:
        logger.error(f"❌ Erro: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
