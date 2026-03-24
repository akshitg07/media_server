from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.models import Library, MediaItem, Subtitle

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi"}
SUB_EXTENSIONS = {".srt"}


def infer_media_type(path: Path) -> str:
    parts = [p.lower() for p in path.parts]
    if "tv" in parts or "shows" in parts:
        return "tv"
    if "music" in parts:
        return "music"
    return "movie"


def scan_library(db: Session, library: Library) -> int:
    base = Path(library.path)
    if not base.exists() or not base.is_dir():
        return 0

    discovered = 0
    for file in base.rglob("*"):
        if file.suffix.lower() not in VIDEO_EXTENSIONS:
            continue
        title = file.stem.replace(".", " ").replace("_", " ")

        existing = db.scalar(
            select(MediaItem).where(MediaItem.library_id == library.id, MediaItem.file_path == str(file))
        )
        if existing:
            continue

        media = MediaItem(
            library_id=library.id,
            file_path=str(file),
            title=title,
            media_type=infer_media_type(file),
        )
        db.add(media)
        db.flush()

        for sub in file.parent.iterdir():
            if sub.suffix.lower() in SUB_EXTENSIONS and sub.stem.startswith(file.stem):
                db.add(Subtitle(media_id=media.id, file_path=str(sub), lang="und"))

        discovered += 1

    db.commit()
    return discovered
