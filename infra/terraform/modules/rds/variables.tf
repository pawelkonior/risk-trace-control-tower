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
  description = "AWS region for RDS deployment"
  type        = string
  default     = "eu-west-1"
}

# ============================================================================
# Networking Configuration
# ============================================================================

variable "vpc_id" {
  description = "VPC ID where RDS instance will be deployed"
  type        = string
}

variable "database_subnet_ids" {
  description = "List of database subnet IDs for RDS subnet group"
  type        = list(string)
  validation {
    condition     = length(var.database_subnet_ids) >= 2
    error_message = "At least 2 database subnets are required for RDS high availability"
  }
}

variable "rds_security_group_id" {
  description = "Security group ID for RDS instance (from networking module)"
  type        = string
}

# ============================================================================
# Encryption Configuration
# ============================================================================

variable "kms_key_arn" {
  description = "KMS key ARN for RDS storage encryption and Secrets Manager"
  type        = string
}

# ============================================================================
# RDS Instance Configuration
# ============================================================================

variable "allocated_storage" {
  description = "Initial allocated storage in GB"
  type        = number
  default     = 100
}

variable "max_allocated_storage" {
  description = "Maximum storage for autoscaling in GB"
  type        = number
  default     = 1000
}

variable "backup_window" {
  description = "Preferred backup window (UTC)"
  type        = string
  default     = "03:00-04:00"
}

variable "maintenance_window" {
  description = "Preferred maintenance window (UTC)"
  type        = string
  default     = "sun:04:00-sun:05:00"
}

variable "enabled_cloudwatch_logs_exports" {
  description = "List of log types to export to CloudWatch"
  type        = list(string)
  default     = ["postgresql", "upgrade"]
}

# ============================================================================
# Tags
# ============================================================================

variable "tags" {
  description = "Additional tags to apply to all resources"
  type        = map(string)
  default     = {}
}