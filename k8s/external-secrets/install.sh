#!/usr/bin/env bash
set -euo pipefail

# Install External Secrets Operator via Helm.
# Prerequisites: helm, kubectl configured against target cluster.

ESO_VERSION="${ESO_VERSION:-0.10.5}"
NAMESPACE="external-secrets"

echo "==> Installing External Secrets Operator v${ESO_VERSION}"

helm repo add external-secrets https://charts.external-secrets.io
helm repo update

helm upgrade --install external-secrets external-secrets/external-secrets \
  --namespace "${NAMESPACE}" \
  --create-namespace \
  --version "${ESO_VERSION}" \
  --set installCRDs=true \
  --set serviceAccount.name=external-secrets-sa \
  --set serviceAccount.annotations."eks\.amazonaws\.com/role-arn"="${ESO_IRSA_ROLE_ARN:?ESO_IRSA_ROLE_ARN must be set}" \
  --wait

echo "==> Waiting for External Secrets Operator pods to be ready..."
kubectl rollout status deployment/external-secrets -n "${NAMESPACE}" --timeout=120s

echo "==> Applying ClusterSecretStore..."
kubectl apply -f "$(dirname "${BASH_SOURCE[0]}")/clustersecretstore.yaml"

echo "==> Verifying ClusterSecretStore..."
kubectl wait clustersecretstore/aws-secrets-manager \
  --for=condition=Ready \
  --timeout=60s

echo "==> External Secrets Operator installed and ClusterSecretStore Ready."
echo "    Apply backend-externalsecret.yaml per namespace:"
echo "    kubectl apply -f backend-externalsecret.yaml"
