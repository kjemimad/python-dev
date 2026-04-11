import json
from pathlib import Path

import pytest

from cleanit.history import (
    clear_last_operation,
    get_last_operation,
    save_operation,
)


@pytest.fixture
def history_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """ Create a temporary history file for each test. """
    history_dir = tmp_path / ".cleanit"
    history_dir.mkdir()
    history_file = history_dir / "history.json"
    history_file.write_text("[]", encoding="utf-8")
    monkeypatch.setattr("cleanit.history.HISTORY_FILE", history_file)
    return history_file

def test_save_operation_creates_entry(history_file: Path) -> None:
    moves = {
        "/downloads/photo.jpg": "/downloads/Images/photo.jpg",
    }
    save_operation(moves)
    content = json.loads(history_file.read_text(encoding="utf-8"))
    assert len(content) == 1
    assert content[0]["moves"] == moves

def test_save_multiple_operations(history_file: Path) -> None:
    save_operation({"downloads/photo.jpg": "downloads/Images/photo.jpg"})
    save_operation({"downloads/document.pdf": "downloads/Documents/document.pdf"})
    content = json.loads(history_file.read_text(encoding="utf-8"))
    assert len(content) == 2

def test_save_operation_records_timestamp(history_file: Path) -> None:
    save_operation({"downloads/photo.jpg": "downloads/Images/photo.jpg"})
    content = json.loads(history_file.read_text(encoding="utf-8"))
    assert "timestamp" in content[0]
    assert len(content[0]["timestamp"]) > 0

def test_get_last_operation_returns_last_moves(history_file: Path) -> None:
    first = {"downloads/photo.jpg": "downloads/Images/photo.jpg"}
    second = {"downloads/document.pdf": "downloads/Documents/document.pdf"}
    save_operation(first)
    save_operation(second)
    result = get_last_operation()
    assert result == second

def test_clear_last_operation_returns_none_when_empty(history_file: Path) -> None:
    result = get_last_operation()
    assert result is None

def test_clear_last_operation_removes_last_entry(history_file: Path) -> None:
    first = {"downloads/photo.jpg": "downloads/Images/photo.jpg"}
    second = {"downloads/document.pdf": "downloads/Documents/document.pdf"}
    save_operation(first)
    save_operation(second)
    clear_last_operation()
    content = json.loads(history_file.read_text(encoding="utf-8"))
    assert len(content) == 1
    assert content[0]["moves"] == first

