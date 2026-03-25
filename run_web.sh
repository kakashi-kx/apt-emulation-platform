#!/bin/bash
# Startup script for APT Emulation Platform Web Interface

echo "🚀 Starting APT Emulation Platform Web Interface"
echo "================================================"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "✅ Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Creating..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ Installing dependencies..."
    pip install --upgrade pip
    pip install Flask==2.2.5 Flask-CORS==4.0.0 pyyaml colorama
fi

echo ""
echo "🌐 Starting web server..."
echo "   Open http://localhost:5000 in your browser"
echo "   Press Ctrl+C to stop"
echo ""

# Run the web app
python3 web_simple.py
