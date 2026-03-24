from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    history: Mapped[list["WatchHistory"]] = relationship(back_populates="user")


class Library(Base):
    __tablename__ = "libraries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    path: Mapped[str] = mapped_column(String(1024), unique=True)
    media_type: Mapped[str] = mapped_column(String(24))
    auto_refresh: Mapped[bool] = mapped_column(Boolean, default=True)

    items: Mapped[list["MediaItem"]] = relationship(back_populates="library", cascade="all, delete")


class MediaItem(Base):
    __tablename__ = "media_items"
    __table_args__ = (UniqueConstraint("library_id", "file_path", name="uq_library_file"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    library_id: Mapped[int] = mapped_column(ForeignKey("libraries.id"), index=True)
    file_path: Mapped[str] = mapped_column(String(2048), index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    media_type: Mapped[str] = mapped_column(String(24), index=True)
    overview: Mapped[str] = mapped_column(Text, default="")
    poster_url: Mapped[str] = mapped_column(String(1024), default="")
    backdrop_url: Mapped[str] = mapped_column(String(1024), default="")
    duration_seconds: Mapped[int] = mapped_column(Integer, default=0)
    codec: Mapped[str] = mapped_column(String(64), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    library: Mapped[Library] = relationship(back_populates="items")
    subtitles: Mapped[list["Subtitle"]] = relationship(back_populates="media", cascade="all, delete")
    watch_entries: Mapped[list["WatchHistory"]] = relationship(back_populates="media")


class Subtitle(Base):
    __tablename__ = "subtitles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    media_id: Mapped[int] = mapped_column(ForeignKey("media_items.id"), index=True)
    lang: Mapped[str] = mapped_column(String(12), default="und")
    file_path: Mapped[str] = mapped_column(String(2048))

    media: Mapped[MediaItem] = relationship(back_populates="subtitles")


class WatchHistory(Base):
    __tablename__ = "watch_history"
    __table_args__ = (UniqueConstraint("user_id", "media_id", name="uq_user_media_history"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    media_id: Mapped[int] = mapped_column(ForeignKey("media_items.id"), index=True)
    progress_seconds: Mapped[int] = mapped_column(Integer, default=0)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Mapped[User] = relationship(back_populates="history")
    media: Mapped[MediaItem] = relationship(back_populates="watch_entries")
