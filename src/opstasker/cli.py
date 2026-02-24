from __future__ import annotations

import argparse
import json
from opstasker.storage import TaskStore

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="opstasker", description="Simple task manager (CLI).")

    # IMPORTANT: global flags must be added to the parent parser
    p.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    sub = p.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add", help="Add a task")
    add.add_argument("title", help="Task title")
    add.add_argument("--priority", choices=["low", "medium", "high"], default="medium")

    sub.add_parser("list", help="List tasks")

    done = sub.add_parser("complete", help="Complete a task by ID")
    done.add_argument("id", type=int)

    delete = sub.add_parser("delete", help="Delete a task by ID")
    delete.add_argument("id", type=int)

    return p

def _task_to_dict(t) -> dict:
    return {"id": t.id, "title": t.title, "priority": t.priority, "completed": t.completed}

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    store = TaskStore()

    if args.cmd == "add":
        task = store.add(title=args.title, priority=args.priority)
        if args.json:
            print(json.dumps({"ok": True, "task": _task_to_dict(task)}, indent=2))
        else:
            print(f"Added [{task.id}] {task.title} ({task.priority})")
        return 0

    if args.cmd == "list":
        tasks = store.list()
        if args.json:
            print(json.dumps({"ok": True, "tasks": [_task_to_dict(t) for t in tasks]}, indent=2))
            return 0

        if not tasks:
            print("No tasks yet.")
            return 0

        for t in tasks:
            status = "✓" if t.completed else " "
            print(f"[{t.id}] [{status}] {t.title} ({t.priority})")
        return 0

    if args.cmd == "complete":
        ok = store.complete(args.id)
        if args.json:
            print(json.dumps({"ok": ok, "action": "complete", "id": args.id}, indent=2))
        else:
            print("Marked complete." if ok else "Task not found.")
        return 0

    if args.cmd == "delete":
        ok = store.delete(args.id)
        if args.json:
            print(json.dumps({"ok": ok, "action": "delete", "id": args.id}, indent=2))
        else:
            print("Deleted." if ok else "Task not found.")
        return 0

    return 2

if __name__ == "__main__":
    raise SystemExit(main())