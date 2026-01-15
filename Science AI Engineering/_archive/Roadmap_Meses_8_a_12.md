# Roadmap: Months 8-12 (Advanced Optimization → Production → Specialized Topics)

## 📋 Overview

This roadmap outlines the final 5 months of the "Scientific AI Engineering & BPS" curriculum, building upon the foundation established in Months 1-7.

**Total Hours:** 300-360 hours (60h/month average)
**Duration:** Months 8-12 (5 consecutive months)

---

## 🗂️ Architecture Overview

```
Months 1-7: FOUNDATION & COMPLIANCE
├── M1-3: Data processing, simulation, time series
├── M4-5: Machine learning surrogates & LLM integration
├── M6-7: Co-simulation architecture & physics compliance
│
Months 8-12: OPTIMIZATION, PRODUCTION & SPECIALIZATION
├── M8: Advanced Multi-Objective Optimization
├── M9: Production Deployment & DevOps
├── M10-11: Advanced Research Topics
└── M12: Integration & Capstone Project
```

---

# 📅 MÊS 8: Advanced Multi-Objective Optimization (60h)

## 🎯 Learning Objectives

By the end of this month:
1. Implement Pareto-optimal solution finding
2. Use genetic algorithms for parameter search
3. Perform trade-off analysis (energy vs cost vs comfort)
4. Handle conflicting objectives in building design
5. Create interactive Pareto frontier visualization

## 📦 Prerequisites

- ✅ Mês 6 (Co-simulation architecture)
- ✅ Mês 7 (Physics compliance testing)
- ✅ Linear algebra & optimization theory
- NumPy, SciPy, DEAP (genetic algorithms)

---

## 📚 Semana 1: Multi-Objective Optimization Fundamentals (12-15h)

### 🎯 Semana 1 Exercises

**Exercise 1.1: Pareto Frontier Concepts (3-4h)**
- Implement NSGA-II (Non-dominated Sorting Genetic Algorithm II)
- Pareto domination relationships
- Multi-objective fitness evaluation
- Expected output: 100+ non-dominated solutions for 3-objective problem

**Exercise 1.2: Conflicting Objectives in BPS (2-3h)**
- Define 4 key objectives:
  - Energy consumption (minimize kWh/year)
  - Capital cost (minimize $/m²)
  - Thermal comfort (maximize PMV range)
  - Environmental impact (minimize CO2 equivalent)
- Implement ScalarizedObjective class
- Test with sample building

**Exercise 1.3: Dominance Checking (2-3h)**
- Implement pareto_dominates() function
- Build dominance graphs
- Calculate hypervolume
- Find Pareto front from 1000 random solutions

**Exercise 1.4: Interactive Visualization (3-4h)**
- 3D scatter plot of Pareto frontier (plotly)
- Hover tooltips showing parameter values
- Interactive filtering by objective
- Export to interactive HTML

---

## 📚 Semana 2: Genetic Algorithms for Building Design (12-15h)

### 🎯 Semana 2 Exercises

**Exercise 2.1: Genetic Algorithm Foundation (4-5h)**
- DEAP library setup
- Chromosome representation for BPS parameters
- Fitness evaluation function
- Selection, crossover, mutation operators
- Example: Optimize 10 parameters across 50 generations

**Exercise 2.2: Constraint Handling in GA (3-4h)**
- Penalty method for physics constraints
- Feasibility checking in population
- Repair operators for invalid solutions
- Test with 50 constraint violations injected

**Exercise 2.3: Convergence Analysis (2-3h)**
- Track fitness statistics per generation
- Convergence plots (best, worst, average)
- Diversity metrics (gene pool diversity)
- Early stopping criteria

**Exercise 2.4: Island Model (2-3h)**
- Parallel GA with population islands
- Inter-island migration strategy
- Distributed optimization across 4 islands
- Compare with single-population GA

---

## 📚 Semana 3: Trade-off Analysis & Decision Support (12-15h)

### 🎯 Semana 3 Exercises

**Exercise 3.1: Sensitivity Analysis (3-4h)**
- Tornado diagrams for 10 key parameters
- Parameter variation impact on objectives
- Identify critical vs non-critical parameters
- Output: Sensitivity report with rankings

