from tests.integration._helpers import (
    auth_headers,
    make_membership,
    make_org,
    make_site,
    make_user,
)


def test_assign_and_unassign_user_to_site(api_client, db_session):
    org = make_org(db_session, code="ASG")
    admin = make_user(db_session)
    member = make_user(db_session)
    make_membership(db_session, org, admin)
    make_membership(db_session, org, member)
    site = make_site(db_session, org, code="S1")

    r = api_client.post(
        f"/mine-sites/{site.id}/assignments",
        headers=auth_headers(admin, org),
        json={"user_id": str(member.id)},
    )
    assert r.status_code == 201, r.text

    r = api_client.get(
        f"/mine-sites/{site.id}/assignments", headers=auth_headers(admin, org)
    )
    assert r.status_code == 200
    assert any(a["user_id"] == str(member.id) for a in r.json())

    r = api_client.delete(
        f"/mine-sites/{site.id}/assignments/{member.id}",
        headers=auth_headers(admin, org),
    )
    assert r.status_code == 204

    r = api_client.get(
        f"/mine-sites/{site.id}/assignments", headers=auth_headers(admin, org)
    )
    assert r.json() == []


def test_duplicate_assignment_rejected(api_client, db_session):
    org = make_org(db_session, code="ASG2")
    admin = make_user(db_session)
    make_membership(db_session, org, admin)
    site = make_site(db_session, org, code="S2")

    r = api_client.post(
        f"/mine-sites/{site.id}/assignments",
        headers=auth_headers(admin, org),
        json={"user_id": str(admin.id)},
    )
    assert r.status_code == 201

    r = api_client.post(
        f"/mine-sites/{site.id}/assignments",
        headers=auth_headers(admin, org),
        json={"user_id": str(admin.id)},
    )
    assert r.status_code == 409
