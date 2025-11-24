# 🏗️ Complete AWS Services Guide - ApraNova LMS

## 📊 Overview

**Account ID:** 322388074242  
**Region:** us-east-1 (N. Virginia)  
**Total Resources:** 31  
**Monthly Cost:** ~$126  
**Status:** Deployed ✅

---

## 🌐 1. NETWORKING (VPC)

### VPC
- **Name:** production-vpc
- **CIDR:** 10.0.0.0/16
- **DNS Hostnames:** Enabled
- **DNS Support:** Enabled

**Where to check:**
- AWS Console → VPC → Your VPCs
- URL: https://console.aws.amazon.com/vpc/home?region=us-east-1#vpcs:

### Subnets (4 total)

#### Public Subnets (2)
| Name | CIDR | AZ | Purpose |
|------|------|----|---------| 
| production-public-1 | 10.0.1.0/24 | us-east-1a | Load Balancer |
| production-public-2 | 10.0.2.0/24 | us-east-1b | Load Balancer |

#### Private Subnets (2)
| Name | CIDR | AZ | Purpose |
|------|------|----|---------| 
| production-private-1 | 10.0.11.0/24 | us-east-1a | ECS, RDS, Redis |
| production-private-2 | 10.0.12.0/24 | us-east-1b | ECS, RDS, Redis |

**Where to check:**
- AWS Console → VPC → Subnets
- URL: https://console.aws.amazon.com/vpc/home?region=us-east-1#subnets:

### Internet Gateway
- **Name:** production-igw
- **Attached to:** production-vpc
- **Purpose:** Allows public subnets to access internet

**Where to check:**
- AWS Console → VPC → Internet Gateways

### NAT Gateway
- **Name:** production-nat
- **Subnet:** production-public-1
- **Elastic IP:** Allocated
- **Purpose:** Allows private subnets to access internet
- **Cost:** ~$33/month

**Where to check:**
- AWS Console → VPC → NAT Gateways

### Route Tables (2)

#### Public Route Table
- **Name:** production-public-rt
- **Routes:**
  - 10.0.0.0/16 → local
  - 0.0.0.0/0 → Internet Gateway

#### Private Route Table
- **Name:** production-private-rt
- **Routes:**
  - 10.0.0.0/16 → local
  - 0.0.0.0/0 → NAT Gateway

**Where to check:**
- AWS Console → VPC → Route Tables

### Security Groups (4)

#### 1. ALB Security Group
- **Name:** production-alb-sg
- **Inbound:**
  - Port 80 (HTTP) from 0.0.0.0/0
  - Port 443 (HTTPS) from 0.0.0.0/0
- **Outbound:** All traffic

#### 2. ECS Security Group
- **Name:** production-ecs-sg
- **ID:** sg-0463d9e4cedff4a45
- **Inbound:**
  - All ports from ALB Security Group
- **Outbound:** All traffic

#### 3. RDS Security Group
- **Name:** production-rds-sg
- **Inbound:**
  - Port 5432 from ECS Security Group
- **Outbound:** None

#### 4. Redis Security Group
- **Name:** production-redis-sg
- **Inbound:**
  - Port 6379 from ECS Security Group
- **Outbound:** None

**Where to check:**
- AWS Console → EC2 → Security Groups
- URL: https://console.aws.amazon.com/ec2/home?region=us-east-1#SecurityGroups:

---

## 🚀 2. COMPUTE (ECS)

### ECS Cluster
- **Name:** production-cluster
- **Type:** Fargate
- **Services:** 2 (backend, frontend)
- **Tasks Running:** 3

**Where to check:**
- AWS Console → ECS → Clusters → production-cluster
- URL: https://console.aws.amazon.com/ecs/home?region=us-east-1#/clusters/production-cluster

### ECS Services

#### Backend Service
- **Name:** backend
- **Task Definition:** backend:4
- **Desired Count:** 1
- **Running Count:** Check console
- **Launch Type:** Fargate
- **CPU:** 512 (0.5 vCPU)
- **Memory:** 1024 MB (1 GB)
- **Port:** 8000
- **Image:** 322388074242.dkr.ecr.us-east-1.amazonaws.com/apranova/backend:latest

**Environment Variables:**
- DATABASE_URL
- REDIS_URL
- DEBUG=True
- ALLOWED_HOSTS
- SECURE_SSL_REDIRECT=False

