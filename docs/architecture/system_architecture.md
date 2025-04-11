# CryptaNet System Architecture

## Overview

CryptaNet integrates permissioned blockchain technology with privacy-preserving mechanisms and explainable AI to detect anomalies in supply chain operations. The system architecture consists of six main components that work together to provide a secure, transparent, and explainable anomaly detection system.

## Architecture Diagram

```
+---------------------------------------------------------------------------------------------------+
|                                        CryptaNet System                                            |
+---------------------------------------------------------------------------------------------------+
                                                |
                +-----------------------------+  |  +-----------------------------+
                |                             |  |  |                             |
                |  Permissioned Blockchain    |<-+->|  Privacy Layer              |
                |  (Hyperledger Fabric)       |     |  (Encryption & Hashing)     |
                |                             |     |                             |
                +-------------+---------------+     +-------------+---------------+
                              |                                   |
                              |                                   |
                              v                                   v
                +-------------+---------------+     +-------------+---------------+
                |                             |     |                             |
                |  Anomaly Detection System  |<--->|  Explainability Module      |
                |  (Isolation Forest)        |     |  (SHAP)                     |
                |                             |     |                             |
                +-------------+---------------+     +-------------+---------------+
                              |                                   |
                              |                                   |
                              v                                   v
                +-------------+-----------------------------------+---------------+
                |                                                               |
                |  Integration Backend (Flask)                                  |
                |                                                               |
                +-------------+-----------------------------------------------+
                              |
                              v
                +-------------+-----------------------------------------------+
                |                                                               |
                |  Frontend Dashboard (React.js)                                |
                |                                                               |
                +---------------------------------------------------------------+
```

## Component Descriptions

### 1. Permissioned Blockchain Network

The blockchain component uses Hyperledger Fabric to create a permissioned network with multiple organizations. It provides:

- Immutable ledger for supply chain data
- Smart contracts for data storage and access control
- Channel configuration for private data sharing
- Event emission for anomaly alerts

### 2. Privacy Layer

The privacy layer ensures data confidentiality and integrity through:

- Symmetric encryption using Fernet for data confidentiality
- SHA-256 hashing for data integrity verification
- Zero-knowledge proof implementation for selective disclosure
- API for secure data submission and verification

### 3. Anomaly Detection System

The anomaly detection system uses machine learning to identify unusual patterns in supply chain data:

- Data preprocessing for supply chain metrics
- Isolation Forest for unsupervised anomaly detection
- Feature engineering for supply chain-specific attributes
- Anomaly scoring system with configurable thresholds

### 4. Explainability Module

The explainability module makes AI decisions transparent and understandable:

- SHAP (SHapley Additive exPlanations) for model interpretation
- Feature importance visualization
- Human-readable explanations for detected anomalies
- API for retrieving explanations for specific anomalies

### 5. Integration Backend

The backend system connects all components and provides APIs for the frontend:

- RESTful APIs for frontend communication
- Authentication and authorization
- Event listeners for blockchain events
- Data flow management between components

### 6. Frontend Dashboard

The React.js-based dashboard provides a user-friendly interface for monitoring and visualization:

- Real-time supply chain data visualization
- Anomaly alerts with severity indicators
- Detailed explanation views for detected anomalies
- Interactive charts using D3.js or Chart.js
- User authentication and role-based access control
- Responsive design for different devices

## Data Flow

1. Supply chain data is submitted to the system through the frontend or API
2. The privacy layer encrypts and hashes the data for confidentiality and integrity
3. The blockchain network stores the encrypted data and metadata
4. The anomaly detection system processes the data to identify anomalies
5. The explainability module generates explanations for detected anomalies
6. The integration backend coordinates the flow of data between components
7. The frontend dashboard visualizes the data, anomalies, and explanations

## Security Considerations

- All communication between components is encrypted using TLS
- Authentication and authorization are enforced at all levels
- Sensitive data is encrypted at rest and in transit
- Access control is managed through the permissioned blockchain
- Audit logs are maintained for all system activities