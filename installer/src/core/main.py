import sys
import logging
import subprocess
import os

from ..hardware.detector import HardwareDetector
from ..boot.uki import UKIManager
from ..fs.btrfs import BtrfsManager
from ..security.luks import LUKSManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("CavrixInstall")

class CavrixInstaller:
    """Orchestrates the entire CavrixOS installation process."""
    
    def __init__(self, target_disk: str, use_luks: bool = False, luks_password: str = ""):
        self.target_disk = target_disk
        self.use_luks = use_luks
        self.luks_password = luks_password
        self.mount_point = "/mnt"

    def _run_cmd(self, cmd: list) -> bool:
        try:
            logger.debug(f"Executing: {' '.join(cmd)}")
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {' '.join(cmd)}")
            logger.error(f"Error output: {e.stderr.decode('utf-8').strip()}")
            return False

    def get_base_packages(self) -> list:
        return [
            "base", "linux-zen", "linux-firmware", "btrfs-progs", "nano",
            "networkmanager", "sudo", "efibootmgr", "pipewire", "pipewire-pulse",
            "plasma-meta", "sddm", "konsole", "wayland",
            "python-pyqt6", "python-gobject", "dbus-python", "polkit-kde-agent",
            "cavrix-welcome", "cavrix-ai", "cavrixos-branding", "cavrixos-desktop-config"
        ]

    def install(self) -> bool:
        logger.info("Starting CavrixOS Installation...")
        
        # 1. Disk & Filesystem
        btrfs = BtrfsManager(self.target_disk, self.mount_point)
        if not btrfs.partition_disk():
            return False
            
        if self.use_luks:
            luks = LUKSManager(btrfs.root_partition)
            if not luks.encrypt_partition(self.luks_password):
                return False
            if not luks.open_partition(self.luks_password):
                return False
                
        if not btrfs.format_partitions(is_encrypted=self.use_luks):
            return False
        if not btrfs.create_subvolumes(is_encrypted=self.use_luks):
            return False
        if not btrfs.mount_subvolumes(is_encrypted=self.use_luks):
            return False

        # 2. Package Installation (pacstrap)
        packages = self.get_base_packages()
        hw_packages = HardwareDetector.get_required_packages()
        logger.info(f"Detected hardware packages: {hw_packages}")
        packages.extend(hw_packages)
        
        logger.info(f"Installing base system... (pacstrap)")
        if not self._run_cmd(["pacstrap", "-K", self.mount_point] + packages):
            return False

        # 3. fstab generation
        logger.info("Generating fstab...")
        try:
            with open(f"{self.mount_point}/etc/fstab", "w") as f:
                subprocess.run(["genfstab", "-U", self.mount_point], stdout=f, check=True)
        except subprocess.CalledProcessError:
            logger.error("genfstab failed.")
            return False

        # 4. System Configuration (chroot)
        logger.info("Configuring system internals (locale, hostname, initramfs)...")
        self._run_cmd(["arch-chroot", self.mount_point, "ln", "-sf", "/usr/share/zoneinfo/UTC", "/etc/localtime"])
        self._run_cmd(["arch-chroot", self.mount_point, "hwclock", "--systohc"])
        
        with open(f"{self.mount_point}/etc/locale.gen", "w") as f:
            f.write("en_US.UTF-8 UTF-8\n")
        self._run_cmd(["arch-chroot", self.mount_point, "locale-gen"])
        with open(f"{self.mount_point}/etc/locale.conf", "w") as f:
            f.write("LANG=en_US.UTF-8\n")
        with open(f"{self.mount_point}/etc/hostname", "w") as f:
            f.write("cavrixos\n")
            
        # Enable essential services
        self._run_cmd(["arch-chroot", self.mount_point, "systemctl", "enable", "NetworkManager"])
        self._run_cmd(["arch-chroot", self.mount_point, "systemctl", "enable", "sddm"])

        # 5. Bootloader & UKI
        uki = UKIManager(self.mount_point)
        if not uki.install_systemd_boot():
            return False
        if not uki.write_loader_conf():
            return False
            
        # Mock UUID for now - in production, parse `blkid`
        root_uuid = "00000000-0000-0000-0000-000000000000"
        if not uki.generate_cmdline(root_uuid, is_encrypted=self.use_luks):
            return False
        if not uki.configure_mkinitcpio_uki("linux-zen"):
            return False
            
        # Add encrypt hook if needed
        if self.use_luks:
            # We would modify /etc/mkinitcpio.conf here to add 'encrypt' before 'filesystems'
            pass
            
        if not uki.generate_ukis():
            return False

        # 6. Finalization
        logger.info("CavrixOS installation completed successfully.")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: cavrixos-installer <disk> [use_luks] [password]")
        sys.exit(1)
        
    disk = sys.argv[1]
    use_luks = len(sys.argv) > 2 and sys.argv[2].lower() == "true"
    password = sys.argv[3] if use_luks and len(sys.argv) > 3 else ""
    
    installer = CavrixInstaller(disk, use_luks, password)
    if not installer.install():
        logger.error("Installation failed.")
        sys.exit(1)
