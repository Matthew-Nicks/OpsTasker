from __future__ import annotations

import json
from pathlib import Path
from opstasker.models import Task

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DATA_FILE = DATA_DIR / "tasks.json"

class TaskStore:
    def __init__(self) -> None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not DATA_FILE.exists():
            DATA_FILE.write_text(json.dumps({"next_id": 1, "tasks": []}, indent=2), encoding="utf-8")

    def _load(self) -> dict:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))

    def _save(self, payload: dict) -> None:
        DATA_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def add(self, title: str, priority: str) -> Task:
        payload = self._load()
        tid = int(payload["next_id"])
        task = {"id": tid, "title": title, "priority": priority, "completed": False}
        payload["tasks"].append(task)
        payload["next_id"] = tid + 1
        self._save(payload)
        return Task(**task)

    def list(self) -> list[Task]:
        payload = self._load()
        return [Task(**t) for t in payload["tasks"]]

    def complete(self, task_id: int) -> bool:
        payload = self._load()
        for t in payload["tasks"]:
            if int(t["id"]) == task_id:
                t["completed"] = True
                self._save(payload)
                return True
        return False

    def delete(self, task_id: int) -> bool:
        payload = self._load()
        before = len(payload["tasks"])
        payload["tasks"] = [t for t in payload["tasks"] if int(t["id"]) != task_id]
        if len(payload["tasks"]) != before:
            self._save(payload)
            return True
        return False