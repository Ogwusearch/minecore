from tests.integration._helpers import (
    auth_headers,
    make_employee,
    make_membership,
    make_org,
    make_user,
)


def test_create_and_list_employees(api_client, db_session):
    org = make_org(db_session, code="EMP1")
    user = make_user(db_session)
    make_membership(db_session, org, user)

    r = api_client.post(
        "/employees",
        headers=auth_headers(user, org),
        json={
            "employee_number": "E-100",
            "full_name": "Jane Miner",
            "job_title": "Geologist",
            "department": "Exploration",
        },
    )
    assert r.status_code == 201, r.text
    assert r.json()["employee_number"] == "E-100"

    r = api_client.get("/employees", headers=auth_headers(user, org))
    assert r.status_code == 200
    numbers = [e["employee_number"] for e in r.json()]
    assert "E-100" in numbers


def test_duplicate_employee_number_rejected(api_client, db_session):
    org = make_org(db_session, code="EMP2")
    user = make_user(db_session)
    make_membership(db_session, org, user)
    make_employee(db_session, org, number="E-DUP")

    r = api_client.post(
        "/employees",
        headers=auth_headers(user, org),
        json={"employee_number": "E-DUP", "full_name": "Another"},
    )
    assert r.status_code == 409


def test_link_employee_to_user(api_client, db_session):
    org = make_org(db_session, code="EMP3")
    admin = make_user(db_session)
    target_user = make_user(db_session)
    make_membership(db_session, org, admin)
    make_membership(db_session, org, target_user)
    emp = make_employee(db_session, org)

    r = api_client.patch(
        f"/employees/{emp.id}",
        headers=auth_headers(admin, org),
        json={"user_id": str(target_user.id)},
    )
    assert r.status_code == 200, r.text
    assert r.json()["user_id"] == str(target_user.id)


def test_delete_employee(api_client, db_session):
    org = make_org(db_session, code="EMP4")
    user = make_user(db_session)
    make_membership(db_session, org, user)
    emp = make_employee(db_session, org)

    r = api_client.delete(f"/employees/{emp.id}", headers=auth_headers(user, org))
    assert r.status_code == 204
    r = api_client.get(f"/employees/{emp.id}", headers=auth_headers(user, org))
    assert r.status_code == 404
