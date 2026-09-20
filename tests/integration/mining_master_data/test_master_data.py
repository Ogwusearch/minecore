"""Integration tests for Phase 04 mining master data.

Uses the shared `api_client` and `db_session` fixtures from the top-level
conftest (same as the Phase 02/03 tests). The `make_org` helper is
defined locally because the shared suite defines `make_org` as a plain
function, not a fixture, and this file is intentionally self-contained.

Every request carries an explicit X-Organization-Id header so the
Phase 04 placeholder dependency can resolve the tenant without the full
Phase 02 auth stack.
"""
from __future__ import annotations

import uuid

import pytest

from app.models.organization import Organization


# ---------------------------------------------------------------------------
# Local helpers
# ---------------------------------------------------------------------------

def make_org(db_session, *, code: str | None = None, name: str = "Test Org"):
    """Insert a fresh organization and return the ORM object.

    The `db_session` fixture is transactional and rolled back at the end
    of the test, so nothing is persisted.
    """
    org = Organization(
        code=code or f"T-{uuid.uuid4().hex[:8]}",
        name=name,
        status="active",
    )
    db_session.add(org)
    db_session.flush()
    return org


def _headers(org) -> dict:
    return {"X-Organization-Id": str(org.id)}


# ---------------------------------------------------------------------------
# Minerals
# ---------------------------------------------------------------------------

def test_requires_organization_header(api_client):
    r = api_client.get("/api/minerals")
    assert r.status_code == 401


def test_create_and_list_minerals(api_client, db_session):
    org = make_org(db_session, code="MIN1")
    headers = _headers(org)

    r = api_client.post(
        "/api/minerals",
        headers=headers,
        json={"code": "AU", "name": "Gold"},
    )
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["code"] == "AU"
    assert body["status"] == "active"

    r = api_client.get("/api/minerals", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_duplicate_code_conflicts(api_client, db_session):
    org = make_org(db_session, code="MIN2")
    headers = _headers(org)

    api_client.post("/api/minerals", headers=headers, json={"code": "AU", "name": "Gold"})
    r = api_client.post("/api/minerals", headers=headers, json={"code": "AU", "name": "Gold"})
    assert r.status_code == 409


def test_org_isolation(api_client, db_session):
    org_a = make_org(db_session, code="MINA")
    org_b = make_org(db_session, code="MINB")

    api_client.post(
        "/api/minerals",
        headers=_headers(org_a),
        json={"code": "AU", "name": "Gold"},
    )

    r = api_client.get("/api/minerals", headers=_headers(org_b))
    assert r.status_code == 200
    assert r.json() == []


def test_get_by_id_cross_org_returns_404(api_client, db_session):
    org_a = make_org(db_session, code="MINX")
    org_b = make_org(db_session, code="MINY")

    created = api_client.post(
        "/api/minerals",
        headers=_headers(org_a),
        json={"code": "AU", "name": "Gold"},
    ).json()

    r = api_client.get(f"/api/minerals/{created['id']}", headers=_headers(org_b))
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# Units → Materials (FK validation)
# ---------------------------------------------------------------------------

def test_create_unit_then_material(api_client, db_session):
    org = make_org(db_session, code="MAT1")
    headers = _headers(org)

    unit = api_client.post(
        "/api/units",
        headers=headers,
        json={"code": "T", "name": "Tonne", "symbol": "t", "dimension": "mass"},
    )
    assert unit.status_code == 201, unit.text

    mineral = api_client.post(
        "/api/minerals",
        headers=headers,
        json={"code": "AU", "name": "Gold"},
    ).json()

    mat = api_client.post(
        "/api/materials",
        headers=headers,
        json={
            "code": "AU-ORE",
            "name": "Gold Ore",
            "unit_id": unit.json()["id"],
            "mineral_id": mineral["id"],
        },
    )
    assert mat.status_code == 201, mat.text
    body = mat.json()
    assert body["unit_id"] == unit.json()["id"]
    assert body["mineral_id"] == mineral["id"]


def test_material_rejects_foreign_unit(api_client, db_session):
    org_a = make_org(db_session, code="MAT2A")
    org_b = make_org(db_session, code="MAT2B")

    unit_b = api_client.post(
        "/api/units",
        headers=_headers(org_b),
        json={"code": "KG", "name": "Kilogram", "symbol": "kg", "dimension": "mass"},
    ).json()

    r = api_client.post(
        "/api/materials",
        headers=_headers(org_a),
        json={"code": "X", "name": "X", "unit_id": unit_b["id"]},
    )
    assert r.status_code == 400


# ---------------------------------------------------------------------------
# Shifts
# ---------------------------------------------------------------------------

def test_create_shift(api_client, db_session):
    org = make_org(db_session, code="SHF1")
    headers = _headers(org)

    r = api_client.post(
        "/api/shifts",
        headers=headers,
        json={
            "code": "DAY",
            "name": "Day Shift",
            "start_time": "06:00:00",
            "end_time": "18:00:00",
        },
    )
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["code"] == "DAY"
    assert body["start_time"] == "06:00:00"
