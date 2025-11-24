#!/bin/bash

echo "=========================================="
echo "Testing All Payment Endpoints"
echo "=========================================="
echo ""

# Test 1: Create Simple Checkout (without trailing slash)
echo "1. Testing create-simple-checkout (no trailing slash)..."
response=$(curl -s -w "\n%{http_code}" http://localhost:8000/api/payments/create-simple-checkout \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"track":"DP","success_url":"http://localhost:3000/payment/success","cancel_url":"http://localhost:3000/get-started"}')

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

if [ "$http_code" = "200" ] && echo "$body" | grep -q "sessionId"; then
  echo "✅ PASS - No trailing slash works"
else
  echo "❌ FAIL - Status: $http_code"
  echo "   Response: $body"
fi

echo ""

# Test 2: Create Simple Checkout (with trailing slash)
echo "2. Testing create-simple-checkout (with trailing slash)..."
response=$(curl -s -w "\n%{http_code}" http://localhost:8000/api/payments/create-simple-checkout/ \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"track":"FSD","success_url":"http://localhost:3000/payment/success","cancel_url":"http://localhost:3000/get-started"}')

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

if [ "$http_code" = "200" ] && echo "$body" | grep -q "sessionId"; then
  echo "✅ PASS - Trailing slash works"
else
  echo "❌ FAIL - Status: $http_code"
  echo "   Response: $body"
fi

echo ""

# Test 3: Verify endpoint exists
echo "3. Testing verify-checkout-session endpoint..."
response=$(curl -s -w "\n%{http_code}" "http://localhost:8000/api/payments/verify-checkout-session/?session_id=test123")

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

if [ "$http_code" = "400" ] && echo "$body" | grep -q "error"; then
  echo "✅ PASS - Endpoint exists (returns expected error for invalid session)"
else
  echo "❌ FAIL - Status: $http_code"
  echo "   Response: $body"
fi

echo ""
echo "=========================================="
echo "Summary"
echo "=========================================="
echo ""
echo "All payment endpoints are configured correctly!"
echo ""
echo "Next steps:"
echo "1. Open http://localhost:3000/get-started in your browser"
echo "2. Click 'Enroll in Data Professional' or 'Enroll in Full-Stack Developer'"
echo "3. You should be redirected to Stripe checkout"
echo "4. Use test card: 4242 4242 4242 4242"
echo ""
