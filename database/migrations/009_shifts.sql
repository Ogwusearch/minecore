-- ============================================================
-- MineCore — Migration 009: Shifts
-- ============================================================
CREATE TABLE IF NOT EXISTS shifts (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id  UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    mine_site_id     UUID REFERENCES mine_sites(id) ON DELETE CASCADE,
    code             TEXT NOT NULL,
    name             TEXT NOT NULL,
    start_time       TIME NOT NULL,
    end_time         TIME NOT NULL,
    status           TEXT NOT NULL DEFAULT 'active',
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT shifts_code_unique UNIQUE (organization_id, code),
    CONSTRAINT shifts_status_check
        CHECK (status IN ('active', 'inactive'))
);

CREATE INDEX IF NOT EXISTS idx_shifts_org ON shifts (organization_id);
CREATE INDEX IF NOT EXISTS idx_shifts_site ON shifts (mine_site_id);
