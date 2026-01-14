# Mês 9 — Week 2 Complete Checklist

## ✅ Kubernetes Manifests Created

### Core Infrastructure
- [00-namespaces.yaml](k8s/00-namespaces.yaml) - dev, staging, prod
- [01-api-deployment.yaml](k8s/01-api-deployment.yaml) - 3-replica API with probes
- [02-configmap-secrets.yaml](k8s/02-configmap-secrets.yaml) - Configuration & secrets
- [03-postgres-statefulset.yaml](k8s/03-postgres-statefulset.yaml) - Persistent DB
- [04-redis-deployment.yaml](k8s/04-redis-deployment.yaml) - Cache service
- [05-network-policy.yaml](k8s/05-network-policy.yaml) - Network segmentation

### Ingress & Security
- [06-cert-manager.yaml](k8s/06-cert-manager.yaml) - TLS certificates
- [07-ingress.yaml](k8s/07-ingress.yaml) - HTTP/HTTPS routing

### Operations
- [08-postgres-backup-cronjob.yaml](k8s/08-postgres-backup-cronjob.yaml) - Daily backups
- [overlays/staging/](k8s/overlays/staging/) - Staging environment (2 replicas)
- [overlays/prod/](k8s/overlays/prod/) - Production environment (3 replicas, LoadBalancer)

## 📚 Documentation & Scripts

- [WEEK_2_KUBERNETES.md](WEEK_2_KUBERNETES.md) - 4 detailed exercises with checkpoints
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions
- [test-k8s.sh](test-k8s.sh) - Bash test script for cluster validation
- [test-k8s.bat](test-k8s.bat) - Windows batch test script
- [setup-k8s.sh](setup-k8s.sh) - Automated cluster setup

## 🔄 CI/CD

- [.github/workflows/ci.yml](.github/workflows/ci.yml) - Testing & scanning
- [.github/workflows/cd.yml](.github/workflows/cd.yml) - Staging + Production deployment

## 🎯 Exercise Breakdown

| Exercise | Description | Time | Status |
|----------|-------------|------|--------|
| **2.1** | Namespace, Deployment, Service, StatefulSet | 4-5h | ✅ Scaffolded |
| **2.2** | Ingress + cert-manager + TLS setup | 3-4h | ✅ Scaffolded |
| **2.3** | PVC persistence + automated backups | 2-3h | ✅ Scaffolded |
| **2.4** | Kustomize overlays for multi-environment | 2-3h | ✅ Scaffolded |

## 🚀 Quick Start

```bash
# 1. Setup local k8s cluster
./setup-k8s.sh k3d

# 2. Verify deployment
./test-k8s.sh dev

# 3. Check all resources
kubectl get all -n bps-dev

# 4. Access API
kubectl port-forward -n bps-dev svc/bps-api 8000:8000 &
curl http://localhost:8000/health
```

## 📋 Week 2 Exercises Ready for Execution

All scaffolding complete. You can now:

1. **Exercise 2.1 — Deploy to Kubernetes**
   - Follow steps in [WEEK_2_KUBERNETES.md](WEEK_2_KUBERNETES.md#exercise-21--kubernetes-manifests-basics)
   - Expected: All pods running, health check responding

2. **Exercise 2.2 — Setup Ingress + TLS**
   - Install nginx-ingress and cert-manager
   - Deploy Ingress and Certificate
   - Test HTTPS access to `api.local`

3. **Exercise 2.3 — Configure Backups**
   - Deploy CronJob
   - Manually trigger backup
   - Verify `.sql.gz` file created

4. **Exercise 2.4 — Multi-Environment**
   - Deploy staging overlay: `kubectl apply -k k8s/overlays/staging/`
   - Deploy production overlay: `kubectl apply -k k8s/overlays/prod/`
   - Verify different configs per environment

## 🔗 Next: Week 3 — CI/CD Pipeline

Once Week 2 is complete:
- GitHub Actions workflows ready in `.github/workflows/`
- CI tests, builds, and scans on every push
- CD deploys to staging automatically
- Production requires manual approval gate

See [Exercicios_Mes_9_Production_Deployment.md](../Exercicios_Mes_9_Production_Deployment.md) for Week 3 roadmap.
