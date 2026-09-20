# MineCore Architecture

## Layers

    Frontend (React / Vite)
            ↓
    FastAPI (Python)
            ↓
    Domain Services
            ↓
    PostgreSQL

## Stack

**Frontend**
- React
- Vite
- React Router
- TanStack Query
- IndexedDB (offline)

**Backend**
- FastAPI
- Python 3.11+
- Pydantic
- SQLAlchemy (from Phase 01)
- Service-oriented domain architecture

**Database**
- PostgreSQL 17
- UUID primary keys
- Foreign keys, constraints, indexes
- Transactions
- Row-Level Security

**Infrastructure**
- Docker / Docker Compose
- Environment-based configuration

## Multi-Tenancy

The fundamental security boundary is the Organization.

    Organization
         ↓
    Mine Site
         ↓
    Deposit
         ↓
    Pit
         ↓
    Mining Operation

Authorization derives from:

    organization membership
            +
          role
            +
        permission
            +
        site scope

Tenant-owned tables carry organization_id. PostgreSQL RLS enforces
isolation. Frontend restrictions are UX only.
