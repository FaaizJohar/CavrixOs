import subprocess
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QGridLayout, QFrame, QHBoxLayout
from PyQt6.QtCore import Qt

class SoftwareWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        
        self.setStyleSheet("background-color: transparent; font-family: 'Inter', sans-serif;")

        title = QLabel("App Store")
        title.setStyleSheet("""
            color: #ffffff;
            font-size: 32px; 
            font-family: 'Space Grotesk', sans-serif; 
            font-weight: 700;
            letter-spacing: -0.5px;
        """)
        layout.addWidget(title)
        
        subtitle = QLabel("Curated applications containerized with Flatpak.")
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 140); margin-bottom: 25px; font-size: 15px;")
        layout.addWidget(subtitle)

        # Scroll Area for apps
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background-color: transparent;")
        
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet("background-color: transparent;")
        grid = QGridLayout(scroll_widget)
        grid.setSpacing(20)

        apps = [
            {"name": "Discord", "id": "com.discordapp.Discord", "desc": "Chat & Voice"},
            {"name": "Spotify", "id": "com.spotify.Client", "desc": "Music Streaming"},
            {"name": "VS Code", "id": "com.visualstudio.code", "desc": "Code Editor"},
            {"name": "Figma", "id": "io.github.Figma_Linux.figma_linux", "desc": "UI Design Tool"}
        ]

        for i, app in enumerate(apps):
            row = i // 2
            col = i % 2
            card = self.create_app_card(app["name"], app["desc"], app["id"])
            grid.addWidget(card, row, col)

        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

    def create_app_card(self, name, desc, flatpak_id):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame { 
                background-color: rgba(255, 255, 255, 10); 
                border: 1px solid rgba(255, 255, 255, 15); 
                border-radius: 14px; 
            }
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)
        
        name_lbl = QLabel(name)
        name_lbl.setStyleSheet("color: #ffffff; font-weight: 700; font-size: 18px; border: none; background: transparent;")
        layout.addWidget(name_lbl)
        
        desc_lbl = QLabel(desc)
        desc_lbl.setStyleSheet("color: rgba(255, 255, 255, 140); border: none; background: transparent;")
        layout.addWidget(desc_lbl)
        
        btn = QPushButton("GET")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 20);
                color: #06B6D4;
                border: none;
                border-radius: 15px; /* Pill shape */
                padding: 6px 16px;
                font-weight: 700;
                font-size: 13px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 40);
            }
        """)
        btn.clicked.connect(lambda _, fid=flatpak_id: self.install_app(fid))
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(btn)
        
        layout.addLayout(btn_layout)
        return frame

    def install_app(self, flatpak_id):
        try:
            subprocess.Popen(["konsole", "-e", f"flatpak install flathub {flatpak_id} -y"])
        except Exception:
            pass
