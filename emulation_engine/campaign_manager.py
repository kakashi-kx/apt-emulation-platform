"""
Campaign Manager - Orchestrates emulation campaigns
"""

from typing import List, Dict, Optional
from datetime import datetime
import json
import logging
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.base_emulator import AdversaryEmulator, EngagementResult

logger = logging.getLogger(__name__)


class CampaignManager:
    """Manages and orchestrates emulation campaigns"""
    
    def __init__(self, target_environment: Optional[Dict] = None):
        self.target_environment = target_environment or {}
        self.campaigns = []
        self.results = []
        self.emulators = {}
        
        # Dynamically import APT profiles
        self._load_emulators()
    
    def _load_emulators(self):
        """Load available APT emulators"""
        try:
            from apt_profiles.apt29 import APT29Emulator
            self.emulators['apt29'] = APT29Emulator
            logger.info("✅ Loaded APT29 emulator")
        except ImportError as e:
            logger.warning(f"Could not load APT29: {e}")
        
        try:
            from apt_profiles.lazarus import LazarusEmulator
            self.emulators['lazarus'] = LazarusEmulator
            logger.info("✅ Loaded Lazarus emulator")
        except ImportError as e:
            logger.warning(f"Could not load Lazarus: {e}")
        
        try:
            from apt_profiles.ransomware import RansomwareEmulator
            self.emulators['ransomware'] = RansomwareEmulator
            logger.info("✅ Loaded Ransomware emulator")
        except ImportError as e:
            logger.warning(f"Could not load Ransomware: {e}")
    
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
                logger.info(f"\n{'='*60}")
                logger.info(f"Running {apt_group.upper()} campaign")
                logger.info(f"{'='*60}")
                result = self.run_campaign(apt_group)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to run {apt_group}: {e}")
                import traceback
                traceback.print_exc()
        
        return results
    
    def save_results(self, filename: str = "campaign_results.json"):
        """Save all results to JSON file"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'target_environment': self.target_environment,
            'campaigns': []
        }
        
        for result in self.results:
            data['campaigns'].append(json.loads(result.to_json()))
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"✅ Results saved to {filename}")
