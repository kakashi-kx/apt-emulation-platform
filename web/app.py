#!/usr/bin/env python3
"""
APT Emulation Platform - Advanced Web Interface
Enterprise-grade Flask application with proper security
"""

from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import sys
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import logging
from logging.handlers import RotatingFileHandler
import glob

sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# File handler for production logs
if not os.path.exists('logs'):
    os.makedirs('logs')
file_handler = RotatingFileHandler('logs/web.log', maxBytes=10000000, backupCount=3)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))
logger.addHandler(file_handler)

# Initialize Flask with security settings
app = Flask(__name__)

# Security: Use environment variable for secret key
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24).hex())
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# CORS - allow only specific origins in production
allowed_origins = os.environ.get('ALLOWED_ORIGINS', '*').split(',')
CORS(app, origins=allowed_origins)

# Rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per hour", "10 per minute"],
    storage_uri="memory://"
)

# Request tracking
request_id_header = 'X-Request-ID'

@app.before_request
def before_request():
    request.request_id = request.headers.get(request_id_header, str(uuid.uuid4()))

@app.after_request
def after_request(response):
    response.headers['X-Request-ID'] = getattr(request, 'request_id', 'unknown')
    return response

# ----------------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------------

@app.route('/')
def index():
    """Serve the main dashboard"""
    return render_template('index.html')

@app.route('/api/run', methods=['POST'])
@limiter.limit("5 per minute")
def run_campaign():
    """Execute an APT campaign with proper validation"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid request body'}), 400
        
        apt_group = data.get('apt_group', 'apt29')
        detection_maturity = data.get('detection_maturity', 0.5)
        safe_mode = data.get('safe_mode', True)
        
        # Validate inputs
        valid_groups = ['apt29', 'lazarus', 'ransomware']
        if apt_group not in valid_groups:
            return jsonify({'error': f'Invalid APT group: {apt_group}'}), 400
        
        if not 0 <= detection_maturity <= 1:
            return jsonify({'error': 'Detection maturity must be between 0 and 1'}), 400
        
        # Import and run
        from emulation_engine.campaign_manager import CampaignManager
        
        manager = CampaignManager({
            'name': 'web_assessment',
            'detection_maturity': detection_maturity,
            'safe_mode': safe_mode,
            'request_id': getattr(request, 'request_id', 'unknown')
        })
        
        result = manager.run_campaign(apt_group)
        
        # ✅ Use CampaignResult attributes correctly
        techniques = []
        for tech_result in result.technique_results:
            techniques.append({
                'id': tech_result.technique_id,
                'name': tech_result.technique_name,
                'tactic': tech_result.tactic,
                'success': tech_result.status.value == 'success',
                'detected': tech_result.detected
            })
        
        response = {
            'success': True,
            'campaign_id': result.campaign_id,
            'success_rate': result.success_rate,
            'detection_rate': result.detection_rate,
            'impact_score': result.impact_score,
            'duration': (result.end_time - result.start_time).total_seconds(),
            'techniques': techniques,
            'techniques_successful': result.successful,
            'techniques_failed': result.failed,
            'safe_mode_used': result.execution_mode.value == 'safe'
        }
        
        logger.info(f"Campaign {apt_group} completed: {response['success_rate']:.1%} success")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Campaign failed: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

# ----------------------------------------------------------------------------
# ✅ ADVANCED MITRE ATT&CK NAVIGATOR EXPORT
# ----------------------------------------------------------------------------
@app.route('/api/export/mitre', methods=['GET'])
def export_mitre_navigator():
    """
    Export results as MITRE ATT&CK Navigator layer
    This is the standard format used by blue teams worldwide
    """
    try:
        # Get the latest campaign results
        files = glob.glob('campaign_results.json')
        if not files:
            return jsonify({'error': 'No campaign results found'}), 404
        
        with open(files[-1], 'r') as f:
            data = json.load(f)
        
        # Build MITRE Navigator Layer
        navigator_layer = {
            "name": "APT Emulation Results",
            "version": "3.0",
            "domain": "enterprise-attack",
            "description": "Detection gaps identified from APT emulation",
            "techniques": []
        }
        
        # Extract techniques from campaigns
        for campaign in data.get('campaigns', []):
            for tech in campaign.get('techniques_executed', []):
                # Check if this technique was detected
                detected = False
                for event in campaign.get('detection_events', []):
                    if event.get('technique') == tech.get('name'):
                        detected = True
                        break
                
                navigator_layer['techniques'].append({
                    "techniqueID": tech.get('id', 'T0000'),
                    "score": 100 if detected else 50,
                    "comment": tech.get('name', 'Unknown'),
                    "metadata": [
                        {"name": "tactic", "value": tech.get('tactic', 'Unknown')},
                        {"name": "detected", "value": str(detected)}
                    ]
                })
        
        logger.info(f"MITRE Navigator export successful: {len(navigator_layer['techniques'])} techniques")
        return jsonify(navigator_layer)
        
    except Exception as e:
        logger.error(f"MITRE export failed: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

# ----------------------------------------------------------------------------
# ✅ HEALTH CHECK
# ----------------------------------------------------------------------------
@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.2',
        'timestamp': datetime.now().isoformat(),
        'endpoints': [
            '/',
            '/api/run (POST)',
            '/api/export/mitre (GET)',
            '/api/health (GET)'
        ]
    })

# ----------------------------------------------------------------------------
# Error handlers
# ----------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(429)
def rate_limit_error(error):
    return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429

# ----------------------------------------------------------------------------
# Main entry point
# ----------------------------------------------------------------------------

if __name__ == '__main__':
    # Production-ready configuration
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║     APT Emulation Platform - Enterprise Web Interface        ║
    ║                         v1.0.2                              ║
    ╠══════════════════════════════════════════════════════════════╣
    ║  🌐  http://{}:{}                                          ║
    ║  🔒  Debug: {}                                              ║
    ║  📋  Logs: ./logs/web.log                                  ║
    ║  🎯  MITRE Export: /api/export/mitre                      ║
    ║  ⏱️   Press Ctrl+C to stop                                 ║
    ╚══════════════════════════════════════════════════════════════╝
    """.format(host, port, "ON" if debug_mode else "OFF"))
    
    # Use Waitress for production, Flask dev server for development
    if debug_mode:
        app.run(debug=True, host=host, port=port)
    else:
        try:
            from waitress import serve
            logger.info("Starting Waitress production server...")
            serve(app, host=host, port=port, threads=4)
        except ImportError:
            logger.warning("Waitress not installed. Using Flask dev server.")
            app.run(debug=False, host=host, port=port)
