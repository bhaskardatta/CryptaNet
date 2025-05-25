#!/bin/bash

# Simple Health Check for CryptaNet Supply Chain System
echo "🏥 CryptaNet System Health Check"
echo "================================="

# Check backend
echo "🔍 Checking Backend (port 5004)..."
if curl -s http://localhost:5004/health > /dev/null; then
    echo "✅ Backend: HEALTHY"
else
    echo "❌ Backend: DOWN"
fi

# Check frontend
echo "🔍 Checking Frontend (port 3000)..."
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend: HEALTHY"
else
    echo "❌ Frontend: DOWN"
fi

# Check if Python processes are running
echo "🔍 Checking Python processes..."
if pgrep -f "simple_backend.py" > /dev/null; then
    echo "✅ Backend process: RUNNING"
else
    echo "❌ Backend process: NOT RUNNING"
fi

if pgrep -f "react-scripts" > /dev/null; then
    echo "✅ Frontend process: RUNNING"
else
    echo "❌ Frontend process: NOT RUNNING"
fi

echo "✅ Health check completed!"
