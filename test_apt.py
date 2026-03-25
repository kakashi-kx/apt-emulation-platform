#!/usr/bin/env python3
"""
Test APT profiles
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import logging
logging.basicConfig(level=logging.INFO)

def test_apt29():
    """Test APT29 emulator"""
    print("\n" + "="*60)
    print("🎯 TESTING APT29 (Cozy Bear) EMULATOR")
    print("="*60)
    
    try:
        from apt_profiles.apt29 import APT29Emulator
        
        emulator = APT29Emulator(target_environment={
            'name': 'test',
            'detection_maturity': 0.5
        })
        
        techniques = emulator.get_technique_sequence()
        print(f"✅ APT29 has {len(techniques)} techniques")
        print("\n📋 APT29 TTP Sequence:")
        
        for i, tech in enumerate(techniques, 1):
            print(f"   {i}. {tech.name} ({tech.id}) - {tech.tactic}")
        
        return len(techniques) > 0
        
    except ImportError as e:
        print(f"❌ APT29 not available: {e}")
        return False

def test_lazarus():
    """Test Lazarus emulator"""
    print("\n" + "="*60)
    print("🎯 TESTING LAZARUS GROUP EMULATOR")
    print("="*60)
    
    try:
        from apt_profiles.lazarus import LazarusEmulator
        
        emulator = LazarusEmulator(target_environment={
            'name': 'test',
            'detection_maturity': 0.5
        })
        
        techniques = emulator.get_technique_sequence()
        print(f"✅ Lazarus has {len(techniques)} techniques")
        print("\n📋 Lazarus TTP Sequence:")
        
        for i, tech in enumerate(techniques, 1):
            print(f"   {i}. {tech.name} ({tech.id}) - {tech.tactic}")
        
        return len(techniques) > 0
        
    except ImportError as e:
        print(f"❌ Lazarus not available: {e}")
        return False

def test_ransomware():
    """Test ransomware emulator"""
    print("\n" + "="*60)
    print("🎯 TESTING RANSOMWARE OPERATOR EMULATOR")
    print("="*60)
    
    try:
        from apt_profiles.ransomware import RansomwareEmulator
        
        emulator = RansomwareEmulator(target_environment={
            'name': 'test',
            'detection_maturity': 0.5
        })
        
        techniques = emulator.get_technique_sequence()
        print(f"✅ Ransomware has {len(techniques)} techniques")
        print("\n📋 Ransomware Kill Chain:")
        
        for i, tech in enumerate(techniques, 1):
            print(f"   {i}. {tech.name} ({tech.id}) - {tech.tactic}")
        
        return len(techniques) > 0
        
    except ImportError as e:
        print(f"❌ Ransomware not available: {e}")
        return False

def run_full_campaign():
    """Run a full APT campaign"""
    print("\n" + "="*60)
    print("🚀 RUNNING FULL APT29 CAMPAIGN")
    print("="*60)
    
    try:
        from emulation_engine.campaign_manager import CampaignManager
        
        manager = CampaignManager({
            'name': 'test',
            'detection_maturity': 0.5,
            'safe_mode': True
        })
        
        print(f"\n📊 Available APT groups: {manager.list_available_apt_groups()}")
        print("\n🎯 Running APT29 campaign...")
        
        result = manager.run_campaign('apt29')
        
        print("\n" + "="*60)
        print("📊 CAMPAIGN RESULTS")
        print("="*60)
        print(f"✅ Successful: {len(result.successful_techniques)}")
        print(f"❌ Failed: {len(result.failed_techniques)}")
        print(f"📈 Success rate: {result.overall_success_rate*100:.1f}%")
        print(f"🛡️  Detection rate: {result.detection_rate*100:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Campaign failed: {e}")
        return False

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║     APT Emulation Platform - APT Profile Tests           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    tests = [
        ("APT29", test_apt29),
        ("Lazarus", test_lazarus),
        ("Ransomware", test_ransomware),
        ("Full Campaign", run_full_campaign)
    ]
    
    for test_name, test_func in tests:
        try:
            if test_func():
                print(f"\n✅ {test_name} test PASSED")
            else:
                print(f"\n❌ {test_name} test FAILED")
        except Exception as e:
            print(f"\n❌ {test_name} test ERROR: {e}")
