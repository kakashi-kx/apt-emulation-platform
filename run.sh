#!/bin/bash
# Production startup script for APT Emulation Platform

set -e

echo "🚀 Starting APT Emulation Platform (Production)"

# Check for virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
pip install -r web/requirements-web.txt 2>/dev/null || true

# Create required directories
mkdir -p logs reports

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Set default environment variables if not set
export FLASK_DEBUG=${FLASK_DEBUG:-false}
export SECRET_KEY=${SECRET_KEY:-$(python3 -c "import secrets; print(secrets.token_hex(32))")}
export PORT=${PORT:-5000}
export HOST=${HOST:-0.0.0.0}

echo "🔒 Security: Secret key set, Debug mode: $FLASK_DEBUG"
echo "🌐 Starting server on http://$HOST:$PORT"

# Run the application
if [ "$FLASK_DEBUG" = "true" ]; then
    python3 web/app.py
else
    # Production: Use Waitress or Gunicorn
    if command -v waitress-serve &> /dev/null; then
        waitress-serve --host=$HOST --port=$PORT web.app:app
    else
        python3 web/app.py
    fi
fi
