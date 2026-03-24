from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.models import Library
from app.schemas.schemas import LibraryCreate, LibraryOut
from app.services.scanner import scan_library

router = APIRouter(prefix="/libraries", tags=["libraries"])


@router.get("", response_model=list[LibraryOut])
def list_libraries(_: object = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.scalars(select(Library)).all()


@router.post("", response_model=LibraryOut)
def create_library(payload: LibraryCreate, _: object = Depends(get_current_user), db: Session = Depends(get_db)):
    exists = db.scalar(select(Library).where(Library.path == payload.path))
    if exists:
        raise HTTPException(status_code=400, detail="Library path already added")
    lib = Library(**payload.model_dump())
    db.add(lib)
    db.commit()
    db.refresh(lib)
    return lib


@router.post("/{library_id}/scan")
def scan(library_id: int, _: object = Depends(get_current_user), db: Session = Depends(get_db)):
    library = db.get(Library, library_id)
    if not library:
        raise HTTPException(status_code=404, detail="Library not found")
    count = scan_library(db, library)
    return {"discovered": count}
