import subprocess
import logging
import os

logger = logging.getLogger(__name__)

class LUKSManager:
    """
    Manages production LUKS2 encryption formatting, unlocking, and TPM2 enrollment.
    """
    
    def __init__(self, partition: str, mapper_name: str = "cavrix_crypt"):
        self.partition = partition
        self.mapper_name = mapper_name
        self.mapped_device = f"/dev/mapper/{self.mapper_name}"

    def has_tpm2(self) -> bool:
        """Checks if a TPM2 device is present and accessible on the host."""
        return os.path.exists("/dev/tpmrm0") or os.path.exists("/dev/tpm0")

    def encrypt_partition(self, password: str) -> bool:
        """Formats the partition with LUKS2 encryption using cryptsetup."""
        logger.info(f"Encrypting {self.partition} with LUKS2...")
        try:
            # -q forces yes on the warning, --type luks2 enforces format
            proc = subprocess.Popen(
                ["cryptsetup", "-q", "luksFormat", "--type", "luks2", self.partition], 
                stdin=subprocess.PIPE, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            stdout, stderr = proc.communicate(input=f"{password}\n".encode('utf-8'))
            
            if proc.returncode != 0:
                logger.error(f"cryptsetup luksFormat failed: {stderr.decode('utf-8').strip()}")
                return False
            return True
        except Exception as e:
            logger.error(f"Encryption exception: {e}")
            return False

    def open_partition(self, password: str) -> bool:
        """Opens the encrypted partition to the device mapper."""
        logger.info(f"Opening encrypted partition {self.partition} as {self.mapper_name}...")
        try:
            proc = subprocess.Popen(
                ["cryptsetup", "open", self.partition, self.mapper_name], 
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = proc.communicate(input=f"{password}\n".encode('utf-8'))
            
            if proc.returncode != 0:
                logger.error(f"cryptsetup open failed: {stderr.decode('utf-8').strip()}")
                return False
            return True
        except Exception as e:
            logger.error(f"Failed to open LUKS partition: {e}")
            return False

    def close_partition(self) -> bool:
        """Closes the mapped LUKS device."""
        logger.info(f"Closing LUKS device {self.mapper_name}...")
        try:
            subprocess.run(["cryptsetup", "close", self.mapper_name], check=True)
            return True
        except subprocess.CalledProcessError:
            logger.warning(f"Failed to close {self.mapper_name}. It might be busy.")
            return False

    def enroll_tpm2(self, password: str) -> bool:
        """Enrolls the LUKS key into the TPM2 chip via systemd-cryptenroll."""
        if not self.has_tpm2():
            logger.warning("No TPM2 device found. Skipping TPM enrollment.")
            return False
            
        logger.info("Enrolling LUKS key into TPM2...")
        try:
            # We must pass the password to cryptenroll to authorize the new enrollment
            env = os.environ.copy()
            env["PASSWORD"] = password
            
            proc = subprocess.Popen(
                ["systemd-cryptenroll", "--tpm2-device=auto", self.partition],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env
            )
            stdout, stderr = proc.communicate(input=f"{password}\n".encode('utf-8'))
            
            if proc.returncode != 0:
                logger.error(f"TPM2 enrollment failed: {stderr.decode('utf-8').strip()}")
                return False
                
            logger.info("TPM2 enrollment successful. System will auto-unlock on boot.")
            return True
        except Exception as e:
            logger.error(f"TPM2 enrollment exception: {e}")
            return False
