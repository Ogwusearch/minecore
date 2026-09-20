-- ============================================================
-- MineCore — Migration 008: Pits
-- ============================================================
CREATE TABLE IF NOT EXISTS pits (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id  UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    mine_site_id     UUID NOT NULL REFERENCES mine_sites(id) ON DELETE CASCADE,
    deposit_id       UUID REFERENCES deposits(id) ON DELETE SET NULL,
    code             TEXT NOT NULL,
    name             TEXT NOT NULL,
    depth_m          NUMERIC(10,2),
    status           TEXT NOT NULL DEFAULT 'active',
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT pits_code_unique UNIQUE (organization_id, code),
    CONSTRAINT pits_status_check
        CHECK (status IN ('active', 'inactive', 'closed')),
    CONSTRAINT pits_depth_check
        CHECK (depth_m IS NULL OR depth_m >= 0)
);

CREATE INDEX IF NOT EXISTS idx_pits_org ON pits (organization_id);
CREATE INDEX IF NOT EXISTS idx_pits_site ON pits (mine_site_id);
CREATE INDEX IF NOT EXISTS idx_pits_deposit ON pits (deposit_id);
