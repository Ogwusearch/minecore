from tests.integration._helpers import (
    auth_headers,
    make_membership,
    make_org,
    make_site,
    make_user,
)


def test_create_and_list_mine_sites(api_client, db_session):
    org = make_org(db_session, code="MS1")
    user = make_user(db_session)
    make_membership(db_session, org, user)

    r = api_client.post(
        "/mine-sites",
        headers=auth_headers(user, org),
        json={"code": "PIT-01", "name": "Pit One", "status": "active"},
    )
    assert r.status_code == 201, r.text
    created = r.json()
    assert created["code"] == "PIT-01"
    assert created["organization_id"] == str(org.id)

    r = api_client.get("/mine-sites", headers=auth_headers(user, org))
    assert r.status_code == 200
    codes = [s["code"] for s in r.json()]
    assert "PIT-01" in codes


def test_duplicate_site_code_rejected(api_client, db_session):
    org = make_org(db_session, code="MS2")
    user = make_user(db_session)
    make_membership(db_session, org, user)
    make_site(db_session, org, code="DUP")

    r = api_client.post(
        "/mine-sites",
        headers=auth_headers(user, org),
        json={"code": "DUP", "name": "Duplicate"},
    )
    assert r.status_code == 409


def test_update_mine_site(api_client, db_session):
    org = make_org(db_session, code="MS3")
    user = make_user(db_session)
    make_membership(db_session, org, user)
    site = make_site(db_session, org, code="UPD")

    r = api_client.patch(
        f"/mine-sites/{site.id}",
        headers=auth_headers(user, org),
        json={"name": "Updated Site", "status": "inactive"},
    )
    assert r.status_code == 200
    assert r.json()["name"] == "Updated Site"
    assert r.json()["status"] == "inactive"


def test_delete_mine_site(api_client, db_session):
    org = make_org(db_session, code="MS4")
    user = make_user(db_session)
    make_membership(db_session, org, user)
    site = make_site(db_session, org, code="DEL")

    r = api_client.delete(f"/mine-sites/{site.id}", headers=auth_headers(user, org))
    assert r.status_code == 204

    r = api_client.get(f"/mine-sites/{site.id}", headers=auth_headers(user, org))
    assert r.status_code == 404


def test_mine_site_latitude_validation(api_client, db_session):
    org = make_org(db_session, code="MS5")
    user = make_user(db_session)
    make_membership(db_session, org, user)

    r = api_client.post(
        "/mine-sites",
        headers=auth_headers(user, org),
        json={"code": "LAT", "name": "Bad", "latitude": "95"},
    )
    assert r.status_code == 422
