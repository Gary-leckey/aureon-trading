# 🦈 Aureon Trading System - DigitalOcean Deployment
# Production-ready Docker image for autonomous trading

FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONIOENCODING=utf-8
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8080
ENV AUREON_STATE_DIR=/app/state

# Create directories for state files
RUN mkdir -p /app/state /app/logs

# Expose HTTP port for DO App Platform (only for web service)
EXPOSE 8080

# Default command for web service (worker overrides via app.yaml run_command)
CMD ["python", "-u", "aureon_command_center_ui.py"]
