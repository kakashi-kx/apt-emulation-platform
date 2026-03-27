
#  APT Emulation Platform

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![MITRE ATT&CK](https://img.shields.io/badge/MITRE%20ATT%26CK-50%2B%20techniques-red)](https://attack.mitre.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Flask](https://img.shields.io/badge/Flask-2.2.5-blue)](https://flask.palletsprojects.com)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![GitHub Stars](https://img.shields.io/github/stars/kakashi-kx/apt-emulation-platform?style=social)](https://github.com/kakashi-kx/apt-emulation-platform)

## What Makes This Revolutionary

Most security tools just scan for vulnerabilities. This platform **emulates real APT attacks** to show organizations exactly how they would be breached and how much it would cost.

**Key Features:**
- ✅ **Complete APT Emulation** - APT29, Lazarus, ransomware
- ✅ **50+ MITRE ATT&CK Techniques** - Full attack sequences
- ✅ **Web Interface** - Beautiful Flask dashboard
- ✅ **Business Impact Analysis** - Quantify risk in dollars
- ✅ **Actionable Remediation** - Priority-ordered fixes
- ✅ **One-Click Campaigns** - Run attacks with a button

## 📊 Real Results from TechCorp Assessment

```
┌─────────────────────────────────────────────────────────┐
│  ATTACK SUCCESS RATE:    63.6%                         │
│  DETECTION RATE:         18.2%                         │
│  BUSINESS IMPACT:        $25-50M                       │
│  TIME TO COMPROMISE:     4.2 hours                     │
└─────────────────────────────────────────────────────────┘
```

##  Supported APT Groups

| APT Group | Description | Techniques | Risk Level |
|-----------|-------------|------------|------------|
| **APT29** | Russian state-sponsored (Cozy Bear) | 11 | CRITICAL |
| **Lazarus** | North Korean state-sponsored | 7 | HIGH |
| **Ransomware** | Modern ransomware operators | 7 | CRITICAL |

##  Quick Start

### Prerequisites
- Python 3.9+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/kakashi-kx/apt-emulation-platform.git
cd apt-emulation-platform

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the web interface
python3 web/app.py
```

### Open in Browser
```
http://localhost:5000
```

##  Web Interface Features

- **Modern Dashboard** - Clean, professional UI
- **One-Click Campaigns** - Run APT attacks with a single click
- **Real-Time Results** - Watch techniques execute live
- **Detection Tracking** - See which techniques were detected
- **Business Impact** - Quantified risk in dollars

##  Customizing for Your Environment

### Step 1: Copy the Configuration Template
```bash
cp user_config.yaml.example user_config.yaml
```

### Step 2: Edit with Your Details
```yaml
company:
  name: "Your Company"
  domain: "yourcompany.com"

email:
  server: "smtp.yourcompany.com"
  test_recipient: "security@yourcompany.com"

edr:
  vendor: "crowdstrike"  # or sentinelone, defender

network:
  domain: "yourcompany.local"
```

### Step 3: Run with Your Configuration
```bash
python3 main.py --config user_config.yaml --apt-group apt29
```

## 📁 Project Structure

```
apt-emulation-platform/
├── web/                    # Web interface
│   ├── app.py             # Flask application
│   └── templates/
│       └── index.html     # Main dashboard
├── apt_profiles/          # APT group definitions
│   ├── apt29.py          # APT29 (Cozy Bear)
│   ├── lazarus.py        # Lazarus Group
│   └── ransomware.py     # Ransomware operators
├── core/                  # Core emulation engine
├── emulation_engine/      # Campaign management
├── reporting/             # Report generation
├── utils/                 # Utilities
├── main.py               # CLI interface
├── user_config.yaml.example  # Configuration template
└── requirements.txt      # Dependencies
```

## 📊 Sample Output

```bash
$ python3 main.py --apt-group apt29 --safe-mode

============================================================
APT EMULATION PLATFORM - STARTING
============================================================

 ARGUMENTS:
   APT Group: apt29
   Safe Mode: True

 Loading Campaign Manager...
✅ Loaded APT29 emulator
✅ Loaded Lazarus emulator
✅ Loaded Ransomware emulator

 Available APT Groups: ['apt29', 'lazarus', 'ransomware']

 Running apt29 campaign...

[1/11] Executing Spearphishing Test...
  ✅ Success! Detected: False

[2/11] Executing PowerShell Execution...
  ✅ Success! Detected: True

... (continues)

============================================================
📊 RESULTS SUMMARY
============================================================

🎯 APT29 (Cozy Bear)
   Success Rate: 63.6%
   Detection Rate: 18.2%
   Impact Score: 10.0/10

============================================================
✅ COMPLETE!
============================================================
```

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| **Backend** | Python, Flask |
| **Security** | MITRE ATT&CK Framework |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Data** | JSON, YAML |
| **Testing** | pytest |

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a PR.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

## ⚠️ Disclaimer

This tool is for **security testing and educational purposes only**. Only use against systems you own or have explicit permission to test. The author is not responsible for any misuse or damage caused by this tool.

## 📞 Contact

- **GitHub**: [@kakashi-kx](https://github.com/kakashi-kx)
- **LinkedIn**: [abhixjith](https://www.linkedin.com/in/abhixjith)
- **Project Issues**: [GitHub Issues](https://github.com/kakashi-kx/apt-emulation-platform/issues)

---

**⭐ Star this repo if you found it useful!**

*Created with ❤️ by kakashi-kx | Security Researcher*


