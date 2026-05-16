# ============================================================================
# AUTH Token — stored in Secrets Manager at /rwa/{env}/redis-url
# ============================================================================

resource "random_password" "auth_token" {
  length  = 32
  special = false # ElastiCache AUTH token: alphanumeric only
}

# ============================================================================
# Subnet Group
# ============================================================================

resource "aws_elasticache_subnet_group" "main" {
  name       = "${var.project_name}-${var.environment}-redis"
  subnet_ids = var.database_subnet_ids

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-redis-subnet-group"
      Environment = var.environment
      Project     = var.project_name
    }
  )
}

# ============================================================================
# Redis 7.2 Replication Group
# Dev:  1 shard × 1 primary  (cache.t3.micro)
# Prod: 3 shards × 2 replicas (cache.m6g.large)
# ============================================================================

resource "aws_elasticache_replication_group" "main" {
  replication_group_id = "${var.project_name}-${var.environment}"
  description          = "Redis 7.2 for ${var.project_name} ${var.environment}"

  engine         = "redis"
  engine_version = "7.2"
  node_type      = var.environment == "prod" ? "cache.m6g.large" : "cache.t3.micro"
  port           = 6380 # TLS port

  # Cluster mode: prod=3 shards×2 replicas, dev=1 shard×0 replicas
  num_node_groups         = var.environment == "prod" ? 3 : 1
  replicas_per_node_group = var.environment == "prod" ? 2 : 0

  # TLS in-transit — required, COMPLIANCE mode (no plaintext)
  transit_encryption_enabled = true
  transit_encryption_mode    = "required"

  # AUTH token
  auth_token                 = random_password.auth_token.result
  auth_token_update_strategy = "ROTATE"

  # Encryption at rest
  at_rest_encryption_enabled = true
  kms_key_id                 = var.kms_key_arn

  # Failover requires multiple nodes
  automatic_failover_enabled = var.environment == "prod" ? true : false
  multi_az_enabled           = var.environment == "prod" ? true : false

  # Snapshots — 3 days per spec
  snapshot_retention_limit = 3
  snapshot_window          = "03:00-04:00"

  # Network
  subnet_group_name  = aws_elasticache_subnet_group.main.name
  security_group_ids = [var.redis_security_group_id]

  # Auto minor version upgrades off — explicit control
  auto_minor_version_upgrade = false

  maintenance_window = "sun:04:00-sun:05:00"

  apply_immediately = var.environment == "prod" ? false : true

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-redis"
      Environment = var.environment
      Project     = var.project_name
      Engine      = "redis"
      Version     = "7.2"
    }
  )

  lifecycle {
    ignore_changes = [auth_token]
  }
}

# ============================================================================
# Secrets Manager — /rwa/{env}/redis-url
# ============================================================================

resource "aws_secretsmanager_secret" "redis_url" {
  name        = "/rwa/${var.environment}/redis-url"
  description = "Redis TLS connection URL for ${var.project_name} ${var.environment}"
  kms_key_id  = var.kms_key_arn

  recovery_window_in_days = var.environment == "prod" ? 30 : 0

  tags = merge(
    var.tags,
    {
      Name        = "/rwa/${var.environment}/redis-url"
      Environment = var.environment
      Project     = var.project_name
    }
  )
}

resource "aws_secretsmanager_secret_version" "redis_url" {
  secret_id = aws_secretsmanager_secret.redis_url.id

  secret_string = jsonencode({
    REDIS_URL = "rediss://:${random_password.auth_token.result}@${aws_elasticache_replication_group.main.primary_endpoint_address}:6380"
  })

  lifecycle {
    ignore_changes = [secret_string]
  }
}
