import subprocess
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt

class SetupWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        self.setStyleSheet("background-color: #09090B; color: #F8FAFC; font-family: 'Inter', sans-serif;")

        title = QLabel("System Setup")
        title.setStyleSheet("font-size: 28px; font-family: 'Space Grotesk', sans-serif; font-weight: bold;")
        layout.addWidget(title)

        # Update System Group
        update_group = QGroupBox("System Updates")
        update_group.setStyleSheet("QGroupBox { border: 1px solid #374151; border-radius: 8px; margin-top: 20px; font-weight: bold; }")
        update_layout = QVBoxLayout(update_group)
        
        update_desc = QLabel("Ensure your system is up to date with the latest packages and security patches.")
        update_desc.setStyleSheet("color: #94A3B8;")
        update_desc.setWordWrap(True)
        update_layout.addWidget(update_desc)
        
        self.btn_update = QPushButton("Update System")
        self.btn_update.setStyleSheet(self.button_style())
        self.btn_update.clicked.connect(self.run_update)
        update_layout.addWidget(self.btn_update)
        layout.addWidget(update_group)

        # Drivers Group
        driver_group = QGroupBox("Hardware Drivers")
        driver_group.setStyleSheet("QGroupBox { border: 1px solid #374151; border-radius: 8px; margin-top: 20px; font-weight: bold; }")
        driver_layout = QVBoxLayout(driver_group)
        
        driver_desc = QLabel("CavrixOS handles open-source drivers automatically. You can install proprietary drivers if needed (e.g. NVIDIA).")
        driver_desc.setStyleSheet("color: #94A3B8;")
        driver_desc.setWordWrap(True)
        driver_layout.addWidget(driver_desc)
        layout.addWidget(driver_group)

        layout.addStretch()

    def button_style(self):
        return """
            QPushButton {
                background-color: #2563EB;
                color: #F8FAFC;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """

    def run_update(self):
        # Open konsole to run pacman update
        try:
            subprocess.Popen(["konsole", "-e", "sudo pacman -Syu"])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not launch terminal: {str(e)}")
