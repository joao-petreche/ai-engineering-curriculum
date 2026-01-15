# Mês 12 - Week 1: Domain Problem Selection & Data Preparation

**Duration:** 12-15 hours | **Exercises:** 4 | **Target Audience:** Advanced ML/AI Engineers

---

## Overview

Week 1 establishes the foundation for your capstone project by taking you from problem conception to baseline model. You'll select or define a real-world optimization challenge, prepare production-scale data, train surrogate models for efficiency, and establish performance baselines.

This week integrates:
- **Mês 1-3:** Domain knowledge, big data pipelines, data quality
- **Mês 4:** Surrogate modeling techniques
- **Mês 2:** Software engineering best practices
- **Mês 7:** Physics-informed constraints

---

## Exercise 1.1: Problem Formulation & Domain Definition

**Duration:** 3 hours | **Difficulty:** Intermediate

### Learning Objectives
- Define a well-scoped optimization problem
- Identify objectives, constraints, and stakeholder requirements
- Establish success metrics and evaluation framework
- Plan data collection strategy

### Context
Real-world optimization projects often fail not due to algorithm limitations, but due to poor problem definition. This exercise teaches you how to structure domain problems rigorously for computational optimization.

### Problem Statement

You are a Lead Data Scientist at an industrial company. Your task: define a capstone optimization problem from one of these domains:

1. **Manufacturing/Logistics:** Production line scheduling, supply chain optimization, quality control
2. **Energy:** Building HVAC optimization, grid demand forecasting, renewable integration
3. **Chemical Engineering:** Reactor condition optimization, yield maximization, safety constraints
4. **Finance:** Portfolio optimization, trading algorithm tuning, risk management
5. **Telecommunications:** Network resource allocation, 5G coverage optimization, customer churn prediction

### Part A: Problem Definition Template

Create a detailed problem specification document covering:

```python
# Problem Definition Structure
problem_definition = {
    "domain": "Manufacturing/Energy/Finance/Other",
    "company_context": {
        "industry": "...",
        "business_unit": "...",
        "annual_revenue_impact": "$X million",
    },
    "problem": {
        "title": "...",
        "description": "250-word business narrative",
        "current_pain_points": [
            "Point 1 with quantified impact",
            "Point 2 with quantified impact",
        ]
    },
    "objectives": {
        "primary": {
            "metric": "Cost reduction / Throughput / Quality",
            "current_baseline": "X units",
            "target_improvement": "Y%",
            "business_value": "$Z annual"
        },
        "secondary": [
            {"metric": "Quality", "target": "99.5%"},
            {"metric": "Safety", "target": "Zero incidents"},
        ]
    },
    "constraints": {
        "operational": [
            "Max capacity: X units/day",
            "Min quality: Y%",
            "Uptime requirement: Z%",
        ],
        "regulatory": [
            "ISO 9001 compliance",
            "Environmental regulations",
        ],
        "resource": [
            "Budget: $X",
            "Timeline: Y months",
            "Team size: Z engineers",
        ]
    },
    "success_metrics": {
        "primary_kpi": "15% cost reduction",
        "secondary_kpis": ["2% quality gain", "10% faster cycle time"],
        "implementation_timeline": "6 months to ROI",
        "risk_tolerance": "Conservative (validate extensively)",
    }
}
```

### Part B: Data Availability Assessment

```python
class DataAvailabilityAssessment:
    """Assess what data exists and what needs to be collected"""
    
    def __init__(self, domain: str):
        self.domain = domain
        self.data_inventory = {}
        self.data_gaps = {}
    
    def assess_sources(self):
        """Catalog all available data sources"""
        return {
            "production_systems": {
                "erp_system": {
                    "available": True,
                    "frequency": "Daily batch",
                    "retention": "5 years",
                    "features": ["SKU", "quantity", "cost", "quality_score"],
                    "volume_gb": 250,
                },
                "iot_sensors": {
                    "available": True,
                    "frequency": "Real-time (30s intervals)",
                    "retention": "2 years",
                    "features": ["temperature", "humidity", "vibration", "pressure"],
                    "volume_gb": 500,
                },
                "quality_logs": {
                    "available": True,
                    "frequency": "Per-batch",
                    "retention": "3 years",
                    "features": ["defect_type", "count", "root_cause"],
                    "volume_gb": 50,
                },
            },
            "historical_context": {
                "maintenance_records": {
                    "available": True,
                    "frequency": "Event-based",
                    "retention": "10 years",
                    "features": ["equipment_id", "work_type", "duration", "cost"],
                },
                "production_schedule": {
                    "available": True,
                    "frequency": "Monthly planning",
                    "retention": "2 years",
                    "features": ["order_id", "qty", "deadline", "priority"],
                },
            },
            "external": {
                "market_data": {
                    "available": True,
                    "source": "Bloomberg/Reuters",
                    "features": ["commodity_prices", "demand_forecast"],
                },
                "weather": {
                    "available": True,
                    "source": "NOAA API",
                    "features": ["temperature", "humidity", "wind_speed"],
                },
            }
        }
    
    def identify_data_gaps(self):
        """Identify missing data that needs collection"""
        gaps = {
            "feature_engineering": [
                "Operator experience levels (new categorization needed)",
                "Equipment condition scores (not currently tracked)",
                "Customer satisfaction correlation (requires survey)",
            ],
            "temporal_coverage": [
                "Need 3+ years continuous data (currently have 2.5 years)",
                "Need seasonal patterns for full year cycle",
            ],
            "granularity": [
                "Current: hourly aggregation → Need: 5-minute intervals",
                "Current: equipment-level → Need: component-level sensors",
            ],
            "external_factors": [
                "Competitor pricing data (confidential, estimate from market)",
                "Supply chain disruption indicators",
            ]
        }
        return gaps
    
    def data_collection_plan(self):
        """Plan how to collect missing data"""
        plan = {
            "phase_1_weeks_1_4": {
                "activity": "Historical data extraction & cleaning",
                "effort_hours": 40,
                "owner": "Data engineer",
                "deliverable": "Clean 5-year dataset (250 GB)",
            },
            "phase_2_weeks_5_8": {
                "activity": "IoT sensor deployment & calibration",
                "effort_hours": 60,
                "owner": "Controls engineer",
                "deliverable": "Real-time data stream (5-min granularity)",
            },
            "phase_3_weeks_9_12": {
                "activity": "Feature engineering & manual annotation",
                "effort_hours": 80,
                "owner": "Data scientist",
                "deliverable": "Enriched features (500+ dimensions)",
            },
            "validation": {
                "activity": "Data quality assessment",
                "checks": [
                    "Completeness: >99.5% non-null",
                    "Consistency: no conflicting values",
                    "Timeliness: <1 hour latency",
                ],
            }
        }
        return plan

# Implementation
assessor = DataAvailabilityAssessment("Manufacturing")
sources = assessor.assess_sources()
gaps = assessor.identify_data_gaps()
collection_plan = assessor.data_collection_plan()
```

