# 👥 Instruções para Colaboradores do Projeto FAPESP

Este documento contém informações essenciais para colaboradores do projeto FAPESP que precisam acessar o material de treinamento.

---

## 📖 Sobre Este Repositório

Este repositório (`ai-engineering-curriculum`) contém o **material completo do curso de treinamento de 12 meses** em Scientific AI Engineering aplicado a Building Performance Simulation. Ele é um **submódulo** do repositório principal do projeto FAPESP.

### 🔗 Estrutura de Repositórios

```
FAPESP-ML-Building-Simulation/          (Repositório Principal)
├── Training_12Meses/                   (Este submódulo - somente leitura)
├── Deep Search Report/
├── Emerging Applications/
├── Projeto_Pesquisa/
└── Tropical Climate Datasets/
```

---

## 🔐 Permissões de Acesso

**Colaboradores do Projeto FAPESP:**
- ✅ **Leitura completa** de todo o material de treinamento
- ✅ **Uso** do material para estudo e aplicação no projeto
- ❌ **Sem permissão de edição** direta neste repositório
- ✅ **Podem sugerir melhorias** via issues ou pull requests

**Coordenador do Projeto:**
- ✅ Acesso completo (leitura e escrita)
- ✅ Gerencia atualizações do material

---

## 📥 Como Clonar o Projeto Completo

### Primeira vez - Clone com submódulos:

```bash
git clone --recurse-submodules https://github.com/joao-petreche/FAPESP-ML-Building-Simulation.git
cd FAPESP-ML-Building-Simulation
```

### Se já clonou sem submódulos:

```bash
cd FAPESP-ML-Building-Simulation
git submodule update --init --recursive
```

---

## 📚 Navegando pelo Material de Treinamento

### Principais Arquivos de Referência:

1. **[README.md](README.md)** - Visão geral do currículo completo
2. **[PERFIL_ALUNO_IDEAL_SUMARIO.md](PERFIL_ALUNO_IDEAL_SUMARIO.md)** - Checklist de pré-requisitos
3. **[Scientific_AI_Engineering_Curriculum.md](Scientific_AI_Engineering_Curriculum.md)** - Plano completo da pesquisa (48 meses)
4. **[Science AI Engineering/CURRICULUM_INDEX.md](Science%20AI%20Engineering/CURRICULUM_INDEX.md)** - Índice dos 12 meses

### Estrutura de Conteúdo:

```
Training_12Meses/
├── Science AI Engineering/
│   ├── Exercicios_Mes_1_EnergyPlus.md
│   ├── Exercicios_Mes_2_Engenharia_Software.md
│   ├── ...
│   ├── Exercicios_Mes_12_Capstone.md
│   ├── mes1_energyplus/              (código e notebooks)
│   ├── mes2_software_engineering/
│   └── ...
├── README.md
├── COLABORADORES.md                   (este arquivo)
└── LICENSE
```

---

## 🔄 Mantendo Atualizado

O coordenador do projeto atualiza periodicamente o material. Para obter as últimas versões:

```bash
cd FAPESP-ML-Building-Simulation
git pull origin main
git submodule update --remote --merge
```

---

## 💡 Como Contribuir

### Reportar Problemas ou Sugerir Melhorias:

1. **Via GitHub Issues** (recomendado):
   - Acesse: https://github.com/joao-petreche/ai-engineering-curriculum/issues
   - Clique em "New Issue"
   - Descreva o problema ou sugestão detalhadamente

2. **Via Pull Request** (para contribuições diretas):
   - Faça um fork do repositório `ai-engineering-curriculum`
   - Implemente suas melhorias
   - Submeta um Pull Request
   - O coordenador revisará e integrará as mudanças

3. **Comunicação Direta**:
   - Entre em contato com o coordenador do projeto para discussões

---

## 📖 Uso do Material

### ✅ Você Pode:

- Estudar todo o conteúdo
- Executar notebooks e código
- Adaptar exercícios para necessidades do projeto FAPESP
- Citar o material em publicações (veja [CITATION.cff](CITATION.cff))
- Compartilhar conhecimento com outros colaboradores

### ❌ Você Não Pode:

- Modificar diretamente o repositório (use PR para sugestões)
- Redistribuir como seu próprio trabalho
- Remover atribuições de autoria

---

## 📄 Licença

Este material está licenciado sob **Creative Commons Attribution 4.0 International (CC BY 4.0)** — veja [LICENSE](LICENSE) para detalhes.

**Citação Acadêmica:**

```bibtex
@misc{petreche2026scientific,
  author = {Petreche, João Paulo Bazzo},
  title = {Scientific AI Engineering Curriculum for Building Performance Simulation},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/joao-petreche/ai-engineering-curriculum}}
}
```

---

## 🆘 Suporte

**Dúvidas ou Problemas?**

1. Consulte o [README.md](README.md) principal
2. Verifique issues existentes: https://github.com/joao-petreche/ai-engineering-curriculum/issues
3. Crie uma nova issue descrevendo sua dúvida
4. Entre em contato com o coordenador do projeto

---

## 🎯 Objetivos do Material de Treinamento

Este currículo de 12 meses prepara colaboradores para:

- ✅ Dominar EnergyPlus e simulação de edifícios
- ✅ Implementar Physics-Informed Machine Learning (PIML)
- ✅ Desenvolver sistemas GenAI/LLM para engenharia
- ✅ Deploy de soluções em produção (Docker/K8s/GCP)
- ✅ Realizar pesquisa científica aplicada
- ✅ Publicar resultados em conferências/journals

**Tempo estimado:** 600-700 horas (50-60h/mês)

---

**Última Atualização:** Janeiro 2026  
**Coordenador:** João Paulo Bazzo Petreche (petreche@usp.br)
