from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from .camera_panel import CameraPanel

class AuthenticationPage(QWidget):
    def __init__(self, continue_callback, skip_callback=None, back_callback=None, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)

        header = QHBoxLayout()
        if back_callback:
            back_btn = QPushButton('← Back')
            back_btn.setStyleSheet('background: #232c4a; color: #b8c8f8; font-weight: bold; padding: 8px 16px;')
            back_btn.clicked.connect(back_callback)
            header.addWidget(back_btn)

        title = QLabel('Face Presence Check')
        title.setObjectName('title')
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)

        subtitle = QLabel('This demo checks whether a face is visible to activate the assistant. Look at the camera or click "Skip Face Check".')
        subtitle.setStyleSheet('color: #a0b0d0; margin-bottom: 8px;')
        layout.addWidget(subtitle)

        self.camera = CameraPanel(continue_callback, skip_callback=skip_callback, parent=self)
        layout.addWidget(self.camera)
