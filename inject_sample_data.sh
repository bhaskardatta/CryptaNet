#!/bin/bash

# Script to inject sample data into CryptaNet backend

echo "🧪 Injecting sample data into CryptaNet..."

# Sample supply chain data for Premium Coffee Beans
curl -s -X POST http://localhost:5004/api/supply-chain/submit -H "Content-Type: application/json" -d '{
  "data": {
    "product": "Premium Coffee Beans",
    "quantity": 1000,
    "location": "Warehouse A - Section 1",
    "temperature": 22.5,
    "humidity": 65.0,
    "timestamp": "2025-05-24T22:00:00Z"
  },
  "organizationId": "Org1MSP",
  "dataType": "supply_chain"
}' | jq '.success, .data_id'

# Sample supply chain data for Electronic Components
curl -s -X POST http://localhost:5004/api/supply-chain/submit -H "Content-Type: application/json" -d '{
  "data": {
    "product": "Electronic Components",
    "quantity": 500,
    "location": "Warehouse B - Section 2",
    "temperature": 20.0,
    "humidity": 45.0,
    "timestamp": "2025-05-24T22:05:00Z"
  },
  "organizationId": "Org1MSP",
  "dataType": "supply_chain"
}' | jq '.success, .data_id'

# Sample supply chain data for Pharmaceutical Products
curl -s -X POST http://localhost:5004/api/supply-chain/submit -H "Content-Type: application/json" -d '{
  "data": {
    "product": "Pharmaceutical Products",
    "quantity": 250,
    "location": "Cold Storage - Section 3",
    "temperature": 18.0,
    "humidity": 40.0,
    "timestamp": "2025-05-24T22:10:00Z"
  },
  "organizationId": "Org1MSP",
  "dataType": "supply_chain"
}' | jq '.success, .data_id'

# Sample supply chain data for Temperature Sensitive Item
curl -s -X POST http://localhost:5004/api/supply-chain/submit -H "Content-Type: application/json" -d '{
  "data": {
    "product": "Temperature Sensitive Item",
    "quantity": 100,
    "location": "Warehouse C - Section 4",
    "temperature": 45.0,
    "humidity": 80.0,
    "timestamp": "2025-05-24T22:15:00Z"
  },
  "organizationId": "Org1MSP",
  "dataType": "supply_chain"
}' | jq '.success, .data_id'

# Anomaly data - high temperature for cold storage
curl -s -X POST http://localhost:5004/api/supply-chain/submit -H "Content-Type: application/json" -d '{
  "data": {
    "product": "Pharmaceutical Products",
    "quantity": 150,
    "location": "Cold Storage - Section 3",
    "temperature": 28.5,
    "humidity": 65.0,
    "timestamp": "2025-05-24T23:00:00Z"
  },
  "organizationId": "Org1MSP",
  "dataType": "supply_chain"
}' | jq '.success, .data_id'

echo "✅ Sample data injection complete!"
echo "📊 Verifying data count:"
curl -s http://localhost:5004/api/supply-chain/query | jq '.count, .total'
