#!/bin/bash
# Basic AWS Deployment Script
# Deploys: VPC, ECS, RDS, Redis, ALB, EFS only

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}ApraNova Basic AWS Deployment${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check AWS credentials
echo -e "${YELLOW}Checking AWS credentials...${NC}"
if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}AWS credentials not configured!${NC}"
    exit 1
fi

AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=${AWS_REGION:-us-east-1}

echo -e "${GREEN}✓ AWS Account: $AWS_ACCOUNT_ID${NC}"
echo -e "${GREEN}✓ Region: $AWS_REGION${NC}"
echo ""

# Set database password
if [ -z "$DB_PASSWORD" ]; then
    echo -e "${YELLOW}Enter database password:${NC}"
    read -s DB_PASSWORD
    export DB_PASSWORD
fi

# Step 1: Build Docker images
echo -e "${GREEN}Step 1: Building Docker images...${NC}"
docker build -t apranova/backend:latest ./backend
docker build -t apranova/frontend:latest ./frontend

# Step 2: Create ECR repositories
echo -e "${GREEN}Step 2: Creating ECR repositories...${NC}"
for repo in backend frontend; do
    aws ecr describe-repositories --repository-names apranova/$repo --region $AWS_REGION 2>/dev/null || \
    aws ecr create-repository --repository-name apranova/$repo --region $AWS_REGION
done

# Step 3: Login to ECR
echo -e "${GREEN}Step 3: Logging into ECR...${NC}"
aws ecr get-login-password --region $AWS_REGION | \
    docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Step 4: Tag and push images
echo -e "${GREEN}Step 4: Pushing images to ECR...${NC}"
for image in backend frontend; do
    docker tag apranova/$image:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/apranova/$image:latest
    docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/apranova/$image:latest
done

# Step 5: Deploy infrastructure
echo -e "${GREEN}Step 5: Deploying infrastructure with Terraform...${NC}"
cd terraform

# Initialize Terraform
terraform init

# Create terraform.tfvars
cat > terraform.tfvars <<EOF
aws_region = "$AWS_REGION"
environment = "production"
db_password = "$DB_PASSWORD"
EOF

# Plan
terraform plan -var-file=terraform.tfvars -out=tfplan

# Apply
echo -e "${YELLOW}Ready to deploy infrastructure. Continue? (yes/no)${NC}"
read -r confirm
if [ "$confirm" = "yes" ]; then
    terraform apply tfplan
else
    echo -e "${RED}Deployment cancelled${NC}"
    exit 1
fi

cd ..

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Access your application:"
echo "  Frontend: http://$(cd terraform && terraform output -raw alb_dns_name)"
echo ""
echo "Next steps:"
echo "  1. Deploy ECS tasks (backend and frontend)"
echo "  2. Run database migrations"
echo "  3. Create admin user"
echo ""
