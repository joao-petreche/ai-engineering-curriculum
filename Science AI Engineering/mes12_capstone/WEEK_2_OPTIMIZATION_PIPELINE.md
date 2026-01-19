# Mês 12 - Week 2: Algorithm Pipeline & Optimization

**Duration:** 12-15 hours | **Exercises:** 4 | **Target Audience:** Advanced ML/AI Engineers

---

## Overview

Week 2 transforms your problem definition and data into production optimization. You'll implement federated optimization across multiple sites, integrate LLM guidance for domain insights, apply constrained optimization with real business rules, and validate robustness.

This week integrates:
- **Mês 10:** Federated learning and distributed optimization
- **Mês 11:** Sensitivity analysis and constrained optimization
- **Mês 5:** LLM prompting for domain insights
- **Mês 8:** Multi-objective optimization and Pareto frontiers

---

## Exercise 2.1: Federated Multi-Site Optimization

**Duration:** 3 hours | **Difficulty:** Advanced

### Learning Objectives
- Implement federated optimization across distributed sites
- Coordinate local and global optimization objectives
- Handle site-specific constraints and data privacy
- Monitor federation convergence and performance

### Context

Modern enterprises operate across multiple facilities. Optimizing each site independently misses synergies; optimizing globally ignores local constraints. Federated optimization balances both.

### Part A: Federated Optimization Architecture

