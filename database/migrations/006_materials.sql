-- ============================================================
-- MineCore — Migration 006: Materials
-- ============================================================
CREATE TABLE IF NOT EXISTS materials (
    id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id    UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    material_type_id   UUID REFERENCES material_types(id) ON DELETE SET NULL,
    mineral_id         UUID REFERENCES minerals(id) ON DELETE SET NULL,
    unit_id            UUID REFERENCES units(id) ON DELETE SET NULL,
    code               TEXT NOT NULL,
    name               TEXT NOT NULL,
    description        TEXT,
    status             TEXT NOT NULL DEFAULT 'active',
    created_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT materials_code_unique UNIQUE (organization_id, code),
    CONSTRAINT materials_status_check
        CHECK (status IN ('active', 'inactive', 'archived'))
);

CREATE INDEX IF NOT EXISTS idx_materials_org ON materials (organization_id);
CREATE INDEX IF NOT EXISTS idx_materials_org_status ON materials (organization_id, status);
CREATE INDEX IF NOT EXISTS idx_materials_type ON materials (material_type_id);
CREATE INDEX IF NOT EXISTS idx_materials_mineral ON materials (mineral_id);
CREATE INDEX IF NOT EXISTS idx_materials_unit ON materials (unit_id);
