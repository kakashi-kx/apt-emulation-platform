#!/usr/bin/env python3
"""
Simple test script for APT Emulation Platform
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.base_emulator import Technique, EngagementResult
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_technique():
    """Test basic technique functionality"""
    print("\n" + "="*60)
    print("TEST 1: Creating and executing a technique")
    print("="*60)
    
    tech = Technique(
        id="TEST001",
        name="Test Technique",
        tactic="Testing",
        platform=["All"],
        permissions=["User"],
        description="This is a test technique",
        detection_risk=0.5,
        success_rate=0.9,
        command="echo 'Hello from test technique!'"
    )
    
    print(f"✅ Created technique: {tech.name} ({tech.id})")
    success = tech.execute()
    
    if success:
        print(f"✅ Technique executed successfully!")
    else:
        print(f"❌ Technique execution failed")
    
    return success

def test_multiple_techniques():
    """Test multiple techniques"""
    print("\n" + "="*60)
    print("TEST 2: Testing multiple techniques")
    print("="*60)
    
    techniques = [
        Technique(
            id="TEST001",
            name="Test Technique 1",
            tactic="Testing",
            platform=["All"],
            permissions=["User"],
            description="First test",
            command="echo 'Test 1'"
        ),
        Technique(
            id="TEST002",
            name="Test Technique 2",
            tactic="Testing",
            platform=["All"],
            permissions=["User"],
            description="Second test",
            command="echo 'Test 2'"
        ),
        Technique(
            id="TEST003",
            name="Test Technique 3",
            tactic="Testing",
            platform=["All"],
            permissions=["User"],
            description="Third test",
            command="echo 'Test 3'"
        )
    ]
    
    results = []
    for tech in techniques:
        print(f"\nExecuting: {tech.name}")
        success = tech.execute()
        results.append(success)
        print(f"  Result: {'✅ Success' if success else '❌ Failed'}")
    
    success_rate = sum(results) / len(results) * 100
    print(f"\n📊 Success Rate: {success_rate:.1f}%")
    
    return all(results)

def test_engagement_result():
    """Test engagement result creation"""
    print("\n" + "="*60)
    print("TEST 3: Creating engagement result")
    print("="*60)
    
    tech1 = Technique(
        id="T1059",
        name="PowerShell Execution",
        tactic="Execution",
        platform=["Windows"],
        permissions=["User"],
        description="Execute PowerShell",
        command="echo 'PowerShell'"
    )
    
    tech2 = Technique(
        id="T1003",
        name="Credential Dumping",
        tactic="Credential Access",
        platform=["Windows"],
        permissions=["Admin"],
        description="Dump credentials",
        command="echo 'Credential Dump'"
    )
    
    result = EngagementResult(
        timestamp=datetime.now(),
        campaign_name="Test Campaign",
        techniques_executed=[tech1, tech2],
        successful_techniques=[tech1],
        failed_techniques=[tech2],
        detection_events=[{"technique": "T1059", "alert": "PowerShell detected"}],
        duration_seconds=5.5,
        overall_success_rate=0.5,
        detection_rate=0.5,
        impact_score=5.0
    )
    
    print("✅ Engagement result created successfully")
    print("\nResult JSON:")
    print(result.to_json())
    result.print_summary()
    
    return True

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║     APT Emulation Platform - Simple Test Suite            ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    tests = [
        ("Technique Creation", test_technique),
        ("Multiple Techniques", test_multiple_techniques),
        ("Engagement Result", test_engagement_result)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n❌ Test '{test_name}' failed with error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {passed/(passed+failed)*100:.1f}%")
    print("="*60)
    
    if failed == 0:
        print("\n🎉 All tests passed! Your platform is working correctly!")
    else:
        print(f"\n⚠️  {failed} test(s) failed.")
