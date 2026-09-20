# MineCore Database

PostgreSQL schema, migrations and reference data.

## Layout

    database/
    ├── migrations/    ordered, immutable schema changes
    ├── seeds/         idempotent reference data
    ├── functions/     SQL functions (Phase 01+)
    └── policies/      Row-Level Security policies (Phase 19)

## Migration Order

    001_foundation.sql
    002_indexes.sql

## Seed Order

    001_permissions.sql
    002_system_roles.sql
    003_demo_organization.sql

## Rules

- Migrations are applied in lexicographic order.
- Each migration is tracked in `schema_migrations`.
- Migrations must be safe to run from an empty database.
- Seeds are idempotent (ON CONFLICT DO NOTHING) and may be re-run.
- DDL is owned by migrations, never by ORM `create_all`.
