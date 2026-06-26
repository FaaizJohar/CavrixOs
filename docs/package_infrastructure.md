# Package Infrastructure Specification

This document outlines the package repository layout, signing policies, and metadata generation for CavrixOS.

## 1. Repository Layout

CavrixOS maintains three local repositories built on top of the Arch Linux core:
- **`cavrix-core`**: Core utilities, mirroring tools, and keyring (`cavrixos-keyring`, `cavrixos-mirrorlist`).
- **`cavrix-extra`**: Desktop environment configurations, themes, and first-party applications (`cavrix-welcome`, `cavrixos-branding`).
- **`cavrix-ai`**: AI subsystem dependencies and the `cavrix-ai-pkg` daemon.

### 1.1 Directory Structure
```text
/packages/
├── cavrix-core/
├── cavrix-extra/
└── cavrix-ai/
```

## 2. Implementation Status

### 2.1 Repository Generation
- **Current Implementation**: Implemented via `Makefile`. The `make repo` target compiles all directories containing a `PKGBUILD` using `makepkg -sfi`, copies the resulting `.pkg.tar.zst` files into `repositories/<repo_name>`, and executes `repo-add` to generate `repo.db.tar.zst` and `repo.files.tar.zst`.
- **Validation Status**: Verified in the GitHub Actions `release.yml` pipeline. The repositories successfully build within the isolated Arch container.

### 2.2 Package Signing
- **Current Implementation**: Scaffolded. A bash script (`ci/scripts/mock-gpg.sh`) is currently utilized in the CI environment to generate ephemeral, passwordless OpenPGP keys. These keys are used to sign the pacman databases.
- **Dependencies**: `gnupg`, `pacman-key`.
- **Validation Status**: Mock keys successfully sign the DB in CI.

## 3. Package Policies

### 3.1 Versioning
- Packages follow semantic versioning (`MAJOR.MINOR.PATCH`).
- PKGBUILD `pkgrel` numbers are incremented for rebuilds without upstream code changes.

### 3.2 Dependency Policy
- No CavrixOS package may introduce a conflict with `core` or `extra` Arch Linux packages unless utilizing the `provides` and `conflicts` arrays explicitly.

## 4. Known Limitations & Technical Debt
- **Cryptographic Trust Chain**: The current GPG implementation uses an ephemeral key (`ci/scripts/mock-gpg.sh`). This is technically unacceptable for a production distribution. A permanent master signing key must be generated on air-gapped hardware, with subkeys exported as GitHub Secrets.
- **Rebuild Policy**: There is currently no automated infrastructure to monitor upstream Arch updates and trigger rebuilds of Cavrix packages if ABI/API breakages occur.
