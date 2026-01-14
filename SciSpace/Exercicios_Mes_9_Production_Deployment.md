# Exercícios Mês 9: Production Deployment & DevOps

## 📋 Visão Geral
- Objetivo: colocar o sistema (API + GA/Co-sim + LLM guardrails) em produção com segurança, observabilidade e CI/CD.
- Carga estimada: 50-60h.
- Pré-requisitos: Meses 4-8 concluídos; Docker, GitHub Actions, Kubernetes básicos.
- Stack: Docker/Compose, GitHub Actions, Kubernetes (k3d/kind/minikube), Prometheus/Grafana, ELK/OTel (conceitos), Postgres/Redis.

## 📦 Setup Rápido
```bash
pip install pre-commit
pre-commit install
```

---
## 🔹 Semana 1 — Docker & Containerização (12-15h)

### Exercício 1.1 — Dockerfile multi-stage (3-4h)
Crie imagem leve para API (FastAPI/Flask). Exemplo:
```Dockerfile
FROM python:3.10-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

FROM gcr.io/distroless/python3
WORKDIR /app
COPY --from=base /app /app
ENV PORT=8000
CMD ["app.main:app"]
```
**Checkpoint:** imagem < 500MB, `docker run -p 8000:8000` responde healthcheck.

### Exercício 1.2 — Docker Compose dev (3-4h)
Serviços: api, postgres, redis. Compose mínimo:
```yaml
version: "3.9"
services:
  api:
    build: .
    ports: ["8000:8000"]
    env_file: .env.dev
    depends_on: [db, cache]
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: devpass
    ports: ["5432:5432"]
  cache:
    image: redis:7
    ports: ["6379:6379"]
```
**Checkpoint:** `docker compose up` sobe 3 serviços; API conecta em DB/Redis.

### Exercício 1.3 — Security hardening (2-3h)
- Rodar como usuário não-root (`USER 1000`), filesystem read-only onde possível.
- Adicionar `HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1`.
**Checkpoint:** container passa healthcheck; sem root.

### Exercício 1.4 — Image scanning (2-3h)
- Use Trivy local: `trivy image your-api:latest`.
**Checkpoint:** sem vulnerabilidades críticas.

---
## 🔹 Semana 2 — Kubernetes Orquestração (12-15h)

### Exercício 2.1 — Manifests básicos (4-5h)
Crie Deployment + Service para API e StatefulSet para Postgres.
```yaml
apiVersion: apps/v1
kind: Deployment
metadata: {name: bps-api}
spec:
  replicas: 3
  selector: {matchLabels: {app: bps-api}}
  template:
    metadata: {labels: {app: bps-api}}
    spec:
      containers:
      - name: api
        image: your-registry/bps-api:latest
        ports: [{containerPort: 8000}]
        readinessProbe: {httpGet: {path: /health, port: 8000}, initialDelaySeconds: 5, periodSeconds: 10}
        livenessProbe: {httpGet: {path: /health, port: 8000}, initialDelaySeconds: 15, periodSeconds: 20}
        resources: {requests: {cpu: "250m", memory: "256Mi"}, limits: {cpu: "1", memory: "512Mi"}}
```
**Checkpoint:** `kubectl get pods` 3/3 Running.

### Exercício 2.2 — Ingress + TLS (3-4h)
- Instale ingress (nginx) e cert-manager.
- Configure Ingress com host `api.local` e TLS (self-signed em dev).
**Checkpoint:** `curl https://api.local/health` retorna 200.

### Exercício 2.3 — Persistência & backups (2-3h)
- PVC para Postgres (10Gi), backup cronjob `pg_dump` para bucket local/minio.
**Checkpoint:** backup file gerado e restaurável.

### Exercício 2.4 — Multi-ambiente (2-3h)
- Namespaces: dev/staging/prod; imagens versionadas por tag (`vX.Y.Z`).
**Checkpoint:** deploy independente por namespace.

---
## 🔹 Semana 3 — CI/CD (12-15h)

### Exercício 3.1 — GitHub Actions CI (3-4h)
Workflow exemplo `.github/workflows/ci.yml`:
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with: {python-version: '3.10'}
    - run: pip install -r requirements.txt
    - run: pytest
  build-image:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: docker/build-push-action@v5
      with:
        push: false
        tags: bps-api:ci
```
**Checkpoint:** CI roda testes em PR.

### Exercício 3.2 — CD com approval (3-4h)
- Job deploy-staging após sucesso do CI; require manual approval para prod.
- Blue/Green ou Canary (10%->50%->100%).
**Checkpoint:** rollout em staging automático; prod com gate manual.

### Exercício 3.3 — GitOps (2-3h)
- Manifests no repositório `infra/`; ArgoCD sincroniza para cluster.
**Checkpoint:** sync automático em dev; manual em prod.

### Exercício 3.4 — Pipeline de segurança (2-3h)
- SAST (bandit), dependency scan, container scan, secret scan (trufflehog).
**Checkpoint:** pipelines bloqueiam PR com falhas críticas.

---
## 🔹 Semana 4 — Observabilidade, Logging & Operações (14-15h)

### Exercício 4.1 — Monitoring (4-5h)
- Instrumentar API com `prometheus_client` (latência, throughput, erro).
- Prometheus scrape + Grafana dashboard.
- Alertas: erro >5%, latência p95 >2s.
**Checkpoint:** alert dispara em carga simulada.

### Exercício 4.2 — Logging estruturado (3-4h)
- JSON logs (request_id, user, latency). Enviar para ELK/Vector/Loki (conceito ok).
**Checkpoint:** consulta por `request_id` retorna evento.

### Exercício 4.3 — Tracing (2-3h)
- OpenTelemetry SDK no API; export Jaeger/Tempo.
**Checkpoint:** trace end-to-end visível com spans (API -> DB -> surrogate call).

### Exercício 4.4 — Runbooks & SLA (2-3h)
- Runbooks: latência alta, erro 500, nó degradado, falta de disco.
- SLA: 99.5% uptime; SLOs para latência/erro.
**Checkpoint:** runbook seguido em simulação de incidente.

---
## 📋 Checklist de Certificação — Mês 9
- [ ] Imagem Docker < 500MB e healthcheck ok
- [ ] Compose sobe API + DB + Redis
- [ ] k8s deployment com readiness/liveness e TLS no ingress
- [ ] Backups funcionando
- [ ] CI executa testes; CD deploya staging e gate para prod
- [ ] GitOps (ArgoCD) sincronizando manifests
- [ ] Scans de segurança ativos (SAST/Deps/Container/Secrets)
- [ ] Observabilidade: Prometheus+Grafana, alerts >5% erro ou p95>2s
- [ ] Logging estruturado pesquisável
- [ ] Tracing end-to-end disponível
- [ ] Runbooks criados e testados em simulação

---
## Recursos
- Docker docs; Docker Buildx; Trivy (scans)
- Kubernetes: Deployments, Services, Ingress, Probes, Resource limits
- cert-manager + nginx-ingress
- GitHub Actions + docker/build-push-action
- ArgoCD (GitOps)
- Prometheus/Grafana, OpenTelemetry SDK
- Loki/ELK/Vector para logs

---
## Próximos Passos
- Mês 10: Federated learning, adaptive prompting, real-time monitoring.
- Antes de M10: feche runbooks e valide métricas de produção em staging.
