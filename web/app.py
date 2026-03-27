#!/usr/bin/env python3
"""
APT Emulation Platform - Simple Web Interface
"""

from flask import Flask, render_template, jsonify, request
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/run', methods=['POST'])
def run_campaign():
    """Run an APT campaign"""
    data = request.json
    apt_group = data.get('apt_group', 'apt29')
    detection_maturity = data.get('detection_maturity', 0.5)
    safe_mode = data.get('safe_mode', True)
    
    try:
        from emulation_engine.campaign_manager import CampaignManager
        
        manager = CampaignManager({
            'name': 'web_assessment',
            'detection_maturity': detection_maturity,
            'safe_mode': safe_mode
        })
        
        result = manager.run_campaign(apt_group)
        
        # Format techniques for display
        techniques = []
        for tech in result.techniques_executed:
            techniques.append({
                'id': tech.id,
                'name': tech.name,
                'tactic': tech.tactic,
                'success': tech in result.successful_techniques,
                'detected': any(e.get('technique') == tech.name for e in result.detection_events)
            })
        
        return jsonify({
            'success': True,
            'success_rate': result.overall_success_rate,
            'detection_rate': result.detection_rate,
            'impact_score': result.impact_score,
            'duration': result.duration_seconds,
            'techniques': techniques,
            'techniques_successful': len(result.successful_techniques),
            'techniques_failed': len(result.failed_techniques)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'version': '1.0'})

if __name__ == '__main__':
    print()
    print("\033[95m" + "=" * 60 + "\033[0m")
    print("\033[96m   ⛓ APT Emulation Platform - Web Interface\033[0m")
    print("\033[95m" + "=" * 60 + "\033[0m")
    print()
    print("   \033[92m🕸\033[0m Open \033[94mhttp://localhost:5000\033[0m in your browser")
    print()
    print("   \033[93m⚠︎\033[0m Press Ctrl+C to stop the server")
    print()
    print("\033[95m" + "=" * 60 + "\033[0m")
    app.run(debug=True, host='0.0.0.0', port=5000)