**Exercise 3.2: Scenario Planning (3-4h)**
- Define 5 scenarios:
  - Scenario A: Energy-first (minimize energy, cost ≤ $200/m²)
  - Scenario B: Cost-first (minimize cost, energy ≤ 50 kWh/m²/year)
  - Scenario C: Balanced (equal weight to all)
  - Scenario D: Climate-aware (minimize CO2 impact)
  - Scenario E: Comfort-first (maximize comfort, other ≤ penalties)
- Run optimization for each
- Compare results

**Exercise 3.3: Preference-Based Selection (2-3h)**
- Implement interactive trade-off selection
- User weights for objectives (0-1 range)
- Filter Pareto front by weights
- Recommend "best compromise" solution

**Exercise 3.4: Decision Making Support (3-4h)**
- Create decision matrix (solutions × criteria)
- Implement AHP (Analytic Hierarchy Process)
- Calculate consistency ratio
- Rank solutions by priority

---

## 📚 Semana 4: Advanced Techniques & Capstone (12-15h)

### 🎯 Semana 4 Exercises

**Exercise 4.1: Adaptive Mutation (3-4h)**
- Implement adaptive mutation rates
- Adjust crossover probability by convergence
- Self-adaptive GA parameters
- Compare with static GA

**Exercise 4.2: Surrogate-Assisted Optimization (3-4h)**
- Use XGBoost surrogate instead of full simulation
- Uncertainty quantification in surrogate
- Hybrid: Sample expensive evaluations strategically
- Track speedup vs accuracy trade-off

**Exercise 4.3: Real-Time Optimization Integration (2-3h)**
- Connect GA to co-simulation controller (Mês 6)
- Real-time parameter adjustment
- Handle streaming data from BMS
- Optimization restart on new conditions

**Exercise 4.4: M8 Capstone: Optimizing Real Office Building (3-4h)**
- Real building geometry & parameters
- 3+ conflicting objectives
- Constraint: < 20% cost increase
- Deliverable: Pareto frontier + recommendation

---

## 📋 Checklist: Mês 8

- [ ] NSGA-II implemented with 100+ Pareto solutions
- [ ] 4 objectives tracked with no single-objective bias
- [ ] GA converges within 50 generations
- [ ] Sensitivity analysis identifies 3+ critical parameters
- [ ] 5 scenarios optimized independently
- [ ] Interactive Pareto visualization (3D + filtering)
- [ ] Trade-off analysis report generated
- [ ] Decision support system evaluates 10+ solutions
- [ ] Capstone project completed with realistic results

---

# 📅 MÊS 9: Production Deployment & DevOps (60h)

## 🎯 Learning Objectives

By the end of this month:
1. Containerize system with Docker
2. Deploy to Kubernetes cluster
3. Implement CI/CD pipelines
4. Set up monitoring & alerting
5. Handle scaling & high availability
6. Manage database migrations

## 📦 Prerequisites

- ✅ All previous months
- Docker, Kubernetes, GitHub Actions
- PostgreSQL, Redis
- Prometheus, Grafana

---

## 📚 Semana 1: Docker & Containerization (12-15h)

### 🎯 Semana 1 Exercises

**Exercise 1.1: Multi-Stage Dockerfile (3-4h)**
- Build stage: Compile dependencies
- Runtime stage: Minimal image
- Layer caching optimization
- Image size optimization (< 500MB)
- Test with image build

**Exercise 1.2: Docker Compose for Local Development (3-4h)**
- Define services: API, Gemini cache, PostgreSQL, Redis
- Volume mounts for hot-reload
- Network configuration
- Health checks for each service
- Local development with docker-compose up

**Exercise 1.3: Docker Registry & Image Management (2-3h)**
- Push to Docker Hub / GCR
- Image tagging strategy (vX.Y.Z, latest, dev)
- Private registry setup
- Image scanning for vulnerabilities

**Exercise 1.4: Container Security (3-4h)**
- Non-root user configuration
- Read-only file system
- Resource limits (CPU, memory)
- Security scanning (Trivy)
- Test: Run container with least privileges

---

## 📚 Semana 2: Kubernetes Orchestration (12-15h)

### 🎯 Semana 2 Exercises

**Exercise 2.1: Kubernetes Basics (4-5h)**
- Deploy Pods, Services, Deployments
- StatefulSets for PostgreSQL
- ConfigMaps & Secrets management
- Resource requests & limits
- Health checks (liveness, readiness, startup probes)

