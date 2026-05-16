# ============================================================================
# EKS Cluster Outputs
# ============================================================================

output "cluster_endpoint" {
  description = "EKS cluster API endpoint URL"
  value       = aws_eks_cluster.main.endpoint
}

output "cluster_ca" {
  description = "EKS cluster certificate authority data (base64 encoded)"
  value       = aws_eks_cluster.main.certificate_authority[0].data
  sensitive   = true
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

output "cluster_security_group_id" {
  description = "Security group ID attached to the EKS cluster"
  value       = aws_eks_cluster.main.vpc_config[0].cluster_security_group_id
}

# ============================================================================
# OIDC Provider Outputs
# ============================================================================

output "oidc_provider_arn" {
  description = "ARN of the OIDC provider for IRSA"
  value       = aws_iam_openid_connect_provider.cluster.arn
}

output "oidc_provider_url" {
  description = "URL of the OIDC provider (without https:// prefix)"
  value       = replace(aws_iam_openid_connect_provider.cluster.url, "https://", "")
}

output "oidc_provider_issuer" {
  description = "Full OIDC provider issuer URL"
  value       = aws_eks_cluster.main.identity[0].oidc[0].issuer
}

# ============================================================================
# Node Group Outputs
# ============================================================================

output "node_role_arn" {
  description = "IAM role ARN for EKS worker nodes"
  value       = aws_iam_role.node_group.arn
}

output "node_role_name" {
  description = "IAM role name for EKS worker nodes"
  value       = aws_iam_role.node_group.name
}

output "system_node_group_id" {
  description = "System node group ID"
  value       = aws_eks_node_group.system.id
}

output "system_node_group_status" {
  description = "System node group status"
  value       = aws_eks_node_group.system.status
}

output "application_node_group_id" {
  description = "Application node group ID"
  value       = aws_eks_node_group.application.id
}

output "application_node_group_status" {
  description = "Application node group status"
  value       = aws_eks_node_group.application.status
}

# ============================================================================
# IRSA Role Outputs
# ============================================================================

output "rwa_backend_irsa_role_arn" {
  description = "IAM role ARN for rwa-backend service account (namespace: rwa-{env})"
  value       = aws_iam_role.rwa_backend.arn
}

output "rwa_backend_irsa_role_name" {
  description = "IAM role name for rwa-backend service account"
  value       = aws_iam_role.rwa_backend.name
}

output "external_secrets_irsa_role_arn" {
  description = "IAM role ARN for external-secrets-sa service account (namespace: external-secrets)"
  value       = aws_iam_role.external_secrets.arn
}

output "external_secrets_irsa_role_name" {
  description = "IAM role name for external-secrets-sa service account"
  value       = aws_iam_role.external_secrets.name
}

output "ebs_csi_controller_irsa_role_arn" {
  description = "IAM role ARN for ebs-csi-controller-sa service account (namespace: kube-system)"
  value       = aws_iam_role.ebs_csi_controller.arn
}

output "ebs_csi_controller_irsa_role_name" {
  description = "IAM role name for ebs-csi-controller-sa service account"
  value       = aws_iam_role.ebs_csi_controller.name
}

# ============================================================================
# EKS Addon Outputs
# ============================================================================

output "vpc_cni_addon_version" {
  description = "Version of vpc-cni addon"
  value       = aws_eks_addon.vpc_cni.addon_version
}

output "coredns_addon_version" {
  description = "Version of coredns addon"
  value       = aws_eks_addon.coredns.addon_version
}

output "kube_proxy_addon_version" {
  description = "Version of kube-proxy addon"
  value       = aws_eks_addon.kube_proxy.addon_version
}

output "ebs_csi_driver_addon_version" {
  description = "Version of aws-ebs-csi-driver addon"
  value       = aws_eks_addon.ebs_csi_driver.addon_version
}

# ============================================================================
# CloudWatch Outputs
# ============================================================================

output "cloudwatch_log_group_name" {
  description = "CloudWatch log group name for EKS control plane logs"
  value       = aws_cloudwatch_log_group.eks_cluster.name
}

output "cloudwatch_log_group_arn" {
  description = "CloudWatch log group ARN for EKS control plane logs"
  value       = aws_cloudwatch_log_group.eks_cluster.arn
}