#!/usr/bin/env python3
"""
Real-Time Alerting System for Supply Chain Monitoring
Provides immediate notifications for critical anomalies and system issues
"""

import smtplib
import json
import requests
import time
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import threading
from typing import Dict, List, Any
import sqlite3
import os
import schedule

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('alerting_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AlertingSystem:
    """Real-time alerting system for supply chain anomalies"""
    
    def __init__(self):
        self.db_path = "alerts.db"
        self.init_database()
        self.alert_channels = {
            'email': True,
            'console': True,
            'webhook': False,  # Can be enabled for Slack/Teams integration
            'log': True
        }
        
        # Alert configuration
        self.alert_rules = {
            'critical_temperature': {'threshold': 40, 'enabled': True},
            'critical_humidity': {'threshold': 95, 'enabled': True},
            'rapid_change': {'threshold': 15, 'enabled': True},
            'system_down': {'threshold': 3, 'enabled': True},  # 3 consecutive failures
            'anomaly_cluster': {'threshold': 5, 'enabled': True}  # 5 anomalies in 10 minutes
        }
        
        # Email configuration (would need real SMTP settings in production)
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'sender_email': 'supply.chain.alerts@company.com',
            'sender_password': 'your_password',  # Use environment variable in production
            'recipients': ['admin@company.com', 'ops@company.com']
        }
        
        # Webhook configuration for Slack/Teams
        self.webhook_config = {
            'slack_url': 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK',
            'teams_url': 'https://outlook.office.com/webhook/YOUR/TEAMS/WEBHOOK'
        }
        
        self.alert_cooldown = {}  # Prevent spam alerts
        self.cooldown_period = 300  # 5 minutes
        
    def init_database(self):
        """Initialize SQLite database for alert tracking"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    alert_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    source TEXT NOT NULL,
                    message TEXT NOT NULL,
                    details TEXT,
                    resolved BOOLEAN DEFAULT FALSE,
                    resolved_at TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alert_stats (
                    date TEXT PRIMARY KEY,
                    total_alerts INTEGER DEFAULT 0,
                    critical_alerts INTEGER DEFAULT 0,
                    resolved_alerts INTEGER DEFAULT 0,
                    avg_resolution_time REAL DEFAULT 0
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Alert database initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
    
    def store_alert(self, alert: Dict[str, Any]) -> int:
        """Store alert in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO alerts (timestamp, alert_type, severity, source, message, details)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                alert['timestamp'],
                alert['type'],
                alert['severity'],
                alert['source'],
                alert['message'],
                json.dumps(alert.get('details', {}))
            ))
            
            alert_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return alert_id
            
        except Exception as e:
            logger.error(f"Error storing alert: {e}")
            return -1
    
    def check_cooldown(self, alert_key: str) -> bool:
        """Check if alert is in cooldown period"""
        now = time.time()
        if alert_key in self.alert_cooldown:
            if now - self.alert_cooldown[alert_key] < self.cooldown_period:
                return True
        
        self.alert_cooldown[alert_key] = now
        return False
    
    def send_email_alert(self, alert: Dict[str, Any]):
        """Send email alert"""
        try:
            if not self.alert_channels['email']:
                return
            
            msg = MIMEMultipart()
            msg['From'] = self.email_config['sender_email']
            msg['To'] = ', '.join(self.email_config['recipients'])
            msg['Subject'] = f"🚨 Supply Chain Alert - {alert['severity'].upper()}: {alert['type']}"
            
            body = f"""
            Supply Chain Monitoring Alert
            =============================
            
            Timestamp: {alert['timestamp']}
            Alert Type: {alert['type']}
            Severity: {alert['severity']}
            Source: {alert['source']}
            
            Message: {alert['message']}
            
            Details:
            {json.dumps(alert.get('details', {}), indent=2)}
            
            Please investigate immediately if this is a critical alert.
            
            ---
            Automated Supply Chain Monitoring System
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Note: In production, use proper SMTP credentials
            logger.info(f"Email alert would be sent: {alert['message']}")
            
        except Exception as e:
            logger.error(f"Error sending email alert: {e}")
    
    def send_webhook_alert(self, alert: Dict[str, Any]):
        """Send webhook alert to Slack/Teams"""
        try:
            if not self.alert_channels['webhook']:
                return
            
            # Slack format
            slack_payload = {
                "text": f"🚨 Supply Chain Alert - {alert['severity'].upper()}",
                "attachments": [
                    {
                        "color": "danger" if alert['severity'] == 'critical' else "warning",
                        "fields": [
                            {"title": "Type", "value": alert['type'], "short": True},
                            {"title": "Source", "value": alert['source'], "short": True},
                            {"title": "Message", "value": alert['message'], "short": False},
                            {"title": "Timestamp", "value": alert['timestamp'], "short": True}
                        ]
                    }
                ]
            }
            
            # Note: In production, would actually send to webhook
            logger.info(f"Webhook alert would be sent: {alert['message']}")
            
        except Exception as e:
            logger.error(f"Error sending webhook alert: {e}")
    
    def send_console_alert(self, alert: Dict[str, Any]):
        """Display alert in console"""
        if not self.alert_channels['console']:
            return
        
        severity_colors = {
            'critical': '\033[91m',  # Red
            'high': '\033[93m',      # Yellow
            'medium': '\033[94m',    # Blue
            'low': '\033[92m'        # Green
        }
        
        reset_color = '\033[0m'
        color = severity_colors.get(alert['severity'], '')
        
        print(f"\n{color}🚨 ALERT - {alert['severity'].upper()}{reset_color}")
        print(f"⏰ Time: {alert['timestamp']}")
        print(f"📋 Type: {alert['type']}")
        print(f"🔍 Source: {alert['source']}")
        print(f"💬 Message: {alert['message']}")
        if alert.get('details'):
            print(f"📊 Details: {json.dumps(alert['details'], indent=2)}")
        print("-" * 60)
    
    def create_alert(self, alert_type: str, severity: str, source: str, 
                    message: str, details: Dict = None) -> int:
        """Create and send alert"""
        try:
            alert = {
                'timestamp': datetime.now().isoformat(),
                'type': alert_type,
                'severity': severity,
                'source': source,
                'message': message,
                'details': details or {}
            }
            
            # Check cooldown to prevent spam
            alert_key = f"{alert_type}_{source}"
            if self.check_cooldown(alert_key):
                logger.info(f"Alert {alert_key} is in cooldown period")
                return -1
            
            # Store alert
            alert_id = self.store_alert(alert)
            
            # Send alerts through all enabled channels
            self.send_console_alert(alert)
            self.send_email_alert(alert)
            self.send_webhook_alert(alert)
            
            if self.alert_channels['log']:
                logger.warning(f"ALERT [{alert['severity']}]: {alert['message']}")
            
            return alert_id
            
        except Exception as e:
            logger.error(f"Error creating alert: {e}")
            return -1
    
    def send_alert(self, alert_type: str, message: str, severity: str = 'medium', 
                   source: str = 'system', metadata: Dict = None) -> int:
        """Send alert using the create_alert method (compatibility wrapper)"""
        return self.create_alert(alert_type, severity, source, message, metadata)
    
    def check_supply_chain_anomalies(self):
        """Check for supply chain anomalies"""
        try:
            # Fetch recent data from backend
            response = requests.get('http://localhost:5004/api/supply-chain/query', timeout=10)
            if response.status_code != 200:
                self.create_alert(
                    'system_connectivity',
                    'critical',
                    'backend_api',
                    'Backend API is not responding',
                    {'status_code': response.status_code}
                )
                return
            
            data = response.json()
            if not data.get('success'):
                self.create_alert(
                    'data_quality',
                    'high',
                    'backend_api',
                    'Backend API returned error',
                    {'response': data}
                )
                return
            
            # Check for anomalies using advanced detection
            anomaly_response = requests.post(
                'http://localhost:5000/detect',  # Would need to expose advanced detection as API
                json={'data': data.get('data', [])},
                timeout=30
            )
            
            # For now, use built-in rule checking
            records = data.get('data', [])
            current_time = datetime.now()
            
            for record in records:
                record_data = record.get('data', {})
                
                # Extract temperature and humidity
                if 'environmental' in record_data:
                    env_data = record_data['environmental']
                    temp = env_data.get('temperature', record_data.get('temperature', 0))
                    humidity = env_data.get('humidity', record_data.get('humidity', 0))
                else:
                    temp = record_data.get('temperature', 0)
                    humidity = record_data.get('humidity', 0)
                
                product_id = record_data.get('productId', record.get('productId', 'Unknown'))
                
                # Check critical temperature
                if self.alert_rules['critical_temperature']['enabled'] and temp > self.alert_rules['critical_temperature']['threshold']:
                    self.create_alert(
                        'critical_temperature',
                        'critical',
                        f'product_{product_id}',
                        f'Critical temperature detected: {temp}°C for product {product_id}',
                        {'temperature': temp, 'product_id': product_id, 'record': record}
                    )
                
                # Check critical humidity
                if self.alert_rules['critical_humidity']['enabled'] and humidity > self.alert_rules['critical_humidity']['threshold']:
                    self.create_alert(
                        'critical_humidity',
                        'critical',
                        f'product_{product_id}',
                        f'Critical humidity detected: {humidity}% for product {product_id}',
                        {'humidity': humidity, 'product_id': product_id, 'record': record}
                    )
                
                # Check if anomaly was injected (for testing)
                if record_data.get('is_anomaly_injected'):
                    self.create_alert(
                        'anomaly_detected',
                        'high',
                        f'product_{product_id}',
                        f'Anomaly detected for product {product_id}',
                        {'product_id': product_id, 'scenario': record_data.get('scenario'), 'record': record}
                    )
            
        except requests.RequestException as e:
            self.create_alert(
                'system_connectivity',
                'critical',
                'backend_api',
                f'Failed to connect to backend API: {str(e)}',
                {'error': str(e)}
            )
        except Exception as e:
            logger.error(f"Error checking supply chain anomalies: {e}")
    
    def check_system_health(self):
        """Check overall system health"""
        try:
            services = [
                ('backend', 'http://localhost:5004/health'),
                ('frontend', 'http://localhost:3000'),
            ]
            
            for service_name, url in services:
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code != 200:
                        self.create_alert(
                            'service_degraded',
                            'high',
                            service_name,
                            f'{service_name.title()} service is responding with status {response.status_code}',
                            {'status_code': response.status_code, 'url': url}
                        )
                except requests.RequestException:
                    self.create_alert(
                        'service_down',
                        'critical',
                        service_name,
                        f'{service_name.title()} service is not responding',
                        {'url': url}
                    )
            
        except Exception as e:
            logger.error(f"Error checking system health: {e}")
    
    def get_alert_statistics(self) -> Dict[str, Any]:
        """Get alert statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get today's stats
            today = datetime.now().date().isoformat()
            
            cursor.execute('SELECT COUNT(*) FROM alerts WHERE DATE(created_at) = ?', (today,))
            today_alerts = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM alerts WHERE severity = "critical" AND DATE(created_at) = ?', (today,))
            today_critical = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM alerts WHERE resolved = 1 AND DATE(created_at) = ?', (today,))
            today_resolved = cursor.fetchone()[0]
            
            # Get recent alerts
            cursor.execute('''
                SELECT alert_type, severity, message, timestamp 
                FROM alerts 
                ORDER BY created_at DESC 
                LIMIT 10
            ''')
            recent_alerts = cursor.fetchall()
            
            conn.close()
            
            return {
                'today_total': today_alerts,
                'today_critical': today_critical,
                'today_resolved': today_resolved,
                'resolution_rate': (today_resolved / today_alerts * 100) if today_alerts > 0 else 0,
                'recent_alerts': [
                    {'type': row[0], 'severity': row[1], 'message': row[2], 'timestamp': row[3]}
                    for row in recent_alerts
                ]
            }
            
        except Exception as e:
            logger.error(f"Error getting alert statistics: {e}")
            return {}
    
    def get_recent_alerts(self, limit: int = 10, severity_filter: str = None) -> List[Dict]:
        """Get recent alerts from database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT id, timestamp, alert_type, severity, source, message, details
                    FROM alerts
                """
                params = []
                
                if severity_filter:
                    query += " WHERE severity = ?"
                    params.append(severity_filter)
                
                query += " ORDER BY timestamp DESC LIMIT ?"
                params.append(limit)
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                alerts = []
                for row in rows:
                    alert = {
                        'id': row[0],
                        'timestamp': row[1],
                        'type': row[2],  # Map alert_type to type for consistency
                        'severity': row[3],
                        'source': row[4],
                        'message': row[5],
                        'details': json.loads(row[6]) if row[6] else {}
                    }
                    alerts.append(alert)
                
                return alerts
                
        except Exception as e:
            logger.error(f"Error retrieving recent alerts: {e}")
            return []

    def run_monitoring_loop(self):
        """Main monitoring loop"""
        logger.info("Starting real-time monitoring loop...")
        
        # Schedule checks
        schedule.every(30).seconds.do(self.check_supply_chain_anomalies)
        schedule.every(1).minutes.do(self.check_system_health)
        
        while True:
            try:
                schedule.run_pending()
                time.sleep(10)  # Check every 10 seconds
            except KeyboardInterrupt:
                logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(30)  # Wait before retrying

