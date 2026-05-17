terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "eu-west-1"

  default_tags {
    tags = local.common_tags
  }
}

locals {
  environment  = "prod"
  project_name = "rwa-control-tower"

  common_tags = {
    Environment = local.environment
    Project     = local.project_name
    ManagedBy   = "terraform"
    Regulatory  = "BCBS239,EBA-GL,DORA-Art6"
  }
}

# ============================================================================
# KMS Key — shared encryption key for all services
# ============================================================================

resource "aws_kms_key" "main" {
  description             = "RWA Control Tower ${local.environment} encryption key"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  tags = {
    Name = "${local.project_name}-${local.environment}-kms"
  }
}

resource "aws_kms_alias" "main" {
  name          = "alias/${local.project_name}-${local.environment}"
  target_key_id = aws_kms_key.main.key_id
}

# ============================================================================
# Networking
# ============================================================================

module "networking" {
  source = "../../modules/networking"

  environment  = local.environment
  project_name = local.project_name

  vpc_cidr              = "10.1.0.0/16"
  availability_zones    = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]
  public_subnet_cidrs   = ["10.1.1.0/24", "10.1.2.0/24", "10.1.3.0/24"]
  private_subnet_cidrs  = ["10.1.11.0/24", "10.1.12.0/24", "10.1.13.0/24"]
  database_subnet_cidrs = ["10.1.21.0/24", "10.1.22.0/24", "10.1.23.0/24"]

  single_nat_gateway = false # One NAT GW per AZ for HA

  tags = local.common_tags
}

# ============================================================================
# EKS
# ============================================================================

module "eks" {
  source = "../../modules/eks"

  environment  = local.environment
  project_name = local.project_name

  cluster_version             = "1.31"
  vpc_id                      = module.networking.vpc_id
  private_subnet_ids          = module.networking.private_subnet_ids
  eks_nodes_security_group_id = module.networking.eks_nodes_security_group_id

  system_node_instance_type = "t3.medium"
  system_node_desired_size  = 3
  system_node_min_size      = 3
  system_node_max_size      = 6

  application_node_instance_type_dev  = "t3.large"
  application_node_instance_type_prod = "m5.xlarge"
  application_node_desired_size       = 3
  application_node_min_size           = 3
  application_node_max_size           = 30

  log_retention_days = 365

  tags = local.common_tags
}

# ============================================================================
# RDS
# ============================================================================

module "rds" {
  source = "../../modules/rds"

  environment  = local.environment
  project_name = local.project_name

  vpc_id                = module.networking.vpc_id
  database_subnet_ids   = module.networking.database_subnet_ids
  rds_security_group_id = module.networking.rds_security_group_id
  kms_key_arn           = aws_kms_key.main.arn

  allocated_storage     = 500
  max_allocated_storage = 2000

  tags = local.common_tags
}

# ============================================================================
# ElastiCache Redis 7.2
# ============================================================================

module "elasticache" {
  source = "../../modules/elasticache"

  environment  = local.environment
  project_name = local.project_name

  vpc_id                  = module.networking.vpc_id
  database_subnet_ids     = module.networking.database_subnet_ids
  redis_security_group_id = module.networking.redis_security_group_id
  kms_key_arn             = aws_kms_key.main.arn

  tags = local.common_tags
}

# ============================================================================
# MSK Kafka 3.7
# ============================================================================

module "msk" {
  source = "../../modules/msk"

  environment  = local.environment
  project_name = local.project_name

  database_subnet_ids   = module.networking.database_subnet_ids
  msk_security_group_id = module.networking.msk_security_group_id
  kms_key_arn           = aws_kms_key.main.arn

  tags = local.common_tags
}

# ============================================================================
# ECR
# ============================================================================

module "ecr" {
  source = "../../modules/ecr"

  environment  = local.environment
  project_name = local.project_name
  kms_key_arn  = aws_kms_key.main.arn

  tags = local.common_tags
}

# ============================================================================
# S3 WORM Compliance Evidence Bucket
# ============================================================================

module "s3_compliance" {
  source = "../../modules/s3"

  environment  = local.environment
  project_name = local.project_name
  kms_key_arn  = aws_kms_key.main.arn

  tags = local.common_tags
}
