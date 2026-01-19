# 📋 Prerequisites & Preparation Guide

**Last Updated:** January 17, 2026  
**Curriculum Status:** ✅ 100% Complete (12 months, 600-700 hours)  
**Target Audience:** Scientific AI Engineers in Building Performance Simulation

---

## ✅ Executive Summary

This 12-month curriculum (600-700 hours) is designed for **intermediate developers/engineers** and **graduate students** with backgrounds in engineering, computer science, or related STEM fields.

**Direct Target Audience:**
- 🎓 Master's and PhD students in engineering
- 💼 Professionals with 2-5 years of programming experience
- 🔬 Researchers in Building Performance Simulation
- 🏢 Engineers transitioning to AI/ML applications

**Critical Requirement:** No formal prerequisites, but prior knowledge significantly accelerates learning and ensures success.

---

## 📚 Expected Academic Background

### Minimum Level

```
✅ Higher Education
├── Bachelor's degree (any engineering, CS, architecture)
├── Minimum duration: 2 years completed
└── Recommended: Currently in graduate program or have professional experience
```

### Ideal Backgrounds

| Degree | Benefit | Fit Level |
|--------|---------|-----------|
| **Civil Engineering** | Building construction & BPS knowledge | ⭐⭐⭐⭐⭐ |
| **Mechanical Engineering** | Thermal systems expertise | ⭐⭐⭐⭐⭐ |
| **Architecture** | Building design familiarity | ⭐⭐⭐⭐ |
| **Computer Science** | Strong programming foundation | ⭐⭐⭐⭐⭐ |
| **Electrical Engineering** | Energy systems knowledge | ⭐⭐⭐⭐ |
| **Environmental Engineering** | Sustainability understanding | ⭐⭐⭐ |
| **Physics** | Mathematical and physical principles | ⭐⭐⭐⭐ |
| **Mathematics** | Excellent for optimization/ML | ⭐⭐⭐⭐ |

**Note:** Even without domain-specific background (BPS/Buildings), any STEM bachelor's degree provides necessary foundations.

---

## 🧠 Minimum Required Knowledge

### Level 1: CRITICAL (Must Have)

#### 1.1 Programming

```
✅ Python Intermediate
├── Basic syntax (variables, loops, functions)
├── Object-oriented programming (classes, inheritance)
├── Exception handling (try/except)
├── File manipulation (read/write)
└── Experience: 6+ months or 500+ lines of code written

✅ Version Control (Git)
├── Basic commands (git add, commit, push, pull)
├── GitHub or GitLab
└── Experience: Participated in 1+ versioned project

✅ Command Line / Terminal
├── Directory navigation (cd, ls, pwd)
├── Program installation
├── Script execution
└── Windows PowerShell OR Linux Bash (comfortable with one)
```

**Proficiency Test:** Can you write a Python function that reads a CSV file, filters data, and saves results without consulting basic tutorials?

#### 1.2 Mathematics

```
✅ Linear Algebra
├── Matrices and vectors (multiplication, transposition)
├── Linear systems
└── Eigenvalues/eigenvectors (conceptual)

✅ Calculus
├── Derivatives and integrals (conceptual)
├── Optimization: maxima/minima
└── Gradients

✅ Basic Statistics
├── Probability distributions
├── Mean, median, standard deviation
├── Hypothesis testing (conceptual)
└── Linear regression
```

**Proficiency Test:** Can you multiply two 2×2 matrices by hand? Can you explain what a gradient represents?

#### 1.3 Physics and Thermodynamics (Minimum)

```
✅ Heat and Temperature Concepts
├── Heat transfer (conduction, convection, radiation)
├── Fourier's law (Q = -k * dT/dx)
├── Thermal capacity and specific heat
└── Understand why buildings need insulation

✅ Energy and Power
├── Joules (J) and Watts (W)
├── Difference between energy and power
├── Energy consumption (kWh)
└── Basic energy efficiency

❓ NOT REQUIRED (will be taught in Month 1):
└── HVAC details, complex thermal load calculations
```

**Proficiency Test:** Can you explain why a house gets hot in the sun? Can you differentiate between Joules and Watts?

### Level 2: HIGHLY RECOMMENDED (Significantly Accelerates Learning)

#### 2.1 Basic Machine Learning

```
✅ Fundamental Concepts
├── Supervised vs unsupervised learning
├── Training vs testing (overfitting/underfitting)
├── Cross-validation
└── Model evaluation metrics

✅ Classical Models
├── Linear regression
├── Decision trees (conceptual)
├── K-nearest neighbors
└── Understand tradeoff between simplicity and performance
```

#### 2.2 Data Analysis

