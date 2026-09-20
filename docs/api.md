# MineCore API

## Framework

FastAPI. Base application entrypoint: apps/api/app/main.py

## Conventions

- JSON request/response bodies
- Pydantic schemas at the boundary
- Domain services hold business logic
- Repositories hold persistence logic
- Authorization enforced per route via dependencies

## Health

    GET /health
    GET /

## Versioning

The API starts unversioned. Once the first external consumer exists,
introduce /v1 prefix without breaking existing routes.

## Error Format

    {
      "detail": "human-readable message",
      "code": "MACHINE_READABLE_CODE"
    }

## Authorization

Every protected route depends on:

    current_user
        +
    organization context
        +
    required permission
        +
    site scope (when applicable)

Frontend permissions are for UX only.
