import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, precision_recall_curve, roc_curve, auc
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import time
from datetime import datetime
import json
import shap

class AdvancedEvaluator:
    """
    Implements a sophisticated evaluation framework for ultra-high-precision anomaly detection.
    
    This class provides cost-sensitive evaluation metrics with financial impact weighting,
    time-to-detection penalties, precision-recall curves at multiple operating points,
    and lift charts for business value assessment.
    """
    
    def __init__(self, results_dir=None):
        """
        Initialize the advanced evaluator.
        
        Args:
            results_dir (str, optional): Directory to save evaluation results
        """
        if results_dir is None:
            self.results_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results')
        else:
            self.results_dir = results_dir
            
        os.makedirs(self.results_dir, exist_ok=True)
        
    def calculate_metrics(self, y_true, y_pred, decision_scores=None, cost_matrix=None):
        """
        Calculate comprehensive evaluation metrics including cost-sensitive metrics.
        
        Args:
            y_true (array): Ground truth labels (1 for normal, -1 for anomaly)
            y_pred (array): Predicted labels (1 for normal, -1 for anomaly)
            decision_scores (array, optional): Decision scores for ROC and PR curves
            cost_matrix (dict, optional): Cost matrix for different error types
                                        {"fp_cost": cost of false positive,
                                         "fn_cost": cost of false negative}
            
        Returns:
            dict: Evaluation metrics
        """
        # Default cost matrix if none provided
        if cost_matrix is None:
            # By default, false negatives are 5x more costly than false positives
            cost_matrix = {"fp_cost": 1.0, "fn_cost": 5.0}
        
        # Convert to binary classification (1 for normal, 0 for anomaly)
        y_true_binary = (y_true == 1).astype(int)
        y_pred_binary = (y_pred == 1).astype(int)
        
        # Calculate basic metrics
        accuracy = accuracy_score(y_true_binary, y_pred_binary)
        precision = precision_score(y_true_binary, y_pred_binary)
        recall = recall_score(y_true_binary, y_pred_binary)
        f1 = f1_score(y_true_binary, y_pred_binary)
        
        # Calculate confusion matrix
        tn, fp, fn, tp = confusion_matrix(y_true_binary, y_pred_binary).ravel()
        
        # Calculate additional metrics
        false_positive_rate = fp / (fp + tn) if (fp + tn) > 0 else 0
        false_negative_rate = fn / (fn + tp) if (fn + tp) > 0 else 0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        
        # Calculate cost-sensitive metrics
        total_cost = (fp * cost_matrix["fp_cost"] + fn * cost_matrix["fn_cost"]) / len(y_true)
        cost_savings = 1.0 - (total_cost / max(cost_matrix["fp_cost"], cost_matrix["fn_cost"]))
        
        # Calculate ROC AUC if decision scores are provided
        roc_auc = None
        pr_auc = None
        if decision_scores is not None:
            from sklearn.metrics import roc_auc_score, average_precision_score
            roc_auc = roc_auc_score(y_true_binary, decision_scores)
            pr_auc = average_precision_score(y_true_binary, decision_scores)
        
        # Compile metrics
        metrics = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'specificity': specificity,
            'false_positive_rate': false_positive_rate,
            'false_negative_rate': false_negative_rate,
            'true_negatives': int(tn),
            'false_positives': int(fp),
            'false_negatives': int(fn),
            'true_positives': int(tp),
            'total_cost': total_cost,
            'cost_savings': cost_savings
        }
        
        if roc_auc is not None:
            metrics['roc_auc'] = roc_auc
        if pr_auc is not None:
            metrics['pr_auc'] = pr_auc
        
        return metrics
    
    def calculate_metrics_at_multiple_thresholds(self, y_true, decision_scores, thresholds=None, cost_matrix=None):
        """
        Calculate metrics at multiple operating points (thresholds).
        
        Args:
            y_true (array): Ground truth labels (1 for normal, -1 for anomaly)
            decision_scores (array): Decision scores
            thresholds (array, optional): Thresholds to evaluate
            cost_matrix (dict, optional): Cost matrix for different error types
            
        Returns:
            DataFrame: Metrics at each threshold
        """
        # Convert to binary classification (1 for normal, 0 for anomaly)
        y_true_binary = (y_true == 1).astype(int)
        
        # Generate thresholds if not provided
        if thresholds is None:
            # Use percentiles as thresholds
            thresholds = np.percentile(decision_scores, np.arange(1, 100, 1))
        
        # Calculate metrics at each threshold
        results = []
        for threshold in thresholds:
            y_pred_binary = (decision_scores >= threshold).astype(int)
            y_pred = np.where(y_pred_binary == 1, 1, -1)
            
            metrics = self.calculate_metrics(y_true, y_pred, None, cost_matrix)
            metrics['threshold'] = threshold
            results.append(metrics)
        
        return pd.DataFrame(results)
    
    def find_optimal_threshold(self, y_true, decision_scores, optimization_metric='f1_score', cost_matrix=None):
        """
        Find the optimal threshold based on a specified metric.
        
        Args:
            y_true (array): Ground truth labels (1 for normal, -1 for anomaly)
            decision_scores (array): Decision scores
            optimization_metric (str): Metric to optimize ('f1_score', 'cost_savings', etc.)
            cost_matrix (dict, optional): Cost matrix for different error types
            
        Returns:
            float: Optimal threshold
        """
        # Calculate metrics at multiple thresholds
        metrics_df = self.calculate_metrics_at_multiple_thresholds(y_true, decision_scores, None, cost_matrix)
        
        # Find optimal threshold
        if optimization_metric == 'cost_savings':
            # For cost savings, higher is better
            best_idx = metrics_df['cost_savings'].idxmax()
        elif optimization_metric == 'total_cost':
            # For total cost, lower is better
            best_idx = metrics_df['total_cost'].idxmin()
        else:
            # For other metrics (accuracy, f1, etc.), higher is better
            best_idx = metrics_df[optimization_metric].idxmax()
        
        optimal_threshold = metrics_df.loc[best_idx, 'threshold']
        optimal_metrics = metrics_df.loc[best_idx].to_dict()
        
        return optimal_threshold, optimal_metrics
    
    def calculate_time_to_detection(self, y_true, y_pred, timestamps, anomaly_label=-1):
        """
        Calculate time-to-detection metrics for anomalies.
        
        Args:
            y_true (array): Ground truth labels (1 for normal, -1 for anomaly)
            y_pred (array): Predicted labels (1 for normal, -1 for anomaly)
            timestamps (array): Timestamps for each data point
            anomaly_label (int): Label value for anomalies
            
        Returns:
            dict: Time-to-detection metrics
        """
        # Convert timestamps to datetime if they're not already
        if not isinstance(timestamps[0], (pd.Timestamp, datetime)):
            timestamps = pd.to_datetime(timestamps)
        
        # Find anomaly events (consecutive anomalies are considered one event)
        anomaly_events = []
        current_event = None
        
        for i in range(len(y_true)):
            if y_true[i] == anomaly_label:
                if current_event is None:
                    # Start of a new anomaly event
                    current_event = {
                        'start_idx': i,
                        'start_time': timestamps[i],
                        'detected': False,
                        'detection_idx': None,
                        'detection_time': None
                    }
            else:
                if current_event is not None:
                    # End of current anomaly event
                    current_event['end_idx'] = i - 1
                    current_event['end_time'] = timestamps[i - 1]
                    anomaly_events.append(current_event)
                    current_event = None
        
        # Handle case where the last point is an anomaly
        if current_event is not None:
            current_event['end_idx'] = len(y_true) - 1
            current_event['end_time'] = timestamps[-1]
            anomaly_events.append(current_event)
        
        # Check if each anomaly event was detected
        detection_times = []
        for event in anomaly_events:
            for i in range(event['start_idx'], event['end_idx'] + 1):
                if y_pred[i] == anomaly_label:
                    event['detected'] = True
                    event['detection_idx'] = i
                    event['detection_time'] = timestamps[i]
                    
                    # Calculate detection delay
                    detection_delay = (event['detection_time'] - event['start_time']).total_seconds()
                    event['detection_delay'] = detection_delay
                    detection_times.append(detection_delay)
                    break
        
        # Calculate metrics
        num_events = len(anomaly_events)
        num_detected = sum(1 for event in anomaly_events if event['detected'])
        detection_rate = num_detected / num_events if num_events > 0 else 0
        
        avg_detection_time = np.mean(detection_times) if detection_times else np.nan
        median_detection_time = np.median(detection_times) if detection_times else np.nan
        max_detection_time = np.max(detection_times) if detection_times else np.nan
        
        return {
            'num_anomaly_events': num_events,
            'num_detected_events': num_detected,
            'detection_rate': detection_rate,
            'avg_detection_time': avg_detection_time,
            'median_detection_time': median_detection_time,
            'max_detection_time': max_detection_time,
            'anomaly_events': anomaly_events
        }
    
    def calculate_business_impact(self, y_true, y_pred, impact_values, anomaly_label=-1):
        """
        Calculate business impact metrics based on financial values.
        
        Args:
            y_true (array): Ground truth labels (1 for normal, -1 for anomaly)
            y_pred (array): Predicted labels (1 for normal, -1 for anomaly)
            impact_values (array): Financial impact value for each data point
            anomaly_label (int): Label value for anomalies
            
        Returns:
            dict: Business impact metrics
        """
        # Calculate confusion matrix
        y_true_binary = (y_true != anomaly_label).astype(int)
        y_pred_binary = (y_pred != anomaly_label).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_true_binary, y_pred_binary).ravel()
        
        # Calculate impact for each category
        true_negative_impact = sum(impact_values[i] for i in range(len(y_true)) 
                                if y_true[i] != anomaly_label and y_pred[i] != anomaly_label)
        
        false_positive_impact = sum(impact_values[i] for i in range(len(y_true)) 
                                 if y_true[i] != anomaly_label and y_pred[i] == anomaly_label)
        
        false_negative_impact = sum(impact_values[i] for i in range(len(y_true)) 
                                 if y_true[i] == anomaly_label and y_pred[i] != anomaly_label)
        
        true_positive_impact = sum(impact_values[i] for i in range(len(y_true)) 
                               if y_true[i] == anomaly_label and y_pred[i] == anomaly_label)
        
        # Calculate total impact
        total_actual_impact = true_negative_impact + false_negative_impact + true_positive_impact + false_positive_impact
        total_prevented_impact = true_positive_impact
        total_missed_impact = false_negative_impact
        total_false_alarm_impact = false_positive_impact
        
        # Calculate impact prevention rate
        impact_prevention_rate = total_prevented_impact / (total_prevented_impact + total_missed_impact) \
                                if (total_prevented_impact + total_missed_impact) > 0 else 0
        
        # Calculate ROI (Return on Investment)
        # Assuming the cost of running the model is negligible compared to the impact
        roi = (total_prevented_impact - total_false_alarm_impact) / total_actual_impact \
              if total_actual_impact > 0 else 0
        
        return {
            'true_negative_impact': true_negative_impact,
            'false_positive_impact': false_positive_impact,
            'false_negative_impact': false_negative_impact,
            'true_positive_impact': true_positive_impact,
            'total_actual_impact': total_actual_impact,
            'total_prevented_impact': total_prevented_impact,
            'total_missed_impact': total_missed_impact,
            'total_false_alarm_impact': total_false_alarm_impact,
            'impact_prevention_rate': impact_prevention_rate,
            'roi': roi
        }
    
    def plot_confusion_matrix(self, y_true, y_pred, normalize=False, title=None, save_path=None):
        """
        Plot confusion matrix with enhanced visualization.
        
        Args:
            y_true (array): Ground truth labels (1 for normal, -1 for anomaly)
            y_pred (array): Predicted labels (1 for normal, -1 for anomaly)
            normalize (bool): Whether to normalize the confusion matrix
            title (str, optional): Title for the plot
            save_path (str, optional): Path to save the plot
            
        Returns:
            matplotlib.figure.Figure: The figure object
        """
        # Convert to binary classification (1 for normal, 0 for anomaly)
        y_true_binary = (y_true == 1).astype(int)
        y_pred_binary = (y_pred == 1).astype(int)
        
        # Calculate confusion matrix
        cm = confusion_matrix(y_true_binary, y_pred_binary)
        
        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        
        # Create figure
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='.4f' if normalize else 'd', cmap='Blues',
                   xticklabels=['Anomaly', 'Normal'], yticklabels=['Anomaly', 'Normal'])
        
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        if title is None:
            title = 'Normalized Confusion Matrix' if normalize else 'Confusion Matrix'
        plt.title(title)
        
        plt.tight_layout()
        
        if save_path is not None:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return plt.gcf()
    
    def plot_precision_recall_curve(self, y_true, decision_scores, title=None, save_path=None):
        """
        Plot precision-recall curve with enhanced visualization.
        
        Args:
            y_true (array): Ground truth labels (1 for normal, -1 for anomaly)
            decision_scores (array): Decision scores
            title (str, optional): Title for the plot
            save_path (str, optional): Path to save the plot
            
        Returns:
            matplotlib.figure.Figure: The figure object
        """
        # Convert to binary classification (1 for normal, 0 for anomaly)
        y_true_binary = (y_true == 1).astype(int)
        
        # Calculate precision-recall curve
        precision, recall, thresholds = precision_recall_curve(y_true_binary, decision_scores)
        pr_auc = auc(recall, precision)
        
        # Create figure
        plt.figure(figsize=(10, 8))
        plt.plot(recall, precision, lw=2, label=f'PR curve (AUC = {pr_auc:.4f})')
        
        # Add operating points
        for threshold_percentile in [90, 95, 99, 99.9]:
            threshold = np.percentile(decision_scores, threshold_percentile)
            y_pred_binary = (decision_scores >= threshold).astype(int)
            
            current_precision = precision_score(y_true_binary, y_pred_binary)
            current_recall = recall_score(y_true_binary, y_pred_binary)
            
            plt.plot(current_recall, current_precision, 'o', markersize=8,
                    label=f'{threshold_percentile}th percentile (P={current_precision:.4f}, R={current_recall:.4f})')
        
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        
        if title is None:
            title = 'Precision-Recall Curve'
        plt.title(title)
        
        plt.legend(loc='lower left')
        plt.grid(True)
        plt.tight_layout()
        
        if save_path is not None:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return plt.gcf()
    
    def plot_roc_curve(self, y_true, decision_scores, title=None, save_path=None):
        """
        Plot ROC curve with enhanced visualization.
        
        Args:
            y_true (array): Ground truth labels (1 for normal, -1 for anomaly)
            decision_scores (array): Decision scores
            title (str, optional): Title for the plot
            save_path (str, optional): Path to save the plot
            
        Returns:
            matplotlib.figure.Figure: The figure object
        """
        # Convert to binary classification (1 for normal, 0 for anomaly)
        y_true_binary = (y_true == 1).astype(int)
        
        # Calculate ROC curve
        fpr, tpr, thresholds = roc_curve(y_true_binary, decision_scores)
        roc_auc = auc(fpr, tpr)
        
        # Create figure
        plt.figure(figsize=(10, 8))
        plt.plot(fpr, tpr, lw=2, label=f'ROC curve (AUC = {roc_auc:.4f})')
        plt.plot([0, 1], [0, 1], 'k--', lw=2)
        
        # Add operating points
        for threshold_percentile in [90, 95, 99, 99.9]:
            threshold = np.percentile(decision_scores, threshold_percentile)
            y_pred_binary = (decision_scores >= threshold).astype(int)
            
            current_fpr = np.sum((y_pred_binary == 1) & (y_true_binary == 0)) / np.sum(y_true_binary == 0)
            current_tpr = np.sum((y_pred_binary == 1) & (y_true_binary == 1)) / np.sum(y_true_binary == 1)
            
            plt.plot(current_fpr, current_tpr, 'o', markersize=8,
                    label=f'{threshold_percentile}th percentile (FPR={current_fpr:.4f}, TPR={current_tpr:.4f})')
        
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        
        if title is None:
            title = 'Receiver Operating Characteristic (ROC) Curve'
        plt.title(title)
        
        plt.legend(loc='lower right')
        plt.grid(True)
        plt.tight_layout()
        
        if save_path is not None:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return plt.gcf()
    
    def plot_lift_chart(self, y_true, decision_scores, num_bins=10, title=None, save_path=None):
        """
        Plot lift chart for business value assessment.
        
        Args:
            y_true (array): Ground truth labels (1 for normal, -1 for anomaly)
            decision_scores (array): Decision scores
            num_bins (int): Number of bins for the lift chart
            title (str, optional): Title for the plot
            save_path (str, optional): Path to save the plot
            
        Returns:
            matplotlib.figure.Figure: The figure object
        """
        # Convert to binary classification (1 for normal, 0 for anomaly)
        y_true_binary = (y_true == 1).astype(int)
        
        # Create a DataFrame for easier manipulation
        df = pd.DataFrame({
            'score': decision_scores,
            'target': y_true_binary
        })
        
        # Sort by score in descending order
        df = df.sort_values('score', ascending=False).reset_index(drop=True)
        
        # Calculate cumulative metrics
        df['cumulative_data_fraction'] = (df.index + 1) / len(df)
        df['cumulative_target_captured'] = df['target'].cumsum()
        df['cumulative_target_fraction'] = df['cumulative_target_captured'] / df['target'].sum()
        df['lift'] = df['cumulative_target_fraction'] / df['cumulative_data_fraction']
        
        # Create bins for the lift chart
        bins = np.linspace(0, 1, num_bins + 1)
        bin_labels = [f'{int(bins[i]*100)}%-{int(bins[i+1]*100)}%' for i in range(num_bins)]
        
        df['bin'] = pd.cut(df['cumulative_data_fraction'], bins, labels=bin_labels)
        
        # Calculate lift for each bin
        bin_lift = df.groupby('bin')['lift'].first().reset_index()
        
        # Create figure
        plt.figure(figsize=(12, 8))
        
        # Plot lift chart
        ax1 = plt.subplot(111)
        ax1.bar(bin_lift['bin'], bin_lift['lift'], color='skyblue', alpha=0.7)
        ax1.axhline(y=1, color='r', linestyle='--', label='Baseline (No Lift)')
        ax1.set_xlabel('Population Percentile (Sorted by Score)')
        ax1.set_ylabel('Lift')
        ax1.set_ylim(bottom=0)
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')
        
        # Add cumulative gains curve on secondary y-axis
        ax2 = ax1.twinx()
        ax2.plot(df['cumulative_data_fraction'], df['cumulative_target_fraction'], 'g-', linewidth=2, label='Cumulative Gains')
        ax2.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random Model')
        ax2.set_ylabel('Cumulative Target Fraction', color='g')
        ax2.set_ylim([0, 1.05])
        
        # Add legends
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        if title is None:
            title = 'Lift Chart and Cumulative Gains Curve'
        plt.title(title)
        
        plt.tight_layout()
        
        if save_path is not None:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return plt.gcf()
    
    def generate_comprehensive_report(self, y_true, y_pred, decision_scores, timestamps=None, impact_values=None, cost_matrix=None, report_path=None):
        """
        Generate a comprehensive evaluation report with all metrics and visualizations.
        
        Args:
            y_true (array): Ground truth labels (1 for normal, -1 for anomaly)
            y_pred (array): Predicted labels (1 for normal, -1 for anomaly)
            decision_scores (array): Decision scores
            timestamps (array, optional): Timestamps for each data point
            impact_values (array, optional): Financial impact value for each data point
            cost_matrix (dict, optional): Cost matrix for different error types
            report_path (str, optional): Path to save the report
            
        Returns:
            dict: Comprehensive evaluation results
        """
        # Create timestamp for report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if report_path is None:
            report_path = os.path.join(self.results_dir, f"evaluation_report_{timestamp}")
        
        os.makedirs(report_path, exist_ok=True)
        
        # Calculate basic metrics
        basic_metrics = self.calculate_metrics(y_true, y_pred, decision_scores, cost_matrix)
        
        # Calculate metrics at multiple thresholds
        threshold_metrics = self.calculate_metrics_at_multiple_thresholds(y_true, decision_scores, None, cost_matrix)
        
        # Find optimal threshold
        optimal_threshold, optimal_metrics = self.find_optimal_threshold(y_true, decision_scores, 'f1_score', cost_matrix)
        
        # Calculate time-to-detection metrics if timestamps are provided
        time_metrics = None
        if timestamps is not None:
            time_metrics = self.calculate_time_to_detection(y_true, y_pred, timestamps)
        
        # Calculate business impact metrics if impact values are provided
        business_metrics = None
        if impact_values is not None:
            business_metrics = self.calculate_business_impact(y_true, y_pred, impact_values)
        
        # Generate visualizations
        # 1. Confusion Matrix
        cm_path = os.path.join(report_path, 'confusion_matrix.png')
        self.plot_confusion_matrix(y_true, y_pred, normalize=False, save_path=cm_path)
        
        cm_norm_path = os.path.join(report_path, 'confusion_matrix_normalized.png')
        self.plot_confusion_matrix(y_true, y_pred, normalize=True, save_path=cm_norm_path)
        
        # 2. Precision-Recall Curve
        pr_path = os.path.join(report_path, 'precision_recall_curve.png')
        self.plot_precision_recall_curve(y_true, decision_scores, save_path=pr_path)
        
        # 3. ROC Curve
        roc_path = os.path.join(report_path, 'roc_curve.png')
        self.plot_roc_curve(y_true, decision_scores, save_path=roc_path)
        
        # 4. Lift Chart
        lift_path = os.path.join(report_path, 'lift_chart.png')
        self.plot_lift_chart(y_true, decision_scores, save_path=lift_path)
        
        # Compile all results
        results = {
            'basic_metrics': basic_metrics,
            'optimal_threshold': optimal_threshold,
            'optimal_metrics': optimal_metrics,
            'visualizations': {
                'confusion_matrix': cm_path,
                'confusion_matrix_normalized': cm_norm_path,
                'precision_recall_curve': pr_path,
                'roc_curve': roc_path,
                'lift_chart': lift_path
            }
        }
        
        if time_metrics is not None:
            results['time_metrics'] = time_metrics
        
        if business_metrics is not None:
            results['business_metrics'] = business_metrics
        
        # Save threshold metrics to CSV
        threshold_metrics_path = os.path.join(report_path, '