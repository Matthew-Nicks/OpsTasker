# OpsTasker

A lightweight, professional Python command-line task manager designed to demonstrate clean CLI design, data persistence, and modern Python project structure.

---

## 🚀 Features

* Add, list, complete, and delete tasks
* Priority levels (low, medium, high)
* Filtering by priority and completion status
* Multiple sorting options
* Machine-readable JSON output mode
* Persistent local storage
* Modern `pyproject.toml` packaging
* Editable install support

---

## 🧰 Installation

Clone the repository:

```bash
git clone https://github.com/Matthew-Nicks/OpsTasker.git
cd OpsTasker
```

Create and activate a virtual environment:

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**

```bash
python -m venv .venv
source .venv/bin/activate
```

Install in editable mode:

```bash
pip install -e .
```

---

## 📋 Usage

### Add a task

```bash
opstasker add "Finish report" --priority high
```

### List tasks

```bash
opstasker list
```

---

## 🔍 Filtering

Filter by priority:

```bash
opstasker list --priority high
```

Show only completed tasks:

```bash
opstasker list --completed
```

Show only pending tasks:

```bash
opstasker list --pending
```

---

## 🔃 Sorting

Sort by id (default):

```bash
opstasker list --sort id
```

Sort by priority descending:

```bash
opstasker list --sort priority --desc
```

Sort by title:

```bash
opstasker list --sort title
```

Sort by status:

```bash
opstasker list --sort status
```

---

## 🧾 JSON Output Mode

For automation and scripting, use the global `--json` flag (must come before the subcommand):

```bash
opstasker --json list
```

Example with filtering and sorting:

```bash
opstasker --json list --priority high --sort title
```

---

## 🗂 Project Structure

```
OpsTasker/
├── src/opstasker/
│   ├── cli.py
│   ├── models.py
│   └── storage.py
├── data/
├── tests/
├── pyproject.toml
└── README.md
```

---

## 🛠 Future Improvements

* Due dates and reminders
* Pretty table output
* Task editing
* Export/import functionality
* Unit test coverage expansion

---

## 📄 License

This project is provided for educational and portfolio purposes.
