#!/bin/bash

echo "Testing Dashboard API Calls..."
echo ""

# Test 1: Check if user is logged in
echo "1. Testing /api/users/profile (should show user info)"
curl -s -c cookies.txt http://localhost:8000/api/users/profile/ | jq '.' || echo "Not authenticated or error"
echo ""

# Test 2: Get tracks
echo "2. Testing /api/curriculum/tracks/ (should show tracks)"
curl -s -b cookies.txt http://localhost:8000/api/curriculum/tracks/ | jq '.' || echo "Error getting tracks"
echo ""

# Test 3: Via Next.js proxy
echo "3. Testing via Next.js proxy /api/curriculum/tracks/"
curl -s http://localhost:3000/api/curriculum/tracks/ | jq '.' || echo "Proxy not working"
echo ""

rm -f cookies.txt