**Exercise 2.2: Ingress & Networking (3-4h)**
- Ingress controller setup
- TLS/SSL certificates (cert-manager)
- API rate limiting (Nginx ingress)
- DNS configuration
- Load balancing strategy

**Exercise 2.3: Persistent Storage (2-3h)**
- PersistentVolumeClaims
- Storage classes
- Database backup strategy
- Data recovery procedures
- Test: Simulate data loss & recovery

**Exercise 2.4: Multi-Region Deployment (2-3h)**
- Regional clusters (US-East, US-West, EU)
- Data replication strategy
- Cross-region failover
- Network latency optimization

---

## 📚 Semana 3: CI/CD Pipelines (12-15h)

### 🎯 Semana 3 Exercises

**Exercise 3.1: GitHub Actions CI (3-4h)**
- Unit test automation
- Code coverage reporting
- Linting & type checking
- Build Docker images on commit
- Push to registry automatically

**Exercise 3.2: Automated Deployment (3-4h)**
- Dev → Staging → Production pipeline
- Approval gates before production
- Automated rollback on failure
- Blue-green deployment strategy
- Canary releases (10% → 50% → 100%)

**Exercise 3.3: GitOps with ArgoCD (2-3h)**
- ArgoCD declarative configuration
- Sync strategies (automatic vs manual)
- Application manifests in Git
- Policy enforcement
- Rollback via Git history

**Exercise 3.4: Testing in Pipeline (3-4h)**
- Smoke tests in dev
- Integration tests in staging
- Load testing before production
- Security scanning (SAST/DAST)
- Compliance checks

---

## 📚 Semana 4: Monitoring, Logging & Operations (12-15h)

### 🎯 Semana 4 Exercises

**Exercise 4.1: Monitoring with Prometheus & Grafana (4-5h)**
- Instrument code with prometheus_client
- Set up Prometheus scraping
- Create Grafana dashboards:
  - System metrics (CPU, memory, disk)
  - Application metrics (response time, error rate)
  - Business metrics (simulations/hour, accuracy)
- Alert rules: Error rate > 5%, latency > 2s

**Exercise 4.2: Centralized Logging with ELK (3-4h)**
- Elasticsearch setup
- Logstash configuration
- Kibana dashboards
- Structured logging (JSON format)
- Query examples: errors in past 24h, performance bottlenecks

**Exercise 4.3: Distributed Tracing (2-3h)**
- OpenTelemetry instrumentation
- Jaeger backend setup
- Trace visualization
- Example: End-to-end trace for one request

**Exercise 4.4: Incident Response & Runbooks (2-3h)**
- Create runbooks for common issues
- On-call rotation setup
- Postmortem template
- SLA definitions (99.5% uptime)
- Test: Simulate failure & execute runbook

---

## 📋 Checklist: Mês 9

- [ ] Docker image builds successfully, < 500MB
- [ ] docker-compose runs all services locally
- [ ] Kubernetes manifests deploy to cluster
- [ ] 3+ node deployment with auto-scaling
- [ ] CI/CD pipeline triggers on each commit
- [ ] Automated tests pass before production
- [ ] Prometheus scrapes 20+ metrics
- [ ] Grafana dashboards show system health
- [ ] ELK stack aggregates all logs
- [ ] OpenTelemetry traces requests end-to-end
- [ ] Alert triggers for critical issues
- [ ] Runbooks written for 5+ scenarios
- [ ] Production deployment checklist signed off

---

# 📅 MÊS 10: Advanced Research Topics - Part 1 (60h)

## 🎯 Learning Objectives

This month focuses on cutting-edge research applications.

---

## 📚 Semana 1: Federated Learning for Privacy-Preserving Training (12-15h)

### Context
Building performance data is sensitive (energy usage, occupancy patterns). Federated learning enables training models across multiple buildings without centralizing data.

### 🎯 Semana 1 Exercises

**Exercise 1.1: Federated Learning Basics (3-4h)**
- Implement FedAvg (Federated Averaging)
- Simulate 10 "building clients"
- Central server aggregation
- Local model training on each client
- Convergence comparison: Federated vs Centralized

**Exercise 1.2: Privacy with Differential Privacy (3-4h)**
- Add Gaussian noise to gradients (DP-SGD)
- Privacy budget (epsilon-delta) tracking
- Privacy-utility trade-off analysis
- Visualize privacy loss curve

