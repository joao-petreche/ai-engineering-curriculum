# Mês 9 — Week 3 Exercises — CI/CD Pipeline

## Overview
Week 3 focuses on automating testing, building, scanning, and deploying the BPS API with GitHub Actions, security scanning, and GitOps principles.

---

## Exercise 3.1 — GitHub Actions CI Pipeline

### Objective
Implement comprehensive continuous integration with linting, testing, security scanning, and image building.

### What's Provided
- [.github/workflows/ci-enhanced.yml](.github/workflows/ci-enhanced.yml): Full CI pipeline
  - Code quality (Black, isort, Flake8, mypy)
  - Security scanning (Bandit, Safety)
  - Unit & integration tests
  - Docker image build and scan

### Checkpoint Tasks

#### 1.1 Setup GitHub Repository
```bash
# Initialize git repo (if not already done)
git init
git remote add origin https://github.com/your-org/bps-api.git
git branch -M main
```

#### 1.2 Push Code to Repository
```bash
git add .
git commit -m "feat: Mês 9 production scaffolding with Docker, k8s, and CI/CD"
git push -u origin main
```

#### 1.3 Enable GitHub Actions
1. Go to repository settings
2. Navigate to Actions > General
3. Ensure "Allow all actions and reusable workflows" is selected
4. Save

#### 1.4 Create Branch Protection Rule
1. Settings > Branches
2. Add rule for `main`
3. Enable:
   - Require status checks to pass before merging
   - Require code reviews
   - Dismiss stale pull request approvals

#### 1.5 Monitor First CI Run
```bash
# Push a change to trigger CI
git checkout -b test-ci
echo "# Test CI" >> README.md
git add README.md
git commit -m "test: trigger CI workflow"
git push origin test-ci
```

Then open a Pull Request and watch the workflow run:
- Go to Actions tab
- Select "Enhanced CI Pipeline"
- Monitor each job:
  - Lint & Format
  - Security Scan
  - Test
  - Build Image
  - Scan Image

#### 1.6 View Test Results
```bash
# In GitHub UI:
# PR checks → Details on each workflow job
# Actions → Artifacts (coverage reports, security scans)
```

#### 1.7 Fix Code Quality Issues (if any)
```bash
# Run locally to fix issues before pushing
pip install black isort flake8 mypy bandit

# Auto-format
black app/ tests/
isort app/ tests/

# Check for issues
flake8 app/ tests/
mypy app/ --ignore-missing-imports
bandit -r app/
```

### Key Points
- **Concurrency**: Only one workflow per ref; cancels previous runs
- **Caching**: Speeds up pip install using GitHub Actions cache
- **Matrix testing**: Could test multiple Python versions (add `strategy.matrix.python-version`)
- **Artifacts**: Security reports stored for audit

---

## Exercise 3.2 — Continuous Deployment to Staging

### Objective
Automatically deploy to staging environment on every successful main branch push.

### What's Provided
- [.github/workflows/cd-staging.yml](.github/workflows/cd-staging.yml): Staging deployment
  - Automatic deployment on main push
  - Health checks post-deployment

### Prerequisites
- Staging Kubernetes cluster running
- GitHub secrets configured:
  - `KUBE_CONFIG_STAGING` (base64-encoded kubeconfig)

### Checkpoint Tasks

#### 2.1 Prepare Kubeconfig for CI
```bash
# On your machine with kubectl access to staging cluster
cat $HOME/.kube/config | base64 -w0
# Copy the output

# In GitHub UI:
# Settings > Secrets and variables > Actions
# New repository secret: KUBE_CONFIG_STAGING
# Paste the base64-encoded kubeconfig
```

#### 2.2 Trigger Staging Deployment
```bash
# Make a change and push to main
git checkout main
echo "# Version 1.1" >> VERSION.md
git add VERSION.md
git commit -m "chore: bump version"
git push origin main
```

#### 2.3 Monitor Deployment
Go to GitHub Actions:
1. Select "CD - Deploy to Staging" workflow
2. Watch jobs:
   - Build and Push (creates image)
   - Deploy Staging (updates k8s)
   - Health Check (verifies deployment)

