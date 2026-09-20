"""Cross-tenant access must fail.

Every test sets up two organizations with their own user and resource,
then attempts to reach the other organization's resource via the API
using the first user's headers. Every attempt must return 404 (not
403), so existence of the other tenant's data is never leaked.
"""
from tests.integration._helpers import (
    auth_headers,
    make_employee,
    make_membership,
    make_org,
    make_site,
    make_user,
)


def _two_orgs(db_session):
    org_a = make_org(db_session, code="TENANT-A")
    org_b = make_org(db_session, code="TENANT-B")
    user_a = make_user(db_session)
    user_b = make_user(db_session)
    make_membership(db_session, org_a, user_a)
    make_membership(db_session, org_b, user_b)
    return org_a, org_b, user_a, user_b


def test_cannot_read_other_tenants_mine_site(api_client, db_session):
    org_a, org_b, user_a, _ = _two_orgs(db_session)
    site_a = make_site(db_session, org_a, code="A-SITE")

    r = api_client.get(f"/mine-sites/{site_a.id}", headers=auth_headers(user_a, org_b))
    assert r.status_code == 404


def test_cannot_update_other_tenants_mine_site(api_client, db_session):
    org_a, org_b, user_a, _ = _two_orgs(db_session)
    site_a = make_site(db_session, org_a, code="A-UPD")

    r = api_client.patch(
        f"/mine-sites/{site_a.id}",
        headers=auth_headers(user_a, org_b),
        json={"name": "Hijacked"},
    )
    assert r.status_code == 404


def test_cannot_delete_other_tenants_mine_site(api_client, db_session):
    org_a, org_b, user_a, _ = _two_orgs(db_session)
    site_a = make_site(db_session, org_a, code="A-DEL")

    r = api_client.delete(f"/mine-sites/{site_a.id}", headers=auth_headers(user_a, org_b))
    assert r.status_code == 404


def test_listing_mine_sites_only_returns_own_org(api_client, db_session):
    org_a, org_b, user_a, _ = _two_orgs(db_session)
    make_site(db_session, org_a, code="A-1")
    make_site(db_session, org_a, code="A-2")
    make_site(db_session, org_b, code="B-1")

    r = api_client.get("/mine-sites", headers=auth_headers(user_a, org_a))
    assert r.status_code == 200
    codes = {s["code"] for s in r.json()}
    assert codes == {"A-1", "A-2"}


def test_cannot_read_other_tenants_employee(api_client, db_session):
    org_a, org_b, user_a, _ = _two_orgs(db_session)
    emp_a = make_employee(db_session, org_a, number="A-EMP")

    r = api_client.get(f"/employees/{emp_a.id}", headers=auth_headers(user_a, org_b))
    assert r.status_code == 404


def test_cannot_assign_user_to_other_tenants_site(api_client, db_session):
    org_a, org_b, user_a, user_b = _two_orgs(db_session)
    site_a = make_site(db_session, org_a, code="A-ASG")

    r = api_client.post(
        f"/mine-sites/{site_a.id}/assignments",
        headers=auth_headers(user_b, org_b),
        json={"user_id": str(user_b.id)},
    )
    assert r.status_code == 404


def test_current_organization_endpoint_is_tenant_scoped(api_client, db_session):
    org_a, org_b, user_a, _ = _two_orgs(db_session)

    r = api_client.get("/organizations/current", headers=auth_headers(user_a, org_b))
    assert r.status_code == 200
    assert r.json()["id"] == str(org_b.id)
    assert r.json()["id"] != str(org_a.id)
