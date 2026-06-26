from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


class HomeWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(24)

        # Transparent background so the main.py glassmorphism shows through
        self.setStyleSheet("background-color: transparent;")

        # Logo
        logo = QLabel()
        pixmap = QPixmap("/usr/share/pixmaps/cavrixos-logo.svg")
        if not pixmap.isNull():
            # Scale logo and make it smooth
            logo.setPixmap(pixmap.scaled(
                180, 180,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo)

        # Welcome Text with Apple-like Typography
        title = QLabel("Welcome to Cavrix AI")
        title.setStyleSheet("""
            color: #ffffff;
            font-size: 38px;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            letter-spacing: -1px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("The World's First AI-Powered Operating System.")
        subtitle.setStyleSheet("""
            color: rgba(255, 255, 255, 140);
            font-size: 16px;
            font-family: 'Inter', sans-serif;
            font-weight: 400;
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        # Get Started Button
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn = QPushButton("Get Started")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(37, 99, 235, 255); /* Cavrix Blue */
                color: #ffffff;
                border: none;
                border-radius: 12px;
                padding: 12px 32px;
                font-family: 'Inter', sans-serif;
                font-size: 15px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: rgba(59, 130, 246, 255);
            }
            QPushButton:pressed {
                background-color: rgba(29, 78, 216, 255);
            }
        """)
        btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)
