# EKS Module

Terraform module for deploying Amazon EKS 1.30 cluster with IRSA (IAM Roles for Service Accounts), managed node groups, and security hardening aligned with DORA Art.6 operational resilience controls.

## Features

- **EKS 1.30 Cluster** with environment-specific API endpoint exposure
- **OIDC Provider** for IAM Roles for Service Accounts (IRSA)
- **Managed Node Groups** with security-hardened launch templates
- **5 EKS Addons** (vpc-cni, coredns, kube-proxy, aws-ebs-csi-driver, aws-load-balancer-controller)
- **4 IRSA Roles** for zero-trust secret management
- **CloudWatch Logging** for control plane audit trails
- **IMDSv2 Enforcement** on all worker nodes

## Security Controls (DORA Art.6 Compliance)

| Control | Implementation |
|---------|----------------|
| Secure IAM Federation | IRSA with OIDC provider (no static keys) |
| Restricted Secret Access | IAM policies scoped to `/rwa/{env}/*` |
| Private API (Production) | `endpoint_public_access = false` |
| Audit Logging | CloudWatch logs for API, audit, authenticator |
| Hardened Metadata Access | IMDSv2 required, no IMDSv1 fallback |
| Network Isolation | Nodes in private subnets, no public IPs |

## Usage

```hcl
module "eks" {
  source = "./modules/eks"

  environment                   = "prod"
  project_name                  = "rwa-control-tower"
  cluster_version               = "1.30"
  
  # Networking (from networking module)
  vpc_id                        = module.networking.vpc_id
  private_subnet_ids            = module.networking.private_subnet_ids
  eks_nodes_security_group_id   = module.networking.eks_nodes_security_group_id
  
  # Node group configuration
  system_node_instance_type     = "t3.medium"
  system_node_min_size          = 2
  system_node_max_size          = 5
  
  application_node_instance_type_prod = "m6i.xlarge"
  application_node_instance_type_dev  = "t3.large"
  application_node_min_size     = 2
  application_node_max_size     = 10
  
  # CloudWatch logging
  log_retention_days            = 7
  
  tags = {
    ManagedBy = "Terraform"
    Epic      = "RCT-4"
  }
}
```

## Environment-Specific Behavior

### Production
- **API Endpoint**: Private only (no public access)
- **Node Instance Type**: m6i.xlarge (4 vCPU, 16 GiB RAM)
- **Purpose**: High availability, production workloads

### Dev/Staging
- **API Endpoint**: Public + Private (developer access)
- **Node Instance Type**: t3.large (2 vCPU, 8 GiB RAM)
- **Purpose**: Cost-optimized development environment

## Node Groups

### System Node Group
- **Purpose**: Platform services (monitoring, logging, ingress controllers)
- **Instance Type**: t3.medium
- **Scaling**: Min 2, Max 5
- **Labels**: `role=system`

### Application Node Group
- **Purpose**: Application workloads (backend microservices, frontend)
- **Instance Type**: Environment-specific (see above)
- **Scaling**: Min 2, Max 10
- **Labels**: `role=application`

## IRSA Roles

### 1. rwa-backend
- **Namespace**: `rwa-{env}` (e.g., `rwa-prod`, `rwa-dev`)
- **Service Account**: `rwa-backend`
- **Permissions**: `secretsmanager:GetSecretValue`, `secretsmanager:DescribeSecret`
- **Resource Scope**: `/rwa/{env}/*`
- **Purpose**: Backend microservices access to database credentials, API keys

