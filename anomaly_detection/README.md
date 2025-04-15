# Supply Chain Anomaly Detection System

This module implements a machine learning-based anomaly detection system for supply chain data. It uses the Isolation Forest algorithm to identify unusual patterns and anomalies in supply chain metrics.

## Overview

The anomaly detection system consists of the following components:

1. **Data Preprocessing**: Handles cleaning, transforming, and normalizing supply chain data
2. **Feature Engineering**: Extracts and transforms supply chain-specific features
3. **Anomaly Detection Model**: Implements the Isolation Forest algorithm for detecting anomalies
4. **Model Evaluation**: Provides metrics and visualizations to evaluate model performance

## Data Requirements

The system works with supply chain data that includes the following types of features:

### Required Features

- **Numerical Features**: Order quantities, lead times, costs, inventory levels, etc.
- **Timestamp Column**: For time-based feature extraction

### Optional Features

- **Categorical Features**: Suppliers, product categories, shipping methods, etc.

### Example Data Format

```
timestamp,order_quantity,lead_time,transportation_cost,inventory_level,supplier_reliability,demand_forecast,product_category,supplier
2022-01-01,500,14,1000,5000,0.95,450,Electronics,SupplierA
2022-01-02,520,13,1050,4800,0.96,460,Electronics,SupplierB
...
```

## Training the Model

The `train_model.py` script provides a complete pipeline for training the anomaly detection model:

1. **Data Generation**: Creates synthetic supply chain data with realistic patterns and injected anomalies
2. **Data Preprocessing**: Cleans and normalizes the data
3. **Feature Engineering**: Extracts supply chain-specific features
4. **Model Training**: Trains the Isolation Forest model
5. **Model Evaluation**: Evaluates the model's performance
6. **Model Optimization**: Optimizes the model to achieve high accuracy (targeting 99%)

### Running the Training Script

```bash
python train_model.py
```

The script will:

1. Generate synthetic supply chain data
2. Train a base anomaly detection model
3. Evaluate the model's performance
4. If accuracy is below 99%, optimize the model
5. Save the trained model to the `saved_models` directory

## Using the Model

The `use_model.py` script demonstrates how to use the trained model for anomaly detection:

```bash
python use_model.py
```

This script will:

1. Load the trained model
2. Generate sample supply chain data
3. Detect anomalies in the data
4. Explain the detected anomalies
5. Visualize the results

## Achieving 99% Accuracy

To achieve 99% accuracy in anomaly detection, the system implements several optimization strategies:

1. **Enhanced Feature Engineering**: Extracts domain-specific features from supply chain data
2. **Optimized Model Parameters**: Uses a higher number of estimators and adjusted contamination parameter
3. **Threshold Optimization**: Finds the optimal threshold for anomaly detection using F1-score optimization
4. **Comprehensive Evaluation**: Uses multiple metrics to ensure high accuracy

### Key Factors for High Accuracy

- **Data Quality**: Ensure your supply chain data is clean and contains relevant features
- **Feature Selection**: Include all relevant supply chain metrics
- **Parameter Tuning**: Adjust the model parameters based on your specific data characteristics
- **Threshold Selection**: Use the optimal threshold for your specific use case

## Integration with CryptaNet

This anomaly detection system is designed to integrate seamlessly with the CryptaNet platform:

1. Import the `AnomalyDetectionAPI` class from the module
2. Initialize the API with your trained model
3. Use the API to detect anomalies in your supply chain data

```python
from anomaly_detection.anomaly_detection_api import AnomalyDetectionAPI

# Initialize the API with a trained model
api = AnomalyDetectionAPI(model_path='path/to/model.joblib')

# Detect anomalies in new data
predictions, scores = api.predict(new_data)

# Explain the detected anomalies
explanations = api.explain_anomalies(new_data, predictions, scores)
```

## Customization

The system can be customized for specific supply chain scenarios:

1. **Custom Features**: Modify the `FeatureExtractor` class to extract domain-specific features
2. **Model Parameters**: Adjust the Isolation Forest parameters in the `AnomalyDetector` class
3. **Evaluation Metrics**: Customize the evaluation metrics in the `ModelEvaluator` class

## Troubleshooting

If you encounter issues with the anomaly detection system:

1. **Low Accuracy**: Try increasing the number of estimators or adjusting the contamination parameter
2. **False Positives**: Adjust the threshold for anomaly detection
3. **Missing Features**: Ensure all required features are present in your data
4. **Model Not Loading**: Check that the model file exists and is accessible