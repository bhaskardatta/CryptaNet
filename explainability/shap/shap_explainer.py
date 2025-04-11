import numpy as np
import pandas as pd
import shap
import matplotlib.pyplot as plt
import joblib
import os

class ShapExplainer:
    """
    Implements SHAP (SHapley Additive exPlanations) for model interpretation in CryptaNet.
    
    SHAP values represent the contribution of each feature to the prediction for a specific instance.
    This class provides methods for generating and visualizing SHAP values to explain anomaly
    detection results.
    """
    
    def __init__(self, model=None, feature_names=None):
        """
        Initialize the SHAP explainer.
        
        Args:
            model: The trained anomaly detection model.
            feature_names (list, optional): Names of the features used in the model.
        """
        self.model = model
        self.feature_names = feature_names
        self.explainer = None
        self.shap_values = None
        self.is_fitted = False
    
    def fit(self, X_background):
        """
        Fit the SHAP explainer to the background data.
        
        Args:
            X_background (array-like): Background data used to explain the model.
            
        Returns:
            self: The fitted explainer.
        """
        if self.model is None:
            raise ValueError("Model must be provided before fitting the explainer.")
        
        # Convert to numpy array if it's a DataFrame
        if isinstance(X_background, pd.DataFrame):
            X_background = X_background.values
        
        # Create the explainer
        self.explainer = shap.KernelExplainer(
            model=self.model.decision_function,
            data=X_background,
            feature_names=self.feature_names
        )
        
        self.is_fitted = True
        return self
    
    def explain(self, X):
        """
        Generate SHAP values to explain predictions for the input data.
        
        Args:
            X (array-like): The input data to explain.
            
        Returns:
            array: The SHAP values for each instance and feature.
        """
        if not self.is_fitted:
            raise ValueError("Explainer has not been fitted yet.")
        
        # Convert to numpy array if it's a DataFrame
        if isinstance(X, pd.DataFrame):
            X = X.values
        
        # Generate SHAP values
        self.shap_values = self.explainer.shap_values(X)
        
        return self.shap_values
    
    def plot_summary(self, max_display=20):
        """
        Create a summary plot of SHAP values.
        
        Args:
            max_display (int): Maximum number of features to display.
            
        Returns:
            matplotlib.figure.Figure: The summary plot.
        """
        if self.shap_values is None:
            raise ValueError("No SHAP values available. Call explain() first.")
        
        # Create figure
        fig = plt.figure(figsize=(10, 8))
        
        # Create summary plot
        shap.summary_plot(
            shap_values=self.shap_values,
            features=self.explainer.data,
            feature_names=self.feature_names,
            max_display=max_display,
            show=False
        )
        
        plt.title('Feature Importance (SHAP Values)')
        
        return fig
    
    def plot_dependence(self, feature_idx, interaction_idx=None):
        """
        Create a dependence plot for a specific feature.
        
        Args:
            feature_idx (int or str): Index or name of the feature to plot.
            interaction_idx (int or str, optional): Index or name of the feature to use for coloring.
            
        Returns:
            matplotlib.figure.Figure: The dependence plot.
        """
        if self.shap_values is None:
            raise ValueError("No SHAP values available. Call explain() first.")
        
        # Convert feature name to index if necessary
        if isinstance(feature_idx, str) and self.feature_names is not None:
            feature_idx = self.feature_names.index(feature_idx)
        
        # Convert interaction feature name to index if necessary
        if isinstance(interaction_idx, str) and self.feature_names is not None:
            interaction_idx = self.feature_names.index(interaction_idx)
        
        # Create figure
        fig = plt.figure(figsize=(10, 8))
        
        # Create dependence plot
        shap.dependence_plot(
            ind=feature_idx,
            shap_values=self.shap_values,
            features=self.explainer.data,
            feature_names=self.feature_names,
            interaction_index=interaction_idx,
            show=False
        )
        
        feature_name = self.feature_names[feature_idx] if self.feature_names is not None else f"Feature {feature_idx}"
        plt.title(f'Dependence Plot for {feature_name}')
        
        return fig
    
    def explain_instance(self, instance, top_features=5):
        """
        Generate a human-readable explanation for a specific instance.
        
        Args:
            instance (array-like): The instance to explain.
            top_features (int): Number of top features to include in the explanation.
            
        Returns:
            dict: A dictionary containing the explanation.
        """
        if not self.is_fitted:
            raise ValueError("Explainer has not been fitted yet.")
        
        # Convert to numpy array if it's a DataFrame or Series
        if isinstance(instance, pd.DataFrame) or isinstance(instance, pd.Series):
            instance = instance.values.reshape(1, -1)
        elif len(instance.shape) == 1:
            instance = instance.reshape(1, -1)
        
        # Generate SHAP values for the instance
        instance_shap_values = self.explainer.shap_values(instance)[0]
        
        # Get feature names
        feature_names = self.feature_names if self.feature_names is not None else [f"Feature {i}" for i in range(len(instance_shap_values))]
        
        # Create a dictionary of feature names and their SHAP values
        feature_contributions = {name: value for name, value in zip(feature_names, instance_shap_values)}
        
        # Sort features by absolute SHAP value
        sorted_features = sorted(feature_contributions.items(), key=lambda x: abs(x[1]), reverse=True)
        
        # Get the top contributing features
        top_contributing_features = sorted_features[:top_features]
        
        # Generate the explanation
        explanation = {
            'base_value': self.explainer.expected_value,
            'prediction': self.model.decision_function(instance)[0],
            'top_features': [
                {
                    'feature': feature,
                    'contribution': contribution,
                    'direction': 'increases anomaly score' if contribution < 0 else 'decreases anomaly score'
                }
                for feature, contribution in top_contributing_features
            ],
            'explanation_text': self._generate_explanation_text(top_contributing_features)
        }
        
        return explanation
    
    def _generate_explanation_text(self, feature_contributions):
        """
        Generate a human-readable explanation text based on feature contributions.
        
        Args:
            feature_contributions (list): List of (feature, contribution) tuples.
            
        Returns:
            str: A human-readable explanation.
        """
        # Start with a general statement
        explanation = "This instance was flagged as anomalous primarily because of the following factors:\n"
        
        # Add details for each feature
        for i, (feature, contribution) in enumerate(feature_contributions):
            direction = "high" if contribution < 0 else "low"
            explanation += f"{i+1}. The {feature} value is unusually {direction} "
            explanation += f"(contributing {abs(contribution):.4f} to the anomaly score).\n"
        
        return explanation
    
    def save(self, filepath):
        """
        Save the fitted explainer to a file.
        
        Args:
            filepath (str): Path to save the explainer.
        """
        if not self.is_fitted:
            raise ValueError("Explainer has not been fitted yet.")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save the explainer
        joblib.dump({
            'explainer': self.explainer,
            'feature_names': self.feature_names,
            'is_fitted': self.is_fitted
        }, filepath)
    
    @classmethod
    def load(cls, filepath, model=None):
        """
        Load a fitted explainer from a file.
        
        Args:
            filepath (str): Path to the saved explainer.
            model: The trained anomaly detection model (optional if already saved with the explainer).
            
        Returns:
            ShapExplainer: The loaded explainer.
        """
        # Load the explainer
        saved_data = joblib.load(filepath)
        
        # Create a new instance
        explainer = cls(model=model, feature_names=saved_data['feature_names'])
        explainer.explainer = saved_data['explainer']
        explainer.is_fitted = saved_data['is_fitted']
        
        # Update the model if provided
        if model is not None:
            explainer.model = model
            explainer.explainer.model = model.decision_function
        
        return explainer