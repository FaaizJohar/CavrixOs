#!/usr/bin/env python3
import time
import logging
from core.service import CavrixAIManager

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def main():
    logger.info("Initializing Cavrix AI Daemon (Phase 3 Architecture)...")
    
    manager = CavrixAIManager()
    
    if manager.start_daemon():
        logger.info("Daemon active. Preloading models based on VRAM heuristics...")
        manager.preload_model()
        
        # Placeholder for REST API / D-Bus event loop
        logger.info("Entering D-Bus wait state... (Mocked)")
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            logger.info("Daemon shutting down.")
    else:
        logger.error("Failed to initialize AI Subsystem.")

if __name__ == "__main__":
    main()