```python
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

@dataclass
class SiteConfig:
    """Configuration for a production site"""
    site_id: str
    location: str
    capacity: float
    operating_costs: float
    quality_baseline: float
    constraints: Dict[str, float]
    data: pd.DataFrame

class OptimizationObjective:
    """Define multi-objective optimization problem"""
    
    def __init__(self):
        self.objectives = []
        self.weights = []
    
    def add_objective(self, objective_func: callable, weight: float, name: str):
        """Add objective function with weight"""
        self.objectives.append({
            'function': objective_func,
            'weight': weight,
            'name': name
        })
        self.weights.append(weight)
    
    def normalize_weights(self):
        """Ensure weights sum to 1"""
        total = sum(self.weights)
        self.weights = [w / total for w in self.weights]
        for i, obj in enumerate(self.objectives):
            obj['weight'] = self.weights[i]
    
    def evaluate(self, config: np.ndarray) -> float:
        """Evaluate weighted sum of objectives"""
        scores = [
            obj['weight'] * obj['function'](config)
            for obj in self.objectives
        ]
        return sum(scores)

class LocalOptimizer:
    """Optimize at individual site level"""
    
    def __init__(self, site_config: SiteConfig):
        self.site_config = site_config
        self.local_best_config = None
        self.local_best_score = float('-inf')
        self.iteration_history = []
    
    def optimize_locally(self, objective: OptimizationObjective, iterations: int = 50) -> np.ndarray:
        """Local optimization using genetic algorithm"""
        
        from deap import base, creator, tools, algorithms
        
        logger.info(f"[{self.site_config.site_id}] Starting local optimization...")
        
        # Define DEAP problem
        if not hasattr(creator, "FitnessMax"):
            creator.create("FitnessMax", base.Fitness, weights=(1.0,))
            creator.create("Individual", list, fitness=creator.FitnessMax)
        
        toolbox = base.Toolbox()
        
        # Attribute generators
        n_params = 10  # Number of configuration parameters
        toolbox.register("param", np.random.uniform, 0, 1)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.param, n=n_params)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        
        # Evaluation function
        def evaluate(individual):
            config = np.array(individual)
            # Check constraints
            if self._check_local_constraints(config):
                return (objective.evaluate(config),)
            else:
                return (-1e6,)  # Penalize constraint violations
        
        toolbox.register("evaluate", evaluate)
        toolbox.register("mate", tools.cxBlend, alpha=0.5)
        toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.2, indpb=0.2)
        toolbox.register("select", tools.selTournament, tournsize=3)
        
        # Bounds checking
        def check_bounds(min_bound, max_bound):
            def decorator(func):
                def wrapper(*args, **kwargs):
                    offspring = func(*args, **kwargs)
                    for child in offspring:
                        for i in range(len(child)):
                            if child[i] < min_bound:
                                child[i] = min_bound
                            elif child[i] > max_bound:
                                child[i] = max_bound
                    return offspring
                return wrapper
            return decorator
        
        toolbox.decorate("mate", check_bounds(0, 1))
        toolbox.decorate("mutate", check_bounds(0, 1))
        
        # Run algorithm
        pop, logbook = algorithms.eaSimple(
            toolbox.population(n=30),
            toolbox,
            cxpb=0.7,
            mutpb=0.3,
            ngen=iterations,
            verbose=False
        )
        
        # Extract best solution
        best_individual = tools.selBest(pop, k=1)[0]
        self.local_best_config = np.array(best_individual)
        self.local_best_score = evaluate(best_individual)[0]
        
        logger.info(f"[{self.site_config.site_id}] Local optimization complete. Score: {self.local_best_score:.4f}")
        
        return self.local_best_config
    
    def _check_local_constraints(self, config: np.ndarray) -> bool:
        """Check if configuration violates site constraints"""
        
        # Cost constraint
        estimated_cost = config[0] * self.site_config.operating_costs
        if estimated_cost > self.site_config.constraints.get('max_cost', float('inf')):
            return False
        
        # Quality constraint
        estimated_quality = config[1] + self.site_config.quality_baseline
        if estimated_quality < self.site_config.constraints.get('min_quality', 0):
            return False
        
        # Capacity constraint
        if config[2] > self.site_config.capacity:
            return False
        
        return True
    
    def get_configuration(self) -> Dict:
        """Return site's optimized configuration"""
        return {
            'site_id': self.site_config.site_id,
            'parameters': self.local_best_config,
            'score': self.local_best_score,
        }

class FederatedOptimizer:
    """Coordinate optimization across multiple sites (FedAvg algorithm)"""
    
    def __init__(self, sites: List[SiteConfig]):
        self.sites = sites
        self.local_optimizers = {
            site.site_id: LocalOptimizer(site) for site in sites
        }
        self.global_best_config = None
        self.federation_history = []
        self.convergence_metrics = []
    
    def federated_optimize(self, objective: OptimizationObjective, max_iterations: int = 100) -> Dict:
        """Federated averaging optimization loop"""
        
        logger.info(f"\n🚀 Starting Federated Optimization ({len(self.sites)} sites)")
        logger.info(f"Objective: {', '.join([obj['name'] for obj in objective.objectives])}")
        
        self.global_best_config = np.random.uniform(0, 1, 10)
        
        for fed_iter in range(max_iterations):
            logger.info(f"\n--- Federated Iteration {fed_iter + 1}/{max_iterations} ---")
            
            # Step 1: Local optimization at each site
            local_results = {}
            for site_id, optimizer in self.local_optimizers.items():
                # Broadcast global best to local optimizer
                optimizer.local_best_config = self.global_best_config.copy()
                
                # Local optimization with perturbation
                perturbed_objective = self._create_perturbed_objective(objective, site_id)
                local_config = optimizer.optimize_locally(perturbed_objective, iterations=20)
                
                local_results[site_id] = {
                    'config': local_config,
                    'score': optimizer.local_best_score,
                }
                
                logger.info(f"  Site {site_id}: Score = {optimizer.local_best_score:.4f}")
            
            # Step 2: Federated Averaging (FedAvg)
            self.global_best_config = self._federated_average(local_results)
            
            # Step 3: Evaluate global performance
            global_score = self._evaluate_global_config(self.global_best_config, objective)
            
            # Step 4: Check convergence
            convergence = self._check_convergence(fed_iter)
            self.convergence_metrics.append({
                'iteration': fed_iter,
                'global_score': global_score,
                'convergence': convergence,
            })
            
            logger.info(f"  Global Score: {global_score:.4f} | Convergence: {convergence:.4f}")
            
            # Early stopping
            if convergence < 0.001 and fed_iter > 10:
                logger.info(f"✅ Converged at iteration {fed_iter + 1}")
                break
        
        return {
            'global_best_config': self.global_best_config,
            'global_best_score': global_score,
            'local_results': {
                site_id: {
                    'config': results['config'],
                    'score': results['score'],
                } for site_id, results in local_results.items()
            },
            'convergence_history': self.convergence_metrics,
        }
    
    def _create_perturbed_objective(self, objective: OptimizationObjective, site_id: str) -> OptimizationObjective:
        """Create site-specific objective with constraints"""
        
        perturbed = OptimizationObjective()
        site = next(s for s in self.sites if s.site_id == site_id)
        
        for obj in objective.objectives:
            # Add site-specific penalty
            def perturbed_func(config, original_func=obj['function'], site=site):
                base_score = original_func(config)
                
                # Penalty for deviating from site operating point
                deviation = np.linalg.norm(config - self.global_best_config)
                deviation_penalty = 0.1 * deviation
                
                return base_score - deviation_penalty
            
            perturbed.add_objective(perturbed_func, obj['weight'], obj['name'])
        
        return perturbed
    
    def _federated_average(self, local_results: Dict) -> np.ndarray:
        """Federated Averaging (FedAvg) algorithm"""
        
        configs = np.array([results['config'] for results in local_results.values()])
        weights = np.array([results['score'] for results in local_results.values()])
        
        # Normalize weights
        weights = weights - weights.min()
        weights = weights / (weights.sum() + 1e-10)
        
        # Weighted average
        global_config = np.average(configs, axis=0, weights=weights)
        
        return global_config
    
    def _evaluate_global_config(self, config: np.ndarray, objective: OptimizationObjective) -> float:
        """Evaluate configuration across all sites"""
        
        scores = []
        for site in self.sites:
            optimizer = self.local_optimizers[site.site_id]
            # Check constraints
            if optimizer._check_local_constraints(config):
                score = objective.evaluate(config)
            else:
                score = -1e6
            scores.append(score)
        
        return np.mean(scores)
    
    def _check_convergence(self, iteration: int, window: int = 5) -> float:
        """Check convergence by measuring score variance in recent iterations"""
        
        if len(self.convergence_metrics) < window:
            return float('inf')
        
        recent_scores = [m['global_score'] for m in self.convergence_metrics[-window:]]
        convergence = np.std(recent_scores)
        
        return convergence
    
    def generate_federation_report(self) -> str:
        """Generate detailed federation report"""
        
        report = "# Federated Optimization Report\n\n"
        
        # Convergence plot data
        iterations = [m['iteration'] for m in self.convergence_metrics]
        scores = [m['global_score'] for m in self.convergence_metrics]
        
        report += f"## Convergence Summary\n"
        report += f"- Total Iterations: {len(self.convergence_metrics)}\n"
        report += f"- Final Global Score: {scores[-1]:.4f}\n"
        report += f"- Score Improvement: {scores[-1] - scores[0]:.4f}\n\n"
        
        report += "## Site-Specific Results\n\n"
        for site_id, optimizer in self.local_optimizers.items():
            report += f"### {site_id}\n"
            report += f"- Local Score: {optimizer.local_best_score:.4f}\n"
            report += f"- Configuration: {optimizer.local_best_config[:3]}\n\n"
        
        return report

# Example usage
if __name__ == "__main__":
    # Create site configurations
    sites = [
        SiteConfig(
            site_id="Site_A_US",
            location="Texas, USA",
            capacity=1000,
            operating_costs=50,
            quality_baseline=90,
            constraints={'max_cost': 400, 'min_quality': 95},
            data=pd.DataFrame({'production': [100, 110, 105]})
        ),
        SiteConfig(
            site_id="Site_B_EU",
            location="Germany, EU",
            capacity=800,
            operating_costs=60,
            quality_baseline=92,
            constraints={'max_cost': 420, 'min_quality': 96},
            data=pd.DataFrame({'production': [95, 105, 100]})
        ),
        SiteConfig(
            site_id="Site_C_APAC",
            location="Singapore, APAC",
            capacity=600,
            operating_costs=40,
            quality_baseline=88,
            constraints={'max_cost': 350, 'min_quality': 92},
            data=pd.DataFrame({'production': [85, 95, 90]})
        ),
    ]
    
    # Define objectives
    objective = OptimizationObjective()
    objective.add_objective(
        lambda config: -config[0] * 100,  # Minimize cost
        weight=0.5,
        name="Cost Minimization"
    )
    objective.add_objective(
        lambda config: config[1] * 50,  # Maximize quality
        weight=0.3,
        name="Quality Maximization"
    )
    objective.add_objective(
        lambda config: config[2] * 30,  # Maximize throughput
        weight=0.2,
        name="Throughput Maximization"
    )
    objective.normalize_weights()
    
    # Run federated optimization
    federated = FederatedOptimizer(sites)
    results = federated.federated_optimize(objective, max_iterations=100)
    
    # Generate report
    report = federated.generate_federation_report()
    with open("federated_optimization_report.md", "w") as f:
        f.write(report)
    
    print("\n✅ Federated optimization complete!")
    print(f"Global best score: {results['global_best_score']:.4f}")
```

