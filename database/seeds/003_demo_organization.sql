-- ============================================================
-- MineCore — Seed 003: Demo Organization
-- ============================================================
-- Deterministic UUIDs so this seed is idempotent and safe to
-- re-run. The demo user is intentionally DISABLED until Phase 02
-- implements password hashing and authentication.
-- ============================================================

-- ------------------------------------------------------------
-- Demo organization
-- ------------------------------------------------------------
INSERT INTO organizations (id, code, name, status) VALUES
    ('00000000-0000-0000-0000-000000000001',
     'demo', 'Demo Mining Co.', 'active')
ON CONFLICT (id) DO NOTHING;

-- ------------------------------------------------------------
-- Demo user (disabled — password is set in Phase 02)
-- ------------------------------------------------------------
INSERT INTO users (id, email, password_hash, full_name, is_active) VALUES
    ('00000000-0000-0000-0000-000000000002',
     'admin@demo.local',
     '<PHASE_02_WILL_SET_PASSWORD_HASH>',
     'Demo Administrator',
     FALSE)
ON CONFLICT (id) DO NOTHING;

-- ------------------------------------------------------------
-- Demo membership
-- ------------------------------------------------------------
INSERT INTO organization_memberships (
    id, organization_id, user_id, status, joined_at
) VALUES (
    '00000000-0000-0000-0000-000000000003',
    '00000000-0000-0000-0000-000000000001',
    '00000000-0000-0000-0000-000000000002',
    'active',
    NOW()
)
ON CONFLICT (id) DO NOTHING;

-- ------------------------------------------------------------
-- Assign org_admin
-- ------------------------------------------------------------
INSERT INTO membership_roles (membership_id, role_id)
SELECT
    '00000000-0000-0000-0000-000000000003'::uuid,
    r.id
FROM roles r
WHERE r.code = 'org_admin' AND r.is_system = TRUE
ON CONFLICT DO NOTHING;

-- ------------------------------------------------------------
-- Demo mine site
-- ------------------------------------------------------------
INSERT INTO mine_sites (
    id, organization_id, code, name, status, location, latitude, longitude
) VALUES (
    '00000000-0000-0000-0000-000000000004',
    '00000000-0000-0000-0000-000000000001',
    'DEMO-01',
    'Demo Site Alpha',
    'active',
    'Demo Region',
    6.524379, 3.379206
)
ON CONFLICT (id) DO NOTHING;

-- ------------------------------------------------------------
-- Assign demo user to demo site
-- ------------------------------------------------------------
INSERT INTO user_site_assignments (
    id, organization_id, user_id, mine_site_id
) VALUES (
    '00000000-0000-0000-0000-000000000005',
    '00000000-0000-0000-0000-000000000001',
    '00000000-0000-0000-0000-000000000002',
    '00000000-0000-0000-0000-000000000004'
)
ON CONFLICT (id) DO NOTHING;
