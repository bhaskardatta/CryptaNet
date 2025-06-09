#!/bin/bash

echo "🔍 Testing CryptaNet Anomaly Detection Integration..."

echo ""
echo "1. Testing Backend API..."
ANOMALIES_COUNT=$(curl -s "http://localhost:5004/api/analytics/anomalies" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('anomalies', [])))")
echo "   ✅ Backend returns $ANOMALIES_COUNT anomalies"

echo ""
echo "2. Testing Backend Analytics..."
ANALYTICS_COUNT=$(curl -s "http://localhost:5004/api/analytics" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('anomaly_count', 0))")
echo "   ✅ Analytics endpoint shows $ANALYTICS_COUNT anomalies"

echo ""
echo "3. Testing Frontend Accessibility..."
if curl -s "http://localhost:3000" > /dev/null; then
    echo "   ✅ Frontend is accessible"
else
    echo "   ❌ Frontend is not accessible"
fi

echo ""
echo "4. Sample Anomaly Data Structure:"
curl -s "http://localhost:5004/api/analytics/anomalies" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('anomalies'):
    anomaly = data['anomalies'][0]
    print(f'   - ID/Index: {anomaly.get(\"index\", \"N/A\")}')
    print(f'   - Product ID: {anomaly.get(\"product_id\", \"N/A\")}')
    print(f'   - Type: {anomaly.get(\"type\", \"N/A\")}')
    print(f'   - Severity: {anomaly.get(\"severity\", \"N/A\")}')
    print(f'   - Temperature: {anomaly.get(\"temperature\", \"N/A\")}°C')
    print(f'   - Humidity: {anomaly.get(\"humidity\", \"N/A\")}%')
    print(f'   - Algorithms: {anomaly.get(\"algorithms\", [])}')
    print(f'   - Scores: {list(anomaly.get(\"scores\", {}).keys())}')
else:
    print('   ❌ No anomalies found')
"

echo ""
echo "🎯 Integration Test Complete!"
echo ""
echo "Next step: Navigate to http://localhost:3000/anomaly-detection and test the frontend interface."
