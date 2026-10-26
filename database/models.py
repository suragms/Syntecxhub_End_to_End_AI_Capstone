from dataclasses import dataclass, field
from datetime import datetime
@dataclass
class HistoryRecord:
    role: str
    content: str
    intent: str = ''
    status: str = ''
    timestamp: datetime = field(default_factory=datetime.now)
