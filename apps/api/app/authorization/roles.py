from __future__ import annotations

from enum import StrEnum

from .permissions import Permission


class Role(StrEnum):
    ADMIN = "admin"
    MANAGER = "manager"
    ENGINEER = "engineer"
    OPERATOR = "operator"
    AUDITOR = "auditor"
    VIEWER = "viewer"


ROLE_PERMISSIONS: dict[Role, frozenset[Permission]] = {
    Role.ADMIN: frozenset(Permission),

    Role.MANAGER: frozenset(
        {
            Permission.ORGANIZATION_READ,
            Permission.USER_READ,
            Permission.USER_MANAGE,
            Permission.ROLE_READ,
            Permission.MINE_SITE_READ,
            Permission.MINE_SITE_MANAGE,
            Permission.MINERAL_READ,
            Permission.MINERAL_MANAGE,
            Permission.MATERIAL_READ,
            Permission.MATERIAL_MANAGE,
            Permission.PRODUCTION_READ,
            Permission.PRODUCTION_CREATE,
            Permission.PRODUCTION_APPROVE,
            Permission.INVENTORY_READ,
            Permission.INVENTORY_POST,
            Permission.INVENTORY_ADJUST,
            Permission.WEIGHBRIDGE_READ,
            Permission.WEIGHBRIDGE_CREATE,
            Permission.WEIGHBRIDGE_APPROVE,
            Permission.REPORT_READ,
            Permission.REPORT_EXPORT,
            Permission.AUDIT_READ,
        }
    ),

    Role.ENGINEER: frozenset(
        {
            Permission.MINE_SITE_READ,
            Permission.MINERAL_READ,
            Permission.MATERIAL_READ,
            Permission.PRODUCTION_READ,
            Permission.PRODUCTION_CREATE,
            Permission.INVENTORY_READ,
            Permission.WEIGHBRIDGE_READ,
            Permission.REPORT_READ,
        }
    ),

    Role.OPERATOR: frozenset(
        {
            Permission.MINE_SITE_READ,
            Permission.MINERAL_READ,
            Permission.MATERIAL_READ,
            Permission.PRODUCTION_READ,
            Permission.PRODUCTION_CREATE,
            Permission.INVENTORY_READ,
            Permission.INVENTORY_POST,
            Permission.WEIGHBRIDGE_READ,
            Permission.WEIGHBRIDGE_CREATE,
        }
    ),

    Role.AUDITOR: frozenset(
        {
            Permission.ORGANIZATION_READ,
            Permission.USER_READ,
            Permission.ROLE_READ,
            Permission.MINE_SITE_READ,
            Permission.MINERAL_READ,
            Permission.MATERIAL_READ,
            Permission.PRODUCTION_READ,
            Permission.INVENTORY_READ,
            Permission.WEIGHBRIDGE_READ,
            Permission.REPORT_READ,
            Permission.REPORT_EXPORT,
            Permission.AUDIT_READ,
        }
    ),

    Role.VIEWER: frozenset(
        {
            Permission.ORGANIZATION_READ,
            Permission.MINE_SITE_READ,
            Permission.MINERAL_READ,
            Permission.MATERIAL_READ,
            Permission.PRODUCTION_READ,
            Permission.INVENTORY_READ,
            Permission.WEIGHBRIDGE_READ,
            Permission.REPORT_READ,
        }
    ),
}