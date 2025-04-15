import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Define path for saving generated data
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

class SupplyChainDataGenerator:
    """
    Generates synthetic supply chain data for anomaly detection model training.
    
    This class creates realistic supply chain data with normal patterns and injected anomalies
    to train and evaluate the anomaly detection model.
    """
    
    def __init__(self, num_samples=10000, anomaly_ratio=0.05, random_state=42):
        """
        Initialize the data generator.
        
        Args:
            num_samples (int): Number of data points to generate
            anomaly_ratio (float): Proportion of anomalies in the dataset
            random_state (int): Random seed for reproducibility
        """
        self.num_samples = num_samples
        self.anomaly_ratio = anomaly_ratio
        self.random_state = random_state
        np.random.seed(random_state)
    
    def generate_timestamps(self, start_date='2022-01-01', end_date='2022-12-31'):
        """
        Generate random timestamps within a date range.
        
        Args:
            start_date (str): Start date in 'YYYY-MM-DD' format
            end_date (str): End date in 'YYYY-MM-DD' format
            
        Returns:
            array: Array of timestamps
        """
        start_ts = pd.Timestamp(start_date).timestamp()
        end_ts = pd.Timestamp(end_date).timestamp()
        
        # Generate random timestamps
        timestamps = np.random.uniform(start_ts, end_ts, self.num_samples)
        return pd.to_datetime(timestamps, unit='s')
    
    def generate_normal_data(self):
        """
        Generate normal supply chain data.
        
        Returns:
            DataFrame: DataFrame containing normal supply chain data
        """
        # Generate timestamps
        timestamps = self.generate_timestamps()
        
        # Sort timestamps
        timestamps = sorted(timestamps)
        
        # Generate normal data
        data = pd.DataFrame({
            'timestamp': timestamps,
            'order_quantity': np.random.normal(500, 50, self.num_samples),
            'lead_time': np.random.normal(14, 2, self.num_samples),
            'transportation_cost': np.random.normal(1000, 100, self.num_samples),
            'inventory_level': np.random.normal(5000, 500, self.num_samples),
            'supplier_reliability': np.random.normal(0.95, 0.02, self.num_samples).clip(0, 1),
            'demand_forecast': np.random.normal(450, 40, self.num_samples),
            'production_capacity': np.random.normal(600, 50, self.num_samples),
            'quality_rating': np.random.normal(0.92, 0.03, self.num_samples).clip(0, 1),
        })
        
        # Add some categorical features
        suppliers = ['SupplierA', 'SupplierB', 'SupplierC', 'SupplierD']
        product_categories = ['Electronics', 'Clothing', 'Food', 'Furniture', 'Toys']
        shipping_methods = ['Air', 'Sea', 'Road', 'Rail']
        
        data['supplier'] = np.random.choice(suppliers, self.num_samples)
        data['product_category'] = np.random.choice(product_categories, self.num_samples)
        data['shipping_method'] = np.random.choice(shipping_methods, self.num_samples)
        
        # Add seasonal patterns
        data['month'] = data['timestamp'].dt.month
        # Increase demand during holiday seasons (months 11-12)
        holiday_mask = data['month'].isin([11, 12])
        data.loc[holiday_mask, 'order_quantity'] *= np.random.uniform(1.2, 1.5, holiday_mask.sum())
        data.loc[holiday_mask, 'demand_forecast'] *= np.random.uniform(1.2, 1.5, holiday_mask.sum())
        
        # Add supply chain relationships
        # 1. Order quantity affects inventory level
        data['inventory_level'] = data['inventory_level'] - data['order_quantity'] + np.random.normal(500, 50, self.num_samples)
        
        # 2. Supplier reliability affects lead time
        data['lead_time'] = data['lead_time'] * (2 - data['supplier_reliability'])
        
        # 3. Shipping method affects transportation cost
        for method, factor in zip(['Air', 'Sea', 'Road', 'Rail'], [1.5, 0.8, 1.0, 0.9]):
            data.loc[data['shipping_method'] == method, 'transportation_cost'] *= factor
        
        return data
    
    def inject_anomalies(self, data):
        """
        Inject anomalies into the supply chain data.
        
        Args:
            data (DataFrame): Normal supply chain data
            
        Returns:
            tuple: (DataFrame with anomalies, array of anomaly labels)
        """
        # Make a copy of the data
        data_with_anomalies = data.copy()
        
        # Calculate number of anomalies
        num_anomalies = int(self.num_samples * self.anomaly_ratio)
        
        # Generate random indices for anomalies
        anomaly_indices = np.random.choice(self.num_samples, num_anomalies, replace=False)
        
        # Create anomaly labels (1 for normal, -1 for anomaly)
        labels = np.ones(self.num_samples)
        labels[anomaly_indices] = -1
        
        # Inject different types of anomalies
        for idx in anomaly_indices:
            anomaly_type = np.random.choice(['quantity_spike', 'lead_time_delay', 'cost_anomaly', 
                                           'inventory_shortage', 'quality_issue', 'forecast_error',
                                           'capacity_drop', 'multi_metric_anomaly'])
            
            if anomaly_type == 'quantity_spike':
                # Sudden spike in order quantity
                data_with_anomalies.loc[idx, 'order_quantity'] *= np.random.uniform(3, 5)
                
            elif anomaly_type == 'lead_time_delay':
                # Significant delay in lead time
                data_with_anomalies.loc[idx, 'lead_time'] *= np.random.uniform(2, 4)
                
            elif anomaly_type == 'cost_anomaly':
                # Unusual transportation cost
                data_with_anomalies.loc[idx, 'transportation_cost'] *= np.random.uniform(2, 3)
                
            elif anomaly_type == 'inventory_shortage':
                # Critical inventory shortage
                data_with_anomalies.loc[idx, 'inventory_level'] *= np.random.uniform(0.1, 0.3)
                
            elif anomaly_type == 'quality_issue':
                # Severe quality issues
                data_with_anomalies.loc[idx, 'quality_rating'] *= np.random.uniform(0.3, 0.6)
                
            elif anomaly_type == 'forecast_error':
                # Large forecast error
                data_with_anomalies.loc[idx, 'demand_forecast'] *= np.random.uniform(0.2, 0.4)
                # Or extremely high forecast
                if np.random.random() > 0.5:
                    data_with_anomalies.loc[idx, 'demand_forecast'] *= np.random.uniform(2.5, 4)
            
            elif anomaly_type == 'capacity_drop':
                # Sudden drop in production capacity
                data_with_anomalies.loc[idx, 'production_capacity'] *= np.random.uniform(0.3, 0.5)
            
            elif anomaly_type == 'multi_metric_anomaly':
                # Anomaly affecting multiple metrics simultaneously
                data_with_anomalies.loc[idx, 'lead_time'] *= np.random.uniform(1.5, 2.5)
                data_with_anomalies.loc[idx, 'transportation_cost'] *= np.random.uniform(1.5, 2.0)
                data_with_anomalies.loc[idx, 'quality_rating'] *= np.random.uniform(0.6, 0.8)
        
        return data_with_anomalies, labels
    
    def generate_dataset(self):
        """
        Generate a complete dataset with normal and anomalous data points.
        
        Returns:
            tuple: (DataFrame with data, array of labels)
        """
        # Generate normal data
        normal_data = self.generate_normal_data()
        
        # Inject anomalies
        data_with_anomalies, labels = self.inject_anomalies(normal_data)
        
        return data_with_anomalies, labels
    
    def visualize_data(self, data, labels=None):
        """
        Visualize the generated data.
        
        Args:
            data (DataFrame): The generated data
            labels (array, optional): Anomaly labels (1 for normal, -1 for anomaly)
        """
        # Create a figure with multiple subplots
        fig, axs = plt.subplots(3, 2, figsize=(15, 15))
        
        # Plot distributions of key numerical features
        features = ['order_quantity', 'lead_time', 'transportation_cost', 
                   'inventory_level', 'supplier_reliability', 'quality_rating']
        
        for i, feature in enumerate(features):
            row, col = i // 2, i % 2
            if labels is not None:
                # Plot normal and anomalous points separately
                sns.histplot(data[labels == 1][feature], ax=axs[row, col], color='blue', alpha=0.5, label='Normal')
                sns.histplot(data[labels == -1][feature], ax=axs[row, col], color='red', alpha=0.5, label='Anomaly')
                axs[row, col].legend()
            else:
                sns.histplot(data[feature], ax=axs[row, col], color='blue')
            
            axs[row, col].set_title(f'Distribution of {feature}')
        
        plt.tight_layout()
        return fig
    
    def save_dataset(self, data, labels, filename='supply_chain_data.csv'):
        """
        Save the generated dataset to a CSV file.
        
        Args:
            data (DataFrame): The generated data
            labels (array): Anomaly labels (1 for normal, -1 for anomaly)
            filename (str): Name of the output file
        """
        # Add labels to the data
        output_data = data.copy()
        output_data['anomaly_label'] = labels
        
        # Save to CSV
        output_path = os.path.join(DATA_DIR, filename)
        output_data.to_csv(output_path, index=False)
        print(f"Dataset saved to {output_path}")
        
        return output_path


