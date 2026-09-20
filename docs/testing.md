# MineCore Testing

## Backend

- Framework: pytest
- Config: apps/api/pyproject.toml
- Location: apps/api/tests
- Run: make test

## Frontend

- Framework: vitest
- Config: apps/web/vite.config.js
- Run: make test

## Security

Dedicated tests under tests/security (Phase 19) exercise:

- authentication
- authorization
- tenant isolation
- site isolation
- permission escalation
- audit integrity

## Integration

Full-domain integration tests live under tests/integration and are
added incrementally, phase by phase.

## Rule

A feature is not complete until its tests exist and pass.
