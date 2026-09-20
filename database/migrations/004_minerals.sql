-- ============================================================
-- MineCore — Migration 004: Minerals
-- ============================================================
CREATE TABLE IF NOT EXISTS minerals (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id  UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    code             TEXT NOT NULL,
    name             TEXT NOT NULL,
    description      TEXT,
    status           TEXT NOT NULL DEFAULT 'active',
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT minerals_code_unique UNIQUE (organization_id, code),
    CONSTRAINT minerals_status_check
        CHECK (status IN ('active', 'inactive', 'archived'))
);

CREATE INDEX IF NOT EXISTS idx_minerals_org ON minerals (organization_id);
CREATE INDEX IF NOT EXISTS idx_minerals_org_status ON minerals (organization_id, status);
