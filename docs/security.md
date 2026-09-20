# MineCore Security

## Chain of Trust

    User
     ↓
    Organization Membership
     ↓
    Role
     ↓
    Permission
     ↓
    Site Scope

## Requirements

- Authentication (JWT)
- Server-side RBAC
- PostgreSQL Row-Level Security
- Audit logging on critical operations
- Tenant isolation
- Least privilege

## Non-Negotiable

1. Never bypass organization isolation.
2. Never trust frontend authorization.
3. All authorization is enforced server-side.
4. Tenant-owned records carry organization context.
5. Critical operational records are auditable.
6. Finalized records are not silently modified.
7. Inventory and financial-like movements are immutable.
8. Secrets are never hard-coded.

## Cross-Tenant Test Requirement

Create two organizations A and B. Verify that A cannot access any of:

- B's organization profile
- B's sites
- B's users
- B's inventory
- B's production
- B's weighbridge tickets

Every such attempt must fail.
