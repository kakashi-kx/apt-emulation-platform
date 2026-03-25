#!/usr/bin/env python3
"""
APT Emulation Platform - Main Entry Point
"""

import argparse
import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from emulation_engine.campaign_manager import CampaignManager
from reporting.report_generator import ReportGenerator
from utils.logger import setup_logger

logger = setup_logger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="APT Emulation Platform - Full-Spectrum Adversary Emulation"
    )
    
    parser.add_argument(
        "--apt-group",
        choices=["apt29", "lazarus", "ransomware", "all"],
        default="all",
        help="APT group to emulate"
    )
    
    parser.add_argument(
        "--target",
        type=str,
        default="production",
        help="Target environment (production, staging, dev)"
    )
    
    parser.add_argument(
        "--safe-mode",
        action="store_true",
        help="Run in safe mode (no actual commands executed)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="report.json",
        help="Output report filename"
    )
    
    parser.add_argument(
        "--detection-maturity",
        type=float,
        default=0.5,
        choices=[0.0, 0.25, 0.5, 0.75, 1.0],
        help="Detection maturity level (0-1)"
    )
    
    args = parser.parse_args()
    
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║     APT Emulation Platform - Full-Spectrum Adversary Emulation ║
    ║                         Version 1.0.0                          ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Configure target environment
    target_environment = {
        'name': args.target,
        'detection_maturity': args.detection_maturity,
        'safe_mode': args.safe_mode
    }
    
    logger.info(f"Target environment: {args.target}")
    logger.info(f"Detection maturity: {args.detection_maturity}")
    logger.info(f"Safe mode: {args.safe_mode}")
    
    # Initialize campaign manager
    manager = CampaignManager(target_environment)
    
    # List available APT groups
    available = manager.list_available_apt_groups()
    logger.info(f"Available APT groups: {', '.join(available)}")
    
    # Run campaigns
    results = []
    
    if args.apt_group == "all":
        logger.info("Running all APT campaigns...")
        results = manager.run_all_campaigns()
    else:
        logger.info(f"Running {args.apt_group} campaign...")
        result = manager.run_campaign(args.apt_group)
        results = [result]
    
    # Save results
    manager.save_results("campaign_results.json")
    
    # Generate reports
    report_gen = ReportGenerator()
    
    # Print console report for each campaign
    for result in results:
        report_gen.print_console_report(result)
    
    # Generate full report
    full_report = report_gen.generate_full_report(results, args.output)
    
    # Print executive summary
    print("\n" + "="*70)
    print("📋 EXECUTIVE SUMMARY")
    print("="*70)
    
    summary = full_report['executive_summary']
    print(f"  Total Campaigns: {summary['total_campaigns']}")
    print(f"  Overall Success Rate: {summary['overall_success_rate']*100:.1f}%")
    print(f"  Overall Detection Rate: {summary['overall_detection_rate']*100:.1f}%")
    print(f"  Risk Score: {summary['risk_score']:.1f}/10.0")
    
    if summary.get('critical_findings'):
        print("\n  🔴 CRITICAL FINDINGS:")
        for finding in summary['critical_findings']:
            print(f"    • {finding['finding']}")
    
    if summary.get('recommendations'):
        print("\n  💡 RECOMMENDATIONS:")
        for rec in summary['recommendations']:
            print(f"    • {rec}")
    
    print("\n" + "="*70)
    print(f"✅ Complete! Report saved to: {args.output}")
    print("="*70)


if __name__ == "__main__":
    main()
