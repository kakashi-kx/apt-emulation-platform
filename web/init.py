"""
Web Interface for APT Emulation Platform
"""

from flask import Flask
from flask_cors import CORS
from flask_session import Session
import os

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-apt-platform')
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['UPLOAD_FOLDER'] = 'uploads'
    
    # Enable CORS
    CORS(app)
    
    # Initialize session
    Session(app)
    
    # Register routes
    from web import routes
    app.register_blueprint(routes.bp)
    
    return app
