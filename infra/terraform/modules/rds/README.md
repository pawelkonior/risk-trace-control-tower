# RDS PostgreSQL 16.2 Terraform Module

Reusable Terraform module for provisioning Amazon RDS PostgreSQL 16.2 with secure defaults, encryption, Secrets Manager integration, and BCBS239-compliant audit controls.

## Features

- **PostgreSQL 16.2** with custom parameter group
- **Environment-specific sizing** (dev: t3.medium, prod: m6g.xlarge)
- **KMS encryption** at rest for storage and secrets
- **SSL enforcement** for all database connections
- **pgaudit** enabled for DDL activity logging
- **AWS Secrets Manager** integration with correct driver format
- **Multi-AZ** deployment for production environments
- **Automated backups** with environment-specific retention
- **Deletion protection** for production databases

## Critical Requirements

### Database Configuration
- **Database Name**: `rwa_steering` (NOT `rwa_db`)
- **Admin Username**: `rwa_admin`
- **Engine**: PostgreSQL 16.2
- **Parameter Group Family**: postgres16

### Secrets Manager
- **Secret Path**: `/rwa/{env}/database-url`
- **Secret Key**: `RWA_DATABASE_URL` (NOT `DATABASE_URL`)
- **Connection String Format**: `postgresql+psycopg://rwa_admin:{password}@{endpoint}:5432/rwa_steering`
- **Driver**: `psycopg` (NOT `asyncpg`)

### Security Controls
- SSL-only connections (`rds.force_ssl=1`)
- Private VPC deployment only
- KMS encryption for storage and secrets
- pgaudit enabled for DDL logging
- Connection logging enabled

## Usage

```hcl
module "rds" {
  source = "./modules/rds"

  # Environment Configuration
  environment  = "dev"
  project_name = "rwa-control-tower"
  region       = "eu-west-1"

  # Networking (from networking module)
  vpc_id                 = module.networking.vpc_id
  database_subnet_ids    = module.networking.database_subnet_ids
  rds_security_group_id  = module.networking.rds_security_group_id

  # Encryption (from KMS module)
  kms_key_arn = module.kms.key_arn

  # Optional: Storage Configuration
  allocated_storage     = 100
  max_allocated_storage = 1000

  # Optional: Backup Windows
  backup_window      = "03:00-04:00"
  maintenance_window = "sun:04:00-sun:05:00"

  # Tags
  tags = {
    ManagedBy = "Terraform"
    Team      = "Platform"
  }
}
```

## Environment-Specific Behavior

### Development (`dev`)
- Instance: `db.t3.medium`
- Multi-AZ: Disabled
- Backup Retention: 7 days
- Deletion Protection: Disabled
- Performance Insights: Disabled
- Secret Recovery: Immediate (0 days)

### Production (`prod`)
- Instance: `db.m6g.xlarge`
- Multi-AZ: Enabled
- Backup Retention: 30 days
- Deletion Protection: Enabled
- Performance Insights: Enabled
- Secret Recovery: 30 days

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| environment | Environment name (dev, staging, prod) | `string` | n/a | yes |
| vpc_id | VPC ID where RDS will be deployed | `string` | n/a | yes |
| database_subnet_ids | List of database subnet IDs (min 2) | `list(string)` | n/a | yes |
| rds_security_group_id | Security group ID for RDS | `string` | n/a | yes |
| kms_key_arn | KMS key ARN for encryption | `string` | n/a | yes |
| project_name | Project name for resource naming | `string` | `"rwa-control-tower"` | no |
| region | AWS region | `string` | `"eu-west-1"` | no |
| allocated_storage | Initial storage in GB | `number` | `100` | no |
| max_allocated_storage | Max storage for autoscaling in GB | `number` | `1000` | no |
| backup_window | Backup window (UTC) | `string` | `"03:00-04:00"` | no |
| maintenance_window | Maintenance window (UTC) | `string` | `"sun:04:00-sun:05:00"` | no |
| enabled_cloudwatch_logs_exports | Log types to export | `list(string)` | `["postgresql", "upgrade"]` | no |
| tags | Additional tags | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| db_instance_endpoint | RDS endpoint (host:port) |
| db_instance_address | RDS hostname (without port) |
| db_instance_identifier | RDS instance identifier |
| db_instance_arn | RDS instance ARN |
| db_name | Database name (rwa_steering) |
| db_port | Database port (5432) |
| parameter_group_name | Parameter group name |
| parameter_group_id | Parameter group ID |
| db_secret_arn | Secrets Manager secret ARN |
| db_secret_name | Secrets Manager secret name |
| db_secret_id | Secrets Manager secret ID |
| db_subnet_group_name | Subnet group name |
| db_subnet_group_arn | Subnet group ARN |
| db_username | Database username (sensitive) |
| db_password | Database password (sensitive) |

