#!/usr/bin/env python3
"""MineCore seed runner.

Applies database/seeds/*.sql in lexicographic order.

Seeds are idempotent reference data (they use ON CONFLICT DO NOTHING)
and are safe to re-run. Each seed file runs inside its own transaction
so a failure rolls back cleanly without leaving partial data behind.
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
SEEDS_DIR = ROOT / "database" / "seeds"
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
# Applying seeds
# ---------------------------------------------------------------------------
def run_seed(conn: psycopg.Connection, path: Path) -> None:
    """Apply one seed file atomically.

    The entire file runs in a single transaction. If any statement fails,
    the transaction rolls back and nothing from that file is persisted.
    """

    sql = path.read_text(encoding="utf-8")

    try:
        with conn.transaction():
            with conn.cursor() as cur:
                cur.execute(sql)

    except Exception as exc:
        print(f"\nERROR: seed {path.stem} failed.", file=sys.stderr)
        print(f"File:   {path}", file=sys.stderr)
        print(f"Reason: {exc}", file=sys.stderr)
        raise


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------
def main() -> int:
    if not SEEDS_DIR.exists():
        print(f"No seeds directory at {SEEDS_DIR}", file=sys.stderr)
        return 1

    files = sorted(SEEDS_DIR.glob("*.sql"))

    if not files:
        print("No seed files found.")
        return 0

    host = DATABASE_URL.rsplit("@", 1)[-1] if "@" in DATABASE_URL else DATABASE_URL

    print(f"Connecting to {host}")
    print(f"Seeds:        {SEEDS_DIR}")
    print()

    try:
        with psycopg.connect(PSYCOPG_URL) as conn:
            for path in files:
                print(f"  ~ {path.stem}")
                run_seed(conn, path)

            print()
            print(f"Ran {len(files)} seed file(s).")

    except psycopg.Error as exc:
        print(f"\nDatabase error: {exc}", file=sys.stderr)
        return 1

    except Exception as exc:
        print(f"\nSeed error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())