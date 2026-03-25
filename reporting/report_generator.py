"""
Report Generator - Creates professional engagement reports
"""

from typing import List, Dict
from datetime import datetime
import json
import logging
from core.base_emulator import EngagementResult

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates comprehensive engagement reports"""
    
    def __init__(self):
        self.reports = []
    
    def generate_executive_summary(self, results: List[EngagementResult]) -> Dict:
        """Generate executive-level summary"""
        
        total_techniques = sum(len(r.techniques_executed) for r in results)
        total_successful = sum(len(r.successful_techniques) for r in results)
        total_detections = sum(len(r.detection_events) for r in results)
        
        summary = {
            'title': 'Adversary Emulation Executive Summary',
            'date': datetime.now().isoformat(),
            'total_campaigns': len(results),
            'total_techniques_executed': total_techniques,
            'overall_success_rate': total_successful / total_techniques if total_techniques > 0 else 0,
            'overall_detection_rate': total_detections / total_techniques if total_techniques > 0 else 0,
            'critical_findings': [],
            'recommendations': [],
            'risk_score': 0
        }
        
        # Collect critical findings
        for result in results:
            if result.overall_success_rate > 0.6:
                summary['critical_findings'].append({
                    'campaign': result.campaign_name,
                    'finding': f"High success rate ({result.overall_success_rate*100:.0f}%) indicates significant detection gaps",
                    'impact': result.impact_score
                })
        
        # Generate recommendations
        if summary['overall_success_rate'] > 0.5:
            summary['recommendations'].append("Immediate improvement needed in detection capabilities")
            summary['recommendations'].append("Implement enhanced logging for critical techniques")
            summary['recommendations'].append("Conduct SOC tabletop exercises for detected attacks")
        
        # Calculate risk score
        summary['risk_score'] = summary['overall_success_rate'] * 10
        
        return summary
    
    def generate_technical_report(self, result: EngagementResult) -> Dict:
        """Generate detailed technical report for a single engagement"""
        
        report = {
            'campaign': result.campaign_name,
            'timestamp': result.timestamp.isoformat(),
            'duration_seconds': result.duration_seconds,
            'summary': {
                'total_techniques': len(result.techniques_executed),
                'successful': len(result.successful_techniques),
                'failed': len(result.failed_techniques),
                'detections': len(result.detection_events),
                'success_rate': f"{result.overall_success_rate*100:.1f}%",
                'detection_rate': f"{result.detection_rate*100:.1f}%",
                'impact_score': f"{result.impact_score:.1f}/10"
            },
            'successful_techniques': [
                {
                    'name': t.name,
                    'id': t.id,
                    'tactic': t.tactic,
                    'command': t.command
                }
                for t in result.successful_techniques
            ],
            'failed_techniques': [
                {
                    'name': t.name,
                    'id': t.id,
                    'tactic': t.tactic,
                    'reason': 'Execution failed'
                }
                for t in result.failed_techniques
            ],
            'detection_events': result.detection_events,
            'recommendations': []
        }
        
        # Add recommendations based on failures and detections
        if len(result.failed_techniques) > 0:
            report['recommendations'].append("Review failed techniques for environmental compatibility")
        
        if len(result.detection_events) == 0 and len(result.successful_techniques) > 0:
            report['recommendations'].append("CRITICAL: Multiple successful techniques with zero detection")
            report['recommendations'].append("Implement immediate detection improvements")
        
        return report
    
    def generate_full_report(self, results: List[EngagementResult], filename: str = "engagement_report.json"):
        """Generate complete report with all campaigns"""
        
        full_report = {
            'executive_summary': self.generate_executive_summary(results),
            'campaign_reports': [self.generate_technical_report(r) for r in results],
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_campaigns': len(results),
                'tool_version': '1.0.0'
            }
        }
        
        # Save to file
        with open(filename, 'w') as f:
            json.dump(full_report, f, indent=2)
        
        logger.info(f"Full report saved to {filename}")
        
        return full_report
    
    def print_console_report(self, result: EngagementResult):
        """Print formatted report to console"""
        
        print("\n" + "="*70)
        print(f"🎯 APT EMULATION REPORT: {result.campaign_name}")
        print("="*70)
        print(f"📅 Date: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏱️  Duration: {result.duration_seconds:.2f} seconds")
        print()
        print("📊 METRICS")
        print("-"*70)
        print(f"  Total Techniques: {len(result.techniques_executed)}")
        print(f"  ✅ Successful: {len(result.successful_techniques)} ({result.overall_success_rate*100:.1f}%)")
        print(f"  ❌ Failed: {len(result.failed_techniques)}")
        print(f"  🛡️  Detected: {len(result.detection_events)} ({result.detection_rate*100:.1f}%)")
        print(f"  💥 Impact Score: {result.impact_score:.1f}/10.0")
        print()
        
        if result.successful_techniques:
            print("✅ SUCCESSFUL TECHNIQUES")
            print("-"*70)
            for tech in result.successful_techniques[:10]:
                print(f"  • {tech.name} ({tech.id}) - {tech.tactic}")
        
        if result.failed_techniques:
            print("\n❌ FAILED TECHNIQUES")
            print("-"*70)
            for tech in result.failed_techniques:
                print(f"  • {tech.name} ({tech.id})")
        
        if result.detection_events:
            print("\n🚨 DETECTION EVENTS")
            print("-"*70)
            for event in result.detection_events[:5]:
                print(f"  • {event.get('technique')}: {event.get('alert')}")
        
        print("\n" + "="*70)