### Part C: Stakeholder Mapping

```python
class StakeholderAnalysis:
    """Map stakeholders and their requirements"""
    
    def __init__(self):
        self.stakeholders = {}
    
    def define_stakeholders(self):
        """Identify all stakeholders and their interests"""
        return {
            "executive_sponsor": {
                "title": "VP Operations",
                "primary_interest": "$X million annual savings",
                "success_metric": "ROI within 12 months",
                "risk_tolerance": "Conservative - wants pilot first",
                "decision_authority": "Budget approval, go/no-go",
                "communication_cadence": "Monthly steering committee",
            },
            "technical_stakeholder": {
                "title": "Head of Data Science",
                "primary_interest": "Technical feasibility & team capability",
                "success_metric": "Model accuracy >95%, latency <100ms",
                "risk_tolerance": "Moderate - willing to iterate",
                "decision_authority": "Architecture decisions",
                "communication_cadence": "Weekly technical reviews",
            },
            "business_stakeholder": {
                "title": "Plant Manager",
                "primary_interest": "Operational stability & throughput",
                "success_metric": "No production disruptions, 15% efficiency gain",
                "risk_tolerance": "High - needs conservative rollout",
                "decision_authority": "Production schedule coordination",
                "communication_cadence": "Daily operational updates",
            },
            "end_users": {
                "title": "Production Operators, Supervisors",
                "primary_interest": "Job security, ease of use, decision clarity",
                "success_metric": "Minimal retraining, <5min decision time",
                "risk_tolerance": "Very high - fear of automation",
                "decision_authority": "Practical feedback, adoption",
                "communication_cadence": "Weekly training & feedback",
            },
            "regulators": {
                "title": "Compliance, HSE (Health, Safety, Environment)",
                "primary_interest": "Regulatory compliance, safety, auditability",
                "success_metric": "Zero incidents, full traceability, audit trail",
                "risk_tolerance": "Zero - must comply with regulations",
                "decision_authority": "Approval for deployment",
                "communication_cadence": "As needed for compliance review",
            }
        }
    
    def create_engagement_plan(self):
        """Plan how to manage stakeholder expectations"""
        plan = {
            "phase_1_problem_definition": {
                "executive": "Steering committee kickoff - align on goals",
                "technical": "Weekly architecture reviews",
                "business": "Understand operational constraints",
                "users": "Discovery interviews - learn current workflows",
                "regulators": "Compliance review - identify constraints",
            },
            "phase_2_pilot": {
                "executive": "Monthly progress reviews",
                "technical": "Bi-weekly technical deep-dives",
                "business": "Real-time operational support",
                "users": "Daily feedback collection",
                "regulators": "Pre-deployment audit",
            },
            "phase_3_deployment": {
                "all": "Daily standup + weekly steering",
            }
        }
        return plan
```

### Part D: Deliverables

Create a document `PROBLEM_DEFINITION.md` including:

1. **Executive Summary** (1 page)
   - Problem statement
   - Expected impact: $X savings, Y% improvement
   - Timeline and resource requirements

2. **Detailed Problem Analysis** (3-5 pages)
   - Business context
   - Pain points with quantified impact
   - Objectives (primary + secondary)
   - Constraints (operational, regulatory, resource)

3. **Data Inventory** (2 pages)
   - Current data sources and quality assessment
   - Data gaps and collection plan
   - Volume, frequency, retention estimates

4. **Stakeholder Map** (1 page)
   - Key stakeholders and their requirements
   - Decision authority and risk tolerance
   - Engagement plan

5. **Success Criteria** (1 page)
   - KPIs and how they'll be measured
   - Go/no-go decision points
   - ROI timeline

### Part E: Validation Checklist

```python
def validate_problem_definition(problem_doc: dict) -> dict:
    """Validate that problem is well-defined and solvable"""
    
    checks = {
        "scope": {
            "is_bounded": bool(problem_doc.get("constraints")),
            "is_quantified": "$X" in str(problem_doc.get("objectives")),
            "timeline_realistic": problem_doc.get("timeline_months", 0) <= 24,
        },
        "data_feasibility": {
            "data_exists": len(problem_doc.get("data_sources", [])) >= 2,
            "volume_sufficient": problem_doc.get("data_volume_gb", 0) >= 10,
            "no_critical_gaps": len(problem_doc.get("data_gaps", [])) <= 3,
        },
        "stakeholder_alignment": {
            "sponsor_identified": "executive_sponsor" in problem_doc,
            "users_consulted": "end_users" in problem_doc,
            "all_risks_mapped": problem_doc.get("risks_count", 0) >= 5,
        },
        "technical_viability": {
            "team_has_skills": bool(problem_doc.get("team_capabilities")),
            "tools_available": len(problem_doc.get("tools", [])) >= 3,
            "no_research_needed": problem_doc.get("uses_established_methods", True),
        },
    }
    
    results = {}
    for category, category_checks in checks.items():
        passed = sum(category_checks.values())
        total = len(category_checks)
        results[category] = {
            "status": "✅ PASS" if passed == total else "⚠️ REVIEW",
            "score": f"{passed}/{total}",
            "details": category_checks
        }
    
    overall_status = "✅ READY" if all(
        r["status"] == "✅ PASS" for r in results.values()
    ) else "⚠️ NEEDS REVISION"
    
    return {
        "overall_status": overall_status,
        "validation_results": results,
        "recommendation": "Proceed to data preparation" if overall_status == "✅ READY" else "Refine problem scope"
    }

# Example usage
validation = validate_problem_definition(problem_doc)
```

