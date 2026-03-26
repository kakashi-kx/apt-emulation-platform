"""
Lazarus Group (Hidden Cobra) Emulation
North Korean state-sponsored group known for financial theft and destructive attacks

============================================
HOW TO CUSTOMIZE FOR YOUR ENVIRONMENT
============================================

1. Edit the "USER CUSTOMIZATION SECTION" below with your details
2. Replace the command in each technique with YOUR test command
3. Run with your config: python3 main.py --apt-group lazarus
"""

from typing import List
from core.base_emulator import AdversaryEmulator, Technique
import logging
import platform

logger = logging.getLogger(__name__)


class LazarusEmulator(AdversaryEmulator):
    """
    Emulates Lazarus Group (North Korea)
    Known for: WannaCry, Sony Pictures hack, cryptocurrency theft
    
    ⚠️  TO CUSTOMIZE FOR YOUR COMPANY:
    Scroll down to the "USER CUSTOMIZATION SECTION" and replace with YOUR details
    """
    
    def __init__(self, target_environment: dict = None):
        super().__init__("Lazarus Group", target_environment)
        self.os_type = platform.system()
        
        # =========================================================
        # 🔧 USER CUSTOMIZATION SECTION - REPLACE WITH YOUR DETAILS
        # =========================================================
        
        # REPLACE with your company's domain
        self.domain = target_environment.get('domain', 'yourcompany.local')
        
        # REPLACE with your test email address
        self.test_email = target_environment.get('test_email', 'securitytest@yourcompany.com')
        
        # REPLACE with your email server
        self.email_server = target_environment.get('email_server', 'smtp.yourcompany.com')
        
        # REPLACE with your EDR vendor (crowdstrike, sentinelone, defender, etc.)
        self.edr_vendor = target_environment.get('edr_vendor', 'crowdstrike')
        
        # REPLACE with path to your test scripts
        self.test_scripts_path = target_environment.get('test_scripts_path', '/opt/security/tests/')
        
        # REPLACE with your SIEM URL for detection checking
        self.siem_url = target_environment.get('siem_url', 'https://splunk.yourcompany.com')
        
        # =========================================================
        # END USER CUSTOMIZATION SECTION
        # =========================================================
        
    def initialize(self) -> bool:
        """Initialize Lazarus environment"""
        logger.info("Initializing Lazarus emulation environment")
        logger.info(f"Target OS: {self.os_type}")
        logger.info(f"Using email server: {self.email_server}")
        logger.info(f"EDR vendor: {self.edr_vendor}")
        logger.info("Deploying malware families...")
        return True
    
    def _get_email_test_command(self) -> str:
        """Get email test command for Lazarus spearphishing"""
        
        # =========================================================
        # 🔧 REPLACE WITH YOUR EMAIL TEST COMMAND
        # =========================================================
        
        return f"""
        # Lazarus-style spearphishing test
        # Option 1: Use your existing test script
        # python3 {self.test_scripts_path}/send_phishing_test.py --to {self.test_email} --template lazarus
        
        # Option 2: Simple email send test
        python3 -c "
import smtplib
from email.mime.text import MIMEText

msg = MIMEText('This is a Lazarus-style spearphishing test. Please verify detection.')
msg['Subject'] = 'Lazarus Test: Invoice Payment Required'
msg['From'] = 'finance@{self.domain}'
msg['To'] = '{self.test_email}'

try:
    server = smtplib.SMTP('{self.email_server}', 25)
    server.send_message(msg)
    server.quit()
    print('Lazarus test email sent')
except Exception as e:
    print(f'Email test failed: {{e}}')
"
        """
    
    def _get_edr_test_command(self) -> str:
        """Get EDR test command for Lazarus"""
        
        # =========================================================
        # 🔧 REPLACE WITH YOUR EDR TEST COMMAND
        # =========================================================
        
        edr_commands = {
            "crowdstrike": "C:\\Windows\\System32\\cs_test_tool.exe --simulate --group lazarus",
            "sentinelone": "C:\\Program Files\\SentinelOne\\s1_test.exe --eicar --variant lazarus",
            "defender": "powershell -c Write-Host 'X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'",
            "carbonblack": "C:\\Program Files\\CarbonBlack\\cb_test.exe --threat lazarus",
        }
        
        return edr_commands.get(self.edr_vendor, "echo 'Please configure your EDR test command in lazarus.py'")
    
    def _get_service_test_command(self) -> str:
        """Get service creation test command"""
        
        # =========================================================
        # 🔧 REPLACE WITH YOUR SERVICE TEST COMMAND
        # =========================================================
        
        if self.os_type == "Windows":
            return f"""
            # Test if service creation is monitored
            sc create LazarusTest binPath= "C:\\Windows\\System32\\calc.exe" start= auto
            timeout /t 2
            sc delete LazarusTest
            echo 'Service creation test completed'
            """
        else:
            return f"""
            # Linux service test
            echo 'Testing service monitoring on Linux'
            # systemctl status test-service
            """
    
    def _get_bruteforce_test_command(self) -> str:
        """Get brute force test command"""
        
        # =========================================================
        # 🔧 REPLACE WITH YOUR BRUTE FORCE TEST COMMAND
        # =========================================================
        
        return f"""
        # Brute force test (use with caution - only on test accounts!)
        # python3 {self.test_scripts_path}/bruteforce_test.py --target {self.domain} --user testuser
        
        echo 'Simulating brute force attempt on test account'
        # Replace with your actual test command
        """
    
    def _get_lateral_movement_test_command(self) -> str:
        """Get lateral movement test command"""
        
        # =========================================================
        # 🔧 REPLACE WITH YOUR LATERAL MOVEMENT TEST COMMAND
        # =========================================================
        
        return f"""
        # Test lateral movement detection
        # python3 {self.test_scripts_path}/lateral_move_test.py --target {self.domain}
        
        echo 'Testing lateral movement detection'
        # Replace with your actual test command
        """
    
    def _get_destruction_test_command(self) -> str:
        """Get data destruction test command"""
        
        # =========================================================
        # 🔧 REPLACE WITH YOUR DATA DESTRUCTION TEST COMMAND
        # =========================================================
        
        return f"""
        # Test data destruction detection (safe test only!)
        # python3 {self.test_scripts_path}/destruction_test.py --safe-mode
        
        echo 'Testing data destruction detection'
        # Replace with your actual test command
        """
    
    def _get_detection_check_command(self) -> str:
        """Check if security tools detected the test"""
        
        # =========================================================
        # 🔧 REPLACE WITH YOUR SIEM/EDR QUERY
        # =========================================================
        
        return f"""
        # Check if SIEM logged the Lazarus test
        curl -X GET '{self.siem_url}/api/search?q=Lazarus+test' \
             -H 'Authorization: Bearer YOUR_API_KEY' 2>/dev/null || echo 'SIEM check not configured'
        """
    
    def get_technique_sequence(self) -> List[Technique]:
        """Get Lazarus group's known TTP sequence with REPLACEABLE commands"""
        
        techniques = [
            # =========================================================
            # TECHNIQUE 1: Spearphishing Test
            # 🔧 REPLACE the 'command' with YOUR email test
            # =========================================================
            Technique(
                id="T1566",
                name="Spearphishing Test",
                tactic="Initial Access",
                platform=["Windows", "Linux"],
                permissions=["User"],
                description="Test if email gateway blocks Lazarus-style spearphishing",
                detection_risk=0.6,
                success_rate=0.7,
                command=self._get_email_test_command()  # ← REPLACE THIS SECTION
            ),
            
            # =========================================================
            # TECHNIQUE 2: User Execution Test
            # 🔧 REPLACE with YOUR user execution test
            # =========================================================
            Technique(
                id="T1204",
                name="User Execution Test",
                tactic="Execution",
                platform=["Windows", "Linux"],
                permissions=["User"],
                description="Test if user execution is monitored",
                detection_risk=0.5,
                success_rate=0.8,
                command="echo 'Testing user execution detection'"  # ← REPLACE THIS
            ),
            
            # =========================================================
            # TECHNIQUE 3: Service Creation Test
            # 🔧 REPLACE with YOUR service test
            # =========================================================
            Technique(
                id="T1543",
                name="Service Creation Test",
                tactic="Persistence",
                platform=["Windows"],
                permissions=["Administrator"],
                description="Test if service creation is monitored",
                detection_risk=0.7,
                success_rate=0.7,
                command=self._get_service_test_command()  # ← REPLACE THIS
            ),
            
            # =========================================================
            # TECHNIQUE 4: Deobfuscation Test
            # 🔧 REPLACE with YOUR deobfuscation test
            # =========================================================
            Technique(
                id="T1140",
                name="Deobfuscation Test",
                tactic="Defense Evasion",
                platform=["Windows"],
                permissions=["User"],
                description="Test if obfuscated code detection works",
                detection_risk=0.4,
                success_rate=0.85,
                command="echo 'Testing obfuscation detection'"  # ← REPLACE THIS
            ),
            
            # =========================================================
            # TECHNIQUE 5: Brute Force Test
            # 🔧 REPLACE with YOUR brute force test
            # =========================================================
            Technique(
                id="T1110",
                name="Brute Force Test",
                tactic="Credential Access",
                platform=["Windows", "Linux"],
                permissions=["User"],
                description="Test if brute force attempts are detected",
                detection_risk=0.8,
                success_rate=0.5,
                command=self._get_bruteforce_test_command()  # ← REPLACE THIS
            ),
            
            # =========================================================
            # TECHNIQUE 6: Lateral Movement Test
            # 🔧 REPLACE with YOUR lateral movement test
            # =========================================================
            Technique(
                id="T1570",
                name="Lateral Movement Test",
                tactic="Lateral Movement",
                platform=["Windows"],
                permissions=["Administrator"],
                description="Test if lateral movement is detected",
                detection_risk=0.6,
                success_rate=0.7,
                command=self._get_lateral_movement_test_command()  # ← REPLACE THIS
            ),
            
            # =========================================================
            # TECHNIQUE 7: Data Destruction Test
            # 🔧 REPLACE with YOUR destruction test
            # =========================================================
            Technique(
                id="T1485",
                name="Data Destruction Test",
                tactic="Impact",
                platform=["Windows"],
                permissions=["Administrator"],
                description="Test if data destruction is detected",
                detection_risk=0.9,
                success_rate=0.6,
                command=self._get_destruction_test_command()  # ← REPLACE THIS
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
                description="Check if security tools detected the tests",
                detection_risk=0.6,
                success_rate=0.75,
                command=self._get_detection_check_command()  # ← REPLACE THIS
            )
        ]
        
        return techniques
    
    def cleanup(self) -> bool:
        """Clean up Lazarus artifacts"""
        logger.info("Cleaning up Lazarus artifacts...")
        logger.info("Removing test services...")
        logger.info("Clearing test files...")
        return True
