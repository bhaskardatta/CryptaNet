#!/usr/bin/env python3
"""
Advanced Machine Learning Anomaly Detection Service
Implements multiple ML algorithms for supply chain anomaly detection
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.svm import OneClassSVM
from scipy import stats
import joblib
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
import requests
import time
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('advanced_anomaly_detection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AdvancedAnomalyDetector:
    """Advanced ML-based anomaly detection for supply chain data"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.is_trained = False
        self.feature_columns = [
            'temperature', 'humidity', 'timestamp_hour', 
            'timestamp_day', 'temperature_diff', 'humidity_diff'
        ]
        self.model_configs = {
            'isolation_forest': {
                'contamination': 0.1,
                'random_state': 42,
                'n_estimators': 100
            },
            'one_class_svm': {
                'kernel': 'rbf',
                'gamma': 'scale',
                'nu': 0.1
            },
            'dbscan': {
                'eps': 0.5,
                'min_samples': 5
            }
        }
        self.anomaly_thresholds = {
            'temperature': {'min': -10, 'max': 50},
            'humidity': {'min': 0, 'max': 100},
            'temperature_change_rate': 5.0,  # degrees per hour
            'humidity_change_rate': 15.0     # % per hour
        }
        
    def extract_features(self, data: List[Dict]) -> pd.DataFrame:
        """Extract features from supply chain data"""
        try:
            # Flatten the nested data structure
            flattened_data = []
            for record in data:
                flat_record = {}
                
                # Get data from nested structure
                if 'data' in record and isinstance(record['data'], dict):
                    nested_data = record['data']
                    # Look for temperature and humidity in nested data
                    if 'environmental' in nested_data:
                        env_data = nested_data['environmental']
                        flat_record['temperature'] = env_data.get('temperature', nested_data.get('temperature', 0))
                        flat_record['humidity'] = env_data.get('humidity', nested_data.get('humidity', 0))
                    else:
                        flat_record['temperature'] = nested_data.get('temperature', 0)
                        flat_record['humidity'] = nested_data.get('humidity', 0)
                    
                    flat_record['productId'] = nested_data.get('productId', record.get('productId', 'Unknown'))
                    flat_record['product'] = nested_data.get('product', record.get('product', 'Unknown'))
                else:
                    # Fallback to record-level data
                    flat_record['temperature'] = record.get('temperature', 0)
                    flat_record['humidity'] = record.get('humidity', 0)
                    flat_record['productId'] = record.get('productId', 'Unknown')
                    flat_record['product'] = record.get('product', 'Unknown')
                
                flat_record['timestamp'] = record.get('timestamp', '')
                flattened_data.append(flat_record)
            
            df = pd.DataFrame(flattened_data)
            
            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Extract time-based features
            df['timestamp_hour'] = df['timestamp'].dt.hour
            df['timestamp_day'] = df['timestamp'].dt.dayofweek
            
            # Sort by timestamp for difference calculations
            df = df.sort_values('timestamp').reset_index(drop=True)
            
            # Calculate differences for trend analysis
            df['temperature_diff'] = df['temperature'].diff().fillna(0)
            df['humidity_diff'] = df['humidity'].diff().fillna(0)
            
            # Calculate moving averages
            df['temp_ma_3'] = df['temperature'].rolling(window=3, min_periods=1).mean()
            df['humidity_ma_3'] = df['humidity'].rolling(window=3, min_periods=1).mean()
            
            # Calculate statistical features
            df['temp_std_3'] = df['temperature'].rolling(window=3, min_periods=1).std().fillna(0)
            df['humidity_std_3'] = df['humidity'].rolling(window=3, min_periods=1).std().fillna(0)
            
            # Calculate z-scores for outlier detection
            if len(df) > 1:
                df['temp_zscore'] = stats.zscore(df['temperature'])
                df['humidity_zscore'] = stats.zscore(df['humidity'])
            else:
                df['temp_zscore'] = 0
                df['humidity_zscore'] = 0
            
            logger.info(f"Extracted features for {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Error extracting features: {e}")
            return pd.DataFrame()
    
    def rule_based_detection(self, df: pd.DataFrame) -> List[Dict]:
        """Rule-based anomaly detection"""
        anomalies = []
        
        for idx, row in df.iterrows():
            anomaly_reasons = []
            
            # Temperature range check
            if row['temperature'] < self.anomaly_thresholds['temperature']['min'] or \
               row['temperature'] > self.anomaly_thresholds['temperature']['max']:
                anomaly_reasons.append(f"Temperature out of range: {row['temperature']:.1f}°C")
            
            # Humidity range check
            if row['humidity'] < self.anomaly_thresholds['humidity']['min'] or \
               row['humidity'] > self.anomaly_thresholds['humidity']['max']:
                anomaly_reasons.append(f"Humidity out of range: {row['humidity']:.1f}%")
            
            # Rapid temperature change
            if abs(row['temperature_diff']) > self.anomaly_thresholds['temperature_change_rate']:
                anomaly_reasons.append(f"Rapid temperature change: {row['temperature_diff']:.1f}°C")
            
            # Rapid humidity change
            if abs(row['humidity_diff']) > self.anomaly_thresholds['humidity_change_rate']:
                anomaly_reasons.append(f"Rapid humidity change: {row['humidity_diff']:.1f}%")
            
            # Z-score based detection
            if abs(row['temp_zscore']) > 3:
                anomaly_reasons.append(f"Temperature statistical outlier (z-score: {row['temp_zscore']:.2f})")
            
            if abs(row['humidity_zscore']) > 3:
                anomaly_reasons.append(f"Humidity statistical outlier (z-score: {row['humidity_zscore']:.2f})")
            
            if anomaly_reasons:
                anomalies.append({
                    'index': idx,
                    'product_id': row.get('productId', 'Unknown'),
                    'timestamp': row['timestamp'].isoformat(),
                    'type': 'rule_based',
                    'severity': 'high' if len(anomaly_reasons) > 1 else 'medium',
                    'reasons': anomaly_reasons,
                    'temperature': row['temperature'],
                    'humidity': row['humidity']
                })
        
        return anomalies
    
    def train_models(self, df: pd.DataFrame):
        """Train ML models on historical data"""
        try:
            if len(df) < 10:
                logger.warning("Insufficient data for training ML models")
                return
            
            # Prepare features
            feature_data = df[self.feature_columns].fillna(0)
            
            # Scale features
            self.scalers['standard'] = StandardScaler()
            scaled_features = self.scalers['standard'].fit_transform(feature_data)
            
            # Train Isolation Forest
            logger.info("Training Isolation Forest...")
            self.models['isolation_forest'] = IsolationForest(**self.model_configs['isolation_forest'])
            self.models['isolation_forest'].fit(scaled_features)
            
            # Train One-Class SVM
            logger.info("Training One-Class SVM...")
            self.models['one_class_svm'] = OneClassSVM(**self.model_configs['one_class_svm'])
            self.models['one_class_svm'].fit(scaled_features)
            
            # Train DBSCAN for clustering-based anomaly detection
            logger.info("Training DBSCAN...")
            self.models['dbscan'] = DBSCAN(**self.model_configs['dbscan'])
            cluster_labels = self.models['dbscan'].fit_predict(scaled_features)
            
            self.is_trained = True
            logger.info("ML models trained successfully")
            
            # Save models
            self.save_models()
            
        except Exception as e:
            logger.error(f"Error training models: {e}")
    
    def ml_based_detection(self, df: pd.DataFrame) -> List[Dict]:
        """ML-based anomaly detection"""
        if not self.is_trained:
            logger.warning("ML models not trained yet")
            return []
        
        anomalies = []
        
        try:
            # Prepare features
            feature_data = df[self.feature_columns].fillna(0)
            scaled_features = self.scalers['standard'].transform(feature_data)
            
            # Isolation Forest predictions
            if_predictions = self.models['isolation_forest'].predict(scaled_features)
            if_scores = self.models['isolation_forest'].score_samples(scaled_features)
            
            # One-Class SVM predictions
            svm_predictions = self.models['one_class_svm'].predict(scaled_features)
            svm_scores = self.models['one_class_svm'].score_samples(scaled_features)
            
            # DBSCAN clustering
            dbscan_labels = self.models['dbscan'].fit_predict(scaled_features)
            
            for idx, row in df.iterrows():
                anomaly_indicators = []
                scores = {}
                
                # Check Isolation Forest result
                if if_predictions[idx] == -1:
                    anomaly_indicators.append("Isolation Forest")
                    scores['isolation_forest'] = float(if_scores[idx])
                
                # Check One-Class SVM result
                if svm_predictions[idx] == -1:
                    anomaly_indicators.append("One-Class SVM")
                    scores['one_class_svm'] = float(svm_scores[idx])
                
                # Check DBSCAN result (outliers have label -1)
                if dbscan_labels[idx] == -1:
                    anomaly_indicators.append("DBSCAN Clustering")
                
                # If multiple models agree, it's likely an anomaly
                if len(anomaly_indicators) >= 2:
                    anomalies.append({
                        'index': idx,
                        'product_id': row.get('productId', 'Unknown'),
                        'timestamp': row['timestamp'].isoformat(),
                        'type': 'ml_based',
                        'severity': 'high' if len(anomaly_indicators) >= 3 else 'medium',
                        'algorithms': anomaly_indicators,
                        'scores': scores,
                        'temperature': row['temperature'],
                        'humidity': row['humidity']
                    })
            
        except Exception as e:
            logger.error(f"Error in ML-based detection: {e}")
        
        return anomalies
    
    def detect_anomalies(self, data: List[Dict]) -> Dict[str, Any]:
        """Main anomaly detection function"""
        try:
            start_time = time.time()
            
            if not data:
                return {'anomalies': [], 'total_checked': 0, 'processing_time': 0}
            
            # Extract features
            df = self.extract_features(data)
            if df.empty:
                return {'anomalies': [], 'total_checked': 0, 'processing_time': 0}
            
            # Train models if not already trained and we have enough data
            if not self.is_trained and len(df) >= 10:
                self.train_models(df)
            
            # Perform rule-based detection
            rule_anomalies = self.rule_based_detection(df)
            
            # Perform ML-based detection
            ml_anomalies = self.ml_based_detection(df)
            
            # Combine results
            all_anomalies = rule_anomalies + ml_anomalies
            
            # Remove duplicates based on index and timestamp
            unique_anomalies = []
            seen_indices = set()
            
            for anomaly in all_anomalies:
                key = f"{anomaly['index']}_{anomaly['timestamp']}"
                if key not in seen_indices:
                    seen_indices.add(key)
                    unique_anomalies.append(anomaly)
            
            # Sort by timestamp
            unique_anomalies.sort(key=lambda x: x['timestamp'])
            
            processing_time = time.time() - start_time
            
            result = {
                'anomalies': unique_anomalies,
                'total_checked': len(df),
                'rule_based_count': len(rule_anomalies),
                'ml_based_count': len(ml_anomalies),
                'unique_anomalies_count': len(unique_anomalies),
                'processing_time': round(processing_time, 3),
                'models_trained': self.is_trained
            }
            
            logger.info(f"Processed {len(df)} records, found {len(unique_anomalies)} anomalies in {processing_time:.3f}s")
            return result
            
        except Exception as e:
            logger.error(f"Error in anomaly detection: {e}")
            return {'anomalies': [], 'total_checked': 0, 'processing_time': 0, 'error': str(e)}
    
    def save_models(self):
        """Save trained models to disk"""
        try:
            models_dir = 'models'
            os.makedirs(models_dir, exist_ok=True)
            
            for name, model in self.models.items():
                if name != 'dbscan':  # DBSCAN doesn't need to be saved (it's fit on each prediction)
                    joblib.dump(model, f'{models_dir}/{name}_model.pkl')
            
            # Save scalers
            for name, scaler in self.scalers.items():
                joblib.dump(scaler, f'{models_dir}/{name}_scaler.pkl')
            
            logger.info("Models saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving models: {e}")
    
    def load_models(self):
        """Load trained models from disk"""
        try:
            models_dir = 'models'
            
            if not os.path.exists(models_dir):
                logger.info("No saved models found")
                return
            
            # Load models
            for model_name in ['isolation_forest', 'one_class_svm']:
                model_path = f'{models_dir}/{model_name}_model.pkl'
                if os.path.exists(model_path):
                    self.models[model_name] = joblib.load(model_path)
                    logger.info(f"Loaded {model_name} model")
            
            # Load scalers
            for scaler_name in ['standard']:
                scaler_path = f'{models_dir}/{scaler_name}_scaler.pkl'
                if os.path.exists(scaler_path):
                    self.scalers[scaler_name] = joblib.load(scaler_path)
                    logger.info(f"Loaded {scaler_name} scaler")
            
            # Initialize DBSCAN (it's trained on each prediction)
            self.models['dbscan'] = DBSCAN(**self.model_configs['dbscan'])
            
            self.is_trained = len(self.models) >= 2 and len(self.scalers) >= 1
            logger.info(f"Models loaded. Trained status: {self.is_trained}")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")

