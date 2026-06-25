# CavrixOS Build System
# Copyright (C) 2024 Cavrix Core Technologies
# SPDX-License-Identifier: GPL-3.0-only

SHELL := /bin/bash
.DEFAULT_GOAL := help

# ── Configuration ──────────────────────────────────────────────
ISO_NAME       := CavrixOS
ISO_VERSION    := $(shell date +%Y.%m.%d)
ARCH           := x86_64
PROFILE_DIR    := $(CURDIR)/cavrixiso
WORK_DIR       := /tmp/cavrixos-build
OUT_DIR        := $(CURDIR)/build
REPO_DIR       := $(CURDIR)/repositories/pkgs
PKG_DIR        := $(CURDIR)/packages
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
.PHONY: help all iso packages repo clean clean-work test check-deps \
        check-root lint

# ── Help ───────────────────────────────────────────────────────
help: ## Show this help message
	@echo ""
	@echo "  $(BOLD)$(CYAN)CavrixOS Build System$(RESET)"
	@echo "  $(CYAN)─────────────────────$(RESET)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-18s$(RESET) %s\n", $$1, $$2}'
	@echo ""

# ── Dependency Checks ─────────────────────────────────────────
check-deps: ## Verify build dependencies are installed
	@echo "$(BOLD)$(CYAN)▸ Checking build dependencies...$(RESET)"
	@command -v mkarchiso  >/dev/null 2>&1 || { echo "$(RED)✗ archiso is not installed$(RESET)"; exit 1; }
	@command -v makepkg    >/dev/null 2>&1 || { echo "$(RED)✗ base-devel is not installed$(RESET)"; exit 1; }
	@command -v git        >/dev/null 2>&1 || { echo "$(RED)✗ git is not installed$(RESET)"; exit 1; }
	@command -v mksquashfs >/dev/null 2>&1 || { echo "$(RED)✗ squashfs-tools is not installed$(RESET)"; exit 1; }
	@echo "$(GREEN)✓ All dependencies satisfied$(RESET)"

check-root: ## Verify running as root (required for mkarchiso)
	@[ "$$(id -u)" -eq 0 ] || { echo "$(RED)✗ Must run as root (use sudo make iso)$(RESET)"; exit 1; }

# ── ISO Build ─────────────────────────────────────────────────
iso: check-deps check-root ## Build the CavrixOS ISO
	@echo ""
	@echo "$(BOLD)$(CYAN)╔══════════════════════════════════════════╗$(RESET)"
	@echo "$(BOLD)$(CYAN)║       Building CavrixOS ISO              ║$(RESET)"
	@echo "$(BOLD)$(CYAN)║       Version: $(ISO_VERSION)              ║$(RESET)"
	@echo "$(BOLD)$(CYAN)╚══════════════════════════════════════════╝$(RESET)"
	@echo ""
	@mkdir -p "$(OUT_DIR)"
	@echo "$(YELLOW)▸ Preparing work directory...$(RESET)"
	@rm -rf "$(WORK_DIR)"
	@mkdir -p "$(WORK_DIR)"
	@echo "$(YELLOW)▸ Running mkarchiso...$(RESET)"
	mkarchiso -v -w "$(WORK_DIR)" -o "$(OUT_DIR)" "$(PROFILE_DIR)"
	@echo ""
	@echo "$(YELLOW)▸ Generating checksums...$(RESET)"
	@cd "$(OUT_DIR)" && sha256sum *.iso > SHA256SUMS
	@echo ""
	@echo "$(GREEN)$(BOLD)✓ ISO built successfully!$(RESET)"
	@echo "  $(CYAN)Output: $(OUT_DIR)/$(RESET)"
	@ls -lh "$(OUT_DIR)"/*.iso 2>/dev/null || true

# ── Package Build ─────────────────────────────────────────────
packages: check-deps ## Build all custom packages
	@echo "$(BOLD)$(CYAN)▸ Building custom packages...$(RESET)"
	@mkdir -p "$(REPO_DIR)"
	@for pkg_dir in $(PKG_DIR)/*/; do \
		pkg_name=$$(basename "$$pkg_dir"); \
		echo "$(YELLOW)  ▸ Building $$pkg_name...$(RESET)"; \
		cd "$$pkg_dir" && makepkg -sfi --noconfirm && \
		cp -f *.pkg.tar.* "$(REPO_DIR)/" && \
		echo "$(GREEN)  ✓ $$pkg_name built$(RESET)" || \
		{ echo "$(RED)  ✗ $$pkg_name failed$(RESET)"; exit 1; }; \
		cd "$(CURDIR)"; \
	done
	@echo "$(GREEN)$(BOLD)✓ All packages built successfully$(RESET)"

