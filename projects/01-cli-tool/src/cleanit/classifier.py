from pathlib import Path

CATEGORIES: dict[str, list[str]] = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".md", ".xlsx", ".csv", ".pptx"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".7z", ".bz2"],
    "Code": [".py", ".js", ".ts", ".html", ".css", ".json", ".yml", ".yaml", ".sh"],
    "Executables": [".exe", ".msi", ".deb", ".AppImage"],
}




def get_category(file: Path) -> str:
    """Get the category of a file based on its extension.

    Args:
        file (Path): The file to classify.

    Returns:
        The category name as a string. Returns 'Other' if no match is found.
    """

    extension = file.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return "Other"
