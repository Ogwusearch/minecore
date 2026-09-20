#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

STATUS=0

echo "==> Backend tests"
if [ -d apps/api/.venv ]; then
  (
    cd apps/api
    # shellcheck disable=SC1091
    . .venv/bin/activate
    cd "$ROOT"
    pytest
  ) || STATUS=1
else
  echo "• apps/api/.venv missing — run 'make setup' first"
  STATUS=1
fi

echo
echo "==> Frontend tests"
(
  cd apps/web
  npm run test --silent
) || STATUS=1

exit "$STATUS"
