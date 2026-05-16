# ============================================================================
# Data Sources
# ============================================================================

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# ============================================================================
# ECR Repositories — backend and frontend
# IMMUTABLE tags + scan_on_push (DORA Art.6)
# ============================================================================

locals {
  repositories = toset(["backend", "frontend"])
}

resource "aws_ecr_repository" "main" {
  for_each = local.repositories

  name                 = "${var.project_name}-${each.key}"
  image_tag_mutability = "IMMUTABLE" # OPA deny-latest-tag compliance

  image_scanning_configuration {
    scan_on_push = true # DORA Art.6 vulnerability gate
  }

  encryption_configuration {
    encryption_type = "KMS"
    kms_key         = var.kms_key_arn
  }

  force_delete = var.environment == "prod" ? false : true

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${each.key}"
      Environment = var.environment
      Project     = var.project_name
      Component   = each.key
    }
  )
}

# ============================================================================
# Lifecycle Policy
# - Expire untagged images after 1 day
# - Keep 10 most recent sha- tagged images
# ============================================================================

resource "aws_ecr_lifecycle_policy" "main" {
  for_each = local.repositories

  repository = aws_ecr_repository.main[each.key].name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Expire untagged images after 1 day"
        selection = {
          tagStatus   = "untagged"
          countType   = "sinceImagePushed"
          countUnit   = "days"
          countNumber = 1
        }
        action = { type = "expire" }
      },
      {
        rulePriority = 2
        description  = "Keep 10 most recent sha- tagged images"
        selection = {
          tagStatus      = "tagged"
          tagPrefixList  = ["sha-"]
          countType      = "imageCountMoreThan"
          countNumber    = 10
        }
        action = { type = "expire" }
      }
    ]
  })
}

# ============================================================================
# Repository Policy — deny image push without immutable tag enforcement
# ============================================================================

resource "aws_ecr_repository_policy" "main" {
  for_each = local.repositories

  repository = aws_ecr_repository.main[each.key].name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowAccountPull"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:BatchCheckLayerAvailability",
          "ecr:DescribeRepositories",
          "ecr:DescribeImages",
          "ecr:ListImages",
        ]
      },
      {
        Sid    = "DenyLatestTag"
        Effect = "Deny"
        Principal = "*"
        Action = [
          "ecr:PutImage",
        ]
        Condition = {
          StringLike = {
            "ecr:imageTag" = "latest"
          }
        }
      }
    ]
  })
}
