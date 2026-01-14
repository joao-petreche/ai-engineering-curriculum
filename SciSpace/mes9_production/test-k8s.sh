#!/bin/bash
# Helper script to test local Kubernetes deployment
# Usage: ./test-k8s.sh [dev|staging|prod]

set -e

ENVIRONMENT=${1:-dev}
NAMESPACE="bps-$ENVIRONMENT"

echo "Testing Kubernetes deployment for: $NAMESPACE"

# Check if namespace exists
if ! kubectl get namespace "$NAMESPACE" &> /dev/null; then
    echo "❌ Namespace $NAMESPACE does not exist"
    exit 1
fi

echo "✅ Namespace $NAMESPACE exists"

# Check pods
echo ""
echo "Checking pods..."
if kubectl get pods -n "$NAMESPACE" --no-headers | grep -q "Running"; then
    echo "✅ Running pods found:"
    kubectl get pods -n "$NAMESPACE" -o wide
else
    echo "❌ No running pods found"
    exit 1
fi

# Check services
echo ""
echo "Checking services..."
kubectl get svc -n "$NAMESPACE"

# Port-forward and test health
echo ""
echo "Testing health endpoint..."
kubectl port-forward -n "$NAMESPACE" svc/bps-api 8000:8000 &
PF_PID=$!
sleep 3

if curl -f http://localhost:8000/health &> /dev/null; then
    echo "✅ Health endpoint responsive"
else
    echo "❌ Health endpoint failed"
    kill $PF_PID
    exit 1
fi

if curl -f http://localhost:8000/health/ready &> /dev/null; then
    echo "✅ Readiness check passed"
else
    echo "⚠️  Readiness check failed (dependencies may not be ready)"
fi

kill $PF_PID

echo ""
echo "✅ All tests passed for $NAMESPACE"
