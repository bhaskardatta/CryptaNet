import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, roc_curve, auc

class ModelEvaluator:
    """
    Evaluates the performance of anomaly detection models.
    
    This class provides methods for calculating various performance metrics
    and visualizing the results of anomaly detection models.
    """
    
    def __init__(self):
        """
        Initialize the model evaluator.
        """
        pass
    
    def calculate_metrics(self, y_true, y_pred):
        """
        Calculate performance metrics for anomaly detection.
        
        Args:
            y_true (array-like): Ground truth labels (1 for normal, -1 for anomalies).
            y_pred (array-like): Predicted labels (1 for normal, -1 for anomalies).
            
        Returns:
            dict: A dictionary containing various performance metrics.
        """
        # Convert to numpy arrays
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        
        # Calculate metrics
        precision = precision_score(y_true, y_pred, pos_label=-1)
        recall = recall_score(y_true, y_pred, pos_label=-1)
        f1 = f1_score(y_true, y_pred, pos_label=-1)
        
        # Calculate confusion matrix
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[1, -1]).ravel()
        
        # Calculate additional metrics
        accuracy = (tp + tn) / (tp + tn + fp + fn)
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        
        return {
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'accuracy': accuracy,
            'specificity': specificity,
            'true_positives': tp,
            'false_positives': fp,
            'true_negatives': tn,
            'false_negatives': fn
        }
    
    def plot_confusion_matrix(self, y_true, y_pred, figsize=(10, 8)):
        """
        Plot the confusion matrix for anomaly detection results.
        
        Args:
            y_true (array-like): Ground truth labels (1 for normal, -1 for anomalies).
            y_pred (array-like): Predicted labels (1 for normal, -1 for anomalies).
            figsize (tuple): Figure size.
            
        Returns:
            matplotlib.figure.Figure: The confusion matrix plot.
        """
        # Convert to numpy arrays
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        
        # Calculate confusion matrix
        cm = confusion_matrix(y_true, y_pred, labels=[1, -1])
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot confusion matrix
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=['Normal', 'Anomaly'], 
                    yticklabels=['Normal', 'Anomaly'])
        
        # Add labels and title
        plt.xlabel('Predicted')
        plt.ylabel('True')
        plt.title('Confusion Matrix')
        
        return fig
    
    def plot_roc_curve(self, y_true, scores, figsize=(10, 8)):
        """
        Plot the ROC curve for anomaly detection results.
        
        Args:
            y_true (array-like): Ground truth labels (1 for normal, -1 for anomalies).
            scores (array-like): Anomaly scores (lower scores indicate more anomalous).
            figsize (tuple): Figure size.
            
        Returns:
            matplotlib.figure.Figure: The ROC curve plot.
        """
        # Convert to numpy arrays
        y_true = np.array(y_true)
        scores = np.array(scores)
        
        # Convert labels to binary (0 for normal, 1 for anomalies)
        y_true_binary = np.where(y_true == -1, 1, 0)
        
        # Calculate ROC curve
        fpr, tpr, thresholds = roc_curve(y_true_binary, -scores)
        roc_auc = auc(fpr, tpr)
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot ROC curve
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        
        # Add labels and title
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve')
        plt.legend(loc='lower right')
        
        return fig
    
    def plot_anomaly_scores(self, scores, threshold=None, anomalies=None, figsize=(12, 6)):
        """
        Plot the anomaly scores with an optional threshold line.
        
        Args:
            scores (array-like): Anomaly scores (lower scores indicate more anomalous).
            threshold (float, optional): Threshold for anomaly detection.
            anomalies (array-like, optional): Boolean array indicating which points are anomalies.
            figsize (tuple): Figure size.
            
        Returns:
            matplotlib.figure.Figure: The anomaly scores plot.
        """
        # Convert to numpy arrays
        scores = np.array(scores)
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot scores
        plt.plot(scores, 'b-', label='Anomaly Scores')
        
        # Plot threshold if provided
        if threshold is not None:
            plt.axhline(y=threshold, color='r', linestyle='--', label=f'Threshold: {threshold:.3f}')
        
        # Highlight anomalies if provided
        if anomalies is not None:
            anomalies = np.array(anomalies)
            plt.scatter(np.where(anomalies)[0], scores[anomalies], color='red', label='Anomalies')
        
        # Add labels and title
        plt.xlabel('Data Point Index')
        plt.ylabel('Anomaly Score')
        plt.title('Anomaly Scores')
        plt.legend()
        
        return fig
    
    def find_optimal_threshold(self, y_true, scores, metric='f1'):
        """
        Find the optimal threshold for anomaly detection based on a specified metric.
        
        Args:
            y_true (array-like): Ground truth labels (1 for normal, -1 for anomalies).
            scores (array-like): Anomaly scores (lower scores indicate more anomalous).
            metric (str): The metric to optimize ('precision', 'recall', 'f1').
            
        Returns:
            float: The optimal threshold value.
        """
        # Convert to numpy arrays
        y_true = np.array(y_true)
        scores = np.array(scores)
        
        # Get unique score values to try as thresholds
        thresholds = np.unique(scores)
        
        # Initialize variables to track the best threshold
        best_threshold = None
        best_metric_value = 0
        
        # Try each threshold
        for threshold in thresholds:
            # Make predictions using the current threshold
            y_pred = np.where(scores < threshold, -1, 1)
            
            # Calculate the specified metric
            if metric == 'precision':
                metric_value = precision_score(y_true, y_pred, pos_label=-1, zero_division=0)
            elif metric == 'recall':
                metric_value = recall_score(y_true, y_pred, pos_label=-1, zero_division=0)
            else:  # default to f1
                metric_value = f1_score(y_true, y_pred, pos_label=-1, zero_division=0)
            
            # Update the best threshold if this one is better
            if metric_value > best_metric_value:
                best_metric_value = metric_value
                best_threshold = threshold
        
        return best_threshold