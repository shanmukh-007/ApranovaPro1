# 🚀 CI/CD Pipeline Setup Guide

## 📋 Overview

Your CI/CD pipeline is now configured using **GitHub Actions** (free for public repos, 2000 minutes/month for private repos).

### What Happens Automatically:
1. You push code changes to GitHub
2. GitHub Actions detects the change
3. Builds Docker image
4. Pushes to AWS ECR
5. Updates ECS service
6. New version goes live automatically

**Total Time:** ~3-5 minutes per deployment

---

## 🔧 Setup Steps

### Step 1: Create AWS IAM User for CI/CD

Create a dedicated IAM user with minimal permissions:

```bash
# Create IAM user
aws iam create-user --user-name github-actions-deployer

# Create access key
aws iam create-access-key --user-name github-actions-deployer
```

**Save the output!** You'll need:
- `AccessKeyId`
- `SecretAccessKey`

### Step 2: Attach IAM Policy

Create a policy file:

```bash
cat > github-actions-policy.json << 'EOF'
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

# Create and attach policy
aws iam put-user-policy \
  --user-name github-actions-deployer \
  --policy-name GitHubActionsDeployPolicy \
  --policy-document file://github-actions-policy.json
```

### Step 3: Add Secrets to GitHub

1. Go to your GitHub repository: https://github.com/shanmukh-007/ApranovaPro1
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these secrets:

| Secret Name | Value |
|-------------|-------|
| `AWS_ACCESS_KEY_ID` | (from Step 1) |
| `AWS_SECRET_ACCESS_KEY` | (from Step 1) |

### Step 4: Push the Workflow Files

```bash
# Add the new workflow files
git add .github/workflows/

# Commit
git commit -m "Add CI/CD pipeline with GitHub Actions"

# Push to GitHub
git push origin main
```

---

## 🎯 How It Works

### Workflow Triggers

**Backend Pipeline** (`.github/workflows/deploy-backend.yml`)
- Triggers when: Changes in `backend/` folder
- Builds: Backend Docker image
- Deploys to: ECS backend service

**Frontend Pipeline** (`.github/workflows/deploy-frontend.yml`)
- Triggers when: Changes in `frontend/` folder
- Builds: Frontend Docker image
- Deploys to: ECS frontend service

### Deployment Flow

```
┌─────────────────────────────────────────────────────────────┐
│  Developer                                                   │
│  ├─ Edit code in backend/ or frontend/                      │
│  ├─ git add .                                                │
│  ├─ git commit -m "Update feature"                          │
│  └─ git push origin main                                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  GitHub Actions (Automatic)                                 │
│  ├─ Checkout code                                           │
│  ├─ Configure AWS credentials                               │
│  ├─ Login to ECR                                            │
│  ├─ Build Docker image                                      │
│  ├─ Tag with git commit SHA                                 │
│  ├─ Push to ECR                                             │
│  ├─ Update ECS task definition                              │
│  └─ Deploy to ECS service                                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  AWS ECS (Automatic)                                        │
│  ├─ Pull new image from ECR                                 │
│  ├─ Start new task with new image                           │
│  ├─ Wait for health checks to pass                          │
│  ├─ Register with load balancer                             │
│  ├─ Drain connections from old task                         │
│  └─ Stop old task                                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  Production (Live)                                          │
│  └─ New version is now serving traffic! ✅                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Monitoring Deployments

### View Workflow Runs
https://github.com/shanmukh-007/ApranovaPro1/actions

### Check Deployment Status
```bash
# Watch backend deployment
aws ecs describe-services \
  --cluster production-cluster \
  --services backend \
  --region us-east-1 \
  --query 'services[0].deployments' \
  --output table

# Watch frontend deployment
aws ecs describe-services \
  --cluster production-cluster \
  --services frontend \
  --region us-east-1 \
  --query 'services[0].deployments' \
  --output table
```

### View Logs
```bash
# Backend logs
aws logs tail /ecs/backend --follow --region us-east-1

# Frontend logs
aws logs tail /ecs/frontend --follow --region us-east-1
```

---

## 🧪 Testing the Pipeline

### Test Backend Deployment
```bash
# Make a small change
echo "# CI/CD test" >> backend/README.md

# Commit and push
git add backend/README.md
git commit -m "Test backend CI/CD pipeline"
git push origin main

# Watch the deployment
# Go to: https://github.com/shanmukh-007/ApranovaPro1/actions
```

### Test Frontend Deployment
```bash
# Make a small change
echo "# CI/CD test" >> frontend/README.md

# Commit and push
git add frontend/README.md
git commit -m "Test frontend CI/CD pipeline"
git push origin main

