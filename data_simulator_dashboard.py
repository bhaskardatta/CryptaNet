#!/usr/bin/env python3
"""
CryptaNet Data Simulator Dashboard
Web interface for real-time supply chain data generation and visualization
"""

import json
import time
import random
import os
import sys
from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template_string, request

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the enhanced data simulator
from enhanced_data_simulator import EnhancedDataSimulator

app = Flask(__name__)
simulator = EnhancedDataSimulator()

# HTML template for dashboard
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>CryptaNet Data Simulator Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
    <style>
        body { background-color: #f8f9fa; padding: 20px; }
        .card { margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .card-header { font-weight: bold; }
        .stats-value { font-size: 2em; font-weight: bold; }
        .log-entry { margin: 5px 0; padding: 8px; border-radius: 4px; }
        .log-normal { background-color: #e9ecef; }
        .log-anomaly { background-color: #f8d7da; }
        .refresh-timer { font-size: 0.8em; color: #6c757d; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="mb-4">CryptaNet Data Simulator Dashboard</h1>
        
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        Control Panel
                    </div>
                    <div class="card-body">
                        <div class="d-flex justify-content-between mb-3">
                            <button id="startBtn" class="btn btn-success">Start Simulation</button>
                            <button id="stopBtn" class="btn btn-danger" disabled>Stop Simulation</button>
                        </div>
                        <div class="form-group mb-3">
                            <label for="intervalSelect">Generation Interval (seconds):</label>
                            <select id="intervalSelect" class="form-control">
                                <option value="1">1 second</option>
                                <option value="5" selected>5 seconds</option>
                                <option value="10">10 seconds</option>
                                <option value="30">30 seconds</option>
                                <option value="60">60 seconds</option>
                            </select>
                        </div>
                        <div class="form-group mb-3">
                            <label for="anomalyRateSelect">Anomaly Injection Rate:</label>
                            <select id="anomalyRateSelect" class="form-control">
                                <option value="0">None (0%)</option>
                                <option value="0.05" selected>Low (5%)</option>
                                <option value="0.15">Medium (15%)</option>
                                <option value="0.30">High (30%)</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header bg-info text-white">
                        Simulation Statistics
                    </div>
                    <div class="card-body">
                        <div class="row text-center">
                            <div class="col-md-4">
                                <div>Total Records</div>
                                <div id="totalRecords" class="stats-value">0</div>
                            </div>
                            <div class="col-md-4">
                                <div>Anomalies</div>
                                <div id="totalAnomalies" class="stats-value">0</div>
                            </div>
                            <div class="col-md-4">
                                <div>Status</div>
                                <div id="status" class="stats-value text-warning">Idle</div>
                            </div>
                        </div>
                        <div class="text-center mt-3">
                            <div id="refreshTimer" class="refresh-timer">Next refresh: 5s</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="card-header bg-dark text-white">
                Activity Log
            </div>
            <div class="card-body">
                <div id="activityLog" style="height: 300px; overflow-y: auto;">
                    <div class="log-entry log-normal">
                        <strong>[{{current_time}}]</strong> System initialized and ready.
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let timer;
        let timerValue = 5;
        
        // Update UI based on simulator status
        function updateStatus() {
            fetch('/stats')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('totalRecords').textContent = data.total_records_sent;
                    document.getElementById('totalAnomalies').textContent = data.anomalies_injected;
                    
                    if (data.running) {
                        document.getElementById('status').textContent = 'Running';
                        document.getElementById('status').className = 'stats-value text-success';
                        document.getElementById('startBtn').disabled = true;
                        document.getElementById('stopBtn').disabled = false;
                    } else {
                        document.getElementById('status').textContent = 'Stopped';
                        document.getElementById('status').className = 'stats-value text-danger';
                        document.getElementById('startBtn').disabled = false;
                        document.getElementById('stopBtn').disabled = true;
                    }
                })
                .catch(error => console.error('Error fetching status:', error));
        }
        
        // Get recent activity
        function updateActivityLog() {
            fetch('/recent-activity')
                .then(response => response.json())
                .then(data => {
                    const logContainer = document.getElementById('activityLog');
                    
                    // Clear existing entries if needed
                    if (data.reset_log) {
                        logContainer.innerHTML = '';
                    }
                    
                    // Add new entries
                    data.activities.forEach(activity => {
                        const entry = document.createElement('div');
                        entry.className = activity.is_anomaly ? 'log-entry log-anomaly' : 'log-entry log-normal';
                        entry.innerHTML = `<strong>[${activity.timestamp}]</strong> ${activity.message}`;
                        logContainer.appendChild(entry);
                    });
                    
                    // Scroll to bottom
                    logContainer.scrollTop = logContainer.scrollHeight;
                })
                .catch(error => console.error('Error updating activity log:', error));
        }
        
        // Start the timer for UI updates
        function startTimer() {
            clearInterval(timer);
            timerValue = 5;
            updateTimerDisplay();
            
            timer = setInterval(() => {
                timerValue -= 1;
                updateTimerDisplay();
                
                if (timerValue <= 0) {
                    updateStatus();
                    updateActivityLog();
                    timerValue = 5;
                }
            }, 1000);
        }
        
        function updateTimerDisplay() {
            document.getElementById('refreshTimer').textContent = `Next refresh: ${timerValue}s`;
        }
        
        // Set up event handlers
        document.getElementById('startBtn').addEventListener('click', () => {
            const interval = document.getElementById('intervalSelect').value;
            const anomalyRate = document.getElementById('anomalyRateSelect').value;
            
            fetch('/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    interval: parseInt(interval),
                    anomaly_rate: parseFloat(anomalyRate)
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    updateStatus();
                    updateActivityLog();
                }
            })
            .catch(error => console.error('Error starting simulation:', error));
        });
        
        document.getElementById('stopBtn').addEventListener('click', () => {
            fetch('/stop', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        updateStatus();
                        updateActivityLog();
                    }
                })
                .catch(error => console.error('Error stopping simulation:', error));
        });
        
        // Initialize
        updateStatus();
        updateActivityLog();
        startTimer();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(
        DASHBOARD_TEMPLATE, 
        current_time=datetime.now().strftime('%H:%M:%S')
    )

