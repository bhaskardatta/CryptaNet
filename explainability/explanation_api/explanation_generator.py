import numpy as np
import pandas as pd
import json
import os
from ..shap.shap_explainer import ShapExplainer
from ..visualization.feature_visualizer import FeatureVisualizer

class ExplanationGenerator:
    """
    Provides a unified API for generating explanations for anomaly detection results.
    
    This class integrates SHAP-based explanations and feature visualization to provide
    comprehensive, human-readable explanations for detected anomalies.
    """
    
    def __init__(self, model=None, feature_names=None):
        """
        Initialize the explanation generator.
        
        Args:
            model: The trained anomaly detection model.
            feature_names (list, optional): Names of the features used in the model.
        """
        self.model = model
        self.feature_names = feature_names
        self.shap_explainer = ShapExplainer(model=model, feature_names=feature_names)
        self.visualizer = FeatureVisualizer(feature_names=feature_names)
        self.is_fitted = False
    
    def fit(self, X_background):
        """
        Fit the explanation generator to the background data.
        
        Args:
            X_background (array-like): Background data used to explain the model.
            
        Returns:
            self: The fitted generator.
        """
        # Fit the SHAP explainer
        self.shap_explainer.fit(X_background)
        self.is_fitted = True
        return self
    
    def explain_anomaly(self, instance, original_data=None, top_features=5, include_visualizations=True):
        """
        Generate a comprehensive explanation for a specific anomaly.
        
        Args:
            instance (array-like): The anomalous instance to explain.
            original_data (DataFrame, optional): The original data for context.
            top_features (int): Number of top features to include in the explanation.
            include_visualizations (bool): Whether to include visualizations in the explanation.
            
        Returns:
            dict: A dictionary containing the explanation and optional visualizations.
        """
        if not self.is_fitted:
            raise ValueError("Explanation generator has not been fitted yet.")
        
        # Get SHAP-based explanation
        shap_explanation = self.shap_explainer.explain_instance(instance, top_features=top_features)
        
        # Create the base explanation
        explanation = {
            'anomaly_score': float(shap_explanation['prediction']),
            'base_value': float(shap_explanation['base_value']),
            'top_contributing_features': shap_explanation['top_features'],
            'explanation_text': shap_explanation['explanation_text']
        }
        
        # Add visualizations if requested
        if include_visualizations and original_data is not None:
            visualizations = self._generate_visualizations(instance, original_data, shap_explanation)
            explanation['visualizations'] = visualizations
        
        return explanation
    
    def explain_multiple_anomalies(self, instances, original_data=None, top_features=5, include_visualizations=True):
        """
        Generate explanations for multiple anomalies.
        
        Args:
            instances (array-like): The anomalous instances to explain.
            original_data (DataFrame, optional): The original data for context.
            top_features (int): Number of top features to include in each explanation.
            include_visualizations (bool): Whether to include visualizations in the explanations.
            
        Returns:
            list: A list of dictionaries containing explanations for each anomaly.
        """
        if not self.is_fitted:
            raise ValueError("Explanation generator has not been fitted yet.")
        
        explanations = []
        for i, instance in enumerate(instances):
            explanation = self.explain_anomaly(
                instance, 
                original_data, 
                top_features, 
                include_visualizations
            )
            explanation['instance_index'] = i
            explanations.append(explanation)
        
        return explanations
    
    def _generate_visualizations(self, instance, original_data, shap_explanation):
        """
        Generate visualizations for an anomaly explanation.
        
        Args:
            instance (array-like): The anomalous instance.
            original_data (DataFrame): The original data for context.
            shap_explanation (dict): The SHAP-based explanation.
            
        Returns:
            dict: A dictionary containing base64-encoded visualizations.
        """
        # Extract feature importance values from SHAP explanation
        feature_importance = [feature['contribution'] for feature in shap_explanation['top_features']]
        feature_names = [feature['feature'] for feature in shap_explanation['top_features']]
        
        # Create feature importance visualization
        importance_fig = self.visualizer.plot_feature_importance(
            feature_importance, 
            feature_names=feature_names
        )
        importance_base64 = self.visualizer.plot_to_base64(importance_fig)
        
        # Create feature distribution visualization for the top feature
        top_feature = feature_names[0]
        if top_feature in original_data.columns:
            # Identify anomalies (simplified approach)
            anomaly_scores = self.model.decision_function(original_data)
            anomalies = anomaly_scores < 0  # Assuming negative scores indicate anomalies
            
            distribution_fig = self.visualizer.plot_feature_distribution(
                original_data, 
                top_feature, 
                anomalies=anomalies
            )
            distribution_base64 = self.visualizer.plot_to_base64(distribution_fig)
        else:
            distribution_base64 = None
        
        # Create feature pair visualization for the top 2 features
        if len(feature_names) >= 2:
            top_feature1 = feature_names[0]
            top_feature2 = feature_names[1]
            if top_feature1 in original_data.columns and top_feature2 in original_data.columns:
                pair_fig = self.visualizer.plot_feature_pair(
                    original_data, 
                    top_feature1, 
                    top_feature2, 
                    anomalies=anomalies
                )
                pair_base64 = self.visualizer.plot_to_base64(pair_fig)
            else:
                pair_base64 = None
        else:
            pair_base64 = None
        
        return {
            'feature_importance': importance_base64,
            'feature_distribution': distribution_base64,
            'feature_pair': pair_base64
        }
    
    def get_feature_names(self):
        """
        Get the names of the features used in the model.
        
        Returns:
            list: The feature names.
        """
        return self.feature_names
    
    def save(self, filepath):
        """
        Save the fitted explanation generator to a file.
        
        Args:
            filepath (str): Path to save the generator.
        """
        if not self.is_fitted:
            raise ValueError("Explanation generator has not been fitted yet.")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save the SHAP explainer
        self.shap_explainer.save(filepath)
    
    @classmethod
    def load(cls, filepath, model=None):
        """
        Load a fitted explanation generator from a file.
        
        Args:
            filepath (str): Path to the saved generator.
            model: The trained anomaly detection model (optional if already saved with the generator).
            
        Returns:
            ExplanationGenerator: The loaded generator.
        """
        # Load the SHAP explainer
        shap_explainer = ShapExplainer.load(filepath, model=model)
        
        # Create a new instance
        generator = cls(model=model, feature_names=shap_explainer.feature_names)
        generator.shap_explainer = shap_explainer
        generator.is_fitted = shap_explainer.is_fitted
        
        return generator