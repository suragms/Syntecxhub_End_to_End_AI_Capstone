from enum import Enum, auto

class SessionState(Enum):
    INITIALIZING = auto(); CAMERA_READY = auto(); FACE_CHECKING = auto(); FACE_CHECK_PASSED = auto()
    IDENTITY_VERIFICATION = auto(); SESSION_ACTIVE = auto(); LISTENING = auto(); PROCESSING = auto()
    EXECUTING = auto(); SPEAKING = auto(); LOGGED_OUT = auto(); ERROR = auto()

_TRANSITIONS = {
    SessionState.INITIALIZING: {SessionState.CAMERA_READY, SessionState.FACE_CHECKING, SessionState.FACE_CHECK_PASSED, SessionState.SESSION_ACTIVE, SessionState.ERROR},
    SessionState.CAMERA_READY: {SessionState.FACE_CHECKING, SessionState.FACE_CHECK_PASSED, SessionState.LOGGED_OUT, SessionState.ERROR},
    SessionState.FACE_CHECKING: {SessionState.FACE_CHECK_PASSED, SessionState.SESSION_ACTIVE, SessionState.ERROR, SessionState.CAMERA_READY, SessionState.LOGGED_OUT},
    SessionState.FACE_CHECK_PASSED: {SessionState.SESSION_ACTIVE, SessionState.CAMERA_READY, SessionState.LOGGED_OUT, SessionState.ERROR},
    SessionState.SESSION_ACTIVE: {SessionState.LISTENING, SessionState.PROCESSING, SessionState.LOGGED_OUT, SessionState.ERROR},
    SessionState.LISTENING: {SessionState.PROCESSING, SessionState.SESSION_ACTIVE, SessionState.LOGGED_OUT, SessionState.ERROR},
    SessionState.PROCESSING: {SessionState.EXECUTING, SessionState.SPEAKING, SessionState.SESSION_ACTIVE, SessionState.LOGGED_OUT, SessionState.ERROR},
    SessionState.EXECUTING: {SessionState.SPEAKING, SessionState.SESSION_ACTIVE, SessionState.LOGGED_OUT, SessionState.ERROR},
    SessionState.SPEAKING: {SessionState.SESSION_ACTIVE, SessionState.LOGGED_OUT, SessionState.ERROR},
    SessionState.ERROR: {SessionState.INITIALIZING, SessionState.CAMERA_READY, SessionState.LOGGED_OUT},
    SessionState.LOGGED_OUT: {SessionState.INITIALIZING, SessionState.CAMERA_READY, SessionState.FACE_CHECKING, SessionState.FACE_CHECK_PASSED, SessionState.SESSION_ACTIVE},
    SessionState.IDENTITY_VERIFICATION: {SessionState.SESSION_ACTIVE, SessionState.ERROR},
}

class StateManager:
    def __init__(self): self._state = SessionState.INITIALIZING
    @property
    def state(self): return self._state
    def transition(self, new_state):
        if new_state not in _TRANSITIONS.get(self._state, set()):
            raise ValueError(f"Invalid transition: {self._state.name} -> {new_state.name}")
        self._state = new_state
        return self._state
