import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QListWidget, QListWidgetItem, QStackedWidget)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QIcon, QPainter, QColor
import os

from ui.home import HomeWidget
from ui.setup import SetupWidget
from ui.software import SoftwareWidget

class GlassSidebar(QListWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(220)
        # Mac-like translucent sidebar styling
        self.setStyleSheet("""
            QListWidget {
                background-color: rgba(30, 30, 35, 180);
                border: none;
                border-right: 1px solid rgba(255, 255, 255, 20);
                padding: 15px 10px;
                outline: 0;
            }
            QListWidget::item {
                color: rgba(255, 255, 255, 200);
                padding: 12px;
                border-radius: 8px;
                margin-bottom: 6px;
                font-family: 'Inter', sans-serif;
                font-size: 14px;
                font-weight: 500;
            }
            QListWidget::item:selected {
                background-color: rgba(37, 99, 235, 200); /* Cavrix Blue */
                color: #ffffff;
            }
            QListWidget::item:hover:!selected {
                background-color: rgba(255, 255, 255, 15);
                color: #ffffff;
            }
        """)

class CavrixWelcome(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome to CavrixOS")
        self.resize(950, 650)
        
        # Mac-like Frameless and Translucent properties
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Container with rounded corners
        self.container = QWidget(central_widget)
        self.container.setStyleSheet("""
            QWidget#MainContainer {
                background-color: rgba(15, 15, 20, 220); /* Dark translucent */
                border-radius: 14px;
                border: 1px solid rgba(255, 255, 255, 20);
            }
        """)
        self.container.setObjectName("MainContainer")
        
        container_layout = QHBoxLayout(self.container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(self.container)
        main_layout.setContentsMargins(10, 10, 10, 10) # Margin for drop shadow

        # Sidebar
        self.sidebar = GlassSidebar()
        
        # Title bar for dragging (embedded in sidebar top)
        self.sidebar.addItem(QListWidgetItem("")) # Spacer
        
        for item_text in ["Welcome", "System Setup", "Software"]:
            item = QListWidgetItem(item_text)
            self.sidebar.addItem(item)
            
        container_layout.addWidget(self.sidebar)

        # Stacked Widget for Pages
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background-color: transparent;")
        container_layout.addWidget(self.stack)

        # Pages
        self.home_page = HomeWidget()
        self.setup_page = SetupWidget()
        self.software_page = SoftwareWidget()

        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.setup_page)
        self.stack.addWidget(self.software_page)

        # Connect and set default
        self.sidebar.currentRowChanged.connect(lambda i: self.stack.setCurrentIndex(i-1) if i > 0 else None)
        self.sidebar.setCurrentRow(1) # Select 'Welcome'

        # Window Drag Variables
        self.oldPos = self.pos()

    # Enable dragging of frameless window
    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CavrixWelcome()
    window.show()
    sys.exit(app.exec())
