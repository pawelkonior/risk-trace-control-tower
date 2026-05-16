# ============================================================================
# Environment Configuration
# ============================================================================

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod"
  }
}

variable "project_name" {
  description = "Project name for resource naming and tagging"
  type        = string
  default     = "rwa-control-tower"
}

variable "region" {
  description = "AWS region for EKS cluster deployment"
  type        = string
  default     = "eu-west-1"
}

# ============================================================================
# EKS Cluster Configuration
# ============================================================================

variable "cluster_version" {
  description = "Kubernetes version for EKS cluster"
  type        = string
  default     = "1.30"
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days for EKS control plane logs"
  type        = number
  default     = 7
}

# ============================================================================
# Networking Configuration
# ============================================================================

variable "vpc_id" {
  description = "VPC ID where EKS cluster will be deployed"
  type        = string
}

variable "private_subnet_ids" {
  description = "List of private subnet IDs for EKS worker nodes"
  type        = list(string)
  validation {
    condition     = length(var.private_subnet_ids) >= 2
    error_message = "At least 2 private subnets are required for EKS high availability"
  }
}

variable "eks_nodes_security_group_id" {
  description = "Security group ID for EKS worker nodes (from networking module)"
  type        = string
}

# ============================================================================
# Node Group Configuration
# ============================================================================

variable "system_node_instance_type" {
  description = "Instance type for system node group (platform services)"
  type        = string
  default     = "t3.medium"
}

variable "system_node_min_size" {
  description = "Minimum number of nodes in system node group"
  type        = number
  default     = 2
}

variable "system_node_max_size" {
  description = "Maximum number of nodes in system node group"
  type        = number
  default     = 5
}

variable "system_node_desired_size" {
  description = "Desired number of nodes in system node group"
  type        = number
  default     = 2
}

variable "application_node_instance_type_prod" {
  description = "Instance type for application node group in production"
  type        = string
  default     = "m6i.xlarge"
}

variable "application_node_instance_type_dev" {
  description = "Instance type for application node group in dev/staging"
  type        = string
  default     = "t3.large"
}

variable "application_node_min_size" {
  description = "Minimum number of nodes in application node group"
  type        = number
  default     = 2
}

variable "application_node_max_size" {
  description = "Maximum number of nodes in application node group"
  type        = number
  default     = 10
}

variable "application_node_desired_size" {
  description = "Desired number of nodes in application node group"
  type        = number
  default     = 2
}

# ============================================================================
# Tags
# ============================================================================

variable "tags" {
  description = "Additional tags to apply to all resources"
  type        = map(string)
  default     = {}
}