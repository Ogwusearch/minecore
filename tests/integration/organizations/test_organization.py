from tests.integration._helpers import auth_headers, make_membership, make_org, make_user


def test_get_current_organization(api_client, db_session):
    org = make_org(db_session, code="ACME", name="Acme Mining")
    user = make_user(db_session)
    make_membership(db_session, org, user)

    r = api_client.get("/organizations/current", headers=auth_headers(user, org))
    assert r.status_code == 200
    body = r.json()
    assert body["code"] == "ACME"
    assert body["name"] == "Acme Mining"
    assert body["id"] == str(org.id)


def test_update_current_organization(api_client, db_session):
    org = make_org(db_session, code="UPD")
    user = make_user(db_session)
    make_membership(db_session, org, user)

    r = api_client.patch(
        "/organizations/current",
        headers=auth_headers(user, org),
        json={"name": "Renamed Org", "status": "inactive"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == "Renamed Org"
    assert body["status"] == "inactive"


def test_get_current_organization_unknown_id_returns_404(api_client, db_session):
    org = make_org(db_session, code="KNOWN")
    user = make_user(db_session)
    make_membership(db_session, org, user)

    from uuid import uuid4

    bogus = uuid4()
    r = api_client.get(
        "/organizations/current",
        headers={"X-User-Id": str(user.id), "X-Organization-Id": str(bogus)},
    )
    assert r.status_code == 404
