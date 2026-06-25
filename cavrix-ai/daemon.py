import sys
import time
from threading import Thread

# In a real environment, this would use a global hotkey library like `keyboard` or bind via KDE shortcuts.
# For now, it's a simple daemon that keeps the app alive.

def start_daemon():
    print("Cavrix AI Daemon Started. Listening for events...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Daemon exiting.")

if __name__ == "__main__":
    # Start background listener
    daemon_thread = Thread(target=start_daemon, daemon=True)
    daemon_thread.start()
    
    # Launch UI
    try:
        from PyQt6.QtWidgets import QApplication
        from ui.chat_window import AIChatWindow
        app = QApplication(sys.argv)
        window = AIChatWindow()
        # Keep window hidden until hotkey is pressed (mocked by just showing it for now)
        window.show()
        sys.exit(app.exec())
    except ImportError:
        print("PyQt6 not installed. Running daemon only.")
        while True:
            time.sleep(1)
