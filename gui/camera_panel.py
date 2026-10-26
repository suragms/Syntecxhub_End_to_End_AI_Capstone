from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from vision.face_detector import FaceDetector

class CameraWorker(QThread):
    frame_ready = Signal(QImage, int)
    error_occurred = Signal(str)

    def __init__(self, camera_index=0, parent=None):
        super().__init__(parent)
        self.camera_index = camera_index
        self._running = False
        self.detector = FaceDetector()

    def run(self):
        import cv2
        cap = cv2.VideoCapture(self.camera_index)
        if not cap.isOpened():
            self.error_occurred.emit('Camera unavailable or permission denied. You can click "Skip Face Check" below.')
            return

        self._running = True
        try:
            while self._running:
                ret, frame = cap.read()
                if not ret or frame is None:
                    self.msleep(30)
                    continue
                try:
                    result = self.detector.detect(frame)
                    annotated = FaceDetector.draw(frame, result)
                    rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgb.shape
                    qimg = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888).copy()
                    self.frame_ready.emit(qimg, result.count)
                except Exception:
                    pass
                self.msleep(33)
        finally:
            cap.release()

    def stop(self):
        self._running = False
        self.wait(1000)

class CameraPanel(QWidget):
    def __init__(self, continue_callback, skip_callback=None, parent=None):
        super().__init__(parent)
        self.continue_callback = continue_callback
        self.skip_callback = skip_callback or continue_callback
        self.worker = None
        self._face_callback = None

        self.preview = QLabel('Camera preview will appear here')
        self.preview.setMinimumSize(640, 360)
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview.setStyleSheet('background:#080b16; border-radius:12px; font-size:16px; color:#6070a0;')

        self.status = QLabel('Ready to start camera')
        self.status.setStyleSheet('color: #8ea7ff; font-size: 15px; font-weight: 600; padding: 4px;')

        self.continue_button = QPushButton('Continue to Assistant')
        self.continue_button.setEnabled(False)
        self.continue_button.clicked.connect(self._on_continue)

        self.skip_button = QPushButton('Skip Face Check (Direct Access)')
        self.skip_button.setStyleSheet('background: #2a3458; color: #b0c0f0;')
        self.skip_button.clicked.connect(self._on_skip)

        btn_row = QHBoxLayout()
        btn_row.addWidget(self.skip_button)
        btn_row.addWidget(self.continue_button)

        layout = QVBoxLayout(self)
        layout.addWidget(self.preview, 1)
        layout.addWidget(self.status)
        layout.addLayout(btn_row)

    def start_camera(self, face_callback=None):
        self._face_callback = face_callback
        self.stop_camera()
        self.status.setText('Initializing camera feed...')
        self.worker = CameraWorker(parent=self)
        self.worker.frame_ready.connect(self._on_frame)
        self.worker.error_occurred.connect(self._on_error)
        self.worker.start()

    def stop_camera(self):
        if self.worker:
            self.worker.stop()
            self.worker = None

    def _on_frame(self, qimg, count):
        pixmap = QPixmap.fromImage(qimg)
        self.preview.setPixmap(pixmap.scaled(
            self.preview.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
        if self._face_callback:
            self._face_callback(count)

    def _on_error(self, err_text):
        self.status.setText(err_text)
        self.status.setStyleSheet('color: #ff6b6b; font-weight: 600;')

    def set_status(self, text, passed=False):
        self.status.setText(text)
        if passed:
            self.continue_button.setEnabled(True)
            self.continue_button.setStyleSheet('background: #28a745; color: white; font-weight: bold;')
            self.status.setStyleSheet('color: #4cd964; font-weight: bold;')
        else:
            self.status.setStyleSheet('color: #8ea7ff;')

    def _on_continue(self):
        self.stop_camera()
        self.continue_callback()

    def _on_skip(self):
        self.stop_camera()
        self.skip_callback()
