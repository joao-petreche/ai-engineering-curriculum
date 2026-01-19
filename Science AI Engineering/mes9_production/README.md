# BPS Production API - Mês 9

Production-ready API scaffolding with Docker, Kubernetes, CI/CD, and observability.

## Quick Start

### Docker Compose (Development)
```bash
docker compose up -d
curl http://localhost:8000/health
```

### Kubernetes (Development Cluster)
```bash
# Create namespaces and deploy
kubectl apply -f k8s/00-namespaces.yaml
kubectl apply -f k8s/01-api-deployment.yaml -n bps-dev
kubectl apply -f k8s/02-configmap-secrets.yaml -n bps-dev
kubectl apply -f k8s/03-postgres-statefulset.yaml -n bps-dev
kubectl apply -f k8s/04-redis-deployment.yaml -n bps-dev

# Port-forward to API
kubectl port-forward -n bps-dev svc/bps-api 8000:8000
```

### Testing
```bash
pytest tests/ -v --cov=app
```

## Structure

```
mes9_production/
├── app/                      # FastAPI application
│   ├── main.py              # App entry point
│   ├── config.py            # Settings
│   ├── observability.py     # Metrics & tracing
│   ├── api/
│   │   └── health.py        # Health endpoints
├── k8s/                      # Kubernetes manifests
│   ├── 00-namespaces.yaml
│   ├── 01-api-deployment.yaml
│   ├── 02-configmap-secrets.yaml
│   ├── 03-postgres-statefulset.yaml
│   ├── 04-redis-deployment.yaml
│   └── 05-network-policy.yaml
├── .github/workflows/        # CI/CD workflows
│   └── ci.yml
├── tests/                    # Test suite
├── scripts/                  # Initialization scripts
│   └── init_db.sql
├── Dockerfile               # Multi-stage build
├── docker-compose.yml       # Dev environment
└── requirements.txt         # Python dependencies
```

## Exercises Status

### Week 1 — Docker & Containerization
- [x] **1.1 — Dockerfile multi-stage**: Multi-stage build with distroless runtime
- [x] **1.2 — Docker Compose dev**: dev environment with API, Postgres, Redis
- [ ] **1.3 — Security hardening**: Run tests with non-root user, readonly filesystem
- [ ] **1.4 — Image scanning**: Run Trivy to check vulnerabilities

### Week 2 — Kubernetes Orchestration
- [ ] **2.1 — Manifests basics**: Deployment, Service, StatefulSet created (ready for deployment)
- [ ] **2.2 — Ingress + TLS**: Setup nginx ingress and cert-manager
- [ ] **2.3 — Persistência & backups**: PVC and backup cronjob
- [ ] **2.4 — Multi-ambiente**: Test dev/staging/prod namespaces

### Week 3 — CI/CD
- [ ] **3.1 — GitHub Actions CI**: CI workflow runs tests
- [ ] **3.2 — CD com approval**: CD pipeline with staging auto-deploy and prod approval gate
- [ ] **3.3 — GitOps**: ArgoCD setup for manifest sync
- [ ] **3.4 — Pipeline de segurança**: SAST, deps scan, container scan integrated

### Week 4 — Observability, Logging & Operações
- [ ] **4.1 — Monitoring**: Prometheus metrics + Grafana dashboard
- [ ] **4.2 — Logging estruturado**: JSON logs indexed
- [ ] **4.3 — Tracing**: OpenTelemetry + Jaeger
- [ ] **4.4 — Runbooks & SLA**: Incident runbooks and SLO tracking

## Next Steps

1. **Test locally**: Run `docker compose up` and test health endpoint
2. **Build image**: `docker build -t bps-api:latest .`
3. **Scan image**: `docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image bps-api:latest`
4. **Deploy to k8s**: Use k8s manifests with local cluster (k3d/kind)
5. **Run CI**: Push to GitHub and verify workflow

## Security Notes

- App runs as non-root user (uid 1000)
- Container has readonly filesystem except `/tmp`
- Network policies restrict traffic
- Secrets stored in k8s Secrets (not in code)
- Pre-commit hooks enforce code quality
