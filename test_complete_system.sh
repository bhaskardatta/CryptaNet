#!/bin/bash

echo "🧪 Testing Complete CryptaNet System"
echo "======================================"

# Test backend health
echo "1. Testing Backend Health..."
BACKEND_HEALTH=$(curl -s http://localhost:5004/health | jq -r '.status // "unhealthy"')
echo "   Backend Status: $BACKEND_HEALTH"

# Test authentication
echo "2. Testing Authentication..."
TOKEN=$(curl -s -X POST http://localhost:5004/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' | jq -r '.token // "failed"')

if [ "$TOKEN" != "failed" ] && [ "$TOKEN" != "null" ] && [ -n "$TOKEN" ]; then
    echo "   ✅ Login successful, token received"
else
    echo "   ❌ Login failed"
    exit 1
fi

# Test data query
echo "3. Testing Data Query..."
DATA_COUNT=$(curl -s -H "Authorization: Bearer $TOKEN" \
  "http://localhost:5004/api/supply-chain/query?organizationId=Org1MSP" | jq -r '.count // 0')
echo "   Records found: $DATA_COUNT"

if [ "$DATA_COUNT" -gt 0 ]; then
    echo "   ✅ Data query successful"
else
    echo "   ❌ No data found"
fi

# Test frontend accessibility
echo "4. Testing Frontend..."
if curl -s http://localhost:3000 > /dev/null; then
    echo "   ✅ Frontend accessible at http://localhost:3000"
else
    echo "   ❌ Frontend not accessible"
fi

echo ""
echo "🎯 System Test Complete!"
echo "📋 Access your CryptaNet system at: http://localhost:3000"
echo "🔑 Login with: admin / admin123"

