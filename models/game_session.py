# models/game_session.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class GameSession:
    id: int
    game_name: str
    start_time: datetime
    end_time: datetime
    duration_seconds: int