**Exercise 1.3: Communication Efficiency (2-3h)**
- Gradient compression
- Sparsification strategies
- Reduce communication rounds by 10x
- Measure accuracy degradation

**Exercise 1.4: Practical Federated System (3-4h)**
- Flower framework for federated learning
- Multi-round training (10+ rounds)
- Handle stragglers (slow clients)
- Produce final global model

---

## 📚 Semana 2: Adaptive Prompting & Dynamic LLM Behavior (12-15h)

### Context
System prompts should adapt to context: time of day, weather, occupancy, user behavior.

### 🎯 Semana 2 Exercises

**Exercise 2.1: Context-Aware Prompting (3-4h)**
- Define 5 context dimensions:
  - Time-of-day (morning, afternoon, night)
  - Weather (sunny, cloudy, rainy)
  - Occupancy (empty, partial, full)
  - Season (winter, spring, summer, fall)
  - User type (facility manager, engineer, occupant)
- Prompt templates for each context
- Test: Verify different outputs for different contexts

**Exercise 2.2: Chain-of-Thought Prompting (3-4h)**
- Implement multi-step reasoning
- Step 1: Analyze input
- Step 2: Apply physics constraints
- Step 3: Check against standards
- Step 4: Generate recommendation
- Compare with direct prompting (fewer hallucinations)

**Exercise 2.3: Prompt Optimization with RL (2-3h)**
- Use reinforcement learning to optimize prompts
- Reward: accuracy + clarity - hallucination
- Simple RL agent (PPO) updates prompt template
- Train on 100+ queries
- Result: Prompts improve iteratively

**Exercise 2.4: Multi-Agent Dialogue (3-4h)**
- Agent A (Generator): Creates candidates
- Agent B (Critic): Reviews for errors
- Agent C (Recommender): Ranks solutions
- Back-and-forth until agreement
- Output: High-confidence recommendation

---

## 📚 Semana 3: Real-Time Building Performance Monitoring (12-15h)

### Context
BMS provides real-time sensor data. System should detect anomalies and trigger recommendations.

### 🎯 Semana 3 Exercises

**Exercise 3.1: Anomaly Detection in Time Series (3-4h)**
- Implement Isolation Forest for multivariate anomalies
- ARIMA forecasting + envelope detection
- Autoencoders for pattern learning
- Test on synthetic anomalies (sensor failure, setpoint error)
- Detect 95%+ anomalies with < 5% false positives

**Exercise 3.2: Real-Time Data Pipeline (3-4h)**
- Kafka topic: sensor stream
- Spark Streaming processing
- Feature engineering (rolling averages, rates)
- Write clean data to TimescaleDB
- Latency: < 1 second end-to-end

**Exercise 3.3: Predictive Maintenance (2-3h)**
- Predict equipment failures 7 days ahead
- XGBoost model trained on failure history
- Maintenance recommendations with urgency
- Cost-benefit analysis (maintenance vs replacement)

**Exercise 3.4: Closed-Loop Control (3-4h)**
- Feedback loop: Sensor → Model → Recommendation → Control
- Example: HVAC setpoint adjustment
- Verify: Building reaches optimal state faster
- Safety bounds: Never violate comfort limits

---

## 📚 Semana 4: Climate Change & Future Scenarios (12-15h)

### Context
Buildings must be designed for future climate. Need to test performance under projected climate conditions.

### 🎯 Semana 4 Exercises

**Exercise 4.1: Climate Data Projection (3-4h)**
- Load climate model outputs (IPCC RCP 4.5, 8.5)
- Bias correction to match local climate
- Interpolation to building location
- Create synthetic future weather years (2050, 2100)

**Exercise 4.2: Future-Proof Building Design (4-5h)**
- Simulate building under 2050 climate
- Identify performance gaps (cooling insufficient?)
- Optimize design for future climate
- Trade-off: Adaptive now vs robust for future
- Example: Oversizing cooling by 20% for 2050 climate

**Exercise 4.3: Resilience Assessment (2-3h)**
- Extreme event scenarios (heat wave, cold snap)
- Building survival analysis (stays above 15°C?)
- Backup system requirements
- Passive survivability (no power, no HVAC)

