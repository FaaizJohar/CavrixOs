import subprocess
import logging
import os
import json
import urllib.request
import urllib.error
from .vram import VRAMEstimator

# Setup structured observability logging
os.makedirs("/var/log/cavrixos", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("/var/log/cavrixos/ai-daemon.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("CavrixAI")

class CavrixAIManager:
    """
    Manages the local LLM runtime, enforcing strict resource limits via systemd cgroups
    to ensure desktop stability.
    """

    def __init__(self):
        self.gpu_info = VRAMEstimator.get_available_vram()
        self.api_url = "http://127.0.0.1:11434/api"

    def get_optimal_model(self) -> str:
        """Determines the best model to run based on available hardware constraints."""
        vendor = self.gpu_info["vendor"]
        vram = self.gpu_info["free_mb"]
        
        logger.info(f"System State detected: {vendor.upper()} GPU with {vram}MB free VRAM.")
        
        if vendor != "cpu" and vram > 6000:
            return "llama3:8b-instruct-q4_K_M"
        elif vendor != "cpu" and vram > 4000:
            return "phi3:3.8b-mini-instruct-4k-fp16"
        else:
            logger.warning("Low VRAM or CPU-only mode. Falling back to tiny model (Qwen 0.5B).")
            return "qwen:0.5b"

    def is_ollama_running(self) -> bool:
        """Polls the local API to check if the runtime is responsive."""
        try:
            req = urllib.request.Request(f"{self.api_url}/tags", method="GET")
            with urllib.request.urlopen(req, timeout=2) as response:
                return response.status == 200
        except (urllib.error.URLError, ConnectionResetError):
            return False

    def start_daemon(self) -> bool:
        """Starts the Ollama daemon inside a constrained systemd scope."""
        if self.is_ollama_running():
            logger.info("Ollama runtime is already active.")
            return True
            
        logger.info("Starting Ollama background service with cgroup limits...")
        try:
            # We enforce MemoryMax to prevent OOM killer from destroying KDE Plasma
            # We set MemoryMax to 80% of total system RAM or 12GB, whichever is lower
            # For simplicity in this implementation, we set a hard limit of 10G
            subprocess.run([
                "systemd-run", 
                "--scope", 
                "-p", "MemoryMax=10G", 
                "--unit=cavrix-ollama-runtime", 
                "systemctl", "start", "ollama"
            ], check=True)
            
            # Wait for socket to bind
            for _ in range(10):
                import time
                time.sleep(1)
                if self.is_ollama_running():
                    logger.info("Runtime successfully initialized and bound to port 11434.")
                    return True
                    
            logger.error("Runtime started but API did not become responsive.")
            return False
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to start bounded Ollama runtime: {e}")
            return False

    def preload_model(self) -> bool:
        """Preloads the optimal model into VRAM/RAM asynchronously."""
        model = self.get_optimal_model()
        logger.info(f"Preloading optimal model: {model}")
        try:
            # Generate a payload to pull the model if not present, or load it
            payload = json.dumps({"name": model}).encode('utf-8')
            req = urllib.request.Request(f"{self.api_url}/pull", data=payload, method="POST")
            req.add_header('Content-Type', 'application/json')
            
            # In production, we'd stream this response. For now, just trigger it.
            urllib.request.urlopen(req, timeout=5)
            logger.info(f"Model {model} requested successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to preload model {model}: {e}")
            return False
