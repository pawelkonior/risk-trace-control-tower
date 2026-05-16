output "replication_group_id" {
  description = "ElastiCache replication group ID"
  value       = aws_elasticache_replication_group.main.id
}

output "replication_group_arn" {
  description = "ElastiCache replication group ARN"
  value       = aws_elasticache_replication_group.main.arn
}

output "primary_endpoint_address" {
  description = "Redis primary endpoint address (TLS port 6380)"
  value       = aws_elasticache_replication_group.main.primary_endpoint_address
}

output "configuration_endpoint_address" {
  description = "Redis cluster configuration endpoint (cluster mode, TLS port 6380)"
  value       = aws_elasticache_replication_group.main.configuration_endpoint_address
}

output "port" {
  description = "Redis TLS port"
  value       = 6380
}

output "redis_secret_arn" {
  description = "Secrets Manager ARN for /rwa/{env}/redis-url"
  value       = aws_secretsmanager_secret.redis_url.arn
}

output "redis_secret_name" {
  description = "Secrets Manager name for /rwa/{env}/redis-url"
  value       = aws_secretsmanager_secret.redis_url.name
}

output "auth_token" {
  description = "Redis AUTH token"
  value       = random_password.auth_token.result
  sensitive   = true
}
