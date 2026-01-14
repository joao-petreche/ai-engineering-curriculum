# Mês 12 - Week 3: Validation, Deployment & Monitoring

**Duration:** 12-15 hours | **Exercises:** 4 | **Target Audience:** Advanced ML/AI Engineers

---

## Overview

Week 3 moves your optimization from theory to production. You'll validate solutions in real-world pilots, deploy monitoring systems, coordinate multi-site rollout, and transfer knowledge to operations teams.

This week integrates:
- **Mês 9:** Production deployment and Kubernetes orchestration
- **Mês 11:** Advanced monitoring and observability
- **Mês 2:** Change management and knowledge transfer
- **Mês 10:** Real-time federation and distributed systems

---

## Exercise 3.1: Real-World Pilot Deployment & A/B Testing

**Duration:** 3 hours | **Difficulty:** Advanced

### Learning Objectives
- Design rigorous A/B testing methodology
- Implement control/treatment group randomization
- Deploy to production with safety mechanisms
- Conduct statistical validation of improvements

### Context

Theory meets reality in the pilot. This exercise teaches you to validate optimization improvements with statistical rigor before full rollout.

### Part A: A/B Testing Framework

```python
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from scipy import stats
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class ABTestDesign:
    """Design rigorous A/B tests for production validation"""
    
    def __init__(self, baseline_metrics: Dict[str, float]):
        self.baseline_metrics = baseline_metrics
        self.sample_size = None
        self.test_duration = None
        self.power = None
    
    def calculate_sample_size(self, metric: str, effect_size: float, alpha: float = 0.05, power: float = 0.80) -> int:
        """Calculate required sample size for statistical power"""
        
        from scipy.stats import norm
        
        # For proportion metric
        if self.baseline_metrics[metric] < 1.0:  # Assume it's a proportion
            p_baseline = self.baseline_metrics[metric]
            p_treatment = p_baseline * (1 + effect_size)  # Effect size as percentage
            
            pooled_p = (p_baseline + p_treatment) / 2
            
            z_alpha = norm.ppf(1 - alpha/2)
            z_beta = norm.ppf(power)
            
            n = 2 * ((z_alpha + z_beta)**2 * pooled_p * (1 - pooled_p)) / (p_treatment - p_baseline)**2
        
        else:  # Continuous metric
            baseline = self.baseline_metrics[metric]
            treatment = baseline * (1 + effect_size)
            
            z_alpha = norm.ppf(1 - alpha/2)
            z_beta = norm.ppf(power)
            
            sigma = baseline * 0.15  # Assume 15% coefficient of variation
            
            n = 2 * ((z_alpha + z_beta)**2 * sigma**2) / (treatment - baseline)**2
        
        self.sample_size = int(np.ceil(n))
        return self.sample_size
    
    def estimate_test_duration(self, daily_samples: int) -> int:
        """Estimate test duration in days"""
        
        if self.sample_size is None:
            raise ValueError("Calculate sample size first")
        
        self.test_duration = int(np.ceil(self.sample_size / daily_samples))
        return self.test_duration
    
    def design_hypothesis(self, metric: str, baseline: float, expected_improvement: float) -> Dict:
        """Design hypothesis test"""
        
        treatment_value = baseline * (1 + expected_improvement)
        
        hypothesis = {
            'null_hypothesis': f"μ_control = {baseline}",
            'alternative_hypothesis': f"μ_treatment = {treatment_value}",
            'expected_effect': f"{expected_improvement*100:.1f}%",
            'required_sample_size': self.calculate_sample_size(metric, expected_improvement),
            'confidence_level': "95%",
            'statistical_power': "80%",
        }
        
        return hypothesis

class ProductionPilot:
    """Run controlled A/B test in production"""
    
    def __init__(self, baseline_config: Dict, optimized_config: Dict, pilot_id: str):
        self.baseline_config = baseline_config
        self.optimized_config = optimized_config
        self.pilot_id = pilot_id
        
        self.control_group_data = []
        self.treatment_group_data = []
        
        self.start_time = None
        self.end_time = None
        
        self.results = {}
    
    def randomize_groups(self, total_units: int, treatment_ratio: float = 0.5) -> Dict:
        """Randomly assign units to control/treatment groups"""
        
        treatment_count = int(total_units * treatment_ratio)
        control_count = total_units - treatment_count
        
        # Randomly assign
        assignment = np.array(
            [1] * treatment_count + [0] * control_count
        )
        np.random.shuffle(assignment)
        
        return {
            'assignment': assignment,
            'control_count': control_count,
            'treatment_count': treatment_count,
            'ratio': treatment_ratio,
        }
    
    def simulate_production_pilot(self, duration_hours: int = 24, baseline_effect: float = 0.95, treatment_effect: float = 1.09) -> None:
        """Simulate production pilot (or can connect to real data stream)"""
        
        logger.info(f"\n🚀 Starting Pilot: {self.pilot_id}")
        logger.info(f"Duration: {duration_hours} hours")
        
        self.start_time = datetime.now()
        
        # Simulate hourly data collection
        for hour in range(duration_hours):
            timestamp = self.start_time + timedelta(hours=hour)
            
            # Generate control group data (baseline performance)
            # With random variation and slight degradation over time
            base_cost = 500 * baseline_effect * (1 + np.random.normal(0, 0.05))
            base_quality = 0.92 + np.random.normal(0, 0.02)
            base_throughput = 250 + np.random.normal(0, 25)
            
            self.control_group_data.append({
                'timestamp': timestamp,
                'hour': hour,
                'cost': base_cost,
                'quality': np.clip(base_quality, 0.85, 0.99),
                'throughput': max(base_throughput, 100),
                'group': 'control',
            })
            
            # Generate treatment group data (optimized performance)
            # Expect 9% cost reduction and 2% quality improvement
            opt_cost = 500 * treatment_effect * (1 + np.random.normal(0, 0.05))
            opt_quality = 0.94 + np.random.normal(0, 0.02)
            opt_throughput = 270 + np.random.normal(0, 25)
            
            self.treatment_group_data.append({
                'timestamp': timestamp,
                'hour': hour,
                'cost': opt_cost,
                'quality': np.clip(opt_quality, 0.87, 0.99),
                'throughput': max(opt_throughput, 120),
                'group': 'treatment',
            })
        
        self.end_time = datetime.now()
        
        logger.info(f"✅ Pilot completed at {self.end_time}")
    
    def analyze_results(self) -> Dict:
        """Statistically analyze pilot results"""
        
        control_df = pd.DataFrame(self.control_group_data)
        treatment_df = pd.DataFrame(self.treatment_group_data)
        
        metrics = {}
        
        # Compare cost
        control_cost = control_df['cost'].values
        treatment_cost = treatment_df['cost'].values
        
        cost_improvement = (control_cost.mean() - treatment_cost.mean()) / control_cost.mean()
        t_stat, p_value = stats.ttest_ind(control_cost, treatment_cost)
        
        metrics['cost'] = {
            'control_mean': control_cost.mean(),
            'treatment_mean': treatment_cost.mean(),
            'improvement': cost_improvement,
            'improvement_pct': f"{cost_improvement*100:.1f}%",
            'p_value': p_value,
            'statistically_significant': p_value < 0.05,
            't_statistic': t_stat,
        }
        
        # Compare quality
        control_quality = control_df['quality'].values
        treatment_quality = treatment_df['quality'].values
        
        quality_improvement = (treatment_quality.mean() - control_quality.mean()) / control_quality.mean()
        t_stat, p_value = stats.ttest_ind(control_quality, treatment_quality)
        
        metrics['quality'] = {
            'control_mean': control_quality.mean(),
            'treatment_mean': treatment_quality.mean(),
            'improvement': quality_improvement,
            'improvement_pct': f"{quality_improvement*100:.1f}%",
            'p_value': p_value,
            'statistically_significant': p_value < 0.05,
            't_statistic': t_stat,
        }
        
        # Compare throughput
        control_throughput = control_df['throughput'].values
        treatment_throughput = treatment_df['throughput'].values
        
        throughput_improvement = (treatment_throughput.mean() - control_throughput.mean()) / control_throughput.mean()
        t_stat, p_value = stats.ttest_ind(control_throughput, treatment_throughput)
        
        metrics['throughput'] = {
            'control_mean': control_throughput.mean(),
            'treatment_mean': treatment_throughput.mean(),
            'improvement': throughput_improvement,
            'improvement_pct': f"{throughput_improvement*100:.1f}%",
            'p_value': p_value,
            'statistically_significant': p_value < 0.05,
            't_statistic': t_stat,
        }
        
        self.results = metrics
        
        return metrics
    
    def generate_pilot_report(self) -> str:
        """Generate comprehensive pilot report"""
        
        report = f"# Pilot Test Report: {self.pilot_id}\n\n"
        
        report += "## Executive Summary\n\n"
        report += f"- **Duration:** {(self.end_time - self.start_time).total_seconds() / 3600:.1f} hours\n"
        report += f"- **Control Group:** {len(self.control_group_data)} observations\n"
        report += f"- **Treatment Group:** {len(self.treatment_group_data)} observations\n\n"
        
        report += "## Results\n\n"
        
        for metric_name, metric_results in self.results.items():
            report += f"### {metric_name.upper()}\n\n"
            report += f"- **Control:** {metric_results['control_mean']:.2f}\n"
            report += f"- **Treatment:** {metric_results['treatment_mean']:.2f}\n"
            report += f"- **Improvement:** {metric_results['improvement_pct']}\n"
            report += f"- **P-value:** {metric_results['p_value']:.4f}\n"
            report += f"- **Statistical Significance:** {'✅ YES' if metric_results['statistically_significant'] else '❌ NO'}\n\n"
        
        report += "## Recommendation\n\n"
        
        all_significant = all(
            m['statistically_significant'] for m in self.results.values()
        )
        
        if all_significant:
            report += "✅ **Approve for Full Rollout**\n"
            report += "All metrics show statistically significant improvement.\n"
        else:
            report += "⚠️ **Conditional Approval**\n"
            report += "Some metrics show improvement but need further validation.\n"
        
        return report
    
    def calculate_roi(self, daily_production_units: int, pilot_duration_days: int, full_year_days: int = 365) -> Dict:
        """Calculate ROI for full rollout"""
        
        if not self.results:
            raise ValueError("Run analyze_results first")
        
        cost_improvement_per_unit = (
            self.results['cost']['control_mean'] - 
            self.results['cost']['treatment_mean']
        )
        
        pilot_savings = cost_improvement_per_unit * daily_production_units * pilot_duration_days
        annual_savings = cost_improvement_per_unit * daily_production_units * full_year_days
        
        # Estimate implementation cost
        implementation_cost = 50000  # One-time cost
        payback_period_days = implementation_cost / (cost_improvement_per_unit * daily_production_units)
        
        roi = {
            'daily_saving_per_unit': cost_improvement_per_unit,
            'pilot_savings': pilot_savings,
            'annual_savings': annual_savings,
            'implementation_cost': implementation_cost,
            'payback_period_days': payback_period_days,
            'roi_percent': (annual_savings / implementation_cost) * 100,
        }
        
        return roi

# Example usage
if __name__ == "__main__":
    # Design test
    baseline = {
        'cost': 500,
        'quality': 0.92,
        'throughput': 250,
    }
    
    test_design = ABTestDesign(baseline)
    sample_size = test_design.calculate_sample_size('cost', effect_size=0.09)
    test_duration = test_design.estimate_test_duration(daily_samples=100)
    
    print(f"Required sample size: {sample_size}")
    print(f"Estimated test duration: {test_duration} days")
    
    # Run pilot
    pilot = ProductionPilot(
        baseline_config={'temperature': 130, 'pressure': 28},
        optimized_config={'temperature': 135, 'pressure': 30},
        pilot_id="Pilot_Line_A_2026_Q1"
    )
    
    # Simulate 24-hour pilot
    pilot.simulate_production_pilot(duration_hours=24)
    
    # Analyze results
    results = pilot.analyze_results()
    
    # Generate report
    report = pilot.generate_pilot_report()
    with open("pilot_report.md", "w") as f:
        f.write(report)
    
    # Calculate ROI
    roi = pilot.calculate_roi(
        daily_production_units=1000,
        pilot_duration_days=1,
        full_year_days=365
    )
    
    print("\n✅ Pilot completed successfully!")
    print(f"Estimated annual savings: ${roi['annual_savings']:,.0f}")
```

