#!/usr/bin/env python3
"""MineCore migration runner.

Applies database/migrations/*.sql in lexicographic order.

Each migration runs inside its own transaction. Successfully applied
migrations are recorded in the schema_migrations table and skipped on
subsequent runs, so the runner is idempotent and safe to re-invoke.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import psycopg


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
MIGRATIONS_DIR = ROOT / "database" / "migrations"
ENV_FILE = ROOT / ".env"


# ---------------------------------------------------------------------------
# Environment loading
# ---------------------------------------------------------------------------
def load_env_file(path: Path) -> None:
    """Load simple KEY=VALUE pairs from a .env file into os.environ.

    Existing environment variables are never overwritten, so anything the
    shell or CI has already exported takes precedence.

    This intentionally supports only the subset of .env syntax MineCore
    needs: comments, blank lines, and KEY=VALUE. It does not handle
    quoted values, multiline values, or variable expansion.
    """
    if not path.exists():
        return

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()

        if not key:
            continue

        os.environ.setdefault(key, value)


load_env_file(ENV_FILE)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DEFAULT_DATABASE_URL = "postgresql+psycopg://minecore:minecore@localhost:5433/minecore"

DATABASE_URL = os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)

# psycopg.connect() does not understand SQLAlchemy driver suffixes
PSYCOPG_URL = DATABASE_URL.replace("postgresql+psycopg://", "postgresql://")


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
def ensure_registry(conn: psycopg.Connection) -> None:
    """Create the migration registry table if it does not exist."""

    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version     TEXT PRIMARY KEY,
                applied_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        )

    conn.commit()


def applied_versions(conn: psycopg.Connection) -> set[str]:
    """Return the set of migration versions already applied."""

    with conn.cursor() as cur:
        cur.execute("SELECT version FROM schema_migrations")

        return {row[0] for row in cur.fetchall()}


# ---------------------------------------------------------------------------
# Applying migrations
# ---------------------------------------------------------------------------
def apply_migration(conn: psycopg.Connection, path: Path) -> None:
    """Apply one migration atomically.

    The DDL and the registry insert share a single transaction. If either
    fails, the whole migration is rolled back and nothing is recorded.
    """

    version = path.stem
    sql = path.read_text(encoding="utf-8")

    try:
        with conn.transaction():
            with conn.cursor() as cur:
                cur.execute(sql)

                cur.execute(
                    "INSERT INTO schema_migrations (version) VALUES (%s)",
                    (version,),
                )

    except Exception as exc:
        print(f"\nERROR: migration {version} failed.", file=sys.stderr)
        print(f"File:   {path}", file=sys.stderr)
        print(f"Reason: {exc}", file=sys.stderr)
        raise


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------
def main() -> int:
    if not MIGRATIONS_DIR.exists():
        print(f"No migrations directory at {MIGRATIONS_DIR}", file=sys.stderr)
        return 1

    files = sorted(MIGRATIONS_DIR.glob("*.sql"))

    if not files:
        print("No migration files found.")
        return 0

    host = DATABASE_URL.rsplit("@", 1)[-1] if "@" in DATABASE_URL else DATABASE_URL

    print(f"Connecting to {host}")
    print(f"Migrations:   {MIGRATIONS_DIR}")
    print()

    try:
        with psycopg.connect(PSYCOPG_URL) as conn:
            ensure_registry(conn)

            done = applied_versions(conn)
            newly_applied = 0

            for path in files:
                version = path.stem

                if version in done:
                    print(f"  = {version} (already applied)")
                    continue

                print(f"  + {version}")
                apply_migration(conn, path)
                newly_applied += 1

            print()
            print(f"Applied {newly_applied} migration(s).")

    except psycopg.Error as exc:
        print(f"\nDatabase error: {exc}", file=sys.stderr)
        return 1

    except Exception as exc:
        print(f"\nMigration error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())