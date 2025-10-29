# Dockerfile for building h3==3.7.7 on ARM64 architecture
# This builds h3 from source to support older versions on Apple Silicon

FROM python:3.11-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies required for building h3
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies first (for better caching)
COPY requirements.txt* ./
RUN pip install --upgrade pip setuptools wheel

# Install h3 version 3.7.7 from source
# This will compile the C library and Python bindings
RUN pip install --no-cache-dir h3==3.7.7

# Install other dependencies if requirements.txt exists
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# Copy the application code
COPY . .

# Install the consume package in development mode
RUN pip install -e .

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Default command
CMD ["python", "-c", "import h3; print(f'h3 version: {h3.__version__}'); import consume; print('CONSUME package imported successfully')"]
