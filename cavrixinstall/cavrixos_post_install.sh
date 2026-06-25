#!/bin/bash
# CavrixOS Post-Installation Setup Script
# Runs inside the arch-chroot during installation

set -e

echo "==> Configuring ZRAM"
cat <<EOF > /etc/systemd/zram-generator.conf
[zram0]
zram-size = ram / 2
compression-algorithm = zstd
swap-priority = 100
fs-type = swap
EOF

echo "==> Applying sysctl performance tweaks"
cat <<EOF > /etc/sysctl.d/99-cavrixos.conf
# CavrixOS Performance Tunings
vm.swappiness = 100
vm.vfs_cache_pressure = 50
vm.dirty_ratio = 10
vm.dirty_background_ratio = 5
kernel.sysrq = 1
net.ipv4.tcp_fastopen = 3
EOF

echo "==> Configuring Firewall defaults"
# Ensure firewalld defaults to a safe zone (public)
firewall-offline-cmd --set-default-zone=public

echo "==> Setting up Flatpak Remotes"
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo

echo "==> Setting SDDM Theme"
cat <<EOF > /etc/sddm.conf.d/cavrixos.conf
[Theme]
Current=cavrixos-sddm
EOF

echo "==> Setup complete!"