**Exercise 4.4: M10 Capstone: Climate Adaptation Strategy (2-3h)**
- Analyze 100-year design life
- Design for 2050 + 2100 climates
- Cost of adaptation measures
- Deliverable: Climate adaptation report

---

## 📋 Checklist: Mês 10

- [ ] Federated learning converges with 10 clients
- [ ] Privacy budget tracked with differential privacy
- [ ] Context-aware prompts generate appropriate outputs
- [ ] Chain-of-thought reduces hallucinations by 30%+
- [ ] Anomaly detection > 95% accuracy
- [ ] Real-time pipeline latency < 1 second
- [ ] Predictive maintenance identifies failures 7+ days ahead
- [ ] Future climate data successfully loaded & projected
- [ ] Building design optimized for 2050 climate
- [ ] Resilience assessment completed for extreme events
- [ ] Capstone: Climate adaptation strategy documented

---

# 📅 MÊS 11: Advanced Research Topics - Part 2 (60h)

## 🎯 Learning Objectives

Deeper exploration of specialized research areas.

---

## 📚 Semana 1-2: Transfer Learning & Domain Adaptation (24-30h)

### Context
Models trained on one building type (office) may not transfer to another (hospital). Domain adaptation bridges this gap.

### 🎯 Exercises

**Exercise 1.1: Transfer Learning from Generic Building Model (4-5h)**
- Start with model trained on 1000 office buildings
- Fine-tune on 50 hospital building samples
- Compare: From-scratch vs transfer learning
- Result: Hospital model reaches 90% accuracy with 10x less data

**Exercise 1.2: Domain Adaptation (4-5h)**
- Adversarial domain adaptation
- Feature alignment between source & target domains
- Gradient reversal layer
- Test on building type mismatch

**Exercise 1.3: Few-Shot Learning (4-5h)**
- Meta-learning (MAML)
- Learn to optimize quickly
- 5-shot learning: Fine-tune on 5 examples
- Compare convergence speeds

**Exercise 1.4: Capstone: New Building Type Transfer (4-5h)**
- Take Mês 4 model (trained on offices)
- Transfer to industrial building
- Minimum labeled data
- Report: Accuracy gained from transfer

---

## 📚 Semana 2: Graph Neural Networks for Building Systems (12-15h)

### Context
Building HVAC systems are graphs: zones connected by dampers, coupled by air flow.

### 🎯 Exercises

**Exercise 2.1: Graph Representation (3-4h)**
- Nodes: Zones, HVAC equipment, dampers
- Edges: Thermal connections, control signals
- Node features: Temperature, setpoint, load
- Build graph for sample building

**Exercise 2.2: Graph Neural Network Implementation (4-5h)**
- Message passing: Information flow through graph
- Graph Convolutional Network (GCN)
- Predict zone temperatures from graph
- Compare with non-graph baseline

**Exercise 2.3: Graph Attention (2-3h)**
- Attention mechanism on edges
- Learn which connections matter most
- Interpretability: Visualize attention weights
- Example: Damper A receives 80% attention in winter

**Exercise 2.4: Physics-Informed GNN (2-3h)**
- Embed conservation laws in graph updates
- Energy balance constraints
- Mass balance constraints
- Verify: Outputs satisfy physics constraints

---

## 📚 Semana 3: Explainability & Interpretability (12-15h)

### Context
For production deployment, engineers need to understand why system made a decision.

### 🎯 Exercises

**Exercise 3.1: SHAP Values (3-4h)**
- Compute SHAP values for XGBoost surrogate
- Identify which parameters drive predictions
- Example: "70% of prediction comes from WWR"
- Interaction analysis: Parameters that interact strongly

**Exercise 3.2: LIME (Local Interpretable Model-Agnostic Explanations) (3-4h)**
- Explain individual predictions
- Perturb inputs locally
- Fit simple linear model
- Result: Human-understandable rule for single prediction

**Exercise 3.3: Attention Visualization (2-3h)**
- For Gemini LLM: Which input tokens influenced output?
- Gradient-based importance
- Visualize attention maps
- Example: LLM focused on "insulation thickness" most

**Exercise 3.4: Capstone: Explainability Report (3-4h)**
- Explain 10 recommendations from system
- Include SHAP, LIME, attention visualizations
- Answer: Why did system recommend this?
- User-friendly explanation vs technical detail