### Assessment Rubric

| Criterion | Excellent (5) | Good (4) | Acceptable (3) | Needs Work (2) | Incomplete (1) |
|-----------|---------------|---------|----------------|----------------|----------------|
| Problem clarity | Crystal clear, unambiguous | Clear, minor questions | Understandable, some gaps | Vague, many assumptions | Missing key details |
| Data feasibility | Rich data exists, >100GB | Good data, 10-100GB | Basic data, >1GB | Sparse data, <1GB | No data |
| Stakeholder buy-in | All stakeholders aligned | Most stakeholders engaged | Some stakeholder input | Limited engagement | No engagement |
| Success metrics | 5+ quantified KPIs | 3-4 KPIs | 2 KPIs | 1 vague metric | No metrics |
| Realistic timeline | 6-12 months | 12-18 months | 18-24 months | >24 months | Undefined |

---

## Exercise 1.2: Industrial Data Pipeline & Preparation

**Duration:** 3 hours | **Difficulty:** Advanced

### Learning Objectives
- Build production-grade data pipelines
- Implement robust data cleaning and validation
- Handle missing data and outliers intelligently
- Create reproducible data preprocessing

### Context

Real-world data is messy. This exercise teaches you to build industrial-strength data pipelines that can handle production scale, schema changes, and missing values.

### Part A: Data Pipeline Architecture

