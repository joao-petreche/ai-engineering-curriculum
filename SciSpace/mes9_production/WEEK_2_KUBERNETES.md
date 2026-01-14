# Mês 9 — Week 2 Exercises — Kubernetes Orchestration

## Overview
Week 2 focuses on deploying BPS API to Kubernetes with proper manifests, ingress/TLS setup, persistent storage, and multi-environment management.

---

## Exercise 2.1 — Kubernetes Manifests Basics

### Objective
Deploy API and dependencies to a Kubernetes cluster with Deployments, Services, and StatefulSets.

### What's Provided
- [00-namespaces.yaml](../k8s/00-namespaces.yaml): dev, staging, prod namespaces
- [01-api-deployment.yaml](../k8s/01-api-deployment.yaml): API Deployment + Service + ServiceAccount
- [02-configmap-secrets.yaml](../k8s/02-configmap-secrets.yaml): ConfigMap + Secrets
- [03-postgres-statefulset.yaml](../k8s/03-postgres-statefulset.yaml): Postgres StatefulSet
- [04-redis-deployment.yaml](../k8s/04-redis-deployment.yaml): Redis Deployment
- [05-network-policy.yaml](../k8s/05-network-policy.yaml): Network policies

### Prerequisites
- Kubernetes cluster running (k3d/kind/minikube/Docker Desktop)
- `kubectl` configured to access cluster

### Checkpoint Tasks

#### 1.1 Setup Local Kubernetes Cluster
```bash
# Option A: Using k3d (recommended)
k3d cluster create bps-dev --servers 1 --agents 2

# Option B: Using kind
kind create cluster --name bps-dev

# Option C: Using Docker Desktop
# Enable Kubernetes in Docker Desktop settings
```

#### 1.2 Create Namespaces
```bash
kubectl apply -f k8s/00-namespaces.yaml
kubectl get namespaces | grep bps
```
Expected output:
```
bps-dev       Active   2m
bps-staging   Active   2m
bps-prod      Active   2m
```

#### 1.3 Deploy Configuration
```bash
kubectl apply -f k8s/02-configmap-secrets.yaml -n bps-dev
kubectl get configmap,secrets -n bps-dev
```

#### 1.4 Deploy Database (Postgres)
```bash
kubectl apply -f k8s/03-postgres-statefulset.yaml -n bps-dev
kubectl get statefulset,pvc -n bps-dev
kubectl wait --for=condition=ready pod -l app=bps-postgres -n bps-dev --timeout=300s
```

#### 1.5 Deploy Cache (Redis)
```bash
kubectl apply -f k8s/04-redis-deployment.yaml -n bps-dev
kubectl get deployment,svc -l app=bps-redis -n bps-dev
```

#### 1.6 Deploy API
First, build and load the image into your cluster:
```bash
# Build image
docker build -t bps-api:latest .

# Option A: k3d (load directly)
k3d image import bps-api:latest -c bps-dev

# Option B: kind (load directly)
kind load docker-image bps-api:latest --name bps-dev

# Option C: Docker Desktop (automatic)
# Image is available to cluster automatically
```

Then deploy:
```bash
kubectl apply -f k8s/01-api-deployment.yaml -n bps-dev
kubectl wait --for=condition=available --timeout=300s deployment/bps-api -n bps-dev
```

#### 1.7 Verify All Pods Are Running
```bash
kubectl get pods -n bps-dev
```
Expected:
```
NAME                       READY   STATUS    RESTARTS   AGE
bps-api-xxxxx              1/1     Running   0          2m
bps-api-xxxxx              1/1     Running   0          2m
bps-api-xxxxx              1/1     Running   0          2m
bps-postgres-0             1/1     Running   0          5m
bps-redis-xxxxx            1/1     Running   0          3m
```

#### 1.8 Test Health Check via Port-Forward
```bash
kubectl port-forward -n bps-dev svc/bps-api 8000:8000 &
sleep 2
curl http://localhost:8000/health
pkill -f "port-forward"
```
Expected response:
```json
{
  "status": "healthy",
  "service": "BPS Production API",
  "version": "1.0.0"
}
```

#### 1.9 Check Pod Logs
```bash
kubectl logs -n bps-dev deployment/bps-api --tail=20
kubectl logs -n bps-dev statefulset/bps-postgres --tail=10
```

### Key Points
- **Deployment**: Manages 3 replicas of API with rolling updates
- **StatefulSet**: Postgres needs stable identity and storage
- **Service**: Exposes pods internally (ClusterIP) for DNS discovery
- **Probes**: Liveness/readiness probes ensure pod health
- **Resource limits**: Prevent resource starvation

