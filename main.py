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
    parser.add_argument("--real", action="store_true",
        help="DANGEROUS: execute techniques for real instead of simulating.")
    parser.add_argument("--config", type=str, default=None)
    parser.add_argument("--target", type=str, default="production")
    parser.add_argument("--detection-maturity", type=float, default=0.5)
    
    args = parser.parse_args()
    
    # Safe mode is the default (not args.real)
    safe_mode = not args.real
    
    print(f"\n📋 ARGUMENTS:")
    print(f"   APT Group: {args.apt_group}")
    print(f"   Safe Mode: {safe_mode} (default)")
    print(f"   Real Mode: {args.real} (DANGEROUS)")
    print(f"   Config: {args.config}")
    print(f"   Target: {args.target}")
    print(f"   Detection Maturity: {args.detection_maturity}")
    
    print("\n🔧 Loading Campaign Manager...")
    
    from emulation_engine.campaign_manager import CampaignManager
    
    target_env = {
        'name': args.target,
        'detection_maturity': args.detection_maturity,
        'safe_mode': safe_mode  # Default: True unless --real is passed
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
        # ✅ FIX: Use correct CampaignResult attributes
        print(f"\n🎯 {result.campaign_name}")
        print(f"   Success Rate: {result.success_rate*100:.1f}%")
        print(f"   Detection Rate: {result.detection_rate*100:.1f}%")
        print(f"   Impact Score: {result.impact_score:.1f}/10")
        print(f"   Total Techniques: {result.total_techniques}")
        print(f"   ✅ Successful: {result.successful}")
        print(f"   ❌ Failed: {result.failed}")
        print(f"   🛡️ Detected: {result.detected}")
    
    print("\n" + "="*60)
    print("✅ COMPLETE! Report saved to campaign_results.json")
    print("="*60)

if __name__ == "__main__":
    main()