---

## 📚 Semana 4: Uncertainty Quantification & Ensemble Methods (12-15h)

### Context
All models have uncertainty. Need to quantify confidence in predictions.

### 🎯 Exercises

**Exercise 4.1: Bayesian Neural Networks (3-4h)**
- Weight distributions instead of point estimates
- Variational inference for posterior
- Predictive uncertainty (aleatoric + epistemic)
- Confidence intervals on predictions

**Exercise 4.2: Monte Carlo Dropout (3-4h)**
- Use dropout at test time
- Multiple forward passes → distribution
- Uncertainty estimation
- Compare with Bayesian approach

**Exercise 4.3: Ensemble Methods (2-3h)**
- Ensemble of 10 surrogates (different architectures)
- Predictions: Mean ± std of ensemble
- Disagreement = uncertainty
- Boosting, bagging, stacking examples

**Exercise 4.4: Capstone: End-to-End Uncertainty (3-4h)**
- Final recommendation with confidence interval
- Example: "Annual energy = 45 ± 3 kWh/m² (95% CI)"
- Risk assessment: 5% chance of exceeding 48 kWh/m²
- Recommendation: "Proceed with 95% confidence" or "More data needed"

---

## 📋 Checklist: Mês 11

- [ ] Transfer learning achieves 90% accuracy on new building type
- [ ] Domain adaptation reduces distribution mismatch
- [ ] Few-shot learning works with 5 examples
- [ ] Graph neural network outperforms MLP baseline
- [ ] Physics constraints enforced in GNN updates
- [ ] SHAP values explain 80%+ of variance
- [ ] LIME produces human-interpretable rules
- [ ] Attention visualization shows meaningful focus
- [ ] Bayesian NN provides calibrated uncertainty
- [ ] Monte Carlo dropout estimates aleatoric vs epistemic uncertainty
- [ ] Ensemble predictions have tight confidence intervals
- [ ] Capstone: Explanation report covers 10+ recommendations

---

# 📅 MÊS 12: Integration & Capstone Project (60h)

## 🎯 Learning Objectives

Integrate all previous months into complete system. Deliver production-ready solution.

---

## 📚 Semana 1: System Integration & Testing (12-15h)

### 🎯 Exercises

**Exercise 1.1: End-to-End Integration (4-5h)**
- User query → LLM → Co-simulation → Optimization → Recommendation
- Test 20+ real building scenarios
- Latency: < 5 seconds
- All checkpoints validated

**Exercise 1.2: Stress Testing (3-4h)**
- 1000 concurrent users
- Load test with Apache JMeter
- Measure response time under load
- Database connection pool tuning
- Result: System handles 1000 requests/second

**Exercise 1.3: Security Testing (2-3h)**
- Penetration testing (OWASP Top 10)
- SQL injection attempts
- XSS prevention
- Authentication/authorization validation
- Result: All security tests pass

**Exercise 1.4: Compliance Verification (2-3h)**
- Mês 7 compliance tests re-run
- All golden dataset cases pass
- No critical hallucinations
- Compliance score > 85
- Sign-off for production

---

## 📚 Semana 2: User Interface & Documentation (12-15h)

### 🎯 Exercises

**Exercise 2.1: Web Dashboard (4-5h)**
- React/Vue frontend
- Real-time building performance plots
- Optimization results visualization
- Export to PDF/Excel
- Mobile-responsive design

**Exercise 2.2: API Documentation (3-4h)**
- OpenAPI 3.0 specification
- Interactive API explorer (Swagger UI)
- Code examples (Python, JavaScript, cURL)
- Rate limiting info
- Error code reference

**Exercise 2.3: User Guide & Training Materials (2-3h)**
- Getting started guide
- Video tutorials
- Troubleshooting FAQ
- Best practices for prompt engineering
- Common use cases

**Exercise 2.4: Operational Runbooks (2-3h)**
- Deployment procedures
- Backup & recovery
- Scaling guidance
- Common issues & solutions
- Escalation procedures

---

## 📚 Semana 3: Performance Validation & Benchmarking (12-15h)

### 🎯 Exercises

**Exercise 3.1: Accuracy Benchmarking (4-5h)**
- Compare 10 building types
- MAPE (Mean Absolute Percentage Error) < 5%
- Confidence intervals on accuracy
- Breakdown: Heating vs cooling, peak vs average
- Report: Accuracy by building type

