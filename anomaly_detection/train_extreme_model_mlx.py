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
import warnings
warnings.filterwarnings('ignore')

# Try to import MLX, fall back to numpy if not available
try:
    import mlx.core as mx
    import mlx.nn as nn
    import mlx.optimizers as optim
    HAS_MLX = True
    print("MLX detected! Using hardware acceleration for Apple Silicon.")
except ImportError:
    HAS_MLX = False
    print("MLX not found. Using standard NumPy implementation.")

# Import sklearn for isolation forest
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.cluster import DBSCAN
from joblib import Parallel, delayed

# Define paths for saving models and results
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saved_models')
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# MLX-optimized Isolation Forest
class MLXIsolationForest:
    """
    MLX-optimized implementation of Isolation Forest for Apple Silicon.
    """
    def __init__(self, n_estimators=100, max_samples='auto', contamination=0.1, random_state=None):
        self.n_estimators = n_estimators
        self.max_samples = max_samples
        self.contamination = contamination
        self.random_state = random_state
        self.sklearn_model = IsolationForest(
            n_estimators=n_estimators,
            max_samples=max_samples,
            contamination=contamination,
            random_state=random_state,
            n_jobs=-1
        )
        self.is_fitted = False
        
    def fit(self, X):
        # Convert to numpy if it's MLX array
        if HAS_MLX and isinstance(X, mx.array):
            X_np = np.array(X)
        else:
            X_np = X
            
        self.sklearn_model.fit(X_np)
        self.is_fitted = True
        return self
    
    def predict(self, X):
        if not self.is_fitted:
            raise ValueError("Model not fitted yet.")
            
        # Convert to numpy if it's MLX array
        if HAS_MLX and isinstance(X, mx.array):
            X_np = np.array(X)
        else:
            X_np = X
            
        return self.sklearn_model.predict(X_np)
    
    def decision_function(self, X):
        if not self.is_fitted:
            raise ValueError("Model not fitted yet.")
            
        # Convert to numpy if it's MLX array
        if HAS_MLX and isinstance(X, mx.array):
            X_np = np.array(X)
        else:
            X_np = X
            
        return self.sklearn_model.decision_function(X_np)

# MLX-optimized Ensemble Detector
class MLXEnsembleDetector:
    """
    MLX-optimized implementation of Ensemble Detector for Apple Silicon.
    """
    def __init__(self, contamination=0.01, random_state=None, use_mlx=True):
        self.contamination = contamination
        self.random_state = random_state
        self.use_mlx = use_mlx and HAS_MLX
        
        # Initialize base detectors
        self.isolation_forest = MLXIsolationForest(
            n_estimators=100,
            contamination=contamination,
            random_state=random_state
        )
        
        self.one_class_svm = OneClassSVM(
            kernel='rbf',
            gamma='auto',
            nu=contamination
        )
        
        self.dbscan = DBSCAN(
            eps=0.5,
            min_samples=5,
            n_jobs=-1
        )
        
        self.is_fitted = False
        self.feature_importances_ = None
        
    def fit(self, X):
        print("Training MLX-optimized Ensemble Detector...")
        
        # Convert to MLX array if using MLX
        if self.use_mlx:
            try:
                X_mx = mx.array(X)
                print(f"Using MLX acceleration with array shape: {X_mx.shape}")
            except Exception as e:
                print(f"Error converting to MLX array: {e}")
                print("Falling back to NumPy implementation")
                self.use_mlx = False
                X_mx = X
        else:
            X_mx = X
        
        # Train base detectors
        print("Training Isolation Forest...")
        self.isolation_forest.fit(X_mx)
        
        print("Training One-Class SVM...")
        self.one_class_svm.fit(X)
        
        print("Training DBSCAN...")
        self.dbscan.fit(X)
        
        self.is_fitted = True
        return self
    
    def predict(self, X):
        if not self.is_fitted:
            raise ValueError("Model not fitted yet.")
        
        # Convert to MLX array if using MLX
        if self.use_mlx:
            try:
                X_mx = mx.array(X)
            except:
                self.use_mlx = False
                X_mx = X
        else:
            X_mx = X
        
        # Get predictions from base detectors
        if_pred = self.isolation_forest.predict(X_mx)
        svm_pred = self.one_class_svm.predict(X)
        
        # For DBSCAN, convert cluster labels to binary predictions
        dbscan_labels = self.dbscan.fit_predict(X)
        dbscan_pred = np.where(dbscan_labels == -1, -1, 1)
        
        # Ensemble predictions (majority voting)
        ensemble_pred = np.zeros(X.shape[0])
        for i in range(X.shape[0]):
            votes = [if_pred[i], svm_pred[i], dbscan_pred[i]]
            if votes.count(-1) >= 2:  # If at least 2 detectors say it's an anomaly
                ensemble_pred[i] = -1
            else:
                ensemble_pred[i] = 1
        
        return ensemble_pred
    
    def decision_function(self, X):
        if not self.is_fitted:
            raise ValueError("Model not fitted yet.")
        
        # Convert to MLX array if using MLX
        if self.use_mlx:
            try:
                X_mx = mx.array(X)
            except:
                self.use_mlx = False
                X_mx = X
        else:
            X_mx = X
        
        # Get decision scores from base detectors
        if_scores = self.isolation_forest.decision_function(X_mx)
        
        # For SVM, we need to negate the scores to match the convention
        # (more negative = more anomalous)
        try:
            svm_scores = -self.one_class_svm.decision_function(X)
        except:
            svm_scores = np.zeros(X.shape[0])
        
        # For DBSCAN, we don't have decision scores, so we'll use a proxy
        # based on the distance to the nearest core point
        dbscan_labels = self.dbscan.fit_predict(X)
        dbscan_scores = np.zeros(X.shape[0])
        for i in range(X.shape[0]):
            if dbscan_labels[i] == -1:  # If it's an outlier
                dbscan_scores[i] = -1  # Assign a negative score
        
        # Combine scores (average)
        ensemble_scores = (if_scores + svm_scores + dbscan_scores) / 3
        
        return ensemble_scores
    
    def save_model(self, filepath):
        joblib.dump(self, filepath)
        print(f"Model saved to {filepath}")
    
    @classmethod
    def load_model(cls, filepath):
        return joblib.load(filepath)