### Part B: Safety Mechanisms and Rollback

```python
class PilotSafetyMechanism:
    """Safety checks and automatic rollback"""
    
    def __init__(self, alert_thresholds: Dict[str, float]):
        self.alert_thresholds = alert_thresholds
        self.alerts = []
        self.rollback_triggered = False
    
    def check_metric(self, metric_name: str, value: float, threshold: float) -> bool:
        """Check if metric violates safety threshold"""
        
        if value < threshold:  # Assumes lower is worse for this example
            alert = {
                'timestamp': datetime.now(),
                'metric': metric_name,
                'value': value,
                'threshold': threshold,
                'violation': value - threshold,
            }
            self.alerts.append(alert)
            logger.warning(f"⚠️ ALERT: {metric_name} = {value:.2f} (threshold: {threshold:.2f})")
            return False
        
        return True
    
    def trigger_rollback(self) -> None:
        """Trigger automatic rollback to baseline configuration"""
        
        self.rollback_triggered = True
        logger.error("🛑 CRITICAL: Triggering automatic rollback!")
        
        # Send alerts to on-call team
        self._notify_team()
    
    def _notify_team(self) -> None:
        """Notify operations team of issues"""
        
        logger.info("Sending alerts to operations team...")
        # Integration with alerting system (PagerDuty, etc.)
```

