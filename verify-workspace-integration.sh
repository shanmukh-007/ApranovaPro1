#!/bin/bash

echo "=========================================="
echo "Verifying VS Code Workspace Integration"
echo "=========================================="
echo ""

# Check frontend components
echo "✓ Frontend Components:"
echo "  - tool-card.tsx: $([ -f frontend/components/student/tool-card.tsx ] && echo '✅ Present' || echo '❌ Missing')"
echo "  - tool-cards-section.tsx: $([ -f frontend/components/student/tool-cards-section.tsx ] && echo '✅ Present' || echo '❌ Missing')"
echo "  - project-card-enhanced.tsx: $([ -f frontend/components/student/project-card-enhanced.tsx ] && echo '✅ Present' || echo '❌ Missing')"
echo ""

# Check frontend pages
echo "✓ Frontend Pages:"
echo "  - projects/[id]/page.tsx: $([ -f frontend/app/student/projects/[id]/page.tsx ] && echo '✅ Present' || echo '❌ Missing')"
echo "  - project-guide/page.tsx: $([ -f frontend/app/student/project-guide/page.tsx ] && echo '✅ Present' || echo '❌ Missing')"
echo ""

# Check backend services
echo "✓ Backend Services:"
echo "  - provisioning_service.py: $([ -f backend/accounts/provisioning_service.py ] && echo '✅ Present' || echo '❌ Missing')"
echo "  - postgres_provisioning.py: $([ -f backend/accounts/postgres_provisioning.py ] && echo '✅ Present' || echo '❌ Missing')"
echo "  - set_workspace_url.py: $([ -f backend/set_workspace_url.py ] && echo '✅ Present' || echo '❌ Missing')"
echo ""

# Check if ToolCard is used in projects page
echo "✓ Integration Checks:"
if grep -q "ToolCard" frontend/app/student/projects/[id]/page.tsx 2>/dev/null; then
    echo "  - ToolCard imported in projects page: ✅ Yes"
else
    echo "  - ToolCard imported in projects page: ❌ No"
fi

# Check if workspace URL is in user model
if grep -q "workspace_url" backend/accounts/models.py 2>/dev/null; then
    echo "  - workspace_url in User model: ✅ Yes"
else
    echo "  - workspace_url in User model: ❌ No"
fi

# Check containers
echo ""
echo "✓ Container Status:"
docker ps --format "  - {{.Names}}: {{.Status}}" | grep apranova

echo ""
echo "✓ API Endpoints:"
curl -s http://localhost:8000/health > /dev/null && echo "  - Backend API: ✅ Running" || echo "  - Backend API: ❌ Down"
curl -s http://localhost:3000 > /dev/null && echo "  - Frontend: ✅ Running" || echo "  - Frontend: ❌ Down"
curl -s http://localhost:8080 > /dev/null && echo "  - VS Code Server: ✅ Running" || echo "  - VS Code Server: ❌ Down"

echo ""
echo "=========================================="
echo "Verification Complete"
echo "=========================================="
