## Reporting a Vulnerability

**Please DO NOT file public issues for security vulnerabilities.**

Instead, contact me directly:
- 📧 Email: kakashi4kx@gmail.com
- 🐙 GitHub: [Create a private security advisory](https://github.com/kakashi-kx/apt-emulation-platform/security/advisories/new)

We will:
1. Acknowledge receipt within 48 hours
2. Investigate and validate the issue
3. Provide a fix within 7-14 days
4. Release a patch and credit the reporter (if desired)

## Security Best Practices

### For Users
- ✅ Always run in safe mode first: `--safe-mode`
- ✅ Only use on systems you own or have permission to test
- ✅ Review commands before execution
- ✅ Keep the tool updated
- ✅ Use environment variables for sensitive configs

### For Developers
- ✅ Use environment variables for secrets (`.env`)
- ✅ Never commit `.env` files to GitHub
- ✅ Enable rate limiting in production
- ✅ Use proper logging for audits
- ✅ Follow OWASP guidelines
- ✅ Run `pip-audit` to check for vulnerable dependencies

## Vulnerability Disclosure Policy

- 🔒 **Private reporting only** - No public issues for security bugs
- 📝 **50-day disclosure timeline** - We'll fix it within 50 days
- 🏷️ **CVE assignment** - We'll request CVE if needed
- 👏 **Credit** - We'll acknowledge your contribution

## Security Contact

For urgent security issues, you can also reach me on LinkedIn:
- 🔗 [Abhijith S](https://www.linkedin.com/in/abhixjith)
