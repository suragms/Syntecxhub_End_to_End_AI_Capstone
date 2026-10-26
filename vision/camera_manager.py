class CameraManager:
    def __init__(self, index=0, width=640, height=480, capture_factory=None):
        self.index, self.width, self.height = index, width, height
        self.capture_factory = capture_factory
        self.capture = None
    def open(self):
        import cv2
        factory = self.capture_factory or cv2.VideoCapture
        self.capture = factory(self.index)
        if self.capture is None or not self.capture.isOpened():
            self.release(); raise RuntimeError("Camera unavailable or permission denied")
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width); self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        return self
    def read(self):
        if self.capture is None: raise RuntimeError("Camera is not open")
        ok, frame = self.capture.read()
        if not ok or frame is None: raise RuntimeError("Camera returned an invalid frame")
        return frame
    def release(self):
        if self.capture is not None:
            self.capture.release(); self.capture = None
