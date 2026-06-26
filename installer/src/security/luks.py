import subprocess
import logging
import os

logger = logging.getLogger(__name__)

class LUKSManager:
    """Manages LUKS2 encryption and TPM2 auto-unlocking for root filesystems."""
    
    def __init__(self, partition: str, mapper_name: str = "cavrix_crypt"):
        self.partition = partition
        self.mapper_name = mapper_name
        self.mapped_device = f"/dev/mapper/{self.mapper_name}"

    def has_tpm2(self) -> bool:
        """Checks if a TPM2 device is present on the system."""
        return os.path.exists("/dev/tpmrm0") or os.path.exists("/dev/tpm0")

    def encrypt_partition(self, password: str) -> bool:
        """Formats the partition with LUKS2 encryption."""
        logger.info(f"Encrypting {self.partition} with LUKS2...")
        try:
            # We use echo to pass the password to cryptsetup
            proc = subprocess.Popen(["cryptsetup", "-q", "luksFormat", "--type", "luks2", self.partition], 
                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            proc.communicate(input=password.encode())
            if proc.returncode != 0:
                return False
            return True
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            return False

    def open_partition(self, password: str) -> bool:
        """Opens the encrypted partition."""
        logger.info(f"Opening encrypted partition {self.partition}...")
        try:
            proc = subprocess.Popen(["cryptsetup", "open", self.partition, self.mapper_name], 
                                    stdin=subprocess.PIPE)
            proc.communicate(input=password.encode())
            return proc.returncode == 0
        except Exception as e:
            logger.error(f"Failed to open LUKS partition: {e}")
            return False

    def enroll_tpm2(self):
        """Enrolls the LUKS key into the TPM2 chip via systemd-cryptenroll."""
        if not self.has_tpm2():
            logger.warning("No TPM2 device found. Skipping TPM enrollment.")
            return False
            
        logger.info("Enrolling LUKS key into TPM2...")
        try:
            subprocess.run(["systemd-cryptenroll", "--tpm2-device=auto", self.partition], check=True)
            logger.info("TPM2 enrollment successful. System will auto-unlock on boot.")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"TPM2 enrollment failed: {e}")
            return False
