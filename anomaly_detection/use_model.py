import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from anomaly_detection_api import AnomalyDetectionAPI

# Define paths for loading models
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saved_models')
OPTIMIZED_MODEL_PATH = os.path.join(MODEL_DIR, 'optimized_anomaly_detection_model.joblib')
OPTIMIZED_PREPROCESSOR_PATH = os.path.join(MODEL_DIR, 'optimized_data_preprocessor.joblib')
BASE_MODEL_PATH = os.path.join(MODEL_DIR, 'anomaly_detection_model.joblib')
BASE_PREPROCESSOR_PATH = os.path.join(MODEL_DIR, 'data_preprocessor.joblib')


def load_model(optimized=True):
    """
    Load a trained anomaly detection model.
    
    Args:
        optimized (bool): Whether to load the optimized model or the base model.
        
    Returns:
        AnomalyDetectionAPI: The loaded model.
    """
    if optimized and os.path.exists(OPTIMIZED_MODEL_PATH):
        print(f"Loading optimized model from {OPTIMIZED_MODEL_PATH}")
        return AnomalyDetectionAPI.load_model(OPTIMIZED_MODEL_PATH, OPTIMIZED_PREPROCESSOR_PATH)
    elif os.path.exists(BASE_MODEL_PATH):
        print(f"Loading base model from {BASE_MODEL_PATH}")
        return AnomalyDetectionAPI.load_model(BASE_MODEL_PATH, BASE_PREPROCESSOR_PATH)
    else:
        raise FileNotFoundError("No trained model found. Please run train_model.py first.")


def detect_anomalies_in_new_data(api, data):
    """
    Detect anomalies in new supply chain data.
    
    Args:
        api (AnomalyDetectionAPI): The loaded anomaly detection model.
        data (DataFrame): New supply chain data.
        
    Returns:
        tuple: (DataFrame with anomaly predictions, array of anomaly scores)
    """
    # Make predictions
    predictions, scores = api.predict(data)
    
    # Add predictions and scores to the data
    result_data = data.copy()
    result_data['anomaly'] = predictions
    result_data['anomaly_score'] = scores
    
    # Generate explanations for anomalies
    anomalies = result_data[result_data['anomaly'] == -1]
    if len(anomalies) > 0:
        explanations = api.explain_anomalies(data, predictions, scores)
        print(f"\nDetected {len(anomalies)} anomalies in the data.")
        
        # Print explanations for the top 5 anomalies (or fewer if less than 5 were detected)
        print("\nTop anomalies:")
        for i, explanation in enumerate(sorted(explanations, key=lambda x: x['score'], reverse=True)[:5]):
            print(f"Anomaly {i+1}:")
            print(f"  Score: {explanation['score']:.4f}")
            print(f"  Index: {explanation['index']}")
            print(f"  Explanation: {explanation['explanation']}")
            
            # Print key features of the anomalous data point
            data_point = explanation['data_point']
            print("  Key features:")
            for feature in ['order_quantity', 'lead_time', 'transportation_cost', 'inventory_level', 
                           'supplier_reliability', 'quality_rating']:
                if feature in data_point:
                    print(f"    {feature}: {data_point[feature]}")
            print()
    else:
        print("\nNo anomalies detected in the data.")
    
    return result_data, scores


def visualize_anomalies(data, scores):
    """
    Visualize the detected anomalies.
    
    Args:
        data (DataFrame): Data with anomaly predictions.
        scores (array): Anomaly scores.
    """
    # Create a figure with multiple subplots
    fig, axs = plt.subplots(3, 1, figsize=(12, 18))
    
    # Plot 1: Anomaly scores
    axs[0].plot(scores, 'b-', label='Anomaly Scores')
    axs[0].scatter(data[data['anomaly'] == -1].index, 
                  scores[data['anomaly'] == -1], 
                  color='red', label='Anomalies')
    axs[0].set_xlabel('Data Point Index')
    axs[0].set_ylabel('Anomaly Score')
    axs[0].set_title('Anomaly Scores')
    axs[0].legend()
    
    # Plot 2: Order quantity with anomalies highlighted
    if 'order_quantity' in data.columns:
        axs[1].plot(data['order_quantity'], 'g-', label='Order Quantity')
        axs[1].scatter(data[data['anomaly'] == -1].index, 
                      data[data['anomaly'] == -1]['order_quantity'], 
                      color='red', label='Anomalies')
        axs[1].set_xlabel('Data Point Index')
        axs[1].set_ylabel('Order Quantity')
        axs[1].set_title('Order Quantity with Anomalies')
        axs[1].legend()
    
    # Plot 3: Lead time with anomalies highlighted
    if 'lead_time' in data.columns:
        axs[2].plot(data['lead_time'], 'm-', label='Lead Time')
        axs[2].scatter(data[data['anomaly'] == -1].index, 
                      data[data['anomaly'] == -1]['lead_time'], 
                      color='red', label='Anomalies')
        axs[2].set_xlabel('Data Point Index')
        axs[2].set_ylabel('Lead Time')
        axs[2].set_title('Lead Time with Anomalies')
        axs[2].legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(MODEL_DIR, 'anomaly_visualization.png'))
    plt.show()


def main():
    """
    Main function to demonstrate using the trained anomaly detection model.
    """
    print("=== Supply Chain Anomaly Detection Demo ===\n")
    
    try:
        # Load the trained model
        api = load_model(optimized=True)
        print("Model loaded successfully.")
        
        # For demonstration, we'll generate some new synthetic data
        # In a real application, this would be your actual supply chain data
        print("\nGenerating sample supply chain data for demonstration...")
        
        # Import the data generator from train_model.py
        from train_model import SupplyChainDataGenerator
        
        # Generate a small dataset with a higher anomaly ratio for demonstration
        data_generator = SupplyChainDataGenerator(num_samples=1000, anomaly_ratio=0.1)
        data, true_labels = data_generator.generate_dataset()
        
        print(f"Generated {len(data)} sample data points with {np.sum(true_labels == -1)} known anomalies.")
        
        # Detect anomalies in the data
        print("\nDetecting anomalies in the data...")
        result_data, scores = detect_anomalies_in_new_data(api, data)
        
        # Calculate detection accuracy
        accuracy = np.mean(result_data['anomaly'] == true_labels)
        print(f"\nAnomaly detection accuracy: {accuracy:.2%}")
        
        # Visualize the results
        print("\nVisualizing the detected anomalies...")
        visualize_anomalies(result_data, scores)
        
        print(f"\nVisualization saved to {os.path.join(MODEL_DIR, 'anomaly_visualization.png')}")
        print("\nAnomaly detection complete.")
        
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()