# Simple data generator for supply chain data
class SupplyChainDataGenerator:
    def __init__(self, num_samples=100000, anomaly_ratio=0.01, random_state=42):
        self.num_samples = num_samples
        self.anomaly_ratio = anomaly_ratio
        self.random_state = random_state
        np.random.seed(random_state)
    
    def generate_dataset(self):
        print(f"Generating {self.num_samples} supply chain data samples...")
        
        # Number of normal and anomalous samples
        n_normal = int(self.num_samples * (1 - self.anomaly_ratio))
        n_anomalies = self.num_samples - n_normal
        
        # Generate normal data
        normal_data = {
            'order_quantity': np.random.normal(500, 100, n_normal),
            'lead_time': np.random.normal(14, 3, n_normal),
            'price': np.random.normal(100, 20, n_normal),
            'shipping_cost': np.random.normal(50, 10, n_normal),
            'product_quality': np.random.normal(0.9, 0.05, n_normal),
            'supplier_reliability': np.random.normal(0.85, 0.1, n_normal),
            'demand_volatility': np.random.normal(0.2, 0.05, n_normal),
            'inventory_level': np.random.normal(1000, 200, n_normal),
            'production_efficiency': np.random.normal(0.8, 0.1, n_normal),
            'delivery_performance': np.random.normal(0.9, 0.05, n_normal)
        }
        
        # Generate anomalous data with extreme values
        anomaly_data = {
            'order_quantity': np.random.choice([np.random.normal(50, 20), np.random.normal(1500, 300)], n_anomalies),
            'lead_time': np.random.choice([np.random.normal(2, 1), np.random.normal(45, 10)], n_anomalies),
            'price': np.random.choice([np.random.normal(10, 5), np.random.normal(500, 100)], n_anomalies),
            'shipping_cost': np.random.choice([np.random.normal(5, 2), np.random.normal(200, 50)], n_anomalies),
            'product_quality': np.random.choice([np.random.normal(0.2, 0.1), np.random.normal(0.99, 0.01)], n_anomalies),
            'supplier_reliability': np.random.choice([np.random.normal(0.2, 0.1), np.random.normal(0.99, 0.01)], n_anomalies),
            'demand_volatility': np.random.choice([np.random.normal(0.01, 0.005), np.random.normal(0.8, 0.1)], n_anomalies),
            'inventory_level': np.random.choice([np.random.normal(50, 20), np.random.normal(5000, 1000)], n_anomalies),
            'production_efficiency': np.random.choice([np.random.normal(0.2, 0.1), np.random.normal(0.99, 0.01)], n_anomalies),
            'delivery_performance': np.random.choice([np.random.normal(0.2, 0.1), np.random.normal(0.99, 0.01)], n_anomalies)
        }
        
        # Create DataFrames
        normal_df = pd.DataFrame(normal_data)
        anomaly_df = pd.DataFrame(anomaly_data)
        
        # Add labels (-1 for anomalies, 1 for normal)
        normal_df['label'] = 1
        anomaly_df['label'] = -1
        
        # Combine datasets
        combined_df = pd.concat([normal_df, anomaly_df], ignore_index=True)
        
        # Shuffle the data
        combined_df = combined_df.sample(frac=1, random_state=self.random_state).reset_index(drop=True)
        
        # Extract features and labels
        X = combined_df.drop('label', axis=1)
        y = combined_df['label']
        
        print(f"Generated {len(X)} samples with {(y == -1).sum()} anomalies ({(y == -1).mean():.2%})")
        
        return X, y