---

## Exercise 2.2 — Ingress & TLS Setup

### Objective
Expose API via HTTP/HTTPS with automatic certificate management.

### What's Provided
- [06-cert-manager.yaml](../k8s/06-cert-manager.yaml): Certificate + Issuer for TLS
- [07-ingress.yaml](../k8s/07-ingress.yaml): Ingress with TLS configuration

### Prerequisites
- nginx-ingress-controller installed
- cert-manager installed

### Checkpoint Tasks

#### 2.1 Install nginx-ingress-controller
```bash
# Using Helm (recommended)
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install nginx-ingress ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace

# Or apply manifests
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/kind/deploy.yaml
```

Verify:
```bash
kubectl get svc -n ingress-nginx
kubectl get pods -n ingress-nginx
```

#### 2.2 Install cert-manager
```bash
# Using Helm
helm repo add jetstack https://charts.jetstack.io
helm repo update
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager --create-namespace \
  --set installCRDs=true

# Or apply manifests
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.2/cert-manager.yaml
```

Verify:
```bash
kubectl get pods -n cert-manager
kubectl api-resources | grep cert-manager
```

#### 2.3 Add Local DNS Entry (for testing)
On your local machine, edit `/etc/hosts` (or `C:\Windows\System32\drivers\etc\hosts` on Windows):
```
127.0.0.1   api.local
```

#### 2.4 Deploy Certificate & Issuer
```bash
kubectl apply -f k8s/06-cert-manager.yaml -n bps-dev
kubectl get certificate,issuer -n bps-dev
kubectl describe certificate bps-tls-cert -n bps-dev  # Check status
```

#### 2.5 Deploy Ingress
```bash
kubectl apply -f k8s/07-ingress.yaml -n bps-dev
kubectl get ingress -n bps-dev
kubectl describe ingress bps-api-ingress -n bps-dev
```

#### 2.6 Configure Port-Forward for Ingress
```bash
# Forward ingress-nginx service to localhost
kubectl port-forward -n ingress-nginx svc/nginx-ingress-ingress-nginx-controller 443:443 &
sleep 2
```

#### 2.7 Test HTTPS Access
```bash
# Test HTTP (should redirect to HTTPS)
curl -L http://api.local/health 2>&1 | head -20

# Test HTTPS (ignore cert warning for self-signed)
curl -k https://api.local/health

# With verbose output to see redirect
curl -v -L http://api.local/health
```

Expected: 200 OK response from health endpoint

### Key Points
- **Ingress**: Routes external traffic to Service based on hostname/path
- **TLS**: Encrypted communication between client and API
- **cert-manager**: Automates certificate provisioning and renewal
- **Self-signed**: Suitable for dev; use Let's Encrypt in production

---

## Exercise 2.3 — Persistence & Backups

### Objective
Ensure data persists across pod restarts and implement automated backups.

### What's Provided
- [03-postgres-statefulset.yaml](../k8s/03-postgres-statefulset.yaml): PVC for Postgres
- [08-postgres-backup-cronjob.yaml](../k8s/08-postgres-backup-cronjob.yaml): Daily backup CronJob

### Checkpoint Tasks

#### 3.1 Verify PersistentVolume and PersistentVolumeClaim
```bash
kubectl get pv,pvc -n bps-dev
kubectl describe pvc postgres-data -n bps-dev
```

#### 3.2 Deploy Backup CronJob
```bash
kubectl apply -f k8s/08-postgres-backup-cronjob.yaml -n bps-dev
kubectl get cronjob,pvc -n bps-dev
```

#### 3.3 Manually Trigger Backup (for testing)
```bash
# Create a one-time Job from the CronJob
kubectl create job postgres-backup-manual --from=cronjob/postgres-backup -n bps-dev

# Monitor the job
kubectl get job,pod -n bps-dev | grep backup
kubectl logs -n bps-dev job/postgres-backup-manual -f
```

#### 3.4 Verify Backup File Created
```bash
# Connect to backup pod and check files
kubectl exec -it postgres-backup-manual -n bps-dev -- ls -lah /backups/
```

Expected: `.sql.gz` file with timestamp

#### 3.5 Test Restore (Optional)
```bash
# Delete some data
kubectl exec -it statefulset/bps-postgres -n bps-dev -- \
  psql -U postgres -d bps_dev -c "DELETE FROM optimization_runs;"

# Restore from backup
kubectl exec -it statefulset/bps-postgres -n bps-dev -- \
  zcat /path/to/backup.sql.gz | psql -U postgres -d bps_dev

# Verify data restored
kubectl exec -it statefulset/bps-postgres -n bps-dev -- \
  psql -U postgres -d bps_dev -c "SELECT COUNT(*) FROM optimization_runs;"
```

