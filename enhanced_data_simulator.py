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
        self.interval_seconds = 10  # Default interval
        self.anomaly_rate = 0.25    # Target: 5 anomalies per 20 records (25%)
        self.anomaly_cycle = []     # Track anomaly pattern
        self.cycle_position = 0     # Current position in anomaly cycle
        
        # Initialize anomaly cycle: 5 anomalies in 20 records, randomly distributed
        self.reset_anomaly_cycle()
        
        # Supply chain entities with more randomization
        self.suppliers = [
            "GlobalTech Manufacturing", "PacificRim Industries", "EuroSupply Co",
            "AsiaLink Logistics", "NorthStar Materials", "MegaCorp Suppliers",
            "QuickShip Express", "ReliableSource Ltd", "FastTrack Supply",
            "QualityFirst Manufacturing", "TechnoCore Systems", "SupplyChain Direct",
            "MetroLogistics Inc", "AlphaSuppliers Corp", "BetaManufacturing Ltd"
        ]
        
        self.products = [
            "Semiconductor Chips", "LCD Displays", "Battery Packs", "Circuit Boards",
            "Sensors", "Microprocessors", "Memory Modules", "Cables & Connectors",
            "Power Supplies", "Cooling Systems", "Graphics Cards", "Storage Drives",
            "Network Equipment", "Control Units", "Display Panels", "Audio Components"
        ]
        
        self.locations = [
            "Shanghai, China", "Shenzhen, China", "Seoul, South Korea", "Tokyo, Japan",
            "Singapore", "Bangkok, Thailand", "Mumbai, India", "Kaohsiung, Taiwan",
            "Ho Chi Minh City, Vietnam", "Manila, Philippines", "Kuala Lumpur, Malaysia",
            "Jakarta, Indonesia", "Bangalore, India", "Guangzhou, China", "Busan, South Korea"
        ]

    def reset_anomaly_cycle(self):
        """Reset the anomaly cycle to ensure 5 anomalies per 20 records"""
        # Create a cycle of 20 records with exactly 5 anomalies
        cycle = [False] * 15 + [True] * 5  # 15 normal + 5 anomalies
        random.shuffle(cycle)  # Randomize positions
        self.anomaly_cycle = cycle
        self.cycle_position = 0

    def generate_supply_chain_record(self, inject_anomaly=False):
        """Generate a single supply chain record with enhanced randomization"""
        base_timestamp = datetime.now()
        
        # Enhanced normal ranges with more variety
        normal_cost_range = (50, 500)
        normal_quantity_range = (100, 1000)
        normal_delivery_days = (5, 14)
        normal_quality_score = (85, 98)
        
        # More randomized selection - initialize all variables
        supplier = random.choice(self.suppliers)
        product = random.choice(self.products)
        location = random.choice(self.locations)
        
        # Initialize default values for all variables
        cost = random.uniform(*normal_cost_range)
        quantity = random.randint(*normal_quantity_range)
        delivery_time = random.randint(*normal_delivery_days)
        quality_score = random.uniform(*normal_quality_score)
        
        if inject_anomaly:
            # Enhanced anomaly types with more variety
            anomaly_type = random.choice([
                "extreme_cost_spike", "massive_quantity_anomaly", "severe_delivery_delay", 
                "critical_quality_drop", "suspicious_location", "timing_anomaly",
                "price_dumping", "counterfeit_risk", "supplier_inconsistency"
            ])
            
            if anomaly_type == "extreme_cost_spike":
                cost = random.uniform(normal_cost_range[1] * 2, normal_cost_range[1] * 4)  # 200-400% spike
                quantity = random.randint(*normal_quantity_range)
                delivery_time = random.randint(*normal_delivery_days)
                quality_score = random.uniform(*normal_quality_score)
                
            elif anomaly_type == "price_dumping":
                cost = random.uniform(5, normal_cost_range[0] * 0.3)  # Suspiciously low
                quantity = random.randint(normal_quantity_range[1], normal_quantity_range[1] * 2)
                delivery_time = random.randint(*normal_delivery_days)
                quality_score = random.uniform(60, 80)
                
            elif anomaly_type == "massive_quantity_anomaly":
                cost = random.uniform(*normal_cost_range)
                quantity = random.choice([5, 15, 10000, 15000])  # Extremely low or high
                delivery_time = random.randint(*normal_delivery_days)
                quality_score = random.uniform(*normal_quality_score)
                
            elif anomaly_type == "severe_delivery_delay":
                cost = random.uniform(*normal_cost_range)
                quantity = random.randint(*normal_quantity_range)
                delivery_time = random.randint(25, 60)  # Severe delay
                quality_score = random.uniform(70, 85)
                
            elif anomaly_type == "critical_quality_drop":
                cost = random.uniform(*normal_cost_range)
                quantity = random.randint(*normal_quantity_range)
                delivery_time = random.randint(*normal_delivery_days)
                quality_score = random.uniform(20, 50)  # Critical quality issues
                
            elif anomaly_type == "suspicious_location":
                cost = random.uniform(*normal_cost_range)
                quantity = random.randint(*normal_quantity_range)
                delivery_time = random.randint(*normal_delivery_days)
                quality_score = random.uniform(*normal_quality_score)
                location = random.choice([
                    "Unknown Location", "Restricted Zone", "Unverified Source",
                    "Blacklisted Region", "Embargo Territory", "High-Risk Area"
                ])
                
            elif anomaly_type == "timing_anomaly":
                cost = random.uniform(*normal_cost_range)
                quantity = random.randint(*normal_quantity_range)
                delivery_time = random.randint(*normal_delivery_days)
                quality_score = random.uniform(*normal_quality_score)
                base_timestamp = base_timestamp.replace(
                    hour=random.choice([1, 2, 3, 4, 23]), 
                    minute=random.randint(0, 59)
                )
                
            elif anomaly_type == "supplier_inconsistency":
                supplier = "UNKNOWN_SUPPLIER_" + str(random.randint(1000, 9999))
                cost = random.uniform(normal_cost_range[0] * 0.5, normal_cost_range[1] * 2)
                quantity = random.randint(*normal_quantity_range)
                delivery_time = random.randint(normal_delivery_days[1], 30)
                quality_score = random.uniform(40, 90)
                
            else:  # counterfeit_risk
                cost = random.uniform(normal_cost_range[0] * 0.3, normal_cost_range[0] * 0.7)
                quantity = random.randint(*normal_quantity_range)
                delivery_time = random.randint(3, 7)  # Too fast
                quality_score = random.uniform(30, 60)
                
            self.anomalies_injected += 1
            
        # If not inject_anomaly, we use the default values initialized above

        # Generate unique transaction ID and comprehensive blockchain information
        timestamp_part = int(time.time() * 1000)
        random_part = random.randint(10000, 99999)
        
        # Generate realistic blockchain transaction data
        block_number = random.randint(1500000, 2000000)
        tx_hash = f"0x{random.getrandbits(256):064x}"
        block_hash = f"0x{random.getrandbits(256):064x}"
        gas_used = random.randint(21000, 85000)
        network_fee = round(random.uniform(0.001, 0.025), 6)
        consensus_score = round(random.uniform(0.95, 1.0), 3)
        
        record = {
            "organizationId": f"Supplier-{random.randint(1, 15):02d}",
            "dataType": "supply_chain",
            "data": {
                "transaction_id": f"TXN_{timestamp_part}_{random_part}",
                "timestamp": base_timestamp.isoformat(),
                "supplier": supplier,
                "product": product,
                "productId": f"PROD-{random.randint(1000, 9999)}",
                "quantity": quantity,
                "cost_per_unit": round(cost, 2),
                "total_cost": round(cost * quantity, 2),
                "delivery_time_days": delivery_time,
                "quality_score": round(quality_score, 1),
                "temperature": round(random.uniform(18, 28), 2),  # Add temperature for anomaly detection
                "humidity": round(random.uniform(40, 80), 2),     # Add humidity for anomaly detection
                "location": location,
                "batch_id": f"BATCH_{self.current_batch}",
                "injected_anomaly": inject_anomaly,
                "anomaly_severity": "high" if inject_anomaly and random.random() > 0.6 else ("medium" if inject_anomaly else "none")
            },
            "location": location,
            # Enhanced blockchain transaction details
            "blockchain": {
                "transactionId": tx_hash,
                "blockNumber": block_number,
                "blockHash": block_hash,
                "blockTimestamp": base_timestamp.isoformat(),
                "gasUsed": gas_used,
                "networkFee": network_fee,
                "consensusScore": consensus_score,
                "validatorNodes": random.randint(3, 7),
                "networkLatency": round(random.uniform(0.1, 2.5), 2),
                "dataIntegrityHash": f"0x{random.getrandbits(160):040x}",
                "encryptionType": "AES-256-GCM",
                "merkleRoot": f"0x{random.getrandbits(256):064x}",
                "previousBlockHash": f"0x{random.getrandbits(256):064x}",
                "nonce": random.randint(1000000, 9999999),
                "difficulty": round(random.uniform(15.0, 25.0), 2),
                "chainId": "cryptanet-supply-chain",
                "organizationMSP": f"Supplier-{random.randint(1, 15):02d}MSP"
            }
        }
        
        return record

    def send_to_backend(self, record):
        """Send record to backend API"""
        try:
            response = requests.post(
                f"{self.backend_url}/api/supply-chain/submit",
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
        """Main simulation loop with guaranteed anomaly pattern"""
        print("🚀 Enhanced Data Simulator started")
        print(f"📡 Sending data to: {self.backend_url}")
        print(f"🎯 Target: 5 anomalies per 20 records (25%)")
        
        while self.running:
            try:
                # Generate batch of records with more variety
                batch_size = random.randint(2, 6)  # Smaller, more frequent batches
                self.current_batch += 1
                
                print(f"\n📦 Generating batch {self.current_batch} ({batch_size} records)")
                
                batch_anomalies = 0
                for i in range(batch_size):
                    # Use cycle-based anomaly determination
                    inject_anomaly = self.anomaly_cycle[self.cycle_position]
                    self.cycle_position = (self.cycle_position + 1) % len(self.anomaly_cycle)
                    
                    # Reset cycle when complete
                    if self.cycle_position == 0:
                        self.reset_anomaly_cycle()
                        print(f"🔄 Anomaly cycle reset - maintaining 5/20 ratio")
                    
                    record = self.generate_supply_chain_record(inject_anomaly)
                    
                    if self.send_to_backend(record):
                        self.total_records_sent += 1
                        if inject_anomaly:
                            batch_anomalies += 1
                        status = "🚨 ANOMALY" if inject_anomaly else "✅ NORMAL"
                        supplier_name = record['data']['supplier']
                        product_name = record['data']['product']
                        print(f"  {status} - {supplier_name} -> {product_name}")
                    else:
                        print(f"  ❌ Failed to send record")
                
                anomaly_rate_actual = (self.anomalies_injected / max(self.total_records_sent, 1)) * 100
                print(f"📊 Total sent: {self.total_records_sent} | Anomalies: {self.anomalies_injected} ({anomaly_rate_actual:.1f}%)")
                
                # Randomized wait time to prevent predictable patterns
                base_wait = self.interval_seconds
                jitter = random.uniform(-0.5, 0.5) * base_wait  # ±50% jitter
                wait_time = max(1, base_wait + jitter)
                time.sleep(wait_time)
                
            except Exception as e:
                print(f"❌ Simulation error: {e}")
                import traceback
                traceback.print_exc()
                time.sleep(5)

    def start_simulation(self, interval_seconds=None, anomaly_rate=None):
        """Start the data simulation"""
        if interval_seconds is not None:
            self.interval_seconds = interval_seconds
        if anomaly_rate is not None:
            self.anomaly_rate = anomaly_rate
            
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
