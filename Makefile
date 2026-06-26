# CavrixOS Master Build System
# Copyright (C) 2026 Cavrix Core Technologies
# SPDX-License-Identifier: GPL-3.0-only

SHELL := /bin/bash
.DEFAULT_GOAL := help

# ── Configuration ──────────────────────────────────────────────
ISO_NAME       := CavrixOS
ISO_VERSION    := $(shell date +%Y.%m.%d)
ARCH           := x86_64
OUT_DIR        := $(CURDIR)/build
WORK_DIR       := /tmp/cavrixos-build

# Repositories
REPO_BASE      := $(CURDIR)/repositories
REPOS          := cavrix-core cavrix-extra cavrix-ai
PKG_BASE       := $(CURDIR)/packages

# ISO Config
PROFILE_DIR    := $(CURDIR)/distribution
QEMU_MEM       := 4G
QEMU_CORES     := 4

# ── Colors ─────────────────────────────────────────────────────
BOLD   := $(shell tput bold 2>/dev/null)
CYAN   := $(shell tput setaf 6 2>/dev/null)
GREEN  := $(shell tput setaf 2 2>/dev/null)
YELLOW := $(shell tput setaf 3 2>/dev/null)
RED    := $(shell tput setaf 1 2>/dev/null)
RESET  := $(shell tput sgr0 2>/dev/null)

# ── Phony Targets ──────────────────────────────────────────────
.PHONY: help all packages $(REPOS) repo iso test test-efi test-secureboot clean

help: ## Show this help message
	@echo ""
	@echo "  $(BOLD)$(CYAN)CavrixOS Master Build System$(RESET)"
	@echo "  $(CYAN)──────────────────────────────$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-18s$(RESET) %s\n", $$1, $$2}'
	@echo ""

# ── Dependencies ───────────────────────────────────────────────
check-deps:
	@command -v mkarchiso >/dev/null || { echo "$(RED)✗ archiso missing$(RESET)"; exit 1; }
	@command -v makepkg >/dev/null || { echo "$(RED)✗ base-devel missing$(RESET)"; exit 1; }
	@command -v repo-add >/dev/null || { echo "$(RED)✗ pacman missing$(RESET)"; exit 1; }

# ── Packages ───────────────────────────────────────────────────
packages: $(REPOS) ## Build all packages across all repositories

$(REPOS): check-deps
	@echo "$(BOLD)$(CYAN)▸ Building Repository: $@$(RESET)"
	@mkdir -p "$(REPO_BASE)/$@"
	@for pkg_dir in $(PKG_BASE)/$@/*/; do \
		if [ -d "$$pkg_dir" ]; then \
			pkg_name=$$(basename "$$pkg_dir"); \
			echo "$(YELLOW)  ▸ Building $$pkg_name...$(RESET)"; \
			set -e; \
			cd "$$pkg_dir" && makepkg -sfi --noconfirm --nocheck; \
			cp -f *.pkg.tar.* "$(REPO_BASE)/$@/"; \
			cd "$(CURDIR)"; \
		fi \
	done
	@echo "$(GREEN)✓ Repository $@ built$(RESET)"

# ── Repository Generation ──────────────────────────────────────
repo: packages ## Generate pacman repository databases
	@echo "$(BOLD)$(CYAN)▸ Generating Repository Databases...$(RESET)"
	@for repo in $(REPOS); do \
		echo "$(YELLOW)  ▸ Generating $$repo.db...$(RESET)"; \
		cd "$(REPO_BASE)/$$repo" && repo-add "$$repo.db.tar.zst" *.pkg.tar.* 2>/dev/null || true; \
		cd "$(CURDIR)"; \
	done
	@echo "$(GREEN)✓ All repositories generated$(RESET)"

# ── ISO Build ──────────────────────────────────────────────────
iso: check-deps ## Build the bootable ISO
	@echo "$(BOLD)$(CYAN)▸ Building CavrixOS ISO (v$(ISO_VERSION))$(RESET)"
	@[ "$$(id -u)" -eq 0 ] || { echo "$(RED)✗ Must run as root$(RESET)"; exit 1; }
	@mkdir -p "$(OUT_DIR)" "$(WORK_DIR)"
	mkarchiso -v -w "$(WORK_DIR)" -o "$(OUT_DIR)" "$(PROFILE_DIR)"
	@cd "$(OUT_DIR)" && sha256sum *.iso > SHA256SUMS
	@echo "$(GREEN)✓ ISO built successfully at $(OUT_DIR)$(RESET)"

# ── Testing ────────────────────────────────────────────────────
test: ## Boot ISO in QEMU (Legacy BIOS)
	@ISO=$$(ls -t "$(OUT_DIR)"/*.iso | head -1); \
	qemu-system-x86_64 -enable-kvm -m $(QEMU_MEM) -smp $(QEMU_CORES) -boot d -cdrom "$$ISO" -vga virtio

test-efi: ## Boot ISO in QEMU (UEFI)
	@ISO=$$(ls -t "$(OUT_DIR)"/*.iso | head -1); \
	qemu-system-x86_64 -enable-kvm -m $(QEMU_MEM) -smp $(QEMU_CORES) -boot d -cdrom "$$ISO" -vga virtio -bios /usr/share/edk2/x64/OVMF.4m.fd

clean: ## Clean all artifacts
	@rm -rf "$(OUT_DIR)" "$(WORK_DIR)" "$(REPO_BASE)"
	@echo "$(GREEN)✓ Cleaned$(RESET)"