### Key Points
- **PersistentVolumeClaim**: Requests storage that survives pod deletion
- **StatefulSet**: Maintains pod identity so PVC can be reattached
- **CronJob**: Schedules backup tasks (daily in this example)
- **Retention**: Script keeps only 7 most recent backups

---

## Exercise 2.4 — Multi-Environment Setup

### Objective
Manage separate configurations for dev, staging, and production environments.

### What's Provided
- [overlays/staging/kustomization.yaml](../k8s/overlays/staging/kustomization.yaml): Staging overlay
- [overlays/prod/kustomization.yaml](../k8s/overlays/prod/kustomization.yaml): Production overlay

### Prerequisites
- Kustomize CLI installed (`kubectl kustomize` is built-in)

### Checkpoint Tasks

#### 4.1 Structure Explanation
```
k8s/
├── 00-namespaces.yaml (shared across environments)
├── 01-api-deployment.yaml (base)
├── 02-configmap-secrets.yaml (base)
├── 03-postgres-statefulset.yaml (base)
├── overlays/
│   ├── staging/
│   │   └── kustomization.yaml (2 replicas, staging config)
│   └── prod/
│       ├── kustomization.yaml (3 replicas, prod config)
│       └── deployment-patch.yaml (higher resources)
```

#### 4.2 Deploy to Staging
```bash
kubectl apply -k k8s/overlays/staging/

# Verify
kubectl get deployments -n bps-staging
kubectl get pods -n bps-staging
```

#### 4.3 Deploy to Production
```bash
kubectl apply -k k8s/overlays/prod/

# Verify
kubectl get deployments -n bps-prod
kubectl get pods -n bps-prod
kubectl get svc -n bps-prod  # Should be LoadBalancer type
```

#### 4.4 Compare Configurations
```bash
# See what would be deployed (dry-run)
kubectl apply -k k8s/overlays/staging/ --dry-run=client -o yaml | head -50
kubectl apply -k k8s/overlays/prod/ --dry-run=client -o yaml | head -50

# Check replicas
kubectl get deployment/bps-api -n bps-staging -o jsonpath='{.spec.replicas}'
kubectl get deployment/bps-api -n bps-prod -o jsonpath='{.spec.replicas}'
```

#### 4.5 Environment-Specific ConfigMap
```bash
# Check ConfigMap values per environment
kubectl get configmap bps-config -n bps-staging -o yaml | grep -A5 data
kubectl get configmap bps-config -n bps-prod -o yaml | grep -A5 data
```

Expected differences:
- **Staging**: 2 replicas, LOG_LEVEL=INFO, API_WORKERS=4
- **Production**: 3 replicas, LOG_LEVEL=WARNING, API_WORKERS=8, REQUIRE_API_KEY=true

### Key Points
- **Kustomize**: Template-free configuration management using overlays
- **Overlays**: Environment-specific patches on top of base manifests
- **Declarative**: Full configuration visible in YAML (vs. Helm templates)
- **Scalability**: Easy to add more environments (canary, compliance, etc.)

---

## Summary of Week 2 Deliverables

| Exercise | Status | Verification |
|----------|--------|--------------|
| 2.1 Manifests | ✅ Done | Cluster setup, 3 namespaces, all pods running |
| 2.2 Ingress+TLS | ✅ Done | `curl https://api.local/health` returns 200 |
| 2.3 Backups | ✅ Done | Backup cronjob runs, `.sql.gz` file created |
| 2.4 Multi-env | ✅ Done | Staging (2 replicas) + Prod (3 replicas) deployed |

## Cleanup

```bash
# Remove Kubernetes cluster
k3d cluster delete bps-dev    # if using k3d
kind delete cluster bps-dev   # if using kind

# Or keep cluster and remove namespaces
kubectl delete namespace bps-dev bps-staging bps-prod
```

## Proceeding to Week 3

Once all Week 2 checkpoints pass, move to Week 3 — CI/CD:
- GitHub Actions workflows for automated testing and deployment
- Blue/Green or Canary deployments
- Security scanning in pipeline
- GitOps with ArgoCD

See [Exercicios_Mes_9_Production_Deployment.md](../Exercicios_Mes_9_Production_Deployment.md) for Week 3 roadmap.