### Part C: Deliverables

Create `PILOT_DEPLOYMENT_REPORT.md` including:

1. **Test Design** (2 pages)
   - Hypothesis and success criteria
   - Sample size calculation
   - Duration and resource requirements

2. **Pilot Execution** (2 pages)
   - Timeline and milestones
   - Group assignments and randomization
   - Data collection procedures

3. **Statistical Results** (2 pages)
   - Metrics comparison (control vs treatment)
   - P-values and significance
   - Effect sizes

4. **Financial Impact** (1 page)
   - Pilot ROI calculation
   - Projected annual savings
   - Payback period

5. **Go/No-Go Recommendation** (1 page)
   - Recommendation for full rollout
   - Conditions and prerequisites
   - Risk assessment

---

## Exercise 3.2: Real-Time Monitoring & Feedback Loops

**Duration:** 3 hours | **Difficulty:** Advanced

### Learning Objectives
- Implement real-time monitoring dashboards
- Create feedback loops for continuous improvement
- Detect and respond to anomalies
- Log and analyze production events

### Context

Once deployed, you need continuous visibility into production. This exercise builds monitoring systems that detect issues before they become problems.

### Part A: Real-Time Monitoring Pipeline

```python
from collections import deque
from threading import Thread
import json
from datetime import datetime

class MetricCollector:
    """Collect metrics from production systems in real-time"""
    
    def __init__(self, buffer_size: int = 1000):
        self.metrics_buffer = deque(maxlen=buffer_size)
        self.collection_thread = None
        self.is_running = False
    
    def start_collection(self, data_source: callable, interval_seconds: float = 5) -> None:
        """Start metric collection in background thread"""
        
        self.is_running = True
        self.collection_thread = Thread(
            target=self._collection_loop,
            args=(data_source, interval_seconds),
            daemon=True
        )
        self.collection_thread.start()
        logger.info("Metric collection started")
    
    def _collection_loop(self, data_source: callable, interval_seconds: float) -> None:
        """Background collection loop"""
        
        while self.is_running:
            try:
                metric = data_source()
                metric['timestamp'] = datetime.now()
                self.metrics_buffer.append(metric)
                
                time.sleep(interval_seconds)
            except Exception as e:
                logger.error(f"Collection error: {e}")
    
    def stop_collection(self) -> None:
        """Stop metric collection"""
        
        self.is_running = False
        if self.collection_thread:
            self.collection_thread.join()
        logger.info("Metric collection stopped")
    
    def get_latest_metrics(self, lookback_minutes: int = 5) -> List[Dict]:
        """Get metrics from last N minutes"""
        
        now = datetime.now()
        cutoff = now - timedelta(minutes=lookback_minutes)
        
        return [
            m for m in self.metrics_buffer
            if m['timestamp'] > cutoff
        ]

class AnomalyDetector:
    """Detect anomalies in real-time metrics"""
    
    def __init__(self, baseline_stats: Dict):
        self.baseline_stats = baseline_stats
        self.anomalies = []
    
    def statistical_test(self, metric_values: List[float], metric_name: str, threshold_std: float = 2.5) -> List[Dict]:
        """Detect anomalies using statistical test (Z-score)"""
        
        baseline_mean = self.baseline_stats[metric_name]['mean']
        baseline_std = self.baseline_stats[metric_name]['std']
        
        detected_anomalies = []
        
        for value in metric_values:
            z_score = abs((value - baseline_mean) / baseline_std)
            
            if z_score > threshold_std:
                anomaly = {
                    'timestamp': datetime.now(),
                    'metric': metric_name,
                    'value': value,
                    'baseline_mean': baseline_mean,
                    'z_score': z_score,
                    'severity': 'critical' if z_score > 3.0 else 'warning',
                }
                detected_anomalies.append(anomaly)
                self.anomalies.append(anomaly)
        
        return detected_anomalies
    
    def isolation_forest_detection(self, metric_dataframe: pd.DataFrame) -> List[Dict]:
        """Detect anomalies using Isolation Forest"""
        
        from sklearn.ensemble import IsolationForest
        
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        predictions = iso_forest.fit_predict(metric_dataframe)
        
        anomalies = []
        for idx, is_anomaly in enumerate(predictions):
            if is_anomaly == -1:
                anomalies.append({
                    'index': idx,
                    'timestamp': metric_dataframe.iloc[idx].get('timestamp'),
                    'values': metric_dataframe.iloc[idx].to_dict(),
                })
        
        return anomalies

class ProductionDashboard:
    """Real-time production monitoring dashboard"""
    
    def __init__(self):
        self.metrics_history = {}
        self.alerts = []
        self.sla_status = {}
    
    def update_sla_status(self, metric_name: str, value: float, sla_target: float) -> None:
        """Update SLA (Service Level Agreement) status"""
        
        sla_met = value >= sla_target
        
        self.sla_status[metric_name] = {
            'current_value': value,
            'sla_target': sla_target,
            'met': sla_met,
            'status': '✅ OK' if sla_met else '❌ VIOLATION',
            'last_updated': datetime.now(),
        }
    
    def generate_dashboard_html(self) -> str:
        """Generate HTML dashboard for monitoring"""
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Production Monitoring Dashboard</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .metric { 
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 5px;
                    background-color: #f5f5f5;
                }
                .ok { background-color: #d4edda; border-left: 4px solid #28a745; }
                .warning { background-color: #fff3cd; border-left: 4px solid #ffc107; }
                .critical { background-color: #f8d7da; border-left: 4px solid #dc3545; }
            </style>
        </head>
        <body>
            <h1>Production Monitoring Dashboard</h1>
            <p>Last updated: {}</p>
            <div class="metrics">
        """.format(datetime.now())
        
        for metric_name, sla_info in self.sla_status.items():
            css_class = 'ok' if sla_info['met'] else 'critical'
            html += f"""
            <div class="metric {css_class}">
                <h3>{metric_name}</h3>
                <p>Current: {sla_info['current_value']:.2f}</p>
                <p>Target: {sla_info['sla_target']:.2f}</p>
                <p>{sla_info['status']}</p>
            </div>
            """
        
        html += """
            </div>
        </body>
        </html>
        """
        
        return html

class FeedbackLoop:
    """Continuous improvement feedback loop"""
    
    def __init__(self, monitoring_system: ProductionDashboard):
        self.monitoring = monitoring_system
        self.feedback_history = []
    
    def collect_feedback(self, metric_changes: Dict) -> Dict:
        """Analyze metric changes and suggest adjustments"""
        
        feedback = {
            'timestamp': datetime.now(),
            'observations': [],
            'recommendations': [],
        }
        
        for metric_name, change_pct in metric_changes.items():
            if abs(change_pct) > 0.05:  # >5% change
                feedback['observations'].append(
                    f"{metric_name} changed by {change_pct*100:.1f}%"
                )
        
        # Generate recommendations based on feedback
        if 'cost' in metric_changes and metric_changes['cost'] > 0.05:
            feedback['recommendations'].append(
                "Cost increased. Consider reviewing configuration parameters."
            )
        
        if 'quality' in metric_changes and metric_changes['quality'] < -0.02:
            feedback['recommendations'].append(
                "Quality decreased. Trigger immediate investigation."
            )
        
        self.feedback_history.append(feedback)
        return feedback

# Example usage
if __name__ == "__main__":
    # Create monitoring system
    dashboard = ProductionDashboard()
    
    # Simulate metric collection
    baseline_stats = {
        'cost': {'mean': 450, 'std': 25},
        'quality': {'mean': 0.93, 'std': 0.02},
    }
    
    anomaly_detector = AnomalyDetector(baseline_stats)
    
    # Simulate metrics over time
    for i in range(100):
        cost = np.random.normal(450, 25)
        quality = np.random.normal(0.93, 0.02)
        
        # Inject an anomaly at t=50
        if i == 50:
            cost = 600  # Major cost spike
        
        dashboard.update_sla_status('cost', cost, sla_target=500)
        dashboard.update_sla_status('quality', quality, sla_target=0.90)
    
    # Detect anomalies
    anomalies = anomaly_detector.statistical_test([600], 'cost')
    print(f"Detected {len(anomalies)} anomalies")
```

