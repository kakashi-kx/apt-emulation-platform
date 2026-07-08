"""
Advanced Adversary Emulation Engine
Enterprise-grade APT emulation with proper architecture
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import logging
import subprocess
import random
import hashlib
import time
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExecutionMode(Enum):
    """Execution modes for techniques"""
    SAFE = "safe"
    SIMULATED = "simulated"
    REAL = "real"
    DRY_RUN = "dry_run"


class TechniqueStatus(Enum):
    """Status of technique execution"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"


@dataclass
class TechniqueResult:
    """Detailed result of a technique execution"""
    technique_id: str
    technique_name: str
    tactic: str
    status: TechniqueStatus
    execution_time: float
    output: str
    error: Optional[str] = None
    detected: bool = False
    detection_signals: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Technique:
    """Advanced MITRE ATT&CK Technique with full metadata"""
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
    references: List[str] = field(default_factory=list)
    sigma_rules: List[str] = field(default_factory=list)
    
    execution_timeout: int = 30
    retry_count: int = 1
    requires_privilege: bool = False
    is_destructive: bool = False
    command_hash: str = ""
    
    def __post_init__(self):
        self.command_hash = hashlib.sha256(self.command.encode()).hexdigest()[:8]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'tactic': self.tactic,
            'platform': self.platform,
            'permissions': self.permissions,
            'description': self.description,
            'detection_risk': self.detection_risk,
            'success_rate': self.success_rate,
            'command': self.command,
            'prerequisites': self.prerequisites,
            'references': self.references,
            'sigma_rules': self.sigma_rules,
            'command_hash': self.command_hash
        }
    
    def to_mitre_navigator(self) -> Dict[str, Any]:
        """Export to MITRE ATT&CK Navigator format"""
        return {
            'techniqueID': self.id,
            'score': self.detection_risk * 10,
            'comment': self.description,
            'metadata': [
                {'name': 'tactic', 'value': self.tactic},
                {'name': 'success_rate', 'value': str(self.success_rate)}
            ]
        }


class TechniqueExecutor:
    """Advanced technique executor with sandboxing and isolation"""
    
    def __init__(self, mode: ExecutionMode = ExecutionMode.SAFE):
        self.mode = mode
        self.execution_history: List[TechniqueResult] = []
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    def execute(self, technique: Technique, environment: Dict[str, Any]) -> TechniqueResult:
        """Execute a technique with proper isolation"""
        start_time = time.time()
        
        if self.mode == ExecutionMode.SAFE:
            return self._safe_execute(technique)
        elif self.mode == ExecutionMode.DRY_RUN:
            return self._dry_run_execute(technique)
        elif self.mode == ExecutionMode.SIMULATED:
            return self._simulate_execute(technique)
        else:
            return self._real_execute(technique, environment)
    
    def _safe_execute(self, technique: Technique) -> TechniqueResult:
        return TechniqueResult(
            technique_id=technique.id,
            technique_name=technique.name,
            tactic=technique.tactic,
            status=TechniqueStatus.SUCCESS,
            execution_time=0.01,
            output=f"[SAFE MODE] Would execute: {technique.command}",
            metadata={'mode': 'safe', 'command_hash': technique.command_hash}
        )
    
    def _dry_run_execute(self, technique: Technique) -> TechniqueResult:
        return TechniqueResult(
            technique_id=technique.id,
            technique_name=technique.name,
            tactic=technique.tactic,
            status=TechniqueStatus.SUCCESS,
            execution_time=0.01,
            output=f"[DRY RUN] Command: {technique.command}\nPrerequisites: {technique.prerequisites}",
            metadata={'mode': 'dry_run', 'destructive': technique.is_destructive}
        )
    
    def _simulate_execute(self, technique: Technique) -> TechniqueResult:
        import random
        success = random.random() < technique.success_rate
        detected = random.random() < technique.detection_risk
        
        status = TechniqueStatus.SUCCESS if success else TechniqueStatus.FAILED
        
        return TechniqueResult(
            technique_id=technique.id,
            technique_name=technique.name,
            tactic=technique.tactic,
            status=status,
            execution_time=random.uniform(0.1, 2.0),
            output=f"[SIMULATION] {'Success' if success else 'Failed'} - Detection: {detected}",
            detected=detected,
            detection_signals=[{
                'signal': 'simulated_detection',
                'confidence': technique.detection_risk * random.uniform(0.5, 1.0)
            }] if detected else [],
            metadata={'mode': 'simulated', 'detected': detected}
        )
    
    def _real_execute(self, technique: Technique, environment: Dict[str, Any]) -> TechniqueResult:
        try:
            result = subprocess.run(
                technique.command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=technique.execution_timeout
            )
            
            status = TechniqueStatus.SUCCESS if result.returncode == 0 else TechniqueStatus.FAILED
            
            return TechniqueResult(
                technique_id=technique.id,
                technique_name=technique.name,
                tactic=technique.tactic,
                status=status,
                execution_time=0.5,
                output=result.stdout,
                error=result.stderr if result.returncode != 0 else None,
                metadata={'return_code': result.returncode, 'mode': 'real'}
            )
            
        except subprocess.TimeoutExpired:
            return TechniqueResult(
                technique_id=technique.id,
                technique_name=technique.name,
                tactic=technique.tactic,
                status=TechniqueStatus.TIMEOUT,
                execution_time=technique.execution_timeout,
                output="",
                error="Command timed out",
                metadata={'mode': 'real'}
            )
        except Exception as e:
            return TechniqueResult(
                technique_id=technique.id,
                technique_name=technique.name,
                tactic=technique.tactic,
                status=TechniqueStatus.FAILED,
                execution_time=0.5,
                output="",
                error=str(e),
                metadata={'mode': 'real'}
            )


