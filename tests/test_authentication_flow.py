from core.assistant_controller import AssistantController
from core.session_manager import SessionManager
from chatbot import RuleBasedChatbot
from commands import CommandRouter
from database import DatabaseManager

def test_controller_requires_stable_presence(tmp_path):
    c=AssistantController(SessionManager(),RuleBasedChatbot(),CommandRouter(),DatabaseManager(tmp_path/'db.sqlite'),required_face_frames=2)
    c.start_camera(); c.face_detected(1); assert c.session.state.name == 'FACE_CHECKING'; c.face_detected(1); assert c.session.state.name == 'SESSION_ACTIVE'
