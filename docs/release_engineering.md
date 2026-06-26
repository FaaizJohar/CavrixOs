# Release Engineering Specification

This document details the Continuous Integration, Continuous Deployment (CI/CD), and release automation pipelines for CavrixOS.

## 1. Build System Architecture

The build process is orchestrated via a GNU `Makefile` at the repository root.

### 1.1 `mkarchiso` Integration
- **Current Implementation**: The `make iso` target invokes the official `mkarchiso` tool. It mounts the `distribution/` directory as the build profile.
- **Dependencies**: `archiso`, `make`, `bash`.
- **Validation Status**: Implemented and functionally validated via GitHub Actions.

## 2. CI/CD Pipeline

The release pipeline is defined in `.github/workflows/release.yml`.

### 2.1 Workflow Stages
1. **Environment Setup**: Provisions an Ubuntu runner and mounts an `archlinux:base-devel` Docker container.
2. **Dependency Injection**: Installs `archiso`, `qemu-full`, and `edk2-ovmf`.
3. **Build & Package**: Runs `make packages` and `make repo`.
4. **ISO Generation**: Runs `make iso`.
5. **Publishing**: Uploads the generated `.iso` and `SHA256SUMS` as GitHub Release artifacts.

### 2.2 Implementation Status
- **Current Implementation**: Fully implemented.
- **Validation Status**: Successfully generates bootable ISO artifacts on tag pushes (`v*`).

## 3. Release Lifecycle

- **Nightly**: Scaffolded. No dedicated nightly workflow exists yet.
- **Testing**: Pending implementation. Testing channels will utilize a separate pacman repository configuration.
- **Stable**: Implemented via Git Tags (e.g., `v1.0.0`).

## 4. Known Limitations & Technical Debt
- **Cache Invalidation**: The pacman cache within GitHub Actions is currently monolithic. If a build fails, the cache might contain corrupted partial downloads, causing subsequent builds to fail.
- **ISO Signing**: Currently, the ISO is only hashed via SHA256. It is not cryptographically signed with `gpg --detach-sign`.
- **Reproducible Builds**: The build environment is somewhat hermetic due to Docker, but true reproducible builds (bit-for-bit identical outputs) are not guaranteed because timestamps within the SquashFS image are not stripped or normalized.
