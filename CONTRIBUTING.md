# Contributing to CavrixOS

Thank you for your interest in contributing to CavrixOS! As a production-grade distribution, we maintain strict engineering and code quality standards.

## 1. Branching Strategy

- `main`: The stable development branch. Must always be in a green (building) state.
- `feature/*`: For new features (e.g., `feature/luks-tpm-support`).
- `bugfix/*`: For fixing documented issues.

## 2. Pull Request Requirements

Before submitting a Pull Request, ensure:
1. **Tests Pass**: Run `pytest testing/tests/` and ensure all tests pass.
2. **Shell Scripts**: All bash/shell scripts must pass `shellcheck` with zero warnings.
3. **PKGBUILDs**: All modified PKGBUILDs must be validated using `namcap`.
4. **Formatting**: Python code must be formatted using `black`.

## 3. RFC Process for Architectural Changes

If you are proposing a significant architectural change (e.g., swapping systemd-boot for GRUB, changing the default filesystem, or adding a new core Daemon), you must first submit an RFC (Request for Comments) issue detailing the technical justification and fallback strategy before writing code.

## 4. Commit Message Standard

We follow Conventional Commits:
- `feat:` A new feature.
- `fix:` A bug fix.
- `docs:` Documentation only changes.
- `refactor:` Code changes that neither fix a bug nor add a feature.
- `test:` Adding missing tests.
- `chore:` Changes to the build process or auxiliary tools.

Example: `feat(installer): implement TPM2 auto-unlock enrollment`