### Part B: Distributed Communication & Aggregation

```python
class FederationCommunicationLayer:
    """Handle communication between sites"""
    
    def __init__(self, sites: List[str], communication_latency_ms: float = 100):
        self.sites = sites
        self.latency = communication_latency_ms
        self.message_log = []
    
    def broadcast_global_config(self, config: np.ndarray) -> Dict:
        """Broadcast global best configuration to all sites"""
        
        message = {
            'type': 'broadcast',
            'timestamp': datetime.now(),
            'config': config,
            'recipients': self.sites,
            'latency_ms': self.latency,
        }
        
        self.message_log.append(message)
        return message
    
    def aggregate_local_results(self, local_configs: Dict[str, np.ndarray], aggregation_method: str = 'weighted_avg') -> np.ndarray:
        """Aggregate local configurations"""
        
        if aggregation_method == 'weighted_avg':
            # Weighted average by model quality
            pass
        elif aggregation_method == 'median':
            # Robust median aggregation (Byzantine-resistant)
            return np.median(list(local_configs.values()), axis=0)
        elif aggregation_method == 'trimmed_mean':
            # Trimmed mean (remove extremes)
            configs = np.array(list(local_configs.values()))
            return np.mean(np.sort(configs, axis=0)[1:-1], axis=0)
        
        return np.mean(list(local_configs.values()), axis=0)
    
    def detect_stragglers(self, response_times: Dict[str, float], threshold_percentile: int = 90) -> List[str]:
        """Detect slow sites (stragglers)"""
        
        times = np.array(list(response_times.values()))
        threshold = np.percentile(times, threshold_percentile)
        
        stragglers = [
            site for site, time in response_times.items()
            if time > threshold
        ]
        
        return stragglers

```

### Part C: Deliverables

Create `FEDERATED_OPTIMIZATION_REPORT.md` including:

1. **Architecture Overview** (2 pages)
   - Federated topology and communication
   - Local vs global optimization balance
   - Constraint handling strategy

2. **Convergence Analysis** (2 pages)
   - Convergence curves and metrics
   - Comparison to centralized optimization
   - Communication overhead analysis

3. **Site-Specific Results** (2 pages)
   - Results for each site
   - Local vs global trade-offs
   - Constraint satisfaction verification

4. **Performance Metrics** (1 page)
   - Global objectives achieved
   - Improvement vs baseline
   - Multi-site coordination benefits

---

## Exercise 2.2: LLM-Guided Configuration Generation

**Duration:** 3 hours | **Difficulty:** Advanced

### Learning Objectives
- Integrate LLMs for domain-specific insights
- Generate interpretable configuration recommendations
- Extract and validate domain knowledge
- Create human-AI collaboration loops

### Context

LLMs understand domain knowledge from training data. This exercise harnesses that to guide optimization, making the process more interpretable and faster to converge.

### Part A: LLM Integration for Optimization