# Watch the deployment
# Go to: https://github.com/shanmukh-007/ApranovaPro1/actions
```

---

## 🎛️ Manual Deployment

You can also trigger deployments manually:

1. Go to: https://github.com/shanmukh-007/ApranovaPro1/actions
2. Select "Deploy Backend" or "Deploy Frontend"
3. Click "Run workflow"
4. Select branch (main)
5. Click "Run workflow"

---

## 🔒 Security Best Practices

### ✅ What We Did Right
- Created dedicated IAM user (not using root)
- Minimal permissions (only ECR and ECS)
- Secrets stored in GitHub (encrypted)
- No credentials in code

### 🔐 Additional Security (Optional)
- Enable MFA for IAM user
- Rotate access keys every 90 days
- Use AWS Secrets Manager for sensitive env vars
- Enable CloudTrail for audit logs

---

## 💰 Cost

**GitHub Actions:**
- Public repos: FREE unlimited
- Private repos: 2000 minutes/month FREE
- Each deployment: ~3-5 minutes
- **Cost:** $0 (within free tier)

**AWS Resources:**
- No additional cost for CI/CD
- Same ECS/ECR costs as before

---

## 🚨 Troubleshooting

### Deployment Failed

**Check GitHub Actions logs:**
1. Go to: https://github.com/shanmukh-007/ApranovaPro1/actions
2. Click on the failed workflow
3. Click on the failed job
4. Review error messages

**Common Issues:**

#### 1. AWS Credentials Invalid
```
Error: The security token included in the request is invalid
```
**Fix:** Check AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in GitHub secrets

#### 2. ECR Permission Denied
```
Error: denied: User is not authorized to perform: ecr:PutImage
```
**Fix:** Verify IAM policy is attached to github-actions-deployer user

#### 3. ECS Service Not Found
```
Error: Service not found
```
**Fix:** Verify service name in workflow file matches actual service name

#### 4. Docker Build Failed
```
Error: failed to solve with frontend dockerfile.v0
```
**Fix:** Check Dockerfile syntax and dependencies

### Rollback a Deployment

If a deployment breaks production:

```bash
# List recent task definitions
aws ecs list-task-definitions \
  --family-prefix backend \
  --sort DESC \
  --max-items 5 \
  --region us-east-1

# Rollback to previous version
aws ecs update-service \
  --cluster production-cluster \
  --service backend \
  --task-definition backend:PREVIOUS_VERSION \
  --region us-east-1
```

---

## 📈 Advanced Features (Optional)

### Add Automated Tests

Add this step before deployment:

```yaml
- name: Run tests
  run: |
    cd backend
    python -m pytest tests/
```

### Add Slack Notifications

```yaml
- name: Notify Slack
  if: always()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Add Staging Environment

Create separate workflows for staging:
- `deploy-backend-staging.yml`
- `deploy-frontend-staging.yml`

Deploy to staging first, then promote to production.

### Blue-Green Deployment

Use AWS CodeDeploy for zero-downtime deployments:
- Deploy new version alongside old
- Switch traffic gradually
- Rollback instantly if issues

---

## 📝 Workflow Files Created

1. **`.github/workflows/deploy-backend.yml`**
   - Deploys backend on changes to `backend/` folder
   - Builds Docker image
   - Pushes to ECR
   - Updates ECS service

2. **`.github/workflows/deploy-frontend.yml`**
   - Deploys frontend on changes to `frontend/` folder
   - Builds Docker image
   - Pushes to ECR
   - Updates ECS service

---

## ✅ Quick Start Checklist

- [ ] Create IAM user for GitHub Actions
- [ ] Create and save access keys
- [ ] Attach IAM policy
- [ ] Add secrets to GitHub repository
- [ ] Push workflow files to GitHub
- [ ] Test backend deployment
- [ ] Test frontend deployment
- [ ] Monitor first deployment
- [ ] Verify application works
- [ ] Document any custom steps

---

## 🎯 Next Steps

1. **Set up the IAM user** (5 minutes)
2. **Add secrets to GitHub** (2 minutes)
3. **Push workflow files** (1 minute)
4. **Test deployment** (5 minutes)

**Total Setup Time:** ~15 minutes

After setup, every code change will automatically deploy to production! 🚀

---

## 📚 Resources

- GitHub Actions Docs: https://docs.github.com/en/actions
- AWS ECS Deploy Action: https://github.com/aws-actions/amazon-ecs-deploy-task-definition
- AWS ECR Login Action: https://github.com/aws-actions/amazon-ecr-login
- Your Workflows: https://github.com/shanmukh-007/ApranovaPro1/actions

---

**Questions?** Check the troubleshooting section or review GitHub Actions logs for detailed error messages.