```python
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from pathlib import Path
from abc import ABC, abstractmethod
import logging

# Configure logging for production
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataValidationRule(ABC):
    """Base class for validation rules"""
    
    @abstractmethod
    def validate(self, df: pd.DataFrame) -> tuple[bool, str]:
        """
        Validate data against rule.
        Returns: (is_valid, message)
        """
        pass

class SchemaValidation(DataValidationRule):
    """Validate data schema"""
    
    def __init__(self, expected_schema: Dict[str, str]):
        self.expected_schema = expected_schema
    
    def validate(self, df: pd.DataFrame) -> tuple[bool, str]:
        # Check columns exist
        missing_cols = set(self.expected_schema.keys()) - set(df.columns)
        if missing_cols:
            return False, f"Missing columns: {missing_cols}"
        
        # Check data types
        for col, dtype in self.expected_schema.items():
            if str(df[col].dtype) != dtype:
                return False, f"Column {col}: expected {dtype}, got {df[col].dtype}"
        
        return True, "Schema valid"

class CompletenessValidation(DataValidationRule):
    """Ensure sufficient data completeness"""
    
    def __init__(self, min_completeness: float = 0.95):
        self.min_completeness = min_completeness
    
    def validate(self, df: pd.DataFrame) -> tuple[bool, str]:
        completeness = 1.0 - (df.isnull().sum().sum() / (len(df) * len(df.columns)))
        
        if completeness < self.min_completeness:
            return False, f"Completeness {completeness:.1%} below threshold {self.min_completeness:.1%}"
        
        return True, f"Completeness: {completeness:.1%}"

class DuplicateValidation(DataValidationRule):
    """Check for duplicates"""
    
    def __init__(self, subset: Optional[List[str]] = None):
        self.subset = subset
    
    def validate(self, df: pd.DataFrame) -> tuple[bool, str]:
        dup_count = df.duplicated(subset=self.subset).sum()
        
        if dup_count > 0:
            logger.warning(f"Found {dup_count} duplicates")
            return False, f"Found {dup_count} duplicate rows"
        
        return True, "No duplicates"

class RangeValidation(DataValidationRule):
    """Check values within expected ranges"""
    
    def __init__(self, column_ranges: Dict[str, tuple]):
        # column_ranges = {"column_name": (min, max)}
        self.column_ranges = column_ranges
    
    def validate(self, df: pd.DataFrame) -> tuple[bool, str]:
        violations = []
        
        for col, (min_val, max_val) in self.column_ranges.items():
            out_of_range = ((df[col] < min_val) | (df[col] > max_val)).sum()
            if out_of_range > 0:
                violations.append(f"{col}: {out_of_range} values out of [{min_val}, {max_val}]")
        
        if violations:
            return False, "; ".join(violations)
        
        return True, "All values within ranges"

class IndustrialDataPipeline:
    """Production-grade data pipeline with validation and cleaning"""
    
    def __init__(self, data_path: str, config: Dict):
        self.data_path = Path(data_path)
        self.config = config
        self.raw_data = None
        self.cleaned_data = None
        self.validation_rules = []
        self.audit_log = []
    
    def register_validation_rule(self, rule: DataValidationRule) -> None:
        """Register a validation rule"""
        self.validation_rules.append(rule)
    
    def load_data(self) -> pd.DataFrame:
        """Load data from multiple sources"""
        logger.info(f"Loading data from {self.data_path}")
        
        if self.data_path.suffix == '.csv':
            self.raw_data = pd.read_csv(self.data_path)
        elif self.data_path.suffix == '.parquet':
            self.raw_data = pd.read_parquet(self.data_path)
        else:
            raise ValueError(f"Unsupported file format: {self.data_path.suffix}")
        
        logger.info(f"Loaded {len(self.raw_data)} rows, {len(self.raw_data.columns)} columns")
        self._log_action("load_data", f"Loaded {len(self.raw_data)} rows")
        
        return self.raw_data
    
    def validate(self) -> bool:
        """Run all validation rules"""
        logger.info("Running validation rules...")
        
        all_valid = True
        for rule in self.validation_rules:
            is_valid, message = rule.validate(self.raw_data)
            status = "✅" if is_valid else "❌"
            logger.info(f"{status} {rule.__class__.__name__}: {message}")
            self._log_action(f"validate_{rule.__class__.__name__}", message)
            
            if not is_valid:
                all_valid = False
        
        return all_valid
    
    def handle_missing_values(self) -> None:
        """Intelligently handle missing values"""
        logger.info("Handling missing values...")
        
        for col in self.raw_data.columns:
            missing_count = self.raw_data[col].isnull().sum()
            
            if missing_count == 0:
                continue
            
            missing_pct = 100 * missing_count / len(self.raw_data)
            logger.info(f"Column '{col}': {missing_count} missing ({missing_pct:.1f}%)")
            
            # Strategy based on column type and missing percentage
            if missing_pct > 50:
                # Drop column if too many missing values
                logger.warning(f"Dropping column '{col}' (>{missing_pct:.1f}% missing)")
                self.raw_data.drop(col, axis=1, inplace=True)
                self._log_action("drop_column", col)
            
            elif self.raw_data[col].dtype == 'object':
                # For categorical, fill with 'MISSING'
                self.raw_data[col].fillna('MISSING', inplace=True)
                self._log_action("fill_categorical", f"{col} -> MISSING")
            
            else:
                # For numeric, use forward fill then backward fill
                self.raw_data[col].fillna(method='ffill', inplace=True)
                self.raw_data[col].fillna(method='bfill', inplace=True)
                
                # Fill any remaining with median
                if self.raw_data[col].isnull().any():
                    median = self.raw_data[col].median()
                    self.raw_data[col].fillna(median, inplace=True)
                    self._log_action("fill_numeric", f"{col} -> median={median:.2f}")
    
    def remove_outliers(self, columns: List[str], method: str = 'iqr', threshold: float = 1.5) -> None:
        """Remove outliers using IQR or Z-score method"""
        logger.info(f"Removing outliers using {method} method...")
        
        initial_count = len(self.raw_data)
        
        for col in columns:
            if self.raw_data[col].dtype not in ['float64', 'int64']:
                continue
            
            if method == 'iqr':
                Q1 = self.raw_data[col].quantile(0.25)
                Q3 = self.raw_data[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                
                outlier_mask = (self.raw_data[col] < lower_bound) | (self.raw_data[col] > upper_bound)
            
            elif method == 'zscore':
                z_scores = np.abs((self.raw_data[col] - self.raw_data[col].mean()) / self.raw_data[col].std())
                outlier_mask = z_scores > threshold
            
            outlier_count = outlier_mask.sum()
            if outlier_count > 0:
                logger.info(f"Column '{col}': removed {outlier_count} outliers")
                self.raw_data = self.raw_data[~outlier_mask]
                self._log_action(f"remove_outliers_{col}", f"Removed {outlier_count}")
        
        removed_count = initial_count - len(self.raw_data)
        logger.info(f"Total rows removed: {removed_count} ({100*removed_count/initial_count:.1f}%)")
    
    def normalize_features(self) -> None:
        """Normalize numeric features to [0, 1] range"""
        logger.info("Normalizing numeric features...")
        
        numeric_cols = self.raw_data.select_dtypes(include=['float64', 'int64']).columns
        
        for col in numeric_cols:
            min_val = self.raw_data[col].min()
            max_val = self.raw_data[col].max()
            
            if max_val - min_val == 0:
                self.raw_data[col] = 0.5  # Constant column -> middle value
            else:
                self.raw_data[col] = (self.raw_data[col] - min_val) / (max_val - min_val)
            
            self._log_action("normalize", f"{col}: [{min_val:.2f}, {max_val:.2f}] -> [0, 1]")
    
    def create_time_features(self, date_column: str) -> None:
        """Create time-based features from datetime column"""
        logger.info(f"Creating time features from '{date_column}'...")
        
        df_copy = self.raw_data.copy()
        df_copy[date_column] = pd.to_datetime(df_copy[date_column])
        
        self.raw_data['year'] = df_copy[date_column].dt.year
        self.raw_data['month'] = df_copy[date_column].dt.month
        self.raw_data['day'] = df_copy[date_column].dt.day
        self.raw_data['weekday'] = df_copy[date_column].dt.weekday
        self.raw_data['quarter'] = df_copy[date_column].dt.quarter
        self.raw_data['is_weekend'] = (self.raw_data['weekday'] >= 5).astype(int)
        
        self._log_action("create_time_features", f"Created 6 time features from {date_column}")
    
    def split_temporal(self, date_column: str, train_ratio: float = 0.7) -> tuple:
        """Split data into train/test based on time (respects temporal order)"""
        logger.info(f"Splitting data temporally (train: {train_ratio:.0%}, test: {1-train_ratio:.0%})...")
        
        self.raw_data.sort_values(date_column, inplace=True)
        split_idx = int(len(self.raw_data) * train_ratio)
        
        train_data = self.raw_data.iloc[:split_idx].copy()
        test_data = self.raw_data.iloc[split_idx:].copy()
        
        logger.info(f"Train: {len(train_data)} rows | Test: {len(test_data)} rows")
        self._log_action("split_temporal", f"Train: {len(train_data)}, Test: {len(test_data)}")
        
        return train_data, test_data
    
    def get_data_quality_report(self) -> Dict:
        """Generate comprehensive data quality report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_rows": len(self.raw_data),
            "total_columns": len(self.raw_data.columns),
            "missing_values": self.raw_data.isnull().sum().to_dict(),
            "duplicate_rows": self.raw_data.duplicated().sum(),
            "column_types": self.raw_data.dtypes.to_dict(),
            "numeric_statistics": self.raw_data.describe().to_dict(),
            "audit_log": self.audit_log,
        }
        return report
    
    def save_checkpoint(self, filename: str) -> None:
        """Save cleaned data checkpoint"""
        output_path = self.data_path.parent / filename
        self.raw_data.to_parquet(output_path, index=False)
        logger.info(f"Saved checkpoint to {output_path}")
        self._log_action("save_checkpoint", filename)
    
    def _log_action(self, action: str, details: str) -> None:
        """Log pipeline action for audit trail"""
        self.audit_log.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details,
        })

# Example usage
if __name__ == "__main__":
    # Initialize pipeline
    pipeline = IndustrialDataPipeline(
        "production_data.csv",
        config={
            "expected_schema": {
                "timestamp": "datetime64[ns]",
                "equipment_id": "object",
                "temperature": "float64",
                "pressure": "float64",
                "quality_score": "float64",
            }
        }
    )
    
    # Register validation rules
    pipeline.register_validation_rule(
        SchemaValidation({"temperature": "float64", "pressure": "float64"})
    )
    pipeline.register_validation_rule(CompletenessValidation(min_completeness=0.95))
    pipeline.register_validation_rule(DuplicateValidation(subset=["timestamp", "equipment_id"]))
    pipeline.register_validation_rule(
        RangeValidation({"temperature": (0, 150), "pressure": (0, 100)})
    )
    
    # Run pipeline
    pipeline.load_data()
    pipeline.validate()
    pipeline.handle_missing_values()
    pipeline.remove_outliers(["temperature", "pressure"])
    pipeline.normalize_features()
    pipeline.create_time_features("timestamp")
    
    # Generate report
    quality_report = pipeline.get_data_quality_report()
    print("\n=== Data Quality Report ===")
    print(f"Rows: {quality_report['total_rows']}")
    print(f"Columns: {quality_report['total_columns']}")
    print(f"Duplicates: {quality_report['duplicate_rows']}")
    
    # Save checkpoint
    pipeline.save_checkpoint("cleaned_production_data.parquet")
```

