# CryptaNet: Privacy-Preserving & Explainable AI for Supply Chain Anomaly Detection

CryptaNet is a comprehensive system that integrates permissioned blockchain technology with privacy-preserving mechanisms and explainable AI to detect anomalies in supply chain operations.

## System Architecture

The CryptaNet system consists of the following components:

1. **Permissioned Blockchain Network**: Hyperledger Fabric implementation with multiple organizations
2. **Privacy Layer**: Encryption and hashing mechanisms for data confidentiality and integrity
3. **Anomaly Detection System**: Machine learning pipeline using Isolation Forest for detecting supply chain anomalies
4. **Explainability Module**: SHAP-based interpretability layer for explaining detected anomalies
5. **Integration Backend**: Flask-based backend connecting all components
6. **Frontend Dashboard**: React.js-based user interface for visualization and monitoring

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

## Installation and Setup

### Prerequisites

- Docker and Docker Compose
- Node.js (v14 or higher)
- Python 3.8+
- Hyperledger Fabric prerequisites

### Setup Instructions

1. Clone the repository
2. Install dependencies
   ```bash
   # Backend dependencies
   cd backend
   pip install -r requirements.txt
   
   # Frontend dependencies
   cd frontend
   npm install
   ```
3. Start the Hyperledger Fabric network
   ```bash
   cd blockchain/network
   ./startFabric.sh
   ```
4. Start the backend server
   ```bash
   cd backend
   python app.py
   ```
5. Start the frontend development server
   ```bash
   cd frontend
   npm start
   ```

## Components

### Blockchain Implementation

The blockchain component uses Hyperledger Fabric to create a permissioned network with multiple organizations. It includes:

- Network configuration for 3+ organizations
- Channel configuration for private data sharing
- Smart contracts for data storage, access control, and event emission

### Privacy Layer

The privacy layer ensures data confidentiality and integrity through:

- Symmetric encryption using Fernet
- SHA-256 hashing for data integrity verification
- Zero-knowledge proof implementation for selective disclosure

### Anomaly Detection System

The anomaly detection system uses machine learning to identify unusual patterns in supply chain data:

- Data preprocessing for supply chain metrics
- Isolation Forest for unsupervised anomaly detection
- Feature engineering for supply chain-specific attributes
- Configurable anomaly scoring system

### Explainability Layer

The explainability layer makes AI decisions transparent and understandable:

- SHAP (SHapley Additive exPlanations) for model interpretation
- Feature importance visualization
- Human-readable explanations for detected anomalies

### Integration Backend

The backend system connects all components and provides APIs for the frontend:

- RESTful APIs for frontend communication
- Authentication and authorization
- Event listeners for blockchain events
- Data flow management between components

### Frontend Dashboard

The React.js-based dashboard provides a user-friendly interface for monitoring and visualization:

- Real-time supply chain data visualization
- Anomaly alerts with severity indicators
- Detailed explanation views for detected anomalies
- Interactive charts using D3.js

## Documentation

Comprehensive documentation is available in the `docs` directory, including:

- System architecture overview
- Installation and setup instructions
- API documentation
- User manual for the dashboard
- Developer guide for extending the system

## Testing

The system includes various tests to ensure reliability and performance:

- Unit tests for individual modules
- Integration tests for component interactions
- End-to-end tests for the complete system
- Performance benchmarks

## Sample Data

Sample supply chain data is provided for demonstration and testing:

- Synthetic dataset representing typical supply chain metrics
- Anomaly injection scripts for testing detection capabilities
- Benchmark dataset for evaluating model performance

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Hyperledger Fabric community
- scikit-learn developers
- SHAP developers
- React.js community