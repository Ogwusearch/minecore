-- ============================================================
-- MineCore — Seed 001: Permissions
-- ============================================================
-- Idempotent reference data. Safe to re-run.
-- ============================================================

INSERT INTO permissions (code, description) VALUES
    ('organization.read',    'View organization profile and settings'),
    ('organization.manage',  'Modify organization profile and settings'),

    ('user.read',            'View users in the organization'),
    ('user.manage',          'Invite, disable and manage users'),

    ('role.read',            'View roles and permissions'),
    ('role.manage',          'Create and modify roles'),

    ('mine_site.read',       'View mine sites'),
    ('mine_site.manage',     'Create and modify mine sites'),

    ('mineral.read',         'View minerals'),
    ('mineral.manage',       'Create and modify minerals'),

    ('material.read',        'View materials'),
    ('material.manage',      'Create and modify materials'),

    ('production.read',      'View production records'),
    ('production.create',    'Create production records'),
    ('production.approve',   'Approve production records'),

    ('inventory.read',       'View inventory balances and transactions'),
    ('inventory.post',       'Post inventory transactions'),
    ('inventory.adjust',     'Post inventory adjustments'),

    ('weighbridge.read',     'View weighbridge tickets'),
    ('weighbridge.create',   'Create weighbridge tickets'),
    ('weighbridge.approve',  'Approve weighbridge tickets'),

    ('report.read',          'View reports'),
    ('report.export',        'Export reports'),

    ('audit.read',           'View audit logs')
ON CONFLICT (code) DO NOTHING;
