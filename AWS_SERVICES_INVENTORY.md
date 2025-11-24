# 🗂️ AWS Services Complete Inventory

**Last Updated:** November 24, 2025  
**AWS Account:** 322388074242  
**Region:** us-east-1 (N. Virginia)  
**Environment:** Production

---

## 📊 Quick Overview

| Category | Service | Status | Resource ID |
|----------|---------|--------|-------------|
| **Compute** | ECS Cluster | ✅ Active | production-cluster |
| **Compute** | Backend Service | ⚠️ No tasks | apranova-backend |
| **Compute** | Frontend Service | ⚠️ No tasks | apranova-frontend |
| **Database** | RDS PostgreSQL | ✅ Running | production-apranova-db |
| **Cache** | ElastiCache Redis | ✅ Running | production-redis |
| **Storage** | EFS | ✅ Available | fs-0718ee8fff27b133a |
| **Registry** | ECR Backend | ✅ Active | apranova/backend |
| **Registry** | ECR Frontend | ✅ Active | apranova/frontend |
| **Network** | VPC | ✅ Active | vpc-0458be7e20a61077e |
| **Network** | ALB | ✅ Active | production-alb |
| **Network** | NAT Gateway | ✅ Active | production-nat |
| **Network** | Internet Gateway | ✅ Active | production-igw |

**Total Resources:** 31 AWS resources deployed  
**Monthly Cost:** ~$134 USD

---

## 1️⃣ COMPUTE SERVICES

### ECS (Elastic Container Service)

**Cluster Name:** `production-cluster`  
**Region:** us-east-1  
**Launch Type:** Fargate (Serverless)

#### Backend Service
- **Service Name:** `apranova-backend`
- **Task Definition:** `apranova-backend:latest`
- **Desired Count:** 1
- **Current Status:** ⚠️ No running tasks
- **Container:**
  - Image: `322388074242.dkr.ecr.us-east-1.amazonaws.com/apranova/backend:latest`
  - Size: 667 MB
  - Port: 8000
  - CPU: 512 (0.5 vCPU)
  - Memory: 1024 MB (1 GB)
  - Platform: linux/amd64

**Environment Variables:**
```
DATABASE_URL=postgresql://apranova_admin:***@production-apranova-db.cqzg84imcy8x.us-east-1.rds.amazonaws.com:5432/apranova_db
REDIS_URL=redis://production-redis.xxxxx.0001.use1.cache.amazonaws.com:6379/0
DJANGO_SETTINGS_MODULE=backend.settings
DEBUG=False
ALLOWED_HOSTS=production-alb-1841167835.us-east-1.elb.amazonaws.com
```

**Where to Check:**
```bash
# List services
aws ecs list-services --cluster production-cluster --region us-east-1

# Describe service
aws ecs describe-services --cluster production-cluster --services apranova-backend --region us-east-1

# View tasks
aws ecs list-tasks --cluster production-cluster --service-name apranova-backend --region us-east-1

# View logs
aws logs tail /ecs/backend --follow --region us-east-1
```

**Console URL:**  
https://console.aws.amazon.com/ecs/home?region=us-east-1#/clusters/production-cluster/services/apranova-backend

---

#### Frontend Service
- **Service Name:** `apranova-frontend`
- **Task Definition:** `apranova-frontend:latest`
- **Desired Count:** 1
- **Current Status:** ⚠️ No running tasks
- **Container:**
  - Image: `322388074242.dkr.ecr.us-east-1.amazonaws.com/apranova/frontend:latest`
  - Size: 391 MB
  - Port: 3000
  - CPU: 256 (0.25 vCPU)
  - Memory: 512 MB
  - Platform: linux/amd64

**Environment Variables:**
```
NEXT_PUBLIC_API_URL=http://production-alb-1841167835.us-east-1.elb.amazonaws.com/api
NODE_ENV=production
```

**Where to Check:**
```bash
# Describe service
aws ecs describe-services --cluster production-cluster --services apranova-frontend --region us-east-1

# View logs
aws logs tail /ecs/frontend --follow --region us-east-1
```

**Console URL:**  
https://console.aws.amazon.com/ecs/home?region=us-east-1#/clusters/production-cluster/services/apranova-frontend

---