#### 2.4 Verify in Staging Cluster
```bash
# Check rollout status
kubectl rollout status deployment/bps-api -n bps-staging

# Check pod logs
kubectl logs -f deployment/bps-api -n bps-staging

# Access API
kubectl port-forward -n bps-staging svc/bps-api 8000:8000 &
curl http://localhost:8000/health
```

#### 2.5 Check Deployment History
```bash
kubectl describe deployment/bps-api -n bps-staging | grep "Image:"
```

### Key Points
- **Automatic**: No manual intervention needed for staging
- **Fast feedback**: Issues caught before production
- **Rollback-friendly**: Easy to revert if issues arise

---

## Exercise 3.3 — Controlled Production Deployment

### Objective
Implement manual approval gate for production with multiple deployment strategies.

### What's Provided
- [.github/workflows/cd-production.yml](.github/workflows/cd-production.yml): Production deployment
  - Manual trigger (workflow_dispatch)
  - Blue-Green deployment strategy
  - Canary deployment option
  - Post-deployment verification

### Prerequisites
- Production Kubernetes cluster
- GitHub secrets:
  - `KUBE_CONFIG_PROD` (base64-encoded kubeconfig)
  - `SLACK_WEBHOOK` (optional, for notifications)

### Checkpoint Tasks

#### 3.1 Configure Production Kubeconfig
```bash
# Same as staging, but for production cluster
cat $HOME/.kube/config-prod | base64 -w0

# Add to GitHub Secrets as KUBE_CONFIG_PROD
```

#### 3.2 Create Production Environment
In GitHub UI:
1. Settings > Environments
2. New environment: "production"
3. Deployment branches: "main"
4. Add deployment protection rules:
   - Required reviewers (assign team members)
   - Wait timer (optional, e.g., 1 hour)

#### 3.3 Trigger Production Deployment (Manual)
Go to Actions > CD - Deploy to Production:
1. Click "Run workflow"
2. Select environment: "production"
3. Confirm approval in review modal
4. Monitor deployment

#### 3.4 Monitor Blue-Green Deployment
```bash
# During deployment, both versions run
kubectl get pods -n bps-prod

# If issues, rollback:
kubectl rollout undo deployment/bps-api -n bps-prod
```

#### 3.5 Monitor Canary Deployment (Alternative)
```bash
# If using canary:
kubectl get canary -n bps-prod
kubectl describe canary bps-api -n bps-prod

# Monitor metrics
kubectl logs -f canary/bps-api-primary -n bps-prod
```

### Key Points
- **Blue-Green**: Zero downtime; easy rollback
- **Canary**: Gradual rollout (10% → 50% → 100%)
- **Approval gate**: Prevents accidental production deployments
- **Verification**: Post-deploy health checks ensure functionality

---

## Exercise 3.4 — GitOps with ArgoCD

### Objective
Implement GitOps principle: Git as single source of truth for cluster state.

### What's Provided
- [k8s/argocd/00-argocd-install.yaml](k8s/argocd/00-argocd-install.yaml): ArgoCD installation
- [k8s/argocd/01-applications.yaml](k8s/argocd/01-applications.yaml): BPS applications
- [k8s/argocd/02-project.yaml](k8s/argocd/02-project.yaml): Project RBAC

### Checkpoint Tasks

#### 4.1 Install ArgoCD
```bash
# Create argocd namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -f k8s/argocd/00-argocd-install.yaml -n argocd

# Wait for ready
kubectl wait --for=condition=Ready pod -l app.kubernetes.io/name=argocd-server \
  -n argocd --timeout=300s
```

#### 4.2 Access ArgoCD UI
```bash
# Port-forward to ArgoCD server
kubectl port-forward -n argocd svc/argocd-server 8080:443 &

# Get admin password
kubectl get secret argocd-initial-admin-secret -n argocd \
  -o jsonpath="{.data.password}" | base64 -d

# Visit: https://localhost:8080 (accept self-signed cert)
# Login: admin / <password>
```

