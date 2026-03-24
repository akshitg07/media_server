# Media Server (Plex/Jellyfin-style, lightweight)

A production-oriented self-hosted media management and streaming app built with **FastAPI + React**, packaged for Docker.

## Features
- Folder-based libraries (movies / TV / music)
- Auto-scan media files and detect type heuristically
- TMDB metadata integration (title, overview, posters)
- Subtitle detection (`.srt`) and playback
- Smart stream mode: direct play vs HLS transcode via FFmpeg
- Login/JWT authentication and media progress tracking
- Search, continue watching row, dark Netflix-like UI
- SQLite by default, optional PostgreSQL via env var
- Dockerized backend and frontend

## Project Structure

```text
media_server/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── deps.py
│   │   │   ├── libraries.py
│   │   │   ├── media.py
│   │   │   └── stream.py
│   │   ├── core/config.py
│   │   ├── db/session.py
│   │   ├── models/models.py
│   │   ├── schemas/schemas.py
│   │   ├── services/
│   │   │   ├── auth.py
│   │   │   ├── metadata.py
│   │   │   ├── scanner.py
│   │   │   └── transcode.py
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/client.js
│   │   ├── components/
│   │   ├── context/AuthContext.jsx
│   │   ├── pages/
│   │   ├── styles/app.css
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## Backend API Endpoints
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/libraries`
- `POST /api/libraries`
- `POST /api/libraries/{id}/scan`
- `GET /api/media?q=&media_type=`
- `GET /api/media/{id}`
- `POST /api/media/history`
- `GET /api/media/{id}/subs/{sub_id}`
- `GET /api/stream/{id}/manifest`
- `GET /api/stream/{id}/direct`
- `GET /api/stream/{id}/hls/{segment}`

## Quick Start

### 1) Configure
```bash
cp .env.example .env
# edit .env
mkdir -p media backend/data transcode
```

### 2) Launch
```bash
docker compose up --build -d
```

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`

### 3) Create first user
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"admin123"}'
```

### 4) Add library and scan
1. Login in UI.
2. Use API tool (or curl) to create library path mapped in container (`/media/...`).
3. Trigger `POST /api/libraries/{id}/scan`.

## Hardware Acceleration Notes
This baseline defaults to software x264 transcoding. To enable NVIDIA/Intel acceleration:
- expose devices to container (`--gpus all` or `/dev/dri`)
- adapt FFmpeg command in `app/services/transcode.py` to use `h264_nvenc` or `h264_qsv`

## Plugin-Ready Extension Points
- Add plugin interfaces in `app/services/` for metadata providers, subtitle providers, and transcode strategies.
- Current modules are isolated and can be swapped via DI/factory pattern.

## Production Tips
- Use PostgreSQL by setting `POSTGRES_URL`.
- Put API behind reverse proxy (Nginx/Traefik) with HTTPS.
- Set strong `SECRET_KEY`.
- Use persistent volumes for `/app/data`, `/media`, `/transcode`.


## Troubleshooting 500 on `/api/auth/register`
- Ensure database path is writable by container/user (`./backend/data` mapped to `/app/data`).
- Check backend logs: `docker logs -f media-server-api`.
- Rebuild after dependency updates: `docker compose build --no-cache backend && docker compose up -d`.
- This project now uses built-in PBKDF2 password hashing (no bcrypt/passlib runtime dependency), so stale cached images can still show old bcrypt errors until rebuilt.
- If your database file is corrupted during early tests, stop stack and remove `backend/data/media_server.db` to reinitialize.
