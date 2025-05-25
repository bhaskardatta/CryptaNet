# CryptaNet Anomaly Detection Dockerfile
# Machine learning-based anomaly detection service

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r cryptanet && useradd -r -g cryptanet cryptanet

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories and set permissions
RUN mkdir -p /app/data /app/logs /app/models /app/saved_models && \
    chown -R cryptanet:cryptanet /app

# Environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Security: Run as non-root
USER cryptanet

# Expose port
EXPOSE 5002

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5002/health || exit 1

# Start command
CMD ["python", "simple_api_server.py"]
