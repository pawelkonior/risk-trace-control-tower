# ============================================================================
# Data Sources
# ============================================================================

# Latest EKS-optimized Amazon Linux 2 AMI
data "aws_ami" "eks_node" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amazon-eks-node-${var.cluster_version}-*"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
}

# Current AWS account ID and region
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# OIDC thumbprint for EKS
data "tls_certificate" "cluster" {
  url = aws_eks_cluster.main.identity[0].oidc[0].issuer
}

# ============================================================================
# CloudWatch Log Group
# ============================================================================

resource "aws_cloudwatch_log_group" "eks_cluster" {
  name              = "/aws/eks/${var.project_name}-${var.environment}/cluster"
  retention_in_days = var.log_retention_days

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-eks-logs"
      Environment = var.environment
      Project     = var.project_name
    }
  )
}

# ============================================================================
# EKS Cluster IAM Role
# ============================================================================

resource "aws_iam_role" "cluster" {
  name = "${var.project_name}-${var.environment}-eks-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "eks.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-eks-cluster-role"
      Environment = var.environment
      Project     = var.project_name
    }
  )
}

resource "aws_iam_role_policy_attachment" "cluster_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.cluster.name
}

resource "aws_iam_role_policy_attachment" "cluster_vpc_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSVPCResourceController"
  role       = aws_iam_role.cluster.name
}

# ============================================================================
# EKS Cluster
# ============================================================================

resource "aws_eks_cluster" "main" {
  name     = "${var.project_name}-${var.environment}"
  version  = var.cluster_version
  role_arn = aws_iam_role.cluster.arn

  vpc_config {
    subnet_ids              = var.private_subnet_ids
    endpoint_private_access = true
    endpoint_public_access  = var.environment == "prod" ? false : true
    security_group_ids      = [var.eks_nodes_security_group_id]
  }

  enabled_cluster_log_types = ["api", "audit", "authenticator"]

  depends_on = [
    aws_cloudwatch_log_group.eks_cluster,
    aws_iam_role_policy_attachment.cluster_policy,
    aws_iam_role_policy_attachment.cluster_vpc_policy
  ]

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-eks"
      Environment = var.environment
      Project     = var.project_name
    }
  )
}

# ============================================================================
# OIDC Provider for IRSA
# ============================================================================

resource "aws_iam_openid_connect_provider" "cluster" {
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [data.tls_certificate.cluster.certificates[0].sha1_fingerprint]
  url             = aws_eks_cluster.main.identity[0].oidc[0].issuer

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-eks-oidc"
      Environment = var.environment
      Project     = var.project_name
    }
  )
}

# ============================================================================
# Node Group IAM Role
# ============================================================================

resource "aws_iam_role" "node_group" {
  name = "${var.project_name}-${var.environment}-eks-node-group-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-eks-node-group-role"
      Environment = var.environment
      Project     = var.project_name
    }
  )
}

resource "aws_iam_role_policy_attachment" "node_group_worker_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.node_group.name
}

resource "aws_iam_role_policy_attachment" "node_group_cni_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.node_group.name
}

resource "aws_iam_role_policy_attachment" "node_group_registry_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.node_group.name
}

# ============================================================================
# Launch Template - System Node Group
# ============================================================================

resource "aws_launch_template" "system" {
  name_prefix = "${var.project_name}-${var.environment}-system-"
  image_id    = data.aws_ami.eks_node.id

  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required" # IMDSv2 only
    http_put_response_hop_limit = 1
    instance_metadata_tags      = "enabled"
  }

  network_interfaces {
    associate_public_ip_address = false
    delete_on_termination       = true
    security_groups             = [var.eks_nodes_security_group_id]
  }

  tag_specifications {
    resource_type = "instance"
    tags = merge(
      var.tags,
      {
        Name        = "${var.project_name}-${var.environment}-system-node"
        Environment = var.environment
        Project     = var.project_name
        NodeGroup   = "system"
      }
    )
  }

  tag_specifications {
    resource_type = "volume"
    tags = merge(
      var.tags,
      {
        Name        = "${var.project_name}-${var.environment}-system-node-volume"
        Environment = var.environment
        Project     = var.project_name
        NodeGroup   = "system"
      }
    )
  }

  lifecycle {
    create_before_destroy = true
  }
}

# ============================================================================
# Launch Template - Application Node Group
# ============================================================================

