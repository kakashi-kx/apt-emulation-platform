#!/bin/bash
# Startup script for web interface

echo "🚀 Starting APT Emulation Platform Web Interface"
echo "================================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install web dependencies
echo "Installing web dependencies..."
pip install -r requirements-web.txt

# Run the web application
echo "Starting Flask server..."
echo "🌐 Open http://localhost:5000 in your browser"
echo "Press Ctrl+C to stop"

export FLASK_APP=web/app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
