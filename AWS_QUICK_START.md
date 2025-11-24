# AWS Quick Start Guide

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** installed and configured
3. **Terraform** >= 1.0 installed
4. **Docker** installed locally
5. **Domain name** (optional, for SSL)

## Environment Variables

Create a `.env.aws` file:

```bash
# AWS Configuration
export AWS_REGION=us-east-1
export AWS_ACCOUNT_ID=your-account-id

# Database Credentials
export DB_USERNAME=apranova_admin
export DB_PASSWORD=your-secure-password-here

# SSL Certificate ARN (from AWS Certificate Manager)
export SSL_CERT_ARN=arn:aws:acm:us-east-1:account:certificate/xxx

# Alert Email
export ALERT_EMAIL=admin@yourdomain.com

# Application Secrets
export DJANGO_SECRET_KEY=your-django-secret-key
export STRIPE_SECRET_KEY=your-stripe-secret-key
```

Load environment variables:
```bash
source .env.aws
```

## Quick Deployment

### Option 1: Automated Deployment (Recommended)

```bash
# Make script executable
chmod +x deploy-aws.sh

# Deploy to production
./deploy-aws.sh production
```

This script will:
1. ✅ Build Docker images
2. ✅ Create ECR repositories
3. ✅ Push images to ECR
4. ✅ Package Lambda function
5. ✅ Deploy infrastructure with Terraform
6. ✅ Initialize database
7. ✅ Display access URLs

**Estimated Time**: 15-20 minutes

### Option 2: Manual Deployment

#### Step 1: Build and Push Images

```bash
# Build images
docker build -t apranova/backend:latest ./backend
docker build -t apranova/frontend:latest ./frontend
docker build -t apranova/vscode:latest ./backend/apra-nova-code-server

# Login to ECR
aws ecr get-login-password --region $AWS_REGION | \
  docker login --username AWS --password-stdin \
  $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Tag and push
docker tag apranova/backend:latest \
  $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/apranova/backend:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/apranova/backend:latest

# Repeat for frontend and vscode
```

#### Step 2: Deploy Infrastructure

```bash
cd terraform

# Initialize Terraform
terraform init

# Create terraform.tfvars
cat > terraform.tfvars <<EOF
aws_region = "us-east-1"
environment = "production"
database_username = "$DB_USERNAME"
database_password = "$DB_PASSWORD"
backend_image = "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/apranova/backend:latest"
frontend_image = "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/apranova/frontend:latest"
vscode_image = "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/apranova/vscode:latest"
superset_image = "apache/superset:latest"
ssl_certificate_arn = "$SSL_CERT_ARN"
alert_email = "$ALERT_EMAIL"
EOF

# Plan
terraform plan -out=tfplan

# Apply
terraform apply tfplan
```

#### Step 3: Initialize Database

```bash
# Get backend task ARN
TASK_ARN=$(aws ecs list-tasks \
  --cluster production-cluster \
  --service-name backend \
  --query 'taskArns[0]' \
  --output text)

# Run migrations
aws ecs execute-command \
  --cluster production-cluster \
  --task $TASK_ARN \
  --container backend \
  --interactive \
  --command "python manage.py migrate"

# Create superuser
aws ecs execute-command \
  --cluster production-cluster \
  --task $TASK_ARN \
  --container backend \
  --interactive \
  --command "python manage.py createsuperuser"
```

## Post-Deployment Configuration

### 1. Configure DNS

Get ALB DNS name:
```bash
cd terraform
terraform output alb_dns_name
```

Create CNAME record:
```
apranova.com -> your-alb-dns-name.us-east-1.elb.amazonaws.com
```

### 2. Test Workspace Provisioning

```bash
# Invoke Lambda to test
aws lambda invoke \
  --function-name production-workspace-manager \
  --payload '{"action":"warm_pool"}' \
  response.json

cat response.json
```

### 3. Monitor Deployment

```bash
# Check ECS services
aws ecs describe-services \
  --cluster production-cluster \
  --services backend frontend

# Check CloudWatch logs
aws logs tail /ecs/production/backend --follow

# Check workspace manager logs
aws logs tail /aws/lambda/production-workspace-manager --follow
```

### 4. Verify Application

