# MineCore

## Mining Operations & Management Platform

**Master Development Phases, Bash Setup Instructions & Coding-Agent Workflow**

**Project Root**

```text
/home/ogwu/workspace/minecore
```

---

# 1. Project Overview

MineCore is a production-oriented Mining Operations & Management Platform designed to manage the operational chain:

```text
Exploration
    ↓
Geology
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
    ↓
Sales / Finance
```

The platform is multi-tenant and designed around:

* Organization isolation
* Mine-site isolation
* Role-based access control
* Permission-based authorization
* Auditable transactions
* PostgreSQL Row-Level Security
* Offline field operations
* Immutable inventory movements
* Traceability
* Operational dashboards
* Reporting
* Security
* Production deployment

---

# 2. Architecture

```text
┌──────────────────────────────────────┐
│              React Web               │
│       Vite + React + Router          │
│ TanStack Query + IndexedDB + PWA     │
└──────────────────┬───────────────────┘
                   │ HTTP
                   ▼
┌──────────────────────────────────────┐
│              FastAPI                 │
│       Authentication / API           │
│       Domain Services                │
│       Authorization                  │
│       Validation                     │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│          PostgreSQL Database         │
│                                      │
│ UUID / FK / CHECK / UNIQUE / INDEX  │
│ Transactions / RLS / Audit           │
└──────────────────────────────────────┘
```

---

# 3. Development Philosophy

MineCore must be developed phase-by-phase.

Do not implement future phases prematurely.

Each phase follows:

```text
Inspect
   ↓
Plan
   ↓
Bash Scaffold
   ↓
Implement
   ↓
Test
   ↓
Security Review
   ↓
Documentation
   ↓
Verification
   ↓
Phase Gate
```

A phase is complete only when its acceptance criteria pass.

---

# 4. Bash vs Coding Agent Responsibilities

## Bash is responsible for

Use Bash for deterministic filesystem and environment work:

* Creating directories
* Creating missing files
* Setting permissions
* Creating environment templates
* Starting/stopping Docker services
* Running migrations
* Running tests
* Running lint/typecheck/build commands
* Checking repository structure
* Git operations

Bash scripts should:

```bash
set -euo pipefail
```

Scripts must:

* Work from any directory
* Resolve the repository root
* Avoid overwriting existing files unless explicitly intended
* Fail loudly
* Avoid hiding errors

## Coding agent is responsible for

Use the coding agent for reasoning-heavy work:

* Inspecting existing architecture
* Implementing application logic
* Database design
* API implementation
* Authorization
* Business rules
* React components
* Service layers
* Tests
* Refactoring
* Security review
* Debugging

The coding agent must inspect the repository before changing existing code.

---

# 5. Standard Bash Pattern

Every phase should use a predictable scaffold script.

Example:

```bash
#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "MineCore phase setup"
echo "Project: $PROJECT_ROOT"

mkdir -p "$PROJECT_ROOT/docs"

create_file() {
    local file="$1"

    if [[ -e "$file" ]]; then
        echo "SKIP   $file"
    else
        touch "$file"
        echo "CREATE $file"
    fi
}

create_dir() {
    local dir="$1"

    if [[ -d "$dir" ]]; then
        echo "SKIP   $dir"
    else
        mkdir -p "$dir"
        echo "CREATE $dir"
    fi
}
```

The important rule is:

```text
Existing working files → SKIP
Missing required files → CREATE
```

Do not overwrite working implementation merely because a phase script is executed again.

---

# 6. Standard Phase Execution

From the project root:

```bash
cd /home/ogwu/workspace/minecore
```

Inspect:

```bash
git status
find . -maxdepth 4 -type f | sort
```

Run the phase scaffold:

```bash
chmod +x scripts/phase-XX.sh
./scripts/phase-XX.sh
```

Then give the repository to the coding agent.

After implementation:

```bash
./scripts/test.sh
```

Then inspect:

```bash
git status
git diff --stat
```

---

# 7. Phase 00 — Project Foundation

## Objective

Create the MineCore application foundation.

## Scope

* Git
* React/Vite
* FastAPI
* PostgreSQL
* Docker
* Environment configuration
* Basic documentation
* Testing
* Formatting
* Linting
* Health endpoint

No mining business functionality.

## Bash Setup

Create:

```text
apps/web
apps/api
database
docs
scripts
```

Create:

