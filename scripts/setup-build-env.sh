#!/bin/bash
# Setup Build Environment
set -e

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

echo "==> Installing build dependencies..."
pacman -S --needed --noconfirm archiso base-devel git squashfs-tools qemu-full qemu-desktop

echo "==> Configuring makepkg..."
sed -i 's/#MAKEFLAGS="-j2"/MAKEFLAGS="-j$(nproc)"/g' /etc/makepkg.conf
sed -i 's/COMPRESSZST=(zstd -c -z -q -)/COMPRESSZST=(zstd -c -z -q - -T0)/g' /etc/makepkg.conf

echo "==> Setup complete!"
