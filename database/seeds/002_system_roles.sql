-- ============================================================
-- MineCore — Seed 002: System Roles
-- ============================================================
-- System roles have organization_id = NULL and are visible to
-- all organizations. Idempotent. Safe to re-run.
-- ============================================================

-- ------------------------------------------------------------
-- Roles
-- ------------------------------------------------------------
INSERT INTO roles (organization_id, code, name, description, is_system) VALUES
    (NULL, 'org_admin',    'Organization Administrator',
        'Full administrative control of a single organization.', TRUE),
    (NULL, 'site_manager', 'Site Manager',
        'Manages operations at assigned mine sites.', TRUE),
    (NULL, 'operator',     'Field Operator',
        'Records production, weighbridge and field operations.', TRUE),
    (NULL, 'viewer',       'Viewer',
        'Read-only access to the organization.', TRUE),
    (NULL, 'auditor',      'Auditor',
        'Read-only access including audit logs.', TRUE)
ON CONFLICT DO NOTHING;

-- ------------------------------------------------------------
-- org_admin — every permission
-- ------------------------------------------------------------
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM roles r
CROSS JOIN permissions p
WHERE r.code = 'org_admin' AND r.is_system = TRUE
ON CONFLICT DO NOTHING;

-- ------------------------------------------------------------
-- site_manager
-- ------------------------------------------------------------
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM roles r
JOIN permissions p ON p.code IN (
    'organization.read',
    'user.read',
    'role.read',
    'mine_site.read',
    'mineral.read',   'mineral.manage',
    'material.read',  'material.manage',
    'production.read', 'production.create', 'production.approve',
    'inventory.read',  'inventory.post',
    'weighbridge.read', 'weighbridge.create', 'weighbridge.approve',
    'report.read', 'report.export'
)
WHERE r.code = 'site_manager' AND r.is_system = TRUE
ON CONFLICT DO NOTHING;

-- ------------------------------------------------------------
-- operator
-- ------------------------------------------------------------
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM roles r
JOIN permissions p ON p.code IN (
    'organization.read',
    'mine_site.read',
    'mineral.read',
    'material.read',
    'production.read', 'production.create',
    'inventory.read',
    'weighbridge.read', 'weighbridge.create'
)
WHERE r.code = 'operator' AND r.is_system = TRUE
ON CONFLICT DO NOTHING;

-- ------------------------------------------------------------
-- viewer — every *.read
-- ------------------------------------------------------------
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM roles r
JOIN permissions p ON p.code LIKE '%.read'
WHERE r.code = 'viewer' AND r.is_system = TRUE
ON CONFLICT DO NOTHING;

-- ------------------------------------------------------------
-- auditor — every *.read plus audit.read
-- ------------------------------------------------------------
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM roles r
JOIN permissions p ON (p.code LIKE '%.read' OR p.code = 'audit.read')
WHERE r.code = 'auditor' AND r.is_system = TRUE
ON CONFLICT DO NOTHING;
