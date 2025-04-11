import pandas as pd
import numpy as np
from datetime import datetime
import re

class FeatureExtractor:
    """
    Extracts and transforms supply chain-specific features from raw data.
    
    This class provides methods for generating domain-specific features
    that can improve the performance of the anomaly detection model.
    """
    
    def __init__(self):
        """
        Initialize the feature extractor.
        """
        self.time_features = ['hour', 'day', 'weekday', 'month', 'quarter', 'year']
        self.statistical_features = ['rolling_mean', 'rolling_std', 'rolling_min', 'rolling_max']
    
    def extract_time_features(self, df, timestamp_col):
        """
        Extract time-based features from a timestamp column.
        
        Args:
            df (DataFrame): The input data.
            timestamp_col (str): The name of the timestamp column.
            
        Returns:
            DataFrame: The input data with additional time-based features.
        """
        # Make a copy to avoid modifying the original dataframe
        result = df.copy()
        
        # Convert to datetime if not already
        if not pd.api.types.is_datetime64_any_dtype(result[timestamp_col]):
            result[timestamp_col] = pd.to_datetime(result[timestamp_col])
        
        # Extract time components
        result[timestamp_col + '_hour'] = result[timestamp_col].dt.hour
        result[timestamp_col + '_day'] = result[timestamp_col].dt.day
        result[timestamp_col + '_weekday'] = result[timestamp_col].dt.weekday
        result[timestamp_col + '_month'] = result[timestamp_col].dt.month
        result[timestamp_col + '_quarter'] = result[timestamp_col].dt.quarter
        result[timestamp_col + '_year'] = result[timestamp_col].dt.year
        
        return result
    
    def extract_statistical_features(self, df, value_col, window_size=7, group_by=None):
        """
        Extract statistical features using rolling windows.
        
        Args:
            df (DataFrame): The input data.
            value_col (str): The name of the value column.
            window_size (int): The size of the rolling window.
            group_by (str, optional): Column to group by before computing statistics.
            
        Returns:
            DataFrame: The input data with additional statistical features.
        """
        # Make a copy to avoid modifying the original dataframe
        result = df.copy()
        
        # Sort by timestamp if available
        if 'timestamp' in result.columns:
            result = result.sort_values('timestamp')
        
        # Compute rolling statistics
        if group_by is not None:
            # Group by the specified column
            for group_name, group_data in result.groupby(group_by):
                # Compute rolling statistics for each group
                result.loc[group_data.index, f'{value_col}_rolling_mean'] = group_data[value_col].rolling(window=window_size).mean()
                result.loc[group_data.index, f'{value_col}_rolling_std'] = group_data[value_col].rolling(window=window_size).std()
                result.loc[group_data.index, f'{value_col}_rolling_min'] = group_data[value_col].rolling(window=window_size).min()
                result.loc[group_data.index, f'{value_col}_rolling_max'] = group_data[value_col].rolling(window=window_size).max()
        else:
            # Compute rolling statistics for the entire dataset
            result[f'{value_col}_rolling_mean'] = result[value_col].rolling(window=window_size).mean()
            result[f'{value_col}_rolling_std'] = result[value_col].rolling(window=window_size).std()
            result[f'{value_col}_rolling_min'] = result[value_col].rolling(window=window_size).min()
            result[f'{value_col}_rolling_max'] = result[value_col].rolling(window=window_size).max()
        
        # Fill NaN values created by the rolling window
        for col in [f'{value_col}_rolling_mean', f'{value_col}_rolling_std', f'{value_col}_rolling_min', f'{value_col}_rolling_max']:
            result[col] = result[col].fillna(result[value_col])
        
        return result
    
    def extract_supply_chain_features(self, df):
        """
        Extract supply chain-specific features.
        
        Args:
            df (DataFrame): The input data containing supply chain information.
            
        Returns:
            DataFrame: The input data with additional supply chain-specific features.
        """
        # Make a copy to avoid modifying the original dataframe
        result = df.copy()
        
        # Calculate lead time if shipment and delivery dates are available
        if 'shipment_date' in result.columns and 'delivery_date' in result.columns:
            # Convert to datetime if not already
            for col in ['shipment_date', 'delivery_date']:
                if not pd.api.types.is_datetime64_any_dtype(result[col]):
                    result[col] = pd.to_datetime(result[col])
            
            # Calculate lead time in days
            result['lead_time_days'] = (result['delivery_date'] - result['shipment_date']).dt.total_seconds() / (24 * 3600)
        
        # Calculate inventory turnover if relevant columns are available
        if 'cost_of_goods_sold' in result.columns and 'average_inventory' in result.columns:
            result['inventory_turnover'] = result['cost_of_goods_sold'] / result['average_inventory']
        
        # Calculate order fulfillment rate if relevant columns are available
        if 'orders_delivered_in_full' in result.columns and 'total_orders' in result.columns:
            result['order_fulfillment_rate'] = result['orders_delivered_in_full'] / result['total_orders']
        
        # Calculate perfect order rate if relevant columns are available
        if 'perfect_orders' in result.columns and 'total_orders' in result.columns:
            result['perfect_order_rate'] = result['perfect_orders'] / result['total_orders']
        
        return result
    
    def extract_all_features(self, df, timestamp_col=None, value_cols=None, window_size=7, group_by=None):
        """
        Extract all available features from the input data.
        
        Args:
            df (DataFrame): The input data.
            timestamp_col (str, optional): The name of the timestamp column.
            value_cols (list, optional): List of value columns for statistical features.
            window_size (int): The size of the rolling window.
            group_by (str, optional): Column to group by before computing statistics.
            
        Returns:
            DataFrame: The input data with all additional features.
        """
        # Make a copy to avoid modifying the original dataframe
        result = df.copy()
        
        # Extract time features if timestamp column is provided
        if timestamp_col is not None and timestamp_col in result.columns:
            result = self.extract_time_features(result, timestamp_col)
        
        # Extract statistical features if value columns are provided
        if value_cols is not None:
            for value_col in value_cols:
                if value_col in result.columns:
                    result = self.extract_statistical_features(result, value_col, window_size, group_by)
        
        # Extract supply chain-specific features
        result = self.extract_supply_chain_features(result)
        
        return result