```
✅ Python Libraries
├── Pandas (DataFrames, manipulation)
├── NumPy (arrays, linear algebra)
├── Matplotlib (basic visualization)
└── SciPy (mathematical functions)

✅ Techniques
├── Data cleaning (missing values, outliers)
├── Aggregation and grouping
├── Pattern visualization
└── Exploratory data analysis (EDA)
```

#### 2.3 Basic SQL

```
✅ Ability to:
├── Execute basic SELECT queries
├── Use WHERE, GROUP BY, JOIN
├── Understand normalization (conceptual)
└── Connect to databases
```

### Level 3: NICE TO HAVE (Interesting But Not Required)

#### 3.1 DevOps / Cloud

```
⭐ Docker (basic knowledge)
├── Understand containers
└── Run simple Docker image

⭐ Google Cloud / AWS
├── Create account and project
├── Launch VM or instance
└── Understand billing model
```

#### 3.2 REST APIs

```
⭐ HTTP Request Concepts
├── GET, POST, PUT, DELETE
├── Status codes (200, 404, 500)
└── JSON / headers
```

#### 3.3 Energy Simulation

```
⭐ Experience with EnergyPlus, TRNSYS, or similar
├── Have run a simulation
├── Understand basic outputs
└── Familiarity with .idf or .ddy files
```

---

## 🛑 What the Training Assumes You DON'T Know

**The curriculum is designed to TEACH:**

| Topic | How It's Taught | Where |
|-------|----------------|-------|
| **EnergyPlus Automation** | From scratch with Eppy | Month 1 |
| **Scientific Validation** | Pydantic + GuardrailValidator | Month 2 |
| **ML Fundamentals** | XGBoost, Neural Networks | Months 3-4 |
| **LLMs and Prompts** | From GPT basics to Vertex AI | Month 5 |
| **Docker & Kubernetes** | Complete setup to deployment | Month 9 |
| **Federated Learning** | Distributed systems from scratch | Month 10 |
| **Advanced Optimization** | NSGA-II, Optuna | Months 8, 11 |
| **Production Systems** | CI/CD, monitoring, logging | Months 9-12 |

---

## 📊 Self-Sufficiency Test - Entry Checklist

Answer **HONESTLY**. If you answer **NO** to more than 3 items, consider:
1. Reviewing basic material BEFORE starting
2. Having a mentor available during the first 4 weeks

### Python Section
- [ ] I can write a Python function that reads a CSV and returns the mean of a column
- [ ] I can use a for loop and understand why `range(10)` goes from 0-9
- [ ] I can clone a GitHub repo, make changes, and commit
- [ ] I can run `pip install` in terminal without panic

### Mathematics Section
- [ ] I can multiply two 2×2 matrices by hand
- [ ] I can sketch and describe a parabola (y = ax² + bx + c)
- [ ] I can explain the difference between derivative and integral
- [ ] I can read a scatter plot and identify correlation

### Physics Section
- [ ] I can explain why a house gets hot in the sun
- [ ] I can sketch heat flow through a wall
- [ ] I can differentiate between Joules (energy) and Watts (power)
- [ ] I can estimate the consumption of an air conditioner (kWh)

### Engineering / Domain Section
- [ ] I can open an EnergyPlus IDD file without panic
- [ ] I can name 3+ thermal zones in a typical house
- [ ] I can describe 2+ causes of thermal discomfort in buildings
- [ ] I can estimate the density of a common material

**Scoring:**
- **13-16 YES answers:** ✅ **Ready to Start**
- **10-12 YES answers:** ⭐ **Recommend 1-2 weeks of prior study**
- **7-9 YES answers:** ⚠️ **Recommend 3-4 weeks of preparation**
- **<7 YES answers:** 🔴 **Recommend waiting 2-3 months and taking Python/Math bootcamp**

---

## 🚀 Pre-Training Preparation Roadmap

### If You Have 0-1 Month:

```
WEEK 1: Python & Git
├── Review: Loops, functions, classes (2h)
├── GitHub: Clone, branch, commit (2h)
└── Mini-project: CSV reader with analysis (3h)

WEEK 2-3: Essential Mathematics
├── Linear Algebra: Matrices (3h)
├── Calculus: Derivatives and optimization (3h)
└── Statistics: Distributions, regression (3h)

WEEK 4: Physics and EnergyPlus
├── Heat transfer: Theory (2h)
├── EnergyPlus: Installation and first simulation (2h)
└── Output analysis (1h)

Free Resources:
• Python: Codecademy, freeCodeCamp (YouTube)
• Math: 3Blue1Brown (Essence of Algebra/Calculus)
• EnergyPlus: Official documentation + examples
```

### If You Have 2-3 Months:

