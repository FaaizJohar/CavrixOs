import subprocess
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QHBoxLayout
from PyQt6.QtCore import Qt

class SetupWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(25)
        
        self.setStyleSheet("background-color: transparent; font-family: 'Inter', sans-serif;")

        title = QLabel("System Configuration")
        title.setStyleSheet("""
            color: #ffffff;
            font-size: 32px; 
            font-family: 'Space Grotesk', sans-serif; 
            font-weight: 700;
            letter-spacing: -0.5px;
        """)
        layout.addWidget(title)

        # Update Card
        layout.addWidget(self.create_card(
            "System Updates",
            "Keep your OS secure and up-to-date with the latest rolling release packages.",
            "Update Now",
            self.run_update
        ))

        # Drivers Card
        layout.addWidget(self.create_card(
            "Hardware Drivers",
            "CavrixOS automatically configures open-source drivers. Install proprietary drivers if needed.",
            "Manage Drivers",
            None
        ))

        layout.addStretch()

    def create_card(self, title, desc, btn_text, callback):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 10);
                border: 1px solid rgba(255, 255, 255, 20);
                border-radius: 12px;
            }
        """)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)

        text_layout = QVBoxLayout()
        t_label = QLabel(title)
        t_label.setStyleSheet("color: #ffffff; font-size: 18px; font-weight: 600; border: none; background: transparent;")
        
        d_label = QLabel(desc)
        d_label.setStyleSheet("color: rgba(255, 255, 255, 140); font-size: 14px; border: none; background: transparent;")
        d_label.setWordWrap(True)
        
        text_layout.addWidget(t_label)
        text_layout.addWidget(d_label)
        layout.addLayout(text_layout)

        btn = QPushButton(btn_text)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 20);
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 30);
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 35);
            }
        """)
        if callback:
            btn.clicked.connect(callback)
        
        layout.addWidget(btn)
        return frame

    def run_update(self):
        try:
            subprocess.Popen(["konsole", "-e", "sudo pacman -Syu"])
        except Exception:
            pass