### Part B: Advanced Data Transformations

```python
class AdvancedTransformations:
    """Advanced feature engineering and transformations"""
    
    @staticmethod
    def create_lag_features(df: pd.DataFrame, column: str, lags: List[int]) -> pd.DataFrame:
        """Create lagged features for time series"""
        for lag in lags:
            df[f"{column}_lag_{lag}"] = df[column].shift(lag)
        return df
    
    @staticmethod
    def create_rolling_features(df: pd.DataFrame, column: str, windows: List[int]) -> pd.DataFrame:
        """Create rolling window features"""
        for window in windows:
            df[f"{column}_rolling_mean_{window}"] = df[column].rolling(window).mean()
            df[f"{column}_rolling_std_{window}"] = df[column].rolling(window).std()
        return df
    
    @staticmethod
    def create_interaction_features(df: pd.DataFrame, features: List[str]) -> pd.DataFrame:
        """Create interaction terms between features"""
        for i, feat1 in enumerate(features):
            for feat2 in features[i+1:]:
                df[f"{feat1}_x_{feat2}"] = df[feat1] * df[feat2]
        return df
    
    @staticmethod
    def encode_categorical(df: pd.DataFrame, columns: List[str], method: str = 'onehot') -> pd.DataFrame:
        """Encode categorical variables"""
        if method == 'onehot':
            df = pd.get_dummies(df, columns=columns, drop_first=True)
        elif method == 'label':
            from sklearn.preprocessing import LabelEncoder
            le = LabelEncoder()
            for col in columns:
                df[col] = le.fit_transform(df[col])
        return df

# Example feature engineering pipeline
transformations = AdvancedTransformations()
df = transformations.create_lag_features(df, "temperature", [1, 7, 30])
df = transformations.create_rolling_features(df, "temperature", [7, 30])
df = transformations.encode_categorical(df, ["equipment_type", "shift"])
```

### Part C: Deliverables

Create `DATA_PREPARATION_REPORT.md` including:

1. **Data Pipeline Architecture** (2 pages)
   - Source systems and data flows diagram
   - Schema and data types
   - Volume and frequency estimates

2. **Data Validation Results** (2 pages)
   - Validation rules and results
   - Data quality metrics
   - Issues found and resolution

3. **Data Cleaning Decisions** (2 pages)
   - Missing value handling strategy
   - Outlier detection and removal
   - Normalization and scaling approach

4. **Feature Engineering** (2 pages)
   - Engineered features and rationale
   - Lag and rolling window features
   - Interaction terms and transformations

5. **Data Split Strategy** (1 page)
   - Train/test split methodology
   - Temporal order preservation
   - Cross-validation approach

### Assessment Rubric

| Criterion | Excellent (5) | Good (4) | Acceptable (3) | Needs Work (2) | Incomplete (1) |
|-----------|---------------|---------|----------------|----------------|----------------|
| Pipeline robustness | Handles all edge cases | Good error handling | Basic validation | Minimal checks | No validation |
| Data quality | >99% complete, outliers removed | >95% complete | >90% complete | >80% complete | <80% |
| Feature engineering | 30+ engineered features | 20-30 features | 10-20 features | 5-10 features | <5 features |
| Documentation | Comprehensive with diagrams | Detailed | Adequate | Minimal | Incomplete |
| Reproducibility | Fully automated, versioned | Mostly automated | Semi-automated | Manual steps | Not reproducible |

---

## Exercise 1.3: Multi-Surrogate Model Training

**Duration:** 3 hours | **Difficulty:** Advanced

### Learning Objectives
- Train ensemble surrogate models for efficiency
- Implement cross-validation and hyperparameter tuning
- Compare multiple modeling approaches
- Establish model performance baselines

### Context

Running expensive production simulations (EnergyPlus, CFD, etc.) for optimization is prohibitively slow. Surrogate models learn to approximate these expensive functions quickly. This exercise trains multiple models and compares them.

### Part A: Surrogate Model Framework

