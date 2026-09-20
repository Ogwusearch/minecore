-- ============================================================
-- MineCore — Migration 002: Indexes
-- ============================================================
-- Non-unique indexes on foreign keys and common query paths.
-- Unique constraints already provide their own indexes.
-- ============================================================

-- organization_memberships
CREATE INDEX IF NOT EXISTS idx_memberships_org
    ON organization_memberships (organization_id);
CREATE INDEX IF NOT EXISTS idx_memberships_user
    ON organization_memberships (user_id);
CREATE INDEX IF NOT EXISTS idx_memberships_status
    ON organization_memberships (status);

-- employees
CREATE INDEX IF NOT EXISTS idx_employees_org
    ON employees (organization_id);
CREATE INDEX IF NOT EXISTS idx_employees_user
    ON employees (user_id);
CREATE INDEX IF NOT EXISTS idx_employees_department
    ON employees (organization_id, department);

-- roles
CREATE INDEX IF NOT EXISTS idx_roles_org
    ON roles (organization_id);

-- role_permissions
CREATE INDEX IF NOT EXISTS idx_role_permissions_permission
    ON role_permissions (permission_id);

-- membership_roles
CREATE INDEX IF NOT EXISTS idx_membership_roles_role
    ON membership_roles (role_id);

-- mine_sites
CREATE INDEX IF NOT EXISTS idx_mine_sites_org
    ON mine_sites (organization_id);
CREATE INDEX IF NOT EXISTS idx_mine_sites_status
    ON mine_sites (organization_id, status);

-- user_site_assignments
CREATE INDEX IF NOT EXISTS idx_user_site_assignments_org
    ON user_site_assignments (organization_id);
CREATE INDEX IF NOT EXISTS idx_user_site_assignments_user
    ON user_site_assignments (user_id);
CREATE INDEX IF NOT EXISTS idx_user_site_assignments_site
    ON user_site_assignments (mine_site_id);

-- Case-insensitive email lookup for authentication
CREATE INDEX IF NOT EXISTS idx_users_email_lower
    ON users (LOWER(email));
