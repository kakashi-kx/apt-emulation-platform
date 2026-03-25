#!/usr/bin/env python3
"""
Simple Web Interface for APT Emulation Platform
"""

from flask import Flask, render_template_string, jsonify, request
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

app = Flask(__name__)

# HTML Template
HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>APT Emulation Platform</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 48px;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 18px;
            opacity: 0.9;
        }
        
        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .card h3 {
            color: #333;
            font-size: 24px;
            margin-bottom: 10px;
        }
        
        .card .badge {
            display: inline-block;
            background: #dc3545;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 12px;
            margin-bottom: 15px;
        }
        
        .card .techniques {
            color: #666;
            font-size: 14px;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid #eee;
        }
        
        .control-panel {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .control-panel h2 {
            margin-bottom: 20px;
            color: #333;
        }
        
        select {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            margin-bottom: 15px;
            cursor: pointer;
        }
        
        button {
            width: 100%;
            padding: 12px;
            background: #dc3545;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        
        button:hover {
            background: #c82333;
        }
        
        .result {
            margin-top: 20px;
            padding: 15px;
            border-radius: 8px;
            display: none;
        }
        
        .result.running {
            display: block;
            background: #fff3cd;
            color: #856404;
            border: 1px solid #ffc107;
        }
        
        .result.complete {
            display: block;
            background: #d4edda;
            color: #155724;
            border: 1px solid #28a745;
        }
        
        .result.error {
            display: block;
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #dc3545;
        }
        
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }
        
        .metric {
            background: white;
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .metric h3 {
            color: #666;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }
        
        .metric-value {
            font-size: 36px;
            font-weight: bold;
            color: #dc3545;
        }
        
        .footer {
            text-align: center;
            color: white;
            margin-top: 40px;
            opacity: 0.8;
        }
        
        @media (max-width: 768px) {
            body {
                padding: 20px;
            }
            .header h1 {
                font-size: 32px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 APT Emulation Platform</h1>
            <p>Simulate real APT attacks and quantify business risk</p>
        </div>
        
        <div class="cards">
            <div class="card">
                <div class="badge">Russian State-Sponsored</div>
                <h3>APT29</h3>
                <p>Cozy Bear - Nobelium</p>
                <div class="techniques">11 MITRE ATT&CK techniques: Spearphishing, PowerShell, LSASS Dump, Lateral Movement</div>
            </div>
            
            <div class="card">
                <div class="badge">North Korean</div>
                <h3>Lazarus</h3>
                <p>Hidden Cobra</p>
                <div class="techniques">7 MITRE ATT&CK techniques: Spearphishing, User Execution, Data Destruction</div>
            </div>
            
            <div class="card">
                <div class="badge">Modern Operators</div>
                <h3>Ransomware</h3>
                <p>Typical Ransomware Kill Chain</p>
                <div class="techniques">7 MITRE ATT&CK techniques: Exploit, Process Injection, Data Encryption</div>
            </div>
        </div>
        
        <div class="control-panel">
            <h2>🚀 Run APT Campaign</h2>
            <select id="aptGroup">
                <option value="apt29">APT29 (Cozy Bear) - Russian State-Sponsored</option>
                <option value="lazarus">Lazarus Group - North Korean</option>
                <option value="ransomware">Ransomware Operator</option>
            </select>
            <button onclick="runCampaign()">▶ Run Campaign</button>
            <div id="result" class="result"></div>
        </div>
        
        <div class="metrics">
            <div class="metric">
                <h3>Attack Success Rate</h3>
                <div class="metric-value" id="successRate">--%</div>
            </div>
            <div class="metric">
                <h3>Detection Rate</h3>
                <div class="metric-value" id="detectionRate">--%</div>
            </div>
            <div class="metric">
                <h3>Business Impact</h3>
                <div class="metric-value" id="impactScore">--/10</div>
            </div>
        </div>
        
        <div class="footer">
            <p>Powered by MITRE ATT&CK Framework | Simulates Real Adversary Behavior</p>
        </div>
    </div>
    
    <script>
        async function runCampaign() {
            const aptGroup = document.getElementById('aptGroup').value;
            const resultDiv = document.getElementById('result');
            
            resultDiv.className = 'result running';
            resultDiv.innerHTML = '🏃 Running campaign... This may take a few seconds.';
            
            try {
                const response = await fetch('/api/run', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({apt_group: aptGroup})
                });
                const data = await response.json();
                
                if (data.error) {
                    resultDiv.className = 'result error';
                    resultDiv.innerHTML = `❌ Error: ${data.error}`;
                } else {
                    resultDiv.className = 'result complete';
                    resultDiv.innerHTML = `
                        ✅ Campaign Complete!<br><br>
                        📊 Success Rate: ${(data.success_rate * 100).toFixed(1)}%<br>
                        🛡️ Detection Rate: ${(data.detection_rate * 100).toFixed(1)}%<br>
                        💥 Impact Score: ${data.impact_score.toFixed(1)}/10<br>
                        ✅ Successful Techniques: ${data.techniques_successful}<br>
                        ❌ Failed Techniques: ${data.techniques_failed}
                    `;
                    
                    document.getElementById('successRate').innerHTML = (data.success_rate * 100).toFixed(1) + '%';
                    document.getElementById('detectionRate').innerHTML = (data.detection_rate * 100).toFixed(1) + '%';
                    document.getElementById('impactScore').innerHTML = data.impact_score.toFixed(1);
                }
                
            } catch (error) {
                resultDiv.className = 'result error';
                resultDiv.innerHTML = `❌ Error: ${error.message}`;
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/run', methods=['POST'])
def run_campaign():
    """Run an APT campaign"""
    data = request.json
    apt_group = data.get('apt_group', 'apt29')
    
    try:
        from emulation_engine.campaign_manager import CampaignManager
        
        manager = CampaignManager({
            'name': 'web_assessment',
            'detection_maturity': 0.5,
            'safe_mode': True
        })
        
        result = manager.run_campaign(apt_group)
        
        return jsonify({
            'success': True,
            'success_rate': result.overall_success_rate,
            'detection_rate': result.detection_rate,
            'impact_score': result.impact_score,
            'techniques_successful': len(result.successful_techniques),
            'techniques_failed': len(result.failed_techniques)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'version': '1.0'})

if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║     APT Emulation Platform - Web Interface                ║
    ║                                                           ║
    ║     🌐 Open http://localhost:5000 in your browser        ║
    ║                                                           ║
    ║     Press Ctrl+C to stop the server                      ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    app.run(debug=True, host='0.0.0.0', port=5000)