## 2️⃣ DATABASE SERVICES

### RDS PostgreSQL

**Instance Identifier:** `production-apranova-db`  
**Status:** ✅ Available  
**Engine:** PostgreSQL 14.19  
**Instance Class:** db.t3.micro (2 vCPU, 1 GB RAM)

**Connection Details:**
- **Endpoint:** `production-apranova-db.cqzg84imcy8x.us-east-1.rds.amazonaws.com`
- **Port:** 5432
- **Database Name:** `apranova_db`
- **Username:** `apranova_admin`
- **Password:** (stored in terraform.tfvars)

**Configuration:**
- Storage: 20 GB (gp2)
- Multi-AZ: No (single instance)
- Backup Retention: 0 days (disabled for cost)
- Encryption: Not enabled
- Public Access: No (private subnet only)
- Availability Zone: us-east-1b

**Security:**
- Security Group: `production-rds-sg`
- Allows: Port 5432 from ECS security group only
- VPC: vpc-0458be7e20a61077e
- Subnets: production-private-1, production-private-2

**Where to Check:**
```bash
# Describe instance
aws rds describe-db-instances --db-instance-identifier production-apranova-db --region us-east-1

# Check status
aws rds describe-db-instances --db-instance-identifier production-apranova-db --query 'DBInstances[0].DBInstanceStatus' --region us-east-1

# Connect from backend container
psql postgresql://apranova_admin:PASSWORD@production-apranova-db.cqzg84imcy8x.us-east-1.rds.amazonaws.com:5432/apranova_db
```

**Console URL:**  
https://console.aws.amazon.com/rds/home?region=us-east-1#database:id=production-apranova-db

**Cost:** ~$15/month

---

## 3️⃣ CACHE SERVICES

### ElastiCache Redis

**Cluster ID:** `production-redis`  
**Status:** ✅ Available  
**Engine:** Redis 7.x  
**Node Type:** cache.t3.micro (2 vCPU, 0.5 GB RAM)

**Connection Details:**
- **Endpoint:** `production-redis.xxxxx.0001.use1.cache.amazonaws.com`
- **Port:** 6379
- **Nodes:** 1

**Configuration:**
- Parameter Group: default.redis7
- Subnet Group: production-redis-subnet
- Multi-AZ: No
- Encryption: Not enabled
- Automatic Failover: No

**Security:**
- Security Group: `production-redis-sg`
- Allows: Port 6379 from ECS security group only
- VPC: vpc-0458be7e20a61077e

**Where to Check:**
```bash
# Describe cluster
aws elasticache describe-cache-clusters --cache-cluster-id production-redis --region us-east-1

# Get endpoint
aws elasticache describe-cache-clusters --cache-cluster-id production-redis --show-cache-node-info --query 'CacheClusters[0].CacheNodes[0].Endpoint' --region us-east-1

# Test connection from backend
redis-cli -h production-redis.xxxxx.0001.use1.cache.amazonaws.com -p 6379 ping
```

**Console URL:**  
https://console.aws.amazon.com/elasticache/home?region=us-east-1#/redis/production-redis

**Cost:** ~$12/month

---

## 4️⃣ STORAGE SERVICES

### EFS (Elastic File System)

**File System ID:** `fs-0718ee8fff27b133a`  
**Status:** ✅ Available  
**Name:** `production-efs`

**Configuration:**
- Performance Mode: General Purpose
- Throughput Mode: Bursting
- Encryption: In transit (TLS)
- Lifecycle Management: Not configured
- Size: Pay per use (currently minimal)

**Mount Targets:**
- **AZ-A (us-east-1a):** subnet-0d44dc8dd8c5fac45
- **AZ-B (us-east-1b):** subnet-0d474695924b452fe

**Security:**
- Security Group: Uses ECS security group
- Access: NFS protocol (port 2049)
- VPC: vpc-0458be7e20a61077e

**Usage:**
- Workspace files for students
- User uploads
- Persistent data across container restarts

**Where to Check:**
```bash
# Describe file system
aws efs describe-file-systems --file-system-id fs-0718ee8fff27b133a --region us-east-1

# List mount targets
aws efs describe-mount-targets --file-system-id fs-0718ee8fff27b133a --region us-east-1

# Check size and usage
aws efs describe-file-systems --file-system-id fs-0718ee8fff27b133a --query 'FileSystems[0].SizeInBytes' --region us-east-1
```