## PostgreSQL Parameter Group

The module creates a custom parameter group with the following settings:

```hcl
rds.force_ssl                = "1"      # SSL-only connections
log_connections              = "1"      # Log all connections
shared_preload_libraries     = "pgaudit" # Enable pgaudit extension
pgaudit.log                  = "ddl"    # Log DDL statements
```

## Secrets Manager Integration

The module creates a secret at `/rwa/{env}/database-url` with the following structure:

```json
{
  "RWA_DATABASE_URL": "postgresql+psycopg://rwa_admin:{password}@{endpoint}:5432/rwa_steering"
}
```

This secret can be consumed by:
- **Backend services** via environment variable `RWA_DATABASE_URL`
- **External Secrets Operator** for Kubernetes secret synchronization
- **ECS tasks** via secrets injection

## Backend Application Compatibility

The connection string format is compatible with:
- SQLAlchemy with psycopg driver
- Python backend services in `apps/backend/`
- Environment variable: `RWA_DATABASE_URL`

Example usage in Python:
```python
import os
from sqlalchemy import create_engine

database_url = os.getenv("RWA_DATABASE_URL")
engine = create_engine(database_url, pool_pre_ping=True)
```

## Security Considerations

### Encryption
- Storage encrypted at rest using customer-managed KMS key
- Secrets encrypted in Secrets Manager using same KMS key
- SSL/TLS enforced for all client connections

### Network Security
- Database deployed in private subnets only
- No public accessibility
- Security group restricts access to EKS nodes only (port 5432)

### Audit & Compliance (BCBS239)
- pgaudit extension enabled for DDL logging
- Connection logging enabled
- CloudWatch Logs integration for centralized logging
- Automated backups with environment-specific retention

### Access Control
- Centralized secret management via AWS Secrets Manager
- IRSA-based access for Kubernetes workloads
- No hardcoded credentials in code or configuration

## Backup & Recovery

### Automated Backups
- **Development**: 7-day retention
- **Production**: 30-day retention
- Backup window: 03:00-04:00 UTC (configurable)

### Final Snapshots
- **Development**: Skipped on deletion
- **Production**: Created automatically on deletion

### Recovery Procedure
1. Identify snapshot: `aws rds describe-db-snapshots`
2. Restore snapshot: `aws rds restore-db-instance-from-db-snapshot`
3. Update Secrets Manager with new endpoint
4. Restart backend services

## Maintenance

### Minor Version Upgrades
- Disabled by default (`auto_minor_version_upgrade = false`)
- Manual upgrades recommended for testing

### Maintenance Window
- Default: Sunday 04:00-05:00 UTC
- Configurable via `maintenance_window` variable

### Password Rotation
- Initial password generated randomly (32 characters)
- Manual rotation via AWS Secrets Manager console
- Future: Implement automatic rotation with Lambda

## Monitoring

### CloudWatch Logs
- PostgreSQL logs exported to CloudWatch
- Upgrade logs exported to CloudWatch

### Performance Insights
- Enabled for production environments
- Encrypted with KMS key
- 7-day retention

### Recommended Alarms
- High CPU utilization (>80%)
- Low free storage space (<10%)
- High database connections (>80% of max)
- Replication lag (Multi-AZ)

## Troubleshooting

### Connection Issues
1. Verify security group allows traffic from EKS nodes
2. Check SSL enforcement: `SHOW rds.force_ssl;`
3. Verify connection string format includes `postgresql+psycopg://`

### Performance Issues
1. Enable Performance Insights (production)
2. Review CloudWatch metrics
3. Check slow query logs
4. Consider instance size upgrade

### Backup Issues
1. Verify backup window doesn't conflict with high-traffic periods
2. Check backup retention settings
3. Test snapshot restoration procedure

## References

- [AWS RDS PostgreSQL Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html)
- [PostgreSQL 16 Release Notes](https://www.postgresql.org/docs/16/release-16.html)
- [pgaudit Extension](https://github.com/pgaudit/pgaudit)
- [BCBS239 Principles](https://www.bis.org/publ/bcbs239.htm)

## License

Internal use only - RWA Control Tower Platform Team