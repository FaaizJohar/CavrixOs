import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt6.QtCore import Qt

class CavrixDriverManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cavrix Driver Manager")
        self.resize(600, 400)
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e24; }
            QLabel { color: #ffffff; font-family: 'Inter'; font-size: 16px; }
            QPushButton { 
                background-color: #2563eb; 
                color: #ffffff; 
                border-radius: 8px; 
                padding: 10px; 
                font-family: 'Inter'; 
                font-weight: bold;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.status_label = QLabel("Scanning hardware...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        self.install_btn = QPushButton("Auto-Install Recommended Drivers")
        self.install_btn.clicked.connect(self.install_drivers)
        layout.addWidget(self.install_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.scan_hardware()

    def scan_hardware(self):
        """Uses lspci to detect GPU and recommend drivers."""
        try:
            output = subprocess.check_output("lspci | grep -i vga", shell=True, text=True).lower()
            if "nvidia" in output:
                self.status_label.setText("NVIDIA GPU Detected.\nRecommended: nvidia-open-dkms")
            elif "amd" in output or "radeon" in output:
                self.status_label.setText("AMD GPU Detected.\nRecommended: vulkan-radeon")
            elif "intel" in output:
                self.status_label.setText("Intel GPU Detected.\nRecommended: vulkan-intel")
            else:
                self.status_label.setText("Generic/Unknown GPU Detected.")
        except Exception:
            self.status_label.setText("Failed to scan hardware.")

    def install_drivers(self):
        self.status_label.setText("Installing drivers... (Requires Polkit authentication)")
        # In production, this would use pkexec pacman -S
        # subprocess.Popen(["pkexec", "pacman", "-S", "nvidia-open-dkms"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CavrixDriverManager()
    window.show()
    sys.exit(app.exec())