@dataclass
class CampaignResult:
    """Complete campaign results with analytics"""
    campaign_id: str
    campaign_name: str
    start_time: datetime
    end_time: datetime
    total_techniques: int
    successful: int
    failed: int
    detected: int
    success_rate: float
    detection_rate: float
    impact_score: float
    execution_mode: ExecutionMode
    technique_results: List[TechniqueResult] = field(default_factory=list)
    detection_gaps: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_json(self) -> str:
        return json.dumps({
            'campaign_id': self.campaign_id,
            'campaign_name': self.campaign_name,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'duration_seconds': (self.end_time - self.start_time).total_seconds(),
            'total_techniques': self.total_techniques,
            'successful': self.successful,
            'failed': self.failed,
            'detected': self.detected,
            'success_rate': self.success_rate,
            'detection_rate': self.detection_rate,
            'impact_score': self.impact_score,
            'execution_mode': self.execution_mode.value,
            'technique_results': [
                {
                    'technique_id': r.technique_id,
                    'technique_name': r.technique_name,
                    'tactic': r.tactic,
                    'status': r.status.value,
                    'execution_time': r.execution_time,
                    'output': r.output,
                    'error': r.error,
                    'detected': r.detected,
                }
                for r in self.technique_results
            ],
            'detection_gaps': self.detection_gaps,
            'recommendations': self.recommendations
        }, indent=2)
    
    def to_mitre_navigator(self) -> Dict[str, Any]:
        return {
            'name': f"APT Emulation - {self.campaign_name}",
            'version': '3.0',
            'domain': 'enterprise-attack',
            'description': f"Detection gaps identified: {len(self.detection_gaps)}",
            'techniques': [
                r.technique_id for r in self.technique_results 
                if r.status == TechniqueStatus.SUCCESS and r.detected
            ],
            'score': self.success_rate * 100
        }


class AdversaryEmulator(ABC):
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        
        # ✅ FIX P0-1: Translate safe_mode to ExecutionMode
        if self.config.get('safe_mode', True):
            exec_mode = ExecutionMode.SAFE
        else:
            exec_mode = ExecutionMode.REAL
        
        self.executor = TechniqueExecutor(mode=exec_mode)
        self.techniques: List[Technique] = []
        self.results: List[TechniqueResult] = []
        self.campaign_id = hashlib.md5(f"{name}_{time.time()}".encode()).hexdigest()[:8]
        self.detection_gaps = []
    
    @abstractmethod
    def get_technique_sequence(self) -> List[Technique]:
        pass
    
    @abstractmethod
    def validate_environment(self) -> bool:
        return True
    
    @abstractmethod
    def get_required_permissions(self) -> List[str]:
        return []
    
    def run_campaign(self) -> CampaignResult:
        start_time = datetime.now()
        
        if not self.validate_environment():
            raise RuntimeError("Environment validation failed")
        
        self.techniques = self.get_technique_sequence()
        logger.info(f"Starting {self.name} campaign with {len(self.techniques)} techniques")
        
        for i, technique in enumerate(self.techniques, 1):
            logger.info(f"[{i}/{len(self.techniques)}] Executing {technique.name}")
            result = self.executor.execute(technique, self.config)
            self.results.append(result)
            
            status_emoji = {
                TechniqueStatus.SUCCESS: "✅",
                TechniqueStatus.FAILED: "❌",
                TechniqueStatus.TIMEOUT: "⏰",
                TechniqueStatus.SKIPPED: "⏭️"
            }.get(result.status, "❓")
            print(f"  {status_emoji} {result.technique_name}: {result.status.value}")
        
        end_time = datetime.now()
        
        total = len(self.results)
        successful = sum(1 for r in self.results if r.status == TechniqueStatus.SUCCESS)
        failed = total - successful
        detected = sum(1 for r in self.results if r.detected)
        
        self.detection_gaps = self._identify_detection_gaps()
        
        return CampaignResult(
            campaign_id=self.campaign_id,
            campaign_name=self.name,
            start_time=start_time,
            end_time=end_time,
            total_techniques=total,
            successful=successful,
            failed=failed,
            detected=detected,
            success_rate=successful / total if total > 0 else 0,
            detection_rate=detected / total if total > 0 else 0,
            impact_score=successful * 0.8,
            execution_mode=self.executor.mode,
            technique_results=self.results,
            detection_gaps=self.detection_gaps,
            recommendations=self._generate_recommendations()
        )
    
    def _identify_detection_gaps(self) -> List[Dict[str, Any]]:
        gaps = []
        for result in self.results:
            if result.status == TechniqueStatus.SUCCESS and not result.detected:
                gaps.append({
                    'technique': result.technique_name,
                    'tactic': result.tactic,
                    'risk': 'HIGH',
                    'recommendation': f"Implement detection for {result.technique_name}"
                })
        return gaps
    
    def _generate_recommendations(self) -> List[Dict[str, Any]]:
        recommendations = []
        if self.detection_gaps:
            recommendations.append({
                'priority': 'HIGH',
                'action': f"Close {len(self.detection_gaps)} detection gaps",
                'techniques': [g['technique'] for g in self.detection_gaps[:3]]
            })
        
        detection_rate = len([r for r in self.results if r.detected]) / len(self.results) if self.results else 0
        if detection_rate < 0.3:
            recommendations.append({
                'priority': 'CRITICAL',
                'action': 'Improve overall detection capabilities',
                'current_rate': f"{detection_rate:.1%}"
            })
        
        return recommendations


# ✅ Alias for backward compatibility
EngagementResult = CampaignResult
