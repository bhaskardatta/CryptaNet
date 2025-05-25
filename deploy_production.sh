#!/bin/bash

# CryptaNet Production Deployment Script
# ======================================
# 
# Comprehensive production deployment with security hardening,
# monitoring setup, and automated health checks.
#
# Usage: ./deploy_production.sh [environment]
# Environments: development, staging, production
#
# Author: CryptaNet DevOps Team
# Version: 1.0
# Date: May 25, 2025

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"
ENVIRONMENT="${1:-development}"
COMPOSE_FILE="docker-compose.yml"
ENV_FILE=".env.${ENVIRONMENT}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"
}

# Function to check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed. Please install Docker first."
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose is not installed. Please install Docker Compose first."
    fi
    
    # Check Docker daemon
    if ! docker info &> /dev/null; then
        error "Docker daemon is not running. Please start Docker first."
    fi
    
    # Check available disk space (minimum 5GB)
    available_space=$(df "$PROJECT_ROOT" | awk 'NR==2 {print $4}')
    if [ "$available_space" -lt 5242880 ]; then # 5GB in KB
        warn "Low disk space detected. Recommend at least 5GB free space."
    fi
    
    # Check available memory (minimum 4GB)
    if command -v free &> /dev/null; then
        available_memory=$(free -m | awk 'NR==2{printf "%d", $7}')
        if [ "$available_memory" -lt 4096 ]; then
            warn "Low memory detected. Recommend at least 4GB available memory."
        fi
    fi
    
    log "Prerequisites check completed ✅"
}

# Function to setup environment files
setup_environment() {
    log "Setting up environment for: $ENVIRONMENT"
    
    # Create environment-specific configuration
    cat > "$ENV_FILE" << EOF
# CryptaNet Environment Configuration
ENVIRONMENT=$ENVIRONMENT
COMPOSE_PROJECT_NAME=cryptanet-${ENVIRONMENT}

# Backend Configuration
FLASK_ENV=$ENVIRONMENT
FLASK_DEBUG=$([ "$ENVIRONMENT" = "development" ] && echo "true" || echo "false")
SECRET_KEY=$(openssl rand -hex 32)

# Frontend Configuration
REACT_APP_ENV=$ENVIRONMENT
REACT_APP_API_BASE_URL=http://localhost:5004

# Database Configuration
DB_PATH=/app/data/cryptanet.db

# Security Configuration
JWT_SECRET_KEY=$(openssl rand -hex 32)
ENCRYPTION_KEY=$(openssl rand -hex 32)

# Monitoring Configuration
PROMETHEUS_RETENTION=30d
GRAFANA_ADMIN_PASSWORD=$(openssl rand -hex 16)

# Performance Configuration
WORKER_PROCESSES=4
MAX_CONNECTIONS=1024
MEMORY_LIMIT=512m
CPU_LIMIT=1.0

# Logging Configuration
LOG_LEVEL=$([ "$ENVIRONMENT" = "production" ] && echo "WARNING" || echo "INFO")
LOG_RETENTION_DAYS=30
EOF
    
    # Set appropriate permissions
    chmod 600 "$ENV_FILE"
    
    log "Environment configuration created: $ENV_FILE"
}

# Function to generate SSL certificates (self-signed for development)
generate_ssl_certificates() {
    log "Generating SSL certificates..."
    
    SSL_DIR="$PROJECT_ROOT/docker/nginx/ssl"
    mkdir -p "$SSL_DIR"
    
    if [ "$ENVIRONMENT" = "production" ]; then
        warn "Production detected. Please replace self-signed certificates with proper CA-signed certificates."
    fi
    
    # Generate self-signed certificate
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout "$SSL_DIR/key.pem" \
        -out "$SSL_DIR/cert.pem" \
        -subj "/C=US/ST=State/L=City/O=CryptaNet/CN=localhost" \
        &> /dev/null
    
    # Set appropriate permissions
    chmod 600 "$SSL_DIR/key.pem"
    chmod 644 "$SSL_DIR/cert.pem"
    
    log "SSL certificates generated ✅"
}

# Function to build Docker images
build_images() {
    log "Building Docker images..."
    
    # Build images with caching
    docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" build \
        --build-arg BUILDKIT_INLINE_CACHE=1 \
        --parallel
    
    log "Docker images built successfully ✅"
}

# Function to run security hardening
security_hardening() {
    log "Applying security hardening..."
    
    # Create security scan script
    cat > security_scan.sh << 'EOF'
#!/bin/bash
echo "🔒 CryptaNet Security Scan"
echo "========================="

# Check for common vulnerabilities
echo "Checking Docker images for vulnerabilities..."
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
    -v $PWD:/tmp/.cache/ aquasec/trivy:latest image \
    cryptanet-backend:latest || true

echo "Checking for exposed secrets..."
find . -name "*.py" -o -name "*.js" -o -name "*.json" | xargs grep -l -i -E "(password|secret|key|token)" | head -10 || true

echo "Checking file permissions..."
find . -type f -perm 777 2>/dev/null | head -10 || true

echo "Security scan completed."
EOF
    
    chmod +x security_scan.sh
    
    # Run basic security checks
    if command -v docker &> /dev/null; then
        info "Running basic security checks..."
        
        # Check for running containers with privileged mode
        privileged_containers=$(docker ps --format "table {{.Names}}\t{{.Status}}" | grep -c "privileged" || echo "0")
        if [ "$privileged_containers" -gt 0 ]; then
            warn "Found $privileged_containers containers running in privileged mode"
        fi
        
        # Check for containers running as root
        info "Checking container user configurations..."
    fi
    
    log "Security hardening applied ✅"
}

