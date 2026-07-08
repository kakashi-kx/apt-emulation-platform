"""
Campaign Replay - Animated timeline of attack chain
"""

import json
import time
from datetime import datetime
from typing import List, Dict, Any

class CampaignReplay:
    """Replay a campaign step by step"""
    
    def __init__(self, results_file: str = "campaign_results.json"):
        self.results_file = results_file
        self.campaign_data = None
        self._load_data()
    
    def _load_data(self):
        """Load campaign data"""
        try:
            with open(self.results_file, 'r') as f:
                self.campaign_data = json.load(f)
        except:
            self.campaign_data = None
    
    def replay(self, delay: float = 0.5):
        """Replay the campaign with a delay between steps"""
        
        if not self.campaign_data:
            print("❌ No campaign data found")
            return
        
        print("\n" + "="*60)
        print("🎬 CAMPAIGN REPLAY")
        print("="*60)
        
        campaigns = self.campaign_data.get('campaigns', [])
        if not campaigns:
            print("❌ No campaigns found")
            return
        
        for campaign in campaigns:
            print(f"\n🎯 {campaign.get('campaign_name', 'Unknown Campaign')}")
            print("-" * 40)
            
            techniques = campaign.get('techniques_executed', [])
            detection_events = campaign.get('detection_events', [])
            detected_names = [e.get('technique') for e in detection_events]
            
            for i, tech in enumerate(techniques, 1):
                tech_name = tech.get('name', 'Unknown')
                detected = tech_name in detected_names
                
                # Visual progress
                bar = "█" * i + "░" * (len(techniques) - i)
                status = "🛡️ DETECTED" if detected else "✅ SUCCESS"
                
                print(f"[{i}/{len(techniques)}] {tech_name}")
                print(f"  {status}")
                print(f"  Progress: [{bar}]")
                
                time.sleep(delay)
            
            print("\n" + "="*60)
            print(f"📊 SUMMARY: {campaign.get('campaign_name')}")
            print(f"   Success Rate: {campaign.get('overall_success_rate', 0)*100:.1f}%")
            print(f"   Detection Rate: {campaign.get('detection_rate', 0)*100:.1f}%")
            print("="*60)