```text
README.md
.env.example
.gitignore
docker-compose.yml
Makefile
```

Create frontend foundation:

```text
apps/web/package.json
apps/web/vite.config.js
apps/web/index.html
apps/web/src/main.jsx
apps/web/src/App.jsx
apps/web/src/app/AppRouter.jsx
apps/web/src/app/AppLayout.jsx
```

Create backend foundation:

```text
apps/api/requirements.txt
apps/api/pyproject.toml
apps/api/app/main.py
apps/api/app/core/config.py
apps/api/app/core/logging.py
apps/api/app/health/routes.py
```

Create scripts:

```text
scripts/setup.sh
scripts/dev.sh
scripts/test.sh
```

## PostgreSQL

Docker Compose should provide:

```text
minecore-postgres
```

using PostgreSQL 17.

## Acceptance

```text
Browser
   ↓
React
   ↓
FastAPI
   ↓
PostgreSQL
```

Health endpoint:

```text
GET /health
```

must work.

---

# 8. Phase 01 — Database Foundation

## Objective

Create the foundational PostgreSQL schema.

## Bash Setup

Create:

```text
database/
├── migrations/
└── seeds/
```

Create:

```text
database/migrations/001_foundation.sql
database/migrations/002_indexes.sql

database/seeds/001_permissions.sql
database/seeds/002_system_roles.sql
database/seeds/003_demo_organization.sql
```

Backend:

```text
apps/api/app/db/
apps/api/app/models/
```

Tests:

```text
tests/integration/
tests/database/
```

## Database

Implement:

* UUID generation
* Organizations
* Users
* Organization memberships
* Employees
* Roles
* Permissions
* Role permissions
* Membership roles
* Mine sites
* User site assignments

## Rules

Use:

```text
UUID
TIMESTAMPTZ
NUMERIC
FOREIGN KEY
CHECK
UNIQUE
INDEX
```

## Tests

Verify:

* Empty database migration
* Repeat migration safely
* Foreign keys
* Unique constraints
* Invalid records rejected

---

# 9. Phase 02 — Identity & RBAC

## Objective

Implement authentication and authorization.

## Bash Setup

Create:

```text
apps/api/app/auth/
apps/api/app/authorization/
apps/web/src/auth/
apps/web/src/components/auth/
tests/security/
tests/e2e/
```

## Backend

Implement:

* Registration
* Invitation
* Login
* Logout
* Session/token handling
* Password hashing
* Current-user endpoint
* Organization membership
* Role authorization
* Permission authorization
* Site authorization

## Permissions

```text
organization.read
organization.manage
user.read
user.manage
role.read
role.manage
mine_site.read
mine_site.manage
mineral.read
mineral.manage
material.read
material.manage
production.read
production.create
production.approve
inventory.read
inventory.post
inventory.adjust
weighbridge.read
weighbridge.create
weighbridge.approve
report.read
report.export
audit.read
```

## Security Tests

Verify:

* Authorized user
* Unauthorized user
* Wrong organization
* Wrong site
* Inactive user
* Inactive membership

---

# 10. Phase 03 — Organizations & Mine Sites

## Objective

Manage organizations, mine sites and employees.

## Bash Setup

```text
apps/api/app/organization/
apps/api/app/employees/
apps/api/app/mine_sites/

apps/web/src/features/organization/
apps/web/src/features/mine-sites/
apps/web/src/features/employees/
```

## Features

* Organization profile
* Mine site CRUD
* Site status
* Site location
* Employees
* Departments
* Job titles
* Site assignments
* Employee dashboards

## Acceptance

```text
Create Organization
        ↓
Create Mine Site
        ↓
Create Employee
        ↓
Assign User
        ↓
Assign Site
```

All operations must respect tenant isolation.

---

# 11. Phase 04 — Mining Master Data

## Objective

Create reusable mining reference data.

## Bash Setup

```text
apps/api/app/minerals/
apps/api/app/materials/
apps/api/app/deposits/
apps/api/app/pits/
apps/api/app/shifts/

apps/web/src/features/minerals/
apps/web/src/features/materials/
apps/web/src/features/deposits/
apps/web/src/features/pits/
apps/web/src/features/shifts/
```

## Data

* Minerals
* Materials
* Material types
* Units
* Deposits
* Pits
* Shifts

## Rules

Validate:

* Organization ownership
* Site ownership
* Status
* Codes
* Unique identifiers

