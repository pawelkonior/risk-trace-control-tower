# ============================================================================
# Random Password Generation
# ============================================================================

resource "random_password" "master" {
  length  = 32
  special = true
  # Use characters safe for PostgreSQL and URL encoding
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

# ============================================================================
# DB Subnet Group
# ============================================================================

resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-${var.environment}-rds-subnet-group"
  subnet_ids = var.database_subnet_ids

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-rds-subnet-group"
      Environment = var.environment
      Project     = var.project_name
    }
  )
}

# ============================================================================
# DB Parameter Group - PostgreSQL 16
# ============================================================================

resource "aws_db_parameter_group" "postgres16" {
  name_prefix = "${var.project_name}-${var.environment}-postgres16-"
  family      = "postgres16"
  description = "Custom parameter group for PostgreSQL 16 with SSL enforcement and pgaudit"

  # SSL Enforcement - CRITICAL REQUIREMENT
  parameter {
    name  = "rds.force_ssl"
    value = "1"
  }

  # Connection Logging - Audit Requirement
  parameter {
    name  = "log_connections"
    value = "1"
  }

  # Enable pgaudit extension - CRITICAL REQUIREMENT
  parameter {
    name  = "shared_preload_libraries"
    value = "pgaudit"
  }

  # pgaudit DDL logging - CRITICAL REQUIREMENT
  parameter {
    name  = "pgaudit.log"
    value = "ddl"
  }

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-postgres16-params"
      Environment = var.environment
      Project     = var.project_name
    }
  )

  lifecycle {
    create_before_destroy = true
  }
}

# ============================================================================
# RDS Instance - PostgreSQL 16.2
# ============================================================================

resource "aws_db_instance" "main" {
  # Instance Identification
  identifier = "${var.project_name}-${var.environment}-postgres"

  # Engine Configuration - CRITICAL REQUIREMENTS
  engine         = "postgres"
  engine_version = "16.2"

  # Instance Sizing - Environment-Specific
  instance_class = var.environment == "prod" ? "db.m6g.xlarge" : "db.t3.medium"

  # Database Configuration - CRITICAL REQUIREMENTS
  db_name  = "rwa_steering" # NOT rwa_db
  username = "rwa_admin"
  password = random_password.master.result

  # Storage Configuration
  allocated_storage     = var.allocated_storage
  max_allocated_storage = var.max_allocated_storage
  storage_type          = "gp3"
  storage_encrypted     = true
  kms_key_id            = var.kms_key_arn

  # High Availability - Environment-Specific
  multi_az = var.environment == "prod" ? true : false

  # Backup Configuration - Environment-Specific
  backup_retention_period = var.environment == "prod" ? 30 : 7
  backup_window           = var.backup_window
  maintenance_window      = var.maintenance_window

  # Deletion Protection - Production Only
  deletion_protection       = var.environment == "prod" ? true : false
  skip_final_snapshot       = var.environment == "prod" ? false : true
  final_snapshot_identifier = var.environment == "prod" ? "${var.project_name}-${var.environment}-final-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}" : null

  # Network Configuration - CRITICAL REQUIREMENT
  publicly_accessible    = false
  vpc_security_group_ids = [var.rds_security_group_id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  # Parameter Group
  parameter_group_name = aws_db_parameter_group.postgres16.name

  # CloudWatch Logs
  enabled_cloudwatch_logs_exports = var.enabled_cloudwatch_logs_exports

  # Performance Insights
  performance_insights_enabled    = var.environment == "prod" ? true : false
  performance_insights_kms_key_id = var.environment == "prod" ? var.kms_key_arn : null

  # Auto Minor Version Upgrade
  auto_minor_version_upgrade = false

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-postgres"
      Environment = var.environment
      Project     = var.project_name
      Engine      = "postgres"
      Version     = "16.2"
    }
  )

  lifecycle {
    ignore_changes = [
      # Ignore password changes after initial creation
      password,
      # Ignore final snapshot identifier timestamp
      final_snapshot_identifier
    ]
  }
}

# ============================================================================
# Secrets Manager Secret
# ============================================================================

resource "aws_secretsmanager_secret" "database_url" {
  name        = "/rwa/${var.environment}/database-url"
  description = "PostgreSQL connection URL for RWA backend services (${var.environment})"
  kms_key_id  = var.kms_key_arn

  # Recovery window - Production has 30 days, dev can be immediate
  recovery_window_in_days = var.environment == "prod" ? 30 : 0

  tags = merge(
    var.tags,
    {
      Name        = "/rwa/${var.environment}/database-url"
      Environment = var.environment
      Project     = var.project_name
      Purpose     = "RDS connection string"
    }
  )
}

# ============================================================================
# Secrets Manager Secret Version
# ============================================================================

resource "aws_secretsmanager_secret_version" "database_url" {
  secret_id = aws_secretsmanager_secret.database_url.id

  # CRITICAL REQUIREMENT: Key must be RWA_DATABASE_URL (NOT DATABASE_URL)
  # CRITICAL REQUIREMENT: Driver must be psycopg (NOT asyncpg)
  # Format: postgresql+psycopg://rwa_admin:{password}@{endpoint}/rwa_steering
  secret_string = jsonencode({
    RWA_DATABASE_URL = "postgresql+psycopg://${aws_db_instance.main.username}:${random_password.master.result}@${aws_db_instance.main.endpoint}/${aws_db_instance.main.db_name}"
  })

  lifecycle {
    ignore_changes = [
      # Ignore secret string changes to prevent drift from password rotation
      secret_string
    ]
  }
}