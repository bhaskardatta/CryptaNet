#!/usr/bin/env python3
"""
Integrated Advanced Supply Chain Analytics System
Combines anomaly detection, predictive analytics, and real-time alerting
"""

import time
import logging
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any
import threading
import schedule

# Import our advanced systems
import advanced_anomaly_detection as aad
import predictive_analytics as pa
import real_time_alerting as rta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('integrated_analytics.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class IntegratedAnalyticsSystem:
    """
    Integrated system combining anomaly detection, predictive analytics, and alerting
    """
    
    def __init__(self):
        self.anomaly_detector = aad.AdvancedAnomalyDetector()
        self.predictive_analytics = pa.PredictiveAnalytics()
        self.alerting_system = rta.AlertingSystem()
        
        self.is_running = False
        self.monitoring_thread = None
        
        # System metrics
        self.metrics = {
            'total_predictions': 0,
            'anomalies_detected': 0,
            'alerts_sent': 0,
            'last_analysis_time': None,
            'system_health': 'healthy'
        }
        
        logger.info("Integrated Analytics System initialized")
    
    def start_continuous_monitoring(self, interval_minutes: int = 30):
        """Start continuous monitoring and analysis"""
        logger.info(f"Starting continuous monitoring (interval: {interval_minutes} minutes)")
        
        self.is_running = True
        
        # Schedule periodic analysis
        schedule.every(interval_minutes).minutes.do(self.run_comprehensive_analysis)
        
        # Start monitoring thread
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        logger.info("Continuous monitoring started")
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        logger.info("Stopping continuous monitoring")
        self.is_running = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("Monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(60)
    
    def run_comprehensive_analysis(self) -> Dict[str, Any]:
        """Run comprehensive analysis combining all systems"""
        logger.info("Starting comprehensive analysis")
        
        try:
            analysis_start = datetime.now()
            results = {
                'timestamp': analysis_start.isoformat(),
                'anomaly_detection': {},
                'predictive_analytics': {},
                'risk_assessment': {},
                'alerts': [],
                'system_metrics': {},
                'recommendations': [],
                'total_records': 0  # Initialize total_records field
            }
            
            # 1. Fetch data for analysis
            logger.info("Fetching data for analysis...")
            data = self._fetch_supply_chain_data()
            
            # Set total_records based on fetched data
            results['total_records'] = len(data) if data else 0
            logger.info(f"Total records for analysis: {results['total_records']}")
            
            # 2. Anomaly Detection
            logger.info("Running anomaly detection...")
            if data:
                anomaly_results = self.anomaly_detector.detect_anomalies(data)
                results['anomaly_detection'] = anomaly_results
                
                # Count anomalies
                if anomaly_results.get('anomalies'):
                    anomaly_count = len(anomaly_results['anomalies'])
                    self.metrics['anomalies_detected'] += anomaly_count
                    logger.info(f"Detected {anomaly_count} anomalies")
                    
                    # Send alerts for critical anomalies
                    for anomaly in anomaly_results['anomalies']:
                        if anomaly.get('severity') == 'HIGH':
                            self.alerting_system.send_alert(
                                alert_type='anomaly_critical',
                                message=f"Critical anomaly detected: {anomaly.get('description', 'Unknown')}",
                                severity='critical',
                                metadata=anomaly
                            )
                            results['alerts'].append({
                                'type': 'anomaly_critical',
                                'message': anomaly.get('description'),
                                'timestamp': datetime.now().isoformat()
                            })
            else:
                logger.warning("No data available for anomaly detection")
                results['anomaly_detection'] = {'error': 'No data available'}
            
            # 2. Predictive Analytics
            logger.info("Running predictive analytics...")
            
            # Fetch data for prediction
            df = self.predictive_analytics.fetch_historical_data()
            if len(df) >= 10:  # Need minimum data for training
                df_features = self.predictive_analytics.engineer_features(df)
                
                # Train models if not trained
                if not self.predictive_analytics.is_trained:
                    logger.info("Training predictive models...")
                    self.predictive_analytics.train_models(df_features)
                
                # Generate predictions
                predictions = self.predictive_analytics.predict_future_values(df_features, days_ahead=7)
                demand_forecast = self.predictive_analytics.generate_demand_forecast(df_features)
                
                results['predictive_analytics'] = {
                    'predictions': predictions,
                    'demand_forecast': demand_forecast,
                    'data_points': len(df),
                    'features_engineered': df_features.shape[1]
                }
                
                self.metrics['total_predictions'] += len(predictions)
                
                # Send alerts for high-risk predictions
                for target, pred_data in predictions.items():
                    if pred_data.get('values'):
                        # Check for concerning trends
                        values = pred_data['values']
                        if target == 'temperature' and any(v > 40 or v < -5 for v in values):
                            self.alerting_system.send_alert(
                                alert_type='temperature_risk',
                                message=f"Critical temperature predicted: {target}",
                                severity='high',
                                metadata={'predictions': values}
                            )
                            results['alerts'].append({
                                'type': 'temperature_risk',
                                'message': f"Critical temperature predicted for {target}",
                                'timestamp': datetime.now().isoformat()
                            })
            else:
                logger.warning("Insufficient data for predictive analytics")
                results['predictive_analytics'] = {'error': 'Insufficient data'}
            
            # 3. Risk Assessment
            logger.info("Performing risk assessment...")
            risk_score = self._calculate_overall_risk(results)
            results['risk_assessment'] = {
                'overall_risk_score': risk_score,
                'risk_level': self._get_risk_level(risk_score),
                'risk_factors': self._identify_risk_factors(results)
            }
            
            # Send alert if risk is high
            if risk_score > 70:
                self.alerting_system.send_alert(
                    alert_type='high_risk',
                    message=f"High overall risk detected: {risk_score}/100",
                    severity='high',
                    metadata={'risk_score': risk_score}
                )
                results['alerts'].append({
                    'type': 'high_risk',
                    'message': f"Overall risk score: {risk_score}/100",
                    'timestamp': datetime.now().isoformat()
                })
            
            # 4. System Health Check
            logger.info("Checking system health...")
            system_health = self.alerting_system.check_system_health()
            results['system_metrics'] = {
                'system_health': system_health,
                'analysis_duration': (datetime.now() - analysis_start).total_seconds(),
                'metrics': self.metrics.copy()
            }
            
            # 5. Generate Recommendations
            results['recommendations'] = self._generate_recommendations(results)
            
            # Update metrics
            self.metrics['last_analysis_time'] = analysis_start.isoformat()
            self.metrics['alerts_sent'] += len(results['alerts'])
            
            # Save results
            self._save_analysis_results(results)
            
            logger.info(f"Comprehensive analysis completed in {results['system_metrics']['analysis_duration']:.2f} seconds")
            return results
            
        except Exception as e:
            logger.error(f"Error in comprehensive analysis: {e}")
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    def _calculate_overall_risk(self, results: Dict) -> int:
        """Calculate overall risk score (0-100)"""
        risk_score = 0
        
        # Anomaly risk (0-40 points)
        anomalies = results.get('anomaly_detection', {}).get('anomalies', [])
        if anomalies:
            high_severity = len([a for a in anomalies if a.get('severity') == 'HIGH'])
            medium_severity = len([a for a in anomalies if a.get('severity') == 'MEDIUM'])
            risk_score += min(40, high_severity * 15 + medium_severity * 5)
        
        # Prediction risk (0-30 points)
        predictions = results.get('predictive_analytics', {}).get('predictions', {})
        for target, pred_data in predictions.items():
            if pred_data.get('values'):
                values = pred_data['values']
                if target == 'temperature' and any(v > 35 or v < 0 for v in values):
                    risk_score += 15
                elif target == 'humidity' and any(v > 85 or v < 15 for v in values):
                    risk_score += 10
        
        # Demand risk (0-20 points)
        demand_forecast = results.get('predictive_analytics', {}).get('demand_forecast', {})
        if demand_forecast.get('risk_assessment', {}).get('anomaly_rate', 0) > 0.2:
            risk_score += 20
        
        # System health risk (0-10 points)
        system_health = results.get('system_metrics', {}).get('system_health', {})
        if not system_health.get('all_services_healthy', True):
            risk_score += 10
        
        return min(100, risk_score)
    
    def _get_risk_level(self, risk_score: int) -> str:
        """Convert risk score to level"""
        if risk_score >= 80:
            return 'CRITICAL'
        elif risk_score >= 60:
            return 'HIGH'
        elif risk_score >= 40:
            return 'MEDIUM'
        elif risk_score >= 20:
            return 'LOW'
        else:
            return 'MINIMAL'
    
    def _identify_risk_factors(self, results: Dict) -> List[str]:
        """Identify key risk factors"""
        factors = []
        
        # Anomaly factors
        anomalies = results.get('anomaly_detection', {}).get('anomalies', [])
        if anomalies:
            factors.append(f"{len(anomalies)} anomalies detected")
        
        # Temperature factors
        predictions = results.get('predictive_analytics', {}).get('predictions', {})
        if 'temperature' in predictions:
            temp_values = predictions['temperature'].get('values', [])
            if any(v > 35 for v in temp_values):
                factors.append("High temperature predicted")
            if any(v < 0 for v in temp_values):
                factors.append("Low temperature predicted")
        
        # Demand factors
        demand_forecast = results.get('predictive_analytics', {}).get('demand_forecast', {})
        anomaly_rate = demand_forecast.get('risk_assessment', {}).get('anomaly_rate', 0)
        if anomaly_rate > 0.2:
            factors.append(f"High anomaly rate: {anomaly_rate:.1%}")
        
        return factors
    
    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Based on risk level
        risk_level = results.get('risk_assessment', {}).get('risk_level', 'UNKNOWN')
        
        if risk_level in ['CRITICAL', 'HIGH']:
            recommendations.append("Immediate attention required - investigate critical alerts")
            recommendations.append("Consider implementing emergency protocols")
        elif risk_level == 'MEDIUM':
            recommendations.append("Monitor system closely for developing issues")
            recommendations.append("Review operational procedures")
        
        # Based on anomalies
        anomalies = results.get('anomaly_detection', {}).get('anomalies', [])
        if len(anomalies) > 5:
            recommendations.append("High anomaly count - investigate data quality")
        
        # Based on predictions
        predictions = results.get('predictive_analytics', {}).get('predictions', {})
        if 'temperature' in predictions:
            temp_values = predictions['temperature'].get('values', [])
            if any(v > 35 for v in temp_values):
                recommendations.append("Prepare cooling systems for predicted high temperatures")
            if any(v < 0 for v in temp_values):
                recommendations.append("Prepare heating systems for predicted low temperatures")
        
        if not recommendations:
            recommendations.append("System operating normally - continue monitoring")
        
        return recommendations
    
    def _save_analysis_results(self, results: Dict):
        """Save analysis results to file"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'analysis_results_{timestamp}.json'
            
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            logger.info(f"Analysis results saved to {filename}")
            
        except Exception as e:
            logger.error(f"Error saving analysis results: {e}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            'is_running': self.is_running,
            'metrics': self.metrics.copy(),
            'last_analysis': self.metrics.get('last_analysis_time'),
            'components': {
                'anomaly_detection': 'active',
                'predictive_analytics': 'active' if self.predictive_analytics.is_trained else 'training',
                'alerting_system': 'active'
            }
        }
    
    def run_manual_analysis(self) -> Dict[str, Any]:
        """Run manual analysis (non-scheduled)"""
        logger.info("Running manual comprehensive analysis")
        return self.run_comprehensive_analysis()
    
    def _fetch_supply_chain_data(self) -> List[Dict]:
        """Fetch supply chain data from backend API"""
        try:
            import requests
            
            # Try to fetch from backend API
            backend_url = "http://localhost:5004/api/supply-chain/query"
            
            response = requests.get(backend_url, timeout=10)
            if response.status_code == 200:
                response_data = response.json()
                data = response_data.get('data', response_data.get('results', []))
                logger.info(f"Fetched {len(data)} records from backend API")
                return data
            else:
                logger.warning(f"Backend API returned status {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error connecting to backend API: {e}")
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
        
        # Fallback: return empty list
        return []
    
    def print_analysis_summary(self, results: Dict[str, Any]):
        """Print a formatted summary of analysis results"""
        print("\n" + "=" * 60)
        print("📊 INTEGRATED ANALYTICS SUMMARY")
        print("=" * 60)
        
        # Timestamp
        timestamp = results.get('timestamp', 'Unknown')
        print(f"Analysis Time: {timestamp}")
        
        # Anomaly Detection Results
        anomaly_data = results.get('anomaly_detection', {})
        if 'error' not in anomaly_data:
            print(f"\n🔍 ANOMALY DETECTION:")
            total_checked = anomaly_data.get('total_checked', 0)
            anomalies_count = anomaly_data.get('unique_anomalies_count', 0)
            print(f"   Records Analyzed: {total_checked}")
            print(f"   Anomalies Detected: {anomalies_count}")
            
            processing_time = anomaly_data.get('processing_time', 0)
            print(f"   Processing Time: {processing_time:.3f}s")
        else:
            print(f"\n🔍 ANOMALY DETECTION: {anomaly_data.get('error', 'Error')}")
        
        # Predictive Analytics Results
        pred_data = results.get('predictive_analytics', {})
        if 'error' not in pred_data and 'predictions' in pred_data:
            predictions = pred_data['predictions']
            print(f"\n🔮 PREDICTIVE ANALYTICS:")
            print(f"   Targets Predicted: {len(predictions)}")
            print(f"   Data Points Used: {pred_data.get('data_points', 0)}")
            print(f"   Features Engineered: {pred_data.get('features_engineered', 0)}")
            
            for target, pred_info in predictions.items():
                if pred_info.get('values'):
                    print(f"   {target}: {len(pred_info['values'])} predictions")
        else:
            print(f"\n🔮 PREDICTIVE ANALYTICS: {pred_data.get('error', 'No predictions available')}")
        
        # Risk Assessment
        risk_data = results.get('risk_assessment', {})
        if risk_data:
            print(f"\n⚠️ RISK ASSESSMENT:")
            print(f"   Overall Risk Score: {risk_data.get('overall_risk_score', 0)}/100")
            print(f"   Risk Level: {risk_data.get('risk_level', 'UNKNOWN')}")
            
            risk_factors = risk_data.get('risk_factors', [])
            if risk_factors:
                print(f"   Risk Factors: {', '.join(risk_factors)}")
        
        # Alerts
        alerts = results.get('alerts', [])
        print(f"\n🚨 ALERTS GENERATED: {len(alerts)}")
        for alert in alerts[:3]:  # Show first 3 alerts
            print(f"   - {alert.get('type', 'unknown')}: {alert.get('message', 'No message')}")
        
        # Recommendations
        recommendations = results.get('recommendations', [])
        print(f"\n💡 RECOMMENDATIONS:")
        if recommendations:
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"   {i}. {rec}")
        else:
            print("   No specific recommendations at this time")
        
        # System Metrics
        print(f"\n📈 SYSTEM METRICS:")
        print(f"   Total Predictions Made: {self.metrics['total_predictions']}")
        print(f"   Anomalies Detected: {self.metrics['anomalies_detected']}")
        print(f"   Alerts Sent: {self.metrics['alerts_sent']}")
        print(f"   System Health: {self.metrics['system_health']}")
        
        print("\n✅ Analysis Summary Complete")

def main():
    """Main function for testing the integrated system"""
    print("🔗 Integrated Advanced Supply Chain Analytics System")
    print("=" * 60)
    
    # Initialize integrated system
    system = IntegratedAnalyticsSystem()
    
    print("📊 Running comprehensive analysis...")
    results = system.run_manual_analysis()
    
    if 'error' in results:
        print(f"❌ Error: {results['error']}")
        return
    
    print("\n📈 COMPREHENSIVE ANALYSIS RESULTS")
    print("=" * 40)
    
    # Display results summary
    print(f"🕒 Analysis Time: {results['timestamp']}")
    print(f"⏱️ Duration: {results.get('system_metrics', {}).get('analysis_duration', 0):.2f} seconds")
    
    # Anomaly Detection Results
    anomaly_data = results.get('anomaly_detection', {})
    anomaly_count = len(anomaly_data.get('anomalies', []))
    print(f"\n🔍 ANOMALY DETECTION:")
    print(f"   Anomalies detected: {anomaly_count}")
    
    if anomaly_count > 0:
        high_severity = len([a for a in anomaly_data['anomalies'] if a.get('severity') == 'HIGH'])
        print(f"   High severity: {high_severity}")
    
    # Predictive Analytics Results
    pred_data = results.get('predictive_analytics', {})
    if 'predictions' in pred_data:
        predictions = pred_data['predictions']
        print(f"\n🔮 PREDICTIVE ANALYTICS:")
        print(f"   Targets predicted: {len(predictions)}")
        print(f"   Data points used: {pred_data.get('data_points', 0)}")
        print(f"   Features engineered: {pred_data.get('features_engineered', 0)}")
        
        for target, pred_info in predictions.items():
            if pred_info.get('values'):
                print(f"   {target}: {len(pred_info['values'])} predictions")
    
    # Risk Assessment
    risk_data = results.get('risk_assessment', {})
    print(f"\n⚠️ RISK ASSESSMENT:")
    print(f"   Overall Risk Score: {risk_data.get('overall_risk_score', 0)}/100")
    print(f"   Risk Level: {risk_data.get('risk_level', 'UNKNOWN')}")
    
    risk_factors = risk_data.get('risk_factors', [])
    if risk_factors:
        print(f"   Risk Factors: {', '.join(risk_factors)}")
    
    # Alerts
    alerts = results.get('alerts', [])
    print(f"\n🚨 ALERTS GENERATED: {len(alerts)}")
    for alert in alerts[:3]:  # Show first 3 alerts
        print(f"   - {alert.get('type', 'unknown')}: {alert.get('message', 'No message')}")
    
    # Recommendations
    recommendations = results.get('recommendations', [])
    print(f"\n💡 RECOMMENDATIONS:")
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"   {i}. {rec}")
    
    # System Status
    print(f"\n🏥 SYSTEM STATUS:")
    status = system.get_system_status()
    print(f"   System Running: {status['is_running']}")
    print(f"   Total Predictions: {status['metrics']['total_predictions']}")
    print(f"   Anomalies Found: {status['metrics']['anomalies_detected']}")
    print(f"   Alerts Sent: {status['metrics']['alerts_sent']}")
    
    print(f"\n✅ Integrated analysis completed!")
    print("\nTo start continuous monitoring:")
    print("system.start_continuous_monitoring(interval_minutes=30)")

if __name__ == "__main__":
    main()
