class FacePresenceVerifier:
    def __init__(self, required_frames=8): self.required_frames, self._streak = required_frames, 0
    def update(self, face_count):
        if face_count == 1:
            self._streak += 1
            return self._streak >= self.required_frames
        self._streak = 0
        return False
    def reset(self): self._streak = 0
    @property
    def streak(self): return self._streak
