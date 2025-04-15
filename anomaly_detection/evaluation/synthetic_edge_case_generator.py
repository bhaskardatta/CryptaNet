import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
from scipy import stats

class SyntheticEdgeCaseGenerator:
    """
    Generates synthetic edge cases for testing anomaly detection models under extreme conditions.
    
    This class creates specialized test datasets including:
    1. Supply chain disruptions
    2. Adversarial examples
    3. Out-of-distribution samples
    
    These edge cases are essential for evaluating model robustness and ensuring 99.9%+ accuracy
    in real-world scenarios with near-zero false positives and negligible false negatives.
    """
    
    def __init__(self, base_data=None, random_state=42):
        """
        Initialize the edge case generator.
        
        Args:
            base_data (DataFrame, optional): Base supply chain data to modify
            random_state (int): Random seed for reproducibility
        """
        self.base_data = base_data
        self.random_state = random_state
        np.random.seed(random_state)
        
        # Define extreme event types
        self.disruption_types = [
            'natural_disaster',
            'geopolitical_crisis',
            'pandemic',
            'financial_crash',
            'cyber_attack',
            'transportation_failure',
            'supplier_bankruptcy',
            'regulatory_change',
            'labor_strike',
            'energy_crisis'
        ]
    
    def generate_supply_chain_disruptions(self, num_samples=1000, severity='high'):
        """
        Generate data simulating major supply chain disruptions.
        
        Args:
            num_samples (int): Number of samples to generate
            severity (str): Severity level ('low', 'medium', 'high', 'extreme')
            
        Returns:
            tuple: (DataFrame with disruption data, array of labels)
        """
        print(f"Generating {num_samples} supply chain disruption samples with {severity} severity...")
        
        # Create base data if not provided
        if self.base_data is None:
            data = self._generate_base_data(num_samples)
        else:
            # Sample from base data
            if len(self.base_data) >= num_samples:
                data = self.base_data.sample(num_samples, random_state=self.random_state).copy()
            else:
                # If base data is smaller, sample with replacement
                data = self.base_data.sample(num_samples, replace=True, random_state=self.random_state).copy()
        
        # Define severity factors
        severity_factors = {
            'low': {'mean': 0.8, 'std': 0.05},
            'medium': {'mean': 0.6, 'std': 0.1},
            'high': {'mean': 0.4, 'std': 0.15},
            'extreme': {'mean': 0.2, 'std': 0.2}
        }
        
        # Get severity parameters
        severity_mean = severity_factors[severity]['mean']
        severity_std = severity_factors[severity]['std']
        
        # Select random disruption type for each sample
        data['disruption_type'] = np.random.choice(self.disruption_types, num_samples)
        
        # Apply disruption effects based on type and severity
        for i, row in data.iterrows():
            disruption = row['disruption_type']
            
            # Generate impact factor (lower means more severe)
            impact_factor = np.random.normal(severity_mean, severity_std)
            impact_factor = max(0.05, min(0.95, impact_factor))  # Clip to reasonable range
            
            if disruption == 'natural_disaster':
                # Natural disasters affect transportation, inventory, and lead time
                data.loc[i, 'transportation_cost'] *= (2.0 / impact_factor)
                data.loc[i, 'lead_time'] *= (2.0 / impact_factor)
                data.loc[i, 'inventory_level'] *= impact_factor
                
            elif disruption == 'geopolitical_crisis':
                # Geopolitical crises affect costs and supplier reliability
                data.loc[i, 'transportation_cost'] *= (1.8 / impact_factor)
                data.loc[i, 'supplier_reliability'] *= impact_factor
                data.loc[i, 'lead_time'] *= (1.5 / impact_factor)
                
            elif disruption == 'pandemic':
                # Pandemics affect all aspects of the supply chain
                data.loc[i, 'order_quantity'] *= impact_factor
                data.loc[i, 'lead_time'] *= (2.0 / impact_factor)
                data.loc[i, 'transportation_cost'] *= (1.5 / impact_factor)
                data.loc[i, 'inventory_level'] *= impact_factor
                data.loc[i, 'supplier_reliability'] *= impact_factor
                data.loc[i, 'demand_forecast'] *= impact_factor
                data.loc[i, 'production_capacity'] *= impact_factor
                
            elif disruption == 'financial_crash':
                # Financial crashes affect demand and costs
                data.loc[i, 'order_quantity'] *= impact_factor
                data.loc[i, 'demand_forecast'] *= impact_factor
                data.loc[i, 'transportation_cost'] *= (1.3 / impact_factor)
                
            elif disruption == 'cyber_attack':
                # Cyber attacks create data inconsistencies
                # Introduce contradictions between related fields
                data.loc[i, 'order_quantity'] *= (1.5 / impact_factor)
                data.loc[i, 'demand_forecast'] *= impact_factor
                data.loc[i, 'inventory_level'] = np.random.uniform(0, data.loc[i, 'inventory_level'])
                
            elif disruption == 'transportation_failure':
                # Transportation failures affect lead time and costs
                data.loc[i, 'lead_time'] *= (2.5 / impact_factor)
                data.loc[i, 'transportation_cost'] *= (2.0 / impact_factor)
                
            elif disruption == 'supplier_bankruptcy':
                # Supplier bankruptcy affects reliability and lead time
                data.loc[i, 'supplier_reliability'] *= impact_factor * 0.5  # Severe impact
                data.loc[i, 'lead_time'] *= (3.0 / impact_factor)
                data.loc[i, 'quality_rating'] *= impact_factor
                
            elif disruption == 'regulatory_change':
                # Regulatory changes affect costs and capacity
                data.loc[i, 'transportation_cost'] *= (1.4 / impact_factor)
                data.loc[i, 'production_capacity'] *= impact_factor
                
            elif disruption == 'labor_strike':
                # Labor strikes affect production capacity and lead time
                data.loc[i, 'production_capacity'] *= impact_factor
                data.loc[i, 'lead_time'] *= (1.7 / impact_factor)
                
            elif disruption == 'energy_crisis':
                # Energy crises affect costs and production
                data.loc[i, 'transportation_cost'] *= (1.6 / impact_factor)
                data.loc[i, 'production_capacity'] *= impact_factor
        
        # Create labels (all are anomalies)
        labels = np.full(num_samples, -1)
        
        return data, labels
    
    def generate_adversarial_examples(self, num_samples=1000, subtlety='medium'):
        """
        Generate adversarial examples that are designed to be difficult to detect.
        
        Args:
            num_samples (int): Number of samples to generate
            subtlety (str): How subtle the adversarial examples should be ('low', 'medium', 'high')
            
        Returns:
            tuple: (DataFrame with adversarial data, array of labels)
        """
        print(f"Generating {num_samples} adversarial examples with {subtlety} subtlety...")
        
        # Create base data if not provided
        if self.base_data is None:
            data = self._generate_base_data(num_samples)
        else:
            # Sample from base data
            if len(self.base_data) >= num_samples:
                data = self.base_data.sample(num_samples, random_state=self.random_state).copy()
            else:
                # If base data is smaller, sample with replacement
                data = self.base_data.sample(num_samples, replace=True, random_state=self.random_state).copy()
        
        # Define subtlety factors (how close to normal the adversarial examples should be)
        subtlety_factors = {
            'low': {'deviation': 0.3, 'fields': 3},
            'medium': {'deviation': 0.2, 'fields': 2},
            'high': {'deviation': 0.1, 'fields': 1}
        }
        
        deviation = subtlety_factors[subtlety]['deviation']
        num_fields = subtlety_factors[subtlety]['fields']
        
        # Numerical columns to modify
        numerical_cols = ['order_quantity', 'lead_time', 'transportation_cost', 'inventory_level',
                         'supplier_reliability', 'demand_forecast', 'production_capacity', 'quality_rating']
        
        # Generate adversarial examples
        for i in range(num_samples):
            # Select random fields to modify
            fields_to_modify = np.random.choice(numerical_cols, size=num_fields, replace=False)
            
            for field in fields_to_modify:
                # Get the current value
                current_value = data.loc[i, field]
                
                # Determine direction of change (increase or decrease)
                direction = 1 if np.random.random() > 0.5 else -1
                
                # Calculate new value with subtle deviation
                if direction > 0:
                    # Increase value
                    new_value = current_value * (1 + deviation)
                else:
                    # Decrease value
                    new_value = current_value * (1 - deviation)
                
                # Update the field
                data.loc[i, field] = new_value
            
            # Ensure consistency between related fields to make detection harder
            if 'order_quantity' in fields_to_modify and 'demand_forecast' not in fields_to_modify:
                # Adjust demand forecast to be somewhat consistent with order quantity
                data.loc[i, 'demand_forecast'] = data.loc[i, 'order_quantity'] * np.random.uniform(0.9, 1.1)
            
            if 'lead_time' in fields_to_modify and 'supplier_reliability' not in fields_to_modify:
                # Adjust supplier reliability to be somewhat consistent with lead time
                if data.loc[i, 'lead_time'] > data.loc[i, 'lead_time'] * 1.1:
                    data.loc[i, 'supplier_reliability'] *= 0.95
        
        # Create labels (all are anomalies, but subtle ones)
        labels = np.full(num_samples, -1)
        
        return data, labels
    
    def generate_out_of_distribution_samples(self, num_samples=1000):
        """
        Generate out-of-distribution samples that fall outside the normal data distribution.
        
        Args:
            num_samples (int): Number of samples to generate
            
        Returns:
            tuple: (DataFrame with OOD data, array of labels)
        """
        print(f"Generating {num_samples} out-of-distribution samples...")
        
        # Create completely new data with extreme values
        data = pd.DataFrame()
        
        # Generate timestamps
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2023, 12, 31)
        timestamps = [start_date + timedelta(days=np.random.randint(0, (end_date - start_date).days)) 
                     for _ in range(num_samples)]
        data['timestamp'] = timestamps
        
        # Generate categorical features with new categories
        suppliers = ['UnknownSupplierX', 'NewVendor', 'ForeignSupplier', 'EmergencyProvider', 'TemporarySource']
        product_categories = ['NewTech', 'Experimental', 'Prototype', 'CustomOrder', 'SpecialEdition']
        shipping_methods = ['Drone', 'Autonomous', 'Hyperloop', 'SpaceX', 'Teleport']
        regions = ['Arctic', 'DeepSea', 'SpaceStation', 'DesertOutpost', 'MountainPeak']
        
        data['supplier'] = np.random.choice(suppliers, num_samples)
        data['product_category'] = np.random.choice(product_categories, num_samples)
        data['shipping_method'] = np.random.choice(shipping_methods, num_samples)
        data['region'] = np.random.choice(regions, num_samples)
        
        # Generate numerical features with extreme distributions
        # Use heavy-tailed distributions or mixture models
        
        # Order quantity (heavy-tailed distribution)
        data['order_quantity'] = np.random.pareto(1.5, num_samples) * 1000
        
        # Lead time (bimodal distribution)
        bimodal = np.concatenate([
            np.random.normal(5, 1, num_samples // 2),  # Extremely short lead times
            np.random.normal(60, 10, num_samples - num_samples // 2)  # Extremely long lead times
        ])
        np.random.shuffle(bimodal)
        data['lead_time'] = bimodal
        
        # Transportation cost (log-normal distribution with high variance)
        data['transportation_cost'] = np.random.lognormal(7, 1, num_samples)
        
        # Inventory level (mixture of very low and very high)
        inventory = np.concatenate([
            np.random.uniform(0, 10, num_samples // 2),  # Near stockout
            np.random.uniform(10000, 20000, num_samples - num_samples // 2)  # Excessive inventory
        ])
        np.random.shuffle(inventory)
        data['inventory_level'] = inventory
        
        # Supplier reliability (U-shaped distribution - either very low or very high)
        beta_dist = np.random.beta(0.5, 0.5, num_samples)
        data['supplier_reliability'] = beta_dist
        
        # Demand forecast (heavy-tailed distribution)
        data['demand_forecast'] = np.random.pareto(1.2, num_samples) * 800
        
        # Production capacity (mixture of very low and very high)
        capacity = np.concatenate([
            np.random.uniform(10, 50, num_samples // 2),  # Very low capacity
            np.random.uniform(2000, 5000, num_samples - num_samples // 2)  # Excessive capacity
        ])
        np.random.shuffle(capacity)
        data['production_capacity'] = capacity
        
        # Quality rating (U-shaped distribution)
        quality_beta = np.random.beta(0.5, 0.5, num_samples)
        data['quality_rating'] = quality_beta
        
        # Create labels (all are anomalies)
        labels = np.full(num_samples, -1)
        
        return data, labels
    
    def generate_mixed_edge_cases(self, num_samples=1000, mix_ratios=None):
        """
        Generate a mixed dataset of different edge cases.
        
        Args:
            num_samples (int): Total number of samples to generate
            mix_ratios (dict, optional): Ratio of each edge case type
                                        {'disruption': 0.4, 'adversarial': 0.3, 'ood': 0.3}
            
        Returns:
            tuple: (DataFrame with mixed edge cases, array of labels)
        """
        if mix_ratios is None:
            mix_ratios = {'disruption': 0.4, 'adversarial': 0.3, 'ood': 0.3}
        
        # Calculate number of samples for each type
        disruption_samples = int(num_samples * mix_ratios['disruption'])
        adversarial_samples = int(num_samples * mix_ratios['adversarial'])
        ood_samples = num_samples - disruption_samples - adversarial_samples
        
        print(f"Generating mixed edge cases:\n" 
              f"  - {disruption_samples} supply chain disruptions\n"
              f"  - {adversarial_samples} adversarial examples\n"
              f"  - {ood_samples} out-of-distribution samples")
        
        # Generate each type of edge case
        disruption_data, disruption_labels = self.generate_supply_chain_disruptions(
            num_samples=disruption_samples, severity='high')
        
        adversarial_data, adversarial_labels = self.generate_adversarial_examples(
            num_samples=adversarial_samples, subtlety='high')
        
        ood_data, ood_labels = self.generate_out_of_distribution_samples(
            num_samples=ood_samples)
        
        # Add type indicator
        disruption_data['edge_case_type'] = 'disruption'
        adversarial_data['edge_case_type'] = 'adversarial'
        ood_data['edge_case_type'] = 'out_of_distribution'
        
        # Combine datasets
        combined_data = pd.concat([disruption_data, adversarial_data, ood_data], ignore_index=True)
        combined_labels = np.concatenate([disruption_labels, adversarial_labels, ood_labels])
        
        # Shuffle the combined dataset
        shuffle_idx = np.random.permutation(len(combined_data))
        combined_data = combined_data.iloc[shuffle_idx].reset_index(drop=True)
        combined_labels = combined_labels[shuffle_idx]
        
        return combined_data, combined_labels
    
    def _generate_base_data(self, num_samples):
        """
        Generate base normal supply chain data.
        
        Args:
            num_samples (int): Number of samples to generate
            
        Returns:
            DataFrame: Base normal data
        """
        # Generate timestamps
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2023, 12, 31)
        timestamps = [start_date + timedelta(days=np.random.randint(0, (end_date - start_date).days)) 
                     for _ in range(num_samples)]
        
        # Generate normal data
        data = pd.DataFrame({
            'timestamp': timestamps,
            'order_quantity': np.random.normal(500, 50, num_samples),
            'lead_time': np.random.normal(14, 2, num_samples),
            'transportation_cost': np.random.normal(1000, 100, num_samples),
            'inventory_level': np.random.normal(5000, 500, num_samples),
            'supplier_reliability': np.random.normal(0.95, 0.02, num_samples).clip(0, 1),
            'demand_forecast': np.random.normal(450, 40, num_samples),
            'production_capacity': np.random.normal(600, 50, num_samples),
            'quality_rating': np.random.normal(0.92, 0.03, num_samples).clip(0, 1),
        })
        
        # Add categorical features
        suppliers = ['SupplierA', 'SupplierB', 'SupplierC', 'SupplierD']
        product_categories = ['Electronics', 'Clothing', 'Food', 'Furniture', 'Toys']
        shipping_methods = ['Air', 'Sea', 'Road', 'Rail']
        regions = ['North America', 'Europe', 'Asia', 'South America', 'Africa', 'Australia']
        
        data['supplier'] = np.random.choice(suppliers, num_samples)
        data['product_category'] = np.random.choice(product_categories, num_samples)
        data['shipping_method'] = np.random.choice(shipping_methods, num_samples)
        data['region'] = np.random.choice(regions, num_samples)
        
        return data