.RECIPEPREFIX = >

.PHONY: help setup dev test lint format typecheck \
        docker-up docker-down docker-logs \
        migrate seed db-reset clean

help:
> @echo "MineCore development commands"
> @echo ""
> @echo "  make setup        Install backend + frontend dependencies"
> @echo "  make dev          Run frontend and backend in development mode"
> @echo "  make test         Run all tests"
> @echo "  make lint         Lint backend + frontend"
> @echo "  make format       Format backend + frontend"
> @echo "  make typecheck    Run mypy (backend)"
> @echo "  make docker-up    Start PostgreSQL"
> @echo "  make docker-down  Stop PostgreSQL"
> @echo "  make docker-logs  Tail PostgreSQL logs"
> @echo "  make migrate      Apply database migrations"
> @echo "  make seed         Apply database seed data"
> @echo "  make db-reset     Drop and recreate the database (DESTRUCTIVE)"
> @echo "  make clean        Remove build artifacts and caches"

setup:
> @bash scripts/setup.sh

dev:
> @bash scripts/dev.sh

test:
> @bash scripts/test.sh

lint:
> @cd apps/api && . .venv/bin/activate && ruff check .
> @cd apps/web && npm run lint

format:
> @cd apps/api && . .venv/bin/activate && ruff format .
> @cd apps/web && npm run format

typecheck:
> @cd apps/api && . .venv/bin/activate && mypy app

docker-up:
> @docker compose up -d

docker-down:
> @docker compose down

docker-logs:
> @docker compose logs -f postgres

migrate:
> @cd apps/api && . .venv/bin/activate && python ../../scripts/migrate.py

seed:
> @cd apps/api && . .venv/bin/activate && python ../../scripts/seed.py

db-reset:
> @echo "Dropping and recreating public schema..."
> @docker compose exec -T postgres psql -U minecore -d minecore -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
> @$(MAKE) migrate
> @$(MAKE) seed

clean:
> @rm -rf apps/web/dist apps/web/node_modules apps/web/.vite
> @rm -rf apps/api/.venv apps/api/.pytest_cache apps/api/.mypy_cache apps/api/.ruff_cache
> @find . -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
