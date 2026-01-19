#!/bin/bash
# Setup script for Week 2 - Kubernetes Orchestration
# This script sets up a local k8s cluster and deploys all manifests

set -e

CLUSTER_NAME="bps-dev"
CLUSTER_TYPE=${1:-k3d}  # k3d, kind, or docker-desktop

echo "🚀 Setting up Kubernetes cluster: $CLUSTER_NAME (using $CLUSTER_TYPE)"

# Create cluster
case $CLUSTER_TYPE in
  k3d)
    echo "Creating k3d cluster..."
    if ! k3d cluster list | grep -q "$CLUSTER_NAME"; then
      k3d cluster create "$CLUSTER_NAME" --servers 1 --agents 2 --port 80:80@loadbalancer --port 443:443@loadbalancer
    else
      echo "Cluster already exists"
    fi
    ;;
  kind)
    echo "Creating kind cluster..."
    if ! kind get clusters | grep -q "$CLUSTER_NAME"; then
      kind create cluster --name "$CLUSTER_NAME" --config - <<EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  ports:
  - containerPort: 80
    hostPort: 80
  - containerPort: 443
    hostPort: 443
- role: worker
EOF
    else
      echo "Cluster already exists"
    fi
    ;;
  docker-desktop)
    echo "Using Docker Desktop Kubernetes (must be enabled)"
    ;;
esac

echo "⏳ Waiting for cluster to be ready..."
kubectl cluster-info
kubectl wait --for=condition=Ready nodes --all --timeout=300s 2>/dev/null || true

# Create namespaces
echo ""
echo "Creating namespaces..."
kubectl apply -f k8s/00-namespaces.yaml

# Deploy to dev namespace
echo ""
echo "Deploying to bps-dev namespace..."
kubectl apply -f k8s/02-configmap-secrets.yaml -n bps-dev
kubectl apply -f k8s/03-postgres-statefulset.yaml -n bps-dev
kubectl apply -f k8s/04-redis-deployment.yaml -n bps-dev

# Build and load image
echo ""
echo "Building Docker image..."
docker build -t bps-api:latest .

if command -v k3d &> /dev/null && [ "$CLUSTER_TYPE" = "k3d" ]; then
  echo "Loading image into k3d cluster..."
  k3d image import bps-api:latest -c "$CLUSTER_NAME"
elif command -v kind &> /dev/null && [ "$CLUSTER_TYPE" = "kind" ]; then
  echo "Loading image into kind cluster..."
  kind load docker-image bps-api:latest --name "$CLUSTER_NAME"
fi

# Deploy API
echo ""
echo "Deploying API..."
kubectl apply -f k8s/01-api-deployment.yaml -n bps-dev

# Wait for readiness
echo ""
echo "Waiting for deployments to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/bps-api -n bps-dev

echo ""
echo "✅ Kubernetes cluster setup complete!"
echo ""
echo "Next steps:"
echo "  1. Test deployment:"
echo "     ./test-k8s.sh dev"
echo ""
echo "  2. (Optional) Install ingress and cert-manager:"
echo "     helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx"
echo "     helm install nginx-ingress ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace"
echo ""
echo "  3. Clean up when done:"
echo "     k3d cluster delete $CLUSTER_NAME"
