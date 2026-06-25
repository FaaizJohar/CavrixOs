# Cavrix AI
**A premium, modern Linux distribution.**
Built by **Cavrix Core Technologies**.

---

## Overview

Cavrix AI is a clean distribution built using standard core tools:
- **archiso** for ISO creation
- **archinstall** for the guided installer
- Standard Arch packaging (`makepkg` / `PKGBUILD`)

Cavrix AI layers premium branding, curated defaults, and custom applications on top of a rock-solid core base.

## Features

- **KDE Plasma 6** on Wayland (dark-first, minimal, premium)
- **PipeWire** audio stack
- **Btrfs** with automatic snapshots via Timeshift
- **ZRAM** swap with zstd compression
- **Secure Boot** support (systemd-boot + UKI)
- **Firewall** enabled by default (firewalld)
- **Flatpak** with Flathub pre-configured
- **NVIDIA / AMD / Intel** driver installer
- **Cavrix AI Welcome** — onboarding application
- **Cavrix AI Settings** — system configuration GUI
- **Cavrix AI Assistant** — desktop AI assistant
- **Custom branding** — GRUB theme, Plymouth splash, SDDM login, icon pack, cursor, wallpapers

## Building Cavrix AI

### Prerequisites

A Linux system (or container) with standard build tools:

```bash
sudo pacman -S archiso base-devel git
```

### Build the ISO

```bash
make iso
```

The ISO will be output to `build/`.

### Test in QEMU

```bash
make test
```

### Full Pipeline

```bash
make all    # packages → repo → iso
```

## Project Structure

```
CavrixOS/
├── archiso/          # archiso profile (ISO configuration)
├── archinstall/      # Custom archinstall profile & config
├── branding/         # Brand assets (logos, colors, fonts)
├── packages/         # Custom PKGBUILD packages
├── repositories/     # Package repository tools
├── installer/        # Installer UI extensions
├── cavrix-settings/  # Settings application
├── cavrix-welcome/   # Welcome application
├── cavrix-ai/        # AI desktop assistant
├── themes/           # KDE Plasma / GTK themes
├── wallpapers/       # Desktop wallpapers
├── grub/             # GRUB theme
├── plymouth/         # Boot splash theme
├── sddm/             # Login screen theme
├── scripts/          # Build & utility scripts
├── build/            # Build output (gitignored)
├── .github/          # CI/CD workflows
└── docs/             # Documentation
```

## Design Philosophy

- **Minimal** — No bloat, every package earns its place
- **Premium** — Apple-grade polish, not "gamer RGB"
- **Modern** — Wayland-first, PipeWire, systemd-boot, UKI
- **Dark-first** — Professional dark theme as the default
- **Rolling Release** — Full package manager access, rolling release

## License

GPL-3.0-only — See [LICENSE](LICENSE).

## Contributing

See [docs/contributing.md](docs/contributing.md).
