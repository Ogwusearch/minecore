"""Temporary authentication shim.

################################################################
# PHASE 02 WILL REPLACE THIS FILE.                              #
#                                                               #
# Real authentication (JWT, login, sessions, password hashing)  #
# is Phase 02. Until then, every request must carry two headers:#
#                                                               #
#     X-User-Id:         <uuid of the acting user>              #
#     X-Organization-Id: <uuid of the active organization>      #
#                                                               #
# The public surface of this module — ``CurrentUser`` and       #
# ``get_current_user`` — is the contract Phase 02 will honour.  #
# Do not invent new auth entrypoints in domain modules.         #
################################################################
"""
from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from fastapi import Header


@dataclass(frozen=True)
class CurrentUser:
    """Identity of the acting user within an active organization."""

    user_id: UUID
    organization_id: UUID


async def get_current_user(
    x_user_id: UUID = Header(..., description="Acting user UUID (Phase 02 placeholder)"),
    x_organization_id: UUID = Header(
        ..., description="Active organization UUID (Phase 02 placeholder)"
    ),
) -> CurrentUser:
    return CurrentUser(user_id=x_user_id, organization_id=x_organization_id)
