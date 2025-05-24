#!/bin/bash

echo "🔥 Generating Sample Data with Anomalies for CryptaNet"
echo "======================================================"

# Login to get a token
TOKEN=$(curl -s -X POST http://localhost:5004/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' | jq -r '.token')

echo "✅ Authenticated with token: ${TOKEN:0:10}..."

# 1. Normal data: Premium Coffee Beans
echo "📦 Adding normal data: Premium Coffee Beans"
curl -s -X POST http://localhost:5004/api/supply-chain/submit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "organizationId": "Org1MSP",
    "dataType": "supply_chain",
    "data": {
      "productId": "COFFEE-001",
      "product": "Premium Coffee Beans",
      "quantity": 1000,
      "location": "Warehouse A - Section 1",
      "temperature": 22.5,
      "humidity": 65.0,
      "timestamp": "2025-05-24T14:00:00Z"
    }
  }' > /dev/null

# 2. Normal data: Electronic Components
echo "📦 Adding normal data: Electronic Components"
curl -s -X POST http://localhost:5004/api/supply-chain/submit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "organizationId": "Org1MSP",
    "dataType": "supply_chain",
    "data": {
      "productId": "ELEC-002",
      "product": "Electronic Components",
      "quantity": 500,
      "location": "Warehouse B - Section 2",
      "temperature": 20.0,
      "humidity": 45.0,
      "timestamp": "2025-05-24T14:30:00Z"
    }
  }' > /dev/null

# 3. Normal data: Pharmaceutical Products
echo "📦 Adding normal data: Pharmaceutical Products"
curl -s -X POST http://localhost:5004/api/supply-chain/submit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "organizationId": "Org1MSP",
    "dataType": "supply_chain",
    "data": {
      "productId": "PHARMA-003",
      "product": "Pharmaceutical Products",
      "quantity": 250,
      "location": "Cold Storage - Section 3",
      "temperature": 18.0,
      "humidity": 40.0,
      "timestamp": "2025-05-24T15:00:00Z"
    }
  }' > /dev/null

# 4. ⚠️ ANOMALY: Temperature Sensitive Item with HIGH TEMPERATURE
echo "🔥 Adding ANOMALY data: Temperature Sensitive Item (HIGH TEMPERATURE)"
curl -s -X POST http://localhost:5004/api/supply-chain/submit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "organizationId": "Org1MSP",
    "dataType": "supply_chain",
    "data": {
      "productId": "TEMP-004",
      "product": "Temperature Sensitive Item",
      "quantity": 100,
      "location": "Warehouse C - Section 4",
      "temperature": 45.0,
      "humidity": 60.0,
      "timestamp": "2025-05-24T15:30:00Z"
    }
  }' > /dev/null

# 5. ⚠️ ANOMALY: Frozen Food with HIGH TEMPERATURE
echo "🔥 Adding ANOMALY data: Frozen Food (HIGH TEMPERATURE)"
curl -s -X POST http://localhost:5004/api/supply-chain/submit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "organizationId": "Org1MSP",
    "dataType": "supply_chain",
    "data": {
      "productId": "FROZEN-005",
      "product": "Frozen Food Products",
      "quantity": 300,
      "location": "Cold Storage - Section 5",
      "temperature": 28.5,
      "humidity": 45.0,
      "timestamp": "2025-05-24T16:00:00Z"
    }
  }' > /dev/null

# 6. ⚠️ ANOMALY: Sensitive Electronics with HIGH HUMIDITY
echo "💧 Adding ANOMALY data: Sensitive Electronics (HIGH HUMIDITY)"
curl -s -X POST http://localhost:5004/api/supply-chain/submit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "organizationId": "Org1MSP",
    "dataType": "supply_chain",
    "data": {
      "productId": "SELEC-006",
      "product": "Sensitive Electronics",
      "quantity": 75,
      "location": "Warehouse D - Section 1",
      "temperature": 22.0,
      "humidity": 85.0,
      "timestamp": "2025-05-24T16:30:00Z"
    }
  }' > /dev/null

# 7. Normal data: Clothing Items
echo "📦 Adding normal data: Clothing Items"
curl -s -X POST http://localhost:5004/api/supply-chain/submit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "organizationId": "Org1MSP",
    "dataType": "supply_chain",
    "data": {
      "productId": "CLOTH-007",
      "product": "Clothing Items",
      "quantity": 1500,
      "location": "Warehouse E - Section 3",
      "temperature": 21.5,
      "humidity": 55.0,
      "timestamp": "2025-05-24T17:00:00Z"
    }
  }' > /dev/null

# 8. Normal data: Furniture
echo "📦 Adding normal data: Furniture"
curl -s -X POST http://localhost:5004/api/supply-chain/submit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "organizationId": "Org1MSP",
    "dataType": "supply_chain",
    "data": {
      "productId": "FURN-008",
      "product": "Furniture",
      "quantity": 50,
      "location": "Warehouse F - Section 1",
      "temperature": 23.0,
      "humidity": 50.0,
      "timestamp": "2025-05-24T17:30:00Z"
    }
  }' > /dev/null

# 9. ⚠️ ANOMALY: Fresh Produce with EXTREME CONDITIONS
echo "⚠️ Adding ANOMALY data: Fresh Produce (EXTREME CONDITIONS)"
curl -s -X POST http://localhost:5004/api/supply-chain/submit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "organizationId": "Org1MSP",
    "dataType": "supply_chain",
    "data": {
      "productId": "FRESH-009",
      "product": "Fresh Produce",
      "quantity": 800,
      "location": "Warehouse A - Section 5",
      "temperature": 38.5,
      "humidity": 90.0,
      "timestamp": "2025-05-24T18:00:00Z"
    }
  }' > /dev/null

# 10. Normal data: Books and Publications
echo "📦 Adding normal data: Books and Publications"
curl -s -X POST http://localhost:5004/api/supply-chain/submit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "organizationId": "Org1MSP",
    "dataType": "supply_chain",
    "data": {
      "productId": "BOOKS-010",
      "product": "Books and Publications",
      "quantity": 2000,
      "location": "Warehouse B - Section 4",
      "temperature": 21.0,
      "humidity": 45.0,
      "timestamp": "2025-05-24T18:30:00Z"
    }
  }' > /dev/null

# Verify the data
echo ""
echo "✅ Sample data generation complete!"
DATA_COUNT=$(curl -s -H "Authorization: Bearer $TOKEN" \
  "http://localhost:5004/api/supply-chain/query" | jq -r '.count')
echo "📊 Total records: $DATA_COUNT"
echo "🔍 Anomalies should be visible in the dashboard now"
echo ""
echo "🚀 Access your CryptaNet system at: http://localhost:3000"
echo "🔑 Login with: admin / admin123"
