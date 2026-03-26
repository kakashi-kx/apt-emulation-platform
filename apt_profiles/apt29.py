"""
APT29 (Cozy Bear, Nobelium) Emulation
Known for: SolarWinds attack, cloud compromise, diplomatic targeting

============================================
HOW TO CUSTOMIZE FOR YOUR ENVIRONMENT
============================================

1. Edit the "USER CUSTOMIZATION SECTION" below with your details
2. Replace the command in each technique with YOUR test command
3. Run with your config: python3 main.py --apt-group apt29
"""

from typing import List
import sys
import platform
from core.base_emulator import AdversaryEmulator, Technique
import logging

logger = logging.getLogger(__name__)


class APT29Emulator(AdversaryEmulator):
    """
    Emulates APT29 (Russian Foreign Intelligence Service)
    TTPs based on public threat intelligence
    
    ⚠️  TO CUSTOMIZE FOR YOUR COMPANY:
    Scroll down to the "USER CUSTOMIZATION SECTION" and replace with YOUR details
    """
    
    def __init__(self, target_environment: dict = None):
        super().__init__("APT29 (Cozy Bear)", target_environment)
        self.os_type = platform.system()
        
        # =========================================================
        # 🔧 USER CUSTOMIZATION SECTION - REPLACE WITH YOUR DETAILS
        # =========================================================
        
        # REPLACE with your company's email server
        self.email_server = target_environment.get('email_server', 'smtp.yourcompany.com')
        
        # REPLACE with your test email address
        self.test_email = target_environment.get('test_email', 'securitytest@yourcompany.com')
        
        # REPLACE with your EDR vendor (crowdstrike, sentinelone, defender, carbonblack, etc.)
        self.edr_vendor = target_environment.get('edr_vendor', 'crowdstrike')
        
        # REPLACE with your domain
        self.domain = target_environment.get('domain', 'yourcompany.local')
        
        # REPLACE with path to your test scripts
        self.test_scripts_path = target_environment.get('test_scripts_path', '/opt/security/tests/')
        
        # REPLACE with your SIEM URL for detection checking
        self.siem_url = target_environment.get('siem_url', 'https://splunk.yourcompany.com')
        
        # =========================================================
        # END USER CUSTOMIZATION SECTION
        # =========================================================
        
    def initialize(self) -> bool:
        """Initialize APT29 environment"""
        logger.info("Initializing APT29 emulation environment")
        logger.info(f"Target OS: {self.os_type}")
        logger.info(f"Using email server: {self.email_server}")
        logger.info(f"EDR vendor: {self.edr_vendor}")
        
        if self.os_type == "Windows":
            logger.info("Setting up Windows persistence mechanisms...")
        else:
            logger.info("Setting up Linux/Unix persistence mechanisms...")
        
        logger.info("Establishing C2 infrastructure...")
        return True
    
    def _get_edr_test_command(self) -> str:
        """Get EDR test command based on your vendor"""
        
        # =========================================================
        # 🔧 REPLACE WITH YOUR EDR TEST COMMANDS
        # =========================================================
        
        edr_commands = {
            "crowdstrike": "C:\\Windows\\System32\\cs_test_tool.exe --simulate",
            "sentinelone": "C:\\Program Files\\SentinelOne\\s1_test.exe --eicar",
            "defender": "powershell -c Write-Host 'X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'",
            "carbonblack": "C:\\Program Files\\CarbonBlack\\cb_test.exe",
            "custom": "YOUR_CUSTOM_EDR_TEST_COMMAND_HERE",
        }
        
        return edr_commands.get(self.edr_vendor, "echo 'Please configure your EDR test command in apt29.py'")
    
    def _get_email_test_command(self) -> str:
        """Get email test command"""
        
        # =========================================================
        # 🔧 REPLACE WITH YOUR EMAIL TEST COMMAND
        # =========================================================
        
        # Option 1: Use your existing test script
        # return f"python3 {self.test_scripts_path}/send_phishing_test.py --to {self.test_email}"
        
        # Option 2: Use simple Python email send
        return f"""
        python3 -c "
import smtplib
from email.mime.text import MIMEText

msg = MIMEText('This is a test phishing email. Please verify if it was blocked.')
msg['Subject'] = 'Test: APT29 Phishing Simulation'
msg['From'] = 'test@{self.domain}'
msg['To'] = '{self.test_email}'

try:
    server = smtplib.SMTP('{self.email_server}', 25)
    server.send_message(msg)
    server.quit()
    print('Test email sent successfully')
except Exception as e:
    print(f'Email test failed: {{e}}')
"
        """
    
    def _get_credential_test_command(self) -> str:
        """Get credential access test command"""
        
        # =========================================================
        # 🔧 REPLACE WITH YOUR CREDENTIAL TEST COMMAND
        # =========================================================
        
        if self.os_type == "Windows":
            return f"""
            # Windows credential test
            # Option 1: Use mimikatz (safe test only!)
            # echo 'sekurlsa::logonpasswords' | mimikatz.exe
            
            # Option 2: Use your own test script
            python3 {self.test_scripts_path}/test_credentials.py
            """
        else:
            return f"""
            # Linux credential test
            # Test if /etc/shadow is accessible
            if [ -r /etc/shadow ]; then
                echo 'WARNING: /etc/shadow is readable by current user'
            else
                echo 'OK: /etc/shadow is protected'
            fi
            """
    
    def _get_network_test_command(self) -> str:
        """Get network discovery test command"""
        
        # =========================================================
        # 🔧 REPLACE WITH YOUR NETWORK TEST COMMAND
        # =========================================================
        
        return f"""
        # Test network monitoring
        # Option 1: Simple ping test
        ping -c 1 {self.domain}
        
        # Option 2: Use nmap (safe scan)
        # nmap -sS -p 80,443 {self.domain}
        
        # Option 3: Use your own test script
        # python3 {self.test_scripts_path}/network_scan.py
        """
    
    def _get_detection_check_command(self) -> str:
        """Check if security tools detected the test"""
        
        # =========================================================
        # 🔧 REPLACE WITH YOUR SIEM/EDR QUERY
        # =========================================================
        
        return f"""
        # Check if SIEM logged the test
        # Option 1: Query your SIEM API
        curl -X GET '{self.siem_url}/api/search?q=test_event' \
             -H 'Authorization: Bearer YOUR_API_KEY'
        
        # Option 2: Check local logs
        grep "test" /var/log/security.log
        """
    
    def get_technique_sequence(self) -> List[Technique]:
        """Get APT29's known TTP sequence with REPLACEABLE commands"""
        
        techniques = [
            # =========================================================
            # TECHNIQUE 1: Spearphishing / Email Security Test
            # 🔧 REPLACE the 'command' with YOUR email test
            # =========================================================
            Technique(
                id="T1566.001",
                name="Spearphishing / Email Security Test",
                tactic="Initial Access",
                platform=["Windows", "Linux"],
                permissions=["User"],
                description="Test if email gateway blocks phishing attempts",
                detection_risk=0.6,
                success_rate=0.7,
                command=self._get_email_test_command()  # ← REPLACE THIS SECTION
            ),
            
            # =========================================================
            # TECHNIQUE 2: EDR / Endpoint Detection Test
            # 🔧 REPLACE the 'command' with YOUR EDR test
            # =========================================================
            Technique(
                id="T1059.001",
                name="EDR / Endpoint Detection Test",
                tactic="Execution",
                platform=["Windows", "Linux"],
                permissions=["User"],
                description="Test if EDR detects suspicious activity",
                detection_risk=0.7,
                success_rate=0.8,
                command=self._get_edr_test_command()  # ← REPLACE THIS SECTION
            ),
            
            # =========================================================
            # TECHNIQUE 3: Persistence Test
            # 🔧 REPLACE with YOUR persistence test
            # =========================================================
            Technique(
                id="T1547.001",
                name="Persistence Mechanism Test",
                tactic="Persistence",
                platform=["Windows", "Linux"],
                permissions=["Administrator"],
                description="Test if persistence mechanisms are monitored",
                detection_risk=0.5,
                success_rate=0.75,
                command="echo 'Testing persistence monitoring'",  # ← REPLACE THIS
            ),
            
            # =========================================================
            # TECHNIQUE 4: Privilege Escalation Test
            # 🔧 REPLACE with YOUR privilege escalation test
            # =========================================================
            Technique(
                id="T1068",
                name="Privilege Escalation Test",
                tactic="Privilege Escalation",
                platform=["Windows", "Linux"],
                permissions=["User"],
                description="Test if privilege escalation attempts are detected",
                detection_risk=0.4,
                success_rate=0.6,
                command="echo 'Testing privilege escalation detection'",  # ← REPLACE THIS
            ),
            
            # =========================================================
            # TECHNIQUE 5: Defense Evasion Test
            # 🔧 REPLACE with YOUR defense evasion test
            # =========================================================
            Technique(
                id="T1070.004",
                name="Defense Evasion Test",
                tactic="Defense Evasion",
                platform=["Windows", "Linux"],
                permissions=["User"],
                description="Test if log clearing is detected",
                detection_risk=0.3,
                success_rate=0.9,
                command="echo 'Testing log monitoring'",  # ← REPLACE THIS
            ),
            
            # =========================================================
            # TECHNIQUE 6: Credential Access Test
            # 🔧 REPLACE with YOUR credential test
            # =========================================================
            Technique(
                id="T1003.001",
                name="Credential Access Test",
                tactic="Credential Access",
                platform=["Windows"],
                permissions=["Administrator"],
                description="Test if credential dumping is detected",
                detection_risk=0.8,
                success_rate=0.65,
                command=self._get_credential_test_command(),  # ← REPLACE THIS
            ),
            
            # =========================================================
            # TECHNIQUE 7: Discovery / Network Test
            # 🔧 REPLACE with YOUR network test
            # =========================================================
            Technique(
                id="T1087.001",
                name="Network Discovery Test",
                tactic="Discovery",
                platform=["Windows", "Linux"],
                permissions=["User"],
                description="Test if network scanning is detected",
                detection_risk=0.3,
                success_rate=0.95,
                command=self._get_network_test_command(),  # ← REPLACE THIS
            ),
            
            # =========================================================
            # TECHNIQUE 8: Lateral Movement Test
            # 🔧 REPLACE with YOUR lateral movement test
            # =========================================================
            Technique(
                id="T1021.006",
                name="Lateral Movement Test",
                tactic="Lateral Movement",
                platform=["Windows", "Linux"],
                permissions=["Administrator"],
                description="Test if lateral movement is detected",
                detection_risk=0.7,
                success_rate=0.7,
                command="echo 'Testing lateral movement detection'",  # ← REPLACE THIS
            ),
            
            # =========================================================
            # TECHNIQUE 9: Collection / Data Access Test
            # 🔧 REPLACE with YOUR data collection test
            # =========================================================
            Technique(
                id="T1005",
                name="Data Collection Test",
                tactic="Collection",
                platform=["Windows", "Linux"],
                permissions=["User"],
                description="Test if sensitive data access is monitored",
                detection_risk=0.4,
                success_rate=0.85,
                command="echo 'Testing data access monitoring'",  # ← REPLACE THIS
            ),
            
            # =========================================================
            # TECHNIQUE 10: C2 Communication Test
            # 🔧 REPLACE with YOUR C2 test
            # =========================================================
            Technique(
                id="T1071.001",
                name="C2 Communication Test",
                tactic="Command and Control",
                platform=["Windows", "Linux"],
                permissions=["User"],
                description="Test if C2 traffic is detected",
                detection_risk=0.5,
                success_rate=0.8,
                command="curl -s https://httpbin.org/get",  # ← REPLACE THIS
            ),
            
            # =========================================================
            # TECHNIQUE 11: Detection Check
            # 🔧 REPLACE with YOUR detection verification
            # =========================================================
            Technique(
                id="T1041",
                name="Detection Verification Test",
                tactic="Exfiltration",
                platform=["Windows", "Linux"],
                permissions=["User"],
                description="Check if security tools detected the tests",
                detection_risk=0.6,
                success_rate=0.75,
                command=self._get_detection_check_command(),  # ← REPLACE THIS
            )
        ]
        
        return techniques
    
    def cleanup(self) -> bool:
        """Clean up APT29 artifacts"""
        logger.info("Cleaning up APT29 artifacts...")
        logger.info("Removing test files...")
        logger.info("Clearing test logs...")
        return True