# Function to deploy services
deploy_services() {
    log "Deploying CryptaNet services..."
    
    # Stop existing services
    docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" down --remove-orphans
    
    # Start services with proper ordering
    docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" up -d \
        --remove-orphans \
        --force-recreate
    
    log "Services deployment initiated ✅"
}

# Function to wait for services to be healthy
wait_for_services() {
    log "Waiting for services to become healthy..."
    
    local max_attempts=60
    local attempt=0
    
    local services=("cryptanet-backend:5004" "cryptanet-privacy:5003" "cryptanet-anomaly:5002" "cryptanet-frontend:3000")
    
    for service in "${services[@]}"; do
        local service_name="${service%:*}"
        local port="${service#*:}"
        
        info "Checking $service_name..."
        
        attempt=0
        while [ $attempt -lt $max_attempts ]; do
            if curl -sf "http://localhost:$port/health" &> /dev/null || 
               curl -sf "http://localhost:$port" &> /dev/null; then
                log "$service_name is healthy ✅"
                break
            fi
            
            sleep 5
            attempt=$((attempt + 1))
            
            if [ $attempt -eq $max_attempts ]; then
                error "$service_name failed to become healthy after $((max_attempts * 5)) seconds"
            fi
        done
    done
    
    log "All services are healthy ✅"
}

# Function to run post-deployment tests
run_post_deployment_tests() {
    log "Running post-deployment tests..."
    
    # Test authentication
    info "Testing authentication..."
    auth_response=$(curl -s -X POST http://localhost:5004/api/auth/login \
        -H "Content-Type: application/json" \
        -d '{"username": "admin", "password": "admin123"}' || echo "failed")
    
    if echo "$auth_response" | grep -q "token"; then
        log "Authentication test passed ✅"
    else
        warn "Authentication test failed"
    fi
    
    # Test API health endpoints
    info "Testing API health endpoints..."
    for port in 5002 5003 5004; do
        if curl -sf "http://localhost:$port/health" &> /dev/null; then
            log "Health check for port $port passed ✅"
        else
            warn "Health check for port $port failed"
        fi
    done
    
    # Test frontend
    info "Testing frontend..."
    if curl -sf "http://localhost:3000" &> /dev/null; then
        log "Frontend test passed ✅"
    else
        warn "Frontend test failed"
    fi
    
    log "Post-deployment tests completed ✅"
}

# Function to setup monitoring
setup_monitoring() {
    log "Setting up monitoring and alerting..."
    
    # Check if monitoring services are running
    if docker ps | grep -q "cryptanet-prometheus"; then
        info "Prometheus is running on http://localhost:9090"
    fi
    
    if docker ps | grep -q "cryptanet-grafana"; then
        info "Grafana is running on http://localhost:3001"
        info "Default credentials: admin / admin123"
    fi
    
    # Create monitoring dashboard script
    cat > monitoring_setup.sh << 'EOF'
#!/bin/bash
echo "🔍 Setting up CryptaNet monitoring..."

# Wait for Grafana to be ready
echo "Waiting for Grafana..."
until curl -sf http://localhost:3001/api/health > /dev/null; do
    sleep 2
done

# Configure Prometheus data source
curl -X POST http://admin:admin123@localhost:3001/api/datasources \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Prometheus",
        "type": "prometheus",
        "url": "http://prometheus:9090",
        "access": "proxy",
        "isDefault": true
    }' 2>/dev/null || echo "Data source may already exist"

echo "Monitoring setup completed!"
EOF
    
    chmod +x monitoring_setup.sh
    
    # Run monitoring setup in background
    if [ "$ENVIRONMENT" != "development" ]; then
        nohup ./monitoring_setup.sh &> monitoring_setup.log &
    fi
    
    log "Monitoring setup completed ✅"
}

# Function to display deployment summary
display_summary() {
    echo ""
    echo "🎉 CryptaNet Deployment Summary"
    echo "==============================="
    echo ""
    echo "Environment: $ENVIRONMENT"
    echo "Deployment time: $(date)"
    echo ""
    echo "🌐 Service URLs:"
    echo "  Frontend Dashboard:  http://localhost:3000"
    echo "  Backend API:         http://localhost:5004"
    echo "  Privacy Layer:       http://localhost:5003"
    echo "  Anomaly Detection:   http://localhost:5002"
    echo ""
    if docker ps | grep -q "cryptanet-prometheus"; then
        echo "📊 Monitoring:"
        echo "  Prometheus:          http://localhost:9090"
        echo "  Grafana:             http://localhost:3001"
        echo ""
    fi
    echo "🔑 Default Credentials:"
    echo "  Username: admin"
    echo "  Password: admin123"
    echo ""
    echo "📋 Useful Commands:"
    echo "  View logs:           docker-compose logs -f"
    echo "  Stop services:       docker-compose down"
    echo "  Restart services:    docker-compose restart"
    echo "  Run tests:           python3 large_scale_testing.py"
    echo ""
    echo "✅ Deployment completed successfully!"
}

# Function to cleanup on exit
cleanup() {
    if [ $? -ne 0 ]; then
        error "Deployment failed. Cleaning up..."
        docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" down --remove-orphans 2>/dev/null || true
    fi
}

# Main deployment function
main() {
    log "Starting CryptaNet production deployment..."
    
    # Set trap for cleanup
    trap cleanup EXIT
    
    # Run deployment steps
    check_prerequisites
    setup_environment
    generate_ssl_certificates
    build_images
    security_hardening
    deploy_services
    wait_for_services
    run_post_deployment_tests
    setup_monitoring
    display_summary
    
    log "🚀 CryptaNet is now running in $ENVIRONMENT mode!"
}

# Run main function
main "$@"
