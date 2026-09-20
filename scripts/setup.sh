#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> MineCore setup"

if [ ! -f .env ]; then
  cp .env.example .env
  echo "• Created .env from .env.example"
else
  echo "• .env already exists, leaving untouched"
fi

echo
echo "==> Backend (apps/api)"
cd apps/api
if [ ! -d .venv ]; then
  python3 -m venv .venv
  echo "• Created virtual environment"
fi
# shellcheck disable=SC1091
. .venv/bin/activate
pip install --upgrade pip >/dev/null
pip install -r requirements.txt
cd "$ROOT"

echo
echo "==> Frontend (apps/web)"
cd apps/web
if [ -f package-lock.json ]; then
  npm ci
else
  npm install
fi
cd "$ROOT"

echo
echo "==> Setup complete"
echo "Next:"
echo "  make docker-up"
echo "  make dev"
