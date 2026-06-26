import subprocess
import logging

logger = logging.getLogger(__name__)

class HardwareDetector:
    """Detects system hardware to automatically provision the correct drivers."""
    
    @staticmethod
    def get_gpu_vendor() -> str:
        """Uses lspci to determine the primary GPU vendor."""
        try:
            output = subprocess.check_output("lspci | grep -i vga", shell=True, text=True).lower()
            if "nvidia" in output:
                return "nvidia"
            elif "amd" in output or "radeon" in output:
                return "amd"
            elif "intel" in output:
                return "intel"
            return "generic"
        except subprocess.CalledProcessError:
            logger.warning("Failed to detect GPU vendor. Falling back to generic.")
            return "generic"

    @staticmethod
    def get_cpu_vendor() -> str:
        """Determines CPU vendor for microcode installation."""
        try:
            with open("/proc/cpuinfo", "r") as f:
                content = f.read().lower()
                if "authenticamd" in content:
                    return "amd-ucode"
                elif "genuineintel" in content:
                    return "intel-ucode"
            return ""
        except FileNotFoundError:
            return ""

    @staticmethod
    def get_required_packages() -> list:
        """Returns a list of Arch packages required for the detected hardware."""
        packages = []
        gpu = HardwareDetector.get_gpu_vendor()
        cpu = HardwareDetector.get_cpu_vendor()
        
        if cpu:
            packages.append(cpu)
            
        if gpu == "nvidia":
            packages.extend(["nvidia-open-dkms", "nvidia-utils", "egl-wayland"])
        elif gpu == "amd":
            packages.extend(["vulkan-radeon", "xf86-video-amdgpu"])
        elif gpu == "intel":
            packages.extend(["vulkan-intel"])
            
        return packages