### Part B: Alert Management

```python
class AlertManager:
    """Manage alerts and escalation"""
    
    def __init__(self):
        self.active_alerts = []
        self.escalation_levels = {
            'info': 0,
            'warning': 1,
            'critical': 2,
        }
    
    def create_alert(self, severity: str, metric: str, message: str) -> Dict:
        """Create alert"""
        
        alert = {
            'id': f"alert_{len(self.active_alerts)}",
            'timestamp': datetime.now(),
            'severity': severity,
            'metric': metric,
            'message': message,
            'acknowledged': False,
        }
        
        self.active_alerts.append(alert)
        
        # Trigger action based on severity
        if severity == 'critical':
            self._escalate_to_manager(alert)
        
        return alert
    
    def _escalate_to_manager(self, alert: Dict) -> None:
        """Escalate critical alert to manager"""
        
        logger.error(f"🚨 CRITICAL ALERT: {alert['message']}")
        # Integration with alerting service (PagerDuty, Slack, etc.)
```

### Part C: Deliverables

Create `MONITORING_FEEDBACK_REPORT.md` including:

1. **Monitoring Architecture** (2 pages)
   - Data collection infrastructure
   - Metrics and KPIs tracked
   - Dashboard design

2. **Anomaly Detection** (2 pages)
   - Detection methods (statistical, ML-based)
   - Anomalies detected during deployment
   - Response actions taken

