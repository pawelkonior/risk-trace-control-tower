# ============================================================================
# VPC
# ============================================================================

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-vpc"
      Environment = var.environment
      Project     = var.project_name
    }
  )
}

# ============================================================================
# Internet Gateway
# ============================================================================

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-igw"
      Environment = var.environment
      Project     = var.project_name
    }
  )
}

# ============================================================================
# Public Subnets (NLB + NAT Gateways)
# ============================================================================

resource "aws_subnet" "public" {
  count = length(var.availability_zones)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = merge(
    var.tags,
    {
      Name                     = "${var.project_name}-${var.environment}-public-${var.availability_zones[count.index]}"
      Environment              = var.environment
      Project                  = var.project_name
      Tier                     = "public"
      "kubernetes.io/role/elb" = "1"
    }
  )
}

# ============================================================================
# Private Subnets (EKS Worker Nodes)
# ============================================================================

resource "aws_subnet" "private" {
  count = length(var.availability_zones)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.private_subnet_cidrs[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = false

  tags = merge(
    var.tags,
    {
      Name                              = "${var.project_name}-${var.environment}-private-${var.availability_zones[count.index]}"
      Environment                       = var.environment
      Project                           = var.project_name
      Tier                              = "private"
      "kubernetes.io/role/internal-elb" = "1"
    }
  )
}

# ============================================================================
# Database Subnets (RDS, MSK, ElastiCache)
# ============================================================================

resource "aws_subnet" "database" {
  count = length(var.availability_zones)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.database_subnet_cidrs[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = false

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-database-${var.availability_zones[count.index]}"
      Environment = var.environment
      Project     = var.project_name
      Tier        = "database"
    }
  )
}

# ============================================================================
# Elastic IPs for NAT Gateways
# ============================================================================

resource "aws_eip" "nat" {
  count = var.single_nat_gateway ? 1 : length(var.availability_zones)

  domain = "vpc"

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-nat-eip-${count.index + 1}"
      Environment = var.environment
      Project     = var.project_name
    }
  )

  depends_on = [aws_internet_gateway.main]
}

# ============================================================================
# NAT Gateways
# ============================================================================

resource "aws_nat_gateway" "main" {
  count = var.single_nat_gateway ? 1 : length(var.availability_zones)

  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-nat-${var.availability_zones[count.index]}"
      Environment = var.environment
      Project     = var.project_name
    }
  )

  depends_on = [aws_internet_gateway.main]
}

# ============================================================================
# Route Tables - Public
# ============================================================================

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-public-rt"
      Environment = var.environment
      Project     = var.project_name
      Tier        = "public"
    }
  )
}

resource "aws_route" "public_internet_gateway" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.main.id
}

resource "aws_route_table_association" "public" {
  count = length(var.availability_zones)

  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# ============================================================================
# Route Tables - Private
# ============================================================================

resource "aws_route_table" "private" {
  count = var.single_nat_gateway ? 1 : length(var.availability_zones)

  vpc_id = aws_vpc.main.id

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-private-rt-${count.index + 1}"
      Environment = var.environment
      Project     = var.project_name
      Tier        = "private"
    }
  )
}

resource "aws_route" "private_nat_gateway" {
  count = var.single_nat_gateway ? 1 : length(var.availability_zones)

  route_table_id         = aws_route_table.private[count.index].id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.main[count.index].id
}

resource "aws_route_table_association" "private" {
  count = length(var.availability_zones)

  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = var.single_nat_gateway ? aws_route_table.private[0].id : aws_route_table.private[count.index].id
}

# ============================================================================
# Route Tables - Database
# ============================================================================

resource "aws_route_table" "database" {
  count = var.single_nat_gateway ? 1 : length(var.availability_zones)

  vpc_id = aws_vpc.main.id

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-database-rt-${count.index + 1}"
      Environment = var.environment
      Project     = var.project_name
      Tier        = "database"
    }
  )
}

resource "aws_route" "database_nat_gateway" {
  count = var.single_nat_gateway ? 1 : length(var.availability_zones)

  route_table_id         = aws_route_table.database[count.index].id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.main[count.index].id
}

resource "aws_route_table_association" "database" {
  count = length(var.availability_zones)

  subnet_id      = aws_subnet.database[count.index].id
  route_table_id = var.single_nat_gateway ? aws_route_table.database[0].id : aws_route_table.database[count.index].id
}

# ============================================================================
# Security Group - Network Load Balancer
# ============================================================================

resource "aws_security_group" "nlb" {
  name_prefix = "${var.project_name}-${var.environment}-nlb-"
  description = "Security group for Network Load Balancer"
  vpc_id      = aws_vpc.main.id

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-nlb-sg"
      Environment = var.environment
      Project     = var.project_name
    }
  )

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_vpc_security_group_ingress_rule" "nlb_https" {
  security_group_id = aws_security_group.nlb.id
  description       = "Allow HTTPS from internet"

  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 443
  to_port     = 443
  ip_protocol = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "nlb_all" {
  security_group_id = aws_security_group.nlb.id
  description       = "Allow all outbound traffic"

  cidr_ipv4   = "0.0.0.0/0"
  ip_protocol = "-1"
}

