#!/usr/bin/env python3
import sys
import os
import logging
from core.service import CavrixAIManager
from api import start_dbus_loop

logger = logging.getLogger("CavrixAI.Main")

def main():
    logger.info("Initializing Cavrix AI Daemon (Production Subsystem)...")
    
    # Ensure dependencies are met
    try:
        import dbus
        import gi
    except ImportError:
        logger.error("Required libraries missing. Ensure 'dbus-python' and 'python-gobject' are installed.")
        sys.exit(1)

    manager = CavrixAIManager()
    
    if manager.start_daemon():
        logger.info("Daemon active. Preloading models based on VRAM heuristics...")
        manager.preload_model()
        
        logger.info("Transferring control to D-Bus GLib Event Loop...")
        start_dbus_loop(manager)
    else:
        logger.error("Failed to initialize AI Subsystem. Ollama failed to start within memory constraints.")
        sys.exit(1)

if __name__ == "__main__":
    main()
