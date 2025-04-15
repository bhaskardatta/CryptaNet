# MLX-Optimized Anomaly Detection for Mac Mini M4

This document explains how to use the MLX-optimized version of the Supply Chain Anomaly Detection system specifically designed for Apple Silicon processors, including the Mac Mini M4.

## Overview

The MLX-optimized version leverages Apple's MLX framework to accelerate training and inference on Apple Silicon chips. MLX is a machine learning framework designed specifically for Apple Silicon that provides efficient execution of machine learning models.

## Requirements

- Mac with Apple Silicon (M1, M2, M3, or M4 chip)
- Python 3.8 or higher
- MLX framework

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements_mlx.txt
```

2. Verify MLX installation:

```bash
python -c "import mlx; print(f'MLX version: {mlx.__version__}')"
```

## Using the MLX-Optimized Model

The `train_model_mlx.py` script provides an optimized implementation of the Isolation Forest algorithm using MLX for Apple Silicon processors.

### Running the Training Script

```bash
python train_model_mlx.py
```

The script will:

1. Automatically detect if MLX is available on your system
2. Use MLX-optimized implementation if available, or fall back to sklearn
3. Generate synthetic supply chain data
4. Train a base anomaly detection model with MLX acceleration
5. Evaluate the model's performance
6. If accuracy is below 99%, optimize the model
7. Save the trained model to the `saved_models` directory

## Performance Benefits on Mac Mini M4

The MLX-optimized version offers several advantages on Apple Silicon processors:

1. **Faster Training**: Leverages the M4's Neural Engine and GPU for accelerated matrix operations
2. **Memory Efficiency**: Uses MLX's memory-efficient operations to reduce RAM usage
3. **Batch Processing**: Implements batch processing to efficiently utilize the M4's cores
4. **Quantization Support**: Leverages MLX's native support for quantization to reduce memory usage
5. **Apple Silicon Optimization**: Takes advantage of the unified memory architecture of Apple Silicon

## Implementation Details

The MLX-optimized version includes:

1. **MLXIsolationForest**: A custom implementation of Isolation Forest using MLX
2. **Batch Processing**: Processes data and trees in batches for better performance
3. **Memory Optimization**: Efficiently manages memory to reduce overhead
4. **Performance Monitoring**: Tracks and reports training time improvements

## Comparing Performance

The script will automatically compare the performance of the base and optimized models, reporting:

- Training time for base and optimized models
- Accuracy metrics for both models
- Memory usage during training

## Troubleshooting

If you encounter issues with the MLX-optimized version:

1. **MLX Not Found**: Ensure MLX is properly installed with `pip install mlx`
2. **Memory Issues**: Reduce batch size by modifying the `batch_size` parameter in the script
3. **Performance Not Improved**: Ensure you're running on Apple Silicon; MLX won't provide benefits on Intel processors

## Integration with CryptaNet

The MLX-optimized model is fully compatible with the CryptaNet platform. The saved model can be used with the existing `AnomalyDetectionAPI` class without any modifications to the API interface.

```python
from anomaly_detection.anomaly_detection_api import AnomalyDetectionAPI

# Initialize the API with the MLX-optimized model
api = AnomalyDetectionAPI(model_path='path/to/mlx_optimized_model.joblib')

# Use the API as normal
predictions, scores = api.predict(new_data)
```

## Further Optimization

For even better performance on Mac Mini M4:

1. **Increase Batch Size**: Adjust the batch size based on your M4's memory configuration
2. **Quantization**: Enable quantization for further memory savings
3. **Parallel Processing**: Utilize all available cores for data preprocessing
4. **Model Pruning**: Remove unnecessary tree nodes to reduce model size

## References

- [MLX GitHub Repository](https://github.com/ml-explore/mlx)
- [Apple Developer Documentation](https://developer.apple.com/metal/)
- [Isolation Forest Algorithm](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)