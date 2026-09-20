"""Constraint-level tests for the Phase 01 schema.

Every assertion runs inside a transaction that is rolled back.
"""
from __future__ import annotations

import psycopg
import pytest
from psycopg.errors import (
    CheckViolation,
    ForeignKeyViolation,
    NotNullViolation,
    UniqueViolation,
)


# ============================================================
# organizations
# ============================================================

def test_organization_code_is_unique(db: psycopg.Connection) -> None:
    with db.transaction():
        db.execute(
            "INSERT INTO organizations (code, name) VALUES (%s, %s)",
            ("ACME", "Acme Mining"),
        )
    with pytest.raises(UniqueViolation):
        with db.transaction():
            db.execute(
                "INSERT INTO organizations (code, name) VALUES (%s, %s)",
                ("ACME", "Acme Mining Duplicate"),
            )


def test_organization_status_must_be_valid(db: psycopg.Connection) -> None:
    with pytest.raises(CheckViolation):
        with db.transaction():
            db.execute(
                "INSERT INTO organizations (code, name, status) VALUES (%s, %s, %s)",
                ("BAD", "Bad Corp", "bogus"),
            )


# ============================================================
# users
# ============================================================

def test_user_email_must_be_unique(db: psycopg.Connection) -> None:
    with db.transaction():
        db.execute(
            "INSERT INTO users (email, password_hash, full_name) VALUES (%s, %s, %s)",
            ("a@x.io", "h", "A"),
        )
    with pytest.raises(UniqueViolation):
        with db.transaction():
            db.execute(
                "INSERT INTO users (email, password_hash, full_name) VALUES (%s, %s, %s)",
                ("a@x.io", "h", "A2"),
            )


def test_user_email_must_be_lowercase(db: psycopg.Connection) -> None:
    with pytest.raises(CheckViolation):
        with db.transaction():
            db.execute(
                "INSERT INTO users (email, password_hash, full_name) VALUES (%s, %s, %s)",
                ("Mixed@x.io", "h", "M"),
            )


def test_user_email_shape_enforced(db: psycopg.Connection) -> None:
    with pytest.raises(CheckViolation):
        with db.transaction():
            db.execute(
                "INSERT INTO users (email, password_hash, full_name) VALUES (%s, %s, %s)",
                ("not-an-email", "h", "X"),
            )


# ============================================================
# organization_memberships
# ============================================================

def test_membership_requires_existing_organization(db: psycopg.Connection) -> None:
    with db.transaction():
        db.execute(
            "INSERT INTO users (id, email, password_hash, full_name) "
            "VALUES ('00000000-0000-0000-0000-00000000aaaa', 'm1@x.io', 'h', 'M')"
        )
    with pytest.raises(ForeignKeyViolation):
        with db.transaction():
            db.execute(
                "INSERT INTO organization_memberships (organization_id, user_id) "
                "VALUES ('00000000-0000-0000-0000-00000000bbbb', "
                "'00000000-0000-0000-0000-00000000aaaa')"
            )


def test_membership_requires_existing_user(db: psycopg.Connection) -> None:
    with db.transaction():
        db.execute(
            "INSERT INTO organizations (id, code, name) "
            "VALUES ('00000000-0000-0000-0000-00000000cccc', 'FK', 'FK Co')"
        )
    with pytest.raises(ForeignKeyViolation):
        with db.transaction():
            db.execute(
                "INSERT INTO organization_memberships (organization_id, user_id) "
                "VALUES ('00000000-0000-0000-0000-00000000cccc', "
                "'00000000-0000-0000-0000-00000000dddd')"
            )


def test_membership_unique_per_org_user(db: psycopg.Connection) -> None:
    with db.transaction():
        db.execute(
            "INSERT INTO organizations (id, code, name) "
            "VALUES ('00000000-0000-0000-0000-00000000ee01', 'U1', 'U1')"
        )
        db.execute(
            "INSERT INTO users (id, email, password_hash, full_name) "
            "VALUES ('00000000-0000-0000-0000-00000000ee02', 'u1@x.io', 'h', 'U1')"
        )
        db.execute(
            "INSERT INTO organization_memberships (organization_id, user_id) "
            "VALUES ('00000000-0000-0000-0000-00000000ee01', "
            "'00000000-0000-0000-0000-00000000ee02')"
        )
    with pytest.raises(UniqueViolation):
        with db.transaction():
            db.execute(
                "INSERT INTO organization_memberships (organization_id, user_id) "
                "VALUES ('00000000-0000-0000-0000-00000000ee01', "
                "'00000000-0000-0000-0000-00000000ee02')"
            )


def test_membership_active_requires_joined_at(db: psycopg.Connection) -> None:
    with db.transaction():
        db.execute(
            "INSERT INTO organizations (id, code, name) "
            "VALUES ('00000000-0000-0000-0000-00000000ff01', 'FF1', 'FF1')"
        )
        db.execute(
            "INSERT INTO users (id, email, password_hash, full_name) "
            "VALUES ('00000000-0000-0000-0000-00000000ff02', 'ff1@x.io', 'h', 'FF1')"
        )
    with pytest.raises(CheckViolation):
        with db.transaction():
            db.execute(
                "INSERT INTO organization_memberships "
                "(organization_id, user_id, status, joined_at) "
                "VALUES ('00000000-0000-0000-0000-00000000ff01', "
                "'00000000-0000-0000-0000-00000000ff02', 'active', NULL)"
            )