```python
from typing import Callable, Tuple
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib

class SurrogateModel:
    """Base class for surrogate models"""
    
    def __init__(self, name: str, model, scaler=None):
        self.name = name
        self.model = model
        self.scaler = scaler or StandardScaler()
        self.training_history = {}
    
    def fit(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the surrogate model"""
        logger.info(f"Training {self.name}...")
        
        X_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_scaled, y_train)
        
        self.training_history['train_r2'] = self.model.score(X_scaled, y_train)
        logger.info(f"{self.name} training R²: {self.training_history['train_r2']:.4f}")
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict:
        """Evaluate model performance"""
        y_pred = self.predict(X_test)
        
        metrics = {
            'model': self.name,
            'mse': mean_squared_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'mae': mean_absolute_error(y_test, y_pred),
            'r2': r2_score(y_test, y_pred),
            'mape': np.mean(np.abs((y_test - y_pred) / y_test)) * 100,
        }
        
        return metrics
    
    def save(self, filepath: str) -> None:
        """Save model to disk"""
        joblib.dump({'model': self.model, 'scaler': self.scaler}, filepath)
        logger.info(f"Saved {self.name} to {filepath}")
    
    def load(self, filepath: str) -> None:
        """Load model from disk"""
        data = joblib.load(filepath)
        self.model = data['model']
        self.scaler = data['scaler']
        logger.info(f"Loaded {self.name} from {filepath}")

class SurrogateEnsemble:
    """Ensemble of surrogate models for improved predictions"""
    
    def __init__(self, models: List[SurrogateModel], weights: Optional[List[float]] = None):
        self.models = models
        self.weights = weights or [1.0 / len(models)] * len(models)
        
        if abs(sum(self.weights) - 1.0) > 1e-6:
            raise ValueError("Weights must sum to 1.0")
    
    def fit(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train all models in ensemble"""
        for model in self.models:
            model.fit(X_train, y_train)
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Ensemble prediction (weighted average)"""
        predictions = np.array([model.predict(X) for model in self.models])
        weighted_prediction = np.average(predictions, axis=0, weights=self.weights)
        return weighted_prediction
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict:
        """Evaluate ensemble performance"""
        y_pred = self.predict(X_test)
        
        metrics = {
            'model': 'Ensemble',
            'mse': mean_squared_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'mae': mean_absolute_error(y_test, y_pred),
            'r2': r2_score(y_test, y_pred),
            'mape': np.mean(np.abs((y_test - y_pred) / y_test)) * 100,
        }
        
        return metrics
    
    def feature_importance(self) -> Dict:
        """Aggregate feature importance across ensemble"""
        importances = {}
        
        for model in self.models:
            if hasattr(model.model, 'feature_importances_'):
                for i, imp in enumerate(model.model.feature_importances_):
                    feature_name = f"Feature_{i}"
                    if feature_name not in importances:
                        importances[feature_name] = []
                    importances[feature_name].append(imp)
        
        # Average importance across models
        avg_importance = {
            feat: np.mean(imps) for feat, imps in importances.items()
        }
        
        return dict(sorted(
            avg_importance.items(),
            key=lambda x: x[1],
            reverse=True
        ))

class SurrogateTrainer:
    """Comprehensive surrogate model training pipeline"""
    
    def __init__(self, output_dir: str = "./models"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.models = {}
        self.best_model = None
    
    def train_all_models(self, X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray) -> Dict:
        """Train multiple surrogate models and compare"""
        
        results = []
        
        # 1. Gradient Boosting
        logger.info("\n=== Training Gradient Boosting ===")
        gb_model = SurrogateModel(
            "Gradient Boosting",
            GradientBoostingRegressor(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=7,
                min_samples_split=5,
                min_samples_leaf=2,
                subsample=0.8,
                random_state=42
            )
        )
        gb_model.fit(X_train, y_train)
        gb_metrics = gb_model.evaluate(X_test, y_test)
        results.append(gb_metrics)
        self.models['gradient_boosting'] = gb_model
        logger.info(f"Gradient Boosting R²: {gb_metrics['r2']:.4f}")
        
        # 2. Random Forest
        logger.info("\n=== Training Random Forest ===")
        rf_model = SurrogateModel(
            "Random Forest",
            RandomForestRegressor(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
        )
        rf_model.fit(X_train, y_train)
        rf_metrics = rf_model.evaluate(X_test, y_test)
        results.append(rf_metrics)
        self.models['random_forest'] = rf_model
        logger.info(f"Random Forest R²: {rf_metrics['r2']:.4f}")
        
        # 3. Ensemble (combine GB + RF)
        logger.info("\n=== Creating Ensemble ===")
        ensemble = SurrogateEnsemble(
            [gb_model, rf_model],
            weights=[0.6, 0.4]  # Weight GB higher due to better performance
        )
        ensemble_metrics = ensemble.evaluate(X_test, y_test)
        results.append(ensemble_metrics)
        self.models['ensemble'] = ensemble
        logger.info(f"Ensemble R²: {ensemble_metrics['r2']:.4f}")
        
        # Find best model
        results_df = pd.DataFrame(results)
        best_idx = results_df['r2'].idxmax()
        self.best_model = list(self.models.values())[best_idx]
        
        logger.info(f"\n✅ Best model: {results_df.iloc[best_idx]['model']} (R²={results_df.iloc[best_idx]['r2']:.4f})")
        
        return results_df.to_dict(orient='records')
    
    def save_models(self) -> None:
        """Save all trained models"""
        for name, model in self.models.items():
            if isinstance(model, SurrogateEnsemble):
                # Save each model in ensemble separately
                for i, m in enumerate(model.models):
                    m.save(str(self.output_dir / f"{name}_model_{i}.pkl"))
            else:
                model.save(str(self.output_dir / f"{name}.pkl"))
        
        logger.info(f"Saved models to {self.output_dir}")

# Example usage
if __name__ == "__main__":
    # Load prepared data
    X_train = np.load("X_train.npy")
    y_train = np.load("y_train.npy")
    X_test = np.load("X_test.npy")
    y_test = np.load("y_test.npy")
    
    # Train surrogates
    trainer = SurrogateTrainer(output_dir="./surrogate_models")
    results = trainer.train_all_models(X_train, y_train, X_test, y_test)
    
    # Display comparison
    results_df = pd.DataFrame(results)
    print("\n=== Surrogate Model Comparison ===")
    print(results_df.to_string(index=False))
    
    # Save models
    trainer.save_models()
```

### Part B: Model Validation and Uncertainty Quantification

