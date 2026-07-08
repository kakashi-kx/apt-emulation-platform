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
        except Exception as e:
            print(f"❌ Failed to load {self.results_file}: {e}")
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
            
            # ✅ FIX: Use 'technique_results' instead of 'techniques_executed'
            technique_results = campaign.get('technique_results', [])
            
            if not technique_results:
                print("⚠️ No technique results found (campaign may have been run in safe mode)")
                print(f"   Success Rate: {campaign.get('success_rate', 0)*100:.1f}%")
                continue
            
            total = len(technique_results)
            
            for i, tech in enumerate(technique_results, 1):
                tech_name = tech.get('technique_name', 'Unknown')
                status = tech.get('status', 'unknown')
                detected = tech.get('detected', False)
                tech_id = tech.get('technique_id', '')
                
                # Visual progress
                bar = "█" * i + "░" * (total - i)
                status_display = "🛡️ DETECTED" if detected else "✅ SUCCESS"
                
                print(f"[{i}/{total}] {tech_name} ({tech_id})")
                print(f"  {status_display}")
                print(f"  Progress: [{bar}]")
                print(f"  Status: {status}")
                
                time.sleep(delay)
            
            print("\n" + "="*60)
            print(f"📊 SUMMARY: {campaign.get('campaign_name')}")
            print(f"   Success Rate: {campaign.get('success_rate', 0)*100:.1f}%")
            print(f"   Detection Rate: {campaign.get('detection_rate', 0)*100:.1f}%")
            print("="*60)