3. **Alert Management** (1 page)
   - Alert levels and escalation
   - On-call procedures
   - False positive rate

4. **Feedback Loop Performance** (1 page)
   - Feedback collected and acted upon
   - Continuous improvement actions
   - Metric trends over time

---

## Exercise 3.3: Multi-Site Rollout Strategy

**Duration:** 2.5 hours | **Difficulty:** Intermediate

### Learning Objectives
- Plan phased rollout across multiple facilities
- Coordinate resource allocation
- Manage change across organization
- Track rollout progress and risks

### Context

Successful rollout requires careful planning. This exercise coordinates deployment across multiple sites with minimal disruption.

### Part A: Rollout Planning

```python
class RolloutPlan:
    """Plan phased rollout across multiple sites"""
    
    def __init__(self, sites: List[str], total_duration_weeks: int = 12):
        self.sites = sites
        self.total_duration = total_duration_weeks
        self.rollout_schedule = {}
        self.risk_assessments = {}
    
    def create_phased_schedule(self, phases: int = 3) -> Dict:
        """Create phased rollout schedule"""
        
        sites_per_phase = len(self.sites) // phases
        schedule = {}
        
        for phase in range(phases):
            phase_sites = self.sites[
                phase * sites_per_phase:(phase + 1) * sites_per_phase
            ]
            
            start_week = phase * (self.total_duration // phases)
            duration_weeks = self.total_duration // phases
            
            schedule[f'phase_{phase+1}'] = {
                'sites': phase_sites,
                'start_week': start_week,
                'duration_weeks': duration_weeks,
                'key_milestones': [
                    'Kickoff',
                    'Configuration',
                    'Testing',
                    'Go-live',
                    'Stabilization',
                ],
            }
        
        self.rollout_schedule = schedule
        return schedule
    
    def assess_site_risk(self, site: str, factors: Dict[str, str]) -> Dict:
        """Assess deployment risk for each site"""
        
        risk_score = 0
        
        # Factor 1: System complexity
        if factors.get('system_complexity') == 'high':
            risk_score += 3
        elif factors.get('system_complexity') == 'medium':
            risk_score += 2
        else:
            risk_score += 1
        
        # Factor 2: Operational staff readiness
        if factors.get('staff_readiness') == 'low':
            risk_score += 3
        elif factors.get('staff_readiness') == 'medium':
            risk_score += 1
        
        # Factor 3: Production criticality
        if factors.get('criticality') == 'high':
            risk_score += 2
        
        risk_level = 'high' if risk_score > 6 else ('medium' if risk_score > 3 else 'low')
        
        self.risk_assessments[site] = {
            'score': risk_score,
            'level': risk_level,
            'factors': factors,
        }
        
        return self.risk_assessments[site]
    
    def prioritize_sites(self) -> List[str]:
        """Prioritize sites for rollout (low-risk first)"""
        
        sorted_sites = sorted(
            self.risk_assessments.items(),
            key=lambda x: x[1]['score']
        )
        
        return [site for site, _ in sorted_sites]

class RolloutExecutionTracker:
    """Track rollout progress and issues"""
    
    def __init__(self):
        self.milestones = []
        self.issues = []
        self.resource_allocation = {}
    
    def record_milestone(self, site: str, milestone: str, status: str) -> None:
        """Record milestone completion"""
        
        self.milestones.append({
            'timestamp': datetime.now(),
            'site': site,
            'milestone': milestone,
            'status': status,  # 'completed', 'delayed', 'blocked'
        })
    
    def log_issue(self, site: str, issue_type: str, description: str, severity: str) -> None:
        """Log issues encountered during rollout"""
        
        self.issues.append({
            'timestamp': datetime.now(),
            'site': site,
            'type': issue_type,
            'description': description,
            'severity': severity,  # 'low', 'medium', 'critical'
            'resolved': False,
        })
    
    def generate_rollout_status(self) -> str:
        """Generate rollout status report"""
        
        status = "# Rollout Status Report\n\n"
        
        status += f"## Milestones Completed: {len(self.milestones)}\n\n"
        for m in self.milestones[-5:]:  # Last 5 milestones
            status += f"- {m['site']}: {m['milestone']} - {m['status']}\n"
        
        status += f"\n## Active Issues: {len([i for i in self.issues if not i['resolved']])}\n\n"
        for i in [issue for issue in self.issues if not issue['resolved']][:5]:
            status += f"- {i['site']}: {i['description']} ({i['severity']})\n"
        
        return status

# Example usage
if __name__ == "__main__":
    # Create rollout plan
    sites = ["Site_A_US", "Site_B_EU", "Site_C_APAC", "Site_D_Americas"]
    
    plan = RolloutPlan(sites, total_duration_weeks=12)
    schedule = plan.create_phased_schedule(phases=2)
    
    # Assess risk
    for site in sites:
        plan.assess_site_risk(site, {
            'system_complexity': 'medium',
            'staff_readiness': 'high',
            'criticality': 'high',
        })
    
    # Prioritize
    prioritized = plan.prioritize_sites()
    print(f"Rollout order: {prioritized}")
    
    # Track execution
    tracker = RolloutExecutionTracker()
    tracker.record_milestone("Site_A_US", "Configuration", "completed")
    tracker.record_milestone("Site_A_US", "Testing", "in-progress")
    
    # Status report
    status = tracker.generate_rollout_status()
    print(status)
```

