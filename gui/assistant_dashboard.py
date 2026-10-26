from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from .chat_panel import ChatPanel
from .voice_panel import VoicePanel

class AssistantDashboard(QWidget):
    def __init__(self, submit, listen, logout, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        title = QLabel('SURA AI Dashboard')
        title.setObjectName('title')
        layout.addWidget(title)

        row = QHBoxLayout()
        self.chat = ChatPanel(submit, parent=self)
        self.voice = VoicePanel(listen, parent=self)
        row.addWidget(self.chat, 3)
        row.addWidget(self.voice, 1)
        layout.addLayout(row)

        logout_btn = QPushButton('Log out')
        logout_btn.setStyleSheet('background: #402030; color: #ffb0b0;')
        logout_btn.clicked.connect(logout)
        layout.addWidget(logout_btn)