```python
from typing import List, Dict
import json
import re

class DomainExpertLLM:
    """Leverage LLM as domain expert for optimization"""
    
    def __init__(self, model_name: str = "gpt-4", temperature: float = 0.7):
        """Initialize LLM-based domain expert"""
        self.model_name = model_name
        self.temperature = temperature
        self.knowledge_base = {}
        self.recommendations = []
    
    def extract_domain_constraints(self, problem_description: str) -> Dict:
        """Extract domain-specific constraints from problem"""
        
        prompt = f"""
        As a domain expert in optimization, analyze this production problem:
        
        {problem_description}
        
        Extract and list:
        1. Key operational constraints
        2. Critical success factors
        3. Typical parameter ranges
        4. Known trade-offs
        5. Common failure modes
        
        Provide JSON response.
        """
        
        # Call LLM (pseudo-code)
        # response = call_llm(prompt, temperature=0.5)
        
        # Example response
        constraints = {
            "operational": [
                "Temperature must stay within equipment limits (50-200°C)",
                "Pressure cannot exceed vessel rating (50 bar)",
                "Cannot change settings more than 10% per hour",
            ],
            "critical_factors": [
                "Product quality (minimize defects)",
                "Equipment safety (prevent failures)",
                "Cost efficiency (minimize waste)",
            ],
            "typical_ranges": {
                "temperature": [100, 150],
                "pressure": [20, 40],
                "flow_rate": [50, 100],
            },
            "known_tradeoffs": [
                "Higher temperature improves throughput but reduces quality",
                "Higher pressure increases yield but increases energy cost",
            ],
            "failure_modes": [
                "Thermal runaway if temperature not controlled",
                "Equipment corrosion if pressure too high",
                "Blockages if flow rate too low",
            ]
        }
        
        self.knowledge_base['constraints'] = constraints
        return constraints
    
    def generate_initial_configurations(self, objective: str, num_configs: int = 5) -> List[Dict]:
        """Generate promising initial configurations via LLM"""
        
        prompt = f"""
        For a production optimization problem with objective: {objective}
        
        Based on domain knowledge, suggest {num_configs} promising initial configurations.
        
        For each configuration, provide:
        1. Configuration values (temperature, pressure, flow rate, etc.)
        2. Rationale for these values
        3. Expected performance metrics
        4. Key risks
        
        Format as JSON with configurations array.
        """
        
        # Example LLM response
        configurations = [
            {
                "id": "config_1_conservative",
                "description": "Conservative operating point - prioritize quality",
                "parameters": {
                    "temperature": 120,
                    "pressure": 25,
                    "flow_rate": 75,
                },
                "rationale": "Moderate settings ensure consistent quality",
                "expected_quality": 95,
                "expected_cost": 450,
                "expected_throughput": 200,
                "risks": ["Lower throughput"]
            },
            {
                "id": "config_2_aggressive",
                "description": "Aggressive operating point - maximize throughput",
                "parameters": {
                    "temperature": 160,
                    "pressure": 38,
                    "flow_rate": 95,
                },
                "rationale": "Push envelope for maximum production",
                "expected_quality": 88,
                "expected_cost": 520,
                "expected_throughput": 350,
                "risks": ["Higher defect rate", "Equipment stress"]
            },
            {
                "id": "config_3_balanced",
                "description": "Balanced operating point - optimize trade-offs",
                "parameters": {
                    "temperature": 140,
                    "pressure": 30,
                    "flow_rate": 85,
                },
                "rationale": "Sweet spot between quality and throughput",
                "expected_quality": 92,
                "expected_cost": 480,
                "expected_throughput": 280,
                "risks": ["None significant"]
            },
        ]
        
        self.knowledge_base['initial_configs'] = configurations
        return configurations
    
    def guide_optimization_search(self, current_solution: Dict, constraints: Dict, iterations: int = 10) -> List[Dict]:
        """Provide guidance for next optimization steps"""
        
        prompt = f"""
        Current solution performance:
        {json.dumps(current_solution, indent=2)}
        
        Constraints to respect:
        {json.dumps(constraints, indent=2)}
        
        Suggest {iterations} small improvement steps:
        1. Which parameter to adjust
        2. Direction and magnitude
        3. Expected improvement
        4. Risk assessment
        
        Prioritize low-risk, high-impact changes.
        """
        
        # LLM-generated suggestions
        suggestions = [
            {
                "step": 1,
                "parameter": "temperature",
                "adjustment": "+5°C",
                "reason": "Increase throughput without quality impact",
                "expected_improvement": "5% cost reduction",
                "risk_level": "Low",
            },
            {
                "step": 2,
                "parameter": "flow_rate",
                "adjustment": "+10 units",
                "reason": "Better material utilization",
                "expected_improvement": "3% quality improvement",
                "risk_level": "Low",
            },
            {
                "step": 3,
                "parameter": "pressure",
                "adjustment": "+2 bar",
                "reason": "Enhance reaction kinetics",
                "expected_improvement": "2% yield improvement",
                "risk_level": "Medium",
            },
        ]
        
        return suggestions
    
    def validate_configuration(self, config: Dict, constraints: Dict) -> Dict:
        """Validate configuration against constraints"""
        
        validation_prompt = f"""
        Validate this configuration against constraints:
        
        Configuration: {json.dumps(config, indent=2)}
        Constraints: {json.dumps(constraints, indent=2)}
        
        Check:
        1. Physical feasibility
        2. Operational safety
        3. Regulatory compliance
        4. Equipment capability
        
        Return validation result with any warnings or issues.
        """
        
        # Validation result
        validation = {
            "valid": True,
            "checks": {
                "physical_feasibility": {
                    "passed": True,
                    "notes": "All parameters within physical bounds"
                },
                "operational_safety": {
                    "passed": True,
                    "notes": "No safety hazards identified"
                },
                "regulatory_compliance": {
                    "passed": True,
                    "notes": "Meets ISO 9001 requirements"
                },
                "equipment_capability": {
                    "passed": True,
                    "notes": "Within equipment specs"
                }
            },
            "warnings": [],
            "recommendations": [
                "Monitor temperature closely in first 30 minutes",
                "Verify pressure sensor calibration",
            ]
        }
        
        return validation
    
    def explain_optimization_results(self, results: Dict) -> str:
        """Generate human-readable explanation of results"""
        
        explanation_prompt = f"""
        Explain these optimization results to a plant manager:
        
        Results: {json.dumps(results, indent=2)}
        
        Provide:
        1. What changed and why
        2. Expected business impact (in dollars)
        3. Implementation steps
        4. Risks and mitigation
        5. Success metrics
        
        Use simple, non-technical language.
        """
        
        # Generate explanation
        explanation = f"""
        # Optimization Results Summary
        
        ## What's Changing
        We optimized your production line configuration based on {len(results)} different parameters.
        The new configuration is expected to reduce costs while maintaining quality.
        
        ## Expected Impact
        - **Cost Savings:** ~15% reduction ($X per month)
        - **Quality:** Maintain 95%+ pass rate
        - **Throughput:** 8% increase in daily output
        - **Timeline to ROI:** 3 months
        
        ## Implementation Plan
        1. Week 1: Validate new configuration in test environment
        2. Week 2: Pilot with 20% of production
        3. Week 3: Monitor performance and collect feedback
        4. Week 4: Full rollout if results confirm projections
        
        ## Risks and Mitigation
        - Risk: Equipment adjustment may take time
          → Mitigation: We'll have technical team on-site during transition
        
        - Risk: New parameters might need fine-tuning
          → Mitigation: We've built in 2-week validation period
        
        ## Success Metrics
        Track these daily:
        - Defect rate (should stay <5%)
        - Energy consumption (should drop 12-15%)
        - Equipment temperature (should be stable)
        """
        
        return explanation

# Example usage
if __name__ == "__main__":
    expert = DomainExpertLLM()
    
    # Extract domain constraints
    constraints = expert.extract_domain_constraints(
        "Optimize chemical reactor for cost minimization while maintaining 95% product purity"
    )
    
    # Generate initial configurations
    initial_configs = expert.generate_initial_configurations(
        objective="Minimize production cost per unit while maintaining quality",
        num_configs=5
    )
    
    # Get optimization guidance
    current_solution = {
        "parameters": {"temperature": 130, "pressure": 28},
        "cost": 500,
        "quality": 92,
    }
    suggestions = expert.guide_optimization_search(
        current_solution,
        constraints,
        iterations=5
    )
    
    # Validate proposed configuration
    new_config = {
        "temperature": 135,
        "pressure": 30,
        "flow_rate": 80,
    }
    validation = expert.validate_configuration(new_config, constraints)
    
    # Explain results
    results = {
        "old_config": {"cost": 500, "quality": 92},
        "new_config": {"cost": 425, "quality": 94},
    }
    explanation = expert.explain_optimization_results(results)
    print(explanation)
```

