from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.models import MediaItem, WatchHistory
from app.schemas.schemas import MediaOut, HistoryUpdate, HistoryOut
from app.services.metadata import fetch_tmdb_metadata

router = APIRouter(prefix="/media", tags=["media"])


@router.get("", response_model=list[MediaOut])
def list_media(
    q: str | None = Query(default=None),
    media_type: str | None = Query(default=None),
    _: object = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = select(MediaItem).options(joinedload(MediaItem.subtitles))
    if media_type:
        stmt = stmt.where(MediaItem.media_type == media_type)
    if q:
        stmt = stmt.where(MediaItem.title.ilike(f"%{q}%"))
    return db.scalars(stmt.order_by(MediaItem.created_at.desc())).unique().all()


@router.get("/{media_id}", response_model=MediaOut)
def get_media(media_id: int, _: object = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.scalar(select(MediaItem).options(joinedload(MediaItem.subtitles)).where(MediaItem.id == media_id))
    if not item:
        raise HTTPException(status_code=404, detail="Media item not found")
    return item


@router.post("/history", response_model=HistoryOut)
def update_history(payload: HistoryUpdate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    media = db.get(MediaItem, payload.media_id)
    if not media:
        raise HTTPException(status_code=404, detail="Media item not found")

    entry = db.scalar(
        select(WatchHistory).where(WatchHistory.user_id == user.id, WatchHistory.media_id == payload.media_id)
    )
    if not entry:
        entry = WatchHistory(user_id=user.id, media_id=payload.media_id)
        db.add(entry)

    entry.progress_seconds = payload.progress_seconds
    entry.completed = payload.completed
    db.commit()
    db.refresh(entry)
    return entry


@router.get("/{media_id}/subs/{sub_id}")
def get_subtitle(media_id: int, sub_id: int, _: object = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.get(MediaItem, media_id)
    if not item:
        raise HTTPException(status_code=404, detail="Media item not found")
    sub = next((s for s in item.subtitles if s.id == sub_id), None)
    if not sub or not Path(sub.file_path).exists():
        raise HTTPException(status_code=404, detail="Subtitle not found")
    return Path(sub.file_path).read_text(encoding="utf-8", errors="ignore")


@router.post("/{media_id}/metadata/refresh", response_model=MediaOut)
async def refresh_metadata(media_id: int, _: object = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.get(MediaItem, media_id)
    if not item:
        raise HTTPException(status_code=404, detail="Media item not found")

    data = await fetch_tmdb_metadata(item.title, item.media_type)
    if data:
        item.title = data.get("title", item.title)
        item.overview = data.get("overview", item.overview)
        item.poster_url = data.get("poster_url", item.poster_url)
        item.backdrop_url = data.get("backdrop_url", item.backdrop_url)
        db.commit()
        db.refresh(item)
    return item