**Console URL:**  
https://console.aws.amazon.com/efs/home?region=us-east-1#/file-systems/fs-0718ee8fff27b133a

**Cost:** ~$10/month (based on usage)

---

### ECR (Elastic Container Registry)

**Repositories:**

#### Backend Repository
- **Name:** `apranova/backend`
- **URI:** `322388074242.dkr.ecr.us-east-1.amazonaws.com/apranova/backend`
- **Latest Image:** `latest` tag
- **Size:** 667 MB
- **Platform:** linux/amd64

#### Frontend Repository
- **Name:** `apranova/frontend`
- **URI:** `322388074242.dkr.ecr.us-east-1.amazonaws.com/apranova/frontend`
- **Latest Image:** `latest` tag
- **Size:** 391 MB
- **Platform:** linux/amd64

**Where to Check:**
```bash
# List repositories
aws ecr describe-repositories --region us-east-1

# List images in backend repo
aws ecr list-images --repository-name apranova/backend --region us-east-1

# Get image details
aws ecr describe-images --repository-name apranova/backend --region us-east-1

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 322388074242.dkr.ecr.us-east-1.amazonaws.com
```

**Console URL:**  
https://console.aws.amazon.com/ecr/repositories?region=us-east-1

**Cost:** ~$1/month (storage)

---

## 5️⃣ NETWORKING SERVICES

### VPC (Virtual Private Cloud)

**VPC ID:** `vpc-0458be7e20a61077e`  
**Name:** `production-vpc`  
**CIDR Block:** 10.0.0.0/16  
**Status:** ✅ Available

**Configuration:**
- DNS Hostnames: Enabled
- DNS Resolution: Enabled
- Default VPC: No
- Tenancy: Default

**Subnets:**

#### Public Subnets (Internet-facing)
1. **production-public-1**
   - Subnet ID: `subnet-0a1b2c3d4e5f6g7h8` (example)
   - CIDR: 10.0.1.0/24
   - AZ: us-east-1a
   - Auto-assign Public IP: Yes
   - Contains: ALB, NAT Gateway

2. **production-public-2**
   - Subnet ID: `subnet-1a2b3c4d5e6f7g8h9` (example)
   - CIDR: 10.0.2.0/24
   - AZ: us-east-1b
   - Auto-assign Public IP: Yes
   - Contains: ALB

#### Private Subnets (No direct internet)
1. **production-private-1**
   - Subnet ID: `subnet-0d44dc8dd8c5fac45`
   - CIDR: 10.0.11.0/24
   - AZ: us-east-1a
   - Contains: ECS tasks, RDS, Redis, EFS

2. **production-private-2**
   - Subnet ID: `subnet-0d474695924b452fe`
   - CIDR: 10.0.12.0/24
   - AZ: us-east-1b
   - Contains: ECS tasks, RDS, Redis, EFS

**Where to Check:**
```bash
# Describe VPC
aws ec2 describe-vpcs --vpc-ids vpc-0458be7e20a61077e --region us-east-1

# List subnets
aws ec2 describe-subnets --filters "Name=vpc-id,Values=vpc-0458be7e20a61077e" --region us-east-1

# Show route tables
aws ec2 describe-route-tables --filters "Name=vpc-id,Values=vpc-0458be7e20a61077e" --region us-east-1
```

**Console URL:**  
https://console.aws.amazon.com/vpc/home?region=us-east-1#vpcs:VpcId=vpc-0458be7e20a61077e

---

### Internet Gateway

**IGW ID:** `production-igw`  
**Status:** ✅ Attached  
**VPC:** vpc-0458be7e20a61077e

**Purpose:** Allows public subnets to access the internet

**Where to Check:**
```bash
aws ec2 describe-internet-gateways --filters "Name=attachment.vpc-id,Values=vpc-0458be7e20a61077e" --region us-east-1
```

---

### NAT Gateway

**NAT Gateway ID:** `production-nat`  
**Status:** ✅ Available  
**Subnet:** production-public-1 (us-east-1a)  
**Elastic IP:** Allocated

