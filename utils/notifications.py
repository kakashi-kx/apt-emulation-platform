"""
Notifications - Send alerts to Slack/Discord
"""

import requests
import json
from typing import Dict, Any

class Notifier:
    """Send notifications to Slack/Discord"""
    
    def __init__(self, webhook_url: str = None, platform: str = "slack"):
        self.webhook_url = webhook_url
        self.platform = platform
    
    def send_campaign_result(self, result: Dict[str, Any], campaign_name: str):
        """Send campaign results to Slack/Discord"""
        
        if not self.webhook_url:
            print("⚠️ No webhook URL configured")
            return
        
        message = self._format_message(result, campaign_name)
        
        if self.platform == "slack":
            self._send_slack(message)
        elif self.platform == "discord":
            self._send_discord(message)
    
    def _format_message(self, result: Dict[str, Any], campaign_name: str) -> Dict:
        """Format message for Slack/Discord"""
        
        success_rate = result.get('overall_success_rate', 0) * 100
        detection_rate = result.get('detection_rate', 0) * 100
        
        return {
            "text": f"🔴 **APT Campaign Complete**",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"🎯 {campaign_name}"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Success Rate:*\n{success_rate:.1f}%"},
                        {"type": "mrkdwn", "text": f"*Detection Rate:*\n{detection_rate:.1f}%"}
                    ]
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Impact Score:*\n{result.get('impact_score', 0):.1f}/10"},
                        {"type": "mrkdwn", "text": f"*Techniques:*\n{result.get('total_techniques', 0)}"}
                    ]
                }
            ]
        }
    
    def _send_slack(self, message: Dict):
        """Send to Slack"""
        try:
            response = requests.post(self.webhook_url, json=message)
            if response.status_code == 200:
                print("✅ Slack notification sent")
            else:
                print(f"❌ Slack error: {response.status_code}")
        except Exception as e:
            print(f"❌ Failed to send Slack notification: {e}")
    
    def _send_discord(self, message: Dict):
        """Send to Discord"""
        try:
            payload = {"content": message.get('text', '')}
            response = requests.post(self.webhook_url, json=payload)
            if response.status_code == 204:
                print("✅ Discord notification sent")
            else:
                print(f"❌ Discord error: {response.status_code}")
        except Exception as e:
            print(f"❌ Failed to send Discord notification: {e}")
