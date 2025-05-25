#!/usr/bin/env python3
"""
Enhanced Data Simulator for CryptaNet
Real-time supply chain data generation with anomaly injection
"""

import json
import time
import random
import threading
from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template_string
import requests
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

class EnhancedDataSimulator:
    def __init__(self):
        self.running = False
        self.backend_url = "http://localhost:5004"
        self.simulation_thread = None
        self.current_batch = 0
        self.total_records_sent = 0
        self.anomalies_injected = 0
        
        # Supply chain entities
        self.suppliers = [
            "GlobalTech Manufacturing", "PacificRim Industries", "EuroSupply Co",
            "AsiaLink Logistics", "NorthStar Materials", "MegaCorp Suppliers",
            "QuickShip Express", "ReliableSource Ltd", "FastTrack Supply",
            "QualityFirst Manufacturing"
        ]
        
        self.products = [
            "Semiconductor Chips", "LCD Displays", "Battery Packs", "Circuit Boards",
            "Sensors", "Microprocessors", "Memory Modules", "Cables & Connectors",
            "Power Supplies", "Cooling Systems"
        ]
        
        self.locations = [
            "Shanghai, China", "Shenzhen, China", "Seoul, South Korea", "Tokyo, Japan",
            "Singapore", "Bangkok, Thailand", "Mumbai, India", "Kaohsiung, Taiwan",
            "Ho Chi Minh City, Vietnam", "Manila, Philippines"
        ]

    def generate_supply_chain_record(self, inject_anomaly=False):
        """Generate a single supply chain record"""
        base_timestamp = datetime.now()
        
        # Normal ranges
        normal_cost_range = (50, 500)
        normal_quantity_range = (100, 1000)
        normal_delivery_days = (5, 14)
        normal_quality_score = (85, 98)
        
        # Generate base data
        supplier = random.choice(self.suppliers)
        product = random.choice(self.products)
        location = random.choice(self.locations)
        
        if inject_anomaly:
            # Inject various types of anomalies
            anomaly_type = random.choice([
                "cost_spike", "quantity_anomaly", "delivery_delay", 
                "quality_drop", "suspicious_location", "timing_anomaly"
            ])
            
            if anomaly_type == "cost_spike":
                cost = random.uniform(800, 1500)  # 60-200% above normal
                quantity = random.randint(*normal_quantity_range)
                delivery_time = random.randint(*normal_delivery_days)
                quality_score = random.uniform(*normal_quality_score)
                
            elif anomaly_type == "quantity_anomaly":
                cost = random.uniform(*normal_cost_range)
                quantity = random.choice([10, 20, 5000, 8000])  # Too low or too high
                delivery_time = random.randint(*normal_delivery_days)
                quality_score = random.uniform(*normal_quality_score)
                
            elif anomaly_type == "delivery_delay":
                cost = random.uniform(*normal_cost_range)
                quantity = random.randint(*normal_quantity_range)
                delivery_time = random.randint(20, 45)  # Major delay
                quality_score = random.uniform(*normal_quality_score)
                
            elif anomaly_type == "quality_drop":
                cost = random.uniform(*normal_cost_range)
                quantity = random.randint(*normal_quantity_range)
                delivery_time = random.randint(*normal_delivery_days)
                quality_score = random.uniform(30, 60)  # Poor quality
                
            elif anomaly_type == "suspicious_location":
                cost = random.uniform(*normal_cost_range)
                quantity = random.randint(*normal_quantity_range)
                delivery_time = random.randint(*normal_delivery_days)
                quality_score = random.uniform(*normal_quality_score)
                location = random.choice(["Unknown Location", "Restricted Zone", "Unverified Source"])
                
            else:  # timing_anomaly
                cost = random.uniform(*normal_cost_range)
                quantity = random.randint(*normal_quantity_range)
                delivery_time = random.randint(*normal_delivery_days)
                quality_score = random.uniform(*normal_quality_score)
                # Transaction at unusual time (weekend/night)
                base_timestamp = base_timestamp.replace(
                    hour=random.choice([2, 3, 4, 23]), 
                    minute=random.randint(0, 59)
                )
                
            self.anomalies_injected += 1
            
        else:
            # Normal data
            cost = random.uniform(*normal_cost_range)
            quantity = random.randint(*normal_quantity_range)
            delivery_time = random.randint(*normal_delivery_days)
            quality_score = random.uniform(*normal_quality_score)

        record = {
            "transaction_id": f"TXN_{int(time.time())}_{random.randint(1000, 9999)}",
            "timestamp": base_timestamp.isoformat(),
            "supplier": supplier,
            "product": product,
            "quantity": quantity,
            "cost_per_unit": round(cost, 2),
            "total_cost": round(cost * quantity, 2),
            "delivery_time_days": delivery_time,
            "quality_score": round(quality_score, 1),
            "location": location,
            "batch_id": f"BATCH_{self.current_batch}",
            "injected_anomaly": inject_anomaly
        }
        
        return record

    def send_to_backend(self, record):
        """Send record to backend API"""
        try:
            response = requests.post(
                f"{self.backend_url}/api/supply-chain/add",
                json=record,
                timeout=5
            )
            if response.status_code == 200:
                return True
            else:
                print(f"❌ Backend error: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error: {e}")
            return False

    def simulation_loop(self):
        """Main simulation loop"""
        print("🚀 Enhanced Data Simulator started")
        print(f"📡 Sending data to: {self.backend_url}")
        
        while self.running:
            try:
                # Generate batch of records
                batch_size = random.randint(3, 8)  # Variable batch size
                self.current_batch += 1
                
                print(f"\n📦 Generating batch {self.current_batch} ({batch_size} records)")
                
                for i in range(batch_size):
                    # 15% chance of anomaly
                    inject_anomaly = random.random() < 0.15
                    
                    record = self.generate_supply_chain_record(inject_anomaly)
                    
                    if self.send_to_backend(record):
                        self.total_records_sent += 1
                        status = "🚨 ANOMALY" if inject_anomaly else "✅ NORMAL"
                        print(f"  {status} - {record['supplier']} -> {record['product']}")
                    else:
                        print(f"  ❌ Failed to send record")
                
                print(f"📊 Total sent: {self.total_records_sent} | Anomalies: {self.anomalies_injected}")
                
                # Wait before next batch (10-30 seconds)
                wait_time = random.randint(10, 30)
                time.sleep(wait_time)
                
            except Exception as e:
                print(f"❌ Simulation error: {e}")
                time.sleep(5)

    def start_simulation(self):
        """Start the data simulation"""
        if not self.running:
            self.running = True
            self.simulation_thread = threading.Thread(target=self.simulation_loop, daemon=True)
            self.simulation_thread.start()
            return True
        return False

    def stop_simulation(self):
        """Stop the data simulation"""
        self.running = False
        return True