resource "aws_launch_template" "application" {
  name_prefix = "${var.project_name}-${var.environment}-application-"
  image_id    = data.aws_ami.eks_node.id

  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required" # IMDSv2 only
    http_put_response_hop_limit = 1
    instance_metadata_tags      = "enabled"
  }

  network_interfaces {
    associate_public_ip_address = false
    delete_on_termination       = true
    security_groups             = [var.eks_nodes_security_group_id]
  }

  tag_specifications {
    resource_type = "instance"
    tags = merge(
      var.tags,
      {
        Name        = "${var.project_name}-${var.environment}-application-node"
        Environment = var.environment
        Project     = var.project_name
        NodeGroup   = "application"
      }
    )
  }

  tag_specifications {
    resource_type = "volume"
    tags = merge(
      var.tags,
      {
        Name        = "${var.project_name}-${var.environment}-application-node-volume"
        Environment = var.environment
        Project     = var.project_name
        NodeGroup   = "application"
      }
    )
  }

  lifecycle {
    create_before_destroy = true
  }
}

# ============================================================================
# Managed Node Group - System
# ============================================================================

resource "aws_eks_node_group" "system" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "system"
  node_role_arn   = aws_iam_role.node_group.arn
  subnet_ids      = var.private_subnet_ids

  scaling_config {
    desired_size = var.system_node_desired_size
    min_size     = var.system_node_min_size
    max_size     = var.system_node_max_size
  }

  instance_types = [var.system_node_instance_type]

  launch_template {
    id      = aws_launch_template.system.id
    version = "$Latest"
  }

  labels = {
    role        = "system"
    environment = var.environment
  }

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-system-ng"
      Environment = var.environment
      Project     = var.project_name
      NodeGroup   = "system"
    }
  )

  depends_on = [
    aws_iam_role_policy_attachment.node_group_worker_policy,
    aws_iam_role_policy_attachment.node_group_cni_policy,
    aws_iam_role_policy_attachment.node_group_registry_policy
  ]

  lifecycle {
    create_before_destroy = true
    ignore_changes        = [scaling_config[0].desired_size]
  }
}

# ============================================================================
# Managed Node Group - Application
# ============================================================================

resource "aws_eks_node_group" "application" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "application"
  node_role_arn   = aws_iam_role.node_group.arn
  subnet_ids      = var.private_subnet_ids

  scaling_config {
    desired_size = var.application_node_desired_size
    min_size     = var.application_node_min_size
    max_size     = var.application_node_max_size
  }

  instance_types = [
    var.environment == "prod" ? var.application_node_instance_type_prod : var.application_node_instance_type_dev
  ]

  launch_template {
    id      = aws_launch_template.application.id
    version = "$Latest"
  }

  labels = {
    role        = "application"
    environment = var.environment
  }

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-application-ng"
      Environment = var.environment
      Project     = var.project_name
      NodeGroup   = "application"
    }
  )

  depends_on = [
    aws_iam_role_policy_attachment.node_group_worker_policy,
    aws_iam_role_policy_attachment.node_group_cni_policy,
    aws_iam_role_policy_attachment.node_group_registry_policy
  ]

  lifecycle {
    create_before_destroy = true
    ignore_changes        = [scaling_config[0].desired_size]
  }
}

# ============================================================================
# EKS Addon - VPC CNI
# ============================================================================

resource "aws_eks_addon" "vpc_cni" {
  cluster_name = aws_eks_cluster.main.name
  addon_name   = "vpc-cni"

  resolve_conflicts_on_create = "OVERWRITE"
  resolve_conflicts_on_update = "PRESERVE"

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-vpc-cni"
      Environment = var.environment
      Project     = var.project_name
    }
  )
}

# ============================================================================
# EKS Addon - CoreDNS
# ============================================================================

resource "aws_eks_addon" "coredns" {
  cluster_name = aws_eks_cluster.main.name
  addon_name   = "coredns"

  resolve_conflicts_on_create = "OVERWRITE"
  resolve_conflicts_on_update = "PRESERVE"

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-coredns"
      Environment = var.environment
      Project     = var.project_name
    }
  )

  depends_on = [
    aws_eks_node_group.system
  ]
}

# ============================================================================
# EKS Addon - kube-proxy
# ============================================================================

