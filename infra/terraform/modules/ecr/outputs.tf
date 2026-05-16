output "repository_urls" {
  description = "Map of component name → ECR repository URL"
  value       = { for k, r in aws_ecr_repository.main : k => r.repository_url }
}

output "repository_arns" {
  description = "Map of component name → ECR repository ARN"
  value       = { for k, r in aws_ecr_repository.main : k => r.arn }
}

output "registry_id" {
  description = "ECR registry ID (AWS account ID)"
  value       = values(aws_ecr_repository.main)[0].registry_id
}

output "backend_repository_url" {
  description = "ECR URL for backend image"
  value       = aws_ecr_repository.main["backend"].repository_url
}

output "frontend_repository_url" {
  description = "ECR URL for frontend image"
  value       = aws_ecr_repository.main["frontend"].repository_url
}
