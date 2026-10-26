import sys
from chatbot import RuleBasedChatbot
from commands import CommandRouter
from core import AssistantController, SessionManager
from database import DatabaseManager
from voice.audio_manager import AudioManager
from voice.speech_recognizer import SpeechRecognizer
from voice.text_to_speech import TextToSpeechEngine

def build_controller():
    audio = AudioManager(SpeechRecognizer(), TextToSpeechEngine())
    return AssistantController(SessionManager(), RuleBasedChatbot(), CommandRouter(), DatabaseManager(), audio)

def main():
    try:
        from PySide6.QtWidgets import QApplication
        from gui.main_window import MainWindow
    except ImportError as exc:
        print(f'GUI dependencies are missing: {exc}'); return 1
    app = QApplication(sys.argv); controller = build_controller(); window = MainWindow(controller); window.show()
    code = app.exec(); controller.shutdown(); return code
if __name__ == '__main__': raise SystemExit(main())