### Part B: Human-in-the-Loop Optimization

```python
class HumanInTheLoopOptimization:
    """Interactive optimization with human feedback"""
    
    def __init__(self, objective_func, llm_expert):
        self.objective_func = objective_func
        self.llm = llm_expert
        self.human_feedback = []
        self.iteration = 0
    
    def interactive_round(self, current_best: Dict) -> Dict:
        """One round of human-in-the-loop optimization"""
        
        self.iteration += 1
        
        # Step 1: LLM suggests improvements
        suggestions = self.llm.guide_optimization_search(
            current_best,
            constraints={},
            iterations=3
        )
        
        # Step 2: Present to human
        print(f"\n=== Iteration {self.iteration} ===")
        print("LLM Suggestions for improvement:")
        for i, sugg in enumerate(suggestions, 1):
            print(f"  {i}. {sugg['parameter']}: {sugg['adjustment']} ({sugg['reason']})")
        
        # Step 3: Get human feedback (simulated)
        feedback = {
            "selected_suggestion": 1,  # Human selects suggestion 1
            "confidence": "high",
            "custom_override": None,  # No override
        }
        
        self.human_feedback.append({
            "iteration": self.iteration,
            "feedback": feedback,
            "timestamp": datetime.now(),
        })
        
        # Step 4: Apply feedback and evaluate
        improved_config = current_best.copy()
        if feedback["selected_suggestion"]:
            sugg = suggestions[feedback["selected_suggestion"] - 1]
            # Apply adjustment...
        
        return improved_config
    
    def run_interactive_optimization(self, initial_config: Dict, num_rounds: int = 5) -> Dict:
        """Run multiple rounds of human-in-the-loop optimization"""
        
        current_best = initial_config
        
        for _ in range(num_rounds):
            current_best = self.interactive_round(current_best)
        
        return current_best
```

### Part C: Deliverables

Create `LLM_GUIDED_OPTIMIZATION_REPORT.md` including:

1. **Domain Knowledge Extraction** (2 pages)
   - Constraints identified
   - Failure modes and mitigation
   - Known trade-offs

2. **Initial Configuration Generation** (1 page)
   - Generated configurations
   - Rationale for each
   - Expected performance

3. **Optimization Guidance** (2 pages)
   - Suggested parameter adjustments
   - Risk assessment for each step
   - Expected improvements

4. **Validation Results** (1 page)
   - Configuration validation results
   - Safety and feasibility checks
   - Warnings and recommendations

5. **Human-AI Collaboration** (1 page)
   - Interactive optimization rounds
   - Human feedback integration
   - Final accepted configuration

---

## Exercise 2.3: Constrained Multi-Objective Optimization

**Duration:** 2.5 hours | **Difficulty:** Advanced

### Learning Objectives
- Implement constrained optimization with real constraints
- Handle multiple competing objectives
- Generate Pareto-optimal solutions
- Validate constraint satisfaction

### Context

Real-world optimization isn't about a single objective—it's about satisfying hard constraints while optimizing multiple competing goals.

### Part A: Constraint-Aware Optimization

