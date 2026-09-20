-- ============================================================
-- MineCore — Migration 003: Units of Measure
-- ============================================================
CREATE TABLE IF NOT EXISTS units (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id  UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    code             TEXT NOT NULL,
    name             TEXT NOT NULL,
    symbol           TEXT NOT NULL,
    dimension        TEXT NOT NULL,
    status           TEXT NOT NULL DEFAULT 'active',
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT units_code_unique UNIQUE (organization_id, code),
    CONSTRAINT units_status_check
        CHECK (status IN ('active', 'inactive', 'archived')),
    CONSTRAINT units_dimension_check
        CHECK (dimension IN ('mass', 'volume', 'length', 'count', 'time', 'other'))
);

CREATE INDEX IF NOT EXISTS idx_units_org ON units (organization_id);
CREATE INDEX IF NOT EXISTS idx_units_org_status ON units (organization_id, status);
