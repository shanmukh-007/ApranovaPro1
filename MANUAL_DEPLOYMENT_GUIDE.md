# 🎯 Manual Deployment Guide

## ✅ Automatic Deployment is NOW DISABLED

Your CI/CD pipeline is now configured for **manual deployment only**.

**What changed:**
- ❌ Pushing code does NOT trigger deployment
- ✅ You manually trigger deployment from GitHub Actions
- ✅ Full control over when to deploy

---

## 🚀 How to Deploy Manually

### Step 1: Go to GitHub Actions

**URL:** https://github.com/shanmukh-007/ApranovaPro1/actions

### Step 2: Choose What to Deploy

You'll see two workflows:
- **Deploy Backend to AWS ECS**
- **Deploy Frontend to AWS ECS**

Click on the one you want to deploy.

### Step 3: Trigger Deployment

1. Click the **"Run workflow"** button (on the right side)
2. A dropdown appears:
   - **Branch:** Select `main` (or any branch you want to deploy)
3. Click the green **"Run workflow"** button
4. Deployment starts!

### Step 4: Watch Progress

- The workflow appears in the list
- Click on it to see live progress
- Wait 3-5 minutes
- ✅ Deployment complete!

---

## 📸 Visual Guide

```
┌─────────────────────────────────────────────────────────────┐
│  GitHub Actions Page                                         │
│  https://github.com/shanmukh-007/ApranovaPro1/actions       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  All workflows                                               │
│                                                              │
│  📦 Deploy Backend to AWS ECS                                │
│     [Run workflow ▼]  ← Click this button                    │
│                                                              │
│  📦 Deploy Frontend to AWS ECS                               │
│     [Run workflow ▼]  ← Or this one                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘

After clicking "Run workflow":

┌─────────────────────────────────────────────────────────────┐
│  Run workflow                                                │
│                                                              │
│  Use workflow from                                           │
│  Branch: main ▼                                              │
│                                                              │
│  [Run workflow]  ← Click this green button                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎬 Complete Workflow Example

### Scenario: Deploy Backend Changes

```bash
# 1. Edit your backend code
vim backend/api/views.py

# 2. Test locally
cd backend
python manage.py test
python manage.py runserver

# 3. Commit and push (does NOT deploy automatically)
git add backend/
git commit -m "Add new feature"
git push main main

# 4. Go to GitHub Actions
# Open: https://github.com/shanmukh-007/ApranovaPro1/actions

# 5. Click "Deploy Backend to AWS ECS"

# 6. Click "Run workflow" button

# 7. Select branch: main

# 8. Click "Run workflow" (green button)

# 9. Watch deployment (3-5 minutes)
# - Tests run
# - Docker image builds
# - Pushes to ECR
# - Deploys to ECS

# 10. ✅ Deployment complete!
# Test: http://production-alb-1841167835.us-east-1.elb.amazonaws.com/api/
```

---

## 🔄 Typical Development Flow

### Option 1: Deploy After Testing

```bash
# Day 1: Development
git checkout -b feature/new-feature
# ... make changes ...
git commit -m "Add new feature"
git push main feature/new-feature

# Day 2: Code Review
# Create Pull Request
# Team reviews
# Approve and merge to main

# Day 3: Manual Deployment
# Go to GitHub Actions
# Click "Run workflow"
# Deploy to production
```

### Option 2: Deploy Multiple Changes Together

```bash
# Monday: Feature 1
git commit -m "Add feature 1"
git push main main

# Tuesday: Feature 2
git commit -m "Add feature 2"
git push main main

# Wednesday: Feature 3
git commit -m "Add feature 3"
git push main main

# Thursday: Deploy all at once
# Go to GitHub Actions
# Click "Run workflow"
# All 3 features deploy together
```

---

## 🎯 When to Deploy

### Good Times to Deploy:
- ✅ After thorough testing
- ✅ During low traffic hours
- ✅ When you're available to monitor
- ✅ After code review approval
- ✅ When multiple features are ready

### Avoid Deploying:
- ❌ During peak traffic hours
- ❌ Right before leaving for the day
- ❌ Without testing first
- ❌ When you're not available to monitor

---

## 📊 Deployment Checklist

Before clicking "Run workflow":

- [ ] Code tested locally
- [ ] Tests pass (`python manage.py test` or `npm test`)
- [ ] Code reviewed (if using PRs)
- [ ] Changes documented
- [ ] Database migrations ready (if any)
- [ ] Low traffic time (if possible)
- [ ] You're available to monitor

After deployment:

- [ ] Check GitHub Actions for success
- [ ] Test application in browser
- [ ] Check logs for errors
- [ ] Monitor for 10-15 minutes
- [ ] Verify new features work

---

## 🚨 Emergency Deployment

If you need to deploy urgently:

### Quick Deploy (Skip Some Steps)

```bash
# 1. Make critical fix
vim backend/api/views.py

# 2. Quick test
python manage.py test

