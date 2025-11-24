#!/bin/bash
# AWS Deployment Script for ApraNova LMS
# Deploys infrastructure and application to AWS

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT=${1:-production}
AWS_REGION=${AWS_REGION:-us-east-1}
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}ApraNova AWS Deployment${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "Environment: ${YELLOW}$ENVIRONMENT${NC}"
echo -e "Region: ${YELLOW}$AWS_REGION${NC}"
echo -e "Account: ${YELLOW}$AWS_ACCOUNT_ID${NC}"
echo ""

# Step 1: Build Docker Images
echo -e "${GREEN}Step 1: Building Docker Images${NC}"
echo "Building backend..."
docker build -t apranova/backend:latest ./backend

echo "Building frontend..."
docker build -t apranova/frontend:latest ./frontend

echo "Building VS Code workspace..."
docker build -t apranova/vscode:latest ./backend/apra-nova-code-server

echo "Building Superset workspace..."
docker build -t apranova/superset:latest -f docker/Dockerfile.superset .

# Step 2: Create ECR Repositories
echo -e "${GREEN}Step 2: Creating ECR Repositories${NC}"
for repo in backend frontend vscode superset; do
    aws ecr describe-repositories --repository-names apranova/$repo --region $AWS_REGION 2>/dev/null || \
    aws ecr create-repository --repository-name apranova/$repo --region $AWS_REGION
done

# Step 3: Login to ECR
echo -e "${GREEN}Step 3: Logging into ECR${NC}"
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Step 4: Tag and Push Images
echo -e "${GREEN}Step 4: Pushing Images to ECR${NC}"
for image in backend frontend vscode superset; do
    echo "Pushing $image..."
    docker tag apranova/$image:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/apranova/$image:latest
    docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/apranova/$image:latest
done

# Step 5: Package Lambda Function
echo -e "${GREEN}Step 5: Packaging Lambda Function${NC}"
cd lambda/workspace_manager
pip install -r requirements.txt -t .
zip -r ../lambda.zip .
cd ../..
mv lambda/lambda.zip terraform/modules/workspace/

# Step 6: Initialize Terraform
echo -e "${GREEN}Step 6: Initializing Terraform${NC}"
cd terraform
terraform init

# Step 7: Create Terraform Variables
echo -e "${GREEN}Step 7: Creating Terraform Variables${NC}"
cat > terraform.tfvars <<EOF
aws_region = "$AWS_REGION"
environment = "$ENVIRONMENT"

# Database
database_username = "$DB_USERNAME"
database_password = "$DB_PASSWORD"

# Docker Images
backend_image = "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/apranova/backend:latest"
frontend_image = "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/apranova/frontend:latest"
vscode_image = "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/apranova/vscode:latest"
superset_image = "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/apranova/superset:latest"

# SSL Certificate
ssl_certificate_arn = "$SSL_CERT_ARN"

# Monitoring
alert_email = "$ALERT_EMAIL"
EOF

# Step 8: Plan Terraform
echo -e "${GREEN}Step 8: Planning Terraform Deployment${NC}"
terraform plan -out=tfplan

# Step 9: Confirm Deployment
echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}Ready to Deploy!${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""
echo "This will create the following resources:"
echo "  - VPC with public/private subnets"
echo "  - RDS PostgreSQL (Multi-AZ)"
echo "  - ElastiCache Redis"
echo "  - ECS Cluster with Fargate"
echo "  - Application Load Balancer"
echo "  - Lambda Workspace Manager"
echo "  - EFS for workspace storage"
echo "  - CloudWatch monitoring"
echo ""
read -p "Continue with deployment? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo -e "${RED}Deployment cancelled${NC}"
    exit 1
fi

# Step 10: Apply Terraform
echo -e "${GREEN}Step 10: Applying Terraform${NC}"
terraform apply tfplan

# Step 11: Get Outputs
echo -e "${GREEN}Step 11: Deployment Complete!${NC}"
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Information${NC}"
echo -e "${GREEN}========================================${NC}"
terraform output

# Step 12: Initialize Database
echo -e "${GREEN}Step 12: Initializing Database${NC}"
BACKEND_TASK=$(aws ecs list-tasks --cluster $ENVIRONMENT-cluster --service-name backend --query 'taskArns[0]' --output text)
aws ecs execute-command \
    --cluster $ENVIRONMENT-cluster \
    --task $BACKEND_TASK \
    --container backend \
    --interactive \
    --command "python manage.py migrate"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Access your application at:"
echo "  Frontend: https://$(terraform output -raw alb_dns_name)"
echo "  Backend API: https://$(terraform output -raw alb_dns_name)/api"
echo ""
echo "Next steps:"
echo "  1. Configure DNS to point to ALB"
echo "  2. Create admin user"
echo "  3. Configure email service"
echo "  4. Test workspace provisioning"
echo ""
