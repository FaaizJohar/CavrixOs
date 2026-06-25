#!/usr/bin/env python
import os
import sys
import json
from pathlib import Path

# Try to import archinstall, otherwise error
try:
    import archinstall
    from archinstall.lib.args import ArchConfigHandler
    from archinstall.lib.installer import Installer
    from archinstall.lib.profile.profiles_handler import profile_handler
    from archinstall.scripts.guided import perform_installation, show_menu
    from archinstall.lib.mirror.mirror_handler import MirrorListHandler
    from archinstall.lib.authentication.authentication_handler import AuthenticationHandler
    from archinstall.lib.applications.application_handler import ApplicationHandler
    from archinstall.lib.configuration import ConfigurationOutput
    from archinstall.lib.bootloader.utils import validate_bootloader_layout
    from archinstall.lib.log import error, debug, info
    from archinstall.tui.components import tui
except ImportError:
    print("Error: archinstall module not found. Are you running this in the CavrixOS live environment?")
    sys.exit(1)

# Import the custom CavrixOS profile
sys.path.append('/root')
try:
    from cavrixos_profile import CavrixOSProfile
    # Register the custom profile with archinstall
    profile_handler.register_profile(CavrixOSProfile())
except ImportError:
    print("Warning: cavrixos_profile.py not found in /root. Falling back to standard profiles.")


def load_default_config():
    config_path = Path('/root/cavrixos-config.json')
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    return {}


def main():
    info("Starting CavrixOS Installer...")

    # Initialize config handler with our custom defaults
    # We will pass the arguments to the archinstall config handler
    sys.argv.extend(['--config', '/root/cavrixos-config.json'])

    arch_config_handler = ArchConfigHandler()
    mirror_list_handler = MirrorListHandler(
        offline=arch_config_handler.args.offline,
        verbose=arch_config_handler.args.verbose,
    )

    if not arch_config_handler.args.silent:
        show_menu(arch_config_handler, mirror_list_handler)

    config = ConfigurationOutput(arch_config_handler.config)
    config.write_debug()
    config.save()

    if failure := validate_bootloader_layout(
        arch_config_handler.config.bootloader_config,
        arch_config_handler.config.disk_config,
    ):
        error(failure.description)
        return

    if not arch_config_handler.args.silent:
        res: bool = tui.run(config.confirm_config)
        if not res:
            debug('Installation aborted')
            return

    if arch_config_handler.config.disk_config:
        from archinstall.lib.disk.filesystem import FilesystemHandler
        from archinstall.lib.menu.util import delayed_warning
        from archinstall.lib.translationhandler import tr

        fs_handler = FilesystemHandler(arch_config_handler.config.disk_config)
        if not delayed_warning(tr('Starting device modifications in ')):
            return
        fs_handler.perform_filesystem_operations()

    perform_installation(
        arch_config_handler,
        mirror_list_handler,
        AuthenticationHandler(),
        ApplicationHandler(),
    )


if __name__ == '__main__':
    main()
