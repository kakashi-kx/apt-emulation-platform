"""
Detection Calculator - Simulates detection capabilities
"""

from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class DetectionCalculator:
    """Calculates detection probabilities and identifies gaps"""
    
    def __init__(self, environment_maturity: float = 0.5):
        """
        Args:
            environment_maturity: 0-1 scale of detection maturity
                                0 = basic logging only
                                1 = advanced EDR with hunting
        """
        self.environment_maturity = environment_maturity
        self.detection_capabilities = {
            'network': environment_maturity * 0.8,
            'endpoint': environment_maturity,
            'cloud': environment_maturity * 0.7,
            'identity': environment_maturity * 0.6
        }
    
    def calculate_detection_probability(self, technique: Dict) -> float:
        """
        Calculate probability of detection based on technique and environment
        """
        base_prob = technique.get('detection_risk', 0.5)
        
        # Adjust based on capability matching
        tactic = technique.get('tactic', '')
        if tactic == 'Initial Access':
            capability = self.detection_capabilities['network']
        elif tactic in ['Execution', 'Persistence', 'Privilege Escalation']:
            capability = self.detection_capabilities['endpoint']
        elif tactic == 'Credential Access':
            capability = self.detection_capabilities['identity']
        elif tactic == 'Exfiltration':
            capability = self.detection_capabilities['network']
        else:
            capability = self.detection_capabilities['endpoint']
        
        # Final probability
        final_prob = base_prob * capability
        
        return min(final_prob, 0.95)  # Cap at 95%
    
    def find_detection_gaps(self, engagement_results: List[Dict]) -> List[Dict]:
        """
        Identify techniques that succeeded without detection
        """
        gaps = []
        
        for result in engagement_results:
            if result.get('success', False) and not result.get('detected', False):
                gaps.append({
                    'technique': result.get('technique'),
                    'id': result.get('id'),
                    'tactic': result.get('tactic', 'Unknown'),
                    'risk_level': 'CRITICAL',
                    'recommendation': self._get_recommendation(result.get('technique')),
                    'example_detection': self._generate_detection_rule(result)
                })
        
        return gaps
    
    def _get_recommendation(self, technique: str) -> str:
        """Get remediation recommendation for a technique"""
        recommendations = {
            'PowerShell': "Enable PowerShell logging (Script Block, Module, Transcription)",
            'LSASS': "Enable Credential Guard and EDR alerting for LSASS access",
            'Registry': "Monitor registry modifications with Sysmon",
            'Default': "Enable detailed logging and tune SIEM alerts"
        }
        
        for key, rec in recommendations.items():
            if key.lower() in technique.lower():
                return rec
        
        return recommendations['Default']
    
    def _generate_detection_rule(self, result: Dict) -> str:
        """Generate example detection rule"""
        technique = result.get('technique', 'unknown')
        
        return f"""
        # Example detection for {technique}
        index=* sourcetype=*
        | where EventCode=4688 AND CommandLine contains "{technique.lower()}"
        | table _time, Computer, User, CommandLine
        | sort - _time
        """
    
    def calculate_risk_score(self, gaps: List[Dict]) -> float:
        """Calculate overall risk score based on detection gaps"""
        if not gaps:
            return 0.0
        
        # Weight critical gaps higher
        critical_count = sum(1 for g in gaps if g.get('risk_level') == 'CRITICAL')
        
        base_score = (critical_count * 2 + len(gaps)) / 10
        
        return min(base_score, 10.0)
