from pathlib import Path

import pytest
from typer.testing import CliRunner

from cleanit.cli import app

runner = CliRunner()

@pytest.fixture
def downloads(tmp_path: Path) -> Path:
    """Create a tmporary downloads folder with sample files."""
    folder = tmp_path / "Downloads"
    folder.mkdir()
    (folder / "photo.jpg").write_text("fake image", encoding="utf-8")
    (folder / "document.pdf").write_text("fake pdf", encoding="utf-8")
    (folder / "music.mp3").write_text("fake music", encoding="utf-8")
    return folder


@pytest.fixture(autouse=True)
def reset_history(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Redirect history file to a tmporary location for each test."""
    history_dir = tmp_path / ".cleanit"
    history_dir.mkdir()
    history_file = history_dir / "history.json"
    history_file.write_text("[]", encoding="utf-8")
    monkeypatch.setattr("cleanit.history.HISTORY_FILE", history_file)


def test_clean_command_exits_with_zero(downloads: Path) -> None:
    result = runner.invoke(app, ["clean", str(downloads)])
    assert result.exit_code == 0


def test_clean_command_moves_files(downloads: Path) -> None:
    runner.invoke(app, ["clean", str(downloads)])
    assert (downloads / "Images" / "photo.jpg").exists()
    assert (downloads / "Documents" / "document.pdf").exists()
    assert (downloads / "Audio" / "music.mp3").exists()


def test_clean_command_dry_run_does_not_move_files(downloads: Path) -> None:
    result = runner.invoke(app, ["clean", str(downloads), '--dry-run'])
    assert result.exit_code == 0
    assert (downloads / "photo.jpg").exists()
    assert (downloads / "document.pdf").exists()


def test_clean_command_dry_run_shows_preview(downloads: Path) -> None:
    result = runner.invoke(app, ["clean", str(downloads), "--dry-run"])
    assert "Preview" in result.output
    assert "would be moved" in result.output


def test_clean_command_shows_done_message(downloads: Path) -> None:
    result = runner.invoke(app, ["clean", str(downloads)])
    assert "organized" in result.output


def test_clean_command_fails_on_missing_folder() -> None:
    result = runner.invoke(app, ["clean", "/dossier/inexistant"])
    assert result.exit_code == 1


def test_clean_command_empty_folder_shows_no_files_message(
    tmp_path: Path,
) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    result = runner.invoke(app, ["clean", str(empty)])
    assert result.exit_code == 0
    assert "No files" in result.output


def test_undo_command_restores_files(downloads: Path) -> None:
    runner.invoke(app, ["clean", str(downloads)])
    result = runner.invoke(app, ["undo"])
    assert result.exit_code == 0
    assert (downloads / "photo.jpg").exists()


def test_undo_command_fails_when_no_history() -> None:
    result = runner.invoke(app, ["undo"])
    assert result.exit_code == 1


def test_undo_command_shows_restored_message(downloads: Path) -> None:
    runner.invoke(app, ["clean", str(downloads)])
    result = runner.invoke(app, ["undo"])
    assert "restored" in result.output


