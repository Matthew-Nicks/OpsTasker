# OpsTasker

[![Tests](https://github.com/Matthew-Nicks/OpsTasker/actions/workflows/tests.yml/badge.svg)](https://github.com/Matthew-Nicks/OpsTasker/actions/workflows/tests.yml)

A lightweight, production-style Python command-line task manager that demonstrates clean CLI architecture, persistent storage, and modern Python packaging practices.

---

## 🚀 Key Features

- Add, list, complete, and delete tasks  
- Priority levels (low, medium, high)  
- Filtering by priority and completion status  
- Multiple sorting strategies  
- Machine-readable JSON output mode  
- Persistent local storage  
- Modern `pyproject.toml` packaging  
- Editable install support  
- Automated test suite with GitHub Actions CI  

---

## 🧰 Installation

Clone the repository:

```bash
git clone https://github.com/Matthew-Nicks/OpsTasker.git
cd OpsTasker

Create and activate a virtual environment.

Windows
python -m venv .venv
.venv\Scripts\activate
macOS / Linux
python -m venv .venv
source .venv/bin/activate

Install in editable mode:

pip install -e .
📋 Quick Start
Add a task
opstasker add "Finish report" --priority high
List tasks
opstasker list
🔍 Filtering

Filter by priority:

opstasker list --priority high

Show only completed tasks:

opstasker list --completed

Show only pending tasks:

opstasker list --pending
🔃 Sorting

Sort by id (default):

opstasker list --sort id

Sort by priority descending:

opstasker list --sort priority --desc

Sort by title:

opstasker list --sort title

Sort by status:

opstasker list --sort status
🧾 JSON Output Mode

For automation and scripting, use the global --json flag (must come before the subcommand):

opstasker --json list

Example with filtering and sorting:

opstasker --json list --priority high --sort title
🧪 Running Tests
pytest -q

Tests run automatically on every push via GitHub Actions.

🗂 Project Structure
OpsTasker/
├── src/opstasker/
│   ├── cli.py
│   ├── models.py
│   └── storage.py
├── data/
├── tests/
├── .github/workflows/
├── pyproject.toml
└── README.md
🛠 Roadmap

Planned enhancements:

Due dates and reminders

Task editing

Export/import functionality

Improved table formatting

Expanded test coverage

📄 License

This project is provided for educational and portfolio purposes.