"""
Ransomware Operator Emulation
Generic ransomware attack simulation

============================================
HOW TO CUSTOMIZE FOR YOUR ENVIRONMENT
============================================

1. Edit the "USER CUSTOMIZATION SECTION" below with your details
2. Replace the command in each technique with YOUR test command
3. Run with your config: python3 main.py --apt-group ransomware
"""

from typing import List
from core.base_emulator import AdversaryEmulator, Technique
import logging
import platform

logger = logging.getLogger(__name__)


class RansomwareEmulator(AdversaryEmulator):
    """
    Emulates modern ransomware operators
    Follows typical ransomware kill chain
    
    ⚠️  TO CUSTOMIZE FOR YOUR COMPANY:
    Scroll down to the "USER CUSTOMIZATION SECTION" and replace with YOUR details
    """
    
    def __init__(self, target_environment: dict = None):
        super().__init__("Ransomware Operator", target_environment)
        self.os_type = platform.system()
        
        # =========================================================
        # 🔧 USER CUSTOMIZATION SECTION - REPLACE WITH YOUR DETAILS
        # =========================================================
        
        # REPLACE with your company's domain
        self.domain = target_environment.get('domain', 'yourcompany.local')
        
        # REPLACE with your test file path (safe location for ransomware tests)
        self.test_file_path = target_environment.get('test_file_path', '/tmp/ransomware_test_file.txt')
        
        # REPLACE with your EDR vendor (crowdstrike, sentinelone, defender, etc.)
        self.edr_vendor = target_environment.get('edr_vendor', 'crowdstrike')
        
        # REPLACE with path to your test scripts
        self.test_scripts_path = target_environment.get('test_scripts_path', '/opt/security/tests/')
        
        # REPLACE with your SIEM URL for detection checking
        self.siem_url = target_environment.get('siem_url', 'https://splunk.yourcompany.com')
        
        # REPLACE with your backup server (for ransomware simulation)
        self.backup_server = target_environment.get('backup_server', 'backup.yourcompany.com')
        
        # =========================================================
        # END USER CUSTOMIZATION SECTION
        # =========================================================
        
    def initialize(self) -> bool:
        """Initialize ransomware simulation"""
        logger.info("Initializing ransomware emulation")
        logger.info(f"Target OS: {self.os_type}")
        logger.info(f"EDR vendor: {self.edr_vendor}")
        logger.info(f"Test file path: {self.test_file_path}")
        logger.info("Preparing ransomware payload...")
        return True
    
    def _get_exploit_test_command(self) -> str:
        """Get exploit test command for ransomware initial access"""
        
        # =========================================================
        # 🔧 REPLACE WITH YOUR EXPLOIT TEST COMMAND
        # =========================================================
        
        if self.os_type == "Windows":
            return f"""
            # Test if vulnerable services are detected
            # python3 {self.test_scripts_path}/exploit_tester.py --target {self.domain} --service rdp
            
            # Simple test: Check for common vulnerabilities
            echo 'Testing exploit detection'
            # Replace with your actual exploit test
            """
        else:
            return f"""
            # Linux exploit test
            # python3 {self.test_scripts_path}/linux_exploit_test.py --target {self.domain}
            
            echo 'Testing Linux exploit detection'
            """
    
    def _get_ransomware_execution_command(self) -> str:
        """Get ransomware execution test command"""
        
        # =========================================================
        # 🔧 REPLACE WITH YOUR RANSOMWARE EXECUTION TEST
        # =========================================================
        
        # Create a safe test file for ransomware simulation
        return f"""
        # Create safe test file for ransomware simulation
        echo "This is a safe test file for ransomware detection" > {self.test_file_path}
        
        # Simulate ransomware behavior (safe test only!)
        # Use EICAR test file or your own safe test
        if [ -f {self.test_file_path} ]; then
            # Simulate file encryption by renaming (safe)
            mv {self.test_file_path} {self.test_file_path}.encrypted
            echo 'Ransomware simulation: test file encrypted'
            
            # Wait for EDR to detect
            sleep 2
            
            # Restore test file
            mv {self.test_file_path}.encrypted {self.test_file_path}
            echo 'Ransomware simulation: test file restored'
        else
            echo 'Warning: Test file not found'
        fi
        
        # Alternative: Use EICAR test file
        # echo 'X5O!P%@AP[4\\PZX54(P^)7CC)7}}EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*' > eicar.com
        """
    
    def _get_process_injection_command(self) -> str:
        """Get process injection test command"""
        
        # =========================================================
        # 🔧 REPLACE WITH YOUR PROCESS INJECTION TEST
        # =========================================================
        
        if self.os_type == "Windows":
            return f"""
            # Test process injection detection
            # python3 {self.test_scripts_path}/process_injection_test.py --target notepad.exe
            
            echo 'Testing process injection detection'
            # Replace with your actual test
            """
        else:
            return f"""
            # Linux process injection test
            # python3 {self.test_scripts_path}/linux_process_injection.py
            
            echo 'Testing Linux process injection'
            """
    
    def _get_defense_evasion_command(self) -> str:
        """Get defense evasion test command"""
        
        # =========================================================
        # 🔧 REPLACE WITH YOUR DEFENSE EVASION TEST
        # =========================================================
        
        # Test if security tools are running
        edr_checks = {
            "crowdstrike": "tasklist | findstr CSAgent",
            "sentinelone": "tasklist | findstr Sentinel",
            "defender": "powershell -c Get-MpComputerStatus",
        }
        
        return f"""
        # Test if security tools are active
        # Check if EDR is running
        {edr_checks.get(self.edr_vendor, "echo 'Checking EDR status'")}
        
        # Test if logs are being captured
        echo 'Testing log integrity'
        logger "Ransomware test: defense evasion simulation"
        
        echo 'Defense evasion test completed'
        """
    
    def _get_file_discovery_command(self) -> str:
        """Get file discovery test command"""
        
        # =========================================================
        # 🔧 REPLACE WITH YOUR FILE DISCOVERY TEST
        # =========================================================
        
        return f"""
        # Test if file access is monitored
        # Find test files (safe test only)
        find /tmp -name "*.txt" -type f 2>/dev/null | head -5
        
        # Check if sensitive file access is logged
        if [ -f /etc/passwd ]; then
            echo 'Testing file access monitoring'
        fi
        
        echo 'File discovery test completed'
        """
    
    def _get_lateral_movement_command(self) -> str:
        """Get lateral movement test command"""
        
        # =========================================================
        # 🔧 REPLACE WITH YOUR LATERAL MOVEMENT TEST
        # =========================================================
        
        return f"""
        # Test lateral movement detection
        # python3 {self.test_scripts_path}/lateral_movement_test.py --target {self.domain}
        
        # Simple test: ping internal hosts
        ping -c 1 {self.backup_server} 2>/dev/null
        
        echo 'Lateral movement test completed'
        """
    
    def _get_encryption_test_command(self) -> str:
        """Get ransomware encryption test command"""
        
        # =========================================================
        # 🔧 REPLACE WITH YOUR ENCRYPTION TEST
        # =========================================================
        
        return f"""
        # Test ransomware encryption detection
        # Create safe test files
        echo "Test file 1" > {self.test_file_path}.1
        echo "Test file 2" > {self.test_file_path}.2
        
        # Simulate encryption by changing extensions (safe)
        for f in {self.test_file_path}.*; do
            mv "$f" "$f.encrypted"
        done
        
        echo 'Encryption simulation completed'
        
        # Restore files
        for f in {self.test_file_path}.*.encrypted; do
            mv "$f" "${{f%.encrypted}}"
        done
        
        echo 'Test files restored'
        """
    
    def _get_detection_check_command(self) -> str:
        """Check if security tools detected the test"""
        
        # =========================================================
        # 🔧 REPLACE WITH YOUR SIEM/EDR QUERY
        # =========================================================
        
        return f"""
        # Check if SIEM logged the ransomware test
        # Option 1: Query your SIEM API
        curl -X GET '{self.siem_url}/api/search?q=ransomware+test' \\
             -H 'Authorization: Bearer YOUR_API_KEY' 2>/dev/null || echo 'SIEM check not configured'
        
        # Option 2: Check local logs
        grep -i "ransomware" /var/log/security.log 2>/dev/null || echo 'No ransomware logs found'
        """
    
    def get_technique_sequence(self) -> List[Technique]:
        """Get typical ransomware attack sequence with REPLACEABLE commands"""
        
        techniques = [
            # =========================================================
            # TECHNIQUE 1: Exploit Test
            # 🔧 REPLACE the 'command' with YOUR exploit test
            # =========================================================
            Technique(
                id="T1190",
                name="Exploit Test",
                tactic="Initial Access",
                platform=["Windows", "Linux"],
                permissions=["User"],
                description="Test if exploits are detected",
                detection_risk=0.7,
                success_rate=0.6,
                command=self._get_exploit_test_command()  # ← REPLACE THIS SECTION
            ),
            
            # =========================================================
            # TECHNIQUE 2: Ransomware Execution Test
            # 🔧 REPLACE with YOUR ransomware execution test
            # =========================================================
            Technique(
                id="T1059",
                name="Ransomware Execution Test",
                tactic="Execution",
                platform=["Windows", "Linux"],
                permissions=["User"],
                description="Test if ransomware execution is detected",
                detection_risk=0.8,
                success_rate=0.75,
                command=self._get_ransomware_execution_command()  # ← REPLACE THIS
            ),
            
            # =========================================================
            # TECHNIQUE 3: Process Injection Test
            # 🔧 REPLACE with YOUR process injection test
            # =========================================================
            Technique(
                id="T1055",
                name="Process Injection Test",
                tactic="Privilege Escalation",
                platform=["Windows"],
                permissions=["User"],
                description="Test if process injection is detected",
                detection_risk=0.85,
                success_rate=0.7,
                command=self._get_process_injection_command()  # ← REPLACE THIS
            ),
            
            # =========================================================
            # TECHNIQUE 4: Defense Evasion Test
            # 🔧 REPLACE with YOUR defense evasion test
            # =========================================================
            Technique(
                id="T1562",
                name="Defense Evasion Test",
                tactic="Defense Evasion",
                platform=["Windows", "Linux"],
                permissions=["Administrator"],
                description="Test if defense evasion is detected",
                detection_risk=0.9,
                success_rate=0.65,
                command=self._get_defense_evasion_command()  # ← REPLACE THIS
            ),
            
            # =========================================================
            # TECHNIQUE 5: File Discovery Test
            # 🔧 REPLACE with YOUR file discovery test
            # =========================================================
            Technique(
                id="T1083",
                name="File Discovery Test",
                tactic="Discovery",
                platform=["Windows", "Linux"],
                permissions=["User"],
                description="Test if file discovery is monitored",
                detection_risk=0.4,
                success_rate=0.95,
                command=self._get_file_discovery_command()  # ← REPLACE THIS
            ),
            
            # =========================================================
            # TECHNIQUE 6: Lateral Movement Test
            # 🔧 REPLACE with YOUR lateral movement test
            # =========================================================
            Technique(
                id="T1021",
                name="Lateral Movement Test",
                tactic="Lateral Movement",
                platform=["Windows", "Linux"],
                permissions=["Administrator"],
                description="Test if lateral movement is detected",
                detection_risk=0.7,
                success_rate=0.6,
                command=self._get_lateral_movement_command()  # ← REPLACE THIS
            ),
            
            # =========================================================
            # TECHNIQUE 7: Ransomware Encryption Test
            # 🔧 REPLACE with YOUR encryption test
            # =========================================================
            Technique(
                id="T1486",
                name="Ransomware Encryption Test",
                tactic="Impact",
                platform=["Windows", "Linux"],
                permissions=["Administrator"],
                description="Test if ransomware encryption is detected",
                detection_risk=0.95,
                success_rate=0.8,
                command=self._get_encryption_test_command()  # ← REPLACE THIS
            ),
            
            # =========================================================
            # TECHNIQUE 8: Detection Verification
            # 🔧 REPLACE with YOUR detection check
            # =========================================================
            Technique(
                id="T1041",
                name="Detection Verification",
                tactic="Exfiltration",
                platform=["Windows", "Linux"],
                permissions=["User"],
                description="Check if security tools detected the ransomware test",
                detection_risk=0.6,
                success_rate=0.75,
                command=self._get_detection_check_command()  # ← REPLACE THIS
            )
        ]
        
        return techniques
    
    def cleanup(self) -> bool:
        """Clean up ransomware artifacts"""
        logger.info("Cleaning up ransomware artifacts...")
        logger.info("Removing test files...")
        
        # Clean up test files
        import os
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)
            logger.info(f"Removed: {self.test_file_path}")
        
        logger.info("Clearing test logs...")
        return True
