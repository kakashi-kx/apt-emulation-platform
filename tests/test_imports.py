"""Test imports for APT Emulation Platform"""

import sys
from pathlib import Path

def test_imports():
    """Test all modules import correctly"""
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    try:
        from core.base_emulator import CampaignResult
        from apt_profiles.apt29 import APT29Emulator
        from emulation_engine.campaign_manager import CampaignManager
        from web.app import app
        assert True
    except Exception as e:
        assert False, f"Import failed: {e}"

def test_campaign_result():
    """Test CampaignResult creation"""
    from core.base_emulator import CampaignResult
    from datetime import datetime
    
    result = CampaignResult(
        campaign_id="test",
        campaign_name="Test",
        start_time=datetime.now(),
        end_time=datetime.now(),
        total_techniques=0,
        successful=0,
        failed=0,
        detected=0,
        success_rate=0.0,
        detection_rate=0.0,
        impact_score=0.0,
        execution_mode=None
    )
    assert result.campaign_id == "test"
