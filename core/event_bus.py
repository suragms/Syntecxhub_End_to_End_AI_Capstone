try:
    from PySide6.QtCore import QObject, Signal
except ImportError:
    class QObject: pass
    class Signal:
        def __init__(self, *args): pass

class EventBus(QObject):
    message = Signal(str, str)
    status = Signal(str)
    error = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent) if hasattr(super(), '__init__') else None