# Global simulator instance
simulator = EnhancedDataSimulator()

# Web interface for monitoring
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Enhanced Data Simulator - CryptaNet</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { color: #2c3e50; text-align: center; margin-bottom: 30px; }
        .status { padding: 15px; margin: 10px 0; border-radius: 5px; }
        .running { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .stopped { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .stats { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0; }
        .stat-box { padding: 15px; background: #e9ecef; border-radius: 5px; text-align: center; }
        .controls { text-align: center; margin: 20px 0; }
        .button { padding: 10px 20px; margin: 5px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; }
        .start-btn { background: #28a745; color: white; }
        .stop-btn { background: #dc3545; color: white; }
        .refresh-btn { background: #007bff; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="header">🚀 Enhanced Data Simulator</h1>
        
        <div class="status {{ 'running' if status.running else 'stopped' }}">
            <strong>Status:</strong> {{ "🟢 RUNNING" if status.running else "🔴 STOPPED" }}
        </div>
        
        <div class="stats">
            <div class="stat-box">
                <h3>📊 Total Records Sent</h3>
                <h2>{{ status.total_records }}</h2>
            </div>
            <div class="stat-box">
                <h3>🚨 Anomalies Injected</h3>
                <h2>{{ status.anomalies_injected }}</h2>
            </div>
        </div>
        
        <div class="stats">
            <div class="stat-box">
                <h3>📦 Current Batch</h3>
                <h2>{{ status.current_batch }}</h2>
            </div>
            <div class="stat-box">
                <h3>🎯 Backend URL</h3>
                <p>{{ status.backend_url }}</p>
            </div>
        </div>
        
        <div class="controls">
            <a href="/start" class="button start-btn">▶️ Start Simulation</a>
            <a href="/stop" class="button stop-btn">⏹️ Stop Simulation</a>
            <a href="/" class="button refresh-btn">🔄 Refresh</a>
        </div>
        
        <div style="margin-top: 30px; padding: 15px; background: #f8f9fa; border-radius: 5px;">
            <h4>📋 Simulation Details:</h4>
            <ul>
                <li>Generates realistic supply chain transactions</li>
                <li>Injects anomalies at ~15% rate</li>
                <li>Variable batch sizes (3-8 records)</li>
                <li>Random intervals (10-30 seconds)</li>
                <li>Sends data to backend API on port 5004</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Dashboard showing simulator status"""
    status = {
        'running': simulator.running,
        'total_records': simulator.total_records_sent,
        'anomalies_injected': simulator.anomalies_injected,
        'current_batch': simulator.current_batch,
        'backend_url': simulator.backend_url
    }
    return render_template_string(DASHBOARD_HTML, status=status)

@app.route('/start')
def start_simulation():
    """Start the simulation"""
    if simulator.start_simulation():
        return jsonify({"status": "started", "message": "Simulation started successfully"})
    else:
        return jsonify({"status": "already_running", "message": "Simulation is already running"})

@app.route('/stop')
def stop_simulation():
    """Stop the simulation"""
    simulator.stop_simulation()
    return jsonify({"status": "stopped", "message": "Simulation stopped"})

@app.route('/status')
def get_status():
    """Get current status"""
    return jsonify({
        'running': simulator.running,
        'total_records_sent': simulator.total_records_sent,
        'anomalies_injected': simulator.anomalies_injected,
        'current_batch': simulator.current_batch,
        'backend_url': simulator.backend_url
    })

if __name__ == "__main__":
    print("🚀 Starting Enhanced Data Simulator")
    print("📊 Dashboard will be available at: http://localhost:8001")
    print("🔗 Backend API target: http://localhost:5004")
    
    # Auto-start simulation when script runs
    simulator.start_simulation()
    
    # Start web dashboard
    app.run(host='0.0.0.0', port=8001, debug=False)
