#!/bin/bash
echo "Starting Railway deployment..."
echo "Environment: $(env | grep -E '^(PORT|RAILWAY_)')"
echo "Python version: $(python --version)"
echo "Working directory: $(pwd)"
echo "Files in directory: $(ls -la)"

# Set default port if not provided
export PORT=${PORT:-8000}
echo "Using port: $PORT"

# Start the application
echo "Starting uvicorn..."
python -m uvicorn minimal_test:app --host 0.0.0.0 --port $PORT --log-level info
