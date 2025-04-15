import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from scipy import stats
from sklearn.preprocessing import StandardScaler
from joblib import Parallel, delayed

# Define path for saving generated data
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

class EnhancedSupplyChainDataGenerator:
    """
    Generates massive synthetic supply chain data for ultra-high-precision anomaly detection.
    
    This class creates 1,000,000+ realistic supply chain samples with advanced time-series
    augmentation to simulate seasonal fluctuations, black swan events, and market disruptions.
    It also creates specialized subsets with varying anomaly ratios for sensitivity testing.
    """
    
    def __init__(self, num_samples=1000000, anomaly_ratio=0.01, random_state=42, n_jobs=-1):
        """
        Initialize the enhanced data generator.
        
        Args:
            num_samples (int): Number of data points to generate (default: 1,000,000)
            anomaly_ratio (float): Proportion of anomalies in the dataset (default: 0.01)
            random_state (int): Random seed for reproducibility
            n_jobs (int): Number of parallel jobs for data generation (-1 uses all cores)
        """
        self.num_samples = num_samples
        self.anomaly_ratio = anomaly_ratio
        self.random_state = random_state
        self.n_jobs = n_jobs
        np.random.seed(random_state)
        
        # Define suppliers with different reliability profiles
        self.suppliers = {
            'SupplierA': {'reliability_mean': 0.95, 'reliability_std': 0.02, 'lead_time_mean': 12, 'lead_time_std': 1.5},
            'SupplierB': {'reliability_mean': 0.92, 'reliability_std': 0.03, 'lead_time_mean': 14, 'lead_time_std': 2.0},
            'SupplierC': {'reliability_mean': 0.98, 'reliability_std': 0.01, 'lead_time_mean': 10, 'lead_time_std': 1.0},
            'SupplierD': {'reliability_mean': 0.88, 'reliability_std': 0.04, 'lead_time_mean': 16, 'lead_time_std': 2.5},
            'SupplierE': {'reliability_mean': 0.90, 'reliability_std': 0.03, 'lead_time_mean': 15, 'lead_time_std': 2.2},
            'SupplierF': {'reliability_mean': 0.93, 'reliability_std': 0.02, 'lead_time_mean': 13, 'lead_time_std': 1.8},
            'SupplierG': {'reliability_mean': 0.97, 'reliability_std': 0.01, 'lead_time_mean': 11, 'lead_time_std': 1.2},
            'SupplierH': {'reliability_mean': 0.89, 'reliability_std': 0.03, 'lead_time_mean': 15, 'lead_time_std': 2.3},
        }
        
        # Define product categories with different characteristics
        self.product_categories = {
            'Electronics': {'order_qty_mean': 500, 'order_qty_std': 50, 'cost_factor': 1.5, 'seasonal_impact': 0.3},
            'Clothing': {'order_qty_mean': 800, 'order_qty_std': 80, 'cost_factor': 1.0, 'seasonal_impact': 0.5},
            'Food': {'order_qty_mean': 1200, 'order_qty_std': 120, 'cost_factor': 0.8, 'seasonal_impact': 0.2},
            'Furniture': {'order_qty_mean': 300, 'order_qty_std': 30, 'cost_factor': 1.2, 'seasonal_impact': 0.4},
            'Toys': {'order_qty_mean': 600, 'order_qty_std': 60, 'cost_factor': 0.9, 'seasonal_impact': 0.6},
            'Pharmaceuticals': {'order_qty_mean': 400, 'order_qty_std': 40, 'cost_factor': 1.8, 'seasonal_impact': 0.1},
            'Automotive': {'order_qty_mean': 250, 'order_qty_std': 25, 'cost_factor': 1.6, 'seasonal_impact': 0.3},
            'Home Goods': {'order_qty_mean': 700, 'order_qty_std': 70, 'cost_factor': 1.1, 'seasonal_impact': 0.4},
        }
        
        # Define shipping methods with different characteristics
        self.shipping_methods = {
            'Air': {'cost_factor': 1.8, 'lead_time_factor': 0.6, 'reliability_factor': 1.2},
            'Sea': {'cost_factor': 0.7, 'lead_time_factor': 1.5, 'reliability_factor': 0.9},
            'Road': {'cost_factor': 1.0, 'lead_time_factor': 1.0, 'reliability_factor': 1.0},
            'Rail': {'cost_factor': 0.8, 'lead_time_factor': 1.2, 'reliability_factor': 1.1},
            'Express': {'cost_factor': 2.0, 'lead_time_factor': 0.5, 'reliability_factor': 1.3},
        }
        
        # Define regions with different characteristics
        self.regions = {
            'North America': {'demand_factor': 1.2, 'cost_factor': 1.1, 'lead_time_factor': 0.9},
            'Europe': {'demand_factor': 1.1, 'cost_factor': 1.2, 'lead_time_factor': 1.0},
            'Asia': {'demand_factor': 1.3, 'cost_factor': 0.8, 'lead_time_factor': 1.1},
            'South America': {'demand_factor': 0.9, 'cost_factor': 0.9, 'lead_time_factor': 1.2},
            'Africa': {'demand_factor': 0.8, 'cost_factor': 0.7, 'lead_time_factor': 1.3},
            'Australia': {'demand_factor': 1.0, 'cost_factor': 1.3, 'lead_time_factor': 1.1},
        }
        
        # Define market events for simulation
        self.market_events = [
            {'name': 'Global Pandemic', 'probability': 0.001, 'impact': {
                'order_quantity': 0.5, 'lead_time': 2.0, 'transportation_cost': 1.5, 'inventory_level': 0.7,
                'supplier_reliability': 0.8, 'demand_forecast': 0.6, 'production_capacity': 0.7
            }},
            {'name': 'Trade War', 'probability': 0.002, 'impact': {
                'order_quantity': 0.8, 'lead_time': 1.3, 'transportation_cost': 1.3, 'inventory_level': 0.9,
                'supplier_reliability': 0.9, 'demand_forecast': 0.8, 'production_capacity': 0.9
            }},
            {'name': 'Natural Disaster', 'probability': 0.003, 'impact': {
                'order_quantity': 0.7, 'lead_time': 1.5, 'transportation_cost': 1.4, 'inventory_level': 0.8,
                'supplier_reliability': 0.7, 'demand_forecast': 0.7, 'production_capacity': 0.6
            }},
            {'name': 'Fuel Price Spike', 'probability': 0.005, 'impact': {
                'order_quantity': 0.9, 'lead_time': 1.1, 'transportation_cost': 1.8, 'inventory_level': 0.95,
                'supplier_reliability': 0.95, 'demand_forecast': 0.9, 'production_capacity': 0.95
            }},
            {'name': 'Labor Strike', 'probability': 0.004, 'impact': {
                'order_quantity': 0.85, 'lead_time': 1.4, 'transportation_cost': 1.2, 'inventory_level': 0.9,
                'supplier_reliability': 0.8, 'demand_forecast': 0.85, 'production_capacity': 0.7
            }},
        ]
    
    def generate_timestamps(self, start_date='2020-01-01', end_date='2023-12-31'):
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
    
    def generate_seasonal_pattern(self, timestamps, base_value, amplitude, period=365, phase=0):
        """
        Generate seasonal pattern based on timestamps.
        
        Args:
            timestamps (array): Array of timestamps
            base_value (float): Base value
            amplitude (float): Amplitude of the seasonal pattern
            period (int): Period in days
            phase (float): Phase shift
            
        Returns:
            array: Seasonal pattern values
        """
        # Convert timestamps to days since epoch
        days = (timestamps - pd.Timestamp('1970-01-01')) / pd.Timedelta('1D')
        
        # Generate seasonal pattern
        seasonal = base_value + amplitude * np.sin(2 * np.pi * (days / period + phase))
        
        return seasonal
    
    def generate_trend_pattern(self, timestamps, base_value, slope):
        """
        Generate trend pattern based on timestamps.
        
        Args:
            timestamps (array): Array of timestamps
            base_value (float): Base value
            slope (float): Slope of the trend
            
        Returns:
            array: Trend pattern values
        """
        # Convert timestamps to days since start
        days = (timestamps - timestamps.min()) / pd.Timedelta('1D')
        
        # Generate trend pattern
        trend = base_value + slope * days
        
        return trend
    
    def apply_market_events(self, data, timestamps):
        """
        Apply random market events to the data.
        
        Args:
            data (DataFrame): The data to apply events to
            timestamps (array): Array of timestamps
            
        Returns:
            DataFrame: Data with market events applied
        """
        result = data.copy()
        
        # Sort data by timestamp
        result = result.sort_values('timestamp')
        
        # Determine event occurrences
        for event in self.market_events:
            # Determine if and when the event occurs
            if np.random.random() < event['probability'] * 10:  # Increase probability for testing
                # Select a random date for the event
                event_date = np.random.choice(timestamps)
                event_duration = np.random.randint(30, 180)  # Event lasts 1-6 months
                
                # Find data points within the event period
                event_mask = (result['timestamp'] >= event_date) & \
                             (result['timestamp'] <= event_date + pd.Timedelta(days=event_duration))
                
                # Apply event impact to affected data points
                for feature, impact in event['impact'].items():
                    if feature in result.columns:
                        if impact < 1:  # Decrease
                            result.loc[event_mask, feature] *= impact
                        else:  # Increase
                            result.loc[event_mask, feature] *= impact
                
                print(f"Applied market event '{event['name']}' from {event_date.date()} for {event_duration} days")
        
        return result
    
    def generate_batch(self, batch_size, batch_index):
        """
        Generate a batch of normal supply chain data.
        
        Args:
            batch_size (int): Size of the batch to generate
            batch_index (int): Index of the batch
            
        Returns:
            DataFrame: DataFrame containing normal supply chain data for this batch
        """
        # Set random seed for this batch
        np.random.seed(self.random_state + batch_index)
        
        # Generate timestamps for this batch
        timestamps = self.generate_timestamps()
        timestamps = sorted(timestamps[:batch_size])
        
        # Create base dataframe
        data = pd.DataFrame({
            'timestamp': timestamps,
        })
        
        # Add categorical features
        data['supplier'] = np.random.choice(list(self.suppliers.keys()), batch_size)
        data['product_category'] = np.random.choice(list(self.product_categories.keys()), batch_size)
        data['shipping_method'] = np.random.choice(list(self.shipping_methods.keys()), batch_size)
        data['region'] = np.random.choice(list(self.regions.keys()), batch_size)
        
        # Extract month for seasonal patterns
        data['month'] = data['timestamp'].dt.month
        data['quarter'] = data['timestamp'].dt.quarter
        data['year'] = data['timestamp'].dt.year
        data['day_of_week'] = data['timestamp'].dt.dayofweek
        
        # Generate numerical features based on categorical features
        # Order quantity with seasonal patterns
        base_order_qty = data.apply(
            lambda row: self.product_categories[row['product_category']]['order_qty_mean'] * 
                       self.regions[row['region']]['demand_factor'],
            axis=1
        )
        
        seasonal_amplitude = data.apply(
            lambda row: self.product_categories[row['product_category']]['order_qty_mean'] * 
                       self.product_categories[row['product_category']]['seasonal_impact'],
            axis=1
        )
        
        data['order_quantity'] = self.generate_seasonal_pattern(data['timestamp'], base_order_qty, seasonal_amplitude)
        data['order_quantity'] += np.random.normal(
            0, 
            data.apply(lambda row: self.product_categories[row['product_category']]['order_qty_std'], axis=1),
            batch_size
        )
        
        # Add trend to order quantity (slight growth over time)
        data['order_quantity'] *= self.generate_trend_pattern(data['timestamp'], 1.0, 0.0001)
        
        # Lead time based on supplier and shipping method
        data['lead_time'] = data.apply(
            lambda row: self.suppliers[row['supplier']]['lead_time_mean'] * 
                       self.shipping_methods[row['shipping_method']]['lead_time_factor'] * 
                       self.regions[row['region']]['lead_time_factor'],
            axis=1
        )
        data['lead_time'] += np.random.normal(
            0,
            data.apply(lambda row: self.suppliers[row['supplier']]['lead_time_std'], axis=1),
            batch_size
        )
        
        # Transportation cost based on shipping method and region
        base_transport_cost = 1000  # Base cost
        data['transportation_cost'] = data.apply(
            lambda row: base_transport_cost * 
                       self.shipping_methods[row['shipping_method']]['cost_factor'] * 
                       self.regions[row['region']]['cost_factor'] * 
                       self.product_categories[row['product_category']]['cost_factor'],
            axis=1
        )
        data['transportation_cost'] += np.random.normal(0, 100, batch_size)
        
        # Inventory level with seasonal patterns (inverse to order quantity)
        base_inventory = 5000  # Base inventory level
        data['inventory_level'] = base_inventory - 0.2 * data['order_quantity'] + np.random.normal(0, 500, batch_size)
        
        # Supplier reliability
        data['supplier_reliability'] = data.apply(
            lambda row: np.random.normal(
                self.suppliers[row['supplier']]['reliability_mean'] * 
                self.shipping_methods[row['shipping_method']]['reliability_factor'],
                self.suppliers[row['supplier']]['reliability_std']
            ),
            axis=1
        ).clip(0, 1)
        
        # Demand forecast (slightly different from order quantity to simulate forecast error)
        data['demand_forecast'] = data['order_quantity'] * np.random.normal(1, 0.1, batch_size)
        
        # Production capacity (higher than order quantity on average)
        data['production_capacity'] = data['order_quantity'] * np.random.normal(1.2, 0.15, batch_size)
        
        # Quality rating
        data['quality_rating'] = data.apply(
            lambda row: np.random.normal(
                0.9 * self.suppliers[row['supplier']]['reliability_mean'],
                0.03
            ),
            axis=1
        ).clip(0, 1)
        
        # Add supply chain relationships
        # 1. Order quantity affects inventory level
        data['inventory_level'] = data['inventory_level'] - data['order_quantity'] + np.random.normal(500, 50, batch_size)
        
        # 2. Supplier reliability affects lead time
        data['lead_time'] = data['lead_time'] * (2 - data['supplier_reliability'])
        
        # 3. Quality issues increase costs
        data['transportation_cost'] = data['transportation_cost'] * (2 - data['quality_rating'])
        
        # Apply holiday season effects (months 11-12)
        holiday_mask = data['month'].isin([11, 12])
        data.loc[holiday_mask, 'order_quantity'] *= np.random.uniform(1.2, 1.5, holiday_mask.sum())
        data.loc[holiday_mask, 'demand_forecast'] *= np.random.uniform(1.2, 1.5, holiday_mask.sum())
        
        # Apply weekend effect (lower activity on weekends)
        weekend_mask = data['day_of_week'].isin([5, 6])  # Saturday and Sunday
        data.loc[weekend_mask, 'order_quantity'] *= np.random.uniform(0.6, 0.8, weekend_mask.sum())
        
        # Clean up temporary columns
        data = data.drop(['month', 'quarter', 'year', 'day_of_week'], axis=1)
        
        return data
    
    def generate_normal_data(self):
        """
        Generate normal supply chain data using parallel processing.
        
        Returns:
            DataFrame: DataFrame containing normal supply chain data
        """
        print(f"Generating {self.num_samples} normal data points...")
        
        # Determine batch size and number of batches
        batch_size = min(100000, self.num_samples)  # Process in batches of 100,000 or less
        num_batches = (self.num_samples + batch_size - 1) // batch_size  # Ceiling division
        
        # Generate data in parallel
        if self.n_jobs == 1:
            # Sequential processing
            batches = []
            for i in range(num_batches):
                actual_batch_size = min(batch_size, self.num_samples - i * batch_size)
                batch = self.generate_batch(actual_batch_size, i)
                batches.append(batch)
        else:
            # Parallel processing
            batches = Parallel(n_jobs=self.n_jobs)(delayed(self.generate_batch)(
                min(batch_size, self.num_samples - i * batch_size), i
            ) for i in range(num_batches))
        
        # Combine all batches
        normal_data = pd.concat(batches, ignore_index=True)
        
        # Apply market events
        normal_data = self.apply_market_events(normal_data, normal_data['timestamp'])
        
        # Sort by timestamp
        normal_data = normal_data.sort_values('timestamp').reset_index(drop=True)
        
        print(f"Generated {len(normal_data)} normal data points")
        return normal_data
    
    def inject_anomalies(self, data):
        """
        Inject sophisticated anomalies into the supply chain data.
        
        Args:
            data (DataFrame): Normal supply chain data
            
        Returns:
            tuple: (DataFrame with anomalies, array of anomaly labels)
        """
        print(f"Injecting anomalies with ratio {self.anomaly_ratio}...")
        
        # Make a copy of the data
        data_with_anomalies = data.copy()
        
        # Calculate number of anomalies
        num_anomalies = int(len(data) * self.anomaly_ratio)
        
        # Generate random indices for anomalies
        anomaly_indices = np.random.choice(len(data), num_anomalies, replace=False)
        
        # Create anomaly labels (1 for normal, -1 for anomaly)
        labels = np.ones(len(data))
        labels[anomaly_indices] = -1
        
        # Define more sophisticated anomaly types
        anomaly_types = [
            'quantity_spike', 'lead_time_delay', 'cost_anomaly', 'inventory_shortage',
            'quality_issue', 'forecast_error', 'capacity_drop', 'multi_metric_anomaly',
            'seasonal_pattern_break', 'supplier_reliability_drop', 'logistics_disruption',
            'demand_supply_mismatch', 'black_swan_event', 'data_quality_issue'
        ]
        
        # Inject different types of anomalies
        for idx in anomaly_indices:
            anomaly_type = np.random.choice(anomaly_types, p=[
                0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05
            ])
            
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
                if np.random.random() > 0.5:
                    # Extremely low forecast
                    data_with_anomalies.loc[idx, 'demand_forecast'] *= np.random.uniform(0.2, 0.4)
                else:
                    # Extremely high forecast
                    data_with_anomalies.loc[idx, 'demand_forecast'] *= np.random.uniform(2.5, 4)
            
            elif anomaly_type == 'capacity_drop':
                # Sudden drop in production capacity
                data_with_anomalies.loc[idx, 'production_capacity'] *= np.random.uniform(0.3, 0.5)
            
            elif anomaly_type == 'multi_metric_anomaly':
                # Anomaly affecting multiple metrics simultaneously
                data_with_anomalies.loc[idx, 'lead_time'] *= np.random.uniform(1.5, 2.5)
                data_with_anomalies.loc[idx, 'transportation_cost'] *= np.random.uniform(1.5, 2.0)
                data_with_anomalies.loc[idx, 'quality_rating'] *= np.random.uniform(0.6, 0.8)
                data_with_anomalies.loc[idx, 'supplier_reliability'] *= np.random.uniform(0.7, 0.9)
            
            elif anomaly_type == 'seasonal_pattern_break':
                # Break in expected seasonal pattern
                if data_with_anomalies.loc[idx, 'timestamp'].month in [11, 12]:  # Holiday season
                    data_with_anomalies.loc[idx, 'order_quantity'] *= np.random.uniform(0.3, 0.5)  # Unexpected drop
                else:
                    data_with_anomalies.loc[idx, 'order_quantity'] *= np.random.uniform(2.5, 3.5)  # Unexpected spike
            
            elif anomaly_type == 'supplier_reliability_drop':
                # Severe drop in supplier reliability
                data_with_anomalies.loc[idx, 'supplier_reliability'] *= np.random.uniform(0.3, 0.5)
                data_with_anomalies.loc[idx, 'lead_time'] *= np.random.uniform(1.5, 2.0)
                data_with_anomalies.loc[idx, 'quality_rating'] *= np.random.uniform(0.5, 0.7)
            
            elif anomaly_type == 'logistics_disruption':
                # Logistics disruption affecting shipping
                data_with_anomalies.loc[idx, 'transportation_cost'] *= np.random.uniform(2.0, 3.0)
                data_with_anomalies.loc[idx, 'lead_time'] *= np.random.uniform(1.8, 2.5)
            
            elif anomaly_type == 'demand_supply_mismatch':
                # Severe mismatch between demand forecast and production capacity
                data_with_anomalies.loc[idx, 'demand_forecast'] *= np.random.uniform(1.8, 2.5)
                data_with_anomalies.loc[idx, 'production_capacity'] *= np.random.uniform(0.5, 0.7)
            
            elif anomaly_type == 'black_swan_event':
                # Extreme event affecting all metrics
                impact_factor = np.random.uniform(0.3, 0.5)  # Severe impact
                for col in ['order_quantity', 'inventory_level', 'production_capacity', 'supplier_reliability', 'quality_rating']:
                    data_with_anomalies.loc[idx, col] *= impact_factor
                for col in ['lead_time', 'transportation_cost']:
                    data_with_anomalies.loc[idx, col] /= impact_factor  # Inverse effect (increase)
            
            elif anomaly_type == 'data_quality_issue':
                # Data quality issues (e.g., impossible values)
                if np.random.random() > 0.5:
                    # Negative values where not possible
                    neg_cols = np.random.choice(['order_quantity', 'lead_time', 'transportation_cost', 'inventory_level', 'production_capacity'], 
                                               size=np.random.randint(1, 3), replace=False)
                    for col in neg_cols:
                        data_with_anomalies.loc[idx, col] *= -1
                else:
                    # Extremely high values
                    extreme_cols = np.random.choice(['order_quantity', 'lead_time', 'transportation_cost', 'inventory_level', 'production_capacity'], 
                                                   size=np.random.randint(1, 3), replace=False)
                    for col in extreme_cols:
                        data_with_anomalies.loc[idx, col] *= np.random.uniform(10, 20)
        
        print(f"Injected {num_anomalies} anomalies")
        return data_with_anomalies, labels
    
    def generate_dataset(self, save_to_file=False, file_prefix='supply_chain_data'):
        """
        Generate a complete dataset with normal and anomalous data points.
        
        Args:
            save_to_file (bool): Whether to save the dataset to a file
            file_prefix (str): Prefix for the saved file name
            
        Returns:
            tuple: (DataFrame with data, array of labels)
        """
        # Generate normal data
        normal_data = self.generate_normal_data()
        
        # Inject anomalies
        data_with_anomalies, labels = self.inject_anomalies(normal_data)
        
        # Save to file if requested
        if save_to_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{file_prefix}_{len(data_with_anomalies)}_{self.anomaly_ratio}_{timestamp}.csv"
        
        # Define anomaly types for greater diversity
        self.anomaly_types = [
            {'name': 'Supply Delay', 'feature': 'lead_time', 'impact': 2.5},
            {'name': 'Order Spike', 'feature': 'order_quantity', 'impact': 3.0},
            {'name': 'Inventory Shortage', 'feature': 'inventory_level', 'impact': 0.2},
            {'name': 'Cost Surge', 'feature': 'transportation_cost', 'impact': 2.0},
            {'name': 'Supplier Failure', 'feature': 'supplier_reliability', 'impact': 0.5},
            {'name': 'Demand Drop', 'feature': 'demand_forecast', 'impact': 0.3},
            {'name': 'Production Halt', 'feature': 'production_capacity', 'impact': 0.1},
            {'name': 'Fake Anomaly', 'feature': 'order_quantity', 'impact': 0.1},
        ]
        
        # Generate normal samples
        n_anomalies = int(self.num_samples * self.anomaly_ratio)
        n_normals = self.num_samples - n_anomalies
        normal_data = self._generate_samples(n_normals, anomaly=False)
        anomaly_data = []
        # Distribute anomalies evenly across types
        n_types = len(self.anomaly_types)
        anomalies_per_type = n_anomalies // n_types
        for anomaly_type in self.anomaly_types:
            anomaly_data.append(self._generate_samples(anomalies_per_type, anomaly=True, anomaly_type=anomaly_type))
        anomaly_data = pd.concat(anomaly_data, ignore_index=True)
        # Concatenate and shuffle
        data = pd.concat([normal_data, anomaly_data], ignore_index=True)
        labels = np.array([1]*n_normals + [-1]*len(anomaly_data))
        idx = np.arange(len(data))
        np.random.shuffle(idx)
        data = data.iloc[idx].reset_index(drop=True)
        labels = labels[idx]
        return data, labels
    def _generate_samples(self, n, anomaly=False, anomaly_type=None):
        # Generate base samples
        samples = []
        for _ in range(n):
            # ... existing code for normal sample generation ...
            sample = self._generate_single_sample()
            if anomaly and anomaly_type is not None:
                # Apply anomaly impact
                feature = anomaly_type['feature']
                impact = anomaly_type['impact']
                if feature in sample:
                    if impact < 1:
                        sample[feature] *= impact
                    else:
                        sample[feature] *= impact
            samples.append(sample)
        return pd.DataFrame(samples)