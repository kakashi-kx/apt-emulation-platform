#!/usr/bin/env python3
"""
APT Emulation Platform - Full-Spectrum Adversary Emulation
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("="*60)
print("APT EMULATION PLATFORM - STARTING")
print("="*60)

def main():
    parser = argparse.ArgumentParser(description="APT Emulation Platform")
    parser.add_argument("--apt-group", choices=["apt29", "lazarus", "ransomware", "all"], default="all")
    parser.add_argument("--safe-mode", action="store_true")
    parser.add_argument("--config", type=str, default=None)
    parser.add_argument("--target", type=str, default="production")
    parser.add_argument("--detection-maturity", type=float, default=0.5)
    
    args = parser.parse_args()
    
    print(f"\n📋 ARGUMENTS:")
    print(f"   APT Group: {args.apt_group}")
    print(f"   Safe Mode: {args.safe_mode}")
    print(f"   Config: {args.config}")
    print(f"   Target: {args.target}")
    print(f"   Detection Maturity: {args.detection_maturity}")
    
    print("\n🔧 Loading Campaign Manager...")
    
    from emulation_engine.campaign_manager import CampaignManager
    
    target_env = {
        'name': args.target,
        'detection_maturity': args.detection_maturity,
        'safe_mode': args.safe_mode
    }
    
    manager = CampaignManager(target_env)
    
    print(f"\n📋 Available APT Groups: {manager.list_available_apt_groups()}")
    
    print(f"\n🚀 Running {args.apt_group} campaign...")
    
    if args.apt_group == "all":
        results = manager.run_all_campaigns()
    else:
        result = manager.run_campaign(args.apt_group)
        results = [result]
    
    # SAVE RESULTS TO JSON FILE
    manager.save_results("campaign_results.json")
    
    print("\n" + "="*60)
    print("📊 RESULTS SUMMARY")
    print("="*60)
    
    for result in results:
        print(f"\n🎯 {result.campaign_name}")
        print(f"   Success Rate: {result.overall_success_rate*100:.1f}%")
        print(f"   Detection Rate: {result.detection_rate*100:.1f}%")
        print(f"   Impact Score: {result.impact_score:.1f}/10")
    
    print("\n" + "="*60)
    print("✅ COMPLETE! Report saved to campaign_results.json")
    print("="*60)

if __name__ == "__main__":
    main()
