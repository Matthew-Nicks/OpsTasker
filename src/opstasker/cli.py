from __future__ import annotations

import argparse
import json

from opstasker.storage import TaskStore


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="opstasker", description="Simple task manager (CLI).")

    # Global flag (must come before the subcommand)
    p.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    sub = p.add_subparsers(dest="cmd", required=True)

    # add command
    add = sub.add_parser("add", help="Add a task")
    add.add_argument("title", help="Task title")
    add.add_argument("--priority", choices=["low", "medium", "high"], default="medium")

    # list command (filters + sorting)
    list_cmd = sub.add_parser("list", help="List tasks")
    list_cmd.add_argument("--priority", choices=["low", "medium", "high"], help="Filter by priority")

    status = list_cmd.add_mutually_exclusive_group()
    status.add_argument("--completed", action="store_true", help="Show only completed tasks")
    status.add_argument("--pending", action="store_true", help="Show only pending tasks")

    list_cmd.add_argument(
        "--sort",
        choices=["id", "title", "priority", "status"],
        default="id",
        help="Sort tasks (default: id)",
    )
    list_cmd.add_argument("--desc", action="store_true", help="Sort descending")

    # complete command
    done = sub.add_parser("complete", help="Complete a task by ID")
    done.add_argument("id", type=int)

    # delete command
    delete = sub.add_parser("delete", help="Delete a task by ID")
    delete.add_argument("id", type=int)

    return p


def _task_to_dict(t) -> dict:
    return {
        "id": t.id,
        "title": t.title,
        "priority": t.priority,
        "completed": t.completed,
    }


def _render_table(tasks: list) -> str:
    headers = ["ID", "Status", "Priority", "Title"]
    rows = []

    for t in tasks:
        status = "Done" if t.completed else "Pending"
        rows.append([str(t.id), status, t.priority, t.title])

    widths = [len(h) for h in headers]
    for r in rows:
        for i, cell in enumerate(r):
            widths[i] = max(widths[i], len(cell))

    def fmt_row(r: list[str]) -> str:
        return "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(r))

    lines = [fmt_row(headers), fmt_row(["-" * w for w in widths])]
    lines += [fmt_row(r) for r in rows]
    return "\n".join(lines)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    store = TaskStore()

    # ----------------------------
    # ADD
    # ----------------------------
    if args.cmd == "add":
        task = store.add(title=args.title, priority=args.priority)
        if args.json:
            print(json.dumps({"ok": True, "task": _task_to_dict(task)}, indent=2), flush=True)
            return 0
        print(f"Added [{task.id}] {task.title} ({task.priority})")
        return 0

    # ----------------------------
    # LIST
    # ----------------------------
    if args.cmd == "list":
        tasks = store.list()

        # filtering
        if getattr(args, "priority", None):
            tasks = [t for t in tasks if t.priority == args.priority]

        if getattr(args, "completed", False):
            tasks = [t for t in tasks if t.completed]

        if getattr(args, "pending", False):
            tasks = [t for t in tasks if not t.completed]

        # sorting
        reverse = getattr(args, "desc", False)
        sort_key = getattr(args, "sort", "id")

        if sort_key == "id":
            tasks = sorted(tasks, key=lambda t: t.id, reverse=reverse)
        elif sort_key == "title":
            tasks = sorted(tasks, key=lambda t: t.title.lower(), reverse=reverse)
        elif sort_key == "priority":
            order = {"low": 0, "medium": 1, "high": 2}
            tasks = sorted(tasks, key=lambda t: order.get(t.priority, 99), reverse=reverse)
        elif sort_key == "status":
            tasks = sorted(tasks, key=lambda t: t.completed, reverse=reverse)

        # JSON output MUST happen even when tasks is empty
        if args.json:
            print(json.dumps({"ok": True, "tasks": [_task_to_dict(t) for t in tasks]}, indent=2), flush=True)
            return 0

        # human output
        if not tasks:
            any_filter = bool(
                getattr(args, "priority", None)
                or getattr(args, "completed", False)
                or getattr(args, "pending", False)
            )
            print("No tasks match your filters." if any_filter else "No tasks yet.")
            return 0

        print(_render_table(tasks))
        return 0

    # ----------------------------
    # COMPLETE
    # ----------------------------
    if args.cmd == "complete":
        ok = store.complete(args.id)
        if args.json:
            print(json.dumps({"ok": ok, "action": "complete", "id": args.id}, indent=2), flush=True)
            return 0
        print("Marked complete." if ok else "Task not found.")
        return 0

    # ----------------------------
    # DELETE
    # ----------------------------
    if args.cmd == "delete":
        ok = store.delete(args.id)
        if args.json:
            print(json.dumps({"ok": ok, "action": "delete", "id": args.id}, indent=2), flush=True)
            return 0
        print("Deleted." if ok else "Task not found.")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())