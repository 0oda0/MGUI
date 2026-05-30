# models/task.py
from dataclasses import dataclass

@dataclass
class Task:
    id: int
    title: str
    important: bool
    urgent: bool
    completed: bool