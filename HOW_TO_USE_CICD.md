# 🚀 How to Use CI/CD Pipeline - Simple Guide

## 📋 One-Time Setup (Do This First)

### Step 1: Add Secrets to GitHub (2 minutes)

1. **Open this link:** https://github.com/shanmukh-007/ApranovaPro1/settings/secrets/actions

2. **Click:** "New repository secret" button (green button on right)

3. **Add First Secret:**
   - In "Name" field, type: `AWS_ACCESS_KEY_ID`
   - In "Secret" field, paste: `AKIAUWD6TT4BJW3Q23CB`
   - Click "Add secret"

4. **Add Second Secret:**
   - Click "New repository secret" again
   - In "Name" field, type: `AWS_SECRET_ACCESS_KEY`
   - In "Secret" field, paste: `8T7XCl26JEXch9ooPAr9obZx2R1kk/WdnGxG/wSr`
   - Click "Add secret"

5. **Verify:** You should see 2 secrets listed

✅ **Done! You only need to do this once.**

---

## 🎯 Daily Usage - How to Deploy Code Changes

### Example 1: Update Backend Code

Let's say you want to fix a bug or add a feature to the backend:

```bash
# 1. Edit your backend code (use any editor)
# For example, edit backend/api/views.py

# 2. Test locally (optional but recommended)
cd backend
python manage.py test

# 3. Commit your changes
cd ..
git add backend/
git commit -m "Fix user login bug"

# 4. Push to GitHub
git push main main

# 5. That's it! 🎉
# GitHub Actions will automatically:
# - Build new Docker image
# - Push to AWS ECR
# - Deploy to production
# - Takes 3-5 minutes
```

**Watch the deployment:**
- Go to: https://github.com/shanmukh-007/ApranovaPro1/actions
- You'll see "Deploy Backend to AWS ECS" running
- Click on it to see live progress

---

### Example 2: Update Frontend Code

Let's say you want to change the UI:

```bash
# 1. Edit your frontend code
# For example, edit frontend/src/pages/index.tsx

# 2. Test locally (optional)
cd frontend
npm run dev
# Check http://localhost:3000

# 3. Commit your changes
cd ..
git add frontend/
git commit -m "Update homepage design"

# 4. Push to GitHub
git push main main

# 5. Done! 🎉
# Automatic deployment starts
```

**Watch the deployment:**
- Go to: https://github.com/shanmukh-007/ApranovaPro1/actions
- You'll see "Deploy Frontend to AWS ECS" running

---

### Example 3: Update Both Backend and Frontend

```bash
# 1. Edit both backend and frontend code
# Edit backend/api/views.py
# Edit frontend/src/components/Header.tsx

# 2. Commit all changes
git add backend/ frontend/
git commit -m "Add new feature: user profile"

# 3. Push to GitHub
git push main main

# 4. Both pipelines will run! 🎉
# - Backend deployment (3-5 min)
# - Frontend deployment (3-5 min)
# They run in parallel
```

---

## 🎛️ Manual Deployment (Without Code Changes)

Sometimes you want to redeploy without changing code:

### Option 1: Via GitHub Website

1. Go to: https://github.com/shanmukh-007/ApranovaPro1/actions
2. Click "Deploy Backend to AWS ECS" (or Frontend)
3. Click "Run workflow" button (on the right)
4. Select branch: `main`
5. Click green "Run workflow" button
6. Deployment starts!

### Option 2: Via Command Line

```bash
# Trigger backend deployment
git commit --allow-empty -m "Redeploy backend"
git push main main

# Or trigger frontend deployment
git commit --allow-empty -m "Redeploy frontend"
git push main main
```

---

## 📊 Monitor Your Deployment

### 1. GitHub Actions Dashboard
**URL:** https://github.com/shanmukh-007/ApranovaPro1/actions

**What you see:**
- ✅ Green checkmark = Deployment successful
- 🟡 Yellow circle = Deployment in progress
- ❌ Red X = Deployment failed

