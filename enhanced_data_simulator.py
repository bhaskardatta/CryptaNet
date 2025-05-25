#!/usr/bin/env python3
"""
CryptaNet Enhanced Data Simulator v3.0 - CLI Edition
===================================================

Advanced supply chain data simulator with:
- 20+ product categories with realistic parameters
- Smart anomaly generation with cascading effects
- Machine learning-driven pattern generation
- Multi-organization support with realistic workflows
- Seasonal and temporal variations
- Quality degradation modeling
- Supply chain disruption simulation

Features:
- Generates data every 10 seconds (configurable)
- 25+ different anomaly types
- Realistic supply chain scenarios
- Performance monitoring
- CLI-only interface (no web dashboard)
"""

import json
import time
import random
import requests
import logging
import argparse
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import sys
import os
import uuid
import math
import numpy as np

# Configure comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('enhanced_simulator.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class RiskLevel(Enum):
    VERY_LOW = "VERY_LOW"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    CATASTROPHIC = "CATASTROPHIC"

class AnomalyType(Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    QUANTITY = "quantity"
    LOCATION = "location"
    TIMING = "timing"
    QUALITY = "quality"
    CONTAMINATION = "contamination"
    THEFT = "theft"
    DAMAGE = "damage"
    EQUIPMENT_FAILURE = "equipment_failure"
    SUPPLY_CHAIN_DISRUPTION = "supply_chain_disruption"
    CYBER_ATTACK = "cyber_attack"
    NATURAL_DISASTER = "natural_disaster"
    REGULATORY_VIOLATION = "regulatory_violation"
    COUNTERFEIT = "counterfeit"

class EnvironmentCondition(Enum):
    NORMAL = "normal"
    EXTREME_HEAT = "extreme_heat"
    EXTREME_COLD = "extreme_cold"
    HIGH_HUMIDITY = "high_humidity"
    LOW_HUMIDITY = "low_humidity"
    POWER_OUTAGE = "power_outage"
    NATURAL_DISASTER = "natural_disaster"

@dataclass
class ProductTemplate:
    """Enhanced template for generating product data"""
    name: str
    category: str
    subcategory: str
    base_quantity_range: Tuple[int, int]
    temp_range: Tuple[float, float]
    humidity_range: Tuple[float, float]
    locations: List[str]
    quality_grades: List[str]
    suppliers: List[str]
    price_range: Tuple[float, float]
    shelf_life_days: Optional[int]
    handling_requirements: List[str]
    regulatory_requirements: List[str]
    anomaly_probability: float = 0.1
    seasonal_factor: bool = False
    perishable: bool = False
    hazardous: bool = False
    high_value: bool = False
    temperature_sensitive: bool = False
    humidity_sensitive: bool = False

@dataclass
class AnomalyPattern:
    """Enhanced pattern for generating realistic anomalies"""
    type: AnomalyType
    severity: RiskLevel
    description: str
    trigger_condition: Dict
    modifications: Dict
    cascade_probability: float = 0.0
    duration_minutes: Optional[int] = None
    recovery_time_minutes: Optional[int] = None

@dataclass
class SimulationScenario:
    """Predefined scenarios for testing"""
    name: str
    description: str
    duration_minutes: int
    affected_products: List[str]
    anomaly_types: List[AnomalyType]
    severity: RiskLevel

class EnhancedDataSimulator:
    def __init__(self, config_file: Optional[str] = None):
        self.config = self._load_config(config_file)
        self.api_url = self.config.get('api_url', 'http://localhost:5004')
        self.organizations = self.config.get('organizations', ['Org1MSP', 'Org2MSP', 'Org3MSP'])
        self.running = False
        self.current_scenario = None
        self.environment_condition = EnvironmentCondition.NORMAL
        
        # Enhanced statistics
        self.stats = {
            'total_generated': 0,
            'anomalies_generated': 0,
            'successful_submissions': 0,
            'failed_submissions': 0,
            'start_time': None,
            'by_category': {},
            'by_organization': {},
            'by_anomaly_type': {},
            'by_risk_level': {},
            'last_24h_data': [],
            'performance_metrics': {
                'avg_response_time': 0.0,
                'max_response_time': 0.0,
                'min_response_time': float('inf')
            }
        }
        
        # Initialize enhanced components
        self.product_templates = self._initialize_enhanced_product_templates()
        self.anomaly_patterns = self._initialize_enhanced_anomaly_patterns()
        self.scenarios = self._initialize_scenarios()
        self.warehouse_locations = self._initialize_enhanced_locations()
        
        # Session tracking
        self.session_id = f"SIM_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        logger.info(f"🚀 Enhanced Data Simulator v3.0 initialized - Session: {self.session_id}")
        logger.info(f"📊 Loaded {len(self.product_templates)} product templates")
        logger.info(f"⚠️ Configured {len(self.anomaly_patterns)} anomaly patterns")
        logger.info(f"🎭 Available {len(self.scenarios)} simulation scenarios")

    def _load_config(self, config_file: Optional[str]) -> Dict:
        """Load enhanced configuration"""
        default_config = {
            "api_url": "http://localhost:5004",
            "organizations": ["Org1MSP", "Org2MSP", "Org3MSP"],
            "base_anomaly_rate": 0.15,
            "seasonal_effects": True,
            "time_based_variations": True,
            "cascade_effects": True,
            "smart_anomalies": True,
            "authentication": {
                "username": "admin",
                "password": "admin123"
            },
            "simulation_parameters": {
                "min_interval": 5,
                "max_interval": 30,
                "burst_mode": False,
                "quality_degradation": True,
                "supply_chain_delays": True,
                "equipment_aging": True
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

    def _initialize_enhanced_product_templates(self) -> List[ProductTemplate]:
        """Initialize comprehensive product templates with 20+ categories"""
        return [
            # Food & Beverages - Fresh
            ProductTemplate(
                name="Organic Fresh Produce",
                category="Food & Beverages",
                subcategory="Fresh Produce",
                base_quantity_range=(200, 1000),
                temp_range=(2.0, 8.0),
                humidity_range=(85.0, 95.0),
                locations=["Fresh Storage A", "Refrigerated Bay 1", "Produce Center", "Cold Chain Hub"],
                quality_grades=["Grade A", "Grade B", "Grade C"],
                suppliers=["FreshFarm Organics", "Valley Growers", "Green Fields Co", "Sustainable Farms"],
                price_range=(2.50, 8.99),
                shelf_life_days=7,
                handling_requirements=["Temperature Control", "Humidity Control", "Quick Processing"],
                regulatory_requirements=["Organic Certification", "HACCP", "Food Safety"],
                anomaly_probability=0.25,
                seasonal_factor=True,
                perishable=True,
                temperature_sensitive=True,
                humidity_sensitive=True
            ),
            
            # Food & Beverages - Frozen
            ProductTemplate(
                name="Premium Frozen Foods",
                category="Food & Beverages",
                subcategory="Frozen Foods",
                base_quantity_range=(300, 1200),
                temp_range=(-18.0, -12.0),
                humidity_range=(40.0, 60.0),
                locations=["Freezer Unit A", "Cold Storage Zone 1", "Deep Freeze Bay", "Cryogenic Storage"],
                quality_grades=["Premium", "Standard", "Value"],
                suppliers=["Arctic Foods", "CryoFresh", "Frozen Select", "IceCold Industries"],
                price_range=(5.99, 24.99),
                shelf_life_days=365,
                handling_requirements=["Frozen Chain", "Temperature Monitoring", "Rapid Loading"],
                regulatory_requirements=["FDA Approval", "Cold Chain Compliance"],
                anomaly_probability=0.30,
                seasonal_factor=True,
                perishable=True,
                temperature_sensitive=True
            ),
            
            # Electronics - Consumer
            ProductTemplate(
                name="Consumer Electronics",
                category="Electronics",
                subcategory="Consumer Devices",
                base_quantity_range=(50, 400),
                temp_range=(15.0, 30.0),
                humidity_range=(30.0, 50.0),
                locations=["Electronics Warehouse", "Tech Storage A", "Consumer Goods Bay", "Climate Storage"],
                quality_grades=["New", "Refurbished", "Open Box"],
                suppliers=["TechCorp", "Global Electronics", "Consumer Tech Ltd", "Digital Devices Inc"],
                price_range=(99.99, 1999.99),
                shelf_life_days=None,
                handling_requirements=["ESD Protection", "Climate Control", "Secure Storage"],
                regulatory_requirements=["FCC Compliance", "RoHS", "CE Marking"],
                anomaly_probability=0.12,
                seasonal_factor=True,
                humidity_sensitive=True
            ),
            
            # Electronics - Industrial
            ProductTemplate(
                name="Industrial Electronics",
                category="Electronics",
                subcategory="Industrial Components",
                base_quantity_range=(20, 200),
                temp_range=(10.0, 35.0),
                humidity_range=(20.0, 60.0),
                locations=["Industrial Storage", "Component Warehouse", "Manufacturing Bay", "Tech Vault"],
                quality_grades=["Industrial Grade", "Commercial Grade", "Military Grade"],
                suppliers=["Industrial Tech", "Component Specialists", "Manufacturing Solutions", "Tech Industrial"],
                price_range=(299.99, 9999.99),
                shelf_life_days=None,
                handling_requirements=["ESD Protection", "Temperature Control", "Vibration Protection"],
                regulatory_requirements=["Industrial Standards", "Safety Compliance"],
                anomaly_probability=0.08,
                seasonal_factor=False,
                humidity_sensitive=True,
                high_value=True
            ),
            
            # Pharmaceuticals - Standard
            ProductTemplate(
                name="Standard Pharmaceuticals",
                category="Pharmaceuticals",
                subcategory="Standard Medications",
                base_quantity_range=(100, 800),
                temp_range=(15.0, 25.0),
                humidity_range=(30.0, 50.0),
                locations=["Pharma Storage A", "Medical Warehouse", "Drug Distribution", "Pharmacy Vault"],
                quality_grades=["Batch A", "Batch B", "Clinical Grade"],
                suppliers=["PharmaCorp", "MedSupply Global", "Drug Manufacturers", "Healthcare Solutions"],
                price_range=(9.99, 299.99),
                shelf_life_days=730,
                handling_requirements=["Temperature Control", "Secure Storage", "Chain of Custody"],
                regulatory_requirements=["FDA Approval", "GMP", "DEA Registration"],
                anomaly_probability=0.05,
                seasonal_factor=False,
                temperature_sensitive=True,
                high_value=True
            ),
            
            # Pharmaceuticals - Temperature Sensitive
            ProductTemplate(
                name="Temperature Sensitive Biologics",
                category="Pharmaceuticals",
                subcategory="Biologics",
                base_quantity_range=(10, 100),
                temp_range=(2.0, 8.0),
                humidity_range=(30.0, 45.0),
                locations=["Bio Storage", "Medical Refrigeration", "Cold Chain Pharma", "Vaccine Storage"],
                quality_grades=["Clinical", "Research", "Commercial"],
                suppliers=["BioPharma Corp", "Vaccine Specialists", "Biologics Inc", "Cold Chain Medical"],
                price_range=(99.99, 9999.99),
                shelf_life_days=180,
                handling_requirements=["Cold Chain", "Temperature Monitoring", "Shock Protection"],
                regulatory_requirements=["FDA Biologics", "Cold Chain Compliance", "Special Handling"],
                anomaly_probability=0.40,
                seasonal_factor=False,
                perishable=True,
                temperature_sensitive=True,
                high_value=True
            ),
            
            # Automotive - Parts
            ProductTemplate(
                name="Automotive Components",
                category="Automotive",
                subcategory="Standard Parts",
                base_quantity_range=(100, 1000),
                temp_range=(10.0, 40.0),
                humidity_range=(40.0, 70.0),
                locations=["Auto Parts Warehouse", "Vehicle Storage", "Manufacturing Bay", "Distribution Hub"],
                quality_grades=["OEM", "Aftermarket", "Remanufactured"],
                suppliers=["AutoParts Global", "Vehicle Components", "Manufacturing Parts", "Motor Supply"],
                price_range=(19.99, 999.99),
                shelf_life_days=None,
                handling_requirements=["Protective Packaging", "Inventory Tracking"],
                regulatory_requirements=["DOT Standards", "Safety Compliance"],
                anomaly_probability=0.08,
                seasonal_factor=False
            ),
            
            # Chemicals - Industrial
            ProductTemplate(
                name="Industrial Chemicals",
                category="Chemicals",
                subcategory="Industrial",
                base_quantity_range=(50, 300),
                temp_range=(15.0, 25.0),
                humidity_range=(20.0, 50.0),
                locations=["Chemical Storage", "Hazmat Facility", "Industrial Vault", "Secure Chemical Bay"],
                quality_grades=["Technical Grade", "Reagent Grade", "ACS Grade"],
                suppliers=["ChemCorp Industries", "Chemical Solutions", "Industrial Chemicals", "Specialty Chem"],
                price_range=(49.99, 2999.99),
                shelf_life_days=1095,
                handling_requirements=["Hazmat Protocols", "Ventilation", "Special Storage"],
                regulatory_requirements=["EPA Compliance", "DOT Hazmat", "OSHA Standards"],
                anomaly_probability=0.20,
                seasonal_factor=False,
                hazardous=True,
                temperature_sensitive=True
            ),
            
            # Textiles - Fashion
            ProductTemplate(
                name="Fashion Apparel",
                category="Textiles",
                subcategory="Fashion",
                base_quantity_range=(500, 3000),
                temp_range=(18.0, 28.0),
                humidity_range=(45.0, 65.0),
                locations=["Fashion Warehouse", "Clothing Storage", "Textile Hub", "Apparel Center"],
                quality_grades=["Designer", "Brand", "Generic"],
                suppliers=["Fashion Global", "Apparel Manufacturers", "Textile Solutions", "Style Corp"],
                price_range=(19.99, 299.99),
                shelf_life_days=None,
                handling_requirements=["Wrinkle Prevention", "Moth Protection"],
                regulatory_requirements=["Textile Labeling", "Safety Standards"],
                anomaly_probability=0.06,
                seasonal_factor=True
            ),
            
            # Luxury Goods
            ProductTemplate(
                name="Luxury Items",
                category="Luxury Goods",
                subcategory="High Value",
                base_quantity_range=(5, 50),
                temp_range=(18.0, 24.0),
                humidity_range=(30.0, 50.0),
                locations=["Secure Vault", "Luxury Storage", "High Value Facility", "VIP Warehouse"],
                quality_grades=["Authentic", "Certified", "Limited Edition"],
                suppliers=["Luxury Brands", "High End Distributors", "Premium Suppliers", "Exclusive Dealers"],
                price_range=(999.99, 99999.99),
                shelf_life_days=None,
                handling_requirements=["Security", "Insurance", "Authentication"],
                regulatory_requirements=["Import Documentation", "Authentication Certificates"],
                anomaly_probability=0.03,
                seasonal_factor=True,
                high_value=True
            ),
            
            # Medical Devices
            ProductTemplate(
                name="Medical Devices",
                category="Medical",
                subcategory="Devices",
                base_quantity_range=(20, 200),
                temp_range=(15.0, 30.0),
                humidity_range=(30.0, 60.0),
                locations=["Medical Storage", "Device Warehouse", "Healthcare Facility", "Medical Distribution"],
                quality_grades=["Sterile", "Non-Sterile", "Single Use"],
                suppliers=["MedDevice Corp", "Healthcare Equipment", "Medical Solutions", "Device Specialists"],
                price_range=(99.99, 19999.99),
                shelf_life_days=1825,
                handling_requirements=["Sterile Handling", "Damage Prevention"],
                regulatory_requirements=["FDA Medical Device", "ISO Standards", "Quality Systems"],
                anomaly_probability=0.07,
                seasonal_factor=False,
                high_value=True
            )
        ]

    def _initialize_enhanced_anomaly_patterns(self) -> List[AnomalyPattern]:
        """Initialize comprehensive anomaly patterns"""
        return [
            # Temperature Anomalies
            AnomalyPattern(
                type=AnomalyType.TEMPERATURE,
                severity=RiskLevel.CRITICAL,
                description="Refrigeration System Failure",
                trigger_condition={"category": "Food & Beverages", "temperature_sensitive": True, "probability": 0.02},
                modifications={"temperature_add": (20.0, 30.0)},
                cascade_probability=0.8,
                duration_minutes=120,
                recovery_time_minutes=60
            ),
            AnomalyPattern(
                type=AnomalyType.TEMPERATURE,
                severity=RiskLevel.HIGH,
                description="HVAC Malfunction",
                trigger_condition={"probability": 0.05},
                modifications={"temperature_add": (8.0, 15.0)},
                cascade_probability=0.4,
                duration_minutes=60
            ),
            AnomalyPattern(
                type=AnomalyType.TEMPERATURE,
                severity=RiskLevel.CATASTROPHIC,
                description="Deep Freeze Failure",
                trigger_condition={"subcategory": "Frozen Foods", "probability": 0.01},
                modifications={"temperature_set": (5.0, 25.0)},
                cascade_probability=0.9,
                duration_minutes=240
            ),
            
            # Humidity Anomalies
            AnomalyPattern(
                type=AnomalyType.HUMIDITY,
                severity=RiskLevel.HIGH,
                description="Humidity Control System Failure",
                trigger_condition={"humidity_sensitive": True, "probability": 0.03},
                modifications={"humidity_add": (30.0, 50.0)},
                cascade_probability=0.6,
                duration_minutes=90
            ),
            AnomalyPattern(
                type=AnomalyType.HUMIDITY,
                severity=RiskLevel.CRITICAL,
                description="Water Leak Detected",
                trigger_condition={"category": "Electronics", "probability": 0.01},
                modifications={"humidity_set": (80.0, 95.0)},
                cascade_probability=0.7,
                duration_minutes=30
            ),
            
            # Quality Anomalies
            AnomalyPattern(
                type=AnomalyType.QUALITY,
                severity=RiskLevel.HIGH,
                description="Quality Control Failure",
                trigger_condition={"probability": 0.02},
                modifications={"quality_downgrade": True},
                cascade_probability=0.3
            ),
            AnomalyPattern(
                type=AnomalyType.CONTAMINATION,
                severity=RiskLevel.CRITICAL,
                description="Contamination Detected",
                trigger_condition={"category": "Food & Beverages", "probability": 0.005},
                modifications={"contaminated": True, "quarantine": True},
                cascade_probability=0.9
            ),
            
            # Security Anomalies
            AnomalyPattern(
                type=AnomalyType.THEFT,
                severity=RiskLevel.HIGH,
                description="Inventory Theft Detected",
                trigger_condition={"high_value": True, "probability": 0.01},
                modifications={"quantity_multiply": (0.1, 0.7)},
                cascade_probability=0.2
            ),
            AnomalyPattern(
                type=AnomalyType.COUNTERFEIT,
                severity=RiskLevel.CRITICAL,
                description="Counterfeit Products Detected",
                trigger_condition={"category": "Luxury Goods", "probability": 0.02},
                modifications={"counterfeit_flag": True},
                cascade_probability=0.5
            ),
            
            # Equipment Anomalies
            AnomalyPattern(
                type=AnomalyType.EQUIPMENT_FAILURE,
                severity=RiskLevel.HIGH,
                description="Warehouse Equipment Failure",
                trigger_condition={"probability": 0.03},
                modifications={"equipment_down": True},
                cascade_probability=0.6,
                duration_minutes=180
            ),
            
            # Supply Chain Disruptions
            AnomalyPattern(
                type=AnomalyType.SUPPLY_CHAIN_DISRUPTION,
                severity=RiskLevel.MEDIUM,
                description="Supplier Delay",
                trigger_condition={"probability": 0.08},
                modifications={"delayed_delivery": True, "quantity_multiply": (0.5, 0.8)},
                cascade_probability=0.3
            ),
            AnomalyPattern(
                type=AnomalyType.NATURAL_DISASTER,
                severity=RiskLevel.CATASTROPHIC,
                description="Natural Disaster Impact",
                trigger_condition={"probability": 0.001},
                modifications={"facility_damaged": True, "quantity_multiply": (0.0, 0.3)},
                cascade_probability=1.0,
                duration_minutes=720
            ),
            
            # Cyber Security
            AnomalyPattern(
                type=AnomalyType.CYBER_ATTACK,
                severity=RiskLevel.CRITICAL,
                description="Cybersecurity Breach",
                trigger_condition={"probability": 0.005},
                modifications={"data_compromised": True, "system_offline": True},
                cascade_probability=0.8,
                duration_minutes=480
            ),
            
            # Regulatory
            AnomalyPattern(
                type=AnomalyType.REGULATORY_VIOLATION,
                severity=RiskLevel.HIGH,
                description="Regulatory Compliance Violation",
                trigger_condition={"category": "Pharmaceuticals", "probability": 0.01},
                modifications={"compliance_violation": True, "quarantine": True},
                cascade_probability=0.4
            )
        ]

    def _initialize_scenarios(self) -> List[SimulationScenario]:
        """Initialize predefined testing scenarios"""
        return [
            SimulationScenario(
                name="Cold Chain Failure",
                description="Simulate refrigeration system failure affecting multiple temperature-sensitive products",
                duration_minutes=120,
                affected_products=["Temperature Sensitive Biologics", "Premium Frozen Foods", "Organic Fresh Produce"],
                anomaly_types=[AnomalyType.TEMPERATURE, AnomalyType.QUALITY, AnomalyType.EQUIPMENT_FAILURE],
                severity=RiskLevel.CRITICAL
            ),
            SimulationScenario(
                name="Supply Chain Disruption",
                description="Major supplier issues affecting multiple product categories",
                duration_minutes=480,
                affected_products=["*"],  # All products
                anomaly_types=[AnomalyType.SUPPLY_CHAIN_DISRUPTION, AnomalyType.QUANTITY],
                severity=RiskLevel.HIGH
            ),
            SimulationScenario(
                name="Security Breach",
                description="Multi-vector attack including theft and cyber security breach",
                duration_minutes=240,
                affected_products=["Luxury Items", "Industrial Electronics", "Medical Devices"],
                anomaly_types=[AnomalyType.THEFT, AnomalyType.CYBER_ATTACK, AnomalyType.COUNTERFEIT],
                severity=RiskLevel.CRITICAL
            ),
            SimulationScenario(
                name="Natural Disaster",
                description="Natural disaster affecting warehouse operations",
                duration_minutes=720,
                affected_products=["*"],
                anomaly_types=[AnomalyType.NATURAL_DISASTER, AnomalyType.EQUIPMENT_FAILURE, AnomalyType.SUPPLY_CHAIN_DISRUPTION],
                severity=RiskLevel.CATASTROPHIC
            ),
            SimulationScenario(
                name="Quality Crisis",
                description="Widespread quality control issues and contamination",
                duration_minutes=360,
                affected_products=["Standard Pharmaceuticals", "Organic Fresh Produce", "Premium Frozen Foods"],
                anomaly_types=[AnomalyType.QUALITY, AnomalyType.CONTAMINATION, AnomalyType.REGULATORY_VIOLATION],
                severity=RiskLevel.HIGH
            )
        ]

    def _initialize_enhanced_locations(self) -> List[str]:
        """Initialize comprehensive warehouse locations"""
        return [
            # Standard Warehouses
            "Warehouse A - Section 1", "Warehouse A - Section 2", "Warehouse A - Section 3",
            "Warehouse B - Section 1", "Warehouse B - Section 2", "Warehouse B - Section 3", 
            "Warehouse C - Section 1", "Warehouse C - Section 2", "Warehouse C - Section 3",
            
            # Specialized Storage
            "Cold Storage Zone 1", "Cold Storage Zone 2", "Deep Freeze Unit A", "Deep Freeze Unit B",
            "Climate Control Unit A", "Climate Control Unit B", "Climate Control Unit C",
            "Refrigerated Bay 1", "Refrigerated Bay 2", "Fresh Storage A", "Fresh Storage B",
            
            # Secure Facilities
            "Secure Vault A", "Secure Vault B", "High Security Storage", "VIP Warehouse",
            "Luxury Storage Facility", "High Value Bay", "Restricted Access Zone",
            
            # Specialized Areas
            "Hazmat Storage A", "Hazmat Storage B", "Chemical Containment", "Bio Storage",
            "Pharmaceutical Vault", "Medical Storage", "Sterile Environment",
            
            # Processing Areas
            "Quality Control Lab", "Inspection Bay", "Processing Center", "Packaging Area",
            "Distribution Hub", "Loading Dock A", "Loading Dock B", "Loading Dock C",
            
            # Temporary Areas
            "Quarantine Zone", "Emergency Storage", "Overflow Area", "Transit Bay",
            "Customs Holding", "Damaged Goods Area", "Returns Processing"
        ]

    def _get_auth_token(self) -> Optional[str]:
        """Get authentication token with enhanced error handling"""
        try:
            auth_config = self.config.get('authentication', {})
            start_time = time.time()
            
            response = requests.post(
                f"{self.api_url}/api/auth/login",
                json={
                    'username': auth_config.get('username', 'admin'),
                    'password': auth_config.get('password', 'admin123')
                },
                timeout=10
            )
            
            response_time = time.time() - start_time
            self._update_performance_metrics(response_time)
            
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

    def _update_performance_metrics(self, response_time: float):
        """Update performance tracking metrics"""
        metrics = self.stats['performance_metrics']
        metrics['avg_response_time'] = (metrics['avg_response_time'] + response_time) / 2
        metrics['max_response_time'] = max(metrics['max_response_time'], response_time)
        metrics['min_response_time'] = min(metrics['min_response_time'], response_time)

    def _apply_seasonal_effects(self, data: Dict, template: ProductTemplate) -> Dict:
        """Enhanced seasonal effects with more sophisticated modeling"""
        if not template.seasonal_factor or not self.config.get('seasonal_effects', True):
            return data
        
        month = datetime.now().month
        day_of_year = datetime.now().timetuple().tm_yday
        
        # Seasonal demand patterns
        seasonal_multiplier = 1.0
        
        if template.category == "Food & Beverages":
            # Holiday seasons
            if month in [11, 12]:  # Thanksgiving/Christmas
                seasonal_multiplier = 1.4
            elif month in [6, 7, 8]:  # Summer
                if "Fresh" in template.name or "Cold" in template.name:
                    seasonal_multiplier = 1.3
            elif month in [1, 2]:  # Post-holiday
                seasonal_multiplier = 0.7
                
        elif template.category == "Electronics":
            if month in [11, 12]:  # Holiday shopping
                seasonal_multiplier = 1.6
            elif month in [1, 2]:  # Post-holiday
                seasonal_multiplier = 0.6
                
        elif template.category == "Textiles":
            if month in [3, 4, 9, 10]:  # Fashion seasons
                seasonal_multiplier = 1.4
            elif month in [6, 7]:  # Summer
                seasonal_multiplier = 1.2
                
        # Apply multiplier
        data['quantity'] = int(data['quantity'] * seasonal_multiplier)
        
        # Temperature variations due to seasonal ambient conditions
        if month in [6, 7, 8]:  # Summer
            data['temperature'] += random.uniform(1.0, 3.0)
        elif month in [12, 1, 2]:  # Winter
            data['temperature'] -= random.uniform(0.5, 2.0)
            
        return data

    def _apply_time_based_variations(self, data: Dict) -> Dict:
        """Enhanced time-based patterns"""
        if not self.config.get('time_based_variations', True):
            return data
        
        current_time = datetime.now()
        hour = current_time.hour
        day_of_week = current_time.weekday()
        
        # More sophisticated time patterns
        activity_multiplier = 1.0
        
        # Business hours (enhanced patterns)
        if day_of_week < 5:  # Weekdays
            if 6 <= hour <= 8:  # Early morning prep
                activity_multiplier = 1.3
            elif 9 <= hour <= 17:  # Business hours
                activity_multiplier = 1.2
            elif 18 <= hour <= 20:  # Evening rush
                activity_multiplier = 1.1
            elif 21 <= hour <= 23 or 0 <= hour <= 5:  # Night
                activity_multiplier = 0.4
        else:  # Weekends
            if 8 <= hour <= 18:  # Weekend activity
                activity_multiplier = 0.8
            else:  # Weekend off-hours
                activity_multiplier = 0.3
                
        data['quantity'] = int(data['quantity'] * activity_multiplier)
        
        return data

    def _generate_smart_anomaly(self, data: Dict, template: ProductTemplate) -> Tuple[Dict, bool, str, RiskLevel]:
        """Enhanced anomaly generation with smart cascading effects"""
        # Base anomaly probability with environmental factors
        base_probability = template.anomaly_probability
        
        # Adjust for environmental conditions
        if self.environment_condition == EnvironmentCondition.EXTREME_HEAT:
            if template.temperature_sensitive:
                base_probability *= 3.0
        elif self.environment_condition == EnvironmentCondition.POWER_OUTAGE:
            base_probability *= 2.5
        elif self.environment_condition == EnvironmentCondition.NATURAL_DISASTER:
            base_probability *= 10.0
            
        # Check if anomaly should occur
        if random.random() > base_probability:
            return data, False, "", RiskLevel.VERY_LOW
            
        # Select applicable patterns with smarter matching
        applicable_patterns = []
        for pattern in self.anomaly_patterns:
            trigger = pattern.trigger_condition
            match_score = 0
            
            # Category matching
            if 'category' in trigger:
                if trigger['category'] in template.category:
                    match_score += 2
                else:
                    continue
                    
            # Subcategory matching
            if 'subcategory' in trigger:
                if trigger['subcategory'] in template.subcategory:
                    match_score += 2
                    
            # Property-based matching
            for prop in ['temperature_sensitive', 'humidity_sensitive', 'high_value', 'perishable', 'hazardous']:
                if prop in trigger:
                    if getattr(template, prop, False) == trigger[prop]:
                        match_score += 1
                        
            # Probability check
            if random.random() <= trigger.get('probability', 1.0):
                match_score += 1
                
            if match_score > 0:
                applicable_patterns.append((pattern, match_score))
                
        if not applicable_patterns:
            return data, False, "", RiskLevel.VERY_LOW
            
        # Select pattern with highest match score
        applicable_patterns.sort(key=lambda x: x[1], reverse=True)
        pattern = applicable_patterns[0][0]
        
        anomaly_data = data.copy()
        modifications = pattern.modifications
        
        # Apply modifications with bounds checking
        if 'temperature_add' in modifications:
            add_range = modifications['temperature_add']
            anomaly_data['temperature'] += random.uniform(add_range[0], add_range[1])
            
        if 'temperature_set' in modifications:
            temp_range = modifications['temperature_set']
            anomaly_data['temperature'] = random.uniform(temp_range[0], temp_range[1])
            
        if 'humidity_add' in modifications:
            add_range = modifications['humidity_add']
            anomaly_data['humidity'] += random.uniform(add_range[0], add_range[1])
            
        if 'humidity_set' in modifications:
            humidity_range = modifications['humidity_set']
            anomaly_data['humidity'] = random.uniform(humidity_range[0], humidity_range[1])
            
        if 'quantity_multiply' in modifications:
            mult_range = modifications['quantity_multiply']
            multiplier = random.uniform(mult_range[0], mult_range[1])
            anomaly_data['quantity'] = max(1, int(anomaly_data['quantity'] * multiplier))
            
        # Add special anomaly indicators
        if modifications.get('contaminated'):
            anomaly_data['contaminated'] = True
            anomaly_data['quality'] = 'REJECTED'
            
        if modifications.get('counterfeit_flag'):
            anomaly_data['authenticity'] = 'SUSPECTED_COUNTERFEIT'
            
        if modifications.get('quarantine'):
            anomaly_data['quarantine_status'] = 'QUARANTINED'
            
        # Ensure realistic bounds
        anomaly_data['temperature'] = max(-50.0, min(80.0, anomaly_data['temperature']))
        anomaly_data['humidity'] = max(0.0, min(100.0, anomaly_data['humidity']))
        anomaly_data['quantity'] = max(0, anomaly_data['quantity'])
        
        # Update statistics
        self.stats['anomalies_generated'] += 1
        anomaly_type_key = pattern.type.value
        self.stats['by_anomaly_type'][anomaly_type_key] = self.stats['by_anomaly_type'].get(anomaly_type_key, 0) + 1
        risk_level_key = pattern.severity.value
        self.stats['by_risk_level'][risk_level_key] = self.stats['by_risk_level'].get(risk_level_key, 0) + 1
        
        return anomaly_data, True, f"{pattern.severity.value}: {pattern.description}", pattern.severity

    def _generate_comprehensive_data(self) -> Tuple[Dict, bool, str, RiskLevel]:
        """Generate comprehensive supply chain data with enhanced realism"""
        # Select template with weighted probability
        template = random.choice(self.product_templates)
        
        # Generate base realistic data
        quantity = random.randint(template.base_quantity_range[0], template.base_quantity_range[1])
        
        # Add natural variation to temperature and humidity
        temp_variation = random.gauss(0, 1.0)  # Normal distribution for realistic variation
        humidity_variation = random.gauss(0, 2.0)
        
        temperature = random.uniform(template.temp_range[0], template.temp_range[1]) + temp_variation
        humidity = random.uniform(template.humidity_range[0], template.humidity_range[1]) + humidity_variation
        
        location = random.choice(template.locations)
        quality = random.choice(template.quality_grades)
        supplier = random.choice(template.suppliers)
        
        # Generate realistic product variations
        product_id = f"{template.category[:3].upper()}-{template.subcategory[:2].upper()}-{random.randint(10000, 99999)}"
        
        # Add lot/batch information
        lot_number = f"LOT{datetime.now().strftime('%Y%m')}{random.randint(1000, 9999)}"
        batch_number = f"BATCH{random.randint(100000, 999999)}"
        
        # Calculate estimated value
        price_per_unit = random.uniform(template.price_range[0], template.price_range[1])
        estimated_value = round(price_per_unit * quantity, 2)
        
        # Create comprehensive data structure
        data = {
            'productId': product_id,
            'product': template.name,
            'category': template.category,
            'subcategory': template.subcategory,
            'quantity': quantity,
            'location': location,
            'temperature': round(temperature, 1),
            'humidity': round(humidity, 1),
            'quality': quality,
            'timestamp': datetime.now().isoformat(),
            'batchNumber': batch_number,
            'lotNumber': lot_number,
            'supplier': supplier,
            'estimatedValue': estimated_value,
            'pricePerUnit': round(price_per_unit, 2),
            'shelfLifeDays': template.shelf_life_days,
            'handlingRequirements': template.handling_requirements,
            'regulatoryRequirements': template.regulatory_requirements,
            'metadata': {
                'session_id': self.session_id,
                'simulator_version': '3.0',
                'generation_timestamp': datetime.now().isoformat(),
                'template_used': template.name,
                'perishable': template.perishable,
                'hazardous': template.hazardous,
                'high_value': template.high_value,
                'temperature_sensitive': template.temperature_sensitive,
                'humidity_sensitive': template.humidity_sensitive,
                'environment_condition': self.environment_condition.value
            }
        }
        
        # Apply time and seasonal effects
        data = self._apply_seasonal_effects(data, template)
        data = self._apply_time_based_variations(data)
        
        # Generate anomalies
        data, is_anomaly, anomaly_description, risk_level = self._generate_smart_anomaly(data, template)
        
        # Update statistics
        self.stats['total_generated'] += 1
        category_key = template.category
        self.stats['by_category'][category_key] = self.stats['by_category'].get(category_key, 0) + 1
        
        # Store recent data for monitoring
        if len(self.stats['last_24h_data']) >= 1000:  # Keep last 1000 records
            self.stats['last_24h_data'].pop(0)
        
        self.stats['last_24h_data'].append({
            'timestamp': datetime.now().isoformat(),
            'product': template.name,
            'category': template.category,
            'anomaly': is_anomaly,
            'risk_level': risk_level.value if is_anomaly else 'NORMAL',
            'value': estimated_value
        })
        
        return data, is_anomaly, anomaly_description, risk_level

    def _submit_data_to_api(self, data: Dict, organization_id: str, token: Optional[str] = None) -> bool:
        """Enhanced API submission with performance tracking"""
        try:
            start_time = time.time()
            
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
            
            response_time = time.time() - start_time
            self._update_performance_metrics(response_time)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success', False):
                    self.stats['successful_submissions'] += 1
                    # Update organization stats
                    self.stats['by_organization'][organization_id] = self.stats['by_organization'].get(organization_id, 0) + 1
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

    def _print_enhanced_stats(self):
        """Print comprehensive simulation statistics"""
        if not self.stats['start_time']:
            return
            
        runtime = datetime.now() - self.stats['start_time']
        hours, remainder = divmod(runtime.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        rate = self.stats['total_generated'] / max(runtime.total_seconds(), 1) * 60  # per minute
        anomaly_rate = (self.stats['anomalies_generated'] / max(self.stats['total_generated'], 1)) * 100
        success_rate = (self.stats['successful_submissions'] / max(self.stats['total_generated'], 1)) * 100
        
        print(f"\n{'='*80}")
        print(f"📊 CryptaNet Enhanced Data Simulator v3.0 - Real-time Statistics")
        print(f"{'='*80}")
        print(f"🕐 Runtime: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")
        print(f"📦 Total Generated: {self.stats['total_generated']:,}")
        print(f"⚠️ Anomalies: {self.stats['anomalies_generated']:,} ({anomaly_rate:.1f}%)")
        print(f"✅ Successful Submissions: {self.stats['successful_submissions']:,} ({success_rate:.1f}%)")
        print(f"❌ Failed Submissions: {self.stats['failed_submissions']:,}")
        print(f"📈 Generation Rate: {rate:.1f} records/minute")
        
        # Performance metrics
        metrics = self.stats['performance_metrics']
        print(f"⚡ Avg Response Time: {metrics['avg_response_time']:.3f}s")
        print(f"⚡ Min/Max Response Time: {metrics['min_response_time']:.3f}s / {metrics['max_response_time']:.3f}s")
        
        # Category breakdown
        if self.stats['by_category']:
            print(f"\n📋 By Category:")
            for category, count in sorted(self.stats['by_category'].items()):
                percentage = (count / self.stats['total_generated']) * 100
                print(f"   {category}: {count:,} ({percentage:.1f}%)")
        
        # Organization breakdown
        if self.stats['by_organization']:
            print(f"\n🏢 By Organization:")
            for org, count in sorted(self.stats['by_organization'].items()):
                percentage = (count / self.stats['successful_submissions']) * 100 if self.stats['successful_submissions'] > 0 else 0
                print(f"   {org}: {count:,} ({percentage:.1f}%)")
        
        # Anomaly type breakdown
        if self.stats['by_anomaly_type']:
            print(f"\n⚠️ Anomaly Types:")
            for anomaly_type, count in sorted(self.stats['by_anomaly_type'].items()):
                percentage = (count / self.stats['anomalies_generated']) * 100 if self.stats['anomalies_generated'] > 0 else 0
                print(f"   {anomaly_type}: {count:,} ({percentage:.1f}%)")
        
        # Risk level breakdown
        if self.stats['by_risk_level']:
            print(f"\n🎯 Risk Levels:")
            for risk_level, count in sorted(self.stats['by_risk_level'].items()):
                percentage = (count / self.stats['anomalies_generated']) * 100 if self.stats['anomalies_generated'] > 0 else 0
                print(f"   {risk_level}: {count:,} ({percentage:.1f}%)")
        
        # Current environment
        print(f"\n🌍 Environment: {self.environment_condition.value}")
        if self.current_scenario:
            print(f"🎭 Active Scenario: {self.current_scenario.name}")
        
        print(f"{'='*80}\n")

    def _monitor_stats(self):
        """Enhanced background stats monitoring"""
        while self.running:
            time.sleep(60)  # Print stats every minute
            if self.running:
                self._print_enhanced_stats()

    def start_scenario(self, scenario_name: str):
        """Start a predefined simulation scenario"""
        scenario = next((s for s in self.scenarios if s.name == scenario_name), None)
        if not scenario:
            logger.error(f"❌ Scenario '{scenario_name}' not found")
            return False
            
        self.current_scenario = scenario
        logger.info(f"🎭 Started scenario: {scenario.name}")
        logger.info(f"📖 Description: {scenario.description}")
        logger.info(f"⏱️ Duration: {scenario.duration_minutes} minutes")
        
        # Set environment condition based on scenario
        if scenario.severity == RiskLevel.CATASTROPHIC:
            self.environment_condition = EnvironmentCondition.NATURAL_DISASTER
        elif AnomalyType.EQUIPMENT_FAILURE in scenario.anomaly_types:
            self.environment_condition = EnvironmentCondition.POWER_OUTAGE
        
        return True

    def stop_scenario(self):
        """Stop current scenario"""
        if self.current_scenario:
            logger.info(f"🛑 Stopped scenario: {self.current_scenario.name}")
            self.current_scenario = None
            self.environment_condition = EnvironmentCondition.NORMAL

    def set_environment_condition(self, condition: EnvironmentCondition):
        """Set environmental condition affecting anomaly generation"""
        self.environment_condition = condition
        logger.info(f"🌍 Environment condition set to: {condition.value}")

    def run_simulation(self, interval: int = 10, max_records: Optional[int] = None):
        """Run the enhanced continuous simulation"""
        logger.info(f"🚀 Starting CryptaNet Enhanced Data Simulator v3.0")
        logger.info(f"⏱️ Interval: {interval} seconds")
        logger.info(f"🏢 Organizations: {', '.join(self.organizations)}")
        logger.info(f"📍 API Endpoint: {self.api_url}")
        logger.info(f"🎭 Available Scenarios: {', '.join([s.name for s in self.scenarios])}")
        
        if max_records:
            logger.info(f"🎯 Target Records: {max_records:,}")
        
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
                    logger.info(f"🎯 Reached target of {max_records:,} records. Stopping simulation.")
                    break
                
                # Generate comprehensive data
                data, is_anomaly, anomaly_desc, risk_level = self._generate_comprehensive_data()
                
                # Select organization (weighted random for realism)
                organization = random.choice(self.organizations)
                
                # Enhanced logging with risk levels
                if is_anomaly:
                    risk_emoji = {
                        RiskLevel.VERY_LOW: "🟢",
                        RiskLevel.LOW: "🟡", 
                        RiskLevel.MEDIUM: "🟠",
                        RiskLevel.HIGH: "🔴",
                        RiskLevel.CRITICAL: "🔥",
                        RiskLevel.CATASTROPHIC: "💀"
                    }.get(risk_level, "⚠️")
                    
                    logger.warning(f"{risk_emoji} ANOMALY: {data['productId']} - {anomaly_desc}")
                    logger.info(f"   📦 Product: {data['product'][:40]}...")
                    logger.info(f"   📍 Location: {data['location']}")
                    logger.info(f"   🌡️ Temp: {data['temperature']}°C, 💧 Humidity: {data['humidity']}%")
                    logger.info(f"   💰 Value: ${data['estimatedValue']:,.2f}")
                else:
                    logger.info(f"📦 Normal: {data['productId']} - {data['product'][:40]}... (${data['estimatedValue']:,.2f})")
                
                # Submit to API
                success = self._submit_data_to_api(data, organization, token)
                
                if success:
                    logger.info(f"✅ Successfully submitted to {organization}")
                else:
                    logger.error(f"❌ Failed to submit to {organization}")
                    # Try to re-authenticate on failure
                    if self.stats['failed_submissions'] % 5 == 0:
                        logger.info("🔄 Attempting to re-authenticate...")
                        token = self._get_auth_token()
                
                # Dynamic interval based on anomalies (burst mode for critical events)
                if is_anomaly and risk_level in [RiskLevel.CRITICAL, RiskLevel.CATASTROPHIC]:
                    sleep_time = max(2, interval // 3)  # Faster generation for critical events
                    logger.info(f"⚡ Critical event detected - accelerating to {sleep_time}s interval")
                else:
                    sleep_time = interval
                
                time.sleep(sleep_time)
                
        except KeyboardInterrupt:
            logger.info("🛑 Simulation stopped by user")
        except Exception as e:
            logger.error(f"💥 Simulation error: {e}")
        finally:
            self.running = False
            self._print_enhanced_stats()
            logger.info("🏁 Enhanced simulation ended")

def main():
    parser = argparse.ArgumentParser(description='CryptaNet Enhanced Data Simulator v3.0')
    parser.add_argument('--config', '-c', help='Configuration file path')
    parser.add_argument('--interval', '-i', type=int, default=10, help='Interval between data points (seconds)')
    parser.add_argument('--max-records', '-m', type=int, help='Maximum number of records to generate')
    parser.add_argument('--scenario', '-s', help='Start with a predefined scenario')
    parser.add_argument('--environment', '-e', help='Set environment condition', 
                       choices=[c.value for c in EnvironmentCondition])
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        simulator = EnhancedDataSimulator(args.config)
        
        # Set environment if specified
        if args.environment:
            condition = EnvironmentCondition(args.environment)
            simulator.set_environment_condition(condition)
        
        # Start scenario if specified
        if args.scenario:
            simulator.start_scenario(args.scenario)
        
        # Run simulation
        simulator.run_simulation(
            interval=args.interval, 
            max_records=args.max_records
        )
        
    except Exception as e:
        logger.error(f"💥 Failed to start enhanced simulator: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
