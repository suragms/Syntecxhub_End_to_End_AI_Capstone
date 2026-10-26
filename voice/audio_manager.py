class AudioManager:
    def __init__(self, recognizer, tts): self.recognizer, self.tts, self.listening = recognizer, tts, False
    def listen(self):
        if self.listening: raise RuntimeError('Already listening')
        self.listening = True
        try: return self.recognizer.listen_once()
        finally: self.listening = False
    def speak(self, text): self.tts.speak(text)
    def shutdown(self): self.tts.stop()
