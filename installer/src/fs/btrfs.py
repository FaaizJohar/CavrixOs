import subprocess
import logging

logger = logging.getLogger(__name__)

class BtrfsManager:
    """Handles advanced BTRFS layouts and Snapper configurations."""
    
    def __init__(self, partition: str, target_mount: str):
        self.partition = partition
        self.target = target_mount
        self.subvolumes = {
            "@": "/",
            "@home": "/home",
            "@snapshots": "/.snapshots",
            "@var_log": "/var/log",
            "@pkg": "/var/cache/pacman/pkg"
        }

    def format_and_mount_root(self):
        """Formats the partition as BTRFS and mounts the top-level volume."""
        logger.info(f"Formatting {self.partition} as BTRFS...")
        subprocess.run(["mkfs.btrfs", "-f", self.partition], check=True)
        
        logger.info("Mounting BTRFS root to create subvolumes...")
        subprocess.run(["mount", "-t", "btrfs", self.partition, "/mnt/btrfs_temp"], check=True)

    def create_subvolumes(self):
        """Creates the optimal subvolume layout for Snapper rollbacks."""
        for subvol in self.subvolumes.keys():
            logger.info(f"Creating subvolume: {subvol}")
            subprocess.run(["btrfs", "subvolume", "create", f"/mnt/btrfs_temp/{subvol}"], check=True)
            
        subprocess.run(["umount", "/mnt/btrfs_temp"], check=True)

    def mount_subvolumes(self):
        """Mounts the subvolumes to the target installation directory with optimized flags."""
        mount_options = "rw,noatime,compress=zstd:1,space_cache=v2,ssd,discard=async"
        
        # Mount root first
        subprocess.run(["mount", "-o", f"{mount_options},subvol=@", self.partition, self.target], check=True)
        
        # Create mount points and mount the rest
        for subvol, mount_point in self.subvolumes.items():
            if subvol == "@":
                continue
                
            full_path = f"{self.target}{mount_point}"
            subprocess.run(["mkdir", "-p", full_path], check=True)
            subprocess.run(["mount", "-o", f"{mount_options},subvol={subvol}", self.partition, full_path], check=True)
            
    def configure_snapper(self):
        """Sets up Snapper and grub-btrfs/systemd-boot integration for rollbacks."""
        logger.info("Configuring Snapper for system rollbacks...")
        try:
            # Assumes arch-chroot is active or packages are installed
            subprocess.run(["arch-chroot", self.target, "snapper", "--no-dbus", "-c", "root", "create-config", "/"], check=True)
            # Adjust permissions to allow user access to snapshots if needed
            subprocess.run(["arch-chroot", self.target, "chmod", "a+rx", "/.snapshots"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to configure Snapper: {e}")
            return False
