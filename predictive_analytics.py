#!/usr/bin/env python3
"""
Advanced Predictive Analytics for Supply Chain Management
Uses machine learning to forecast trends, demand, and potential issues
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import joblib
import json
import requests
import logging
import os
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('predictive_analytics.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PredictiveAnalytics:
    """Advanced predictive analytics for supply chain management"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.is_trained = False
        self.prediction_horizons = [1, 7, 30]  # 1 day, 1 week, 1 month
        
        # Model configurations
        self.model_configs = {
            'random_forest': {
                'n_estimators': 100,
                'random_state': 42,
                'max_depth': 10
            },
            'gradient_boosting': {
                'n_estimators': 100,
                'random_state': 42,
                'max_depth': 6,
                'learning_rate': 0.1
            },
            'neural_network': {
                'hidden_layer_sizes': (100, 50),
                'random_state': 42,
                'max_iter': 1000
            },
            'linear_regression': {},
            'ridge': {'alpha': 1.0}
        }
        
        # Feature engineering parameters
        self.feature_windows = [3, 7, 14, 30]  # Rolling window sizes
        self.lag_features = [1, 2, 3, 7, 14]   # Lag periods
        
    def fetch_historical_data(self) -> pd.DataFrame:
        """Fetch historical supply chain data"""
        try:
            response = requests.get('http://localhost:5004/api/supply-chain/query', timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return self.process_raw_data(data.get('data', []))
            return pd.DataFrame()
            
        except Exception as e:
            logger.error(f"Error fetching historical data: {e}")
            return pd.DataFrame()
    
    def process_raw_data(self, raw_data: List[Dict]) -> pd.DataFrame:
        """Process raw supply chain data into structured format"""
        try:
            processed_records = []
            
            for record in raw_data:
                processed_record = {}
                
                # Extract basic info
                processed_record['timestamp'] = pd.to_datetime(record.get('timestamp'))
                processed_record['product_id'] = record.get('productId', 'Unknown')
                processed_record['organization'] = record.get('organizationId', 'Unknown')
                
                # Extract nested data
                record_data = record.get('data', {})
                
                # Temperature and humidity
                if 'environmental' in record_data:
                    env_data = record_data['environmental']
                    processed_record['temperature'] = env_data.get('temperature', record_data.get('temperature', 0))
                    processed_record['humidity'] = env_data.get('humidity', record_data.get('humidity', 0))
                    processed_record['air_quality'] = env_data.get('air_quality_index', 100)
                    processed_record['light_exposure'] = env_data.get('light_exposure', 500)
                    processed_record['vibration'] = env_data.get('vibration_level', 1.0)
                    processed_record['scenario'] = env_data.get('scenario', 'normal')
                else:
                    processed_record['temperature'] = record_data.get('temperature', 0)
                    processed_record['humidity'] = record_data.get('humidity', 0)
                    processed_record['air_quality'] = 100
                    processed_record['light_exposure'] = 500
                    processed_record['vibration'] = 1.0
                    processed_record['scenario'] = 'normal'
                
                # Product category and details
                processed_record['category'] = record_data.get('category', 'Unknown')
                processed_record['product'] = record_data.get('product', 'Unknown')
                processed_record['supplier'] = record_data.get('supplier', 'Unknown')
                processed_record['location'] = record_data.get('location', 'Unknown')
                
                # Quality metrics
                quality_data = record_data.get('quality', {})
                processed_record['quality_score'] = quality_data.get('integrity_score', 0.8)
                processed_record['compliance_score'] = quality_data.get('compliance_score', 0.9)
                processed_record['appearance_score'] = quality_data.get('appearance_score', 0.8)
                processed_record['shelf_life'] = quality_data.get('shelf_life_remaining', 365)
                
                # Logistics
                logistics_data = record_data.get('logistics', {})
                processed_record['transport_mode'] = logistics_data.get('transport_mode', 'truck')
                processed_record['origin'] = logistics_data.get('origin', 'Unknown')
                processed_record['destination'] = logistics_data.get('destination', 'Unknown')
                
                # Risk indicators
                processed_record['is_anomaly'] = record_data.get('is_anomaly_injected', False)
                processed_record['anomaly_score'] = record.get('anomaly_score', 0.0)
                
                processed_records.append(processed_record)
            
            df = pd.DataFrame(processed_records)
            logger.info(f"Processed {len(df)} records into structured format")
            return df
            
        except Exception as e:
            logger.error(f"Error processing raw data: {e}")
            return pd.DataFrame()
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer features for predictive modeling"""
        try:
            if df.empty:
                return df
            
            # Sort by timestamp
            df = df.sort_values('timestamp').reset_index(drop=True)
            
            # Time-based features
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.dayofweek
            df['month'] = df['timestamp'].dt.month
            df['quarter'] = df['timestamp'].dt.quarter
            df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
            
            # Encode categorical variables
            categorical_cols = ['category', 'supplier', 'location', 'transport_mode', 'scenario']
            for col in categorical_cols:
                if col not in self.encoders:
                    self.encoders[col] = LabelEncoder()
                
                if col in df.columns:
                    df[f'{col}_encoded'] = self.encoders[col].fit_transform(df[col].fillna('Unknown'))
            
            # Rolling window features for numerical columns
            numerical_cols = ['temperature', 'humidity', 'air_quality', 'quality_score', 'vibration']
            
            for col in numerical_cols:
                if col in df.columns:
                    for window in self.feature_windows:
                        if len(df) >= window:
                            df[f'{col}_rolling_mean_{window}'] = df[col].rolling(window=window, min_periods=1).mean()
                            df[f'{col}_rolling_std_{window}'] = df[col].rolling(window=window, min_periods=1).std().fillna(0)
                            df[f'{col}_rolling_min_{window}'] = df[col].rolling(window=window, min_periods=1).min()
                            df[f'{col}_rolling_max_{window}'] = df[col].rolling(window=window, min_periods=1).max()
            
            # Lag features
            for col in numerical_cols:
                if col in df.columns:
                    for lag in self.lag_features:
                        if len(df) > lag:
                            df[f'{col}_lag_{lag}'] = df[col].shift(lag)
            
            # Rate of change features
            for col in numerical_cols:
                if col in df.columns:
                    df[f'{col}_change_1'] = df[col].diff(1).fillna(0)
                    df[f'{col}_change_rate'] = df[col].pct_change(1).fillna(0)
            
            # Environmental stress indicators
            df['temp_stress'] = ((df['temperature'] < 0) | (df['temperature'] > 35)).astype(int)
            df['humidity_stress'] = ((df['humidity'] < 30) | (df['humidity'] > 80)).astype(int)
            df['environmental_stress'] = df['temp_stress'] + df['humidity_stress']
            
            # Quality trend
            if 'quality_score' in df.columns and len(df) > 1:
                df['quality_trend'] = df['quality_score'].diff(1).fillna(0)
                df['quality_deteriorating'] = (df['quality_trend'] < -0.1).astype(int)
            
            # Fill NaN values
            df = df.fillna(0)
            
            logger.info(f"Engineered features: {df.shape[1]} total columns")
            return df
            
        except Exception as e:
            logger.error(f"Error engineering features: {e}")
            return df
    
    def prepare_training_data(self, df: pd.DataFrame, target_col: str) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """Prepare data for training"""
        try:
            # Select feature columns (exclude timestamp, identifiers, and target)
            exclude_cols = ['timestamp', 'product_id', 'organization', 'product', 'supplier', 
                           'location', 'origin', 'destination', 'category', 'transport_mode', 
                           'scenario', target_col]
            
            feature_cols = [col for col in df.columns if col not in exclude_cols]
            
            X = df[feature_cols].values
            y = df[target_col].values
            
            logger.info(f"Training data prepared: {X.shape} features, {len(y)} samples")
            return X, y, feature_cols
            
        except Exception as e:
            logger.error(f"Error preparing training data: {e}")
            return np.array([]), np.array([]), []
    
    def train_models(self, df: pd.DataFrame):
        """Train predictive models"""
        try:
            if len(df) < 10:
                logger.warning("Insufficient data for training models")
                return
            
            # Define prediction targets
            targets = {
                'temperature': 'temperature',
                'humidity': 'humidity',
                'quality_score': 'quality_score',
                'anomaly_risk': 'is_anomaly'
            }
            
            for target_name, target_col in targets.items():
                if target_col not in df.columns:
                    continue
                
                logger.info(f"Training models for {target_name}...")
                
                X, y, feature_cols = self.prepare_training_data(df, target_col)
                if len(X) == 0:
                    continue
                
                # Split data
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.2, random_state=42
                )
                
                # Scale features
                scaler = StandardScaler()
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)
                
                self.scalers[target_name] = scaler
                
                # Train multiple models
                self.models[target_name] = {}
                model_scores = {}
                
                for model_name, config in self.model_configs.items():
                    try:
                        if model_name == 'random_forest':
                            model = RandomForestRegressor(**config)
                        elif model_name == 'gradient_boosting':
                            model = GradientBoostingRegressor(**config)
                        elif model_name == 'neural_network':
                            model = MLPRegressor(**config)
                        elif model_name == 'linear_regression':
                            model = LinearRegression(**config)
                        elif model_name == 'ridge':
                            model = Ridge(**config)
                        
                        # Train model
                        if model_name in ['neural_network', 'linear_regression', 'ridge']:
                            model.fit(X_train_scaled, y_train)
                            y_pred = model.predict(X_test_scaled)
                        else:
                            model.fit(X_train, y_train)
                            y_pred = model.predict(X_test)
                        
                        # Evaluate model
                        mae = mean_absolute_error(y_test, y_pred)
                        mse = mean_squared_error(y_test, y_pred)
                        r2 = r2_score(y_test, y_pred)
                        
                        self.models[target_name][model_name] = model
                        model_scores[model_name] = {'mae': mae, 'mse': mse, 'r2': r2}
                        
                        logger.info(f"  {model_name}: MAE={mae:.4f}, R²={r2:.4f}")
                        
                    except Exception as e:
                        logger.error(f"Error training {model_name} for {target_name}: {e}")
                
                # Select best model based on R² score
                if model_scores:
                    best_model = max(model_scores.items(), key=lambda x: x[1]['r2'])
                    logger.info(f"Best model for {target_name}: {best_model[0]} (R²={best_model[1]['r2']:.4f})")
            
            self.is_trained = True
            self.save_models()
            logger.info("Model training completed")
            
        except Exception as e:
            logger.error(f"Error training models: {e}")
    
    def predict_future_values(self, df: pd.DataFrame, days_ahead: int = 7) -> Dict[str, Any]:
        """Predict future values"""
        try:
            if not self.is_trained:
                logger.warning("Models not trained yet")
                return {}
            
            predictions = {}
            
            # Get latest data point for prediction
            latest_data = df.iloc[-1:].copy()
            
            # Generate predictions for each target
            for target_name in self.models.keys():
                if target_name not in self.scalers:
                    continue
                
                target_predictions = []
                confidence_intervals = []
                
                # Predict for each day ahead
                for day in range(1, days_ahead + 1):
                    try:
                        # Prepare features (would need more sophisticated approach for real forecasting)
                        X, _, feature_cols = self.prepare_training_data(df, target_name)
                        if len(X) == 0:
                            continue
                        
                        X_latest = X[-1:] # Use latest data point
                        
                        # Get predictions from all models
                        model_predictions = []
                        
                        for model_name, model in self.models[target_name].items():
                            if model_name in ['neural_network', 'linear_regression', 'ridge']:
                                X_scaled = self.scalers[target_name].transform(X_latest)
                                pred = model.predict(X_scaled)[0]
                            else:
                                pred = model.predict(X_latest)[0]
                            
                            model_predictions.append(pred)
                        
                        # Ensemble prediction (average)
                        ensemble_pred = np.mean(model_predictions)
                        pred_std = np.std(model_predictions)
                        
                        target_predictions.append(ensemble_pred)
                        confidence_intervals.append((ensemble_pred - 1.96 * pred_std, 
                                                   ensemble_pred + 1.96 * pred_std))
                        
                    except Exception as e:
                        logger.error(f"Error predicting {target_name} for day {day}: {e}")
                
                predictions[target_name] = {
                    'values': target_predictions,
                    'confidence_intervals': confidence_intervals,
                    'days_ahead': list(range(1, len(target_predictions) + 1))
                }
            
            return predictions
            
        except Exception as e:
            logger.error(f"Error making predictions: {e}")
            return {}
    
    def generate_demand_forecast(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate demand forecasting analysis"""
        try:
            forecast = {
                'product_demand': {},
                'category_trends': {},
                'seasonal_patterns': {},
                'risk_assessment': {}
            }
            
            # Product demand analysis
            if 'category' in df.columns and 'product' in df.columns:
                category_counts = df['category'].value_counts().to_dict()
                forecast['category_trends'] = category_counts
                
                # Product demand by category
                for category in df['category'].unique():
                    category_data = df[df['category'] == category]
                    products = category_data['product'].value_counts().head(5).to_dict()
                    forecast['product_demand'][category] = products
            
            # Seasonal patterns
            if 'month' in df.columns:
                monthly_volume = df.groupby('month').size().to_dict()
                forecast['seasonal_patterns']['monthly_volume'] = monthly_volume
            
            # Risk assessment
            if 'is_anomaly' in df.columns:
                anomaly_rate = df['is_anomaly'].mean()
                forecast['risk_assessment']['anomaly_rate'] = anomaly_rate
                
                if 'category' in df.columns:
                    category_risk = df.groupby('category')['is_anomaly'].mean().to_dict()
                    forecast['risk_assessment']['category_risk'] = category_risk
            
            return forecast
            
        except Exception as e:
            logger.error(f"Error generating demand forecast: {e}")
            return {}
    
    def save_models(self):
        """Save trained models"""
        try:
            models_dir = 'predictive_models'
            os.makedirs(models_dir, exist_ok=True)
            
            # Save models
            for target_name, target_models in self.models.items():
                for model_name, model in target_models.items():
                    joblib.dump(model, f'{models_dir}/{target_name}_{model_name}.pkl')
            
            # Save scalers and encoders
            joblib.dump(self.scalers, f'{models_dir}/scalers.pkl')
            joblib.dump(self.encoders, f'{models_dir}/encoders.pkl')
            
            logger.info("Predictive models saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving models: {e}")
    
    def load_models(self):
        """Load trained models"""
        try:
            models_dir = 'predictive_models'
            
            if not os.path.exists(models_dir):
                logger.info("No saved predictive models found")
                return
            
            # Load scalers and encoders
            if os.path.exists(f'{models_dir}/scalers.pkl'):
                self.scalers = joblib.load(f'{models_dir}/scalers.pkl')
            
            if os.path.exists(f'{models_dir}/encoders.pkl'):
                self.encoders = joblib.load(f'{models_dir}/encoders.pkl')
            
            # Load models
            self.models = {}
            for file in os.listdir(models_dir):
                if file.endswith('.pkl') and file not in ['scalers.pkl', 'encoders.pkl']:
                    parts = file.replace('.pkl', '').split('_')
                    if len(parts) >= 2:
                        target_name = '_'.join(parts[:-1])
                        model_name = parts[-1]
                        
                        if target_name not in self.models:
                            self.models[target_name] = {}
                        
                        self.models[target_name][model_name] = joblib.load(f'{models_dir}/{file}')
            
            self.is_trained = len(self.models) > 0
            logger.info(f"Loaded predictive models for {len(self.models)} targets")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")

def main():
    """Main function for testing"""
    print("🔮 Advanced Predictive Analytics Starting...")
    
    analytics = PredictiveAnalytics()
    
    # Try to load existing models
    analytics.load_models()
    
    # Fetch data
    print("\n📊 Fetching historical data...")
    df = analytics.fetch_historical_data()
    
    if df.empty:
        print("❌ No data available for analysis")
        return
    
    print(f"📈 Fetched {len(df)} historical records")
    
    # Engineer features
    print("\n🔧 Engineering features...")
    df_features = analytics.engineer_features(df)
    print(f"✅ Created {df_features.shape[1]} features")
    
    # Train models if not already trained
    if not analytics.is_trained:
        print("\n🤖 Training predictive models...")
        analytics.train_models(df_features)
    
    # Generate predictions
    print("\n🔮 Generating predictions...")
    predictions = analytics.predict_future_values(df_features, days_ahead=7)
    
    print("\n" + "="*60)
    print("PREDICTIVE ANALYTICS RESULTS")
    print("="*60)
    
    for target, pred_data in predictions.items():
        print(f"\n📊 {target.upper()} FORECAST (Next 7 days):")
        for i, (value, ci) in enumerate(zip(pred_data['values'], pred_data['confidence_intervals'])):
            print(f"Day {i+1}: {value:.2f} (CI: {ci[0]:.2f} - {ci[1]:.2f})")
    
    # Generate demand forecast
    print("\n📈 Generating demand forecast...")
    demand_forecast = analytics.generate_demand_forecast(df_features)
    
    if demand_forecast:
        print(f"\n📊 DEMAND FORECAST:")
        
        if 'category_trends' in demand_forecast:
            print(f"Top categories: {dict(list(demand_forecast['category_trends'].items())[:3])}")
        
        if 'risk_assessment' in demand_forecast and 'anomaly_rate' in demand_forecast['risk_assessment']:
            anomaly_rate = demand_forecast['risk_assessment']['anomaly_rate']
            print(f"Anomaly rate: {anomaly_rate:.1%}")
    
    print("\n" + "="*60)
    print("✅ Predictive analytics completed!")

if __name__ == "__main__":
    main()
