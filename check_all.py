import urllib.request
import json
import sys

pkgs = """
base
linux-zen
linux-zen-headers
linux-firmware
mkinitcpio
amd-ucode
intel-ucode
archinstall
arch-install-scripts
btrfs-progs
dosfstools
e2fsprogs
exfatprogs
f2fs-tools
ntfs-3g
xfsprogs
mtools
networkmanager
iwd
wpa_supplicant
dhclient
bind
openssh
pipewire
pipewire-pulse
pipewire-alsa
wireplumber
mesa
vulkan-radeon
vulkan-intel
nvidia-open-dkms
nvidia-utils
bluez
bluez-utils
git
vim
nano
htop
wget
curl
rsync
bash-completion
zsh
zsh-completions
terminus-font
sudo
pacman-contrib
reflector
zram-generator
plasma-meta
sddm
konsole
dolphin
firefox
xorg-server
xorg-xwayland
wayland
papirus-icon-theme
kvantum
inter-font
ttf-jetbrains-mono
ttf-cascadia-code
python-pyqt6
appmenu-gtk-module
breeze-gtk
plasma-browser-integration
ollama
""".strip().split('\n')

missing = []

for pkg in pkgs:
    url = f"https://archlinux.org/packages/search/json/?name={pkg}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            if not data.get('results'):
                missing.append(pkg)
                print(f"NOT FOUND: {pkg}")
    except Exception as e:
        print(f"Error checking {pkg}: {e}")

print(f"Missing total: {missing}")
