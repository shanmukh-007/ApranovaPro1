#!/bin/bash

echo "Testing Enrollment API..."
echo ""

# Test Data Professional Track
echo "1. Testing Data Professional Track (DP)..."
response=$(curl -s http://localhost:8000/api/payments/create-simple-checkout/ \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "track":"DP",
    "success_url":"http://localhost:3000/payment/success",
    "cancel_url":"http://localhost:3000/get-started"
  }')

if echo "$response" | grep -q "sessionId"; then
  echo "✅ DP Track - SUCCESS"
  echo "   Session ID: $(echo $response | grep -o '"sessionId":"[^"]*"' | cut -d'"' -f4)"
else
  echo "❌ DP Track - FAILED"
  echo "   Error: $response"
fi

echo ""

# Test Full-Stack Developer Track
echo "2. Testing Full-Stack Developer Track (FSD)..."
response=$(curl -s http://localhost:8000/api/payments/create-simple-checkout/ \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "track":"FSD",
    "success_url":"http://localhost:3000/payment/success",
    "cancel_url":"http://localhost:3000/get-started"
  }')

if echo "$response" | grep -q "sessionId"; then
  echo "✅ FSD Track - SUCCESS"
  echo "   Session ID: $(echo $response | grep -o '"sessionId":"[^"]*"' | cut -d'"' -f4)"
else
  echo "❌ FSD Track - FAILED"
  echo "   Error: $response"
fi

echo ""
echo "=========================================="
echo "Enrollment API is working! 🎉"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Go to http://localhost:3000/get-started"
echo "2. Click 'Enroll in Data Professional' or 'Enroll in Full-Stack Developer'"
echo "3. You'll be redirected to Stripe checkout"
echo "4. Use test card: 4242 4242 4242 4242"
echo "5. Use any future expiry date and any CVC"
echo ""