**Click on any workflow to see:**
- Build logs
- Deployment progress
- Error messages (if any)

### 2. Check Deployment Status

```bash
# Check if new version is running
aws ecs describe-services \
  --cluster production-cluster \
  --services backend frontend \
  --region us-east-1 \
  --query 'services[*].[serviceName,runningCount,desiredCount]' \
  --output table
```

### 3. View Application Logs

```bash
# Backend logs (live)
aws logs tail /ecs/backend --follow --region us-east-1

# Frontend logs (live)
aws logs tail /ecs/frontend --follow --region us-east-1

# Last 10 minutes only
aws logs tail /ecs/backend --since 10m --region us-east-1
```

### 4. Test Your Application

```bash
# Test frontend
curl http://production-alb-1841167835.us-east-1.elb.amazonaws.com

# Test backend API
curl http://production-alb-1841167835.us-east-1.elb.amazonaws.com/api/health

# Or open in browser
open http://production-alb-1841167835.us-east-1.elb.amazonaws.com
```

---

## 🔄 Complete Workflow Example

Let's walk through a real scenario:

### Scenario: Add a new API endpoint

```bash
# 1. Create a new branch (optional, good practice)
git checkout -b feature/new-api

# 2. Edit backend code
# Add new endpoint in backend/api/views.py
cat >> backend/api/views.py << 'EOF'

@api_view(['GET'])
def get_user_stats(request):
    return Response({'users': 100, 'active': 75})
EOF

# 3. Test locally
cd backend
python manage.py runserver
# Test: curl http://localhost:8000/api/stats

# 4. Commit changes
cd ..
git add backend/api/views.py
git commit -m "Add user stats API endpoint"

# 5. Push to GitHub
git push main feature/new-api

# 6. Create Pull Request (optional)
# Go to GitHub and create PR
# Review changes
# Merge to main

# 7. Merge triggers deployment automatically!
# Or push directly to main:
git checkout main
git merge feature/new-api
git push main main

# 8. Watch deployment
# Go to: https://github.com/shanmukh-007/ApranovaPro1/actions

# 9. Wait 3-5 minutes

# 10. Test new endpoint
curl http://production-alb-1841167835.us-east-1.elb.amazonaws.com/api/stats
```

---

## 🚨 What If Deployment Fails?

### Step 1: Check GitHub Actions Logs

1. Go to: https://github.com/shanmukh-007/ApranovaPro1/actions
2. Click on the failed workflow (red X)
3. Click on the failed job
4. Read error messages

### Step 2: Common Issues and Fixes

#### Issue: "Docker build failed"
**Cause:** Syntax error in code or missing dependency

**Fix:**
```bash
# Test Docker build locally
cd backend  # or frontend
docker build -t test .

# Fix the error in your code
# Commit and push again
git add .
git commit -m "Fix Docker build error"
git push main main
```

#### Issue: "AWS credentials invalid"
**Cause:** GitHub secrets not set correctly

**Fix:**
1. Go to: https://github.com/shanmukh-007/ApranovaPro1/settings/secrets/actions
2. Delete old secrets
3. Add them again with correct values

#### Issue: "ECS deployment timeout"
**Cause:** Application not starting or health check failing

**Fix:**
```bash
# Check application logs
aws logs tail /ecs/backend --follow --region us-east-1

# Look for errors in startup
# Fix the error in your code
# Deploy again
```

### Step 3: Rollback to Previous Version

If new version is broken, rollback:

```bash
# List recent versions
aws ecs list-task-definitions \
  --family-prefix backend \
  --sort DESC \
  --max-items 5 \
  --region us-east-1

# Rollback to previous version (e.g., backend:5)
aws ecs update-service \
  --cluster production-cluster \
  --service backend \
  --task-definition backend:5 \
  --region us-east-1

# Wait 2-3 minutes for rollback
```

---

## 💡 Pro Tips

