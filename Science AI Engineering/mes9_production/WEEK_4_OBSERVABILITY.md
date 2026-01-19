# Mês 9 — Week 4 Exercises — Observability, Logging & Operations

## Overview
Week 4 focuses on production monitoring, structured logging, distributed tracing, and operational runbooks for incident response.

---

## Exercise 4.1 — Monitoring with Prometheus & Grafana

### Objective
Deploy Prometheus for metrics collection and Grafana for visualization and alerting.

### What's Provided
- [k8s/monitoring/00-namespace-alertmanager.yaml](k8s/monitoring/00-namespace-alertmanager.yaml): Monitoring namespace + Alertmanager
- [k8s/monitoring/01-prometheus.yaml](k8s/monitoring/01-prometheus.yaml): Prometheus deployment + scrape configs
- [k8s/monitoring/02-grafana.yaml](k8s/monitoring/02-grafana.yaml): Grafana dashboards

### Checkpoint Tasks

#### 1.1 Deploy Monitoring Stack
```bash
# Create monitoring namespace and deploy Prometheus
kubectl apply -f k8s/monitoring/00-namespace-alertmanager.yaml
kubectl apply -f k8s/monitoring/01-prometheus.yaml
kubectl apply -f k8s/monitoring/02-grafana.yaml

# Wait for ready
kubectl wait --for=condition=ready pod -l app=prometheus -n monitoring --timeout=300s
kubectl wait --for=condition=ready pod -l app=grafana -n monitoring --timeout=300s
```

#### 1.2 Access Prometheus UI
```bash
# Port-forward to Prometheus
kubectl port-forward -n monitoring svc/prometheus 9090:9090 &

# Visit: http://localhost:9090
# - Status > Targets: should show API endpoints
# - Alerts: check configured alerts
```

#### 1.3 Test Metrics
In Prometheus UI, search for metrics:
```
http_requests_total
http_request_duration_seconds
errors_total
active_connections
```

#### 1.4 Access Grafana Dashboard
```bash
# Port-forward to Grafana
kubectl port-forward -n monitoring svc/grafana 3000:3000 &

# Visit: http://localhost:3000
# Login: admin / admin
# Add Prometheus datasource: http://prometheus:9090
```

#### 1.5 Create Custom Dashboard
In Grafana:
1. Create Dashboard > Add Panel
2. Data source: Prometheus
3. Metrics:
   - Request Rate: `rate(http_requests_total[5m])`
   - Error Rate: `rate(http_requests_total{status=~"5.."}[5m])`
   - Latency p95: `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))`
4. Save

#### 1.6 Configure Alerting
In Prometheus, verify alert rules loaded:
```bash
kubectl get prometheusrule -n monitoring
kubectl describe prometheusrule bps-api-alerts -n monitoring
```

In Grafana:
1. Alerting > Contact Points > New contact point
2. Type: Webhook / Email / PagerDuty (as available)
3. Set notification policy

#### 1.7 Test Alert Trigger
```bash
# Generate load to trigger alerts
kubectl run -it load-test --image=curlimages/curl -n bps-prod --restart=Never -- \
  bash -c "for i in {1..1000}; do curl http://bps-api:8000/health; done"

# Monitor in Prometheus UI
# Status > Alerts should show "FIRING"
```

### Key Points
- **ServiceMonitor** (optional): Auto-discover scrape targets
- **Recording rules**: Pre-compute expensive queries
- **Alert routing**: Different channels for severity levels (critical, warning, info)

---

## Exercise 4.2 — Structured Logging with Loki

### Objective
Implement centralized log aggregation with searchable structured logs.

### What's Provided
- [k8s/monitoring/03-fluent-bit-loki.yaml](k8s/monitoring/03-fluent-bit-loki.yaml): Fluent Bit log collector
- [k8s/monitoring/04-loki.yaml](k8s/monitoring/04-loki.yaml): Loki log storage

### Checkpoint Tasks

#### 2.1 Deploy Loki Stack
```bash
# Deploy Loki and Fluent Bit
kubectl apply -f k8s/monitoring/04-loki.yaml
kubectl apply -f k8s/monitoring/03-fluent-bit-loki.yaml

# Wait for ready
kubectl wait --for=condition=ready pod -l app=loki -n monitoring --timeout=300s
kubectl wait --for=condition=ready daemonset/fluent-bit -n monitoring --timeout=300s
```

#### 2.2 Configure Grafana Loki Datasource
```bash
# Port-forward Grafana (if not running)
kubectl port-forward -n monitoring svc/grafana 3000:3000 &

# In Grafana UI:
# - Connections > Data sources > Prometheus
# - Add new > Loki
# - URL: http://loki:3100
# - Save & Test
```