---

# 12. Phase 05 — Mining Operations

## Objective

Track mining activities.

## Bash Setup

```text
apps/api/app/mining/
apps/web/src/features/mining/
tests/mining/
```

## Operation

Include:

* Operation number
* Pit
* Shift
* Material
* Date
* Quantity
* Operator
* Equipment
* Notes

## Workflow

```text
Draft
  ↓
Recorded
  ↓
Approved
```

Cancellation must be controlled.

Approved records cannot be silently edited.

Every important operation must be auditable.

---

# 13. Phase 06 — Production & Stockpiles

## Objective

Track production and stockpile movements.

## Production

* Daily production
* Shift production
* Targets
* Material
* Grade
* Moisture

## Stockpile

* Location
* Material
* Capacity
* Movements

Stockpile quantity must not be directly edited.

Use movement records:

```text
Opening
   ↓
Production
   ↓
Transfer
   ↓
Processing
   ↓
Shipment
```

All movements must be auditable.

---

# 14. Phase 07 — Inventory Ledger

## Objective

Create an immutable inventory transaction system.

## Inventory Transactions

Support:

```text
RECEIVE
ISSUE
TRANSFER
ADJUSTMENT
PROCESSING_INPUT
PROCESSING_OUTPUT
SHIPMENT_ISSUE
OPENING_BALANCE
```

Every transaction must include:

```text
organization
material
quantity
unit
source
destination
transaction type
reference
user
timestamp
idempotency key
```

Never implement:

```text
UPDATE inventory SET quantity = ...
```

as the primary inventory mechanism.

Balances must be derived from ledger transactions.

## Tests

* Receipts
* Issues
* Transfers
* Adjustments
* Balance calculation
* Idempotency
* Reconciliation
* Rollback

---

# 15. Phase 08 — Weighbridge

## Objective

Implement truck weighing.

## Data

```text
Vehicles
Drivers
Customers
Weighbridges
Tickets
```

Calculations:

```text
Net = Gross - Tare
```

Support:

* Gross
* Tare
* Net
* Moisture
* Wet weight
* Dry weight
* Direction
* Ticket number
* Status
* Approval
* Reprint
* Search
* Daily totals

Finalized tickets must be protected from silent modification.

---

# 16. Phase 09 — Processing

## Objective

Track processing from input to output.

## Flow

```text
Stockpile
   ↓
Processing Batch
   ↓
Input
   ↓
Processing Stage
   ↓
Output
   ↓
Inventory
```

Track:

* Plants
* Batches
* Stages
* Inputs
* Outputs
* Recovery
* Losses
* Status
* Traceability

Processing inputs reduce inventory.

Processing outputs create inventory transactions.

---

# 17. Phase 10 — Equipment & Maintenance

## Objective

Manage mining equipment.

## Equipment

* Equipment registry
* Types
* Status
* Site
* Operating hours
* Fuel

## Maintenance

* Maintenance plans
* Work orders
* Maintenance records
* Parts
* Costs

Equipment history must remain available when equipment moves between sites.

---

# 18. Phase 11 — Exploration & Geology

## Objective

Track exploration and geological information.

## Features

* Exploration projects
* Drill programs
* Drill holes
* Samples
* Geological observations
* Resource estimates
* Sampling locations

Sample provenance must be preserved.

---

# 19. Phase 12 — Laboratory

## Objective

Manage laboratory results.

## Features

* Laboratories
* Samples
* Assays
* Results
* Multi-element analysis
* QA/QC
* Standards
* Blanks
* Duplicates
* Reference materials
* Verification

Original laboratory results must never be silently overwritten.

---

# 20. Phase 13 — Logistics

## Objective

Manage material shipment and delivery.

## Flow

```text
Inventory
   ↓
Shipment
   ↓
Weighbridge
   ↓
Vehicle
   ↓
Driver
   ↓
Destination
   ↓
Customer
```

Shipment quantity cannot exceed available inventory.

---

# 21. Phase 14 — Sales & Finance

## Objective

Add operational sales and financial tracking.

## Features

* Customers
* Sales orders
* Sales lines
* Pricing
* Currency
* Exchange rates
* Revenue
* Expenses
* Categories
* Approvals
* Reports

Sales must remain traceable to shipments.

This phase is operational mining finance, not a complete ERP unless separately requested.

---

# 22. Phase 15 — Safety & Environment

## Safety

Track:

