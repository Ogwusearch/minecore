from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models import (
    Employee,
    MineSite,
    Organization,
    OrganizationMembership,
    User,
)


def make_org(
    session: Session, code: str | None = None, name: str | None = None
) -> Organization:
    code = code or f"ORG-{uuid4().hex[:8].upper()}"
    org = Organization(code=code, name=name or f"Org {code}", status="active")
    session.add(org)
    session.flush()
    return org


def make_user(
    session: Session, email: str | None = None, active: bool = True
) -> User:
    email = email or f"user-{uuid4().hex[:8]}@example.test"
    user = User(
        email=email,
        password_hash="not-used-in-phase-03",
        full_name="Test User",
        is_active=active,
    )
    session.add(user)
    session.flush()
    return user


def make_membership(
    session: Session,
    org: Organization,
    user: User,
    status: str = "active",
) -> OrganizationMembership:
    m = OrganizationMembership(
        organization_id=org.id,
        user_id=user.id,
        status=status,
        joined_at=datetime.now(timezone.utc) if status == "active" else None,
    )
    session.add(m)
    session.flush()
    return m


def make_site(
    session: Session,
    org: Organization,
    code: str | None = None,
    name: str | None = None,
) -> MineSite:
    code = code or f"SITE-{uuid4().hex[:8].upper()}"
    site = MineSite(
        organization_id=org.id,
        code=code,
        name=name or f"Site {code}",
        status="active",
    )
    session.add(site)
    session.flush()
    return site


def make_employee(
    session: Session,
    org: Organization,
    number: str | None = None,
    full_name: str | None = None,
) -> Employee:
    number = number or f"E-{uuid4().hex[:6].upper()}"
    emp = Employee(
        organization_id=org.id,
        employee_number=number,
        full_name=full_name or f"Employee {number}",
        status="active",
    )
    session.add(emp)
    session.flush()
    return emp


def auth_headers(user: User, org: Organization) -> dict[str, str]:
    return {
        "X-User-Id": str(user.id),
        "X-Organization-Id": str(org.id),
    }
