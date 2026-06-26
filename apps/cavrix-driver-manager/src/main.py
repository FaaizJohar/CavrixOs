import sys
import logging
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QTextEdit
from PyQt6.QtCore import Qt, QProcess

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("CavrixDriverManager")

class CavrixDriverManager(QMainWindow):
    """
    GUI utility to detect and install proprietary and open-source hardware drivers.
    Utilizes QProcess to prevent the main UI thread from freezing during long pacman operations.
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cavrix Driver Manager")
        self.resize(650, 500)
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e24; }
            QLabel { color: #ffffff; font-family: 'Inter'; font-size: 16px; margin: 10px; }
            QTextEdit { background-color: #2b2b36; color: #a1a1aa; border: 1px solid #3f3f46; font-family: 'JetBrains Mono'; }
            QPushButton { 
                background-color: #2563eb; 
                color: #ffffff; 
                border-radius: 6px; 
                padding: 12px; 
                font-family: 'Inter'; 
                font-weight: bold;
            }
            QPushButton:disabled { background-color: #3f3f46; color: #71717a; }
        """)

        self.recommended_packages = []
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.status_label = QLabel("Scanning hardware buses...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        self.install_btn = QPushButton("Install Recommended Drivers")
        self.install_btn.setEnabled(False)
        self.install_btn.clicked.connect(self.install_drivers)
        layout.addWidget(self.install_btn)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        # Setup asynchronous processes
        self.scan_process = QProcess(self)
        self.scan_process.finished.connect(self.handle_scan_result)
        
        self.install_process = QProcess(self)
        self.install_process.readyReadStandardOutput.connect(self.handle_install_output)
        self.install_process.readyReadStandardError.connect(self.handle_install_error)
        self.install_process.finished.connect(self.handle_install_finished)

        self.start_hardware_scan()

    def start_hardware_scan(self):
        logger.info("Initiating hardware scan via lspci...")
        self.scan_process.start("sh", ["-c", "lspci | grep -i vga"])

    def handle_scan_result(self, exit_code, exit_status):
        if exit_code != 0:
            self.status_label.setText("Failed to scan PCI bus. Are pciutils installed?")
            return
            
        output = self.scan_process.readAllStandardOutput().data().decode('utf-8').lower()
        logger.info(f"Scan result: {output.strip()}")
        
        if "nvidia" in output:
            self.status_label.setText("NVIDIA GPU Detected.\nRecommended: nvidia-open-dkms, egl-wayland")
            self.recommended_packages = ["nvidia-open-dkms", "nvidia-utils", "egl-wayland"]
            self.install_btn.setEnabled(True)
        elif "amd" in output or "radeon" in output:
            self.status_label.setText("AMD GPU Detected.\nRecommended: vulkan-radeon, xf86-video-amdgpu")
            self.recommended_packages = ["vulkan-radeon", "xf86-video-amdgpu"]
            self.install_btn.setEnabled(True)
        elif "intel" in output:
            self.status_label.setText("Intel GPU Detected.\nRecommended: vulkan-intel")
            self.recommended_packages = ["vulkan-intel"]
            self.install_btn.setEnabled(True)
        else:
            self.status_label.setText("Generic/Unknown GPU Detected. No proprietary drivers needed.")

    def install_drivers(self):
        self.install_btn.setEnabled(False)
        self.status_label.setText("Waiting for Polkit authorization...")
        self.log_output.append(">>> Starting installation...\n")
        
        cmd = ["pkexec", "pacman", "-S", "--noconfirm"] + self.recommended_packages
        logger.info(f"Executing: {' '.join(cmd)}")
        self.install_process.start(cmd[0], cmd[1:])

    def handle_install_output(self):
        data = self.install_process.readAllStandardOutput().data().decode('utf-8')
        self.log_output.append(data.strip())
        
    def handle_install_error(self):
        data = self.install_process.readAllStandardError().data().decode('utf-8')
        self.log_output.append(f"[ERROR] {data.strip()}")
        
    def handle_install_finished(self, exit_code, exit_status):
        if exit_code == 0:
            self.status_label.setText("Drivers installed successfully. Reboot recommended.")
            self.log_output.append("\n>>> Installation Complete.")
        else:
            self.status_label.setText("Installation failed. Check logs.")
            self.install_btn.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CavrixDriverManager()
    window.show()
    sys.exit(app.exec())
