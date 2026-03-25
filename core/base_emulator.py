"""
Base classes for adversary emulation
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import logging
import time
import subprocess
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Technique:
    """MITRE ATT&CK Technique"""
    id: str
    name: str
    tactic: str
    platform: List[str]
    permissions: List[str]
    description: str
    detection_risk: float = 0.5
    success_rate: float = 0.7
    command: str = ""
    prerequisites: List[str] = field(default_factory=list)
    executed: bool = False
    success: bool = False
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'tactic': self.tactic,
            'platform': self.platform,
            'permissions': self.permissions,
            'description': self.description,
            'detection_risk': self.detection_risk,
            'success_rate': self.success_rate,
            'command': self.command
        }
    
    def execute(self) -> bool:
        """Execute the technique command"""
        if not self.command:
            logger.warning(f"No command defined for {self.name}")
            return False
        
        try:
            logger.info(f"Executing {self.name} ({self.id})...")
            result = subprocess.run(
                self.command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            self.executed = True
            self.success = result.returncode == 0
            
            if self.success:
                logger.info(f"✅ {self.name} executed successfully")
            else:
                logger.error(f"❌ {self.name} failed: {result.stderr}")
            
            return self.success
            
        except subprocess.TimeoutExpired:
            logger.error(f"Timeout executing {self.name}")
            return False
        except Exception as e:
            logger.error(f"Error executing {self.name}: {e}")
            return False


@dataclass
class EngagementResult:
    """Results from a single engagement"""
    timestamp: datetime
    campaign_name: str
    techniques_executed: List[Technique]
    successful_techniques: List[Technique]
    failed_techniques: List[Technique]
    detection_events: List[Dict]
    duration_seconds: float
    overall_success_rate: float
    detection_rate: float
    impact_score: float
    raw_logs: List[str] = field(default_factory=list)
    
    def to_json(self) -> str:
        return json.dumps({
            'timestamp': self.timestamp.isoformat(),
            'campaign_name': self.campaign_name,
            'total_techniques': len(self.techniques_executed),
            'successful_techniques': [t.id for t in self.successful_techniques],
            'failed_techniques': [t.id for t in self.failed_techniques],
            'detection_events': self.detection_events,
            'duration_seconds': self.duration_seconds,
            'overall_success_rate': self.overall_success_rate,
            'detection_rate': self.detection_rate,
            'impact_score': self.impact_score
        }, indent=2)
    
    def print_summary(self):
        """Print engagement summary to console"""
        print("\n" + "="*60)
        print(f"📊 ENGAGEMENT SUMMARY: {self.campaign_name}")
        print("="*60)
        print(f"⏱️  Duration: {self.duration_seconds:.2f} seconds")
        print(f"🎯 Techniques: {len(self.techniques_executed)} total")
        print(f"✅ Success Rate: {self.overall_success_rate*100:.1f}%")
        print(f"🛡️  Detection Rate: {self.detection_rate*100:.1f}%")
        print(f"💥 Impact Score: {self.impact_score:.2f}/10.0")
        print(f"\n⚠️  Failed Techniques:")
        for tech in self.failed_techniques:
            print(f"  - {tech.name} ({tech.id})")
        print(f"\n🚨 Detection Events: {len(self.detection_events)}")
        for event in self.detection_events[:5]:  # Show first 5
            print(f"  - {event.get('technique', 'Unknown')}: {event.get('alert', 'No alert')}")


class AdversaryEmulator(ABC):
    """Base class for adversary emulation"""
    
    def __init__(self, name: str, target_environment: Dict = None):
        self.name = name
        self.target = target_environment or {}
        self.techniques: List[Technique] = []
        self.executed_techniques = []
        self.detection_events = []
        self.start_time = None
        self.end_time = None
        
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize emulation environment"""
        pass
    
    @abstractmethod
    def get_technique_sequence(self) -> List[Technique]:
        """Get ordered list of techniques for this adversary"""
        pass
    
    def execute_technique(self, technique: Technique) -> Dict:
        """Execute a specific technique"""
        result = {
            'technique': technique.name,
            'id': technique.id,
            'success': False,
            'detected': False,
            'error': None
        }
        
        try:
            # Execute the technique
            success = technique.execute()
            result['success'] = success
            
            if success:
                self.executed_techniques.append(technique)
                # Check if detected (simulated)
                result['detected'] = self._check_detection(technique)
                if result['detected']:
                    self.detection_events.append({
                        'technique': technique.name,
                        'alert': f"Potential {technique.tactic} detected",
                        'timestamp': datetime.now().isoformat()
                    })
            else:
                result['error'] = "Execution failed"
                
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Error executing {technique.name}: {e}")
        
        return result
    
    def _check_detection(self, technique: Technique) -> bool:
        """Simulate detection based on technique risk and environment"""
        import random
        
        # Base detection probability from technique
        detection_prob = technique.detection_risk
        
        # Adjust based on environment security maturity
        env_maturity = self.target.get('detection_maturity', 0.5)
        
        # Higher maturity = higher detection chance
        final_prob = detection_prob * (1 + env_maturity) / 2
        
        return random.random() < final_prob
    
    def cleanup(self) -> bool:
        """Clean up after emulation"""
        logger.info(f"Cleaning up {self.name} campaign...")
        return True
    
    def run_campaign(self) -> EngagementResult:
        """Run complete adversary campaign"""
        self.start_time = datetime.now()
        
        try:
            # Initialize
            if not self.initialize():
                raise Exception("Failed to initialize environment")
            
            # Get technique sequence
            techniques = self.get_technique_sequence()
            logger.info(f"Starting {self.name} campaign with {len(techniques)} techniques")
            
            successful = []
            failed = []
            
            for i, technique in enumerate(techniques, 1):
                print(f"\n[{i}/{len(techniques)}] Executing {technique.name} ({technique.id})...")
                result = self.execute_technique(technique)
                
                if result['success']:
                    successful.append(technique)
                    print(f"  ✅ Success! Detected: {result['detected']}")
                else:
                    failed.append(technique)
                    print(f"  ❌ Failed: {result.get('error', 'Unknown error')}")
            
            self.end_time = datetime.now()
            duration = (self.end_time - self.start_time).total_seconds()
            
            # Calculate metrics
            total = len(techniques)
            success_rate = len(successful) / total if total > 0 else 0
            detection_rate = len(self.detection_events) / total if total > 0 else 0
            
            # Calculate impact score (simplified)
            impact_score = self._calculate_impact(successful, failed)
            
            # Cleanup
            self.cleanup()
            
            # Create result
            result = EngagementResult(
                timestamp=self.start_time,
                campaign_name=self.name,
                techniques_executed=techniques,
                successful_techniques=successful,
                failed_techniques=failed,
                detection_events=self.detection_events,
                duration_seconds=duration,
                overall_success_rate=success_rate,
                detection_rate=detection_rate,
                impact_score=impact_score
            )
            
            result.print_summary()
            return result
            
        except Exception as e:
            logger.error(f"Campaign failed: {e}")
            raise
    
    def _calculate_impact(self, successful: List[Technique], failed: List[Technique]) -> float:
        """Calculate business impact score"""
        # Simplified impact calculation
        critical_tactics = ['Privilege Escalation', 'Credential Access', 'Lateral Movement', 'Exfiltration']
        
        impact = 0
        for tech in successful:
            if tech.tactic in critical_tactics:
                impact += 2.5
            else:
                impact += 1
        
        return min(impact, 10.0)  # Cap at 10
