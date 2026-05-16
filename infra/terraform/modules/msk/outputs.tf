output "cluster_arn" {
  description = "MSK cluster ARN"
  value       = aws_msk_cluster.main.arn
}

output "cluster_name" {
  description = "MSK cluster name"
  value       = aws_msk_cluster.main.cluster_name
}

output "bootstrap_brokers_sasl_scram" {
  description = "SASL/SCRAM bootstrap broker endpoints (TLS)"
  value       = aws_msk_cluster.main.bootstrap_brokers_sasl_scram
}

output "bootstrap_brokers_tls" {
  description = "TLS bootstrap broker endpoints"
  value       = aws_msk_cluster.main.bootstrap_brokers_tls
}

output "zookeeper_connect_string" {
  description = "ZooKeeper connect string (empty for KRaft clusters)"
  value       = aws_msk_cluster.main.zookeeper_connect_string
}

output "scram_secret_arns" {
  description = "Map of principal name → Secrets Manager secret ARN"
  value       = { for k, s in aws_secretsmanager_secret.scram : k => s.arn }
}

output "scram_secret_names" {
  description = "Map of principal name → Secrets Manager secret name"
  value       = { for k, s in aws_secretsmanager_secret.scram : k => s.name }
}

output "current_version" {
  description = "MSK cluster current version (needed for updates)"
  value       = aws_msk_cluster.main.current_version
}
