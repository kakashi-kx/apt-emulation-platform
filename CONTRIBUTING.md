# Contributing

Thanks for considering a contribution — this project is more useful the more real-world technique coverage and integrations it has.

## Ways to help

- **New techniques** for an existing profile (`apt_profiles/apt29.py`, `lazarus.py`, `ransomware.py`) — each `Technique` needs a MITRE ATT&CK ID, tactic, and a safe test command
- **New threat-actor profiles** — subclass `AdversaryEmulator` in `core/base_emulator.py` and implement `get_technique_sequence()`, `validate_environment()`, and `get_required_permissions()`
- **SIEM/detection export formats** beyond Sigma
- **Bug reports** — please include the exact command you ran and the output

## Getting set up

```bash
git clone https://github.com/kakashi-kx/apt-emulation-platform.git
cd apt-emulation-platform
pip install -r requirements.txt -r requirements-web.txt
pytest tests/ -v
```

## Before opening a PR

- Run `pytest tests/ -v` locally — CI will run the same suite and blocks on failure
- Keep new technique commands safe by default (no destructive actions, no real exfiltration, no network calls to anything other than clearly-labeled test endpoints)
- If you're adding a technique, include its MITRE ATT&CK technique ID and a one-line description of what real-world tradecraft it models

## Reporting security issues

Please don't open a public issue for a security vulnerability — see [SECURITY.md](SECURITY.md) instead.
