# ============================================================================
# S3 WORM Compliance Evidence Bucket
# COMPLIANCE mode Object Lock — never use GOVERNANCE (regulatory requirement)
# Retention: 365 days, SSE-KMS, versioning, no public access
# ============================================================================

resource "aws_s3_bucket" "compliance" {
  bucket = "${var.project_name}-compliance-evidence-${var.environment}"

  # Object Lock requires this set at bucket creation
  object_lock_enabled = true

  # Prod: never force destroy (COMPLIANCE lock prevents it anyway)
  force_destroy = false

  tags = merge(
    var.tags,
    {
      Name           = "${var.project_name}-compliance-evidence-${var.environment}"
      Environment    = var.environment
      Project        = var.project_name
      DataClass      = "REGULATORY"
      RetentionYears = "1"
      Regulation     = "BCBS239,EBA-GL,DORA-Art6"
    }
  )
}

# ============================================================================
# Versioning — required for Object Lock
# ============================================================================

resource "aws_s3_bucket_versioning" "compliance" {
  bucket = aws_s3_bucket.compliance.id

  versioning_configuration {
    status = "Enabled"
  }
}

# ============================================================================
# Server-Side Encryption — SSE-KMS
# ============================================================================

resource "aws_s3_bucket_server_side_encryption_configuration" "compliance" {
  bucket = aws_s3_bucket.compliance.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = var.kms_key_arn
    }
    bucket_key_enabled = true
  }
}

# ============================================================================
# Block ALL public access
# ============================================================================

resource "aws_s3_bucket_public_access_block" "compliance" {
  bucket = aws_s3_bucket.compliance.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# ============================================================================
# Object Lock — COMPLIANCE mode, 365-day default retention
# CRITICAL: COMPLIANCE mode cannot be shortened or removed — regulatory
# ============================================================================

resource "aws_s3_bucket_object_lock_configuration" "compliance" {
  bucket = aws_s3_bucket.compliance.id

  rule {
    default_retention {
      mode = "COMPLIANCE" # NOT GOVERNANCE — regulatory requirement
      days = 365
    }
  }

  depends_on = [aws_s3_bucket_versioning.compliance]
}

# ============================================================================
# Bucket Policy — deny delete and unencrypted uploads
# ============================================================================

resource "aws_s3_bucket_policy" "compliance" {
  bucket = aws_s3_bucket.compliance.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "DenyNonTLSRequests"
        Effect = "Deny"
        Principal = "*"
        Action    = "s3:*"
        Resource = [
          aws_s3_bucket.compliance.arn,
          "${aws_s3_bucket.compliance.arn}/*",
        ]
        Condition = {
          Bool = { "aws:SecureTransport" = "false" }
        }
      },
      {
        Sid    = "DenyUnencryptedObjectUploads"
        Effect = "Deny"
        Principal = "*"
        Action    = "s3:PutObject"
        Resource  = "${aws_s3_bucket.compliance.arn}/*"
        Condition = {
          StringNotEquals = {
            "s3:x-amz-server-side-encryption" = "aws:kms"
          }
        }
      }
    ]
  })

  depends_on = [aws_s3_bucket_public_access_block.compliance]
}