**Kubernetes Service Account Annotation:**
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: rwa-backend
  namespace: rwa-prod
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::ACCOUNT_ID:role/rwa-control-tower-prod-rwa-backend-irsa
```

### 2. external-secrets-sa
- **Namespace**: `external-secrets`
- **Service Account**: `external-secrets-sa`
- **Permissions**: `secretsmanager:GetSecretValue`, `secretsmanager:DescribeSecret`, `secretsmanager:ListSecrets`
- **Resource Scope**: `/rwa/{env}/*`
- **Purpose**: External Secrets Operator synchronization

**Kubernetes Service Account Annotation:**
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: external-secrets-sa
  namespace: external-secrets
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::ACCOUNT_ID:role/rwa-control-tower-prod-external-secrets-irsa
```

### 3. ebs-csi-controller-sa
- **Namespace**: `kube-system`
- **Service Account**: `ebs-csi-controller-sa`
- **Permissions**: AWS Managed Policy `AmazonEBSCSIDriverPolicy`
- **Purpose**: EBS volume provisioning and attachment

**Note**: This service account is automatically created by the `aws-ebs-csi-driver` addon.

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

## EKS Addons

| Addon | Purpose | IRSA Required | Dependencies |
|-------|---------|---------------|--------------|
| vpc-cni | Pod networking | No | None |
| coredns | DNS resolution | No | System node group |
| kube-proxy | Network proxy | No | None |
| aws-ebs-csi-driver | Persistent volumes | Yes | ebs-csi-controller-sa |
| aws-load-balancer-controller | ALB/NLB provisioning | Yes | aws-load-balancer-controller SA |

## Outputs

### Cluster Outputs
- `cluster_endpoint` - EKS API endpoint URL
- `cluster_ca` - Certificate authority data (sensitive)
- `cluster_name` - Cluster name for kubectl context
- `cluster_id` - Cluster identifier
- `cluster_arn` - Cluster ARN
- `cluster_version` - Kubernetes version

### OIDC Provider Outputs
- `oidc_provider_arn` - ARN for creating additional IRSA roles
- `oidc_provider_url` - URL without `https://` prefix
- `oidc_provider_issuer` - Full OIDC issuer URL

### Node Group Outputs
- `node_role_arn` - Worker node IAM role ARN
- `system_node_group_id` - System node group ID
- `application_node_group_id` - Application node group ID

### IRSA Role Outputs
- `rwa_backend_irsa_role_arn` - ARN for rwa-backend service account
- `external_secrets_irsa_role_arn` - ARN for external-secrets-sa
- `ebs_csi_controller_irsa_role_arn` - ARN for ebs-csi-controller-sa
- `aws_load_balancer_controller_irsa_role_arn` - ARN for aws-load-balancer-controller service account

### CloudWatch Outputs
- `cloudwatch_log_group_name` - Log group name
- `cloudwatch_log_group_arn` - Log group ARN

## Accessing the Cluster

### Configure kubectl
```bash
aws eks update-kubeconfig \
  --region eu-west-1 \
  --name rwa-control-tower-prod
```

### Verify Cluster Access
```bash
kubectl get nodes
kubectl get pods -n kube-system
```

### Verify IRSA Roles
```bash
# Check OIDC provider
aws iam list-open-id-connect-providers

# List IRSA roles
aws iam list-roles | grep irsa

# Verify service account annotation
kubectl get sa rwa-backend -n rwa-prod -o yaml
```

## Launch Template Security

All node groups use launch templates with the following security hardening:

- **AMI**: Latest EKS-optimized Amazon Linux 2
- **IMDSv2**: Required (no IMDSv1 fallback)
- **Public IP**: Disabled (nodes in private subnets)
- **Metadata Configuration**: Secure defaults
- **Instance Metadata Tags**: Enabled

## CloudWatch Logging

Control plane logs are streamed to CloudWatch with the following log types enabled:

- **API Server**: Kubernetes API server component logs
- **Audit**: Kubernetes audit logs (who did what, when)
- **Authenticator**: AWS IAM Authenticator logs

**Log Group**: `/aws/eks/{project_name}-{environment}/cluster`  
**Retention**: 7 days (configurable via `log_retention_days`)

## Validation

```bash
# Format check
terraform fmt -check -recursive

# Validation
terraform validate

# Plan
terraform plan -var-file=prod.tfvars
```

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.5 |
| aws | >= 5.0 |

## Providers

| Name | Version |
|------|---------|
| aws | >= 5.0 |
| tls | >= 4.0 |

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

## Cost Estimation

### Production Environment
- **EKS Control Plane**: $0.10/hour (~$73/month)
- **System Nodes** (2x t3.medium): ~$60/month
- **Application Nodes** (2x m6i.xlarge): ~$280/month
- **NAT Gateway**: ~$32/month (from networking module)
- **CloudWatch Logs**: ~$5/month (7-day retention)

**Estimated Total**: ~$450/month

### Dev Environment
- **EKS Control Plane**: $0.10/hour (~$73/month)
- **System Nodes** (2x t3.medium): ~$60/month
- **Application Nodes** (2x t3.large): ~$120/month
- **NAT Gateway**: ~$32/month (single NAT for cost savings)
- **CloudWatch Logs**: ~$5/month

**Estimated Total**: ~$290/month

## Troubleshooting

### Nodes Not Joining Cluster
1. Check security group rules allow node-to-control-plane communication
2. Verify IAM role has required policies attached
3. Check CloudWatch logs for authentication errors

### IRSA Not Working
1. Verify OIDC provider exists: `aws iam list-open-id-connect-providers`
2. Check service account annotation matches IAM role ARN
3. Verify IAM role trust policy references correct OIDC issuer
4. Check pod has correct service account: `kubectl get pod POD_NAME -o yaml`

### Addon Installation Fails
1. Ensure node group is healthy: `kubectl get nodes`
2. Check addon version compatibility with EKS 1.30
3. Review CloudWatch logs for addon errors
4. For EBS CSI driver, verify IRSA role exists

## References

- [AWS EKS Best Practices Guide](https://aws.github.io/aws-eks-best-practices/)
- [IRSA Documentation](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html)
- [EKS Addons](https://docs.aws.amazon.com/eks/latest/userguide/eks-add-ons.html)
- [DORA Regulation (EU 2022/2554)](https://eur-lex.europa.eu/eli/reg/2022/2554/oj)

## Related Jira Issues

- **Implements**: [RCT-6](https://azenoca.atlassian.net/browse/RCT-6) - EKS 1.30 cluster + IRSA
- **Parent Epic**: [RCT-4](https://azenoca.atlassian.net/browse/RCT-4) - AWS Platform Infrastructure & CI/CD Foundation