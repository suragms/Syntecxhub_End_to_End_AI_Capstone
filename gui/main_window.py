from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget
from .theme import DARK_STYLE
from .authentication_page import AuthenticationPage
from .assistant_dashboard import AssistantDashboard
from .settings_page import SettingsPage

class VoiceWorker(QThread):
    finished_with_text = Signal(str)
    finished_with_error = Signal(str)

    def __init__(self, audio_manager, parent=None):
        super().__init__(parent)
        self.audio_manager = audio_manager

    def run(self):
        try:
            if not self.audio_manager:
                self.finished_with_error.emit('Audio manager is not available')
                return
            text = self.audio_manager.listen()
            self.finished_with_text.emit(text)
        except Exception as exc:
            self.finished_with_error.emit(str(exc))

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.voice_worker = None
        self.setWindowTitle('SURA AI — Smart Personal Assistant')
        self.resize(1100, 720)
        self.setStyleSheet(DARK_STYLE)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Page 0: Welcome Screen
        welcome = QWidget()
        layout = QVBoxLayout(welcome)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(16)

        title = QLabel('SURA AI')
        title.setObjectName('title')
        layout.addWidget(title)

        info = QLabel(
            'Smart Personal Assistant\n'
            'Developed by Surag M S · Syntecxhub AI Internship\n\n'
            'Key Capabilities:\n'
            '• Real-time OpenCV face presence check with camera preview\n'
            '• Safe desktop application launch (Notepad, Calculator, Paint, etc.)\n'
            '• Web searches and queries with URL validation\n'
            '• Speech-to-Text & Text-to-Speech audio support\n'
            '• Privacy-first local SQLite architecture'
        )
        info.setStyleSheet('line-height: 1.6; color: #b8c4e8; font-size: 15px; margin-bottom: 16px;')
        layout.addWidget(info)

        start = QPushButton('▶  Start Assistant')
        start.setStyleSheet('background: #4657d6; font-size: 16px; font-weight: bold; padding: 14px 28px;')
        start.clicked.connect(self.start_camera)

        settings_btn = QPushButton('⚙  Settings & Privacy')
        settings_btn.setStyleSheet('background: #232c4a; color: #9ab0e0; font-size: 14px; padding: 10px 20px;')
        settings_btn.clicked.connect(lambda: self.stack.setCurrentIndex(3))

        layout.addWidget(start)
        layout.addWidget(settings_btn)
        layout.addStretch()
        self.stack.addWidget(welcome)

        # Page 1: Face Authentication Page
        self.auth = AuthenticationPage(
            continue_callback=self.open_dashboard,
            skip_callback=self.open_dashboard,
            back_callback=self.go_to_welcome,
            parent=self
        )
        self.stack.addWidget(self.auth)

        # Page 2: Assistant Dashboard
        self.dashboard = AssistantDashboard(self.submit, self.listen, self.logout, parent=self)
        self.stack.addWidget(self.dashboard)

        # Page 3: Settings Page
        self.settings = SettingsPage(
            back_callback=self.go_to_welcome,
            database=self.controller.database,
            audio=self.controller.audio,
            parent=self
        )
        self.stack.addWidget(self.settings)

        self.statusBar().showMessage('Ready — select Start Assistant to begin')
        controller.on_message = lambda user, assistant: (
            self.dashboard.chat.add_message('You', user),
            self.dashboard.chat.add_message('SURA', assistant)
        )
        controller.on_status = self.update_status

    def go_to_welcome(self):
        self.auth.camera.stop_camera()
        self.stack.setCurrentIndex(0)
        self.update_status('Ready — select Start Assistant to begin')

    def start_camera(self):
        self.stack.setCurrentWidget(self.auth)
        self.controller.start_camera()
        self.auth.camera.start_camera(self.controller.face_detected)

    def update_status(self, text):
        self.statusBar().showMessage(text)
        self.auth.camera.set_status(text, 'Passed' in text)

    def open_dashboard(self):
        self.auth.camera.stop_camera()
        self.stack.setCurrentWidget(self.dashboard)
        if self.controller.session.state.name != 'SESSION_ACTIVE':
            self.controller.session.face_check_passed()
        self.update_status('Session active — Ready for commands')

    def submit(self, text):
        try:
            self.controller.submit_text(text)
        except RuntimeError as exc:
            self.update_status(str(exc))

    def listen(self):
        if self.voice_worker and self.voice_worker.isRunning():
            return
        if not self.controller.audio:
            self.update_status('Audio is not available on this system')
            return

        self.dashboard.voice.set_listening(True)
        self.update_status('Listening for voice input... Speak now.')

        self.voice_worker = VoiceWorker(self.controller.audio, parent=self)

        def on_text(text):
            self.dashboard.voice.set_listening(False)
            self.update_status(f'Heard: "{text}"')
            self.submit(text)

        def on_error(err):
            self.dashboard.voice.set_listening(False)
            self.update_status(f'Voice error: {err}')

        self.voice_worker.finished_with_text.connect(on_text)
        self.voice_worker.finished_with_error.connect(on_error)
        self.voice_worker.start()

    def logout(self):
        self.auth.camera.stop_camera()
        if self.voice_worker and self.voice_worker.isRunning():
            self.voice_worker.terminate()
            self.voice_worker = None
        self.controller.logout()
        self.stack.setCurrentIndex(0)
        self.update_status('Logged out — Ready to start again')

    def closeEvent(self, event):
        self.auth.camera.stop_camera()
        if self.voice_worker and self.voice_worker.isRunning():
            self.voice_worker.terminate()
            self.voice_worker = None
        self.controller.shutdown()
        event.accept()
