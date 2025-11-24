#!/bin/bash
# Merge changes from upstream repo while preserving AWS/Terraform files

set -e

echo "🔄 Merging changes from upstream repo..."
echo ""

# Create a backup branch
echo "📦 Creating backup branch..."
git branch backup-before-merge-$(date +%Y%m%d-%H%M%S) || true

# Fetch latest from upstream
echo "📥 Fetching latest changes from upstream..."
git fetch upstream

# Create a temporary branch for merging
echo "🌿 Creating temporary merge branch..."
git checkout -b temp-merge-upstream

# Merge upstream/master but don't commit yet
echo "🔀 Merging upstream changes..."
git merge upstream/master --no-commit --no-ff || true

# Reset (unstage) files we want to keep from our repo
echo "🔒 Preserving AWS and Terraform files..."

# List of files/folders to keep from YOUR repo (not merge from upstream)
FILES_TO_KEEP=(
    "terraform/"
    "backend-task-def.json"
    "frontend-task-def.json"
    "deploy-basic-aws.sh"
    "deploy-production.sh"
    "aws-cost-calculator.py"
    ".github/workflows/deploy-backend.yml"
    ".github/workflows/deploy-frontend.yml"
    "setup-cicd.sh"
    "AWS_SERVICES_INVENTORY.md"
    "AWS_MASTER_GUIDE.md"
    "AWS_COMPLETE_SERVICES_GUIDE.md"
    "YOUR_AWS_ARCHITECTURE.md"
    "NAT_GATEWAY_REMOVAL_SUCCESS.md"
    "NAT_GATEWAY_REMOVAL_PLAN.md"
    "CI_CD_SETUP_GUIDE.md"
    "CI_CD_QUICK_START.md"
    "MANUAL_DEPLOYMENT_GUIDE.md"
    "AUTOMATED_TESTING_GUIDE.md"
    "AUTOMATIC_TRIGGER_EXPLAINED.md"
    "COMPLETE_SETUP_SUMMARY.md"
    "CICD_VISUAL_GUIDE.md"
    "HOW_TO_USE_CICD.md"
)

for file in "${FILES_TO_KEEP[@]}"; do
    if [ -e "$file" ]; then
        echo "  ✓ Keeping: $file"
        git checkout --ours "$file" 2>/dev/null || true
    fi
done

echo ""
echo "📊 Checking merge status..."
git status

echo ""
echo "✅ Merge prepared!"
echo ""
echo "📋 Next steps:"
echo "1. Review the changes: git status"
echo "2. Check specific files: git diff --cached"
echo "3. If looks good, commit: git commit -m 'Merge upstream changes'"
echo "4. Switch back to main: git checkout main"
echo "5. Merge temp branch: git merge temp-merge-upstream"
echo "6. Push: git push main main"
echo ""
echo "Or run: ./complete-merge.sh"