```
WEEK 1-4: Intermediate Python
├── OOP in depth (4h)
├── Pandas + NumPy (8h)
├── Mini-projects (12h)
└── Real GitHub workflow (4h)

WEEK 5-8: Mathematics & Physics
├── Complete linear algebra (8h)
├── Multivariable calculus (8h)
├── Advanced statistics (6h)
└── Basic thermodynamics (6h)

WEEK 9-12: Machine Learning Basics
├── Coursera: Machine Learning (Andrew Ng) (20h)
├── XGBoost + scikit-learn (8h)
└── Mini-project: Prediction with real data (12h)

WEEK 13: EnergyPlus
├── Complete installation (1h)
├── Guided simulations (8h)
└── Output data analysis (4h)

Investment: ~100 hours (well invested!)
```

---

## 🎓 Recommended Entry Courses / Resources

### Free Online

#### Python
- **freeCodeCamp** (YouTube): "Python for Beginners" (4h)
- **Codecademy**: Python course (interactive)
- **Real Python**: Tutorials (blog)
- **Python.org**: Official documentation

#### Mathematics
- **3Blue1Brown** (YouTube):
  - "Essence of Linear Algebra" (15min videos, ~3h total)
  - "Essence of Calculus" (15min videos, ~3h total)
- **Khan Academy**: Linear Algebra, Calculus sections
- **MIT OpenCourseWare**: 18.06 Linear Algebra

#### Physics / Thermodynamics
- **MIT OpenCourseWare**: Physics I (Classical Mechanics)
- **YouTube**: "Thermodynamics Basics" from Crash Course
- **Khan Academy**: Thermodynamics and heat transfer

#### Machine Learning
- **Fast.ai**: "Practical Deep Learning for Coders" (free)
- **Google Cloud Skills Boost**: "ML Fundamentals"
- **Elements of AI**: Beginner-friendly introduction

### Paid (Worth the Investment)

#### Coursera (~$40-50/month, FREE via many universities)
- "Machine Learning" - Andrew Ng (Stanford)
- "Deep Learning Specialization" (5 courses)
- "TensorFlow Developer Professional Certificate"
- "Mathematics for Machine Learning"

#### LinkedIn Learning (Often free via university/library)
- "Learning Python"
- "Git Essential Training"
- "Data Science Foundations"

#### Udemy ($12-15 on sale)
- "Complete Python Bootcamp" - José Portilla
- "Machine Learning A-Z" - Kirill Eremenko
- "Python for Data Science and Machine Learning"

---

## ⏱️ Recommended Time Commitment

### During the 12-Month Training

```
Typical Week: 12-15 hours
├── 2 work sessions of 6-7h each (e.g., Mon-Wed and Fri-Sat)
├── 1 rest day per week (e.g., Thursday)
└── Weekends for review and catching up

Activity Distribution:
├── Reading material: 20%
├── Hands-on coding: 50%
├── Testing and validation: 15%
└── Review and documentation: 15%
```

### Recommended Schedule

```
✅ BEST: Morning (5am-10am)
   Reason: Code requires maximum concentration

⭐ GOOD: Afternoon (2pm-7pm)
   Reason: Theory and reading also work well

❌ AVOID: Night after full workday
   Reason: Mental fatigue reduces learning
```

### Program Duration Options

```
Standard Path: 12 months
├── 12-15 hours per week
├── Follow monthly progression
└── Recommended for most students

Intensive Path: 6-8 months
├── 20-25 hours per week
├── Faster progression
└── Suitable for career transitions

Extended Path: 18-24 months
├── 6-8 hours per week
├── More gradual pace
└── Ideal for part-time alongside work
```

---

## 🎯 Success Criteria

### Completion Metrics

| Metric | Target | How to Validate |
|--------|--------|----------------|
| Exercises per month | 12-15 per month | Checkpoints in README files |
| Code committed | 2-3 per week | Git log with clear messages |
| Monthly reports | 1 per month end | MES_X_DELIVERY_SUMMARY completed |
| Final capstone | 1 real project | Published on public GitHub |
| Code coverage | 80%+ | Tests passing, linting clean |
| Documentation | Complete | All files have clear README |

### Learning Outcomes

By completing this curriculum, you will be able to:

**Technical Skills:**
- ✅ Design and implement Physics-Informed Machine Learning systems
- ✅ Build production-ready AI applications with Docker and Kubernetes
- ✅ Optimize complex multi-objective problems with constraints
- ✅ Deploy federated learning systems across distributed sites
- ✅ Integrate Large Language Models with scientific guardrails
- ✅ Implement monitoring and observability for production systems
- ✅ Write reproducible scientific code with proper testing

