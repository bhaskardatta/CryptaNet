#!/usr/bin/env python3
"""
CryptaNet Data Simulator with Web Dashboard
==========================================

Enhanced version of the data simulator with a built-in web dashboard
for real-time monitoring and control.
"""

import json
import time
import random
import requests
import logging
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import html

# Import the main simulator class
from data_simulator import AdvancedDataSimulator, logger

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler for the web dashboard"""
    
    def __init__(self, *args, simulator=None, **kwargs):
        self.simulator = simulator
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.serve_dashboard()
        elif self.path == '/api/stats':
            self.serve_stats()
        elif self.path == '/api/control':
            self.serve_control()
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/control':
            self.handle_control()
        else:
            self.send_error(404)
    
    def serve_dashboard(self):
        """Serve the main dashboard HTML"""
        html_content = self.get_dashboard_html()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def serve_stats(self):
        """Serve current statistics as JSON"""
        if not self.simulator:
            stats = {"error": "Simulator not available"}
        else:
            stats = self.simulator.stats.copy()
            if stats['start_time']:
                runtime = datetime.now() - stats['start_time']
                stats['runtime_seconds'] = runtime.total_seconds()
                stats['runtime_formatted'] = str(runtime).split('.')[0]
                stats['rate_per_minute'] = stats['total_generated'] / max(runtime.total_seconds(), 1) * 60
                stats['anomaly_percentage'] = (stats['anomalies_generated'] / max(stats['total_generated'], 1)) * 100
                stats['success_percentage'] = (stats['successful_submissions'] / max(stats['total_generated'], 1)) * 100
            stats['is_running'] = self.simulator.running if self.simulator else False
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(stats).encode('utf-8'))
    
    def serve_control(self):
        """Serve control panel info"""
        control_info = {
            "actions": ["start", "stop", "pause", "resume"],
            "status": "running" if self.simulator and self.simulator.running else "stopped"
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(control_info).encode('utf-8'))
    
    def handle_control(self):
        """Handle control actions"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            action = data.get('action')
            response = {"status": "error", "message": "Unknown action"}
            
            if self.simulator:
                if action == "stop":
                    self.simulator.running = False
                    response = {"status": "success", "message": "Simulator stopped"}
                elif action == "start" and not self.simulator.running:
                    # This would need to be implemented differently for a real start
                    response = {"status": "info", "message": "Use the startup script to start the simulator"}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            error_response = {"status": "error", "message": str(e)}
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    def get_dashboard_html(self):
        """Generate the dashboard HTML"""
        return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CryptaNet Data Simulator Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
            padding: 20px;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        }
        .header { 
            text-align: center; 
            margin-bottom: 30px; 
            color: #4a5568;
        }
        .header h1 { 
            font-size: 2.5em; 
            margin-bottom: 10px; 
            color: #2d3748;
        }
        .status-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #f7fafc;
            padding: 15px 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            border-left: 5px solid #4299e1;
        }
        .status-indicator {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #48bb78;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
            border-left: 4px solid #4299e1;
            transition: transform 0.2s;
        }
        .stat-card:hover { transform: translateY(-2px); }
        .stat-card h3 {
            color: #4a5568;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 10px;
        }
        .stat-card .value {
            font-size: 2.5em;
            font-weight: bold;
            color: #2d3748;
            line-height: 1;
        }
        .stat-card .subtitle {
            color: #718096;
            font-size: 0.9em;
            margin-top: 5px;
        }
        .anomaly { border-left-color: #f56565; }
        .success { border-left-color: #48bb78; }
        .warning { border-left-color: #ed8936; }
        .controls {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
            margin-bottom: 20px;
        }
        .controls h3 {
            margin-bottom: 15px;
            color: #2d3748;
        }
        .btn {
            background: #4299e1;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            margin-right: 10px;
            font-weight: 500;
            transition: background 0.2s;
        }
        .btn:hover { background: #3182ce; }
        .btn.danger { background: #f56565; }
        .btn.danger:hover { background: #e53e3e; }
        .log-area {
            background: #1a202c;
            color: #e2e8f0;
            padding: 20px;
            border-radius: 12px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            height: 300px;
            overflow-y: auto;
            white-space: pre-wrap;
        }
        .error { color: #333; background: #fed7d7; }
        .offline { background: #e2e8f0; color: #4a5568; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 CryptaNet Data Simulator</h1>
            <p>Real-time Supply Chain Data Generation Dashboard</p>
        </div>
        
        <div class="status-bar">
            <div class="status-indicator">
                <div class="status-dot" id="statusDot"></div>
                <span id="statusText">Connecting...</span>
            </div>
            <div id="lastUpdate">Last update: Never</div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>Total Generated</h3>
                <div class="value" id="totalGenerated">0</div>
                <div class="subtitle" id="rateInfo">0 records/min</div>
            </div>
            
            <div class="stat-card anomaly">
                <h3>Anomalies Detected</h3>
                <div class="value" id="anomaliesGenerated">0</div>
                <div class="subtitle" id="anomalyRate">0%</div>
            </div>
            
            <div class="stat-card success">
                <h3>Successful Submissions</h3>
                <div class="value" id="successfulSubmissions">0</div>
                <div class="subtitle" id="successRate">0%</div>
            </div>
            
            <div class="stat-card warning">
                <h3>Failed Submissions</h3>
                <div class="value" id="failedSubmissions">0</div>
                <div class="subtitle" id="runtime">Runtime: 00:00:00</div>
            </div>
        </div>
        
        <div class="controls">
            <h3>Simulator Controls</h3>
            <button class="btn danger" onclick="stopSimulator()">⏹️ Stop Simulator</button>
            <button class="btn" onclick="refreshStats()">🔄 Refresh</button>
        </div>
        
        <div class="controls">
            <h3>System Log</h3>
            <div class="log-area" id="logArea">Loading simulator status...</div>
        </div>
    </div>

    <script>
        let updateInterval;
        let logMessages = [];
        
        function updateStats() {
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        setOfflineStatus();
                        return;
                    }
                    
                    setOnlineStatus(data.is_running);
                    
                    document.getElementById('totalGenerated').textContent = data.total_generated || 0;
                    document.getElementById('anomaliesGenerated').textContent = data.anomalies_generated || 0;
                    document.getElementById('successfulSubmissions').textContent = data.successful_submissions || 0;
                    document.getElementById('failedSubmissions').textContent = data.failed_submissions || 0;
                    
                    document.getElementById('rateInfo').textContent = 
                        (data.rate_per_minute || 0).toFixed(1) + ' records/min';
                    document.getElementById('anomalyRate').textContent = 
                        (data.anomaly_percentage || 0).toFixed(1) + '%';
                    document.getElementById('successRate').textContent = 
                        (data.success_percentage || 0).toFixed(1) + '%';
                    document.getElementById('runtime').textContent = 
                        'Runtime: ' + (data.runtime_formatted || '00:00:00');
                    
                    document.getElementById('lastUpdate').textContent = 
                        'Last update: ' + new Date().toLocaleTimeString();
                    
                    addLogMessage(
                        `📊 Stats: ${data.total_generated} total, ${data.anomalies_generated} anomalies, ` +
                        `${data.successful_submissions} successful`
                    );
                })
                .catch(error => {
                    setOfflineStatus();
                    console.error('Error fetching stats:', error);
                });
        }
        
        function setOnlineStatus(isRunning) {
            const dot = document.getElementById('statusDot');
            const text = document.getElementById('statusText');
            
            if (isRunning) {
                dot.style.background = '#48bb78';
                text.textContent = 'Simulator Running';
                text.style.color = '#48bb78';
            } else {
                dot.style.background = '#ed8936';
                text.textContent = 'Simulator Stopped';
                text.style.color = '#ed8936';
            }
        }
        
        function setOfflineStatus() {
            const dot = document.getElementById('statusDot');
            const text = document.getElementById('statusText');
            
            dot.style.background = '#e2e8f0';
            text.textContent = 'Simulator Offline';
            text.style.color = '#4a5568';
        }
        
        function addLogMessage(message) {
            const timestamp = new Date().toLocaleTimeString();
            logMessages.push(`[${timestamp}] ${message}`);
            
            // Keep only last 50 messages
            if (logMessages.length > 50) {
                logMessages.shift();
            }
            
            document.getElementById('logArea').textContent = logMessages.join('\\n');
            document.getElementById('logArea').scrollTop = document.getElementById('logArea').scrollHeight;
        }
        
        function stopSimulator() {
            if (confirm('Are you sure you want to stop the simulator?')) {
                fetch('/api/control', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({action: 'stop'})
                })
                .then(response => response.json())
                .then(data => {
                    addLogMessage('🛑 ' + data.message);
                })
                .catch(error => {
                    addLogMessage('❌ Error stopping simulator: ' + error);
                });
            }
        }
        
        function refreshStats() {
            updateStats();
            addLogMessage('🔄 Statistics refreshed manually');
        }
        
        // Initialize
        updateStats();
        updateInterval = setInterval(updateStats, 5000); // Update every 5 seconds
        
        addLogMessage('🚀 Dashboard initialized');
        addLogMessage('📡 Connecting to simulator...');
    </script>
</body>
</html>
        '''

class WebDashboardSimulator(AdvancedDataSimulator):
    """Enhanced simulator with web dashboard"""
    
    def __init__(self, config_file: Optional[str] = None, dashboard_port: int = 8080):
        super().__init__(config_file)
        self.dashboard_port = dashboard_port
        self.dashboard_server = None
        self.dashboard_thread = None
    
    def start_dashboard(self):
        """Start the web dashboard"""
        try:
            # Create a handler class with access to the simulator
            def make_handler(*args, **kwargs):
                return DashboardHandler(*args, simulator=self, **kwargs)
            
            self.dashboard_server = socketserver.TCPServer(("", self.dashboard_port), make_handler)
            self.dashboard_thread = threading.Thread(target=self.dashboard_server.serve_forever, daemon=True)
            self.dashboard_thread.start()
            
            logger.info(f"🌐 Web Dashboard started on http://localhost:{self.dashboard_port}")
            
        except Exception as e:
            logger.error(f"❌ Failed to start web dashboard: {e}")
    
    def stop_dashboard(self):
        """Stop the web dashboard"""
        if self.dashboard_server:
            self.dashboard_server.shutdown()
            self.dashboard_server = None
            logger.info("🛑 Web Dashboard stopped")
    
    def run_simulation_with_dashboard(self, interval: int = 10, max_records: Optional[int] = None):
        """Run simulation with web dashboard"""
        self.start_dashboard()
        
        try:
            self.run_simulation(interval, max_records)
        finally:
            self.stop_dashboard()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='CryptaNet Data Simulator with Web Dashboard')
    parser.add_argument('--config', '-c', help='Configuration file path')
    parser.add_argument('--interval', '-i', type=int, default=10, help='Interval between data points (seconds)')
    parser.add_argument('--max-records', '-m', type=int, help='Maximum number of records to generate')
    parser.add_argument('--dashboard-port', '-p', type=int, default=8080, help='Web dashboard port')
    parser.add_argument('--no-dashboard', action='store_true', help='Disable web dashboard')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        if args.no_dashboard:
            simulator = AdvancedDataSimulator(args.config)
            simulator.run_simulation(args.interval, args.max_records)
        else:
            simulator = WebDashboardSimulator(args.config, args.dashboard_port)
            print(f"\n🌐 Web Dashboard will be available at: http://localhost:{args.dashboard_port}")
            print("📊 Open this URL in your browser to monitor the simulation\n")
            simulator.run_simulation_with_dashboard(args.interval, args.max_records)
            
    except Exception as e:
        logger.error(f"💥 Failed to start simulator: {e}")
        import sys
        sys.exit(1)

if __name__ == "__main__":
    main()
