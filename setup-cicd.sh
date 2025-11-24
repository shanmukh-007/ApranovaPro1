#!/bin/bash
# Setup CI/CD Pipeline for GitHub Actions

set -e

echo "🚀 Setting up CI/CD Pipeline for GitHub Actions"
echo ""

# Step 1: Create IAM user
echo "📝 Step 1: Creating IAM user for GitHub Actions..."
aws iam create-user --user-name github-actions-deployer 2>/dev/null || echo "User already exists"

# Step 2: Create IAM policy
echo "📝 Step 2: Creating IAM policy..."
cat > /tmp/github-actions-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ecs:DescribeTaskDefinition",
        "ecs:RegisterTaskDefinition",
        "ecs:UpdateService",
        "ecs:DescribeServices"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "iam:PassRole"
      ],
      "Resource": "arn:aws:iam::322388074242:role/ecsTaskExecutionRole"
    }
  ]
}
EOF

aws iam put-user-policy \
  --user-name github-actions-deployer \
  --policy-name GitHubActionsDeployPolicy \
  --policy-document file:///tmp/github-actions-policy.json

echo "✅ IAM policy attached"

# Step 3: Create access key
echo ""
echo "📝 Step 3: Creating access key..."
echo ""
echo "⚠️  IMPORTANT: Save these credentials securely!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if access key already exists
EXISTING_KEYS=$(aws iam list-access-keys --user-name github-actions-deployer --query 'AccessKeyMetadata[*].AccessKeyId' --output text)

if [ -n "$EXISTING_KEYS" ]; then
    echo "⚠️  Access keys already exist for this user:"
    echo "$EXISTING_KEYS"
    echo ""
    read -p "Do you want to create a new access key? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Skipping access key creation"
        exit 0
    fi
fi

ACCESS_KEY_OUTPUT=$(aws iam create-access-key --user-name github-actions-deployer)

echo "🔑 AWS Credentials for GitHub Secrets:"
echo ""
echo "AWS_ACCESS_KEY_ID:"
echo "$ACCESS_KEY_OUTPUT" | grep -o '"AccessKeyId": "[^"]*' | cut -d'"' -f4
echo ""
echo "AWS_SECRET_ACCESS_KEY:"
echo "$ACCESS_KEY_OUTPUT" | grep -o '"SecretAccessKey": "[^"]*' | cut -d'"' -f4
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Go to: https://github.com/shanmukh-007/ApranovaPro1/settings/secrets/actions"
echo "2. Click 'New repository secret'"
echo "3. Add these two secrets:"
echo "   - Name: AWS_ACCESS_KEY_ID"
echo "   - Name: AWS_SECRET_ACCESS_KEY"
echo ""
echo "4. Push the workflow files:"
echo "   git add .github/workflows/"
echo "   git commit -m 'Add CI/CD pipeline'"
echo "   git push origin main"
echo ""
echo "5. Test the pipeline:"
echo "   - Make a change in backend/ or frontend/"
echo "   - Commit and push"
echo "   - Watch deployment at: https://github.com/shanmukh-007/ApranovaPro1/actions"
echo ""
echo "✅ CI/CD setup complete!"
