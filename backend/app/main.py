from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, libraries, media, stream
from app.core.config import get_settings
from app.db.session import Base, engine

settings = get_settings()
app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    Path("./data").mkdir(exist_ok=True)
    Path(settings.transcode_dir).mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth.router, prefix="/api")
app.include_router(libraries.router, prefix="/api")
app.include_router(media.router, prefix="/api")
app.include_router(stream.router, prefix="/api")
