# 🤖 Claude Code Project Context — Scientific AI Engineering Curriculum

**Document Purpose:** Persistent context for Claude Code sessions working on this curriculum repository.

**Last Updated:** May 7, 2026

---

## 📌 Project Overview

**Scientific AI Engineering Curriculum** — Open-source 12-month training program (600+ hours, 60,000+ lines of code) for mastering Physics-Informed Machine Learning, Building Performance Simulation, and Production AI Systems.

**Status:** 🟡 **Pre-Onboarding** (April 2026 audit)
- Content: ~80% complete (6 gaps open, 12 partial)
- Infrastructure: ✅ Complete (environment, GCP, VSCode setup)
- Capstone: ✅ Complete (Jan 2026, 7.09% optimization, $350K/year savings)
- Instructor enablement: 🔴 Not started (~40–80h)

**Key Reference:** [AUDITORIA_2026_04_REVISAO.md](AUDITORIA_2026_04_REVISAO.md) — April 2026 re-audit with verified gap list (20 priority items, residual ~45h technical + ~40–80h instructor material)

---

## 🎯 Current Phase: F2 (May–Aug 2026)

**Objective:** Close residual technical gaps, dry-run curriculum as student, prepare instructor enablement materials.

**Timeline:**
- **May–Jun:** Quick wins (Bloco A) + documentation (Bloco D) + pytest suite start (Bloco B)
- **Jul–Aug:** Advanced topics (Blocos B, C) + full end-to-end dry-run + student kit
- **Target:** Student-ready repo by 2026-08-15

**Resource:** [PROGRAMACAO_F2_F3.md](PROGRAMACAO_F2_F3.md) — Week-by-week execution plan with checkboxes and hour allocations.

---

## 📂 Key Files & Directories

### Documentation (Root Level)
| File | Purpose | Last Updated |
|------|---------|--------------|
| [README.md](README.md) | Main project landing page | May 7, 2026 |
| [AUDITORIA_2026_04_REVISAO.md](AUDITORIA_2026_04_REVISAO.md) | April 2026 audit with 20 priority gaps | Apr 30, 2026 |
| [PROGRAMACAO_F2_F3.md](PROGRAMACAO_F2_F3.md) | F2/F3 execution plan (week-by-week) | May 1, 2026 |
| [Scientific_AI_Engineering_Curriculum.md](Scientific_AI_Engineering_Curriculum.md) | 12-month master curriculum (50 pages) | May 7, 2026 |
| [STUDENT_PROFILE.md](STUDENT_PROFILE.md) | Readiness assessment + prep guide | May 7, 2026 |
| [PREREQUISITES.md](PREREQUISITES.md) | Technical & academic requirements | May 7, 2026 |
| [CURRICULUM_FAPESP_ALIGNMENT_REPORT.md](CURRICULUM_FAPESP_ALIGNMENT_REPORT.md) | Research project alignment (98/100) | Maintained (separate scope) |

### Curriculum Content
| Path | Content | Status |
|------|---------|--------|
| [Science AI Engineering/](Science%20AI%20Engineering/) | 12-month curriculum with 140+ exercises | ✅ Months 0-9 complete; Months 10-12 partial |
| [Science AI Engineering/CURRICULUM_INDEX.md](Science%20AI%20Engineering/CURRICULUM_INDEX.md) | Master index of all months | ✅ Current |
| [Science AI Engineering/mes12_capstone/](Science%20AI%20Engineering/mes12_capstone/) | Capstone project (completed Jan 2026) | ✅ Complete |
| [Bootcamp Express/](Bootcamp%20Express/) | 1-week prep (Infrastructure/Python/Git/Cloud) | ✅ English & Portuguese |
| [Literature Alignment/](Literature%20Alignment/) | 30+ papers + LaTeX manuscript (888 papers reviewed) | ✅ Refreshed May 2026 |

### Infrastructure
| File | Purpose |
|------|---------|
| [setup_env.ps1](setup_env.ps1) | Windows PowerShell environment setup (Python venv, dependencies) |
| [setup_gcp_env.sh](setup_gcp_env.sh) | GCP/FinOps validation (RAM, Cloud SDK, project cost) |
| [requirements.txt](requirements.txt) | Python dependencies (currently uses `>=` ranges, needs pinning) |
| [.devcontainer/](devcontainer%20/) | GitHub Codespaces dev container config |
| [.vscode/settings.json](.vscode/settings.json) | VSCode workspace settings + extension recommendations |

