from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class HomeWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        
        self.setStyleSheet("background-color: #09090B;")

        # Logo
        logo = QLabel()
        pixmap = QPixmap("/usr/share/pixmaps/cavrixos-logo.svg")
        if not pixmap.isNull():
            # Scale logo
            logo.setPixmap(pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo)

        # Welcome Text
        title = QLabel("Welcome to CavrixOS")
        title.setStyleSheet("color: #F8FAFC; font-size: 32px; font-family: 'Space Grotesk', sans-serif; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Your journey into a premium Linux experience begins here.")
        subtitle.setStyleSheet("color: #94A3B8; font-size: 16px; font-family: 'Inter', sans-serif;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