# 3. Push
git add backend/
git commit -m "HOTFIX: Critical bug fix"
git push main main

# 4. Deploy immediately
# Go to: https://github.com/shanmukh-007/ApranovaPro1/actions
# Click "Run workflow"
# Deploy!

# 5. Monitor closely
aws logs tail /ecs/backend --follow --region us-east-1
```

---

## 🔄 Deploy Both Backend and Frontend

If you changed both:

### Sequential Deployment (Recommended)

```bash
# 1. Deploy backend first
# Go to GitHub Actions
# Click "Deploy Backend to AWS ECS"
# Click "Run workflow"
# Wait for completion (3-5 min)

# 2. Then deploy frontend
# Click "Deploy Frontend to AWS ECS"
# Click "Run workflow"
# Wait for completion (3-5 min)
```

### Parallel Deployment (Faster)

```bash
# 1. Deploy both at the same time
# Go to GitHub Actions

# 2. Open two tabs
# Tab 1: Deploy Backend → Run workflow
# Tab 2: Deploy Frontend → Run workflow

# 3. Both deploy in parallel (3-5 min total)
```

---

## 📱 Deploy from Mobile

You can also deploy from your phone!

1. Open GitHub mobile app
2. Go to your repository
3. Tap "Actions"
4. Tap "Deploy Backend" or "Deploy Frontend"
5. Tap "Run workflow"
6. Select branch
7. Tap "Run workflow"
8. Done!

---

## 🎛️ Advanced: Deploy Specific Branch

You can deploy any branch, not just main:

```bash
# 1. Create feature branch
git checkout -b feature/experimental
git commit -m "Experimental feature"
git push main feature/experimental

# 2. Deploy feature branch to test
# Go to GitHub Actions
# Click "Run workflow"
# Select branch: feature/experimental  ← Not main!
# Click "Run workflow"

# 3. Test in production
# If works: Merge to main and deploy main
# If broken: No problem, main is still safe
```

---

## 📊 Comparison: Automatic vs Manual

### Automatic Deployment (OLD - Now Disabled)

```
✅ Pros:
- Fast (deploys immediately)
- No manual steps

❌ Cons:
- No control over timing
- Deploys even if you're not ready
- Multiple small deploys
- Can't batch changes
```

### Manual Deployment (NEW - Current Setup)

```
✅ Pros:
- Full control over when to deploy
- Deploy during low traffic
- Batch multiple changes
- Review before deploying
- Deploy only when ready

❌ Cons:
- Need to remember to deploy
- Extra manual step
```

---

## 🔧 Re-enable Automatic Deployment (If Needed)

If you want automatic deployment back:

### Backend Workflow

Edit `.github/workflows/deploy-backend.yml`:

```yaml
# Change from:
on:
  workflow_dispatch:

# To:
on:
  push:
    branches:
      - main
    paths:
      - 'backend/**'
  workflow_dispatch:
```

### Frontend Workflow

Edit `.github/workflows/deploy-frontend.yml`:

```yaml
# Change from:
on:
  workflow_dispatch:

# To:
on:
  push:
    branches:
      - main
    paths:
      - 'frontend/**'
  workflow_dispatch:
```

Then commit and push.

---

## 📈 Deployment History

View all past deployments:

1. Go to: https://github.com/shanmukh-007/ApranovaPro1/actions
2. See list of all workflow runs
3. Click on any to see details
4. See who triggered it, when, and results

---

## 🎯 Quick Reference

### Deploy Backend
1. https://github.com/shanmukh-007/ApranovaPro1/actions
2. Click "Deploy Backend to AWS ECS"
3. Click "Run workflow"
4. Select branch: main
5. Click "Run workflow"

### Deploy Frontend
1. https://github.com/shanmukh-007/ApranovaPro1/actions
2. Click "Deploy Frontend to AWS ECS"
3. Click "Run workflow"
4. Select branch: main
5. Click "Run workflow"

### Check Deployment Status
```bash
aws ecs describe-services \
  --cluster production-cluster \
  --services backend frontend \
  --region us-east-1 \
  --query 'services[*].[serviceName,runningCount,desiredCount]' \
  --output table
```

### View Logs
```bash
# Backend
aws logs tail /ecs/backend --follow --region us-east-1

# Frontend
aws logs tail /ecs/frontend --follow --region us-east-1
```

---

## ✅ Summary

**Before (Automatic):**
```
git push → Automatic deployment → Production updated
```

**Now (Manual):**
```
git push → Nothing happens
         ↓
You decide when to deploy
         ↓
Click "Run workflow" → Deployment starts → Production updated
```

**Benefits:**
- ✅ Full control over deployments
- ✅ Deploy during low traffic
- ✅ Batch multiple changes
- ✅ Review before deploying
- ✅ No surprises

**To Deploy:**
1. Go to: https://github.com/shanmukh-007/ApranovaPro1/actions
2. Click "Run workflow"
3. Wait 3-5 minutes
4. Done!

---

**You now have full control over when your code goes to production!** 🎯
