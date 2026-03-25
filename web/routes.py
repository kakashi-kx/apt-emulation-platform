"""
API Routes for Web Interface
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
import json
import os
import sys
from pathlib import Path
from datetime import datetime
import threading
import subprocess

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from emulation_engine.campaign_manager import CampaignManager
from reporting.report_generator import ReportGenerator

bp = Blueprint('main', __name__)

# Store running campaigns
running_campaigns = {}

@bp.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@bp.route('/dashboard')
def dashboard():
    """Dashboard with metrics"""
    return render_template('dashboard.html')

@bp.route('/campaigns')
def campaigns():
    """Run campaigns page"""
    return render_template('campaigns.html')

@bp.route('/results')
def results():
    """View results page"""
    return render_template('results.html')

@bp.route('/api/campaigns/run', methods=['POST'])
def run_campaign():
    """Run an APT campaign"""
    data = request.json
    apt_group = data.get('apt_group', 'apt29')
    detection_maturity = data.get('detection_maturity', 0.5)
    safe_mode = data.get('safe_mode', True)
    
    campaign_id = f"{apt_group}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Run campaign in background
    def run():
        try:
            manager = CampaignManager({
                'name': 'web_assessment',
                'detection_maturity': detection_maturity,
                'safe_mode': safe_mode
            })
            
            result = manager.run_campaign(apt_group)
            
            # Store result
            running_campaigns[campaign_id] = {
                'status': 'completed',
                'result': result.to_json(),
                'apt_group': apt_group,
                'success_rate': result.overall_success_rate,
                'detection_rate': result.detection_rate,
                'impact_score': result.impact_score
            }
            
            # Save to file
            manager.save_results(f"campaign_{campaign_id}.json")
            
        except Exception as e:
            running_campaigns[campaign_id] = {
                'status': 'failed',
                'error': str(e)
            }
    
    # Start background thread
    thread = threading.Thread(target=run)
    thread.start()
    
    running_campaigns[campaign_id] = {'status': 'running'}
    
    return jsonify({
        'campaign_id': campaign_id,
        'status': 'started',
        'message': f'Running {apt_group} campaign...'
    })

@bp.route('/api/campaigns/status/<campaign_id>', methods=['GET'])
def get_campaign_status(campaign_id):
    """Get campaign status"""
    if campaign_id in running_campaigns:
        return jsonify(running_campaigns[campaign_id])
    return jsonify({'status': 'not_found'})

@bp.route('/api/campaigns/list', methods=['GET'])
def list_campaigns():
    """List available APT groups"""
    manager = CampaignManager({})
    return jsonify({
        'available_groups': manager.list_available_apt_groups()
    })

@bp.route('/api/results/latest', methods=['GET'])
def get_latest_results():
    """Get latest campaign results"""
    # Find most recent campaign file
    import glob
    files = glob.glob('campaign_*.json')
    if files:
        latest = max(files, key=os.path.getctime)
        with open(latest, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    return jsonify({'error': 'No campaigns found'})

@bp.route('/api/reports/generate', methods=['POST'])
def generate_report():
    """Generate executive report"""
    data = request.json
    campaign_id = data.get('campaign_id')
    
    try:
        # Load campaign results
        with open(f'campaign_{campaign_id}.json', 'r') as f:
            campaign_data = json.load(f)
        
        # Generate HTML report
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>APT Emulation Report - {campaign_id}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background: #dc3545; color: white; padding: 20px; }}
                .metric {{ display: inline-block; margin: 20px; padding: 20px; background: #f8f9fa; }}
                .critical {{ color: #dc3545; }}
                .warning {{ color: #ffc107; }}
                .success {{ color: #28a745; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>APT Emulation Assessment Report</h1>
                <p>Campaign: {campaign_id}</p>
                <p>Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="metrics">
                <div class="metric">
                    <h3>Success Rate</h3>
                    <p class="critical">{campaign_data.get('campaigns', [{}])[0].get('overall_success_rate', 0)*100:.1f}%</p>
                </div>
                <div class="metric">
                    <h3>Detection Rate</h3>
                    <p class="warning">{campaign_data.get('campaigns', [{}])[0].get('detection_rate', 0)*100:.1f}%</p>
                </div>
                <div class="metric">
                    <h3>Impact Score</h3>
                    <p class="critical">{campaign_data.get('campaigns', [{}])[0].get('impact_score', 0):.1f}/10</p>
                </div>
            </div>
            
            <h2>Recommendations</h2>
            <ul>
                <li>Deploy EDR to all endpoints</li>
                <li>Enable MFA for admin accounts</li>
                <li>Implement email filtering</li>
                <li>Segment network infrastructure</li>
            </ul>
        </body>
        </html>
        """
        
        return html
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })
