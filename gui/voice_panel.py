from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class VoicePanel(QWidget):
    def __init__(self, listen_callback, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.state = QLabel('Microphone Ready')
        self.state.setStyleSheet('color: #8ea7ff; font-weight: 600;')
        self.button = QPushButton('🎤 Start Listening')
        self.button.clicked.connect(listen_callback)
        layout.addWidget(self.state)
        layout.addWidget(self.button)
        layout.addStretch()

    def set_listening(self, is_listening):
        if is_listening:
            self.state.setText('Listening...')
            self.state.setStyleSheet('color: #ffb86c; font-weight: bold;')
            self.button.setText('Listening...')
            self.button.setEnabled(False)
        else:
            self.state.setText('Microphone Ready')
            self.state.setStyleSheet('color: #8ea7ff; font-weight: 600;')
            self.button.setText('🎤 Start Listening')
            self.button.setEnabled(True)
