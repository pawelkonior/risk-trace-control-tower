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