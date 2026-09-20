-- ============================================================
-- MineCore — Migration 011: Audit Logs
-- ============================================================
-- Generic audit trail. Any entity in MineCore can append entries
-- keyed by (entity_type, entity_id). Rows are immutable by policy —
-- no UPDATE or DELETE endpoints touch this table.
-- ============================================================
CREATE TABLE IF NOT EXISTS audit_logs (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id  UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    actor_user_id    UUID REFERENCES users(id) ON DELETE SET NULL,
    entity_type      TEXT NOT NULL,
    entity_id        UUID NOT NULL,
    action           TEXT NOT NULL,
    from_status      TEXT,
    to_status        TEXT,
    changes          JSONB,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_audit_logs_org
    ON audit_logs (organization_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_entity
    ON audit_logs (entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created
    ON audit_logs (organization_id, created_at DESC);
