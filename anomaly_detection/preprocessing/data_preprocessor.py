import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os

class DataPreprocessor:
    """
    Handles preprocessing of supply chain data for anomaly detection.
    
    This class provides methods for cleaning, transforming, and normalizing
    supply chain data before feeding it into the anomaly detection model.
    """
    
    def __init__(self):
        """
        Initialize the data preprocessor.
        """
        self.numerical_pipeline = None
        self.categorical_pipeline = None
        self.preprocessor = None
        self.numerical_features = None
        self.categorical_features = None
        self.is_fitted = False
    
    def fit(self, data, numerical_features=None, categorical_features=None):
        """
        Fit the preprocessor to the data.
        
        Args:
            data (DataFrame): The input data to fit the preprocessor.
            numerical_features (list): List of numerical feature names.
            categorical_features (list): List of categorical feature names.
            
        Returns:
            self: The fitted preprocessor.
        """
        # If features are not specified, infer them from the data
        if numerical_features is None and categorical_features is None:
            numerical_features = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
            categorical_features = data.select_dtypes(include=['object', 'category']).columns.tolist()
        
        self.numerical_features = numerical_features
        self.categorical_features = categorical_features
        
        # Create preprocessing pipelines
        self.numerical_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        
        self.categorical_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])
        
        # Create column transformer
        transformers = []
        
        if numerical_features:
            transformers.append(('num', self.numerical_pipeline, numerical_features))
        
        if categorical_features:
            transformers.append(('cat', self.categorical_pipeline, categorical_features))
        
        self.preprocessor = ColumnTransformer(transformers)
        
        # Fit the preprocessor
        self.preprocessor.fit(data)
        self.is_fitted = True
        
        return self
    
    def transform(self, data):
        """
        Transform the data using the fitted preprocessor.
        
        Args:
            data (DataFrame): The input data to transform.
            
        Returns:
            array: The transformed data.
        """
        if not self.is_fitted:
            raise ValueError("Preprocessor has not been fitted yet.")
        
        return self.preprocessor.transform(data)
    
    def fit_transform(self, data, numerical_features=None, categorical_features=None):
        """
        Fit the preprocessor to the data and transform it.
        
        Args:
            data (DataFrame): The input data to fit and transform.
            numerical_features (list): List of numerical feature names.
            categorical_features (list): List of categorical feature names.
            
        Returns:
            array: The transformed data.
        """
        self.fit(data, numerical_features, categorical_features)
        return self.transform(data)
    
    def get_feature_names(self):
        """
        Get the names of the features after transformation.
        
        Returns:
            list: The feature names after transformation.
        """
        if not self.is_fitted:
            raise ValueError("Preprocessor has not been fitted yet.")
        
        feature_names = []
        
        # Get numerical feature names (unchanged)
        if self.numerical_features:
            feature_names.extend(self.numerical_features)
        
        # Get categorical feature names (with one-hot encoding)
        if self.categorical_features and hasattr(self.preprocessor.named_transformers_['cat'].named_steps['onehot'], 'get_feature_names_out'):
            cat_features = self.preprocessor.named_transformers_['cat'].named_steps['onehot'].get_feature_names_out(self.categorical_features)
            feature_names.extend(cat_features)
        
        return feature_names
    
    def save(self, filepath):
        """
        Save the fitted preprocessor to a file.
        
        Args:
            filepath (str): Path to save the preprocessor.
        """
        if not self.is_fitted:
            raise ValueError("Preprocessor has not been fitted yet.")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save the preprocessor
        joblib.dump({
            'preprocessor': self.preprocessor,
            'numerical_features': self.numerical_features,
            'categorical_features': self.categorical_features,
            'is_fitted': self.is_fitted
        }, filepath)
    
    @classmethod
    def load(cls, filepath):
        """
        Load a fitted preprocessor from a file.
        
        Args:
            filepath (str): Path to the saved preprocessor.
            
        Returns:
            DataPreprocessor: The loaded preprocessor.
        """
        # Load the preprocessor
        saved_data = joblib.load(filepath)
        
        # Create a new instance
        preprocessor = cls()
        preprocessor.preprocessor = saved_data['preprocessor']
        preprocessor.numerical_features = saved_data['numerical_features']
        preprocessor.categorical_features = saved_data['categorical_features']
        preprocessor.is_fitted = saved_data['is_fitted']
        
        # Extract the pipelines from the column transformer
        if 'num' in preprocessor.preprocessor.named_transformers_:
            preprocessor.numerical_pipeline = preprocessor.preprocessor.named_transformers_['num']
        
        if 'cat' in preprocessor.preprocessor.named_transformers_:
            preprocessor.categorical_pipeline = preprocessor.preprocessor.named_transformers_['cat']
        
        return preprocessor