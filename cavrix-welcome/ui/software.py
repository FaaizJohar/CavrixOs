import subprocess
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QGridLayout, QFrame
from PyQt6.QtCore import Qt

class SoftwareWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        
        self.setStyleSheet("background-color: #09090B; color: #F8FAFC; font-family: 'Inter', sans-serif;")

        title = QLabel("Recommended Software")
        title.setStyleSheet("font-size: 28px; font-family: 'Space Grotesk', sans-serif; font-weight: bold;")
        layout.addWidget(title)
        
        subtitle = QLabel("Install popular applications easily via Flatpak.")
        subtitle.setStyleSheet("color: #94A3B8; margin-bottom: 20px;")
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
            {"name": "Discord", "id": "com.discordapp.Discord", "desc": "Chat for gamers"},
            {"name": "Spotify", "id": "com.spotify.Client", "desc": "Music streaming"},
            {"name": "VS Code", "id": "com.visualstudio.code", "desc": "Code editor"},
            {"name": "VLC", "id": "org.videolan.VLC", "desc": "Media player"},
            {"name": "GIMP", "id": "org.gimp.GIMP", "desc": "Image editor"}
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
        frame.setStyleSheet("QFrame { background-color: #111827; border: 1px solid #374151; border-radius: 8px; }")
        layout = QVBoxLayout(frame)
        
        name_lbl = QLabel(name)
        name_lbl.setStyleSheet("font-weight: bold; font-size: 16px; border: none;")
        layout.addWidget(name_lbl)
        
        desc_lbl = QLabel(desc)
        desc_lbl.setStyleSheet("color: #94A3B8; border: none;")
        layout.addWidget(desc_lbl)
        
        btn = QPushButton("Install")
        btn.setStyleSheet("""
            QPushButton {
                background-color: #1F2937;
                color: #06B6D4;
                border: 1px solid #06B6D4;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #06B6D4;
                color: #09090B;
            }
        """)
        btn.clicked.connect(lambda _, fid=flatpak_id: self.install_app(fid))
        layout.addWidget(btn)
        
        return frame

    def install_app(self, flatpak_id):
        try:
            subprocess.Popen(["konsole", "-e", f"flatpak install flathub {flatpak_id} -y"])
        except Exception:
            pass
