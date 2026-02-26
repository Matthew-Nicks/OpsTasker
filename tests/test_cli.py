import json
import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable

def run_cmd(args, env=None):
    """Run opstasker via python -m to avoid entrypoint issues."""
    result = subprocess.run(
        [PYTHON, "-m", "opstasker.cli", *args],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        env=env,
    )
    return result

def test_list_json_returns_structure(tmp_path):
    # isolate data file for this test run
    env = os.environ.copy()
    env["OPSTASKER_DATA_DIR"] = str(tmp_path)

    r = run_cmd(["--json", "list"], env=env)
    assert r.returncode == 0
    payload = json.loads(r.stdout)
    assert payload["ok"] is True
    assert "tasks" in payload
    assert isinstance(payload["tasks"], list)

def test_add_then_list_contains_task(tmp_path):
    env = os.environ.copy()
    env["OPSTASKER_DATA_DIR"] = str(tmp_path)

    r1 = run_cmd(["--json", "add", "Test task", "--priority", "high"], env=env)
    assert r1.returncode == 0
    p1 = json.loads(r1.stdout)
    assert p1["ok"] is True
    assert p1["task"]["title"] == "Test task"

    r2 = run_cmd(["--json", "list"], env=env)
    assert r2.returncode == 0
    p2 = json.loads(r2.stdout)
    assert any(t["title"] == "Test task" for t in p2["tasks"])