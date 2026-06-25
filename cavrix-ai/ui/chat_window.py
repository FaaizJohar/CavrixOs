from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QMainWindow
from PyQt6.QtCore import Qt

class AIChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cavrix AI Assistant")
        self.resize(400, 600)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        # Glassmorphism container
        central.setStyleSheet("""
            QWidget {
                background-color: rgba(17, 24, 39, 0.85); /* #111827 with opacity */
                border: 1px solid #374151;
                border-radius: 12px;
                color: #F8FAFC;
                font-family: 'Inter', sans-serif;
            }
            QTextEdit {
                background: transparent;
                border: none;
            }
            QLineEdit {
                background-color: #1F2937;
                border: 1px solid #06B6D4;
                border-radius: 8px;
                padding: 8px;
            }
        """)

        layout = QVBoxLayout(central)
        
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.append("<b>Cavrix AI</b>: Hello! How can I help you today?")
        layout.addWidget(self.chat_history)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask Cavrix AI...")
        self.input_field.returnPressed.connect(self.process_input)
        layout.addWidget(self.input_field)

    def process_input(self):
        user_text = self.input_field.text().strip()
        if not user_text: return
        
        self.chat_history.append(f"<br><b>You</b>: {user_text}")
        self.input_field.clear()
        
        # Simple mock response
        self.chat_history.append("<b>Cavrix AI</b>: I'm currently just a UI scaffold, but I will be integrated with a local LLM or API soon!")
        
    def mousePressEvent(self, event):
        # Allow dragging the frameless window
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'drag_pos'):
            delta = event.globalPosition().toPoint() - self.drag_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.drag_pos = event.globalPosition().toPoint()
            event.accept()
