import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os

class AnomalyDetector:
    """
    Implements an anomaly detection system using Isolation Forest algorithm.
    
    Isolation Forest is an unsupervised learning algorithm that explicitly identifies
    anomalies by isolating them in the feature space. It's particularly effective for
    high-dimensional datasets and works by randomly selecting a feature and then randomly
    selecting a split value between the maximum and minimum values of that feature.
    """
    
    def __init__(self, n_estimators=100, contamination='auto', random_state=42):
        """
        Initialize the anomaly detector with the specified parameters.
        
        Args:
            n_estimators (int): The number of base estimators in the ensemble.
            contamination (float or 'auto'): The proportion of outliers in the data set.
            random_state (int): Random seed for reproducibility.
        """
        self.model = IsolationForest(
            n_estimators=n_estimators,
            contamination=contamination,
            random_state=random_state
        )
        self.scaler = StandardScaler()
        self.is_fitted = False
        self.feature_names = None
    
    def fit(self, X, feature_names=None):
        """
        Fit the anomaly detection model to the data.
        
        Args:
            X (array-like or DataFrame): The input samples to fit the model.
            feature_names (list, optional): Names of the features. If None and X is a DataFrame,
                                           column names will be used.
        
        Returns:
            self: The fitted estimator.
        """
        # Save feature names for later use in explanation
        if feature_names is not None:
            self.feature_names = feature_names
        elif isinstance(X, pd.DataFrame):
            self.feature_names = X.columns.tolist()
        
        # Convert to numpy array if it's a DataFrame
        if isinstance(X, pd.DataFrame):
            X = X.values
        
        # Scale the data
        X_scaled = self.scaler.fit_transform(X)
        
        # Fit the model
        self.model.fit(X_scaled)
        self.is_fitted = True
        
        return self
    
    def predict(self, X):
        """
        Predict if instances are anomalies or not.
        
        Args:
            X (array-like or DataFrame): The input samples.
        
        Returns:
            array: 1 for normal points and -1 for anomalies.
        """
        if not self.is_fitted:
            raise ValueError("Model has not been fitted yet.")
        
        # Convert to numpy array if it's a DataFrame
        if isinstance(X, pd.DataFrame):
            X = X.values
        
        # Scale the data
        X_scaled = self.scaler.transform(X)
        
        # Predict
        return self.model.predict(X_scaled)
    
    def decision_function(self, X):
        """
        Calculate the anomaly score of each sample using the fitted detector.
        The more negative the score, the more abnormal the sample.
        
        Args:
            X (array-like or DataFrame): The input samples.
        
        Returns:
            array: The anomaly score of each input sample.
        """
        if not self.is_fitted:
            raise ValueError("Model has not been fitted yet.")
        
        # Convert to numpy array if it's a DataFrame
        if isinstance(X, pd.DataFrame):
            X = X.values
        
        # Scale the data
        X_scaled = self.scaler.transform(X)
        
        # Get anomaly scores
        return self.model.decision_function(X_scaled)
    
    def score_samples(self, X):
        """
        Calculate the anomaly score of each sample using the fitted detector.
        The lower the score, the more abnormal the sample.
        
        Args:
            X (array-like or DataFrame): The input samples.
        
        Returns:
            array: The anomaly score of each input sample.
        """
        if not self.is_fitted:
            raise ValueError("Model has not been fitted yet.")
        
        # Convert to numpy array if it's a DataFrame
        if isinstance(X, pd.DataFrame):
            X = X.values
        
        # Scale the data
        X_scaled = self.scaler.transform(X)
        
        # Get anomaly scores
        return self.model.score_samples(X_scaled)
    
    def detect_anomalies(self, X, threshold=None, return_scores=False):
        """
        Detect anomalies in the data based on the anomaly scores.
        
        Args:
            X (array-like or DataFrame): The input samples.
            threshold (float, optional): Custom threshold for anomaly detection.
                                        If None, the model's internal threshold is used.
            return_scores (bool): Whether to return anomaly scores along with predictions.
        
        Returns:
            tuple or array: If return_scores is True, returns (predictions, scores),
                          otherwise returns just predictions (1 for normal, -1 for anomalies).
        """
        if not self.is_fitted:
            raise ValueError("Model has not been fitted yet.")
        
        # Get anomaly scores
        scores = self.decision_function(X)
        
        if threshold is not None:
            # Use custom threshold
            predictions = np.ones_like(scores)
            predictions[scores < threshold] = -1
        else:
            # Use model's internal threshold
            predictions = self.predict(X)
        
        if return_scores:
            return predictions, scores
        else:
            return predictions
    
    def save_model(self, filepath):
        """
        Save the trained model to a file.
        
        Args:
            filepath (str): Path to save the model.
        """
        if not self.is_fitted:
            raise ValueError("Model has not been fitted yet.")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save the model and scaler
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'is_fitted': self.is_fitted,
            'feature_names': self.feature_names
        }, filepath)
    
    @classmethod
    def load_model(cls, filepath):
        """
        Load a trained model from a file.
        
        Args:
            filepath (str): Path to the saved model.
        
        Returns:
            AnomalyDetector: The loaded model.
        """
        # Load the model and scaler
        saved_data = joblib.load(filepath)
        
        # Create a new instance
        detector = cls()
        detector.model = saved_data['model']
        detector.scaler = saved_data['scaler']
        detector.is_fitted = saved_data['is_fitted']
        detector.feature_names = saved_data['feature_names']
        
        return detector