#### 4.3 Configure Git Repository
In ArgoCD UI:
1. Settings > Repositories
2. Connect repo:
   - Type: git
   - Repository URL: https://github.com/your-org/bps-api
   - Authentication: HTTPS (leave credentials if public)

#### 4.4 Create Applications
```bash
# Deploy ArgoCD applications
kubectl apply -f k8s/argocd/01-applications.yaml -n argocd
kubectl apply -f k8s/argocd/02-project.yaml -n argocd
```

#### 4.5 Verify Applications in UI
In ArgoCD dashboard:
1. Applications tab
2. Should see:
   - bps-api-dev (synced)
   - bps-api-staging (synced)
   - bps-api-prod (synced)

#### 4.6 Test GitOps Sync
```bash
# Make a change in repo
git checkout -b gitops-test
# Modify k8s/overlays/dev/kustomization.yaml (change LOG_LEVEL)
git add k8s/overlays/dev/kustomization.yaml
git commit -m "test: update dev logging level via GitOps"
git push origin gitops-test

# In ArgoCD UI:
# Applications > bps-api-dev
# Should detect change within 3 minutes (or click "Refresh")
# Click "Sync" to apply changes
```

#### 4.7 Enable Auto-Sync (Optional)
In ArgoCD UI:
1. Application > bps-api-dev > App Details
2. Sync Policy: Automated
3. Prune: Yes
4. Self-heal: Yes

Now changes to Git are applied automatically to cluster.

### Key Points
- **Single source of truth**: Git repository defines cluster state
- **Audit trail**: Every change tracked in version control
- **Declarative**: Infrastructure as Code (IaC) principles
- **Multi-tenancy**: Project-based access control (bps-production project)

---

## Exercise 3.5 — Pipeline Security & Governance

### Objective
Integrate security scanning and enforce policies in CI/CD pipeline.

### Checkpoint Tasks

#### 5.1 Review Security Scans
In GitHub UI:
1. Settings > Code security and analysis
2. Enable:
   - Secret scanning (alerts on leaked credentials)
   - Dependabot alerts (outdated packages)
   - Code scanning (CodeQL - optional)

#### 5.2 Configure Branch Protection
```bash
# Require security checks before merge
# Settings > Branches > Branch protection rules > main
# Required status checks: ci-enhanced, cd-staging, code-scanning
```

#### 5.3 Audit Deployment History
```bash
# View all deployments
git log --oneline | head -20

# View rollouts in k8s
kubectl rollout history deployment/bps-api -n bps-staging
kubectl rollout history deployment/bps-api -n bps-prod
```

#### 5.4 Test Rollback
```bash
# Simulate issue in production
# In GitHub: cd-production workflow > Run > canary
# Monitor canary metrics
# If fails, Flagger automatically rolls back
```

---

## Summary of Week 3 Deliverables

| Exercise | Status | Verification |
|----------|--------|--------------|
| 3.1 CI Pipeline | ✅ Done | PR checks pass, artifacts available |
| 3.2 Staging CD | ✅ Done | Auto-deploy on main push, health checks pass |
| 3.3 Production CD | ✅ Done | Manual approval, blue-green/canary options |
| 3.4 GitOps | ✅ Done | ArgoCD syncs manifests from Git |
| 3.5 Security | ✅ Done | SAST, deps, container scans in pipeline |

## Cleanup

```bash
# Remove ArgoCD
kubectl delete namespace argocd

# Remove branches
git branch -d test-ci gitops-test
```

## Proceeding to Week 4

Once all Week 3 checkpoints pass, move to Week 4 — Observability & Operations:
- Prometheus metrics + Grafana dashboards
- Structured JSON logging (ELK/Loki)
- OpenTelemetry tracing (Jaeger)
- SLOs and runbooks

See [Exercicios_Mes_9_Production_Deployment.md](../Exercicios_Mes_9_Production_Deployment.md) for Week 4 roadmap.
