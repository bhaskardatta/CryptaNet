import pandas as pd
import numpy as np
import os
import sys
import json
from pathlib import Path

# Add the current directory to the Python path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from preprocessing.data_preprocessor import DataPreprocessor
from feature_engineering.feature_extractor import FeatureExtractor
from models.isolation_forest import AnomalyDetector
from evaluation.model_evaluator import ModelEvaluator

class AnomalyDetectionAPI:
    """
    Provides a unified API for the anomaly detection system of CryptaNet.
    
    This class integrates preprocessing, feature engineering, and anomaly detection
    to provide a complete pipeline for detecting anomalies in supply chain data.
    """
    
    def __init__(self, model_path=None):
        """
        Initialize the anomaly detection API.
        
        Args:
            model_path (str, optional): Path to a saved model. If provided, the model will be loaded.
        """
        self.preprocessor = DataPreprocessor()
        self.feature_extractor = FeatureExtractor()
        self.model = AnomalyDetector()
        self.evaluator = ModelEvaluator()
        self.is_fitted = False
        
        # Load model if path is provided
        if model_path and os.path.exists(model_path):
            self.model = AnomalyDetector.load_model(model_path)
            self.is_fitted = self.model.is_fitted
    
    def preprocess_data(self, data, numerical_features=None, categorical_features=None):
        """
        Preprocess the input data for anomaly detection.
        
        Args:
            data (DataFrame): The input data.
            numerical_features (list, optional): List of numerical feature names.
            categorical_features (list, optional): List of categorical feature names.
            
        Returns:
            array: The preprocessed data.
        """
        return self.preprocessor.fit_transform(data, numerical_features, categorical_features)
    
    def extract_features(self, data, timestamp_col=None, value_cols=None, window_size=7, group_by=None):
        """
        Extract features from the input data.
        
        Args:
            data (DataFrame): The input data.
            timestamp_col (str, optional): The name of the timestamp column.
            value_cols (list, optional): List of value columns for statistical features.
            window_size (int): The size of the rolling window.
            group_by (str, optional): Column to group by before computing statistics.
            
        Returns:
            DataFrame: The data with extracted features.
        """
        return self.feature_extractor.extract_all_features(data, timestamp_col, value_cols, window_size, group_by)
    
    def fit(self, data, numerical_features=None, categorical_features=None, timestamp_col=None, value_cols=None):
        """
        Fit the anomaly detection model to the data.
        
        Args:
            data (DataFrame): The input data.
            numerical_features (list, optional): List of numerical feature names.
            categorical_features (list, optional): List of categorical feature names.
            timestamp_col (str, optional): The name of the timestamp column.
            value_cols (list, optional): List of value columns for statistical features.
            
        Returns:
            self: The fitted model.
        """
        # Extract features
        if timestamp_col or value_cols:
            data = self.extract_features(data, timestamp_col, value_cols)
        
        # Preprocess data
        preprocessed_data = self.preprocessor.fit_transform(data, numerical_features, categorical_features)
        
        # Get feature names
        feature_names = self.preprocessor.get_feature_names()
        
        # Fit the model
        self.model.fit(preprocessed_data, feature_names)
        self.is_fitted = True
        
        return self
    
    def predict(self, data, threshold=None):
        """
        Predict anomalies in the input data.
        
        Args:
            data (DataFrame): The input data.
            threshold (float, optional): Custom threshold for anomaly detection.
            
        Returns:
            tuple: (predictions, scores) where predictions is an array of 1 (normal) and -1 (anomaly),
                  and scores is an array of anomaly scores.
        """
        if not self.is_fitted:
            raise ValueError("Model has not been fitted yet.")
        
        # Preprocess data
        preprocessed_data = self.preprocessor.transform(data)
        
        # Predict anomalies
        predictions, scores = self.model.detect_anomalies(preprocessed_data, threshold, return_scores=True)
        
        return predictions, scores
    
    def explain_anomalies(self, data, predictions, scores):
        """
        Generate explanations for detected anomalies.
        
        Args:
            data (DataFrame): The original input data.
            predictions (array): Predictions from the model (1 for normal, -1 for anomalies).
            scores (array): Anomaly scores from the model.
            
        Returns:
            list: A list of dictionaries containing explanations for each anomaly.
        """
        # Find indices of anomalies
        anomaly_indices = np.where(predictions == -1)[0]
        
        # Generate explanations
        explanations = []
        for idx in anomaly_indices:
            explanation = {
                'index': idx,
                'score': scores[idx],
                'data_point': data.iloc[idx].to_dict() if isinstance(data, pd.DataFrame) else None,
                'explanation': f"Anomaly detected with score {scores[idx]:.4f}"
            }
            explanations.append(explanation)
        
        return explanations
    
    def evaluate(self, data, labels):
        """
        Evaluate the performance of the anomaly detection model.
        
        Args:
            data (DataFrame): The input data.
            labels (array-like): Ground truth labels (1 for normal, -1 for anomalies).
            
        Returns:
            dict: A dictionary containing various performance metrics.
        """
        if not self.is_fitted:
            raise ValueError("Model has not been fitted yet.")
        
        # Preprocess data
        preprocessed_data = self.preprocessor.transform(data)
        
        # Predict anomalies
        predictions, scores = self.model.detect_anomalies(preprocessed_data, return_scores=True)
        
        # Calculate metrics
        metrics = self.evaluator.calculate_metrics(labels, predictions)
        
        return metrics
    
    def save_model(self, model_path, preprocessor_path=None):
        """
        Save the trained model and preprocessor.
        
        Args:
            model_path (str): Path to save the model.
            preprocessor_path (str, optional): Path to save the preprocessor.
        """
        if not self.is_fitted:
            raise ValueError("Model has not been fitted yet.")
        
        # Save the model
        self.model.save_model(model_path)
        
        # Save the preprocessor if path is provided
        if preprocessor_path:
            self.preprocessor.save(preprocessor_path)
    
    @classmethod
    def load_model(cls, model_path, preprocessor_path=None):
        """
        Load a trained model and preprocessor.
        
        Args:
            model_path (str): Path to the saved model.
            preprocessor_path (str, optional): Path to the saved preprocessor.
            
        Returns:
            AnomalyDetectionAPI: The loaded model.
        """
        # Create a new instance
        api = cls()
        
        # Load the model
        api.model = AnomalyDetector.load_model(model_path)
        api.is_fitted = api.model.is_fitted
        
        # Load the preprocessor if path is provided
        if preprocessor_path and os.path.exists(preprocessor_path):
            api.preprocessor = DataPreprocessor.load(preprocessor_path)
        
        return api