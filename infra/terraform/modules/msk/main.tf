# ============================================================================
# Data Sources
# ============================================================================

data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

# ============================================================================
# SCRAM Credentials — one secret per principal
# Path: AmazonMSK_rwa-{env}-{principal}
# (AWS SCRAM secrets must start with AmazonMSK_)
# ============================================================================

locals {
  scram_principals = toset([
    "rwa-backend",
    "rwa-worker",
    "compliance-mcp",
    "datahub-connector",
    "audit-sink",
  ])
}

resource "random_password" "scram" {
  for_each = local.scram_principals

  length  = 32
  special = true
  # Avoid characters that break SCRAM parsing
  override_special = "!#$%&*()-_=+[]{}?"
}

resource "aws_secretsmanager_secret" "scram" {
  for_each = local.scram_principals

  # AWS MSK SCRAM requirement: secret name must start with "AmazonMSK_"
  name        = "AmazonMSK_rwa-${var.environment}-${each.key}"
  description = "MSK SCRAM credentials for principal ${each.key} (${var.environment})"
  kms_key_id  = var.kms_key_arn

  recovery_window_in_days = var.environment == "prod" ? 30 : 0

  tags = merge(
    var.tags,
    {
      Name        = "AmazonMSK_rwa-${var.environment}-${each.key}"
      Environment = var.environment
      Project     = var.project_name
      Principal   = each.key
    }
  )
}

resource "aws_secretsmanager_secret_version" "scram" {
  for_each = local.scram_principals

  secret_id = aws_secretsmanager_secret.scram[each.key].id

  secret_string = jsonencode({
    username = each.key
    password = random_password.scram[each.key].result
  })

  lifecycle {
    ignore_changes = [secret_string]
  }
}

# ============================================================================
# MSK Configuration — Kafka 3.7 KRaft settings
# ============================================================================

resource "aws_msk_configuration" "main" {
  name           = "${var.project_name}-${var.environment}-kafka-config"
  description    = "Kafka 3.7 KRaft configuration for ${var.project_name} ${var.environment}"
  kafka_versions = ["3.7.x"]

  server_properties = <<-EOF
    auto.create.topics.enable=false
    default.replication.factor=${var.environment == "prod" ? 3 : 1}
    min.insync.replicas=${var.environment == "prod" ? 2 : 1}
    num.partitions=12
    log.retention.hours=168
    delete.topic.enable=true
    # KRaft mode — no ZooKeeper
    EOF
}

# ============================================================================
# MSK Cluster — Kafka 3.7, SASL/SCRAM-SHA-512 + TLS, KRaft (no ZooKeeper)
# Dev:  1 × kafka.t3.small  × 100 GB
# Prod: 3 × kafka.m5.xlarge × 1000 GB  (1 per AZ)
# ============================================================================

resource "aws_msk_cluster" "main" {
  cluster_name           = "${var.project_name}-${var.environment}"
  kafka_version          = "3.7.x"
  number_of_broker_nodes = var.environment == "prod" ? 3 : 1

  configuration_info {
    arn      = aws_msk_configuration.main.arn
    revision = aws_msk_configuration.main.latest_revision
  }

  broker_node_group_info {
    instance_type   = var.environment == "prod" ? "kafka.m5.xlarge" : "kafka.t3.small"
    client_subnets  = var.environment == "prod" ? var.database_subnet_ids : [var.database_subnet_ids[0]]
    security_groups = [var.msk_security_group_id]
    az_distribution = "DEFAULT"

    storage_info {
      ebs_storage_info {
        volume_size = var.environment == "prod" ? 1000 : 100

        provisioned_throughput {
          enabled           = var.environment == "prod" ? true : false
          volume_throughput = var.environment == "prod" ? 250 : null
        }
      }
    }
  }

  # SASL/SCRAM-SHA-512 + TLS — no plaintext
  client_authentication {
    sasl {
      scram = true
    }
    unauthenticated = false
  }

  encryption_info {
    # No plaintext broker-to-client connections
    encryption_in_transit {
      client_broker = "TLS"
      in_cluster    = true
    }
    encryption_at_rest_kms_key_arn = var.kms_key_arn
  }

  open_monitoring {
    prometheus {
      jmx_exporter {
        enabled_in_broker = true
      }
      node_exporter {
        enabled_in_broker = true
      }
    }
  }

  logging_info {
    broker_logs {
      cloudwatch_logs {
        enabled   = true
        log_group = "/aws/msk/${var.project_name}-${var.environment}"
      }
    }
  }

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-msk"
      Environment = var.environment
      Project     = var.project_name
      KafkaMode   = "KRaft"
    }
  )
}

# ============================================================================
# Associate SCRAM Secrets with MSK Cluster
# ============================================================================

resource "aws_msk_scram_secret_association" "main" {
  cluster_arn     = aws_msk_cluster.main.arn
  secret_arn_list = [for s in aws_secretsmanager_secret.scram : s.arn]

  depends_on = [aws_secretsmanager_secret_version.scram]
}

# ============================================================================
# CloudWatch Log Group for MSK
# ============================================================================

resource "aws_cloudwatch_log_group" "msk" {
  name              = "/aws/msk/${var.project_name}-${var.environment}"
  retention_in_days = 90

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-msk-logs"
      Environment = var.environment
      Project     = var.project_name
    }
  )
}
