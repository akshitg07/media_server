#!/usr/bin/env bash
set -euo pipefail

COMPOSE_CMD="docker compose"
if ! docker compose version >/dev/null 2>&1; then
  COMPOSE_CMD="docker-compose"
fi

echo "Using compose command: ${COMPOSE_CMD}"
${COMPOSE_CMD} down
${COMPOSE_CMD} build --no-cache backend
${COMPOSE_CMD} up -d --force-recreate backend frontend

echo "Backend image/container rebuilt."
echo "Check logs: ${COMPOSE_CMD} logs -f backend || docker logs -f media-server-api"