```python
from scipy.optimize import minimize, LinearConstraint, Bounds
import warnings

class ConstrainedOptimizer:
    """Optimization with explicit constraint handling"""
    
    def __init__(self):
        self.constraints = []
        self.bounds = []
        self.objectives = {}
    
    def add_hard_constraint(self, name: str, constraint_func: Callable[[np.ndarray], bool]) -> None:
        """Add hard constraint that must be satisfied"""
        self.constraints.append({
            'type': 'hard',
            'name': name,
            'func': constraint_func,
        })
    
    def add_soft_constraint(self, name: str, penalty_func: Callable[[np.ndarray], float], weight: float = 1.0) -> None:
        """Add soft constraint with penalty for violation"""
        self.constraints.append({
            'type': 'soft',
            'name': name,
            'func': penalty_func,
            'weight': weight,
        })
    
    def add_objective(self, name: str, objective_func: Callable[[np.ndarray], float], weight: float = 1.0) -> None:
        """Add optimization objective"""
        self.objectives[name] = {
            'func': objective_func,
            'weight': weight,
        }
    
    def check_constraints(self, config: np.ndarray) -> Tuple[bool, List[str]]:
        """Check if configuration satisfies all hard constraints"""
        
        violations = []
        
        for constraint in self.constraints:
            if constraint['type'] == 'hard':
                if not constraint['func'](config):
                    violations.append(constraint['name'])
        
        return len(violations) == 0, violations
    
    def evaluate_with_penalties(self, config: np.ndarray) -> float:
        """Evaluate objective with soft constraint penalties"""
        
        # Check hard constraints
        feasible, violations = self.check_constraints(config)
        
        if not feasible:
            # Large penalty for infeasible solution
            return 1e10 + len(violations) * 1e9
        
        # Evaluate objectives
        objective_value = 0
        for name, obj in self.objectives.items():
            value = obj['func'](config)
            objective_value += obj['weight'] * value
        
        # Add soft constraint penalties
        total_penalty = 0
        for constraint in self.constraints:
            if constraint['type'] == 'soft':
                penalty = constraint['func'](config)
                total_penalty += constraint['weight'] * penalty
        
        return objective_value + total_penalty
    
    def optimize(self, initial_guess: np.ndarray, bounds: List[Tuple], method: str = 'SLSQP') -> Dict:
        """Perform constrained optimization"""
        
        result = minimize(
            fun=self.evaluate_with_penalties,
            x0=initial_guess,
            method=method,
            bounds=bounds,
            options={'maxiter': 1000, 'ftol': 1e-9}
        )
        
        optimal_config = result.x
        feasible, violations = self.check_constraints(optimal_config)
        
        return {
            'optimal_config': optimal_config,
            'optimal_value': result.fun,
            'feasible': feasible,
            'violations': violations,
            'iterations': result.nit,
            'convergence': result.success,
        }

class MultiObjectiveOptimizer:
    """Multi-objective optimization with Pareto front"""
    
    def __init__(self, constraint_optimizer: ConstrainedOptimizer):
        self.constraint_optimizer = constraint_optimizer
        self.pareto_front = []
    
    def generate_pareto_front(self, n_points: int = 20) -> List[Dict]:
        """Generate Pareto-optimal solutions"""
        
        from scipy.spatial import distance
        
        pareto_solutions = []
        
        # Scalarization approach: generate different weight combinations
        for i in range(n_points):
            weight1 = i / n_points
            weight2 = 1 - weight1
            
            # Temporarily modify weights
            original_weights = {name: obj['weight'] for name, obj in self.constraint_optimizer.objectives.items()}
            
            objectives = list(self.constraint_optimizer.objectives.keys())
            if len(objectives) >= 2:
                self.constraint_optimizer.objectives[objectives[0]]['weight'] = weight1
                self.constraint_optimizer.objectives[objectives[1]]['weight'] = weight2
            
            # Optimize with these weights
            result = self.constraint_optimizer.optimize(
                initial_guess=np.random.uniform(0, 1, 10),
                bounds=[(0, 1)] * 10
            )
            
            if result['feasible']:
                # Evaluate all objectives
                objective_values = {}
                for name, obj in self.constraint_optimizer.objectives.items():
                    objective_values[name] = obj['func'](result['optimal_config'])
                
                pareto_solutions.append({
                    'config': result['optimal_config'],
                    'objectives': objective_values,
                    'weights': {'obj1': weight1, 'obj2': weight2},
                })
            
            # Restore weights
            for name, weight in original_weights.items():
                self.constraint_optimizer.objectives[name]['weight'] = weight
        
        # Filter to Pareto front (remove dominated solutions)
        self.pareto_front = self._filter_pareto_front(pareto_solutions)
        
        return self.pareto_front
    
    def _filter_pareto_front(self, solutions: List[Dict]) -> List[Dict]:
        """Filter to only Pareto-optimal solutions"""
        
        pareto = []
        
        for sol in solutions:
            is_dominated = False
            
            for other_sol in solutions:
                if sol == other_sol:
                    continue
                
                # Check if other_sol dominates sol
                dominates = True
                for metric in sol['objectives']:
                    if other_sol['objectives'][metric] < sol['objectives'][metric]:
                        dominates = False
                        break
                
                if dominates:
                    is_dominated = True
                    break
            
            if not is_dominated:
                pareto.append(sol)
        
        return pareto
    
    def visualize_pareto_front(self, save_path: str = "pareto_front.png") -> None:
        """Visualize Pareto front (for 2D case)"""
        
        if len(self.pareto_front) == 0:
            logger.warning("Empty Pareto front")
            return
        
        objectives_list = list(self.pareto_front[0]['objectives'].keys())
        
        if len(objectives_list) >= 2:
            obj1_values = [sol['objectives'][objectives_list[0]] for sol in self.pareto_front]
            obj2_values = [sol['objectives'][objectives_list[1]] for sol in self.pareto_front]
            
            import matplotlib.pyplot as plt
            
            plt.figure(figsize=(10, 6))
            plt.scatter(obj1_values, obj2_values, s=100, alpha=0.6)
            plt.xlabel(objectives_list[0])
            plt.ylabel(objectives_list[1])
            plt.title("Pareto Front")
            plt.grid(True)
            plt.savefig(save_path)
            logger.info(f"Saved Pareto front plot to {save_path}")

# Example usage
if __name__ == "__main__":
    # Create optimizer
    optimizer = ConstrainedOptimizer()
    
    # Add constraints
    optimizer.add_hard_constraint(
        "cost_limit",
        lambda x: x[0] * 100 <= 500  # Cost must be <= 500
    )
    optimizer.add_hard_constraint(
        "quality_minimum",
        lambda x: x[1] >= 0.9  # Quality >= 90%
    )
    optimizer.add_soft_constraint(
        "temperature_preference",
        lambda x: abs(x[2] - 0.5) * 10,  # Prefer temperature near 0.5
        weight=0.1
    )
    
    # Add objectives
    optimizer.add_objective(
        "cost",
        lambda x: x[0] * 100,  # Minimize cost
        weight=0.6
    )
    optimizer.add_objective(
        "quality",
        lambda x: -(x[1] * 100),  # Maximize quality
        weight=0.4
    )
    
    # Multi-objective optimization
    mo_optimizer = MultiObjectiveOptimizer(optimizer)
    pareto_front = mo_optimizer.generate_pareto_front(n_points=20)
    
    print(f"\n✅ Generated {len(pareto_front)} Pareto-optimal solutions")
    
    # Visualize
    mo_optimizer.visualize_pareto_front()
```

