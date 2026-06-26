# Security Policy

## Supported Versions

CavrixOS provides security updates for the packages maintained within its specific repositories (`cavrix-core`, `cavrix-extra`, `cavrix-ai`).
Packages derived from upstream Arch Linux are supported by the Arch Security Team.

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| 0.x.x   | :x:                |

## Reporting a Vulnerability

If you discover a vulnerability in a CavrixOS-specific application (e.g., the Cavrix AI Daemon, the CavrixInstall process, or desktop configuration scripts), please DO NOT open a public issue.

Instead, report it privately via email:
**security@cavrixos.org**

### Threat Models of Concern
We are specifically interested in:
- Local privilege escalation (LPE) vulnerabilities within the `cavrix-ai-daemon` or Polkit policies.
- Secrets handling vulnerabilities in the `cavrixos-install.py` LUKS implementation.
- Arbitrary code execution (ACE) flaws in the `cavrix-welcome` or update utilities.

We will acknowledge receipt of the vulnerability within 48 hours and strive to issue a patched release within 7 days.
