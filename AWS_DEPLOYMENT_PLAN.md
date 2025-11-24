# AWS Deployment Plan - ApraNova LMS
## Auto-Scaling VS Code Server Containers with Fast Startup

## 🎯 Objectives

1. **Cost Optimization**: Destroy containers when idle (no active users)
2. **Fast Startup**: Launch containers in < 30 seconds when needed
3. **Auto-Scaling**: Scale based on demand
4. **High Availability**: Multi-AZ deployment
5. **Security**: Isolated student workspaces

## 📐 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         CloudFront CDN                          │
│                    (Static Assets + Caching)                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────────┐
│                     Application Load Balancer                   │
│              (SSL Termination + Path Routing)                   │
└─────┬──────────────────────┬──────────────────────┬─────────────┘
      │                      │                      │
      │                      │                      │
┌─────▼──────┐    ┌──────────▼──────────┐   ┌──────▼──────────────┐
│  Frontend  │    │   Backend API       │   │  Workspace Manager  │
│  (Next.js) │    │   (Django)          │   │  (Lambda + Fargate) │
│            │    │                     │   │                     │
│  ECS        │    │  ECS Fargate       │   │  On-Demand          │
│  Fargate    │    │  Auto-Scaling      │   │  Container Launch   │
└────────────┘    └──────────┬──────────┘   └──────┬──────────────┘
                             │                     │
                    ┌────────┴─────────────────────┴────────┐
                    │                                        │
              ┌─────▼──────┐                    ┌───────────▼────────┐
              │  RDS        │                    │  ECS Fargate       │
              │  PostgreSQL │                    │  (VS Code/Superset)│
              │  Multi-AZ   │                    │  Auto-Terminate    │
              └─────────────┘                    │  After Idle        │
                                                 └────────────────────┘
```

## 🚀 Key Components

### 1. Frontend (Next.js)
- **Service**: ECS Fargate
- **Scaling**: 2-10 tasks
- **Auto-Scaling Trigger**: CPU > 70% or Request Count > 1000/min
- **Health Check**: `/api/health`

### 2. Backend (Django)
- **Service**: ECS Fargate
- **Scaling**: 2-20 tasks
- **Auto-Scaling Trigger**: CPU > 70% or Request Count > 2000/min
- **Health Check**: `/health`

### 3. Database (PostgreSQL)
- **Service**: RDS PostgreSQL 14
- **Instance**: db.t3.medium (start), scale to db.r5.large
- **Multi-AZ**: Yes (High Availability)
- **Backup**: Automated daily backups (7-day retention)
- **Encryption**: At rest and in transit

### 4. Cache (Redis)
- **Service**: ElastiCache Redis
- **Instance**: cache.t3.micro (start), scale to cache.r5.large
- **Cluster Mode**: Enabled for HA
- **Backup**: Daily snapshots

### 5. **Workspace Manager (NEW - Core Innovation)**
- **Service**: Lambda + ECS Fargate (On-Demand)
- **Purpose**: Launch and destroy VS Code/Superset containers
- **Startup Time**: < 30 seconds
- **Auto-Terminate**: After 30 minutes of inactivity

## 💡 Workspace Container Lifecycle (Innovation)

### Problem
- Running 100 student containers 24/7 = **$3,000+/month**
- Students only use workspace 2-3 hours/day
- Wasted resources 21 hours/day

### Solution: On-Demand Container Provisioning

```
Student Request → Lambda Trigger → ECS Task Launch → Ready in 30s
                                         ↓
                                  Activity Monitor
                                         ↓
                              Idle 30 min? → Terminate
```

### Implementation Strategy

#### A. Fast Container Startup (< 30 seconds)

**Method 1: Pre-Warmed Container Pool (Recommended)**
- Keep 2-3 "warm" containers ready
- When student requests workspace, assign from pool
- Immediately launch replacement container
- Cost: ~$50/month for warm pool vs $3,000/month for all containers

**Method 2: Optimized Image + EFS**
- Use AWS EFS for persistent student data
- Optimized Docker image (< 500MB)
- ECS Fargate Spot for cost savings (70% cheaper)
- Startup: 25-35 seconds

**Method 3: Hybrid (Best Performance)**
- Warm pool (2 containers) for instant access
- On-demand launch for overflow
- Auto-scale warm pool during peak hours (9 AM - 9 PM)

#### B. Auto-Termination Logic

**Activity Monitoring**
```python
# Lambda function checks every 5 minutes
def check_workspace_activity():
    for container in active_containers:
        last_activity = get_last_activity(container)
        idle_time = now() - last_activity
        
        if idle_time > 30_minutes:
            # Graceful shutdown
            save_workspace_state(container)
            terminate_container(container)
            notify_student("Workspace saved and stopped")
