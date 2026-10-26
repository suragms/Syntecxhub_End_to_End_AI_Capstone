import pytest
from PySide6.QtWidgets import QApplication
from core.assistant_controller import AssistantController
from core.session_manager import SessionManager
from chatbot import RuleBasedChatbot
from commands import CommandRouter
from database import DatabaseManager
from gui.main_window import MainWindow

@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app

def test_main_window_flow(qapp, tmp_path):
    c = AssistantController(
        SessionManager(),
        RuleBasedChatbot(),
        CommandRouter(),
        DatabaseManager(tmp_path / "test.db"),
        required_face_frames=2
    )
    window = MainWindow(c)
    assert window.stack.currentIndex() == 0

    # Start camera page
    window.start_camera()
    assert window.stack.currentIndex() == 1
    assert not window.auth.camera.continue_button.isEnabled()

    # Simulate face detections
    c.face_detected(1)
    assert not window.auth.camera.continue_button.isEnabled()
    c.face_detected(1)
    assert window.auth.camera.continue_button.isEnabled()

    # Open dashboard
    window.open_dashboard()
    assert window.stack.currentIndex() == 2
    assert c.session.state.name == "SESSION_ACTIVE"

    # Submit a command
    window.submit("hello")
    assert "Hello" in window.dashboard.chat.history.toPlainText()

    # Logout
    window.logout()
    assert window.stack.currentIndex() == 0

    # Re-start camera after logout (must not raise Invalid transition error)
    window.start_camera()
    assert window.stack.currentIndex() == 1

    # Skip face check directly into dashboard
    window.open_dashboard()
    assert window.stack.currentIndex() == 2
    assert c.session.state.name == "SESSION_ACTIVE"

    # Go to settings and back
    window.logout()
    window.stack.setCurrentIndex(3)
    assert window.stack.currentIndex() == 3
    window.go_to_welcome()
    assert window.stack.currentIndex() == 0

    window.close()
