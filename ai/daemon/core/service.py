import subprocess
import logging
from .vram import VRAMEstimator

logger = logging.getLogger(__name__)

class CavrixAIManager:
    """Manages the local Ollama LLM execution environments based on hardware constraints."""

    def __init__(self):
        self.gpu_info = VRAMEstimator.get_available_vram()

    def get_optimal_model(self) -> str:
        """Determines the best model to run based on available VRAM."""
        vendor = self.gpu_info["vendor"]
        vram = self.gpu_info["free_mb"]
        
        logger.info(f"System State: {vendor.upper()} with {vram}MB free VRAM.")
        
        if vendor != "cpu" and vram > 6000:
            return "llama3:8b-instruct-q4_K_M"
        elif vendor != "cpu" and vram > 4000:
            return "phi3:3.8b-mini-instruct-4k-fp16"
        else:
            logger.warning("Low VRAM or CPU-only detected. Falling back to tiny models.")
            return "qwen:0.5b"

    def start_daemon(self):
        """Starts the Ollama daemon safely."""
        logger.info("Starting Ollama background service...")
        try:
            # In production, this would communicate via D-Bus or systemctl
            subprocess.run(["systemctl", "start", "ollama"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to start Ollama: {e}")
            return False

    def preload_model(self):
        """Preloads the optimal model into memory."""
        model = self.get_optimal_model()
        logger.info(f"Preloading optimal model: {model}")
        try:
            # We use an empty completion request to force Ollama to load the model into VRAM
            subprocess.Popen(["ollama", "run", model, '""'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            logger.error(f"Failed to preload model: {e}")