# ============================================================================
# Security Group - EKS Nodes
# ============================================================================

resource "aws_security_group" "eks_nodes" {
  name_prefix = "${var.project_name}-${var.environment}-eks-nodes-"
  description = "Security group for EKS worker nodes"
  vpc_id      = aws_vpc.main.id

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-eks-nodes-sg"
      Environment = var.environment
      Project     = var.project_name
    }
  )

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_vpc_security_group_ingress_rule" "eks_nodes_self" {
  security_group_id = aws_security_group.eks_nodes.id
  description       = "Allow all traffic from EKS nodes to themselves"

  referenced_security_group_id = aws_security_group.eks_nodes.id
  ip_protocol                  = "-1"
}

resource "aws_vpc_security_group_ingress_rule" "eks_nodes_from_nlb" {
  security_group_id = aws_security_group.eks_nodes.id
  description       = "Allow HTTPS from NLB"

  referenced_security_group_id = aws_security_group.nlb.id
  from_port                    = 443
  to_port                      = 443
  ip_protocol                  = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "eks_nodes_all" {
  security_group_id = aws_security_group.eks_nodes.id
  description       = "Allow all outbound traffic"

  cidr_ipv4   = "0.0.0.0/0"
  ip_protocol = "-1"
}

# ============================================================================
# Security Group - RDS (PostgreSQL)
# ============================================================================

resource "aws_security_group" "rds" {
  name_prefix = "${var.project_name}-${var.environment}-rds-"
  description = "Security group for RDS PostgreSQL database"
  vpc_id      = aws_vpc.main.id

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-rds-sg"
      Environment = var.environment
      Project     = var.project_name
    }
  )

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_vpc_security_group_ingress_rule" "rds_from_eks" {
  security_group_id = aws_security_group.rds.id
  description       = "Allow PostgreSQL from EKS nodes only"

  referenced_security_group_id = aws_security_group.eks_nodes.id
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"
}

# ============================================================================
# Security Group - Redis (ElastiCache)
# ============================================================================

resource "aws_security_group" "redis" {
  name_prefix = "${var.project_name}-${var.environment}-redis-"
  description = "Security group for ElastiCache Redis"
  vpc_id      = aws_vpc.main.id

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-redis-sg"
      Environment = var.environment
      Project     = var.project_name
    }
  )

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_vpc_security_group_ingress_rule" "redis_from_eks" {
  security_group_id = aws_security_group.redis.id
  description       = "Allow Redis TLS from EKS nodes only"

  referenced_security_group_id = aws_security_group.eks_nodes.id
  from_port                    = 6380 # TLS port — transit_encryption_mode=required
  to_port                      = 6380
  ip_protocol                  = "tcp"
}

# ============================================================================
# Security Group - MSK (Managed Streaming for Kafka)
# ============================================================================

resource "aws_security_group" "msk" {
  name_prefix = "${var.project_name}-${var.environment}-msk-"
  description = "Security group for MSK Kafka cluster"
  vpc_id      = aws_vpc.main.id

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-msk-sg"
      Environment = var.environment
      Project     = var.project_name
    }
  )

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_vpc_security_group_ingress_rule" "msk_from_eks" {
  security_group_id = aws_security_group.msk.id
  description       = "Allow Kafka from EKS nodes only"

  referenced_security_group_id = aws_security_group.eks_nodes.id
  from_port                    = 9094
  to_port                      = 9094
  ip_protocol                  = "tcp"
}

# ============================================================================
# Default Security Group — no rules (CKV2_AWS_12)
# ============================================================================

resource "aws_default_security_group" "main" {
  vpc_id = aws_vpc.main.id

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-default-sg"
      Environment = var.environment
      Project     = var.project_name
    }
  )
}

# ============================================================================
# VPC Flow Logs → CloudWatch (CKV2_AWS_11)
# ============================================================================

resource "aws_cloudwatch_log_group" "vpc_flow_logs" {
  name              = "/aws/vpc/${var.project_name}-${var.environment}/flow-logs"
  retention_in_days = 365
  kms_key_id        = var.kms_key_arn

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-vpc-flow-logs"
      Environment = var.environment
      Project     = var.project_name
    }
  )
}

resource "aws_iam_role" "vpc_flow_logs" {
  name = "${var.project_name}-${var.environment}-vpc-flow-logs-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "vpc-flow-logs.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-vpc-flow-logs-role"
      Environment = var.environment
      Project     = var.project_name
    }
  )
}

resource "aws_iam_role_policy" "vpc_flow_logs" {
  name = "cloudwatch-logs-policy"
  role = aws_iam_role.vpc_flow_logs.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams"
      ]
      Resource = "${aws_cloudwatch_log_group.vpc_flow_logs.arn}:*"
    }]
  })
}

resource "aws_flow_log" "main" {
  iam_role_arn    = aws_iam_role.vpc_flow_logs.arn
  log_destination = aws_cloudwatch_log_group.vpc_flow_logs.arn
  traffic_type    = "ALL"
  vpc_id          = aws_vpc.main.id

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-vpc-flow-log"
      Environment = var.environment
      Project     = var.project_name
    }
  )
}