### Part B: Deliverables

Create `CONSTRAINED_OPTIMIZATION_REPORT.md` including:

1. **Constraint Definition** (2 pages)
   - Hard constraints and validation
   - Soft constraints and penalties
   - Feasibility region analysis

2. **Optimization Results** (2 pages)
   - Optimal solutions for different weight scenarios
   - Constraint satisfaction verification
   - Trade-off analysis

3. **Pareto Front Analysis** (2 pages)
   - Pareto-optimal solutions generated
   - Visualization and interpretation
   - Solution selection criteria

---

## Exercise 2.4: Robustness Testing & Sensitivity Analysis

**Duration:** 2.5 hours | **Difficulty:** Advanced

### Learning Objectives
- Perform sensitivity analysis on optimal solutions
- Test robustness to parameter variations
- Identify critical parameters
- Generate uncertainty margins

### Context

Production environments are uncertain. Optimal solutions in the lab may fail in reality. This exercise tests robustness and identifies what needs tight control.

### Part A: Sensitivity Analysis

```python
from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.plotting.bar import plot as barplot
import matplotlib.pyplot as plt

class SensitivityAnalyzer:
    """Analyze sensitivity of optimization to parameters"""
    
    def __init__(self, objective_func: Callable, num_samples: int = 1000):
        self.objective_func = objective_func
        self.num_samples = num_samples
        self.sensitivity_results = {}
    
    def morris_sensitivity(self, parameters: Dict[str, List[float]]) -> Dict:
        """One-at-a-time sensitivity analysis (Morris method)"""
        
        from SALib.sample import morris as morris_sampler
        from SALib.analyze import morris as morris_analyzer
        
        problem = {
            'num_vars': len(parameters),
            'names': list(parameters.keys()),
            'bounds': [[min(v), max(v)] for v in parameters.values()]
        }
        
        param_values = morris_sampler.sample(problem, N=1000, num_levels=10)
        
        Y = np.array([self.objective_func(x) for x in param_values])
        
        Si = morris_analyzer.analyze(problem, param_values, Y)
        
        return {
            'mu': Si['mu'],  # Mean effect
            'sigma': Si['sigma'],  # Interaction/nonlinearity
            'mu_star': Si['mu_star'],  # Mean absolute effect
        }
    
    def sobol_sensitivity(self, parameters: Dict[str, List[float]]) -> Dict:
        """Variance-based sensitivity analysis (Sobol method)"""
        
        problem = {
            'num_vars': len(parameters),
            'names': list(parameters.keys()),
            'bounds': [[min(v), max(v)] for v in parameters.values()]
        }
        
        # Generate samples
        param_values = saltelli.sample(problem, N=1000, calc_second_order=True)
        
        # Evaluate objective
        Y = np.array([self.objective_func(x) for x in param_values])
        
        # Analyze sensitivity
        Si = sobol.analyze(problem, Y)
        
        return {
            'S1': Si['S1'],  # First-order indices
            'S1_conf': Si['S1_conf'],
            'ST': Si['ST'],  # Total-order indices
        }
    
    def generate_sensitivity_report(self, morris_results: Dict, sobol_results: Dict) -> str:
        """Generate sensitivity analysis report"""
        
        report = "# Sensitivity Analysis Report\n\n"
        
        report += "## Parameter Importance (Morris Method)\n\n"
        report += "| Parameter | μ* (Overall Effect) | σ (Interaction) |\n"
        report += "|-----------|-------------------|------------------|\n"
        
        for i, param_name in enumerate(list(morris_results['mu_star'].keys())):
            mu_star = morris_results['mu_star'][param_name]
            sigma = morris_results['sigma'][param_name]
            report += f"| {param_name} | {mu_star:.4f} | {sigma:.4f} |\n"
        
        report += "\n## Variance Decomposition (Sobol Method)\n\n"
        report += "| Parameter | S1 (Main Effect) | ST (Total Effect) |\n"
        report += "|-----------|------------------|-------------------|\n"
        
        for i, param_name in enumerate(list(sobol_results['S1'].keys())):
            s1 = sobol_results['S1'][param_name]
            st = sobol_results['ST'][param_name]
            report += f"| {param_name} | {s1:.4f} | {st:.4f} |\n"
        
        return report

class RobustnessAnalyzer:
    """Test robustness of solutions to perturbations"""
    
    def __init__(self, optimal_config: np.ndarray, objective_func: Callable):
        self.optimal_config = optimal_config
        self.objective_func = objective_func
        self.robustness_results = {}
    
    def test_parameter_variations(self, variation_levels: List[float] = [0.95, 0.975, 1.0, 1.025, 1.05]) -> Dict:
        """Test how performance changes with parameter variations"""
        
        results = {'variation_levels': variation_levels, 'performance': []}
        
        for level in variation_levels:
            perturbed_config = self.optimal_config * level
            performance = self.objective_func(perturbed_config)
            results['performance'].append(performance)
        
        self.robustness_results['parameter_variations'] = results
        
        return results
    
    def monte_carlo_robustness(self, num_samples: int = 1000, std_dev: float = 0.05) -> Dict:
        """Monte Carlo robustness testing with random perturbations"""
        
        performances = []
        
        for _ in range(num_samples):
            noise = np.random.normal(0, std_dev, len(self.optimal_config))
            perturbed_config = self.optimal_config + (self.optimal_config * noise)
            
            # Clip to valid bounds
            perturbed_config = np.clip(perturbed_config, 0, 1)
            
            performance = self.objective_func(perturbed_config)
            performances.append(performance)
        
        performances = np.array(performances)
        
        robustness_metrics = {
            'mean_performance': np.mean(performances),
            'std_performance': np.std(performances),
            'worst_case': np.max(performances),
            'best_case': np.min(performances),
            'coefficient_of_variation': np.std(performances) / np.mean(performances),
        }
        
        self.robustness_results['monte_carlo'] = robustness_metrics
        
        return robustness_metrics
    
    def worst_case_scenario_test(self, worst_scenarios: List[np.ndarray]) -> Dict:
        """Test performance under worst-case scenarios"""
        
        results = {}
        
        for i, scenario_config in enumerate(worst_scenarios):
            performance = self.objective_func(scenario_config)
            results[f'scenario_{i}'] = {
                'config': scenario_config,
                'performance': performance,
                'degradation_pct': (performance - self.objective_func(self.optimal_config)) / self.objective_func(self.optimal_config) * 100,
            }
        
        self.robustness_results['worst_case'] = results
        
        return results
```

