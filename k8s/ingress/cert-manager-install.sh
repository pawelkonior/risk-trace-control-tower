#!/usr/bin/env bash
set -euo pipefail

# Install cert-manager and NGINX Ingress Controller via Helm.
# Prerequisites: helm, kubectl configured against target cluster.

CERT_MANAGER_VERSION="${CERT_MANAGER_VERSION:-v1.15.3}"
NGINX_VERSION="${NGINX_VERSION:-4.11.2}"

echo "==> Installing NGINX Ingress Controller (AWS NLB)..."

helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --version "${NGINX_VERSION}" \
  --set controller.service.type=LoadBalancer \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/aws-load-balancer-type"=nlb \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/aws-load-balancer-scheme"=internet-facing \
  --set controller.metrics.enabled=true \
  --set controller.config.proxy-body-size=1m \
  --wait

echo "==> Waiting for NGINX Ingress external IP..."
kubectl wait svc/ingress-nginx-controller \
  -n ingress-nginx \
  --for=jsonpath='{.status.loadBalancer.ingress[0].hostname}' \
  --timeout=300s

echo "==> Installing cert-manager ${CERT_MANAGER_VERSION}..."

helm repo add jetstack https://charts.jetstack.io
helm repo update

helm upgrade --install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version "${CERT_MANAGER_VERSION}" \
  --set installCRDs=true \
  --wait

echo "==> Waiting for cert-manager webhook..."
kubectl rollout status deployment/cert-manager-webhook -n cert-manager --timeout=120s

echo "==> Applying ClusterIssuers..."
kubectl apply -f "$(dirname "${BASH_SOURCE[0]}")/../cert-manager/cluster-issuer-staging.yaml"
kubectl apply -f "$(dirname "${BASH_SOURCE[0]}")/../cert-manager/cluster-issuer-prod.yaml"

echo "==> cert-manager and NGINX Ingress installed."
echo "    NGINX LB hostname:"
kubectl get svc ingress-nginx-controller -n ingress-nginx \
  -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
echo ""
