from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from cleanit.cleaner import FolderNotFoundError, NothingToUndoError, clean, undo

app = typer.Typer(
    name="cleanit",
    help="Automatically organize your downloads folder.",
    add_completion=False,
)

console = Console()
error_console = Console(stderr=True, style="red")

@app.command("clean")
def clean_command(
    folder: Path = typer.Argument(
        default=Path.home() / "Downloads",
        help="The folder to clean.",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-d",
        help="Simulate the cleaning operation without moving any files.",
    ),
) -> None:
    """scan a folder and organize files into categorized subfolders."""
    try:
        moves = clean(folder, dry_run=dry_run)
    except FolderNotFoundError as e:
        error_console.print(f"Error: {e}")
        raise typer.Exit(code=1) from e

    if not moves:
        console.print("[yellow]No files to organize.[/yellow]")
        return

    table = Table(title="cleanit - Preview" if dry_run else "cleanit - Done")
    table.add_column("File", style="cyan")
    table.add_column("Destination", style="green")

    for source, destination in moves.items():
        table.add_row(
            Path(source).name,
            Path(destination).parent.name,
        )

    console.print(table)

    if dry_run:
        console.print(
        f"\n[yellow]Dry run - {len(moves)} files would be moved.[/yellow]"
        )
    else:
        console.print(
        f"\n[green]Done - {len(moves)} files organized.[/green]"
        )

@app.command("undo")
def undo_command() -> None:
    """Reverse the most recent cleaning operation."""
    try:
        reversed_moves = undo()
    except NothingToUndoError as e:
        error_console.print(f"Error: {e}")
        raise typer.Exit(code=1) from e

    table = Table(title="cleanit - Undo")
    table.add_column("File", style="cyan")
    table.add_column("Restored to", style="green")

    for source, destination in reversed_moves.items():
        table.add_row(
            Path(source).name,
            Path(destination).parent.name,
        )

    console.print(table)
    console.print(f"\n[green]Done - {len(reversed_moves)} files restored.[/green]")

def main() -> None:
    """Entry point for the CLI."""
    app()
