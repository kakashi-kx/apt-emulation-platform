"""
Technique Templates - Users can copy and customize these
"""

class TechniqueTemplates:
    """Ready-to-use technique templates that users can modify"""
    
    @staticmethod
    def email_security_test():
        """Template for testing email security"""
        return """
        # ============================================
        # EMAIL SECURITY TEST - CUSTOMIZE THIS SECTION
        # ============================================
        
        # REPLACE WITH YOUR EMAIL SERVER
        EMAIL_SERVER = "smtp.yourcompany.com"
        
        # REPLACE WITH YOUR TEST EMAIL ADDRESS
        TEST_EMAIL = "securitytest@yourcompany.com"
        
        # REPLACE WITH YOUR PHISHING TEMPLATE
        PHISHING_TEMPLATE = """
        Subject: Urgent: Password Reset Required
        Click here to reset your password: http://test-phishing.com
        """
        
        # Command to send test email
        command = f"""
        python3 -c "
        import smtplib
        server = smtplib.SMTP('{EMAIL_SERVER}')
        server.sendmail('test@{EMAIL_SERVER}', '{TEST_EMAIL}', '''{PHISHING_TEMPLATE}''')
        server.quit()
        "
        """
        
        return Technique(
            id="T1566",
            name="Email Security Test",
            tactic="Initial Access",
            platform=["All"],
            permissions=["User"],
            description="Test if email gateway blocks phishing",
            command=command  # USER REPLACES THIS SECTION
        )
    
    @staticmethod
    def edr_test():
        """Template for testing EDR detection"""
        return """
        # ============================================
        # EDR TEST - CUSTOMIZE THIS SECTION
        # ============================================
        
        # REPLACE WITH YOUR EDR VENDOR
        EDR_VENDOR = "crowdstrike"  # Options: crowdstrike, sentinelone, defender
        
        # REPLACE WITH YOUR EDR TEST COMMAND
        if EDR_VENDOR == "crowdstrike":
            command = "C:\\Windows\\System32\\cs_test_tool.exe --simulate"
        elif EDR_VENDOR == "sentinelone":
            command = "C:\\Program Files\\SentinelOne\\s1_test.exe --eicar"
        elif EDR_VENDOR == "defender":
            command = "powershell -c Write-Host 'X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'"
        else:
            command = "echo 'Please configure your EDR test command'"
        
        return Technique(
            id="T1059",
            name="EDR Detection Test",
            tactic="Execution",
            platform=["Windows"],
            permissions=["User"],
            description="Test if EDR detects suspicious activity",
            command=command  # USER REPLACES THIS SECTION
        )
    
    @staticmethod
    def siem_test():
        """Template for testing SIEM detection"""
        return """
        # ============================================
        # SIEM TEST - CUSTOMIZE THIS SECTION
        # ============================================
        
        # REPLACE WITH YOUR SIEM URL
        SIEM_URL = "https://splunk.yourcompany.com:8089"
        
        # REPLACE WITH YOUR API KEY
        API_KEY = "your-api-key-here"
        
        # REPLACE WITH YOUR SEARCH QUERY
        SEARCH_QUERY = "index=security source=windows event_code=4688"
        
        # Command to query SIEM
        command = f"""
        curl -X GET '{SIEM_URL}/services/search/jobs' \\
             -H 'Authorization: Bearer {API_KEY}' \\
             -d search='{SEARCH_QUERY}'
        """
        
        return Technique(
            id="T1071",
            name="SIEM Detection Test",
            tactic="Discovery",
            platform=["All"],
            permissions=["User"],
            description="Test if SIEM logs the test activity",
            command=command  # USER REPLACES THIS SECTION
        )
