import pytest
from core.session_manager import SessionManager
from core.state_manager import SessionState

def test_session_flow():
    session = SessionManager(); session.start_camera(); session.face_check_passed()
    assert session.state == SessionState.SESSION_ACTIVE

def test_action_before_face_check_rejected():
    session = SessionManager()
    with pytest.raises(RuntimeError): session.begin_processing()
