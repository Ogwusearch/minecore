"""MineCore API application entrypoint.

Feature routers are imported dynamically. Missing modules are skipped so
the app still boots on partial checkouts, and each phase adds its own
module to `_FEATURE_MODULES` without touching anything else.
"""
from __future__ import annotations

import importlib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import configure_logging
from app.health.routes import router as health_router

configure_logging()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    debug=settings.app_debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health is always mounted.
app.include_router(health_router)

# Feature routers — added phase by phase. Names must match a package
# under app/ that exposes a `router` in its `routes.py`.
_FEATURE_MODULES = (
    "auth",
    "organizations",
    "employees",
    "mine_sites",
    "units",
    "minerals",
    "material_types",
    "materials",
    "deposits",
    "pits",
    "shifts",
)

for _name in _FEATURE_MODULES:
    try:
        _mod = importlib.import_module(f"app.{_name}.routes")
    except ModuleNotFoundError:
        continue
    _router = getattr(_mod, "router", None)
    if _router is not None:
        app.include_router(_router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": settings.app_name,
        "env": settings.app_env,
        "status": "ok",
    }