def generate_multiple_datasets():
    """
    Generate multiple datasets with different characteristics for training and testing.
    """
    # Dataset 1: Standard supply chain data (10,000 samples, 5% anomalies)
    print("Generating standard supply chain dataset...")
    generator1 = SupplyChainDataGenerator(num_samples=10000, anomaly_ratio=0.05)
    data1, labels1 = generator1.generate_dataset()
    generator1.save_dataset(data1, labels1, 'standard_supply_chain_data.csv')
    
    # Dataset 2: High anomaly ratio for testing (5,000 samples, 10% anomalies)
    print("\nGenerating high-anomaly test dataset...")
    generator2 = SupplyChainDataGenerator(num_samples=5000, anomaly_ratio=0.10)
    data2, labels2 = generator2.generate_dataset()
    generator2.save_dataset(data2, labels2, 'high_anomaly_test_data.csv')
    
    # Dataset 3: Seasonal patterns with anomalies (12,000 samples, 5% anomalies)
    print("\nGenerating seasonal pattern dataset...")
    generator3 = SupplyChainDataGenerator(num_samples=12000, anomaly_ratio=0.05)
    # Generate data with stronger seasonal patterns
    data3 = generator3.generate_normal_data()
    # Enhance seasonal patterns
    for month in range(1, 13):
        month_mask = data3['month'] == month
        # Add seasonal variations to order quantity
        if month in [11, 12]:  # Holiday season
            data3.loc[month_mask, 'order_quantity'] *= 1.5
            data3.loc[month_mask, 'demand_forecast'] *= 1.4
        elif month in [6, 7, 8]:  # Summer season
            data3.loc[month_mask, 'order_quantity'] *= 1.2
            data3.loc[month_mask, 'demand_forecast'] *= 1.15
        elif month in [1, 2]:  # Post-holiday slump
            data3.loc[month_mask, 'order_quantity'] *= 0.8
            data3.loc[month_mask, 'demand_forecast'] *= 0.85
    
    # Inject anomalies
    data3, labels3 = generator3.inject_anomalies(data3)
    generator3.save_dataset(data3, labels3, 'seasonal_supply_chain_data.csv')
    
    print("\nAll datasets generated successfully.")
    
    # Visualize one of the datasets
    print("\nVisualizing the standard dataset...")
    fig = generator1.visualize_data(data1, labels1)
    plt.savefig(os.path.join(DATA_DIR, 'data_visualization.png'))
    print(f"Visualization saved to {os.path.join(DATA_DIR, 'data_visualization.png')}")


def main():
    """
    Main function to generate supply chain data for anomaly detection.
    """
    print("=== Supply Chain Data Generation for Anomaly Detection ===\n")
    
    # Generate multiple datasets
    generate_multiple_datasets()
    
    print("\nData generation complete.")
    print(f"All datasets saved to {DATA_DIR}")


if __name__ == "__main__":
    main()