**Exercise 3.2: Performance Benchmarking (3-4h)**
- Response time: 1st percentile, median, 95th, 99th
- Throughput: requests/second
- Resource usage: CPU, memory, disk I/O
- Cost analysis: $/prediction
- SLA compliance: 99.5% uptime achieved?

**Exercise 3.3: Hallucination Rate (2-3h)**
- Run 1000 queries from diverse users
- Manual evaluation: How many hallucinations?
- Severity distribution
- Target: < 1% critical hallucination rate
- Report: Hallucination metrics over time

**Exercise 3.4: Capstone: Benchmarking Report (2-3h)**
- Comprehensive comparison vs competitors
- Feature matrix: Our system vs alternatives
- Cost-benefit analysis
- ROI analysis for building owners
- Recommendation: Adoption strategy

---

## 📚 Semana 4: Final Capstone Project (12-15h)

### 🎯 Capstone Project: Real-World Building Optimization

**Scope:** Optimize design & operation of a real or realistic building

**Phase 1: Building Profile (2-3h)**
- Building type: Office / Hospital / Residential / Industrial
- Location: Climate zone
- Size: 5,000-100,000 m²
- Current baseline energy consumption
- Stakeholder goals & constraints

**Phase 2: Analysis & Optimization (5-6h)**
- Month 3: Load simulation (100 design variants)
- Month 4: Surrogate models (XGBoost + MLP)
- Month 5: LLM-guided recommendations
- Month 6: Co-simulation architecture design
- Month 8: Multi-objective optimization (Pareto frontier)
- Generate 50+ candidate designs

**Phase 3: Validation & Compliance (2-3h)**
- Month 7: Physics compliance testing
- All golden dataset cases validated
- No critical violations
- Hallucination detection passed
- Recommendation: Approved for use

**Phase 4: Deployment & Monitoring (2-3h)**
- Month 9: Deploy to production
- Real-time monitoring dashboard
- Anomaly detection active
- Feedback loop: Refine surrogates monthly

**Phase 5: Documentation & Presentation (0-1h)**
- Technical report (50-100 pages)
  - Executive summary
  - Methodology
  - Results (Pareto frontier, trade-offs)
  - Validation (accuracy, compliance)
  - Deployment plan
- Presentation (30 min)
  - Key findings
  - Top 3 recommendations
  - Implementation roadmap
  - ROI projection

**Deliverables:**
```
capstone/
├── technical_report.pdf (50+ pages)
├── code/
│   ├── simulation_models/
│   ├── surrogate_training/
│   ├── optimization/
│   ├── dashboard/
│   └── deployment_config/
├── results/
│   ├── pareto_frontier.png
│   ├── trade_off_analysis.html
│   ├── recommendation.json
│   └── validation_report.pdf
├── presentation.pptx
└── README.md
```

**Evaluation Criteria:**
- ✅ Achieves < 5% error on validation data
- ✅ Compliance score > 85%
- ✅ Hallucination rate < 1%
- ✅ Pareto frontier with 50+ solutions
- ✅ Documentation complete & clear
- ✅ Deployment checklist signed off
- ✅ Reproducible: Code + data for others

---

## 📋 Checklist: Mês 12 - Capstone Completion

- [ ] End-to-end system integration tested
- [ ] 1000 concurrent user stress test passed
- [ ] Security testing: All vulnerabilities fixed
- [ ] Compliance score > 85%, sign-off received
- [ ] Web dashboard deployed & functional
- [ ] API documentation complete with examples
- [ ] User guide & training materials created
- [ ] Operational runbooks written (5+ scenarios)
- [ ] Accuracy benchmarking: MAPE < 5% across types
- [ ] Performance benchmarking: SLA 99.5% uptime verified
- [ ] Hallucination rate < 1% on 1000 test queries
- [ ] Capstone project deliverables complete
- [ ] Technical report (50+ pages) submitted
- [ ] Presentation (30 min) prepared
- [ ] Code repository organized & documented
- [ ] Ready for production deployment & public demo

---

## 🎓 Curriculum Completion Summary

### Total Investment
- **Time:** 420-480 hours (12 months × 35-40h/week)
- **Months:** 1-7 (Foundation), 8-9 (Optimization & Production), 10-12 (Advanced & Capstone)

