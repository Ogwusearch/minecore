"""MineCore API application entrypoint.

Feature routers are imported dynamically from `_FEATURE_MODULES`. Every
mounted or skipped router is logged so a bad import is never invisible.
"""
from __future__ import annotations

import importlib
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import configure_logging
from app.health.routes import router as health_router

configure_logging()
logger = logging.getLogger("minecore.main")

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

app.include_router(health_router)
logger.info("Mounted /health")

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
    "mining",
)

for _name in _FEATURE_MODULES:
    try:
        _mod = importlib.import_module(f"app.{_name}.routes")
    except ModuleNotFoundError as exc:
        # Only skip when the feature itself is absent. If a *dependency*
        # of the feature is missing, that is a real error and must not be
        # hidden.
        missing = getattr(exc, "name", "") or ""
        if missing.startswith(f"app.{_name}"):
            logger.info("Feature '%s' not present — skipping", _name)
            continue
        logger.exception("Feature '%s' import failed (missing: %s)", _name, missing)
        raise
    except Exception:
        logger.exception("Feature '%s' failed to import", _name)
        raise

    _router = getattr(_mod, "router", None)
    if _router is None:
        logger.warning("Feature '%s' has no `router` attribute — skipping", _name)
        continue

    app.include_router(_router)
    logger.info("Mounted feature router '%s'", _name)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": settings.app_name,
        "env": settings.app_env,
        "status": "ok",
    }
