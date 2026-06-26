#!/bin/bash
# CavrixOS Post-Installation Setup Script
# Runs inside the arch-chroot during installation

set -e

echo "==> Configuring ZRAM"
cat <<EOF > /etc/systemd/zram-generator.conf
[zram0]
zram-size = ram * 1.5
compression-algorithm = zstd
swap-priority = 100
fs-type = swap
EOF

echo "==> Applying sysctl performance tweaks"
cat <<EOF > /etc/sysctl.d/99-cavrixos.conf
# Enable aggressive swap for ZRAM
vm.swappiness = 150
vm.page-cluster = 0
vm.watermark_scale_factor = 125
vm.dirty_ratio = 10
vm.dirty_background_ratio = 5
kernel.sysrq = 1
net.ipv4.tcp_fastopen = 3
EOF

echo "==> Configuring Firewall defaults"
# Ensure firewalld defaults to a safe zone (public)
firewall-offline-cmd --set-default-zone=public

echo "==> Disabling KDE Bloat (Baloo)"
mkdir -p /etc/skel/.config
cat <<EOF > /etc/skel/.config/baloofilerc
[Basic Settings]
Indexing-Enabled=false
EOF

echo "==> Setting up Flatpak Remotes"
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo

echo "==> Enabling Multilib for Windows App Support (Wine)"
sed -i "/\[multilib\]/,/Include/"'s/^#//' /etc/pacman.conf

echo "==> Setup complete!"