### Core Competencies Achieved

**Month 1-3: Data Science & Simulation**
- ✅ EnergyPlus automation
- ✅ Scientific software engineering
- ✅ Big data & time series analysis

**Month 4-5: AI/ML & LLM Integration**
- ✅ Physics-informed ML (surrogate models)
- ✅ Prompt engineering & LLM integration
- ✅ Hallucination detection & control

**Month 6-7: Architecture & Compliance**
- ✅ Co-simulation framework design
- ✅ Physics compliance testing
- ✅ Production-ready validation suite

**Month 8-9: Optimization & Deployment**
- ✅ Advanced multi-objective optimization
- ✅ DevOps & containerization
- ✅ Kubernetes orchestration
- ✅ CI/CD pipelines

**Month 10-12: Research & Integration**
- ✅ Federated learning & privacy
- ✅ Adaptive prompting & multi-agent systems
- ✅ Real-time monitoring & predictive maintenance
- ✅ Climate change resilience
- ✅ Transfer learning & domain adaptation
- ✅ Graph neural networks
- ✅ Explainability & interpretability
- ✅ Uncertainty quantification
- ✅ Full system integration & capstone

---

## 🚀 Post-Curriculum Paths

### Path A: Research & Academia
- Publish papers on physics-informed LLMs
- Federated learning for buildings
- Climate-aware design optimization
- PhD program applications

### Path B: Industry Product Development
- Launch SaaS platform for building design optimization
- Integration with popular CAD software (Revit, SketchUp)
- Real-time BMS optimization
- Licensing to MEP engineers & architects

### Path C: Consulting & Custom Solutions
- Build optimized designs for major clients
- Climate adaptation strategies
- Retrofit analysis & recommendations
- Energy transition planning

### Path D: Policy & Standardization
- Contribute to ASHRAE standards
- Building code updates
- Climate-aware building regulations
- International collaboration (ISO 13790, CEN)

---

## 📚 Recommended References

### Optimization
- Deb, K. (2001). "Multi-objective Optimization Using Evolutionary Algorithms"
- Forrester, A., et al. (2008). "Engineering Design via Surrogate Modelling"

### DevOps & Cloud
- Humble, J. & Farley, D. (2010). "Continuous Delivery"
- Newman, S. (2021). "Building Microservices" (2nd edition)

### Advanced AI
- LeCun, Y., Bengio, Y., Hinton, G. (2015). "Deep Learning" (Nature Review)
- Kipf & Welling (2016). "Semi-Supervised Classification with Graph Convolutional Networks"

### Buildings & Climate
- ASHRAE (2023). "ASHRAE Handbook - Fundamentals"
- IPCC (2021). "Climate Change 2021: Physical Science Basis"

---

## 🎯 Success Metrics (End of Month 12)

**Technical:**
- [ ] System accuracy > 95% on validation data
- [ ] Latency < 5 seconds for recommendations
- [ ] Uptime > 99.5% in production
- [ ] 0 critical security vulnerabilities
- [ ] 0 critical hallucinations in 1000 test queries

**Business:**
- [ ] Cost per recommendation < $0.10
- [ ] User satisfaction > 4.5/5 stars
- [ ] ROI for building owners > 5x
- [ ] Deployment to 10+ buildings

**Career:**
- [ ] Portfolio project for job applications
- [ ] Publication of research findings
- [ ] Speaking opportunity at conference
- [ ] Job offers from top ML/buildings companies

---

## 💡 Final Thoughts

This 12-month curriculum takes you from fundamentals to production-ready systems. The combination of:
- **Scientific rigor** (physics constraints, validation)
- **ML sophistication** (surrogates, LLMs, optimization)
- **Production excellence** (DevOps, monitoring, compliance)
- **Research innovation** (federated learning, climate adaptation)

...positions you at the intersection of science, engineering, and AI—a powerful combination for meaningful impact.

The buildings sector accounts for 30% of global CO2 emissions. The skills you've developed can contribute to decarbonization at massive scale.

**Good luck, and may your models always converge! 🚀**

---

**Curriculum Version:** 2.0 Complete (Months 1-12)  
**Last Updated:** January 13, 2026  
**Total Hours:** 420-480  
**Difficulty:** Intermediate → Advanced  
**Recommended Pace:** 35-40 hours/week

