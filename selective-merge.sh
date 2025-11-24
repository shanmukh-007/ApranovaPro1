#!/bin/bash
# Selectively merge changes from upstream repo

set -e

echo "🔄 Selective merge from upstream repo"
echo "======================================"
echo ""

# Checkout specific folders/files from upstream
echo "📥 Pulling new features from upstream..."

# Backend changes (except AWS-related)
echo "  → Backend code..."
git checkout upstream/master -- backend/ 2>/dev/null || echo "    (no changes)"

# Frontend changes
echo "  → Frontend code..."
git checkout upstream/master -- frontend/ 2>/dev/null || echo "    (no changes)"

# Restore AWS/CI-CD files (keep ours)
echo ""
echo "🔒 Restoring AWS and CI/CD files..."
git checkout main -- terraform/
git checkout main -- backend-task-def.json
git checkout main -- frontend-task-def.json
git checkout main -- deploy-basic-aws.sh
git checkout main -- .github/workflows/

echo ""
echo "✅ Selective merge complete!"
echo ""
echo "📊 Changes staged:"
git status

echo ""
echo "📋 Next steps:"
echo "1. Review changes: git diff --cached"
echo "2. Test locally if needed"
echo "3. Commit: git commit -m 'Merge new features from upstream'"
echo "4. Push: git push main main"