```python
class UncertaintyQuantification:
    """Estimate prediction uncertainty"""
    
    @staticmethod
    def bootstrap_uncertainty(model: SurrogateModel, X_test: np.ndarray, y_test: np.ndarray, n_bootstrap: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """Estimate uncertainty using bootstrap"""
        predictions = []
        
        for _ in range(n_bootstrap):
            # Randomly resample training data
            indices = np.random.choice(len(X_test), len(X_test), replace=True)
            y_pred = model.predict(X_test[indices])
            predictions.append(y_pred)
        
        predictions = np.array(predictions)
        mean_pred = predictions.mean(axis=0)
        uncertainty = predictions.std(axis=0)
        
        return mean_pred, uncertainty
    
    @staticmethod
    def prediction_intervals(predictions: np.ndarray, uncertainty: np.ndarray, confidence: float = 0.95) -> Tuple[np.ndarray, np.ndarray]:
        """Calculate prediction intervals"""
        z_score = norm.ppf((1 + confidence) / 2)
        lower = predictions - z_score * uncertainty
        upper = predictions + z_score * uncertainty
        return lower, upper

class ModelCalibration:
    """Calibrate model predictions to match reality"""
    
    def __init__(self, model: SurrogateModel):
        self.model = model
        self.calibration_curve = None
    
    def calibrate(self, X_val: np.ndarray, y_val: np.ndarray) -> None:
        """Fit calibration curve"""
        y_pred_raw = self.model.predict(X_val)
        
        # Isotonic regression for calibration
        from sklearn.isotonic import IsotonicRegression
        self.calibration_curve = IsotonicRegression(out_of_bounds='clip')
        self.calibration_curve.fit(y_pred_raw, y_val)
        
        logger.info("Model calibrated")
    
    def predict_calibrated(self, X: np.ndarray) -> np.ndarray:
        """Make calibrated predictions"""
        y_pred_raw = self.model.predict(X)
        return self.calibration_curve.predict(y_pred_raw)
```

### Part C: Deliverables

Create `SURROGATE_MODELS_REPORT.md` including:

1. **Model Architecture** (2 pages)
   - Model types tested and hyperparameters
   - Training procedures and validation strategy
   - Computational requirements and timing

2. **Performance Comparison** (2 pages)
   - Metrics for each model (R², RMSE, MAE, MAPE)
   - Training vs test performance
   - Convergence plots and learning curves

3. **Feature Importance Analysis** (1 page)
   - Top 20 most important features
   - Feature interaction analysis
   - Recommendations for feature selection

4. **Model Validation** (2 pages)
   - Cross-validation results
   - Uncertainty quantification
   - Prediction interval analysis

5. **Production Deployment** (1 page)
   - Model serving architecture
   - Latency and throughput requirements
   - Monitoring and retraining schedule

---

## Exercise 1.4: Baseline Measurement & Gap Analysis

**Duration:** 2 hours | **Difficulty:** Intermediate

### Learning Objectives
- Establish performance baselines
- Identify improvement opportunities (gaps)
- Define KPIs for success measurement
- Create baseline documentation

### Context

Before optimization, you must understand current performance. The gap between baseline and target defines your optimization problem.

### Part A: Baseline Calculation

```python
class BaselineCalculator:
    """Calculate current performance baseline"""
    
    def __init__(self, data: pd.DataFrame, target_column: str):
        self.data = data
        self.target_column = target_column
        self.baseline_metrics = {}
    
    def calculate_current_performance(self) -> Dict:
        """Calculate current business metrics"""
        
        metrics = {
            'cost_current': self.data['cost'].sum() if 'cost' in self.data.columns else None,
            'quality_current': self.data['quality_score'].mean() if 'quality_score' in self.data.columns else None,
            'throughput_current': len(self.data) / (self.data['timestamp'].max() - self.data['timestamp'].min()).days if 'timestamp' in self.data.columns else None,
            'efficiency_current': self.data['efficiency'].mean() if 'efficiency' in self.data.columns else None,
        }
        
        # Remove None values
        self.baseline_metrics = {k: v for k, v in metrics.items() if v is not None}
        
        return self.baseline_metrics
    
    def simulate_simple_heuristic(self) -> Dict:
        """Simulate simple rule-based improvements (upper bound)"""
        
        # Example: Simple threshold-based rules
        improved_data = self.data.copy()
        
        # Rule 1: If temperature > 100, reduce by 10%
        if 'temperature' in improved_data.columns:
            improved_data.loc[improved_data['temperature'] > 100, 'cost'] *= 0.9
        
        # Rule 2: Prioritize high-quality materials
        if 'material_quality' in improved_data.columns:
            improved_data.loc[improved_data['material_quality'] == 'high', 'cost'] *= 0.95
        
        heuristic_metrics = {
            'cost_heuristic': improved_data['cost'].sum(),
            'quality_heuristic': improved_data['quality_score'].mean(),
        }
        
        return heuristic_metrics
    
    def calculate_gap_analysis(self, target_metrics: Dict) -> Dict:
        """Calculate gap between current and target performance"""
        
        gap_analysis = {}
        
        for metric, current_value in self.baseline_metrics.items():
            if metric in target_metrics:
                target_value = target_metrics[metric]
                
                if metric == 'cost_current' or metric == 'cost':
                    # For cost, lower is better
                    absolute_gap = current_value - target_value
                    percent_gap = (absolute_gap / current_value) * 100
                    direction = "reduction"
                else:
                    # For others, higher is better
                    absolute_gap = target_value - current_value
                    percent_gap = (absolute_gap / current_value) * 100
                    direction = "increase"
                
                gap_analysis[metric] = {
                    'current': current_value,
                    'target': target_value,
                    'absolute_gap': absolute_gap,
                    'percent_gap': percent_gap,
                    'direction': direction,
                }
        
        return gap_analysis

# Example usage
baseline_calc = BaselineCalculator(production_data, 'quality_score')
current_perf = baseline_calc.calculate_current_performance()
heuristic_perf = baseline_calc.simulate_simple_heuristic()

target_metrics = {
    'cost_current': current_perf['cost_current'] * 0.85,  # 15% reduction
    'quality_current': current_perf['quality_current'] * 1.02,  # 2% improvement
}

gap_analysis = baseline_calc.calculate_gap_analysis(target_metrics)

print("\n=== Baseline vs Target ===")
for metric, gaps in gap_analysis.items():
    print(f"{metric}:")
    print(f"  Current: {gaps['current']:.2f}")
    print(f"  Target: {gaps['target']:.2f}")
    print(f"  Gap: {gaps['percent_gap']:.1f}% {gaps['direction']}")
```

### Part B: Baseline Documentation

