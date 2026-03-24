# Media Server (Plex/Jellyfin-style, lightweight)

A production-oriented self-hosted media management and streaming app built with **FastAPI + React**, packaged for Docker.

## Features
- Folder-based libraries (movies / TV / music)
- Auto-scan media files and detect type heuristically
- TMDB metadata integration (title, overview, posters)
- Subtitle detection (`.srt`) and playback
- Smart stream mode: direct play vs HLS transcode via FFmpeg
- Open local access (no login required) and media progress tracking
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
Use the command your host supports:
```bash
# Docker Compose v2 plugin
docker compose up --build -d

# or legacy binary
docker-compose up --build -d
```

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`

### 3) Add library and scan
1. Use API tool (or curl) to create library path mapped in container (`/media/...`).
2. Trigger `POST /api/libraries/{id}/scan`.

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


## Troubleshooting
- Ensure database path is writable by container/user (`./backend/data` mapped to `/app/data`).
- Rebuild after dependency updates: `docker compose build --no-cache backend && docker compose up -d`.
- Check health endpoint: `curl http://localhost:8000/health`.
- If your database file is corrupted during early tests, stop stack and remove `backend/data/media_server.db` to reinitialize.

### Rebuild backend safely (recommended if auth errors persist)
```bash
./scripts/redeploy_backend.sh
```

Backend root now returns a small API landing payload; primary API routes remain under `/api` and health is `/health`.