**Purpose:** Allows private subnets to access the internet (for updates, API calls, etc.)

**Where to Check:**
```bash
# Describe NAT Gateway
aws ec2 describe-nat-gateways --filter "Name=vpc-id,Values=vpc-0458be7e20a61077e" --region us-east-1

# Check associated Elastic IP
aws ec2 describe-addresses --region us-east-1
```

**Cost:** ~$33/month (most expensive networking component)

---

### Application Load Balancer

**Name:** `production-alb`  
**DNS Name:** `production-alb-1841167835.us-east-1.elb.amazonaws.com`  
**Status:** ✅ Active  
**Type:** Application Load Balancer  
**Scheme:** Internet-facing

**Configuration:**
- Subnets: production-public-1, production-public-2
- Security Group: production-alb-sg
- IP Address Type: IPv4
- Deletion Protection: Disabled

**Listeners:**
- **HTTP (Port 80)**
  - Default Action: Forward to frontend-tg
  - Rule 100: Forward /api/* and /admin/* to backend-tg

**Target Groups:**

#### Backend Target Group
- **Name:** `production-backend-tg`
- **Port:** 8000
- **Protocol:** HTTP
- **Target Type:** IP
- **Health Check:**
  - Path: /health
  - Interval: 300 seconds
  - Timeout: 60 seconds
  - Healthy Threshold: 2
  - Unhealthy Threshold: 10

#### Frontend Target Group
- **Name:** `production-frontend-tg`
- **Port:** 3000
- **Protocol:** HTTP
- **Target Type:** IP
- **Health Check:**
  - Path: /
  - Interval: 30 seconds
  - Timeout: 5 seconds

**Where to Check:**
```bash
# Describe load balancer
aws elbv2 describe-load-balancers --names production-alb --region us-east-1

# List target groups
aws elbv2 describe-target-groups --load-balancer-arn <ARN> --region us-east-1

# Check target health
aws elbv2 describe-target-health --target-group-arn <TG-ARN> --region us-east-1

# Test endpoint
curl http://production-alb-1841167835.us-east-1.elb.amazonaws.com
```

**Console URL:**  
https://console.aws.amazon.com/ec2/home?region=us-east-1#LoadBalancers:

**Cost:** ~$16/month

---

### Security Groups

#### ALB Security Group
- **Name:** `production-alb-sg`
- **Inbound Rules:**
  - Port 80 (HTTP) from 0.0.0.0/0
  - Port 443 (HTTPS) from 0.0.0.0/0
- **Outbound Rules:**
  - All traffic to 0.0.0.0/0

#### ECS Security Group
- **Name:** `production-ecs-sg`
- **Inbound Rules:**
  - All ports from ALB security group
- **Outbound Rules:**
  - All traffic to 0.0.0.0/0

#### RDS Security Group
- **Name:** `production-rds-sg`
- **Inbound Rules:**
  - Port 5432 from ECS security group
- **Outbound Rules:**
  - None (default deny)

#### Redis Security Group
- **Name:** `production-redis-sg`
- **Inbound Rules:**
  - Port 6379 from ECS security group
- **Outbound Rules:**
  - None (default deny)

**Where to Check:**
```bash
# List security groups
aws ec2 describe-security-groups --filters "Name=vpc-id,Values=vpc-0458be7e20a61077e" --region us-east-1

# Describe specific SG
aws ec2 describe-security-groups --group-names production-alb-sg --region us-east-1
```

---

## 6️⃣ MONITORING & LOGGING

### CloudWatch Logs

**Log Groups:**
- `/ecs/backend` - Backend application logs
- `/ecs/frontend` - Frontend application logs
- `/aws/ecs/containerinsights/production-cluster/performance` - ECS metrics

**Retention:** 7 days (default)

**Where to Check:**
```bash
# List log groups
aws logs describe-log-groups --region us-east-1

# Tail backend logs
aws logs tail /ecs/backend --follow --region us-east-1

# Tail frontend logs
aws logs tail /ecs/frontend --follow --region us-east-1

# Search logs
aws logs filter-log-events --log-group-name /ecs/backend --filter-pattern "ERROR" --region us-east-1
```

**Console URL:**  
https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups

---

### CloudWatch Metrics

**Available Metrics:**
- ECS: CPU, Memory, Network
- RDS: CPU, Connections, Storage
- ALB: Request Count, Target Response Time
- ElastiCache: CPU, Memory, Evictions

**Where to Check:**
```bash
# Get ECS metrics
aws cloudwatch get-metric-statistics --namespace AWS/ECS --metric-name CPUUtilization --dimensions Name=ClusterName,Value=production-cluster --start-time 2025-11-24T00:00:00Z --end-time 2025-11-24T23:59:59Z --period 3600 --statistics Average --region us-east-1
```

**Console URL:**  
https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#metricsV2:

**Cost:** ~$2/month

---

## 7️⃣ IAM ROLES & PERMISSIONS

### ECS Task Execution Role
- **Name:** `ecsTaskExecutionRole`
- **Purpose:** Pull images from ECR, write logs to CloudWatch
- **Policies:**
  - AmazonECSTaskExecutionRolePolicy

### ECS Task Role
- **Name:** `ecsTaskRole` (if created)
- **Purpose:** Access AWS services from containers
- **Policies:**
  - Access to EFS
  - Access to S3 (if needed)
  - Access to Secrets Manager (if needed)

**Where to Check:**
```bash
# List roles
aws iam list-roles --query 'Roles[?contains(RoleName, `ecs`)]' --region us-east-1

# Get role details
aws iam get-role --role-name ecsTaskExecutionRole --region us-east-1
```

**Console URL:**  
https://console.aws.amazon.com/iam/home#/roles

---

## 8️⃣ COST BREAKDOWN

### Monthly Cost Estimate: ~$134

| Service | Cost | Percentage |
|---------|------|------------|
| **NAT Gateway** | $33 | 24.6% |
| **ECS Fargate** | $40 | 29.9% |
| **ALB** | $16 | 11.9% |
| **RDS PostgreSQL** | $15 | 11.2% |
| **ElastiCache Redis** | $12 | 9.0% |
| **EFS** | $10 | 7.5% |
| **Data Transfer** | $5 | 3.7% |
| **CloudWatch** | $2 | 1.5% |
| **ECR** | $1 | 0.7% |
| **TOTAL** | **$134** | **100%** |

**Cost Optimization Tips:**
1. Remove NAT Gateway if not needed (save $33/month)
2. Use Fargate Spot for non-critical workloads (save 70%)
3. Enable RDS Reserved Instances (save 30-40%)
4. Implement auto-scaling to reduce idle resources
5. Use S3 instead of EFS for static files (cheaper)

**Where to Check:**
```bash
# Get cost and usage
aws ce get-cost-and-usage --time-period Start=2025-11-01,End=2025-11-30 --granularity MONTHLY --metrics BlendedCost --region us-east-1
```

**Console URL:**  
https://console.aws.amazon.com/billing/home

---

## 9️⃣ DEPLOYMENT ARTIFACTS

### Local Files

**Terraform Configuration:**
- `terraform/basic-deployment.tf` - Infrastructure as Code
- `terraform/terraform.tfstate` - Current state
- `terraform/terraform.tfvars` - Variables (contains secrets)

**Docker Images:**
- `backend/Dockerfile` - Backend image definition
- `frontend/Dockerfile.simple` - Frontend image definition

**ECS Task Definitions:**
- `backend-task-def.json` - Backend task configuration
- `frontend-task-def.json` - Frontend task configuration

**Deployment Scripts:**
- `deploy-basic-aws.sh` - Main deployment script
- `create_superuser.py` - Database initialization

**Documentation:**
- `AWS_MASTER_GUIDE.md` - Complete guide
- `AWS_COMPLETE_SERVICES_GUIDE.md` - Service details
- `YOUR_AWS_ARCHITECTURE.md` - Architecture diagrams
- `AWS_ARCHITECTURE_DIAGRAM.md` - Visual diagrams

---

## 🔟 QUICK ACCESS COMMANDS

### Check Everything
```bash
# ECS Services
aws ecs list-services --cluster production-cluster --region us-east-1

# Running Tasks
aws ecs list-tasks --cluster production-cluster --region us-east-1

# RDS Status
aws rds describe-db-instances --db-instance-identifier production-apranova-db --query 'DBInstances[0].DBInstanceStatus' --output text --region us-east-1

# Redis Status
aws elasticache describe-cache-clusters --cache-cluster-id production-redis --query 'CacheClusters[0].CacheClusterStatus' --output text --region us-east-1

# ALB DNS
aws elbv2 describe-load-balancers --names production-alb --query 'LoadBalancers[0].DNSName' --output text --region us-east-1

# EFS Status
aws efs describe-file-systems --file-system-id fs-0718ee8fff27b133a --query 'FileSystems[0].LifeCycleState' --output text --region us-east-1
```

### Start Services
```bash
# Update backend service
aws ecs update-service --cluster production-cluster --service apranova-backend --desired-count 1 --region us-east-1

# Update frontend service
aws ecs update-service --cluster production-cluster --service apranova-frontend --desired-count 1 --region us-east-1
```

### View Logs
```bash
# Backend logs (last 10 minutes)
aws logs tail /ecs/backend --since 10m --region us-east-1

# Frontend logs (follow)
aws logs tail /ecs/frontend --follow --region us-east-1
```

### Test Application
```bash
# Test ALB
curl http://production-alb-1841167835.us-east-1.elb.amazonaws.com

# Test backend API
curl http://production-alb-1841167835.us-east-1.elb.amazonaws.com/api/health

# Test frontend
curl http://production-alb-1841167835.us-east-1.elb.amazonaws.com/
```

---

## 📍 WHERE TO FIND EVERYTHING IN AWS CONSOLE

### Main Services Dashboard
https://console.aws.amazon.com/console/home?region=us-east-1

### Individual Services

1. **ECS Cluster**  
   https://console.aws.amazon.com/ecs/home?region=us-east-1#/clusters/production-cluster

2. **RDS Database**  
   https://console.aws.amazon.com/rds/home?region=us-east-1#database:id=production-apranova-db

3. **ElastiCache Redis**  
   https://console.aws.amazon.com/elasticache/home?region=us-east-1#/redis/production-redis

4. **VPC**  
   https://console.aws.amazon.com/vpc/home?region=us-east-1#vpcs:VpcId=vpc-0458be7e20a61077e

5. **Load Balancers**  
   https://console.aws.amazon.com/ec2/home?region=us-east-1#LoadBalancers:

6. **ECR Repositories**  
   https://console.aws.amazon.com/ecr/repositories?region=us-east-1

7. **CloudWatch Logs**  
   https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups

8. **EFS File Systems**  
   https://console.aws.amazon.com/efs/home?region=us-east-1

9. **Billing Dashboard**  
   https://console.aws.amazon.com/billing/home

10. **IAM Roles**  
    https://console.aws.amazon.com/iam/home#/roles

---

## 🎯 CURRENT STATUS SUMMARY

✅ **Working:**
- VPC and networking infrastructure
- RDS PostgreSQL database
- ElastiCache Redis cache
- EFS file system
- ECR repositories with images
- Application Load Balancer
- Security groups and IAM roles

⚠️ **Needs Attention:**
- ECS services have no running tasks
- Need to start backend and frontend services
- Health checks may need adjustment

🔧 **To Start Application:**
```bash
# Start both services
aws ecs update-service --cluster production-cluster --service apranova-backend --desired-count 1 --region us-east-1
aws ecs update-service --cluster production-cluster --service apranova-frontend --desired-count 1 --region us-east-1

# Wait 2-3 minutes, then check
aws ecs list-tasks --cluster production-cluster --region us-east-1

# Access application
open http://production-alb-1841167835.us-east-1.elb.amazonaws.com
```

---

## 📚 RELATED DOCUMENTATION

- **AWS_MASTER_GUIDE.md** - Complete deployment guide
- **AWS_COMPLETE_SERVICES_GUIDE.md** - Detailed service documentation
- **YOUR_AWS_ARCHITECTURE.md** - Architecture overview with diagrams
- **AWS_ARCHITECTURE_DIAGRAM.md** - Visual architecture diagrams
- **DEPLOYMENT_SUCCESS.md** - Deployment history
- **SIGNUP_ERROR_FIX.md** - Troubleshooting guide

---

**This inventory contains everything you need to understand, manage, and troubleshoot your AWS deployment!** 🚀
