from .state_manager import SessionState
from vision.face_verification import FacePresenceVerifier
class AssistantController:
    def __init__(self, session, chatbot, commands, database, audio=None, required_face_frames=8):
        self.session, self.chatbot, self.commands, self.database, self.audio = session, chatbot, commands, database, audio
        self.verifier = FacePresenceVerifier(required_face_frames)
        self.on_message = None; self.on_status = None
    def start_camera(self):
        self.verifier.reset()
        self.session.start_camera()
        self._status('Searching for a face...')
    def face_detected(self, count):
        if count == 1:
            if self.session.states.state == SessionState.FACE_CHECKING:
                if self.session_manager_check(count):
                    self.session.face_check_passed()
                    self._status('Face Presence Check Passed — Demo Access')
                else:
                    self._status(f'Face detected ({self.verifier.streak}/{self.verifier.required_frames}) — Hold steady...')
        elif count == 0:
            self.verifier.reset()
            self._status('No face detected. Please position yourself in front of the camera.')
        else:
            self.verifier.reset()
            self._status('Multiple faces detected. Please ensure only one person is in front of the camera.')
    def session_manager_check(self, count):
        return self.verifier.update(count)
    def submit_text(self, text):
        if self.session.state != SessionState.SESSION_ACTIVE: raise RuntimeError('Complete face presence check first')
        response = self.chatbot.respond(text); self.database.add_history('user', text, response.intent)
        result = self.commands.execute(response.command, response.argument) if response.command else None
        message = result.message if result else response.text
        self.database.add_history('assistant', message, response.intent, 'success' if not result or result.success else 'failed')
        if self.on_message: self.on_message(text, message)
        if self.audio: self.audio.speak(message)
        if response.intent in {'logout','exit'}: self.logout()
        return message
    def logout(self):
        self.verifier.reset()
        self.session.logout()
        self._status('Logged out')
    def _status(self, text):
        if self.on_status: self.on_status(text)
    def shutdown(self):
        if self.audio: self.audio.shutdown()
        self.database.close()
