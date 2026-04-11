import json
from datetime import datetime
from pathlib import Path
from typing import TypedDict

HISTORY_FILE = Path.home() / ".cleanit" / "history.json"


class Operation(TypedDict):
    """Represent a single cleaning operation stored in history."""

    timestamp: str
    moves: dict[str, str]


def _ensure_history_file() -> None:
    """Create the history file and its parent directory if they don't exist."""
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not HISTORY_FILE.exists():
        HISTORY_FILE.write_text("[]", encoding="utf-8")


def _parse_operation(entry: object) -> Operation | None:
    """Parse and validate a raw JSON entry into an Operation.

    Args:
        entry: A raw object parsed from JSON.

    Returns:
        An Operation if the entry is valid, None otherwise.
    """
    if not isinstance(entry, dict):
        return None
    timestamp = entry.get("timestamp")
    moves = entry.get("moves")
    if not isinstance(timestamp, str):
        return None
    if not isinstance(moves, dict):
        return None
    validated_moves: dict[str, str] = {}
    for key, value in moves.items():
        if not isinstance(key, str) or not isinstance(value, str):
            return None
        validated_moves[key] = value
    return Operation(timestamp=timestamp, moves=validated_moves)


def _load_history() -> list[Operation]:
    """Read and parse the history file.

    Returns:
        A list of valid Operation dictionaries.
    """
    content = HISTORY_FILE.read_text(encoding="utf-8")
    raw = json.loads(content)
    if not isinstance(raw, list):
        return []
    operations: list[Operation] = []
    for entry in raw:
        operation = _parse_operation(entry)
        if operation is not None:
            operations.append(operation)
    return operations


def save_operation(moves: dict[str, str]) -> None:
    """Save a cleaning operation to the history file.

    Args:
        moves: A dictionary mapping source paths to destination paths.
    """
    _ensure_history_file()
    history = _load_history()
    operation = Operation(
        timestamp=datetime.now().isoformat(),
        moves=moves,
    )
    history.append(operation)
    HISTORY_FILE.write_text(
        json.dumps(history, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def get_last_operation() -> dict[str, str] | None:
    """Return the most recent cleaning operation, or None if history is empty.

    Returns:
        A dictionary mapping source paths to destination paths,
        or None if no operations have been recorded.
    """
    _ensure_history_file()
    history = _load_history()
    if not history:
        return None
    return history[-1]["moves"]


def clear_last_operation() -> None:
    """Remove the most recent operation from the history file."""
    _ensure_history_file()
    history = _load_history()
    if history:
        history.pop()
    HISTORY_FILE.write_text(
        json.dumps(history, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
