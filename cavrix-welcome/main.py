import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QListWidget, QListWidgetItem, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from ui.home import HomeWidget
from ui.setup import SetupWidget
from ui.software import SoftwareWidget

class CavrixWelcome(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome to CavrixOS")
        self.resize(900, 600)
        self.setWindowIcon(QIcon("/usr/share/pixmaps/cavrixos-logo.svg"))
        
        # Apply dark styling globally
        self.setStyleSheet("""
            QMainWindow {
                background-color: #09090B;
            }
            QListWidget {
                background-color: #111827;
                border: none;
                border-right: 1px solid #374151;
                padding: 10px;
                outline: 0;
            }
            QListWidget::item {
                color: #94A3B8;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 5px;
                font-family: 'Inter', sans-serif;
                font-size: 14px;
            }
            QListWidget::item:selected {
                background-color: #2563EB;
                color: #F8FAFC;
            }
            QListWidget::item:hover:!selected {
                background-color: #1F2937;
                color: #F8FAFC;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(200)
        main_layout.addWidget(self.sidebar)

        # Stacked Widget for Pages
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # Add Pages
        self.home_page = HomeWidget()
        self.setup_page = SetupWidget()
        self.software_page = SoftwareWidget()

        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.setup_page)
        self.stack.addWidget(self.software_page)

        # Add Sidebar Items
        for item_text in ["Home", "System Setup", "Software"]:
            item = QListWidgetItem(item_text)
            self.sidebar.addItem(item)
            
        self.sidebar.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.sidebar.setCurrentRow(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CavrixWelcome()
    window.show()
    sys.exit(app.exec())