#### Frontend Service
- **Name:** frontend
- **Task Definition:** frontend:1
- **Desired Count:** 1
- **Running Count:** 1
- **Launch Type:** Fargate
- **CPU:** 256 (0.25 vCPU)
- **Memory:** 512 MB
- **Port:** 3000
- **Image:** 322388074242.dkr.ecr.us-east-1.amazonaws.com/apranova/frontend:latest

**Where to check:**
- AWS Console → ECS → Clusters → production-cluster → Services
- Backend logs: CloudWatch → /ecs/backend
- Frontend logs: CloudWatch → /ecs/frontend

---

## 🗄️ 3. DATABASE (RDS)

### PostgreSQL Database
- **Identifier:** production-apranova-db
- **Endpoint:** production-apranova-db.cqzg84imcy8x.us-east-1.rds.amazonaws.com:5432
- **Engine:** PostgreSQL 14
- **Instance Class:** db.t3.micro
- **Storage:** 20 GB (gp2)
- **Multi-AZ:** No (can be enabled)
- **Database Name:** apranova_db
- **Username:** apranova_admin
- **Password:** ApraNova2024SecurePass!
- **Publicly Accessible:** No
- **VPC:** production-vpc
- **Subnets:** Private subnets
- **Security Group:** production-rds-sg
- **Backup:** Automated (skip final snapshot)
- **Cost:** ~$15/month

**Where to check:**
- AWS Console → RDS → Databases → production-apranova-db
- URL: https://console.aws.amazon.com/rds/home?region=us-east-1#database:id=production-apranova-db

**Connection String:**
```
postgresql://apranova_admin:ApraNova2024SecurePass!@production-apranova-db.cqzg84imcy8x.us-east-1.rds.amazonaws.com:5432/apranova_db
```

---

## 💾 4. CACHE (ElastiCache)

### Redis Cluster
- **Cluster ID:** production-redis
- **Endpoint:** production-redis.ca9eju.0001.use1.cache.amazonaws.com:6379
- **Engine:** Redis 7
- **Node Type:** cache.t3.micro
- **Nodes:** 1
- **VPC:** production-vpc
- **Subnets:** Private subnets
- **Security Group:** production-redis-sg
- **Cost:** ~$12/month

**Where to check:**
- AWS Console → ElastiCache → Redis clusters → production-redis
- URL: https://console.aws.amazon.com/elasticache/home?region=us-east-1#redis-group-nodes:id=production-redis

**Connection String:**
```
redis://production-redis.ca9eju.0001.use1.cache.amazonaws.com:6379/0
```

---

## 📦 5. CONTAINER REGISTRY (ECR)

### Repositories (2)

#### Backend Repository
- **Name:** apranova/backend
- **URI:** 322388074242.dkr.ecr.us-east-1.amazonaws.com/apranova/backend
- **Image Size:** 667 MB
- **Platform:** linux/amd64
- **Latest Tag:** latest

#### Frontend Repository
- **Name:** apranova/frontend
- **URI:** 322388074242.dkr.ecr.us-east-1.amazonaws.com/apranova/frontend
- **Image Size:** 391 MB
- **Platform:** linux/amd64
- **Latest Tag:** latest

**Where to check:**
- AWS Console → ECR → Repositories
- URL: https://console.aws.amazon.com/ecr/repositories?region=us-east-1

**View Images:**
- Click on repository name
- See all image tags and details

---

## ⚖️ 6. LOAD BALANCER (ALB)

### Application Load Balancer
- **Name:** production-alb
- **DNS:** production-alb-1841167835.us-east-1.elb.amazonaws.com
- **Scheme:** Internet-facing
- **IP Address Type:** IPv4
- **VPC:** production-vpc
- **Subnets:** Public subnets (Multi-AZ)
- **Security Group:** production-alb-sg
- **Cost:** ~$16/month

**Where to check:**
- AWS Console → EC2 → Load Balancers → production-alb
- URL: https://console.aws.amazon.com/ec2/home?region=us-east-1#LoadBalancers:

### Listeners

#### HTTP Listener (Port 80)
- **Protocol:** HTTP
- **Port:** 80
- **Default Action:** Forward to frontend target group
- **Rules:**
  - Path `/api/*` → Forward to backend target group
  - Path `/admin/*` → Forward to backend target group
  - Default → Forward to frontend target group

**Where to check:**
- Load Balancer → Listeners tab

### Target Groups (2)

