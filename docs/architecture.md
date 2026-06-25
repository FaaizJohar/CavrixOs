# CavrixOS Architecture

CavrixOS is a derivative built on the following principles:

1. **Upstream First**: We do not fork core packages unless absolutely necessary. We rely on the upstream repositories for the base system.
2. **Archiso**: We use standard ISO generation tools to build our live environment. Our customizations are layered via the `airootfs` overlay.
3. **Installer**: Our installer is a custom wrapper around the official `archinstall` library. We provide a pre-configured profile (`cavrixos_profile.py`) that sets up the system with our defaults.
4. **Local Repository**: We maintain a local package repository for our custom branding, configurations, and applications. This repository is included in the live ISO and configured on the installed system.

## Components

```mermaid
graph TD
    A[Hardware] --> B[UEFI Firmware]
    B --> C[systemd-boot]
    C --> D[Linux-Zen Kernel]
    D --> E[systemd init]
    E --> F[Wayland Display Server]
    F --> G[KDE Plasma 6]
    
    %% Custom UI Overrides
    G --> H[Javascript Plasma Layout overrides]
    H --> I[Mac Top Bar & Global Menus]
    H --> J[Floating Bottom Dock]
    
    %% Core Apps
    G --> K[Cavrix AI Assistant Daemon]
    G --> L[Cavrix Welcome App]
    
    classDef core fill:#2563EB,stroke:#1E40AF,stroke-width:2px,color:#fff;
    classDef ui fill:#93C5FD,stroke:#3B82F6,stroke-width:2px,color:#000;
    
    class C,D,E core;
    class G,I,J,K,L ui;
```

- **Base**: `linux-zen`, `systemd`, `btrfs`
- **Boot**: `systemd-boot` (UEFI) / `GRUB` (Legacy), `Plymouth`
- **Display**: `Wayland`, `KDE Plasma 6`, `SDDM`
- **Audio**: `PipeWire`
- **Networking**: `NetworkManager`, `firewalld`
- **Package Management**: `pacman`, `Flatpak` (with Flathub)