#### 2.3 View Logs in Grafana
1. Explore > Loki
2. Label filters:
   - job: bps-api
   - namespace: bps-prod
3. Log level: (none, debug, info, warning, error)

#### 2.4 Search Logs by Request ID
In app/main.py, we set `request_id` in logs. Query in Loki:
```
{job="bps-api"} | json | request_id="<REQUEST_ID>"
```

#### 2.5 Set Log Retention
In [k8s/monitoring/04-loki.yaml](k8s/monitoring/04-loki.yaml), adjust:
```yaml
table_manager:
  retention_deletes_enabled: true
  retention_period: 168h  # 7 days
```

#### 2.6 Create Log Alert
In Grafana > Alerting:
1. New alert rule
2. Data source: Loki
3. Query: `{job="bps-api", level="error"}`
4. Alert when: count > 10 in 5m

### Key Points
- **Structured logs**: JSON format enables filtering and parsing
- **Labels**: Tag logs by job, pod, namespace for easy searching
- **Retention**: Balance storage with audit requirements
- **Integration**: Query logs and metrics together in Grafana

---

## Exercise 4.3 — Distributed Tracing with Jaeger

### Objective
Implement end-to-end tracing to understand request flow through API, DB, and services.

### What's Provided
- [k8s/monitoring/05-jaeger.yaml](k8s/monitoring/05-jaeger.yaml): Jaeger all-in-one deployment
- [app/observability.py](app/observability.py): OpenTelemetry setup

### Checkpoint Tasks

#### 3.1 Deploy Jaeger
```bash
kubectl apply -f k8s/monitoring/05-jaeger.yaml

# Wait for ready
kubectl wait --for=condition=ready pod -l app=jaeger -n monitoring --timeout=300s
```

#### 3.2 Access Jaeger UI
```bash
# Port-forward to Jaeger UI
kubectl port-forward -n monitoring svc/jaeger-ui 16686:16686 &

# Visit: http://localhost:16686
```

#### 3.3 Generate Trace Data
```bash
# Make API request to generate trace
curl http://localhost:8000/health

# In Jaeger UI:
# - Service: bps-api
# - View traces
# - Click trace to see spans (API -> DB -> Redis interactions)
```

#### 3.4 Analyze Trace Spans
In Jaeger, for a trace:
1. Service name: bps-api
2. Span name: /health (HTTP endpoint)
3. Duration: total latency
4. Logs: structured events during span
5. Tags: service, endpoint, status

#### 3.5 Create Service Map
In Jaeger UI:
1. Service Graph tab
2. Shows dependencies between services
3. Visualizes call graph (API -> DB -> Redis)

#### 3.6 Set Trace Sampling
In app/observability.py, adjust sampler:
```python
sampler=AlwaysOnSampler()  # 100% (dev)
sampler=ProbabilitySampler(0.1)  # 10% (prod)
```

### Key Points
- **Spans**: Individual operation (e.g., HTTP request, DB query)
- **Trace**: Collection of spans for one request
- **Sampling**: Balance detail vs. overhead (high in dev, low in prod)
- **Context propagation**: Pass trace ID across services

---

## Exercise 4.4 — SLOs, Runbooks & Incident Response

### Objective
Define service level objectives and procedures for handling incidents.

### Checkpoint Tasks

#### 4.1 Define SLOs
Create `RUNBOOKS.md`:
```markdown
# SLA & SLO Definition

## SLA (Service Level Agreement)
- **Uptime**: 99.5% monthly (≤ 3.6 hours downtime)
- **Support**: 24/7

## SLOs (Service Level Objectives)

### Availability
- **Target**: 99.5%
- **Alert threshold**: < 99% in 1 hour

### Latency
- **p50**: < 100ms
- **p95**: < 500ms
- **p99**: < 2s
- **Alert**: p95 > 500ms for 5 min

### Error Rate
- **Target**: < 0.1%
- **Alert**: > 0.5% for 5 min

## Error Budget
- Monthly budget: 4.32 hours (0.5% downtime)
- Spend rate: can afford ~10 min downtime/week
```

#### 4.2 Create Incident Response Runbooks
Create `RUNBOOKS.md` section for each scenario:

**High Latency Runbook:**
```markdown
## High Latency Incident

### Detection
- Alert: `HighLatency` fires when p95 > 500ms for 5 min

### Triage (5 min)
1. Check Grafana dashboard
   - Request rate
   - DB connection pool usage
   - Redis latency
2. Check logs for errors
   ```
   {job="bps-api", level="error"} | json
   ```

### Response (10 min)
- **If DB slow**: Check slow query logs, add index if needed
- **If Redis slow**: Check memory usage, eviction rate
- **If code issue**: Check recent deployments, consider rollback

### Mitigation (ongoing)
1. If code issue: rollback
   ```bash
   kubectl rollout undo deployment/bps-api -n bps-prod
   ```
2. If resource issue: scale up
   ```bash
   kubectl scale deployment/bps-api --replicas=5 -n bps-prod
   ```

### Resolution
- Apply fix (code change, config, or infrastructure)
- Monitor metrics for improvement
```