#### Backend Target Group
- **Name:** production-backend-tg
- **ARN:** arn:aws:elasticloadbalancing:us-east-1:322388074242:targetgroup/production-backend-tg/53f6431f37581c66
- **Protocol:** HTTP
- **Port:** 8000
- **Target Type:** IP
- **Health Check:**
  - Path: /health
  - Interval: 300 seconds
  - Timeout: 60 seconds
  - Healthy threshold: 2
  - Unhealthy threshold: 10

#### Frontend Target Group
- **Name:** production-frontend-tg
- **ARN:** arn:aws:elasticloadbalancing:us-east-1:322388074242:targetgroup/production-frontend-tg/81154200cca29f97
- **Protocol:** HTTP
- **Port:** 3000
- **Target Type:** IP
- **Health Check:**
  - Path: /
  - Default settings

**Where to check:**
- AWS Console → EC2 → Target Groups
- Check health status of targets

---

## 📁 7. FILE STORAGE (EFS)

### Elastic File System
- **File System ID:** fs-0718ee8fff27b133a
- **Performance Mode:** General Purpose
- **Throughput Mode:** Bursting
- **Encryption:** Enabled (in transit)
- **VPC:** production-vpc
- **Mount Targets:** 2 (one per AZ)
- **Purpose:** Workspace file storage
- **Cost:** ~$10/month (for 30GB)

**Where to check:**
- AWS Console → EFS → File systems → fs-0718ee8fff27b133a
- URL: https://console.aws.amazon.com/efs/home?region=us-east-1#/file-systems/fs-0718ee8fff27b133a

**Mount Targets:**
- Subnet: production-private-1 (us-east-1a)
- Subnet: production-private-2 (us-east-1b)

---

## 📊 8. MONITORING (CloudWatch)

### Log Groups (2)

#### Backend Logs
- **Name:** /ecs/backend
- **Retention:** 7 days (default)
- **Purpose:** Backend application logs

#### Frontend Logs
- **Name:** /ecs/frontend
- **Retention:** 7 days (default)
- **Purpose:** Frontend application logs

**Where to check:**
- AWS Console → CloudWatch → Log groups
- URL: https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups

**View Logs:**
- Click on log group
- Click on log stream
- See real-time logs

---

## 🔐 9. IAM ROLES

### ECS Task Execution Role
- **Name:** ecsTaskExecutionRole
- **ARN:** arn:aws:iam::322388074242:role/ecsTaskExecutionRole
- **Purpose:** Allows ECS to pull images from ECR and write logs to CloudWatch
- **Policies:**
  - AmazonECSTaskExecutionRolePolicy

**Where to check:**
- AWS Console → IAM → Roles → ecsTaskExecutionRole
- URL: https://console.aws.amazon.com/iam/home#/roles/ecsTaskExecutionRole

---

## 🌍 10. NETWORKING DETAILS

### Elastic IP
- **Allocation ID:** Check NAT Gateway
- **Associated with:** NAT Gateway
- **Purpose:** Static IP for NAT Gateway

### Network ACLs
- **Default NACL:** Allows all traffic
- **Custom NACLs:** None created

---

## 📈 11. RESOURCE MAP

```
Internet
    ↓
[Internet Gateway]
    ↓
[Public Subnets] ← [Application Load Balancer]
    ↓                      ↓
[NAT Gateway]         [Listeners]
    ↓                      ↓
[Private Subnets]     [Target Groups]
    ↓                      ↓
┌───────────────────────────────────────┐
│  [ECS Cluster: production-cluster]    │
│                                       │
│  ┌─────────────┐  ┌─────────────┐   │
│  │  Backend    │  │  Frontend   │   │
│  │  Service    │  │  Service    │   │
│  │  (2 tasks)  │  │  (1 task)   │   │
│  └─────────────┘  └─────────────┘   │
└───────────────────────────────────────┘
    ↓                      ↓
[RDS PostgreSQL]      [ElastiCache Redis]
    ↓                      ↓
[EFS Storage]         [CloudWatch Logs]
```

---

## 💰 12. COST BREAKDOWN

| Service | Resource | Monthly Cost |
|---------|----------|--------------|
| **Compute** | ECS Fargate (3 tasks) | $40 |
| **Database** | RDS PostgreSQL (db.t3.micro) | $15 |
| **Cache** | ElastiCache Redis (cache.t3.micro) | $12 |
| **Networking** | NAT Gateway | $33 |
| **Load Balancer** | Application Load Balancer | $16 |
| **Storage** | EFS (30 GB) | $10 |
| **Container Registry** | ECR (storage) | $1 |
| **Monitoring** | CloudWatch Logs | $2 |
| **Data Transfer** | Outbound data | $5 |
| **TOTAL** | | **~$134/month** |

