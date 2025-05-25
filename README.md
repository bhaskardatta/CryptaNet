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

## 🔄 **Recent Updates & Fixes**

### **Latest Improvements (May 25, 2025)**

**🐛 Critical Bug Fixes:**
- ✅ **Dashboard Zero Values Issue**: Fixed anomaly detection field references in `integrated_analytics.py`
- ✅ **Data Flow Problem**: Corrected `anomalies_detected` → `anomalies` field mapping
- ✅ **Analytics Display**: Dashboard now shows live data (259+ records, 219+ anomalies)

**🧹 Project Cleanup:**
- ✅ **Removed 20+ unnecessary files**: Python cache, duplicate scripts, old documentation
- ✅ **Enhanced .gitignore**: Added comprehensive patterns for better version control
- ✅ **Streamlined structure**: Organized essential files and removed clutter

**📦 System Improvements:**
- ✅ **Docker Integration**: Complete containerization setup with `docker-compose.yml`
- ✅ **Enhanced Documentation**: Comprehensive setup guide for new systems
- ✅ **Health Monitoring**: Improved system health checks and monitoring scripts

**🔧 Technical Details:**
- Fixed 5 field reference errors in analytics engine
- Updated comprehensive analytics endpoint data structure
- Improved real-time data flow between simulator and dashboard
- Added robust error handling and logging

### **System Health Status**
```bash
# Quick health check
./simple_health_check.sh

# Current metrics (live)
curl -s http://localhost:5004/api/analytics/comprehensive | python3 -c "
import json, sys; data=json.load(sys.stdin); 
print(f'Records: {data[\"analytics\"][\"total_records\"]}')
print(f'Anomalies: {len(data[\"analytics\"][\"anomaly_detection\"][\"anomalies\"])}')
"
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
git clone https://github.com/your-username/CryptaNet.git
cd CryptaNet

# Start all services with one script
chmod +x start_enhanced_system.sh
./start_enhanced_system.sh
```

> **Note**: Replace `your-username` with your actual GitHub username in the clone URL.

## 🆕 **Complete New System Setup**

### **Step 1: System Prerequisites**

**macOS:**
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required tools
brew install python@3.11 node@18 git
```

**Ubuntu/Debian:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install prerequisites
sudo apt install -y python3.11 python3-pip nodejs npm git curl
```

**Verify Installation:**
```bash
python3 --version  # Should be 3.8+
node --version     # Should be 16+
npm --version      # Should be 8+
git --version      # Any recent version
```

### **Step 2: Clone and Setup Project**

```bash
# Clone the repository
git clone https://github.com/your-username/CryptaNet.git
cd CryptaNet

# Make scripts executable
chmod +x start_enhanced_system.sh
chmod +x simple_health_check.sh
chmod +x system_health_monitor.sh
```

### **Step 3: Install Dependencies**

```bash
# Backend Python dependencies
cd backend
pip3 install -r requirements.txt
cd ..

# Frontend Node.js dependencies
cd frontend
npm install
cd ..

# Anomaly detection dependencies
cd anomaly_detection
pip3 install -r requirements.txt
cd ..

# Main simulator dependencies
pip3 install -r simulator_requirements.txt
```

### **Step 4: Start the System**

```bash
# Option A: Use the automated startup script (Recommended)
./start_enhanced_system.sh

# Option B: Manual startup (for debugging)
# Terminal 1: Backend
cd backend && python3 simple_backend.py

# Terminal 2: Frontend (in new terminal)
cd frontend && npm start

# Terminal 3: Data Simulator Dashboard (in new terminal)
python3 data_simulator_dashboard.py

# Terminal 4: Analytics (in new terminal)
python3 -c "
import integrated_analytics as ia
system = ia.IntegratedAnalyticsSystem()
system.start_continuous_monitoring(interval_minutes=5)
"
```

### **Step 5: Verify Installation**