```bash
# Get ALB URL
ALB_URL=$(cd terraform && terraform output -raw alb_dns_name)

# Test backend health
curl https://$ALB_URL/health

# Test frontend
curl https://$ALB_URL/

# Test workspace launch (requires auth token)
curl -X POST https://$ALB_URL/api/workspace/create/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

## Cost Optimization

### Enable Auto-Scaling

Auto-scaling is configured by default:
- **Backend**: 2-20 tasks based on CPU
- **Frontend**: 2-10 tasks based on CPU
- **Workspaces**: On-demand with warm pool

### Monitor Costs

```bash
# View current month costs
aws ce get-cost-and-usage \
  --time-period Start=$(date -d "$(date +%Y-%m-01)" +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=SERVICE

# Set up billing alerts
aws cloudwatch put-metric-alarm \
  --alarm-name high-billing \
  --alarm-description "Alert when monthly bill exceeds $1000" \
  --metric-name EstimatedCharges \
  --namespace AWS/Billing \
  --statistic Maximum \
  --period 21600 \
  --evaluation-periods 1 \
  --threshold 1000 \
  --comparison-operator GreaterThanThreshold
```

### Adjust Warm Pool Size

Edit `terraform/terraform.tfvars`:
```hcl
# Reduce warm pool during off-hours
warm_pool_size = 1  # Default: 3

# Increase idle timeout to save costs
idle_timeout_minutes = 45  # Default: 30
```

Apply changes:
```bash
cd terraform
terraform apply
```

## Scaling

### Horizontal Scaling

Increase task count:
```bash
# Scale backend
aws ecs update-service \
  --cluster production-cluster \
  --service backend \
  --desired-count 10

# Scale frontend
aws ecs update-service \
  --cluster production-cluster \
  --service frontend \
  --desired-count 5
```

### Vertical Scaling

Edit `terraform/terraform.tfvars`:
```hcl
# Increase backend resources
backend_cpu = 1024      # Default: 512
backend_memory = 2048   # Default: 1024

# Increase database
rds_instance_class = "db.r5.large"  # Default: db.t3.medium
```

Apply:
```bash
cd terraform
terraform apply
```

## Backup and Recovery

### Database Backup

Automated daily backups are enabled by default (7-day retention).

Manual backup:
```bash
aws rds create-db-snapshot \
  --db-instance-identifier production-apranova-db \
  --db-snapshot-identifier manual-backup-$(date +%Y%m%d)
```

Restore from backup:
```bash
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier production-apranova-db-restored \
  --db-snapshot-identifier manual-backup-20241123
```

### EFS Backup

Automated daily backups via AWS Backup.

Manual backup:
```bash
aws backup start-backup-job \
  --backup-vault-name Default \
  --resource-arn arn:aws:elasticfilesystem:us-east-1:account:file-system/fs-xxx \
  --iam-role-arn arn:aws:iam::account:role/service-role/AWSBackupDefaultServiceRole
```

## Troubleshooting

### Workspace Won't Launch

```bash
# Check Lambda logs
aws logs tail /aws/lambda/production-workspace-manager --follow

# Check ECS task status
aws ecs list-tasks --cluster production-cluster --family workspace-vscode

# Check warm pool
aws lambda invoke \
  --function-name production-workspace-manager \
  --payload '{"action":"warm_pool"}' \
  response.json
```

### High Costs

```bash
# Check running tasks
aws ecs list-tasks --cluster production-cluster

# Check idle workspaces
aws dynamodb scan \
  --table-name production-workspace-state \
  --filter-expression "#status = :running" \
  --expression-attribute-names '{"#status":"status"}' \
  --expression-attribute-values '{":running":{"S":"running"}}'

# Manually terminate idle workspaces
aws lambda invoke \
  --function-name production-workspace-manager \
  --payload '{"action":"monitor"}' \
  response.json
```

### Database Connection Issues

```bash
# Check RDS status
aws rds describe-db-instances \
  --db-instance-identifier production-apranova-db

# Check security groups
aws ec2 describe-security-groups \
  --filters "Name=tag:Name,Values=production-rds-sg"

# Test connection from backend
aws ecs execute-command \
  --cluster production-cluster \
  --task $TASK_ARN \
  --container backend \
  --interactive \
  --command "python manage.py dbshell"
```

## Monitoring Dashboard

Access CloudWatch Dashboard:
```bash
# Get dashboard URL
echo "https://console.aws.amazon.com/cloudwatch/home?region=$AWS_REGION#dashboards:name=ApraNova-Production"
```

Key metrics to monitor:
- **Workspace Launch Time**: Should be < 30 seconds
- **Active Workspaces**: Number of running containers
- **Warm Pool Size**: Should match configured size
- **API Response Time**: Should be < 200ms
- **Error Rate**: Should be < 0.1%
- **Cost per Day**: Track daily spending

## Cleanup

To destroy all resources:

```bash
cd terraform

# Destroy infrastructure
terraform destroy

# Delete ECR images
for repo in backend frontend vscode superset; do
    aws ecr delete-repository \
      --repository-name apranova/$repo \
      --force \
      --region $AWS_REGION
done

# Delete S3 buckets (if any)
aws s3 rb s3://apranova-terraform-state --force
```

**Warning**: This will delete all data including databases and backups!

## Support

For issues:
1. Check CloudWatch logs
2. Review Terraform state
3. Verify security groups
4. Check IAM permissions
5. Contact AWS Support

## Next Steps

1. ✅ Configure custom domain
2. ✅ Set up CI/CD pipeline
3. ✅ Configure email service (SES)
4. ✅ Enable CloudTrail for audit logs
5. ✅ Set up monitoring alerts
6. ✅ Configure backup retention
7. ✅ Load testing
8. ✅ Security audit

---

**Estimated Monthly Cost**: $845 (100 students)
**Deployment Time**: 15-20 minutes
**Uptime SLA**: 99.9%