# Main function to train and evaluate the model
def train_and_evaluate(num_samples=1000000, anomaly_ratio=0.01, use_mlx=True, random_state=42):
    print(f"\n{'='*80}\nMLX-OPTIMIZED EXTREME ANOMALY DETECTION\n{'='*80}")
    print(f"Starting training with {num_samples:,} samples and {anomaly_ratio:.1%} anomaly ratio")
    print(f"MLX acceleration: {'Enabled' if use_mlx and HAS_MLX else 'Disabled'}")
    
    # Use enhanced data generator
    from enhanced_data_generator import EnhancedSupplyChainDataGenerator
    data_generator = EnhancedSupplyChainDataGenerator(
        num_samples=num_samples,
        anomaly_ratio=anomaly_ratio,
        random_state=random_state,
        n_jobs=-1
    )
    data, labels = data_generator.generate_normal_data(), None
    data, labels = data_generator.inject_anomalies(data)

    # Drop timestamp and categorical columns for modeling
    drop_cols = ['timestamp', 'supplier', 'product_category', 'shipping_method', 'region']
    X = data.drop(columns=[col for col in drop_cols if col in data.columns])
    y = labels

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state, stratify=y
    )

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train model
    start_time = time.time()
    model = MLXEnsembleDetector(
        contamination=anomaly_ratio,
        random_state=random_state,
        use_mlx=use_mlx
    )
    model.fit(X_train_scaled)
    training_time = time.time() - start_time
    print(f"Training completed in {training_time:.2f} seconds")

    # Make predictions
    y_pred = model.predict(X_test_scaled)

    # Calculate metrics
    accuracy = np.mean(y_pred == y_test)
    precision = np.sum((y_pred == -1) & (y_test == -1)) / np.sum(y_pred == -1) if np.sum(y_pred == -1) > 0 else 0
    recall = np.sum((y_pred == -1) & (y_test == -1)) / np.sum(y_test == -1) if np.sum(y_test == -1) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    print(f"\n{'='*80}\nPERFORMANCE METRICS\n{'='*80}")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")

    # Save model
    model_path = os.path.join(MODEL_DIR, 'extreme_optimized_model_mlx.joblib')
    model.save_model(model_path)

    # Plot confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.colorbar()
    plt.xticks([0, 1], ['Anomaly (-1)', 'Normal (1)'])
    plt.yticks([0, 1], ['Anomaly (-1)', 'Normal (1)'])
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    thresh = cm.max() / 2
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, format(cm[i, j], 'd'),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()
    plt.savefig(os.path.join(MODEL_DIR, 'confusion_matrix.png'))

    # Plot ROC curve
    decision_scores = model.decision_function(X_test_scaled)
    min_score = np.min(decision_scores)
    max_score = np.max(decision_scores)
    normalized_scores = (decision_scores - min_score) / (max_score - min_score)
    from sklearn.metrics import roc_curve, auc, precision_recall_curve
    fpr, tpr, _ = roc_curve(y_test == -1, -normalized_scores)
    roc_auc = auc(fpr, tpr)
    plt.figure(figsize=(10, 8))
    plt.plot(fpr, tpr, color='orange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.savefig(os.path.join(MODEL_DIR, 'roc_curve.png'))

    # Calculate precision-recall curve
    precision_curve, recall_curve, _ = precision_recall_curve(y_test == -1, -normalized_scores)
    pr_auc = auc(recall_curve, precision_curve)
    plt.figure(figsize=(8, 6))
    plt.plot(recall_curve, precision_curve, lw=2, label=f'PR curve (area = {pr_auc:.2f})')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.legend(loc="lower left")
    plt.grid(True)
    plt.savefig(os.path.join(MODEL_DIR, 'pr_curve.png'))

    # Plot anomaly scores
    plt.figure(figsize=(10, 6))
    plt.hist(decision_scores[y_test == 1], bins=50, alpha=0.5, label='Normal')
    plt.hist(decision_scores[y_test == -1], bins=50, alpha=0.5, label='Anomaly')
    plt.xlabel('Anomaly Score')
    plt.ylabel('Count')
    plt.title('Distribution of Anomaly Scores')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(MODEL_DIR, 'anomaly_scores.png'))

    print(f"\nModel saved to {model_path}")
    print(f"Plots saved to {MODEL_DIR}")

    return model, accuracy, precision, recall, f1

# Main execution
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Train MLX-optimized extreme anomaly detection model')
    parser.add_argument('--num_samples', type=int, default=100000, help='Number of samples to generate')
    parser.add_argument('--anomaly_ratio', type=float, default=0.01, help='Ratio of anomalies in the dataset')
    parser.add_argument('--use_mlx', type=bool, default=True, help='Whether to use MLX acceleration')
    parser.add_argument('--random_state', type=int, default=42, help='Random seed for reproducibility')
    
    args = parser.parse_args()
    
    train_and_evaluate(
        num_samples=args.num_samples,
        anomaly_ratio=args.anomaly_ratio,
        use_mlx=args.use_mlx,
        random_state=args.random_state
    )