* Incidents
* Severity
* People
* Inspections
* Corrective actions

## Environment

Track:

* Environmental locations
* Measurements
* Parameters
* Limits
* Regulatory references

Historical measurements must remain immutable.

---

# 23. Phase 16 — Compliance

## Objective

Manage licenses, permits and regulatory requirements.

Track:

* Licenses
* Permits
* Jurisdictions
* Regulatory references
* Expiration
* Status
* Documents
* Reminders

Implement notifications for approaching expiration.

All compliance changes must be auditable.

---

# 24. Phase 17 — Offline & Synchronization

## Objective

Provide field-operation resilience.

## Frontend

Create:

```text
IndexedDB
Offline forms
Pending queue
Sync engine
Retry handling
Conflict handling
Device registration
Sync status
```

Initial offline domains:

* Mining operations
* Production
* Equipment
* Maintenance
* Samples
* Safety inspections

## Backend

Create synchronization APIs.

Use idempotency.

Never silently overwrite conflicts.

---

# 25. Phase 18 — Analytics & Reporting

## Objective

Build operational reporting.

## Dashboards

```text
Executive
Production
Stockpile
Processing
Equipment
Weighbridge
Inventory
Sales
HSE
```

## Exports

Support:

```text
PDF
CSV
Excel
```

Reports must contain:

* Reporting period
* Generation timestamp
* Source data context

KPIs must be calculated from verified transactional data.

Do not maintain manually entered KPI values.

---

# 26. Phase 19 — Security Hardening

## Objective

Perform a complete security review.

## Bash Verification

Run:

```bash
git status
```

```bash
docker compose config
```

```bash
./scripts/test.sh
```

Run backend tests:

```bash
pytest
```

Run frontend tests/build:

```bash
npm test
npm run build
```

## Security Tests

Verify:

* PostgreSQL RLS
* Organization isolation
* Site isolation
* Permission enforcement
* Authentication
* Session security
* Rate limiting
* Input validation
* SQL injection protection
* Audit logging
* Secret handling
* Backup/restore

Critical test:

```text
Organization A
       ↓
attempts access
       ↓
Organization B
       ↓
MUST FAIL
```

Critical/high findings must be fixed before proceeding.

---

# 27. Phase 20 — Production Release

## Objective

Prepare MineCore for production.

## Infrastructure

```text
infra/
├── docker/
├── nginx/
├── postgres/
└── monitoring/
```

## Scripts

Create:

```text
scripts/
├── deploy.sh
├── backup.sh
├── restore.sh
├── health-check.sh
├── migrate-production.sh
└── rollback.sh
```

## Production Requirements

* Production Docker configuration
* Database backups
* Restore testing
* Monitoring
* Logging
* Health checks
* Error tracking
* HTTPS
* Secrets management
* Database migrations
* Rollback procedure
* Deployment documentation
* Disaster recovery

Do not declare production-ready if critical requirements remain incomplete.

---

# 28. Standard Coding-Agent Prompt

For every phase, adapt this prompt.

```text
You are the senior engineer implementing MineCore.

WORKING DIRECTORY:
/home/ogwu/workspace/minecore

IMPORTANT:
The MineCore README and development roadmap are authoritative.

PHASE:
[INSERT PHASE NUMBER AND NAME]

You must implement ONLY this phase.

Do not implement future phases.

Before changing anything:

1. Inspect the repository.
2. Inspect README.md.
3. Inspect docs/development-roadmap.md.
4. Inspect existing migrations.
5. Inspect existing database models.
6. Inspect existing API routes.
7. Inspect frontend structure.
8. Inspect tests.
9. Inspect configuration.
10. Inspect git status.

Do not recreate working files.

Do not overwrite working implementations unnecessarily.

Do not invent database tables that contradict the approved schema.

Do not duplicate existing business logic.

Follow the existing architecture.

IMPLEMENTATION REQUIREMENTS:

- Database changes required by this phase
- Backend/API
- Domain/service logic
- Authorization
- Validation
- Frontend
- Tests
- Auditability
- Documentation

SECURITY:

- Organization isolation is mandatory.
- Site isolation is mandatory where applicable.
- Authorization must be enforced server-side.
- Never trust frontend permissions.
- Validate organization ownership.
- Validate site ownership.
- Protect finalized records.
- Preserve audit history.

DATABASE:

- UUID primary keys
- UTC timestamps
- Foreign keys
- CHECK constraints
- UNIQUE constraints
- Indexes
- Transactions
- Appropriate NUMERIC types
- RLS where required

TESTING:

Run all relevant tests.

Also run:

- Backend tests
- Frontend tests
- Typecheck
- Lint
- Build
- Database validation
- Security tests

Fix failures instead of hiding them.

Do not modify tests merely to make failing behavior pass unless the test itself is demonstrably incorrect.

FINAL REPORT:

IMPLEMENTED

FILES CREATED

FILES MODIFIED

DATABASE CHANGES

API CHANGES

FRONTEND CHANGES

AUTHORIZATION CHANGES

TESTS

SECURITY REVIEW

DOCUMENTATION

TODO REMAINING

BLOCKERS

PHASE STATUS: PASS / FAIL / BLOCKED
```