def main():
    """Main function for testing"""
    print("🚨 Real-Time Alerting System Starting...")
    
    alerting = AlertingSystem()
    
    # Test alerts
    print("\n📋 Testing alert system...")
    
    alerting.create_alert(
        'system_test',
        'medium',
        'test_source',
        'This is a test alert to verify the system is working',
        {'test': True, 'timestamp': datetime.now().isoformat()}
    )
    
    # Check current system status
    print("\n🔍 Checking supply chain anomalies...")
    alerting.check_supply_chain_anomalies()
    
    print("\n🏥 Checking system health...")
    alerting.check_system_health()
    
    # Show statistics
    stats = alerting.get_alert_statistics()
    print(f"\n📊 Alert Statistics:")
    print(f"Today's alerts: {stats.get('today_total', 0)}")
    print(f"Critical alerts: {stats.get('today_critical', 0)}")
    print(f"Resolved alerts: {stats.get('today_resolved', 0)}")
    print(f"Resolution rate: {stats.get('resolution_rate', 0):.1f}%")
    
    # Ask if user wants to start continuous monitoring
    print(f"\n🔄 To start continuous monitoring, uncomment the monitoring loop call")
    print(f"   This will continuously check for anomalies and system issues")
    
    # Uncomment to start continuous monitoring
    # alerting.run_monitoring_loop()

if __name__ == "__main__":
    main()