# ============================================================
# mine_sites
# ============================================================

def test_mine_site_code_unique_within_org(db: psycopg.Connection) -> None:
    with db.transaction():
        db.execute(
            "INSERT INTO organizations (id, code, name) "
            "VALUES ('00000000-0000-0000-0000-0000000000a1', 'OA', 'OA')"
        )
        db.execute(
            "INSERT INTO mine_sites (organization_id, code, name) "
            "VALUES ('00000000-0000-0000-0000-0000000000a1', 'P1', 'Pit 1')"
        )
    with pytest.raises(UniqueViolation):
        with db.transaction():
            db.execute(
                "INSERT INTO mine_sites (organization_id, code, name) "
                "VALUES ('00000000-0000-0000-0000-0000000000a1', 'P1', 'Pit 1 dup')"
            )


def test_mine_site_latitude_bounds(db: psycopg.Connection) -> None:
    with db.transaction():
        db.execute(
            "INSERT INTO organizations (id, code, name) "
            "VALUES ('00000000-0000-0000-0000-0000000000b1', 'OB', 'OB')"
        )
    with pytest.raises(CheckViolation):
        with db.transaction():
            db.execute(
                "INSERT INTO mine_sites (organization_id, code, name, latitude) "
                "VALUES ('00000000-0000-0000-0000-0000000000b1', 'X', 'X', 91)"
            )


def test_mine_site_longitude_bounds(db: psycopg.Connection) -> None:
    with db.transaction():
        db.execute(
            "INSERT INTO organizations (id, code, name) "
            "VALUES ('00000000-0000-0000-0000-0000000000c1', 'OC', 'OC')"
        )
    with pytest.raises(CheckViolation):
        with db.transaction():
            db.execute(
                "INSERT INTO mine_sites (organization_id, code, name, longitude) "
                "VALUES ('00000000-0000-0000-0000-0000000000c1', 'Y', 'Y', 181)"
            )


# ============================================================
# roles
# ============================================================

def test_system_role_must_have_null_org(db: psycopg.Connection) -> None:
    with db.transaction():
        db.execute(
            "INSERT INTO organizations (id, code, name) "
            "VALUES ('00000000-0000-0000-0000-0000000000d1', 'OD', 'OD')"
        )
    with pytest.raises(CheckViolation):
        with db.transaction():
            db.execute(
                "INSERT INTO roles (organization_id, code, name, is_system) "
                "VALUES ('00000000-0000-0000-0000-0000000000d1', 'x', 'X', TRUE)"
            )


def test_org_role_must_have_org(db: psycopg.Connection) -> None:
    with pytest.raises(CheckViolation):
        with db.transaction():
            db.execute(
                "INSERT INTO roles (organization_id, code, name, is_system) "
                "VALUES (NULL, 'x', 'X', FALSE)"
            )


def test_system_role_codes_unique(db: psycopg.Connection) -> None:
    with pytest.raises(UniqueViolation):
        with db.transaction():
            db.execute(
                "INSERT INTO roles (organization_id, code, name, is_system) "
                "VALUES (NULL, 'org_admin', 'Duplicate', TRUE)"
            )


# ============================================================
# permissions
# ============================================================

def test_permission_code_unique(db: psycopg.Connection) -> None:
    with pytest.raises(UniqueViolation):
        with db.transaction():
            db.execute(
                "INSERT INTO permissions (code, description) "
                "VALUES ('organization.read', 'dup')"
            )


def test_permission_code_shape_enforced(db: psycopg.Connection) -> None:
    with pytest.raises(CheckViolation):
        with db.transaction():
            db.execute(
                "INSERT INTO permissions (code, description) "
                "VALUES ('NotADotCode', 'bad')"
            )


# ============================================================
# employees
# ============================================================

def test_employee_number_unique_per_org(db: psycopg.Connection) -> None:
    with db.transaction():
        db.execute(
            "INSERT INTO organizations (id, code, name) "
            "VALUES ('00000000-0000-0000-0000-0000000000e1', 'OE', 'OE')"
        )
        db.execute(
            "INSERT INTO employees "
            "(organization_id, employee_number, full_name) "
            "VALUES ('00000000-0000-0000-0000-0000000000e1', 'E-001', 'Emp One')"
        )
    with pytest.raises(UniqueViolation):
        with db.transaction():
            db.execute(
                "INSERT INTO employees "
                "(organization_id, employee_number, full_name) "
                "VALUES ('00000000-0000-0000-0000-0000000000e1', 'E-001', 'Emp Two')"
            )


# ============================================================
# NOT NULL enforcement spot check
# ============================================================

def test_organization_name_required(db: psycopg.Connection) -> None:
    with pytest.raises(NotNullViolation):
        with db.transaction():
            db.execute(
                "INSERT INTO organizations (code, name) VALUES (%s, NULL)",
                ("NN",),
            )
