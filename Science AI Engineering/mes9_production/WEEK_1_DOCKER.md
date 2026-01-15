# Mês 9 — Week 1 Exercises — Docker & Containerization

## Overview
Week 1 focuses on containerizing the BPS API with security best practices, multi-stage builds, and local development environment setup.

---

## Exercise 1.1 — Dockerfile Multi-Stage

### Objective
Create a lightweight, secure Docker image using multi-stage builds.

### What's Provided
- [Dockerfile](../Dockerfile): Multi-stage build (builder + runtime)
- Uses `python:3.10-slim` for build, optimized final image
- Non-root user (uid 1000) for security
- Healthcheck endpoint included
- Read-only filesystem recommendations

### Checkpoint Tasks
1. **Build the image:**
   ```bash
   docker build -t bps-api:latest .
   ```

2. **Check image size (should be <500MB):**
   ```bash
   docker images | grep bps-api
   ```
   Expected: ~200MB (slim + optimized)

3. **Run and test healthcheck:**
   ```bash
   docker run -d -p 8000:8000 --name bps-test bps-api:latest
   sleep 3
   curl http://localhost:8000/health
   docker inspect bps-test | grep Health
   docker stop bps-test && docker rm bps-test
   ```

### Key Points
- Multi-stage reduces final image size by excluding build tools
- Non-root user prevents privilege escalation
- Healthcheck allows Kubernetes to verify container is responding
- `PYTHONDONTWRITEBYTECODE` prevents `.pyc` files

---

## Exercise 1.2 — Docker Compose Development Environment

### Objective
Set up a complete local dev environment with API, Postgres, and Redis using Docker Compose.

### What's Provided
- [docker-compose.yml](../docker-compose.yml): Services for api, db, cache
- Volume mounts for live code editing
- Health checks for dependencies
- Environment variables for easy configuration

### Checkpoint Tasks
1. **Start services:**
   ```bash
   docker compose up -d
   docker compose ps
   ```
   Expected: All services in `Up` state

2. **Wait for services to be healthy:**
   ```bash
   docker compose logs db  # Look for "database system is ready"
   docker compose logs cache  # Look for redis is ready
   ```

3. **Test API health:**
   ```bash
   curl http://localhost:8000/health
   ```
   Expected response:
   ```json
   {
     "status": "healthy",
     "service": "BPS Production API",
     "version": "1.0.0"
   }
   ```

4. **Test database connection:**
   ```bash
   docker compose exec db psql -U postgres -d bps_dev -c "SELECT COUNT(*) FROM optimization_runs;"
   ```
   Expected: 0 rows (empty table)

5. **Test Redis connection:**
   ```bash
   docker compose exec cache redis-cli ping
   ```
   Expected: `PONG`

6. **Stop all services:**
   ```bash
   docker compose down -v  # -v removes volumes
   ```

### Key Points
- Compose orchestrates multiple services locally
- Volume mounts enable hot code reload during development
- Health checks ensure dependencies are ready before app starts
- Database initialization runs automatically from `scripts/init_db.sql`

---

## Exercise 1.3 — Security Hardening

### Objective
Ensure container runs with minimal privileges and read-only filesystem where possible.

### What's Provided
- [Dockerfile](../Dockerfile): Non-root user (1000), recommendations for read-only FS
- App structured to use `/tmp` for temporary files only

### Checkpoint Tasks
1. **Verify non-root user in image:**
   ```bash
   docker build -t bps-api:latest .
   docker run --rm bps-api:latest whoami
   ```
   Expected: `appuser` (not `root`)

2. **Test with read-only filesystem:**
   ```bash
   docker run --rm --read-only \
     -v /tmp:/tmp \
     -p 8000:8000 \
     bps-api:latest &
   sleep 3
   curl http://localhost:8000/health
   ```
   Expected: API responds even with read-only root

3. **Verify security context:**
   ```bash
   docker inspect bps-api:latest | grep -A 5 "User"
   ```
   Expected: User shows as `1000` or `appuser`

### Key Points
- Non-root prevents container escape exploits
- Read-only filesystem protects against file modification attacks
- Any writable paths (`/tmp`) should be listed explicitly

---

## Exercise 1.4 — Image Vulnerability Scanning

### Objective
Scan Docker image for known vulnerabilities using Trivy.

### Prerequisites
```bash
# Install Trivy (on Windows with choco/scoop, or download binary)
# Option 1: Using docker (no local install needed)
# Option 2: scoop install trivy (Windows)
```

### Checkpoint Tasks
1. **Build image for scanning:**
   ```bash
   docker build -t bps-api:latest .
   ```

2. **Scan with Trivy (via Docker):**
   ```bash
   docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
     aquasec/trivy image --severity HIGH,CRITICAL bps-api:latest
   ```
   Expected: No CRITICAL or HIGH severity vulnerabilities

3. **If vulnerabilities found, update dependencies:**
   ```bash
   # Check requirements.txt for outdated packages
   pip list --outdated
   # Update (cautiously):
   pip install --upgrade <package>
   # Update requirements.txt
   pip freeze > requirements.txt
   ```

4. **Scan again to verify fix:**
   ```bash
   docker build -t bps-api:latest .
   docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
     aquasec/trivy image --severity HIGH,CRITICAL bps-api:latest
   ```

### Key Points
- Trivy scans for CVEs in dependencies
- Regular scanning prevents security drift
- Container registry integrations (Docker Hub, ECR, GCR) can automate scanning

---

## Summary of Week 1 Deliverables

| Exercise | Status | Verification |
|----------|--------|--------------|
| 1.1 Dockerfile | ✅ Done | `docker build`, image <500MB, healthcheck ✓ |
| 1.2 Compose | ✅ Done | `docker compose up`, all services healthy ✓ |
| 1.3 Security | ✅ Done | Non-root user, read-only FS test ✓ |
| 1.4 Scanning | ✅ Done | Trivy scan passes (no critical vulns) ✓ |

## Proceeding to Week 2

Once all Week 1 checkpoints pass, move to Week 2 — Kubernetes Orchestration:
- Namespace creation
- Deployment manifests with probes and resource limits
- StatefulSet for Postgres persistence
- Service discovery and networking

See [Exercicios_Mes_9_Production_Deployment.md](../Exercicios_Mes_9_Production_Deployment.md) for Week 2 roadmap.