### Part B: Uncertainty Margins

```python
class UncertaintyAnalysis:
    """Quantify uncertainty margins in optimized solution"""
    
    def __init__(self, optimal_value: float, robustness_metrics: Dict):
        self.optimal_value = optimal_value
        self.robustness_metrics = robustness_metrics
    
    def calculate_safety_margins(self) -> Dict:
        """Calculate safety margins for deployment"""
        
        std_dev = self.robustness_metrics['std_performance']
        
        margins = {
            '1_sigma_margin': 1 * std_dev,  # 68% confidence
            '2_sigma_margin': 2 * std_dev,  # 95% confidence
            '3_sigma_margin': 3 * std_dev,  # 99.7% confidence
        }
        
        return margins
    
    def generate_implementation_spec(self, optimal_config: Dict, safety_margins: Dict) -> str:
        """Generate implementation specification with margins"""
        
        spec = "# Implementation Specification\n\n"
        
        spec += "## Optimal Configuration\n\n"
        for param, value in optimal_config.items():
            spec += f"- {param}: {value}\n"
        
        spec += "\n## Operating Ranges (with Safety Margins)\n\n"
        
        for param, optimal_value in optimal_config.items():
            margin = safety_margins.get('1_sigma_margin', optimal_value * 0.05)
            lower = optimal_value - margin
            upper = optimal_value + margin
            spec += f"- {param}: [{lower:.2f}, {upper:.2f}] (optimal: {optimal_value:.2f})\n"
        
        spec += "\n## Monitoring Requirements\n\n"
        spec += "- Monitor parameters within specified ranges\n"
        spec += "- Alert if parameter deviates >1σ from optimal\n"
        spec += "- Automatically re-optimize if deviation >2σ\n"
        spec += "- Stop process if violation >3σ\n"
        
        return spec
```

### Part C: Deliverables

Create `ROBUSTNESS_ANALYSIS_REPORT.md` including:

1. **Sensitivity Analysis** (2 pages)
   - Morris one-at-a-time analysis
   - Sobol variance decomposition
   - Critical parameters identified

2. **Robustness Testing** (2 pages)
   - Parameter variation results
   - Monte Carlo robustness metrics
   - Worst-case scenario analysis

3. **Uncertainty Quantification** (1 page)
   - Safety margins at 1σ, 2σ, 3σ
   - Probability distributions
   - Risk assessment

4. **Implementation Specification** (1 page)
   - Operating ranges with margins
   - Monitoring requirements
   - Alert thresholds

---

## Week 2 Summary

### What You've Accomplished
- ✅ Implemented federated multi-site optimization
- ✅ Integrated LLMs for domain guidance
- ✅ Applied constrained multi-objective optimization
- ✅ Validated robustness and uncertainty

### Key Deliverables
1. Federated Optimization Report (6 pages)
2. LLM-Guided Optimization Report (8 pages)
3. Constrained Multi-Objective Report (6 pages)
4. Robustness Analysis Report (6 pages)

### Technology Stack Used
- DEAP genetic algorithms
- Scipy constrained optimization (SLSQP)
- SALib sensitivity analysis
- LangChain + LLM integration
- Pareto front analysis

### Certification Checkpoint
**✅ Week 2 Complete** when you have:
- [ ] Federated optimization converged across all sites
- [ ] LLM guidance integrated and validated
- [ ] Pareto-optimal solutions generated
- [ ] Robustness testing completed
- [ ] All 4 exercises completed with documentation

---

## Next Week Preview

**Week 3: Validation, Deployment & Monitoring**
- Real-world pilot deployment
- Monitoring and feedback loops
- Multi-site rollout strategy
- Knowledge transfer documentation

**Estimated Effort:** 12-15 hours, 4 exercises

---

## References

1. McMahan, H. B., et al. (2017). "Communication-efficient learning of deep networks from decentralized data"
2. Forrester, A., Sobester, A., & Keane, A. (2008). "Engineering design via surrogate modelling"
3. Saltelli, A., et al. (2008). "Global sensitivity analysis"
4. OpenAI. "GPT-4 Technical Report"

---

**Prepared by:** AI Engineering Curriculum Team  
**Date:** January 14, 2026  
**Status:** Ready for Execution
