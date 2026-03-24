from datetime import datetime
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    is_admin: bool

    class Config:
        from_attributes = True


class LibraryCreate(BaseModel):
    name: str
    path: str
    media_type: str
    auto_refresh: bool = True


class LibraryOut(BaseModel):
    id: int
    name: str
    path: str
    media_type: str
    auto_refresh: bool

    class Config:
        from_attributes = True


class SubtitleOut(BaseModel):
    id: int
    lang: str
    file_path: str

    class Config:
        from_attributes = True


class MediaOut(BaseModel):
    id: int
    library_id: int
    title: str
    media_type: str
    file_path: str
    overview: str
    poster_url: str
    backdrop_url: str
    duration_seconds: int
    codec: str
    subtitles: list[SubtitleOut] = []

    class Config:
        from_attributes = True


class HistoryUpdate(BaseModel):
    media_id: int
    progress_seconds: int
    completed: bool = False


class HistoryOut(BaseModel):
    media_id: int
    progress_seconds: int
    completed: bool
    updated_at: datetime

    class Config:
        from_attributes = True
