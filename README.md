<div align="center">
  <img src="assets/cavrixos-logo.svg" alt="Cavrix AI Logo" width="200" />
  
  # Cavrix AI
  **The Next-Generation, Mac-Inspired Linux Distribution**

  [![Build Status](https://img.shields.io/github/actions/workflow/status/FaaizJohar/CavrixOS/build-iso.yml?branch=main&style=for-the-badge&logo=github)](https://github.com/FaaizJohar/CavrixOS/actions)
  [![License](https://img.shields.io/badge/License-GPL%20v3-blue.svg?style=for-the-badge)](LICENSE)
  [![Architecture](https://img.shields.io/badge/Architecture-x86__64-orange?style=for-the-badge)]()
  [![Desktop](https://img.shields.io/badge/Desktop-Plasma_6_Custom-purple?style=for-the-badge)]()
</div>

---

## ⚡ Overview

**Cavrix AI** is an advanced, uncompromising desktop operating system engineered by **Cavrix Core Technologies**. Built on a rolling-release foundation, it bridges the gap between high-performance Linux architecture and premium, Apple-grade aesthetics. 

By aggressively customizing KDE Plasma 6 through programmatic Javascript layout overrides, native PyQT6 glassmorphism, and a custom repository architecture, Cavrix AI delivers an out-of-the-box experience that is minimal, visually stunning, and radically efficient.

## 🚀 Core Architecture & Features

### 1. UI/UX Paradigm
- **Mac-Inspired Topology**: The standard taskbar is programmatically annihilated on first boot, replaced by a 30px **Global Menu Top Bar** and a dynamically scaling, floating **Bottom Dock**.
- **Glassmorphic Ecosystem**: The `cavrix-welcome` and custom daemon applications are built entirely frameless, utilizing native Qt translucency and deep 14px border radii to emulate macOS Sonoma.
- **Unified GTK/Qt Theming**: Native integration of `appmenu-gtk-module` and `breeze-gtk` ensures GTK applications export their menus to the Plasma Top Bar flawlessly.

### 2. Under The Hood
- **Immutable Bootloader**: Built entirely around **systemd-boot** for UEFI systems (with GRUB fallback for legacy), ensuring instantaneous micro-second boot times.
- **Btrfs Subvolumes**: Aggressive `btrfs` snapshot topology is pre-configured during installation for instantaneous system rollbacks.
- **Cavrix AI Assistant**: Integrated daemon for desktop-level machine learning assistance.
- **Zero Bloat**: Pre-configured with Firewalld, Pipewire, Wayland, and Flathub. Nothing more, nothing less.

---

## 🛠️ Build Pipeline

Cavrix AI relies on a heavily orchestrated CI/CD pipeline using standard ISO generation toolchains (`cavrixiso`) and a modified guided installer (`cavrixinstall`).

### Local Development Prerequisites
To build the ISO locally, you require a standard Linux environment equipped with core development headers:
```bash
sudo pacman -S --needed base-devel git squashfs-tools qemu-full qemu-desktop
```

### Compiling the ISO
We utilize a monolithic Makefile to orchestrate the build process. Execute the build as root:
```bash
sudo make all
```
The resulting artifact `CavrixOS-<date>-x86_64.iso` will be synthesized into the `build/` directory.

### Testing the Build
To rapidly test the ISO in an ephemeral QEMU virtual machine without burning to physical media:
```bash
make test
```

---

## 📁 Repository Architecture

```text
CavrixOS/
├── cavrixiso/           # Cavrix AI live-environment overlay (airootfs)
├── cavrixinstall/       # Custom Python installer profile
├── branding/            # SVG vector assets, Plymouth themes, SDDM configs
├── packages/            # Proprietary PKGBUILDs (cavrix-welcome, cavrix-ai)
├── repositories/        # Local pacman repository generation logic
├── scripts/             # Orchestration scripts for CI/CD ISO building
└── Makefile             # Monolithic build system
```

---

## 💻 The Custom Installer

The standard CLI installer has been completely rewritten. Invoking `cavrixos-installer` in the live environment triggers a highly advanced bash script utilizing ANSI escape codes to render an animated, color-shifting ASCII representation of the **Cavrix AI** logo before seamlessly handing off the process to the Python installation backend.

---

## 🤝 Contributing & Documentation

We demand high-quality, strictly formatted code. If you wish to contribute to the Cavrix AI ecosystem:
1. Review the [Architecture Documentation](docs/architecture.md) to understand our upstream-first philosophy.
2. Read the [Building Guide](docs/building.md) for local compilation specifics.
3. Ensure all Python applications include `__init__.py` and pass `python -m py_compile`.
4. Submit pull requests against the `main` branch.

<div align="center">
  <i>Engineered for the future of the Linux Desktop.</i>
</div>
