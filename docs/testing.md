# Testing and Validation Specification

This document details the validation strategies, testing matrices, and CI/CD testing integration for CavrixOS.

## 1. Unit Testing

- **Framework**: `pytest` (Python).
- **Current Implementation**: Scaffolded. Basic unit tests exist in `testing/tests/test_installer.py` to validate isolated functions like the hardware detector fallback logic and subvolume generation strings.
- **Coverage**: Extremely low. Currently only covers isolated string/list generation logic in the installer.
- **Validation Status**: Syntactically valid, but no automated runner is configured in CI to execute these tests before ISO generation.

## 2. Boot & Integration Testing

- **Current Implementation**: Scaffolded. The root `Makefile` includes `test` and `test-efi` targets that utilize `qemu-system-x86_64` to boot the generated ISO.
- **Validation Status**: These commands must be run manually by the developer on their local host. They are not currently executed headlessly within the GitHub Actions pipeline.

## 3. Hardware Validation Matrix

Physical hardware validation is currently a manual checklist process. 

### Pending Execution Matrix:
- [ ] UEFI Boot (Intel x64)
- [ ] UEFI Boot (AMD x64)
- [ ] Secure Boot (Signed UKI)
- [ ] NVIDIA Proprietary Driver Injection
- [ ] AMDGPU Open Driver Injection
- [ ] Wi-Fi/Bluetooth Initialization (Intel AX200 series)
- [ ] Sleep/Resume (S3) State Validation

## 4. Known Limitations & Technical Debt

- **No Regression Testing**: There is no framework in place to detect if an upstream Arch Linux package update breaks Cavrix-specific desktop configurations.
- **No Automated GUI Testing**: The Qt-based first-party applications (`cavrix-settings`, `cavrix-welcome`) do not have UI testing frameworks (like `pytest-qt` or `Squish`) implemented.
