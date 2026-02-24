from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Task:
    id: int
    title: str
    priority: str
    completed: bool = False