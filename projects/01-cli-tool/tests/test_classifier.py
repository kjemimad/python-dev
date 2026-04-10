from pathlib import Path

from cleanit.classifier import CATEGORIES, get_category


def test_jpg_returns_images() -> None:
    assert get_category(Path("photo.jpg")) == "Images"

def test_jpeg_returns_images() -> None:
    assert get_category(Path("photo.jpeg")) == "Images"

def test_pdf_returns_documents() -> None:
    assert get_category(Path("rapport.pdf")) == "Documents"


def test_mp4_returns_videos() -> None:
    assert get_category(Path("video.mp4")) == "Videos"


def test_mp3_returns_audio() -> None:
    assert get_category(Path("musique.mp3")) == "Audio"

def test_zip_returns_archives() -> None:
    assert get_category(Path("archive.zip")) == "Archives"


def test_py_returns_code() -> None:
    assert get_category(Path("script.py")) == "Code"


def test_unknown_extension_returns_other() -> None:
    assert get_category(Path("fichier.xyz")) == "Other"


def test_no_extension_returns_other() -> None:
    assert get_category(Path("fichier")) == "Other"

def test_uppercase_extension_is_normalized() -> None:
    assert get_category(Path("PHOTO.JPG")) == "Images"


def test_all_categories_have_at_least_one_extension() -> None:
    for category, extensions in CATEGORIES.items():
        assert len(extensions) > 0, f"{category} has no extensions"

def test_no_duplicate_extensions_across_categories() -> None:
    seen: dict[str, str] = {}
    for category, extensions in CATEGORIES.items():
        for ext in extensions:
            assert ext not in seen, (
                f"Extension {ext} appears in both {seen.get(ext)} and {category}"
            )
            seen[ext] = category
