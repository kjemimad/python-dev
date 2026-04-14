# cleanit

A CLI tool to automatically organize your downloads folder by file type.

## Features

- Organizes files into categorized subfolders (Images, Documents, Videos, Audio, Archives, Code, Executables, Other)
- Dry-run mode to preview changes before applying them
- Undo support to reverse the last cleaning operation
- Clean terminal output with rich tables

## Installation

```bash
git clone https://github.com/kjemimad/python-dev.git
cd python-dev/projects/01-cli-tool
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Usage

### Organize a folder

```bash
cleanit clean ~/Downloads
```

### Preview without moving files

```bash
cleanit clean ~/Downloads --dry-run
```

### Undo the last operation

```bash
cleanit undo
```

### Help

```bash
cleanit --help
cleanit clean --help
```

## Project structure

    cleanit/
    ├── src/
    │   └── cleanit/
    │       ├── cli.py          # CLI interface — typer commands
    │       ├── cleaner.py      # Core logic — orchestrates cleaning and undo
    │       ├── classifier.py   # File classification by extension
    │       └── history.py      # Operation history persistence
    ├── tests/
    │   ├── test_classifier.py
    │   ├── test_cleaner.py
    │   ├── test_cli.py
    │   └── test_history.py
    ├── pyproject.toml
    └── README.md

## Code quality

| Tool | Purpose |
|------|---------|
| ruff | Linting and formatting |
| mypy | Static type checking |
| pytest | Unit and integration tests |
| pytest-cov | Test coverage reporting |

Run all checks :

```bash
ruff check src/ tests/
mypy src/
pytest
```

## Stack

- [Typer](https://typer.tiangolo.com) — CLI framework
- [Rich](https://rich.readthedocs.io) — Terminal formatting
- [pytest](https://pytest.org) — Testing framework