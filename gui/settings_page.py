from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox, QGroupBox, QMessageBox
)

class SettingsPage(QWidget):
    def __init__(self, back_callback=None, database=None, audio=None, parent=None):
        super().__init__(parent)
        self.back_callback = back_callback
        self.database = database
        self.audio = audio

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(16)

        # Header with back button
        header_row = QHBoxLayout()
        back_btn = QPushButton('← Back')
        back_btn.setStyleSheet('background: #232c4a; color: #b8c8f8; font-weight: bold; padding: 8px 16px;')
        if back_callback:
            back_btn.clicked.connect(back_callback)
        header_row.addWidget(back_btn)

        title = QLabel('Settings & Privacy')
        title.setObjectName('title')
        header_row.addWidget(title)
        header_row.addStretch()
        layout.addLayout(header_row)

        # Audio settings group
        audio_group = QGroupBox('Audio & Speech')
        audio_layout = QVBoxLayout(audio_group)
        self.mute_tts = QCheckBox('Mute Text-to-Speech voice responses')
        self.mute_tts.setStyleSheet('color: #d0dbff; font-size: 14px;')
        self.mute_tts.stateChanged.connect(self._toggle_mute)
        audio_layout.addWidget(self.mute_tts)
        layout.addWidget(audio_group)

        # Privacy & Data group
        privacy_group = QGroupBox('Local Privacy & Security')
        privacy_layout = QVBoxLayout(privacy_group)
        privacy_text = QLabel(
            '• SURA AI operates 100% locally on your PC.\n'
            '• Face presence verification does not save photos, video recordings, or facial templates.\n'
            '• Voice audio is processed locally and discarded immediately.\n'
            '• Local logs are kept only in a lightweight SQLite database for session history.'
        )
        privacy_text.setStyleSheet('color: #a4b4de; font-size: 13px; line-height: 1.6;')
        privacy_layout.addWidget(privacy_text)

        clear_btn = QPushButton('Clear Local Chat History')
        clear_btn.setStyleSheet('background: #4a2030; color: #ffb0b0; font-weight: 600; padding: 8px 16px; margin-top: 8px;')
        clear_btn.clicked.connect(self._clear_history)
        privacy_layout.addWidget(clear_btn)
        layout.addWidget(privacy_group)

        # System Information group
        info_group = QGroupBox('About')
        info_layout = QVBoxLayout(info_group)
        about_text = QLabel(
            'SURA AI — Smart Personal Assistant\n'
            'Syntecxhub Artificial Intelligence Internship · Capstone Project 2\n'
            'Developer: Surag M S\n'
            'Platform: Windows 10/11'
        )
        about_text.setStyleSheet('color: #889ac2; font-size: 13px;')
        info_layout.addWidget(about_text)
        layout.addWidget(info_group)

        layout.addStretch()

    def _toggle_mute(self, state):
        if self.audio and hasattr(self.audio, 'tts'):
            self.audio.tts.set_muted(bool(state))

    def _clear_history(self):
        if self.database and hasattr(self.database, 'cursor'):
            try:
                self.database.cursor.execute('DELETE FROM history')
                self.database.connection.commit()
                QMessageBox.information(self, 'Success', 'Local chat history has been cleared.')
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Could not clear history: {e}')
        else:
            QMessageBox.information(self, 'Notice', 'Local history is already empty.')
