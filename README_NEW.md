# CryptaNet - Advanced Supply Chain Analytics Platform

**CryptaNet** is a comprehensive, real-time supply chain monitoring and analytics platform that combines blockchain technology, machine learning, and advanced data analytics to provide unprecedented visibility and security for supply chain operations.

## 🚀 **Key Features**

- **📊 Real-time Analytics Dashboard** - Live monitoring with 30-second auto-refresh
- **🤖 AI-Powered Anomaly Detection** - Machine learning models detecting supply chain irregularities
- **⛓️ Blockchain Integration** - Hyperledger Fabric for immutable record keeping
- **🔮 Predictive Analytics** - Forecasting and trend analysis for proactive management
- **🔒 Privacy Layer** - Zero-knowledge proofs and encrypted data handling
- **📱 Modern Web Interface** - React-based dashboard with Material-UI components
- **🐳 Docker Ready** - Complete containerization for easy deployment

## 🏗️ **System Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Analytics     │
│   (React)       │◄──►│   (Flask)       │◄──►│   Engine        │
│   Port: 3000    │    │   Port: 5004    │    │   (ML Models)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       ▼                       │
         │              ┌─────────────────┐              │
         │              │   Data Storage  │              │
         │              │   & Blockchain  │              │
         │              └─────────────────┘              │
         │                                               │
         └───────────────► Data Simulator ◄──────────────┘
                        (Generates test data)
```

## 🎯 **Quick Start Guide**

### **Prerequisites**
- **Python 3.8+** (with pip)
- **Node.js 16+** (with npm)
- **Git**
- **macOS/Linux** (recommended)

### **🚀 One-Command Setup**

```bash
# Clone and setup the entire project
git clone <your-repository-url>
cd CryptaNet

# Start all services with one script
chmod +x start_enhanced_system.sh
./start_enhanced_system.sh
```

### **📦 Manual Setup (Step by Step)**

**1. Setup Backend Services**
```bash
# Install Python dependencies
pip install -r backend/requirements.txt
pip install flask flask-cors requests numpy pandas scikit-learn

# Start the main backend API
cd backend
python simple_backend.py
```

**2. Setup Frontend**
```bash
# In a new terminal
cd frontend
npm install
npm start
```

**3. Start Data Simulator**
```bash
# In a new terminal (from project root)
python data_simulator_dashboard.py --interval 2 --verbose
```

**4. Start Analytics Engine**
```bash
# In a new terminal
cd anomaly_detection
pip install -r requirements.txt
python anomaly_detection_api.py
```

## 🌐 **Access Points**

After starting all services:

- **🖥️ Main Dashboard**: http://localhost:3000
- **🔧 Backend API**: http://localhost:5004
- **📊 Analytics API**: http://localhost:8001
- **🔬 Data Simulator**: Running in terminal with live updates

## 📊 **Current System Status**

**✅ System is fully operational with:**
- **Backend**: Running on port 5004 ✅
- **Frontend**: Running on port 3000 ✅  
- **Data Flow**: ~161 total records processed ✅
- **Anomaly Detection**: ~139 anomalies detected ✅
- **Real-time Updates**: 30-second refresh cycle ✅

## 🔧 **Key Components**

### **Frontend (`frontend/`)**
- **React 18** with Material-UI components
- **Redux** for state management
- **Real-time dashboard** with auto-refresh
- **Responsive design** for all devices

### **Backend (`backend/`)**
- **Flask API server** with CORS support
- **RESTful endpoints** for all data operations
- **Authentication system** (token-based)
- **Data aggregation** and analytics processing

### **Analytics Engine (`anomaly_detection/` & root files)**
- **`integrated_analytics.py`** - Main analytics orchestrator
- **`advanced_anomaly_detection.py`** - ML-based anomaly detection
- **`predictive_analytics.py`** - Forecasting and predictions
- **`real_time_alerting.py`** - Alert system

### **Data Simulation (`data_simulator_dashboard.py`)**
- **Real-time data generation** with configurable intervals
- **Realistic supply chain scenarios** (temperature, humidity, location)
- **Automatic anomaly injection** for testing

### **Blockchain Layer (`blockchain/`)**
- **Hyperledger Fabric** network configuration
- **Smart contracts** for supply chain verification
- **Immutable record keeping**

## 🚀 **Production Deployment**

### **Docker Deployment**
```bash
# Start all services with Docker
docker-compose up -d

# Monitor logs
docker-compose logs -f
```

### **Production Script**
```bash
chmod +x deploy_production.sh
./deploy_production.sh
```

## 🔍 **API Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/analytics/comprehensive` | GET | Complete analytics dashboard data |
| `/api/analytics/real-time` | GET | Live metrics and KPIs |
| `/api/supply-chain/data` | GET | Raw supply chain data |
| `/api/auth/login` | POST | User authentication |
| `/api/health` | GET | System health check |

## 🛠️ **Development Commands**

### **Health Checks**
```bash
# Quick system health check
./simple_health_check.sh

# Comprehensive system monitoring
./system_health_monitor.sh
```

### **Testing Data Flow**
```bash
# Test comprehensive analytics
curl -s http://localhost:5004/api/analytics/comprehensive | python3 -m json.tool

# Check real-time metrics
curl -s http://localhost:5004/api/analytics/real-time | python3 -m json.tool
```

### **Start Individual Services**
```bash
# Backend only
cd backend && python simple_backend.py

# Frontend only  
cd frontend && npm start

# Data simulator only
python data_simulator_dashboard.py --interval 5 --verbose

# Analytics engine only
cd anomaly_detection && python anomaly_detection_api.py
```

## 📁 **Project Structure**

```
CryptaNet/
├── 📱 frontend/                 # React web application
├── 🔧 backend/                  # Flask API server
├── 🤖 anomaly_detection/        # ML models and APIs
├── ⛓️ blockchain/              # Hyperledger Fabric network
├── 🔒 privacy_layer/           # Privacy and security components
├── 🐳 docker/                   # Docker configurations
├── 📊 integrated_analytics.py   # Main analytics engine
├── 🔮 predictive_analytics.py   # Forecasting system
├── 🚨 real_time_alerting.py     # Alert management
├── 📈 data_simulator_dashboard.py # Data generation
└── 🚀 start_enhanced_system.sh  # One-command startup
```

## 🔧 **Troubleshooting**

### **Common Issues**

**Port Already in Use:**
```bash
# Kill processes on specific ports
sudo lsof -ti:3000 | xargs kill -9  # Frontend
sudo lsof -ti:5004 | xargs kill -9  # Backend
```

**Missing Dependencies:**
```bash
# Python dependencies
pip install flask flask-cors requests numpy pandas scikit-learn

# Node.js dependencies
cd frontend && npm install
```

**Data Not Showing:**
```bash
# Restart data simulator
python data_simulator_dashboard.py --interval 2 --verbose

# Check backend status
curl http://localhost:5004/api/health
```

## 🤝 **Contributing**

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

## 📜 **License**

This project is licensed under the **MIT License** - see the LICENSE file for details.

## 🆘 **Support**

- **📧 Issues**: Open an issue on GitHub
- **💬 Discussions**: Use GitHub Discussions for questions
- **📖 Documentation**: Check the `/docs` folder for detailed guides

---

**🎉 CryptaNet - Revolutionizing Supply Chain Analytics with Real-time Intelligence!**
