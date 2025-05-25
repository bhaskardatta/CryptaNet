#!/usr/bin/env python3
"""
CryptaNet Advanced Data Simulator
=================================

This simulator generates realistic supply chain data with controlled anomalies
and pushes data to the CryptaNet backend every 10 seconds.

Features:
- Multiple product categories with realistic parameters
- Configurable anomaly injection rates and types
- Seasonal and time-based variations
- Various organization support
- Real-time dashboard with statistics
- Configurable patterns and scenarios

Usage:
    python3 data_simulator.py [--config config.json] [--interval 10] [--verbose]
"""

import json
import time
import random
import requests
import logging
import argparse
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import numpy as np
from dataclasses import dataclass, asdict
from enum import Enum
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_simulator.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class RiskLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class AnomalyType(Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    QUANTITY = "quantity"
    LOCATION = "location"
    TIMING = "timing"
    QUALITY = "quality"

@dataclass
class ProductTemplate:
    """Template for generating product data"""
    name: str
    category: str
    base_quantity_range: Tuple[int, int]
    temp_range: Tuple[float, float]  # Normal temperature range
    humidity_range: Tuple[float, float]  # Normal humidity range
    locations: List[str]
    quality_grades: List[str]
    suppliers: List[str]
    anomaly_probability: float = 0.1  # 10% chance of anomaly
    seasonal_factor: bool = False

@dataclass
class AnomalyPattern:
    """Pattern for generating anomalies"""
    type: AnomalyType
    severity: RiskLevel
    description: str
    trigger_condition: Dict
    modifications: Dict

class AdvancedDataSimulator:
    def __init__(self, config_file: Optional[str] = None):
        self.config = self._load_config(config_file)
        self.api_url = self.config.get('api_url', 'http://localhost:5004')
        self.organizations = self.config.get('organizations', ['Org1MSP', 'Org2MSP', 'Org3MSP'])
        self.running = False
        self.stats = {
            'total_generated': 0,
            'anomalies_generated': 0,
            'successful_submissions': 0,
            'failed_submissions': 0,
            'start_time': None
        }
        
        # Initialize product templates
        self.product_templates = self._initialize_product_templates()
        
        # Initialize anomaly patterns
        self.anomaly_patterns = self._initialize_anomaly_patterns()
        
        # Initialize warehouse locations
        self.warehouse_locations = self._initialize_locations()
        
        # Current session ID for tracking
        self.session_id = f"SIM_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        logger.info(f"🚀 Advanced Data Simulator initialized - Session: {self.session_id}")

    def _load_config(self, config_file: Optional[str]) -> Dict:
        """Load configuration from file or use defaults"""
        default_config = {
            "api_url": "http://localhost:5004",
            "organizations": ["Org1MSP", "Org2MSP", "Org3MSP"],
            "anomaly_rate": 0.15,  # 15% anomaly rate
            "seasonal_effects": True,
            "time_based_variations": True,
            "authentication": {
                "username": "admin",
                "password": "admin123"
            }
        }
        
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
                logger.info(f"✅ Loaded configuration from {config_file}")
            except Exception as e:
                logger.warning(f"⚠️ Failed to load config file: {e}. Using defaults.")
        
        return default_config

    def _initialize_product_templates(self) -> List[ProductTemplate]:
        """Initialize comprehensive product templates"""
        return [
            # Food & Beverages
            ProductTemplate(
                name="Premium Coffee Beans",
                category="Food & Beverages",
                base_quantity_range=(500, 2000),
                temp_range=(18.0, 25.0),
                humidity_range=(45.0, 65.0),
                locations=["Warehouse A - Section 1", "Climate Storage A", "Distribution Center 1"],
                quality_grades=["A", "B", "C"],
                suppliers=["Brazilian Coffee Co", "Ethiopian Highlands", "Colombian Farms"],
                anomaly_probability=0.12,
                seasonal_factor=True
            ),
            ProductTemplate(
                name="Frozen Food Products",
                category="Food & Beverages",
                base_quantity_range=(200, 800),
                temp_range=(-18.0, -12.0),  # Frozen requirements
                humidity_range=(40.0, 60.0),
                locations=["Cold Storage - Section 1", "Cold Storage - Section 2", "Freezer Unit A"],
                quality_grades=["A", "B"],
                suppliers=["FrozenFresh Inc", "Arctic Foods", "CryoSupply"],
                anomaly_probability=0.25,  # Higher anomaly rate for temperature-sensitive
                seasonal_factor=True
            ),
            ProductTemplate(
                name="Fresh Produce",
                category="Food & Beverages",
                base_quantity_range=(300, 1200),
                temp_range=(2.0, 8.0),
                humidity_range=(85.0, 95.0),
                locations=["Fresh Storage A", "Refrigerated Bay 1", "Produce Center"],
                quality_grades=["Premium", "Standard", "Economy"],
                suppliers=["Fresh Farm Co", "Organic Growers", "Valley Produce"],
                anomaly_probability=0.20,
                seasonal_factor=True
            ),
            
            # Electronics
            ProductTemplate(
                name="Sensitive Electronics",
                category="Electronics",
                base_quantity_range=(50, 300),
                temp_range=(18.0, 24.0),
                humidity_range=(30.0, 50.0),  # Low humidity critical
                locations=["Electronics Warehouse", "Clean Room Storage", "Tech Bay A"],
                quality_grades=["Grade A", "Grade B"],
                suppliers=["TechCorp Industries", "ElectroSupply", "Digital Components"],
                anomaly_probability=0.18,
                seasonal_factor=False
            ),
            ProductTemplate(
                name="Mobile Devices",
                category="Electronics",
                base_quantity_range=(100, 500),
                temp_range=(15.0, 30.0),
                humidity_range=(35.0, 60.0),
                locations=["Mobile Storage Unit", "Electronics Bay B", "Secure Storage 1"],
                quality_grades=["New", "Refurbished"],
                suppliers=["Mobile Solutions Inc", "Device Distributors", "TechGlobal"],
                anomaly_probability=0.10,
                seasonal_factor=True
            ),
            
            # Pharmaceuticals
            ProductTemplate(
                name="Pharmaceutical Products",
                category="Pharmaceuticals",
                base_quantity_range=(100, 600),
                temp_range=(15.0, 25.0),
                humidity_range=(30.0, 50.0),
                locations=["Pharma Storage A", "Climate Control Unit", "Medical Warehouse"],
                quality_grades=["Batch A", "Batch B"],
                suppliers=["PharmaCorp", "MedSupply International", "Healthcare Solutions"],
                anomaly_probability=0.08,  # Lower tolerance for pharma
                seasonal_factor=False
            ),
            ProductTemplate(
                name="Temperature Sensitive Medicine",
                category="Pharmaceuticals",
                base_quantity_range=(50, 200),
                temp_range=(2.0, 8.0),  # Refrigerated
                humidity_range=(30.0, 45.0),
                locations=["Pharma Cold Storage", "Medical Refrigeration", "Bio Storage"],
                quality_grades=["Critical", "Standard"],
                suppliers=["BioMed Corp", "CryoMedical", "Precision Pharma"],
                anomaly_probability=0.30,  # High sensitivity
                seasonal_factor=False
            ),
            
            # Industrial
            ProductTemplate(
                name="Industrial Components",
                category="Industrial",
                base_quantity_range=(200, 1000),
                temp_range=(10.0, 35.0),
                humidity_range=(40.0, 70.0),
                locations=["Industrial Bay 1", "Heavy Storage", "Manufacturing Unit"],
                quality_grades=["Grade 1", "Grade 2", "Grade 3"],
                suppliers=["Industrial Supply Co", "Manufacturing Parts", "Heavy Industries"],
                anomaly_probability=0.05,
                seasonal_factor=False
            ),
            
            # Textiles
            ProductTemplate(
                name="Clothing Items",
                category="Textiles",
                base_quantity_range=(800, 3000),
                temp_range=(18.0, 28.0),
                humidity_range=(45.0, 65.0),
                locations=["Textile Warehouse", "Clothing Storage", "Fashion Center"],
                quality_grades=["Premium", "Standard", "Budget"],
                suppliers=["Fashion Textiles", "Global Garments", "Style Solutions"],
                anomaly_probability=0.05,
                seasonal_factor=True
            ),
            
            # Automotive
            ProductTemplate(
                name="Automotive Parts",
                category="Automotive",
                base_quantity_range=(100, 800),
                temp_range=(15.0, 30.0),
                humidity_range=(40.0, 65.0),
                locations=["Auto Parts Warehouse", "Vehicle Storage", "Parts Distribution"],
                quality_grades=["OEM", "Aftermarket", "Refurbished"],
                suppliers=["AutoParts Inc", "Vehicle Solutions", "Motor Supply"],
                anomaly_probability=0.07,
                seasonal_factor=False
            )
        ]

    def _initialize_anomaly_patterns(self) -> List[AnomalyPattern]:
        """Initialize various anomaly patterns"""
        return [
            # Temperature Anomalies
            AnomalyPattern(
                type=AnomalyType.TEMPERATURE,
                severity=RiskLevel.HIGH,
                description="Extreme High Temperature",
                trigger_condition={"probability": 0.3},
                modifications={"temperature_offset": (15.0, 25.0)}
            ),
            AnomalyPattern(
                type=AnomalyType.TEMPERATURE,
                severity=RiskLevel.CRITICAL,
                description="Freezer Failure",
                trigger_condition={"category": "Frozen", "probability": 0.15},
                modifications={"temperature_set": (20.0, 35.0)}
            ),
            AnomalyPattern(
                type=AnomalyType.TEMPERATURE,
                severity=RiskLevel.MEDIUM,
                description="Slight Temperature Variance",
                trigger_condition={"probability": 0.5},
                modifications={"temperature_offset": (5.0, 10.0)}
            ),
            
            # Humidity Anomalies
            AnomalyPattern(
                type=AnomalyType.HUMIDITY,
                severity=RiskLevel.HIGH,
                description="Excessive Humidity",
                trigger_condition={"category": "Electronics", "probability": 0.4},
                modifications={"humidity_offset": (20.0, 40.0)}
            ),
            AnomalyPattern(
                type=AnomalyType.HUMIDITY,
                severity=RiskLevel.CRITICAL,
                description="Humidity Control Failure",
                trigger_condition={"probability": 0.1},
                modifications={"humidity_set": (85.0, 95.0)}
            ),
            
            # Quantity Anomalies
            AnomalyPattern(
                type=AnomalyType.QUANTITY,
                severity=RiskLevel.MEDIUM,
                description="Inventory Discrepancy",
                trigger_condition={"probability": 0.2},
                modifications={"quantity_multiplier": (0.1, 0.7)}
            ),
            AnomalyPattern(
                type=AnomalyType.QUANTITY,
                severity=RiskLevel.HIGH,
                description="Significant Shortage",
                trigger_condition={"probability": 0.1},
                modifications={"quantity_multiplier": (0.05, 0.3)}
            ),
            
            # Location Anomalies
            AnomalyPattern(
                type=AnomalyType.LOCATION,
                severity=RiskLevel.MEDIUM,
                description="Unauthorized Location",
                trigger_condition={"probability": 0.05},
                modifications={"location_override": ["Unknown Location", "Unauthorized Area", "Misplaced Storage"]}
            )
        ]

    def _initialize_locations(self) -> List[str]:
        """Initialize additional warehouse locations"""
        return [
            "Warehouse A - Section 1", "Warehouse A - Section 2", "Warehouse A - Section 3",
            "Warehouse B - Section 1", "Warehouse B - Section 2", "Warehouse B - Section 3",
            "Warehouse C - Section 1", "Warehouse C - Section 2", "Warehouse C - Section 3",
            "Cold Storage - Section 1", "Cold Storage - Section 2", "Cold Storage - Section 3",
            "Climate Control Unit A", "Climate Control Unit B", "Climate Control Unit C",
            "Distribution Center 1", "Distribution Center 2", "Distribution Center 3",
            "Loading Dock A", "Loading Dock B", "Loading Dock C",
            "Quarantine Area", "Quality Control Lab", "Secure Storage",
            "Emergency Storage", "Overflow Area", "Transit Bay"
        ]

    def _get_auth_token(self) -> Optional[str]:
        """Get authentication token from the backend"""
        try:
            auth_config = self.config.get('authentication', {})
            response = requests.post(
                f"{self.api_url}/api/auth/login",
                json={
                    'username': auth_config.get('username', 'admin'),
                    'password': auth_config.get('password', 'admin123')
                },
                timeout=10
            )
            
            if response.status_code == 200:
                token = response.json().get('token')
                logger.info("✅ Successfully authenticated with backend")
                return token
            else:
                logger.warning(f"⚠️ Authentication failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.warning(f"⚠️ Authentication error: {e}")
            return None

    def _apply_seasonal_effects(self, data: Dict, template: ProductTemplate) -> Dict:
        """Apply seasonal variations to data"""
        if not template.seasonal_factor or not self.config.get('seasonal_effects', True):
            return data
        
        # Get current month to determine season
        month = datetime.now().month
        
        # Define seasonal factors
        if template.category == "Food & Beverages":
            if month in [12, 1, 2]:  # Winter - higher demand for hot beverages, preserved foods
                if "Coffee" in template.name:
                    data['quantity'] = int(data['quantity'] * 1.3)
                elif "Frozen" in template.name:
                    data['quantity'] = int(data['quantity'] * 1.1)
            elif month in [6, 7, 8]:  # Summer - fresh produce, cold items
                if "Fresh" in template.name:
                    data['quantity'] = int(data['quantity'] * 1.4)
                    data['temperature'] += random.uniform(1.0, 3.0)
                elif "Frozen" in template.name:
                    data['quantity'] = int(data['quantity'] * 1.2)
        
        elif template.category == "Electronics":
            if month in [11, 12]:  # Holiday season
                data['quantity'] = int(data['quantity'] * 1.5)
        
        elif template.category == "Textiles":
            if month in [3, 4, 9, 10]:  # Fashion seasons
                data['quantity'] = int(data['quantity'] * 1.3)
        
        return data

    def _apply_time_based_variations(self, data: Dict) -> Dict:
        """Apply time-of-day and day-of-week variations"""
        if not self.config.get('time_based_variations', True):
            return data
        
        current_time = datetime.now()
        hour = current_time.hour
        day_of_week = current_time.weekday()  # 0 = Monday, 6 = Sunday
        
        # Business hours effect (9 AM to 5 PM, Monday to Friday)
        if day_of_week < 5 and 9 <= hour <= 17:
            # Higher activity during business hours
            data['quantity'] = int(data['quantity'] * random.uniform(1.1, 1.3))
        elif day_of_week >= 5:  # Weekend
            # Lower activity on weekends
            data['quantity'] = int(data['quantity'] * random.uniform(0.7, 0.9))
        elif hour < 6 or hour > 22:  # Night hours
            # Minimal activity at night
            data['quantity'] = int(data['quantity'] * random.uniform(0.5, 0.8))
        
        return data

    def _generate_anomaly(self, data: Dict, template: ProductTemplate) -> Tuple[Dict, bool, str]:
        """Generate anomaly based on patterns and template"""
        # Check if anomaly should be generated
        if random.random() > template.anomaly_probability:
            return data, False, ""
        
        # Select applicable anomaly patterns
        applicable_patterns = []
        for pattern in self.anomaly_patterns:
            trigger = pattern.trigger_condition
            
            # Check category match
            if 'category' in trigger:
                if trigger['category'].lower() not in template.category.lower():
                    continue
            
            # Check probability
            if random.random() <= trigger.get('probability', 1.0):
                applicable_patterns.append(pattern)
        
        if not applicable_patterns:
            return data, False, ""
        
        # Select random pattern
        pattern = random.choice(applicable_patterns)
        anomaly_data = data.copy()
        
        # Apply modifications
        mods = pattern.modifications
        
        if 'temperature_offset' in mods:
            offset_range = mods['temperature_offset']
            offset = random.uniform(offset_range[0], offset_range[1])
            anomaly_data['temperature'] += offset
        
        if 'temperature_set' in mods:
            temp_range = mods['temperature_set']
            anomaly_data['temperature'] = random.uniform(temp_range[0], temp_range[1])
        
        if 'humidity_offset' in mods:
            offset_range = mods['humidity_offset']
            offset = random.uniform(offset_range[0], offset_range[1])
            anomaly_data['humidity'] += offset
        
        if 'humidity_set' in mods:
            humidity_range = mods['humidity_set']
            anomaly_data['humidity'] = random.uniform(humidity_range[0], humidity_range[1])
        
        if 'quantity_multiplier' in mods:
            mult_range = mods['quantity_multiplier']
            multiplier = random.uniform(mult_range[0], mult_range[1])
            anomaly_data['quantity'] = max(1, int(anomaly_data['quantity'] * multiplier))
        
        if 'location_override' in mods:
            anomaly_data['location'] = random.choice(mods['location_override'])
        
        # Ensure values are within reasonable bounds
        anomaly_data['temperature'] = max(-30.0, min(60.0, anomaly_data['temperature']))
        anomaly_data['humidity'] = max(0.0, min(100.0, anomaly_data['humidity']))
        anomaly_data['quantity'] = max(1, anomaly_data['quantity'])
        
        self.stats['anomalies_generated'] += 1
        
        return anomaly_data, True, f"{pattern.severity.value}: {pattern.description}"

    def _generate_supply_chain_data(self) -> Tuple[Dict, bool, str]:
        """Generate a single supply chain data point"""
        # Select random template
        template = random.choice(self.product_templates)
        
        # Generate base data
        quantity = random.randint(template.base_quantity_range[0], template.base_quantity_range[1])
        temperature = random.uniform(template.temp_range[0], template.temp_range[1])
        humidity = random.uniform(template.humidity_range[0], template.humidity_range[1])
        location = random.choice(template.locations)
        quality = random.choice(template.quality_grades)
        supplier = random.choice(template.suppliers)
        
        # Generate product ID with some variation
        product_variants = [
            template.name,
            f"{template.name} - Premium",
            f"{template.name} - Standard",
            f"{template.name} - Economy"
        ]
        product_name = random.choice(product_variants)
        
        # Create base data
        data = {
            'productId': f"{template.category[:3].upper()}-{random.randint(1000, 9999)}",
            'product': product_name,
            'quantity': quantity,
            'location': location,
            'temperature': round(temperature, 1),
            'humidity': round(humidity, 1),
            'timestamp': datetime.now().isoformat(),
            'batchNumber': f"BATCH{random.randint(1000, 9999)}",
            'quality': quality,
            'metadata': {
                'supplier': supplier,
                'category': template.category,
                'session_id': self.session_id,
                'simulator_version': '2.0'
            }
        }
        
        # Apply seasonal effects
        data = self._apply_seasonal_effects(data, template)
        
        # Apply time-based variations
        data = self._apply_time_based_variations(data)
        
        # Check for anomalies
        data, is_anomaly, anomaly_description = self._generate_anomaly(data, template)
        
        self.stats['total_generated'] += 1
        
        return data, is_anomaly, anomaly_description

    def _submit_data_to_api(self, data: Dict, organization_id: str, token: Optional[str] = None) -> bool:
        """Submit data to the CryptaNet API"""
        try:
            headers = {'Content-Type': 'application/json'}
            if token:
                headers['Authorization'] = f'Bearer {token}'
            
            payload = {
                'organizationId': organization_id,
                'dataType': 'supply_chain',
                'data': data
            }
            
            response = requests.post(
                f"{self.api_url}/api/supply-chain/submit",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success', False):
                    self.stats['successful_submissions'] += 1
                    return True
                else:
                    logger.error(f"❌ API Error: {result.get('error', 'Unknown error')}")
                    self.stats['failed_submissions'] += 1
                    return False
            else:
                logger.error(f"❌ HTTP Error {response.status_code}: {response.text}")
                self.stats['failed_submissions'] += 1
                return False
                
        except Exception as e:
            logger.error(f"❌ Request Error: {e}")
            self.stats['failed_submissions'] += 1
            return False

    def _print_stats(self):
        """Print current simulation statistics"""
        if self.stats['start_time']:
            runtime = datetime.now() - self.stats['start_time']
            rate = self.stats['total_generated'] / max(runtime.total_seconds(), 1) * 60  # per minute
            anomaly_rate = (self.stats['anomalies_generated'] / max(self.stats['total_generated'], 1)) * 100
            success_rate = (self.stats['successful_submissions'] / max(self.stats['total_generated'], 1)) * 100
            
            print(f"\n{'='*60}")
            print(f"📊 CryptaNet Data Simulator Statistics")
            print(f"{'='*60}")
            print(f"🕐 Runtime: {str(runtime).split('.')[0]}")
            print(f"📦 Total Generated: {self.stats['total_generated']}")
            print(f"⚠️ Anomalies: {self.stats['anomalies_generated']} ({anomaly_rate:.1f}%)")
            print(f"✅ Successful: {self.stats['successful_submissions']} ({success_rate:.1f}%)")
            print(f"❌ Failed: {self.stats['failed_submissions']}")
            print(f"📈 Generation Rate: {rate:.1f} records/minute")
            print(f"{'='*60}\n")

    def _monitor_stats(self):
        """Background thread to print statistics periodically"""
        while self.running:
            time.sleep(60)  # Print stats every minute
            if self.running:
                self._print_stats()

    def run_simulation(self, interval: int = 10, max_records: Optional[int] = None):
        """Run the continuous data simulation"""
        logger.info(f"🚀 Starting CryptaNet Data Simulator")
        logger.info(f"⏱️ Interval: {interval} seconds")
        logger.info(f"🏢 Organizations: {', '.join(self.organizations)}")
        logger.info(f"📍 API Endpoint: {self.api_url}")
        
        if max_records:
            logger.info(f"🎯 Target Records: {max_records}")
        
        # Get authentication token
        token = self._get_auth_token()
        
        self.running = True
        self.stats['start_time'] = datetime.now()
        
        # Start stats monitoring thread
        stats_thread = threading.Thread(target=self._monitor_stats, daemon=True)
        stats_thread.start()
        
        try:
            while self.running:
                if max_records and self.stats['total_generated'] >= max_records:
                    logger.info(f"🎯 Reached target of {max_records} records. Stopping simulation.")
                    break
                
                # Generate data
                data, is_anomaly, anomaly_desc = self._generate_supply_chain_data()
                
                # Select random organization
                organization = random.choice(self.organizations)
                
                # Log the data being generated
                status_emoji = "🔥" if is_anomaly else "📦"
                logger.info(f"{status_emoji} Generated: {data['productId']} - {data['product'][:30]}...")
                
                if is_anomaly:
                    logger.warning(f"⚠️ Anomaly: {anomaly_desc}")
                
                # Submit to API
                success = self._submit_data_to_api(data, organization, token)
                
                if success:
                    logger.info(f"✅ Successfully submitted to {organization}")
                else:
                    logger.error(f"❌ Failed to submit to {organization}")
                
                # Wait for next iteration
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("🛑 Simulation stopped by user")
        except Exception as e:
            logger.error(f"💥 Simulation error: {e}")
        finally:
            self.running = False
            self._print_stats()
            logger.info("🏁 Simulation ended")

def main():
    parser = argparse.ArgumentParser(description='CryptaNet Advanced Data Simulator')
    parser.add_argument('--config', '-c', help='Configuration file path')
    parser.add_argument('--interval', '-i', type=int, default=10, help='Interval between data points (seconds)')
    parser.add_argument('--max-records', '-m', type=int, help='Maximum number of records to generate')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        simulator = AdvancedDataSimulator(args.config)
        simulator.run_simulation(args.interval, args.max_records)
    except Exception as e:
        logger.error(f"💥 Failed to start simulator: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
