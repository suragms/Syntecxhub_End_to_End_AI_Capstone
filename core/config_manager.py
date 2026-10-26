import json
from pathlib import Path

DEFAULTS = {"camera_index": 0, "camera_width": 640, "camera_height": 480, "stable_face_frames": 8, "history_enabled": True, "tts_enabled": True, "speech_timeout": 5, "tts_volume": 0.85, "tts_rate": 175}
class ConfigManager:
    def __init__(self, path=None):
        self.path = Path(path) if path else Path(__file__).parents[1] / "config" / "settings.json"
        self.values = dict(DEFAULTS)
        if self.path.exists():
            try: self.values.update(json.loads(self.path.read_text(encoding="utf-8")))
            except (OSError, ValueError): pass
    def get(self, key, default=None): return self.values.get(key, default)
    def set(self, key, value):
        self.values[key] = value
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.values, indent=2), encoding="utf-8")