---

## 🔧 Common Tasks

### Running Curriculum Code
```bash
# Setup environment (once)
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
source .venv/bin/activate      # Linux/Mac
pip install -r requirements.txt

# Run capstone quick test (edit rounds for speed)
cd "Science AI Engineering/mes12_capstone"
python capstone_week2_optimization.py  # ~2 min with reduced rounds
```

### Making Documentation Changes
- **Status updates:** Update dates in headers + [README.md](README.md) timestamp
- **Audit references:** Link new findings to [AUDITORIA_2026_04_REVISAO.md](AUDITORIA_2026_04_REVISAO.md)
- **Timeline changes:** Update [PROGRAMACAO_F2_F3.md](PROGRAMACAO_F2_F3.md) week-by-week table

### Code Changes Requiring Commits
- **Requirements pinning:** `requirements.txt` — currently uses `>=`, needs `==`
- **Physics validators:** [Science AI Engineering/mes7_physics/physics_violation_validator_complete.py](Science%20AI%20Engineering/mes7_physics/physics_violation_validator_complete.py) — missing 3-4 validators
- **FedAvg stragglers:** [Science AI Engineering/mes10_federated_learning/](Science%20AI%20Engineering/mes10_federated_learning/) — needs timeout + async handling
- **Test suites:** Months 1-7, 9-12 lack pytest files (only Months 4, 8 have coverage)

---

## 📊 Audit Findings (April 2026)

### Gaps by Priority

**P0 (Critical) — 6 open/partial:**
- Gap 8: `technical_examples_library.json` (50 examples) — **missing**
- Gap 11: Pin versions in `requirements.txt` — **partially fixed**
- Gap 17: Physics validators (energy balance, 2ª law, conservation) — **16/20 implemented**
- Gap 18: Stragglers handling in FedAvg — **not implemented**
- Gap 19: Conflict detection (correlation matrix) — **not implemented**
- Gap 20: Operations runbook — **not implemented**

**P1 (Important) — 6 partial:**
- Gaps 3, 9, 12, 13, 14, 16 — See [AUDITORIA_2026_04_REVISAO.md](AUDITORIA_2026_04_REVISAO.md) Table (lines 42-63) for details

### Residual Work Estimate
- **Technical (Blocos A–D):** ~45 hours
  - Quick wins (A): ~8h
  - Robustness (B): ~19h
  - Advanced topics (C): ~15h
  - Documentation (D): ~3h
- **Instructor enablement (F3):** ~40–80 hours
  - Guide, answer keys, slides, FAQ, dry-run, onboarding script

---

## 💼 Preferences & Known Patterns

### When Making Changes
1. **Verify against audit:** New features/fixes should reference which gap they close
2. **Keep docs in sync:** Update README + audit links when changing status
3. **Test curriculum as student:** Before marking gaps "done," execute the code path (dry-run)
4. **No infrastructure bloat:** Avoid new dependencies unless critical (check `requirements.txt` first)

### File Organization
- **Root:** Main docs (README, audit, program)
- **Science AI Engineering/:** Curriculum content (Months 0-12)
- **Literature Alignment/:** Academic references (separate track, not blocking F2/F3)
- **Bootcamp Express/:** 1-week prep (language variants in same folder)
- **results_archive/:** Historical cleanup logs (can be deleted after F2)

---

## 🚀 Next Steps (Week of May 7, 2026)

**Priority this week:**
- A11: Pin versions in `requirements.txt` (Gap 11)
- A8: Generate and validate `technical_examples_library.json` (Gap 8)
- Plan B3: pytest suite structure for GuardrailValidator
- Plan B16: 3rd layer cross-validation for hallucination detector

**Execution:** See [PROGRAMACAO_F2_F3.md](PROGRAMACAO_F2_F3.md) Week 1-2 rows for hour allocation and checkboxes.

---

## 📞 Contact & Attribution

**Project Lead:** João Roberto Diego Petreche (petreche@usp.br)  
**Repository:** https://github.com/joao-petreche/ai-engineering-curriculum  
**License:** CC BY 4.0  
**FAPESP Project:** University of São Paulo

---

**This file should be updated every time project status, timeline, or high-level strategy changes.**
