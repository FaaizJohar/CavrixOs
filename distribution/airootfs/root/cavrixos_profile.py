from typing import override
from archinstall.default_profiles.profile import Profile, ProfileType, GreeterType, DisplayServerType
from archinstall.lib.installer import Installer
from archinstall.lib.log import info


class CavrixOSProfile(Profile):
    def __init__(self) -> None:
        super().__init__(
            'CavrixOS Desktop',
            ProfileType.DesktopEnv,
            support_gfx_driver=True,
            display_server=DisplayServerType.Wayland,
        )

    @property
    @override
    def packages(self) -> list[str]:
        return [
            # Base Desktop
            'plasma-meta',
            'wayland',
            'xorg-xwayland',
            'sddm',

            # Audio
            'pipewire',
            'pipewire-pulse',
            'pipewire-alsa',
            'wireplumber',

            # Network & Bluetooth
            'networkmanager',
            'bluez',
            'bluez-utils',
            'firewalld',

            # Utilities & FS
            'btrfs-progs',
            'timeshift',
            'zram-generator',
            'flatpak',
            'discover',
            'git',
            'wget',
            'curl',
            'nano',
            'vim',
            'htop',

            # CavrixOS specific (from local repo)
            'cavrixos-branding',
            'cavrixos-desktop-config',
            'cavrixos-keyring',
            'cavrixos-mirrorlist'
        ]

    @property
    @override
    def services(self) -> list[str]:
        return [
            'NetworkManager',
            'bluetooth',
            'sddm',
            'firewalld',
            'fstrim.timer'
        ]

    @property
    @override
    def default_greeter_type(self) -> GreeterType:
        return GreeterType.Sddm

    @override
    def post_install(self, install_session: Installer) -> None:
        info("Running CavrixOS post-installation setup...")
        # Execute the bash script for system tuning and flatpak setup
        install_session.arch_chroot('/bin/bash -c "curl -sL file:///root/cavrixos_post_install.sh | bash"')
