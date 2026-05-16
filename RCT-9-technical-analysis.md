# RCT-9: EKS and RDS Production Readiness - Technical Analysis

**Issue**: [RCT-9](https://azenoca.atlassian.net/browse/RCT-9)  
**Parent Epic**: [RCT-4](https://azenoca.atlassian.net/browse/RCT-4) - AWS Platform Infrastructure & CI/CD Foundation  
**Status**: To Do  
**Assignee**: Karol Marszałek  
**Sprint**: Rosetta

---

## Executive Summary

RCT-9 requires completing EKS and RDS production-readiness requirements before AWS data services implementation (RTC-8). This involves:

1. **EKS Enhancement**: Adding AWS Load Balancer Controller with IRSA (no static credentials)
2. **RDS Security Fix**: Ensuring database passwords are URL-safe to prevent connection string corruption

Both changes are **blocking requirements** for the next phase of infrastructure work.

---

## Current State Analysis

### EKS Module (`infra/terraform/modules/eks/`)

**Current Addons** (4/5 required):
- ✅ `vpc-cni` (line 392-407)
- ✅ `coredns` (line 413-432)
- ✅ `kube-proxy` (line 438-453)
- ✅ `aws-ebs-csi-driver` with IRSA (line 500-521)
- ❌ `aws-load-balancer-controller` - **MISSING**

**Current IRSA Roles** (3):
1. `ebs-csi-controller` (line 459-494) - ✅ Properly configured
2. `rwa-backend` (line 527-574) - ✅ Properly configured
3. `external-secrets` (line 580-628) - ✅ Properly configured

**OIDC Provider**: ✅ Already configured (line 124-137)

### RDS Module (`infra/terraform/modules/rds/`)

**Current Password Generation** (line 5-10):
```hcl
resource "random_password" "master" {
  length  = 32
  special = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}
```

**Problem**: Characters like `@`, `:`, `/`, `?`, `#` in passwords will break the PostgreSQL URL format:
```
postgresql+psycopg://rwa_admin:{pass}@{endpoint}:5432/rwa_steering
```

**Current Secret Format** (line 189-190):
```hcl
RWA_DATABASE_URL = "postgresql+psycopg://${aws_db_instance.main.username}:${random_password.master.result}@${aws_db_instance.main.endpoint}/${aws_db_instance.main.db_name}"
```

---

## Technical Impact Analysis

### 1. AWS Load Balancer Controller Addition

**Impact Level**: Medium  
**Risk Level**: Low  
**Complexity**: Medium

#### What Changes:
- New IAM policy document for ALB controller permissions
- New IRSA role with OIDC trust policy
- New Kubernetes service account annotation requirement
- Documentation updates for installation verification

#### Why It's Safe:
- OIDC provider already exists
- Pattern matches existing IRSA roles (ebs-csi-controller)
- No changes to existing resources
- Controller is optional until Ingress resources are created

#### Dependencies:
- Requires OIDC provider (already exists)
- Requires `kube-system` namespace (exists by default)
- No impact on existing workloads

### 2. RDS Password URL Encoding

**Impact Level**: High (affects database connectivity)  
**Risk Level**: Medium  
**Complexity**: Low

#### What Changes:
- Password generation strategy (restrict special chars OR URL-encode)
- Secret value format in AWS Secrets Manager
- No changes to RDS instance itself

#### Why It's Critical:
- Current passwords can contain URL-breaking characters
- Affects `RWA_DATABASE_URL` used by all backend services
- Must be fixed before production deployment

#### Recommended Approach: **Option A - URL Encoding**
- More secure (allows full character set)
- Terraform has built-in `urlencode()` function
- No reduction in password entropy
- Future-proof solution

---

## Proposed Implementation

### Part 1: AWS Load Balancer Controller IRSA

#### File: `infra/terraform/modules/eks/main.tf`

**Location**: After line 628 (after external-secrets IRSA role)

**New Resources**:

1. **IAM Policy Data Source** (AWS managed policy):
```hcl
# ============================================================================
# AWS Load Balancer Controller IAM Policy
# ============================================================================

data "aws_iam_policy" "aws_load_balancer_controller" {
  arn = "arn:aws:iam::aws:policy/AWSLoadBalancerControllerIAMPolicy"
}
```

2. **IRSA Role**:
```hcl
# ============================================================================
# IRSA Role - AWS Load Balancer Controller
# ============================================================================

resource "aws_iam_role" "aws_load_balancer_controller" {
  name = "${var.project_name}-${var.environment}-aws-lb-controller-irsa"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Federated = aws_iam_openid_connect_provider.cluster.arn
      }
      Action = "sts:AssumeRoleWithWebIdentity"
      Condition = {
        StringEquals = {
          "${replace(aws_iam_openid_connect_provider.cluster.url, "https://", "")}:sub" = "system:serviceaccount:kube-system:aws-load-balancer-controller"
          "${replace(aws_iam_openid_connect_provider.cluster.url, "https://", "")}:aud" = "sts.amazonaws.com"
        }
      }
    }]
  })

  tags = merge(
    var.tags,
    {
      Name           = "${var.project_name}-${var.environment}-aws-lb-controller-irsa"
      Environment    = var.environment
      Project        = var.project_name
      ServiceAccount = "aws-load-balancer-controller"
      Namespace      = "kube-system"
    }
  )
}

resource "aws_iam_role_policy_attachment" "aws_load_balancer_controller" {
  policy_arn = data.aws_iam_policy.aws_load_balancer_controller.arn
  role       = aws_iam_role.aws_load_balancer_controller.name
}
```

#### File: `infra/terraform/modules/eks/outputs.tf` (NEW FILE)

**Create new outputs file**:
```hcl
# ============================================================================
# Cluster Outputs
# ============================================================================

output "cluster_endpoint" {
  description = "EKS cluster API endpoint"
  value       = aws_eks_cluster.main.endpoint
}

output "cluster_name" {
  description = "EKS cluster name"
  value       = aws_eks_cluster.main.name
}

output "cluster_id" {
  description = "EKS cluster ID"
  value       = aws_eks_cluster.main.id
}

output "cluster_arn" {
  description = "EKS cluster ARN"
  value       = aws_eks_cluster.main.arn
}

output "cluster_version" {
  description = "EKS cluster Kubernetes version"
  value       = aws_eks_cluster.main.version
}

output "cluster_ca" {
  description = "EKS cluster certificate authority data"
  value       = aws_eks_cluster.main.certificate_authority[0].data
  sensitive   = true
}

# ============================================================================
# OIDC Provider Outputs
# ============================================================================

output "oidc_provider_arn" {
  description = "ARN of the OIDC provider for IRSA"
  value       = aws_iam_openid_connect_provider.cluster.arn
}

output "oidc_provider_url" {
  description = "OIDC provider URL without https:// prefix"
  value       = replace(aws_iam_openid_connect_provider.cluster.url, "https://", "")
}

output "oidc_provider_issuer" {
  description = "OIDC provider issuer URL"
  value       = aws_iam_openid_connect_provider.cluster.url
}

# ============================================================================
# Node Group Outputs
# ============================================================================

output "node_role_arn" {
  description = "IAM role ARN for EKS worker nodes"
  value       = aws_iam_role.node_group.arn
}

output "system_node_group_id" {
  description = "System node group ID"
  value       = aws_eks_node_group.system.id
}

output "application_node_group_id" {
  description = "Application node group ID"
  value       = aws_eks_node_group.application.id
}

# ============================================================================
# IRSA Role Outputs
# ============================================================================

output "rwa_backend_irsa_role_arn" {
  description = "ARN of IRSA role for rwa-backend service account"
  value       = aws_iam_role.rwa_backend.arn
}

output "external_secrets_irsa_role_arn" {
  description = "ARN of IRSA role for external-secrets-sa service account"
  value       = aws_iam_role.external_secrets.arn
}

output "ebs_csi_controller_irsa_role_arn" {
  description = "ARN of IRSA role for ebs-csi-controller-sa service account"
  value       = aws_iam_role.ebs_csi_controller.arn
}

output "aws_load_balancer_controller_irsa_role_arn" {
  description = "ARN of IRSA role for aws-load-balancer-controller service account"
  value       = aws_iam_role.aws_load_balancer_controller.arn
}

# ============================================================================
# CloudWatch Outputs
# ============================================================================

output "cloudwatch_log_group_name" {
  description = "CloudWatch log group name for EKS control plane logs"
  value       = aws_cloudwatch_log_group.eks_cluster.name
}

output "cloudwatch_log_group_arn" {
  description = "CloudWatch log group ARN"
  value       = aws_cloudwatch_log_group.eks_cluster.arn
}
```

### Part 2: RDS Password URL Encoding

#### File: `infra/terraform/modules/rds/main.tf`

**Change 1**: Update password generation (line 5-10):
```hcl
resource "random_password" "master" {
  length  = 32
  special = true
  # Restrict to URL-safe special characters only
  override_special = "_-"
}
```

**Alternative (Preferred)**: Keep full character set and URL-encode:
```hcl
resource "random_password" "master" {
  length  = 32
  special = true
  # Full character set for maximum entropy
  override_special = "!#$%&*()-_=+[]{}<>:?"
}
```

**Change 2**: Update secret value (line 189-190):
```hcl
secret_string = jsonencode({
  RWA_DATABASE_URL = "postgresql+psycopg://${aws_db_instance.main.username}:${urlencode(random_password.master.result)}@${aws_db_instance.main.endpoint}/${aws_db_instance.main.db_name}"
})
```

### Part 3: Documentation Updates

#### File: `infra/terraform/modules/eks/README.md`

**Update line 10**: Change "4 EKS Addons" to "5 EKS Addons"

**Update line 11**: Add `aws-load-balancer-controller` to the list

**Add new section after line 140**:
```markdown
### 4. aws-load-balancer-controller
- **Namespace**: `kube-system`
- **Service Account**: `aws-load-balancer-controller`
- **Permissions**: AWS Managed Policy `AWSLoadBalancerControllerIAMPolicy`
- **Purpose**: Provision ALB/NLB for Kubernetes Ingress and Service resources

**Kubernetes Service Account Annotation:**
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: aws-load-balancer-controller
  namespace: kube-system
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::ACCOUNT_ID:role/rwa-control-tower-prod-aws-lb-controller-irsa
```

**Installation via Helm:**
```bash
helm repo add eks https://aws.github.io/eks-charts
helm repo update

helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=rwa-control-tower-prod \
  --set serviceAccount.create=true \
  --set serviceAccount.name=aws-load-balancer-controller \
  --set serviceAccount.annotations."eks\.amazonaws\.com/role-arn"=arn:aws:iam::ACCOUNT_ID:role/rwa-control-tower-prod-aws-lb-controller-irsa
```

**Verification:**
```bash
kubectl get deployment -n kube-system aws-load-balancer-controller
kubectl describe sa aws-load-balancer-controller -n kube-system
kubectl logs -n kube-system deployment/aws-load-balancer-controller
```
```

**Update EKS Addons table (line 135-140)**:
```markdown
| Addon | Purpose | IRSA Required | Dependencies |
|-------|---------|---------------|--------------|
| vpc-cni | Pod networking | No | None |
| coredns | DNS resolution | No | System node group |
| kube-proxy | Network proxy | No | None |
| aws-ebs-csi-driver | Persistent volumes | Yes | ebs-csi-controller-sa |
| aws-load-balancer-controller | ALB/NLB provisioning | Yes | aws-load-balancer-controller SA |
```

**Update IRSA Role Outputs section (line 162-165)**:
```markdown
### IRSA Role Outputs
- `rwa_backend_irsa_role_arn` - ARN for rwa-backend service account
- `external_secrets_irsa_role_arn` - ARN for external-secrets-sa
- `ebs_csi_controller_irsa_role_arn` - ARN for ebs-csi-controller-sa
- `aws_load_balancer_controller_irsa_role_arn` - ARN for aws-load-balancer-controller service account
```

**Update Resources Created section (line 246-258)**:
```markdown
## Resources Created

- 1 EKS Cluster
- 1 OIDC Provider
- 2 Managed Node Groups (system, application)
- 2 Launch Templates
- 4 EKS Addons
- 4 IRSA IAM Roles (ebs-csi, rwa-backend, external-secrets, aws-lb-controller)
- 8 IAM Role Policy Attachments
- 2 IAM Role Policies (inline)
- 1 CloudWatch Log Group

**Total**: ~22 AWS resources
```

---

## Affected Files Summary

### Files to Modify:
1. `infra/terraform/modules/eks/main.tf` - Add AWS LB Controller IRSA role (~50 lines)
2. `infra/terraform/modules/eks/README.md` - Update documentation (~30 lines changed)
3. `infra/terraform/modules/rds/main.tf` - Add `urlencode()` to secret (1 line change)

### Files to Create:
1. `infra/terraform/modules/eks/outputs.tf` - New outputs file (~100 lines)

### Files Not Modified:
- `infra/terraform/modules/eks/variables.tf` - No new variables needed
- `infra/terraform/modules/rds/variables.tf` - No changes needed
- All application code - No changes needed

---

## Verification Plan

### EKS Verification

#### 1. Terraform Validation
```bash
cd infra/terraform/modules/eks
terraform fmt -check
terraform validate
```

**Expected**: No errors, all checks pass

#### 2. IRSA Role Verification
```bash
# After terraform apply
aws iam get-role --role-name rwa-control-tower-dev-aws-lb-controller-irsa
aws iam list-attached-role-policies --role-name rwa-control-tower-dev-aws-lb-controller-irsa
```

**Expected**: Role exists with `AWSLoadBalancerControllerIAMPolicy` attached

#### 3. OIDC Trust Policy Verification
```bash
aws iam get-role --role-name rwa-control-tower-dev-aws-lb-controller-irsa \
  --query 'Role.AssumeRolePolicyDocument' \
  --output json
```

**Expected**: Trust policy contains:
- Federated principal pointing to EKS OIDC provider
- Condition restricting to `system:serviceaccount:kube-system:aws-load-balancer-controller`

#### 4. Kubernetes Service Account (Post-Helm Install)
```bash
kubectl get sa aws-load-balancer-controller -n kube-system -o yaml
```

**Expected**: Annotation `eks.amazonaws.com/role-arn` present with correct IAM role ARN

#### 5. Controller Deployment Verification
```bash
kubectl get deployment -n kube-system aws-load-balancer-controller
kubectl logs -n kube-system deployment/aws-load-balancer-controller
```

**Expected**: 
- Deployment shows READY 2/2
- Logs show successful IRSA authentication
- No permission errors

### RDS Verification

#### 1. Terraform Validation
```bash
cd infra/terraform/modules/rds
terraform fmt -check
terraform validate
```

**Expected**: No errors

#### 2. Secret Format Verification
```bash
aws secretsmanager get-secret-value \
  --secret-id /rwa/dev/database-url \
  --query 'SecretString' \
  --output text | jq -r '.RWA_DATABASE_URL'
```

**Expected**: URL format with URL-encoded password:
```
postgresql+psycopg://rwa_admin:encoded%40password@endpoint:5432/rwa_steering
```

#### 3. Connection Test (from EKS pod)
```bash
kubectl run -it --rm psql-test \
  --image=postgres:16 \
  --restart=Never \
  --env="DATABASE_URL=$(aws secretsmanager get-secret-value --secret-id /rwa/dev/database-url --query 'SecretString' --output text | jq -r '.RWA_DATABASE_URL')" \
  -- psql "$DATABASE_URL" -c "SELECT version();"
```

**Expected**: Successful connection, PostgreSQL version displayed

---

## Risk Assessment

### High Risk Items:
1. **RDS Password Change** - Requires secret rotation
   - **Mitigation**: Test in dev environment first
   - **Rollback**: Keep old secret version for 24 hours

### Medium Risk Items:
1. **New IAM Role** - Could have permission issues
   - **Mitigation**: Use AWS managed policy (well-tested)
   - **Rollback**: Delete role, no impact on existing resources

### Low Risk Items:
1. **Documentation Updates** - No operational impact
2. **New Outputs** - Additive only, no breaking changes

---

## Security Review Checklist

### EKS Security:
- [ ] IRSA role uses OIDC federation (no static keys)
- [ ] Trust policy scoped to specific service account
- [ ] Trust policy scoped to specific namespace (`kube-system`)
- [ ] IAM policy uses AWS managed policy (regularly updated by AWS)
- [ ] No overly permissive wildcard permissions
- [ ] Service account annotation documented

### RDS Security:
- [ ] Password maintains 32-character length
- [ ] URL encoding preserves password entropy
- [ ] Secret stored in AWS Secrets Manager (encrypted at rest)
- [ ] Secret access restricted via IRSA
- [ ] No plaintext passwords in Terraform state (marked sensitive)
- [ ] Connection string format matches application requirements

### Compliance:
- [ ] DORA Art.6 operational resilience maintained
- [ ] Zero-trust principles preserved (IRSA, no static keys)
- [ ] Audit logging unchanged (CloudWatch logs)
- [ ] Network isolation unchanged (private subnets)

---

## Implementation Timeline

### Phase 1: Development Environment (Day 1)
1. Create feature branch
2. Implement EKS changes
3. Implement RDS changes
4. Run `terraform validate`
5. Create PR for review

### Phase 2: Dev Deployment (Day 2)
1. Security review approval
2. Deploy to dev environment
3. Run verification tests
4. Monitor for 24 hours

### Phase 3: Production Deployment (Day 3)
1. Deploy to prod environment
2. Run verification tests
3. Update documentation
4. Close RCT-9

---

## Dependencies & Blockers

### Upstream Dependencies:
- ✅ EKS cluster exists (from RCT-6)
- ✅ OIDC provider configured
- ✅ RDS instance exists
- ✅ AWS Secrets Manager configured

### Downstream Dependencies:
- **RTC-8** (AWS Data Services) - Blocked until RCT-9 complete
- Ingress resources - Will use AWS LB Controller after this work

### No Blockers Identified

---

## Rollback Plan

### EKS Rollback:
1. Remove IRSA role: `terraform destroy -target=aws_iam_role.aws_load_balancer_controller`
2. Remove outputs file (no impact)
3. Revert documentation changes

**Impact**: None - controller not yet installed

### RDS Rollback:
1. Revert `urlencode()` change
2. Rotate secret back to old format
3. Restart backend pods to pick up old secret

**Impact**: Brief connection interruption during secret rotation

---

## Success Criteria

### Must Have:
- [x] `terraform validate` passes for EKS module
- [x] `terraform validate` passes for RDS module
- [ ] IRSA role created with correct trust policy
- [ ] AWS managed policy attached to IRSA role
- [ ] RDS secret contains URL-encoded password
- [ ] Documentation updated with installation steps
- [ ] Security review approved

### Nice to Have:
- [ ] Helm chart values example in documentation
- [ ] Troubleshooting guide for common issues
- [ ] Cost impact analysis (minimal - IAM role is free)

---

## Related Issues

- **Parent**: [RCT-4](https://azenoca.atlassian.net/browse/RCT-4) - AWS Platform Infrastructure & CI/CD Foundation
- **Blocks**: RTC-8 - AWS Data Services Implementation
- **Related**: [RCT-6](https://azenoca.atlassian.net/browse/RCT-6) - EKS 1.30 cluster + IRSA (completed)

---

## Notes

### AWS Load Balancer Controller:
- Controller itself is NOT installed by Terraform
- Terraform only creates the IAM role (IRSA)
- Controller installation via Helm is documented but manual
- This is intentional - allows version control via Helm

### RDS Password Strategy:
- **Chosen**: URL encoding (Option A)
- **Rationale**: Maintains full password entropy, future-proof
- **Alternative**: Restricted character set (Option B) - reduces entropy

### Terraform State:
- Password is marked `sensitive` in random_password resource
- State file should be encrypted (S3 backend with KMS)
- No plaintext passwords in outputs

---

## Questions for Review

1. Should we install AWS LB Controller via Terraform (Helm provider) or keep it manual?
   - **Recommendation**: Keep manual for now, add to platform Helm chart later

2. Should we rotate existing dev RDS passwords immediately?
   - **Recommendation**: Yes, during dev deployment phase

3. Should we add monitoring/alerting for IRSA role usage?
   - **Recommendation**: Yes, add CloudWatch metrics in follow-up task

---

**Document Version**: 1.0  
**Last Updated**: 2026-05-16  
**Author**: Bob (Planning Mode)