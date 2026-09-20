"""Phase 05 integration tests.

Self-contained: defines its own helpers so it does not depend on the
exact shape of the shared Phase 02/03 test helpers. Uses `api_client`
and `db_session` fixtures which the top-level conftest provides.
"""
from __future__ import annotations

import uuid
from datetime import date
from decimal import Decimal

import pytest

from app.materials.models import Material
from app.mining.models import MiningOperation
from app.models.mine_site import MineSite
from app.models.organization import Organization
from app.models.user import User
from app.pits.models import Pit
from app.units.models import Unit


# ---------------------------------------------------------------------------
# Local helpers
# ---------------------------------------------------------------------------

def make_org(db_session, code: str | None = None) -> Organization:
    org = Organization(
        code=code or f"T-{uuid.uuid4().hex[:8]}",
        name="Test Org",
        status="active",
    )
    db_session.add(org)
    db_session.flush()
    return org


def make_user(db_session, email: str | None = None) -> User:
    user = User(
        email=email or f"u-{uuid.uuid4().hex[:8]}@x.io",
        password_hash="x",
        full_name="Test User",
        is_active=True,
    )
    db_session.add(user)
    db_session.flush()
    return user


def make_site(db_session, org: Organization, code: str = "S1") -> MineSite:
    site = MineSite(
        organization_id=org.id,
        code=code,
        name="Site",
        status="active",
    )
    db_session.add(site)
    db_session.flush()
    return site


def make_pit(db_session, org: Organization, site: MineSite, code: str = "P1") -> Pit:
    pit = Pit(
        organization_id=org.id,
        mine_site_id=site.id,
        code=code,
        name="Pit",
        status="active",
    )
    db_session.add(pit)
    db_session.flush()
    return pit


def make_material(db_session, org: Organization, code: str = "M1") -> Material:
    mat = Material(
        organization_id=org.id,
        code=code,
        name="Gold Ore",
        status="active",
    )
    db_session.add(mat)
    db_session.flush()
    return mat


def make_unit(db_session, org: Organization, code: str = "T") -> Unit:
    unit = Unit(
        organization_id=org.id,
        code=code,
        name="Tonne",
        symbol="t",
        dimension="mass",
        status="active",
    )
    db_session.add(unit)
    db_session.flush()
    return unit


def headers(user: User, org: Organization) -> dict:
    return {
        "X-Organization-Id": str(org.id),
        "X-User-Id": str(user.id),
    }


def base_payload(site, pit, material, unit=None) -> dict:
    payload = {
        "mine_site_id": str(site.id),
        "pit_id": str(pit.id),
        "material_id": str(material.id),
        "operation_date": "2026-01-15",
        "quantity": "100.5000",
    }
    if unit is not None:
        payload["unit_id"] = str(unit.id)
    return payload


@pytest.fixture
def ctx(db_session):
    """A ready-to-use (org, user, site, pit, material, unit) tuple."""
    org = make_org(db_session)
    user = make_user(db_session)
    site = make_site(db_session, org)
    pit = make_pit(db_session, org, site)
    material = make_material(db_session, org)
    unit = make_unit(db_session, org)
    return {
        "org": org,
        "user": user,
        "site": site,
        "pit": pit,
        "material": material,
        "unit": unit,
        "headers": headers(user, org),
    }


# ---------------------------------------------------------------------------
# Create + read
# ---------------------------------------------------------------------------

def test_create_draft(api_client, db_session, ctx):
    r = api_client.post(
        "/api/mining-operations",
        headers=ctx["headers"],
        json=base_payload(ctx["site"], ctx["pit"], ctx["material"], ctx["unit"]),
    )
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["status"] == "draft"
    assert body["operation_number"].startswith("MO-")
    assert body["operation_seq"] == 1
    assert body["quantity"] == "100.5000"


def test_operation_numbers_increment(api_client, db_session, ctx):
    p = base_payload(ctx["site"], ctx["pit"], ctx["material"])
    a = api_client.post("/api/mining-operations", headers=ctx["headers"], json=p).json()
    b = api_client.post("/api/mining-operations", headers=ctx["headers"], json=p).json()
    assert a["operation_seq"] == 1
    assert b["operation_seq"] == 2
    assert a["operation_number"] != b["operation_number"]


