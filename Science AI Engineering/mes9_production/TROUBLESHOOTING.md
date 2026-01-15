# Troubleshooting Guide for Week 2 - Kubernetes Deployment

## Common Issues

### 1. Pods Stuck in "Pending" State

**Symptom:** `kubectl get pods -n bps-dev` shows pods in "Pending"

**Cause:** Usually insufficient resources or missing PersistentVolume

**Solution:**
```bash
# Check pod events
kubectl describe pod <pod-name> -n bps-dev

# Check node resources
kubectl top nodes
kubectl describe node <node-name>

# For PVC issues
kubectl describe pvc postgres-data -n bps-dev
kubectl get pv
```

### 2. Postgres StatefulSet Not Initializing

**Symptom:** bps-postgres-0 stays in "Init" or "CrashLoopBackOff"

**Cause:** Database initialization script error or permission issue

**Solution:**
```bash
# Check logs
kubectl logs bps-postgres-0 -n bps-dev

# Check init script
kubectl exec -it bps-postgres-0 -n bps-dev -- cat /docker-entrypoint-initdb.d/01-init.sql

# Re-run init (dangerous - deletes data!)
kubectl exec bps-postgres-0 -n bps-dev -- psql -U postgres -f /docker-entrypoint-initdb.d/01-init.sql
```

### 3. API Can't Connect to Database

**Symptom:** API logs show "connection refused" or "database unavailable"

**Cause:** Service discovery or credentials issue

**Solution:**
```bash
# Verify Service DNS name
kubectl exec -it deployment/bps-api -n bps-dev -- nslookup bps-postgres.bps-dev.svc.cluster.local

# Check Secret
kubectl get secret bps-secrets -n bps-dev -o yaml

# Test connection from within cluster
kubectl run -it debug --image=postgres:15-alpine -n bps-dev --restart=Never -- \
  psql -h bps-postgres -U postgres -d bps_dev -c "SELECT version();"
```

### 4. Image Pull Issues

**Symptom:** Pods fail with "ImagePullBackOff"

**Cause:** Image not available locally, registry auth issues

**Solution:**
```bash
# For local development clusters (k3d/kind)
docker build -t bps-api:latest .
k3d image import bps-api:latest -c bps-dev

# Check available images in cluster
kubectl get nodes -o wide
docker exec k3d-bps-dev-agent-0 crictl images  # for k3d
```

### 5. Ingress Not Routing Traffic

**Symptom:** `curl api.local` times out or 404

**Cause:** Ingress controller not installed, DNS not configured, TLS issues

**Solution:**
```bash
# Verify ingress controller
kubectl get pods -n ingress-nginx

# Check ingress configuration
kubectl describe ingress bps-api-ingress -n bps-dev

# Port-forward as workaround
kubectl port-forward -n ingress-nginx svc/nginx-ingress-ingress-nginx-controller 443:443

# Test with curl -k (skip cert validation)
curl -k https://localhost/health
```

### 6. Certificate Not Ready

**Symptom:** Ingress shows certificate but status is "Pending"

**Cause:** cert-manager not installed or Issuer not created

**Solution:**
```bash
# Verify cert-manager
kubectl get pods -n cert-manager

# Check certificate status
kubectl describe certificate bps-tls-cert -n bps-dev

# Check issuer
kubectl describe issuer bps-selfsigned-issuer -n bps-dev

# Force renewal
kubectl delete certificate bps-tls-cert -n bps-dev
kubectl apply -f k8s/06-cert-manager.yaml -n bps-dev
```

### 7. Redis Connection Issues

**Symptom:** App logs show "cannot connect to Redis"

**Cause:** Redis pod not running or SERVICE_URL incorrect

**Solution:**
```bash
# Check Redis pod
kubectl get pods -l app=bps-redis -n bps-dev

# Test Redis connectivity
kubectl run -it redis-test --image=redis:7-alpine -n bps-dev --restart=Never -- \
  redis-cli -h bps-redis ping

# Check ConfigMap
kubectl get configmap bps-config -n bps-dev -o yaml | grep redis
```

### 8. Backup CronJob Not Running

**Symptom:** No backup files created, CronJob shows 0 successful runs

**Cause:** ServiceAccount permissions, PVC issues, or job failures

**Solution:**
```bash
# Check CronJob status
kubectl get cronjob -n bps-dev
kubectl describe cronjob postgres-backup -n bps-dev

# Check last job
kubectl get jobs -n bps-dev
kubectl logs -l job-name=<job-name> -n bps-dev

# Manually trigger for testing
kubectl create job postgres-backup-manual --from=cronjob/postgres-backup -n bps-dev
kubectl logs -f job/postgres-backup-manual -n bps-dev

# Verify backup location and permissions
kubectl describe pvc backup-pvc -n bps-dev
```

## Debugging Commands

```bash
# Get detailed cluster status
kubectl get all -n bps-dev
kubectl get all -A  # all namespaces

# Check events
kubectl get events -n bps-dev --sort-by='.lastTimestamp'

# Stream logs from multiple pods
kubectl logs -f deployment/bps-api -n bps-dev
kubectl logs -f statefulset/bps-postgres -n bps-dev

# Execute commands in pod
kubectl exec -it <pod-name> -n bps-dev -- /bin/sh

# Port-forward for manual testing
kubectl port-forward -n bps-dev pod/bps-postgres-0 5432:5432

# Scale deployments
kubectl scale deployment/bps-api --replicas=5 -n bps-dev

# Delete and recreate resources
kubectl delete pod <pod-name> -n bps-dev  # pod will be recreated
kubectl delete deployment bps-api -n bps-dev  # complete removal
```

## Performance Tuning

```bash
# Check resource utilization
kubectl top nodes
kubectl top pods -n bps-dev

# Adjust resource requests/limits
kubectl set resources deployment bps-api \
  -n bps-dev \
  --requests=cpu=250m,memory=256Mi \
  --limits=cpu=1000m,memory=512Mi
```

## Reset Cluster

```bash
# Keep cluster, remove all BPS resources
kubectl delete namespace bps-dev bps-staging bps-prod

# Delete entire cluster
k3d cluster delete bps-dev
kind delete cluster --name bps-dev
```

## Additional Resources

- [Kubernetes Debugging Guide](https://kubernetes.io/docs/tasks/debug-application-cluster/)
- [kubectl Cheatsheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [cert-manager Troubleshooting](https://cert-manager.io/docs/faq/troubleshooting/)
- [nginx-ingress Documentation](https://kubernetes.github.io/ingress-nginx/)