---

# 29. Standard Bash Phase Script

Each phase may have a script:

```text
scripts/phase-XX.sh
```

Example:

```bash
#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=========================================="
echo " MineCore Phase XX Setup"
echo "=========================================="

create_dir() {
    local dir="$1"

    if [[ -d "$dir" ]]; then
        echo "SKIP   $dir"
    else
        mkdir -p "$dir"
        echo "CREATE $dir"
    fi
}

create_file() {
    local file="$1"

    if [[ -e "$file" ]]; then
        echo "SKIP   $file"
    else
        mkdir -p "$(dirname "$file")"
        touch "$file"
        echo "CREATE $file"
    fi
}

# Add ONLY directories required by the current phase.

# Example:
# create_dir "$PROJECT_ROOT/apps/api/app/example"
# create_dir "$PROJECT_ROOT/apps/web/src/features/example"
# create_dir "$PROJECT_ROOT/tests/example"

echo
echo "Phase setup complete."
echo
echo "Project root:"
echo "  $PROJECT_ROOT"
echo
echo "Next:"
echo "  Inspect the repository."
echo "  Run the coding-agent implementation prompt."
echo "  Run tests."
```

---

# 30. Standard Verification Script

A phase verification script can use:

```bash
#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

echo "=========================================="
echo " MineCore Verification"
echo "=========================================="

echo
echo "== Git status =="
git status --short

echo
echo "== Repository structure =="
find . \
    -path './.git' -prune -o \
    -path './node_modules' -prune -o \
    -path './.venv' -prune -o \
    -type f -print | sort

echo
echo "== Docker configuration =="
docker compose config

echo
echo "== Backend tests =="
if [[ -d apps/api ]]; then
    (
        cd apps/api
        pytest
    )
fi

echo
echo "== Frontend tests =="
if [[ -f apps/web/package.json ]]; then
    (
        cd apps/web
        npm test -- --run
    )
fi

echo
echo "Verification commands completed."
```

The verification script must be adapted to the actual project configuration rather than assuming commands that do not exist.

---

# 31. Standard Phase Verification Prompt

```text
You are verifying a MineCore development phase.

WORKING DIRECTORY:
/home/ogwu/workspace/minecore

PHASE:
[INSERT PHASE]

Do NOT implement new features.

Your job is verification only.

Inspect:

1. README.md
2. docs/development-roadmap.md
3. Phase TODO
4. Database migrations
5. Models
6. API routes
7. Services
8. Frontend
9. Authorization
10. Tests
11. Documentation
12. Git status

Run all appropriate:

- Database checks
- Migration checks
- Backend tests
- Frontend tests
- Typecheck
- Lint
- Build
- Security tests
- Integration tests

Verify:

- Organization isolation
- Site isolation
- Authorization
- Validation
- Transactions
- Auditability
- Database integrity
- API contracts
- Frontend behavior
- Error handling

Do not hide failures.

Do not modify implementation.

REPORT:

COMPLETED

INCOMPLETE

FAILING TESTS

DATABASE

BACKEND

FRONTEND

AUTHORIZATION

SECURITY

AUDITABILITY

DOCUMENTATION

BLOCKERS

PHASE STATUS: PASS / FAIL / BLOCKED
```

---

# 32. Phase Gate

Never automatically move to the next phase.

The current phase must satisfy:

```text
Database
   +
Backend
   +
Authorization
   +
Frontend
   +
Validation
   +
Tests
   +
Auditability
   +
Documentation
```

Then:

```text
PASS
```

Only after PASS:

