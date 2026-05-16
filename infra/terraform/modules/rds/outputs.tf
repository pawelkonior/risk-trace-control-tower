# ============================================================================
# RDS Instance Outputs
# ============================================================================

output "db_instance_endpoint" {
  description = "RDS instance endpoint (host:port format)"
  value       = aws_db_instance.main.endpoint
}

output "db_instance_address" {
  description = "RDS instance hostname (without port)"
  value       = aws_db_instance.main.address
}

output "db_instance_identifier" {
  description = "RDS instance identifier"
  value       = aws_db_instance.main.identifier
}

output "db_instance_arn" {
  description = "RDS instance ARN"
  value       = aws_db_instance.main.arn
}

output "db_name" {
  description = "Database name (rwa_steering)"
  value       = aws_db_instance.main.db_name
}

output "db_port" {
  description = "Database port"
  value       = aws_db_instance.main.port
}

# ============================================================================
# Parameter Group Outputs
# ============================================================================

output "parameter_group_name" {
  description = "PostgreSQL parameter group name"
  value       = aws_db_parameter_group.postgres16.name
}

output "parameter_group_id" {
  description = "PostgreSQL parameter group ID"
  value       = aws_db_parameter_group.postgres16.id
}

# ============================================================================
# Secrets Manager Outputs
# ============================================================================

output "db_secret_arn" {
  description = "Secrets Manager secret ARN for database connection URL"
  value       = aws_secretsmanager_secret.database_url.arn
}

output "db_secret_name" {
  description = "Secrets Manager secret name"
  value       = aws_secretsmanager_secret.database_url.name
}

output "db_secret_id" {
  description = "Secrets Manager secret ID"
  value       = aws_secretsmanager_secret.database_url.id
}

# ============================================================================
# Subnet Group Outputs
# ============================================================================

output "db_subnet_group_name" {
  description = "RDS subnet group name"
  value       = aws_db_subnet_group.main.name
}

output "db_subnet_group_arn" {
  description = "RDS subnet group ARN"
  value       = aws_db_subnet_group.main.arn
}

# ============================================================================
# Connection Information (Sensitive)
# ============================================================================

output "db_username" {
  description = "Database master username (rwa_admin)"
  value       = aws_db_instance.main.username
  sensitive   = true
}

output "db_password" {
  description = "Database master password (randomly generated)"
  value       = random_password.master.result
  sensitive   = true
}