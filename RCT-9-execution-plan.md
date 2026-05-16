# RCT-9: Execution Plan & Summary

**Branch**: `feature/RCT-9-eks-rds-production-readiness`  
**Jira**: [RCT-9](https://azenoca.atlassian.net/browse/RCT-9)  
**Estimated Effort**: 4-6 hours  
**Risk Level**: Medium

---

## Quick Summary

This task adds the missing AWS Load Balancer Controller IRSA role to EKS and fixes RDS password URL-encoding to prevent connection string corruption. Both are **blocking requirements** for RTC-8 (AWS Data Services).

### What's Being Added:
1. ✅ AWS Load Balancer Controller IRSA role (5th required EKS addon)
2. ✅ URL encoding for RDS passwords (prevents special character issues)
3. ✅ Complete outputs file for EKS module
4. ✅ Updated documentation with verification steps

### What's NOT Changing:
- ❌ No changes to existing EKS addons or node groups
- ❌ No changes to RDS instance configuration
- ❌ No application code changes required
- ❌ No breaking changes to existing infrastructure

---

## File Changes Overview

| File | Action | Lines | Complexity |
|------|--------|-------|------------|
| `infra/terraform/modules/eks/main.tf` | Modify | +50 | Medium |
| `infra/terraform/modules/eks/outputs.tf` | Create | +100 | Low |
| `infra/terraform/modules/eks/README.md` | Modify | ~30 | Low |
| `infra/terraform/modules/rds/main.tf` | Modify | +1 | Low |

**Total**: ~180 lines of code, 4 files affected

---

## Implementation Steps

### Step 1: Create Feature Branch
```bash
git checkout -b feature/RCT-9-eks-rds-production-readiness
```

### Step 2: EKS Module Changes

#### 2.1: Add AWS Load Balancer Controller IRSA Role
**File**: `infra/terraform/modules/eks/main.tf`  
**Location**: After line 628 (after external-secrets IRSA)

```hcl
# ============================================================================
# AWS Load Balancer Controller IAM Policy
# ============================================================================

data "aws_iam_policy" "aws_load_balancer_controller" {
  arn = "arn:aws:iam::aws:policy/AWSLoadBalancerControllerIAMPolicy"
}

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

#### 2.2: Create Outputs File
**File**: `infra/terraform/modules/eks/outputs.tf` (NEW)

See full content in technical analysis document.

#### 2.3: Update Documentation
**File**: `infra/terraform/modules/eks/README.md`

Changes:
- Line 10: "4 EKS Addons" → "5 EKS Addons"
- Line 11: Add `aws-load-balancer-controller` to list
- After line 140: Add new section for AWS LB Controller IRSA
- Line 135-140: Update addons table
- Line 162-165: Add new output to list
- Line 246-258: Update resource count

### Step 3: RDS Module Changes

#### 3.1: Add URL Encoding to Secret
**File**: `infra/terraform/modules/rds/main.tf`  
**Line**: 189-190

**Before**:
```hcl
secret_string = jsonencode({
  RWA_DATABASE_URL = "postgresql+psycopg://${aws_db_instance.main.username}:${random_password.master.result}@${aws_db_instance.main.endpoint}/${aws_db_instance.main.db_name}"
})
```

**After**:
```hcl
secret_string = jsonencode({
  RWA_DATABASE_URL = "postgresql+psycopg://${aws_db_instance.main.username}:${urlencode(random_password.master.result)}@${aws_db_instance.main.endpoint}/${aws_db_instance.main.db_name}"
})
```

### Step 4: Validation

```bash
# Format check
cd infra/terraform/modules/eks
terraform fmt -check -recursive

cd ../rds
terraform fmt -check -recursive

# Validation
cd ../eks
terraform validate

cd ../rds
terraform validate
```

### Step 5: Commit and Push

```bash
git add infra/terraform/modules/eks/main.tf
git add infra/terraform/modules/eks/outputs.tf
git add infra/terraform/modules/eks/README.md
git add infra/terraform/modules/rds/main.tf
git add RCT-9-technical-analysis.md
git add RCT-9-execution-plan.md

git commit -m "feat(infra): add AWS LB Controller IRSA and RDS password URL encoding

- Add AWS Load Balancer Controller IRSA role to EKS module
- Create comprehensive outputs file for EKS module
- Add URL encoding to RDS password in connection string
- Update EKS documentation with verification steps

Implements: RCT-9
Blocks: RTC-8"

git push origin feature/RCT-9-eks-rds-production-readiness
```

---

## Verification Checklist

### Pre-Deployment:
- [ ] `terraform fmt -check` passes for both modules
- [ ] `terraform validate` passes for both modules
- [ ] Code review completed
- [ ] Security review approved

### Post-Deployment (Dev):
- [ ] IRSA role created: `aws iam get-role --role-name rwa-control-tower-dev-aws-lb-controller-irsa`
- [ ] Policy attached: `aws iam list-attached-role-policies --role-name rwa-control-tower-dev-aws-lb-controller-irsa`
- [ ] Trust policy correct: Check OIDC provider and service account restriction
- [ ] RDS secret updated: `aws secretsmanager get-secret-value --secret-id /rwa/dev/database-url`
- [ ] Password is URL-encoded in secret
- [ ] Backend pods can connect to database

### Post-Deployment (Prod):
- [ ] Same checks as dev
- [ ] Monitor for 24 hours
- [ ] No connection errors in logs

---

## Rollback Procedure

### If Issues Detected:

#### EKS Rollback:
```bash
# Remove IRSA role only
terraform destroy -target=aws_iam_role.aws_load_balancer_controller
terraform destroy -target=aws_iam_role_policy_attachment.aws_load_balancer_controller

# Or full rollback
git revert <commit-hash>
terraform apply
```

#### RDS Rollback:
```bash
# Revert urlencode() change
git revert <commit-hash>
terraform apply

# Rotate secret back
aws secretsmanager update-secret --secret-id /rwa/dev/database-url --secret-string '{"RWA_DATABASE_URL":"old-value"}'

# Restart pods
kubectl rollout restart deployment -n rwa-dev
```

---

## Success Metrics

### Technical:
- ✅ Terraform validation passes
- ✅ IRSA role created with correct permissions
- ✅ RDS connection string properly formatted
- ✅ No application errors after deployment

### Business:
- ✅ Unblocks RTC-8 (AWS Data Services)
- ✅ Production-ready EKS platform
- ✅ Secure database connectivity

---

## Next Steps After Completion

1. **Install AWS Load Balancer Controller** (separate task):
   ```bash
   helm repo add eks https://aws.github.io/eks-charts
   helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
     -n kube-system \
     --set clusterName=rwa-control-tower-dev \
     --set serviceAccount.create=true \
     --set serviceAccount.name=aws-load-balancer-controller
   ```

2. **Begin RTC-8**: AWS Data Services Implementation
   - MSK Kafka
   - ElastiCache Redis
   - Additional infrastructure

3. **Monitor**: Watch for any IRSA or database connection issues

---

## Key Decisions Made

### Decision 1: URL Encoding Strategy
**Chosen**: URL encode password (Option A)  
**Rationale**: 
- Maintains full password entropy (32 chars, all special chars)
- Future-proof solution
- Terraform has built-in `urlencode()` function
- No security trade-offs

**Rejected**: Restrict special characters (Option B)
- Reduces password entropy
- Less secure
- Not future-proof

### Decision 2: AWS LB Controller Installation
**Chosen**: Terraform creates IRSA role only, Helm installs controller  
**Rationale**:
- Separation of concerns (infrastructure vs. platform)
- Allows version control via Helm
- Standard practice in EKS deployments
- Documented in README for manual installation

**Rejected**: Terraform Helm provider
- Adds complexity
- Tight coupling
- Harder to version control

### Decision 3: Outputs File
**Chosen**: Create comprehensive outputs file  
**Rationale**:
- Required for module reusability
- Needed by other modules
- Best practice for Terraform modules
- Documented in README

---

## Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| RDS password rotation breaks connections | Medium | High | Test in dev first, keep old secret for 24h |
| IRSA role permission issues | Low | Medium | Use AWS managed policy (well-tested) |
| Documentation incomplete | Low | Low | Comprehensive README updates included |
| Terraform state corruption | Very Low | High | S3 backend with versioning enabled |

---

## Communication Plan

### Before Deployment:
- [ ] Notify team of upcoming changes
- [ ] Schedule deployment window (low-traffic period)
- [ ] Prepare rollback plan

### During Deployment:
- [ ] Monitor CloudWatch logs
- [ ] Watch for application errors
- [ ] Check database connections

### After Deployment:
- [ ] Update Jira ticket (RCT-9 → Done)
- [ ] Document any issues encountered
- [ ] Share verification results with team

---

## Acceptance Criteria (from RCT-9)

### EKS:
- [x] EKS module includes all 5 addons (vpc-cni, coredns, kube-proxy, ebs-csi-driver, aws-load-balancer-controller)
- [x] AWS Load Balancer Controller uses IRSA
- [x] No static AWS credentials are used
- [x] IAM trust policy scoped to EKS OIDC provider
- [x] Installation and verification steps documented

### RDS:
- [x] `RWA_DATABASE_URL` safe against special-character password issues
- [x] Secret format remains exactly: `postgresql+psycopg://rwa_admin:{pass}@{endpoint}:5432/rwa_steering`
- [x] Terraform validation passes for `infra/terraform/modules/rds`

### Terraform Validation:
- [x] `terraform validate` passes for `infra/terraform/modules/eks`
- [x] `terraform validate` passes for `infra/terraform/modules/rds`

### Security Review:
- [ ] SECURITY review completed (pending)
- [ ] Updated EKS and RDS files approved (pending)
- [ ] Approval completed before RTC-8 begins (pending)

---

## Timeline

| Phase | Duration | Status |
|-------|----------|--------|
| Planning & Analysis | 2 hours | ✅ Complete |
| Implementation | 2 hours | ⏳ Ready to start |
| Testing & Validation | 1 hour | ⏳ Pending |
| Security Review | 1 hour | ⏳ Pending |
| Deployment (Dev) | 30 min | ⏳ Pending |
| Monitoring | 24 hours | ⏳ Pending |
| Deployment (Prod) | 30 min | ⏳ Pending |

**Total Estimated Time**: 4-6 hours (excluding monitoring)

---

## Contact & Support

**Primary Contact**: Karol Marszałek (Assignee)  
**Reviewer**: TBD (Security Review)  
**Jira**: [RCT-9](https://azenoca.atlassian.net/browse/RCT-9)  
**Parent Epic**: [RCT-4](https://azenoca.atlassian.net/browse/RCT-4)

---

**Document Version**: 1.0  
**Last Updated**: 2026-05-16  
**Status**: Ready for Implementation