"""
Campaign Manager - Orchestrates emulation campaigns
"""

from typing import List, Dict, Optional
from datetime import datetime
import json
import logging
from core.base_emulator import AdversaryEmulator, EngagementResult
from apt_profiles import APT29Emulator, LazarusEmulator, RansomwareEmulator

logger = logging.getLogger(__name__)


class CampaignManager:
    """Manages and orchestrates emulation campaigns"""
    
    def __init__(self, target_environment: Optional[Dict] = None):
        self.target_environment = target_environment or {}
        self.campaigns = []
        self.results = []
        
        # Register available emulators
        self.emulators = {
            'apt29': APT29Emulator,
            'lazarus': LazarusEmulator,
            'ransomware': RansomwareEmulator
        }
    
    def list_available_apt_groups(self) -> List[str]:
        """List all available APT groups"""
        return list(self.emulators.keys())
    
    def run_campaign(self, apt_group: str) -> EngagementResult:
        """Run a single campaign for specified APT group"""
        
        if apt_group not in self.emulators:
            raise ValueError(f"Unknown APT group: {apt_group}. Available: {self.list_available_apt_groups()}")
        
        logger.info(f"Starting {apt_group} campaign...")
        
        # Create emulator instance
        emulator_class = self.emulators[apt_group]
        emulator = emulator_class(self.target_environment)
        
        # Run campaign
        result = emulator.run_campaign()
        
        # Store result
        self.results.append(result)
        
        return result
    
    def run_all_campaigns(self) -> List[EngagementResult]:
        """Run all available APT campaigns"""
        results = []
        
        for apt_group in self.list_available_apt_groups():
            try:
                result = self.run_campaign(apt_group)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to run {apt_group}: {e}")
        
        return results
    
    def save_results(self, filename: str = "campaign_results.json"):
        """Save all results to JSON file"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'target_environment': self.target_environment,
            'campaigns': [result.to_json() for result in self.results]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Results saved to {filename}")
    
    def compare_campaigns(self) -> Dict:
        """Compare results across campaigns"""
        comparison = {
            'campaigns': [],
            'metrics': {}
        }
        
        for result in self.results:
            comparison['campaigns'].append({
                'name': result.campaign_name,
                'success_rate': result.overall_success_rate,
                'detection_rate': result.detection_rate,
                'impact_score': result.impact_score,
                'duration': result.duration_seconds
            })
        
        # Calculate averages
        if self.results:
            comparison['metrics']['avg_success_rate'] = sum(r.overall_success_rate for r in self.results) / len(self.results)
            comparison['metrics']['avg_detection_rate'] = sum(r.detection_rate for r in self.results) / len(self.results)
            comparison['metrics']['avg_impact'] = sum(r.impact_score for r in self.results) / len(self.results)
        
        return comparison
