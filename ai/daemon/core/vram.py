import subprocess
import logging
import json

logger = logging.getLogger(__name__)

class VRAMEstimator:
    """Estimates available VRAM across Nvidia and AMD GPUs to route LLM execution."""
    
    @staticmethod
    def get_nvidia_vram() -> int:
        """Returns available NVIDIA VRAM in MB."""
        try:
            output = subprocess.check_output(
                ["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"],
                text=True
            )
            vram = int(output.strip().split('\n')[0])
            return vram
        except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
            return 0

    @staticmethod
    def get_amd_vram() -> int:
        """Returns available AMD VRAM in MB using rocm-smi."""
        try:
            output = subprocess.check_output(["rocm-smi", "--showmeminfo", "vram", "--json"], text=True)
            data = json.loads(output)
            # Find the first card
            for card, info in data.items():
                if "VRAM Total Memory (B)" in info and "VRAM Total Used Memory (B)" in info:
                    total = int(info["VRAM Total Memory (B)"])
                    used = int(info["VRAM Total Used Memory (B)"])
                    return (total - used) // (1024 * 1024)
            return 0
        except (subprocess.CalledProcessError, FileNotFoundError, ValueError, json.JSONDecodeError):
            return 0

    @staticmethod
    def get_available_vram() -> dict:
        """Returns the best available GPU and its free VRAM."""
        nv_vram = VRAMEstimator.get_nvidia_vram()
        amd_vram = VRAMEstimator.get_amd_vram()
        
        if nv_vram > amd_vram:
            return {"vendor": "nvidia", "free_mb": nv_vram}
        elif amd_vram > 0:
            return {"vendor": "amd", "free_mb": amd_vram}
        else:
            return {"vendor": "cpu", "free_mb": 0}