```text
Phase N
   ↓
Phase N+1
```

If:

```text
FAIL
```

remain in the current phase.

If:

```text
BLOCKED
```

document the blocker before proceeding.

---

# 33. Master Phase Tracker

| Phase | Name                      | Status      |
| ----: | ------------------------- | ----------- |
|    00 | Project Foundation        | NOT STARTED |
|    01 | Database Foundation       | NOT STARTED |
|    02 | Identity & RBAC           | NOT STARTED |
|    03 | Organization & Mine Sites | NOT STARTED |
|    04 | Mining Master Data        | NOT STARTED |
|    05 | Mining Operations         | NOT STARTED |
|    06 | Production & Stockpiles   | NOT STARTED |
|    07 | Inventory Ledger          | NOT STARTED |
|    08 | Weighbridge               | NOT STARTED |
|    09 | Processing                | NOT STARTED |
|    10 | Equipment & Maintenance   | NOT STARTED |
|    11 | Exploration & Geology     | NOT STARTED |
|    12 | Laboratory                | NOT STARTED |
|    13 | Logistics                 | NOT STARTED |
|    14 | Sales & Finance           | NOT STARTED |
|    15 | Safety & Environment      | NOT STARTED |
|    16 | Compliance                | NOT STARTED |
|    17 | Offline & Synchronization | NOT STARTED |
|    18 | Analytics & Reporting     | NOT STARTED |
|    19 | Security Hardening        | NOT STARTED |
|    20 | Production Release        | NOT STARTED |

---

# 34. Recommended Repository Growth

Do not create the entire final repository on day one.

Phase 00 should remain small.

Later phases introduce their own modules.

For example:

```text
Phase 00
apps/
database/
docs/
scripts/
```

Then Phase 01 introduces:

```text
database/migrations/
database/seeds/
apps/api/app/db/
apps/api/app/models/
tests/
```

Phase 02 introduces:

```text
apps/api/app/auth/
apps/api/app/authorization/
apps/web/src/auth/
```

Phase 05 introduces:

```text
apps/api/app/mining/
apps/web/src/features/mining/
```

Phase 07 introduces:

```text
apps/api/app/inventory/
apps/web/src/features/inventory/
```

This keeps the repository understandable and prevents hundreds of empty files from being created before they are needed.

---

# 35. Daily Development Workflow

## Start

```bash
cd /home/ogwu/workspace/minecore
git status
```

## Inspect

```bash
find . \
  -path './.git' -prune -o \
  -path './node_modules' -prune -o \
  -path './.venv' -prune -o \
  -type f -print | sort
```

## Start infrastructure

```bash
docker compose up -d
```

## Check services

```bash
docker compose ps
```

## Run phase setup

```bash
./scripts/phase-XX.sh
```

## Implement

Use the coding agent with the phase-specific implementation prompt.

## Test

```bash
./scripts/test.sh
```

## Review

```bash
git status
git diff --stat
```

## Verify

Use the phase verification prompt.

## Commit only after verification

```bash
git add .
git status
git commit -m "phase XX: implement <phase name>"
```

---

# 36. Critical Engineering Rules

Never:

```text
Trust frontend authorization
Bypass tenant isolation
Modify finalized records silently
Delete audit history
Hard-code secrets
Store inventory as mutable quantity only
Duplicate backend business rules in React
Skip database constraints
Skip tests
Ignore failed tests
Invent schema
Change API contracts silently
Implement future phases early
```

Always:

```text
Inspect first
Plan first
Use Bash for deterministic setup
Use coding agent for implementation
Validate server-side
Use database constraints
Use transactions
Audit important changes
Test security boundaries
Verify before marking complete
```

---

# 37. Final Definition of Done

MineCore is complete only when the relevant phase has:

```text
[ ] Database
[ ] Backend
[ ] Authorization
[ ] Frontend
[ ] Validation
[ ] Tests
[ ] Auditability
[ ] Documentation
[ ] Security review
[ ] Verification
```

The final production release additionally requires:

```text
[ ] Deployment
[ ] Backups
[ ] Restore testing
[ ] Monitoring
[ ] Logging
[ ] HTTPS
[ ] Secrets management
[ ] Migration strategy
[ ] Rollback strategy
[ ] Disaster recovery
[ ] Production readiness audit
```

**No phase is complete merely because code was written.**

A phase is complete only after it has been implemented, tested, reviewed, documented, and verified.
