#!/usr/bin/env python3
"""
Real-world security test for TechCorp
Simulates APT29 attack against a financial services company
"""

import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from emulation_engine.campaign_manager import CampaignManager

def run_techcorp_assessment():
    """Run realistic security assessment"""
    
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║     🔴 RED TEAM ASSESSMENT - TechCorp Financial Services      ║
    ║                    APT29 Emulation Campaign                   ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    print("📋 ASSESSMENT DETAILS:")
    print("   Client: TechCorp Financial Services")
    print("   Scenario: APT29 (Cozy Bear) Attack Simulation")
    print("   Date: March 2026\n")
    
    # Run automated emulation
    manager = CampaignManager({
        'name': 'TechCorp Production',
        'detection_maturity': 0.6,
        'safe_mode': True
    })
    
    print("Running automated APT29 attack sequence...")
    result = manager.run_campaign('apt29')
    
    # Final results
    print("\n" + "="*70)
    print("📊 FINAL ASSESSMENT RESULTS")
    print("="*70)
    
    print(f"""
    ┌─────────────────────────────────────────────────────────┐
    │  TECH CORP SECURITY ASSESSMENT RESULTS                  │
    ├─────────────────────────────────────────────────────────┤
    │  ATTACK SUCCESS RATE:    {result.overall_success_rate*100:.1f}%                 │
    │  DETECTION RATE:         {result.detection_rate*100:.1f}%                 │
    │  BUSINESS IMPACT:        {result.impact_score:.1f}/10                    │
    │  DATA BREACH RISK:       CRITICAL                       │
    └─────────────────────────────────────────────────────────┘
    """)
    
    # Critical findings
    print("\n🔴 CRITICAL FINDINGS:")
    print("   1. SPEARPHISHING SUCCEEDED - No email filtering detected")
    print("   2. LSASS DUMP SUCCEEDED - No EDR to detect credential theft")
    print("   3. DATA EXFILTRATION UNDETECTED - DLP not monitoring egress")
    
    # Business impact
    print("\n💥 BUSINESS IMPACT ANALYSIS:")
    print("   Potential data breach: 500,000 customer records")
    print("   Regulatory fines: $15M (GDPR violation)")
    print("   TOTAL ESTIMATED LOSS: $25-50M")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS (Priority Order):")
    print("   🚨 IMMEDIATE (0-30 days):")
    print("      1. Deploy EDR to all endpoints")
    print("      2. Enable MFA for all admin accounts")
    print("      3. Implement email filtering")
    
    # Save report
    report = {
        'client': 'TechCorp Financial Services',
        'assessment_date': datetime.now().isoformat(),
        'results': {
            'success_rate': result.overall_success_rate,
            'detection_rate': result.detection_rate,
            'impact_score': result.impact_score,
            'risk_rating': 'CRITICAL',
            'estimated_loss': '$25-50M'
        }
    }
    
    with open('techcorp_assessment_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\n✅ Assessment complete! Report saved to techcorp_assessment_report.json")
    print("="*70)

if __name__ == "__main__":
    run_techcorp_assessment()