def test_create_requires_auth(api_client, db_session, ctx):
    r = api_client.post(
        "/api/mining-operations",
        json=base_payload(ctx["site"], ctx["pit"], ctx["material"]),
    )
    assert r.status_code == 401


def test_create_rejects_quantity_zero(api_client, db_session, ctx):
    payload = base_payload(ctx["site"], ctx["pit"], ctx["material"])
    payload["quantity"] = "0"
    r = api_client.post("/api/mining-operations", headers=ctx["headers"], json=payload)
    assert r.status_code == 422


def test_create_rejects_foreign_material(api_client, db_session, ctx):
    other = make_org(db_session)
    foreign_material = make_material(db_session, other, code="F-1")

    payload = base_payload(ctx["site"], ctx["pit"], foreign_material)
    r = api_client.post("/api/mining-operations", headers=ctx["headers"], json=payload)
    assert r.status_code == 400


def test_create_rejects_pit_from_other_site(api_client, db_session, ctx):
    other_site = make_site(db_session, ctx["org"], code="S2")
    other_pit = make_pit(db_session, ctx["org"], other_site, code="P2")

    payload = base_payload(ctx["site"], other_pit, ctx["material"])
    r = api_client.post("/api/mining-operations", headers=ctx["headers"], json=payload)
    assert r.status_code == 400


def test_cross_org_read_returns_404(api_client, db_session, ctx):
    created = api_client.post(
        "/api/mining-operations",
        headers=ctx["headers"],
        json=base_payload(ctx["site"], ctx["pit"], ctx["material"]),
    ).json()

    other = make_org(db_session)
    other_user = make_user(db_session)

    r = api_client.get(
        f"/api/mining-operations/{created['id']}",
        headers=headers(other_user, other),
    )
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# Update / delete — draft only
# ---------------------------------------------------------------------------

def test_update_draft(api_client, db_session, ctx):
    created = api_client.post(
        "/api/mining-operations",
        headers=ctx["headers"],
        json=base_payload(ctx["site"], ctx["pit"], ctx["material"]),
    ).json()

    r = api_client.patch(
        f"/api/mining-operations/{created['id']}",
        headers=ctx["headers"],
        json={"quantity": "200.0000", "notes": "adjusted"},
    )
    assert r.status_code == 200, r.text
    assert r.json()["quantity"] == "200.0000"
    assert r.json()["notes"] == "adjusted"


def test_delete_draft(api_client, db_session, ctx):
    created = api_client.post(
        "/api/mining-operations",
        headers=ctx["headers"],
        json=base_payload(ctx["site"], ctx["pit"], ctx["material"]),
    ).json()

    r = api_client.delete(
        f"/api/mining-operations/{created['id']}",
        headers=ctx["headers"],
    )
    assert r.status_code == 204

    r2 = api_client.get(
        f"/api/mining-operations/{created['id']}",
        headers=ctx["headers"],
    )
    assert r2.status_code == 404


# ---------------------------------------------------------------------------
# Workflow
# ---------------------------------------------------------------------------

def _create_draft(api_client, ctx) -> dict:
    return api_client.post(
        "/api/mining-operations",
        headers=ctx["headers"],
        json=base_payload(ctx["site"], ctx["pit"], ctx["material"]),
    ).json()