```

**Activity Tracking**
- HTTP requests to workspace
- WebSocket connections (VS Code)
- File modifications
- Terminal commands

#### C. State Persistence

**Student Data Storage**
- **EFS (Elastic File System)**: Persistent workspace files
- **S3**: Backup snapshots (daily)
- **RDS**: Workspace metadata (status, last_activity, etc.)

**Fast Resume**
- Student data always available on EFS
- New container mounts same EFS volume
- Appears as "resume" to student

## 📦 Container Images

### VS Code Server (Full Stack Development)
```dockerfile
FROM codercom/code-server:latest

# Pre-install common extensions
RUN code-server --install-extension dbaeumer.vscode-eslint \
    && code-server --install-extension esbenp.prettier-vscode \
    && code-server --install-extension ms-python.python

# Pre-install tools
RUN apt-get update && apt-get install -y \
    git nodejs npm python3 pip \
    && rm -rf /var/lib/apt/lists/*

# Optimize for fast startup
RUN code-server --list-extensions

EXPOSE 8080
CMD ["code-server", "--auth", "none", "--bind-addr", "0.0.0.0:8080"]
```

**Image Size**: ~800MB (optimized from 1.2GB)
**Startup Time**: 15-20 seconds on Fargate

### Apache Superset (Data Professional)
```dockerfile
FROM apache/superset:latest

# Pre-initialize database
RUN superset db upgrade && \
    superset init

# Pre-load examples
ENV SUPERSET_LOAD_EXAMPLES=yes

EXPOSE 8088
CMD ["superset", "run", "-h", "0.0.0.0", "-p", "8088"]
```

**Image Size**: ~1.1GB
**Startup Time**: 25-30 seconds on Fargate

## 🔧 Infrastructure as Code (Terraform)

### Directory Structure
```
terraform/
├── main.tf                 # Main configuration
├── variables.tf            # Input variables
├── outputs.tf              # Output values
├── modules/
│   ├── vpc/               # VPC, Subnets, NAT
│   ├── ecs/               # ECS Cluster, Services
│   ├── rds/               # PostgreSQL Database
│   ├── elasticache/       # Redis Cache
│   ├── alb/               # Application Load Balancer
│   ├── workspace/         # Workspace Manager (Lambda + ECS)
│   ├── efs/               # Elastic File System
│   └── monitoring/        # CloudWatch, Alarms
└── environments/
    ├── dev/
    ├── staging/
    └── production/
```

## 💰 Cost Estimation

### Traditional Approach (Always-On Containers)
```
100 students × 24/7 containers
- ECS Fargate: $0.04/hour × 100 × 730 hours = $2,920/month
- EFS Storage: 100GB × $0.30 = $30/month
- Data Transfer: ~$100/month
Total: ~$3,050/month
```

### Optimized Approach (On-Demand + Warm Pool)
```
Warm Pool: 3 containers × 24/7
- ECS Fargate: $0.04/hour × 3 × 730 hours = $87.60/month

On-Demand: 100 students × 3 hours/day average
- ECS Fargate: $0.04/hour × 100 × 90 hours = $360/month

Lambda (Workspace Manager): 
- 10,000 invocations/month × $0.20/1M = $0.002/month

EFS Storage: 100GB × $0.30 = $30/month
S3 Backups: 500GB × $0.023 = $11.50/month
Data Transfer: ~$50/month

Total: ~$539/month
Savings: $2,511/month (82% reduction!)
```

### Complete Infrastructure Cost (Production)
```
Core Services:
- Frontend (ECS): 2 tasks × $0.04/hour × 730 = $58.40
- Backend (ECS): 2 tasks × $0.04/hour × 730 = $58.40
- RDS (db.t3.medium): $0.068/hour × 730 = $49.64
- ElastiCache (cache.t3.micro): $0.017/hour × 730 = $12.41
- ALB: $0.0225/hour × 730 = $16.43
- NAT Gateway: $0.045/hour × 730 = $32.85

Workspace Services:
- Warm Pool + On-Demand: $539/month (from above)

Storage:
- EFS: $30/month
- S3: $11.50/month
- RDS Storage: 100GB × $0.115 = $11.50

Monitoring & Logs:
- CloudWatch: ~$20/month
- CloudTrail: ~$5/month

Total Monthly Cost: ~$845/month
```

**Scaling Projections:**
- 500 students: ~$1,800/month
- 1,000 students: ~$3,200/month
- 5,000 students: ~$12,000/month

## 🏗️ Deployment Steps

### Phase 1: Infrastructure Setup (Week 1)

#### Step 1: VPC and Networking
```bash
cd terraform/modules/vpc
terraform init
terraform plan
terraform apply
```

**Creates:**
- VPC with CIDR 10.0.0.0/16
- 3 Public Subnets (Multi-AZ)
- 3 Private Subnets (Multi-AZ)
- Internet Gateway
- NAT Gateways (Multi-AZ)
- Route Tables

#### Step 2: RDS PostgreSQL
```bash
cd terraform/modules/rds
terraform apply
```

**Creates:**
- RDS PostgreSQL 14 (Multi-AZ)
- Security Groups
- Parameter Groups
- Subnet Groups

#### Step 3: ElastiCache Redis
```bash
cd terraform/modules/elasticache
terraform apply
```

#### Step 4: EFS for Workspace Storage
```bash
cd terraform/modules/efs
terraform apply
```

**Creates:**
- EFS File System
- Mount Targets in each AZ
- Access Points for each student

### Phase 2: Application Deployment (Week 2)

#### Step 5: ECR Repositories
```bash
# Create repositories
aws ecr create-repository --repository-name apranova/frontend
aws ecr create-repository --repository-name apranova/backend
aws ecr create-repository --repository-name apranova/code-server
aws ecr create-repository --repository-name apranova/superset

# Build and push images
docker build -t apranova/frontend:latest ./frontend
docker tag apranova/frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/apranova/frontend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/apranova/frontend:latest

# Repeat for backend, code-server, superset
```

#### Step 6: ECS Cluster and Services
```bash
cd terraform/modules/ecs
terraform apply
```

**Creates:**
- ECS Cluster
- Task Definitions (Frontend, Backend)
- ECS Services with Auto-Scaling
- CloudWatch Log Groups

#### Step 7: Application Load Balancer
```bash
cd terraform/modules/alb
terraform apply
```

**Creates:**
- ALB with SSL certificate
- Target Groups
- Listener Rules
- Health Checks

### Phase 3: Workspace Manager (Week 3)

#### Step 8: Lambda Workspace Manager
```bash
cd terraform/modules/workspace
terraform apply
```

**Creates:**
- Lambda function for workspace lifecycle
- EventBridge rules (activity monitoring)
- IAM roles and policies
- DynamoDB table (workspace state)

#### Step 9: Warm Pool Setup
```bash
# Deploy warm pool containers
aws ecs run-task \
  --cluster apranova-cluster \
  --task-definition workspace-vscode:latest \
  --count 3 \
  --launch-type FARGATE
```

### Phase 4: Monitoring and Optimization (Week 4)

#### Step 10: CloudWatch Dashboards
```bash
cd terraform/modules/monitoring
terraform apply
```

**Creates:**
- CloudWatch Dashboards
- Alarms (CPU, Memory, Errors)
- SNS Topics for alerts
- Log Insights queries

#### Step 11: Auto-Scaling Policies
```bash
# Configure auto-scaling for backend
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --resource-id service/apranova-cluster/backend \
  --scalable-dimension ecs:service:DesiredCount \
  --min-capacity 2 \
  --max-capacity 20

aws application-autoscaling put-scaling-policy \
  --policy-name backend-cpu-scaling \
  --service-namespace ecs \
  --resource-id service/apranova-cluster/backend \
  --scalable-dimension ecs:service:DesiredCount \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration file://scaling-policy.json
```

## 🔐 Security Best Practices

### 1. Network Security
- Private subnets for all application containers
- NAT Gateway for outbound internet access
- Security Groups with least privilege
- VPC Flow Logs enabled

### 2. Data Encryption
- RDS encryption at rest (KMS)
- EFS encryption at rest (KMS)
- S3 encryption at rest (SSE-S3)
- TLS 1.2+ for all traffic

### 3. Access Control
- IAM roles for ECS tasks (no hardcoded credentials)
- Secrets Manager for sensitive data
- Parameter Store for configuration
- MFA for AWS console access

### 4. Student Isolation
- Each student gets unique EFS Access Point
- Network isolation via Security Groups
- Resource limits per container (CPU, Memory)
- No privileged containers

### 5. Compliance
- CloudTrail for audit logs
- AWS Config for compliance monitoring
- GuardDuty for threat detection
- AWS WAF for web application firewall

## 📊 Monitoring and Alerts

### Key Metrics to Monitor

**Application Metrics:**
- Request latency (p50, p95, p99)
- Error rate (4xx, 5xx)
- Active users
- Workspace launch time
- Container startup time

**Infrastructure Metrics:**
- CPU utilization
- Memory utilization
- Network throughput
- Disk I/O
- Database connections

**Cost Metrics:**
- Daily spend by service
- Cost per student
- Idle container time
- Warm pool utilization

### Alert Thresholds

**Critical Alerts (PagerDuty):**
- Error rate > 5%
- Database CPU > 90%
- Any service down
- Workspace launch failure rate > 10%

**Warning Alerts (Email):**
- CPU > 80% for 10 minutes
- Memory > 85%
- Disk space < 20%
- Warm pool depleted

## 🚀 CI/CD Pipeline

### GitHub Actions Workflow

```yaml
name: Deploy to AWS

on:
  push:
    branches: [main, staging]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
      
      - name: Build and push Docker images
        run: |
          docker build -t apranova/backend:${{ github.sha }} ./backend
          docker push ${{ steps.login-ecr.outputs.registry }}/apranova/backend:${{ github.sha }}
      
      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster apranova-cluster \
            --service backend \
            --force-new-deployment
```

## 📝 Workspace Manager Lambda Function

```python
# lambda/workspace_manager.py
import boto3
import os
from datetime import datetime, timedelta

ecs = boto3.client('ecs')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('workspace-state')

CLUSTER_NAME = os.environ['ECS_CLUSTER']
IDLE_TIMEOUT = 30  # minutes

def lambda_handler(event, context):
    """
    Handles workspace lifecycle:
    1. Launch workspace on demand
    2. Monitor activity
    3. Terminate idle workspaces
    """
    
    action = event.get('action')
    
    if action == 'launch':
        return launch_workspace(event)
    elif action == 'monitor':
        return monitor_workspaces()
    elif action == 'terminate':
        return terminate_workspace(event)
    
def launch_workspace(event):
    """Launch workspace container from warm pool or on-demand"""
    user_id = event['user_id']
    workspace_type = event['workspace_type']  # 'vscode' or 'superset'
    
    # Check warm pool first
    warm_container = get_warm_container(workspace_type)
    
    if warm_container:
        # Assign warm container to user
        assign_container(warm_container, user_id)
        # Launch replacement warm container
        launch_warm_container(workspace_type)
        return {
            'status': 'ready',
            'url': warm_container['url'],
            'startup_time': 0
        }
    else:
        # Launch on-demand
        task_arn = launch_ecs_task(user_id, workspace_type)
        wait_for_task_running(task_arn)
        url = get_task_url(task_arn)
        
        # Record in DynamoDB
        table.put_item(Item={
            'user_id': user_id,
            'task_arn': task_arn,
            'workspace_type': workspace_type,
            'status': 'running',
            'last_activity': datetime.now().isoformat(),
            'url': url
        })
        
        return {
            'status': 'ready',
            'url': url,
            'startup_time': 25  # seconds
        }

def monitor_workspaces():
    """Check all running workspaces for inactivity"""
    response = table.scan(
        FilterExpression='#status = :running',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':running': 'running'}
    )
    
    terminated_count = 0
    
    for item in response['Items']:
        last_activity = datetime.fromisoformat(item['last_activity'])
        idle_time = datetime.now() - last_activity
        
        if idle_time > timedelta(minutes=IDLE_TIMEOUT):
            # Terminate idle workspace
            terminate_workspace({'task_arn': item['task_arn']})
            terminated_count += 1
    
    return {
        'terminated': terminated_count,
        'active': len(response['Items']) - terminated_count
    }

def terminate_workspace(event):
    """Gracefully terminate workspace and save state"""
    task_arn = event['task_arn']
    
    # Save workspace state to S3
    save_workspace_snapshot(task_arn)
    
    # Stop ECS task
    ecs.stop_task(
        cluster=CLUSTER_NAME,
        task=task_arn,
        reason='Idle timeout'
    )
    
    # Update DynamoDB
    table.update_item(
        Key={'task_arn': task_arn},
        UpdateExpression='SET #status = :stopped',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':stopped': 'stopped'}
    )
    
    return {'status': 'terminated'}

def launch_ecs_task(user_id, workspace_type):
    """Launch ECS Fargate task for workspace"""
    task_definition = f'workspace-{workspace_type}'
    
    response = ecs.run_task(
        cluster=CLUSTER_NAME,
        taskDefinition=task_definition,
        launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': os.environ['SUBNETS'].split(','),
                'securityGroups': [os.environ['SECURITY_GROUP']],
                'assignPublicIp': 'DISABLED'
            }
        },
        overrides={
            'containerOverrides': [{
                'name': 'workspace',
                'environment': [
                    {'name': 'USER_ID', 'value': str(user_id)},
                    {'name': 'EFS_PATH', 'value': f'/mnt/efs/student_{user_id}'}
                ]
            }]
        },
        tags=[
            {'key': 'user_id', 'value': str(user_id)},
            {'key': 'type', 'value': workspace_type}
        ]
    )
    
    return response['tasks'][0]['taskArn']
```

## 🔄 Disaster Recovery

### Backup Strategy
- **RDS**: Automated daily backups (7-day retention)
- **EFS**: AWS Backup daily snapshots (30-day retention)
- **S3**: Versioning enabled, lifecycle policy to Glacier after 90 days
- **Configuration**: Terraform state in S3 with versioning

### Recovery Procedures
1. **Database Failure**: Restore from latest RDS snapshot (< 15 minutes)
2. **Region Failure**: Failover to secondary region (manual, ~1 hour)
3. **Data Corruption**: Restore from S3 versioned backups
4. **Complete Disaster**: Rebuild from Terraform + latest backups (< 4 hours)

## 📈 Scaling Strategy

### Horizontal Scaling
- **Frontend**: Auto-scale 2-10 tasks based on CPU
- **Backend**: Auto-scale 2-20 tasks based on CPU + Request Count
- **Workspaces**: On-demand launch, no fixed limit

### Vertical Scaling
- **RDS**: Start with db.t3.medium, scale to db.r5.xlarge as needed
- **ElastiCache**: Start with cache.t3.micro, scale to cache.r5.large
- **ECS Tasks**: 0.5 vCPU / 1GB RAM → 2 vCPU / 4GB RAM

### Database Scaling
- Read replicas for reporting queries
- Connection pooling (PgBouncer)
- Query optimization and indexing

## 🎓 Student Experience

### Workspace Launch Flow
1. Student clicks "Launch Workspace" button
2. Frontend sends request to Backend API
3. Backend calls Lambda Workspace Manager
4. Lambda checks warm pool:
   - **If available**: Instant assignment (< 2 seconds)
   - **If not**: Launch new container (< 30 seconds)
5. Student redirected to workspace URL
6. VS Code/Superset loads in browser

### Auto-Save and Resume
- All files saved to EFS automatically
- Container termination is transparent
- Next launch resumes from last state
- No data loss

## 🔧 Maintenance Windows

### Planned Maintenance
- **Schedule**: Sundays 2 AM - 4 AM EST
- **Notification**: 48 hours advance notice
- **Process**: Rolling updates (zero downtime)

### Emergency Maintenance
- Immediate notification via email/SMS
- Estimated downtime: < 30 minutes
- Automatic rollback if issues detected

## 📞 Support and Troubleshooting

### Common Issues

**Issue: Workspace won't launch**
- Check warm pool status
- Verify ECS task limits
- Check CloudWatch logs

**Issue: Slow performance**
- Check CPU/Memory metrics
- Scale up ECS tasks
- Optimize database queries

**Issue: High costs**
- Review idle container metrics
- Adjust idle timeout
- Optimize warm pool size

## 🎯 Success Metrics

### Performance KPIs
- Workspace launch time: < 30 seconds (95th percentile)
- API response time: < 200ms (95th percentile)
- Uptime: > 99.9%
- Error rate: < 0.1%

### Cost KPIs
- Cost per student: < $10/month
- Infrastructure efficiency: > 80%
- Idle container time: < 5%

### User Experience KPIs
- Student satisfaction: > 4.5/5
- Workspace availability: > 99.5%
- Support tickets: < 5% of users

## 📚 Next Steps

1. **Review and approve this plan**
2. **Set up AWS account and billing alerts**
3. **Create Terraform configurations**
4. **Build and optimize Docker images**
5. **Deploy to staging environment**
6. **Load testing and optimization**
7. **Production deployment**
8. **Monitor and iterate**

---

**Estimated Timeline**: 4-6 weeks
**Estimated Cost**: $845/month (100 students)
**Cost Savings**: 82% vs traditional approach
**Startup Time**: < 30 seconds
**Scalability**: Up to 10,000 students

