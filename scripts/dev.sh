#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [ ! -f .env ]; then
  echo "Missing .env — run 'make setup' first" >&2
  exit 1
fi

cleanup() {
  echo
  echo "==> Shutting down dev processes"
  kill 0 2>/dev/null || true
}
trap cleanup EXIT INT TERM

echo "==> Backend  http://localhost:8000"
(
  cd apps/api
  # shellcheck disable=SC1091
  . .venv/bin/activate
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
) &

echo "==> Frontend http://localhost:5173"
(
  cd apps/web
  npm run dev
) &

wait
