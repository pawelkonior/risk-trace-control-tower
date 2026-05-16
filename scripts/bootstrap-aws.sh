#!/usr/bin/env bash
set -euo pipefail

# Bootstrap Terraform state backend for a given environment.
# Usage: ./scripts/bootstrap-aws.sh <environment>
# Requires: AWS_PROFILE and AWS_DEFAULT_REGION environment variables.
#
# Idempotent: safe to run multiple times.
# Reads bucket and DynamoDB table names from backend.tf — no hardcoded values.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# ============================================================================
# Validate required env vars
# ============================================================================

if [[ -z "${AWS_PROFILE:-}" ]]; then
  echo "ERROR: AWS_PROFILE is not set. Export it before running this script." >&2
  exit 1
fi

if [[ -z "${AWS_DEFAULT_REGION:-}" ]]; then
  echo "ERROR: AWS_DEFAULT_REGION is not set. Export it before running this script." >&2
  exit 1
fi

# ============================================================================
# Validate environment argument
# ============================================================================

ENV="${1:-}"
if [[ -z "${ENV}" ]]; then
  echo "ERROR: Environment argument required." >&2
  echo "Usage: $0 <environment>  (e.g. dev, prod)" >&2
  exit 1
fi

ENV_DIR="${REPO_ROOT}/infra/terraform/environments/${ENV}"
BACKEND_TF="${ENV_DIR}/backend.tf"

if [[ ! -f "${BACKEND_TF}" ]]; then
  echo "ERROR: backend.tf not found at ${BACKEND_TF}" >&2
  exit 1
fi

# ============================================================================
# Parse bucket and DynamoDB table from backend.tf
# ============================================================================

STATE_BUCKET=$(grep -E '^\s+bucket\s*=' "${BACKEND_TF}" | head -1 | sed 's/.*"\(.*\)".*/\1/')
DYNAMODB_TABLE=$(grep -E '^\s+dynamodb_table\s*=' "${BACKEND_TF}" | head -1 | sed 's/.*"\(.*\)".*/\1/')
BACKEND_REGION=$(grep -E '^\s+region\s*=' "${BACKEND_TF}" | head -1 | sed 's/.*"\(.*\)".*/\1/')

if [[ -z "${STATE_BUCKET}" ]]; then
  echo "ERROR: Could not parse 'bucket' from ${BACKEND_TF}" >&2
  exit 1
fi
if [[ -z "${DYNAMODB_TABLE}" ]]; then
  echo "ERROR: Could not parse 'dynamodb_table' from ${BACKEND_TF}" >&2
  exit 1
fi
if [[ -z "${BACKEND_REGION}" ]]; then
  BACKEND_REGION="${AWS_DEFAULT_REGION}"
fi

echo "==> Environment  : ${ENV}"
echo "==> State bucket : ${STATE_BUCKET} (${BACKEND_REGION})"
echo "==> Lock table   : ${DYNAMODB_TABLE}"
echo "==> AWS profile  : ${AWS_PROFILE}"
echo ""

# ============================================================================
# Create S3 state bucket (idempotent)
# ============================================================================

echo "==> Bootstrapping S3 state bucket..."

if aws s3api head-bucket --bucket "${STATE_BUCKET}" --region "${BACKEND_REGION}" 2>/dev/null; then
  echo "    Bucket already exists, skipping creation."
else
  aws s3api create-bucket \
    --bucket "${STATE_BUCKET}" \
    --region "${BACKEND_REGION}" \
    --create-bucket-configuration LocationConstraint="${BACKEND_REGION}" \
    --output text > /dev/null
  echo "    Bucket created."
fi

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket "${STATE_BUCKET}" \
  --versioning-configuration Status=Enabled \
  --region "${BACKEND_REGION}" > /dev/null
echo "    Versioning enabled."

# Enable SSE-S3 encryption
aws s3api put-bucket-encryption \
  --bucket "${STATE_BUCKET}" \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      },
      "BucketKeyEnabled": true
    }]
  }' \
  --region "${BACKEND_REGION}" > /dev/null
echo "    SSE-S3 encryption enabled."

# Block all public access
aws s3api put-public-access-block \
  --bucket "${STATE_BUCKET}" \
  --public-access-block-configuration \
    "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true" \
  --region "${BACKEND_REGION}" > /dev/null
echo "    Public access blocked."

# ============================================================================
# Create DynamoDB lock table (idempotent)
# ============================================================================

echo ""
echo "==> Bootstrapping DynamoDB lock table..."

if aws dynamodb describe-table \
    --table-name "${DYNAMODB_TABLE}" \
    --region "${BACKEND_REGION}" \
    --output text > /dev/null 2>&1; then
  echo "    Table already exists, skipping creation."
else
  aws dynamodb create-table \
    --table-name "${DYNAMODB_TABLE}" \
    --attribute-definitions AttributeName=LockID,AttributeType=S \
    --key-schema AttributeName=LockID,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region "${BACKEND_REGION}" \
    --output text > /dev/null
  echo "    Table created."

  aws dynamodb wait table-exists \
    --table-name "${DYNAMODB_TABLE}" \
    --region "${BACKEND_REGION}"
  echo "    Table active."
fi

# ============================================================================
# Terraform init → plan → prompt → apply
# ============================================================================

echo ""
echo "==> Running Terraform in ${ENV_DIR}"
cd "${ENV_DIR}"

echo ""
echo "--- terraform init ---"
terraform init -reconfigure

echo ""
echo "--- terraform plan ---"
terraform plan -out=tfplan.out

echo ""
read -r -p "Apply? [y/N] " CONFIRM
if [[ "${CONFIRM}" != "y" && "${CONFIRM}" != "Y" ]]; then
  echo "Aborted. Plan saved to ${ENV_DIR}/tfplan.out"
  exit 0
fi

echo ""
echo "--- terraform apply ---"
terraform apply tfplan.out

echo ""
echo "==> Bootstrap complete for environment: ${ENV}"
