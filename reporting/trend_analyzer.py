"""
Detection Trend Analyzer - Track improvements over time
"""

import json
import glob
from datetime import datetime
from typing import List, Dict, Any

class TrendAnalyzer:
    """Analyze detection trends across multiple campaigns"""
    
    def __init__(self, report_dir: str = "."):
        self.report_dir = report_dir
        self.campaigns = []
        self._load_campaigns()
    
    def _load_campaigns(self):
        """Load all campaign results"""
        files = glob.glob(f"{self.report_dir}/campaign_*.json")
        files.extend(glob.glob(f"{self.report_dir}/campaign_results.json"))
        
        for file in files:
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    timestamp = data.get('timestamp', datetime.now().isoformat())
                    if isinstance(timestamp, str):
                        timestamp = datetime.fromisoformat(timestamp)
                    
                    self.campaigns.append({
                        'timestamp': timestamp,
                        'data': data,
                        'file': file
                    })
            except Exception as e:
                print(f"⚠️ Could not load {file}: {e}")
        
        self.campaigns.sort(key=lambda x: x['timestamp'])
    
    def get_trend_report(self) -> Dict[str, Any]:
        """Generate trend report"""
        
        if len(self.campaigns) < 2:
            return {
                'status': 'insufficient_data',
                'message': 'Need at least 2 campaigns for trend analysis',
                'campaigns_found': len(self.campaigns)
            }
        
        # Calculate trends
        first = self.campaigns[0]['data']
        last = self.campaigns[-1]['data']
        
        # Extract metrics from campaigns
        def get_metrics(data):
            if 'campaigns' in data and data['campaigns']:
                # New format
                campaigns = data['campaigns']
                success_rates = [c.get('overall_success_rate', 0) or c.get('success_rate', 0) for c in campaigns]
                detection_rates = [c.get('detection_rate', 0) for c in campaigns]
                avg_success = sum(success_rates) / len(success_rates) if success_rates else 0
                avg_detection = sum(detection_rates) / len(detection_rates) if detection_rates else 0
                return avg_success, avg_detection
            else:
                # Old format
                return data.get('overall_success_rate', 0), data.get('detection_rate', 0)
        
        first_success, first_detection = get_metrics(first)
        last_success, last_detection = get_metrics(last)
        
        return {
            'status': 'success',
            'campaigns_analyzed': len(self.campaigns),
            'time_period': {
                'start': self.campaigns[0]['timestamp'].isoformat(),
                'end': self.campaigns[-1]['timestamp'].isoformat()
            },
            'improvements': {
                'success_rate': {
                    'before': first_success,
                    'after': last_success,
                    'change': last_success - first_success,
                    'trend': '✅ Improved' if last_success < first_success else '⚠️ Worsened'
                },
                'detection_rate': {
                    'before': first_detection,
                    'after': last_detection,
                    'change': last_detection - first_detection,
                    'trend': '✅ Improved' if last_detection > first_detection else '⚠️ Worsened'
                }
            },
            'message': self._get_message(first_success, last_success, 
                                         first_detection, last_detection),
            'campaigns': [
                {
                    'timestamp': c['timestamp'].isoformat(),
                    'file': c['file']
                }
                for c in self.campaigns
            ]
        }
    
    def _get_message(self, fs, ls, fd, ld) -> str:
        """Generate human-readable message"""
        if ls < fs and ld > fd:
            return "🎉 Great improvement! Detection rate increased while success rate decreased."
        elif ld > fd:
            return f"✅ Detection rate improved by {(ld - fd)*100:.1f}%. Keep going!"
        elif ld < fd:
            return f"⚠️ Detection rate decreased by {(fd - ld)*100:.1f}%. Review your changes."
        else:
            return "📊 No significant change. Try new techniques."
    
    def print_report(self):
        """Print trend report to console"""
        report = self.get_trend_report()
        
        print("\n" + "="*60)
        print("📊 DETECTION TREND REPORT")
        print("="*60)
        
        if report['status'] == 'insufficient_data':
            print(f"⚠️ {report['message']}")
            print(f"   Campaigns found: {report['campaigns_found']}")
            return
        
        print(f"📅 Period: {report['time_period']['start']} → {report['time_period']['end']}")
        print(f"📊 Campaigns Analyzed: {report['campaigns_analyzed']}")
        print()
        
        print("📈 SUCCESS RATE:")
        print(f"   Before: {report['improvements']['success_rate']['before']*100:.1f}%")
        print(f"   After:  {report['improvements']['success_rate']['after']*100:.1f}%")
        print(f"   Change: {report['improvements']['success_rate']['change']*100:+.1f}% {report['improvements']['success_rate']['trend']}")
        print()
        
        print("🛡️ DETECTION RATE:")
        print(f"   Before: {report['improvements']['detection_rate']['before']*100:.1f}%")
        print(f"   After:  {report['improvements']['detection_rate']['after']*100:.1f}%")
        print(f"   Change: {report['improvements']['detection_rate']['change']*100:+.1f}% {report['improvements']['detection_rate']['trend']}")
        print()
        
        print(f"💬 {report['message']}")
        print("="*60)
