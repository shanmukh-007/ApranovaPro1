#!/bin/bash
# Switch to new GitHub repository

set -e

NEW_REPO="https://github.com/dinesh78161/ApranovaPro"
OLD_REPO="https://github.com/shanmukh-007/ApranovaPro1"

echo "🔄 Switching Git Remote Repository"
echo ""
echo "Old: $OLD_REPO"
echo "New: $NEW_REPO"
echo ""

# Step 1: Remove old remote
echo "📝 Step 1: Removing old remote..."
git remote remove main 2>/dev/null || echo "Remote 'main' not found"
git remote remove origin 2>/dev/null || echo "Remote 'origin' not found"

# Step 2: Add new remote
echo "📝 Step 2: Adding new remote..."
git remote add origin $NEW_REPO

# Step 3: Verify
echo "📝 Step 3: Verifying new remote..."
git remote -v

echo ""
echo "✅ Remote repository changed successfully!"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Make sure you have access to the new repo:"
echo "   $NEW_REPO"
echo ""
echo "2. Push your code to the new repo:"
echo "   git push -u origin main"
echo ""
echo "3. If you get permission denied, you may need to:"
echo "   - Add your SSH key to GitHub"
echo "   - Or use HTTPS with personal access token"
echo ""
echo "4. After pushing, set up CI/CD:"
echo "   - Go to: https://github.com/dinesh78161/ApranovaPro/settings/secrets/actions"
echo "   - Add AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY"
echo "   - Run: ./setup-cicd.sh"
echo ""