**Soft Skills:**
- ✅ Manage complete project lifecycle: problem → publication
- ✅ Write technical documentation and academic papers
- ✅ Calculate and communicate business impact (ROI, NPV)
- ✅ Present complex technical work to varied audiences
- ✅ Collaborate using Git and modern development practices

---

## 📋 Final Preparation Checklist

### Before Starting Month 0

#### Hardware
- [ ] Computer with 8GB+ RAM (16GB recommended)
- [ ] SSD with 100GB+ free space
- [ ] Second monitor (desirable, not mandatory)
- [ ] Stable internet connection (>10 Mbps)

#### Software Installed
- [ ] Python 3.10.x
- [ ] VS Code + extensions (Python, Jupyter, GitHub Copilot)
- [ ] Git and GitHub account
- [ ] EnergyPlus 24.1.0
- [ ] Browser (Chrome/Firefox/Edge)

#### Knowledge Validated
- [ ] Solved "self-sufficiency test" with 70%+
- [ ] Can execute `git clone`, make edits, and `git commit`
- [ ] Can write and execute Python script that reads data
- [ ] Can explain heat transfer through a wall

#### Accounts Activated
- [ ] GitHub account (Education Pack active if student)
- [ ] Google Cloud ($300 credit via GCP free tier)
- [ ] Institutional email working
- [ ] (Optional) Coursera access via university

#### Mindset
- [ ] Willing to dedicate 12-15 hours/week for 12 months
- [ ] Accepted that Month 0 is mandatory (no skipping)
- [ ] Planned how to accommodate this in professional/personal life
- [ ] Have mentor/support for questions

---

## 📞 Support and Resources During Training

If you feel lost:

1. **Weeks 1-2 of Month:** Review prerequisites for that month in README
2. **Technical problems:** Consult relevant TROUBLESHOOTING.md (exists for Months 7+)
3. **Concepts:** Review with ChatGPT/Copilot (with specific prompts)
4. **Mentor:** Ideally have 1 person available for 1h/week Q&A
5. **Community:** GitHub Issues, Stack Overflow, Reddit communities

### Official Resources

- **Main Repository:** https://github.com/joao-petreche/ai-engineering-curriculum
- **Curriculum Index:** [CURRICULUM_INDEX.md](Science%20AI%20Engineering/CURRICULUM_INDEX.md)
- **Literature Alignment:** [curriculum_alignment_matrix.md](Science%20AI%20Engineering/curriculum_alignment_matrix.md)
- **Month Summaries:** Each month has MES_X_DELIVERY_SUMMARY.md

---

## 📊 Student Profile Recommendations

### Final Recommendations by Profile

#### Profile A: "I Have Everything" ✅
- Bachelor's in Engineering/CS
- 2+ years of programming experience
- Knowledge of ML or Physics
- **Action:** Start now! Month 0 → Month 1

#### Profile B: "I Have Python, Missing Physics/ML" ⭐
- Competent programmer
- But without Physics/ML knowledge
- **Action:** 2-4 weeks of prior study (math/physics), then start

#### Profile C: "I Have Physics, Missing Code" ⭐
- Engineer/architect with strong physics
- But weak programming
- **Action:** 3-6 weeks of Python/Git, then start

#### Profile D: "I Have Little of Everything" ⚠️
- Recently graduated bachelor's
- Basic Python, weak physics/ML
- **Action:** 2-3 months of autonomous bootcamp, then start

#### Profile E: "I'm Not Ready" 🔴
- No STEM bachelor's
- Very weak programming
- **Action:** Consider 3-6 month bootcamp before

---

## ✅ Conclusion

**The 12-month training is accessible to any STEM bachelor's degree holder with determination.**

You don't need to be a programming genius or have a PhD in Physics. What you need is:

1. ✅ **Solid foundations** in Python, Mathematics, and basic Physics
2. ✅ **Discipline** to complete 12-15 hours/week for 12 months
3. ✅ **Learning mindset** - comfortable being a beginner in AI/ML
4. ✅ **Curiosity** - want to understand how things work (not just execute)

**Final Recommendation:**
- If you answered YES to 12+ items in checklist: **Start Now (Month 0)**
- If you answered YES to 8-11 items: **Dedicate 2-4 weeks to preparation, then start**
- If you answered YES to <8 items: **Consider 6-8 week bootcamp, then this training**

The training is designed to be **challenging but accessible**. It won't be easy, but it will be possible and very rewarding!

---

**Report Completed:** Complete prerequisites analysis provided.  
**Next Step:** Review [STUDENT_PROFILE.md](STUDENT_PROFILE.md) for detailed readiness assessment.  
**Last Updated:** January 17, 2026
