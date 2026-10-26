from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QHBoxLayout, QLineEdit, QPushButton
class ChatPanel(QWidget):
    def __init__(self, submit, parent=None):
        super().__init__(parent); self.submit = submit
        self.history = QTextEdit(readOnly=True); self.entry = QLineEdit(placeholderText='Type a command here...'); self.send = QPushButton('Send'); self.send.clicked.connect(self._send); self.entry.returnPressed.connect(self._send)
        row = QHBoxLayout(); row.addWidget(self.entry); row.addWidget(self.send); layout = QVBoxLayout(self); layout.addWidget(self.history); layout.addLayout(row)
    def _send(self):
        text = self.entry.text().strip()
        if text: self.submit(text); self.entry.clear()
    def add_message(self, role, text): self.history.append(f'<b>{role}:</b> {text}')
