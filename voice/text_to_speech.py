import queue, threading
class TextToSpeechEngine:
    def __init__(self, engine_factory=None):
        self._factory = engine_factory; self._queue = queue.Queue(); self._stop = threading.Event(); self._muted = False
        self._thread = threading.Thread(target=self._run, daemon=True); self._thread.start()
    def _run(self):
        try: engine = (self._factory or __import__('pyttsx3').init)()
        except Exception: engine = None
        while not self._stop.is_set():
            try: text = self._queue.get(timeout=.1)
            except queue.Empty: continue
            if engine and not self._muted:
                try: engine.say(text); engine.runAndWait()
                except Exception: pass
    def speak(self, text):
        if text: self._queue.put(str(text))
    def set_muted(self, muted): self._muted = bool(muted)
    def stop(self): self._stop.set()
