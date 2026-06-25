# CavrixOS

**A premium, modern Arch-based Linux distribution.**

Built by **Cavrix Core Technologies**.

---

## Overview

CavrixOS is a clean Arch-based distribution built using official Arch tools:
- **archiso** for ISO creation
- **archinstall** for the guided installer
- Standard Arch packaging (`makepkg` / `PKGBUILD`)

CavrixOS does **not** fork Arch Linux. It layers branding, curated defaults, and custom applications on top of a pure Arch base.

## Features

- **KDE Plasma 6** on Wayland (dark-first, minimal, premium)
- **PipeWire** audio stack
- **Btrfs** with automatic snapshots via Timeshift
- **ZRAM** swap with zstd compression
- **Secure Boot** support (systemd-boot + UKI)
- **Firewall** enabled by default (firewalld)
- **Flatpak** with Flathub pre-configured
- **NVIDIA / AMD / Intel** driver installer
- **CavrixOS Welcome** — onboarding application
- **CavrixOS Settings** — system configuration GUI
- **CavrixOS AI** — desktop AI assistant
- **Custom branding** — GRUB theme, Plymouth splash, SDDM login, icon pack, cursor, wallpapers

## Building

### Prerequisites

An Arch Linux system (or container) with:

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
- **Arch at the core** — Full AUR access, pacman, rolling release

## License

GPL-3.0-only — See [LICENSE](LICENSE).

## Contributing

See [docs/contributing.md](docs/contributing.md).
