import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import time
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_curve, auc
from sklearn.preprocessing import StandardScaler
from datetime import datetime
import mlx.core as mx
import mlx.nn as nn
import mlx.optimizers as optim
from joblib import Parallel, delayed
import shap
import warnings
warnings.filterwarnings('ignore')

# Import custom modules
from models.ensemble_detector import HierarchicalEnsembleDetector
from feature_engineering.advanced_feature_extractor import AdvancedFeatureExtractor
from enhanced_data_generator import EnhancedSupplyChainDataGenerator

# Define paths for saving models and results
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saved_models')
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

class ExtremeOptimizationTrainer:
    """
    Implements the extreme optimization protocol for supply chain anomaly detection.
    
    This class orchestrates the entire training pipeline including:
    1. Massive data generation with realistic variability patterns
    2. Advanced feature engineering with 100+ derived features
    3. Hierarchical ensemble model training with multiple algorithms
    4. Bayesian hyperparameter optimization
    5. Adaptive thresholding based on business impact
    6. MLX hardware acceleration on Apple Silicon
    7. Comprehensive evaluation with cost-sensitive metrics
    
    The goal is to achieve 99.9%+ accuracy with near-zero false positives and negligible false negatives.
    """
    
    def __init__(self, random_state=42, use_mlx=True, n_jobs=-1):
        """
        Initialize the extreme optimization trainer.
        
        Args:
            random_state (int): Random seed for reproducibility
            use_mlx (bool): Whether to use MLX acceleration on Apple Silicon
            n_jobs (int): Number of parallel jobs for data processing (-1 uses all cores)
        """
        self.random_state = random_state
        self.use_mlx = use_mlx
        self.n_jobs = n_jobs
        self.feature_extractor = AdvancedFeatureExtractor()
        self.model = None
        self.best_params = None
        self.best_threshold = None
        self.feature_importance = None
        self.training_time = None
        self.evaluation_metrics = None
        
    def generate_data(self, num_samples=1000000, anomaly_ratio=0.01, save_to_file=True):
        """
        Generate massive synthetic supply chain data for training.
        
        Args:
            num_samples (int): Number of data points to generate
            anomaly_ratio (float): Proportion of anomalies in the dataset
            save_to_file (bool): Whether to save the generated data to disk
            
        Returns:
            tuple: (DataFrame with data, array of labels)
        """
        print(f"\n{'='*80}\nGENERATING EXTREME SCALE DATASET\n{'='*80}")
        print(f"Generating {num_samples:,} samples with {anomaly_ratio:.1%} anomaly ratio...")
        
        start_time = time.time()
        
        # Generate data using the enhanced generator
        data_generator = EnhancedSupplyChainDataGenerator(
            num_samples=num_samples,
            anomaly_ratio=anomaly_ratio,
            random_state=self.random_state,
            n_jobs=self.n_jobs
        )
        
        data, labels = data_generator.generate_dataset()
        
        generation_time = time.time() - start_time
        print(f"Data generation completed in {generation_time:.2f} seconds")
        print(f"Generated {len(data):,} samples with {np.sum(labels == -1):,} anomalies ({np.mean(labels == -1):.2%})")
        
        # Save to file if requested
        if save_to_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            data_file = os.path.join(DATA_DIR, f"extreme_data_{num_samples}_{anomaly_ratio}_{timestamp}.csv")
            labels_file = os.path.join(DATA_DIR, f"extreme_labels_{num_samples}_{anomaly_ratio}_{timestamp}.csv")
            
            data.to_csv(data_file, index=False)
            pd.DataFrame({'label': labels}).to_csv(labels_file, index=False)
            
            print(f"Data saved to {data_file}")
            print(f"Labels saved to {labels_file}")
        
        return data, labels
    
    def extract_features(self, data, timestamp_col='timestamp'):
        """
        Extract 100+ advanced features from the supply chain data.
        
        Args:
            data (DataFrame): The input data
            timestamp_col (str): The name of the timestamp column
            
        Returns:
            DataFrame: The data with advanced features
        """
        print(f"\n{'='*80}\nEXTRACTING ADVANCED FEATURES\n{'='*80}")
        start_time = time.time()
        
        # Determine numerical and categorical columns
        numerical_cols = data.select_dtypes(include=['number']).columns.tolist()
        if timestamp_col in numerical_cols:
            numerical_cols.remove(timestamp_col)
            
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
        
        print(f"Base features: {len(numerical_cols)} numerical, {len(categorical_cols)} categorical")
        
        # Extract all advanced features
        data_with_features = self.feature_extractor.extract_all_features(
            data, timestamp_col, numerical_cols, categorical_cols
        )
        
        # Remove any columns with NaN values
        data_with_features = data_with_features.dropna(axis=1, how='any')
        
        # Remove any constant columns
        non_constant_cols = [col for col in data_with_features.columns 
                           if data_with_features[col].nunique() > 1]
        data_with_features = data_with_features[non_constant_cols]
        
        feature_extraction_time = time.time() - start_time
        print(f"Feature extraction completed in {feature_extraction_time:.2f} seconds")
        print(f"Extracted {len(data_with_features.columns)} total features")
        
        return data_with_features
    
    def select_features(self, data, labels, top_n=100):
        """
        Select the most important features using SHAP importance scoring.
        
        Args:
            data (DataFrame): The data with all features
            labels (array): The ground truth labels
            top_n (int): Number of top features to select
            
        Returns:
            DataFrame: The data with selected features
        """
        print(f"\n{'='*80}\nSELECTING TOP FEATURES\n{'='*80}")
        start_time = time.time()
        
        # Remove non-numeric columns for feature selection
        numeric_data = data.select_dtypes(include=['number'])
        
        # Train a simple model for feature importance
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(n_estimators=100, random_state=self.random_state, n_jobs=self.n_jobs)
        model.fit(numeric_data, labels)
        
        # Calculate feature importance using SHAP
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(numeric_data.iloc[:1000])  # Use a subset for speed
        
        # Get feature importance
        feature_importance = np.abs(shap_values).mean(axis=0)
        feature_importance_df = pd.DataFrame({
            'feature': numeric_data.columns,
            'importance': feature_importance
        }).sort_values('importance', ascending=False)
        
        # Select top features
        top_features = feature_importance_df['feature'].head(top_n).tolist()
        
        # Add back categorical columns that were encoded
        categorical_cols = [col for col in data.columns if col not in numeric_data.columns]
        selected_features = top_features + categorical_cols
        
        # Store feature importance for later analysis
        self.feature_importance = feature_importance_df
        
        feature_selection_time = time.time() - start_time
        print(f"Feature selection completed in {feature_selection_time:.2f} seconds")
        print(f"Selected {len(selected_features)} features")
        
        # Save feature importance
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        importance_file = os.path.join(RESULTS_DIR, f"feature_importance_{timestamp}.csv")
        feature_importance_df.to_csv(importance_file, index=False)
        print(f"Feature importance saved to {importance_file}")
        
        return data[selected_features]
    
    def optimize_hyperparameters(self, data, labels, n_trials=100):
        """
        Perform Bayesian hyperparameter optimization.
        
        Args:
            data (DataFrame): The training data
            labels (array): The ground truth labels
            n_trials (int): Number of optimization trials
            
        Returns:
            dict: Best hyperparameters
        """
        print(f"\n{'='*80}\nOPTIMIZING HYPERPARAMETERS\n{'='*80}")
        start_time = time.time()
        
        # Import optuna for Bayesian optimization
        import optuna
        from optuna.samplers import TPESampler
        
        # Split data for optimization
        X_train, X_val, y_train, y_val = train_test_split(
            data, labels, test_size=0.2, random_state=self.random_state, stratify=labels
        )
        
        # Define the objective function for optimization
        def objective(trial):
            # Define hyperparameters to optimize
            params = {
                'contamination': trial.suggest_float('contamination', 0.001, 0.1, log=True),
                'use_mlx': self.use_mlx
            }
            
            # Create and train the model
            model = HierarchicalEnsembleDetector(**params)
            model.fit(X_train, y_train)
            
            # Evaluate on validation set
            y_pred = model.predict(X_val)
            
            # Calculate F1 score (primary metric)
            from sklearn.metrics import f1_score
            y_true_binary = (y_val == 1).astype(int)
            y_pred_binary = (y_pred == 1).astype(int)
            f1 = f1_score(y_true_binary, y_pred_binary)
            
            return f1
        
        # Create study and optimize
        sampler = TPESampler(seed=self.random_state)
        study = optuna.create_study(direction='maximize', sampler=sampler)
        study.optimize(objective, n_trials=n_trials)
        
        # Get best parameters
        self.best_params = study.best_params
        self.best_params['use_mlx'] = self.use_mlx  # Ensure MLX setting is preserved
        
        optimization_time = time.time() - start_time
        print(f"Hyperparameter optimization completed in {optimization_time:.2f} seconds")
        print(f"Best parameters: {self.best_params}")
        print(f"Best F1 score: {study.best_value:.4f}")
        
        return self.best_params
    
    def train_model(self, data, labels, params=None):
        """
        Train the hierarchical ensemble model with the optimized parameters.
        
        Args:
            data (DataFrame): The training data
            labels (array): The ground truth labels
            params (dict, optional): Model parameters (uses best_params if None)
            
        Returns:
            HierarchicalEnsembleDetector: The trained model
        """
        print(f"\n{'='*80}\nTRAINING HIERARCHICAL ENSEMBLE MODEL\n{'='*80}")
        start_time = time.time()
        
        # Use best parameters if none provided
        if params is None:
            if self.best_params is None:
                print("No parameters provided and no best parameters found. Using defaults.")
                params = {'contamination': 0.01, 'use_mlx': self.use_mlx}
            else:
                params = self.best_params
        
        # Create and train the model
        self.model = HierarchicalEnsembleDetector(**params)
        self.model.fit(data, labels)
        
        self.training_time = time.time() - start_time
        print(f"Model training completed in {self.training_time:.2f} seconds")
        
        return self.model
    
    def optimize_threshold(self, data, labels, cost_matrix=None):
        """
        Optimize the decision threshold based on business impact.
        
        Args:
            data (DataFrame): The validation data
            labels (array): The ground truth labels
            cost_matrix (dict, optional): Cost matrix for different error types
                                        {"fp_cost": cost of false positive,
                                         "fn_cost": cost of false negative}
            
        Returns:
            float: Optimized threshold
        """
        print(f"\n{'='*80}\nOPTIMIZING DECISION THRESHOLD\n{'='*80}")
        
        if self.model is None:
            raise ValueError("Model must be trained before optimizing threshold")
        
        # Default cost matrix if none provided
        if cost_matrix is None:
            # By default, false negatives are 5x more costly than false positives
            cost_matrix = {"fp_cost": 1.0, "fn_cost": 5.0}
        
        # Get decision scores
        decision_scores = self.model.decision_function(data)
        
        # Calculate precision-recall curve
        y_true_binary = (labels == 1).astype(int)
        precision, recall, thresholds = precision_recall_curve(y_true_binary, decision_scores)
        
        # Calculate F1 score for each threshold
        f1_scores = 2 * (precision * recall) / (precision + recall + 1e-10)
        
        # Calculate business cost for each threshold
        costs = []
        for threshold in thresholds:
            predictions = (decision_scores >= threshold).astype(int)
            
            # Calculate confusion matrix
            tn, fp, fn, tp = confusion_matrix(y_true_binary, predictions).ravel()
            
            # Calculate cost
            total_cost = (fp * cost_matrix["fp_cost"] + fn * cost_matrix["fn_cost"]) / len(labels)
            costs.append(total_cost)
        
        # Find threshold with minimum cost
        min_cost_idx = np.argmin(costs)
        self.best_threshold = thresholds[min_cost_idx]
        
        # Update model threshold
        self.model.threshold = self.best_threshold
        
        print(f"Optimized threshold: {self.best_threshold:.4f}")
        print(f"At this threshold:")
        print(f"  Precision: {precision[min_cost_idx]:.4f}")
        print(f"  Recall: {recall[min_cost_idx]:.4f}")
        print(f"  F1 Score: {f1_scores[min_cost_idx]:.4f}")
        print(f"  Business Cost: {costs[min_cost_idx]:.4f}")
        
        return self.best_threshold
    
    def evaluate_model(self, data, labels):
        """
        Evaluate the model with comprehensive metrics.
        
        Args:
            data (DataFrame): The test data
            labels (array): The ground truth labels
            
        Returns:
            dict: Evaluation metrics
        """
        print(f"\n{'='*80}\nEVALUATING MODEL PERFORMANCE\n{'='*80}")
        
        if self.model is None:
            raise ValueError("Model must be trained before evaluation")
        
        # Get predictions
        predictions = self.model.predict(data)
        decision_scores = self.model.decision_function(data)
        
        # Convert to binary classification (1 for normal, 0 for anomaly)
        y_true_binary = (labels == 1).astype(int)
        y_pred_binary = (predictions == 1).astype(int)
        
        # Calculate basic metrics
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
        
        accuracy = accuracy_score(y_true_binary, y_pred_binary)
        precision = precision_score(y_true_binary, y_pred_binary)
        recall = recall_score(y_true_binary, y_pred_binary)
        f1 = f1_score(y_true_binary, y_pred_binary)
        roc_auc = roc_auc_score(y_true_binary, decision_scores)
        
        # Calculate confusion matrix
        tn, fp, fn, tp = confusion_matrix(y_true_binary, y_pred_binary).ravel()
        
        # Calculate additional metrics
        false_positive_rate = fp / (fp + tn) if (fp + tn) > 0 else 0
        false_negative_rate = fn / (fn + tp) if (fn + tp) > 0 else 0
        
        # Store metrics
        self.evaluation_metrics = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'roc_auc': roc_auc,
            'false_positive_rate': false_positive_rate,
            'false_negative_rate': false_negative_rate,
            'true_negatives': tn,
            'false_positives': fp,
            'false_negatives': fn,
            'true_positives': tp
        }
        
        # Print metrics
        print(f"Model Evaluation Metrics:")
        print(f"  Accuracy: {accuracy:.6f} ({accuracy:.2%})")
        print(f"  Precision: {precision:.6f} ({precision:.2%})")
        print(f"  Recall: {recall:.6f} ({recall:.2%})")
        print(f"  F1 Score: {f1:.6f}")
        print(f"  ROC AUC: {roc_auc:.6f}")
        print(f"  False Positive Rate: {false_positive_rate:.6f} ({false_positive_rate:.2%})")
        print(f"  False Negative Rate: {false_negative_rate:.6f} ({false_negative_rate:.2%})")
        
        # Print confusion matrix
        print(f"\nConfusion Matrix:")
        print(f"  True Negatives: {tn}")
        print(f"  False Positives: {fp}")
        print(f"  False Negatives: {fn}")
        print(f"  True Positives: {tp}")
        
        # Save evaluation results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = os.path.join(RESULTS_DIR, f"evaluation_results_{timestamp}.json")
        
        import json
        with open(results_file, 'w') as f:
            json.dump(self.evaluation_metrics, f, indent=2)
        
        print(f"Evaluation results saved to {results_file}")
        
        return self.evaluation_metrics
    
    def save_model(self, model_path=None):
        """
        Save the trained model to disk.
        
        Args:
            model_path (str, optional): Path to save the model
            
        Returns:
            str: Path where the model was saved
        """
        if self.model is None:
            raise ValueError("Model must be trained before saving")
        
        if model_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            model_path = os.path.join(MODEL_DIR, f"extreme_optimized_model_{timestamp}.joblib")
        
        self.model.save_model(model_path)
        
        # Save metadata
        metadata = {
            'training_time': self.training_time,
            'best_params': self.best_params,
            'best_threshold': self.best_threshold,
            'evaluation_metrics': self.evaluation_metrics,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        metadata_path = os.path.splitext(model_path)[0] + "_metadata.json"
        import json
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Model metadata saved to {metadata_path}")
        
        return model_path
    
    def run_full_pipeline(self, num_samples=1000000, anomaly_ratio=0.01, n_trials=100):
        """
        Run the complete extreme optimization pipeline.
        
        Args:
            num_samples (int): Number of data points to generate
            anomaly_ratio (float): Proportion of anomalies in the dataset
            n_trials (int): Number of hyperparameter optimization trials
            
        Returns:
            dict: Evaluation metrics
        """
        print(f"\n{'='*80}\nSTARTING EXTREME OPTIMIZATION PIPELINE\n{'='*80}")
        pipeline_start_time = time.time()
        
        # 1. Generate data
        data, labels = self.generate_data(num_samples, anomaly_ratio)
        
        # 2. Extract features
        data_with_features = self.extract_features(data)
        
        # 3. Select features
        selected_data = self.select_features(data_with_features, labels)
        
        # 4. Split data
        X_train, X_test, y_train, y_test = train_test_split(
            selected_data, labels, test_size=0.2, random_state=self.random_state, stratify=labels
        )
        
        # 5. Optimize hyperparameters
        self.optimize_hyperparameters(X_train, y_train, n_trials)
        
        # 6. Train model
        self.train_model(X_train, y_train)
        
        # 7. Optimize threshold
        self.optimize_threshold(X_test, y_test)
        
        # 8. Evaluate model
        metrics = self.evaluate_model(X_test, y_test)
        
        # 9. Save model
        model_path = self.save_model()
        
        pipeline_time = time.time() - pipeline_start_time
        print(f"\n{'='*80}\nEXTREME OPTIMIZATION PIPELINE COMPLETED\n{'='*80}")
        print(f"Total pipeline execution time: {pipeline_time:.2f} seconds ({pipeline_time/60:.2f} minutes)")
        print(f"Final model saved to: {model_path}")
        print(f"Achieved accuracy: {metrics['accuracy']:.6f} ({metrics['accuracy']:.4%})")
        
        return metrics

# Main execution
if __name__ == "__main__":
    print(f"\n{'='*80}\nSUPPLY CHAIN ANOMALY DETECTION: EXTREME OPTIMIZATION PROTOCOL\n{'='*80}")
    
    # Check if MLX is available
    use_mlx = True
    try:
        import mlx.core as mx
        print("MLX detected - using hardware acceleration on Apple Silicon")
    except ImportError:
        use_mlx = False
        print("MLX not available - falling back to standard processing")
    
    # Create trainer
    trainer = ExtremeOptimizationTrainer(use_mlx=use_mlx)
    
    # Run full pipeline
    # Note: For testing, use smaller values (e.g., num_samples=10000, n_trials=5)
    # For production, use the full values (num_samples=1000000, n_trials=100)
    metrics = trainer.run_full_pipeline(num_samples=10000, anomaly_ratio=0.01, n_trials=5)
    
    print("\nExtreme optimization complete!")