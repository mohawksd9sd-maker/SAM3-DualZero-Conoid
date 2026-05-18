# ============================================
# SAM3-DualZero-Conoid Dockerfile
# Reproducible environment for the project
# ============================================

FROM python:3.12-slim

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Upgrade pip and install Python packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Environment variables for reproducibility
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Default command (you can change this later)
CMD ["python", "--version"]
