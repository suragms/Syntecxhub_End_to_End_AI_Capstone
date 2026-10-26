from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

@dataclass(frozen=True)
class FaceDetectionResult:
    faces: list[tuple[int, int, int, int]] = field(default_factory=list)
    frame: Any = None
    timestamp: datetime = field(default_factory=datetime.now)
    @property
    def count(self): return len(self.faces)

@dataclass(frozen=True)
class ChatResponse:
    text: str
    intent: str
    command: str | None = None
    argument: str | None = None

@dataclass(frozen=True)
class CommandResult:
    success: bool
    message: str
    intent: str = ""

@dataclass(frozen=True)
class HistoryEntry:
    role: str
    content: str
    intent: str = ""
    status: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
