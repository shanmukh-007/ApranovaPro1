#!/bin/bash

echo "=========================================="
echo "Merging Upstream Features Selectively"
echo "=========================================="
echo ""

# Create a temporary directory to checkout upstream files
TEMP_DIR=$(mktemp -d)
echo "Created temp directory: $TEMP_DIR"

# Clone upstream to temp directory
echo "Cloning upstream repository..."
git clone https://github.com/dinesh78161/ApranovaPro.git "$TEMP_DIR" --depth 1 --quiet

if [ $? -ne 0 ]; then
    echo "❌ Failed to clone upstream repository"
    exit 1
fi

echo "✅ Upstream repository cloned"
echo ""

# List of features to merge
echo "Features to merge:"
echo "1. VS Code workspace integration"
echo "2. Project submission features"
echo "3. GitHub integration for DP track"
echo "4. Support ticket system"
echo "5. Live sessions"
echo "6. Trainer assignment"
echo ""

# Copy specific files that don't conflict with our payment fixes
echo "Copying workspace integration files..."

# Backend workspace files
if [ -f "$TEMP_DIR/backend/workspace/__init__.py" ]; then
    mkdir -p backend/workspace
    cp -r "$TEMP_DIR/backend/workspace/"* backend/workspace/ 2>/dev/null
    echo "✅ Copied backend/workspace"
fi

# Frontend workspace components
if [ -d "$TEMP_DIR/frontend/components/workspace" ]; then
    mkdir -p frontend/components/workspace
    cp -r "$TEMP_DIR/frontend/components/workspace/"* frontend/components/workspace/ 2>/dev/null
    echo "✅ Copied frontend/components/workspace"
fi

# Support ticket system
if [ -d "$TEMP_DIR/backend/support" ]; then
    mkdir -p backend/support
    cp -r "$TEMP_DIR/backend/support/"* backend/support/ 2>/dev/null
    echo "✅ Copied backend/support"
fi

if [ -d "$TEMP_DIR/frontend/app/student/support" ]; then
    mkdir -p frontend/app/student/support
    cp -r "$TEMP_DIR/frontend/app/student/support/"* frontend/app/student/support/ 2>/dev/null
    echo "✅ Copied frontend/app/student/support"
fi

# Live sessions
if [ -d "$TEMP_DIR/backend/live_sessions" ]; then
    mkdir -p backend/live_sessions
    cp -r "$TEMP_DIR/backend/live_sessions/"* backend/live_sessions/ 2>/dev/null
    echo "✅ Copied backend/live_sessions"
fi

if [ -d "$TEMP_DIR/frontend/app/student/live-sessions" ]; then
    mkdir -p frontend/app/student/live-sessions
    cp -r "$TEMP_DIR/frontend/app/student/live-sessions/"* frontend/app/student/live-sessions/ 2>/dev/null
    echo "✅ Copied frontend/app/student/live-sessions"
fi

# Submissions
if [ -d "$TEMP_DIR/backend/submissions" ]; then
    mkdir -p backend/submissions
    cp -r "$TEMP_DIR/backend/submissions/"* backend/submissions/ 2>/dev/null
    echo "✅ Copied backend/submissions"
fi

if [ -d "$TEMP_DIR/frontend/app/student/submissions" ]; then
    mkdir -p frontend/app/student/submissions
    cp -r "$TEMP_DIR/frontend/app/student/submissions/"* frontend/app/student/submissions/ 2>/dev/null
    echo "✅ Copied frontend/app/student/submissions"
fi

# Utils
if [ -d "$TEMP_DIR/backend/utils" ]; then
    mkdir -p backend/utils
    cp -r "$TEMP_DIR/backend/utils/"* backend/utils/ 2>/dev/null
    echo "✅ Copied backend/utils"
fi

# Cleanup
rm -rf "$TEMP_DIR"
echo ""
echo "✅ Cleanup complete"
echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo "1. Review the copied files"
echo "2. Update backend/core/settings.py to include new apps"
echo "3. Run migrations: docker exec apranova_backend python manage.py makemigrations"
echo "4. Run migrations: docker exec apranova_backend python manage.py migrate"
echo "5. Restart containers: docker-compose restart"
echo ""
