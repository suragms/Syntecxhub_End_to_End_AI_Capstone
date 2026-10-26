import pytest
from voice.audio_manager import AudioManager
class FakeRecognizer:
    def listen_once(self): return 'hello'
class FakeTTS:
    def __init__(self): self.spoken=[]
    def speak(self,text): self.spoken.append(text)
    def stop(self): pass
def test_audio_manager():
    tts=FakeTTS(); audio=AudioManager(FakeRecognizer(),tts); assert audio.listen() == 'hello'; audio.speak('hi'); assert tts.spoken == ['hi']
def test_overlapping_listen_rejected():
    audio=AudioManager(FakeRecognizer(),FakeTTS()); audio.listening=True
    with pytest.raises(RuntimeError): audio.listen()
