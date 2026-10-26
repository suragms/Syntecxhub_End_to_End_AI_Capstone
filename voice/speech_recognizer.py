class SpeechRecognizer:
    def __init__(self, recognizer=None, microphone_factory=None, timeout=5, phrase_time_limit=8):
        self.recognizer = recognizer
        self.microphone_factory = microphone_factory
        self.timeout, self.phrase_time_limit = timeout, phrase_time_limit
    def listen_once(self):
        try:
            import speech_recognition as sr
            recognizer = self.recognizer or sr.Recognizer(); factory = self.microphone_factory or sr.Microphone
            with factory() as source:
                recognizer.adjust_for_ambient_noise(source, duration=.5)
                audio = recognizer.listen(source, timeout=self.timeout, phrase_time_limit=self.phrase_time_limit)
            return recognizer.recognize_google(audio)
        except Exception as exc:
            name = type(exc).__name__
            if name == 'WaitTimeoutError': raise RuntimeError('No speech detected before timeout') from exc
            if name == 'UnknownValueError': raise RuntimeError('Speech was not understood') from exc
            if name == 'RequestError': raise RuntimeError('Speech recognition service is unavailable') from exc
            raise RuntimeError(f'Microphone error: {exc}') from exc
