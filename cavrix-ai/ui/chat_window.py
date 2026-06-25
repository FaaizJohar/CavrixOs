from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QMainWindow
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import requests
import json


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
        if not user_text:
            return

        self.chat_history.append(f"<br><b>You</b>: {user_text}")
        self.input_field.clear()
        self.input_field.setEnabled(False)
        self.input_field.setPlaceholderText("Cavrix AI is thinking...")
        
        # Start background thread to query Ollama API
        self.worker = OllamaWorker(user_text)
        self.worker.response_signal.connect(self.on_ai_response)
        self.worker.error_signal.connect(self.on_ai_error)
        self.worker.start()

    def on_ai_response(self, text):
        self.chat_history.append(f"<br><b>Cavrix AI</b>: {text}")
        self.reset_input()

    def on_ai_error(self, error_msg):
        self.chat_history.append(f"<br><span style='color:#ef4444;'><b>System</b>: Failed to connect to local AI engine. Make sure Ollama is running. ({error_msg})</span>")
        self.reset_input()

    def reset_input(self):
        self.input_field.setEnabled(True)
        self.input_field.setPlaceholderText("Ask Cavrix AI...")
        self.input_field.setFocus()

class OllamaWorker(QThread):
    response_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt

    def run(self):
        try:
            # Query local Ollama instance (llama3 or phi3)
            payload = {
                "model": "llama3",
                "prompt": self.prompt,
                "stream": False
            }
            # Add a slight timeout so it doesn't hang forever if Ollama is off
            response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            reply = data.get("response", "").strip()
            self.response_signal.emit(reply.replace('\\n', '<br>'))
        except requests.exceptions.RequestException as e:
            self.error_signal.emit(str(e))

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