### Part B: Deliverables

Create `ROLLOUT_STRATEGY_REPORT.md` including:

1. **Rollout Plan** (2 pages)
   - Phased approach and timeline
   - Site prioritization
   - Resource allocation

2. **Risk Assessment** (2 pages)
   - Site-specific risks
   - Mitigation strategies
   - Contingency plans

3. **Execution Tracking** (1 page)
   - Milestones and progress
   - Issues and resolutions
   - Lessons learned

---

## Exercise 3.4: Knowledge Transfer & Documentation

**Duration:** 2 hours | **Difficulty:** Intermediate

### Learning Objectives
- Create operational documentation
- Train operations teams
- Document configuration and procedures
- Establish runbooks for common scenarios

### Context

Optimization is worthless if the team can't maintain and operate it. This exercise ensures knowledge transfer to operations.

### Part A: Documentation & Training

```python
class OperationalDocumentation:
    """Create operational documentation for production systems"""
    
    def __init__(self, system_name: str):
        self.system_name = system_name
        self.documents = {}
    
    def create_quick_start_guide(self, configuration: Dict, key_parameters: List[str]) -> str:
        """Create quick start guide for operators"""
        
        guide = f"# {self.system_name} - Quick Start Guide\n\n"
        
        guide += "## Overview\n"
        guide += "This system optimizes production for cost and quality.\n\n"
        
        guide += "## Key Parameters\n\n"
        guide += "| Parameter | Optimal Value | Range | Why? |\n"
        guide += "|-----------|--------------|-------|------|\n"
        
        for param in key_parameters:
            guide += f"| {param} | {configuration.get(param, 'N/A')} | [min, max] | Impacts cost/quality |\n"
        
        guide += "\n## Daily Checklist\n"
        guide += "- [ ] Monitor key parameters within ranges\n"
        guide += "- [ ] Check system health dashboard\n"
        guide += "- [ ] Log any anomalies\n"
        guide += "- [ ] Verify quality metrics\n\n"
        
        guide += "## Troubleshooting\n"
        guide += "See detailed troubleshooting guide for common issues.\n\n"
        
        guide += "## Emergency Contacts\n"
        guide += "- Technical Support: +1-XXX-XXX-XXXX\n"
        guide += "- Operations Lead: ops-lead@company.com\n"
        
        self.documents['quick_start'] = guide
        return guide
    
    def create_runbook(self, scenario: str, steps: List[str], expected_outcome: str) -> str:
        """Create runbook for specific operational scenario"""
        
        runbook = f"# Runbook: {scenario}\n\n"
        
        runbook += "## Situation\n"
        runbook += f"When: {scenario}\n\n"
        
        runbook += "## Steps\n"
        for i, step in enumerate(steps, 1):
            runbook += f"{i}. {step}\n"
        
        runbook += f"\n## Expected Outcome\n"
        runbook += f"{expected_outcome}\n\n"
        
        runbook += "## Rollback (if needed)\n"
        runbook += "1. Contact technical support\n"
        runbook += "2. Revert to baseline configuration\n"
        runbook += "3. Monitor system for 30 minutes\n"
        
        self.documents[f'runbook_{scenario}'] = runbook
        return runbook
    
    def create_troubleshooting_guide(self) -> str:
        """Create comprehensive troubleshooting guide"""
        
        guide = "# Troubleshooting Guide\n\n"
        
        guide += "## Issue: High Production Cost\n"
        guide += "**Symptoms:** Cost metric 20%+ above baseline\n"
        guide += "**Diagnosis:**\n"
        guide += "1. Check temperature setting (should be 135°C)\n"
        guide += "2. Verify pressure setting (should be 30 bar)\n"
        guide += "**Solution:**\n"
        guide += "- Adjust parameters to optimal values\n"
        guide += "- Monitor cost trend for 1 hour\n"
        guide += "- If not improving, contact support\n\n"
        
        guide += "## Issue: Low Product Quality\n"
        guide += "**Symptoms:** Quality score < 90%\n"
        guide += "**Diagnosis:**\n"
        guide += "1. Check equipment maintenance schedule\n"
        guide += "2. Verify material supplier quality\n"
        guide += "**Solution:**\n"
        guide += "- Slow down flow rate temporarily\n"
        guide += "- Contact quality team\n\n"
        
        self.documents['troubleshooting'] = guide
        return guide

class TrainingProgram:
    """Organize training for operations staff"""
    
    def __init__(self, system_name: str):
        self.system_name = system_name
        self.training_modules = []
    
    def add_training_module(self, title: str, duration_minutes: int, content: str, audience: str) -> None:
        """Add training module"""
        
        module = {
            'title': title,
            'duration_minutes': duration_minutes,
            'content': content,
            'audience': audience,
            'completed_by': [],
        }
        
        self.training_modules.append(module)
    
    def create_training_schedule(self, num_batches: int = 3, batch_size: int = 20) -> List[Dict]:
        """Create training schedule for all staff"""
        
        schedule = []
        
        for batch in range(num_batches):
            for module in self.training_modules:
                schedule.append({
                    'batch': batch + 1,
                    'module': module['title'],
                    'duration_minutes': module['duration_minutes'],
                    'audience': module['audience'],
                    'start_date': datetime.now() + timedelta(days=batch*7),
                })
        
        return schedule
    
    def generate_training_content(self) -> str:
        """Generate training materials"""
        
        content = f"# Training Program: {self.system_name}\n\n"
        
        content += "## Modules\n\n"
        for module in self.training_modules:
            content += f"### {module['title']}\n"
            content += f"- Duration: {module['duration_minutes']} minutes\n"
            content += f"- Audience: {module['audience']}\n"
            content += f"- Content: {module['content'][:100]}...\n\n"
        
        return content

# Example usage
if __name__ == "__main__":
    # Create documentation
    docs = OperationalDocumentation("Production Optimization System")
    
    quick_start = docs.create_quick_start_guide(
        configuration={'temperature': 135, 'pressure': 30, 'flow_rate': 85},
        key_parameters=['temperature', 'pressure', 'flow_rate']
    )
    
    runbook = docs.create_runbook(
        scenario="Cost exceeds 20% threshold",
        steps=[
            "Check current cost metric on dashboard",
            "Review temperature and pressure settings",
            "Adjust temperature down by 5°C",
            "Monitor cost for 30 minutes",
            "If no improvement, contact support",
        ],
        expected_outcome="Cost returns to baseline levels"
    )
    
    troubleshooting = docs.create_troubleshooting_guide()
    
    # Create training program
    training = TrainingProgram("Production Optimization System")
    
    training.add_training_module(
        title="System Overview",
        duration_minutes=30,
        content="Overview of optimization system, key metrics, and interfaces",
        audience="All operators"
    )
    
    training.add_training_module(
        title="Daily Operations",
        duration_minutes=45,
        content="Daily monitoring procedures, alert responses, troubleshooting",
        audience="Plant operators"
    )
    
    training.add_training_module(
        title="Advanced Configuration",
        duration_minutes=60,
        content="Parameter tuning, sensitivity analysis, advanced troubleshooting",
        audience="Supervisors and technical leads"
    )
    
    schedule = training.create_training_schedule(num_batches=2)
    print(f"Training schedule created with {len(schedule)} sessions")
```