def fetch_data_from_backend():
    """Fetch recent supply chain data from backend"""
    try:
        response = requests.get('http://localhost:5004/api/supply-chain/query', timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('data'):
                return data['data']
        return []
    except Exception as e:
        logger.error(f"Error fetching data from backend: {e}")
        return []

def main():
    """Main function for testing"""
    logger.info("Starting Advanced Anomaly Detection Service")
    
    # Initialize detector
    detector = AdvancedAnomalyDetector()
    
    # Try to load existing models
    detector.load_models()
    
    # Fetch data from backend
    logger.info("Fetching data from backend...")
    data = fetch_data_from_backend()
    
    if not data:
        logger.warning("No data available from backend")
        return
    
    # Detect anomalies
    logger.info(f"Analyzing {len(data)} records...")
    results = detector.detect_anomalies(data)
    
    # Display results
    print("\n" + "="*60)
    print("ADVANCED ANOMALY DETECTION RESULTS")
    print("="*60)
    print(f"📊 Total records processed: {results['total_checked']}")
    print(f"🔍 Rule-based anomalies: {results.get('rule_based_count', 0)}")
    print(f"🤖 ML-based anomalies: {results.get('ml_based_count', 0)}")
    print(f"🚨 Unique anomalies found: {results.get('unique_anomalies_count', 0)}")
    print(f"⏱️  Processing time: {results['processing_time']}s")
    print(f"🧠 ML models trained: {results.get('models_trained', False)}")
    
    if results.get('error'):
        print(f"❌ Error: {results['error']}")
    
    if results.get('anomalies', []):
        print(f"\n🚨 ANOMALY DETAILS:")
        for i, anomaly in enumerate(results['anomalies'][:10], 1):  # Show first 10
            print(f"\n{i}. Product: {anomaly['product_id']}")
            print(f"   Time: {anomaly['timestamp']}")
            print(f"   Type: {anomaly['type']}")
            print(f"   Severity: {anomaly['severity']}")
            print(f"   Temperature: {anomaly['temperature']:.1f}°C")
            print(f"   Humidity: {anomaly['humidity']:.1f}%")
            
            if anomaly['type'] == 'rule_based':
                print(f"   Reasons: {', '.join(anomaly['reasons'])}")
            elif anomaly['type'] == 'ml_based':
                print(f"   Algorithms: {', '.join(anomaly['algorithms'])}")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
