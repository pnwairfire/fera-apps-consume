#!/bin/bash
# Build and run script for CONSUME Docker container with h3==3.7.7

set -e

echo "Building CONSUME Docker image with h3==3.7.7..."
docker build -t consume-h3:latest .

echo "Build complete! Testing the installation..."
docker run --rm consume-h3:latest

echo ""
echo "To run the container interactively:"
echo "docker run -it --rm consume-h3:latest /bin/bash"
echo ""
echo "To run with volume mounting (for development):"
echo "docker run -it --rm -v \$(pwd):/app consume-h3:latest /bin/bash"