def test_draft_can_be_recorded(api_client, db_session, ctx):
    op = _create_draft(api_client, ctx)
    r = api_client.post(
        f"/api/mining-operations/{op['id']}/record",
        headers=ctx["headers"],
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["status"] == "recorded"
    assert body["recorded_at"] is not None


def test_recorded_can_be_approved(api_client, db_session, ctx):
    op = _create_draft(api_client, ctx)
    api_client.post(f"/api/mining-operations/{op['id']}/record", headers=ctx["headers"])
    r = api_client.post(
        f"/api/mining-operations/{op['id']}/approve",
        headers=ctx["headers"],
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["status"] == "approved"
    assert body["approved_at"] is not None


def test_approved_cannot_be_edited(api_client, db_session, ctx):
    op = _create_draft(api_client, ctx)
    api_client.post(f"/api/mining-operations/{op['id']}/record", headers=ctx["headers"])
    api_client.post(f"/api/mining-operations/{op['id']}/approve", headers=ctx["headers"])

    r = api_client.patch(
        f"/api/mining-operations/{op['id']}",
        headers=ctx["headers"],
        json={"quantity": "999"},
    )
    assert r.status_code == 409


def test_approved_cannot_be_deleted(api_client, db_session, ctx):
    op = _create_draft(api_client, ctx)
    api_client.post(f"/api/mining-operations/{op['id']}/record", headers=ctx["headers"])
    api_client.post(f"/api/mining-operations/{op['id']}/approve", headers=ctx["headers"])

    r = api_client.delete(
        f"/api/mining-operations/{op['id']}",
        headers=ctx["headers"],
    )
    assert r.status_code == 409


def test_recorded_cannot_be_edited(api_client, db_session, ctx):
    op = _create_draft(api_client, ctx)
    api_client.post(f"/api/mining-operations/{op['id']}/record", headers=ctx["headers"])

    r = api_client.patch(
        f"/api/mining-operations/{op['id']}",
        headers=ctx["headers"],
        json={"quantity": "999"},
    )
    assert r.status_code == 409


def test_cannot_approve_draft_directly(api_client, db_session, ctx):
    op = _create_draft(api_client, ctx)
    r = api_client.post(
        f"/api/mining-operations/{op['id']}/approve",
        headers=ctx["headers"],
    )
    assert r.status_code == 409


def test_cancel_requires_reason(api_client, db_session, ctx):
    op = _create_draft(api_client, ctx)
    r = api_client.post(
        f"/api/mining-operations/{op['id']}/cancel",
        headers=ctx["headers"],
        json={"reason": ""},
    )
    assert r.status_code == 422


def test_cancel_draft(api_client, db_session, ctx):
    op = _create_draft(api_client, ctx)
    r = api_client.post(
        f"/api/mining-operations/{op['id']}/cancel",
        headers=ctx["headers"],
        json={"reason": "recorded in error"},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["status"] == "cancelled"
    assert body["cancellation_reason"] == "recorded in error"


def test_cancelled_is_terminal(api_client, db_session, ctx):
    op = _create_draft(api_client, ctx)
    api_client.post(
        f"/api/mining-operations/{op['id']}/cancel",
        headers=ctx["headers"],
        json={"reason": "x"},
    )
    for action in ("record", "approve"):
        r = api_client.post(
            f"/api/mining-operations/{op['id']}/{action}",
            headers=ctx["headers"],
        )
        assert r.status_code == 409


# ---------------------------------------------------------------------------
# Audit trail
# ---------------------------------------------------------------------------

def test_audit_records_full_lifecycle(api_client, db_session, ctx):
    op = _create_draft(api_client, ctx)
    api_client.patch(
        f"/api/mining-operations/{op['id']}",
        headers=ctx["headers"],
        json={"quantity": "150"},
    )
    api_client.post(f"/api/mining-operations/{op['id']}/record", headers=ctx["headers"])
    api_client.post(f"/api/mining-operations/{op['id']}/approve", headers=ctx["headers"])

    r = api_client.get(
        f"/api/mining-operations/{op['id']}/audit",
        headers=ctx["headers"],
    )
    assert r.status_code == 200
    entries = r.json()
    actions = [e["action"] for e in entries]
    assert actions == ["create", "update", "record", "approve"]

    record_entry = next(e for e in entries if e["action"] == "record")
    assert record_entry["from_status"] == "draft"
    assert record_entry["to_status"] == "recorded"

    update_entry = next(e for e in entries if e["action"] == "update")
    assert "quantity" in update_entry["changes"]


def test_audit_is_org_scoped(api_client, db_session, ctx):
    op = _create_draft(api_client, ctx)
    other = make_org(db_session)
    other_user = make_user(db_session)

    r = api_client.get(
        f"/api/mining-operations/{op['id']}/audit",
        headers=headers(other_user, other),
    )
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------

def test_list_filter_by_status(api_client, db_session, ctx):
    _create_draft(api_client, ctx)
    b = _create_draft(api_client, ctx)
    api_client.post(f"/api/mining-operations/{b['id']}/record", headers=ctx["headers"])

    drafts = api_client.get(
        "/api/mining-operations?status=draft",
        headers=ctx["headers"],
    ).json()
    recorded = api_client.get(
        "/api/mining-operations?status=recorded",
        headers=ctx["headers"],
    ).json()

    assert len(drafts) == 1
    assert len(recorded) == 1
