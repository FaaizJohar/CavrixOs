import subprocess
import logging
import os
import time

logger = logging.getLogger(__name__)

class BtrfsManager:
    """
    Handles production-grade disk partitioning, Btrfs formatting, and Snapper-compliant 
    subvolume layouts for CavrixOS.
    """
    
    def __init__(self, disk: str, target_mount: str = "/mnt"):
        self.disk = disk
        self.target = target_mount
        self.efi_partition = f"{self.disk}1"
        self.root_partition = f"{self.disk}2"
        self.subvolumes = {
            "@": "/",
            "@home": "/home",
            "@snapshots": "/.snapshots",
            "@var_log": "/var/log",
            "@pkg": "/var/cache/pacman/pkg"
        }

    def _run_cmd(self, cmd: list) -> bool:
        """Executes a command and returns True if successful, False otherwise."""
        try:
            logger.debug(f"Executing: {' '.join(cmd)}")
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {' '.join(cmd)}")
            logger.error(f"Error output: {e.stderr.decode('utf-8').strip()}")
            return False

    def partition_disk(self) -> bool:
        """Wipes the target disk and creates a GPT EFI + Linux partition layout."""
        logger.info(f"Partitioning disk: {self.disk} (ALL DATA WILL BE DESTROYED)")
        
        # Unmount anything on the disk first
        self._run_cmd(["umount", "-q", "-f", f"{self.disk}*"])
        
        cmds = [
            ["parted", "-s", self.disk, "mklabel", "gpt"],
            ["parted", "-s", self.disk, "mkpart", "ESP", "fat32", "1MiB", "1025MiB"],
            ["parted", "-s", self.disk, "set", "1", "esp", "on"],
            ["parted", "-s", self.disk, "mkpart", "primary", "btrfs", "1025MiB", "100%"]
        ]
        
        for cmd in cmds:
            if not self._run_cmd(cmd):
                return False
                
        # Wait for device nodes to propagate
        time.sleep(2)
        return True

    def format_partitions(self, is_encrypted: bool = False) -> bool:
        """Formats the EFI partition as vfat and the root as Btrfs (or LUKS mapper)."""
        logger.info("Formatting partitions...")
        
        if not self._run_cmd(["mkfs.fat", "-F32", self.efi_partition]):
            return False
            
        root_target = self.root_partition
        if is_encrypted:
            root_target = "/dev/mapper/cavrix_crypt"
            logger.info("Encrypted root detected. Formatting mapped device as Btrfs.")
            
        if not self._run_cmd(["mkfs.btrfs", "-f", "-L", "CavrixOS", root_target]):
            return False
            
        return True

    def create_subvolumes(self, is_encrypted: bool = False) -> bool:
        """Mounts the top-level Btrfs volume and creates the optimal subvolume layout."""
        logger.info("Creating Btrfs subvolumes for Snapper...")
        root_target = "/dev/mapper/cavrix_crypt" if is_encrypted else self.root_partition
        
        os.makedirs("/mnt/btrfs_temp", exist_ok=True)
        if not self._run_cmd(["mount", "-t", "btrfs", root_target, "/mnt/btrfs_temp"]):
            return False
            
        for subvol in self.subvolumes.keys():
            logger.info(f"Creating subvolume: {subvol}")
            if not self._run_cmd(["btrfs", "subvolume", "create", f"/mnt/btrfs_temp/{subvol}"]):
                return False
                
        return self._run_cmd(["umount", "/mnt/btrfs_temp"])

    def mount_subvolumes(self, is_encrypted: bool = False) -> bool:
        """Mounts the subvolumes to the target installation directory with optimized flags."""
        logger.info(f"Mounting subvolumes to {self.target}...")
        root_target = "/dev/mapper/cavrix_crypt" if is_encrypted else self.root_partition
        mount_options = "rw,noatime,compress=zstd:1,space_cache=v2,ssd,discard=async"
        
        # Mount root (@) first
        if not self._run_cmd(["mount", "-o", f"{mount_options},subvol=@", root_target, self.target]):
            return False
            
        # Mount remaining subvolumes
        for subvol, mount_point in self.subvolumes.items():
            if subvol == "@":
                continue
            full_path = f"{self.target}{mount_point}"
            os.makedirs(full_path, exist_ok=True)
            if not self._run_cmd(["mount", "-o", f"{mount_options},subvol={subvol}", root_target, full_path]):
                return False
                
        # Mount EFI partition
        efi_path = f"{self.target}/efi"
        os.makedirs(efi_path, exist_ok=True)
        if not self._run_cmd(["mount", self.efi_partition, efi_path]):
            return False
            
        return True

    def configure_snapper(self) -> bool:
        """Sets up Snapper configuration within the chroot."""
        logger.info("Configuring Snapper for system rollbacks...")
        try:
            self._run_cmd(["arch-chroot", self.target, "snapper", "--no-dbus", "-c", "root", "create-config", "/"])
            self._run_cmd(["arch-chroot", self.target, "chmod", "a+rx", "/.snapshots"])
            return True
        except Exception as e:
            logger.error(f"Failed to configure Snapper: {e}")
            return False