resource "aws_eks_addon" "kube_proxy" {
  cluster_name = aws_eks_cluster.main.name
  addon_name   = "kube-proxy"

  resolve_conflicts_on_create = "OVERWRITE"
  resolve_conflicts_on_update = "PRESERVE"

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-kube-proxy"
      Environment = var.environment
      Project     = var.project_name
    }
  )
}

# ============================================================================
# IRSA Role - EBS CSI Controller
# ============================================================================

resource "aws_iam_role" "ebs_csi_controller" {
  name = "${var.project_name}-${var.environment}-ebs-csi-controller-irsa"

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
          "${replace(aws_iam_openid_connect_provider.cluster.url, "https://", "")}:sub" = "system:serviceaccount:kube-system:ebs-csi-controller-sa"
          "${replace(aws_iam_openid_connect_provider.cluster.url, "https://", "")}:aud" = "sts.amazonaws.com"
        }
      }
    }]
  })

  tags = merge(
    var.tags,
    {
      Name           = "${var.project_name}-${var.environment}-ebs-csi-controller-irsa"
      Environment    = var.environment
      Project        = var.project_name
      ServiceAccount = "ebs-csi-controller-sa"
      Namespace      = "kube-system"
    }
  )
}

resource "aws_iam_role_policy_attachment" "ebs_csi_controller_policy" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy"
  role       = aws_iam_role.ebs_csi_controller.name
}

# ============================================================================
# EKS Addon - EBS CSI Driver
# ============================================================================

resource "aws_eks_addon" "ebs_csi_driver" {
  cluster_name             = aws_eks_cluster.main.name
  addon_name               = "aws-ebs-csi-driver"
  service_account_role_arn = aws_iam_role.ebs_csi_controller.arn

  resolve_conflicts_on_create = "OVERWRITE"
  resolve_conflicts_on_update = "PRESERVE"

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-ebs-csi-driver"
      Environment = var.environment
      Project     = var.project_name
    }
  )

  depends_on = [
    aws_iam_role.ebs_csi_controller,
    aws_eks_node_group.system
  ]
}

# ============================================================================
# IRSA Role - rwa-backend
# ============================================================================

resource "aws_iam_role" "rwa_backend" {
  name = "${var.project_name}-${var.environment}-rwa-backend-irsa"

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
          "${replace(aws_iam_openid_connect_provider.cluster.url, "https://", "")}:sub" = "system:serviceaccount:rwa-${var.environment}:rwa-backend"
          "${replace(aws_iam_openid_connect_provider.cluster.url, "https://", "")}:aud" = "sts.amazonaws.com"
        }
      }
    }]
  })

  tags = merge(
    var.tags,
    {
      Name           = "${var.project_name}-${var.environment}-rwa-backend-irsa"
      Environment    = var.environment
      Project        = var.project_name
      ServiceAccount = "rwa-backend"
      Namespace      = "rwa-${var.environment}"
    }
  )
}

resource "aws_iam_role_policy" "rwa_backend_secrets" {
  name = "secrets-manager-access"
  role = aws_iam_role.rwa_backend.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret"
      ]
      Resource = "arn:aws:secretsmanager:${data.aws_region.current.id}:${data.aws_caller_identity.current.account_id}:secret:/rwa/${var.environment}/*"
    }]
  })
}

# ============================================================================
# IRSA Role - external-secrets-sa
# ============================================================================

resource "aws_iam_role" "external_secrets" {
  name = "${var.project_name}-${var.environment}-external-secrets-irsa"

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
          "${replace(aws_iam_openid_connect_provider.cluster.url, "https://", "")}:sub" = "system:serviceaccount:external-secrets:external-secrets-sa"
          "${replace(aws_iam_openid_connect_provider.cluster.url, "https://", "")}:aud" = "sts.amazonaws.com"
        }
      }
    }]
  })

  tags = merge(
    var.tags,
    {
      Name           = "${var.project_name}-${var.environment}-external-secrets-irsa"
      Environment    = var.environment
      Project        = var.project_name
      ServiceAccount = "external-secrets-sa"
      Namespace      = "external-secrets"
    }
  )
}

resource "aws_iam_role_policy" "external_secrets_secrets" {
  name = "secrets-manager-access"
  role = aws_iam_role.external_secrets.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret",
        "secretsmanager:ListSecrets"
      ]
      Resource = "arn:aws:secretsmanager:${data.aws_region.current.id}:${data.aws_caller_identity.current.account_id}:secret:/rwa/${var.environment}/*"
    }]
  })
}