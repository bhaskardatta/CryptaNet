# Backend Service Dockerfile - Production Ready
# ==============================================

FROM python:3.11-slim as base

# Security: Create non-root user
RUN groupadd -r cryptanet && useradd -r -g cryptanet cryptanet

# System dependencies and security updates
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories and set permissions
RUN mkdir -p /app/data /app/logs /app/models \
    && chown -R cryptanet:cryptanet /app

# Security: Switch to non-root user
USER cryptanet

# Expose port
EXPOSE 5004

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5004/health || exit 1

# Environment variables
ENV FLASK_APP=simple_backend.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Start the application
CMD ["python", "simple_backend.py"]
