-- ============================================================
-- MineCore — Migration 007: Deposits
-- ============================================================
CREATE TABLE IF NOT EXISTS deposits (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id     UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    mine_site_id        UUID NOT NULL REFERENCES mine_sites(id) ON DELETE CASCADE,
    primary_mineral_id  UUID REFERENCES minerals(id) ON DELETE SET NULL,
    code                TEXT NOT NULL,
    name                TEXT NOT NULL,
    description         TEXT,
    status              TEXT NOT NULL DEFAULT 'active',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT deposits_code_unique UNIQUE (organization_id, code),
    CONSTRAINT deposits_status_check
        CHECK (status IN ('active', 'inactive', 'depleted'))
);

CREATE INDEX IF NOT EXISTS idx_deposits_org ON deposits (organization_id);
CREATE INDEX IF NOT EXISTS idx_deposits_site ON deposits (mine_site_id);
CREATE INDEX IF NOT EXISTS idx_deposits_mineral ON deposits (primary_mineral_id);
