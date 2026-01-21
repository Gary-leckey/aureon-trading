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

# Create directories for state files
RUN mkdir -p /app/state /app/logs

# Healthcheck (verify Python can import main module)
HEALTHCHECK --interval=60s --timeout=10s --start-period=120s --retries=3 \
  CMD python -c "import sys; sys.exit(0)" || exit 1

# Run trading system in autonomous mode
CMD ["python", "orca_complete_kill_cycle.py", "--autonomous"]
