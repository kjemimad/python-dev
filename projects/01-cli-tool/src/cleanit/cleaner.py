from pathlib import Path

from cleanit.classifier import get_category
from cleanit.history import clear_last_operation, get_last_operation, save_operation


class NothingToUndoError(Exception):
    """Raised when undo is requested but no operations are recorded."""

class FolderNotFoundError(Exception):
    """Raised when the target folder does not exist."""

def clean(folder: Path, dry_run: bool = False) -> dict[str, str]:
    """Scan a folder and move files into categorized subfolders.

    Args:
        folder: The folder to clean.
        dry_run: If True, simulate the opertaion without moving any files.

    Returns:
        A dictionary mapping source paths to destination paths.

    Raises:
        FolderNotFoundError: If the target folder does not exist.
    """
    if not folder.exists():
        raise FolderNotFoundError(f"Folder {folder} does not exist")

    moves: dict[str, str] = {}

    for file in folder.iterdir():
        if not file.is_file():
            continue

        category = get_category(file)
        destination_dir = folder / category
        destination = destination_dir / file.name

        moves[str(file)] = str(destination)

        if not dry_run:
            destination_dir.mkdir(exist_ok=True)
            file.rename(destination)

    if not dry_run and moves:
        save_operation(moves)

    return moves


def undo() -> dict[str, str]:
    """Reverse the most recent cleaning operation.

    Returns:
        A dictionary mapping files back to their original locations.

    Raises:
        NothingToUndoError: if no operations are recored in history.
    """
    last_operation = get_last_operation()
    if last_operation is None:
        raise NothingToUndoError("No operations to undo")

    reversed_moves: dict[str, str] = {}

    for source, destination in last_operation.items():
        source_path = Path(source)
        destination_path = Path(destination)

        if destination_path.exists():
            destination_path.rename(source_path)
            reversed_moves[str(destination_path)] = str(source_path)

    clear_last_operation()
    return reversed_moves
