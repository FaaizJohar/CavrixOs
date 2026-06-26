# AI Subsystem Architecture

This document outlines the architecture for CavrixOS's optional local Artificial Intelligence runtime. The AI layer is an optional user-space service, completely decoupled from core operating system stability.

## 1. System Design

The subsystem operates as a layered stack:

1. **Operating System**: Arch Linux base.
2. **Desktop**: KDE Plasma (UI representation).
3. **AI Daemon (`cavrix-ai-daemon`)**: The Python orchestration layer.
4. **AI Runtime**: `ollama` (for executing GGUF models).

### 1.1 Hardware Detection
- **Current Implementation**: Scaffolded. The daemon (`ai/daemon/core/vram.py`) implements wrapper logic around `nvidia-smi` and `rocm-smi` to parse JSON outputs and calculate free VRAM in Megabytes.
- **Dependencies**: `nvidia-utils`, `rocm-smi-lib`.
- **Validation Status**: Python unit tests exist but have not been validated against diverse hardware configurations in CI.

### 1.2 Model Selection
- **Current Implementation**: Scaffolded. The daemon dynamically selects between `llama3`, `phi3`, or `qwen` depending on the VRAM thresholds calculated.
- **Validation Status**: Pending runtime integration.

## 2. API Interfaces

- **REST API**: Pending implementation.
- **D-Bus Interface**: Pending implementation. Currently, the GUI and CLI (`cavrix-ask`) interact directly with the Ollama HTTP socket (`127.0.0.1:11434`), bypassing proper system message bus integration.

## 3. Known Limitations & Technical Debt

- **Resource Limits**: The daemon does not currently enforce cgroups resource limits. If a user runs a model that exceeds available memory, it will trigger the Linux OOM killer, potentially crashing desktop applications.
- **Permissions**: The underlying runtime (`ollama`) runs as a global system service, accessible to any local user. No token-based authentication is currently implemented.
- **CPU Fallback**: If GPU VRAM is insufficient, the system falls back to CPU execution (`qwen`), which is not explicitly rate-limited and will heavily throttle overall system responsiveness.