**High Error Rate Runbook:**
```markdown
## High Error Rate Incident

### Detection
- Alert: `HighErrorRate` fires when error rate > 5% for 5 min

### Triage (5 min)
1. Check error types
   ```
   {job="bps-api", level="error"} | json | status_code
   ```
2. Check database connectivity
   ```bash
   kubectl exec -it deployment/bps-api -n bps-prod -- \
     psql -h bps-postgres -U postgres -d bps_dev -c "SELECT 1;"
   ```

### Response (10 min)
- If 5xx errors: likely code issue → consider rollback
- If 4xx errors: client issue → check API usage
- If connection errors: infrastructure issue → check pod logs

### Mitigation
1. Rollback if code issue
2. Scale if load issue
3. Bounce pods if stuck
   ```bash
   kubectl delete pod -l app=bps-api -n bps-prod
   ```
```

**Service Down Runbook:**
```markdown
## Service Down Incident

### Detection
- Alert: `LowAvailability` fires when service is unresponsive

### Triage (2 min)
1. Check if pods running
   ```bash
   kubectl get pods -l app=bps-api -n bps-prod
   ```
2. Check pod events
   ```bash
   kubectl describe pod <pod> -n bps-prod
   ```

### Response (5 min)
- Check logs
  ```bash
  kubectl logs deployment/bps-api -n bps-prod --tail=100
  ```
- Restart pod
  ```bash
  kubectl delete pod -l app=bps-api -n bps-prod
  ```

### Resolution
- Investigate root cause in logs
- Apply fix
- Monitor recovery
```

#### 4.3 Test Incident Response
```bash
# Simulate high error rate
kubectl exec deployment/bps-api -n bps-prod -- \
  python -c "import random; random.seed(0); [print(500) for _ in range(100)]"

# Monitor in Grafana
# Follow runbook steps
# Verify alert clears after mitigation
```

#### 4.4 Create On-Call Rotation
Document in `RUNBOOKS.md`:
```markdown
## On-Call Rotation

- **Primary**: Mon-Fri 9-17 UTC (production issues)
- **Secondary**: 24/7 (critical/P1 only)
- **Escalation**: After 15 min, page manager

## Contact Info
- Slack: #bps-incidents
- PagerDuty: [link]
- War room: [Zoom link]
```

#### 4.5 Postmortem Template
Create `POSTMORTEM_TEMPLATE.md`:
```markdown
# Incident Postmortem

## Overview
- **Incident**: [Brief title]
- **Date**: [YYYY-MM-DD HH:MM UTC]
- **Duration**: [minutes]
- **Impact**: [affected users/services]
- **Severity**: [P1/P2/P3]

## Timeline
- **HH:MM** - Alert fired
- **HH:MM** - On-call notified
- **HH:MM** - Root cause identified
- **HH:MM** - Mitigation applied
- **HH:MM** - Service recovered

## Root Cause
[Detailed explanation]

## Resolution
[What was done to fix]

## Action Items
- [ ] Fix X by [date]
- [ ] Add alert for Y by [date]
- [ ] Document Z by [date]

## Lessons Learned
- What went well
- What could be better
- How to prevent recurrence
```

---

## Summary of Week 4 Deliverables

| Exercise | Status | Verification |
|----------|--------|--------------|
| 4.1 Monitoring | ✅ Done | Prometheus scrapes metrics, Grafana dashboards display |
| 4.2 Logging | ✅ Done | Loki aggregates logs, searchable by request_id |
| 4.3 Tracing | ✅ Done | Jaeger shows end-to-end traces with spans |
| 4.4 Runbooks | ✅ Done | SLOs defined, incident runbooks created & tested |

## Cleanup

```bash
# Remove monitoring stack
kubectl delete namespace monitoring
```

## Certification Checklist — Mês 9 Complete

- [x] Week 1: Docker containerization (multi-stage, security, scanning)
- [x] Week 2: Kubernetes orchestration (manifests, ingress, backups, multi-env)
- [x] Week 3: CI/CD pipeline (GitHub Actions, GitOps, deployments)
- [x] Week 4: Observability & operations (metrics, logs, traces, runbooks)

## Next Steps

**Mês 10 — Federated Learning & Adaptive Prompting**
- Implement federated multi-agent optimization
- Dynamic LLM prompt adaptation
- Real-time monitoring and feedback loops
- Advanced co-simulation with edge devices

See [Exercicios_Mes_10_Federated_Learning.md](../Exercicios_Mes_10_Federated_Learning.md) for roadmap.
