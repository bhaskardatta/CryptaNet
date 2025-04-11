# CryptaNet Project Structure

This document outlines the directory structure and organization of the CryptaNet project.

## Directory Structure

```
CryptaNet/
├── blockchain/                  # Hyperledger Fabric network configuration
│   ├── chaincode/              # Smart contracts (chaincode)
│   ├── network/                # Network configuration files
│   └── docker/                 # Docker configuration for blockchain
├── privacy_layer/              # Privacy-preserving mechanisms
│   ├── encryption/             # Symmetric encryption using Fernet
│   ├── hashing/                # SHA-256 hashing for data integrity
│   └── zkp/                    # Zero-knowledge proof implementation
├── anomaly_detection/          # Machine learning pipeline
│   ├── preprocessing/          # Data preprocessing modules
│   ├── models/                 # Isolation Forest implementation
│   ├── feature_engineering/    # Feature engineering for supply chain data
│   └── evaluation/             # Model evaluation scripts
├── explainability/             # Explainability module
│   ├── shap/                   # SHAP implementation for model interpretation
│   ├── visualization/          # Feature importance visualization
│   └── explanation_api/        # API for retrieving explanations
├── backend/                    # Integration backend
│   ├── api/                    # RESTful API endpoints
│   ├── auth/                   # Authentication and authorization
│   ├── events/                 # Event listeners for blockchain
│   └── data_flow/              # Data flow management
├── frontend/                   # React.js-based dashboard
│   ├── src/                    # Source code
│   ├── public/                 # Public assets
│   └── package.json            # Dependencies
├── deployment/                 # Deployment configuration
│   ├── docker/                 # Docker containers for all components
│   ├── kubernetes/             # Kubernetes manifests
│   └── ci_cd/                  # CI/CD pipeline configuration
├── docs/                       # Documentation
│   ├── architecture/           # System architecture overview
│   ├── installation/           # Installation and setup instructions
│   ├── api/                    # API documentation
│   ├── user_manual/            # User manual for the dashboard
│   └── developer_guide/        # Developer guide for extending the system
├── tests/                      # Testing
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   ├── e2e/                    # End-to-end tests
│   └── performance/            # Performance benchmarks
└── sample_data/                # Sample supply chain data
    ├── synthetic/              # Synthetic dataset
    ├── anomaly_injection/      # Anomaly injection scripts
    └── benchmark/              # Benchmark dataset
```

## Component Descriptions

### Blockchain

The blockchain component implements a Hyperledger Fabric network with multiple organizations, channels, and chaincode for data storage, access control, and event emission.

### Privacy Layer

The privacy layer implements encryption, hashing, and zero-knowledge proof mechanisms to ensure data confidentiality, integrity, and selective disclosure.

### Anomaly Detection

The anomaly detection component implements a machine learning pipeline using Isolation Forest for detecting anomalies in supply chain data.

### Explainability

The explainability component implements SHAP-based interpretability for explaining detected anomalies in a human-readable format.

### Backend

The backend component integrates all other components and provides RESTful APIs for the frontend, handles authentication, and manages data flow.

### Frontend

The frontend component provides a user-friendly dashboard for visualizing supply chain data, anomaly alerts, and explanations.

### Deployment

The deployment component provides configuration for deploying the system using Docker, Kubernetes, and CI/CD pipelines.

### Documentation

The documentation component provides comprehensive documentation for the system, including architecture, installation, API, user manual, and developer guide.

### Tests

The tests component provides unit, integration, end-to-end, and performance tests for the system.

### Sample Data

The sample data component provides synthetic datasets, anomaly injection scripts, and benchmark datasets for testing and demonstration.