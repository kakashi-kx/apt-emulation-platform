"""
Sigma Rule Generator - Converts detection gaps to Sigma rules
Sigma is the standard format for SIEM detections (Splunk, Elastic, etc.)
"""

import yaml
from typing import List, Dict, Any
from datetime import datetime

class SigmaRuleGenerator:
    """Generate Sigma rules from detection gaps"""
    
    def __init__(self):
        self.rules = []
    
    def generate_rule(self, gap: Dict[str, Any]) -> str:
        """Generate a Sigma rule for a single detection gap"""
        
        technique = gap.get('technique', 'Unknown')
        tactic = gap.get('tactic', 'Unknown')
        
        rule = {
            "title": f"Detection Gap: {technique}",
            "id": f"apt-{technique.lower().replace(' ', '-')[:30]}",
            "status": "experimental",
            "description": f"Detect {technique} activity - identified by APT Emulation Platform",
            "references": [
                "https://attack.mitre.org/techniques/"
            ],
            "author": "APT Emulation Platform",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "logsource": {
                "category": "process_creation",
                "product": "windows"
            },
            "detection": {
                "selection": {
                    "CommandLine|contains": technique.split()[0] if technique else "unknown"
                },
                "condition": "selection"
            },
            "level": "high"
        }
        
        return yaml.dump(rule, default_flow_style=False, sort_keys=False)
    
    def generate_all_rules(self, gaps: List[Dict[str, Any]]) -> List[str]:
        """Generate Sigma rules for all gaps"""
        return [self.generate_rule(gap) for gap in gaps]
    
    def export_to_file(self, gaps: List[Dict[str, Any]], filename: str = "sigma_rules.yml"):
        """Export all rules to a single YAML file"""
        if not gaps:
            return "No gaps found"
        
        rules = self.generate_all_rules(gaps)
        
        with open(filename, 'w') as f:
            f.write("# Sigma Rules for APT Emulation Platform\n")
            f.write(f"# Generated: {datetime.now().isoformat()}\n")
            f.write(f"# Total Rules: {len(rules)}\n\n")
            f.write("\n---\n".join(rules))
        
        return f"✅ Exported {len(rules)} rules to {filename}"