**Where to check:**
- AWS Console → Billing → Cost Explorer
- URL: https://console.aws.amazon.com/billing/home#/

---

## 🔍 13. HOW TO CHECK EACH SERVICE

### Quick Access URLs

1. **ECS Cluster:**
   https://console.aws.amazon.com/ecs/home?region=us-east-1#/clusters/production-cluster

2. **RDS Database:**
   https://console.aws.amazon.com/rds/home?region=us-east-1#database:id=production-apranova-db

3. **ElastiCache Redis:**
   https://console.aws.amazon.com/elasticache/home?region=us-east-1#redis-group-nodes:id=production-redis

4. **Load Balancer:**
   https://console.aws.amazon.com/ec2/home?region=us-east-1#LoadBalancers:

5. **ECR Repositories:**
   https://console.aws.amazon.com/ecr/repositories?region=us-east-1

6. **VPC:**
   https://console.aws.amazon.com/vpc/home?region=us-east-1#vpcs:

7. **CloudWatch Logs:**
   https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups

8. **EFS:**
   https://console.aws.amazon.com/efs/home?region=us-east-1#/file-systems

9. **Security Groups:**
   https://console.aws.amazon.com/ec2/home?region=us-east-1#SecurityGroups:

10. **Cost Explorer:**
    https://console.aws.amazon.com/billing/home#/

---

## 📋 14. TERRAFORM STATE

All infrastructure is managed by Terraform. The state includes:

- 31 resources created
- State file: `terraform/terraform.tfstate`
- Lock file: `terraform/.terraform.lock.hcl`

**View all resources:**
```bash
cd terraform
terraform state list
```

**View specific resource:**
```bash
terraform state show aws_vpc.main
terraform state show aws_ecs_cluster.main
```

---

## 🎯 15. APPLICATION ENDPOINTS

### Public Endpoints

**Main Application:**
- http://production-alb-1841167835.us-east-1.elb.amazonaws.com

**Frontend:**
- http://production-alb-1841167835.us-east-1.elb.amazonaws.com/

**Backend API:**
- http://production-alb-1841167835.us-east-1.elb.amazonaws.com/api/

**Admin Panel:**
- http://production-alb-1841167835.us-east-1.elb.amazonaws.com/admin/

### Internal Endpoints (Private)

**Database:**
- production-apranova-db.cqzg84imcy8x.us-east-1.rds.amazonaws.com:5432

**Redis:**
- production-redis.ca9eju.0001.use1.cache.amazonaws.com:6379

---

## 📊 16. ARCHITECTURE DIAGRAMS

See these files for visual representations:
- **AWS_ARCHITECTURE_DIAGRAM.md** - Complete architecture diagrams
- **AWS_DEPLOYMENT_PLAN.md** - Detailed architecture explanation
- **DEPLOYMENT_COMPARISON.md** - Architecture comparisons

---

## ✅ 17. VERIFICATION CHECKLIST

Check each service is working:

- [ ] VPC exists and has correct CIDR
- [ ] Subnets are in correct AZs
- [ ] Internet Gateway attached
- [ ] NAT Gateway has Elastic IP
- [ ] Security Groups have correct rules
- [ ] ECS Cluster is active
- [ ] Backend service is running
- [ ] Frontend service is running
- [ ] RDS database is available
- [ ] Redis cluster is available
- [ ] Load Balancer is active
- [ ] Target groups are healthy
- [ ] ECR has both images
- [ ] EFS is available
- [ ] CloudWatch logs are collecting
- [ ] Application is accessible

---

## 🎓 SUMMARY

**Total AWS Services Used:** 10
1. VPC (Networking)
2. ECS (Container Orchestration)
3. RDS (Database)
4. ElastiCache (Cache)
5. ECR (Container Registry)
6. ALB (Load Balancer)
7. EFS (File Storage)
8. CloudWatch (Monitoring)
9. IAM (Access Management)
10. Route 53 (DNS - not configured yet)

**Total Resources Created:** 31
**Monthly Cost:** ~$134
**Region:** us-east-1
**Account:** 322388074242

---

**All services are deployed and accessible through the AWS Console!** 🚀
