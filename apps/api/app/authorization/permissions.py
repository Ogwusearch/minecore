from __future__ import annotations

from enum import StrEnum


class Permission(StrEnum):
    ORGANIZATION_READ = "organization.read"
    ORGANIZATION_MANAGE = "organization.manage"

    USER_READ = "user.read"
    USER_MANAGE = "user.manage"

    ROLE_READ = "role.read"
    ROLE_MANAGE = "role.manage"

    MINE_SITE_READ = "mine_site.read"
    MINE_SITE_MANAGE = "mine_site.manage"

    MINERAL_READ = "mineral.read"
    MINERAL_MANAGE = "mineral.manage"

    MATERIAL_READ = "material.read"
    MATERIAL_MANAGE = "material.manage"

    PRODUCTION_READ = "production.read"
    PRODUCTION_CREATE = "production.create"
    PRODUCTION_APPROVE = "production.approve"

    INVENTORY_READ = "inventory.read"
    INVENTORY_POST = "inventory.post"
    INVENTORY_ADJUST = "inventory.adjust"

    WEIGHBRIDGE_READ = "weighbridge.read"
    WEIGHBRIDGE_CREATE = "weighbridge.create"
    WEIGHBRIDGE_APPROVE = "weighbridge.approve"

    REPORT_READ = "report.read"
    REPORT_EXPORT = "report.export"

    AUDIT_READ = "audit.read"


ALL_PERMISSIONS = frozenset(Permission)