### Tip 1: Use Meaningful Commit Messages
```bash
# ❌ Bad
git commit -m "fix"

# ✅ Good
git commit -m "Fix user login validation bug"
```

### Tip 2: Test Locally First
```bash
# Backend
cd backend
python manage.py test
python manage.py runserver

# Frontend
cd frontend
npm run dev
```

### Tip 3: Deploy During Low Traffic
- Best time: Late night or early morning
- Avoid: Peak business hours

### Tip 4: Monitor After Deployment
```bash
# Watch logs for 5 minutes after deployment
aws logs tail /ecs/backend --follow --region us-east-1

# Check for errors
aws logs filter-log-events \
  --log-group-name /ecs/backend \
  --filter-pattern "ERROR" \
  --region us-east-1
```

### Tip 5: Use Feature Branches
```bash
# Create feature branch
git checkout -b feature/new-feature

# Work on feature
# ... make changes ...

# Push feature branch
git push main feature/new-feature

# Create PR on GitHub
# Review and test
# Merge to main (triggers deployment)
```

---

## 📈 Deployment Timeline

```
You push code
    ↓
    0:00 - GitHub receives push
    ↓
    0:05 - GitHub Actions starts
    ↓
    0:10 - Checkout code
    ↓
    0:15 - Build Docker image (2-3 min)
    ↓
    2:30 - Push to ECR (30 sec)
    ↓
    3:00 - Update ECS task definition
    ↓
    3:10 - ECS starts new task
    ↓
    3:40 - Health checks pass
    ↓
    4:00 - Register with load balancer
    ↓
    4:30 - Drain old task
    ↓
    5:00 - ✅ Deployment complete!
```

**Total Time:** 3-5 minutes

---

## 🎯 Quick Reference Commands

### Deploy Backend
```bash
# Edit code
vim backend/api/views.py

# Commit and push
git add backend/
git commit -m "Update backend"
git push main main
```

### Deploy Frontend
```bash
# Edit code
vim frontend/src/pages/index.tsx

# Commit and push
git add frontend/
git commit -m "Update frontend"
git push main main
```

### Check Deployment Status
```bash
# Via AWS CLI
aws ecs describe-services \
  --cluster production-cluster \
  --services backend frontend \
  --region us-east-1

# Via GitHub
open https://github.com/shanmukh-007/ApranovaPro1/actions
```

### View Logs
```bash
# Backend
aws logs tail /ecs/backend --follow --region us-east-1

# Frontend
aws logs tail /ecs/frontend --follow --region us-east-1
```

### Rollback
```bash
# List versions
aws ecs list-task-definitions --family-prefix backend --sort DESC --max-items 5 --region us-east-1

# Rollback
aws ecs update-service --cluster production-cluster --service backend --task-definition backend:PREVIOUS_VERSION --region us-east-1
```

---

## ✅ Checklist for Each Deployment

- [ ] Code changes tested locally
- [ ] Meaningful commit message
- [ ] Pushed to GitHub
- [ ] Watched deployment in GitHub Actions
- [ ] Checked for green checkmark (success)
- [ ] Tested application after deployment
- [ ] Monitored logs for errors
- [ ] Verified new feature works

---

## 🔗 Important Links

| What | URL |
|------|-----|
| **GitHub Actions** | https://github.com/shanmukh-007/ApranovaPro1/actions |
| **Add Secrets** | https://github.com/shanmukh-007/ApranovaPro1/settings/secrets/actions |
| **Application** | http://production-alb-1841167835.us-east-1.elb.amazonaws.com |
| **ECS Console** | https://console.aws.amazon.com/ecs/home?region=us-east-1#/clusters/production-cluster |

---

## 🎉 Summary

**To deploy code changes:**
1. Edit code
2. `git add .`
3. `git commit -m "Description"`
4. `git push main main`
5. Wait 3-5 minutes
6. Done! ✅

**That's it! No manual Docker builds, no manual deployments, just push and relax!** 🚀
