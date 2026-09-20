"""Verify the Phase 01 foundation schema end-to-end."""
from __future__ import annotations

import psycopg
import pytest


EXPECTED_TABLES = {
    "organizations",
    "users",
    "organization_memberships",
    "employees",
    "roles",
    "permissions",
    "role_permissions",
    "membership_roles",
    "mine_sites",
    "user_site_assignments",
    "schema_migrations",
}


def test_expected_tables_exist(db: psycopg.Connection) -> None:
    with db.cursor() as cur:
        cur.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            """
        )
        present = {row[0] for row in cur.fetchall()}

    missing = EXPECTED_TABLES - present
    assert not missing, f"Missing tables: {sorted(missing)}"


def test_pgcrypto_or_builtin_uuid_available(db: psycopg.Connection) -> None:
    with db.cursor() as cur:
        cur.execute("SELECT gen_random_uuid()")
        value = cur.fetchone()
    assert value is not None
    assert value[0] is not None


def test_seeded_permissions_present(db: psycopg.Connection) -> None:
    with db.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM permissions")
        count = cur.fetchone()[0]
    # Phase 01 seeds 24 permissions; later phases may add more.
    assert count >= 24


def test_seeded_system_roles_present(db: psycopg.Connection) -> None:
    with db.cursor() as cur:
        cur.execute(
            "SELECT code FROM roles WHERE is_system = TRUE ORDER BY code"
        )
        codes = {row[0] for row in cur.fetchall()}
    expected = {"org_admin", "site_manager", "operator", "viewer", "auditor"}
    assert expected.issubset(codes)


def test_demo_organization_present(db: psycopg.Connection) -> None:
    with db.cursor() as cur:
        cur.execute(
            "SELECT name, status FROM organizations WHERE code = 'demo'"
        )
        row = cur.fetchone()
    assert row is not None, "demo organization seed did not run"
    assert row[0] == "Demo Mining Co."
    assert row[1] == "active"


def test_demo_user_is_disabled(db: psycopg.Connection) -> None:
    with db.cursor() as cur:
        cur.execute(
            "SELECT is_active FROM users WHERE email = 'admin@demo.local'"
        )
        row = cur.fetchone()
    assert row is not None
    assert row[0] is False, "demo user must be disabled until Phase 02"
