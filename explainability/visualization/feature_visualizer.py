import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
from io import BytesIO

class FeatureVisualizer:
    """
    Provides visualization tools for feature importance and anomaly explanations.
    
    This class creates various visualizations to help users understand the
    importance of different features in anomaly detection and the reasons
    behind specific anomaly detections.
    """
    
    def __init__(self, feature_names=None):
        """
        Initialize the feature visualizer.
        
        Args:
            feature_names (list, optional): Names of the features to visualize.
        """
        self.feature_names = feature_names
    
    def plot_feature_importance(self, importance_values, feature_names=None, top_n=10, figsize=(10, 8)):
        """
        Create a bar chart of feature importance.
        
        Args:
            importance_values (array-like): The importance values for each feature.
            feature_names (list, optional): Names of the features. If None, uses self.feature_names.
            top_n (int): Number of top features to display.
            figsize (tuple): Figure size.
            
        Returns:
            matplotlib.figure.Figure: The feature importance plot.
        """
        # Use provided feature names or fall back to instance variable
        if feature_names is None:
            feature_names = self.feature_names
        
        if feature_names is None:
            feature_names = [f"Feature {i}" for i in range(len(importance_values))]
        
        # Create a DataFrame for easier sorting and plotting
        importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importance_values
        })
        
        # Sort by importance and take top N
        importance_df = importance_df.sort_values('Importance', ascending=False).head(top_n)
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot horizontal bar chart
        sns.barplot(x='Importance', y='Feature', data=importance_df, ax=ax)
        
        # Add labels and title
        plt.xlabel('Importance')
        plt.ylabel('Feature')
        plt.title('Feature Importance')
        
        return fig
    
    def plot_feature_distribution(self, data, feature, anomalies=None, figsize=(10, 6)):
        """
        Create a distribution plot for a specific feature, highlighting anomalies.
        
        Args:
            data (DataFrame): The dataset containing the feature.
            feature (str): The name of the feature to visualize.
            anomalies (array-like, optional): Boolean array indicating which points are anomalies.
            figsize (tuple): Figure size.
            
        Returns:
            matplotlib.figure.Figure: The feature distribution plot.
        """
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        if anomalies is not None:
            # Plot normal points
            sns.histplot(data.loc[~anomalies, feature], color='blue', label='Normal', alpha=0.5, ax=ax)
            
            # Plot anomalies
            sns.histplot(data.loc[anomalies, feature], color='red', label='Anomaly', alpha=0.5, ax=ax)
            
            plt.legend()
        else:
            # Plot all points
            sns.histplot(data[feature], ax=ax)
        
        # Add labels and title
        plt.xlabel(feature)
        plt.ylabel('Count')
        plt.title(f'Distribution of {feature}')
        
        return fig
    
    def plot_feature_pair(self, data, feature_x, feature_y, anomalies=None, figsize=(10, 8)):
        """
        Create a scatter plot for a pair of features, highlighting anomalies.
        
        Args:
            data (DataFrame): The dataset containing the features.
            feature_x (str): The name of the feature for the x-axis.
            feature_y (str): The name of the feature for the y-axis.
            anomalies (array-like, optional): Boolean array indicating which points are anomalies.
            figsize (tuple): Figure size.
            
        Returns:
            matplotlib.figure.Figure: The feature pair plot.
        """
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        if anomalies is not None:
            # Plot normal points
            ax.scatter(data.loc[~anomalies, feature_x], data.loc[~anomalies, feature_y], 
                      color='blue', label='Normal', alpha=0.5)
            
            # Plot anomalies
            ax.scatter(data.loc[anomalies, feature_x], data.loc[anomalies, feature_y], 
                      color='red', label='Anomaly', alpha=0.8)
            
            plt.legend()
        else:
            # Plot all points
            ax.scatter(data[feature_x], data[feature_y], alpha=0.5)
        
        # Add labels and title
        plt.xlabel(feature_x)
        plt.ylabel(feature_y)
        plt.title(f'{feature_x} vs {feature_y}')
        
        return fig
    
    def create_interactive_feature_importance(self, importance_values, feature_names=None, top_n=10):
        """
        Create an interactive bar chart of feature importance using Plotly.
        
        Args:
            importance_values (array-like): The importance values for each feature.
            feature_names (list, optional): Names of the features. If None, uses self.feature_names.
            top_n (int): Number of top features to display.
            
        Returns:
            plotly.graph_objects.Figure: The interactive feature importance plot.
        """
        # Use provided feature names or fall back to instance variable
        if feature_names is None:
            feature_names = self.feature_names
        
        if feature_names is None:
            feature_names = [f"Feature {i}" for i in range(len(importance_values))]
        
        # Create a DataFrame for easier sorting and plotting
        importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importance_values
        })
        
        # Sort by importance and take top N
        importance_df = importance_df.sort_values('Importance', ascending=False).head(top_n)
        
        # Create interactive bar chart
        fig = px.bar(
            importance_df,
            x='Importance',
            y='Feature',
            orientation='h',
            title='Feature Importance',
            labels={'Importance': 'Importance', 'Feature': 'Feature'},
            color='Importance',
            color_continuous_scale='Viridis'
        )
        
        # Update layout
        fig.update_layout(
            xaxis_title='Importance',
            yaxis_title='Feature',
            yaxis={'categoryorder': 'total ascending'},
            height=500,
            width=800
        )
        
        return fig
    
    def create_interactive_anomaly_dashboard(self, data, anomaly_scores, anomalies, feature_importance=None, top_features=5):
        """
        Create an interactive dashboard for anomaly visualization using Plotly.
        
        Args:
            data (DataFrame): The dataset containing the features.
            anomaly_scores (array-like): The anomaly scores for each data point.
            anomalies (array-like): Boolean array indicating which points are anomalies.
            feature_importance (array-like, optional): The importance values for each feature.
            top_features (int): Number of top features to display.
            
        Returns:
            plotly.graph_objects.Figure: The interactive anomaly dashboard.
        """
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Anomaly Scores',
                'Feature Importance',
                'Feature Distribution',
                'Feature Correlation'
            ),
            specs=[
                [{'type': 'scatter'}, {'type': 'bar'}],
                [{'type': 'histogram'}, {'type': 'scatter'}]
            ],
            vertical_spacing=0.1,
            horizontal_spacing=0.1
        )
        
        # 1. Anomaly Scores Plot
        fig.add_trace(
            go.Scatter(
                x=list(range(len(anomaly_scores))),
                y=anomaly_scores,
                mode='markers',
                marker=dict(
                    color=['red' if a else 'blue' for a in anomalies],
                    size=8,
                    opacity=0.7
                ),
                name='Anomaly Score'
            ),
            row=1, col=1
        )
        
        # 2. Feature Importance Plot
        if feature_importance is not None:
            # Use provided feature names or fall back to instance variable
            feature_names = self.feature_names
            if feature_names is None:
                feature_names = [f"Feature {i}" for i in range(len(feature_importance))]
            
            # Create a DataFrame for easier sorting and plotting
            importance_df = pd.DataFrame({
                'Feature': feature_names,
                'Importance': feature_importance
            })
            
            # Sort by importance and take top N
            importance_df = importance_df.sort_values('Importance', ascending=False).head(top_features)
            
            fig.add_trace(
                go.Bar(
                    x=importance_df['Importance'],
                    y=importance_df['Feature'],
                    orientation='h',
                    marker=dict(color='rgba(58, 71, 80, 0.6)'),
                    name='Feature Importance'
                ),
                row=1, col=2
            )
        
        # 3. Feature Distribution Plot (for the most important feature)
        if feature_importance is not None and len(data.columns) > 0:
            # Get the most important feature
            top_feature = importance_df.iloc[0]['Feature']
            
            # Create separate traces for normal and anomalous points
            fig.add_trace(
                go.Histogram(
                    x=data.loc[~anomalies, top_feature],
                    opacity=0.5,
                    name='Normal',
                    marker=dict(color='blue')
                ),
                row=2, col=1
            )
            
            fig.add_trace(
                go.Histogram(
                    x=data.loc[anomalies, top_feature],
                    opacity=0.5,
                    name='Anomaly',
                    marker=dict(color='red')
                ),
                row=2, col=1
            )
        
        # 4. Feature Correlation Plot (for the top 2 important features)
        if feature_importance is not None and len(data.columns) > 1:
            # Get the top 2 important features
            top_feature1 = importance_df.iloc[0]['Feature']
            top_feature2 = importance_df.iloc[1]['Feature']
            
            # Create separate traces for normal and anomalous points
            fig.add_trace(
                go.Scatter(
                    x=data.loc[~anomalies, top_feature1],
                    y=data.loc[~anomalies, top_feature2],
                    mode='markers',
                    marker=dict(color='blue', size=8, opacity=0.5),
                    name='Normal'
                ),
                row=2, col=2
            )
            
            fig.add_trace(
                go.Scatter(
                    x=data.loc[anomalies, top_feature1],
                    y=data.loc[anomalies, top_feature2],
                    mode='markers',
                    marker=dict(color='red', size=8, opacity=0.7),
                    name='Anomaly'
                ),
                row=2, col=2
            )
            
            # Update axis labels
            fig.update_xaxes(title_text=top_feature1, row=2, col=2)
            fig.update_yaxes(title_text=top_feature2, row=2, col=2)
        
        # Update layout
        fig.update_layout(
            height=800,
            width=1200,
            title_text='Anomaly Detection Dashboard',
            showlegend=True
        )
        
        # Update axis labels
        fig.update_xaxes(title_text='Data Point Index', row=1, col=1)
        fig.update_yaxes(title_text='Anomaly Score', row=1, col=1)
        
        fig.update_xaxes(title_text='Importance', row=1, col=2)
        fig.update_yaxes(title_text='Feature', row=1, col=2)
        
        if feature_importance is not None and len(data.columns) > 0:
            top_feature = importance_df.iloc[0]['Feature']
            fig.update_xaxes(title_text=top_feature, row=2, col=1)
            fig.update_yaxes(title_text='Count', row=2, col=1)
        
        return fig
    
    def plot_to_base64(self, fig):
        """
        Convert a matplotlib figure to a base64-encoded string.
        
        Args:
            fig (matplotlib.figure.Figure): The figure to convert.
            
        Returns:
            str: The base64-encoded string representation of the figure.
        """
        # Save figure to a BytesIO object
        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        
        # Encode the BytesIO object to base64
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        
        return img_str