```bash
# Check system health
./simple_health_check.sh

# Test API endpoints
curl http://localhost:5004/api/health
curl http://localhost:5004/api/analytics/comprehensive | python3 -m json.tool

# Access the dashboard
open http://localhost:3000  # macOS
# or visit http://localhost:3000 in your browser
```

### **📦 Manual Setup (Step by Step)**

**1. Setup Backend Services**
```bash
# Install Python dependencies
cd backend
pip install -r requirements.txt
cd ..

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
- **Data Flow**: 259+ total records processed ✅
- **Anomaly Detection**: 219+ anomalies detected ✅
- **Real-time Updates**: 30-second refresh cycle ✅
- **Dashboard Fix**: Anomaly detection display issue resolved ✅

> **Last Updated**: May 25, 2025 - Dashboard now correctly displays live analytics data instead of showing 0 values.

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
- **Hyperledger Fabric 2.x** network configuration
- **Smart contracts** for supply chain verification
- **Immutable record keeping**
- **Channel participation API** for advanced channel management
- **Diagnostic tools** for network troubleshooting

> The blockchain network has been updated to be compatible with Hyperledger Fabric 2.x with improved DNS resolution between containers and enhanced network configuration.

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

### **New System Setup Issues**

**Python Module Not Found:**
```bash
# If you get "ModuleNotFoundError"
pip3 install --upgrade pip
pip3 install flask flask-cors requests numpy pandas scikit-learn joblib

# For macOS with multiple Python versions
python3.11 -m pip install [package-name]
```

**Node.js Version Issues:**
```bash
# Install Node Version Manager (nvm)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc  # or ~/.zshrc for zsh

# Install and use Node 18
nvm install 18
nvm use 18
```

**Permission Errors:**
```bash
# Make scripts executable
chmod +x *.sh

# Fix npm permissions (if needed)
sudo chown -R $(whoami) ~/.npm
```

### **Runtime Issues**

**Port Already in Use:**
```bash
# Kill processes on specific ports
sudo lsof -ti:3000 | xargs kill -9  # Frontend
sudo lsof -ti:5004 | xargs kill -9  # Backend
sudo lsof -ti:8001 | xargs kill -9  # Analytics
```

**Services Not Starting:**
```bash
# Check if Python/Node are properly installed
which python3
which node
which npm

# Restart all services
./start_enhanced_system.sh
```

**Dashboard Shows Zero Values:**
```bash
# This issue has been fixed! If you still see it:
# 1. Restart the data simulator dashboard
python3 data_simulator_dashboard.py

# 2. Check backend health
curl http://localhost:5004/api/analytics/comprehensive

# 3. Refresh your browser
```

**Missing Dependencies:**
```bash
# Python dependencies (using requirements files)
cd backend && pip3 install -r requirements.txt && cd ..
cd anomaly_detection && pip3 install -r requirements.txt && cd ..
pip3 install -r simulator_requirements.txt

# Node.js dependencies
cd frontend && npm install && cd ..
```

**Data Not Showing:**
```bash
# Restart data simulator dashboard
python3 data_simulator_dashboard.py

# Check backend status
curl http://localhost:5004/api/health
```

### **Performance Issues**

**Slow Loading:**
- Ensure you have at least 4GB RAM available
- Close unnecessary applications
- Check system resource usage with `top` or Activity Monitor

**High CPU Usage:**
- Use the simulator dashboard to select a longer interval (10 or 30 seconds)
- Monitor with: `./system_health_monitor.sh`

### **Blockchain Network Issues**

**Channel Creation Issues:**
```bash
# Run blockchain diagnostic script
cd blockchain/network
./diagnostic.sh

# Manual channel creation (if needed)
./create_channel_manual.sh
```

**Container Connectivity Issues:**
```bash
# Check container DNS resolution
docker exec cli ping peer0.org1.example.com

# Check if orderer admin API is accessible
docker exec cli curl -s http://orderer.example.com:9443/participation/v1/channels
```

**Reset Blockchain Network:**
```bash
cd blockchain/docker
docker-compose down -v
cd ../network
./generate.sh
cd ../docker
./prepare_environment.sh clean
docker-compose up -d
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