# ── Repository ────────────────────────────────────────────────
repo: packages ## Build local package repository
	@echo "$(BOLD)$(CYAN)▸ Building package repository...$(RESET)"
	@mkdir -p "$(REPO_DIR)"
	@repo-add "$(REPO_DIR)/cavrixos.db.tar.zst" "$(REPO_DIR)"/*.pkg.tar.*
	@echo "$(GREEN)$(BOLD)✓ Repository built at $(REPO_DIR)$(RESET)"

# ── Full Pipeline ─────────────────────────────────────────────
all: packages repo iso ## Full build pipeline: packages → repo → iso
	@echo ""
	@echo "$(GREEN)$(BOLD)════════════════════════════════════════════$(RESET)"
	@echo "$(GREEN)$(BOLD)  CavrixOS build complete!$(RESET)"
	@echo "$(GREEN)$(BOLD)════════════════════════════════════════════$(RESET)"

# ── Testing ───────────────────────────────────────────────────
test: ## Boot the ISO in QEMU for testing
	@echo "$(BOLD)$(CYAN)▸ Launching CavrixOS in QEMU...$(RESET)"
	@ISO=$$(ls -t "$(OUT_DIR)"/*.iso 2>/dev/null | head -1); \
	if [ -z "$$ISO" ]; then \
		echo "$(RED)✗ No ISO found in $(OUT_DIR)/. Run 'make iso' first.$(RESET)"; \
		exit 1; \
	fi; \
	echo "$(CYAN)  Using: $$ISO$(RESET)"; \
	qemu-system-x86_64 \
		-enable-kvm \
		-m $(QEMU_MEM) \
		-smp $(QEMU_CORES) \
		-boot d \
		-cdrom "$$ISO" \
		-drive file=/tmp/cavrixos-test.qcow2,if=virtio,format=qcow2,size=40G \
		-device virtio-vga \
		-device virtio-net-pci,netdev=net0 \
		-netdev user,id=net0 \
		-bios /usr/share/edk2/x64/OVMF.4m.fd \
		-display gtk

# ── Linting ───────────────────────────────────────────────────
lint: ## Lint shell scripts and Python files
	@echo "$(BOLD)$(CYAN)▸ Linting...$(RESET)"
	@echo "$(YELLOW)  ▸ Shell scripts$(RESET)"
	@shellcheck scripts/*.sh 2>/dev/null && echo "$(GREEN)  ✓ Shell OK$(RESET)" || true
	@echo "$(YELLOW)  ▸ Python files$(RESET)"
	@python -m py_compile cavrixinstall/cavrixos_profile.py 2>/dev/null && echo "$(GREEN)  ✓ Python OK$(RESET)" || true
	@echo "$(YELLOW)▸ Validating JSON config...$(RESET)"
	@python -m json.tool cavrixinstall/cavrixos_config.json >/dev/null 2>&1 && echo "$(GREEN)  ✓ JSON OK$(RESET)" || true

# ── Cleanup ───────────────────────────────────────────────────
clean: ## Remove build artifacts and work directory
	@echo "$(BOLD)$(CYAN)▸ Cleaning build artifacts...$(RESET)"
	@rm -rf "$(OUT_DIR)"/*.iso "$(OUT_DIR)"/SHA256SUMS
	@rm -rf "$(WORK_DIR)"
	@rm -rf "$(REPO_DIR)"
	@for pkg_dir in $(PKG_DIR)/*/; do \
		rm -rf "$$pkg_dir"/src "$$pkg_dir"/pkg "$$pkg_dir"/*.pkg.tar.*; \
	done
	@echo "$(GREEN)✓ Clean$(RESET)"

clean-work: ## Remove only the work directory (keep ISO)
	@rm -rf "$(WORK_DIR)"
	@echo "$(GREEN)✓ Work directory cleaned$(RESET)"
