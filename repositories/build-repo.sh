#!/bin/bash
# Local Repository Builder
set -e

REPO_DIR="pkgs"
DB_NAME="cavrixos.db.tar.zst"

cd "$(dirname "${BASH_SOURCE[0]}")"
mkdir -p "$REPO_DIR"

echo "==> Adding packages to repository..."
repo-add "${REPO_DIR}/${DB_NAME}" "${REPO_DIR}"/*.pkg.tar.*

echo "==> Repository built successfully."
