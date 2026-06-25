<div align="center">
  <img src="assets/cavrixos-logo.svg" alt="Cavrix AI Logo" width="220" />
  
  # CAVRIX AI
  **The Sovereign, AI-Native Operating Environment**

  [![Build Status](https://img.shields.io/github/actions/workflow/status/FaaizJohar/CavrixOS/build-iso.yml?branch=main&style=for-the-badge&logo=github)](https://github.com/FaaizJohar/CavrixOS/actions)
  [![License](https://img.shields.io/badge/License-GPL%20v3-blue.svg?style=for-the-badge)](LICENSE)
  [![Architecture](https://img.shields.io/badge/Architecture-x86__64-orange?style=for-the-badge)]()
  [![Desktop](https://img.shields.io/badge/Topology-Wayland%20%7C%20Plasma_6-purple?style=for-the-badge)]()
</div>

<br>

## Cavrix AI - The World's First AI-Powered Operating System

Welcome to **Cavrix AI**, the first operating system where artificial intelligence is natively baked into the core architecture. Built on a blazing-fast, ultra-optimized Linux base, Cavrix AI delivers a premium, hyper-intelligent desktop experience that outsmarts everything else on the market.

## ✨ AI At The Core
- **Native AI Engine**: Powered by Ollama built directly into `systemd`, running local LLMs securely.
- **Desktop AI Assistant**: A stunning, glassmorphism transparent AI widget permanently available on your desktop.
- **Terminal AI Assistant**: Ask your terminal anything with the built-in `cavrix-ask` command (e.g. `cavrix-ask "how do I unzip a file?"`).
- **Unbelievably Optimized**: Aggressive ZRAM, strict kernel tuning, and UI optimizations designed to run flawlessly in just **2GB of RAM**.

---

## 🚀 Core Architecture

The system is constructed across four highly isolated computing tiers:

| Tier | Component | Specification | Description |
| :--- | :--- | :--- | :--- |
| **0. Boot** | `systemd-boot` | UEFI / UKI | Micro-second initialization topology bypassing legacy GRUB overhead. |
| **1. Kernel** | `linux-zen` | Scheduler | Heavily tuned for desktop responsiveness and low-latency throughput. |
| **2. Display** | `Wayland` + `Plasma 6`| Compositor | Hardware-accelerated window management overriding standard layouts. |
| **3. Logic** | `Cavrix Assistant` | ML Daemon | Integrated artificial intelligence subsystem operating at the desktop layer. |

### ❯ Proprietary Enhancements
* **Dynamic Global Topography**: The window manager topology is programmatically rewritten on initialization. Standard taskbars are destroyed and replaced by a 30px Global Menu header and a dynamically scaling, floating dock mechanism.
* **Translucent Qt Rendering**: Core applications (such as the `cavrix-welcome` suite) are executed utilizing `WA_TranslucentBackground` flags, bypassing standard window manager frames in favor of hardware-blurred, deeply rounded (14px radius) glass elements.
* **Immutable Rollbacks**: Configured natively with rapid-deployment Btrfs subvolumes, allowing instantaneous temporal system restoration.

---

## 🛠️ Build Pipeline & CI/CD

Cavrix AI utilizes a deeply integrated continuous integration (CI) pipeline to synthesize its ISO artifacts. The repository relies on `cavrixiso` for environment generation and `cavrixinstall` for the customized deployment wizard.

### Prerequisites (Local Synthesis)
To compile the environment locally, a standard Linux toolchain is strictly required:
```bash
sudo pacman -S --needed base-devel git squashfs-tools qemu-full qemu-desktop
```

### Orchestration Commands
We employ a monolithic `Makefile` to govern the build orchestration. Execution requires elevated privileges:

```bash
# Synthesize the complete x86_64 ISO artifact
sudo make all

# Validate syntax across Python and Bash subsystems
make lint

# Launch ephemeral QEMU test environment
make test

# Purge compilation artifacts
sudo make clean
```
*Generated artifacts are deposited securely within the `build/` directory.*

---

## 📁 Repository Structure

```text
CavrixOS/
├── cavrixiso/           # Core live-environment filesystem overlay (airootfs)
├── cavrixinstall/       # Proprietary Python deployment profile algorithms
├── branding/            # SVG vector assets, Plymouth splashes, SDDM login definitions
├── packages/            # Cavrix AI specific PKGBUILD compilation scripts
├── repositories/        # Local package mirror generation logic
├── scripts/             # Subsystem orchestration for CI/CD ISO building
├── .github/             # Enterprise governance, Issue Templates, and linting pipelines
└── Makefile             # Monolithic artifact build system
```

---

## 💻 Animated Deployment Terminal

The deployment logic has been decoupled from standard Linux installers. When invoking the installer in the live environment, the `cavrixos-installer` daemon hijacks the standard output. Utilizing ANSI escape sequences and `tput` buffering, it renders a high-fidelity, color-shifting ASCII loading sequence for the **Cavrix AI** subsystem before handing off execution to the asynchronous Python installation backend.

---

## 🤝 Enterprise Governance & Contribution

This repository adheres to strict enterprise-grade development standards. If you are contributing code to Cavrix AI, you must abide by the following protocols:

1. **Architecture Integrity**: Review [Architecture Documentation](docs/architecture.md) prior to submitting logic changes.
2. **Automated Linting**: All pull requests must pass the `.github/workflows/lint.yml` CI pipeline (`flake8` / `shellcheck`).
3. **Security Policy**: Vulnerabilities must be reported in accordance with [SECURITY.md](SECURITY.md).
4. **Code of Conduct**: All contributors are bound by the [Contributor Covenant](CODE_OF_CONDUCT.md).

---

## 🌐 Contact & Corporate

For business inquiries, enterprise licensing, or direct engineering support, please reach out via our official channels:
* **Website**: [cavrixcore.com](https://cavrixcore.com)
* **Email**: [hello@cavrixcore.com](mailto:hello@cavrixcore.com)

<br>

<div align="center">
  <i>Engineered by Cavrix Core Technologies. The apex of sovereign computing.</i>
</div>
