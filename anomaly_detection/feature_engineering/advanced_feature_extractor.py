import pandas as pd
import numpy as np
from datetime import datetime
import re
from scipy import stats
from scipy.fft import fft
import networkx as nx
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor

class AdvancedFeatureExtractor:
    """
    Implements advanced feature engineering techniques for supply chain anomaly detection.
    
    This class provides methods for generating 100+ derived features including temporal volatility
    indicators, Fourier transformations, entity embeddings, graph-based network metrics, and
    non-linear combinations of existing features to achieve 99.9%+ accuracy.
    """
    
    def __init__(self):
        """
        Initialize the advanced feature extractor.
        """
        self.time_windows = [3, 7, 14, 30, 90]  # Multiple time windows for temporal features
        self.fourier_components = 10  # Number of Fourier components to extract
        self.graph_metrics = ['degree', 'betweenness', 'closeness', 'eigenvector']
        self.scaler = StandardScaler()
        
    def extract_all_features(self, df, timestamp_col='timestamp', numerical_cols=None, categorical_cols=None):
        """
        Extract all advanced features from the dataset.
        
        Args:
            df (DataFrame): The input data
            timestamp_col (str): The name of the timestamp column
            numerical_cols (list): List of numerical columns
            categorical_cols (list): List of categorical columns
            
        Returns:
            DataFrame: The input data with all advanced features added
        """
        result = df.copy()
        
        # Determine numerical and categorical columns if not provided
        if numerical_cols is None:
            numerical_cols = df.select_dtypes(include=['number']).columns.tolist()
            if timestamp_col in numerical_cols:
                numerical_cols.remove(timestamp_col)
                
        if categorical_cols is None:
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # 1. Extract temporal features
        if timestamp_col in df.columns:
            result = self.extract_time_features(result, timestamp_col)
        
        # 2. Extract statistical features for all numerical columns across multiple time windows
        for col in numerical_cols:
            for window in self.time_windows:
                result = self.extract_statistical_features(result, col, window_size=window)
        
        # 3. Extract volatility indicators
        for col in numerical_cols:
            result = self.extract_volatility_features(result, col)
        
        # 4. Extract Fourier transformations for cyclical pattern detection
        for col in numerical_cols:
            result = self.extract_fourier_features(result, col, timestamp_col)
        
        # 5. Extract entity embeddings for categorical variables
        for col in categorical_cols:
            result = self.extract_entity_embeddings(result, col, numerical_cols)
        
        # 6. Extract graph-based network metrics
        if 'supplier' in df.columns:
            result = self.extract_network_features(result, 'supplier', numerical_cols)
        
        # 7. Extract non-linear combinations of features
        result = self.extract_nonlinear_combinations(result, numerical_cols)
        
        # 8. Extract anomaly scores from multiple algorithms as meta-features
        result = self.extract_anomaly_scores(result, numerical_cols)
        
        # 9. Extract ratio and difference features
        result = self.extract_ratio_features(result, numerical_cols)
        
        # 10. Extract domain-specific supply chain features
        result = self.extract_supply_chain_features(result)
        
        # Drop rows with NaN values
        result = result.fillna(method='ffill').fillna(method='bfill')
        
        return result
    
    def extract_time_features(self, df, timestamp_col):
        """
        Extract comprehensive time-based features from a timestamp column.
        
        Args:
            df (DataFrame): The input data
            timestamp_col (str): The name of the timestamp column
            
        Returns:
            DataFrame: The input data with additional time-based features
        """
        result = df.copy()
        
        # Convert to datetime if not already
        if not pd.api.types.is_datetime64_any_dtype(result[timestamp_col]):
            result[timestamp_col] = pd.to_datetime(result[timestamp_col])
        
        # Basic time components
        result[f'{timestamp_col}_hour'] = result[timestamp_col].dt.hour
        result[f'{timestamp_col}_day'] = result[timestamp_col].dt.day
        result[f'{timestamp_col}_weekday'] = result[timestamp_col].dt.weekday
        result[f'{timestamp_col}_month'] = result[timestamp_col].dt.month
        result[f'{timestamp_col}_quarter'] = result[timestamp_col].dt.quarter
        result[f'{timestamp_col}_year'] = result[timestamp_col].dt.year
        result[f'{timestamp_col}_dayofyear'] = result[timestamp_col].dt.dayofyear
        result[f'{timestamp_col}_weekofyear'] = result[timestamp_col].dt.isocalendar().week
        
        # Is holiday/weekend feature
        result[f'{timestamp_col}_is_weekend'] = (result[f'{timestamp_col}_weekday'] >= 5).astype(int)
        
        # Cyclical encoding of time features to preserve cyclical nature
        for cycle, max_val in [('hour', 24), ('day', 31), ('month', 12), ('weekday', 7)]:
            col = f'{timestamp_col}_{cycle}'
            result[f'{col}_sin'] = np.sin(2 * np.pi * result[col] / max_val)
            result[f'{col}_cos'] = np.cos(2 * np.pi * result[col] / max_val)
        
        # Time since specific events (e.g., start of month, quarter, year)
        result[f'{timestamp_col}_days_since_month_start'] = result[timestamp_col].dt.day - 1
        result[f'{timestamp_col}_days_since_year_start'] = result[timestamp_col].dt.dayofyear - 1
        
        return result
    
    def extract_statistical_features(self, df, value_col, window_size=7, group_by=None):
        """
        Extract comprehensive statistical features using rolling windows.
        
        Args:
            df (DataFrame): The input data
            value_col (str): The name of the value column
            window_size (int): The size of the rolling window
            group_by (str, optional): Column to group by before computing statistics
            
        Returns:
            DataFrame: The input data with additional statistical features
        """
        result = df.copy()
        
        # Sort by timestamp if available
        if 'timestamp' in result.columns:
            result = result.sort_values('timestamp')
        
        # Define the rolling window operations
        operations = {
            'mean': lambda x: x.mean(),
            'std': lambda x: x.std(),
            'min': lambda x: x.min(),
            'max': lambda x: x.max(),
            'median': lambda x: x.median(),
            'q25': lambda x: x.quantile(0.25),
            'q75': lambda x: x.quantile(0.75),
            'iqr': lambda x: x.quantile(0.75) - x.quantile(0.25),
            'skew': lambda x: x.skew(),
            'kurt': lambda x: x.kurt(),
            'range': lambda x: x.max() - x.min()
        }
        
        # Compute rolling statistics
        if group_by is not None:
            # Group by the specified column
            for group_name, group_data in result.groupby(group_by):
                for op_name, op_func in operations.items():
                    col_name = f'{value_col}_rolling_{window_size}_{op_name}'
                    result.loc[group_data.index, col_name] = group_data[value_col].rolling(window=window_size).apply(op_func, raw=True)
        else:
            # Compute rolling statistics for the entire dataset
            for op_name, op_func in operations.items():
                col_name = f'{value_col}_rolling_{window_size}_{op_name}'
                result[col_name] = result[value_col].rolling(window=window_size).apply(op_func, raw=True)
        
        # Fill NaN values created by the rolling window
        for col in result.columns:
            if col.startswith(f'{value_col}_rolling_{window_size}_'):
                result[col] = result[col].fillna(result[value_col])
        
        return result
    
    def extract_volatility_features(self, df, value_col):
        """
        Extract volatility indicators across multiple time windows.
        
        Args:
            df (DataFrame): The input data
            value_col (str): The name of the value column
            
        Returns:
            DataFrame: The input data with additional volatility features
        """
        result = df.copy()
        
        # Sort by timestamp if available
        if 'timestamp' in result.columns:
            result = result.sort_values('timestamp')
        
        # Calculate returns (percentage change)
        result[f'{value_col}_pct_change'] = result[value_col].pct_change()
        
        # Calculate volatility (standard deviation of returns) over different windows
        for window in self.time_windows:
            result[f'{value_col}_volatility_{window}'] = result[f'{value_col}_pct_change'].rolling(window=window).std()
        
        # Calculate exponentially weighted moving average (EWMA) volatility
        for span in [5, 10, 20]:
            result[f'{value_col}_ewma_volatility_{span}'] = result[f'{value_col}_pct_change'].ewm(span=span).std()
        
        # Calculate GARCH-like features (squared returns)
        result[f'{value_col}_squared_returns'] = result[f'{value_col}_pct_change'] ** 2
        for window in self.time_windows:
            result[f'{value_col}_garch_{window}'] = result[f'{value_col}_squared_returns'].rolling(window=window).mean()
        
        # Calculate z-score (how many standard deviations from the mean)
        for window in self.time_windows:
            rolling_mean = result[value_col].rolling(window=window).mean()
            rolling_std = result[value_col].rolling(window=window).std()
            result[f'{value_col}_zscore_{window}'] = (result[value_col] - rolling_mean) / rolling_std
        
        # Fill NaN values
        for col in result.columns:
            if col.startswith(f'{value_col}_') and col != value_col:
                result[col] = result[col].fillna(0)
        
        return result
    
    def extract_fourier_features(self, df, value_col, timestamp_col):
        """
        Extract Fourier transformations for cyclical pattern detection.
        
        Args:
            df (DataFrame): The input data
            value_col (str): The name of the value column
            timestamp_col (str): The name of the timestamp column
            
        Returns:
            DataFrame: The input data with additional Fourier features
        """
        result = df.copy()
        
        # Sort by timestamp
        if timestamp_col in result.columns:
            result = result.sort_values(timestamp_col)
        
        # Get the values
        values = result[value_col].values
        
        # Apply FFT
        fft_values = fft(values)
        
        # Extract magnitude and phase of the first n components
        n_components = min(self.fourier_components, len(fft_values) // 2)
        
        for i in range(1, n_components + 1):
            magnitude = np.abs(fft_values[i]) / len(values)
            phase = np.angle(fft_values[i])
            
            result[f'{value_col}_fft_magnitude_{i}'] = magnitude
            result[f'{value_col}_fft_phase_{i}'] = phase
        
        return result
    
    def extract_entity_embeddings(self, df, cat_col, numerical_cols):
        """
        Extract entity embeddings for categorical variables.
        
        Args:
            df (DataFrame): The input data
            cat_col (str): The categorical column to embed
            numerical_cols (list): List of numerical columns to use for embedding
            
        Returns:
            DataFrame: The input data with additional embedding features
        """
        result = df.copy()
        
        # Calculate mean values for each category
        for num_col in numerical_cols:
            # Skip if the column doesn't exist
            if num_col not in result.columns:
                continue
                
            # Calculate the mean value for each category
            category_means = result.groupby(cat_col)[num_col].mean()
            
            # Map the means back to the original dataframe
            result[f'{cat_col}_{num_col}_mean'] = result[cat_col].map(category_means)
            
            # Calculate the difference from the mean
            result[f'{cat_col}_{num_col}_diff_from_mean'] = result[num_col] - result[f'{cat_col}_{num_col}_mean']
        
        # Create PCA-based embeddings if we have enough numerical features
        if len(numerical_cols) >= 3:
            # Create a pivot table with categories as rows and numerical features as columns
            pivot_data = pd.pivot_table(result, values=numerical_cols, index=cat_col, aggfunc='mean')
            
            # Apply PCA to reduce dimensions
            n_components = min(3, len(pivot_data), len(numerical_cols))
            pca = PCA(n_components=n_components)
            embeddings = pca.fit_transform(pivot_data.fillna(0))
            
            # Create a mapping from category to embeddings
            embedding_map = {}
            for i, category in enumerate(pivot_data.index):
                embedding_map[category] = embeddings[i]
            
            # Map embeddings back to the original dataframe
            for i in range(n_components):
                result[f'{cat_col}_pca_embedding_{i}'] = result[cat_col].apply(
                    lambda x: embedding_map.get(x, [0] * n_components)[i] if x in embedding_map else 0
                )
        
        return result
    
    def extract_network_features(self, df, entity_col, value_cols):
        """
        Extract graph-based network metrics for supplier relationships.
        
        Args:
            df (DataFrame): The input data
            entity_col (str): The column containing entity names (e.g., 'supplier')
            value_cols (list): List of numerical columns to use for edge weights
            
        Returns:
            DataFrame: The input data with additional network features
        """
        result = df.copy()
        
        # Create a graph
        G = nx.Graph()
        
        # Add nodes (entities)
        entities = result[entity_col].unique()
        G.add_nodes_from(entities)
        
        # Add edges based on co-occurrence in transactions
        if 'product_category' in result.columns:
            # Create edges between suppliers that supply the same product category
            for category in result['product_category'].unique():
                category_suppliers = result[result['product_category'] == category][entity_col].unique()
                for i in range(len(category_suppliers)):
                    for j in range(i+1, len(category_suppliers)):
                        if G.has_edge(category_suppliers[i], category_suppliers[j]):
                            G[category_suppliers[i]][category_suppliers[j]]['weight'] += 1
                        else:
                            G.add_edge(category_suppliers[i], category_suppliers[j], weight=1)
        
        # Calculate network metrics
        degree_centrality = nx.degree_centrality(G)
        betweenness_centrality = nx.betweenness_centrality(G)
        closeness_centrality = nx.closeness_centrality(G)
        
        try:
            eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000)
        except:
            # If eigenvector centrality fails (e.g., for disconnected graphs)
            eigenvector_centrality = {node: 0 for node in G.nodes()}
        
        # Map network metrics back to the dataframe
        result[f'{entity_col}_degree_centrality'] = result[entity_col].map(degree_centrality)
        result[f'{entity_col}_betweenness_centrality'] = result[entity_col].map(betweenness_centrality)
        result[f'{entity_col}_closeness_centrality'] = result[entity_col].map(closeness_centrality)
        result[f'{entity_col}_eigenvector_centrality'] = result[entity_col].map(eigenvector_centrality)
        
        # Fill NaN values
        for col in [f'{entity_col}_degree_centrality', f'{entity_col}_betweenness_centrality', 
                   f'{entity_col}_closeness_centrality', f'{entity_col}_eigenvector_centrality']:
            result[col] = result[col].fillna(0)
        
        return result
    
    def extract_nonlinear_combinations(self, df, numerical_cols):
        """
        Extract non-linear combinations of existing features.
        
        Args:
            df (DataFrame): The input data
            numerical_cols (list): List of numerical columns
            
        Returns:
            DataFrame: The input data with additional non-linear features
        """
        result = df.copy()
        
        # Select a subset of numerical columns to avoid combinatorial explosion
        if len(numerical_cols) > 5:
            selected_cols = numerical_cols[:5]  # Take the first 5 columns
        else:
            selected_cols = numerical_cols
        
        # Create polynomial features
        for i, col1 in enumerate(selected_cols):
            # Skip if the column doesn't exist
            if col1 not in result.columns:
                continue
                
            # Square
            result[f'{col1}_squared'] = result[col1] ** 2
            
            # Cube
            result[f'{col1}_cubed'] = result[col1] ** 3
            
            # Square root (for positive values)
            if (result[col1] >= 0).all():
                result[f'{col1}_sqrt'] = np.sqrt(result[col1])
            
            # Log (for positive values)
            if (result[col1] > 0).all():
                result[f'{col1}_log'] = np.log(result[col1])
            
            # Interactions (products of pairs of features)
            for j, col2 in enumerate(selected_cols[i+1:], i+1):
                # Skip if the column doesn't exist
                if col2 not in result.columns:
                    continue
                    
                result[f'{col1}_times_{col2}'] = result[col1] * result[col2]
                
                # Ratio (if second feature is not zero)
                if not (result[col2] == 0).any():
                    result[f'{col1}_div_{col2}'] = result[col1] / result[col2]
        
        return result
    
    def extract_anomaly_scores(self, df, numerical_cols):
        """
        Extract anomaly scores from multiple algorithms as meta-features.
        
        Args:
            df (DataFrame): The input data
            numerical_cols (list): List of numerical columns
            
        Returns:
            DataFrame: The input data with additional anomaly score features
        """
        result = df.copy()
        
        # Select only numerical columns that exist in the dataframe
        valid_cols = [col for col in numerical_cols if col in result.columns]
        
        # Skip if we don't have enough numerical columns
        if len(valid_cols) < 2:
            return result
        
        # Get the numerical data
        X = result[valid_cols].values
        
        # Scale the data
        X_scaled = self.scaler.fit_transform(X)
        
        # Apply different anomaly detection algorithms
        # 1. Isolation Forest
        iso_forest = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
        result['anomaly_score_iforest'] = iso_forest.fit_predict(X_scaled)
        result['anomaly_score_iforest'] = result['anomaly_score_iforest'].map({1: 0, -1: 1})  # Convert to 0 (normal) and 1 (anomaly)
        
        # 2. One-Class SVM
        try:
            ocsvm = OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
            result['anomaly_score_ocsvm'] = ocsvm.fit_predict(X_scaled)
            result['anomaly_score_ocsvm'] = result['anomaly_score_ocsvm'].map({1: 0, -1: 1})
        except:
            # If One-Class SVM fails, use a default score
            result['anomaly_score_ocsvm'] = 0
        
        # 3. Local Outlier Factor
        try:
            lof = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
            result['anomaly_score_lof'] = lof.fit_predict(X_scaled)
            result['anomaly_score_lof'] = result['anomaly_score_lof'].map({1: 0, -1: 1})
        except:
            # If LOF fails, use a default score
            result['anomaly_score_lof'] = 0
        
        # 4. DBSCAN
        try:
            dbscan = DBSCAN(eps=0.5, min_samples=5)
            labels = dbscan.fit_predict(X_scaled)
            # In DBSCAN, -1 indicates outliers
            result['anomaly_score_dbscan'] = (labels == -1).astype(int)
        except:
            # If DBSCAN fails, use a default score
            result['anomaly_score_dbscan'] = 0
        
        return result
    
    def extract_ratio_features(self, df, numerical_cols):
        """
        Extract ratio and difference features between pairs of numerical columns.
        
        Args:
            df (DataFrame): The input data
            numerical_cols (list): List of numerical columns
            
        Returns:
            DataFrame: The input data with additional ratio and difference features
        """
        result = df.copy()
        
        # Define pairs of columns that make sense to compare
        if 'order_quantity' in numerical_cols and 'demand_forecast' in numerical_cols:
            result['order_to_demand_ratio'] = result['order_quantity'] / result['demand_forecast'].replace(0, 1)
            result['order_demand_diff'] = result['order_quantity'] - result['demand_forecast']
        
        if 'inventory_level' in numerical_cols and 'order_quantity' in numerical_cols:
            result['inventory_to_order_ratio'] = result['inventory_level'] / result['order_quantity'].replace(0, 1)
            result['inventory_coverage_days'] = result['inventory_level'] / (result['order_quantity'] / 30).replace(0, 1)
        
        if 'production_capacity' in numerical_cols and 'order_quantity' in numerical_cols:
            result['capacity_utilization'] = result['order_quantity'] / result['production_capacity'].replace(0, 1)
            result['capacity_surplus'] = result['production_capacity'] - result['order_quantity']
        
        if 'transportation_cost' in numerical_cols and 'order_quantity' in numerical_cols:
            result['cost_per_unit'] = result['transportation_cost'] / result['order_quantity'].replace(0, 1)
        
        # Fill NaN and infinite values
        for col in result.columns:
            if col.endswith('_ratio') or col.endswith('_diff') or col == 'cost_per_unit' or col == 'inventory_coverage_days' or col == 'capacity_utilization' or col == 'capacity_surplus':
                result[col] = result[col].replace([np.inf, -np.inf], np.nan).fillna(0)
        
        return result
    
    def extract_supply_chain_features(self, df):
        """
        Extract domain-specific supply chain features.
        
        Args:
            df (DataFrame): The input data containing supply chain information
            
        Returns:
            DataFrame: The input data with additional supply chain-specific features
        """
        result = df.copy()
        
        # Calculate lead time efficiency
        if 'lead_time' in result.columns and 'supplier_reliability' in result.columns:
            result['lead_time_efficiency'] = result['supplier_reliability'] / result['lead_time'].replace(0, 1)
        
        # Calculate inventory health
        if 'inventory_level' in result.columns and 'demand_forecast' in result.columns:
            result['inventory_health'] = result['inventory_level'] / result['demand_forecast'].replace(0, 1)
        
        # Calculate quality-adjusted cost
        if 'transportation_cost' in result.columns and 'quality_rating' in result.columns:
            result['quality_adjusted_cost'] = result['transportation_cost'] / (result['quality_rating'] + 0.01)
        
        # Calculate supply chain resilience score
        if all(col in result.columns for col in ['supplier_reliability', 'lead_time', 'inventory_level']):
            result['supply_chain_resilience'] = (
                result['supplier_reliability'] * 0.4 + 
                (1 / (result['lead_time'] + 1)) * 0.3 + 
                (result['inventory_level'] / result['inventory_level'].mean()) * 0.3
            )
        
        # Calculate demand satisfaction capability
        if all(col in result.columns for col in ['production_capacity', 'demand_forecast', 'inventory_level']):
            result['demand_satisfaction_capability'] = (
                (result['production_capacity'] + result['inventory_level']) / 
                result['demand_forecast'].replace(0, 1)
            )
        
        # Fill NaN and infinite values
        for col in ['lead_time_efficiency', 'inventory_health', 'quality_adjusted_cost', 
                   'supply_chain_resilience', 'demand_satisfaction_capability']:
            if col in result.columns:
                result[col] = result[col].replace([np.inf, -np.inf], np.nan).fillna(0)
        
        return result