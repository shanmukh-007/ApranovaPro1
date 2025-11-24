#!/bin/bash

echo "Checking Docker build status..."
echo ""

# Wait for build to complete
echo "Waiting for containers to be ready..."
sleep 60

echo ""
echo "=== Container Status ==="
docker ps --format "table {{.Names}}\t{{.Status}}"

echo ""
echo "=== Backend Health ==="
curl -s http://localhost:8000/health || echo "Backend not ready yet"

echo ""
echo "=== Frontend Status ==="
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:3000 || echo "Frontend not ready yet"

echo ""
echo "=== Build Complete! ==="
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo "Enrollment: http://localhost:3000/get-started"
