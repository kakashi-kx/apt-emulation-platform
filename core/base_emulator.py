"""
Base classes for adversary emulation
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import logging
import subprocess
import random
import os

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
    safe_mode: bool = True  # ✅ NEW: Safe mode per technique
    
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
        """Execute the technique command with safe_mode support"""
        if not self.command:
            logger.warning(f"No command defined for {self.name}")
            return False
        
        # ✅ FIX: Check safe_mode
        if self.safe_mode:
            logger.info(f"[SAFE MODE] Would execute: {self.command}")
            self.executed = True
            self.success = True
            return True
        
        try:
            logger.info(f"Executing {self.name} ({self.id})...")
            
            # ✅ FIX: Use list form for safety, but keep shell for complex commands
            # For simple commands, use list; for complex, use shell with caution
            if '|' in self.command or ';' in self.command or '&&' in self.command:
                result = subprocess.run(
                    self.command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
            else:
                # Safer: split command into list
                cmd_parts = self.command.split()
                result = subprocess.run(
                    cmd_parts,
                    capture_output=True,
                    text=True,
                    timeout=10
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
    safe_mode_used: bool = True  # ✅ NEW: Track if safe mode was used
    
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
            'impact_score': self.impact_score,
            'safe_mode_used': self.safe_mode_used
        }, indent=2)
    
    def print_summary(self):
        """Print engagement summary"""
        print("\n" + "="*60)
        print(f"📊 ENGAGEMENT SUMMARY: {self.campaign_name}")
        print("="*60)
        print(f"⏱️  Duration: {self.duration_seconds:.2f} seconds")
        print(f"🎯 Techniques: {len(self.techniques_executed)} total")
        print(f"✅ Success Rate: {self.overall_success_rate*100:.1f}%")
        print(f"🛡️  Detection Rate: {self.detection_rate*100:.1f}%")
        print(f"💥 Impact Score: {self.impact_score:.2f}/10.0")
        if self.safe_mode_used:
            print("🔒 SAFE MODE: Enabled (no actual commands executed)")


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
        
        # ✅ FIX: Read safe_mode from environment
        self.safe_mode = self.target.get('safe_mode', True)
    
    @abstractmethod
    def get_technique_sequence(self) -> List[Technique]:
        """Get ordered list of techniques for this adversary"""
        pass
    
    def initialize(self) -> bool:
        """Initialize emulation environment"""
        mode = "SAFE" if self.safe_mode else "REAL"
        logger.info(f"Initializing {self.name} emulation in {mode} mode")
        return True
    
    def execute_technique(self, technique: Technique) -> Dict:
        """Execute a specific technique with safe_mode"""
        # ✅ FIX: Apply safe_mode to technique
        technique.safe_mode = self.safe_mode
        
        result = {
            'technique': technique.name,
            'id': technique.id,
            'success': False,
            'detected': False,
            'error': None
        }
        
        try:
            success = technique.execute()
            result['success'] = success
            
            if success:
                self.executed_techniques.append(technique)
                result['detected'] = self._check_detection(technique)
                if result['detected']:
                    self.detection_events.append({
                        'technique': technique.name,
                        'alert': f"Potential {technique.tactic} detected",
                        'timestamp': datetime.now().isoformat()
                    })
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Error executing {technique.name}: {e}")
        
        return result
    
    def _check_detection(self, technique: Technique) -> bool:
        """Simulate detection based on technique risk"""
        # ✅ FIX: This is SIMULATED detection, not real telemetry
        detection_prob = technique.detection_risk
        env_maturity = self.target.get('detection_maturity', 0.5)
        final_prob = detection_prob * (1 + env_maturity) / 2
        detected = random.random() < final_prob
        
        logger.debug(f"Detection check for {technique.name}: {detected} (prob={final_prob:.2f})")
        return detected
    
    def cleanup(self) -> bool:
        """Clean up after emulation"""
        logger.info(f"Cleaning up {self.name} campaign...")
        return True
    
    def run_campaign(self) -> EngagementResult:
        """Run complete adversary campaign"""
        self.start_time = datetime.now()
        
        try:
            self.initialize()
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
            
            total = len(techniques)
            success_rate = len(successful) / total if total > 0 else 0
            detection_rate = len(self.detection_events) / total if total > 0 else 0
            impact_score = min(len(successful) * 0.8, 10.0)
            
            self.cleanup()
            
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
                impact_score=impact_score,
                safe_mode_used=self.safe_mode
            )
            
            result.print_summary()
            return result
            
        except Exception as e:
            logger.error(f"Campaign failed: {e}")
            raise
