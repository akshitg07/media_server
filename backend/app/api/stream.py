from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import get_settings
from app.db.session import get_db
from app.models.models import MediaItem
from app.services.transcode import needs_transcode, create_hls

router = APIRouter(prefix="/stream", tags=["stream"])
settings = get_settings()


@router.get("/{media_id}/direct")
def direct_play(media_id: int, _: object = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.get(MediaItem, media_id)
    if not item:
        raise HTTPException(status_code=404, detail="Media item not found")

    path = Path(item.file_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path)


@router.get("/{media_id}/manifest")
def hls_manifest(media_id: int, _: object = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.get(MediaItem, media_id)
    if not item:
        raise HTTPException(status_code=404, detail="Media item not found")

    src = Path(item.file_path)
    if not src.exists():
        raise HTTPException(status_code=404, detail="File not found")

    if not needs_transcode(str(src)):
        return {"mode": "direct", "url": f"/api/stream/{media_id}/direct"}

    output_dir = Path(settings.transcode_dir) / str(media_id)
    playlist = output_dir / "index.m3u8"
    if not playlist.exists():
        create_hls(str(src), str(output_dir))

    return {"mode": "hls", "url": f"/api/stream/{media_id}/hls/index.m3u8"}


@router.get("/{media_id}/hls/{segment:path}")
def hls_segment(media_id: int, segment: str, _: object = Depends(get_current_user)):
    path = Path(settings.transcode_dir) / str(media_id) / segment
    if not path.exists():
        raise HTTPException(status_code=404, detail="Segment not found")
    return FileResponse(path)