### Part B: Deliverables

Create `KNOWLEDGE_TRANSFER_REPORT.md` including:

1. **Operational Documentation** (3 pages)
   - Quick start guide
   - System architecture overview
   - Configuration parameters and ranges

2. **Runbooks and Procedures** (3 pages)
   - Common operational scenarios
   - Step-by-step procedures
   - Emergency procedures and rollback

3. **Troubleshooting Guide** (2 pages)
   - Common issues and symptoms
   - Diagnostic procedures
   - Solutions and escalation paths

4. **Training Program** (2 pages)
   - Training modules and schedule
   - Certification requirements
   - Knowledge assessment tests

---

## Week 3 Summary

### What You've Accomplished
- ✅ Deployed optimization with rigorous A/B testing
- ✅ Established real-time monitoring and alerting
- ✅ Planned multi-site rollout with risk management
- ✅ Transferred knowledge to operations teams

### Key Deliverables
1. Pilot Deployment Report (7 pages)
2. Monitoring & Feedback Report (6 pages)
3. Rollout Strategy Report (5 pages)
4. Knowledge Transfer Report (10 pages)

### Technology Stack Used
- A/B testing and statistical analysis
- Kubernetes-based monitoring (from Mês 9)
- Real-time dashboards and alerting
- Feedback loops and continuous improvement

### Certification Checkpoint
**✅ Week 3 Complete** when you have:
- [ ] Pilot completed with statistical validation
- [ ] Monitoring system operational
- [ ] Multi-site rollout plan approved
- [ ] Operations staff trained
- [ ] All 4 exercises completed with documentation

---

## Next Week Preview

**Week 4: Publication, Results & Capstone**
- Comprehensive results reporting
- Academic publication preparation
- Industry case study development
- Final capstone presentation

**Estimated Effort:** 14-15 hours, 4 exercises

---

## References

1. Kohavi, R., Longbotham, R., Sommerfield, D., & Henne, R. M. (2009). "Controlled experiments on the web: survey and practical guide"
2. Nagaraj, K., & Fiore, C. (2020). "Observability Engineering"
3. Humble, J., & Farley, D. (2010). "Continuous Delivery"
4. Forsgren, N., Humble, J., & Kim, G. (2018). "Accelerate"

---

**Prepared by:** AI Engineering Curriculum Team  
**Date:** January 14, 2026  
**Status:** Ready for Execution
