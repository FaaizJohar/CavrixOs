import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt6.QtCore import Qt

class CavrixSettings(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cavrix Settings")
        self.resize(600, 400)
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e24; }
            QLabel { color: #ffffff; font-family: 'Inter'; font-size: 16px; }
            QPushButton { 
                background-color: #4f46e5; 
                color: #ffffff; 
                border-radius: 8px; 
                padding: 10px; 
                font-family: 'Inter'; 
                font-weight: bold;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.status_label = QLabel("CavrixOS Core System Settings")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        self.zram_btn = QPushButton("Optimize ZRAM Performance")
        self.zram_btn.clicked.connect(self.optimize_zram)
        layout.addWidget(self.zram_btn)

        self.layout_btn = QPushButton("Reset Plasma Layout to Cavrix Default")
        self.layout_btn.clicked.connect(self.reset_layout)
        layout.addWidget(self.layout_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def optimize_zram(self):
        self.status_label.setText("Applying aggressive ZRAM swappiness... (Requires Polkit)")
        # subprocess.Popen(["pkexec", "sysctl", "vm.swappiness=150"])

    def reset_layout(self):
        self.status_label.setText("Resetting KDE Plasma layout...")
        # subprocess.Popen(["qdbus", "org.kde.plasmashell", "/PlasmaShell", "org.kde.PlasmaShell.evaluateScript", "..."])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CavrixSettings()
    window.show()
    sys.exit(app.exec())
