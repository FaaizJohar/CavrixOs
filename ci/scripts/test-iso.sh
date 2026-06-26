#!/bin/bash
# Test ISO in QEMU Wrapper
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$DIR")"

echo "==> Triggering Makefile..."
cd "$ROOT_DIR"
make test
