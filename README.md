<div align="center">
  <img src="assets/cavrixos-logo.svg" alt="CavrixOS Logo" width="220" />
  
  # CavrixOS
  **An Arch Linux derivative featuring integrated local AI and customized KDE Plasma**

  [![Build Status](https://img.shields.io/github/actions/workflow/status/FaaizJohar/CavrixOS/release.yml?branch=main&style=for-the-badge&logo=github)](https://github.com/FaaizJohar/CavrixOS/actions)
  [![License](https://img.shields.io/badge/License-GPL%20v3-blue.svg?style=for-the-badge)](LICENSE)
  [![Architecture](https://img.shields.io/badge/Architecture-x86__64-orange?style=for-the-badge)]()
  [![Desktop](https://img.shields.io/badge/Desktop-Wayland%20%7C%20Plasma_6-purple?style=for-the-badge)]()
</div>

<br>

CavrixOS is an open-source Linux distribution based on Arch Linux. Our primary goal is to provide a pre-configured desktop environment (KDE Plasma 6 on Wayland) bundled with local Large Language Model (LLM) execution capabilities via Ollama. 

Rather than requiring users to manually configure their environments for local AI workloads, CavrixOS handles the integration out-of-the-box.

## Features

- **Base System**: Inherits directly from Arch Linux, utilizing the `linux-zen` kernel for desktop responsiveness and `systemd` for initialization.
- **Local AI Daemon**: Includes `ollama` as a pre-configured, enabled systemd service. This allows for immediate local execution of models without external API dependencies.
- **Terminal Integration**: Provides a custom `cavrix-ask` command-line utility, which interfaces directly with the local Ollama daemon to assist with terminal commands and system administration.
- **Custom Desktop Layout**: Modifies the default KDE Plasma 6 topology to include a top global menu bar and a floating bottom dock, utilizing standard Plasma applets.
- **Automated Installer**: Features a custom Python-based deployment wizard built on top of the official `archinstall` library.

---

## Architecture Overview

CavrixOS is fundamentally an overlay on top of Arch Linux. We rely on upstream repositories for the vast majority of our packages. Our customizations are applied during the ISO generation process and installation via our `archinstall` profile.

For a detailed technical breakdown, please refer to the [Architecture Documentation](docs/architecture.md).

---

## Build Pipeline & CI/CD

CavrixOS utilizes GitHub Actions for continuous integration. The ISO is generated automatically on every push to the `main` branch.

### Prerequisites (Local Building)

To build the ISO locally on a Linux host, you will need the standard Arch build tools:
```bash
sudo pacman -S --needed base-devel git archiso squashfs-tools qemu-full qemu-desktop
```

### Build Commands

We use a `Makefile` to automate the `mkarchiso` build process. Root privileges are required for `archiso` environment preparation.

```bash
# Build custom packages, generate the local repository, and build the ISO
sudo make all

# Validate Python and Bash script syntax
make lint

# Launch the generated ISO in an ephemeral QEMU VM
make test

# Clean build artifacts and work directories
sudo make clean
```

The resulting ISO will be placed in the `build/` directory. For more details, see [Building CavrixOS](docs/building.md).

---

## Repository Structure

```text
CavrixOS/
├── cavrixiso/           # Configuration files and overlays for mkarchiso (airootfs)
├── cavrixinstall/       # Custom Python profiles extending the archinstall library
├── packages/            # PKGBUILDs for custom branding, themes, and scripts
├── repositories/        # Local pacman repository generated during the build process
├── docs/                # Technical documentation (architecture, building, contributing)
├── scripts/             # Helper scripts for the CI/CD pipeline
├── .github/             # GitHub Actions workflows and issue templates
└── Makefile             # Automation for ISO and package building
```

---

## Performance & Benchmarks

> [!NOTE]  
> **TODO: Await formal benchmark data.**
> We are currently gathering comprehensive benchmarks for memory utilization, boot times, and LLM token generation rates across various hardware configurations. Claims regarding baseline memory usage (e.g., operating under 2GB RAM) are currently unverified and subject to rigorous testing.

---

## Contributing

We welcome contributions to CavrixOS. Please ensure that all modifications align with our design philosophy of remaining as close to upstream Arch Linux as possible while providing our specific AI and UI enhancements.

Please review the following documentation before submitting pull requests:
1. [Architecture Documentation](docs/architecture.md)
2. [Contributing Guidelines](docs/contributing.md)

All pull requests must pass the automated `.github/workflows/release.yml` CI pipeline (`flake8` for Python, `shellcheck` for Bash).

---

## License

CavrixOS is licensed under the GPL v3 License. See the [LICENSE](LICENSE) file for more information.

For direct contact regarding the project, please email [hello@cavrixcore.com](mailto:hello@cavrixcore.com).
