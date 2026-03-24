#!/usr/bin/env bash
set -euo pipefail

COMPOSE_CMD="docker compose"
if ! docker compose version >/dev/null 2>&1; then
  COMPOSE_CMD="docker-compose"
fi

echo "Using compose command: ${COMPOSE_CMD}"
${COMPOSE_CMD} down
${COMPOSE_CMD} build --no-cache backend frontend
${COMPOSE_CMD} up -d --force-recreate backend frontend

echo "Backend + frontend images/containers rebuilt."
echo "Check backend logs: docker logs -f media-server-api"
echo "Check frontend logs: docker logs -f media-server-ui"