@app.route('/stats')
def stats():
    """Return simulator statistics"""
    return jsonify({
        "total_records_sent": simulator.total_records_sent,
        "anomalies_injected": simulator.anomalies_injected,
        "running": simulator.running,
        "current_batch": simulator.current_batch
    })

@app.route('/start', methods=['POST'])
def start_simulation():
    """Start the data simulation"""
    params = request.json
    interval = params.get('interval', 5)
    anomaly_rate = params.get('anomaly_rate', 0.05)
    
    if not simulator.running:
        simulator.start_simulation(interval_seconds=interval, anomaly_rate=anomaly_rate)
        return jsonify({"status": "success", "message": "Simulation started"})
    
    return jsonify({"status": "error", "message": "Simulation already running"})

@app.route('/stop', methods=['POST'])
def stop_simulation():
    """Stop the data simulation"""
    if simulator.running:
        simulator.stop_simulation()
        return jsonify({"status": "success", "message": "Simulation stopped"})
    
    return jsonify({"status": "error", "message": "Simulation not running"})

# Store recent activities
recent_activities = []

@app.route('/recent-activity')
def get_recent_activity():
    """Get recent activity log entries"""
    return jsonify({
        "activities": recent_activities[-20:],  # Last 20 entries
        "reset_log": False
    })

@app.route('/log-activity', methods=['POST'])
def log_activity():
    """Add an entry to the activity log (internal use)"""
    data = request.json
    entry = {
        "timestamp": datetime.now().strftime('%H:%M:%S'),
        "message": data.get("message", "Unknown activity"),
        "is_anomaly": data.get("is_anomaly", False)
    }
    
    recent_activities.append(entry)
    # Keep only the last 100 entries
    if len(recent_activities) > 100:
        recent_activities.pop(0)
        
    return jsonify({"status": "success"})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8001))
    app.run(host='0.0.0.0', port=port, debug=True)
