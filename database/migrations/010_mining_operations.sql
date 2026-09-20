-- ============================================================
-- MineCore — Migration 010: Mining Operations
-- ============================================================
CREATE TABLE IF NOT EXISTS mining_operations (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id         UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    operation_seq           INTEGER NOT NULL,
    operation_number        TEXT NOT NULL,
    mine_site_id            UUID NOT NULL REFERENCES mine_sites(id) ON DELETE RESTRICT,
    pit_id                  UUID NOT NULL REFERENCES pits(id) ON DELETE RESTRICT,
    shift_id                UUID REFERENCES shifts(id) ON DELETE SET NULL,
    material_id             UUID NOT NULL REFERENCES materials(id) ON DELETE RESTRICT,
    unit_id                 UUID REFERENCES units(id) ON DELETE SET NULL,
    operation_date          DATE NOT NULL,
    quantity                NUMERIC(18,4) NOT NULL,
    operator_user_id        UUID REFERENCES users(id) ON DELETE SET NULL,
    operator_name           TEXT,
    equipment_note          TEXT,
    notes                   TEXT,
    status                  TEXT NOT NULL DEFAULT 'draft',
    created_by_user_id      UUID REFERENCES users(id) ON DELETE SET NULL,
    recorded_at             TIMESTAMPTZ,
    recorded_by_user_id     UUID REFERENCES users(id) ON DELETE SET NULL,
    approved_at             TIMESTAMPTZ,
    approved_by_user_id     UUID REFERENCES users(id) ON DELETE SET NULL,
    cancelled_at            TIMESTAMPTZ,
    cancelled_by_user_id    UUID REFERENCES users(id) ON DELETE SET NULL,
    cancellation_reason     TEXT,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT mining_operations_number_unique
        UNIQUE (organization_id, operation_number),
    CONSTRAINT mining_operations_seq_unique
        UNIQUE (organization_id, operation_seq),
    CONSTRAINT mining_operations_status_check
        CHECK (status IN ('draft', 'recorded', 'approved', 'cancelled')),
    CONSTRAINT mining_operations_quantity_check
        CHECK (quantity > 0),
    CONSTRAINT mining_operations_recorded_check
        CHECK (
            (status IN ('recorded', 'approved') AND recorded_at IS NOT NULL)
            OR status NOT IN ('recorded', 'approved')
        ),
    CONSTRAINT mining_operations_approved_check
        CHECK (
            (status = 'approved' AND approved_at IS NOT NULL AND approved_by_user_id IS NOT NULL)
            OR status <> 'approved'
        ),
    CONSTRAINT mining_operations_cancelled_check
        CHECK (
            (status = 'cancelled' AND cancelled_at IS NOT NULL AND cancellation_reason IS NOT NULL)
            OR status <> 'cancelled'
        )
);

CREATE INDEX IF NOT EXISTS idx_mining_operations_org
    ON mining_operations (organization_id);
CREATE INDEX IF NOT EXISTS idx_mining_operations_site
    ON mining_operations (mine_site_id);
CREATE INDEX IF NOT EXISTS idx_mining_operations_pit
    ON mining_operations (pit_id);
CREATE INDEX IF NOT EXISTS idx_mining_operations_status
    ON mining_operations (organization_id, status);
CREATE INDEX IF NOT EXISTS idx_mining_operations_date
    ON mining_operations (organization_id, operation_date);
CREATE INDEX IF NOT EXISTS idx_mining_operations_number
    ON mining_operations (organization_id, operation_number);
