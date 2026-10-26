from vision.camera_manager import CameraManager
class ClosedCapture:
    def isOpened(self): return False
    def release(self): self.released=True

def test_camera_open_failure_releases():
    cap=ClosedCapture()
    try: CameraManager(capture_factory=lambda _: cap).open()
    except RuntimeError: pass
    assert getattr(cap,'released',False)
