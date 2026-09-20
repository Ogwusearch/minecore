# MineCore Database

## Principles

- UUID primary keys
- TIMESTAMPTZ for all timestamps (UTC)
- NUMERIC for quantities and currency
- Foreign keys on every relationship
- CHECK constraints for domain rules
- Unique constraints for codes and natural keys
- Indexes on foreign keys and query paths
- Transactions for multi-table operations

## Core Hierarchy

    Organization
        ↓
    Mine Site
        ↓
    Deposit
        ↓
    Pit
        ↓
    Mining Operation
        ↓
    Production
        ↓
    Stockpile
        ↓
    Processing
        ↓
    Inventory
        ↓
    Weighbridge
        ↓
    Shipment
        ↓
    Customer

## Migration Policy

- Migrations are ordered and immutable once applied.
- Every migration must run from an empty database.
- Every migration must be safe to run twice.
- No business data is stored in migration files.

## Inventory Ledger

Inventory is never stored as a mutable quantity. All movements are
immutable transaction rows with an idempotency key.

## Row-Level Security

Tenant-owned tables enable RLS policies keyed off organization_id.
Site-scoped tables further restrict by site scope.
