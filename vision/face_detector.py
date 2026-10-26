from pathlib import Path
from core.models import FaceDetectionResult

class FaceDetector:
    def __init__(self, cascade=None, scale_factor=1.1, min_neighbors=5, min_size=(50, 50)):
        self._cascade = cascade
        self.scale_factor, self.min_neighbors, self.min_size = scale_factor, min_neighbors, min_size
    def _load(self):
        if self._cascade is None:
            import cv2
            self._cascade = cv2.CascadeClassifier(str(Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"))
        if hasattr(self._cascade, 'empty') and self._cascade.empty(): raise RuntimeError("Face detection model is unavailable")
    def detect(self, frame):
        self._load()
        import cv2
        if frame is None: raise ValueError("Invalid camera frame")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self._cascade.detectMultiScale(gray, self.scale_factor, self.min_neighbors, minSize=self.min_size)
        boxes = [tuple(map(int, box)) for box in faces]
        return FaceDetectionResult(boxes, frame)
    @staticmethod
    def draw(frame, result, color=(70, 180, 255)):
        import cv2
        output = frame.copy()
        for x, y, w, h in result.faces: cv2.rectangle(output, (x, y), (x+w, y+h), color, 2)
        cv2.putText(output, f"Faces detected: {result.count}", (12, 30), cv2.FONT_HERSHEY_SIMPLEX, .75, color, 2)
        return output
