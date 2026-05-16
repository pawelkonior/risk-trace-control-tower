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

variable "vpc_id" {
  description = "VPC ID for ElastiCache subnet group"
  type        = string
}

variable "database_subnet_ids" {
  description = "Subnet IDs for ElastiCache subnet group"
  type        = list(string)
  validation {
    condition     = length(var.database_subnet_ids) >= 2
    error_message = "At least 2 subnets required"
  }
}

variable "redis_security_group_id" {
  description = "Security group ID for ElastiCache Redis (from networking module)"
  type        = string
}

variable "kms_key_arn" {
  description = "KMS key ARN for at-rest encryption"
  type        = string
}

variable "tags" {
  description = "Additional tags to apply to all resources"
  type        = map(string)
  default     = {}
}
