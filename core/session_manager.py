import uuid
from .state_manager import SessionState, StateManager

class SessionManager:
    def __init__(self):
        self.states = StateManager()
        self.session_id = None

    @property
    def state(self):
        return self.states.state

    def start_camera(self):
        if self.state in {SessionState.LOGGED_OUT, SessionState.ERROR}:
            self.states.transition(SessionState.INITIALIZING)
        if self.state == SessionState.INITIALIZING:
            self.states.transition(SessionState.CAMERA_READY)
        if self.state == SessionState.CAMERA_READY:
            self.states.transition(SessionState.FACE_CHECKING)

    def face_check_passed(self):
        if self.state != SessionState.SESSION_ACTIVE:
            if self.state in {SessionState.LOGGED_OUT, SessionState.ERROR}:
                self.states.transition(SessionState.INITIALIZING)
            if self.state == SessionState.INITIALIZING:
                self.states.transition(SessionState.CAMERA_READY)
            if self.state == SessionState.CAMERA_READY:
                self.states.transition(SessionState.FACE_CHECKING)
            if self.state == SessionState.FACE_CHECKING:
                self.states.transition(SessionState.FACE_CHECK_PASSED)
                self.states.transition(SessionState.SESSION_ACTIVE)
            elif self.state == SessionState.FACE_CHECK_PASSED:
                self.states.transition(SessionState.SESSION_ACTIVE)
        self.session_id = uuid.uuid4().hex

    def begin_processing(self):
        if self.state != SessionState.SESSION_ACTIVE:
            raise RuntimeError("Complete face presence check first")
        self.states.transition(SessionState.PROCESSING)

    def logout(self):
        if self.state != SessionState.LOGGED_OUT:
            self.states.transition(SessionState.LOGGED_OUT)
        self.session_id = None
