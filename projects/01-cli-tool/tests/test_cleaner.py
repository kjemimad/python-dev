from pathlib import Path

import pytest

from cleanit.cleaner import FolderNotFoundError, NothingToUndoError, clean, undo


@pytest.fixture
def downloads(tmp_path: Path) -> Path:
    """Create a temporary downloads folder with sample files."""
    folder = tmp_path / "downloads"
    folder.mkdir()
    (folder / "photo.jpg").write_text("fake image", encoding="utf-8")
    (folder / "rapport.pdf").write_text("fake pdf", encoding="utf-8")
    (folder / "video.mp4").write_text("fake video", encoding="utf-8")
    (folder / "script.py").write_text("fake script", encoding="utf-8")
    (folder / "fichier.xyz").write_text("fake unknown", encoding="utf-8")

    return folder

@pytest.fixture(autouse=True)
def reset_history(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Redirect history file to a temporary location for each test."""
    history_dir = tmp_path / ".cleanit"
    history_dir.mkdir()
    history_file = history_dir / "history.json"
    history_file.write_text("[]", encoding="utf-8")
    monkeypatch.setattr("cleanit.history.HISTORY_FILE", history_file)

def test_clean_moves_files_to_correct_folders(downloads: Path) -> None:
    clean(downloads)
    assert (downloads / "Images" / "photo.jpg").exists()
    assert (downloads / "Documents" / "rapport.pdf").exists()
    assert (downloads / "Videos" / "video.mp4").exists()
    assert (downloads / "Code" / "script.py").exists()
    assert (downloads / "Other" / "fichier.xyz").exists()

def test_clean_removes_files_from_root(downloads: Path) -> None:
    clean(downloads)
    assert not (downloads / "photo.jpg").exists()
    assert not (downloads / "rapport.pdf").exists()
    assert not (downloads / "video.mp4").exists()

def test_clean_dry_run_does_not_move_files(downloads: Path) -> None:
    moves = clean(downloads, dry_run=True)
    assert (downloads / "photo.jpg").exists()
    assert (downloads / "rapport.pdf").exists()
    assert len(moves) == 5

def test_clean_dry_run_does_not_save_history(
    downloads: Path,
    tmp_path: Path,
) -> None:
    clean(downloads, dry_run=True)
    history_file = tmp_path / ".cleanit" / "history.json"
    import json
    content = json.loads(history_file.read_text(encoding="utf-8"))
    assert content == []

def test_clean_returns_moves_dict(downloads: Path) -> None:
    moves = clean(downloads)
    assert isinstance(moves, dict)
    assert len(moves) == 5

def test_clean_raises_on_missing_folder() -> None:
    with pytest.raises(FolderNotFoundError):
        clean(Path("/dossier/qui/nexiste/pas"))

def test_clean_ignore_subfolders(downloads: Path) -> None:
    subfolder = downloads / "subfolder"
    subfolder.mkdir()
    moves = clean(downloads)
    assert str(subfolder) not in moves.values()
    assert str(subfolder) not in moves.keys()


def test_clean_empty_folder_returns_empty_dict(tmp_path: Path) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    moves = clean(empty)
    assert moves == {}

def test_undo_restores_files_to_original_location(downloads: Path) -> None:
    clean(downloads)
    undo()
    assert (downloads / "photo.jpg").exists()
    assert (downloads / "rapport.pdf").exists()
    assert (downloads / "video.mp4").exists()


def test_removes_files_from_category_folders(downloads: Path) -> None:
    clean(downloads)
    undo()
    assert not (downloads / "Images" / "photo.jpg").exists()
    assert not (downloads / "Documents" / "rapport.pdf").exists()

def test_undo_raises_when_no_history(downloads: Path) -> None:
    with pytest.raises(NothingToUndoError):
        undo()

def test_undo_returns_reversed_moves(downloads: Path) -> None:
    clean(downloads)
    reversed_moves = undo()
    assert isinstance(reversed_moves, dict)
    assert len(reversed_moves) == 5

