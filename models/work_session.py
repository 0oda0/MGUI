# models/work_session.py
from dataclasses import dataclass

@dataclass
class WorkSession:
    id: int
    date: str
    month: int
    year: int
    seconds: int