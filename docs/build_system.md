# Build System Specification

This document details the build environment, caching strategies, and artifact generation processes for CavrixOS.

## 1. Makefile Orchestration

The root `Makefile` serves as the primary entry point for all build operations.

### 1.1 Targets
- `make packages`: Iterates through the `packages/` directory and builds each PKGBUILD using `makepkg`.
- `make repo`: Compiles the generated `.pkg.tar.zst` files into pacman databases via `repo-add`.
- `make iso`: Invokes `mkarchiso` to build the final bootable image using the `distribution/` profile.
- `make clean`: Removes the `build/`, `repositories/`, and `/tmp/cavrixos-build` directories.

## 2. Docker Build Environment

- **Current Implementation**: CI/CD builds occur inside a privileged `archlinux:base-devel` Docker container runner on Ubuntu.
- **Dependencies Installed at Runtime**: `archiso`, `git`, `grub`, `edk2-ovmf`, `mtools`.

### 2.1 Caching Strategy
- **Pacman Cache**: The GitHub Actions runner utilizes `actions/cache@v3` to preserve `/var/cache/pacman/pkg` across runs.
- **Limitation**: The cache key is derived from a hash of all `PKGBUILD` files. This means any change to a PKGBUILD will invalidate the entire cache, requiring a full re-download of all ISO dependencies (e.g., Plasma, Wayland) during the next run. This is a significant source of technical debt causing 10-15 minute CI runs.

## 3. Artifact Generation

- **ISO Generation**: The SquashFS image is built using ZSTD compression. The final artifact is output to `build/CavrixOS-*.iso`.
- **Checksums**: A `SHA256SUMS` file is generated via `sha256sum`.

## 4. Known Limitations & Technical Debt

- **Build Reproducibility**: The ISO build process is not deterministic. File timestamps within the SquashFS image and pacman databases are based on build-time clocks, preventing bit-for-bit reproducible builds.
- **Privileged Container Requirement**: `mkarchiso` requires root privileges to mount filesystems, necessitating a `--privileged` Docker container in CI, which expands the attack surface of the runner environment.
