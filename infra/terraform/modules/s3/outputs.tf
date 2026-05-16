output "bucket_id" {
  description = "Compliance evidence bucket name"
  value       = aws_s3_bucket.compliance.id
}

output "bucket_arn" {
  description = "Compliance evidence bucket ARN"
  value       = aws_s3_bucket.compliance.arn
}

output "bucket_domain_name" {
  description = "Compliance evidence bucket regional domain name"
  value       = aws_s3_bucket.compliance.bucket_regional_domain_name
}

output "object_lock_enabled" {
  description = "Confirms Object Lock is enabled on this bucket"
  value       = aws_s3_bucket.compliance.object_lock_enabled
}