```python
class BaselineReport:
    """Generate comprehensive baseline report"""
    
    def __init__(self):
        self.sections = {}
    
    def add_executive_summary(self, summary: str) -> None:
        """Add executive summary section"""
        self.sections['executive_summary'] = summary
    
    def add_current_state(self, metrics: Dict) -> None:
        """Add current state metrics"""
        self.sections['current_state'] = metrics
    
    def add_benchmark_comparison(self, industry_benchmarks: Dict) -> None:
        """Compare against industry benchmarks"""
        self.sections['benchmarks'] = industry_benchmarks
    
    def add_improvement_opportunities(self, opportunities: List[Dict]) -> None:
        """Document improvement opportunities"""
        self.sections['opportunities'] = opportunities
    
    def generate_markdown(self) -> str:
        """Generate markdown report"""
        
        md = "# Baseline Assessment Report\n\n"
        
        if 'executive_summary' in self.sections:
            md += f"## Executive Summary\n\n{self.sections['executive_summary']}\n\n"
        
        if 'current_state' in self.sections:
            md += "## Current State Metrics\n\n"
            md += "| Metric | Value | Unit |\n"
            md += "|--------|-------|------|\n"
            for metric, value in self.sections['current_state'].items():
                md += f"| {metric} | {value:.2f} | [unit] |\n"
            md += "\n"
        
        if 'benchmarks' in self.sections:
            md += "## Industry Benchmarks\n\n"
            md += "| Metric | Company | Benchmark | Gap |\n"
            md += "|--------|---------|-----------|-----|\n"
            for metric, bench in self.sections['benchmarks'].items():
                md += f"| {metric} | {bench['company_value']:.2f} | {bench['benchmark_value']:.2f} | {bench['gap']:.1f}% |\n"
            md += "\n"
        
        if 'opportunities' in self.sections:
            md += "## Improvement Opportunities\n\n"
            for i, opp in enumerate(self.sections['opportunities'], 1):
                md += f"### {i}. {opp['title']}\n"
                md += f"- **Potential Impact:** {opp['impact']}\n"
                md += f"- **Effort:** {opp['effort']}\n"
                md += f"- **Timeline:** {opp['timeline']}\n\n"
        
        return md
```

### Part C: Deliverables

Create `BASELINE_REPORT.md` including:

1. **Executive Summary** (1 page)
   - Current performance snapshot
   - Key gaps vs target
   - Improvement potential

2. **Current State Metrics** (1 page)
   - All baseline KPIs with values
   - Historical trends
   - Seasonality analysis

3. **Industry Benchmarking** (1 page)
   - Comparison to industry standards
   - Competitive positioning
   - Relative gaps

4. **Gap Analysis** (2 pages)
   - Target vs current for each metric
   - Quantified improvement potential
   - Priority ranking of improvements

5. **Improvement Opportunities** (2 pages)
   - Top 10 improvement opportunities
   - Potential impact and effort estimates
   - Quick wins vs long-term initiatives

### Assessment Rubric

| Criterion | Excellent (5) | Good (4) | Acceptable (3) | Needs Work (2) | Incomplete (1) |
|-----------|---------------|---------|----------------|----------------|----------------|
| Baseline accuracy | Validated against systems | Multiple sources | Single source | Estimated | Unclear |
| Gap quantification | Precise financial impact | Clear metrics | General estimates | Rough estimates | Missing |
| Benchmarking | External industry data | Peer comparison | Historical only | Informal | None |
| Opportunities | 10+ identified, prioritized | 7-10 identified | 5-7 identified | 3-5 identified | <3 |
| Documentation | Comprehensive, visual | Detailed | Adequate | Minimal | Incomplete |

---

## Week 1 Summary

### What You've Accomplished
- ✅ Defined a well-scoped real-world optimization problem
- ✅ Built production-grade data pipelines with validation
- ✅ Trained ensemble surrogate models (R² > 0.95)
- ✅ Established quantified performance baselines
- ✅ Identified improvement opportunities ($X millions in potential)

### Key Deliverables
1. Problem Definition Document (5 pages)
2. Data Preparation Report (8 pages)
3. Surrogate Models Report (8 pages)
4. Baseline Assessment (6 pages)

### Technology Stack Used
- Python 3.10+
- Pandas, NumPy, Scikit-learn
- Production data pipeline architecture
- Gradient Boosting, Random Forest
- Model ensemble techniques

### Certification Checkpoint
**✅ Week 1 Complete** when you have:
- [ ] Problem formulation validated
- [ ] Data pipeline implemented and tested
- [ ] Surrogate models trained with R² > 0.90
- [ ] Baseline metrics established
- [ ] All 4 exercises completed with documentation

---

## Next Week Preview

**Week 2: Algorithm Pipeline & Optimization**
- Implement federated multi-site optimization (Mês 10 integration)
- LLM-guided configuration generation (Mês 5 integration)
- Constrained optimization with real business constraints
- Robustness testing and sensitivity analysis (Mês 11 integration)

**Estimated Effort:** 12-15 hours, 4 exercises

---

## Troubleshooting & Support

### Common Issues

**Problem:** Data pipeline too slow
- **Solution:** Use Parquet format, parallelize preprocessing, implement caching

**Problem:** Surrogate models not accurate enough
- **Solution:** Collect more training data, engineer better features, ensemble models

**Problem:** Baseline doesn't match reality
- **Solution:** Validate against multiple systems, account for seasonal factors

**Problem:** Problem scope too large
- **Solution:** Focus on single facility/product line, narrow optimization objectives

### Resources

- [Data Quality Patterns](https://example.com)
- [Surrogate Modeling Best Practices](https://example.com)
- [Production ML Pipelines](https://example.com)
- [Real-World Optimization Case Studies](https://example.com)

---

## References

1. Kennedy, M. C., & O'Hagan, A. (2001). "Bayesian calibration of computer models"
2. Forrester, A. I., Sobester, A., & Keane, A. J. (2008). "Engineering design via surrogate modelling"
3. Friedman, J. H. (2001). "Greedy function approximation: A gradient boosting machine"
4. Breiman, L. (2001). "Random forests"

---

**Prepared by:** AI Engineering Curriculum Team  
**Date:** January 14, 2026  
**Status:** Ready for Execution  
**Estimated Completion:** January 14, 2026 (1.5 hours)
