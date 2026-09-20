-- ============================================================
-- MineCore — Migration 005: Material Types
-- ============================================================
CREATE TABLE IF NOT EXISTS material_types (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id  UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    code             TEXT NOT NULL,
    name             TEXT NOT NULL,
    description      TEXT,
    status           TEXT NOT NULL DEFAULT 'active',
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT material_types_code_unique UNIQUE (organization_id, code),
    CONSTRAINT material_types_status_check
        CHECK (status IN ('active', 'inactive', 'archived'))
);

CREATE INDEX IF NOT EXISTS idx_material_types_org ON material_types (organization_id);
