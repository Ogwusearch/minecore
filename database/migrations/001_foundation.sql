-- ============================================================
-- MineCore — Migration 001: Foundation
-- ============================================================
-- Enables UUID generation and creates the core identity,
-- organization, and access-control tables.
--
-- All tables use UUID primary keys, TIMESTAMPTZ timestamps in UTC,
-- explicit foreign keys, and CHECK / UNIQUE constraints.
-- ============================================================

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ------------------------------------------------------------
-- organizations
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS organizations (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code        TEXT NOT NULL,
    name        TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'active',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT organizations_code_unique UNIQUE (code),
    CONSTRAINT organizations_status_check
        CHECK (status IN ('active', 'inactive', 'suspended'))
);

-- ------------------------------------------------------------
-- users
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email          TEXT NOT NULL,
    password_hash  TEXT NOT NULL,
    full_name      TEXT NOT NULL,
    is_active      BOOLEAN NOT NULL DEFAULT TRUE,
    last_login_at  TIMESTAMPTZ,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT users_email_unique UNIQUE (email),
    CONSTRAINT users_email_lowercase_check
        CHECK (email = LOWER(email)),
    CONSTRAINT users_email_shape_check
        CHECK (email LIKE '%_@_%._%')
);

-- ------------------------------------------------------------
-- organization_memberships
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS organization_memberships (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id  UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id          UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status           TEXT NOT NULL DEFAULT 'invited',
    joined_at        TIMESTAMPTZ,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT organization_memberships_unique
        UNIQUE (organization_id, user_id),
    CONSTRAINT organization_memberships_status_check
        CHECK (status IN ('invited', 'active', 'inactive', 'suspended')),
    CONSTRAINT organization_memberships_joined_check
        CHECK ((status = 'active' AND joined_at IS NOT NULL)
            OR (status <> 'active'))
);

-- ------------------------------------------------------------
-- employees
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS employees (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id  UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id          UUID REFERENCES users(id) ON DELETE SET NULL,
    employee_number  TEXT NOT NULL,
    full_name        TEXT NOT NULL,
    job_title        TEXT,
    department       TEXT,
    hire_date        DATE,
    status           TEXT NOT NULL DEFAULT 'active',
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT employees_number_unique
        UNIQUE (organization_id, employee_number),
    CONSTRAINT employees_user_unique
        UNIQUE (organization_id, user_id),
    CONSTRAINT employees_status_check
        CHECK (status IN ('active', 'inactive', 'terminated'))
);

-- ------------------------------------------------------------
-- roles
-- ------------------------------------------------------------
-- organization_id IS NULL  → system role (visible to all orgs)
-- organization_id NOT NULL → organization-scoped role
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS roles (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id  UUID REFERENCES organizations(id) ON DELETE CASCADE,
    code             TEXT NOT NULL,
    name             TEXT NOT NULL,
    description      TEXT,
    is_system        BOOLEAN NOT NULL DEFAULT FALSE,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT roles_system_scope_check
        CHECK ((is_system = TRUE  AND organization_id IS NULL)
            OR (is_system = FALSE AND organization_id IS NOT NULL))
);

CREATE UNIQUE INDEX IF NOT EXISTS roles_org_code_unique
    ON roles (organization_id, code)
    WHERE organization_id IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS roles_system_code_unique
    ON roles (code)
    WHERE organization_id IS NULL;

-- ------------------------------------------------------------
-- permissions
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS permissions (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code         TEXT NOT NULL,
    description  TEXT,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT permissions_code_unique UNIQUE (code),
    CONSTRAINT permissions_code_shape_check
        CHECK (code ~ '^[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*$')
);

-- ------------------------------------------------------------
-- role_permissions
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS role_permissions (
    role_id        UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    permission_id  UUID NOT NULL REFERENCES permissions(id) ON DELETE CASCADE,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (role_id, permission_id)
);

-- ------------------------------------------------------------
-- membership_roles
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS membership_roles (
    membership_id  UUID NOT NULL REFERENCES organization_memberships(id) ON DELETE CASCADE,
    role_id        UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (membership_id, role_id)
);

-- ------------------------------------------------------------
-- mine_sites
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS mine_sites (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id  UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    code             TEXT NOT NULL,
    name             TEXT NOT NULL,
    status           TEXT NOT NULL DEFAULT 'active',
    location         TEXT,
    latitude         NUMERIC(9, 6),
    longitude        NUMERIC(9, 6),
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT mine_sites_code_unique UNIQUE (organization_id, code),
    CONSTRAINT mine_sites_status_check
        CHECK (status IN ('active', 'inactive', 'closed')),
    CONSTRAINT mine_sites_latitude_check
        CHECK (latitude IS NULL OR (latitude BETWEEN -90 AND 90)),
    CONSTRAINT mine_sites_longitude_check
        CHECK (longitude IS NULL OR (longitude BETWEEN -180 AND 180))
);

-- ------------------------------------------------------------
-- user_site_assignments
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS user_site_assignments (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id  UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id          UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    mine_site_id     UUID NOT NULL REFERENCES mine_sites(id) ON DELETE CASCADE,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT user_site_assignments_unique
        UNIQUE (user_id, mine_site_id)
);
