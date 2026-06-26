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
            color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #ffffff, stop:1 #a0a0a0);
            font-size: 42px;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 800;
            letter-spacing: -1.5px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("The World's Most Advanced AI-Powered Operating System.")
        subtitle.setStyleSheet("""
            color: rgba(255, 255, 255, 160);
            font-size: 18px;
            font-family: 'Inter', sans-serif;
            font-weight: 400;
            letter-spacing: 0.5px;
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
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(37, 99, 235, 255), stop:1 rgba(79, 70, 229, 255));
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 40);
                border-radius: 14px;
                padding: 14px 36px;
                font-family: 'Inter', sans-serif;
                font-size: 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(59, 130, 246, 255), stop:1 rgba(99, 102, 241, 255));
                border: 1px solid rgba(255, 255, 255, 80);
            }
            QPushButton:pressed {
                background-color: rgba(29, 78, 216, 255);
            }
        """)
        btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)
