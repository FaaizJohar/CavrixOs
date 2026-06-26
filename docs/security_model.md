# Security Model Specification

This document details the security layers, threat models, and access control policies implemented in CavrixOS.

## 1. Disk Encryption (LUKS2)

- **Current Implementation**: Scaffolded. The installer script (`installer/src/security/luks.py`) contains logic to format the root partition with `cryptsetup` using the LUKS2 specification.
- **Dependencies**: `cryptsetup`, `systemd`.
- **Validation Status**: Syntactically valid Python code. End-to-end integration within the Arch installation chroot is pending validation.

## 2. TPM2 Auto-Unlock

- **Current Implementation**: Scaffolded. Hardware detection for `/dev/tpmrm0` and execution of `systemd-cryptenroll --tpm2-device=auto` are present in the installer module.
- **Validation Status**: Pending. Requires testing on physical hardware with an active TPM 2.0 module. Virtual Machine testing with `swtpm` has not yet been executed.

## 3. Mandatory Access Control (AppArmor)

- **Current Implementation**: Scaffolded. A basic AppArmor profile exists for the AI Daemon (`distribution/security/apparmor.d/usr.bin.cavrix-ai-daemon`) to restrict arbitrary code execution while allowing GPU polling.
- **Validation Status**: The profile is syntactically valid but has not been enforced in `enforce` mode during runtime testing.

## 4. Boot Security

- **Secure Boot**: Pending implementation. Integration with `sbctl` or `shim` for UEFI Secure Boot signing of Unified Kernel Images is not currently present in the installer.

## 5. Known Limitations & Technical Debt

- **Key Management**: Passwords handled during the LUKS2 formatting phase in the installer are currently passed via standard shell pipes, which poses a memory-snooping risk.
- **Secret Storage**: Integration with KWallet or GNOME Keyring for storing user secrets is currently handled purely by upstream KDE defaults; no Cavrix-specific hardening has been applied.
