#!/usr/bin/env python3
"""
Customization Helper - Helps users create their own test configurations
"""

import os
import sys

def create_custom_technique():
    """Interactive tool to create custom techniques"""
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║     APT Emulation Platform - Customization Wizard         ║
    ║                                                           ║
    ║     This will help you create techniques for YOUR system  ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Get technique details
    name = input("Technique Name (e.g., Test Email Filter): ")
    tactic = input("MITRE Tactic (e.g., Initial Access): ")
    command = input("Command to run on YOUR system: ")
    
    # Generate the technique code
    technique_code = f"""
from core.base_emulator import Technique

def get_my_technique():
    return Technique(
        id="CUSTOM001",
        name="{name}",
        tactic="{tactic}",
        platform=["All"],
        permissions=["User"],
        description="Custom test for my environment",
        command="{command}"  # ← THIS IS YOUR COMMAND
    )
"""
    
    # Save to file
    filename = "my_custom_techniques.py"
    with open(filename, 'w') as f:
        f.write(technique_code)
    
    print(f"\n✅ Created: {filename}")
    print(f"   Edit this file to add more techniques")
    print(f"   Run: python3 {filename}")

def create_config_template():
    """Create a configuration template"""
    
    template = """# ============================================
# MY COMPANY CONFIGURATION
# Copy this file and replace with your details
# ============================================

company:
  name: "YOUR_COMPANY_NAME"
  environment: "production"

# REPLACE WITH YOUR DETAILS
network:
  domain: "yourcompany.local"
  ip_range: "10.0.0.0/16"

# REPLACE WITH YOUR SECURITY TOOLS
security_tools:
  email_gateway: "your_email_gateway"
  edr: "your_edr_vendor"
  siem: "your_siem"

# REPLACE WITH YOUR TEST COMMANDS
tests:
  email_test: "python3 /path/to/your/email_test.py"
  edr_test: "C:\\\\path\\\\to\\\\your\\\\edr_test.exe"
  network_test: "nmap yourcompany.com"
"""
    
    with open("my_config.yaml", 'w') as f:
        f.write(template)
    
    print("✅ Created: my_config.yaml")
    print("   Edit this file with your company details")

if __name__ == "__main__":
    print("""
    1. Create custom technique
    2. Create config template
    """)
    choice = input("Choose (1 or 2): ")
    
    if choice == "1":
        create_custom_technique()
    elif choice == "2":
        create_config_template()
